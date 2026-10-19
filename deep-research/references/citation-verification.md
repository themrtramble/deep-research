# Citation Verification

Fabricated citations are the signature failure of model-driven research.
The iron rule: **a citation is verified against the opened source, or it
does not ship.**

## Citation hallucination taxonomy (what to catch)

1. **Total fabrication** — author/title/venue that never existed.
2. **Plausible-author** — a real author attached to a paper they never
   wrote. Verify authorship, not just name existence.
3. **Incomplete** — real paper, wrong year/venue/DOI.
4. **Partial-mashup** — title of one paper merged with authors of another
   (usually from a related-work section).
5. **Subtle** — everything right, page number or figure reference invented.

Counter-patterns: author spoofing (famous name + fake venue), venue
exploitation (real journal + fake DOI), temporal masking (plausible year
shift), DOI misdirection (resolving to a different paper).

## Verification procedure (high-importance citations)

1. Open the source URL / resolve the DOI. If it 404s or pays-walls after
   reasonable effort: mark `[unverified]` or drop it. "Difficult to
   verify" is not a verdict.
2. Check the load-bearing claim actually appears in the source — find the
   passage, record it as `quote_or_locator`.
3. Numbers: confirm units, dates, and the comparison baseline from the
   ORIGINAL source, not a summary of it.
4. Cross-check dates for temporal masking: paper predating the technology
   it allegedly describes?

## Citogenesis & circular citations

Symptoms: many "sources" quoting identical unusual phrasing; web rings
citing each other; one press release mirrored everywhere.
Procedure: pick an unusual verbatim phrase from the claim and search it —
the oldest dated appearance is the likely origin. If the origin is a
single low-quality source, the cluster is ONE source, and the claim is
`single-source` regardless of apparent corroboration.

## URL sanity (mechanical, via validate.py)

- `example.com`, `localhost`, `insert-url` patterns = fabricated.
- `doi.org/10.TODO` patterns = placeholder, must fail.
- Every report URL should have been opened in this run — validators check
  claim-to-ledger traceability, but you are the one who opened them.

## Quoting rules

- Quote verbatim or give a locator (section, table, timestamp) — not
  "somewhere in the paper".
- Never stitch fragments with ellipses into a new claim the source
  doesn't make.
- Translate quotes faithfully; mark translations as such.
