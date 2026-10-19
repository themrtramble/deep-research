# deep-research

A tiered deep-research skill for Claude Code and opencode. Pulls the best
patterns from six reference implementations ([Weizhena], [199-biotechnologies],
[altmbr], [paddo.dev], [Smithery], [MCPmarket]) into one skill that auto-selects
depth, dispatches parallel subagents, and survives context compaction by
persisting evidence to disk.

[Weizhena]: https://github.com/Weizhena/Deep-Research-skills
[199-biotechnologies]: https://github.com/199-biotechnologies/claude-deep-research-skill
[altmbr]: https://github.com/altmbr/claude-research-skill
[paddo.dev]: https://paddo.dev/blog/three-ways-deep-research-claude/
[Smithery]: https://smithery.ai/skills/glebis/deep-research
[MCPmarket]: https://mcpmarket.com/tools/skills/deep-research-4

## Modes

| Mode      | Time    | Sources | Subagents  | Critique         | Evidence ledger |
|-----------|---------|---------|------------|------------------|-----------------|
| quick     | ~3 min  | 3–6     | 0 (inline) | none             | no              |
| standard  | ~10 min | 10–20   | 2–3        | 1 pass           | no              |
| deep      | ~25 min+| 20–40   | 4–5        | up to 3 loops    | yes             |

The skill classifies each query automatically. If the scope is ambiguous it
asks *once* (scope + depth + time budget), then commits.

## Install

```bash
# Claude Code
make install-claude

# opencode
make install-opencode
```

Both targets symlink `skill/` into the host's skills directory. Override the
target location with `CLAUDE_SKILL_DIR=...` or `OPENCODE_SKILL_DIR=...`.

## Search backends

Baseline: `WebSearch` + `WebFetch` (built into both hosts).

The skill auto-detects and prefers MCP search backends if present:
`Exa → Tavily → Perplexity → Firecrawl → Brave`. No MCP is required.

See `docs/adding-a-backend.md` for adding your own.

## Output layout

Every run writes to `research/<slug>-<YYYY-MM-DD>/`:

```
research/state-of-ai-code-review-2026-04-21/
├── plan.md               # phase-1 research plan
├── report.md             # primary output, inline-cited
├── sources.json          # dedup'd URLs + fetch status
├── evidence.jsonl        # deep mode only: claim-level ledger
└── agents/
    ├── agent-1.md
    ├── agent-1.heartbeat
    └── ...
```

## Testing

```bash
make test            # classifier unit tests
make smoke           # end-to-end with cached web fixtures
make test-pressure   # TDD-for-skills pressure scenarios
```

## Docs

- `docs/quickstart.md` — 5-minute walkthrough per mode
- `docs/architecture.md` — phase diagram + data flow
- `docs/modes.md` — per-mode quality bars
- `docs/adding-a-backend.md` — plug in a new search MCP
- `docs/extending-critique-personas.md` — add a red-team persona
- `docs/host-compatibility.md` — Claude Code vs opencode
- `docs/adr/` — architecture decision records

## License

MIT
