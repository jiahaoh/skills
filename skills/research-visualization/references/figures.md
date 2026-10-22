# Figures

## Size and type

- Draw at the final print size, in mm. Typical journal widths are 89 mm (single column), 120 mm (1.5 column) and 183 mm (double column); pages are at most about 247 mm tall. Never rescale later, in code or in the vector editor.
- Use Arial (or the journal font): 7 pt text, 6 pt ticks and legends, 8 pt bold panel letters. Text inside small panels (ring labels, compact legends) may drop to 4–5.5 pt, never below about 3.3 pt.
- Axes lines 0.5 pt, data lines 0.75 pt.

## Export

- Save every panel as SVG and PDF with editable text (`svg.fonttype = none`, PDF Type 42), plus a PNG for review.
- Rasterize only the layers with many marks (embedding points, map cells, 3D renders) at 600 dpi. Axes, text, legends and scale bars stay vector.
- Panels for a composed figure are saved **untrimmed** at the exact slot size. Use a transparent background when the composed figure has a tinted background.
- Compose pages from the panel PDFs at 1:1, using mm coordinates (PyMuPDF works). The compose script should warn when a panel exceeds its slot or when slots overlap. Deliver the composed PDF with its fonts embedded.

## Layout

- Give each figure one focus. Every other panel supports it.
- Align panel edges and heights across a row. Size siblings so they match exactly (for example, two stacked panels whose combined height equals the panel beside them).
- Fill large gaps by enlarging panels or fonts before adding decoration. Leave no big gap between a frame and its first element.
- A mirrored or symmetric layout reads as two halves of one story. Mirrored panels use the same plot radius and point size, so the two clouds look identical.
- To group the halves of a page, use a very light tint (about 3.5%: 1% is invisible, 7% too strong) or a dashed colored border on white. Decorative connectors (arrows, streams, funnels) must stay lighter than the data.

## Chart conventions

- **Histograms / QC**: log x when the data span decades; about 50 bins; closed frame; fill in the assay color with a dashed median in the same color; one assay per panel. State any cells left off a log axis (zero counts).
- **Embeddings (UMAP and similar)**: rasterized points; small axis arrows at the lower left, with no ticks or frame. For an atlas style, color by the fine level, put coarse-level codes in free space and add a ring (a band for the fine level, a thin line for the coarse level). The ring must never overlap the cloud; put the ring scale in a small gap, without %.
- **Dot plots**: a light grey block marks a group's markers and a thin dark square marks the genes that define each row; leave gaps between groups and no group headers above the grid. Use portrait (genes as rows) for long supplementary pages.
- **Heatmaps / matrices**: mark rows as confident or review rather than adding a numeric confidence column. Put the colorbar below, and never make the heatmap wider than the page column. In a bubble matrix, size encodes fraction and color encodes enrichment.
- **Spatial 2D maps**: color cells by label and draw region borders dashed (dark, 0.8 pt), each shared border once, with a dashed tissue outline. Compare against a reference at the level that matches what is being called, next to its coarser level.
- **3D renders**: a flat illustration style beats shaded spheres. Add depth cues (envelope tones, light fog, a floor shadow) rather than heavy lighting, and pick the camera with a picker. Keep cells at true size and exaggerate z only between cells, stating the factor on the panel. Use a 3D scale bar (xy plus z). When shapes are schematic, or a panel duplicates or mirrors other data, say so in the caption.
- **Zoom panels**: draw a dashed red box on the overview and a solid frame (or the box's own outline) on the zoom. Windows must not overlap. Number the windows so their leaders do not cross, and mark the same spot on any comparison panel.
- **Sankey**: color bands from the target palette and leave residual nodes (per-group unclassified) unlabelled to keep the plot quiet.
- **Examples cited in the text**: put numbered arrows at the same spots on each compared panel.
- **Scale bars** on every spatial panel.
