#!/usr/bin/env python3
"""
Validate a deep research report for quality and integrity.

Performs structural checks on the research report to ensure it meets
minimum quality standards before delivery.

Usage:
    python validate_report.py <report_path> [--mode quick|standard|deep|ultradeep]
"""

import re
import sys
import json
import argparse
from pathlib import Path
from collections import Counter


# Minimum source counts by research mode
MIN_SOURCES = {
    "quick": 20,
    "standard": 50,
    "deep": 80,
    "ultradeep": 120,
}

# Minimum Tier 1 percentage by mode
MIN_TIER1_PCT = {
    "quick": 0.20,
    "standard": 0.25,
    "deep": 0.25,
    "ultradeep": 0.30,
}


def extract_citations(text: str) -> list[int]:
    """Extract all citation numbers [N] from the report text."""
    return [int(n) for n in re.findall(r'\[(\d+)\]', text)]


def extract_sections(text: str) -> dict[str, str]:
    """Extract major sections from the report."""
    sections = {}
    current_section = "preamble"
    current_content = []

    for line in text.split('\n'):
        if line.startswith('## '):
            if current_content:
                sections[current_section] = '\n'.join(current_content)
            current_section = line.strip('# ').strip()
            current_content = []
        else:
            current_content.append(line)

    if current_content:
        sections[current_section] = '\n'.join(current_content)

    return sections


def count_bibliography_entries(text: str) -> dict:
    """Count bibliography entries by tier."""
    tiers = {"tier1": 0, "tier2": 0, "tier3": 0, "total": 0}

    in_bib = False
    current_tier = None

    for line in text.split('\n'):
        lower = line.lower().strip()

        # Detect bibliography section start (only ## level headings, not ### tier subheadings)
        if not in_bib and ('bibliography' in lower
                or (lower.startswith('## ') and 'sources' in lower)):
            in_bib = True
            continue

        if in_bib:
            if 'tier 1' in lower or 'credibility >= 0.75' in lower:
                current_tier = "tier1"
            elif 'tier 2' in lower or 'credibility 0.50' in lower:
                current_tier = "tier2"
            elif 'tier 3' in lower or 'background' in lower and 'context' in lower:
                current_tier = "tier3"

            # Match numbered entries: "1.", "12.", etc. (with optional leading whitespace)
            if re.match(r'^\s*\d+\.', line) and current_tier:
                tiers[current_tier] += 1
                tiers["total"] += 1

    # Fallback: if no tier headers found, count all numbered entries in bibliography
    if tiers["total"] == 0 and in_bib:
        for line in text.split('\n'):
            if in_bib and re.match(r'^\s*\d+\.', line):
                tiers["total"] += 1
                tiers["tier2"] += 1  # default to tier2 if no headers

    return tiers


def check_url_patterns(text: str) -> list[str]:
    """Find potential hallucinated URLs (common patterns)."""
    urls = re.findall(r'https?://[^\s\)]+', text)
    suspicious = []

    for url in urls:
        # Check for obviously fake patterns
        if 'example.com' in url:
            suspicious.append(f"Example URL found: {url}")
        if 'arxiv.org' in url:
            if not re.search(r'arxiv\.org/abs/\d{4}\.\d{5}\b', url):
                suspicious.append(f"Malformed arxiv URL: {url}")
        if 'doi.org/10.xxxx' in url.lower():
            suspicious.append(f"Placeholder DOI found: {url}")

    return suspicious


