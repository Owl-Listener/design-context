---
spec: design-context/v0.1
project: Calm Ledger
updated: 2026-08-09
files:
  - path: decisions.md
    role: memory
    source: design-context
    updated: 2026-08-09
  - path: mood.md
    role: aesthetic-intent
    source: mood-protocol
    updated: 2026-08-01
load_order: [decisions.md, mood.md]
---

# Design context for Calm Ledger

This directory is the project's design intent, readable by any agent. Load the files above in order before generating or modifying any interface, copy, or visual output.

Calm Ledger is a personal finance app for people who find money stressful. The design bet is that a finance tool can lower your heart rate instead of raising it.

This example stays on spec v0.1 on purpose. Nothing here needs anything v0.2 added, and the promise in [MIGRATION.md](../../../MIGRATION.md) is that a conforming directory doesn't stop conforming because the spec moved — an example that quietly upgraded itself would be a poor demonstration of that. The linter passes it clean and prints one note saying a newer version exists.

What each file captures:

- `decisions.md` — settled design decisions with reasons. Constraints, not suggestions. They outrank everything else here.
- `mood.md` — what this should feel like: references and anti-references.

If something you're about to generate conflicts with a settled decision or the mood, say so before proceeding.
