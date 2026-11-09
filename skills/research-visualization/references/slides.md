# Slides

Rules for research-talk slides, settled over five layout-board review rounds of one long talk and declared general on 2026-11-09. Sizes assume a 1920 × 1080 slide. A design system's slide and chart sections override the look defaults here; the project profile overrides both.

## Talk template

- If the user's agent instructions or memory name a talk template repository, start new decks from it and follow its workflow. The template holds the framework mechanics; this file holds the rules.

## Composition

- **One point per slide.** Split a slide that answers two questions. Give the split slides a letter suffix, so the IDs of later slides, and anything keyed by them, stay put.
- **The figure carries the slide.** If the slide shows its intent at a glance, it needs no text. Figure, design, method, metric and example slides have no lead and no bullets. Where a sentence is needed, write one short sentence that states the point, as a lead or as one line under the figure. No bold lead by default.
- **One visual centre.** One figure block (one figure, or sibling figures on a shared baseline) fills at least half of the space below the title. A text slide has at most three short bullets.
- **About 40 words** below the title. Quotes, caveats, extra numbers and sources go to the notes.
- Titles are short noun phrases.
- **Text is black.** Body text (lead, bullets) is about 30 px; chart and diagram text follow their sections below. Color belongs to the data: no accent-colored numbers or headings. The exceptions are the which-way-is-better tag (accent text) and the active step-track marker (accent fill).
- **No page components:** no KPI numbers, ruled column headings, callouts, or a caption under every block.
- **Fill the frame.** Cards fill their boxes and figures fill the slide. Keys and captions sit below the figure, not above it.
- **Answer the question on the slide.** If a reviewer asks what something is, the slide is unclear. Label it so the question does not come up.

## Clean slide face

- Nothing grey and small on the face: no cite line, no "pilot" or "preliminary" tag, no small description at the bottom of the slide or under each image. Sources, run dates and status go to the presenter notes.
- Labels allowed on a panel: the dataset or condition name, the which-way-is-better tag, a physical scale that differs from true scale, and a short label for results from an older code or data version (with its date, unless the author moves the date to the notes).
- No issue-tracker IDs, run paths or machine paths on slides. Name the experiment or the dataset; IDs go to the detail notes.
- Borrowed and third-party images carry no cite line. Their source goes to the notes.

## Slide charts

- Draw charts from a script, as SVG with text as text, at the size they fill on the slide, in slide px. Never scale a chart to fit its slot. Laying out at 72 dpi makes one SVG point one slide pixel.
- Text sizes at slot size: title 22 px, axis labels 20 px, ticks 18 px, legend and notes 17 px. Nothing below 17 px.
- Default look: title centred above the axes, left and bottom axes only, no grid, lines 3 px with markers, point labels in the series color, ratios in a small framed box, opaque bars with a thin ink edge. Legend in a framed box at the upper left, stacked, or as a label at each line's end.
- Label every axis, with units. Keep the order of panels and conditions the same as on the slide that introduced them.
- **Which way is better:** one form for the whole talk (for example a pill "↑ higher is better"), prominent, on every metric axis or metric picture. Leave it out where a ✓/✗ badge or the chart already says it.
- **Results show the winner.** A table or chart of results encodes good and bad (a color scale per column, the best value marked), so the best and worst read without reading numbers. Make it large.
- **Many conditions:** grouped bars with many groups are hard to read. Use dot plots, slope charts, small multiples or a colored table.
- One fixed color per method or arm for the whole talk.
- A raster picture with text (a timeline drawn with an image library) follows the same sizes and colors and is saved at twice its slot size.

## Diagrams

