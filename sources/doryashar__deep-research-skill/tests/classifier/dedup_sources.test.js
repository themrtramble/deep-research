// Unit tests for dedup_sources.js — URL normalization and merge semantics.

import { test } from "node:test";
import assert from "node:assert/strict";
import { normalizeUrl, merge } from "../../skill/scripts/dedup_sources.js";

test("normalizeUrl strips fragment", () => {
  assert.equal(normalizeUrl("https://example.com/docs#intro"), "https://example.com/docs");
});

test("normalizeUrl strips tracking params", () => {
  assert.equal(
    normalizeUrl("https://example.com/x?utm_source=twitter&utm_campaign=foo"),
    "https://example.com/x"
  );
});

test("normalizeUrl keeps non-tracking params", () => {
  assert.equal(
    normalizeUrl("https://example.com/search?q=hello&utm_source=x"),
    "https://example.com/search?q=hello"
  );
});

test("normalizeUrl strips single-trailing slash after path", () => {
  assert.equal(normalizeUrl("https://example.com/docs/"), "https://example.com/docs");
});

test("normalizeUrl normalizes root URLs consistently", () => {
  const a = normalizeUrl("https://example.com/");
  const b = normalizeUrl("https://example.com");
  assert.equal(a, b);
});

test("normalizeUrl passes through invalid URLs", () => {
  assert.equal(normalizeUrl("not a url"), "not a url");
});

test("merge deduplicates by normalized URL", () => {
  const existing = { version: 1, sources: [{ url: "https://a.com/x", title: "A" }] };
  const incoming = [
    { url: "https://a.com/x/#frag", title: "A (dup)" },
    { url: "https://b.com/y", title: "B" },
  ];
  const result = merge(existing, incoming);
  assert.equal(result.sources.length, 2);
  const aEntry = result.sources.find((s) => s.url.includes("a.com"));
  assert.equal(aEntry.title, "A"); // first-seen wins
});

test("merge fills in missing fields from incoming", () => {
  const existing = { version: 1, sources: [{ url: "https://a.com/x" }] };
  const incoming = [{ url: "https://a.com/x", title: "Filled", fetched_at: "2026-04-21" }];
  const result = merge(existing, incoming);
  assert.equal(result.sources[0].title, "Filled");
  assert.equal(result.sources[0].fetched_at, "2026-04-21");
});

test("merge skips entries without url", () => {
  const result = merge(
    { version: 1, sources: [] },
    [{ title: "no url" }, { url: "https://ok.com/" }]
  );
  assert.equal(result.sources.length, 1);
});
