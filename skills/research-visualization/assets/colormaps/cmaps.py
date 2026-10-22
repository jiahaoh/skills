#!/usr/bin/env python3
"""Personal colormap and palette collection: load, check, register in matplotlib, preview.

The collection lives in colormaps.json next to this file (the single source; copy both into a project together).
Entry kinds:
  sequential / diverging   `colors` (custom stops) or `base` (a matplotlib colormap name) with an optional `range`
  categorical / pair / single   `colors`
  nested-categorical       `families`: [{"main": hex, "members": [hex, ...]}, ...]
Status: tried (used and liked once), proven (used in two or more figures or projects), rejected (kept as a warning).

Usage:
  python cmaps.py list
  python cmaps.py check
  python cmaps.py preview OUT.png        (needs matplotlib)

In code:
  import cmaps
  cmaps.register_all()                   # custom maps become plt.get_cmap("apricot-violet")
  cmap = cmaps.to_cmap("ylgnbu-trunc")
  colors = cmaps.colors("tint-shade-families", level="main")
"""
from __future__ import annotations

import itertools
import json
import re
import sys
from pathlib import Path

PATH = Path(__file__).with_name("colormaps.json")
KINDS = {"sequential", "diverging", "categorical", "pair", "single", "nested-categorical"}
STATUSES = {"tried", "proven", "rejected"}
HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
# checks (CIE76 distances in CIELAB): categorical colors must be told apart, family members a little less so;
# a sequential map's light end must stay visible on white
MIN_DE_CATEGORICAL = 10.0
MIN_DE_MEMBERS = 7.0
MAX_L_LIGHT_END = 96.0


def load(path: Path = PATH) -> dict[str, dict]:
    """Entries by name, in file order."""
    return {e["name"]: e for e in json.loads(Path(path).read_text(encoding="utf-8"))["entries"]}


def _lab(hex_color: str) -> tuple[float, float, float]:
    """sRGB hex -> CIELAB (D65)."""
    rgb = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    x = (0.4124 * lin[0] + 0.3576 * lin[1] + 0.1805 * lin[2]) / 0.95047
    y = 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
    z = (0.0193 * lin[0] + 0.1192 * lin[1] + 0.9505 * lin[2]) / 1.08883
    f = [t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116 for t in (x, y, z)]
    return 116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])


def delta_e(a: str, b: str) -> float:
    """CIE76 color difference between two hex colors."""
    return sum((p - q) ** 2 for p, q in zip(_lab(a), _lab(b))) ** 0.5


def lightness(hex_color: str) -> float:
    return _lab(hex_color)[0]


def colors(name: str, level: str = "members", entries: dict | None = None) -> list[str]:
    """Flat color list of an entry. Nested palettes: level "main" (one per family) or "members" (all members)."""
    e = (entries or load())[name]
    if e["kind"] == "nested-categorical":
        if level == "main":
            return [f["main"] for f in e["families"]]
        return [c for f in e["families"] for c in f["members"]]
    return list(e.get("colors", []))


def families(name: str, entries: dict | None = None) -> list[tuple[str, list[str]]]:
    """(main, members) per family of a nested palette."""
    return [(f["main"], list(f["members"])) for f in (entries or load())[name]["families"]]


def _min_de(cs: list[str]) -> float:
    return min((delta_e(a, b) for a, b in itertools.combinations(cs, 2)), default=float("inf"))


def check(entries: dict | None = None) -> list[str]:
    """Problems in the collection (empty list = fine). Rejected entries are only checked for structure."""
    entries = entries if entries is not None else load()
    errors = []
    for name, e in entries.items():
        where = f"{name}:"
        for key in ("kind", "status", "added", "why"):
            if not e.get(key):
                errors.append(f"{where} missing {key}")
        kind, status = e.get("kind"), e.get("status")
        if kind not in KINDS:
            errors.append(f"{where} unknown kind {kind!r}")
            continue
        if status not in STATUSES:
            errors.append(f"{where} unknown status {status!r}")
        if status != "rejected" and not e.get("good_for"):
            errors.append(f"{where} missing good_for")
        hexes = colors(name, entries=entries) + (colors(name, "main", entries) if kind == "nested-categorical" else [])
        bad = [c for c in hexes if not HEX_RE.match(c)]
        if bad:
            errors.append(f"{where} invalid hex {bad[:3]}")
            continue
        if kind in ("sequential", "diverging"):
            if bool(e.get("colors")) == bool(e.get("base")):
                errors.append(f"{where} needs exactly one of colors / base")
            rng = e.get("range", [0.0, 1.0])
            if not (len(rng) == 2 and 0 <= rng[0] < rng[1] <= 1):
                errors.append(f"{where} range must be [lo, hi] within 0-1")
        if status == "rejected":
            continue
        if kind == "sequential" and e.get("colors"):
            ls = [lightness(c) for c in e["colors"]]
            steps = [b - a for a, b in zip(ls, ls[1:])]
            if not (all(s < 0 for s in steps) or all(s > 0 for s in steps)):
                errors.append(f"{where} lightness is not monotonic ({', '.join(f'{v:.0f}' for v in ls)})")
            if max(ls) > MAX_L_LIGHT_END:
                errors.append(f"{where} light end L*={max(ls):.0f} is invisible on white (max {MAX_L_LIGHT_END:.0f})")
        if kind in ("categorical", "pair"):
            d = _min_de(e["colors"])
            if d < MIN_DE_CATEGORICAL:
                errors.append(f"{where} two colors differ by only dE={d:.1f} (min {MIN_DE_CATEGORICAL:.0f})")
        if kind == "nested-categorical":
            d = _min_de(colors(name, "main", entries))
            if d < MIN_DE_CATEGORICAL:
                errors.append(f"{where} two main colors differ by only dE={d:.1f} (min {MIN_DE_CATEGORICAL:.0f})")
            for i, f in enumerate(e["families"], 1):
                d = _min_de(f["members"])
                if d < MIN_DE_MEMBERS:
                    errors.append(f"{where} family {i}: two members differ by only dE={d:.1f} (min {MIN_DE_MEMBERS:.0f})")
    return errors


