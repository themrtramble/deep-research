# Research Protocol

The core discipline: a **hop** is a deliberate action that changes the
research graph — a new query angle, opening a promising source, verifying
a citation. Reading another paragraph is not a hop.

## Effort tiers

| Mode | Max hops | Min sources | Min classes | Wave cap |
|---|---|---|---|---|
| quick | 4 | 2 | 2 | 1 |
| standard | 10 | 5 | 3 | 3 |
| deep | 16 | 10 | 4 | 5 |
| exhaustive | 24 | 15 | 5 | 8 |

Adapt upward when the user explicitly asks for depth; never silently
downgrade below the classified mode.

## Plan pre-mortem (before searching)

Answer in `plan.md`, in one line each:
1. **Anchoring**: which first source could set a frame the rest copies?
2. **Missing voices**: who has direct incentive to dispute the consensus?
3. **Source homogeneity**: which domain dominates my query results likely?
4. **Scope drift**: what adjacent topic will tempt digression?
5. **Load-bearing assumption**: if my main sub-question rests on one
   definition or dataset, which is it?

## Sub-question decomposition

- 3–8 sub-questions for standard mode; more for deep/exhaustive.
- Mark each `INDEPENDENT` or `DEPENDS-ON <id>` — independent ones can run
  as parallel subagent workstreams where the host supports them.
- Each sub-question states what evidence would *disprove* the expected
  answer, not just confirm it.
- Distinguish "what is known" (facts) from "what is claimed" (vendor
  statements, preprints, anecdotes).

## Claim discipline

- Claim text is a single falsifiable sentence. No compound claims
  ("X is fast and cheap") — split them.
- `importance` 4–5 = the answer changes if this is wrong. 1–2 = color.
- `stance`: supports / contradicts / neutral — never shoehorn counterevidence
  as "supports" to keep the narrative clean.
- Correlation vs mechanism: record causal language as the SOURCE's claim
  ("the authors claim X causes Y"), and never as ledger-established fact
  unless the design supports it (experiment, natural experiment, mechanism
  verified independently).

## Conflict handling

- When two sources disagree on a material claim, add a conflict record —
  never silently pick a winner.
- Prefer primary over secondary; check dates and versions before assuming
  supersession (a newer doc is not automatically more correct).
- Unresolved conflicts appear in the report verbatim: "Source A says X
  (evidence E3); Source B says not-X (evidence E7); the disagreement is
  unresolved because <reason>."

## Wave mechanics

1. Before each wave, re-read open questions; never re-search a satisfied
   sub-question.
2. Hand off "ALREADY FOUND" dedup notes to any spawned searchers so waves
   don't repeat each other.
3. After each wave: `python scripts/ledger.py status <run_dir>` — checkpoint
   at 1/3 and 2/3 of hop budget; ask whether remaining questions are worth
   remaining budget.
4. Dead ends are recorded (`--status dead_end`), with one line on why —
   they prevent re-running the same trap in the next wave.

## Persistence & resumability

The run directory IS the state. To resume an interrupted session: read
`metadata.json` + `plan.md`, run `ledger.py status`, read `hops.jsonl`
tail, and continue from the last open question. Never redo completed hops.
