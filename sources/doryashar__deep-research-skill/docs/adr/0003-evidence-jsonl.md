# ADR 0003 — evidence.jsonl (deep-mode claim ledger)

- **Status:** accepted, 2026-04-21
- **Inspired by:** 199-biotechnologies/claude-deep-research-skill

## Context

Deep-mode runs can take 25+ minutes and involve 20–40 sources across 4–5
subagents. At some point during a long run, the orchestrator's context window
gets compacted — older messages are summarized or truncated. Once that
happens, the orchestrator cannot remember specific claim→source bindings from
earlier in the run.

This matters most for the critique phase. A persona asked "is this claim
backed by a primary source?" has to actually see the cited URL and its
source class (primary/secondary). If that binding lives only in context, the
critique runs on vapor.

## Decision

In deep mode only, each substantive claim gets one line in `evidence.jsonl`:

```json
{"agent": 2, "claim": "…", "url": "…", "quote": "…", "accessed": "ISO8601", "primary": true}
```

Fields:

| Field | Required | Why |
|---|---|---|
| agent | yes | trace back to the subagent's workstream file |
| claim | yes | what's being evidenced |
| url | yes | the source — normalized on write |
| quote | no | short verbatim excerpt; omit with `--no-quotes` |
| accessed | yes | ISO-8601; lets critique flag stale sources |
| primary | no | true = paper/spec/vendor doc, false = blog/summary |

The critique personas receive the full `evidence.jsonl` alongside the draft
report. They can reason about primary/secondary distribution per H2 section,
source freshness, and whether a claim in the draft actually has a supporting
line in the ledger.

The validator (`validate_outputs.js`) enforces the required fields per line.

## Why not include this in standard mode?

Token cost. In standard mode (10–20 sources, one critique pass), the
orchestrator's context still comfortably holds the full source map. Writing
`evidence.jsonl` would just duplicate that information at extra cost.

If a future change raises standard-mode source counts, revisit.

## Why not in quick mode?

Quick mode has inline citations in `report.md` and nothing else. It's a
single-loop run with no critique. `evidence.jsonl` would be dead weight.

## Alternatives considered

### Store evidence in sources.json

Reject: `sources.json` is indexed by URL, not by claim. One URL can back
multiple claims in different sections.

### Stream evidence to the critique personas via context

Reject: defeats the purpose — context compaction is the thing we're
protecting against.

### Store as YAML, not JSONL

Reject: JSONL appends atomically; YAML requires load/merge/dump. JSONL also
parses trivially in any language.

## Consequences

**Positive:**

- Deep-mode critique runs on facts, not on the orchestrator's increasingly
  fuzzy memory.
- The ledger is grepable, diffable, and trivially audited by a human after
  the run.
- Post-hoc analysis of the run (did the skill produce a reasonable source
  distribution?) becomes a `jq` one-liner.

**Negative:**

- Quotes stored verbatim have a privacy dimension. For proprietary /
  authenticated sources, the user should pass `--no-quotes`.
- Extra write per claim in deep mode. Measured overhead: ~50–150 tokens per
  line, vs ~600 tokens saved by not re-fetching.

## Known limitations

- The `primary` flag is set by the subagent and is not independently verified.
  A subagent could mark a blog post as `primary: true`. The Skeptical
  Practitioner persona is the second line of defense — it classifies each
  cited URL independently during critique.
- There's no automatic deduplication of `evidence.jsonl` lines. If two
  subagents independently surface the same claim+URL, you get two lines.
  This is intentional — it signals independent corroboration. The critique
  can merge.