def to_cmap(name: str, entries: dict | None = None):
    """matplotlib colormap of a sequential / diverging entry (custom stops, or a base map cut to `range`)."""
    import matplotlib.colors as mcolors
    import matplotlib.pyplot as plt
    import numpy as np

    e = (entries or load())[name]
    if e.get("colors"):
        return mcolors.LinearSegmentedColormap.from_list(name, e["colors"])
    lo, hi = e.get("range", [0.0, 1.0])
    base = plt.get_cmap(e["base"])
    if (lo, hi) == (0.0, 1.0):
        return base.copy()
    return mcolors.LinearSegmentedColormap.from_list(name, base(np.linspace(lo, hi, 256)))


def register_all(entries: dict | None = None) -> list[str]:
    """Register every non-rejected custom or cut map with matplotlib under its entry name."""
    import matplotlib as mpl

    entries = entries or load()
    done = []
    for name, e in entries.items():
        if e["kind"] in ("sequential", "diverging") and e["status"] != "rejected" and (e.get("colors") or e.get("range")):
            if name not in mpl.colormaps:
                mpl.colormaps.register(to_cmap(name, entries), name=name)
            done.append(name)
    return done


def preview(out: str | Path, entries: dict | None = None) -> Path:
    """One sheet with every entry: gradients, swatch rows, nested families (main on the left, members after)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    entries = entries or load()
    rows = []
    for name, e in entries.items():
        if e["kind"] == "nested-categorical":
            rows += [(name if i == 0 else "", e, ("family", f)) for i, f in enumerate(e["families"])]
        else:
            rows.append((name, e, None))
    fig, axes = plt.subplots(len(rows), 1, figsize=(7, 0.26 * len(rows) + 0.3))
    for ax, (label, e, fam) in zip(axes, rows):
        ax.set_axis_off()
        tag = f"{label}  [{e['status']}]" if label else ""
        ax.text(-0.01, 0.5, tag, transform=ax.transAxes, ha="right", va="center", fontsize=6,
                color="#999999" if e["status"] == "rejected" else "black")
        if fam:
            cs = [fam[1]["main"]] + fam[1]["members"]
            for i, c in enumerate(cs):
                ax.add_patch(plt.Rectangle((i * 1.1 + (0.4 if i else 0), 0), 1, 1, color=c))
            ax.set_xlim(0, 20)
        elif e["kind"] in ("sequential", "diverging"):
            ax.imshow(np.linspace(0, 1, 256)[None, :], aspect="auto", cmap=to_cmap(e["name"], entries),
                      extent=(0, 20, 0, 1))
            ax.set_xlim(0, 20)
        else:
            for i, c in enumerate(e["colors"]):
                ax.add_patch(plt.Rectangle((i * 1.0, 0), 0.9, 1, color=c))
            ax.set_xlim(0, 20)
        ax.set_ylim(0, 1)
    fig.subplots_adjust(left=0.3, right=0.98, top=0.98, bottom=0.02, hspace=0.35)
    out = Path(out)
    fig.savefig(out, dpi=200)
    plt.close(fig)
    return out


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "list"
    if cmd == "list":
        for name, e in load().items():
            print(f"{name:26} {e['kind']:19} {e['status']:9} {e.get('good_for', '')}")
        return 0
    if cmd == "check":
        errors = check()
        for err in errors:
            print(f"ERROR: {err}")
        print(f"{len(load())} entries, {len(errors)} problem(s)")
        return 1 if errors else 0
    if cmd == "preview" and len(argv) == 3:
        print(preview(argv[2]))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
