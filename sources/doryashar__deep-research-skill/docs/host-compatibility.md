# Host compatibility

The skill targets two hosts — **Claude Code** and **opencode** — and
degrades gracefully in any third host that lacks subagent dispatch.

## Detection

At the start of every run, the skill inspects its available tool names:

| Signal | Host | Dispatch primitive |
|---|---|---|
| `Task` tool present | Claude Code | `Task(subagent_type, prompt, description)` |
| `agent` or `subtask` tool present | opencode | its agent/subtask tool |
| Neither | Degraded | run the subagent contract in the main loop |

## Key differences

### Claude Code

- Subagent dispatch via `Task` is **blocking** — the parent waits for the
  subagent to return. There is no streaming handle.
- Heartbeat files are the ONLY way the parent can detect a stuck subagent
  (stdout isn't available mid-run). This is the defining constraint.
- `AskUserQuestion` is available interactively; skill uses it exactly once
  when the classifier lands in the ambiguous band.

### opencode

- Subagent dispatch API is the host's `agent` or `subtask` tool; exact
  invocation varies by version. Check the opencode docs.
- opencode's conversational model is similar to Claude Code's; the same
  subagent contract works.
- If opencode exposes a streaming handle for subagents in the future, the
  skill can switch to stdout heartbeats in addition to file heartbeats —
  file-based remains the fallback.

### Degraded mode (neither host primitive present)

- Standard and deep still produce the same output layout.
- Subagents run **sequentially** inside the main session. Agent 1 finishes,
  then agent 2 starts.
- Stuck-agent detection is **skipped** — the parent is the agent, there's
  nothing to poll.
- Wall time scales linearly with subagent count; adjust mode expectations
  accordingly.

## Differences the skill papers over

- **Tool name prefixes.** MCP tools are named differently across hosts
  (`mcp__exa__search` vs `exa_search`). `backend-detection.md`'s `match_hints`
  list covers the common prefixes.
- **File path conventions.** Both hosts let the skill write anywhere under
  the working directory. `research/<slug>-<date>/` is used unconditionally.
- **Skill loading.** Claude Code loads from `~/.claude/skills/`; opencode
  loads from `~/.config/opencode/skills/` (confirm the exact path for your
  opencode version). `make install-claude` / `make install-opencode` handle
  the symlinks.

## Known issues

- **opencode subagent API stability.** Between opencode versions, the
  dispatch tool has changed name (`agent` → `subtask` → back). The skill's
  host-detection code tries both and falls back to degraded mode if neither
  is present. If your opencode version exposes a different name, add it to
  `skill/references/host-detection.md`'s signature table.
- **`AskUserQuestion` in CI / scripted runs.** Not all hosts expose an
  interactive question primitive. The classifier detects absence and defaults
  to `standard` silently, logging the ambiguity in `plan.md`.

## Verifying compatibility

```
# Claude Code
make install-claude
# ... open a Claude Code session and run quick/standard/deep queries ...

# opencode
make install-opencode
# ... open an opencode session and run the same queries ...
```

The output layout and validator pass should be identical. Any divergence is
a bug in `host-detection.md`'s signature table — file an issue.
