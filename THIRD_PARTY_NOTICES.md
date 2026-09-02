# Third-party notices

This repository contains material adapted from the projects below. Upstream
revisions are pinned so later updates can be reviewed as explicit diffs.

## Cursor pstack: `unslop`

- Source: <https://github.com/cursor/plugins/tree/main/pstack/skills/unslop>
- Pinned repository commit: `efa2a531985e0a8084d36ff3cf87233be8a9f34b`
- Pinned `SKILL.md` SHA-256:
  `2789ab80477b7e382292e4d7acca1057784df19713fffb74622ff0f83b2f3733`
- Upstream license: MIT, Copyright (c) 2026 Lauren Tan
- Local changes: `SKILL.md` is preserved byte-for-byte; Codex UI metadata and a
  per-skill license file were added alongside it without changing the source.
- License text:
  [`third_party/licenses/cursor-pstack-MIT.txt`](third_party/licenses/cursor-pstack-MIT.txt),
  also included inside the installable skill directory

## Matt Pocock skills

The following skills contain material adapted from
<https://github.com/mattpocock/skills>:

- `grill-with-docs`, including the upstream `grilling`, `domain-modeling`, ADR,
  and context-format guidance bundled as internal references
- `wizard`, including `template.sh`
- `wayfinder`

Pinned repository commit: `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76`.

Upstream license: MIT, Copyright (c) 2026 Matt Pocock.

Local changes:

- `grill-with-docs` was made self-contained rather than requiring separately
  installed `grilling` and `domain-modeling` skills.
- `wayfinder` defaults to Linear, removes the dependency on Matt's repository
  setup skill, and requires explicit authorization before subagent dispatch.
- Cursor/Claude-specific invocation frontmatter was removed from copied skills;
  Codex invocation metadata was retained or completed for all three.

License text:
[`third_party/licenses/mattpocock-skills-MIT.txt`](third_party/licenses/mattpocock-skills-MIT.txt),
also included inside each installable adapted skill directory.
