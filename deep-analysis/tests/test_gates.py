"""Tests for the deep-analysis artifact gates."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
from analysis_gates import evaluate as eval_gates  # noqa: E402


@pytest.fixture()
def good_run(tmp_path):
    d = tmp_path / "analysis"
    d.mkdir()
    (d / "analysis-plan.md").write_text(
        "# Problem Framing\n\nWhy does the payment service fail at month-end?\n\n"
        "# Evaluation Criteria (pre-committed)\n\n"
        "- explains the April 30 incident timeline\n"
        "- discriminates between load and race-condition hypotheses\n\n"
        "# Scope\n\nPayment service only; excludes fraud module.\n\n"
        "# Assumptions and Blind Spots\n\n- what we haven't considered: single-region dependency\n",
        encoding="utf-8")
    (d / "assumptions.md").write_text(
        "| Assumption | Status | Note |\n|---|---|---|\n"
        "| DB is the bottleneck | validate | check slow query log |\n"
        "| Deploy at 23:50 caused it | discard | timeline mismatch |\n"
        "| Lock contention | unresolved | need trace data |\n",
        encoding="utf-8")
    (d / "hypotheses.md").write_text(
        "| Hypothesis | Status | Discriminating evidence |\n|---|---|---|\n"
        "| Lock contention at month-end close | confirmed | deadlock traces 23:58-00:02 |\n"
        "| Traffic spike from retry storm | eliminated | request rate flat in APM |\n"
        "| Clock skew across nodes | unresolved | NTP logs unavailable |\n",
        encoding="utf-8")
    (d / "decision-matrix.md").write_text(
        "| Option | Cost | Risk | Reversibility |\n|---|---|---|---|\n"
        "| Fix lock ordering | 3 dev-days | low | reversible |\n"
        "| Queue the close job | 1 dev-day | medium | reversible |\n"
        "| Weight | 0.5 | 0.3 | 0.2 |\n\n"
        "Verdict: queue the close job first, then fix lock ordering.\n",
        encoding="utf-8")
    (d / "failure-modes.md").write_text(
        "| Failure mode | Severity | Likelihood | Mitigation |\n|---|---|---|---|\n"
        "| Queue backlog delays payouts | high | medium | idempotent retry + alert |\n",
        encoding="utf-8")
    (d / "review-log.md").write_text(
        "# Adversarial Review\n\n"
        "Round: 2\n\n"
        "F1 The queue option still requires the lock to be taken during reconciliation "
        "- accepted: yes - added to failure modes.\n"
        "F2 Claim that traffic was flat assumes APM sampled correctly - rejected: "
        "APM sampling audit exists, see TRACE-917; not a real risk.\n\n"
        "Verdict: approved\n",
        encoding="utf-8")
    (d / "research-request.json").write_text(json.dumps({
        "schema": "deep-analysis-request/1",
        "requests": [{
            "question": "What is the lock-ordering contract in ledger service v3?",
            "why_needed": "F1 cannot be dispositioned without it",
            "decision_at_stake": "queue vs fix-lock ordering",
        }],
    }))
    return d


class TestFullPass:
    def test_good_run_passes(self, good_run):
        result = eval_gates(good_run)
        assert result["pass"] is True, result["gates"]

    def test_gate_names(self, good_run):
        result = eval_gates(good_run)
        assert set(result["gates"]) == {
            "framing", "assumptions", "hypotheses", "decision-matrix",
            "failure-modes", "review-log", "research-request"}


class TestFramingGate:
    def test_missing_plan(self, tmp_path):
        result = eval_gates(tmp_path)
        assert any("analysis-plan.md missing" in v for v in result["gates"]["framing"])

    def test_no_precommitted_criteria(self, tmp_path):
        d = tmp_path / "a"; d.mkdir()
        (d / "analysis-plan.md").write_text("# Problem\n\nx\n\n# Scope\n\ny\n\n# Risks\n\nz\n")
        result = eval_gates(d)
        assert any("pre-commit" in v for v in result["gates"]["framing"])


class TestAssumptionsGate:
    def test_bad_disposition(self, good_run):
        p = good_run / "assumptions.md"
        p.write_text("| Assumption | Status |\n|---|---|\n| X | maybe |\n")
        result = eval_gates(good_run)
        assert any("not in" in v for v in result["gates"]["assumptions"])

    def test_missing_status_column(self, good_run):
        p = good_run / "assumptions.md"
        p.write_text("| A | B |\n|---|---|\n| x | y |\n")
        result = eval_gates(good_run)
        assert any("status/disposition column" in v for v in result["gates"]["assumptions"])


class TestHypothesesGate:
    def test_bad_status(self, good_run):
        p = good_run / "hypotheses.md"
        p.write_text("| Hypothesis | Status | Evidence |\n|---|---|---|\n| H1 | maybe | x |\n")
        result = eval_gates(good_run)
        assert any("status not in" in v for v in result["gates"]["hypotheses"])

    def test_unresolved_without_reason(self, good_run):
        p = good_run / "hypotheses.md"
        p.write_text(
            "| Hypothesis | Status | Discriminating evidence |\n|---|---|---|\n"
            "| H1 | unresolved |  |\n")
        result = eval_gates(good_run)
        assert any("no evidence/reason" in v for v in result["gates"]["hypotheses"])

    def test_empty_hypotheses_fails(self, good_run):
        (good_run / "hypotheses.md").unlink()
        result = eval_gates(good_run)
        assert result["pass"] is False


class TestDecisionMatrixGate:
    def test_ragged_rows(self, good_run):
        p = good_run / "decision-matrix.md"
        p.write_text("| Option | Cost | Risk |\n|---|---|---|\n| A | 1 | 2 | 3 |\n\nVerdict: A\n")
        result = eval_gates(good_run)
        assert any("ragged" in v for v in result["gates"]["decision-matrix"])

    def test_weights_must_sum(self, good_run):
        p = good_run / "decision-matrix.md"
        p.write_text("| Option | Cost | Risk |\n|---|---|---|\n| A | 1 | 2 |\n"
                     "| Weight | 0.7 | 0.6 |\n\nVerdict: A\n")
        result = eval_gates(good_run)
        assert any("weights sum" in v for v in result["gates"]["decision-matrix"])

    def test_verdict_required(self, good_run):
        p = good_run / "decision-matrix.md"
        p.write_text("| Option | Cost | Risk |\n|---|---|---|\n| A | 1 | 2 |\n| B | 2 | 1 |\n")
        result = eval_gates(good_run)
        assert any("verdict" in v for v in result["gates"]["decision-matrix"])

    def test_matrix_optional(self, good_run):
        (good_run / "decision-matrix.md").unlink()
        result = eval_gates(good_run)
        assert result["gates"]["decision-matrix"] == []


class TestReviewLogGate:
    def test_missing_log(self, good_run):
        (good_run / "review-log.md").unlink()
        result = eval_gates(good_run)
        assert result["pass"] is False

    def test_not_approved(self, good_run):
        p = good_run / "review-log.md"
        p.write_text("Round: 1\nF1 something - accepted: yes\n\nVerdict: revise\n")
        result = eval_gates(good_run)
        assert any("not APPROVED" in v for v in result["gates"]["review-log"])

    def test_round_cap(self, good_run):
        p = good_run / "review-log.md"
        p.write_text("Round: 7\n\nF1 x - accepted: yes\n\nVerdict: approved\n")
        result = eval_gates(good_run)
        assert any("round cap" in v for v in result["gates"]["review-log"])

    def test_undispositioned_finding(self, good_run):
        p = good_run / "review-log.md"
        p.write_text("Round: 1\n\nF3 was never dispositioned in this log.\n\nVerdict: approved\n")
        result = eval_gates(good_run)
        assert any("F3" in v for v in result["gates"]["review-log"])


class TestResearchRequestGate:
    def test_bad_schema(self, good_run):
        p = good_run / "research-request.json"
        p.write_text(json.dumps({"schema": "wrong/1", "requests": []}))
        result = eval_gates(good_run)
        assert any("deep-analysis-request/1" in v for v in result["gates"]["research-request"])

    def test_missing_fields(self, good_run):
        p = good_run / "research-request.json"
        p.write_text(json.dumps({
            "schema": "deep-analysis-request/1",
            "requests": [{"question": "q only"}]}))
        result = eval_gates(good_run)
        assert any("why_needed" in v for v in result["gates"]["research-request"])


class TestCLI:
    def test_cli_json(self, good_run):
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "analysis_gates.py"), str(good_run), "--json"],
            capture_output=True, text=True)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        data = json.loads(proc.stdout)
        assert data["pass"] is True
