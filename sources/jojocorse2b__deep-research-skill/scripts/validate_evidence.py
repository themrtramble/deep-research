#!/usr/bin/env python3
"""Validate the persistent claim/source/evidence contract for a run."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path.name}:{line_no}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path.name}:{line_no}: expected an object")
        rows.append(value)
    return rows


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    manifest = root / "run_manifest.json"
    if not manifest.is_file():
        errors.append("missing run_manifest.json")
    else:
        try:
            json.loads(manifest.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid run_manifest.json: {exc}")

    sources = read_jsonl(root / "sources.jsonl")
    evidence = read_jsonl(root / "evidence.jsonl")
    claims = read_jsonl(root / "claims.jsonl")
    source_ids = {row.get("source_id") for row in sources}
    claim_ids = {row.get("claim_id") for row in claims}
    evidence_ids: set[object] = set()
    for row in sources:
        if not row.get("source_id") or not row.get("url"):
            errors.append("every source needs source_id and url")
    for row in evidence:
        evidence_id = row.get("evidence_id")
        evidence_ids.add(evidence_id)
        if not evidence_id or row.get("source_id") not in source_ids:
            errors.append(f"evidence {evidence_id!r} references an unknown source")
        if not row.get("quote") or not row.get("locator"):
            errors.append(f"evidence {evidence_id!r} needs quote and locator")
    for row in claims:
        claim_id = row.get("claim_id")
        if not claim_id or not row.get("claim"):
            errors.append("every claim needs claim_id and claim")
        for evidence_id in row.get("evidence_ids", []):
            if evidence_id not in evidence_ids:
                errors.append(f"claim {claim_id!r} references unknown evidence {evidence_id!r}")
        if row.get("confidence") not in {"high", "medium", "low", "unknown"}:
            errors.append(f"claim {claim_id!r} has invalid confidence")
    for row in read_jsonl(root / "conflicts.jsonl"):
        if not row.get("conflict_id") or not row.get("claim_ids"):
            errors.append("every conflict needs conflict_id and claim_ids")
        if any(claim_id not in claim_ids for claim_id in row.get("claim_ids", [])):
            errors.append(f"conflict {row.get('conflict_id')!r} references unknown claim")
    if not sources and not claims:
        errors.append("no sources or claims found")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    try:
        errors = validate(args.run_dir)
    except (OSError, ValueError) as exc:
        print(f"evidence validation error: {exc}", file=sys.stderr)
        return 2
    if errors:
        print("evidence validation failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"evidence validation passed: {args.run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

