# ADR 0001 — Tiered modes (quick / standard / deep)

- **Status:** accepted, 2026-04-21
- **Supersedes:** n/a

## Context

We reviewed six existing deep-research skill implementations
(Weizhena, 199-biotechnologies, altmbr, paddo.dev, Smithery, MCPmarket).
They cluster into three shapes:

- **Lean parallel orchestrators** (altmbr): 2–4 subagents, inline citations,
  no critique. Ships in ~10 minutes.
- **Human-in-the-loop outline+fill** (Weizhena): outline approval gate,
  deep fill per item, structured JSON intermediate.
- **Enterprise pipelines** (199-bio): 8 phases, credibility scoring, 3-persona
  red-team, HTML/PDF render, runs ~30+ minutes.

No single shape fits every query. A factoid doesn't need 4 subagents or a
critique loop. A landscape review of a contested topic needs 20+ sources and
a red-team pass; cramming it into a 3-minute single-loop produces garbage.

## Decision

Ship three modes with an auto-classifier that picks among them:

| Mode | Time | Sources | Subagents | Critique |
|---|---|---|---|---|
| quick | ~3 min | 3–6 | 0 (inline) | none |
| standard | ~10 min | 10–20 | 2–3 | 1 pass |
| deep | ~25 min+ | 20–40 | 4–5 | up to 3 loops |

The classifier is a keyword-scoring heuristic, **not** an LLM call
(`skill/scripts/classify.js`). It returns a mode + score + `ambiguous` flag.
When ambiguous, the skill asks the user exactly once via `AskUserQuestion`,
then commits.

## Alternatives considered

### A single "deep" workflow that scales down via short-circuits

Reject: the short-circuit logic ends up just as complex as three explicit
modes, and users can't reason about "why did this query take 30 minutes?".

### A continuous depth dial (0.0 … 1.0)

Reject: cognitively harder for users. Discrete modes match how people think
about "quick answer" vs "thorough report".

### An LLM-based classifier

Reject for v1: adds 1–2s of latency per run and a cost tail; keyword scoring
gets us ~95% accuracy on the fixture set at zero cost. Flagged as future
work if the ambiguous band grows.

## Consequences

**Positive:**

- Every mode has clear quality bars (source counts, critique behavior) that
  the validator can enforce. No fuzzy "how deep was this run?".
- The classifier is cheap, deterministic, and unit-testable — `make test`
  covers 30+ query→mode cases.
- Users can override with `--quick`/`--standard`/`--deep`. Overrides beat the
  classifier unconditionally.

**Negative:**

- Keyword scoring is brittle on non-English and domain jargon. A query like
  "state of the union address analysis" contains "state of" and misclassifies
  as deep. Mitigation: explicit override, or fix the heuristic when a real
  query breaks.
- Three modes means three quality bars to maintain. Every pressure test has
  to consider "does this also apply in quick/standard/deep?".

## Known limitations

- The score bands (≤ −1 → quick, ≥ 3 → deep) are arbitrary thresholds
  tuned against a small fixture set. Expect to re-tune after real-world use.
- The ambiguous band (1..2, no strong anchor) currently catches very few
  queries. If we see significant drift in the classifier, an LLM fallback
  for the ambiguous band is the next step.
