#!/usr/bin/env bash
# run_deep.sh — deep-mode smoke test (synthetic, no live web, no live LLM).
#
# Constructs a research dir representing a completed deep-mode run on a
# contested topic ("long-context vs RAG"). Exercises:
#   - classify.js → deep
#   - 4 agent workstream files with citations
#   - evidence.jsonl with primary/secondary flags
#   - "Where sources disagree" section (Persona 2 output materialized)
#   - Known Limitations section (same-gap escape)
# Validates the full shape contract via validate_outputs.js.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SKILL="$ROOT/skill"
TMPROOT="$(mktemp -d -t drs-deep-XXXXXX)"
trap 'rm -rf "$TMPROOT"' EXIT

QUERY="Survey the debate over whether LLM agents should use long context vs retrieval-augmented generation"
DATE="2026-04-21"

# 1. classify → must pick deep
MODE="$(node "$SKILL/scripts/classify.js" "$QUERY" | node -e 'let d=""; process.stdin.on("data",c=>d+=c).on("end",()=>console.log(JSON.parse(d).mode));')"
if [[ "$MODE" != "deep" ]]; then
  echo "FAIL: expected mode=deep, got $MODE" >&2
  exit 1
fi

# 2. slugify + run dir
SLUG="$(bash "$SKILL/scripts/slugify.sh" "$QUERY")"
RUNDIR="$TMPROOT/research/${SLUG}-${DATE}"
mkdir -p "$RUNDIR/agents"

# 3. plan.md
cat > "$RUNDIR/plan.md" <<EOF
# Research plan: $QUERY

- **Date:** $DATE
- **Mode:** deep
- **Backend:** websearch
- **Classifier score:** 4 (reason: breadth-landscape +2 + depth +2)
- **Ambiguous:** false
- **Critique iterations:** 3 (capped; 1 gap moved to Known Limitations)

## Scope

Landscape the technical and empirical debate between long-context and
retrieval-augmented generation for LLM agents, surfacing where expert sources
disagree. 2023–2026 scope, English-language primary sources preferred.

## Sub-questions

1. What are the empirical benchmarks comparing long-context vs RAG on QA and reasoning?
2. Where do practitioners disagree about cost and latency tradeoffs?
3. Which classes of agent tasks favor each approach?
4. What do the major architectures (Anthropic, OpenAI, Google) recommend?

## Subagent assignments

- **Agent 1 — Empirical benchmarks:** sub-question 1
- **Agent 2 — Cost/latency:** sub-question 2
- **Agent 3 — Task classes:** sub-question 3
- **Agent 4 — Vendor recommendations:** sub-question 4
EOF

# 4. agent workstream files (skeleton-first + inline citations)
for N in 1 2 3 4; do
  cat > "$RUNDIR/agents/agent-$N.md" <<EOF
# Agent $N: <scope>

## Section A

