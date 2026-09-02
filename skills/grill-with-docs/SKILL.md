---
name: grill-with-docs
description: Run a relentless interview that sharpens a plan while creating its glossary and selective ADRs. Use only when the user invokes `$grill-with-docs` or explicitly asks for this workflow.
license: MIT; see LICENSE.txt
---

# Grill with Docs

Stress-test a plan or design while recording the vocabulary and durable
decisions that emerge. This skill is self-contained; do not require separately
installed `grilling` or `domain-modeling` skills.

Before starting, read:

- [references/grilling.md](references/grilling.md) for the round-based design
  tree and questioning discipline.
- [references/domain-modeling.md](references/domain-modeling.md) for glossary,
  scenario, code-cross-check, and ADR rules.

Apply both references together. Inspect the repository before asking questions
whose answers are already available in files, configuration, history, or tools.
Ask the current decision frontier, include a recommended answer for each
question, and wait for the user before advancing dependent branches.

As terms become settled, update the appropriate `CONTEXT.md` immediately. Add
an ADR only when the decision is hard to reverse, surprising without context,
and the result of a real trade-off. Do not implement the plan during this
skill. Finish when the decision frontier is empty and the user confirms the
shared understanding.
