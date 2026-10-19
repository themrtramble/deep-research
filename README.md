# deep-skills

**Two production-grade, interoperable, independently usable AI agent skills:**

- **`deep-research/`** — evidence-driven deep research: decomposes questions, runs multi-source discovery waves, maintains a structured evidence ledger, verifies citations, hunts counterevidence, and ships calibrated, cited reports with explicit gaps.
- **`deep-analysis/`** — rigorous analytical reasoning: frames the real question, pre-commits evaluation criteria, audits assumptions, tests competing hypotheses, runs multi-perspective and adversarial review, quantifies risk, and delivers calibrated conclusions.

Both skills were engineered by auditing **29 open-source research/analysis
repos** (8 original seeds + 9 additional seeds + 12 discovered candidates),
extracting the strongest verified capabilities, and rebuilding them as one
coherent, tested system. See `docs/` for the full discovery inventory,
source-to-capability matrix, and architecture.

## Why two skills

They answer different questions with a defined handoff contract:

| | deep-research | deep-analysis |
|---|---|---|
| Answers | *What is known? What evidence exists? How reliable is it?* | *What does the evidence establish? Which explanation survives scrutiny?* |
| Core loop | plan → search waves → evidence ledger → verify → report | frame → decompose → hypothesize → perspectives → adversarial review → calibrated conclusions |
| Handoff out | `research-package.json` (claims + sources + conflicts + gaps) | `research-request.json` (targeted questions for missing evidence) |

Each works standalone. Together they close the research→analysis→more-research loop.

## What's inside each skill

```
deep-research/                    deep-analysis/
├── SKILL.md            entry      ├── SKILL.md            entry
├── references/         protocols  ├── references/         frameworks
│   research-protocol, source-quality, │ first-principles, perspectives, causal-reasoning,
│   query-playbook, citation-verify,   │ adversarial-review, calibration, quantitative,
│   stop-conditions, security, handoff │ handoff
├── templates/          artifacts  ├── templates/          artifacts
├── scripts/            deterministic tools                 │
│   ledger, classify, dedup, validate, │ calibrate (epistemic linter),
│   gates, package, dr_core            │ analysis_gates (artifact validators)
└── tests/              pytest + eval scenarios            └── tests/  pytest + eval scenarios
```

Everything is **stdlib-only Python 3** — no dependencies, no API keys, no
paid services required. Free components only; the skills use whatever
search/LLM capabilities your agent host already provides.

## Quick start

Skills are consumed by AI agent hosts (Claude Code, Cursor, Codex,
OpenCode, or any agent that reads SKILL.md files and can run Python).

1. **Install**: clone this repo (or copy a skill folder) into your agent's
   skills directory.
2. **Research**:
   ```
   python deep-research/scripts/classify.py "compare vector DBs for RAG" --json
   python deep-research/scripts/ledger.py init research/run-1 --question "..." --mode deep
   # the SKILL.md drives the agent through waves, ledger, verification
   python deep-research/scripts/gates.py research/run-1
   python deep-research/scripts/validate.py research/run-1/report.md --run-dir research/run-1
   ```
3. **Analyze**:
   ```
   # agent follows deep-analysis/SKILL.md; artifacts gate themselves:
   python deep-analysis/scripts/analysis_gates.py analysis/case-1
   python deep-analysis/scripts/calibrate.py analysis/case-1/conclusions.md
   ```

## Tests

```
python3 -m pytest deep-research/tests deep-analysis/tests -q
# 101 passed (offline, deterministic, no network, no keys)
```

Agent-level eval scenarios (20 + integration cases) are specified in
`deep-research/tests/evals.md` and `deep-analysis/tests/evals.md` — they
require a live agent runner and are judge-scored, not automated.

## Documentation

- `docs/discovery-inventory.md` — every repo audited, included, and excluded (with reasons)
- `docs/capability-matrix.md` — source-to-capability provenance and license constraints
- `docs/architecture.md` — the unified design and how the two skills interoperate
- `docs/test-report.md` — what actually runs, what passed, what's honest about limits

## License

MIT — see `LICENSE`. Attribution for reused components: `ATTRIBUTION.md`.
