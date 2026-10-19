# Calibration & Epistemic Status

Every conclusion carries an epistemic status. Prose may NEVER exceed it.
`scripts/calibrate.py` mechanically enforces the worst violations; the
rest is judgment.

## Status ladder

| Status | Meaning | Prose may say | Prose may NOT say |
|---|---|---|---|
| established | independently verified, reproducible | shows, demonstrates | (anything goes within honesty) |
| supported | good single-source evidence | indicates, supports | proves, definitely, certainly, guaranteed |
| likely | reasonable evidence, residual uncertainty | likely, probably | proves, definitely, guaranteed, establishes, confirms |
| preliminary | early evidence, small samples | suggests, hints | demonstrates, shows, confirms |
| speculative | hypothesis, extrapolation | might, could, one possibility | shows, demonstrates, proves |
| contested | credible sources disagree | "X claims... Y claims..." | any of the above as settled |
| weak/unknown | thin or no evidence | unknown, unclear | shows, demonstrates |

## Silent upgrades (the failure mode)

"Weak evidence proves the point" is the classic drift: the ladder status
says `weak`, the prose says "the data shows". Readers inherit false
confidence. Enforcement: declare status per conclusion (a status line or
table column), and match register. Unverifiable certainty in a conclusion
is a defect worse than admitted ignorance.

## Vague-language discipline

- "Significantly better" without a number is unmeasured language. Either
  quantify (40% lower latency, 120ms vs 200ms) or mark `[unquantified]`.
- Banned without measurement context: significantly, dramatically,
  substantially, vastly, "much/far better", "10x" without a derivation.
- Every number needs: units, a date/condition, and a baseline
  ("42" alone is a typo waiting to happen).
- Fermi estimates: show the decomposition (each factor + assumption) —
  a hidden estimate is a hidden assumption.

## Confidence statements

- Confidence is grounded: "high — because two independent primary
  sources", not "high" alone.
- Name what would change your mind, per conclusion.
- Uncertainty is asymmetric: note whether being wrong is cheap or
  catastrophic; confidence must shrink with stakes, not with vibes.
- Withholding a conclusion is valid: "the evidence does not support a
  verdict between H1 and H2" beats a coin-flip dressed as analysis.

## From analysis to recommendation

Recommendations inherit their supporting conclusions' status — a
`likely`-grade conclusion supports a "recommended, with monitoring for
X" — never a "we must". One-way vs. two-way doors: for one-way doors,
the status bar rises (speculative supports at most an experiment, not a
commitment).
