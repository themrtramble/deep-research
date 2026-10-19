# Deep Research Skill for Claude Code

Parallel expert agents conduct multi-dimensional research and produce high-quality research reports with cross-validated sources.

## Features

- **3-tier research**: Express (~10K chars) / Standard (~25K) / Full (~50K+)
- **Parallel expert agents**: Web Intelligence, Academic, Institutional, Counter-Evidence
- **Cross-validation**: URL verification, contradiction detection, gap analysis
- **Quality assurance**: 5-dimension scoring loop (Detail, Readability, Insight, Source Quality, Actionability)
- **Source evaluation**: A-E reliability grading with citation rules
- **Resumable sessions**: State management via `state.json`

## Installation

### Quick install (recommended)

```bash
# From your project root directory:
bash <(curl -fsSL https://raw.githubusercontent.com/comeonvictor/claude-code-deep-research/main/install.sh)
```

### Manual install

```bash
# From your project root directory:
mkdir -p .claude/skills/deep-research
git clone https://github.com/comeonvictor/claude-code-deep-research.git /tmp/deep-research-tmp
cp /tmp/deep-research-tmp/SKILL.md .claude/skills/deep-research/
cp -r /tmp/deep-research-tmp/references .claude/skills/deep-research/
rm -rf /tmp/deep-research-tmp
```

### Git submodule (for version tracking)

```bash
git submodule add https://github.com/comeonvictor/claude-code-deep-research.git .claude/skills/deep-research
```

## Usage

In Claude Code, type:

```
/deep-research [your research topic]
```

Or just describe your research need:

```
"딥리서치해줘: AI agents in education 2026"
"deep research: comparing vector databases for RAG"
```

## Structure

```
.claude/skills/deep-research/
├── SKILL.md              # Main skill definition (phases 0-7)
└── references/
    ├── agent-prompts.md   # Detailed prompts for each expert agent
    ├── citation_rules.md  # Citation formatting rules
    ├── overview.md        # Output directory structure
    ├── phase_contracts.md # Phase input/output contracts
    ├── quality_rubric.md  # Quality scoring rubric
    ├── question_scoping.md # Scope interview templates
    ├── report-template.md # Report format templates per tier
    ├── source-evaluation.md # Source reliability grading
    └── state_schema.md    # state.json schema for resumable sessions
```

## Research Output

Reports are saved to `RESEARCH/{topic}_{timestamp}/`:

```
RESEARCH/{topic}_{timestamp}/
├── state.json                          # Session state (resumable)
├── sources/
│   ├── sources.jsonl
│   └── bibliography.md
├── outputs/
│   ├── {topic}_deep-research_v1.md     # Final report
│   ├── {topic}_claims_v1.yaml          # Claim database
│   └── summary_context.md
└── artifacts/
    ├── research_plan.json
    └── agent_results/
```

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI or IDE extension
- WebSearch and WebFetch tools enabled

## License

MIT
