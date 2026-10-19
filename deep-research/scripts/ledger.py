#!/usr/bin/env python3
"""ledger.py — run-directory state manager for the Deep Research skill.

Manages an append-only research run: sources, hops, evidence, and conflicts.
Every high-impact claim must trace to ledger evidence; the linter enforces
structural integrity, counterevidence presence, independence, and secret
hygiene. Gates computed here are arithmetic — never LLM-self-reported.

Adapted from B143KC47/deep-research-skill research_ledger.py (MIT) and the
evidence-first layer of jojocorse2b/deep-research-skill (MIT, Lan Zheng).

Usage:
  python ledger.py init RUN_DIR --question "..." [--mode standard]
  python ledger.py add-source RUN_DIR --url URL --title TITLE [...]
  python ledger.py add-hop RUN_DIR --mode seed --description "..." [--parent H0001]
  python ledger.py add-evidence RUN_DIR --source-id S0001 --claim "..." [...]
  python ledger.py add-conflict RUN_DIR --claim-ids C1,C2 --positions "A|B"
  python ledger.py status RUN_DIR
  python ledger.py lint RUN_DIR
  python ledger.py export RUN_DIR
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dr_core import (  # noqa: E402
    EFFORT_DEFAULTS, EFFORT_MODES, FRESHNESS, HOP_MODES, HOP_STATUSES,
    IMPORTANCE_SCALE, INDEPENDENCE, QUALITY_SCALE, SOURCE_TYPES, STANCES,
    UNCERTAINTY, append_jsonl, domain_of, die, next_id, ok, read_json,
    read_jsonl, scan_secrets, short_hash, write_json,
)

RUN_FILES = ("sources.jsonl", "hops.jsonl", "evidence.jsonl", "conflicts.jsonl")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_all(run: Path) -> dict[str, list[dict]]:
    return {name[:-6]: read_jsonl(run / name) for name in RUN_FILES}


# ---------------------------------------------------------------------------
# init
# ---------------------------------------------------------------------------

def cmd_init(args) -> None:
    run = Path(args.run_dir)
    if run.exists() and any(run.iterdir()):
        die(f"run dir not empty: {run}")
    if args.mode not in EFFORT_MODES:
        die(f"mode must be one of {EFFORT_MODES}")
    max_hops, min_sources, min_classes = EFFORT_DEFAULTS[args.mode]
    if args.max_hops:
        max_hops = args.max_hops
    if args.min_sources:
        min_sources = args.min_sources
    if args.min_classes:
        min_classes = args.min_classes
    run.mkdir(parents=True, exist_ok=True)
    for name in RUN_FILES:
        (run / name).touch()
    write_json(run / "metadata.json", {
        "question": args.question,
        "mode": args.mode,
        "created_at": now(),
        "budget": {
            "max_hops": max_hops,
            "min_sources": min_sources,
            "min_source_classes": min_classes,
        },
        "stop_rule": (
            "stop when: all sub-questions answered with sufficient evidence, "
            "or additional research yields <15% novel claims for 2 consecutive "
            "waves, or budget exhausted; never keep searching just to spend budget"
        ),
    })
    (run / "plan.md").write_text(
        f"# Research Plan\n\nQuestion: {args.question}\nMode: {args.mode}\n\n"
        "## Sub-questions\n\n- [ ] \n\n## Pre-mortem\n\n"
        "(What could make this research wrong? Anchoring, missing voices, "
        "source homogeneity, scope drift, load-bearing assumptions.)\n",
        encoding="utf-8",
    )
    ok(f"initialized run: {run} (mode={args.mode}, max_hops={max_hops})")


# ---------------------------------------------------------------------------
# add-source / add-hop / add-evidence / add-conflict
# ---------------------------------------------------------------------------

def cmd_add_source(args) -> None:
    run = Path(args.run_dir)
    sources = read_jsonl(run / "sources.jsonl")
    norm_url = (args.url or "").strip()
    if not norm_url:
        die("--url is required")
    for s in sources:
        if s.get("url") == norm_url:
            die(f"duplicate url already recorded as {s.get('source_id')}")
    if args.source_type not in SOURCE_TYPES:
        die(f"--source-type must be one of {SOURCE_TYPES}")
    if args.quality is not None and args.quality not in QUALITY_SCALE:
        die(f"--quality must be one of {QUALITY_SCALE}")
    sid = next_id(sources, "S", "source_id")
    rec = {
        "source_id": sid,
        "url": norm_url,
        "title": args.title or "",
        "publisher": args.publisher or domain_of(norm_url),
        "source_type": args.source_type,
        "published_date": args.published_date or "",
        "accessed_at": now(),
        "quality": args.quality if args.quality is not None else 3,
        "independence_family": domain_of(norm_url),
        "notes": args.notes or "",
    }
    append_jsonl(run / "sources.jsonl", rec)
    ok(sid)


def cmd_add_hop(args) -> None:
    run = Path(args.run_dir)
    hops = read_jsonl(run / "hops.jsonl")
    meta = read_json(run / "metadata.json") or {}
    budget = meta.get("budget", {})
    max_hops = budget.get("max_hops", 10)
    if args.mode not in HOP_MODES:
        die(f"--mode must be one of {HOP_MODES}")
    if args.status not in HOP_STATUSES:
        die(f"--status must be one of {HOP_STATUSES}")
    if args.parent:
        if not any(h.get("hop_id") == args.parent for h in hops):
            die(f"parent hop {args.parent} does not exist")
    if len(hops) >= max_hops and not args.force:
        die(f"hop budget exhausted ({len(hops)}/{max_hops}); use --force to override")
    hid = next_id(hops, "H", "hop_id")
    append_jsonl(run / "hops.jsonl", {
        "hop_id": hid,
        "mode": args.mode,
        "description": args.description or "",
        "status": args.status,
        "parent": args.parent or None,
        "created_at": now(),
    })
    ok(f"{hid} ({args.mode}) {len(hops) + 1}/{max_hops}")


def cmd_add_evidence(args) -> None:
    run = Path(args.run_dir)
    sources = read_jsonl(run / "sources.jsonl")
    evidence = read_jsonl(run / "evidence.jsonl")
    if args.source_id not in {s.get("source_id") for s in sources}:
        die(f"source {args.source_id} not found — add it first")
    if args.stance not in STANCES:
        die(f"--stance must be one of {STANCES}")
    if args.importance not in IMPORTANCE_SCALE:
        die(f"--importance must be one of {IMPORTANCE_SCALE}")
    if args.quality not in QUALITY_SCALE:
        die(f"--quality must be one of {QUALITY_SCALE}")
    for f in ("freshness", "independence", "uncertainty"):
        v = getattr(args, f)
        if v not in {"current", "recent", "dated", "unknown",
                     "independent", "correlated", "established", "likely",
                     "contested", "weak"}:
            die(f"--{f} value {v!r} not allowed")
    claim = (args.claim or "").strip()
    if not claim:
        die("--claim is required (the claim text)")
    claim_id = args.claim_id or f"CL-{short_hash(claim)[:8]}"
    eid = next_id(evidence, "E", "evidence_id")
    append_jsonl(run / "evidence.jsonl", {
        "evidence_id": eid,
        "claim_id": claim_id,
        "claim": claim,
        "source_id": args.source_id,
        "stance": args.stance,
        "quote_or_locator": args.quote or "",
        "importance": args.importance,
        "quality": args.quality,
        "freshness": args.freshness,
        "independence": args.independence,
        "uncertainty": args.uncertainty,
        "captured_at": now(),
    })
    ok(f"{eid} -> {claim_id} ({args.stance})")


def cmd_add_conflict(args) -> None:
    run = Path(args.run_dir)
    conflicts = read_jsonl(run / "conflicts.jsonl")
    evidence = read_jsonl(run / "evidence.jsonl")
    claim_ids = [c.strip() for c in args.claim_ids.split(",") if c.strip()]
    if len(claim_ids) < 1:
        die("--claim-ids requires at least one claim id")
    known = {e.get("claim_id") for e in evidence}
    unknown = [c for c in claim_ids if c not in known]
    if unknown:
        die(f"unknown claim ids: {', '.join(unknown)}")
    positions = [p.strip() for p in args.positions.split("|") if p.strip()]
    if len(positions) < 2:
        die("--positions requires at least two positions separated by |")
    if args.status not in ("resolved", "unresolved"):
        die("--status must be resolved|unresolved")
    if args.status == "resolved" and not args.resolution:
        die("resolved conflicts require --resolution text")
    cid = next_id(conflicts, "C", "conflict_id")
    append_jsonl(run / "conflicts.jsonl", {
        "conflict_id": cid,
        "claim_ids": claim_ids,
        "positions": positions,
        "resolution": args.resolution or "",
        "status": args.status,
        "recorded_at": now(),
    })
    ok(f"{cid} ({args.status})")


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------

def cmd_status(args) -> None:
    run = Path(args.run_dir)
    data = load_all(run)
    meta = read_json(run / "metadata.json") or {}
    budget = meta.get("budget", {})
    max_hops = budget.get("max_hops", "?")
    hops = data["hops"]
    sources = data["sources"]
    evidence = data["evidence"]
    claims = {e.get("claim_id") for e in evidence}
    hi = [e for e in evidence if (e.get("importance") or 0) >= 4]
    hi_claims = {e.get("claim_id") for e in hi}
    contradicted = {e.get("claim_id") for e in evidence
                    if e.get("stance") == "contradicts"}
    n_contr_checked = len(hi_claims & contradicted)
    classes = {s.get("source_type") for s in sources if s.get("source_type")}
    print(f"mode={meta.get('mode', '?')} hops={len(hops)}/{max_hops} "
          f"sources={len(evidence) and len(sources)} "
          f"evidence={len(evidence)} claims={len(claims)}")
    print(f"source_classes={len(classes)}/{budget.get('min_source_classes', '?')} "
          f"({', '.join(sorted(classes)) or 'none'})")
    print(f"high_importance_claims={len(hi_claims)} "
          f"with_counterevidence={n_contr_checked}")
    if not sources:
        print("hint: no sources recorded yet — add-source before evidence")
    elif len(hops) >= int(max_hops or 0) * 2 // 3:
        print("hint: >2/3 of hop budget used — run `lint` and review stop conditions")


# ---------------------------------------------------------------------------
# lint
# ---------------------------------------------------------------------------

def cmd_lint(args) -> None:
    run = Path(args.run_dir)
    errors: list[str] = []
    warnings: list[str] = []
    data = load_all(run)
    meta = read_json(run / "metadata.json") or {}
    budget = meta.get("budget", {})
    sources, hops, evidence, conflicts = (data["sources"], data["hops"],
                                          data["evidence"], data["conflicts"])
    src_ids = {s.get("source_id") for s in sources}
    hop_ids = {h.get("hop_id") for h in hops}
    claim_ids = {e.get("claim_id") for e in evidence}

    # --- structural errors ---
    if not meta:
        errors.append("metadata.json missing or empty — run `init` first")
    for e in evidence:
        if e.get("source_id") not in src_ids:
            errors.append(f"{e.get('evidence_id')}: references unknown source {e.get('source_id')}")
        if not (e.get("claim") or "").strip():
            errors.append(f"{e.get('evidence_id')}: empty claim text")
    for h in hops:
        if h.get("parent") and h["parent"] not in hop_ids:
            errors.append(f"{h.get('hop_id')}: parent {h['parent']} does not exist")
    for name in RUN_FILES:
        dup_ids = set()
        seen = set()
        for rec in data[name[:-6]]:
            rid = rec.get(f"{name[:-6][:-1]}_id") or rec.get("hop_id") \
                or rec.get("source_id") or rec.get("evidence_id") \
                or rec.get("conflict_id")
            if rid in seen:
                dup_ids.add(rid)
            seen.add(rid)
        for rid in dup_ids:
            errors.append(f"{name}: duplicate id {rid}")
    for c in conflicts:
        for cl in c.get("claim_ids", []):
            if cl not in claim_ids:
                errors.append(f"{c.get('conflict_id')}: unknown claim id {cl}")

    # --- secrets (fail-closed) ---
    for name in RUN_FILES:
        p = run / name
        if p.exists():
            text = p.read_text(encoding="utf-8")
            for hit in scan_secrets(text):
                errors.append(f"{name}: {hit} — redact before packaging")

    # --- quality warnings ---
    for e in evidence:
        imp = e.get("importance") or 0
        if imp >= 4:
            if not (e.get("quote_or_locator") or "").strip():
                warnings.append(f"{e.get('evidence_id')}: high-importance claim lacks quote/locator")
            if (e.get("quality") or 3) <= 2:
                warnings.append(f"{e.get('evidence_id')}: high-importance claim rests on low-quality source")
            if e.get("freshness") == "unknown":
                warnings.append(f"{e.get('evidence_id')}: high-importance claim has unknown freshness")
            fams = {s.get("independence_family") for s in sources
                    if s.get("source_id") == e.get("source_id")}
            others = {s.get("independence_family") for s in sources
                      if s.get("source_id") != e.get("source_id"
                      ) and any(x.get("claim_id") == e.get("claim_id")
                                and x.get("stance") != "contradicts"
                                for x in evidence if x.get("source_id") == s.get("source_id"))}
            if len(fams | others) < 2:
                warnings.append(f"{e.get('evidence_id')}: high-importance claim {e.get('claim_id')} "
                                "supported by <2 independence families — label single-source or find corroboration")
    hi_claims = {e.get("claim_id") for e in evidence if (e.get("importance") or 0) >= 4}
    contradicted = {e.get("claim_id") for e in evidence if e.get("stance") == "contradicts"}
    for cl in sorted(hi_claims - contradicted):
        warnings.append(f"claim {cl}: no counterevidence searched — run a contradict hop")
    if evidence and not any(h.get("mode") in ("verify", "contradict") for h in hops):
        warnings.append("no verify/contradict hops recorded — evidence is unchallenged")
    classes = {s.get("source_type") for s in sources if s.get("source_type")}
    min_classes = budget.get("min_source_classes", 3)
    if len(classes) < min_classes:
        warnings.append(f"source class diversity {len(classes)} < required {min_classes}")
    for c in conflicts:
        if c.get("status") == "unresolved" and (c.get("resolution") or "").strip():
            warnings.append(f"{c.get('conflict_id')}: marked unresolved but has resolution text")
        if c.get("status") == "resolved" and not (c.get("resolution") or "").strip():
            errors.append(f"{c.get('conflict_id')}: resolved conflicts require resolution text")

    for e in errors:
        print(f"ERROR: {e}")
    for w in warnings:
        print(f"WARN: {w}")
    print(f"lint: {len(errors)} error(s), {len(warnings)} warning(s)")
    if errors:
        raise SystemExit(1)
    ok("ledger is structurally sound")


# ---------------------------------------------------------------------------
# export
# ---------------------------------------------------------------------------

def cmd_export(args) -> None:
    run = Path(args.run_dir)
    data = load_all(run)
    payload = {
        "metadata": read_json(run / "metadata.json") or {},
        "sources": data["sources"],
        "hops": data["hops"],
        "evidence": data["evidence"],
        "conflicts": data["conflicts"],
    }
    import json
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Deep Research evidence ledger")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("init")
    sp.add_argument("run_dir")
    sp.add_argument("--question", required=True)
    sp.add_argument("--mode", default="standard", choices=EFFORT_MODES)
    sp.add_argument("--max-hops", type=int)
    sp.add_argument("--min-sources", type=int)
    sp.add_argument("--min-classes", type=int)
    sp.set_defaults(func=cmd_init)

    sp = sub.add_parser("add-source")
    sp.add_argument("run_dir")
    sp.add_argument("--url", required=True)
    sp.add_argument("--title", default="")
    sp.add_argument("--publisher", default="")
    sp.add_argument("--source-type", default="secondary", choices=SOURCE_TYPES)
    sp.add_argument("--published-date", default="")
    sp.add_argument("--quality", type=int, default=None)
    sp.add_argument("--notes", default="")
    sp.set_defaults(func=cmd_add_source)

    sp = sub.add_parser("add-hop")
    sp.add_argument("run_dir")
    sp.add_argument("--mode", required=True, choices=HOP_MODES)
    sp.add_argument("--description", default="")
    sp.add_argument("--parent", default="")
    sp.add_argument("--status", default="done", choices=HOP_STATUSES)
    sp.add_argument("--force", action="store_true")
    sp.set_defaults(func=cmd_add_hop)

    sp = sub.add_parser("add-evidence")
    sp.add_argument("run_dir")
    sp.add_argument("--source-id", required=True)
    sp.add_argument("--claim", required=True)
    sp.add_argument("--claim-id", default="")
    sp.add_argument("--stance", default="supports", choices=STANCES)
    sp.add_argument("--quote", default="")
    sp.add_argument("--importance", type=int, default=3, choices=IMPORTANCE_SCALE)
    sp.add_argument("--quality", type=int, default=3, choices=QUALITY_SCALE)
    sp.add_argument("--freshness", default="unknown")
    sp.add_argument("--independence", default="unknown")
    sp.add_argument("--uncertainty", default="unknown")
    sp.set_defaults(func=cmd_add_evidence)

    sp = sub.add_parser("add-conflict")
    sp.add_argument("run_dir")
    sp.add_argument("--claim-ids", required=True)
    sp.add_argument("--positions", required=True)
    sp.add_argument("--resolution", default="")
    sp.add_argument("--status", default="unresolved", choices=("resolved", "unresolved"))
    sp.set_defaults(func=cmd_add_conflict)

    sp = sub.add_parser("status")
    sp.add_argument("run_dir")
    sp.set_defaults(func=cmd_status)

    sp = sub.add_parser("lint")
    sp.add_argument("run_dir")
    sp.set_defaults(func=cmd_lint)

    sp = sub.add_parser("export")
    sp.add_argument("run_dir")
    sp.set_defaults(func=cmd_export)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        args.func(args)
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        die(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
