---
name: research-visualization
description: House rules for research figures, talk slides, analysis reports and review pages, distilled from many rounds of review comments; covers the design process, print-ready panel export, slide composition and slide charts, diagrams, color, labels and legends, chart-specific conventions, HTML report structure and shared-page mechanics. Use before drawing a manuscript panel or composed figure, making slides or a deck for a research talk (slide charts and diagrams, layout-board review rounds, click builds and animation, presenter notes), building an HTML report or review page for collaborators, choosing a palette or colormap, or applying review comments to any of these.
---

# Research Visualization

Rules that came back as review comments on first drafts of figures, slides, reports and review pages. Apply them to the **first draft**. The goal is fewer review rounds, not decoration.

## Start here

1. Look for the project's visualization profile: a file such as `docs/visualization-standard.md`, or a section the project's agent instructions point to. It holds the project's color meanings or palette files, reference material, overrides and decisions already made; look values come from the design system (step 2). **Project rules override this skill.**
2. If the project uses a design system, read its tokens and its chart and slide sections. They override this skill's look defaults (colors, fonts, chart look, slide layout); the project profile overrides both.
3. Read only the reference files the task needs (index below).
4. Before designing, confirm the inputs: which label version, which embedding, which reference level. Several design rounds were lost to the wrong input.

## Core rules

