# Jiahao's agent skills

A curated repository of reusable agent skills and their supporting assets. The
collection is intentionally small: each skill should capture a recurring
workflow, a non-obvious constraint, or a deterministic helper worth carrying
between projects.

## Skills

| Skill | Invocation | Purpose | Origin |
| --- | --- | --- | --- |
| [`sync-reading-notes`](skills/sync-reading-notes/SKILL.md) | Explicit | Create missing Obsidian reading notes for recent Zotero papers as a controlled batch. | Personal |
| [`zotero-paper-summarizer`](skills/zotero-paper-summarizer/SKILL.md) | Automatic or explicit | Create one evidence-grounded reading note from verified full text. | Personal |
| [`research-visualization`](skills/research-visualization/SKILL.md) | Automatic or explicit | Apply review-tested rules for research figures, talk slides, reports and review pages. | Personal |
| [`unslop`](skills/unslop/SKILL.md) | Explicit | Remove common AI-writing patterns while preserving meaning and voice. | Vendored from Cursor pstack |
| [`grill-with-docs`](skills/grill-with-docs/SKILL.md) | Explicit | Stress-test a plan while maintaining a project glossary and selective ADRs. | Adapted from Matt Pocock |
| [`wizard`](skills/wizard/SKILL.md) | Automatic or explicit | Generate an interactive shell guide for manual setup or migration steps. | Adapted from Matt Pocock |
| [`wayfinder`](skills/wayfinder/SKILL.md) | Explicit | Map a large effort as decision tickets, using Linear by default. | Adapted from Matt Pocock |

## Install

Ask Codex to install a skill from its GitHub directory. For example:

> Install `unslop` from
> `https://github.com/jiahaoh/skills/tree/main/skills/unslop`.

For the reading-note workflow, install both skills:

> Install `sync-reading-notes` and `zotero-paper-summarizer` from
> `https://github.com/jiahaoh/skills`.

The cross-agent [`skills`](https://skills.sh/) installer can also discover the
repository:

```bash
npx skills@latest add jiahaoh/skills
```

Choose only the skills needed on that machine or project. Do not install a
managed copy and a repository symlink at the same time.

## Reading-note assets

`zotero-paper-summarizer` carries the canonical reading-note template, helper
scripts, and Codex/Claude agent-wrapper examples inside its directory. This
keeps the batch and single-paper workflows aligned without duplicating their
rules across the repository.

The helper scripts are designed to run from the Obsidian vault root. Set
`READING_NOTES_VAULT` when the current directory is not the vault. The
OpenAlex citation refresh is a whole-vault operation and must not run without
explicit authorization for that scope.

## Maintenance

Run the repository checks before committing:

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests
```

Third-party origins, pinned revisions, modifications, and license notices live
in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). Upstream changes are
reviewed and merged deliberately; they are never pulled into installed skills
automatically.

No repository-wide license has been selected for original material. The
third-party portions remain available under their recorded upstream licenses.
