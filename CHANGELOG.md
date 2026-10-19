# Changelog

## 1.0.0 (2026-10-19)

Initial unified release.

### deep-research
- Contract-style SKILL.md: 8-phase protocol (intake → plan → waves →
  evidence → verification → stop → synthesis → package) with 8 output laws.
- `ledger.py`: append-only run state (sources/hops/evidence/conflicts),
  effort-tier budgets, DAG-validated hops, fail-closed lint.
- `classify.py`: mode classification with explicit-override precedence,
  one-question ambiguity rule, dual-use refusal checks.
- `dedup.py`: URL normalization + same-domain near-title merge with
  provenance-cluster rationale.
- `validate.py`: report structure, citation density, claim-matrix ↔ ledger
  cross-reference, fabricated-URL heuristics, calibrated-language check.
- `gates.py`: arithmetic stop/coverage gates (computed, never
  self-reported) scaled by effort mode.
- `package.py`: research-package.json handoff builder + fail-closed
  verification (secrets, referential integrity, status semantics).
- References: research-protocol, source-quality, query-playbook,
  citation-verification, stop-conditions, security, handoff.
- 87 deterministic tests + 10 agent-level eval scenarios.

### deep-analysis
- Contract-style SKILL.md: 8-phase protocol (frame → decompose → evidence
  → hypotheses → perspectives → quantify/risk → adversarial review →
  conclusions) with 8 output laws.
- `calibrate.py`: epistemic calibration linter (silent-upgrade detection,
  unmeasured-language flags).
- `analysis_gates.py`: mechanical validators for framing pre-commitment,
  assumption dispositions, hypothesis statuses, decision matrices, failure
  modes, bounded adversarial review, research-request schema.
- References: first-principles, perspectives, causal-reasoning,
  adversarial-review, calibration, quantitative, handoff.
- 14 deterministic tests + 10 agent-level eval scenarios.

### Project
- Audited 29 source repositories across research/analysis ecosystems
  (full inventory and capability matrix in docs/).
- Zero third-party runtime dependencies (stdlib-only); no paid services.
