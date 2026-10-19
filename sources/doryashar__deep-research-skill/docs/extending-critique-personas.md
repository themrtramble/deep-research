# Extending critique personas

The three shipped personas (Skeptical Practitioner, Adversarial Reviewer,
Implementation Engineer) are a base, not a ceiling. You can add personas for
a specific domain — just don't exceed 5 total.

## When to add

- **Domain-specific rigor check** — e.g., a "Medical Evidence Reviewer" for
  health-research runs that checks PICO framing and effect sizes.
- **Audience-specific gap finder** — e.g., "Executive Summary Reviewer" that
  asks whether non-technical readers can act on the report.
- **Ethics / safety reviewer** — e.g., flags recommendations that have
  downstream harm potential.

## When NOT to add

- To reinforce a persona that already covers the ground. Three copies of the
  Skeptical Practitioner with different wording do not triple rigor; they
  correlate.
- To compensate for a weak Adversarial Reviewer. Fix the Adversarial prompt
  instead.
- Because "more personas = more thorough". Beyond ~5 personas, returns
  diminish sharply and the loop-back logic becomes noisy.

## How to add

### 1. Write the persona prompt

Follow the shape of the three existing ones:

```
You are <role> reading this report to <specific job>. Your job is
<one-sentence contract>.

For each <load-bearing claim | recommendation | counter-position>:
  1. <step>
  2. <step>
  3. <step>

Output: <JSON schema>.

Rules:
  - <hard constraint>
  - <hard constraint>
```

Every persona's output must be a JSON object the orchestrator can parse.
Free-form prose is not a persona — it's a review.

### 2. Add the persona to `skill/references/critique-personas.md`

Insert alongside the other three. Match the heading style (`## Persona N — <Name>`).

### 3. Update the loop-back rule

In the same file, add a new entry to the **Loop back iff** list:

```
5. <Your persona> returns <specific failure signal>.
```

Also add a row to `stop-conditions.md`'s "Coverage checklist" if your
persona gates a new completeness requirement.

### 4. Add a pressure test

Create `tests/pressure/<your-persona>.md` documenting:

- The scenario your persona catches.
- The pressure the orchestrator might feel to skip it.
- Static checks the `run_pressure.js` runner can assert.

Then add those static checks to `tests/pressure/run_pressure.js`.

### 5. Bump the spawn cap

Deep mode's default `--max-spawns=30` assumes 3 personas × 3 iterations + 3
re-dispatches. With 4 personas the math changes; bump the deep default by 5
per added persona.

## Failure modes to avoid

- **Persona collusion** — all personas share a base model. A persona that
  "agrees with the draft" is adding noise, not signal. Make each persona's
  job adversarial to the report in some dimension.
- **Nit personas** — personas that flag cosmetic issues (tone, grammar)
  should not gate loop-back. Loop-back is reserved for evidentiary gaps.
- **Double-counting** — if Persona 4's output is always a superset of
  Persona 1's, drop Persona 4.

## Running the full suite after a change

```
make test
make smoke-deep
```

The deep smoke run emits a synthetic research directory that includes a
`## Where sources disagree` section; your added persona should not cause the
validator to reject it.
