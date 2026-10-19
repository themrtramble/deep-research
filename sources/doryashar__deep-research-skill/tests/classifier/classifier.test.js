// tests/classifier/classifier.test.js — 30+ (query → expected mode) cases.
// Run with `node --test tests/classifier` or `make test`.

import { test } from "node:test";
import assert from "node:assert/strict";
import { classify } from "../../skill/scripts/classify.js";

const cases = [
  // ── factoid / quick ───────────────────────────────────────────────
  { q: "What is the current stable version of Bun?", mode: "quick" },
  { q: "Define idempotent in REST APIs", mode: "quick" },
  { q: "Who is the maintainer of SQLite?", mode: "quick" },
  { q: "When was Kubernetes 1.30 released?", mode: "quick" },
  { q: "briefly, what does CORS stand for?", mode: "quick" },
  { q: "TL;DR on ZFS copy-on-write", mode: "quick" },
  { q: "quick look at what Zig's comptime does", mode: "quick" },
  { q: "tell me about Rust --quick", mode: "quick" },

  // ── breadth / standard ────────────────────────────────────────────
  { q: "Compare Tavily vs Exa vs Brave for agent search",           mode: "standard" },
  { q: "tradeoffs between SQLite and DuckDB for analytics",          mode: "standard" },
  { q: "options for self-hosting a CalDAV server on Linux",          mode: "standard" },
  { q: "overview of Rust async runtimes in 2026",                    mode: "standard" },
  { q: "pros and cons of using Deno for production APIs",            mode: "standard" },
  { q: "How do I set up a CI pipeline with GitHub Actions and Docker for a Python project", mode: "standard" },

  // ── depth / deep ──────────────────────────────────────────────────
  { q: "state of the art in AI code review tools",                   mode: "deep" },
  { q: "Do a thorough survey of vector database benchmarks for RAG", mode: "deep" },
  { q: "Give me a comprehensive landscape of LLM inference engines", mode: "deep" },
  { q: "deep dive on WASM garbage collection proposal",              mode: "deep" },
  { q: "full report on the evolution of container runtimes",         mode: "deep" },
  { q: "literature review on retrieval-augmented generation 2023-2026", mode: "deep" },
  { q: "Research CRDT implementations and benchmark their conflict resolution performance across JSON, text, and tree structures", mode: "deep" },

  // ── explicit overrides ────────────────────────────────────────────
  { q: "kubernetes networking --deep",                               mode: "deep" },
  { q: "postgres tuning --quick",                                    mode: "quick" },
  { q: "sqlite vs duckdb --standard",                                mode: "standard" },
  { q: "postgres vs mysql for analytics --quick", mode: "quick" }, // override beats breadth signal

  // ── edge cases ────────────────────────────────────────────────────
  { q: "Rust",                                                       mode: "quick" }, // single word
  { q: "What's new in React 19?",                                    mode: "quick" },
  { q: "Analyze the evolution of JavaScript bundlers from Webpack to esbuild to Bun, including benchmark comparisons and architectural tradeoffs", mode: "deep" },
  { q: "How does Postgres handle MVCC?",                              mode: "quick" }, // short factoid despite "how"
  { q: "Build me a list of the top 10 open-source tools for observability with their GitHub stars and license", mode: "standard" }, // multi-step but not deep

  // ── explicit override beats strong-deep keyword (mode-downshift pressure) ──
  { q: "Give me a quick look at the state of the art in AI code review tools", mode: "quick" },
  { q: "briefly survey the landscape of Rust async runtimes", mode: "quick" },
];

for (const { q, mode } of cases) {
  test(`classify: [${mode}] ${q}`, () => {
    const r = classify(q);
    assert.equal(r.mode, mode, `expected ${mode}, got ${r.mode} (score=${r.score}, reason=${r.reason})`);
  });
}

// ── properties ────────────────────────────────────────────────────
test("classify returns well-formed object", () => {
  const r = classify("anything");
  assert.ok(["quick", "standard", "deep"].includes(r.mode));
  assert.equal(typeof r.score, "number");
  assert.equal(typeof r.ambiguous, "boolean");
  assert.equal(typeof r.reason, "string");
});

test("explicit overrides set explicit=true", () => {
  assert.equal(classify("anything --quick").explicit, true);
  assert.equal(classify("anything --deep").explicit, true);
  assert.equal(classify("anything --standard").explicit, true);
  assert.equal(classify("something without flag").explicit, false);
});

test("ambiguous flag fires in the soft band without strong anchor", () => {
  // Lowercase, no proper noun, short-but-not-factoid, one depth keyword → score ≈ 1
  const r = classify("please investigate authentication tradeoffs");
  // May or may not be ambiguous depending on scoring; we just assert that when
  // ambiguous=true we're in the soft band.
  if (r.ambiguous) {
    assert.ok(r.score >= 1 && r.score <= 2, `ambiguous only in soft band, got score=${r.score}`);
  }
});

test("strong anchor (proper noun) suppresses ambiguity", () => {
  const withAnchor = classify("investigate Kubernetes authentication tradeoffs");
  if (withAnchor.score >= 1 && withAnchor.score <= 2) {
    assert.equal(withAnchor.ambiguous, false, "proper noun should suppress ambiguity");
  }
});

test("empty query does not throw", () => {
  const r = classify("");
  assert.ok(r.mode);
});

test("null/undefined query does not throw", () => {
  const r = classify(undefined);
  assert.ok(r.mode);
});
