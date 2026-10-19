# Causal Reasoning & Hypothesis Testing

## Competing hypotheses (mandatory)

Every non-trivial explanation generates at least two COMPETING
hypotheses — including:
- the **boring explanation** (most likely a plain operational cause)
- **"my framing is wrong"** (the question itself assumes a falsehood)

For each hypothesis, fill `hypotheses.md`:

| Hypothesis | Status | Discriminating evidence | Notes |
|---|---|---|---|

The **discriminator** is the key field: an observation that differs
BETWEEN hypotheses ("lock waits appear in traces" discriminates lock
contention from traffic spike; both spike request latency). A hypothesis
without a discriminator is a belief, not a hypothesis.

Status assignment: `confirmed` (discriminating evidence found),
`eliminated` (discriminating evidence against), `unresolved` (missing
evidence — name it and why it's missing). Never mark unresolved
hypotheses confirmed to force closure.

## 5-Whys discipline

- Ask why until reaching a level where intervention prevents the whole
  class of failure — for process failures, that's usually level 4–5.
- Each level must be an actual mechanism, not a rephrase.
- Stop at the level where the fix would actually land; "human error" and
  "we need more training" are symptoms, not levels.
- Rank multiple candidate chains before settling: which chain explains
  ALL the observations, not just most?

## Elimination patterns

- **Necessary-condition elimination**: if H requires X and X is absent,
  H is dead (no traffic spike in APM kills the traffic hypothesis).
- **Timing analysis**: what changed, what stayed? A cause must precede
  its effect.
- **Differential diagnosis**: find a case where the failure did NOT
  happen and identify the differing factor.
- **Known-cause match**: compare against well-documented failure modes
  for the component class before inventing novel causes.

## Causal traps

- **Correlation laundering**: "X correlates with Y" becomes "X causes Y"
  in the retelling. Causal language requires mechanism + evidence, or an
  explicit "the causal direction is unestablished".
- **Survivorship**: analyzing only what arrived; ask what's missing from
  the sample by construction.
- **Common-mode mirage**: two "independent" systems failing together
  usually share a hidden dependency (clock, power, config service).
- **Post-hoc sequencing**: "we fixed X and it recovered" — check what
  else changed, and whether it self-recovered.
- **Confirmation cascade**: each confirming observation counts less if
  it's derived from the same underlying source.

## From diagnosis to verdict

Conclude with: ranked residual hypotheses, the confidence of each, what
monitoring/experiment would collapse the remaining uncertainty, and —
if this feeds a decision — the cost of being wrong.
