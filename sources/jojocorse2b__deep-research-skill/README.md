# Deep Research Skill

Evidence-first research workflows for Codex, Claude Code and OpenCode.

This bundle turns a complex research question into a reproducible run with
multiple sources, claim-level evidence, reliability scoring, contradiction
tracking and a packaged report.

## What it provides

- multi-source and multi-angle research;
- explicit verification of claims, numbers and quotations;
- source reliability scoring separated from claim confidence;
- visible contradiction and unresolved-point tracking;
- persistent `sources.jsonl`, `evidence.jsonl`, `claims.jsonl` and
  `conflicts.jsonl` records;
- Markdown and HTML report generation, with optional PDF through Pandoc;
- secret scanning before sharing or committing research artifacts;
- a dependency-light path that works without a paid search API whenever the
  host provides web search or the user supplies public URLs.

## Install for Codex

```bash
git clone https://github.com/jojocorse2b/deep-research-skill.git
cd deep-research-skill

mkdir -p ~/.codex/skills ~/.codex/agents
cp -R skills/research-codex-en/* ~/.codex/skills/
cp agents-codex/web-researcher.toml ~/.codex/agents/
cp -R agents-codex/web-search-modules ~/.codex/agents/
```

The main skill is installed as `deep-research`. The bundle also includes the
outline, deep-research and report skills used by the `/research` workflow.

For multi-agent execution, enable the relevant Codex feature in your local
configuration and review `agents-codex/web-researcher.toml` before use.

## Install for Claude Code or OpenCode

```bash
cp -R skills/research-en/* ~/.claude/skills/
cp agents/web-search-agent.md ~/.claude/agents/
cp -R agents/web-search-modules ~/.claude/agents/
```

Use the equivalent `skills/research-zh` or `skills/research-codex-zh` folders
for Chinese-language workflows.

## Use the skill

Ask naturally:

```text
Use deep-research to compare two technologies for a production decision.
```

The legacy command flow is also available:

```text
/research <topic>
/research-deep
/research-report
```

The recommended run directory contains:

```text
research-run/
├── run_manifest.json
├── sources.jsonl
├── evidence.jsonl
├── claims.jsonl
├── conflicts.jsonl
├── report.md
└── report.html
```

## Validate and package a run

```bash
python scripts/secret_scan.py research-run
python scripts/validate_evidence.py research-run
python scripts/build_report.py research-run --html
python scripts/build_report.py research-run --html --pdf  # requires pandoc
```

See [docs/USAGE.md](docs/USAGE.md) for the evidence format, reliability rubric,
conflict records, report workflow and security checklist.

## Quality rules

The workflow distinguishes verified facts from inference and unknowns. It
requires a source locator for evidence, matching units and dates for numerical
claims, short attributable quotations, and an explicit counter-evidence pass.
It never treats repeated low-quality claims as independent confirmation.

## Testing

```bash
python -m pytest
python tests/test_validate_json_schemas.py
python scripts/secret_scan.py .
```

## Responsible use

Review sensitive outputs before sharing them. Do not place API keys, private
URLs, personal data or confidential documents in a research run or commit.
For medical, legal, financial and safety-sensitive decisions, use current
authoritative sources and consult a qualified professional.

## License

MIT. Optional external tools and providers keep their own terms and licenses.

