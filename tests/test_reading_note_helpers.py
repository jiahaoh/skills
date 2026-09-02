from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELPERS = ROOT / "skills" / "zotero-paper-summarizer" / "scripts"


class ReadingNoteHelperTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.vault = Path(self.tempdir.name)
        self.notes = self.vault / "04.Reading" / "Notes"
        self.notes.mkdir(parents=True)
        self.env = os.environ.copy()
        self.env["READING_NOTES_VAULT"] = str(self.vault)

        (self.notes / "Example et al. (2026) - Test.md").write_text(
            """---
doi: "10.1000/example"
tags:
  - astrocytes
---

# Example
""",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_helper(self, script: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(HELPERS / script), *args],
            cwd=self.vault,
            env=self.env,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_duplicate_and_tag_checks_use_configured_vault(self) -> None:
        duplicate = self.run_helper("note_tools.py", "check-dup", "10.1000/example")
        self.assertEqual(duplicate.returncode, 1)
        self.assertIn("Example et al. (2026) - Test", duplicate.stdout)

        collision = self.run_helper("note_tools.py", "check-tags", "astrocyte")
        self.assertEqual(collision.returncode, 1)
        self.assertIn("reuse existing variant: astrocytes", collision.stdout)

    def test_tracker_update_is_scoped_to_configured_vault(self) -> None:
        tracker = self.vault / "04.Reading" / "Reading-tracker.md"
        tracker.write_text(
            """# Reading tracker

**Progress: 0 done / 1 total  ·  1 pending**

## Queue

- [ ] Example paper doi:10.1000/example
""",
            encoding="utf-8",
        )

        result = self.run_helper("note_tools.py", "tick", "10.1000/example")
        self.assertEqual(result.returncode, 0)
        self.assertIn("- [x] Example paper", tracker.read_text(encoding="utf-8"))

    def test_citation_refresh_refuses_unconfirmed_vault_scan(self) -> None:
        result = self.run_helper("refresh_citations.py")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--confirm-whole-vault", result.stdout)
        self.assertFalse((self.vault / ".cache").exists())


if __name__ == "__main__":
    unittest.main()
