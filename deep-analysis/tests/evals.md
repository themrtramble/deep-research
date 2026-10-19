# Deep Analysis — Eval Scenarios

Agent-level scenarios for the SKILL.md protocol (live runner required).
Deterministic companions in `tests/` (pytest, offline).

| # | Scenario | Protocol behaviors under test | Pass criteria |
|---|---|---|---|
| A1 | First-principles: "should we rewrite our monolith in Rust?" | framing, pre-committed criteria, facts-vs-assumptions, 10x-simpler sweep | criteria written before conclusions; assumptions dispositioned; boring alternative (incremental optimization) genuinely considered |
| A2 | Competing hypotheses: "did the deploy or the traffic spike cause the outage?" | hypothesis table, discriminators, elimination | >=2 hypotheses with discriminators; status from evidence; no premature closure |
| A3 | Root cause: "our checkout conversion dropped 30% last week" | 5-Whys to mechanism, differential diagnosis | chain reaches an intervenable level; alternative chains ranked; measurement-artifact hypothesis checked |
| A4 | Trade-off: "Postgres vs MongoDB for our workload" | decision matrix, weights, verdict with deciding criterion | matrix complete, no empty cells, weights sum to 1.0, do-nothing baseline present, verdict names its criterion |
| A5 | Hidden assumptions & contradictions: analyze a plan whose premises conflict | assumption audit, contradiction surfacing | contradictions named, not smoothed; conflicting premises visible in conclusions |
| A6 | Risk: "we're launching this feature next week" | failure-hypothesis table incl. misuse/adversarial classes | severity/likelihood closed vocabulary; mitigations trace to IDs; pre-mortem paragraph |
| A7 | Uncertain evidence: analysis on thin/missing data | calibration, gap handling, research request | conclusions capped at speculative/likely; research-request.json well-formed OR gaps recorded |
| A8 | Adversarial review: review a confident-but-flawed draft conclusion | review-log mechanics, dispositions, verdict | findings numbered & dispositioned; rejected findings have reasons; verdict vocabulary respected |
| A9 | Quantitative: "will this infrastructure handle 10x growth?" | numbers discipline, Fermi decomposition, sanity anchors | every number has units/baseline or [unquantified]; Fermi shows factors; weak factor named |
| A10 | Withholding judgment: a genuinely undecidable 50/50 call | epistemic honesty | output says the evidence doesn't decide, names what would decide it — no coin-flip dressed as analysis |

## Judge notes

- An analysis that reaches the "right" answer by skipping pre-commitment,
  assumption dispositions, or adversarial review is a FAIL.
- A10's correct output is a withholding — grading it as "incomplete"
  misses the point of the skill.
- Integration cases: hand deep-research's package.json from scenario R2
  into A1 and verify uncertainty labels are respected end to end; verify
  A7's research-request is accepted and answerable by deep-research.
