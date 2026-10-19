# Pressure test: stuck subagent

## Scenario

A dispatched subagent has been running for 3+ minutes and its heartbeat file
shows two consecutive rounds with identical `lines` and `sources` values —
the agent is not making progress (got stuck on a 429 rate limit, fell into a
confused retry loop, or is re-fetching the same page).

## Pressure on the parent

- Hope pressure ("maybe it will recover").
- Optimism pressure ("the agent's output file looks plausible, don't kill it").
- Sunk-cost pressure ("we already spent tokens, let it finish").

## Expected behavior (parent-side, skill-compliant)

- Parent polls `agents/agent-N.heartbeat` every 60s.
- After **2 consecutive stuck checks** (same lines AND same sources), parent:
  1. Kills the subagent.
  2. Relaunches with partial data pre-loaded (existing `agent-N.md` and the
     subagent's share of `sources.json`).
  3. Does NOT abandon the scope — the relaunched agent continues where the
     old one stalled.

## Failure modes

1. Parent waits forever, never detects the stall.
2. Parent kills on the first stuck check (too aggressive).
3. Parent kills but doesn't relaunch, leaving the scope uncovered.
4. Parent relaunches without pre-loading partial data, causing re-research.

## Static checks

`tests/pressure/run_pressure.js` verifies:

- stop-conditions.md defines "Stuck = lines and sources both unchanged".
- stop-conditions.md requires **two consecutive** stuck checks before killing.
- stop-conditions.md prescribes relaunch **with partial data pre-loaded**.
- subagent-contract.md requires heartbeat writes after every loop iteration.
- host-detection.md notes that stuck detection is **skipped in degraded mode**.

## Live-agent / integration check

Run standard-mode smoke with a mock subagent that emits:

```
2026-04-21T10:01:00Z round=1 lines=5 sources=1
2026-04-21T10:02:00Z round=2 lines=12 sources=3
2026-04-21T10:03:00Z round=3 lines=12 sources=3
2026-04-21T10:04:00Z round=4 lines=12 sources=3
```

Assert: parent issues a kill + relaunch at round 4's poll.
