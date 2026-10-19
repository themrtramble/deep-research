#!/usr/bin/env python3
"""classify.py — task classifier for the Deep Research skill.

Determines the research effort tier before any budget is spent: explicit
user flags always win; otherwise strong-signal phrases and an additive
score decide. Output is a JSON plan consumed by the skill workflow.

Adapted from doryashar/deep-research-skill classify.js (MIT, (c) 2026
dyashar) with effort tiers from B143KC47/deep-research-skill (MIT).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dr_core import EFFORT_DEFAULTS, die  # noqa: E402

DEEP_PHRASES = (
    "deep research", "deep dive", "comprehensive", "exhaustive",
    "thorough", "in-depth", "state of the art", "systematic review",
    "literature review", "competitive analysis", "landscape",
    "everything about", "all aspects", "compare all", "trade-offs",
)
QUICK_PHRASES = (
    "quick", "brief", "just", "fast", "short", "headline",
    "one-liner", "tl;dr", "tldr", "definition of", "what is",
)
BREADTH_MARKERS = ("all", "every", "compare", "landscape", "survey", "overview",
                   "multiple", "various", "versus", " vs ", "ecosystem")
DEPTH_MARKERS = ("why", "how", "mechanism", "under the hood", "internals",
                 "root cause", "architecture", "trade-offs", "implications",
                 "consequences", "derive", "prove")
FACTOID_MARKERS = ("when did", "what year", "who is", "how many",
                   "capital of", "population of", "price of", "release date",
                   "email of", "phone number of")
ENUM_MARKERS = ("list", "top ", "best ", "examples of", "types of",
                "kinds of", "alternatives to")

_SCORE = {
    "short": -2,
    "factoid": -3,
    "breadth": 2,
    "depth": 2,
    "enum": 1,
    "deep_phrase": 3,
    "quick_phrase": -3,
}


def classify(text: str, explicit_mode: str | None = None) -> dict:
    """Classify a research request into a mode + budget plan."""
    orig = (text or "").strip()
    t = orig.lower()
    if explicit_mode:
        if explicit_mode not in EFFORT_DEFAULTS:
            raise ValueError(f"unknown mode {explicit_mode!r}")
        mode = explicit_mode
        rationale = "explicit user flag"
    else:
        score = 0
        hits: list[str] = []
        if len(t) < 25:
            score += _SCORE["short"]
            hits.append("short-query")
        for m in FACTOID_MARKERS:
            if m in t:
                score += _SCORE["factoid"]
                hits.append("factoid")
                break
        n_breadth = sum(1 for m in BREADTH_MARKERS if m in t)
        if n_breadth:
            score += _SCORE["breadth"] * min(n_breadth, 2)
            hits.append(f"breadth x{min(n_breadth, 2)}")
        n_depth = sum(1 for m in DEPTH_MARKERS if m in t)
        if n_depth:
            score += _SCORE["depth"] * min(n_depth, 2)
            hits.append(f"depth x{min(n_depth, 2)}")
        for m in ENUM_MARKERS:
            if m in t:
                score += _SCORE["enum"]
                hits.append("enumeration")
                break
        deep_hit = next((p for p in DEEP_PHRASES if p in t), None)
        quick_hit = next((p for p in QUICK_PHRASES if p in t), None)
        if deep_hit:
            # explicit depth intent cancels brevity/factoid penalties
            score += _SCORE["deep_phrase"]
            score -= _SCORE["short"] if len(t) < 25 else 0
            score -= _SCORE["factoid"] if any(m in t for m in FACTOID_MARKERS) else 0
            hits.append(f"deep-phrase({deep_hit})")
        else:
            if quick_hit:
                score += _SCORE["quick_phrase"]
                hits.append(f"quick-phrase({quick_hit})")

        if score <= -1:
            mode = "quick"
        elif score >= 4:
            mode = "exhaustive"
        elif score >= 3:
            mode = "deep"
        else:
            mode = "standard"
        rationale = f"score={score} hits=[{', '.join(hits) or 'none'}]"

    max_hops, min_sources, min_classes = EFFORT_DEFAULTS[mode]
    needs_clarification = _ambiguity(t, orig) and mode != "quick"
    return {
        "mode": mode,
        "rationale": rationale,
        "needs_clarification": needs_clarification,
        "budget": {
            "max_hops": max_hops,
            "min_sources": min_sources,
            "min_source_classes": min_classes,
            "searches_per_wave": {"quick": 2, "standard": 4,
                                  "deep": 6, "exhaustive": 8}[mode],
            "waves_cap": {"quick": 1, "standard": 3, "deep": 5, "exhaustive": 8}[mode],
        },
        "refusal_check": _dual_use(t),
    }


_AMBIGUOUS = re.compile(r"\b(it|this|that|they|the problem|the issue)\b", re.I)
_PROPER_NOUN = re.compile(r"\b[A-Z][a-z]{2,}\b")


def _ambiguity(t: str, orig: str) -> bool:
    """True when the request has a pronoun-style unresolved referent and no
    proper-noun or quoted anchor — recommend one clarifying question."""
    if t.count(" ") < 3:
        return False
    has_anchor = bool(_PROPER_NOUN.search(orig)) or '"' in orig or "'" in orig
    return bool(_AMBIGUOUS.search(t)) and not has_anchor


_DUAL_USE = re.compile(
    r"\b(exploit|weaponiz\w*|malware|ransomware|keylogger|bypass (?:the )?security"
    r"|poison|hack (?:into|email)|steal (?:data|credentials)|credit card)\b", re.I)


def _dual_use(t: str) -> dict:
    m = _DUAL_USE.search(t)
    if not m:
        return {"flagged": False}
    return {
        "flagged": True,
        "trigger": m.group(0),
        "policy": ("Dual-use topic: proceed only with defensive/legitimate framing; "
                   "refuse operational uplift for attacks on systems you do not own."),
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Classify a research request")
    p.add_argument("question", help="the research question")
    p.add_argument("--mode", choices=tuple(EFFORT_DEFAULTS), default=None,
                   help="explicit override (always wins)")
    p.add_argument("--json", action="store_true", help="JSON output")
    args = p.parse_args(argv)
    try:
        result = classify(args.question, args.mode)
    except ValueError as exc:
        die(str(exc))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"mode={result['mode']} ({result['rationale']}) "
              f"clarify={result['needs_clarification']} "
              f"refusal_flag={result['refusal_check']['flagged']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
