# Deep Research

A general-purpose deep research skill for AI agents. Decomposes any topic into sub-goals, dispatches parallel sub-agents to investigate the open web, refines its research plan across waves until convergence, and returns a structured, citation-dense report inline.

Built for the [skills.sh](https://skills.sh) ecosystem — works in Claude Code, Cursor, Copilot, Cline, Windsurf, Codex, Gemini, and 30+ other agents.

## What it does

Produces a structured Markdown research report covering:

- **TL;DR** — 3–5 bullets
- **Scope and framing**
- **Key findings**
- **Evidence** — organized per sub-goal
- **Counter-evidence and dissent**
- **Gaps and unknowns**
- **Sources** — footnoted, tier-labeled

Reports use Markdown footnote citations (`[^1]`) and triangulate material claims across at least two independent sources.

## Install

```bash
npx skills add ramit-mitra/deep-research-skill
```

## Usage

Invoke the skill in your AI agent — pass the topic inline:

```
/deep-research <topic or question or URL>
```

If invoked without args, the skill asks once for the topic. It then infers scope, audience, and recency from the topic, announces the framing in one line, and kicks off research. A single targeted clarifier is asked only when the topic is too ambiguous to frame confidently.

The skill runs parallel sub-agents across multiple research waves, refining its plan as evidence accumulates, and prints the final report inline.

## Key principles

- **Iterative agent loop** — search, read, reason, re-plan, repeat
- **Subagent-driven** — parallel research, not single-agent linear
- **Convergence-stopped** — stops when extra searching adds <15% novel claims for two consecutive waves, with a floor of 10 distinct sources
- **Triangulated** — material claims need at least 2 independent sources; single-source claims are flagged
- **Source-tier ladder** — primary docs > peer-reviewed > reputable news > industry > expert blogs > community
- **Honest about gaps** — missing or weakly supported claims are surfaced, not hidden
- **Refuses harmful topics** — weapons synthesis, CSAM, malware, doxxing

## Source-tier ladder

| Tier | Examples |
|---|---|
| 1. Primary | Official docs, regulatory filings, source code, RFCs, gov data, standards bodies |
| 2. Peer-reviewed | arXiv, journals, conference papers |
| 3. Reputable news | FT, Reuters, NYT, WSJ, Bloomberg, Economist, AP, BBC |
| 4. Industry | Analyst reports, whitepapers, conference talks, eng blogs |
| 5. Expert blogs | Practitioner posts, substacks, newsletters |
| 6. Community | Forums, GitHub issues, HackerNews, Reddit, StackExchange |

Higher tier wins on conflict. Conflicts are surfaced in Counter-evidence.

## Inspiration

- [Indian Stock Analyser](https://github.com/ramit-mitra/indian-stock-analyser) — sibling skill demonstrating subagent-driven domain research

## Supported agents

Works with Claude Code, GitHub Copilot, Cursor, Cline, Windsurf, OpenAI Codex, Google Gemini, and 30+ other agents via the [skills.sh](https://skills.sh) ecosystem.

## License

MIT
