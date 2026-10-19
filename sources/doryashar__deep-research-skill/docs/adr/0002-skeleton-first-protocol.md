# ADR 0002 — Skeleton-first + strict write-after-search

- **Status:** accepted, 2026-04-21
- **Inspired by:** altmbr/claude-research-skill

## Context

Subagents told "research X, then write a report" naturally batch searches
before writing. Observed failure modes:

1. **Long silent prefix.** The subagent spends the first half of its run
   issuing search calls with no output on disk. If it's killed (stuck
   detection, context compaction, rate limit), nothing is recoverable.
2. **End-of-run synthesis from memory.** After many searches, the subagent
   tries to write a coherent narrative from its context window — which by
   then has been partially truncated. Claims drift from sources. Citations
   get dropped.
3. **Runaway loops.** Without a write step between searches, the subagent has
   no natural stop signal. It keeps finding "one more interesting thing" and
   never converges.

## Decision

Enforce two protocols on every subagent:

### 1. Skeleton-first

Before any search call, the subagent writes `agents/agent-<N>.md` containing
the H1 scope heading and H2 sub-question headings from `plan.md`. The
skeleton is on disk BEFORE the first search.

### 2. Strict write-after-search

Each loop iteration is:

1. ONE search call.
2. WebFetch up to 3 promising results.
3. Write findings under the relevant H2 with inline URL citations.
4. Append sources to `sources.json` via `dedup_sources.js`.
5. (deep) Append a line to `evidence.jsonl`.
6. Append a heartbeat line.

**No two searches without a write in between.** This is enforced by the
subagent contract prompt and catchable (statically) by
`tests/pressure/run_pressure.js`.

## Alternatives considered

### Write-at-end with checkpoint saves

Reject: checkpoint saves require infrastructure the host doesn't guarantee.
Write-after-search uses the same tool (`Write`) for every step.

### Freeform agent style, enforced via post-hoc critique

Reject: the critique personas find evidentiary gaps, not protocol
violations. A subagent that never wrote anything has no draft for the
critique to examine.

## Consequences

**Positive:**

- Every subagent's workstream is incrementally checkpointed. If killed, the
  parent re-launches with the existing `agent-N.md` pre-loaded.
- Heartbeat line counts monotonically increase — stuck detection becomes a
  trivial delta check (`lines` unchanged across two polls → stuck).
- No "silent prefix" failure; every subagent produces output within one
  search round.

**Negative:**

- More `Write` calls per run. Token cost per agent is ~5–10% higher than
  batch-write styles.
- Subagents that write prematurely can produce fragmentary prose that the
  orchestrator has to rework during synthesis. Mitigated by the report-level
  critique pass.

## Why this is load-bearing

Without skeleton-first + write-after-search:

- Stuck detection stops working (no file to watch).
- Evidence.jsonl can't be appended incrementally.
- Kill-and-relaunch has no partial data to preserve.
- The citation-drift pressure test can't be caught by the validator.

Every one of those is a regression path. The protocol is the foundation
every other guarantee rests on.
