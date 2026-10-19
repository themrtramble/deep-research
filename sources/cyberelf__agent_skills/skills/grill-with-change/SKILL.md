---
name: grill-with-change
description: Stress-test and refine an OpenSpec change through one-question-at-a-time, phase-gated discussion and batched write-back. Use when the user wants to interrogate, complete, or improve a change while preserving decision fidelity across proposal.md, design.md, specs, and tasks.md.
---

Interrogate an OpenSpec change until its requirements, design, specs, and tasks
tell one coherent story. Challenge terminology against project docs and code,
sharpen vague language, and probe boundaries with concrete scenarios.

## Hard Rules

- Ask exactly one user-facing question at a time and wait for the answer. State
  why the decision matters and recommend an answer when one is defensible.
- Inspect local evidence instead of asking questions it can answer.
- Only user-confirmed decisions may become normative. Repository facts provide
  context; assistant recommendations remain `OPEN` until confirmed.
- During a phase, update only working state. Batch-write formal artifacts after
  the user confirms that the phase can close.
- Do not implement application code or edit `CONTEXT.md` or ADRs. Edit only the
  target change's OpenSpec artifacts.
- Answer side questions directly, then return to the current branch unless the
  answer changes the decision tree.

## Locate And Inspect The Change

Accept a change id, a reference such as "this change," or a partial change idea.
If the target is unclear, run:

```bash
openspec list --json
```

Use the only active change automatically. If several exist, ask which one; if
none exist, ask whether to create a change or refine a proposal.

Before grilling, run:

```bash
openspec status --change "<change-id>" --json
```

Read the change's `proposal.md`, `design.md`, `tasks.md`, and
`specs/**/spec.md`, plus relevant existing specs, referenced docs or ADRs, named
code paths, and validation commands. Before creating a missing artifact, get
its current template and rules:

```bash
openspec instructions <artifact-id> --change "<change-id>" --json
```

Do not copy instruction metadata into artifacts.

## Working State

Maintain three views of the same discussion:

- **Change map:** outcome, actors, scope and non-goals, capability deltas,
  scenarios, design commitments, tasks, validation, contradictions, and risks.
- **Panorama:** a compact visible phase/progress/current-branch view. Show it
  before the first question, before ordinary questions in compact form, and
  redraw it when the decision tree changes materially.
- **Decision ledger:** confirmed, deferred, open, rejected, and superseded
  branches. For sessions likely to span turns, persist it as
  `decision-log.md` inside the change.

For each material decision, record its normalized meaning, rationale when
important, exclusions, phase, and affected artifacts. Qualified acceptance
confirms only the accepted portion. When corrected, mark the old decision
`SUPERSEDED` and reconcile anything that inherited it.

Keep a downstream-impact queue in the ledger or plan. Recording an impact does
not authorize an early formal write.

## Phase Transaction

Run every phase as one transaction:

1. **Discover:** inspect evidence and map the phase's branches.
2. **Discuss:** ask one question at a time; update only the map, panorama,
   ledger, plan, and impact queue. Keep formal artifacts frozen.
3. **Close:** summarize confirmed decisions, exclusions, deferrals, and risks;
   ask one focused question to confirm phase closure.
4. **Commit:** re-read the ledger and batch-write every affected artifact that
   can express the confirmed decisions without inventing a later decision.
5. **Validate:** inspect the diff and run the cheapest relevant OpenSpec check.

Do not infer closure from silence or a topic change. Intermediate validation may
report missing downstream artifacts or queued inconsistencies; do not update
later content merely to make validation green early.

If a later phase exposes a missing or changed upstream decision, pause, reopen
the upstream phase, confirm and commit it, then resume. Fix transcription and
formatting errors directly; reopen a phase when a fix needs a product decision.

If the user explicitly requests an early artifact write, treat it as a
provisional snapshot, label it accordingly, and reconcile it at phase close.

## Phase Guide

| Phase | Resolve | Batch-write at close |
| --- | --- | --- |
| Requirements | Actor, outcome, defaults, scope/non-goals, compatibility, constraints, important failure behavior | `proposal.md` and directly entailed spec requirements/scenarios; queue design and task impacts |
| Design | Ownership/source of truth, flows, interfaces/versioning, state, authorization/audit, failure/degraded behavior, migration/rollback, alternatives | `design.md` and specs whose observable behavior changed; queue task impacts |
| Specs | Precise behavioral requirements with observable positive, negative, conflict, and degraded scenarios where material | All affected `specs/<capability>/spec.md` files |
| Tasks | Dependency-ordered implementation, tests, docs, migration, and validation work justified by committed artifacts | `tasks.md` |
| Final Sweep | Cross-artifact fidelity and consistency; no new product decisions | Consistency and transcription fixes only |

Specs describe what the system shall do, not implementation. Tasks must cover
confirmed behavior without expanding scope. Create missing capability specs
only after reading their OpenSpec instructions.

For changes spanning agents and platform runtime, read
[references/interaction-contracts.md](references/interaction-contracts.md)
before completing Design.

## Commit Fidelity

At each phase commit:

- Apply confirmed decisions wherever they can be expressed without resolving an
  unconfirmed downstream choice.
- Keep deferred or proposed content in the ledger unless an explicit formal
  open-questions section helps readers without disguising a blocker.
- Compare the diff with the ledger, reject added behavior, mark applied impacts
  resolved, and queue newly discovered impacts.

## Final Validation

Before finishing:

1. Confirm all phases are closed and the impact queue is empty.
2. Re-read the ledger and every artifact. Check terminology, requirement and
   scenario alignment, design rationale, task justification, compatibility,
   migration, rollback, authorization, failure behavior, and validation.
3. Search for deprecated terms, pseudo-states, removed tools, or stale
   capability claims.
4. Run, fix artifact issues, and run again:

   ```bash
   openspec validate "<change-id>"
   openspec status --change "<change-id>"
   ```

Finish with the change id/location, artifacts updated, key confirmed decisions,
open questions, and validation result. Do not declare completion while an open
question blocks coherent artifacts.
