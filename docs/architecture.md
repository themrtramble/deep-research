# Architecture

## Design goal

Two skills, independently usable, interoperable through explicit JSON
contracts, zero third-party runtime dependencies, host-agnostic (any
agent that reads markdown and can run Python 3), and honest about
limits. All quality gates are computed mechanically from artifacts —
never self-reported by the model.

## Why this shape

The 29 audited sources cluster into four families:
1. **Pure protocol skills** (SKILL.md + references) — strong judgment
   rules, no enforcement.
2. **Script-backed skills** — deterministic helpers (validators,
   ledgers, classifiers) the agent must call.
3. **Heavy frameworks** — multi-agent runtimes; ideas portable, code not.
4. **Analysis frameworks** — perspective libraries, adversarial loops.

The unified design takes family 1+2 as the shape (skills are protocols
enforced by small deterministic tools) and mines family 3+4 for
mechanics. The result: judgment lives in SKILL.md + references
(progressive disclosure keeps context lean); verification lives in
stdlib-only Python scripts whose exit codes gate the workflow.

## deep-research pipeline

```
question ──▶ classify.py ──▶ mode + budgets + clarify? + refusal-check
   │
   ▼
ledger.py init (run dir: metadata, plan.md, 4 JSONL ledgers)
   │
   ▼
discovery waves ─▶ add-source / add-hop (DAG-validated, budget-capped)
   │                query playbook: broad/specific/contrarian/comparative
   ▼
evidence capture ─▶ add-evidence (claim ids, stance, quality, freshness,
   │                 independence, uncertainty; quote/locator required)
   ▼
verification ────▶ contradict hops + add-conflict (no forced resolution)
   │
   ▼
gates.py (arithmetic: sources, classes, families, counterevidence,
   │         waves) ──▶ stop / another wave
   ▼
report.md ───────▶ validate.py (sections, citation density, claim-matrix
   │                 ↔ ledger cross-ref, fabricated URLs, calibrated
   │                 language, secrets) + ledger.py lint
   ▼
package.py build ─▶ research-package.json (handoff contract)
```

Key invariants enforced mechanically:
- Evidence references only recorded sources; hops reference existing
  parents; ids are unique; secrets fail closed at every stage.
- High-importance claims require quote/locator + corroboration or an
  explicit `single-source` label; counterevidence search is expected and
  warned when absent.
- The report may not cite claim ids absent from the ledger, and
  high-importance ledger claims must appear in the report.

## deep-analysis pipeline

```
problem ──▶ frame (analysis-plan.md: real question, PRE-COMMITTED
   │          criteria, scope)        [gate: framing]
   ▼
first-principles (facts vs assumptions, 4 lenses) ─▶ assumptions.md
   │          dispositions            [gate: assumptions]
   ▼
evidence base (research-package.json if provided; respect uncertainty)
   │
   ▼
competing hypotheses ──▶ hypotheses.md (discriminators; statuses from
   │                      evidence, never preference) [gate: hypotheses]
   ▼
perspectives (4–10 roles, mandatory Devil's Advocate)
   │
   ▼
quantify + risk ─▶ decision-matrix.md / failure-modes.md [gates]
   │
   ▼
adversarial review ─▶ review-log.md (F1..Fn, dispositions, APPROVED/
   │                  REVISE/BLOCKED, ≤5 rounds, honest disagreement)
   ▼                   [gate: review-log]
conclusions.md ──▶ calibrate.py (silent-upgrade + unmeasured-language
                   lint) + analysis_gates.py (all artifacts)
```

Key invariants: criteria precede conclusions; assumptions are
dispositioned; unresolved hypotheses name their missing evidence;
findings are dispositioned with reasons; prose never exceeds declared
epistemic status.

## Interoperability

```
deep-research ──research-package.json──▶ deep-analysis
deep-analysis ──research-request.json───▶ deep-research (targeted follow-up)
```

- Both schemas are versioned (`/1`), fail-closed verified by the
  emitting skill, and self-describing (schema field).
- Loop bound: at most two request rounds before publishing residual
  uncertainty.
- Manual mode: the files travel by hand; each reference explains what to
  do with them.
- Independence: neither skill requires the other. Analysis without a
  package uses its own evidence discipline; research without analysis
  ships the package anyway.

## Security posture

- Retrieved content is data, never instructions (injection payloads are
  literal test fixtures).
- Secrets fail closed at lint, validate, and package time; redaction
  tooling provided.
- No repo code execution during research; no install-script execution.
- All writes confined to run directories; destructive ops need explicit
  user authorization.

## What is deliberately NOT here

Multi-model orchestration, MCP servers, semantic indexes, live
dashboards, overnight loops — out of scope for a dependency-free,
host-agnostic skill pair (rationale in capability-matrix.md).
