---
name: sync-reading-notes
description: Check recently added Zotero papers for missing Obsidian reading notes and create the missing notes as a coordinated batch. Use only when the user explicitly invokes `$sync-reading-notes`; use `$zotero-paper-summarizer` for one identified paper.
---

# Sync Reading Notes

Turn recent Zotero additions into missing Obsidian reading notes. This is an
explicit batch command. It authorizes the requested note writes, but does not
by itself authorize subagents or a whole-vault OpenAlex refresh.

Use the separately installed `zotero-paper-summarizer` skill as the authority
for Zotero routing, duplicate detection, full-text quality, note structure,
tags, and validation. If it is unavailable, stop and ask the user to install it
from this repository before continuing.

## Invocation

- `$sync-reading-notes` — inspect the 30 most recently added top-level Zotero items.
- `$sync-reading-notes limit 100` — override the recent-item limit.
- `$sync-reading-notes since 2026-09-01` — inspect items added on or after the given date.
- `$sync-reading-notes dry run` — report existing, missing, and blocked candidates without creating notes.
- `$sync-reading-notes parallel` — explicitly authorize subagents for independent papers.
- `$sync-reading-notes refresh citations` — explicitly authorize the bounded whole-vault OpenAlex citation refresh after review.

Options may be combined. Reject invalid dates or non-positive limits instead of guessing.

## Select the Batch

1. Use `zotero-mcp` `zotero_get_recent`; do not repeat the inventory through `@Zotero`.
2. With no option, request 30 items. For `since`, start with 100 and increase in bounded steps until the returned data crosses the requested date, stopping at 500 unless the user requests a larger scope.
3. If MCP omits metadata needed for a requested `since` filter, use a read-only Zotero local-API request as the documented fallback.
4. Keep top-level scholarly papers such as journal articles, preprints, and conference papers. Exclude books, book sections, attachments, notes, and webpages unless the user explicitly includes them.
5. Match existing notes by DOI first, then Zotero key, then normalized title plus first author and year. Repeated runs must be idempotent.

## Create Missing Notes

For a dry run, stop after reporting the batch and attachment/full-text readiness.

Otherwise:

1. Run duplicate checks centrally.
2. Resolve and quality-check each attached PDF once with the helper bundled in
   `zotero-paper-summarizer/scripts/extract_pdf.py`.
3. Process missing papers serially by default. Only when `parallel` was
   explicitly included, assign independent papers to subagents in bounded
   waves. Pass each worker its Zotero metadata, duplicate result, extraction
   report, and `OUTPUT` path; do not make it repeat discovery or extraction.
4. Do not create a full reading note when only an abstract or incomplete text is available. Report the exact blocker.
5. Review all returned notes centrally and apply tracker updates when the
   tracker exists. Run the global citation refresh once only when `refresh
   citations` was explicitly included; first run its confirmed whole-vault dry
   run, inspect the scope, then apply it.

## Completion Report

Report:

- scope used and Zotero items inspected;
- notes already present;
- notes created or updated, with absolute links;
- papers skipped or blocked and why;
- whether parallel processing or citation refresh was authorized;
- validation and citation-refresh limitations.
