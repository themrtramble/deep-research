#!/usr/bin/env python3
"""Build a simple report from the persistent JSONL evidence files."""

from __future__ import annotations

import argparse
import html
import json
import shutil
import subprocess
from pathlib import Path


def rows(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def build_markdown(root: Path) -> Path:
    claims = rows(root / "claims.jsonl")
    sources = rows(root / "sources.jsonl")
    conflicts = rows(root / "conflicts.jsonl")
    lines = ["# Research report", "", "## Findings", ""]
    for claim in claims:
        confidence = claim.get("confidence", "unknown")
        lines.append(f"### {claim.get('claim_id', 'claim')} — confidence: {confidence}")
        lines.append("")
        lines.append(str(claim.get("claim", "")))
        if claim.get("evidence_ids"):
            lines.append(f"\nEvidence: {', '.join(map(str, claim['evidence_ids']))}")
        lines.append("")
    lines += ["## Contradictions", ""]
    if conflicts:
        for conflict in conflicts:
            lines.append(f"- **{conflict.get('conflict_id')}** ({conflict.get('status', 'unresolved')}): {conflict.get('resolution', 'No resolution recorded.')}")
    else:
        lines.append("No contradictions recorded.")
    lines += ["", "## Sources", ""]
    for source in sources:
        lines.append(f"- [{source.get('title', source.get('source_id', 'source'))}]({source.get('url', '')})")
    output = root / "report.md"
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--html", action="store_true")
    parser.add_argument("--pdf", action="store_true")
    args = parser.parse_args()
    markdown = build_markdown(args.run_dir)
    if args.html:
        body = html.escape(markdown.read_text(encoding="utf-8")).replace("\n", "<br>\n")
        (args.run_dir / "report.html").write_text(
            f"<!doctype html><meta charset='utf-8'><title>Research report</title><main>{body}</main>\n",
            encoding="utf-8",
        )
    if args.pdf:
        converter = shutil.which("pandoc")
        if not converter:
            parser.error("--pdf requires pandoc; Markdown and HTML were still generated")
        subprocess.run([converter, str(markdown), "-o", str(args.run_dir / "report.pdf")], check=True)
    print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

