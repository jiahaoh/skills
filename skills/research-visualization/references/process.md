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

## Pickers for choices that are hard to say in words

- **Many candidates**: build a checklist page whose saved state the agent reads back, instead of asking the user to type the names.
- **Continuous parameters** (camera azimuth, elevation, roll, scale, cutoffs): build a page with sliders that prints the parameters ready to paste back as code.
- Re-render from the picked parameters, and record them in the script under a named job.

## Everything from a script

- Number the scripts and give each one its own output folder. A rerun must reproduce every figure, report and review page.
- Panels meant for hand labelling in a vector editor get an extra "all labels" reference version, at the same size and position.
- Long-running renders take a job argument (`python render.py <job>`) and record their run time and memory in the project profile.

## Review rounds

- Reviewers comment on the published page. Read every thread and apply the comments.
- A comment applies to the element it was left on. When it states a pattern ("same colorbar problem"), apply it to every sibling panel and say so.
- Keep a **Changes** table on the review page (location | comment | what was done) and a short list of open questions. Bump the version note each round.
- Archive review marks before resetting them for a new round.
- After a round, say which threads remain open and why (for example: not sent to the agent, so it cannot resolve them).
