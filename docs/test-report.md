# Test Report

Run date: 2026-10-19. Environment: Python 3.12.15, pytest 9.0.2,
Linux, fully offline (no network, no API keys, no LLM calls — all
service boundaries are mocked or replaced by fixture files).

## Automated suite (deterministic)

```
python3 -m pytest deep-research/tests deep-analysis/tests -q
101 passed in ~4s
```

Breakdown by file:

| Suite | Tests | Covers |
|---|---|---|
| deep-research/tests/test_ledger.py | 18 | init budgets/flat-reject, source id assignment + duplicate-URL rejection, hop parent validation + budget enforcement (+force), evidence source-check + enums, conflict claim validation + resolution semantics, lint (secrets fail-closed, unknown source refs, duplicate ids, orphan parents, unchallenged high-importance warnings), status/export |
| deep-research/tests/test_classify_dedup.py | 20 | explicit-override precedence, deep/quick/exhaustive scoring, ambiguity (pronoun w/o anchor, proper-noun and quoted anchors), dual-use refusal flags, CLI JSON; URL normalization (scheme/www/tracking/fragment), same-URL + near-title dedup, cross-domain non-dedup, title similarity, CLI merge log |
| deep-research/tests/test_validate_gates_package.py | 27 | report structure by mode, citation density, fabricated URLs, answer-status requirement, overclaim language, claim-matrix↔ledger cross-reference (unknown claim ids, dropped high-importance claims), research gates (sparse/rich runs, class diversity, counterevidence), package build/verify (unknown sources, bad status, secret fail-closed), CLI build |
| deep-research/tests/test_security.py | 5 | injection fixture inertness (data-not-instructions), quoting-injection still validates, secrets in ledger artifacts fail lint, secrets in reports fail validation |
| deep-analysis/tests/test_calibrate.py | 13 | silent-upgrade detection per status (contested/likely/speculative/supported/unknown/sequential), no-status conservative default, unmeasured language (vague w/o numbers passes with numbers, naked numbers, unit/year exemptions), CLI exit codes + strict mode |
| deep-analysis/tests/test_gates.py | 18 | full-artifact pass, framing pre-commitment, assumption dispositions, hypothesis statuses + unresolved-without-reason, matrix ragged/weights/verdict/optional, review verdicts + round cap + undispositioned findings + missing log, research-request schema + fields, CLI JSON |

**Failures during development, fixed (honest log):** 27 → 11 → 4 → 1 → 0.
Root causes: a leftover syntax error, a Python module-name collision
(both skills originally exported `gates.py` — analysis side renamed to
`analysis_gates.py`), a subparser-vs-parser argparse bug in package.py,
a set-of-dicts TypeError in research gates.py, over-strict claim-matrix
requirements, case-sensitive regexes on lowercased text, and two test
fixture bugs. All fixed in code, not by weakening assertions.

## Agent-level eval scenarios (NOT automated — honest status)

`deep-research/tests/evals.md` (R1–R10) and `deep-analysis/tests/evals.md`
(A1–A10) define live-runner scenarios: 10 research cases (conflicting
sources, malicious retrieved content, no-search degradation, iterative
gaps, unanswerable questions...) and 10 analysis cases (first principles,
competing hypotheses, root cause, trade-offs, adversarial review,
quantitative reasoning, withholding judgment...). **These require a live
agent with tools and were NOT executed in this build** — they are
judge-scored specifications, documented as such, not claimed as passed.

## Static checks

- All scripts: `python -m py_compile` clean (run via test imports).
- No third-party imports anywhere: verified by inspection (stdlib only:
  argparse, json, re, sys, pathlib, hashlib, unicodedata, difflib,
  urllib.parse, datetime, subprocess-in-tests, tempfile-in-tests).
- Secret scan of the published tree: clean (the test fixtures contain
  synthetic placeholder patterns that are the scanning targets).

## Reproducing

```
git clone https://github.com/themrtramble/deep-skills
cd deep-skills && python3 -m pytest deep-research/tests deep-analysis/tests -q
```
