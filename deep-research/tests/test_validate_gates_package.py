"""Tests for validate.py, gates.py, package.py — output verification,
arithmetic gates, and the handoff package contract."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
from validate import validate as validate_report  # noqa: E402
from gates import evaluate as eval_gates  # noqa: E402
from package import build, verify  # noqa: E402
from dr_core import scan_secrets, redact_secrets  # noqa: E402

GOOD_REPORT = """# Summary

answer status: partially-answered

## Findings

Postgres shows serializable isolation [docs](https://www.postgresql.org/docs/current/transaction-iso.html).
CRDTs claim convergence [paper](https://arxiv.org/abs/2011.02341).

## Method

Ledgered evidence from two independent sources CL-A1, CL-B2.

## Claim matrix

| Claim | Status | Evidence |
|---|---|---|
| Serializability exists | established | E0001 |
| CRDT convergence | likely | E0002 |

## Gaps

- vendor benchmarks were not independently verified

## Limitations

- paywalled sources excluded

## Sources

- [PostgreSQL docs](https://www.postgresql.org/docs/current/transaction-iso.html)
- [CRDT paper](https://arxiv.org/abs/2011.02341)
"""


@pytest.fixture()
def report(tmp_path):
    p = tmp_path / "report.md"
    p.write_text(GOOD_REPORT, encoding="utf-8")
    return p


@pytest.fixture()
def run_dir(tmp_path):
    d = tmp_path / "run"
    d.mkdir()
    (d / "metadata.json").write_text(json.dumps({
        "question": "q", "mode": "quick",
        "budget": {"max_hops": 4, "min_sources": 2, "min_source_classes": 2}}))
    (d / "hops.jsonl").write_text(
        '{"hop_id": "H0001", "mode": "contradict", "status": "done", "parent": null}\n'
        '{"hop_id": "H0002", "mode": "contradict", "status": "done", "parent": null}\n'
        '{"hop_id": "H0003", "mode": "contradict", "status": "done", "parent": null}\n')
    (d / "sources.jsonl").write_text(
        '{"source_id": "S0001", "url": "https://pg.org", "independence_family": "pg.org", "source_type": "primary"}\n'
        '{"source_id": "S0002", "url": "https://arxiv.org", "independence_family": "arxiv.org", "source_type": "primary"}\n'
        '{"source_id": "S0003", "url": "https://blog.io", "independence_family": "blog.io", "source_type": "secondary"}\n'
        '{"source_id": "S0004", "url": "https://news.com", "independence_family": "news.com", "source_type": "aggregator"}\n')
    (d / "evidence.jsonl").write_text(
        '{"evidence_id": "E0001", "claim_id": "CL-A1", "claim": "c1", "source_id": "S0001", "stance": "supports", "importance": 5}\n'
        '{"evidence_id": "E0002", "claim_id": "CL-B2", "claim": "c2", "source_id": "S0002", "stance": "contradicts", "importance": 5}\n'
        '{"evidence_id": "E0003", "claim_id": "CL-A1", "claim": "c1 counter", "source_id": "S0003", "stance": "contradicts", "importance": 5}\n'
        '{"evidence_id": "E0004", "claim_id": "CL-C3", "claim": "c3", "source_id": "S0004", "stance": "supports", "importance": 2}\n')
    (d / "conflicts.jsonl").write_text("")
    return d


class TestValidateReport:
    def test_good_report_passes(self, report):
        result = validate_report(report, mode="deep")
        failed = [c for c in result["checks"] if c["status"] == "FAIL"]
        assert not failed, failed

    def test_missing_report(self, tmp_path):
        result = validate_report(tmp_path / "nope.md")
        assert result["pass"] is False

    def test_no_citations_fails(self, tmp_path):
        p = tmp_path / "r.md"
        p.write_text("# Summary\n\nWords with no citations at all. " * 30)
        result = validate_report(p, mode="quick")
        assert any(c["check"] == "citation-density" and c["status"] == "FAIL"
                   for c in result["checks"])

    def test_fabricated_urls_flagged(self, tmp_path):
        p = tmp_path / "r.md"
        p.write_text("# Findings\n\nSee [docs](http://example.com/x) "
                     "and [doi](https://doi.org/10.TODO/xyz).\n\n## Sources\n\n")
        result = validate_report(p, mode="quick")
        assert any(c["check"] == "no-fabricated-urls" and c["status"] == "FAIL"
                   for c in result["checks"])

    def test_answer_status_required(self, tmp_path):
        p = tmp_path / "r.md"
        p.write_text("# Findings\n\nx [y](https://a.com)\n\n## Sources\n\n")
        result = validate_report(p, mode="quick")
        assert any(c["check"] == "answer-status-declared" and c["status"] == "FAIL"
                   for c in result["checks"])

    def test_overclaim_language_flagged(self, tmp_path):
        p = tmp_path / "r.md"
        p.write_text("# Findings\n\nThis definitely proves everything "
                     "[s](https://a.com).\n\n## Sources\n\n")
        result = validate_report(p, mode="quick")
        assert any(c["check"] == "calibrated-language" and c["status"] == "FAIL"
                   for c in result["checks"])

    def test_ledger_cross_reference(self, report, run_dir):
        # report references CL-A1 and CL-B2 — both in ledger
        result = validate_report(report, run_dir=run_dir, mode="deep")
        xr = [c for c in result["checks"] if c["check"].startswith(("ledger", "report", "high", "unsupported"))]
        assert all(c["status"] == "pass" for c in xr), xr

    def test_report_cites_unknown_claim(self, tmp_path):
        p = tmp_path / "r.md"
        p.write_text("# Findings\n\nCL-DEADBEEF says hi [s](https://a.com).\n\n## Sources\n\n")
        result = validate_report(p, run_dir=tmp_path, mode="quick")
        assert any("report-claims-in-ledger" == c["check"] and c["status"] == "FAIL"
                   for c in result["checks"])

    def test_missing_hi_claims_in_report(self, report, tmp_path):
        d = tmp_path / "run"
        d.mkdir()
        (d / "evidence.jsonl").write_text(
            '{"evidence_id": "E0001", "claim_id": "CL-ZZZ", "claim": "dropped", "source_id": "S0001", "importance": 5, "stance": "supports"}\n')
        result = validate_report(report, run_dir=d, mode="quick")
        assert any(c["check"] == "ledger-claims-in-report" and c["status"] == "FAIL"
                   for c in result["checks"])


class TestResearchGates:
    def test_failing_gates_on_sparse_run(self, tmp_path):
        d = tmp_path / "sparse"
        d.mkdir()
        (d / "metadata.json").write_text(json.dumps({"question": "q", "mode": "standard"}))
        for name in ("sources.jsonl", "hops.jsonl", "evidence.jsonl", "conflicts.jsonl"):
            (d / name).write_text("")
        result = eval_gates(d)
        assert result["pass"] is False
        assert result["gates"]["sources-count"]["pass"] is False

    def test_passing_gates_on_rich_run(self, run_dir):
        result = eval_gates(run_dir)
        failures = {k: v for k, v in result["gates"].items() if not v["pass"]}
        assert not failures, failures

    def test_class_diversity_gate(self, run_dir):
        # collapse all sources to one class
        srcs = []
        for line in (run_dir / "sources.jsonl").read_text().splitlines():
            rec = json.loads(line)
            rec["source_type"] = "secondary"
            srcs.append(rec)
        (run_dir / "sources.jsonl").write_text(
            "\n".join(json.dumps(s) for s in srcs) + "\n")
        result = eval_gates(run_dir)
        assert result["gates"]["source-class-diversity"]["pass"] is False

    def test_counterevidence_gate(self, run_dir):
        # make all evidence supportive: high-importance claims unchallenged
        evs = []
        for line in (run_dir / "evidence.jsonl").read_text().splitlines():
            rec = json.loads(line)
            rec["stance"] = "supports"
            evs.append(rec)
        (run_dir / "evidence.jsonl").write_text(
            "\n".join(json.dumps(e) for e in evs) + "\n")
        result = eval_gates(run_dir)
        assert result["gates"]["counterevidence-searched"]["pass"] is False


class TestPackage:
    def test_build_and_verify(self, run_dir):
        pkg = build(run_dir, "partially-answered",
                    gaps=["vendor benchmarks unverified"],
                    limitations=["paywalls excluded"])
        errors, warnings = verify(pkg)
        assert not errors, errors
        assert pkg["schema"] == "deep-research-package/1"
        assert pkg["answer_status"] == "partially-answered"
        assert len(pkg["claims"]) == 3
        assert pkg["claims"][0]["importance"] >= pkg["claims"][1]["importance"]

    def test_verify_bad_status(self, run_dir):
        pkg = build(run_dir, "partially-answered", [], [])
        pkg["answer_status"] = "maybe"
        errors, _ = verify(pkg)
        assert any("answer_status" in e for e in errors)

    def test_verify_unknown_source(self, run_dir):
        pkg = build(run_dir, "fully-answered", [], [])
        pkg["claims"][0]["source_ids"] = ["S9999"]
        errors, _ = verify(pkg)
        assert any("S9999" in e for e in errors)

    def test_verify_secret_fails_closed(self, run_dir):
        pkg = build(run_dir, "fully-answered", [], [])
        pkg["sources"].append({
            "source_id": "S0999", "url": "https://x.com?t=ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456",
            "title": "leaky"})
        errors, _ = verify(pkg)
        assert any("secret" in e.lower() for e in errors)

    def test_cli_build(self, run_dir):
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "package.py"), "build", str(run_dir),
             "--answer-status", "fully-answered", "--gap", "g1", "--limitation", "l1"],
            capture_output=True, text=True)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        out = json.loads((run_dir / "package.json").read_text())
        assert out["gaps"] == ["g1"]


class TestSecretTooling:
    def test_scan_patterns(self):
        assert scan_secrets("token = ghp_" + "A" * 36)
        assert scan_secrets("Authorization: Bearer abcdefghijklmnopqrstuvwxyz123456")
        assert not scan_secrets("normal text with the word password only")

    def test_redact(self):
        red = redact_secrets("key: sk-" + "B" * 40)
        assert "sk-" not in red and "[REDACTED]" in red
