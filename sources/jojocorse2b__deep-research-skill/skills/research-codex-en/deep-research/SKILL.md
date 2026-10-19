---
name: deep-research
description: Conduct rigorous multi-source research with persistent evidence, claim verification, source reliability scoring, contradiction tracking, secret scanning, and Markdown/HTML/PDF reports.
---

# Deep Research

Use this skill for complex questions, comparisons, state-of-the-art reviews,
due diligence, market research, and any request where a shallow lookup could
mislead. Do not use it for a simple fact that can be answered from one or two
authoritative sources.

## Operating contract

- Separate facts, interpretations, hypotheses, and unknowns.
- Prefer primary sources: official documentation, regulations, standards,
  original papers, datasets, filings, and maintainer statements.
- Use multiple independent sources and search at least one counter-position.
- Never invent citations, quotes, figures, or source access.
- Record enough evidence that another person can reproduce the conclusion.
- Do not expose credentials or put secrets in reports, evidence files, or git.
- For medical, legal, financial, or safety-sensitive topics, state the limits
  and use current authoritative sources.

## Workflow

1. **Scope** — restate the question, date boundary, geography, audience,
   decision to support, and what would count as disconfirming evidence.
2. **Plan** — split the question into independent angles and define the source
   hierarchy and acceptance criteria for each angle.
3. **Retrieve** — search in parallel where useful. For every fetched source,
   record URL, title, publisher, publication/update date, access date, source
   type, and whether it was adopted or discarded.
4. **Extract** — save atomic claims and evidence snippets with locators. Keep
   the original URL and a local evidence record; do not rely on prose memory.
5. **Appraise** — score reliability using the rubric in
   [research-protocol.md](../../../../references/research-protocol.md). Score
   the source itself separately from the strength of support for a claim.
6. **Cross-check** — compare independent sources. Log conflicts with both
   positions, explain the resolution, or mark the issue unresolved.
7. **Verify** — run the evidence validator and claim-support checker. Numbers,
   dates, quotations, and causal claims need direct supporting evidence.
8. **Synthesize** — write a balanced answer with inline citations, confidence,
   limitations, and an explicit unknowns section.
9. **Package** — run the secret scan, persist the manifest and evidence store,
   then generate Markdown. Generate HTML/PDF only after the Markdown passes.

## Evidence files

For each research run, create a directory containing:

- `run_manifest.json` — question, scope, date, tools, assumptions, and status;
- `sources.jsonl` — one normalized record per fetched source;
- `evidence.jsonl` — atomic excerpts, locators, and source IDs;
- `claims.jsonl` — claim text, confidence, support edges, and conflict IDs;
- `conflicts.jsonl` — incompatible claims and their resolution state;
- `report.md` — the human-readable report;
- `report.html` and optionally `report.pdf` — generated deliverables.

Use the bundled helpers when applicable:

```bash
python scripts/validate_evidence.py RUN_DIR
python scripts/secret_scan.py RUN_DIR
python scripts/build_report.py RUN_DIR --html --pdf
```

The helpers are deliberately dependency-light. PDF generation is optional and
uses an installed converter when available; a missing converter must be
reported, never hidden.

## Output standard

Every final report should contain: executive summary, scope and method,
findings grouped by question, evidence-backed claims, contradictions and
unresolved points, limitations, recommendations (if requested), and a complete
bibliography. Label inference explicitly. Do not claim certainty merely because
many low-quality sources repeat the same statement.

