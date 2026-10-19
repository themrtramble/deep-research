# Interaction Contract Checks

Read this reference only when a change crosses agent, client, helper, API, or
platform-runtime boundaries.

Map the complete path across the client skill or UI, MCP/helper layer, API
validation, persisted state, worker/runtime behavior, readiness or status
query, review or execution gate, feedback/handoff evidence, and regression
coverage.

Challenge these failure patterns:

- A capability is advertised before the downstream path can complete it or
  reject it with an actionable remedy.
- A support matrix is used as a permissive runtime flag instead of release
  guidance.
- A pseudo-state represents partial implementation rather than a real product
  state.
- Diagnostic-only evidence is routed through formal production objects.
- A failure hides who owns remediation or whether the user should retry,
  re-upload, review, or wait for downstream execution.

Identify separately which boundary owns truth and which owns remediation. Do
not collapse failures that require different actions, such as an ingest failure
requiring re-upload and a downstream materialization failure requiring mapping,
review, or worker remediation.
