# Repository instructions

This repository is the canonical source for Jiahao's portable agent skills.

## Structure

- Keep installable skills directly under `skills/<skill-name>/`.
- Every skill must contain `SKILL.md` and `agents/openai.yaml`.
- Keep a skill's required scripts, references, templates, and agent examples
  inside that skill so installing its directory does not depend on this
  repository's surrounding layout.
- Do not add per-skill READMEs. Use the root README as the catalog.

## Invocation

- Human-run commands use `policy.allow_implicit_invocation: false` in
  `agents/openai.yaml`. Their descriptions also state the explicit trigger so
  other harnesses do not treat them as automatic behavior.
- When a vendored `SKILL.md` must remain byte-for-byte identical to its source,
  preserve source-specific invocation frontmatter and express the matching Codex
  behavior in `agents/openai.yaml`.
- Model-invoked skills omit that policy setting.
- A description must say what the skill does and when it applies. Except in a
  byte-for-byte vendored source, an explicit-only description should not claim
  that it always runs.

## Provenance and privacy

- Record every adopted or substantially adapted source in
  `THIRD_PARTY_NOTICES.md`, including the upstream URL, pinned commit, license,
  and local changes.
- Preserve the upstream copyright and license text for copied material.
- Review upstream updates as diffs. Do not auto-sync them.
- Never commit credentials, auth state, caches, sessions, private vault
  content, personal email addresses, machine-specific absolute paths, or local
  tool registrations.

## Validation

Run `python3 scripts/validate_skills.py` and
`python3 -m unittest discover -s tests`. Also execute or syntax-check every new
helper script through its meaningful safe path. Validators prove structure and
syntax, not live credentials, external services, or host-app behavior.
