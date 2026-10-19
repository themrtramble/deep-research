// Unit tests for validate_outputs.js — runs the validator via child_process
// against synthetic research dirs (both "good" and deliberately broken).

import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, writeFileSync, rmSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { spawnSync } from "node:child_process";

const SCRIPT = new URL("../../skill/scripts/validate_outputs.js", import.meta.url).pathname;

function run(dir) {
  return spawnSync("node", [SCRIPT, dir], { encoding: "utf8" });
}

function scaffold(contents) {
  const root = mkdtempSync(join(tmpdir(), "drs-validate-"));
  writeFileSync(join(root, "plan.md"), contents.plan ?? "# plan\n");
  writeFileSync(join(root, "report.md"), contents.report ?? "# report\n");
  writeFileSync(join(root, "sources.json"), contents.sources ?? JSON.stringify({ version: 1, sources: [] }));
  if (contents.evidence !== undefined) writeFileSync(join(root, "evidence.jsonl"), contents.evidence);
  if (contents.agents) {
    mkdirSync(join(root, "agents"));
    for (const [name, body] of Object.entries(contents.agents)) {
      writeFileSync(join(root, "agents", name), body);
    }
  }
  return root;
}

test("accepts a well-formed quick-mode run", () => {
  const citations = Array.from({ length: 3 }, (_, i) => `claim ${i} ([src](https://example.com/${i}))`).join(". ") + ".";
  const dir = scaffold({
    report: `# Bun version\n\n${citations}\n`,
    sources: JSON.stringify({
      version: 1,
      sources: [
        { url: "https://example.com/0" },
        { url: "https://example.com/1" },
        { url: "https://example.com/2" },
      ],
    }),
  });
  const r = run(dir);
  assert.equal(r.status, 0, `expected success, got stderr:\n${r.stderr}`);
  rmSync(dir, { recursive: true });
});

test("rejects report.md with no H1", () => {
  const dir = scaffold({
    report: "no heading at all, just a paragraph with [a](https://a.com) and [b](https://b.com) and [c](https://c.com).",
  });
  const r = run(dir);
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /no H1/);
  rmSync(dir, { recursive: true });
});

test("rejects report.md with too few citations", () => {
  const dir = scaffold({
    report: "# A report\n\nA claim with just [one](https://one.com) citation.\n",
  });
  const r = run(dir);
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /inline URL citations/);
  rmSync(dir, { recursive: true });
});

test("rejects duplicate sources after normalization", () => {
  const cites = Array.from({ length: 3 }, (_, i) => `[x](https://a.com/#frag${i})`).join(" ");
  const dir = scaffold({
    report: `# r\n${cites}\n`,
    sources: JSON.stringify({
      version: 1,
      sources: [
        { url: "https://a.com/docs" },
        { url: "https://a.com/docs/?utm_source=x" },
      ],
    }),
  });
  const r = run(dir);
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /duplicate source/);
  rmSync(dir, { recursive: true });
});

test("rejects evidence.jsonl missing required fields", () => {
  const cites = [0, 1, 2].map((i) => `[s${i}](https://e.com/${i})`).join(" ");
  const dir = scaffold({
    report: `# r\n${cites}\n`,
    evidence: JSON.stringify({ agent: 1, claim: "x" }) + "\n", // missing url, accessed
  });
  const r = run(dir);
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /missing "url"|missing "accessed"/);
  rmSync(dir, { recursive: true });
});

test("rejects 'recent reports' without citations", () => {
  const dir = scaffold({
    report: "# r\n\nRecent reports show that things happened.\n",
  });
  const r = run(dir);
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /recent reports.*drift|no H1|inline URL/);
  rmSync(dir, { recursive: true });
});

test("flags agent file without H2 sections (skeleton-first violation)", () => {
  const cites = [0, 1, 2].map((i) => `[s](https://a.com/${i})`).join(" ");
  const dir = scaffold({
    report: `# r\n${cites}\n`,
    agents: {
      "agent-1.md": "# Agent 1\n\nI just started writing without any headings.",
    },
  });
  const r = run(dir);
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /skeleton-first/);
  rmSync(dir, { recursive: true });
});
