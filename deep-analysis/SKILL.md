---
name: deep-analysis
description: >
  Rigorous analytical reasoning for complex problems: frames the problem,
  generates and eliminates competing hypotheses, audits assumptions, runs
  first-principles decomposition, applies multi-perspective and adversarial
  review, quantifies risk, and produces calibrated, defensible conclusions
  with explicit uncertainty. Use when the user asks to analyze, evaluate,
  diagnose, decide, compare, review, or find root cause — especially when
  the answer requires judgment over evidence. For discovering new external
  evidence, defer to deep-research.
license: MIT
version: 1.0.0
---

# Deep Analysis

You are executing a structured analysis protocol. Its purpose: conclusions
that survive adversarial scrutiny — not conclusions that feel right.
Load `references/*.md` per phase (progressive disclosure). Where the task
is primarily evidence-gathering rather than judgment, hand off to
`deep-research` instead.

## Activation

Activate for: root-cause analysis, design/spec review, hypothesis
evaluation, trade-off and decision analysis, risk assessment,
first-principles breakdowns, "why did this happen", "which option should
we pick", "poke holes in this plan".
Do NOT activate for: open-ended research ("what's known about X"),
simple lookups, or creative generation without an evaluation component.

If a deep-research handoff package (`research-package.json`) is provided,
load its claims/sources/conflicts as your evidence base in Phase 2.

## Phase 0 — Frame

Create an analysis run dir `analysis/<slug>-<date>/` with:

1. `analysis-plan.md` (template: `templates/analysis-plan.md.tmpl`) with:
   - **Problem framing**: the real question behind the stated one
     ("The Real Question" reframe — "what do you actually need to decide?").
   - **Pre-committed evaluation criteria**: fixed BEFORE analysis, they
     kill read-then-rationalize drift. Measurable, weighted where
     possible.
   - **Scope and boundaries**: in-scope, explicitly out-of-scope.
   - **Assumption and blind-spot inventory starters**.
2. Effort calibration: Quick (1–2 perspectives) / Standard (4–6) /
   Deep (6–10, mandatory adversarial round). Match to stakes; one-way-door
   decisions deserve Deep.

Do not begin analysis before criteria are written down.

## Phase 1 — Decompose (first principles)

From `references/first-principles.md`:
1. List verified facts vs. assumptions, each with evidence pointer
   (claim id, file:line, or "no evidence — assumption").
2. Apply the four lenses: inherited-vs-real assumptions (counterfactual:
   "what if this is false?"), irreducible core and actual dependencies,
   systems view (blast radius), root-cause-vs-symptom test.
3. Fill `assumptions.md` (template) — every row gets a disposition:
   `validate | keep | discard | unresolved`.

## Phase 2 — Evidence base

If a research package was provided: adopt its claims as your fact base —
respect its uncertainty labels (an `established` claim supports more than
a `likely` one; never upgrade a claim's status beyond its source's).

If evidence is missing for a load-bearing question: EITHER run
`deep-research` (when available) with a targeted
`research-request.json` (schema in `references/handoff.md`), OR record
the gap in `hypotheses.md` as unresolved with the reason. Never fill
gaps with plausible-sounding invented facts.

## Phase 3 — Competing explanations

Fill `hypotheses.md` (template): generate >=2 genuinely competing
hypotheses (including "the boring explanation" and "my framing is
wrong"). For each: what observation would DISCRIMINATE it from rivals;
then assign `confirmed | eliminated | unresolved` from the evidence —
never from preference. Unresolved requires the missing evidence named.

For causal chains (outages, failures): 5-Whys to mechanism level, ranked
hypotheses, and explicit elimination — see
`references/causal-reasoning.md`. Stop at the level where a fix would
actually land (usually 4–5 for process failures).

## Phase 4 — Perspectives

From `references/perspectives.md`: run 4–10 role lenses (domain expert,
operator, security/abuser, economist, skeptical practitioner, and the
mandatory **Devil's Advocate**). Each contributes: key points, core
insight, gaps, risks, assumptions, improvements, blind spots. Mark
divergent views and cross-cutting concerns; do not average them away.

## Phase 5 — Quantify & risk

From `references/quantitative.md` and `templates/failure-modes.md.tmpl`:
- Every comparative gets numbers with units, dates, and baselines —
  or an explicit `[unquantified]` marker. Fermi-estimate when data is
  missing (show the decomposition).
- Fill the failure-hypothesis table: IF / THEN / BECAUSE / severity /
  mitigation — including misuse and adversarial failure classes. Trace
  every mitigation back to a failure id.
- Decision problems: fill `decision-matrix.md` (alternatives x criteria,
  weights summing to 1.0, explicit verdict, reversibility noted).

## Phase 6 — Adversarial review

From `references/adversarial-review.md`: run a hostile review of your own
draft conclusions in `review-log.md`. Rules: findings numbered F1..Fn;
every finding dispositioned (accepted-with-fix or rejected-with-reason);
verdict vocabulary `APPROVED | REVISE | BLOCKED`; cap 5 rounds; if cap
hit without APPROVED — publish the disagreement honestly instead of
faking convergence. Zero findings must be stated explicitly.

## Phase 7 — Conclusions & QA

Write `conclusions.md` from `templates/conclusion-skeleton.md`:
calibrated language per `references/calibration.md`, epistemic status on
every conclusion, recommendations with priorities and measurable
acceptance criteria, and "what would change this conclusion".

Run the gates — all must pass before delivering:

```
python scripts/analysis_gates.py <run_dir> --json
python scripts/calibrate.py <run_dir>/conclusions.md
```

Fix violations honestly. Withholding a confident conclusion when evidence
doesn't support one is a PASS, not a failure.

## Output Laws

1. Criteria are pre-committed before conclusions exist — never written
   after the fact to fit.
2. Every conclusion carries an epistemic status, and prose never exceeds
   it (calibrate.py enforces mechanically).
3. Assumptions are dispositioned, not implied.
4. Competing hypotheses were genuinely considered and the discriminator
   between them is stated.
5. Adversarial findings are dispositioned with reasons; rejected findings
   need evidence, not annoyance.
6. Numbers have units, dates, baselines — or are marked unquantified.
7. What would change the conclusion is part of the conclusion.
8. When no defensible conclusion exists, say so — that IS the deliverable.

## Agent Hosts

File I/O + Python 3 shell required (stdlib-only scripts). Where a host
supports subagents, perspectives (Phase 4) and adversarial review
(Phase 6) gain independence by running in fresh contexts — recommended
but never required.
