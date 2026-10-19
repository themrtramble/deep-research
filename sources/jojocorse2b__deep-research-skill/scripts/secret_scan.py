#!/usr/bin/env python3
"""Fail closed when a research directory contains likely credentials."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "bearer token": re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    "cloud access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "assignment secret": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{12,}"
    ),
}
SKIP_NAMES = {".git", ".venv", "__pycache__"}


def scan(root: Path) -> list[tuple[str, int, str]]:
    findings: list[tuple[str, int, str]] = []
    for path in root.rglob("*"):
        if not path.is_file() or any(part in SKIP_NAMES for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            for label, pattern in PATTERNS.items():
                if pattern.search(line):
                    findings.append((str(path.relative_to(root)), line_no, label))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    findings = scan(args.root)
    if findings:
        for path, line, label in findings:
            print(f"SECRET-LIKE {label}: {path}:{line}", file=sys.stderr)
        return 1
    print(f"secret scan passed: {args.root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

