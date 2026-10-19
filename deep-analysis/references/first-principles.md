# First Principles & Assumption Audit

## Facts vs. assumptions

Build the table first, debate later:

| Statement | Status | Evidence | Confidence |
|---|---|---|---|
| "The DB is the bottleneck" | assumption | none yet | low |
| "Latency rose at 00:00" | verified fact | APM dashboard, claim CL-A2 | high |

Rules:
- A statement without an evidence pointer is an assumption — even if
  everyone in the room believes it.
- Confidence is grounded in evidence quality, not eloquence: `high`
  requires independent corroboration; `medium` a single decent source;
  `low` everything else.
- The deliverable lists claims that STILL need data/citation support —
  not silently.

## The four lenses

1. **Inherited vs. real assumptions** — for each load-bearing assumption:
   where did it come from (measurement, convention, habit, someone's
   blog)? Run the counterfactual: "what changes if this is false?" If
   the analysis survives, it wasn't load-bearing. If it collapses,
   it goes to the validation queue.
2. **Irreducible core** — strip the problem to what actually must hold.
   What are the REAL dependencies vs. ceremony? (A deployment is not a
   dependency; a working database is.)
3. **Systems view** — map the blast radius: what else moves when the
   component in question moves? Second-order effects, feedback loops,
  common-mode failures (the backup that shares the primary's power feed).
4. **Root cause vs. symptom** — the five-times test: ask "why" until the
   answer would have prevented the problem; the fix level for process
   failures is usually 4–5 (systemic), not 1–2 (proximate trigger).

## Mandatory challenges

- **Assumptions-to-Challenge table**: every high-impact assumption gets
  `validate | keep | discard`. "Keep" needs a reason (cheap to hold,
  reversible if wrong). Never leave high-impact assumptions implicit.
- **"What you haven't considered"**: sweep at least: a 10x-simpler
  alternative, a political/organizational cause, a measurement artifact
  (is the metric even true?), a compound failure (two small things), and
  an adversarial actor.
- **The Real Question reframe**: restate what the user actually needs to
  decide — "should we migrate?" often means "will the current thing
  survive the next 18 months?" Answer the real one.

## Effort calibration

Depth is calibrated to the smallest structure that exposes every
deliverable and integration point — not to how worried the user sounds.
A quick analysis that answers the real question beats a deep one that
answers an adjacent one. If the effort is 10x the stakes, say so.
