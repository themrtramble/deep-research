# Adversarial Review

A separate hostile pass over your own draft conclusions. Its job: find
what breaks, not to be agreeable. Mechanics adapted from bounded
adversarial-review protocols; the reviewer must not be the author's echo.

## Setup

- Review target: draft conclusions/recommendations + the criteria
  pre-committed in `analysis-plan.md`.
- Reviewer stance: skeptical, senior, time-pressed. Seek: wrong
  assumptions, logical inconsistencies, evidence-claim mismatches,
  unjustified leaps, missed alternatives, hidden risks, and the simplest
  thing that would invalidate the conclusion.
- Fresh context strongly preferred (subagent / new session). If
  self-review is unavoidable, re-read ONLY the written artifacts, not
  your memory of the reasoning.

## Round mechanics

Each round, the reviewer emits numbered findings `F1..Fn`, each with:
- the flaw (specific, quoted where possible)
- why it matters
- the minimal fix or the evidence that would change it

The author then dispositions EVERY finding, in writing:
- **accepted**: yes + the fix applied (or a pointer to where)
- **rejected**: no + evidence-backed reason (not annoyance)

Zero findings is valid — but must be stated explicitly ("I attempted to
break this and could not; here is where I probed hardest"). A reviewer
forced to find problems invents noise; a reviewer told to approve misses
real flaws.

## Verdicts (final word of each round)

- `APPROVED` — remaining concerns are documented as accepted limitations
- `REVISE` — specific findings must be addressed first
- `BLOCKED` — the analysis cannot support its conclusion as-is

Rules:
- Verdict vocabulary is closed; no "looks good to me".
- Approval binds to the reviewed artifact: change the conclusions, and
  the approval is void — re-review.
- Round cap: 5. If the cap hits without APPROVED: publish the
  disagreement — unresolved points with both positions — never fake
  convergence.
- The author is the FINAL ARBITER on substance: accept warranted
  findings, reject unwarranted ones with logged reasons. Sycophantic
  acceptance of a bad finding is as bad as defensive rejection of a
  good one.
- Malformed or empty review output fails closed: rerun the round.

## Anti-sycophancy checks (self-test before dispositioning)

- Did I reject any finding? If not, ask: is that because they're all
  right — or because agreeing is easier?
- Did I verify the reviewer's factual claims, or take them on authority?
- Am I defending the conclusion or the analysis? Only the latter is
  legitimate.
