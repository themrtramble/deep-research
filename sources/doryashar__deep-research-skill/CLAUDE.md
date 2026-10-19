# deep-research-skill — project conventions

- Tests live in `./tests/`, docs live in `./docs/`, shipped skill files live in `./skill/`.
- Every new feature ships with a test. Classifier changes require a case in `tests/classifier/classifier.test.js`; orchestration changes require a pressure scenario in `tests/pressure/`.
- `skill/SKILL.md` is the entry point. Keep it ≤ 700 words. Push details into `skill/references/*.md` which are loaded on demand.
- The skill must work on **both** Claude Code and opencode. Never hard-require a specific tool name — detect availability first (`host-detection.md`, `backend-detection.md`).
- Citations are inline URLs in markdown (`[…](https://url)`) — never bibliographies, never "recent reports show…" without a URL.
- Skeleton-first: every subagent creates its output file with headings before calling any search tool. Strict write-after-search afterward.
- Run `make test` before committing.
