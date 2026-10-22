---
name: research-visualization
description: House rules for research figures, analysis reports and review pages, distilled from many rounds of review comments; covers the design process, print-ready panel export, color, labels and legends, chart-specific conventions, HTML report structure and shared-page mechanics. Use before drawing a manuscript panel or composed figure, building an HTML report or review page for collaborators, choosing a palette or colormap, or applying review comments to any of these.
---

# Research Visualization

Rules that came back as review comments on first drafts of figures, reports and review pages. Apply them to the **first draft**. The goal is fewer review rounds, not decoration.

## Start here

1. Look for the project's visualization profile: a file such as `docs/visualization-standard.md`, or a section the project's agent instructions point to. It holds the project's palette files, accent colors, fonts, page sizes and decisions already made. **Project rules override this skill.**
2. Read only the reference files the task needs (index below).
3. Before designing, confirm the inputs: which label version, which embedding, which reference level. Several design rounds were lost to the wrong input.

## Core rules

- **Discuss, then draw.** Propose content and layout first when the user wants to discuss. For visual choices, draw variants side by side, recommend one and say why.
- **Record decisions and rejections** with the date in the project profile. Never offer a rejected option again.
- **Everything from a script.** Every figure, report and review page is rebuilt by rerunning its script. Hand edits happen only later, on exported vector files.
- **Final size from the start.** Draw panels at print size in mm, with print font sizes, and never rescale them.
- **Vector out, raster inside.** Export editable vector files plus a PNG preview. Rasterize only dense layers such as points, maps and renders.
- **One color source.** Read colors from a frozen palette file. Start from the colormap collection, and add any colormap the user liked to it. Every color code needs a visible key, and "unclassified" is always neutral grey.
- **Nothing overlaps.** Labels never sit on color strips, leaders or data. Leaders are short and never cross.
- **Names are consistent.** Short codes go on the plot and full names in the legend. One quantity keeps one name everywhere. Numbering is consecutive, with no gaps.
- **Panels carry no prose.** Definitions and caveats go to the caption.
- **Evidence over impressions.** Back a visual claim with numbers computed on the same view, and flag metrics that are not independent of how the labels were made.
- **Reports open with conclusions**, written as bullets, and keep bullets everywhere, including inside table cells.

## Reference index

| File | Read when |
| --- | --- |
| [references/process.md](references/process.md) | Planning a figure or page, running a review round, building a picker |
| [references/figures.md](references/figures.md) | Drawing or composing manuscript panels, specific chart types |
| [references/color-and-labels.md](references/color-and-labels.md) | Choosing palettes or colormaps, placing labels, legends, colorbars and leaders |
| [references/colormaps.md](references/colormaps.md) | Picking a colormap or palette from the collection, or adding one the user liked |
| [references/reports.md](references/reports.md) | Building an HTML report, review page or figure preview for collaborators |
| [references/artifacts.md](references/artifacts.md) | Publishing pages as Claude Artifacts (Claude-specific mechanics) |
| [assets/figstyle.py](assets/figstyle.py) | Starting matplotlib style for a new project: rcParams, mm sizing, `save()`, panel header |
| [assets/colormaps/](assets/colormaps/colormaps.json) | The colormap collection (`colormaps.json`) and its tool (`cmaps.py`: list, check, preview, register) |

## Checklist before sending

- [ ] Panels at final size in mm; Arial (or the project font); ticks ≥ 6 pt (≥ ~4 pt inside small panels); vector files plus a PNG preview.
- [ ] Colors from the frozen palette; every color code has a key; unclassified is grey.
- [ ] No overlaps between labels, strips, leaders and data; leaders short and uncrossed.
- [ ] Codes on plots, full names in legends; gene symbols in the species' convention; no counts in labels.
- [ ] Panel titles aligned and equal in size; colorbars below their panel; no notes left on panels.
- [ ] Sibling panels aligned and equal in height; no large empty gaps.
- [ ] Claims backed by numbers on the same view; non-independent metrics flagged.
- [ ] Decision and rejected options recorded in the project profile.
- [ ] Report: conclusions first, bullets, column definitions with a worked example, version note, changes table.

## Maintaining these rules

- When a review agrees on a new rule, add it to the project profile under **Candidates**, with the date, its source (which page and which comment) and one line of **Why**.
- Promote a candidate into this skill only when it also holds in a second project, or when the user says it is general. Write it without project names, data or links, because this repository is public.
- Apply a newly agreed rule only to the cases discussed. When it would overturn other review decisions, ask first.
- At project milestones, consolidate: merge duplicates, drop rules that were superseded, and re-verify the Claude-specific mechanics in `references/artifacts.md`.
