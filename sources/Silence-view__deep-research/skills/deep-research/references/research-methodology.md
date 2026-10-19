# Research Methodology Reference

Detailed methodology guide for the deep-research skill. Read this file when you need specifics on search strategies, credibility scoring formulas, or citation chasing procedures.

---

## Table of Contents
1. [Search Query Engineering](#search-query-engineering)
2. [Source Credibility Scoring](#source-credibility-scoring)
3. [Citation Chasing Procedures](#citation-chasing-procedures)
4. [Evidence Triangulation Framework](#evidence-triangulation-framework)
5. [Agent Prompt Templates](#agent-prompt-templates)
6. [Quality Assurance Checklist](#quality-assurance-checklist)
7. [Source Bibliography](#source-bibliography)

---

## 1. Search Query Engineering

### Query Formulation Best Practices

Good research queries are specific, targeted, and diverse. Generate 2-3 queries per sub-question per agent type.

**Pattern 1: Exact Phrase + Domain Filter**
```
"multi-agent research" architecture site:arxiv.org 2025
```

**Pattern 2: Concept + Synonym Expansion**
```
"deep research" OR "comprehensive investigation" OR "literature survey" AI methodology
```

**Pattern 3: Author/Institution Targeting**
```
"Stanford" OR "MIT" OR "Google Research" [topic] 2024 2025
```

**Pattern 4: Problem-Oriented**
```
"challenges" OR "limitations" OR "problems with" [technology/approach]
```

**Pattern 5: Comparison Queries**
```
[A] vs [B] comparison benchmark performance 2025
```

**Pattern 6: Implementation-Focused**
```
"how to implement" OR "tutorial" OR "step by step" [specific technique]
```

**Pattern 7: Contrarian/Critical**
```
"criticism of" OR "against" OR "why not" [popular approach]
```

### Query Diversity Matrix

For each sub-question, ensure coverage across these axes:

| Axis | Variation 1 | Variation 2 | Variation 3 |
|------|-------------|-------------|-------------|
| Terminology | Technical jargon | Plain language | Acronyms |
| Recency | "2025 2026" | "latest" "recent" | No date filter |
| Source type | "site:arxiv.org" | "site:github.com" | General |
| Perspective | Best practices | Problems/limitations | Alternatives |
| Geography | English sources | Multi-language if relevant | Regional perspectives |

### YouTube-Specific Queries
When deploying the Video agent:
```
[topic] tutorial site:youtube.com
[topic] explained conference talk
[expert name] [topic] youtube
[topic] deep dive 2025
```

---

## 2. Source Credibility Scoring

### Scoring Dimensions (Detailed)

#### Authority (weight: 0.25)
Measures the expertise and reputation of the source/author.

| Score | Criteria |
|-------|----------|
| 0.95-1.0 | Peer-reviewed journal (Nature, Science, top-tier venue), Nobel laureate, major institution official doc |
| 0.85-0.94 | Top conference paper (NeurIPS, ICML, ICLR, ACL), recognized industry expert, official documentation |
| 0.70-0.84 | Established tech blog (Google AI Blog, Anthropic, OpenAI), well-cited researcher, major publisher |
| 0.50-0.69 | Medium/Substack by identified expert, company engineering blog, known community contributor |
| 0.30-0.49 | Personal blog with credentials, forum post by experienced user, unverified but detailed source |
| 0.10-0.29 | Anonymous source, unknown author, no visible credentials |
| 0.0-0.09 | Content farm, AI-generated slop, obvious misinformation site |

#### Freshness (weight: 0.15)
Measures temporal relevance. Apply time decay with domain-specific adjustments.

| Score | Criteria |
|-------|----------|
| 1.0 | Published within last 3 months (2026) |
| 0.9 | Published within last 6 months |
| 0.8 | Published within last 12 months (2025) |
| 0.6 | Published 1-2 years ago (2024) |
| 0.4 | Published 2-3 years ago (2023) |
| 0.2 | Published 3-5 years ago |
| 0.1 | Published 5+ years ago |

**Evergreen adjustment**: For foundational/seminal works that remain highly cited and relevant, add +0.3 to freshness score (cap at 0.8). Example: Wei et al. 2022 (CoT paper) gets 0.4 + 0.3 = 0.7 despite being from 2022.

#### Relevance (weight: 0.25)
How directly the source addresses the research sub-question.

| Score | Criteria |
|-------|----------|
| 0.9-1.0 | Directly and comprehensively answers the sub-question |
| 0.7-0.89 | Addresses the sub-question substantially but with gaps |
| 0.5-0.69 | Partially relevant — covers related topics with useful context |
| 0.3-0.49 | Tangentially relevant — some useful information but mostly off-topic |
| 0.1-0.29 | Barely relevant — only a sentence or two applies |

#### Evidence Quality (weight: 0.20)
The type and strength of evidence presented.

| Score | Criteria |
|-------|----------|
| 0.9-1.0 | Empirical data, benchmarks, randomized controlled experiments, meta-analyses |
| 0.7-0.89 | Case studies with data, observational studies, well-designed comparisons |
| 0.5-0.69 | Expert analysis with reasoning, theoretical frameworks with citations |
| 0.3-0.49 | Opinion with some supporting evidence, anecdotal but detailed |
| 0.1-0.29 | Pure opinion, unsupported assertions, marketing copy |

#### Peer Validation (weight: 0.10)
External validation of the source's claims.

| Score | Criteria |
|-------|----------|
| 1.0 | Published in peer-reviewed journal |
| 0.8 | Accepted at peer-reviewed conference |
| 0.6 | Highly cited preprint (>50 citations) or officially endorsed |
| 0.4 | Preprint with moderate citations, reviewed by community |
| 0.2 | Self-published, no external validation |

#### Independence (weight: 0.05)
Freedom from conflicts of interest.

| Score | Criteria |
|-------|----------|
| 1.0 | Independent researcher, no commercial ties to subject |
| 0.7 | Funded research with disclosed relationships |
| 0.5 | Company publishing about their own technology (acknowledged) |
| 0.3 | Promotional content disguised as analysis |
| 0.1 | Sponsored/paid content, undisclosed conflicts |

### Composite Score Calculation

```
composite = (authority * 0.25) + (freshness * 0.15) + (relevance * 0.25)
          + (evidence * 0.20) + (peer * 0.10) + (independence * 0.05)
```

### Tier Assignment
- **Tier 1**: composite >= 0.75 — Primary sources, anchor claims here
- **Tier 2**: composite 0.50-0.74 — Supporting sources, corroborate Tier 1
- **Tier 3**: composite 0.25-0.49 — Context/background only
- **Discard**: composite < 0.25 — Too low quality

---

## 3. Citation Chasing Procedures

### Backward Citation Chasing (Reference List Mining)

For each Tier 1 source:

1. **Extract references**: Identify all sources cited in the text
2. **Filter by relevance**: Select 3-5 most relevant to our research questions
3. **Search and retrieve**: Use WebSearch to find each cited work
4. **Evaluate**: Run through credibility scoring
5. **Integrate**: Add new evidence objects to the collection

**Priority for backward chasing**:
- Sources cited to support KEY claims (not just background references)
- Sources that appear in multiple Tier 1 reference lists (convergence signal)
- Sources from high-authority venues
- Seminal/foundational works cited by many

### Forward Citation Chasing (Who Cites This?)

For the most impactful sources:

1. **Search for citations**: Query `"[exact title]"` or `[author year] cited by`
2. **Check Google Scholar**: If accessible, find "cited by N" count
3. **Evaluate newer works**: These may update or supersede the original
4. **Integrate**: Add as evidence objects

**Priority for forward chasing**:
- Sources that are foundational to our key findings
- Sources published 2+ years ago (enough time for citations to accumulate)
- Sources where newer work might change conclusions

### Programmatic Citation Chasing (API-based)

When researching academic topics, use these APIs for systematic citation chasing
(more reliable than web search for citation networks):

**Semantic Scholar API** (free, no auth required for basic access):
- Forward citations: `GET https://api.semanticscholar.org/graph/v1/paper/{id}/citations`
- Backward references: `GET https://api.semanticscholar.org/graph/v1/paper/{id}/references`
- Search by title: `GET https://api.semanticscholar.org/graph/v1/paper/search?query={title}`

**OpenAlex API** (free, comprehensive):
- Forward: `cited_by` field on work objects
- Backward: `referenced_works` field
- Search: `GET https://api.openalex.org/works?search={query}`

**Usage in the skill**: Deploy a citation-chasing agent with instructions to call these
APIs via WebFetch when the topic is academic/scientific. This provides structured citation
graphs that web search cannot match.

### Citation Chain Tracking

Maintain a citation graph:
```
Original search -> Source A (Tier 1)
  -> backward: Source A cites Source B (new, Tier 1)
    -> backward: Source B cites Source C (new, Tier 2)
  -> forward: Source D cites Source A (new, Tier 1)
```

Maximum chase depth:
- Standard: depth 1 backward (A -> B)
- Deep: depth 2 backward + depth 1 forward (A -> B -> C, plus who cites A)
- UltraDeep: depth 2 backward + depth 2 forward (maximum expansion)

### Circular Citation Detection

Flag and discard when:
- A cites B AND B cites A (mutual citation)
- Three or more sources in a citation loop
- Multiple sources all trace to ONE original study without independent verification
- A "fact" is widely repeated but originates from a single blog post or press release

---

## 4. Evidence Triangulation Framework

### Claim Classification

| Type | Description | Verification Need |
|------|-------------|-------------------|
| Quantitative | Numbers, percentages, benchmarks | 2+ independent measurements |
| Qualitative | Expert opinions, best practices | 3+ independent experts |
| Methodological | How to do something | 2+ implementations/tutorials |
| Comparative | X is better than Y | Benchmarks + expert opinion |
| Causal | X causes Y | Experimental evidence preferred |
| Predictive | X will happen in the future | Multiple expert forecasts |

### Triangulation Protocol

For each major claim:

1. **Identify all sources that address this claim**
2. **Classify each source's position**: Supports / Contradicts / Neutral / Nuances
3. **Assess independence**: Are sources truly independent or do they share origins?
4. **Calculate consensus score**:
   - Full consensus (all agree): confidence = HIGH
   - Strong majority (>75% agree): confidence = STRONG
   - Mixed (50-75% agree): confidence = MODERATE
   - Split (roughly even): confidence = CONTESTED
   - Minority position (<25% support): flag as EMERGING or OUTLIER

5. **Apply evidence hierarchy**:
   Meta-analysis > RCT > Cohort study > Case study > Expert opinion > Anecdote

### Contradiction Handling

When sources conflict:

1. **Check methodology**: Is one source using better methods?
2. **Check scope**: Are they actually measuring the same thing?
3. **Check recency**: Has newer evidence superseded older?
4. **Check context**: Do they apply to different situations?
5. **Present both**: Always show the user the disagreement with evidence

---

## 5. Agent Prompt Templates

### Academic Research Agent

```
You are a specialized academic research agent. Find peer-reviewed papers,
preprints, and scholarly articles on the assigned sub-questions.

SEARCH STRATEGY:
- Use site:arxiv.org, site:scholar.google.com for academic sources
- Include conference abbreviations: NeurIPS, ICML, ICLR, ACL, EMNLP, CVPR
- Search for survey/review papers first (they aggregate many sources)
- Look for papers from known research labs (Stanford, MIT, Google, Anthropic, etc.)

SUB-QUESTIONS TO RESEARCH:
{assigned sub-questions}

SEARCH QUERIES TO EXECUTE:
{pre-generated queries}

For EACH source found, create an evidence object with all fields.
Target: {N} high-quality academic sources.
```

### Industry Best Practices Agent

```
You are a specialized industry research agent. Find real-world implementations,
case studies, benchmarks, and engineering best practices.

SEARCH STRATEGY:
- Target company engineering blogs (Google, Meta, Stripe, Netflix, etc.)
- Search for benchmark comparisons and performance data
- Look for production deployment case studies
- Find best practice guides from official documentation

SUB-QUESTIONS TO RESEARCH:
{assigned sub-questions}

For EACH source found, create an evidence object with all fields.
Target: {N} industry sources.
```

### Contrarian/Critical Agent

```
You are a contrarian research agent. Your job is to find criticism, limitations,
failures, and alternative viewpoints that the other agents might miss.

SEARCH STRATEGY:
- Search for "problems with [topic]", "criticism of [topic]"
- Look for failed implementations and postmortems
- Find debates and disagreements between experts
- Search for "why not [approach]", "[approach] considered harmful"

This perspective is CRITICAL for producing balanced research. The main agents
tend to find positive evidence. Your job is to find the counterarguments.

SUB-QUESTIONS TO RESEARCH:
{assigned sub-questions with contrarian framing}

Target: {N} critical/contrarian sources.
```

### Citation Chasing Agent

```
You are a citation chasing agent. Given high-credibility sources, find and
evaluate the sources THEY cite (backward) and sources that cite THEM (forward).

SOURCES TO CHASE:
{Tier 1 sources with cited_sources field}

BACKWARD CHASING:
For each source, search for its top 3-5 cited references.
Prioritize citations that support KEY claims, not background refs.

FORWARD CHASING:
For each foundational source, search for newer works that cite it.
Use queries like: "[title]" OR "[first author] [year]"

CREATE evidence objects for each new source found.
FLAG circular citations if detected.
Target: {N} new unique sources.
```

---

## 6. Quality Assurance Checklist

Before delivering the final report, verify:

### Citation Integrity
- [ ] Every factual claim has at least one citation
- [ ] Major claims have 3+ independent citations
- [ ] All cited URLs are real (not hallucinated)
- [ ] Citations actually support the claims they're attached to
- [ ] No circular citations treated as independent evidence

### Balance & Coverage
- [ ] All sub-questions from Phase 1 are addressed
- [ ] Contrarian/critical perspectives are included
- [ ] Contested claims present both sides
- [ ] No single source dominates the narrative
- [ ] Source diversity: mix of academic, industry, community

### Quality Metrics
- [ ] Total sources >= minimum for research mode
- [ ] Tier 1 sources >= 25% of total
- [ ] No major claim relies solely on Tier 3 sources
- [ ] Confidence levels assigned to all major findings
- [ ] Knowledge gaps explicitly identified

### Output Quality
- [ ] Executive summary captures top findings
- [ ] Sections are logically ordered
- [ ] Evidence hierarchy respected (strongest first)
- [ ] Methodology section explains how research was conducted
- [ ] Bibliography sorted by tier with credibility scores

---

## 7. Source Bibliography

### Research System Architecture
1. Shao et al. (2024) — "STORM: Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking", Stanford University
2. Co-STORM (2024) — Collaborative STORM with human-in-the-loop, Stanford OVAL
3. OpenAI (2025) — "Introducing Deep Research", Triage-Clarify-Instruct-Research architecture
4. Perplexity (2025) — Three-layer reranking with XGBoost, hybrid retrieval
5. LangChain (2025) — Open Deep Research, LangGraph-based modular pipeline
6. 199-Biotechnologies (2025) — 8-phase enterprise deep research skill for Claude Code

### Systematic Review Methodology
7. Haddaway et al. (2022) — "Citationchaser: A tool for transparent and efficient forward and backward citation chasing", Research Synthesis Methods
8. Briscoe (2020) — "Conduct and reporting of citation searching in Cochrane systematic reviews"
9. TARCiS Statement — Guidelines for citation searching in systematic reviews
10. PRISMA (2020) — Preferred Reporting Items for Systematic Reviews and Meta-Analyses

### Source Credibility Assessment
11. WebTrust (Tsinghua 2025) — Fine-tuned IBM Granite-1B for credibility scoring (MAE 0.09)
12. CRAAP Test — Currency, Relevance, Authority, Accuracy, Purpose framework
13. SIFT Method (Caulfield) — Stop, Investigate source, Find better coverage, Trace claims
14. ACM TOIS (2025) — Survey on Automatic Credibility Assessment of Textual Signals

### Multi-Agent Research
15. PRISM (2025) — Agentic retrieval with Question Analyzer + Selector + Adder
16. ReAgent (EMNLP 2025) — Reversible multi-agent reasoning with backtracking
17. MA-RAG (2025) — Multi-agent RAG with collaborative chain-of-thought
18. ReSP (ACM Web 2025) — Retrieve, Summarize, Plan iterative method
19. Du et al. (ICML 2024) — Multi-agent debate for factuality improvement

### Prompt Engineering
20. Wei et al. (NeurIPS 2022) — Chain-of-Thought prompting
21. Yao et al. (NeurIPS 2023) — Tree of Thoughts
22. Wang et al. (ICLR 2023) — Self-Consistency
23. Khot et al. (ICLR 2023) — Decomposed Prompting
24. Madaan et al. (NeurIPS 2023) — Self-Refine
25. Anthropic (2025-2026) — Claude Prompting Best Practices, Extended Thinking
