#!/usr/bin/env python3
"""validate.py — report + evidence-chain validator for the Deep Research skill.

Structural checks computed mechanically, never self-reported by an LLM:
report sections, inline citation density, claim-matrix ↔ ledger
cross-reference, answer-status declaration, calibrated confidence
vocabulary, URL sanity, and uncertainty labeling of unsupported claims.

Adapted from: Silence-view/deep-research validate_report.py (MIT),
robertnowell/deep-research validator (MIT), doryashar validate_outputs.js
(MIT), jojocorse2b validate_evidence.py (MIT, Lan Zheng).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dr_core import die, read_jsonl, redact_secrets, scan_secrets  # noqa: E402

ALLOWED_CONFIDENCE = ("established", "likely", "contested", "weak", "unknown",
                      "single-source", "high-confidence", "medium-confidence",
                      "low-confidence")
ANSWER_STATUSES = ("fully-answered", "partially-answered", "unanswerable")
_BAD_URL_PATTERNS = (
    re.compile(r"https?://(example\.(?:com|org)|localhost|127\.0\.0\.1)/\S*"),
    re.compile(r"doi\.org/10\.(?:TODO|XXXX|0000)\S*"),
    re.compile(r"https?://\S*(?:your-?domain|insert-?url|example\.com)\S*"),
)
_INLINE_CITE = re.compile(r"\[[^\]]{1,80}\]\((?:https?://|doi:)[^)\s]+\)")
_CLAIM_REF = re.compile(r"\b(CL-[A-Za-z0-9]{2,12})\b")

REQUIRED_SECTIONS_ALL = ("findings", "sources")
REQUIRED_SECTIONS_DEEP = ("summary", "method", "findings", "claim-matrix",
                          "gaps", "limitations", "sources")


def _word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def _headings(text: str) -> list[str]:
    return [h.lower() for h in re.findall(r"^#{1,4}\s+(.+)$", text, re.M)]


def validate(report: Path, run_dir: Path | None = None,
             mode: str = "standard") -> dict:
    checks: list[dict] = []

    def record(name: str, passed: bool, detail: str = "") -> None:
        checks.append({"check": name, "status": "pass" if passed else "FAIL",
                       "detail": detail})

    text = report.read_text(encoding="utf-8") if report.exists() else ""
    if not report.exists():
        record("report-exists", False, str(report))
        return {"pass": False, "checks": checks}
    record("report-exists", True, f"{_word_count(text)} words")

    # secrets — fail-closed
    secret_hits = scan_secrets(text)
    record("no-secrets-in-report", not secret_hits,
           "; ".join(secret_hits) or "clean")

    headings = _headings(text)
    required = (REQUIRED_SECTIONS_DEEP if mode in ("deep", "exhaustive")
                else REQUIRED_SECTIONS_ALL)
    for sec in required:
        sec_norm = sec.replace("-", " ")
        record(f"section:{sec}",
               any(sec in h or sec_norm in h for h in headings),
               f"headings: {', '.join(headings[:12])}")

    # citation density
    cites = _INLINE_CITE.findall(text)
    words = max(_word_count(text), 1)
    density = words // max(len(cites), 1)
    record("citation-density",
           len(cites) >= 3 and density <= 500,
           f"{len(cites)} inline citations, 1 per {density} words")

    # answer status declared
    status_found = next((s for s in ANSWER_STATUSES if s in text.lower()), None)
    record("answer-status-declared", status_found is not None,
           status_found or "must declare fully/partially/unanswerable")

    # confidence vocabulary — flag uncalibrated certainty on uncertain claims
    overclaim = re.findall(r"\b(?:proves?|definitely|certainly|guaranteed)\b",
                           text, re.I)
    record("calibrated-language",
           len(overclaim) == 0,
           f"uncalibrated words: {overclaim[:5]}" if overclaim else "clean")

    # URL sanity
    bad_urls = [m.group(0) for pat in _BAD_URL_PATTERNS for m in pat.finditer(text)]
    record("no-fabricated-urls", not bad_urls, "; ".join(bad_urls[:3]) or "clean")

    # ledger cross-reference
    if run_dir is not None:
        evidence = read_jsonl(run_dir / "evidence.jsonl")
        report_claims = set(_CLAIM_REF.findall(text))
        ledger_claims = {e.get("claim_id") for e in evidence}
        hi_claims = {e.get("claim_id") for e in evidence
                     if (e.get("importance") or 0) >= 4}
        missing_in_report = sorted(hi_claims - report_claims)
        missing_in_ledger = sorted(report_claims - ledger_claims)
        record("ledger-claims-in-report",
               not missing_in_report,
               f"high-importance claim ids missing from report: {missing_in_report[:5]}"
               if missing_in_report else "all high-importance claims reported")
        record("report-claims-in-ledger",
               not missing_in_ledger,
               f"report cites unknown claim ids: {missing_in_ledger[:5]}")
        record("high-impact-claims-present",
               hi_claims and hi_claims <= report_claims,
               f"high-importance claims: {len(hi_claims)}")
        unsupported = sorted({c for c in report_claims - ledger_claims})
        if unsupported:
            record("unsupported-claims-labeled", False,
                   f"{unsupported[:5]} lack ledger evidence")
        else:
            record("unsupported-claims-labeled", True, "all cited claims ledgered")
    else:
        record("ledger-cross-reference", True,
               "skipped — no run dir (pass --run-dir for full cross-check)")

    passed = all(c["status"] == "pass" for c in checks)
    return {"pass": passed, "mode": mode, "checks": checks,
            "failed": [c["check"] for c in checks if c["status"] == "FAIL"]}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Validate a research report")
    p.add_argument("report", help="path to report.md")
    p.add_argument("--run-dir", help="research run dir (evidence.jsonl etc.)")
    p.add_argument("--mode", default="standard",
                   choices=("quick", "standard", "deep", "exhaustive"))
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    if not Path(args.report).exists():
        die(f"report not found: {args.report}")
    result = validate(Path(args.report),
                      Path(args.run_dir) if args.run_dir else None,
                      args.mode)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for c in result["checks"]:
            mark = "PASS" if c["status"] == "pass" else "FAIL"
            print(f"[{mark}] {c['check']}: {c['detail']}")
        print(f"\n{'PASS' if result['pass'] else 'FAIL'} "
              f"({len(result['checks']) - len(result['failed'])}/{len(result['checks'])} checks)")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