def validate_report(report_path: str, mode: str = "standard") -> dict:
    """Run all validation checks on the report."""
    path = Path(report_path)
    if not path.exists():
        return {"error": f"Report not found: {report_path}"}

    text = path.read_text(encoding='utf-8')
    sections = extract_sections(text)
    citations = extract_citations(text)
    bib = count_bibliography_entries(text)

    results = {
        "report": report_path,
        "mode": mode,
        "checks": [],
        "pass_count": 0,
        "fail_count": 0,
        "warn_count": 0,
    }

    def check(name: str, passed: bool, detail: str = "", severity: str = "fail"):
        status = "PASS" if passed else severity.upper()
        results["checks"].append({
            "name": name,
            "status": status,
            "detail": detail
        })
        if passed:
            results["pass_count"] += 1
        elif severity == "fail":
            results["fail_count"] += 1
        else:
            results["warn_count"] += 1

    # Check 1: Executive Summary exists
    has_summary = any('summary' in k.lower() for k in sections)
    check("Executive Summary present", has_summary,
          "Missing Executive Summary section")

    # Check 2: Key Findings section exists
    has_findings = any('finding' in k.lower() for k in sections)
    check("Key Findings section present", has_findings,
          "Missing Key Findings section")

    # Check 3: Bibliography exists
    has_bib = any('bibliography' in k.lower() or 'sources' in k.lower()
                  for k in sections)
    check("Bibliography present", has_bib,
          "Missing Bibliography/Sources section")

    # Check 4: Minimum source count
    min_sources = MIN_SOURCES.get(mode, 40)
    check("Minimum source count",
          bib["total"] >= min_sources,
          f"Found {bib['total']} sources, need {min_sources} for {mode} mode")

    # Check 5: Tier 1 percentage
    if bib["total"] > 0:
        tier1_pct = bib["tier1"] / bib["total"]
        min_pct = MIN_TIER1_PCT.get(mode, 0.25)
        check("Tier 1 source percentage",
              tier1_pct >= min_pct,
              f"Tier 1 sources: {tier1_pct:.0%}, need {min_pct:.0%}",
              severity="warn")

    # Check 6: Citations used in text
    unique_citations = set(citations)
    check("Citations present in text",
          len(unique_citations) >= 5,
          f"Found {len(unique_citations)} unique citations in text")

    # Check 7: No obviously fake URLs
    suspicious_urls = check_url_patterns(text)
    check("No suspicious URLs",
          len(suspicious_urls) == 0,
          "; ".join(suspicious_urls) if suspicious_urls else "",
          severity="warn")

    # Check 8: Methodology section exists
    has_methodology = any('methodology' in k.lower() for k in sections)
    check("Methodology section present", has_methodology,
          "Missing Methodology section — research transparency is important",
          severity="warn")

    # Check 9: Limitations section exists
    has_limitations = any('limitation' in k.lower() or 'gap' in k.lower()
                         for k in sections)
    check("Limitations section present", has_limitations,
          "Missing Limitations/Gaps section",
          severity="warn")

    # Check 10: Report length check
    word_count = len(text.split())
    min_words = {"quick": 500, "standard": 1500, "deep": 3000, "ultradeep": 5000}
    min_w = min_words.get(mode, 1500)
    check("Minimum report length",
          word_count >= min_w,
          f"Report is {word_count} words, minimum for {mode} is {min_w}")

    # Check 11: Evidence confidence tags present
    confidence_tags = re.findall(
        r'Evidence Confidence.*?(Verified|Strong|Moderate|Emerging|Contested)',
        text, re.IGNORECASE
    )
    check("Evidence confidence tags present",
          len(confidence_tags) >= 1,
          f"Found {len(confidence_tags)} confidence tags",
          severity="warn")

    # Summary
    if results["fail_count"] > 0:
        results["overall"] = "FAIL"
    elif results["warn_count"] > 0:
        results["overall"] = "WARN"
    else:
        results["overall"] = "PASS"

    return results


def main():
    parser = argparse.ArgumentParser(description="Validate a deep research report")
    parser.add_argument("report", help="Path to the research report markdown file")
    parser.add_argument("--mode", default="standard",
                        choices=["quick", "standard", "deep", "ultradeep"],
                        help="Research mode (affects minimum thresholds)")
    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON")

    args = parser.parse_args()
    results = validate_report(args.report, args.mode)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"DEEP RESEARCH REPORT VALIDATION")
        print(f"Report: {results['report']}")
        print(f"Mode: {results['mode']}")
        print(f"{'='*60}\n")

        for check in results["checks"]:
            icon = {"PASS": "+", "FAIL": "X", "WARN": "!"}.get(check["status"], "?")
            print(f"  [{icon}] {check['name']}: {check['status']}")
            if check["detail"]:
                print(f"      {check['detail']}")

        print(f"\n{'='*60}")
        print(f"RESULT: {results['overall']}")
        print(f"  Passed: {results['pass_count']}")
        print(f"  Failed: {results['fail_count']}")
        print(f"  Warnings: {results['warn_count']}")
        print(f"{'='*60}\n")

    sys.exit(0 if results["overall"] in ("PASS", "WARN") else 1)


if __name__ == "__main__":
    main()
