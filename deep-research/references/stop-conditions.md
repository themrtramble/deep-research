# Stop Conditions

Research terminates when additional effort has negative expected value.
The gates in `scripts/gates.py` compute coverage arithmetically; these
rules decide when to respect the stop.

## Stop when (any one, plus gates pass)

1. **Coverage**: every sub-question has either an answer with sufficient
   evidence, or a documented gap (what's missing and why it's unobtainable
   in-scope: paywalled, unpublished, nondisclosed).
2. **Saturation**: the last wave produced <15% novel claims for two
   consecutive waves — the search space is exhausted.
3. **Diminishing returns**: remaining budget is high-importance-only and
   those claims are already corroborated; extra sources add nothing.
4. **Budget exhaustion**: hop budget spent. Stop. Report honestly what
   remains open.

## Do NOT stop while

- A high-importance claim (>=4) lacks a contradict hop or second
  independence family — unless explicitly labeled `single-source`.
- An unresolved conflict affects the final answer.
- The report would fail `validate.py` on structure or citation density.

## The "never" rules

- Never keep searching just to spend the budget.
- Never declare "no information exists" after one failed search — record
  which searches failed and say "not found under these queries", not
  "does not exist".
- Never skip the verification phase to hit a deadline — mark the affected
  claims `unverified` instead and downgrade the answer status.

## Answer status semantics

- `fully-answered`: every sub-question resolved, high-importance claims
  corroborated and challenged, no material gaps.
- `partially-answered`: core resolved; named gaps remain.
- `unanswerable`: no reliable evidence obtainable (say WHY: paywalled
  everywhere, proprietary data, genuinely unstudied). Recommend what
  evidence would change this.

## Unanswerable ≠ failure

A well-evidenced "we could not answer this, and here is exactly what's
missing" is a valid research outcome — often the most valuable one.
