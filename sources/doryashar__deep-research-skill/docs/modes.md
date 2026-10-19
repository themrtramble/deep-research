# Modes

## Summary

| | quick | standard | deep |
|---|---|---|---|
| Time budget | ~3 min | ~10 min | ~25+ min |
| Total sources | 3–6 | 10–20 | 20–40 |
| Subagents | 1 (inline) | 2–3 parallel | 4–5 parallel |
| Min sources / subagent | 3 | 5 | 6 |
| Max search rounds / subagent | 3 | 5 | 8 |
| Time / subagent | 180s | 480s | 900s |
| Critique passes | 0 | 1 | up to 3 |
| `evidence.jsonl` | no | no | yes |
| Default spawn cap | 1 | 10 | 30 |

## When each mode runs

The classifier picks a mode by scoring query keywords. See
`skill/references/classifier-heuristics.md` for the full rules. In brief:

- **quick** — factoid / definition queries, ≤ 8 words, phrases like "briefly"
  or "TL;DR", or explicit `--quick`.
- **standard** — default. Comparisons, how-tos, overviews that need 10–20
  sources.
- **deep** — "state of the art", "comprehensive landscape", "literature
  review", or a query that scores ≥ 3 on breadth + depth keywords.

## Mode-specific behavior

### quick

- No subagent dispatch. The main session runs the subagent-contract loop
  with `N=1, TOTAL=1`.
- No `evidence.jsonl`; inline citations in `report.md` are the evidence.
- No critique pass.
- Report length typically ≤ 400 words.

### standard

- 2–3 scoped subagents dispatched in parallel.
- Parent polls heartbeats every 60s for stuck detection.
- One critique pass runs the 3 personas on the draft; loop-back is
  **disabled** in standard (corrections applied inline, ship).
- `report.md` often includes a comparison table or numbered procedure.

### deep

- 4–5 scoped subagents dispatched in parallel.
- `evidence.jsonl` is required; each substantive claim gets a line.
- Up to 3 critique iterations. After each, the loop-back rule (see
  `stop-conditions.md`) decides whether to dispatch a targeted retrieval
  subagent or ship.
- Same-gap-twice → move to `## Known Limitations` and ship.
- Optional `--approve-outline`: pauses after `plan.md` for user approval
  before dispatching subagents (Weizhena-style gate).

## Quality bars

The validator (`validate_outputs.js`) enforces:

- Every mode: ≥ 1 H1, ≥ 1 inline URL citation per 500 words (min 3 total).
- Sources deduped by normalized URL.
- Evidence JSONL lines (when present) have required fields.
- Agents' workstream files have ≥ 1 H2 (skeleton-first evidence).

## Hard caps (protects token budget)

| Cap | Value | Why |
|---|---|---|
| `--max-spawns` | 1 / 10 / 30 by mode | Deep: 5 researchers × up to 3 critique loops × 3 personas + re-dispatch. |
| Total wall time | 2× the mode target | Runaway loop indicator. |

## Choosing a mode explicitly

When the classifier would pick the wrong mode, pass a flag:

- `--quick` — force quick (useful for contested-but-short queries)
- `--standard` — force standard
- `--deep` — force deep (useful when the query is terse but actually deep)

Explicit flags beat every other signal, including strong-deep keywords.

## Degraded host behavior

If the host has no subagent dispatch, standard and deep run the subagent
contract **sequentially** in the main session — one agent file at a time
instead of in parallel. Output layout and quality bars are unchanged; wall
time scales linearly with the number of agents.

See `docs/host-compatibility.md` for specifics.
