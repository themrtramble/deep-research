# Query Playbook

How to turn sub-questions into search queries that actually discriminate
between answers.

## Pre-flight: kill bad queries before spending budget

Before running a query, check it against these failure classes:

1. **Demographic shopping** — "what percentage of developers use X":
  survey percentages depend on who was surveyed; search the METHODOLOGY.
2. **Numeric traps** — "how much does X cost": costs vary by plan, region,
  date, and are usually marketing-tier answers. Reframe: "X pricing page".
3. **Tutorial phrasing** — "how to do X" returns tutorials, not technical
  evaluations. Reframe: "X limitations / X failure modes / X vs Y".
4. **Generic nouns** — "performance" alone returns nothing usable; name
  the metric: latency, throughput, memory.
5. **Non-Latin/translated topics** — consider both English and the native
  terminology; the best sources may be in another language.

## Query generation per wave

Each wave runs 4–8 queries across four angles:
- **broad**: domain-language phrasing ("CRDT convergence guarantees")
- **specific**: exact entities, versions, error messages
- **contrarian**: "X problems", "X criticism", "X does not scale",
  "X vs Y benchmarks"
- **comparative**: "X alternative", "switched from X to Y"

Include ONE follow-up query generated from the previous wave's learnings
("learnings accumulation"): what partial answer is missing a number,
date, or disconfirming case?

## Search discipline

1. Read beyond the first results page for high-importance claims.
2. Fetch the underlying source of a summary before citing it — a blog
   describing a paper is not evidence until the paper is opened.
3. Use date filters when recency matters; state the date window used.
4. Record failed searches (query + zero useful results) in the run —
  coverage limits are findings, not embarrassments.
5. When results repeat the same 2–3 sources, the search space is
  saturated: stop that angle and check whether you're seeing syndication
  (one source) or genuine corroboration (independent families).

## Following the citation chain

- Backward: which sources does the opened page actually cite? Open the
  load-bearing ones.
- Forward: search who cites THIS source for critique/correction.
- A citation chain ending in "personal communication", a dead link, or a
  404 stops there. Note it; do not launder it.

## Backend detection

Use whatever search the host provides (WebSearch, web_search MCP, browser
tools, or manual URLs given by the user). If multiple backends are
available, prefer the one with recency control. If NONE is available:
state the limitation up front, restrict to user-provided/local sources,
and mark the report `partially-answered` at best. Never simulate search
results.
