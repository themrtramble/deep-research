"""Tests for calibrate.py — the epistemic calibration linter."""
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
from calibrate import calibrate  # noqa: E402


class TestSilentUpgrades:
    def test_contested_claim_may_not_be_proven(self):
        text = (
            "## Claim A\nstatus: contested\n\n"
            "This definitely proves the migration caused the outage."
        )
        result = calibrate(text)
        assert result["upgrades"], "contested + 'definitely proves' must be flagged"
        assert "status=contested" in result["upgrades"][0]

    def test_established_allows_all(self):
        text = "status: established\n\nThe census definitely shows population growth."
        assert calibrate(text)["upgrades"] == []

    def test_likely_blocks_guaranteed(self):
        text = "status: likely\n\nThe fix is guaranteed to work."
        assert any("likely" in u for u in calibrate(text)["upgrades"])

    def test_speculative_blocks_shows(self):
        text = "status: speculative\n\nThe data shows a clear trend."
        result = calibrate(text)
        assert result["upgrades"], "speculative + 'shows' must be flagged"

    def test_supported_blocks_definitely(self):
        text = "status: supported\n\nIt certainly resolves the race condition."
        assert calibrate(text)["upgrades"]

    def test_no_declared_status_defaults_conservative(self):
        text = "The benchmark results show nothing else matters.\nSomething unrelated follows here."
        result = calibrate(text)
        # 'unknown' forbids 'show(s)'
        assert result["upgrades"]
        assert any("status=unknown" in u for u in result["upgrades"])

    def test_sequential_blocks(self):
        text = (
            "status: established\nEstablished facts are fine here; everything checks out.\n\n"
            "status: weak\nThe vendor's tiny study proves the 10x speedup.\n"
        )
        result = calibrate(text)
        assert any("weak" in u for u in result["upgrades"])


class TestUnmeasuredLanguage:
    def test_vague_comparative_without_numbers(self):
        text = "The new pipeline is significantly better than the old one."
        assert calibrate(text)["vague"]

    def test_vague_with_measurement_passes(self):
        text = "The new pipeline is significantly better: 40% lower latency (120ms vs 200ms)."
        assert calibrate(text)["vague"] == []

    def test_naked_number_flagged(self):
        text = "Latency dropped to 42 after the change."
        assert calibrate(text)["naked_numbers"]

    def test_unit_or_year_exempt(self):
        text = ("Response time is 120ms. The study ran in 2023 across 40 users. "
                "Costs fell 30%.")
        assert calibrate(text)["naked_numbers"] == []


class TestCLI:
    def test_cli_exit_codes(self, tmp_path):
        bad = tmp_path / "bad.md"
        bad.write_text("status: contested\n\nThe data definitely proves it.")
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "calibrate.py"), str(bad)],
            capture_output=True, text=True)
        assert proc.returncode == 1
        assert "silent upgrade" in proc.stdout.lower()

        good = tmp_path / "good.md"
        good.write_text("status: established\n\nSolid facts with 42 users.")
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "calibrate.py"), str(good)],
            capture_output=True, text=True)
        assert proc.returncode == 0
        assert "CALIBRATED" in proc.stdout

    def test_strict_mode(self, tmp_path):
        p = tmp_path / "m.md"
        p.write_text("status: established\n\nIt is significantly faster.")
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "calibrate.py"), str(p), "--strict"],
            capture_output=True, text=True)
        assert proc.returncode == 1
