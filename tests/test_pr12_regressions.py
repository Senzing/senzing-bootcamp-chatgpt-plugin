"""Regression tests for the fixes made while preparing pull request 12."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "plugins" / "senzing-bootcamp" / "scripts"


def load_script(name: str, filename: str):
    """Load a hyphen-directory script as a normal test module."""
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


bootcamp_state = load_script("bootcamp_state_under_test", "bootcamp_state.py")
recap_video = load_script("generate_recap_video_under_test", "generate_recap_video.py")
write_gate = load_script("write_gate_under_test", "write-gate.py")


class NumberNarrationTests(unittest.TestCase):
    def test_dates_and_ranges_are_not_partially_spelled(self):
        text = "On 2026-09-30, inspect records 3-5 and score 3.5 of 10,000."
        self.assertEqual(
            recap_video.spell_numbers(text),
            "On 2026-09-30, inspect records 3-5 and score three point five "
            "of ten thousand.",
        )


class WriteGateTests(unittest.TestCase):
    def test_update_accepts_no_final_newline_marker(self):
        command = r"""*** Begin Patch
*** Update File: notes.txt
@@
-before
+after
\ No newline at end of file
*** End Patch"""
        self.assertEqual(write_gate.patch_targets(command), ["notes.txt"])

    def test_move_and_delete_targets_are_collected(self):
        command = """*** Begin Patch
*** Update File: old.txt
*** Move to: new.txt
@@
 unchanged
*** Delete File: retired.txt
*** End Patch"""
        self.assertEqual(
            write_gate.patch_targets(command),
            ["old.txt", "new.txt", "retired.txt"],
        )

    def test_malformed_patch_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "malformed or unsupported"):
            write_gate.patch_targets("*** Begin Patch\nnot a header\n*** End Patch")

    def test_symlink_escape_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            root = Path(directory)
            workspace = root / "workspace"
            outside = root / "outside"
            workspace.mkdir()
            outside.mkdir()
            (workspace / "escape").symlink_to(outside, target_is_directory=True)
            previous = Path.cwd()
            try:
                os.chdir(workspace)
                with self.assertRaisesRegex(ValueError, "outside the Bootcamp project"):
                    write_gate.validate_target("escape/file.txt", workspace)
            finally:
                os.chdir(previous)


class PreferenceTests(unittest.TestCase):
    def run_in_project(self, progress: str, preferences: str | None = None):
        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "config").mkdir()
            (root / "config" / "bootcamp_progress.json").write_text(
                progress,
                encoding="utf-8",
            )
            if preferences is not None:
                (root / "config" / "bootcamp_preferences.yaml").write_text(
                    preferences,
                    encoding="utf-8",
                )
            try:
                os.chdir(root)
                return bootcamp_state.active_progress()
            finally:
                os.chdir(previous)

    def test_first_duplicate_preference_wins(self):
        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "config").mkdir()
            (root / "config" / "bootcamp_preferences.yaml").write_text(
                "disable_stop_nudge: false\ndisable_stop_nudge: true\n",
                encoding="utf-8",
            )
            try:
                os.chdir(root)
                self.assertFalse(bootcamp_state.preference("disable_stop_nudge"))
            finally:
                os.chdir(previous)

    def test_blank_or_non_string_module_is_inactive(self):
        self.assertIsNone(self.run_in_project('{"current_module": "   "}'))
        self.assertIsNone(self.run_in_project('{"current_module": 6}'))

    def test_completion_preference_makes_recorded_progress_inactive(self):
        self.assertIsNone(
            self.run_in_project(
                '{"current_module": "Graduation"}',
                "bootcamp_complete: true\n",
            )
        )


if __name__ == "__main__":
    unittest.main()
