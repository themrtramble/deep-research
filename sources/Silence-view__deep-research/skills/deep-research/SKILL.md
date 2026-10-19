---
name: deep-research
description: "Professional multi-agent deep research system that autonomously investigates any topic across 100+ sources with recursive citation chasing, source credibility scoring, evidence triangulation, and knowledge synthesis. Use this skill whenever the user asks to research a topic in depth, investigate something thoroughly, find comprehensive information, do a literature review, explore state-of-the-art on any subject, compare technologies or approaches with evidence, or needs a well-sourced report on any topic. Also trigger when user says 'deep research', 'ricerca approfondita', 'investigate this thoroughly', 'find everything about', 'comprehensive analysis of', 'what does the research say about', 'survey the literature on', 'state of the art', or any variation requesting thorough multi-source investigation. This skill deploys parallel research agents, validates every source, chases citations recursively (source of sources), cross-verifies claims across 3+ independent sources, and produces professional reports with full bibliography and credibility scores. Updates CLAUDE.md with relevant findings."
---

# Deep Research v1.0

## Overview

A professional-grade multi-agent research system that conducts autonomous deep investigation across 100+ sources, inspired by Stanford STORM, OpenAI Deep Research, and Perplexity's architecture. The system deploys parallel specialized agents, scores source credibility, chases citations recursively, triangulates evidence across independent sources, and synthesizes findings into professional reports with full bibliography.

**Core cycle:** Context Load -> Query Decomposition -> Research Planning -> Parallel Research Waves -> Credibility Scoring -> Recursive Citation Chasing -> Evidence Triangulation -> Synthesis -> Quality Assurance -> Output & Integration

**Key differentiators:**
- **100+ sources**: Multiple research waves with recursive expansion
- **Source of sources**: Backward and forward citation chasing up to 2 levels deep
- **Credibility scoring**: Every source scored on 6 dimensions (0-1 scale)
- **Evidence triangulation**: Major claims require 3+ independent corroborations
- **Multi-agent parallel research**: 5-8 specialized agents per wave
- **Dynamic skill communication**: Invokes yt-learner, paper, and other skills when relevant
- **CLAUDE.md integration**: Updates project context with research findings
- **Adaptive depth**: Scales from Quick (20 sources) to UltraDeep (150+ sources)

## When to Use

This skill activates on ANY request for thorough, multi-source research. The depth of investigation separates this from a simple WebSearch — this is a full research pipeline with validation, not a quick lookup.

## Language & Output Handling

- **Language**: Detect the user's language from their message. Write the report in the SAME language the user used. If the user writes in Italian, the report is in Italian. If English, in English. Research queries should use English (broader coverage) but the synthesis should match the user's language.
- **Output location**: For Standard+ modes, save the report to a markdown file and tell the user the path. For Quick mode, present inline unless the user requests a file.
- **File naming**: `{topic_slug}_deep_research_{date}.md` in the current working directory or user-specified path.

---

## Research Modes

| Mode | Sources | Agents | Depth | Duration | Best For |
|------|---------|--------|-------|----------|----------|
| Quick | 20-30 | 3 | 1 wave, no citation chasing | 2-5 min | Focused questions with clear scope |
| Standard | 50-70 | 5 | 2 waves + shallow citation chase | 5-15 min | General research topics |
| Deep | 80-120 | 6-8 | 3 waves + recursive citation chase | 15-30 min | Complex topics requiring depth |
| UltraDeep | 120-200+ | 8-10 | 4+ waves + deep citation chase + red team | 30-60 min | Critical decisions, literature reviews, state-of-art |

**Mode selection**: Infer from user's language. "Quick overview" -> Quick. "Everything about" -> Deep. "Comprehensive survey" / "literature review" -> UltraDeep. When uncertain, ask the user or default to Standard.

---

## Pipeline Execution (10 Phases)

### Phase 0: CONTEXT LOAD (inline, no subagent)

Before anything, load context to ground the research:

1. **Read CLAUDE.md** (if exists) — extract project context, tech stack, domain
2. **Check conversation history** — extract prior findings, user preferences, ongoing work
3. **Detect research domain** — classify: technical, scientific, business, creative, general
4. **Check for existing research** — look for prior research files in workspace to avoid duplication
5. **Load ROSETTA.md** (if exists) — extract user preferences for output format, depth, language

Build a `<research-context>` block passed to all subsequent agents.

### Phase 1: QUERY DECOMPOSITION (inline, with ultrathink)

Transform the user's research question into a structured research plan:

**1.1 Extract Core Question**
Identify the TRUE research question behind the user's request. Users often ask surface-level questions when they need deeper investigation. Use theory of mind to understand what they actually need.

