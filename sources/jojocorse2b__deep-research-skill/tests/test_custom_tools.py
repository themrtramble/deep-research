from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_report import build_markdown
from secret_scan import scan
from validate_evidence import validate


def make_run(tmp_path: Path) -> Path:
    run = tmp_path / "run"
    run.mkdir()
    (run / "run_manifest.json").write_text('{"question":"test"}', encoding="utf-8")
    (run / "sources.jsonl").write_text(
        '{"source_id":"s1","url":"https://example.test","title":"Example"}\n',
        encoding="utf-8",
    )
    (run / "evidence.jsonl").write_text(
        '{"evidence_id":"e1","source_id":"s1","claim_id":"c1","quote":"fact","locator":"p. 1"}\n',
        encoding="utf-8",
    )
    (run / "claims.jsonl").write_text(
        '{"claim_id":"c1","claim":"A verified fact","confidence":"high","evidence_ids":["e1"]}\n',
        encoding="utf-8",
    )
    return run


def test_evidence_contract_and_report(tmp_path):
    run = make_run(tmp_path)
    assert validate(run) == []
    report = build_markdown(run)
    assert "A verified fact" in report.read_text(encoding="utf-8")


def test_secret_scan_detects_private_material(tmp_path):
    clean = tmp_path / "clean"
    clean.mkdir()
    (clean / "notes.md").write_text("no credentials here", encoding="utf-8")
    assert scan(clean) == []

    dirty = tmp_path / "dirty"
    dirty.mkdir()
    suspicious = "Authorization: " + "Bearer " + ("a" * 26)
    (dirty / "notes.md").write_text(suspicious, encoding="utf-8")
    assert scan(dirty)


def test_jsonl_files_are_real_json_objects(tmp_path):
    run = make_run(tmp_path)
    row = json.loads((run / "claims.jsonl").read_text(encoding="utf-8"))
    assert row["claim_id"] == "c1"
