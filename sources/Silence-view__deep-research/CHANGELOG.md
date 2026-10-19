# Changelog

## [1.0.0] - 2026-03-27

### Added
- 10-phase research pipeline (Context Load through Post-Research Debrief)
- 4 research modes: Quick (20-30 sources), Standard (50-70), Deep (80-120), UltraDeep (120-200+)
- 6-dimension source credibility scoring (authority, freshness, relevance, evidence quality, peer validation, independence)
- Recursive citation chasing (backward + forward, up to 2 levels deep)
- Evidence triangulation requiring 3+ independent sources for major claims
- Parallel research agent deployment (5-8 agents per wave)
- Wave 2 targeted deep-dive for gap filling
- QA red-team phase with Chain-of-Verification
- CLAUDE.md integration for project context updates
- Dynamic skill communication (yt-learner, paper, etc.)
- Automated report validation script (validate_report.py)
- Perspective-guided simulated conversation (Co-STORM inspired)
- Adaptive source type selection based on topic
- Source diversity enforcement
- Progress communication protocol with milestone banners
- Adaptive query refinement between waves
- Circular citation detection with cascade ratio
- Semantic Scholar and OpenAlex API integration for academic citation chasing
- Dempster-Shafer inspired evidence aggregation
- Multilingual support (report language matches user language)

### Scientific Grounding
- Based on 200+ sources consulted during development
- Incorporates methodologies from STORM, OpenAI Deep Research, Perplexity, Cochrane Standards
- Validated against empirical findings: saturation at 4 agents, 17x error trap, 90.2% multi-agent improvement
