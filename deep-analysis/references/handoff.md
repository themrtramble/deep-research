# Handoff Contract (Deep Analysis side)

Both skills are independently usable. The handoff is a JSON artifact.

## Incoming: research-package.json (from deep-research)

Schema `deep-research-package/1` (see deep-research/references/handoff.md
for the full shape). Consumption rules:

1. Adopt `claims` as the evidence base; **respect uncertainty labels**
   — an `established` claim supports more than a `likely` one. Never
   upgrade a claim beyond its recorded status (calibrate.md enforces the
   register side; you enforce the input side).
2. `conflicts` with `status: unresolved` enter Phase 3 as competing
   positions — they are grist for hypotheses, not noise to be resolved
   by fiat.
3. `gaps` and `limitations` cap your confidence directly: conclusions
   that lean on a gap are `speculative` at best.
4. Where the package is stale or thin for a load-bearing question,
   request more evidence (below) rather than inventing it.

## Outgoing: research-request.json (to deep-research)

When a conclusion depends on missing EXTERNAL evidence, write:

```json
{
  "schema": "deep-analysis-request/1",
  "requests": [
    {
      "question": "targeted, answerable question",
      "why_needed": "which conclusion/hypothesis depends on it",
      "decision_at_stake": "what decision it unblocks or changes"
    }
  ]
}
```

Rules for good requests:
- One question per request; make it answerable by research (not "is X
  good?" but "what did independent benchmarks measure for X under Y?").
- Include the decision context — researchers prioritize and scope by
  what's at stake.
- If deep-research is unavailable, record the gap in hypotheses.md as
  unresolved with the reason; proceed with capped confidence and label
  conclusions that lean on the gap.

## Ordering with an orchestrator

Where the platform supports chaining (subagents, workflows):
`deep-research -> package.json -> deep-analysis -> (research-request.json
-> deep-research) -> final conclusions`. The loop runs at most twice;
after two rounds, publish the residual uncertainty honestly.

## Manual handoff

Without orchestration: tell the user which file to carry across:
"Run deep-research on this question, then give me package.json; I'll
finish the analysis on top of it" (and the reverse for requests). The
artifacts are self-describing — schema field included.
