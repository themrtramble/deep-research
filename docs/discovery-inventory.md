# Discovery Inventory

Audit conducted 2026-10-19. Every repository was cloned shallowly and
inspected on the filesystem (read-only; no install scripts or repo code
executed). "Verdict" reflects reuse value for this project.

## Original seeds (8/8 accessible, 0 inaccessible)

| # | Repository | License | Verdict |
|---|---|---|---|
| 1 | Weizhena/deep-research-skills | MIT (Lan Zheng) | duplicate of #2's base — analyzed once with #2 |
| 2 | jojocorse2b/deep-research-skill | MIT (Lan Zheng) | KEPT — evidence-first layer, schema gates, secret scan |
| 3 | B143KC47/deep-research-skill | MIT | KEPT — ledger backbone, eval suite, injection fixtures |
| 4 | hec-ovi/research-skill | MIT (Hector Oviedo) | KEPT — benchmark-tested protocol rules |
| 5 | TheAdamLabs/deep-research-skill | MIT declared, no file | ideas-only — pre-mortem, self-score loop, dashboard UX |
| 6 | doryashar/deep-research-skill | MIT (dyashar) | KEPT — classifier, subagent contract, stop conditions |
| 7 | alirezakarimi82/Deep-Research | **no license** | ideas-only (clean-room) — ranker, free-API pattern |
| 8 | zy839971925-zyy/Agent--deep-research-Workflow-Skills | MIT | KEPT — depth gates, provenance clusters, traceability |

## Additional seeds (9/9 accessible)

| # | Repository | License | Verdict |
|---|---|---|---|
| 9 | 199-biotechnologies/claude-deep-research-skill | MIT declared, no file | ideas-only — hash-ID evidence, deterministic claim checks |
| 10 | nraford7/deep-research | MIT (Noah Raford) | KEPT — citation-laundering detection, claim tags |
| 11 | comeonvictor/claude-code-deep-research | MIT | ideas-only — URL-verification taxonomy, QA scorecard |
| 12 | robertnowell/deep-research | MIT (Robert Nowell) | KEPT — validator + answer-status gates, angles mode |
| 13 | hashbulla/deep-research | MIT (hashbulla) | KEPT — verify_gates pattern, hash-before-trust, CRAG |
| 14 | ramit-mitra/deep-research-skill | MIT (Ramit Mitra) | ideas-only — convergence rule, leads[] re-planning |
| 15 | cyberelf/agent_skills | MIT | ideas-only — mode routing, raw/curated separation |
| 16 | Silence-view/deep-research | MIT (Andre) | KEPT — credibility rubric, citogenesis detection, validator |
| 17 | bntvllnt/agent-skills | MIT (bntvllnt) | KEPT — universal-analyzer framework inventory (analysis seed) |

## Discovered via GitHub search (12 cloned + inspected of 141 unique candidates)

Search coverage: 20 queries across research + analysis categories
("deep research skill", "deep-research claude skill", "deep research
agent", "multi-agent research", "autonomous research agent", "academic
research skill", "research synthesis agent", "source verification skill",
"evidence synthesis agent", "deep analysis skill", "universal analyzer
skill", "multi-perspective analysis skill", "critical thinking skill
claude", "root cause analysis agent", "reasoning skill claude",
"technical audit skill", "codebase analysis agent", "adversarial review
skill", "decision analysis agent", "deep-analysis").

| Repository | License | Verdict |
|---|---|---|
| mvanhorn/last30days-skill | MIT (Matt Van Horn) | KEPT — contract-style SKILL.md, query pre-flight, doctor audit |
| dzhng/deep-research | MIT (David Zhang) | KEPT — iterative learnings loop (breadth×depth) |
| wanshuiyin/Auto-claude-code-research-in-sleep (ARIS) | MIT (wanshuiyin) | ideas-only — autonomous markdown skills |
| SkyworkAI/DeepResearchAgent | MIT (AgentOrchestra lineage) | ideas-only — plan-decision rounds, completeness gates |
| assafelovic/gpt-researcher | Apache-2.0 | ideas-only — recursive tree, curator, HITL plan review |
| MiroMindAI/MiroThinker | Apache-2.0 | ideas-only — duplicate-query rollback, keep-K, post-mortems |
| bytedance/deer-flow | MIT (Bytedance + DeerFlow) | ideas-only — acceptance-criteria receipts, continuity |
| Leonxlnx/unlazy | MIT (Leonxlnx) | KEPT — gates/EXPECT/EVIDENCE, four-pass loop, ABANDON |
| zLanqing/codex-claude-academic-skills | MIT | KEPT — evidence labels, source-map discipline |
| Imbad0202/academic-research-skills | **CC BY-NC 4.0** | ideas-only — epistemic ladder, hallucination taxonomy |
| chaseai-yt/claudex-loop | MIT local / NOASSERTION metadata | ideas-only — bounded adversarial review mechanics |
| HughYau/AcademicForge | mixed / NOASSERTION | ideas-only — retrieve-first DOI verification |

## Excluded (inspected, judged not worth deep reuse)

129 of the 141 search candidates were triaged out after title/description/
license screening — dominant reasons: unrelated domain (ML time-series,
genomics, CV libraries), commercial SaaS without protocol substance,
near-forks of already-included repos, or content management systems. No
inaccessible seed repos were found (all 17 seeds cloned successfully).

## Fork/duplicate handling

Weizhena vs jojocorse2b are the same author's near-twins (jojo is a
strict superset with the evidence-first layer); analyzed once under #2.
Imbad0202's `-codex` variant (13.2k★) is the same content family —
covered by the main repo's audit.

## Limitations

- Search was GitHub-API only (no other forges); starred ranking biases
  toward popular, not necessarily protocol-strong, repos.
- Analysis depth for the 12 framework-grade repos was README +
  architecture + key modules, not line-by-line.
- Non-English-language skills (Korean, Chinese) were audited for
  protocol, not prose fidelity.