**1.2 Perspective Discovery (STORM-inspired)**
Before generating sub-questions, discover diverse perspectives on the topic:
- Use WebSearch to find 3-5 existing articles/papers on the topic
- Extract the different angles and frameworks these sources use
- These perspectives guide sub-question generation to ensure comprehensive coverage

**1.3 Sub-Question Generation**
Decompose into 5-15 sub-questions organized by:
- **Foundational**: What is X? How does X work? (background knowledge)
- **State-of-art**: What's the latest research? What are current best practices?
- **Comparative**: How does X compare to Y? What are the tradeoffs?
- **Practical**: How is X implemented? What are real-world examples?
- **Critical**: What are the limitations? What do critics say? What can go wrong?
- **Forward-looking**: What's the future direction? What emerging trends exist?

**1.4 Complexity Assessment**
Based on sub-question count and topic breadth, confirm or adjust research mode.

**1.5 Check for Skill Synergies**
Scan available skills. If the topic aligns with a specialized skill (e.g., `paper` for academic LaTeX, `solana-dev` for blockchain, `claude-api` for Anthropic SDK), note it for Phase 9 integration.

### Phase 2: RESEARCH PLANNING (inline)

Create the research execution plan:

**2.1 Agent Assignment Matrix**

Map sub-questions to specialized agent types:

| Agent Type | Focus | Search Strategy | Sources |
|------------|-------|----------------|---------|
| Academic | Peer-reviewed papers, arxiv, surveys | "site:arxiv.org", "site:scholar.google.com", conference names | Papers, preprints |
| Industry | Best practices, case studies, benchmarks | Company blogs, engineering posts, benchmarks | Blog posts, docs |
| Documentation | Official docs, APIs, specifications | "site:docs.*", official URLs | Reference docs |
| Community | Discussions, real-world experience | "site:reddit.com", "site:news.ycombinator.com", forums | Forum posts |
| News | Recent developments, announcements | Date-filtered searches, news sites | Articles |
| Video | Tutorials, talks, deep dives | YouTube via yt-learner skill | Video transcripts |
| Contrarian | Criticism, limitations, failures | "problems with", "criticism of", "failed", "limitations" | Counter-evidence |

**2.2 Search Query Generation**
For each sub-question x agent type, generate 2-3 specific search queries. Good queries:
- Include domain-specific terminology
- Use quotation marks for exact phrases
- Include year filters for recency (2024-2026)
- Target specific high-quality sources

**2.3 Wave Planning**
Organize searches into waves:
- **Wave 1**: Broad survey (all agent types, foundational + state-of-art questions)
- **Wave 2**: Targeted deep-dive (fill gaps from Wave 1, chase promising leads)
- **Wave 3**: Citation expansion (forward/backward citation chasing)
- **Wave 4** (UltraDeep only): Adversarial verification + emerging research

### Phase 3: PRIMARY RESEARCH WAVE (Parallel Agents)

Deploy research agents using the Agent tool. Each agent runs as a background subagent with specific instructions.

**3.1 Agent Dispatch Protocol**

For each agent, provide:

```
You are a specialized {agent_type} research agent. Your task is to find high-quality,
credible sources on a specific research sub-question.

RESEARCH CONTEXT:
<research-context>
{from Phase 0}
</research-context>

YOUR ASSIGNMENT:
- Sub-questions: {assigned sub-questions}
- Search queries to execute: {pre-generated queries}
- Target source count: {N sources}
- Source types to prioritize: {types}

INSTRUCTIONS:
1. Execute each search query via WebSearch
2. For each promising result, use WebFetch to extract key findings
3. For EACH source, record a structured evidence object:

EVIDENCE OBJECT FORMAT:
- source_url: the URL
- source_title: title of the page/paper
- source_type: academic|industry|documentation|community|news|video
- source_date: publication date (extract or estimate)
- author: author name(s) if identifiable
- key_findings: 2-5 bullet points of relevant findings
- direct_quotes: 1-3 verbatim quotes with context
- relevance_to_question: which sub-question(s) this addresses
- cited_sources: list any sources THIS source cites that look promising (for citation chasing)
- credibility_signals: {
    domain_authority: known reputable source? (high/medium/low/unknown)
    author_credentials: identifiable expert? (yes/partial/no)
    peer_reviewed: (yes/no/n-a)
    recency: publication year
    citation_count: if visible (number or "unknown")
    cross_referenced: does other evidence support these claims? (yes/partial/no)
  }
- citation_chain: "search"  # how you found this source (always "search" for Wave 1)
- NOTE: Do NOT compute numeric credibility_score or tier — the coordinator assigns these in Phase 4

4. If a search returns poor results, reformulate the query and try again (up to 2 retries)
5. If you discover an unexpectedly rich source, explore it deeply rather than moving on

CRITICAL INSTRUCTION (place at end for maximum attention):
Return ALL evidence objects as a structured list. Aim for {N} sources minimum.
Include a brief "Gaps Identified" section listing what you couldn't find.
Use the ReAct pattern: Think about what you know -> Search -> Observe results -> Think about gaps -> Search again.
```

