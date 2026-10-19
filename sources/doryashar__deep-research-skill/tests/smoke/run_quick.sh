#!/usr/bin/env bash
# run_quick.sh — smoke-test the quick-mode pipeline without an agent.
#
# Produces a synthetic research/<slug>-<date>/ directory by seeding the
# templates + scripts the skill would use, then validates it. This exercises:
#   - slugify.sh
#   - classify.js (must return mode=quick)
#   - dedup_sources.js
#   - validate_outputs.js
#   - output schema from references/output-schemas.md
#
# When the skill is run for real inside Claude Code, the same scripts power
# the same outputs — so if this passes, the shape contract holds.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SKILL="$ROOT/skill"
TMPROOT="$(mktemp -d -t drs-quick-XXXXXX)"
trap 'rm -rf "$TMPROOT"' EXIT

QUERY="What is the current stable version of Bun?"
DATE="2026-04-21"

# 1. classify → must pick quick
CLASSIFY_JSON="$(node "$SKILL/scripts/classify.js" "$QUERY")"
MODE="$(echo "$CLASSIFY_JSON" | node -e 'let d=""; process.stdin.on("data",c=>d+=c).on("end",()=>console.log(JSON.parse(d).mode));')"
if [[ "$MODE" != "quick" ]]; then
  echo "FAIL: expected mode=quick, got $MODE" >&2
  echo "$CLASSIFY_JSON" >&2
  exit 1
fi

# 2. slugify → filename-safe
SLUG="$(bash "$SKILL/scripts/slugify.sh" "$QUERY")"
RUNDIR="$TMPROOT/research/${SLUG}-${DATE}"
mkdir -p "$RUNDIR/agents"

# 3. seed plan.md (in a real run the agent fills these templates)
cat > "$RUNDIR/plan.md" <<EOF
# Research plan: $QUERY

- **Date:** $DATE
- **Mode:** quick
- **Backend:** websearch
- **Classifier score:** -6 (reason: short factoid)
- **Ambiguous:** false

## Scope

Identify the current stable version of Bun as of $DATE with at least 3 corroborating sources.

## Sub-questions

1. What is the latest stable Bun release tag?
2. What is its release date?
3. Are there known post-release patches?
EOF

# 4. seed sources.json via dedup_sources (tests the merge)
cat > "$TMPROOT/new.json" <<'EOF'
[
  {"url": "https://bun.sh/docs", "title": "Bun Docs", "status": 200},
  {"url": "https://github.com/oven-sh/bun/releases", "title": "Bun Releases", "status": 200},
  {"url": "https://bun.sh/blog", "title": "Bun Blog", "status": 200}
]
EOF
cp "$SKILL/templates/sources.json.tmpl" "$RUNDIR/sources.json"
node "$SKILL/scripts/dedup_sources.js" "$RUNDIR/sources.json" "$TMPROOT/new.json" > /dev/null

# 5. seed report.md with inline citations
cat > "$RUNDIR/report.md" <<'EOF'
# Current stable version of Bun

Bun's latest stable release is tracked on its documentation site ([source](https://bun.sh/docs)) and the GitHub release page ([source](https://github.com/oven-sh/bun/releases)). The release cadence and patch history are documented on the Bun blog ([source](https://bun.sh/blog)).
EOF

# 6. validate
node "$SKILL/scripts/validate_outputs.js" "$RUNDIR"
echo "smoke-quick: PASS"