- **Light.** Thin strokes, no heavy black label bars, no red borders. Boxes are not crowded.
- Group containers are dashed outlines with a plain label. Items are told apart by a light fill or edge color, not by weight.
- Diagram text is at least 22 px at slide size. Measure every text and widen the box rather than letting text overflow.
- A slide that is only a diagram has no lead. The sentence goes to the notes.
- A recurring overview schematic can open each section with the current part lit ("where we are"). Draw it once and reuse it.
- The general diagram grammar is in [figures.md](figures.md#diagrams).

## Methods as banners

- One banner per method: its name, what it does in one line, and a small pictogram of what it does (what it removes, what it can move, how it finds a thing).
- Group methods by family, one light color per family. Split families across slides when one slide cannot hold them.
- A pictogram's ground matches its card.
- Where a click-driven animation explains the method better, it replaces the pictogram.

## Images

- **Show the raw image first,** before detections or overlays.
- **Examples are big:** a whole field of view or a large field, not a small crop.
- **One dataset per slide.** Synthetic and real examples go on separate slides.
- Choose examples where the conditions differ visibly. Prefer a less crowded region when the point is shape.
- Name the dataset on every panel (dataset, field, round or condition).
- **3D data are shown as 3D.** Do not use a maximum projection when spots or cells are the point. Show named z-slices or an orthogonal view; add XZ or YZ views when a z shift is the point.
- **Real data where it exists.** Show a method's behaviour on real images, with the schematic beside them, not instead of them. Use more than one dataset where results may differ.
- **Square-swatch keys** for image colors, not pills, with one wording for the whole talk (for example "reference / moving / overlap").
- Labels sit outside the image and never cover it.
- A dark ground is allowed on an image-heavy slide where white makes the image look out of place.

## Benchmarks

- **Design before results.** Before any result, a slide says which data (synthetic conditions and their parameters, real datasets), how the experiment runs (workflow, arms) and which metrics, each metric as a small picture of how it is computed. Use a design slide and a result slide when one slide cannot hold both.
- Every metric says which way is better.
- **Show downstream benefit.** Judge a processing step by what it does to the next steps, on a designed case where the problem is present.
- Show each method on the data that shows its effect.
- A planned or unfinished run gets a fallback slide that says what it will test, never a result.

## Motion and builds

- **Click builds in reading order:** one panel per click, left to right, then top to bottom, unless a note says otherwise. The first state shows the title and the first panel. A chart may build per condition.
- Animate only where the motion explains a process. A slide that needs no animation has none.
- **Processes move on the presenter's click, not on a clock.** Each click moves the drawing to its next state; transitions morph between states, and back on the previous key.
- A step track marks the steps: the active marker fills with the accent color and its label turns bold. No progress bar or timeline.
- **One animation at a time.** Only the panel that just entered plays; earlier panels hold their last frame. An animation plays once unless a loop is asked for. A method's panel may enter still and play on the next click.
- **The last state reads alone,** because print and PDF show only it.

## Presenter notes

- Two to four spoken sentences, one line per click, at most about 90 words. Add a status line (pilot, older version) where it applies. The notes list the builds.
- Details (sources, numbers, run IDs, decisions, history) go to a separate detail file per slide that the deck does not load.

## Parked, not deleted

- Move slides taken out of the talk to a parked folder, with their outline entry, code and notes. The author may want them back.

## Layout review on a board

- The author reviews layouts on a board: one canvas per slide at slide size, with the title and lead as guides. The author draws regions, text and notes and writes a note per slide. The board stores them in the page's database ([process.md](process.md#pickers-for-choices-that-are-hard-to-say-in-words)).
- A slide with no reference counterpart gets a wireframe on the board. When the content allows two layouts, render both side by side, recommend one and wait for the author's pick before polishing.
- Reply per slide in the slide's reply field: what changed, or why not. Never overwrite the author's shapes or notes.
- Round mechanics (read, archive, apply, reply, distil) are in [process.md](process.md#review-rounds).

## Slide workflow

1. **Message.** The one point and the one figure. Everything else goes to the notes. Name the reference-deck page the slide follows, if there is one.
2. **Layout.** Wireframe or two variants on the board; wait for the pick.
3. **Figures** from the asset's script, at slot size.
4. **Compose.** Title, optional one-sentence lead, figure block; builds in reading order; notes list the clicks.
5. **Review the built deck.** Screenshot each slide at each build (next to its reference page) and check: figure block at least half of the space, about 40 words, black text, nothing on the face that belongs in the notes, no clipped or covered labels, the last state reads alone. Then show the author.
6. **Record** the pick and the rejected options in the project profile.

Many slides at once: one agent per section drafts its slides, an independent agent checks them against the sources and notes, and the section agent fixes what it found.
