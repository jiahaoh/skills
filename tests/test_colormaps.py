from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CMAPS = ROOT / "skills" / "research-visualization" / "assets" / "colormaps" / "cmaps.py"


def load_module():
    spec = importlib.util.spec_from_file_location("cmaps", CMAPS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ColormapCollectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cmaps = load_module()

    def test_collection_passes_checks(self) -> None:
        self.assertEqual(self.cmaps.check(), [])

    def test_lab_conversion(self) -> None:
        self.assertAlmostEqual(self.cmaps.lightness("#FFFFFF"), 100.0, places=1)
        self.assertAlmostEqual(self.cmaps.lightness("#000000"), 0.0, places=1)
        self.assertAlmostEqual(self.cmaps.delta_e("#FF0000", "#FF0000"), 0.0)

    def test_checks_catch_bad_entries(self) -> None:
        base = dict(added="2026-01-01", why="test", good_for="test", status="tried")
        bad = {
            "flat": dict(base, name="flat", kind="sequential", colors=["#FFFFFF", "#808080", "#C0C0C0"]),
            "twins": dict(base, name="twins", kind="categorical", colors=["#1F77B4", "#2077B4"]),
            "hex": dict(base, name="hex", kind="pair", colors=["#12345", "#000000"]),
        }
        errors = " ".join(self.cmaps.check(bad))
        self.assertIn("flat: lightness is not monotonic", errors)
        self.assertIn("flat: light end", errors)
        self.assertIn("twins: two colors differ", errors)
        self.assertIn("hex: invalid hex", errors)

    def test_nested_palette_levels(self) -> None:
        entries = self.cmaps.load()
        nested = [n for n, e in entries.items() if e["kind"] == "nested-categorical"]
        for name in nested:
            mains = self.cmaps.colors(name, "main", entries)
            members = self.cmaps.colors(name, "members", entries)
            self.assertEqual(len(mains), len(self.cmaps.families(name, entries)))
            self.assertGreaterEqual(len(members), len(mains))


if __name__ == "__main__":
    unittest.main()
