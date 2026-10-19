# Architecture

## One-minute read

The skill is an orchestrator that (1) classifies the query into a mode,
(2) plans scoped sub-questions, (3) dispatches parallel research subagents
that each own a slice of the scope, (4) collects their workstream files and
a dedup'd `sources.json`, (5) runs a red-team critique (standard: 1 pass,
deep: up to 3 loops), and (6) synthesizes the final `report.md`.

Evidence is persisted to disk at every step so the run survives context
compaction.

## Phase diagram

```
     user query
         │
         ▼
    [classify.js] ───► mode ∈ {quick, standard, deep}
         │                      │
         ▼                      │
  write plan.md                 │
         │                      │
         ▼                      │
  [probe_backends.sh] ───► backend choice
         │                      │
         ▼                      │
  ┌──────┴──────┐                │
  │ quick: inline research loop │
  │ standard: 2–3 parallel      │
  │ deep:     4–5 parallel + critique loop
  └──────┬──────┘
         ▼
  agents/agent-N.md + heartbeats (written skeleton-first)
         │
         ▼
  sources.json (dedup'd via dedup_sources.js)
         │
         ▼
  evidence.jsonl (deep only, one claim per line)
         │
         ▼
  [critique personas: parallel dispatch]
         │
         ▼
  loop-back? ─► targeted retrieval (back to agents/)
         │no
         ▼
  synthesize report.md
         │
         ▼
  [validate_outputs.js]
         │
         ▼
   ship / deliver
```

## Data flow

| From | To | Written by | Read by |
|---|---|---|---|
| user | classify.js | user | orchestrator |
| classify output | plan.md | orchestrator | user, smoke tests |
| subagent search | sources.json | subagent (via dedup_sources.js) | all agents, validator |
| subagent writes | agents/agent-N.md | subagent (skeleton first) | orchestrator, critique personas |
| subagent heartbeat | agents/agent-N.heartbeat | subagent | parent (stuck detection) |
| subagent claim | evidence.jsonl | subagent (deep only) | critique personas, validator |
| critique personas | synthesized edits | orchestrator | report.md |
| orchestrator | report.md | orchestrator | user, validator |

## Why these design choices

### Why skeleton-first

Without a skeleton, subagents tend to batch searches and defer writing. That
turns the workstream file into a single write at the end — and if the agent
is killed mid-run (stuck detection, context compaction), nothing survives.
Skeleton-first means the structure is on disk before the first search and
every round adds content under a known heading.

See `adr/0002-skeleton-first-protocol.md`.

### Why inline URLs only (no bibliography)

Bibliographies at the bottom of a report let claims drift away from their
sources. Inline URLs force every factual claim to co-locate with its evidence.
The `validate_outputs.js` check for `"recent reports"` without citations is
the canary for this drift.

### Why evidence.jsonl in deep mode

Context compaction is inevitable on long runs. Once the orchestrator's
context is truncated mid-deep-mode run, the only memory of what was seen is
what is on disk. `evidence.jsonl` stores one JSON object per claim so the
critique personas can read any subset without re-loading the full workstream
files.

See `adr/0003-evidence-jsonl.md`.

### Why tiered modes instead of a single workflow

The six reference implementations we studied cluster into three
workflows: lean parallel orchestrators (altmbr), human-in-the-loop outline+fill
(Weizhena), and enterprise pipelines with credibility scoring (199-bio). No
single workflow matches every query type. Factoids don't need 4 subagents;
landscape reviews don't fit in a 3-minute loop.

The classifier is a cheap keyword-scoring heuristic (not an LLM call) that
picks the right workflow for the shape of the query, asking the user only
when the score is genuinely ambiguous.

See `adr/0001-tiered-modes.md`.

### Why host auto-detection

The same skill runs on Claude Code (has `Task` tool) and opencode (has its
own dispatch primitive). Hard-coding either host would halve the user base.
The skill inspects available tool names at start and picks the dispatch path.
If neither is present, it falls back to degraded mode — sequential scoped
loops in the main session — which is slower but still produces the same
output layout.

## What the skill does NOT do

- Rendering to HTML or PDF (199-bio style). Markdown is the source of truth.
- Source credibility scoring via heuristics. Primary/secondary is the only
  tier we track; fine-grained scoring is domain-dependent and out of scope.
- Recursive auto-continuation for 18k+ word reports. If the report is that
  big, break the topic into sub-runs.
- Automatic PII scrubbing of fetched quotes. Users needing this should pass
  `--no-quotes`.

## File responsibilities

| File | Responsibility | Consumers |
|---|---|---|
| `skill/SKILL.md` | Entry point, workflow, red flags | Host (auto-loaded) |
| `skill/scripts/classify.js` | Query → mode | SKILL.md, tests |
| `skill/scripts/slugify.sh` | Query → run-dir name | SKILL.md |
| `skill/scripts/probe_backends.sh` | Emit backend precedence | SKILL.md |
| `skill/scripts/dedup_sources.js` | Merge subagent sources | Subagents |
| `skill/scripts/validate_outputs.js` | Shape check final run | SKILL.md, tests, CI |
| `skill/references/*.md` | On-demand load for details | SKILL.md |
| `skill/templates/*.tmpl` | Boilerplate subagents start from | Subagents |
| `tests/classifier/*` | Unit tests for scripts | CI |
| `tests/pressure/*.md` | Pressure scenarios (docs) | Manual / SDK |
| `tests/pressure/run_pressure.js` | Static grep for countermeasures | CI |
| `tests/smoke/run_*.sh` | Synthetic E2E smoke per mode | CI |
