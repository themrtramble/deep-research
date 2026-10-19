# Adding a search backend

Adding a new MCP search backend to the precedence list takes five small edits
and one fixture.

## Step 1 — Edit the precedence list

In `skill/scripts/probe_backends.sh`:

```sh
"precedence": ["exa", "tavily", "perplexity", "firecrawl", "brave", "<NEW>", "websearch"],
```

Precedence order is a judgment call — see the principle below.

## Step 2 — Add match hints

Still in `probe_backends.sh`, add an entry under `match_hints`:

```json
"<new>": ["mcp__<new>__", "<new>_search", "<new>.search"]
```

Include every plausible tool-name prefix the MCP might use.

## Step 3 — Document in backend-detection.md

Add a row to the "Examples of matching tool names" table in
`skill/references/backend-detection.md` and a one-line note about when the
new backend is preferable to the others.

## Step 4 — Add to SKILL.md precedence reference

The precedence list also appears in `skill/SKILL.md` ("Backend detection"
section). Keep the two in sync, or `tests/pressure/run_pressure.js` will
start drifting — one of the static checks asserts the SKILL mentions
`websearch` as a valid backend.

## Step 5 — Add a fixture (optional but recommended)

Create `tests/fixtures/cached-web/backends/<new>.json` with a canned search
response so smoke tests can exercise the new backend path.

## Principle: precedence ordering

1. **Agent-optimized APIs** (return LLM-ready summaries with citations) first — Exa, Tavily, Perplexity.
2. **Crawl/scrape APIs** (Firecrawl) after — they're slower but more general.
3. **Classic web search** (Brave) last among MCPs — broad recall but noisier.
4. **`WebSearch` is always the floor.** Never below another MCP. Never removed.

If a new backend sits between these tiers, place it at the boundary you think
best matches its strengths. Don't be afraid to adjust after a week of use.

## What NOT to do

- **Do not** tell the user to install the new MCP for "better results". The
  skill must work with `WebSearch` alone. If your backend requires setup, that
  documentation lives in the backend's own readme, not in the skill.
- **Do not** short-circuit the fallback chain. Every backend can fail for
  rate-limit or auth reasons; the skill must continue to the next one.
- **Do not** couple `WebFetch` to a specific backend. Page retrieval is
  always `WebFetch`, regardless of which search provider chose the URL.

## Testing your change

```
make test              # classifier + pressure static checks
make smoke-standard    # exercises the backend-selection path
```

If `run_pressure.js` fails on `probe_backends.sh instruction forbids 'install an MCP' message`,
your edits accidentally removed that rule. Put it back.