Finding $N-A with an inline citation ([source](https://example.com/agent$N/a)).

## Section B

Finding $N-B with another citation ([source](https://example.com/agent$N/b)).

## Sources

See run-wide sources.json.
EOF
  cat > "$RUNDIR/agents/agent-$N.heartbeat" <<EOF
2026-04-21T10:0${N}:00Z round=1 lines=4 sources=1
2026-04-21T10:0${N}:30Z round=2 lines=10 sources=2
2026-04-21T10:0${N}:50Z round=3 lines=18 sources=3
EOF
done

# 5. sources.json
cat > "$TMPROOT/new.json" <<'EOF'
[
  {"url": "https://example.com/agent1/a", "title": "Benchmark A", "agent": 1, "primary": true},
  {"url": "https://example.com/agent1/b", "title": "Benchmark B", "agent": 1, "primary": true},
  {"url": "https://example.com/agent2/a", "title": "Cost study",  "agent": 2, "primary": false},
  {"url": "https://example.com/agent2/b", "title": "Latency study","agent": 2, "primary": true},
  {"url": "https://example.com/agent3/a", "title": "Task survey",  "agent": 3, "primary": false},
  {"url": "https://example.com/agent3/b", "title": "Task paper",   "agent": 3, "primary": true},
  {"url": "https://example.com/agent4/a", "title": "Vendor rec A", "agent": 4, "primary": true},
  {"url": "https://example.com/agent4/b", "title": "Vendor rec B", "agent": 4, "primary": true},
  {"url": "https://example.com/disagree", "title": "Dissenting paper", "primary": true}
]
EOF
cp "$SKILL/templates/sources.json.tmpl" "$RUNDIR/sources.json"
node "$SKILL/scripts/dedup_sources.js" "$RUNDIR/sources.json" "$TMPROOT/new.json" > /dev/null

# 6. evidence.jsonl (one line per load-bearing claim)
cat > "$RUNDIR/evidence.jsonl" <<'EOF'
{"agent": 1, "claim": "Long-context wins on single-doc QA benchmarks.", "url": "https://example.com/agent1/a", "quote": "long context outperforms RAG on SDQA", "accessed": "2026-04-21T10:01:00Z", "primary": true}
{"agent": 1, "claim": "RAG matches or beats long-context on multi-doc synthesis.", "url": "https://example.com/agent1/b", "quote": "RAG retains an edge for >4-doc synthesis tasks", "accessed": "2026-04-21T10:01:30Z", "primary": true}
{"agent": 2, "claim": "Long-context is cheaper per-query at small context sizes.", "url": "https://example.com/agent2/b", "quote": "under 16k tokens, long-context dominates cost", "accessed": "2026-04-21T10:02:00Z", "primary": true}
{"agent": 3, "claim": "RAG is preferred for tasks requiring fresh data.", "url": "https://example.com/agent3/b", "quote": "retrieval decouples knowledge update from model update", "accessed": "2026-04-21T10:03:00Z", "primary": true}
{"agent": 4, "claim": "Vendor A recommends hybrid approaches by default.", "url": "https://example.com/agent4/a", "quote": "hybrid pipelines are our recommended default", "accessed": "2026-04-21T10:04:00Z", "primary": true}
{"agent": 4, "claim": "A dissenting group argues long-context suffices beyond 1M tokens.", "url": "https://example.com/disagree", "quote": "with 1M+ context windows, retrieval becomes redundant", "accessed": "2026-04-21T10:04:30Z", "primary": true}
EOF

# 7. report.md with "Where sources disagree" + "Known Limitations" sections
cat > "$RUNDIR/report.md" <<'EOF'
# Long context vs retrieval-augmented generation for LLM agents

A landscape of the 2023–2026 debate over whether LLM agents should rely on
long context windows or retrieval-augmented generation (RAG), drawing on
empirical benchmarks and vendor recommendations.

## Executive summary

- Long context wins on single-document QA ([source](https://example.com/agent1/a)).
- RAG wins on multi-document synthesis ([source](https://example.com/agent1/b)).
- Cost tradeoffs flip at ~16k tokens ([source](https://example.com/agent2/b)).
- Fresh-data tasks favor RAG regardless of context size ([source](https://example.com/agent3/b)).
- Major vendors recommend hybrid by default ([source](https://example.com/agent4/a)).

## Position A — Long-context camp

Benchmarks at small context sizes favor long-context, with measurable cost
advantages under 16k tokens ([source](https://example.com/agent2/b)). A
dissenting subgroup goes further, arguing that retrieval becomes redundant
beyond 1M-token context windows ([source](https://example.com/disagree)).

## Position B — RAG camp

Multi-document synthesis remains a RAG stronghold
([source](https://example.com/agent1/b)), and tasks requiring fresh or
frequently-updated data strongly favor retrieval since it decouples knowledge
updates from model updates ([source](https://example.com/agent3/b)).

## Where sources disagree

The central disagreement is about the crossover point where long context
overtakes RAG. Some sources place it at ~16k tokens for cost
([source](https://example.com/agent2/b)); the dissenting view places it at 1M
tokens for capability
([source](https://example.com/disagree)). Neither side presents a benchmark
that resolves the question under identical conditions.

## Known Limitations

- Benchmark suites differ across positions; no head-to-head study under
  identical conditions was found in the sources collected. (Critique loops
  flagged this gap twice and moved it here per the same-gap escape.)

## Sources

See sources.json for the run-wide dedup'd source list.
EOF

# 8. validate
node "$SKILL/scripts/validate_outputs.js" "$RUNDIR"
echo "smoke-deep: PASS"
