---
spec: design-context/v0.1
project: PROJECT_NAME
updated: YYYY-MM-DD
files:
  - path: decisions.md
    role: memory
    source: design-context
    updated: YYYY-MM-DD
load_order: [decisions.md]
---

# Design context for PROJECT_NAME

This directory is the project's design intent, readable by any agent. Load the files above in order before generating or modifying any interface, copy, or visual output.

One line on what this project is: WRITE_ME.

What each file captures:

- `decisions.md` — settled design decisions with reasons. These are constraints, not suggestions. They outrank everything else here.

<!-- Add a file to the frontmatter and to the list above as you create it, never before.
A manifest entry for a file that isn't there sends the agent looking for something it
cannot read, and the spec has no answer for what it should do then.

    path: mood.md      role: aesthetic-intent    source: mood-protocol
    path: vocab.md     role: vocabulary          source: vocab-protocol
    path: voice.md     role: verbal-identity     source: voice-protocol
    path: tokens.md    role: token-intent        source: tokens-protocol

decisions.md always stays first in load_order. Add the rest after it, in the order above.
Only create a file you have real content for. Empty scaffolds are noise.
-->

If something you're about to generate conflicts with a settled decision or the mood, say so before proceeding. If a file seems stale relative to the current direction, flag it rather than silently obeying it.
