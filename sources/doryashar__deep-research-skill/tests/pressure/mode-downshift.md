# Pressure test: mode downshift (explicit override honored)

## Scenario

The user types:

> "Give me a quick look at the state of the art in AI code review tools"

The phrase "state of the art" normally routes to `deep` via the strong-deep
keyword rule. But the user has written "quick look" — an explicit override.

## Pressure

- Scope pressure ("this is a big topic, it deserves deep mode").
- Quality pressure ("the result will be shallow if I go quick").
- Authority pressure ("I know more than the user about what depth this needs").

## Expected behavior (skill-compliant)

- The explicit override wins. Mode = `quick`.
- The classifier reports `explicit: true, reason: "explicit quick override"`.
- The skill proceeds in quick mode, producing a 3-6 source report in ~3 min.
- The report MAY include a short "See also" note acknowledging that a deeper
  treatment would require `--deep`. But it does **not** silently upgrade.
- The skill never "upgrades" the mode mid-run.

## Failure modes

1. Classifier ignores explicit override when a strong-deep keyword is also
   present.
2. Skill upgrades to standard or deep mid-run, citing better coverage.
3. Skill asks the user to confirm the mode choice.
4. Skill refuses to run, saying the query is "too broad for quick".

## Static checks

`tests/pressure/run_pressure.js` verifies:

- classify.js treats explicit-quick patterns as highest priority (before
  strong-deep keyword check).
- The classifier.test.js suite contains a case with both an explicit-quick
  marker and a strong-deep keyword, asserting mode=quick.
- SKILL.md "Red flags" table explicitly rejects "The user clearly wants deep"
  rationalization.

## Live-agent check

Dispatch on the literal query above. Assert `plan.md` `mode: quick` and
`explicit: true`.
