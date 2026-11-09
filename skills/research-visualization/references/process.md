# Process

## Discuss, then draw

- For a new figure or page, propose the content and layout first: the panels, what each one shows, and the encodings. Wait for agreement when the user asks to discuss first.
- Confirm the inputs before designing: which annotation version, which embedding, which reference level. Wrong inputs cost more rounds than wrong styling.
- When the choice is visual (colormap, label style, render style, border style), draw the variants side by side on a contact sheet (`review_*.png`). Recommend one and give the reason.
- Some figures will be kept "for reference" but not used. Keep them under their own name and say so in the project profile.

## Record decisions

- In the project profile, record each choice with the date and the options that were rejected. Name the winner, the alternatives that were compared and why the winner was chosen.
- Never offer a rejected option again unless the user brings it back.
- Keep superseded layouts in the script under their own names until the user drops them, and make the newest one the default.
- When a choice was a trade-off, note what was given up.
- Keep the project profile as one current rule set, ordered by topic. When review rounds disagree, the later round wins; list each replaced rule, and the round that replaced it, in a short history section.

## Pickers for choices that are hard to say in words

- **Many candidates**: build a checklist page whose saved state the agent reads back, instead of asking the user to type the names.
- **Continuous parameters** (camera azimuth, elevation, roll, scale, cutoffs): build a page with sliders that prints the parameters ready to paste back as code.
- **Layouts** (slides, figure pages): build a layout board, a page backed by its database with one canvas per item at its real size. The author draws regions, text and notes and writes a note per item; the agent reads them back and replies per item in a reply field. The agent never overwrites the author's shapes or notes. To propose shapes, ask the author to close the board first, then append to the stored shapes. See [slides.md](slides.md#layout-review-on-a-board).
- Re-render from the picked parameters, and record them in the script under a named job.
- A picker or tool opens in a working state, with real data or clearly marked example data. It speaks to the reader as "you", says what to do next ("then press Save and tell the agent in chat"), and its status line states the result ("Saved.", "Not saved yet.").

## Everything from a script

- Number the scripts and give each one its own output folder. A rerun must reproduce every figure, report and review page.
- Panels meant for hand labelling in a vector editor get an extra "all labels" reference version, at the same size and position.
- Long-running renders take a job argument (`python render.py <job>`) and record their run time and memory in the project profile.

## Review rounds

- Reviewers comment on the published page. Read every thread and apply the comments.
- On a board or picker, the notes live where the page stores them (its database), not in comment threads. Read the database; check comment threads too.
- **Archive the notes verbatim before applying** anything, and archive the replies before the board is cleared, so every round can be traced.
- Sort the notes into item-specific ones and general ones ("apply to every slide like this").
- Reply per item: what changed, or why not.
- Many items: one agent per section applies its notes, an independent agent checks each section against the notes, and the section agent fixes what it found.
- **Distil** the general notes into rules in the project profile, each with its date, source and one line of Why, so promotion into this skill stays mechanical.
- An item's own note overrides a general rule for that item; do not extend the exception to other items.
- A comment applies to the element it was left on. When it states a pattern ("same colorbar problem"), apply it to every sibling panel and say so.
- Keep a **Changes** table on the review page (location | comment | what was done) and a short list of open questions. Bump the version note each round.
- Archive review marks before resetting them for a new round.
- After a round, say which threads remain open and why (for example: not sent to the agent, so it cannot resolve them).
