# Quickstart

## Install

```bash
# Claude Code
make install-claude

# opencode
make install-opencode
```

Both targets symlink `skill/` into the host's skills directory. The skill
is auto-discovered on the host's next session start.

Override the target with environment variables:

```bash
CLAUDE_SKILL_DIR=/custom/path make install-claude
```

## Five-minute tour

### Quick mode

```
> What is the current stable version of Bun?
```

Expected:

- Classifier scores the query as `quick` (~3 min budget, 3–6 sources).
- Skill creates `research/what-is-the-current-stable-version-of-bun-<date>/`.
- Inline search → fetch → write loop runs in the main session.
- `report.md` under 400 words, with ≥ 3 inline URL citations.

### Standard mode

```
> Compare Tavily vs Exa vs Brave for agent search
```

Expected:

- Classifier scores as `standard` (~10 min, 10–20 sources, 2–3 subagents).
- Skeleton-first `agents/agent-1.md` and `agents/agent-2.md` appear almost
  immediately.
- Final `report.md` includes a comparison table and a recommendation with
  inline citations.
- One critique pass runs before write.

### Deep mode

```
> State of the art in AI code review tools in 2026
```

Expected:

- Classifier auto-jumps to `deep` via strong-deep keyword match.
- 4–5 subagents dispatched in parallel, each with a scoped workstream.
- `evidence.jsonl` accumulates one claim-per-line with `primary` flags.
- Up to 3 critique iterations with 3 personas each. Loop-back only when
  personas surface real gaps.
- `report.md` typically includes a `## Where sources disagree` section and
  may include `## Known Limitations` if a gap was flagged twice and moved.

## Common flags

```
... --quick          # force quick
... --deep           # force deep
... --approve-outline   # deep only: pause after plan.md for user approval
... --no-quotes      # skip verbatim quotes in evidence.jsonl
... --max-spawns=20  # cap total subagent spawns
```

## Where the output lives

Every run writes a directory under `research/`:

```
research/<slug>-<date>/
├── plan.md
├── report.md
├── sources.json
├── evidence.jsonl         # deep only
└── agents/                # standard + deep
    ├── agent-1.md
    └── agent-1.heartbeat
```

The host-rooted `research/` directory persists across sessions; the skill
never overwrites an existing run dir (it appends `-2`, `-3`, … when needed).

## Troubleshooting

- **Classifier picks the wrong mode** — pass `--quick`/`--standard`/`--deep` explicitly.
- **Skill hangs on deep mode** — check `agents/*.heartbeat`; a flat line count
  across two rounds means a subagent is stuck. Parent should auto-kill and
  relaunch after ~2 min; if not, cancel and re-run.
- **"Install Exa / Tavily" suggestions appearing** — regression; run
  `make test-pressure` to confirm `backend-detection.md` rules are intact.
- **Citations missing** — `validate_outputs.js` enforces ≥ 1 inline citation
  per 500 words. Run it manually on the run dir: `node skill/scripts/validate_outputs.js research/<dir>`.

## What NOT to use this skill for

- Single-fact lookups — use `WebSearch` directly.
- Code generation, refactoring, debugging.
- Questions about the current repo — use `Grep`/`Read`.
