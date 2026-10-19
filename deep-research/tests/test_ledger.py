"""Tests for ledger.py — the evidence-ledger state manager."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
LEDGER = [sys.executable, str(SCRIPTS / "ledger.py")]


def run(args, expect_ok=True):
    proc = subprocess.run(LEDGER + args, capture_output=True, text=True)
    if expect_ok:
        assert proc.returncode == 0, f"stderr: {proc.stderr}\nstdout: {proc.stdout}"
    return proc


@pytest.fixture()
def run_dir(tmp_path):
    d = tmp_path / "run"
    run(["init", str(d), "--question", "What makes distributed systems hard?",
         "--mode", "standard"])
    return d


class TestInit:
    def test_init_creates_artifacts(self, run_dir):
        for name in ("metadata.json", "plan.md", "sources.jsonl", "hops.jsonl",
                     "evidence.jsonl", "conflicts.jsonl"):
            assert (run_dir / name).exists(), name
        meta = json.loads((run_dir / "metadata.json").read_text())
        assert meta["mode"] == "standard"
        assert meta["budget"]["max_hops"] == 10
        assert meta["budget"]["min_sources"] == 5

    def test_init_refuses_nonempty(self, run_dir):
        proc = run(["init", str(run_dir), "--question", "x"], expect_ok=False)
        assert proc.returncode != 0
        assert "not empty" in proc.stderr

    def test_init_rejects_bad_mode(self, tmp_path):
        proc = run(["init", str(tmp_path / "r"), "--question", "q",
                    "--mode", "turbo"], expect_ok=False)
        assert proc.returncode != 0


class TestSources:
    def test_add_source_assigns_ids(self, run_dir):
        out = run(["add-source", str(run_dir), "--url", "https://a.com/x",
                   "--title", "A", "--source-type", "primary", "--quality", "5"])
        assert "S0001" in out.stdout
        out = run(["add-source", str(run_dir), "--url", "https://b.com/y",
                  "--title", "B"])
        assert "S0002" in out.stdout

    def test_duplicate_url_rejected(self, run_dir):
        run(["add-source", str(run_dir), "--url", "https://a.com/x", "--title", "A"])
        proc = run(["add-source", str(run_dir), "--url", "https://a.com/x",
                    "--title", "A again"], expect_ok=False)
        assert "duplicate" in proc.stderr

    def test_bad_type_rejected(self, run_dir):
        proc = run(["add-source", str(run_dir), "--url", "https://a.com",
                    "--title", "A", "--source-type", "gossip"], expect_ok=False)
        assert proc.returncode != 0


class TestHops:
    def test_hop_and_parent_validation(self, run_dir):
        run(["add-hop", str(run_dir), "--mode", "seed",
             "--description", "initial scan"])
        proc = run(["add-hop", str(run_dir), "--mode", "expand",
                    "--description", "x", "--parent", "H9999"], expect_ok=False)
        assert "does not exist" in proc.stderr
        out = run(["add-hop", str(run_dir), "--mode", "expand",
                   "--description", "ok", "--parent", "H0001"])
        assert "H0002" in out.stdout

    def test_hop_budget_enforced(self, tmp_path):
        d = tmp_path / "quick"
        run(["init", str(d), "--question", "q", "--mode", "quick",
             "--max-hops", "2"])
        run(["add-hop", str(d), "--mode", "seed", "--description", "1"])
        run(["add-hop", str(d), "--mode", "seed", "--description", "2"])
        proc = run(["add-hop", str(d), "--mode", "seed", "--description", "3"],
                   expect_ok=False)
        assert "budget" in proc.stderr
        run(["add-hop", str(d), "--mode", "seed", "--description", "forced",
             "--force"])
        assert len((d / "hops.jsonl").read_text().strip().splitlines()) == 3


class TestEvidence:
    def test_evidence_requires_source(self, run_dir):
        proc = run(["add-evidence", str(run_dir), "--source-id", "S9999",
                    "--claim", "c"], expect_ok=False)
        assert "not found" in proc.stderr

    def test_evidence_flow(self, run_dir):
        run(["add-source", str(run_dir), "--url", "https://a.com/x", "--title", "A"])
        out = run(["add-evidence", str(run_dir), "--source-id", "S0001",
                   "--claim", "Latency dominates failures",
                   "--importance", "4", "--quality", "4",
                   "--quote", "p. 42, table 3",
                   "--freshness", "current", "--independence", "independent",
                   "--uncertainty", "established"])
        assert "E0001" in out.stdout
        assert "CL-" in out.stdout

    def test_stance_enum(self, run_dir):
        run(["add-source", str(run_dir), "--url", "https://a.com", "--title", "A"])
        proc = run(["add-evidence", str(run_dir), "--source-id", "S0001",
                    "--claim", "x", "--stance", "refutes"], expect_ok=False)
        assert proc.returncode != 0


class TestConflicts:
    def test_conflict_requires_known_claims(self, run_dir):
        run(["add-source", str(run_dir), "--url", "https://a.com", "--title", "A"])
        run(["add-evidence", str(run_dir), "--source-id", "S0001",
             "--claim", "claim one", "--claim-id", "CL-1"])
        proc = run(["add-conflict", str(run_dir), "--claim-ids", "CL-1,CL-NOPE",
                   "--positions", "A | B"], expect_ok=False)
        assert "unknown claim" in proc.stderr

    def test_resolved_requires_resolution(self, run_dir):
        run(["add-source", str(run_dir), "--url", "https://a.com", "--title", "A"])
        run(["add-evidence", str(run_dir), "--source-id", "S0001",
             "--claim", "c1", "--claim-id", "CL-1"])
        proc = run(["add-conflict", str(run_dir), "--claim-ids", "CL-1",
                    "--positions", "A | B", "--status", "resolved"], expect_ok=False)
        assert "resolution" in proc.stderr
        out = run(["add-conflict", str(run_dir), "--claim-ids", "CL-1",
                   "--positions", "A | B", "--status", "resolved",
                   "--resolution", "A wins on primary evidence"])
        assert "C0001" in out.stdout


class TestLint:
    def _seed_run(self, d, with_contradiction=False, with_secret=False):
        run(["add-source", str(d), "--url", "https://a.com/paper", "--title",
             "Paper", "--source-type", "primary", "--quality", "5"])
        run(["add-source", str(d), "--url", "https://b.org/post", "--title",
             "Post", "--source-type", "secondary", "--quality", "4"])
        run(["add-evidence", str(d), "--source-id", "S0001",
             "--claim", "Strong claim", "--claim-id", "CL-A",
             "--importance", "5", "--quality", "5",
             "--quote", "section 4.1", "--freshness", "current",
             "--independence", "independent", "--uncertainty", "established"])
        if with_contradiction:
            run(["add-hop", str(d), "--mode", "contradict", "--description", "counter"])
            run(["add-evidence", str(d), "--source-id", "S0002",
                 "--claim", "Strong claim", "--claim-id", "CL-A",
                 "--stance", "contradicts", "--importance", "5",
                 "--quote", "section 9", "--freshness", "current"])
        if with_secret:
            run(["add-evidence", str(d), "--source-id", "S0002",
                 "--claim", "key = ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456",
                 "--claim-id", "CL-SECRET"])
        return d

    def test_lint_flags_unchallenged_high_importance(self, run_dir):
        self._seed_run(run_dir)
        proc = run(["lint", str(run_dir)], expect_ok=False)
        assert proc.returncode == 0  # warnings do not fail lint
        assert "counterevidence" in proc.stdout

    def test_lint_passes_when_challenged(self, run_dir):
        self._seed_run(run_dir, with_contradiction=True)
        proc = run(["lint", str(run_dir)])
        assert "0 error" in proc.stdout

    def test_lint_fails_on_secrets(self, run_dir):
        self._seed_run(run_dir, with_secret=True)
        proc = run(["lint", str(run_dir)], expect_ok=False)
        assert proc.returncode == 1
        assert "secret" in proc.stdout.lower()

    def test_lint_flags_unknown_source_reference(self, run_dir):
        run(["add-source", str(run_dir), "--url", "https://a.com", "--title", "A"])
        run(["add-evidence", str(run_dir), "--source-id", "S0001",
             "--claim", "c", "--claim-id", "CL-1"])
        # hand-tamper the record to reference a missing source
        p = run_dir / "evidence.jsonl"
        rec = json.loads(p.read_text().strip().splitlines()[0])
        rec["source_id"] = "S7777"
        p.write_text(json.dumps(rec) + "\n")
        proc = run(["lint", str(run_dir)], expect_ok=False)
        assert proc.returncode == 1
        assert "unknown source" in proc.stdout

    def test_lint_flags_duplicate_ids(self, run_dir):
        p = run_dir / "sources.jsonl"
        p.write_text('{"source_id": "S0001", "url": "https://a.com"}\n'
                     '{"source_id": "S0001", "url": "https://b.com"}\n')
        proc = run(["lint", str(run_dir)], expect_ok=False)
        assert "duplicate id" in proc.stdout

    def test_lint_flags_orphan_parent(self, run_dir):
        p = run_dir / "hops.jsonl"
        p.write_text('{"hop_id": "H0001", "mode": "expand", "status": "done",'
                     ' "parent": "H0404"}\n')
        proc = run(["lint", str(run_dir)], expect_ok=False)
        assert "parent" in proc.stdout


class TestStatusExport:
    def test_status_and_export(self, run_dir):
        run(["add-source", str(run_dir), "--url", "https://a.com", "--title", "A"])
        run(["add-evidence", str(run_dir), "--source-id", "S0001",
             "--claim", "c", "--claim-id", "CL-1", "--importance", "4"])
        out = run(["status", str(run_dir)])
        assert "sources=" in out.stdout and "claims=1" in out.stdout
        out = run(["export", str(run_dir)])
        data = json.loads(out.stdout)
        assert data["metadata"]["question"].startswith("What makes")
