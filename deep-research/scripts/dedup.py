#!/usr/bin/env python3
"""dedup.py — duplicate-source detector for the Deep Research skill.

Reads a sources.json (or JSONL) file, merges duplicates by normalized URL
and near-identical same-domain titles, and reports a merge log. Duplicates
inflating apparent corroboration is the failure mode this tool prevents:
"ten copies of one press release are one source."

Adapted from doryashar/deep-research-skill dedup_sources.js (MIT) and the
provenance-cluster rule from zy839971925-zyy (MIT).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dr_core import dedup_sources, read_jsonl  # noqa: E402


def load_sources(path: Path) -> list[dict]:
    if path.suffix == ".jsonl":
        return read_jsonl(path)
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data, dict) and "sources" in data:
        data = data["sources"]
    if not isinstance(data, list):
        raise SystemExit(f"ERROR: {path} must be a list or {{'sources': [...]}}")
    return data


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Deduplicate research sources")
    p.add_argument("sources_file", help="sources.json or sources.jsonl")
    p.add_argument("--out", help="write deduped JSON here (default: stdout)")
    p.add_argument("--threshold", type=float, default=0.85,
                   help="title similarity threshold (default 0.85)")
    args = p.parse_args(argv)

    sources = load_sources(Path(args.sources_file))
    deduped, merge_log = dedup_sources(sources, args.threshold)

    payload = {
        "input_count": len(sources),
        "deduped_count": len(deduped),
        "duplicates_merged": len(merge_log),
        "merge_log": merge_log,
        "sources": deduped,
    }
    out = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    if args.out:
        Path(args.out).write_text(out + "\n", encoding="utf-8")
        print(f"deduped {len(sources)} -> {len(deduped)} "
              f"({len(merge_log)} merged); wrote {args.out}")
    else:
        print(out)
    # exit code 1 signals that corroboration was overstated before dedup
    return 1 if merge_log and len(sources) - len(deduped) >= max(2, len(sources) // 4) else 0


if __name__ == "__main__":
    raise SystemExit(main())
