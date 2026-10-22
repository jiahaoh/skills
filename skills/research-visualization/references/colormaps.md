# Colormap collection

A personal collection of colormaps and palettes that worked in real figures, plus a few that were rejected, kept as warnings. The colors live only in [`assets/colormaps/colormaps.json`](../assets/colormaps/colormaps.json); `cmaps.py` beside it loads, checks, registers and previews them. Do not copy hex values into this file.

## Use

- `python cmaps.py list` prints every entry with its kind, status and use. Pick from `proven`, then `tried`, and never from `rejected`.
- `python cmaps.py preview OUT.png` draws all entries on one sheet. Show it to the user when they are choosing a palette.
- In figure code, `cmaps.register_all()` makes the custom maps available as `plt.get_cmap("<name>")`. Other helpers are `cmaps.to_cmap(name)`, `cmaps.colors(name)`, and `cmaps.colors(name, level="main")` or `cmaps.families(name)` for nested palettes.
- When copying into a project, copy the whole `colormaps/` folder (JSON and script together). The project profile records which entries the project uses, and where.

## Kinds

| Kind | Holds | Typical use |
| --- | --- | --- |
| `sequential` | `colors` (custom stops) or `base` (a matplotlib map) with an optional `range` cut | Magnitudes: expression, density, depth |
| `diverging` | the same, with a meaningful center | Signed change: log2 enrichment, fold change |
| `categorical` | `colors` | Unordered labels |
| `nested-categorical` | `families`: a main color plus member colors per family | Two-level labels (classes and their subtypes) |
| `pair` | two colors | Two modalities or a class and its nested subset |
| `single` | one color | Neutral or background roles (unclassified, ghost) |

## Status

- `tried`: used in a figure and the user liked it.
- `proven`: used in two or more figures or projects.
- `rejected`: tried and turned down. Keep it with the reason, so it is not proposed again.

## Adding an entry

- Add an entry when the user approves a colormap or palette in a figure. Give its name, kind, colors (or base and range), status, date added, `good_for`, `avoid` and `why`. Add `origin` when it comes from a published palette.
- Strip all project context. A categorical palette enters as an ordered list of colors (or families), never with the label names it was made for.
- Name entries by their look (`apricot-violet`, `steel-blue`), not by a project or data type.
- Run `python cmaps.py check`, then the repository tests, which run the same checks:
  - sequential lightness must be monotonic;
  - the light end must stay visible on white;
  - categorical colors must differ by at least ΔE 10 (CIE76);
  - members of one family must differ by at least ΔE 7.
- When a figure uses an entry again, upgrade `tried` to `proven`.
