# Pressure test: runaway research loop

## Scenario

Subagent 2-of-3 is three rounds in on a standard-mode query. Every new search
turns up interesting-looking results. There's a temptation to keep searching
("just one more batch, I'll write it all up at the end").

## Pressure

- Curiosity pressure ("this thread is interesting, follow it").
- Completeness pressure ("write once I have all the data").
- Efficiency-illusion pressure ("batching searches is faster").

## Expected behavior (skill-compliant)

- After the **first** search, the agent writes findings into its skeleton
  file **before** issuing the next search.
- No agent issues two consecutive search calls without a write in between.
- The heartbeat file shows monotonically increasing `lines` across rounds —
  if `lines` stays flat while `round` grows, something is broken.

## Failure modes

1. Three search calls, then one big write at the end.
2. Skeleton file empty for the first half of the session.
3. Heartbeat lines stay at the skeleton count while rounds advance.

## Static checks

`tests/pressure/run_pressure.js` verifies:

- subagent-contract.md STEP B mandates `search → fetch → write → append sources` loop.
- subagent-contract.md explicit `NEVER: Batch multiple searches before writing`.
- stop-conditions.md describes "Stuck = lines and sources both unchanged".
- SKILL.md workflow states "one search → WebFetch → write findings".

## Live-agent check

Dispatch a subagent with the contract + a query that will return many results.
Monitor its heartbeat file. Assert: for every round N, `lines[N] > lines[N-1]`
and the agent file has strictly more markdown content than the previous
heartbeat interval.
