---
name: zotero-paper-summarizer
description: Create or update structured Obsidian reading notes from papers in the user's Zotero library, including traceable Zotero metadata, full-text quality checks, duplicate detection, controlled tags, and citation links. Use for paper summaries, reading notes, journal-club notes, or lab-meeting preparation by title, author, DOI, keyword, or Zotero item.
---

# Zotero Paper Summarizer

Create evidence-grounded reading notes for later research use. Do not treat an abstract as if it were the full paper.

## Sources of Truth

- Read the bundled `assets/Reading-note-template.md` before drafting and follow
  its core and applicable conditional sections.
- Resolve the vault from `READING_NOTES_VAULT`, or use the current working
  directory when the variable is unset. Save finished notes in
  `04.Reading/Notes/` using `<FirstAuthor et al. (Year) - Short description>.md`.
- Reuse the live tag vocabulary in existing notes; the template's tag table is a canonical baseline, not a complete catalog.
- Resolve helper paths relative to this skill's directory and use the scripts
  in `scripts/`. Run them from the vault root unless `READING_NOTES_VAULT` is
  set.

## Zotero Access Routing

Keep the data path consistent instead of mixing overlapping Zotero integrations without a reason.

1. Use the configured `zotero-mcp` tools as the default structured backend for recent items, search, metadata, child attachments, and indexed full text. Prefer read-only tools unless the user explicitly requests a Zotero write.
2. Use the curated `@Zotero` plugin helper for Zotero Desktop status/bootstrap and citation-specific operations such as BibTeX export or citation insertion. Do not repeat an MCP query through the helper merely because both routes are available.
3. Use a raw Zotero local-API request only when the MCP tools lack a parameter required by the task. State the missing capability and keep the request read-only when possible.
4. Use Zotero GUI or Computer Use only for a genuinely UI-only operation or an authenticated-session fallback, not for routine metadata or attachment reads.
5. Regardless of how metadata is retrieved, use the bundled
   `scripts/extract_pdf.py` as the authoritative attached-PDF quality gate for
   a full reading note.

## Retrieve and Verify the Paper

1. Search Zotero with the user's title, DOI, author, keyword, or item identifier through `zotero-mcp`, following the routing above.
2. If several plausible items match, give concise identifying details and ask the user to choose.
3. Retrieve metadata, including the parent item's eight-character Zotero key and DOI when available. Never invent metadata or a Zotero key.
4. Once the DOI is known, run:

   ```bash
   python3 <skill-dir>/scripts/note_tools.py check-dup "<doi>"
   ```

   If it reports a duplicate, do not create a second note. Report the existing note and ask whether the user wants it updated. For papers without a DOI, check title, author, and year manually.
5. Prefer the attached PDF as the full-text source. Run:

   ```bash
   python3 <skill-dir>/scripts/extract_pdf.py <zotero-item-key>
   ```

   Branch on its report:

   - `STATUS: OK`: read the Markdown path printed at `OUTPUT`.
   - `STATUS: ESCALATE`: inspect the page images printed at `IMAGES`; note if the rendered fallback covers fewer pages than the paper.
   - `STATUS: ERROR`: inspect `NOTE`. A complete Zotero-indexed full text may be used as a fallback when it is demonstrably complete. Otherwise report the missing or unusable full text and do not create a full reading note.

Do not read a large raw PDF through a generic text reader. Read the abstract, introduction, methods, results, discussion, and relevant figure or table context from the verified full-text source.

An abstract-only note is allowed only when the user explicitly asks for one. Label the limitation clearly in the note and in the completion message.

## Draft the Note

Classify the paper by its dominant contribution and include the matching article-type tag. Follow the template, including applicable technology, biological-discovery, resource/atlas, or review sections.

Required frontmatter for a Zotero-backed paper:

```yaml
---
title: "Full article title"
authors: "First/co-first author(s); Corresponding author(s)"
journal: "Journal or preprint-server name only"
doi: "10.xxxx/xxxxx"
zotero_key: "MXQZECW5"
zotero_uri: "zotero://select/library/items/MXQZECW5"
year: 2024
status: "published"
summary: "What the paper delivers."
motivation: "Why the work was needed."
storyline: "How the method and evidence build to the conclusion."
tags:
  - technology-development
---
```

- Set `status` to `preprint` for non-peer-reviewed preprints and `published` otherwise.
- Keep `summary`, `motivation`, and `storyline` distinct, each on one line.
- Keep `journal` to the venue name; do not append volume, issue, pages, dates, or other citation text.
- Omit `doi` only when none exists. Omit `zotero_key` and `zotero_uri` only when there is genuinely no corresponding Zotero item.
- Separate reported evidence from your interpretation. Highlight novelty, limitations, and the figures or tables that carry the main claims.

## Validate and Finish

1. Inspect the live vocabulary before choosing final tags:

   ```bash
   python3 <skill-dir>/scripts/note_tools.py tags
   ```

2. Validate proposed tags:

   ```bash
   python3 <skill-dir>/scripts/note_tools.py check-tags <tag1> <tag2> ...
   ```

   Replace every `FIX` result with the existing form. Use a `NEW` tag only when it represents a genuinely new concept.
3. Save the note and verify its filename, frontmatter, Zotero URI, required sections, evidence clarity, and save location.
4. Do not refresh citations merely because a note has a DOI. The helper scans
   the whole private vault and contacts OpenAlex for its DOI set. Only after the
   user explicitly authorizes that scope, run a dry run and review it before
   applying:

   ```bash
   python3 <skill-dir>/scripts/refresh_citations.py --confirm-whole-vault
   python3 <skill-dir>/scripts/refresh_citations.py --confirm-whole-vault --apply
   ```

5. If `04.Reading/Reading-tracker.md` exists, mark the item complete with
   `<skill-dir>/scripts/note_tools.py tick "<doi>"`. Do not create a tracker
   merely to satisfy this workflow.
6. Report the created or updated file and any access or extraction limitation.

## Batch Requests

Use subagents only when the user explicitly requests subagents, delegation, or parallel agent work.

- The coordinator should retrieve the recent-item batch and run duplicate checks once, using `zotero-mcp` rather than asking every worker to rediscover the batch.
- Keep each worker scoped to an independent paper. Extract and quality-check each PDF once; pass the verified `OUTPUT` path and extraction report to its worker instead of repeating extraction.
- Workers create and validate their assigned notes but skip the global citation refresh. After all notes pass review, the coordinator runs `refresh_citations.py` once for the batch and performs any applicable tracker updates.
- If citation refresh cannot reach OpenAlex, report the limitation and leave existing notes untouched. Do not escalate to a broad external refresh that sends every vault DOI or may rewrite many notes unless the user explicitly authorizes that scope.
- Finish with a coordinator review of filenames, frontmatter, Zotero keys/URIs, tags, required sections, and one-note-per-DOI consistency.
