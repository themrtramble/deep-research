// Regression test: the CLI "am I the entry?" check must work when scripts
// are invoked via a symlink (as they are after `make install-claude` /
// `make install-opencode`). Original bug: classify.js exited silently when
// invoked through ~/.claude/skills/deep-research/scripts/classify.js because
// import.meta.url (realpath) != process.argv[1] (symlink path).

import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, rmSync, symlinkSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { spawnSync } from "node:child_process";

const SCRIPTS = new URL("../../skill/scripts/", import.meta.url).pathname;

function runViaSymlink(scriptName, args, cwd = tmpdir()) {
  const root = mkdtempSync(join(tmpdir(), "drs-symlink-"));
  const link = join(root, scriptName);
  try {
    symlinkSync(join(SCRIPTS, scriptName), link);
    return spawnSync("node", [link, ...args], { encoding: "utf8", cwd });
  } finally {
    rmSync(root, { recursive: true });
  }
}

test("classify.js CLI runs through a symlink", () => {
  const r = runViaSymlink("classify.js", ["Compare Tavily vs Exa vs Brave"]);
  assert.equal(r.status, 0, `stderr: ${r.stderr}`);
  assert.match(r.stdout, /"mode":\s*"standard"/);
});

test("classify.js CLI prints usage when no query given (through symlink)", () => {
  const r = runViaSymlink("classify.js", []);
  assert.equal(r.status, 2);
  assert.match(r.stderr, /usage/);
});

test("validate_outputs.js CLI runs through a symlink", () => {
  // Invoking without args → usage error, not silent success.
  const r = runViaSymlink("validate_outputs.js", []);
  assert.notEqual(r.status, 0, "symlinked CLI must not silently exit 0");
  assert.match(r.stderr, /usage/);
});

test("dedup_sources.js CLI runs through a symlink", () => {
  const r = runViaSymlink("dedup_sources.js", []);
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /usage/);
});
