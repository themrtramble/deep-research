# Perspectives (Multi-Perspective Analysis)

Run the analysis through role lenses. Subagents/fresh contexts preferred
where the host supports them — self-play echoes your own blind spots.

## Core protocol per perspective

Each role returns, structured identically:
1. **Key points** — what this role sees first
2. **Core insight** — the one thing others would miss
3. **Gaps** — what's missing from the analysis so far
4. **Risks** — what could hurt, in this role's experience
5. **Assumptions** — what this role suspects is being taken for granted
6. **Improvements** — concrete changes
7. **Blind spots** — what even this analysis-and-role combination still
   can't see

Plus, for Deep mode: **dependencies, alternatives, timeline risks,
resource gaps, success metrics**, and a **failure-hypothesis table row**
(IF / THEN / BECAUSE / severity / mitigation).

## Role library (pick per domain, 4–6 standard, 6–10 deep)

- **Domain expert** — mechanism-level concerns, known failure modes
- **Operator/SRE** — what happens at 3am; runbooks, blast radius
- **Security/abuser** — how would a hostile user exploit this?
- **Economist/analyst** — incentives, hidden costs, second-order effects
- **Skeptical practitioner** — "has anyone actually done this
  successfully in production?"
- **Devil's Advocate** — MANDATORY: must produce the strongest case
  against the leading conclusion, even (especially) if it feels stretched
- **Future self (1yr/5yr)** — what will we regret / what becomes obvious
- **The maintainer** — who inherits this; documentation, complexity debt
- **The user** — actual usage vs. designed usage
- **Regulator/compliance** — where the rules constrain the design

## Synthesis mechanics

- Flag **divergent views** explicitly: "Operator says X; Economist says
  not-X" — do not average. State the tension and what would resolve it.
- **Consensus** requires 3+ independent perspectives converging; 2 is
  agreement, not consensus.
- Record **cross-cutting concerns** (security + cost + timeline hitting
  the same component).
- A perspective that finds nothing wrong must SAY so explicitly —
  silence is not approval.

## Temporal check

Run the "future you" lens on any irreversible decision: in one year,
would we still choose this? What would have to be true for the choice to
be wrong? Those conditions go into the monitoring/revisit list.
