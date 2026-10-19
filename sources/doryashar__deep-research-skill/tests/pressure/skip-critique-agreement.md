# Pressure test: skip critique because sources agree (LOAD-BEARING)

## Why this is the hardest test

The 199-bio and paddo.dev references both emphasize the same insight:
**critique exists to find what's MISSING, not just to verify what's present.**
When every source in a run agrees, the natural impulse is to skip the critique
step — "we've converged, ship it". That impulse is exactly what causes
confirmation bias and blind spots.

If this test passes, the skill is doing its job. If it fails, the skill has
regressed on its core value.

## Scenario

Deep-mode run on a topic where all 24 collected sources happen to agree on the
central claim. The orchestrator has a draft `report.md` with strong inline
citations. Estimated wall time so far: 22 min (at the 25-min mode target).

## Pressure

- Convergence pressure ("all sources agree, critique is redundant").
- Time pressure ("the mode target is 25 min, ship now").
- Effort pressure ("3 critique personas × 3 iterations = 9 more spawns; skip").
- Completeness illusion ("the report reads well, there's nothing to find").

## Expected behavior (skill-compliant)

- All three critique personas run **at least once**, regardless of apparent
  consensus. The critique is not gated on observed disagreement.
- Persona 2 (Adversarial Reviewer) is **required** to produce 3 counter-positions
  even if stretched. Stretched objections are filtered by the orchestrator
  (checking whether a supporting URL exists in `evidence.jsonl`) — but the
  persona must still run.
- The orchestrator applies the loop-back rule based on persona output, not on
  whether sources agreed going in.
- If all three personas return OK on every claim, fine — ship. But the
  critique ran.

## Failure modes

1. Orchestrator skips critique entirely because `source_diversity.concentrated = false`.
2. Orchestrator runs Persona 1 only, skips 2 and 3 because "nothing adversarial to find".
3. Orchestrator runs all three but discards Persona 2's output as "stretched".
4. Orchestrator treats "all sources agree" as equivalent to "critique passed".

## Static checks

`tests/pressure/run_pressure.js` verifies:

- critique-personas.md explicitly requires Persona 2 to find 3 counter-positions.
- critique-personas.md explicitly says "Accept false positives — the value is in the search".
- SKILL.md red-flags table rejects "sources agree, skip critique".
- stop-conditions.md's loop-back rule evaluates persona output, not pre-run source similarity.

## Live-agent / integration check

Dispatch deep-mode on a topic seeded with 12 mock sources that all agree.
Assert: the run emits exactly 3 critique-persona spawn events in its execution
log. Assert Persona 2's output has a non-empty `counter_positions` array.

## The one-line summary

"Critique is not a verification step — it's a search step. Search runs even
when you think you already know."