- **Discuss, then draw.** Propose content and layout first when the user wants to discuss. For visual choices, draw variants side by side, recommend one and say why.
- **Record decisions and rejections** with the date in the project profile. Never offer a rejected option again.
- **Everything from a script.** Every figure, slide asset, report and review page is rebuilt by rerunning its script. Hand edits happen only later, on exported vector files.
- **Final size from the start**, in the target medium's unit, and never rescale. Print panels in mm and pt ([figures.md](references/figures.md)); slide figures in slide px at the slot they fill ([slides.md](references/slides.md)).
- **Vector out, raster inside.** Export editable vector files plus a PNG preview. Rasterize only dense layers such as points, maps and renders.
- **One color source.** Read colors from a frozen palette file, or from the design system's tokens by name (record the design-system version). Start from the colormap collection, and add any colormap the user liked to it. Every color code needs a visible key, and "unclassified" is always neutral grey.
- **Nothing overlaps.** Labels never sit on color strips, leaders or data. Leaders are short and never cross.
- **Names are consistent.** Short codes go on the plot and full names in the legend. One quantity keeps one name everywhere. Numbering is consecutive, with no gaps.
- **Panels carry no prose.** Definitions and caveats go to the caption (figures, reports) or the presenter notes (slides).
- **Evidence over impressions.** Back a visual claim with numbers computed on the same view, and flag metrics that are not independent of how the labels were made.
- **Claim only what the data can show.** Without ground truth, write agreement or yield, not accuracy. Never show a planned or unfinished analysis as a result. Results from an older code or data version carry a short label for that version and their date (on slides the date may move to the presenter notes at the author's request; see [slides.md](references/slides.md)).
- **Reports open with conclusions**, written as bullets, and keep bullets everywhere, including inside table cells.

## Reference index

| File | Read when |
| --- | --- |
| [references/process.md](references/process.md) | Planning a figure, slide or page, running a review round, building a picker or layout board |
| [references/figures.md](references/figures.md) | Drawing or composing manuscript panels, specific chart types, microscopy images, diagrams |
| [references/slides.md](references/slides.md) | Making slides for a talk: composition, slide charts, diagrams, images, benchmarks, motion, presenter notes, layout-board review |
| [references/color-and-labels.md](references/color-and-labels.md) | Choosing palettes or colormaps, placing labels, legends, colorbars and leaders, formatting numbers |
| [references/colormaps.md](references/colormaps.md) | Picking a colormap or palette from the collection, or adding one the user liked |
| [references/reports.md](references/reports.md) | Building an HTML report, review page or figure preview for collaborators |
| [references/artifacts.md](references/artifacts.md) | Publishing pages or decks as Claude Artifacts (Claude-specific mechanics), testing a built page, SVG in web pages |
| [assets/figstyle.py](assets/figstyle.py) | Starting matplotlib style for print panels in a new project: rcParams, mm sizing, deterministic `save()`, panel header |
| [assets/colormaps/](assets/colormaps/colormaps.json) | The colormap collection (`colormaps.json`) and its tool (`cmaps.py`: list, check, preview, register) |

## Checklist before sending

- [ ] Print: panels at final size in mm; Arial (or the project font); ticks ≥ 6 pt (≥ ~4 pt inside small panels); vector files plus a PNG preview.
- [ ] Slides: figures at slot size in slide px; chart and diagram text at the design system's sizes, nothing below its floor; about 40 words; nothing on the face that belongs in the notes; the last build reads alone.
- [ ] Reruns produce identical bytes (same SHA-256 when nothing changed).
- [ ] Colors from the frozen palette or design-system tokens; every color code has a key; unclassified is grey.
- [ ] No overlaps between labels, strips, leaders and data; leaders short and uncrossed.
- [ ] Codes on plots, full names in legends; gene symbols in the species' convention; no counts in labels.
- [ ] Panel titles aligned and equal in size; colorbars below their panel; no notes left on panels.
- [ ] Sibling panels aligned and equal in height; no large empty gaps.
- [ ] Claims backed by numbers on the same view; non-independent metrics flagged; agreement or yield without ground truth; no planned analysis shown as a result.
- [ ] Decision and rejected options recorded in the project profile.
- [ ] Report: conclusions first, bullets, column definitions with a worked example, version note, changes table.

## Maintaining these rules

- When a review agrees on a new rule, add it to the project profile under **Candidates**, with the date, its source (which page and which comment) and one line of **Why**. Keep each candidate's status current: adopted (and where), still a candidate, or rejected.
- Route each rule to one home. Look values (colors, type, sizes, component appearance) go to the design system, then into every project that vendors its tokens. General practice goes to this skill. Rules about one project's data, colors or reference material stay in its profile. Precedence when they disagree: project profile, then design system (look), then this skill.
- Promote a candidate into this skill only when it also holds in a second project, or when the user says it is general. Write it without project names, data or links, because this repository is public.
- Apply a newly agreed rule only to the cases discussed. When it would overturn other review decisions, ask first.
- Record each promotion below with its date and source.
- At project milestones, consolidate: merge duplicates, drop rules that were superseded, and re-verify the Claude-specific mechanics in `references/artifacts.md`.

### Promotions

- 2026-11-09: rules routed here from one project's profile and its design-system notes when the author split the material into four layers (design system for the look, this skill for the how, the project profile for project rules, a shared template for the machinery), declared general by the author: [references/slides.md](references/slides.md) (slide-drawn charts only when animated, the histogram for distribution-changing methods, reduced motion, method principle, keys below tables, answer reviewer questions in the reply, dark ground never as a theme; chart sizes and line weights now taken from the design system), [references/color-and-labels.md](references/color-and-labels.md) (one mapping across talks, reports and papers; color never alone; 4.5:1 contrast; third-party logos as labels; real minus; tabular figures), [references/reports.md](references/reports.md) (sticky table of contents, filter row, plain writing, sentence case, technical terms in English, citation under borrowed figures, offline fonts), [references/process.md](references/process.md) (one current rule set with a history, picker voice and working state, an item's note overrides a general rule) and this file (candidate status, routing to one home).
- 2026-11-09: the slide rules in [references/slides.md](references/slides.md), the claim rules, the Numbers block and the layout-board pattern were declared general by the author, after five layout-board review rounds of one talk. Several also confirm existing rules in a second project: one point per slide (one focus per figure), fill the frame (fill large gaps), labels never cover an image (nothing overlaps), square-swatch image keys (every color code has a key).
