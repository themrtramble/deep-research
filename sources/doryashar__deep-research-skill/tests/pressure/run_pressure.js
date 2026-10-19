#!/usr/bin/env node
// run_pressure.js — static checks that the skill still carries the rules that
// prevent each documented pressure scenario. These are guardrails against
// regressions where someone edits SKILL.md or a reference and accidentally
// removes a countermeasure.
//
// This is NOT a substitute for live-agent pressure testing per the
// superpowers:writing-skills methodology. It's a cheap CI proxy that catches
// documentation drift. Live-agent tests go in tests/integration/.

import { readFileSync, existsSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");

function read(relpath) {
  const p = resolve(ROOT, relpath);
  if (!existsSync(p)) throw new Error(`missing required file: ${relpath}`);
  return readFileSync(p, "utf8");
}

const checks = [];

function check(name, predicate) {
  checks.push({ name, predicate });
}

// ── citation-drift countermeasures ────────────────────────────────
check("SKILL.md mentions inline-URL citation discipline", () => {
  const s = read("skill/SKILL.md").toLowerCase();
  return s.includes("inline-url") || s.includes("inline url");
});

check("subagent-contract.md requires ([source](https://url)) format", () => {
  return read("skill/references/subagent-contract.md").includes("([source](https://url))");
});

check("output-schemas.md forbids bibliographies-in-lieu-of-inline", () => {
  const s = read("skill/references/output-schemas.md").toLowerCase();
  return s.includes("no bibliographies") || s.includes("no bibliography");
});

check("validate_outputs.js enforces min inline citations", () => {
  return read("skill/scripts/validate_outputs.js").includes("inline URL citations");
});

check("validate_outputs.js flags 'recent reports' drift", () => {
  return /recent reports/i.test(read("skill/scripts/validate_outputs.js"));
});

// ── runaway-loop countermeasures ──────────────────────────────────
check("subagent-contract.md enforces write-after-search loop", () => {
  const s = read("skill/references/subagent-contract.md");
  return /STRICT WRITE-AFTER-SEARCH/.test(s) && /Batch multiple searches before writing/.test(s);
});

check("stop-conditions.md defines stuck = lines and sources unchanged", () => {
  const s = read("skill/references/stop-conditions.md").toLowerCase();
  return s.includes("lines") && s.includes("sources") && s.includes("unchanged");
});

// ── stuck-subagent countermeasures ────────────────────────────────
check("stop-conditions.md requires two consecutive stuck checks", () => {
  return /two consecutive/i.test(read("skill/references/stop-conditions.md"));
});

check("stop-conditions.md prescribes relaunch with partial data", () => {
  const s = read("skill/references/stop-conditions.md").toLowerCase();
  return s.includes("relaunch") && (s.includes("partial data") || s.includes("pre-loaded"));
});

check("host-detection.md notes stuck detection skipped in degraded mode", () => {
  const s = read("skill/references/host-detection.md").toLowerCase();
  return s.includes("degraded") && (s.includes("skip") || s.includes("not meaningful"));
});

check("subagent-contract.md requires heartbeat writes", () => {
  return /heartbeat/i.test(read("skill/references/subagent-contract.md"));
});

// ── mode-downshift countermeasures ────────────────────────────────
check("classify.js checks explicit overrides before strong-deep keywords", () => {
  const src = read("skill/scripts/classify.js");
  const explicitIdx = src.indexOf("EXPLICIT_QUICK");
  const strongDeepIdx = src.indexOf("STRONG_DEEP_KEYWORDS");
  const explicitMatchIdx = src.search(/anyMatch\(q, EXPLICIT_QUICK\)/);
  const strongDeepMatchIdx = src.search(/containsAny\(nq, STRONG_DEEP_KEYWORDS\)/);
  return explicitIdx > -1 && strongDeepIdx > -1 && explicitMatchIdx < strongDeepMatchIdx;
});

check("SKILL.md red-flags rejects 'user clearly wants deep' rationalization", () => {
  const s = read("skill/SKILL.md").toLowerCase();
  return s.includes("explicit override") || s.includes("honor the override");
});

// ── skip-critique-on-agreement countermeasures (LOAD-BEARING) ─────
check("critique-personas.md requires Persona 2 to find 3 counter-positions even if stretched", () => {
  const s = read("skill/references/critique-personas.md");
  return /MUST find 3 counter-positions/i.test(s) || /find 3 counter-positions even if you have to stretch/i.test(s);
});

check("critique-personas.md accepts false-positive objections as the price of independence", () => {
  const s = read("skill/references/critique-personas.md").toLowerCase();
  return s.includes("accept false positives") || s.includes("price of independence");
});

check("SKILL.md red-flags rejects 'sources agree, skip critique'", () => {
  const s = read("skill/SKILL.md").toLowerCase();
  return s.includes("sources agree") && s.includes("critique");
});

check("stop-conditions.md loop-back evaluates persona output, not pre-run source similarity", () => {
  const s = read("skill/references/stop-conditions.md");
  return /Persona 1|Persona 2|Persona 3|Skeptical Practitioner|Adversarial Reviewer|Implementation Engineer/.test(s);
});

check("critique-personas.md requires all three personas run in parallel", () => {
  const s = read("skill/references/critique-personas.md").toLowerCase();
  return s.includes("all three personas") && s.includes("parallel");
});

check("critique-personas.md documents same-gap escape (bounds the loop)", () => {
  const s = read("skill/references/critique-personas.md").toLowerCase();
  return s.includes("same-gap") || s.includes("same gap");
});

check("critique-personas.md hard-caps iterations at 3", () => {
  const s = read("skill/references/critique-personas.md");
  return /3 critique iterations|Hard cap: 3|Hard cap.{0,20}3/.test(s);
});

// ── backend-fallback countermeasures ──────────────────────────────
check("backend-detection.md forbids telling user to install MCP", () => {
  const s = read("skill/references/backend-detection.md").toLowerCase();
  return s.includes("never instruct") || s.includes("never tell");
});

check("SKILL.md lists websearch in the precedence", () => {
  return /websearch/i.test(read("skill/SKILL.md"));
});

check("probe_backends.sh instruction forbids 'install an MCP' message", () => {
  return read("skill/scripts/probe_backends.sh").includes("NEVER tell the user to install");
});

check("subagent-contract.md bans 'install an MCP' in its NEVER list", () => {
  const s = read("skill/references/subagent-contract.md").toLowerCase();
  return s.includes("install an mcp");
});

// ── run ───────────────────────────────────────────────────────────
let passed = 0;
let failed = 0;
for (const { name, predicate } of checks) {
  let ok = false;
  let err;
  try { ok = Boolean(predicate()); } catch (e) { err = e; }
  if (ok) { console.log(`  ok  ${name}`); passed += 1; }
  else { console.error(`  FAIL ${name}${err ? ` — ${err.message}` : ""}`); failed += 1; }
}

console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
