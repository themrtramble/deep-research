# Source-to-Capability Matrix

Traceability from each final capability to its origin(s), and the
integration decision. "Adapted" = mechanism reused with attribution
(permissive license). "Ideas-only" = concept re-implemented from scratch
(origin had no/unclear/non-permissive license).

## deep-research capabilities

| Final capability | Origin source(s) | Status | Integration decision |
|---|---|---|---|
| Effort-tier budgets (quick→exhaustive) | B143KC47 (MIT); zy839971925-zyy depth gates (MIT) | adapted | unified into one 4-tier ladder wired into classify.py + ledger |
| Append-only evidence/hop ledger, DAG-validated hops | B143KC47 research_ledger.py (MIT) | adapted | re-engineered to JSONL with claim-evidence chain |
| Required-by-default schema gate | jojocorse2b (MIT) | adapted | informs validate.py semantics |
| Claim-granularity evidence chain + conflict records | jojocorse2b (MIT) | adapted | conflicts.jsonl with resolved/unresolved semantics |
| Secret fail-closed scanning | jojocorse2b secret_scan (MIT), B143KC47 patterns (MIT) | adapted | dr_core SECRET_PATTERNS, wired into lint/validate/package |
| Prompt-injection defense + fixture | B143KC47 fixture (MIT) | adapted | fixture regenerated; defense rules in security.md + tests |
| Task classifier w/ explicit-override + ambiguity rule | doryashar classify.js (MIT) | adapted | rewritten in Python; added dual-use refusal checks |
| Subagent contract, heartbeats, saturation signal | doryashar (MIT), TheAdamLabs (ideas) | adapted | distilled into research-protocol.md wave mechanics |
| Stop conditions (<15% novel claims, budget, gates) | ramit-mitra (ideas), doryashar (MIT), hec-ovi (MIT) | adapted | stop-conditions.md + gates.py arithmetic |
| Source quality rubric, independence families | B143KC47 (MIT), zy839971925 provenance clusters (MIT) | adapted | source-quality.md; family = domain-level with vendor-family rule |
| URL-normalization dedup (syndication collapse) | doryashar dedup (MIT), jojocorse2b (MIT) | adapted | dr_core.dedup_sources + dedup.py |
| Citation hallucination taxonomy + citogenesis | Imbad0202 (CC BY-NC — ideas), nraford7 laundering detection (MIT) | ideas-only | citation-verification.md; no text copied |
| Weighted credibility rubric + cascade ratio | Silence-view (MIT) | adapted | source-quality.md rubric (weighted dimensions) |
| Report validator (structure, density, claim matrix) | Silence-view (MIT), robertnowell (MIT), hashbulla gates (MIT) | adapted | validate.py — merged checks from three validators |
| Arithmetic gates, never LLM-self-reported | hashbulla verify_gates (MIT) | adapted | gates.py |
| Contract-style SKILL.md laws + query pre-flight traps | mvanhorn last30days (MIT) | adapted | SKILL.md Output Laws; query-playbook pre-flight |
| Contrarian pass, opening-attribution rule | hec-ovi (MIT, benchmark-tested) | adapted | verification phase + Output Law 5 |
| Iterative learnings accumulation | dzhng (MIT), gpt-researcher (Apache-2.0 — ideas) | adapted | wave mechanics (learnings → next-wave queries) |
| Recursive breadth×depth descent | gpt-researcher (ideas) | ideas-only | wave structure; simplified for single-skill runtime |
| Duplicate-query rollback / keep-K retention | MiroThinker (ideas) | ideas-only | noted in wave mechanics; runtime-specific |
| Free academic APIs pattern | alirezakarimi82 (no license — ideas) | ideas-only | query-playbook mentions OpenAlex/S2/Crossref as free options |
| Answer-status gate | robertnowell (MIT) | adapted | package.py + validate.py statuses |
| Handoff package schema | original (informed by all sources) | new | package.py + handoff.md contracts |

## deep-analysis capabilities

| Final capability | Origin source(s) | Status | Integration decision |
|---|---|---|---|
| Universal-analyzer framework inventory | bntvllnt agent-skills analyze (MIT) | adapted | SKILL.md phases 1, 3, 4; perspectives library |
| Failure-hypothesis tables (IF/THEN/BECAUSE, misuse+adversarial) | bntvllnt (MIT) | adapted | quantitative.md + failure-modes template + gate |
| Gates/EXPECT/EVIDENCE mechanical contracts | Leonxlnx unlazy (MIT) | adapted | analysis_gates.py validates artifacts |
| Four-pass polish loop, ABANDON-with-reason | Leonxlnx (MIT) | adapted | adversarial-review.md honest-stopping rules |
| Bounded adversarial review (verdicts, dispositions, round caps) | chaseai-yt claudex-loop (ideas-only), claudex + unlazy (MIT parts) | ideas-only | adversarial-review.md + review-log gate |
| Epistemic ladder + silent-upgrade lint | Imbad0202 (CC BY-NC — ideas) | ideas-only | calibrate.py — original implementation |
| 4-way evidence labels, vague-adjective ban | zLanqing (MIT) | adapted | first-principles.md + calibrate unmeasured-language checks |
| Pre-committed evaluation criteria (anti-rationalize) | Imbad0202 (ideas), unlazy gates (MIT) | ideas-only | Phase 0 + framing gate |
| First-principles lenses, assumptions-to-challenge | bntvllnt (MIT) | adapted | first-principles.md |
| Hypothesis discriminators + elimination patterns | claudex-loop debugging refs (ideas), causal-reasoning research family | ideas-only | causal-reasoning.md |
| Depth calibration (smallest sufficient structure) | Leonxlnx (MIT) | adapted | SKILL.md effort calibration |
| Decision matrix with weights + verdict | decision-analysis family (bntvllnt, zLanqing) | adapted | decision-matrix template + gate |
| Fermi estimation + numbers discipline | quantitative.md family | new (informed) | quantitative.md |
| Retrieve-first DOI verification | HughYau AcademicForge (ideas-only) | ideas-only | citation-verification.md (research side) |
| Handoff contracts (both directions) | original | new | research-request.json + package consumption rules |

## Capabilities NOT integrated (and why)

- **Multi-model dispatch across 5 providers** (nraford7): powerful but
  cost-heavy ($5–150/run) and host-specific — documented as optional
  pattern, not built in; violates the free-components requirement.
- **MCP server packaging** (alirezakarimi82): no license, and single-host;
  skills here are host-agnostic by design.
- **Live dashboards as deliverable** (TheAdamLabs): presentation choice;
  kept markdown reports (portable, gateable); dashboard left as
  extension.
- **Overnight autonomous loops** (ARIS): runtime behavior, not a skill
  capability; the artifacts here are loop-compatible but the loop itself
  is out of scope.
- **Semantic search index / sqlite-vec** (nraford7): runtime dependency
  beyond stdlib-only constraint.
- **12-agent academic paper pipeline** (Imbad0202): NC license + domain
  specificity; only the evidence-integrity ideas were carried.
