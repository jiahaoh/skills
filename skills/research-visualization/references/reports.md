# HTML reports and review pages

## Page structure

- Use a short title that names the thing, with no eyebrow line, date or count meta line, and no footer listing paths.
- Open with **Conclusions** as a plain bullet list (not summary cards). Then put the requests to the reader in a callout (tinted box, left border), keeping only the ones really needed.
- Order: what was tried → comparison figure → why the choice → workflow → the rules used to assign or score labels → results table → result figures → follow-up questions. Methods sit right after the workflow they belong to.
- Section titles name their content, never a generic word such as "Results".
- Use the full page column (about 1180 px) for text, tables and figures, with no narrow reading column. Sibling tables and figures share one width; only a multi-panel map row may break out. A wide table gets fixed, equal-width columns instead of breaking out.
- Show the version history as a bullet list, with a clean comparison table across versions (counts and what changed). Give each version its own tab, with the latest as the default.
- A preview whose purpose is the look of the figures is a clean board: titles only, no prose.

## Text and tables

- Prefer bullets to paragraphs, inside table cells too (no comma- or semicolon-joined lists).
- Put the definitions of a table's columns right above it, with a **worked example**. A small card with leaders pointing at each part of one cell works well. Define only that table's columns and skip self-evident ones.
- A name column shows the clean name; the reason or evidence goes in its own column.
- Sort rows within groups, with "others", "unassigned" and unclassified rows last. Make long groups collapsible.
- In a variant table, highlight what differs from the baseline row.
- Give columns room for their content: a gene with three numbers puts the numbers on their own line.
- When a row has no siblings to compare with, show the evidence at the next level up instead of "none".
- After an annotation table, add a confusion table against the reference (row %, rows grouped by the assigned label, columns by major division, plus outside and unresolved columns so that rows sum to 100%).

## Figures on pages

- Multi-panel figures: panel titles aligned on one line, nothing overlapping strips or annotations, and no wasted whitespace.
- Show the final labels next to the reference levels in one row (for example, reference summary | reference fine level | our labels), not only the raw clusters.
- When many groups need inspecting, add a dropdown that shows one group at a time, with its key evidence next to the map.
- Interactive side panels use the vertical space: one evidence item per line (gene, value, small bar), the color key in one column, one-line captions, and right-aligned values.

## Review pages

- Each row shows a spatial map thumbnail and an embedding thumbnail, the marker evidence (gene, % in the group, % in the comparison set), the composition by region and the reference match.
- Include a dot plot, with hover values, of the genes the table actually names. Add comparison genes when asked.
- Collect Agree / Change plus a note per row, including unclassified rows, with one stored record per reviewer.
- Back visual impressions with numbers computed on the same view. State the trade-off in the caption, and flag metrics that are not independent (for example, agreement with a reference that was used to name the labels).

## Deliverables

- Build the page with a script. Also export a self-contained single HTML file (its own skeleton and charset, figures inlined as WebP, data inlined) as the file to send.
