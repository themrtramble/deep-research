# Quantitative Reasoning & Risk

## Numbers discipline

Every quantitative statement needs: value + unit + date/condition +
baseline. Review your own numbers: "42" — of what, when, compared to
what? A number without a baseline is decoration.

- Prefer measured > derived > estimated > guessed — and say which.
- Show the arithmetic: "3 nodes x 2 replicas = 6 replicas" beats a bare 6.
- Order-of-magnitude sanity check every headline number against a known
  anchor (population, request rates, prices). If it's off by 1000x,
  something upstream is wrong.
- Percentages: name the base. "+80%" of what?
- Growth rates: check compounding illusions; "we'll grow 10%/month"
  is a 3x/year claim — is that even possible in this market?

## Fermi estimation (when data is missing)

Decompose into factors you can bound, multiply, show your work, give a
range not a point. State the weakest factor — it's usually the real
question. Mark every estimate `estimate:` so it survives into the
conclusions as what it is.

## Risk assessment

Failure-hypothesis table (fill `templates/failure-modes.md.tmpl`):

| ID | IF (trigger/condition) | THEN (consequence) | BECAUSE (mechanism) | Severity | Likelihood | Mitigation |
|---|---|---|---|---|---|---|

- Include MISUSE and ADVERSARIAL classes, not just accident classes.
- Severity uses the closed scale: low/medium/high/critical. Likelihood
  gets a reason ("happened twice last quarter" > "seems unlikely").
- Every mitigation traces back to a failure ID — no orphan mitigations,
  no mitigations for invented failures to look thorough.
- Pre-mortem: "it's 6 months later and this failed — write the postmortem
  in one paragraph." Those causes go in the table.

## Trade-offs and decisions

`decision-matrix.md` (template) requirements:
- alternatives x criteria, every cell filled, weights sum to 1.0, a
  verdict in prose.
- Include reversibility (one-way vs. two-way door) and a do-nothing
  baseline column where meaningful.
- The verdict names the deciding criteria: "B wins because criterion 3
  dominates, even though A wins criteria 1-2" — not "B is better".
- Watch for decision-theory traps: sunk cost (the matrix has no column
  for money already spent — by design), opportunity cost (what you stop
  doing by choosing this), status-quo bias (do-nothing must earn its
  place like any row), and committee aggregation (never average across
  incommensurable criteria without saying so).

## Sensitivity & scenarios

- Name the load-bearing variable; if it moved 2x either way, does the
  conclusion flip? If yes, the analysis is really about that variable.
- Where futures matter: 3 scenarios (expected / upside / stress), each
  with the observable trigger that tells you which world you're in.
