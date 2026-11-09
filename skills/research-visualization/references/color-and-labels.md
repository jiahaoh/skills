# Color, labels and legends

## Color

- Start from the colormap collection ([colormaps.md](colormaps.md)). Prefer `proven` entries, and never propose a `rejected` one.
- Follow the field's reference scheme where one exists, such as an atlas's cell-type and region colors. Give new types colors on their family's **tint-shade surface** around the reference main color (chroma follows lightness), so they still read as members of the family.
- Use color to show relations the reader should see: **hue** separates sub-families (layers, subclasses, lineages) and **lightness** separates members. Explain the color logic in words when delivering a palette.
- When asked to make a palette "more harmonious", keep each color's direction (hue order) and change only lightness and chroma.
- Freeze an agreed palette as a CSV and read colors only from it. Use neutral grey (`#D9D9D9`) for unclassified and no-type cells.
- Print default (a design system's chart section overrides it; slides use opaque fills, see [slides.md](slides.md#slide-charts)): fill bars and boxes translucently (alpha about 0.5) with thin dark edges.
- Draw medians and other marks in the **same hue, opaque**. No red marker lines: they look loud and break the panel's color unity.
- Sequential maps: use a light map whose low end is tinted rather than white, so low values stay visible on a white page, with lightness falling monotonically. Avoid green-to-pink ramps, which turn grey in the middle. For expression values, scale the map to the 1st–99th percentile of the expressing cells and draw non-expressing cells faint grey.
- Check accent colors against data colors: an accent that matches a data class makes the page ambiguous. Give one assay or modality one hue everywhere (histograms, colormaps, page accents).
- Every color code (pills, chips, bands, heatmaps) needs a visible key.
- When a design system supplies the colors, use its token names, never copied hex values, and record its version. Where several tokens share a hue, label each colored mark by name too.
- One mapping per concept across a talk or paper: an image channel, a method or a stage keeps its color everywhere.

## Names

- Put short codes on the plot and full names in the legend. Labels carry no counts.
- Number labels consecutively per prefix, with no gaps such as 1, 2, 3, 6. Record the closest reference match in a table column, not in the label.
- One quantity has one name in the definition, the column header, the figure annotation and any interactive panel.
- Write gene symbols in the species' convention in figures, whatever the case in the data.

## Numbers

- Give every number its unit and context.
- Use thousands separators (12,400).
- Use `×` for factors and dimensions (2.3×, 30×2048×2048), an en dash for ranges (5–10 µm), and `→` for before → after.
- Name the base of every percentage where it could have two ("12 % of all reads" vs "15 % more than the baseline").
- Use log axes where values span decades, labelled with units.
- Annotate ratios on the chart ("2.3× faster").
- Set paths, IDs and config keys in mono.

## On-plot labels and leaders

- Place labels in free space near their group, with no white halo. On maps, put labels inside regions first (white on dark fills) and outside with leaders only where they do not fit.
- Leaders are short. They leave the label horizontally, bend once at 45°, and end on a dot just inside the target. They never cross each other or a label. Prefer placements with the fewest crossings, then the shortest leaders.
- When labels must be placed by hand, provide a reference version with every label at its region's most interior point.

## Legends, strips and colorbars

- Keep legends compact, one line per item: swatch, code, then a grey annotation. Drop a legend whose content the on-plot labels already give. Print default (a design system's chart section overrides it): put legends to the right of grids.
- Group legend items by family. Members can be joined by a thin black line.
- Color strips beside heatmaps and dot plots are thin rectangles, clear of the labels.
- Colorbars are thin, sit below their panel and show the value range.
- Panel titles are one line, aligned across a row and the same size on every panel (for example, a 7 pt header with a rule on each side).
- No explanatory notes on panels: definitions and caveats go to the caption (presenter notes on slides). The exceptions, stated on the panel: a physical scale that differs from true scale (such as an exaggerated axis), the dataset or condition name, the which-way-is-better tag, and a short label for results from an older code or data version.
