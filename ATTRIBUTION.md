# Attribution

This project is a unified re-engineering. Its code was written fresh, but
specific mechanisms were **adapted** from third-party open-source works,
and many more informed the design (ideas only, no code or text copied).
All adapted components come from permissive licenses (MIT / Apache-2.0);
their required notices are preserved here and in file headers.

## Code/text adapted (with license compliance)

| Component | Adapted from | License | Copyright |
|---|---|---|---|
| Evidence/hop ledger CLI (ledger.py), secret patterns, injection-fixture design | B143KC47/deep-research-skill `research_ledger.py`, fixtures | MIT | (c) 2026 Deep Research contributors |
| Required-by-default schema gate, claim-granularity evidence chain, secret scan concepts, URL-normalization dedup (dedup.py) | jojocorse2b/deep-research-skill (validate_evidence.py, secret_scan.py, dedup logic) | MIT | (c) 2026 Lan Zheng |
| Task classifier scoring (classify.py) | doryashar/deep-research-skill `classify.js` | MIT | (c) 2026 dyashar |
| Report validator shape (validate.py) | Silence-view/deep-research `validate_report.py` + robertnowell/deep-research validator | MIT | (c) 2026 respective authors |
| Arithmetic-gates pattern (gates.py) | hashbulla/deep-research `verify_gates.py` | MIT | (c) 2026 hashbulla |
| Contract-style SKILL.md laws, query pre-flight traps | mvanhorn/last30days-skill | MIT | (c) 2026 Matt Van Horn |
| Depth gates / Ultra overlay / provenance clusters (concepts in research-protocol.md) | zy839971925-zyy/Agent--deep-research-Workflow-Skills | MIT | (c) 2026 zy839971925-zyy |
| Benchmark-tested protocol rules: contrarian pass, opening-attribution, storage discipline | hec-ovi/research-skill | MIT | (c) 2026 Hector Oviedo |
| Gates/EXPECT/EVIDENCE pattern, four-pass loop, ABANDON-with-reason (analysis_gates.py, references) | Leonxlnx/unlazy | MIT | (c) 2026 Leonxlnx |
| Evidence labels, source-map discipline (calibration.md, first-principles.md) | zLanqing/codex-claude-academic-skills | MIT | respective authors |
| Failure-hypothesis tables, perspective protocol, UltraThink concepts | bntvllnt/agent-skills `analyze` | MIT | (c) 2026 bntvllnt |

## Ideas-only sources (NO code or text copied — license unavailable or non-permissive)

Informed the design; nothing was copied; original implementations were written:

- **alirezakarimi82/Deep-Research** (no license file) — ranker concepts,
  free academic APIs pattern, config layering ideas.
- **Imbad0202/academic-research-skills** (CC BY-NC 4.0) — epistemic-status
  ladder & silent-upgrade detection (re-implemented from scratch in
  calibrate.py), citation hallucination taxonomy, pre-committed review
  criteria.
- **chaseai-yt/claudex-loop** (license metadata NOASSERTION) — bounded
  adversarial-review mechanics: verdict vocabulary, dispositioned findings,
  round caps (re-implemented in adversarial-review.md + analysis_gates.py).
- **199-biotechnologies/claude-deep-research-skill** (README declares MIT,
  no LICENSE file) — evidence hash IDs, canonical locators, deterministic
  claim-support checks.
- **TheAdamLabs/deep-research-skill** (README declares MIT, no LICENSE
  file) — plan pre-mortem, self-score patch loop, saturation stop signal.
- **comeonvictor/claude-code-deep-research** (MIT, Korean-language) —
  URL-verification taxonomy, 5-dimension QA scorecard.
- **ramit-mitra/deep-research-skill** (MIT) — convergence stop rule,
  leads[] re-planning.
- **cyberelf/agent_skills** (MIT) — mode routing, raw/curated evidence
  separation, signal-weight composites.
- Frameworks (architecture references, MIT/Apache-2.0): **gpt-researcher**
  (recursive breadth×depth tree, learnings accumulation, curator ranking),
  **MiroThinker** (duplicate-query rollback, keep-K observations, failure
  post-mortems), **deer-flow** (HITL clarification, acceptance criteria
  receipts, task continuity), **SkyworkAI/DeepResearchAgent** (plan-decision
  rounds, completeness gates), **dzhng/deep-research** (iterative
  learnings loop), **wanshuiyin/Auto-claude-code-research-in-sleep**,
  **HughYau/AcademicForge** (mixed licensing — retrieve-first DOI
  verification, verbatim-quote mandates).

## Full provenance

See `docs/capability-matrix.md` for the source-to-capability mapping and
`docs/discovery-inventory.md` for every repository audited, including
excluded ones.
