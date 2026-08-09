---
spec: design-context/v0.1
project: PROJECT_NAME
updated: YYYY-MM-DD
files:
  - path: decisions.md
    role: memory
    source: design-context
    updated: YYYY-MM-DD
  - path: mood.md
    role: aesthetic-intent
    source: mood-protocol
    updated: YYYY-MM-DD
  - path: vocab.md
    role: vocabulary
    source: vocab-protocol
    updated: YYYY-MM-DD
load_order: [decisions.md, mood.md, vocab.md]
---

# Design context for PROJECT_NAME

This directory is the project's design intent, readable by any agent. Load the files above in order before generating or modifying any interface, copy, or visual output.

One line on what this project is: WRITE_ME.

What each file captures:

- `decisions.md` — settled design decisions with reasons. These are constraints, not suggestions. They outrank everything else here.
- `mood.md` — the aesthetic intent: what this should feel like, references, and anti-references.
- `vocab.md` — the words this team uses for aesthetic qualities, and what they mean here.

If something you're about to generate conflicts with a settled decision or the mood, say so before proceeding. If a file seems stale relative to the current direction, flag it rather than silently obeying it.
