#!/usr/bin/env python3
"""calibrate.py — epistemic calibration linter for the Deep Analysis skill.

Detects two classes of reasoning-language defects in analysis documents:

1. SILENT UPGRADES — prose certainty exceeding the declared epistemic
   status of a claim. A claim labeled `contested` may never be written as
   "proves", "definitely", or "established". Inspired by the silent-upgrade
   lint of Imbad0202/academic-research-skills (CC BY-NC — ideas only, no
   text copied) and the vague-adjective ban of
   zLanqing/codex-claude-academic-skills (MIT).

2. UNMEASURED LANGUAGE — vague comparatives ("significantly better") and
   naked numbers without units or baselines.

Exit 0 = calibrated (warnings allowed); exit 1 = silent upgrades found.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

STATUS_DECL = re.compile(
    r"(?P<prefix>^#{1,6}\s|\s[-*]\s|\||\b)status\s*[:=]\s*"
    r"\**(?P<status>established|supported|likely|preliminary|speculative"
    r"|contested|weak|unknown)\**",
    re.I,
)

# What stronger vocabulary each status still permits (regex fragments).
FORBIDDEN = {
    "established": set(),
    "supported": {"proves?", "definitely", "certainly", "guaranteed"},
    "likely": {"proves?", "definitely", "certainly", "guaranteed",
               "establishes?", "confirmed"},
    "preliminary": {"proves?", "definitely", "certainly", "guaranteed",
                    "establishes?", "confirmed", "demonstrates?"},
    "speculative": {"proves?", "definitely", "certainly", "guaranteed",
                    "establishes?", "confirmed", "demonstrates?", "shows?"},
    "contested": {"proves?", "definitely", "certainly", "guaranteed",
                  "establishes?", "confirmed", "demonstrates?", "shows?"},
    "weak": {"proves?", "definitely", "certainly", "guaranteed",
             "establishes?", "confirmed", "demonstrates?", "shows?"},
    "unknown": {"proves?", "definitely", "certainly", "guaranteed",
                "establishes?", "confirmed", "demonstrates?", "shows?"},
}

VAGUE = re.compile(
    r"\b(?:significantly|dramatically|substantially|much (?:better|worse|faster)"
    r"|far (?:more|less|better|worse)|vastly|hugely|massively)\b", re.I)
NUMBER = re.compile(r"\b\d[\d,\.]*\b")
UNIT = re.compile(
    r"(?:%|percent\b|ms\b|s\b|seconds?\b|min(?:utes?)?\b|hours?\b|days?\b"
    r"|weeks?\b|months?\b|years?\b|usd\b|\$\s?\d|eur\b|inr\b|gb\b|mb\b|kb\b"
    r"|tb\b|x\b|times\b|users?\b|requests?\b|lines?\b|files?\b|nodes?\b)", re.I)


def _status_blocks(text: str) -> list[tuple[str, str]]:
    """Split text into (declared_status, block_text) segments."""
    blocks: list[tuple[str, str]] = []
    matches = list(STATUS_DECL.finditer(text))
    if not matches:
        return [("unknown", text)]
    start = 0
    for i, m in enumerate(matches):
        blocks.append(("unknown" if i == 0 and m.start() > 0 else blocks and blocks[-1][0] or "unknown",
                       text[start:m.start()]))
        status = m.group("status").lower()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        blocks.append((status, text[m.end():end]))
        start = end
    return blocks


def calibrate(text: str, strict: bool = False) -> dict:
    """Return {upgrades: [str], vague: [str], naked_numbers: [str]}."""
    upgrades: list[str] = []
    vague_hits: list[str] = []
    naked_numbers: list[str] = []

    for status, block in _status_blocks(text):
        forbidden = FORBIDDEN.get(status, set())
        for word in forbidden:
            for m in re.finditer(rf"\b{word}\b", block, re.I):
                fragment = block[max(0, m.start() - 40):m.end() + 40]
                fragment = re.sub(r"\s+", " ", fragment).strip()
                upgrades.append(f"[status={status}] ...{fragment}...")

    for m in VAGUE.finditer(text):
        window = text[max(0, m.start() - 60):m.end() + 60]
        window_clean = re.sub(r"\s+", " ", window).strip()
        if not NUMBER.search(window):
            vague_hits.append(f"no measurement near: ...{window_clean}...")

    for line_no, line in enumerate(text.splitlines(), 1):
        for m in NUMBER.finditer(line):
            window = line[max(0, m.start() - 30):m.end() + 30]
            if not UNIT.search(window) and not re.search(r"\b(19|20)\d{2}\b", m.group(0)):
                naked_numbers.append(f"line {line_no}: ...{line.strip()[:80]}...")

    return {"upgrades": upgrades, "vague": vague_hits,
            "naked_numbers": naked_numbers}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Calibration linter")
    p.add_argument("document", help="markdown file to lint")
    p.add_argument("--strict", action="store_true",
                   help="treat vague/unmeasured warnings as errors too")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    path = Path(args.document)
    if not path.exists():
        print(json.dumps({"error": f"not found: {path}"}))
        return 2
    result = calibrate(path.read_text(encoding="utf-8"), args.strict)
    errors = result["upgrades"]
    warnings = result["vague"] + result["naked_numbers"]
    if args.json:
        print(json.dumps({"errors": errors, "warnings": warnings},
                         ensure_ascii=False, indent=2))
    else:
        for u in errors:
            print(f"ERROR silent-upgrade: {u}")
        for w in warnings:
            print(f"WARN unmeasured: {w}")
        verdict = "CALIBRATED" if not errors and not (args.strict and warnings) \
            else "MISALIGNED"
        print(f"\n{verdict}: {len(errors)} silent upgrade(s), "
              f"{len(warnings)} unmeasured-language warning(s)")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
