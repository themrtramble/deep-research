# Handoff Contract (Deep Research side)

Deep Research answers: *what is known, what evidence exists, where it
came from, how reliable it is, which claims are disputed, what's missing.*
Deep Analysis answers: *what the evidence establishes, which explanations
survive, what assumptions remain, what conclusions are justified.*

Both skills work independently. The handoff is a JSON artifact — no direct
skill-to-skill invocation is assumed.

## Outgoing: research-package.json

Built by `scripts/package.py build <run_dir> --answer-status <status>`:

```json
{
  "schema": "deep-research-package/1",
  "question": "string",
  "answer_status": "fully-answered | partially-answered | unanswerable",
  "claims": [
    {
      "claim_id": "CL-xxxxxxxx",
      "claim": "single falsifiable sentence",
      "importance": 4,
      "uncertainty": "established | likely | contested | weak | unknown",
      "evidence_ids": ["E0001"],
      "source_ids": ["S0001"],
      "stances": ["supports"]
    }
  ],
  "sources": [
    {"source_id": "S0001", "url": "https://...", "title": "...",
     "source_type": "primary", "quality": 4, "accessed_at": "..."}
  ],
  "conflicts": [{"conflict_id": "C0001", "positions": ["...", "..."],
                 "status": "unresolved"}],
  "gaps": ["what is missing and why"],
  "coverage": {"mode": "standard", "sources": 12, "evidence": 34,
                "unresolved_conflicts": 1},
  "limitations": ["honest constraints of this run"]
}
```

Guarantees: claims reference only listed sources; secret-free (verified
fail-closed); answer_status reflects documented gaps; every claim carries
its uncertainty honestly.

## Incoming: research-request.json

If deep-analysis (or the user) hands you a request file with schema
`deep-analysis-request/1`:

```json
{
  "schema": "deep-analysis-request/1",
  "requests": [
    {
      "question": "targeted question",
      "why_needed": "which conclusion depends on it",
      "decision_at_stake": "what decision it unblocks"
    }
  ]
}
```

Treat each request as a new run (or a continuation of the existing run):
classify it, plan, and research it with the same rigor — requests do NOT
bypass the evidence rules. Prioritize questions whose `decision_at_stake`
is load-bearing.

## Manual handoff

When running outside an orchestrator: give the user `package.json` and
tell them: "hand this to deep-analysis (or attach it when asking for
analysis) — it contains the full evidence chain." When consuming a
research package as deep-research input (e.g., a follow-up question),
load its claims/sources into a new run's ledger via `add-source`/
`add-evidence` so provenance is preserved, and note the origin run in
`plan.md`.
