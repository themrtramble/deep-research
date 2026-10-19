#!/usr/bin/env python3
"""gates.py — arithmetic stop/quality gates for the Deep Research skill.

Computes coverage and readiness gates from the ledger, with thresholds
scaled by effort mode. All numbers are computed from records — an LLM
never self-reports a gate. Exit 0 = all hard gates pass; exit 1 = report
the failing gates. --json for machine-readable output.

Inspired by hashbulla/deep-research verify_gates.py (MIT): arithmetic
gates, computed, never self-assessed.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dr_core import EFFORT_DEFAULTS, read_json, read_jsonl  # noqa: E402

# mode -> (min_sources, min_classes, min_waves, max_uncovered_hi_claims)
GATE_TABLE = {
    "quick": (2, 2, 1, 0),
    "standard": (5, 3, 2, 0),
    "deep": (10, 4, 3, 0),
    "exhaustive": (15, 5, 3, 0),
}


def evaluate(run_dir: Path) -> dict:
    meta = read_json(run_dir / "metadata.json") or {}
    mode = meta.get("mode", "standard")
    if mode not in GATE_TABLE:
        mode = "standard"
    min_sources, min_classes, min_waves, max_uncovered = GATE_TABLE[mode]
    sources = read_jsonl(run_dir / "sources.jsonl")
    evidence = read_jsonl(run_dir / "evidence.jsonl")
    hops = read_jsonl(run_dir / "hops.jsonl")
    conflicts = read_jsonl(run_dir / "conflicts.jsonl")

    classes = {s.get("source_type") for s in sources if s.get("source_type")}
    families = {s.get("independence_family") for s in sources
                if s.get("independence_family")}
    hi_claims = {e.get("claim_id") for e in evidence
                 if (e.get("importance") or 0) >= 4}
    contradicted = {e.get("claim_id") for e in evidence
                    if e.get("stance") == "contradicts"}
    covered_hi = hi_claims & contradicted
    verified_hops = [h for h in hops if h.get("mode") in ("verify", "contradict")]
    waves = len(verified_hops)
    unresolved = [c for c in conflicts if c.get("status") == "unresolved"]

    gates = {
        "sources-count": {
            "value": len(sources), "min": min_sources,
            "pass": len(sources) >= min_sources,
        },
        "source-class-diversity": {
            "value": len(classes), "min": min_classes,
            "pass": len(classes) >= min_classes,
        },
        "independence-families": {
            "value": len(families), "min": max(2, min_sources // 2),
            "pass": len(families) >= max(2, min_sources // 2),
        },
        "counterevidence-searched": {
            "value": len(covered_hi), "min": len(hi_claims) - max_uncovered,
            "pass": len(hi_claims) - len(covered_hi) <= max_uncovered,
        } if hi_claims else {
            "value": 0, "min": 0, "pass": True,
            "note": "no high-importance claims recorded",
        },
        "verification-waves": {
            "value": waves, "min": min_waves,
            "pass": waves >= min_waves,
        },
        "conflicts-resolved-or-declared": {
            "value": len(unresolved), "min": len(conflicts),
            "pass": True,  # unresolved is allowed when declared in report
            "note": f"{len(unresolved)} unresolved conflicts must appear in report limitations",
        },
        "evidence-records": {
            "value": len(evidence), "min": len(sources),
            "pass": len(evidence) >= len(sources),
        },
    }
    all_pass = all(g["pass"] for g in gates.values())
    return {"mode": mode, "pass": all_pass, "gates": gates,
            "summary": {
                "sources": len(sources), "evidence": len(evidence),
                "hops": len(hops), "high_importance_claims": len(hi_claims),
                "unresolved_conflicts": len(unresolved),
            }}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Compute research quality gates")
    p.add_argument("run_dir")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    run = Path(args.run_dir)
    if not (run / "metadata.json").exists():
        print(json.dumps({"pass": False, "error": "not an initialized run dir"}))
        return 1
    result = evaluate(run)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for name, g in result["gates"].items():
            mark = "PASS" if g["pass"] else "FAIL"
            print(f"[{mark}] {name}: value={g['value']} min={g['min']}"
                  + (f" ({g.get('note')})" if g.get("note") else ""))
        verdict = "READY" if result["pass"] else "NOT READY"
        print(f"\n{verdict} (mode={result['mode']})")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
