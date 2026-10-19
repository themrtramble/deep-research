# Research protocol

## Source reliability rubric

Score each source from 0 to 5 and explain the score:

- **5** — primary, authoritative, current, directly relevant, transparent
  methodology or provenance;
- **4** — strong institutional or expert source with minor limitations;
- **3** — useful secondary source with identifiable editorial or methodological
  limits;
- **2** — weak secondary source, advocacy, marketing, or incomplete context;
- **1** — anecdotal, unsourced, stale, or materially biased;
- **0** — inaccessible, unverifiable, deceptive, or contradicted by stronger
  evidence.

Reliability is not the same as claim support. A reliable source can be indirect;
an unreliable source can accidentally contain a true fact.

## Minimum evidence record

Each `evidence.jsonl` line should contain:

```json
{"evidence_id":"e_001","source_id":"s_001","claim_id":"c_001","quote":"short excerpt","locator":"section or page","captured_at":"YYYY-MM-DD","supports":true}
```

Use short excerpts and a precise locator. Store a hash of large downloaded
artifacts instead of copying copyrighted documents into the research folder.

## Conflict record

```json
{"conflict_id":"x_001","claim_ids":["c_001","c_002"],"positions":["...","..."],"resolution":"...","status":"resolved|unresolved"}
```

Do not force a resolution when the evidence genuinely remains mixed.

## Claim checks

- Every numerical claim has a source edge and matching units/date.
- Every quotation is verbatim, short, and attributed to a source locator.
- Every causal claim distinguishes correlation from demonstrated mechanism.
- Every recommendation names the evidence, assumptions, and main downside.
- Contradictory evidence is visible rather than silently omitted.

