#!/usr/bin/env bash
# run_standard.sh — standard-mode pipeline smoke test (synthetic, no live web).
#
# Constructs a research dir as if two parallel subagents had run:
#   - agent-1: product A scope
#   - agent-2: product B scope
# Each writes a skeleton-first workstream file with inline citations and a
# heartbeat. The orchestrator then synthesizes report.md with citations drawn
# from sources.json. The validator enforces the shape contract.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SKILL="$ROOT/skill"
TMPROOT="$(mktemp -d -t drs-standard-XXXXXX)"
trap 'rm -rf "$TMPROOT"' EXIT

QUERY="Compare Tavily vs Exa vs Brave for agent search"
DATE="2026-04-21"

# 1. classify → must pick standard
MODE="$(node "$SKILL/scripts/classify.js" "$QUERY" | node -e 'let d=""; process.stdin.on("data",c=>d+=c).on("end",()=>console.log(JSON.parse(d).mode));')"
if [[ "$MODE" != "standard" ]]; then
  echo "FAIL: expected mode=standard, got $MODE" >&2
  exit 1
fi

# 2. slugify + run dir
SLUG="$(bash "$SKILL/scripts/slugify.sh" "$QUERY")"
RUNDIR="$TMPROOT/research/${SLUG}-${DATE}"
mkdir -p "$RUNDIR/agents"

# 3. plan.md records the backend choice
cat > "$RUNDIR/plan.md" <<EOF
# Research plan: $QUERY

- **Date:** $DATE
- **Mode:** standard
- **Backend:** websearch
- **Classifier score:** 2 (reason: breadth-comparison +2)
- **Ambiguous:** false

## Scope

Side-by-side comparison of three agent-oriented search APIs with concrete tradeoffs.

## Sub-questions

1. What is each product's core retrieval model?
2. How do they compare on pricing and rate limits?
3. Which is best suited for agent search and why?

## Subagent assignments

- **Agent 1 — Tavily & Exa:** sub-questions 1, 2
- **Agent 2 — Brave + recommendation:** sub-questions 1, 2, 3
EOF

# 4. agent workstream files (skeleton-first with inline citations)
cat > "$RUNDIR/agents/agent-1.md" <<'EOF'
# Agent 1: Tavily & Exa

## Core retrieval model

Tavily positions itself as an agent-oriented search API with LLM-aware ranking ([source](https://tavily.com/)). Exa emphasizes semantic / neural embedding search over keyword matching ([source](https://exa.ai/)).

## Pricing and rate limits

Tavily publishes tiered pricing on their plans page ([source](https://tavily.com/#pricing)). Exa documents its pricing alongside its API docs ([source](https://docs.exa.ai/)).

## Sources

See run-wide sources.json.
EOF

cat > "$RUNDIR/agents/agent-2.md" <<'EOF'
# Agent 2: Brave + recommendation

## Core retrieval model

Brave Search exposes a web-scale keyword + discussion index with a privacy posture ([source](https://brave.com/search/api/)).

## Pricing and rate limits

Brave's pricing is published alongside the API docs and distinguishes free and paid tiers ([source](https://brave.com/search/api/)).

## Best for agent search

For pure agent-driven synthesis tasks, semantic search tends to return fewer but higher-signal results; for large-recall discovery, keyword-heavy indexes still win ([source](https://exa.ai/)).

## Sources

See run-wide sources.json.
EOF

# 5. heartbeats (two rounds each, simulating normal progress)
for N in 1 2; do
  cat > "$RUNDIR/agents/agent-$N.heartbeat" <<EOF
2026-04-21T10:01:00Z round=1 lines=4 sources=2
2026-04-21T10:03:00Z round=2 lines=14 sources=4
EOF
done

# 6. sources.json via dedup
cat > "$TMPROOT/new.json" <<'EOF'
[
  {"url": "https://tavily.com/", "title": "Tavily", "agent": 1},
  {"url": "https://tavily.com/#pricing", "title": "Tavily Pricing", "agent": 1},
  {"url": "https://exa.ai/", "title": "Exa", "agent": 1},
  {"url": "https://docs.exa.ai/", "title": "Exa Docs", "agent": 1},
  {"url": "https://brave.com/search/api/", "title": "Brave Search API", "agent": 2}
]
EOF
cp "$SKILL/templates/sources.json.tmpl" "$RUNDIR/sources.json"
node "$SKILL/scripts/dedup_sources.js" "$RUNDIR/sources.json" "$TMPROOT/new.json" > /dev/null

# 7. synthesized report.md with comparison table and inline citations
cat > "$RUNDIR/report.md" <<'EOF'
# Tavily vs Exa vs Brave for agent search

This report compares three agent-oriented web search APIs along retrieval model, pricing, and fit for agent workflows, with citations drawn from each vendor's own documentation.

## Summary

- **Tavily** is purpose-built for agents with LLM-aware ranking ([source](https://tavily.com/)).
- **Exa** emphasizes semantic / neural search over keyword matching ([source](https://exa.ai/)).
- **Brave** provides a web-scale keyword index with a privacy posture ([source](https://brave.com/search/api/)).

## Comparison

| Product | Retrieval model | Pricing reference |
|---|---|---|
| Tavily | LLM-aware ranking ([source](https://tavily.com/)) | [pricing page](https://tavily.com/#pricing) |
| Exa    | Semantic/neural ([source](https://exa.ai/))         | [docs](https://docs.exa.ai/) |
| Brave  | Keyword + discussions ([source](https://brave.com/search/api/)) | [api](https://brave.com/search/api/) |

## Recommendation

For agent synthesis, semantic retrieval is the stronger primitive; for high-recall discovery, keyword-heavy indexes still win on breadth ([source](https://exa.ai/)).
EOF

# 8. validate
node "$SKILL/scripts/validate_outputs.js" "$RUNDIR"
echo "smoke-standard: PASS"
