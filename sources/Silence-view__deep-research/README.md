# Deep Research — Claude Code Plugin

Professional multi-agent deep research system for [Claude Code](https://claude.com/claude-code). Investigates any topic across **100+ sources** with recursive citation chasing, source credibility scoring, evidence triangulation, and knowledge synthesis.

## What It Does

When you ask Claude to research something in depth, this skill deploys **parallel specialized agents** that:

1. **Decompose** your question into sub-questions using perspective-guided discovery (inspired by Stanford STORM)
2. **Search** across academic papers, industry blogs, official docs, community forums, news, and YouTube videos
3. **Score** every source on 6 credibility dimensions (authority, freshness, relevance, evidence quality, peer validation, independence)
4. **Chase citations** recursively — finding the sources behind each source (backward + forward citation chasing)
5. **Triangulate** evidence across 3+ independent sources before presenting claims as verified
6. **Red-team** the synthesis with a QA agent using Chain-of-Verification
7. **Deliver** a professional report with full bibliography, credibility scores, and confidence levels

## Installation

```bash
claude plugin add Silence-view/deep-research
```

Or manually:
```bash
git clone https://github.com/Silence-view/deep-research.git ~/.claude/plugins/deep-research
```

## Usage

Invoke via natural language:

```
"Deep research on multi-agent AI architectures in 2025"
"Fammi una ricerca approfondita sulle best practice per..."
"Comprehensive analysis of WebAssembly adoption trends"
"Survey the literature on source credibility scoring"
```

Or explicitly:
```
/deep-research
```

## Research Modes

| Mode | Sources | Agents | Duration | Best For |
|------|---------|--------|----------|----------|
| **Quick** | 20-30 | 3 | 2-5 min | Focused questions |
| **Standard** | 50-70 | 5 | 5-15 min | General topics |
| **Deep** | 80-120 | 6-8 | 15-30 min | Complex topics |
| **UltraDeep** | 120-200+ | 8-10 | 30-60 min | Literature reviews, critical decisions |

Mode is inferred from your language. "Quick overview" -> Quick. "Everything about" -> Deep. "Comprehensive survey" -> UltraDeep.

## Pipeline (10 Phases)

```
Phase 0:  Context Load (CLAUDE.md, ROSETTA.md, project context)
Phase 1:  Query Decomposition (STORM-inspired perspective discovery)
Phase 2:  Research Planning (agent assignment, query generation)
Phase 3:  Primary Research Wave (5-8 parallel agents)
Phase 3.5: Wave 2 Targeted Deep-Dive (gap filling)
Phase 4:  Source Credibility Assessment (6-dimension scoring)
Phase 5:  Recursive Citation Chasing (backward + forward, up to 2 levels)
Phase 6:  Evidence Triangulation (3+ independent sources per claim)
Phase 7:  Synthesis & Knowledge Construction
Phase 8:  Quality Assurance (red-team with Chain-of-Verification)
Phase 9:  Output & Integration (report + CLAUDE.md update)
Phase 10: Post-Research Debrief
```

## Source Credibility Scoring

Every source is scored on 6 dimensions (0.0 to 1.0):

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Authority | 25% | Institution/author reputation |
| Freshness | 15% | Publication recency (with evergreen adjustment) |
| Relevance | 25% | How directly it answers the question |
| Evidence Quality | 20% | Empirical data vs. opinion |
| Peer Validation | 10% | Peer review, citation count |
| Independence | 5% | Freedom from conflicts of interest |

Sources are tiered: **Tier 1** (>= 0.75), **Tier 2** (0.50-0.74), **Tier 3** (0.25-0.49), **Discarded** (< 0.25).

## Scientific Grounding

Built on research from 50+ sources including:

- **STORM / Co-STORM** (Stanford) — Perspective-guided multi-agent research
- **OpenAI Deep Research** — Triage-Clarify-Instruct-Research pipeline
- **Perplexity Architecture** — Three-layer source ranking
- **Cochrane Standards** — Forward and backward citation chasing
- **WebTrust** (Tsinghua 2025) — Automated credibility scoring (MAE 0.09)
- **PRISM, ReAgent, MA-RAG** — Multi-agent retrieval (2025)
- **Anthropic Multi-Agent System** — Opus + Sonnet architecture (+90.2% vs single-agent)
- **Chain-of-Verification** (Dhuliawala et al.) — Claim verification prompting

## Plugin Structure

```
deep-research/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── skills/
│   └── deep-research/
│       ├── SKILL.md                    (main skill - 834 lines)
│       ├── references/
│       │   ├── research-methodology.md (scoring, chasing, agent templates)
│       │   └── output-templates.md     (report templates, evidence schema)
│       └── scripts/
│           └── validate_report.py      (automated report validation)
├── README.md
├── LICENSE
└── CHANGELOG.md
```

## Validation Script

Validate generated reports:

```bash
python3 scripts/validate_report.py report.md --mode standard
```

Checks: executive summary, key findings, bibliography, source count, tier distribution, citations, URLs, methodology, limitations, report length, confidence tags.

## Requirements

- Claude Code with Agent tool access
- WebSearch and WebFetch tools available
- Works best with Opus model (recommended) or Sonnet

## License

MIT
