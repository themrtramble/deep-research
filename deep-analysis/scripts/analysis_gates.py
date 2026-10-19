#!/usr/bin/env python3
"""gates.py — artifact validators for the Deep Analysis skill.

Mechanically validates the analysis artifacts against their contracts, in
the spirit of unlazy's CHECK/EXPECT/EVIDENCE gates (MIT, Leonxlnx) and
the bounded adversarial-review mechanics of chaseai-yt/claudex-loop
(ideas-only source):

  framing          — analysis-plan must frame the problem + pre-commit
                     evaluation criteria before conclusions
  assumptions      — every assumption row carries a disposition
                     (validate|keep|discard|unresolved)
  hypotheses       — every hypothesis row has a status
                     (confirmed|eliminated|unresolved) + discriminating
                     evidence or an explicit reason it is unresolved
  decision-matrix  — alternatives x criteria coverage; weights sum to 1;
                     no empty cells; a verdict exists
  failure-modes    — IF/THEN rows have severity, likelihood, and a
                     mitigation that exists
  review-log       — adversarial review has bounded rounds, vocabulary
                     verdicts (approved|revise|blocked), and every
                     finding is dispositioned (accepted/rejected + reason)
  research-request — handoff JSON to deep-research is well-formed

Exit 0 = all gates pass; exit 1 = violations printed.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DISPOSITIONS = ("validate", "keep", "discard", "unresolved")
HYP_STATUS = ("confirmed", "eliminated", "unresolved")
SEVERITY = ("low", "medium", "high", "critical")
REVIEW_VERDICTS = ("approved", "revise", "blocked")


def _rows(path: Path, section: str | None = None) -> list[list[str]]:
    """Parse markdown tables; optionally only under a heading containing *section*."""
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if section:
        m = re.search(rf"^#{1,6}[^\n]*{re.escape(section)}[^\n]*\n(.*?)(?=^#{1,6}\s|\Z)",
                      text, re.I | re.S | re.M)
        text = m.group(1) if m else ""
    rows: list[list[str]] = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                rows.append(cells)
    return rows


def gate_framing(run: Path) -> list[str]:
    plan = run / "analysis-plan.md"
    if not plan.exists():
        return ["analysis-plan.md missing — frame before analyzing"]
    text = plan.read_text(encoding="utf-8").lower()
    v = []
    if not re.search(r"^#+\s*(problem|question|objective|framing)", text, re.M):
        v.append("plan lacks a Problem/Question/Framing section")
    if not re.search(r"(evaluation|success)\s+criteria", text):
        v.append("plan does not pre-commit evaluation criteria — criteria must be fixed before conclusions")
    if not re.search(r"^#+\s*(scope|boundaries|out-of-scope)", text, re.M):
        v.append("plan lacks scope/boundaries")
    if not re.search(r"(assumption|blind spot|what we haven't considered|failure mode)", text):
        v.append("plan lacks assumption/blind-spot/risk section")
    return v


def gate_assumptions(run: Path) -> list[str]:
    rows = _rows(run / "assumptions.md")
    if not rows:
        return ["assumptions.md has no table rows"]
    v = []
    header = [c.lower() for c in rows[0]]
    status_idx = next((i for i, c in enumerate(header) if "status" in c or "disposition" in c), None)
    if status_idx is None:
        return ["assumptions table lacks a status/disposition column"]
    for row in rows[1:]:
        if len(row) <= status_idx:
            v.append("assumption row missing status cell")
            continue
        if row[status_idx].lower() not in DISPOSITIONS:
            v.append(f"assumption {row[0][:40]!r}: status {row[status_idx]!r} not in {DISPOSITIONS}")
    return v


def gate_hypotheses(run: Path) -> list[str]:
    rows = _rows(run / "hypotheses.md")
    if not rows:
        return ["hypotheses.md has no table rows — competing explanations must be explicit"]
    header = [c.lower() for c in rows[0]]
    status_idx = next((i for i, c in enumerate(header) if "status" in c), None)
    ev_idx = next((i for i, c in enumerate(header)
                   if "discriminating" in c or "evidence" in c), None)
    if status_idx is None:
        return ["hypothesis table lacks a status column"]
    v = []
    for row in rows[1:]:
        if len(row) <= status_idx or row[status_idx].lower() not in HYP_STATUS:
            v.append(f"hypothesis {row[0][:40]!r}: status not in {HYP_STATUS}")
            continue
        if row[status_idx].lower() == "unresolved" and ev_idx is not None:
            reason = row[ev_idx] if len(row) > ev_idx else ""
            if not reason.strip():
                v.append(f"hypothesis {row[0][:40]!r}: unresolved but no evidence/reason given")
    return v


def gate_decision_matrix(run: Path) -> list[str]:
    rows = _rows(run / "decision-matrix.md")
    if not rows:
        return []
    v = []
    header, body = rows[0], rows[1:]
    if len(header) < 3:
        v.append("decision matrix needs >=2 criteria columns")
        return v
    width = len(header)
    for i, row in enumerate(body):
        if len(row) != width:
            v.append(f"matrix row {i+1} ragged: {len(row)} cells vs {width} columns")
        elif any(not c for c in row):
            v.append(f"matrix row {i+1} has empty cells")
    # weights row (optional, named "weight")
    weight_row = next((r for r in body if r and r[0].lower() in ("weight", "weights")), None)
    if weight_row:
        try:
            nums = [float(re.sub(r"[^0-9\.]", "", c)) for c in weight_row[1:] if c]
            if abs(sum(nums) - 1.0) > 0.05:
                v.append(f"criteria weights sum to {sum(nums):.2f}, expected 1.0")
        except ValueError:
            v.append("weights row contains non-numeric values")
    text = (run / "decision-matrix.md").read_text(encoding="utf-8").lower()
    if not re.search(r"(verdict|recommend|preferred|chosen)", text):
        v.append("decision matrix lacks a verdict/recommendation")
    return v


def gate_failure_modes(run: Path) -> list[str]:
    rows = _rows(run / "failure-modes.md")
    if not rows:
        return []
    header = [c.lower() for c in rows[0]]
    sev_idx = next((i for i, c in enumerate(header) if "severity" in c), None)
    mit_idx = next((i for i, c in enumerate(header) if "mitigation" in c), None)
    v = []
    for i, row in enumerate(rows[1:]):
        if sev_idx is not None and len(row) > sev_idx:
            if row[sev_idx].lower() not in SEVERITY:
                v.append(f"failure mode row {i+1}: severity {row[sev_idx]!r} not in {SEVERITY}")
        if mit_idx is not None and len(row) > mit_idx:
            if not row[mit_idx].strip():
                v.append(f"failure mode row {i+1}: missing mitigation")
    return v


def gate_review_log(run: Path) -> list[str]:
    path = run / "review-log.md"
    if not path.exists():
        return ["review-log.md missing — adversarial review is mandatory before conclusions"]
    text = path.read_text(encoding="utf-8").lower()
    v = []
    verdicts = re.findall(r"\bverdict\s*[:=]?\s*\**(approved|revise|blocked)\**", text)
    if not verdicts:
        v.append("review log has no APPROVED/REVISE/BLOCKED verdict")
    final = verdicts[-1] if verdicts else None
    if final != "approved":
        v.append(f"final review verdict is {final!r}, not APPROVED — conclusions cannot ship as-is")
    rounds = re.findall(r"\bround\s*[:=]?\s*\**(\d+)\**", text)
    if rounds and int(rounds[-1]) > 5:
        v.append(f"review exceeded round cap: {rounds[-1]} > 5")
    fids = re.findall(r"\bF\d+\b", text, re.I)
    for fid in set(fids):
        m = re.search(rf"{fid}[^\n]*?(accepted[^\n]*|rejected[^\n]*)", text, re.I)
        if not m:
            v.append(f"finding {fid.upper()} lacks an accepted/rejected disposition")
    if not fids:
        v.append("review log records no findings — a review with zero findings must say so explicitly")
    return v


def gate_research_request(run: Path) -> list[str]:
    path = run / "research-request.json"
    if not path.exists():
        return []  # optional artifact
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"research-request.json malformed: {exc}"]
    v = []
    if data.get("schema") != "deep-analysis-request/1":
        v.append("research-request.json schema must be 'deep-analysis-request/1'")
    reqs = data.get("requests", [])
    if not isinstance(reqs, list) or not reqs:
        v.append("research-request.json requires a non-empty requests[] list")
    for i, r in enumerate(reqs):
        if not isinstance(r, dict):
            v.append(f"request {i}: not an object")
            continue
        for field in ("question", "why_needed", "decision_at_stake"):
            if not (r.get(field) or "").strip():
                v.append(f"request {i}: missing {field}")
    return v


GATES = {
    "framing": gate_framing,
    "assumptions": gate_assumptions,
    "hypotheses": gate_hypotheses,
    "decision-matrix": gate_decision_matrix,
    "failure-modes": gate_failure_modes,
    "review-log": gate_review_log,
    "research-request": gate_research_request,
}


def evaluate(run_dir: Path) -> dict:
    results = {}
    for name, fn in GATES.items():
        results[name] = fn(run_dir)
    # framing, hypotheses, review-log are mandatory; others optional-if-present
    mandatory_pass = all(not results[n] for n in ("framing", "hypotheses", "review-log"))
    return {"pass": mandatory_pass and not any(results.values()),
            "gates": results}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Validate analysis artifacts")
    p.add_argument("run_dir", help="analysis run directory")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    run = Path(args.run_dir)
    if not run.is_dir():
        print(json.dumps({"pass": False, "error": "not a directory"}))
        return 2
    result = evaluate(run)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for name, violations in result["gates"].items():
            if violations:
                for v in violations:
                    print(f"FAIL [{name}] {v}")
            else:
                print(f"PASS [{name}]")
        print(f"\n{'READY' if result['pass'] else 'NOT READY'}")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
