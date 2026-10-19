#!/usr/bin/env python3
"""package.py — build + verify the Deep Research handoff package.

Compiles research-package.json from a run directory: the machine-readable
artifact consumed by deep-analysis (or any downstream consumer). Validating
the package here guarantees the handoff contract holds even when the two
skills never run in the same session.

Contract (v1):
{
  "schema": "deep-research-package/1",
  "question": str,
  "answer_status": "fully-answered"|"partially-answered"|"unanswerable",
  "sub_questions": [{id, question, answer, confidence, evidence_ids}],
  "claims": [{claim_id, claim, importance, uncertainty, evidence_ids,
              source_ids, stances}],
  "sources": [{source_id, url, title, source_type, quality, accessed_at}],
  "conflicts": [{conflict_id, positions, status}],
  "gaps": [str],
  "coverage": {mode, sources, evidence, unresolved_conflicts},
  "limitations": [str]
}
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dr_core import (  # noqa: E402
    read_json, read_jsonl, redact_secrets, scan_secrets, write_json,
)

SCHEMA = "deep-research-package/1"
ANSWER_STATUSES = ("fully-answered", "partially-answered", "unanswerable")


def build(run_dir: Path, answer_status: str, gaps: list[str],
          limitations: list[str]) -> dict:
    meta = read_json(run_dir / "metadata.json") or {}
    sources = read_jsonl(run_dir / "sources.jsonl")
    evidence = read_jsonl(run_dir / "evidence.jsonl")
    conflicts = read_jsonl(run_dir / "conflicts.jsonl")

    claims: dict[str, dict] = {}
    for e in evidence:
        cid = e.get("claim_id", "")
        c = claims.setdefault(cid, {
            "claim_id": cid,
            "claim": e.get("claim", ""),
            "importance": e.get("importance", 3),
            "uncertainty": e.get("uncertainty", "unknown"),
            "evidence_ids": [],
            "source_ids": [],
            "stances": [],
        })
        c["evidence_ids"].append(e.get("evidence_id"))
        if e.get("source_id") not in c["source_ids"]:
            c["source_ids"].append(e.get("source_id"))
        if e.get("stance") not in c["stances"]:
            c["stances"].append(e.get("stance"))

    src_ids = {s.get("source_id") for s in sources}
    for c in claims.values():
        c["source_ids"] = [s for s in c["source_ids"] if s in src_ids]

    unresolved = [{"conflict_id": c.get("conflict_id"),
                   "positions": c.get("positions", []),
                   "status": c.get("status")}
                  for c in conflicts if c.get("status") == "unresolved"]

    return {
        "schema": SCHEMA,
        "question": meta.get("question", ""),
        "answer_status": answer_status,
        "claims": sorted(claims.values(), key=lambda c: -c["importance"]),
        "sources": [{"source_id": s.get("source_id"), "url": s.get("url"),
                     "title": s.get("title"),
                     "source_type": s.get("source_type"),
                     "quality": s.get("quality"),
                     "accessed_at": s.get("accessed_at")}
                    for s in sources],
        "conflicts": unresolved,
        "gaps": gaps,
        "coverage": {
            "mode": meta.get("mode", "standard"),
            "sources": len(sources),
            "evidence": len(evidence),
            "unresolved_conflicts": len(unresolved),
        },
        "limitations": limitations,
    }


def verify(pkg: dict) -> tuple[list[str], list[str]]:
    """Validate a package. Returns (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []
    if pkg.get("schema") != SCHEMA:
        errors.append(f"schema must be {SCHEMA!r}, got {pkg.get('schema')!r}")
    if not (pkg.get("question") or "").strip():
        errors.append("question is empty")
    if pkg.get("answer_status") not in ANSWER_STATUSES:
        errors.append(f"answer_status must be one of {ANSWER_STATUSES}")

    src_ids = {s.get("source_id") for s in pkg.get("sources", [])}
    ev_ids: set[str] = set()
    for c in pkg.get("claims", []):
        for eid in c.get("evidence_ids", []):
            ev_ids.add(eid)
        for sid in c.get("source_ids", []):
            if sid not in src_ids:
                errors.append(f"claim {c.get('claim_id')}: unknown source_id {sid}")
        if not c.get("claim", "").strip():
            errors.append(f"claim {c.get('claim_id')}: empty claim text")
        if c.get("uncertainty") not in ("established", "likely", "contested",
                                        "weak", "unknown"):
            errors.append(f"claim {c.get('claim_id')}: bad uncertainty value")
        if not c.get("evidence_ids"):
            warnings.append(f"claim {c.get('claim_id')}: no evidence ids")

    hi = [c for c in pkg.get("claims", []) if (c.get("importance") or 0) >= 4]
    for c in hi:
        if len({s for s in c.get("source_ids", [])}) < 2:
            warnings.append(f"high-importance claim {c.get('claim_id')}: "
                            "fewer than 2 supporting sources")

    for blob in (json.dumps(pkg.get("sources", [])),
                 json.dumps(pkg.get("claims", []))):
        for hit in scan_secrets(blob):
            errors.append(f"secrets in package: {hit}")

    if pkg.get("answer_status") == "unanswerable" and not pkg.get("gaps"):
        warnings.append("unanswerable package should explain what was missing")

    return errors, warnings


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Build/verify handoff package")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("build")
    sp.add_argument("run_dir")
    sp.add_argument("--answer-status", required=True, choices=ANSWER_STATUSES)
    sp.add_argument("--gap", action="append", default=[],
                    help="research gap (repeatable)")
    sp.add_argument("--limitation", action="append", default=[],
                    help="limitation (repeatable)")
    sp.add_argument("--out", default=None, help="output path (default: run_dir/package.json)")
    args = p.parse_args(argv)
    run = Path(args.run_dir)
    pkg = build(run, args.answer_status, args.gap, args.limitation)
    errors, warnings = verify(pkg)
    for e in errors:
        print(f"ERROR: {e}")
    for w in warnings:
        print(f"WARN: {w}")
    if errors:
        return 1
    out = Path(args.out) if args.out else run / "package.json"
    write_json(out, pkg)
    print(f"OK: package written to {out} "
          f"({len(pkg['claims'])} claims, {len(pkg['sources'])} sources, "
          f"{len(pkg['conflicts'])} unresolved conflicts)")
    return 0

    # unreachable: subcommand guard above


if __name__ == "__main__":
    raise SystemExit(main())