**3.2 Parallel Dispatch Rules**
- Launch ALL Wave 1 agents in a SINGLE message (parallel execution)
- Use `run_in_background: true` for agents that aren't blocking the next step
- Each agent should target 8-15 sources
- Total Wave 1 target: 40-60 sources across all agents

**3.3 Video Research (yt-learner integration)**
If a Video agent is deployed, it should:
1. Use WebSearch to find relevant YouTube URLs
2. For each video, invoke the `yt-learner` skill to extract structured notes
3. Video content is especially valuable for tutorials, conference talks, and expert explanations

**3.4 While Agents Work**
While Wave 1 agents execute in background:
- Do your own targeted searches on the most critical sub-questions
- Read any existing research files in the workspace
- Prepare the credibility scoring framework for Phase 4

### Phase 3.5: WAVE 2 TARGETED DEEP-DIVE (Standard+ modes only)

After Wave 1 agents return and you've done initial gap analysis:

**3.5.1 Gap Identification**
Review all Wave 1 evidence objects. Identify:
- Sub-questions with fewer than 3 sources
- Sub-questions with only Tier 3/low-quality sources
- Promising leads mentioned in agents' "Gaps Identified" sections
- Unexpected angles discovered that merit deeper investigation

**3.5.2 Query Refinement**
For each gap, reformulate queries using the Adaptive Query Refinement protocol:
- Try different terminology (if technical jargon failed, try plain language)
- Try different source types (if academic didn't work, try industry/community)
- Narrow or broaden scope based on what Wave 1 returned
- Include findings from Wave 1 as context: "Given that [Wave 1 finding], search for [refined query]"

**3.5.3 Wave 2 Agent Dispatch**
Deploy 2-3 targeted agents (fewer than Wave 1, more focused):

```
You are a targeted deep-dive research agent. Wave 1 research has been completed
on [topic]. Your job is to fill specific gaps and explore promising leads.

WAVE 1 FINDINGS SUMMARY:
{brief summary of what was already found}

GAPS TO FILL:
{specific sub-questions that need more/better sources}

PROMISING LEADS TO EXPLORE:
{sources or angles discovered in Wave 1 that deserve deeper investigation}

ALREADY FOUND (do NOT re-find these):
{list of URLs already collected — avoid duplicating}

Search queries: {refined queries targeting gaps}
Target: {N} new unique sources that fill the identified gaps.
Use ReAct: Think about what's missing -> Search -> Observe -> Refine -> Search again.
```

**3.5.4 Serendipity Integration**
If Wave 1 agents found something unexpected but valuable, generate 1-2 new sub-questions to explore that direction in Wave 2. The best research often follows unexpected leads.

---

### Phase 4: SOURCE CREDIBILITY ASSESSMENT (inline)

When Wave 1 agents return, score every source:

**4.1 Credibility Scoring Framework**

Score each source on 6 dimensions (0.0 to 1.0):

| Dimension | Weight | Scoring Guide |
|-----------|--------|---------------|
| **Authority** | 0.25 | Known institution/expert=0.9+, Established blog=0.6-0.8, Unknown=0.3-0.5, Anonymous=0.1-0.2 |
| **Freshness** | 0.15 | 2026=1.0, 2025=0.8, 2024=0.6, 2023=0.4, 2022=0.2, older=0.1 (add +0.3 for evergreen seminal works, cap 0.8) |
| **Relevance** | 0.25 | Directly answers sub-question=1.0, Partially relevant=0.5-0.7, Tangentially=0.2-0.4 |
| **Evidence Quality** | 0.20 | Empirical data/benchmarks=0.9+, Cited claims=0.7, Opinion with reasoning=0.5, Pure opinion=0.2 |
| **Peer Validation** | 0.10 | Peer-reviewed journal=1.0, Conference paper=0.8, Cited by many=0.6, Not validated=0.3 |
| **Independence** | 0.05 | No conflict of interest=1.0, Potential bias noted=0.5, Promotional=0.2 |

**Composite Score**: `authority*0.25 + freshness*0.15 + relevance*0.25 + evidence*0.20 + peer*0.10 + independence*0.05`

**4.2 Source Tiers**
- **Tier 1** (score >= 0.75): Primary sources — anchor claims on these
- **Tier 2** (score 0.50-0.74): Supporting sources — corroborate Tier 1
- **Tier 3** (score 0.25-0.49): Context sources — useful background, not for claims
- **Discard** (score < 0.25): Too low quality to include

**4.3 Deduplication**
Remove sources that:
- Share the same underlying data/study (keep the primary publication)
- Are mirrors or reposts of the same content
- Cite each other circularly without independent evidence

### Phase 5: RECURSIVE CITATION CHASING (Parallel Agents)

The "source of sources" expansion. This is what separates professional research from surface-level searching.

**5.1 Backward Citation Chasing**
For each Tier 1 source (credibility >= 0.75):
- Extract all cited sources mentioned in the text
- Identify the most promising 3-5 citations per source
- Search for these cited works via WebSearch
- Fetch and evaluate them through the same credibility pipeline

**5.2 Forward Citation Chasing**
For the most important findings:
- Search for "who cites this paper/article"
- Use queries like: `"[paper title]" cited by` or `"[author] [year]" references`
- This reveals newer work that builds on foundational sources

**5.3 Chase Depth**
- **Standard mode**: 1 level backward only (A -> B)
- **Deep mode**: 2 levels backward + 1 level forward (A -> B -> C, plus who cites A)
- **UltraDeep mode**: 2 levels backward + 2 levels forward (maximum expansion)

**5.4 Agent Dispatch for Citation Chasing**
Deploy 2-4 citation-chasing agents in parallel:

```
You are a citation-chasing research agent. Given a set of high-credibility sources,
your job is to find and evaluate the sources THEY cite (backward chasing) and
sources that cite THEM (forward chasing).

HIGH-CREDIBILITY SOURCES TO CHASE:
{list of Tier 1 sources with their cited_sources fields}

FOR EACH SOURCE:
1. Backward chase: Search for the top 3-5 cited works
2. Forward chase: Search for "[title]" + "cite" or "[author year]"
3. For each found source, create an evidence object (same format as Phase 3)
4. Note the citation chain: Source A -> Source B -> Source C

CRITICAL: Do NOT just re-find the same sources. The goal is to EXPAND
the knowledge base with sources we haven't seen yet.

TARGET: {N} new unique sources from citation chasing.
```

**5.5 Programmatic Citation Chasing (when available)**
For technical topics, leverage APIs for systematic citation chasing:
- **Semantic Scholar API**: `GET /paper/{paper_id}/citations` (forward) and `/references` (backward)
- **OpenAlex API**: `referenced_works` and `cited_by` fields
- These APIs provide structured citation graphs — far more reliable than web search for academic sources

**5.6 Circular Citation Detection**
Flag when:
- Source A cites B, B cites A (mutual citation — use graph cycle detection)
- Multiple sources trace back to the same single original study (citogenesis)
- A "fact" appears widely cited but originates from a single unverified claim (information cascade)
- The cascade ratio (unique original sources / total citations) drops below 0.3 — this indicates most "sources" are just echoing one original

### Phase 6: EVIDENCE TRIANGULATION (inline, with ultrathink)

Cross-verify findings across independent sources. This is where research quality is built.

**6.1 Claim Extraction**
From all collected evidence, extract distinct claims:
- Factual assertions ("X increases Y by Z%")
- Best practice recommendations ("Use A instead of B because...")
- Consensus positions ("Most experts agree that...")
- Contested claims ("Some argue X while others argue Y")

**6.2 Triangulation Matrix**
For each major claim, build a support matrix:

```
CLAIM: [specific claim]
SUPPORTING SOURCES:
  - Source A (Tier 1, score 0.85): [evidence quote]
  - Source C (Tier 1, score 0.78): [evidence quote]
  - Source F (Tier 2, score 0.62): [evidence quote]
CONTRADICTING SOURCES:
  - Source D (Tier 2, score 0.55): [contradicting evidence]
CONFIDENCE: HIGH (3 Tier 1 sources agree, 1 Tier 2 dissent)
```

**6.3 Confidence Levels**
- **Verified** (3+ independent Tier 1 sources agree): Present as established fact
- **Strong** (2 Tier 1 + 1 Tier 2 agree): Present with high confidence
- **Moderate** (1 Tier 1 + multiple Tier 2): Present with caveats
- **Emerging** (1-2 sources, recent): Present as emerging finding
- **Contested** (sources disagree): Present all perspectives with evidence
- **Unverified** (single source only): Flag clearly, recommend further investigation

**6.4 Evidence Aggregation (Dempster-Shafer inspired)**
For quantitative confidence assessment, use a simplified belief function approach:
- Each source contributes a "belief mass" proportional to its credibility score
- When sources agree: beliefs combine multiplicatively (stronger than either alone)
- When sources conflict: the conflicting mass is redistributed proportionally
- Result: a composite confidence score that accounts for both agreement AND source quality

**6.5 Contradiction Resolution**
When sources conflict:
1. Compare credibility scores — higher-credibility source gets more weight
2. Check recency — newer research may supersede older
3. Check methodology — empirical > theoretical > opinion
4. Check independence — are they truly independent or sharing an origin? (cascade detection)
5. Present both sides in output with evidence for each
6. Note the disagreement explicitly — contradictions are often the most valuable findings

### Phase 7: SYNTHESIS & KNOWLEDGE CONSTRUCTION (inline, with ultrathink)

Build structured knowledge from verified evidence.

**7.1 Hierarchical Outline**
Create a multi-level outline covering:
- Executive summary (key findings in 3-5 sentences)
- Background/context
- Main findings (organized by sub-question or theme)
- Comparative analysis (if applicable)
- Practical implications
- Limitations & knowledge gaps
- Future directions
- Methodology note (how this research was conducted)

**7.2 Evidence Weaving**
For each section:
- Lead with the strongest evidence (Tier 1 sources)
- Support with corroborating evidence
- Acknowledge contradictions and alternative views
- Include direct quotes for critical claims
- Cite every claim with [source_number] notation

**7.3 Knowledge Gaps Identification**
Explicitly identify:
- Sub-questions that couldn't be fully answered
- Areas where only low-credibility sources were found
- Topics that need primary research (not available via web search)
- Emerging areas with insufficient published material

### Phase 8: QUALITY ASSURANCE (Critic Agent)

Deploy a QA agent to red-team the synthesis using **Chain-of-Verification** (CoVe) — the #2 ranked prompting technique for research verification.

```
You are a research quality assurance critic. Your job is to find flaws
in a research synthesis before it's delivered to the user.

VERIFICATION METHOD: Chain-of-Verification (CoVe)
For each major claim in the report:
1. Generate a specific verification question
2. Answer the question independently (without looking at the claim)
3. Compare your independent answer with the claim
4. Flag any discrepancies

RESEARCH REPORT DRAFT:
{full synthesis from Phase 7}

SOURCE EVIDENCE:
{all evidence objects with credibility scores}

CHECK EACH OF THESE:

1. HALLUCINATION CHECK
   - Does every factual claim trace back to a specific source?
   - Are any claims made without evidence?
   - Are any quotes fabricated or distorted?

2. CITATION INTEGRITY
   - Is every [source_number] reference real and accessible?
   - Do the citations actually support the claims they're attached to?
   - Are there claims that should be cited but aren't?

3. BIAS CHECK
   - Is the report balanced or does it favor one perspective?
   - Are contrarian views fairly represented?
   - Is there selection bias in which sources were emphasized?

4. COVERAGE CHECK
   - Are all sub-questions from Phase 1 addressed?
   - Are there obvious angles that were missed?
   - Is the depth proportional to importance?

5. RECENCY CHECK
   - Are outdated findings presented as current?
   - Are newer studies that supersede older ones acknowledged?

6. LOGICAL CONSISTENCY
   - Do the conclusions follow from the evidence?
   - Are there internal contradictions in the report?

OUTPUT: For each check, provide:
- PASS/FAIL/PARTIAL
- Specific issues found (with references)
- Suggested fixes

If critical issues found, flag them as MUST-FIX.
If minor issues found, flag as SHOULD-FIX.
```

**8.1 Fix Loop**
If the QA agent finds MUST-FIX issues:
1. Fix them immediately
2. If the fix requires new evidence, dispatch a targeted search agent (delta-query)
3. Re-run QA on the fixed sections only
4. Maximum 2 fix iterations

### Phase 9: OUTPUT & INTEGRATION

**9.1 Report Generation**

Generate the final report in this structure:

```markdown
# [Research Topic] — Deep Research Report

> Conducted: [date] | Mode: [Quick/Standard/Deep/UltraDeep]
> Sources analyzed: [N] | Credibility threshold: [tier]
> Evidence confidence: [overall assessment]

## Executive Summary
[3-5 sentences capturing the most important findings]

## Key Findings

### [Finding 1 Title]
[Detailed finding with evidence citations]

**Evidence confidence:** [Verified/Strong/Moderate/Emerging/Contested]
**Sources:** [1], [3], [7], [12]

### [Finding 2 Title]
...

## Comparative Analysis
[If applicable — structured comparison with evidence]

## Practical Implications
[What this means for the user's specific context/project]

## Limitations & Gaps
[What this research could not answer and why]

## Future Directions
[Emerging trends and areas to watch]

## Methodology
This research was conducted using [N] parallel research agents across [M] search
waves. Sources were scored on 6 credibility dimensions and claims were triangulated
across [K]+ independent sources. Citation chasing expanded the source base by [X]%.

## Bibliography

### Tier 1 Sources (Credibility >= 0.75)
1. [Author(s)]. "[Title]". [Source/Publication], [Date]. [URL]. Credibility: [score]
2. ...

### Tier 2 Sources (Credibility 0.50-0.74)
N. [Author(s)]. "[Title]". [Source/Publication], [Date]. [URL]. Credibility: [score]
...

### Tier 3 Sources (Context/Background)
M. ...
```

**9.2 CLAUDE.md Integration**
After generating the report, check if findings are relevant to the current project:
- If the research topic directly relates to the project in CLAUDE.md:
  - Propose specific additions to CLAUDE.md (architecture insights, best practices discovered, new conventions)
  - Only update with user approval
- If the research produced reusable reference material:
  - Save to a reference file in the project
  - Add a pointer in CLAUDE.md

**9.3 Dynamic Skill Invocation**
If the output needs post-processing:
- Academic paper format -> invoke `paper` skill if available
- Code implementation guide -> invoke relevant development skill
- Presentation/slides -> note this for user
- The skill communicates with other skills by checking the skill registry and invoking them via the Skill tool

**9.4 Memory Update**
If research findings include information worth remembering across sessions:
- Save key findings to the auto-memory system
- Update ROSETTA.md with research patterns that worked well

### Phase 10: POST-RESEARCH DEBRIEF (inline)

Present results to user with:

```
--- DEEP RESEARCH COMPLETE ---
Topic: [research topic]
Mode: [mode used]
Sources analyzed: [total N] (Tier 1: [n1], Tier 2: [n2], Tier 3: [n3])
Citation chains explored: [N chains, M levels deep]
Evidence confidence: [overall]
Report: [inline (Quick mode) | saved to: file path (Standard+)]

Key findings summary:
1. [Finding 1 - one sentence]
2. [Finding 2 - one sentence]
3. [Finding 3 - one sentence]

[If relevant to project]: Proposed CLAUDE.md updates ready for your review.
---
```

Note: For Quick mode with inline output, omit "saved to" line. For Standard+ modes, always save to file.

---

## Progress Communication Protocol

During long research sessions (Standard+), keep the user informed at natural milestones. Research that takes 10+ minutes without updates feels broken, even if it's working perfectly.

### Progress Banners

Display at these checkpoints:

**After Phase 1 (Query Decomposition):**
```
--- DEEP RESEARCH INITIATED ---
Topic: {topic}
Mode: {mode} | Sub-questions: {N} | Perspectives: {M}
Deploying {N_AGENTS} research agents...
---
```

**After Wave 1 completes:**
```
--- WAVE 1 COMPLETE ---
Sources found: {N} | Unique: {M} | Tier 1: {K}
Top domains: {list top 3 source domains}
Launching {citation chasing | wave 2 | QA}...
---
```

**After Citation Chasing (if applicable):**
```
--- CITATION EXPANSION COMPLETE ---
New sources from chasing: {N} | Total sources: {M}
Citation chains explored: {K}
Circular references detected: {C}
---
```

**After QA (before final output):**
```
--- QUALITY ASSURANCE PASSED ---
All {N} checks passed | {M} claims triangulated
Generating final report...
---
```

### Adaptive Query Refinement

Between waves, analyze what's working and what's not:

1. **Gap analysis**: Which sub-questions have few/no good sources?
2. **Query refinement**: For under-served sub-questions, reformulate queries:
   - Try different terminology (synonyms, jargon vs. plain language)
   - Try different source types (if academic failed, try industry)
   - Try broader or narrower scope
3. **Serendipity tracking**: If an agent found something unexpected but valuable, generate new sub-questions to explore that direction
4. **Saturation detection**: If new searches keep returning the same sources, that sub-question is saturated — move on

---

## Agent Coordination Protocol

### Dispatch Rules
- Always dispatch agents via the Agent tool with `run_in_background: true`
- Include full research context in each agent prompt — agents don't share memory
- Set model to `opus` for complex analysis/synthesis, `sonnet` for straightforward searching (Anthropic's own system uses Opus lead + Sonnet subagents — this outperforms single-agent Opus by 90.2%)
- Use `subagent_type: "general-purpose"` for research agents (they need WebSearch + WebFetch)
- **Saturation threshold**: Coordination gains plateau beyond 4 parallel agents (Google/MIT 2025). Use 3-4 focused agents rather than 8+ scattered ones for each wave. Deploy more agents across waves, not within a single wave
- **CRITICAL — avoid role prompting for research agents**: Recent research (March 2026) shows role prompting damages accuracy on factual tasks. Instead of "You are a senior researcher...", use task-focused instructions: "Find and verify factual claims about..."
- **Place critical instructions at END of agent prompts**: Queries at end of context improve quality by up to 30% (primacy/recency effect)
- **Use ReAct pattern**: The Reason-Act loop (think -> search -> observe -> think -> search...) is the #1 ranked prompting technique for research tasks. Tell agents: "Think about what you know, search for what you don't, observe results, then decide what to search next"

### Result Aggregation
When background agents return:
1. Collect all evidence objects
2. Deduplicate by URL
3. Merge findings that cover the same source
4. Run credibility scoring on the full set
5. Identify gaps for next wave

### Error Handling
- If an agent returns empty results: reformulate queries and retry (1x)
- If an agent times out: capture partial results and redistribute remaining queries
- If WebSearch is unavailable: fall back to WebFetch on known authoritative URLs
- If a source URL is dead: note it and search for cached/archived versions
- If too many agents fail: fall back to sequential inline research (no parallel agents)
- If credibility scoring produces mostly Tier 3/Discard: broaden search terms and try different source types

### MCP Tool Integration
If available, leverage MCP tools for enhanced research:
- **Context7** (`mcp__plugin_context7_context7__resolve-library-id` + `mcp__plugin_context7_context7__query-docs`): For technical topics, resolve library IDs and query up-to-date documentation directly
- **Playwright** (`mcp__plugin_playwright_playwright__*`): For sources that require JavaScript rendering or are behind interactive pages
- **Mermaid Chart**: For generating visual diagrams of findings (architecture, flows, comparisons)

When these tools are available, agents should use them to augment WebSearch results with authoritative documentation that may not be indexed by search engines.

---

## Dynamic Skill Communication

This skill communicates with other skills in the ecosystem:

| When | Invoke | How |
|------|--------|-----|
| YouTube URLs found | `yt-learner` | Via Skill tool for each video URL |
| Academic LaTeX needed | `paper` | Via Skill tool for compilation |
| Code examples found | relevant dev skill | Via Skill tool based on language |
| Prompt optimization needed | `llm-language` | Via Skill tool for research prompts |
| Brainstorming the approach | `brainstorming` | Via Skill tool before starting |
| Verifying completion | `verification-before-completion` | Via Skill tool before delivering |

The skill checks `available_skills` registry at Phase 1.5 and activates relevant skills as needed throughout the pipeline.

---

## Advanced Techniques

### Perspective-Guided Simulated Conversation (Co-STORM)
For Deep and UltraDeep modes, after Phase 1, simulate a brief conversation between two expert perspectives on the topic. This reveals sub-questions that a single perspective would miss:

1. **Expert A** (mainstream perspective): States the conventional wisdom
2. **Expert B** (contrarian/alternative perspective): Challenges assumptions
3. **Moderator**: Identifies the most interesting disagreements as priority sub-questions

This adds 2-3 high-value sub-questions that improve coverage of contested areas.

### Adaptive Source Type Selection
Not all topics benefit from the same source mix. Adapt the agent assignment:

| Topic Type | Emphasize | De-emphasize |
|-----------|-----------|-------------|
| Cutting-edge tech | News, Industry, Community | Academic (may lag) |
| Established science | Academic, Documentation | News (may oversimplify) |
| Business strategy | Industry, News | Academic, Documentation |
| Implementation how-to | Documentation, Community, Video | Academic |
| Comparative analysis | Industry (benchmarks), Academic | News |

### Source Diversity Enforcement
After each wave, check source diversity. If >50% of sources come from a single domain or author, actively search for alternative perspectives. A healthy source distribution has:
- At least 3 different source types represented
- No single source contributing >15% of all evidence
- Geographic/institutional diversity when possible

---

## Quality Principles

Based on 100+ sources across academic papers, industry best practices, and research systems:

1. **STORM principle** (Stanford): Use perspective-guided question asking to ensure breadth
2. **Triangulation principle** (systematic review methodology): Require 3+ independent sources for major claims
3. **Citation chasing** (Cochrane standards): Both backward and forward citation chasing
4. **Credibility scoring** (WebTrust, CRAAP test): Multi-dimensional source assessment
5. **Adversarial review** (Constitutional AI): Red-team every synthesis before delivery
6. **Evidence hierarchy** (EBM pyramid): Empirical > theoretical > opinion
7. **Freshness decay** (Perplexity architecture): Weight recent sources higher with time decay
8. **Decomposed prompting** (Khot et al., ICLR 2023): Break complex research into specialized sub-tasks
9. **Self-consistency** (Wang et al., ICLR 2023): Multiple reasoning paths for confidence
10. **Multi-agent debate** (Du et al., ICML 2024): Heterogeneous agents catch blind spots

---

## Critical Warnings (from empirical research)

1. **The 17x Error Trap**: Unstructured "bag of agents" networks amplify errors 17x through cascading. Centralized orchestration (the pipeline in this skill) is essential to suppress this.
2. **72% Failure Rate**: MAST study (March 2025, 1,642 traces) found 72% of enterprise multi-agent projects fail, with coordination breakdowns as the #1 cause (36.9%). This skill mitigates this through structured phases with clear handoffs.
3. **Token Usage = Performance**: Anthropic's research shows token usage explains 80% of performance variance. Model quality upgrades yield MORE benefit than doubling token budgets — use Opus for synthesis, Sonnet for searching.
4. **Sequential Degradation**: Multi-agent approaches degrade performance 39-70% on strictly sequential tasks. Do NOT parallelize inherently sequential reasoning (e.g., Phase 6 triangulation, Phase 7 synthesis). Only parallelize independent search tasks (Phase 3, Phase 5).
5. **~30% Unsupported Claims**: Even with RAG, ~30% of LLM statements are unsupported by retrieved sources. The QA phase (Phase 8) with Chain-of-Verification is essential, not optional.

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Prevention |
|-------------|-------------|------------|
| Surface-level search (5-10 sources) | Misses nuance, contradictions, and depth | Enforce minimum source counts per mode |
| Echo chamber (all sources agree) | Likely selection bias | Always deploy a Contrarian agent |
| Recency bias (only newest sources) | Foundational work is often older | Include date range diversity in queries |
| Authority worship (only big names) | Smaller sources can have unique insights | Include Community agent for diverse perspectives |
| Circular citation (A cites B cites A) | Creates illusion of consensus | Detect and flag circular references |
| Hallucinated citations | Destroys credibility | QA phase verifies every citation |
| Over-engineering output | User wants answers, not a thesis | Match output length to mode and question |
| Ignoring contradictions | User needs the full picture | Always surface disagreements with evidence |
| No methodology transparency | User can't assess reliability | Always include methodology section |

---

## Token Cost Estimate

| Mode | Agents | Estimated Tokens | Approximate Cost |
|------|--------|-----------------|------------------|
| Quick | 3 | 50K-100K | $0.30-0.60 |
| Standard | 5 | 150K-300K | $0.90-1.80 |
| Deep | 6-8 | 300K-600K | $1.80-3.60 |
| UltraDeep | 8-10 | 600K-1.2M | $3.60-7.20 |

These are estimates. Actual costs depend on source density and citation chase depth.

---

## Scientific Grounding

This skill synthesizes methodologies from:

### Research Systems
- **STORM** (Shao et al., Stanford 2024): Perspective-guided question asking + simulated expert conversations
- **Co-STORM** (Stanford 2024): Collaborative multi-agent discourse with moderator
- **OpenAI Deep Research** (2025): Triage-Clarify-Instruct-Research multi-agent pipeline
- **Perplexity Architecture**: Three-layer source ranking with XGBoost reranker
- **LangChain Open Deep Research**: Modular pipeline with configurable agent roles

### Academic Methodology
- **Cochrane Standards**: Citation chasing methodology (forward + backward)
- **Citationchaser** (Haddaway et al., 2022): Systematic citation chasing tool design
- **PRISMA Guidelines**: Systematic review methodology
- **Evidence-Based Medicine Pyramid**: Evidence hierarchy framework

### AI Research Techniques
- **PRISM** (2025): Agentic retrieval with Question Analyzer + Selector + Adder
- **ReAgent** (EMNLP 2025): Reversible multi-agent reasoning with backtracking
- **MA-RAG** (2025): Multi-agent RAG with collaborative chain-of-thought
- **ReSP** (ACM Web 2025): Retrieve, Summarize, Plan iterative method

### Source Assessment
- **WebTrust** (Tsinghua 2025): Fine-tuned credibility scoring (MAE 0.09)
- **CRAAP Test**: Currency, Relevance, Authority, Accuracy, Purpose
- **SIFT Method**: Stop, Investigate, Find better coverage, Trace claims

### Multi-Agent Coordination (from agent research)
- **Anthropic Multi-Agent Research System** (2025): Opus lead + Sonnet subagents, 90.2% improvement over single-agent
- **Mixture-of-Agents** (Wang et al., 2024): Layered refinement achieving 65.1% on AlpacaEval
- **AgentOrchestra** (2025): Hierarchical TEA protocol, 89.04% on GAIA benchmark
- **AgentGroupChat-V2** (2025): Divide-and-conquer with 70% agent reduction, 91.5% on GSM8K
- **Google/MIT Scaling Study** (2025): Saturation threshold at 4 agents, sequential degradation 39-70%

### Prompt Engineering
- **ReAct** (Yao et al., 2023) — #1 for research: Reason-Act interleaving
- **Chain-of-Verification** (Dhuliawala et al., 2023) — #2 for verification
- **Chain-of-Thought** (Wei et al., NeurIPS 2022)
- **Tree-of-Thought** (Yao et al., NeurIPS 2023)
- **Self-Consistency** (Wang et al., ICLR 2023)
- **Decomposed Prompting** (Khot et al., ICLR 2023)
- **Self-Refine** (Madaan et al., NeurIPS 2023)
- **Multi-Agent Debate** (Du et al., ICML 2024)

### Evaluation Benchmarks
- **RACE / DeepResearch Bench**: PhD-level research task evaluation
- **DR. BENCH**: Multi-domain research capability assessment
- **ReportBench**: Research report quality evaluation

For detailed reference: see `references/research-methodology.md`
