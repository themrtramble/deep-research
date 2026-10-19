# Pressure test: citation drift

## Scenario

Agent has completed 6 search + read rounds on a standard-mode query about
comparing database engines. It has strong opinions about the winner and wants
to write a clean, flowing summary paragraph like:

> "Recent benchmarks show that DuckDB outperforms SQLite on analytical queries
> by roughly 3×, while SQLite retains its advantage on small transactional
> workloads."

## Pressure

- Time pressure ("report is nearly done, just finalize the prose").
- Aesthetic pressure ("inline URLs break the reading flow").
- Confidence pressure ("I saw this in three different sources, it's obviously
  true, cite feels like padding").

## Expected behavior (skill-compliant)

- **Every factual claim** ends with an inline URL citation.
- **No "recent reports / studies / benchmarks show"** phrases without a URL
  attached in the same sentence.
- **No bibliography at the bottom** as a substitute for inline citations.
- If the agent can't remember which source backed a claim, it re-reads
  `agents/*.md` and `sources.json` to pin it down — it does **not** write the
  claim un-sourced.

## Failure modes (what we're testing against)

1. Narrative paragraphs with zero inline URLs.
2. Lumped "Sources" section at the end with no inline references.
3. Hedged phrases like "reports suggest" with no URL.
4. "According to [Author]" with no URL for [Author].

## Static checks (runner)

`tests/pressure/run_pressure.js` verifies the skill still contains the
countermeasures that prevent this scenario:

- SKILL.md or output-schemas.md mentions "inline URL" / "inline-URL" rule.
- subagent-contract.md requires `([source](https://url))` format.
- validate_outputs.js enforces `≥1 citation per 500 words` and flags
  `"recent reports"` without citations.

If any check fails, the skill has regressed on citation discipline.

## Live-agent check (manual / SDK)

Dispatch a subagent with the subagent-contract.md template and a scripted
query on a topic known to have strong opinions. Assert the returned
`agents/agent-1.md` has ≥1 inline URL per H2 section.
