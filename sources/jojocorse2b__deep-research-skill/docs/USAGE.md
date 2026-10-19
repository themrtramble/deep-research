# Usage guide

## Evidence-first run

Start by defining the decision, time range, geography and what evidence could
change the conclusion. Search independent angles, including a counter-case.
For every source, record its URL, title, publisher, date, access date, source
type, reliability score and adoption status.

Each evidence entry must point to a source and a precise locator:

```json
{"evidence_id":"e_001","source_id":"s_001","claim_id":"c_001","quote":"short excerpt","locator":"section 2","captured_at":"2026-09-04","supports":true}
```

Each claim should include a confidence value (`high`, `medium`, `low` or
`unknown`) and the evidence IDs that support it. Keep claim confidence separate
from source reliability: a reliable source may still be indirect.

## Reliability rubric

Use the rubric in `references/research-protocol.md`: 5 is primary,
authoritative and current; 0 is unverifiable, deceptive or contradicted by
stronger evidence. Explain the score rather than presenting it as objective
truth.

## Contradictions

Record both positions in `conflicts.jsonl`. A conflict may be `resolved` only
when the resolution explains why one position is better supported. Otherwise
keep it `unresolved` and reflect that uncertainty in the report.

## Report generation

The report builder creates a readable Markdown report from the persistent JSONL
files, and can also produce a simple HTML version. PDF output is optional and
requires `pandoc`; a missing converter is reported instead of silently
pretending that a PDF exists.

## Security checklist

Before sharing or pushing a run:

1. run `scripts/secret_scan.py`;
2. remove private URLs and personal data;
3. retain hashes instead of confidential source documents;
4. review generated HTML/PDF for embedded secrets;
5. inspect `git diff --cached` before committing.

