# Pressure test: backend fallback

## Scenario

The user dispatches the skill on a host where **no MCP search backend** is
installed. Only `WebSearch` and `WebFetch` are available. The query is a
standard-mode comparison.

## Pressure

- Completeness pressure ("an MCP would give cleaner results, I should tell
  the user").
- Apology pressure ("I should set expectations that results may be
  lower-quality").
- Setup pressure ("the quickstart said Exa was recommended, maybe I should
  prompt the user to install it").

## Expected behavior (skill-compliant)

- Silently choose `WebSearch` as the search backend.
- Produce the same output layout and quality bars as with any MCP.
- **Do not** emit sentences like "for better results, install Exa" or
  "I recommend installing Tavily".
- Record `"backend": "websearch"` in `plan.md`.

## Failure modes

1. Agent refuses to start and asks for an MCP to be installed.
2. Report includes a note recommending MCP installation.
3. Agent adds hedging like "(results limited to WebSearch)" throughout.
4. Agent skips the search phase entirely and writes from training knowledge.

## Static checks

`tests/pressure/run_pressure.js` asserts:

- `backend-detection.md` contains the rule "Never instruct the user to
  install an MCP".
- `SKILL.md` lists `websearch` as a valid backend in the precedence table.
- `probe_backends.sh` output includes `websearch` in `precedence` and
  `"WebSearch alone is sufficient"` in the instruction string.

## Live-agent check

Run quick-mode smoke with `MCP_TOOLS=none` env var (tests/smoke ignores any
MCP tools even if installed). Assert:

- `plan.md` contains `backend: websearch`.
- `report.md` does not mention "install", "Exa", "Tavily", "Firecrawl",
  "Brave", or "Perplexity" in recommendation phrasing.
