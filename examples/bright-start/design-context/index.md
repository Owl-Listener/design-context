---
spec: design-context/v0.2
project: Bright Start
updated: 2026-08-16
files:
  - path: decisions.md
    role: memory
    source: design-context
    updated: 2026-08-16
  - path: mood.md
    role: aesthetic-intent
    source: mood-protocol
    updated: 2026-06-12
    status: partial
    governed_by: 2026-07-30 — No celebration animations on completion
load_order: [decisions.md, mood.md]
---

# Design context for Bright Start

Bright Start is a reading app for children aged five to eight, used at home alongside a parent. Load the files above in order before generating or modifying any interface, copy, or visual output.

This example exists to test precedence. `mood.md` was written at kickoff in June and asks for visible celebration. A settled decision from July, taken after a usability round, bans exactly that. The two files disagree, on purpose. The six week gap between their `updated` dates is the signal that one of them has aged.

It is also the worked example of the v0.1 → v0.2 migration. The mood file's `status: partial` and `governed_by` above replaced a decision entry that had been doing that job in prose; the entry was superseded rather than deleted, which is what every reversal in this format looks like. See [MIGRATION.md](../../../MIGRATION.md) and the top two entries of `decisions.md`.

What each file captures:

- `decisions.md` — settled design decisions with reasons. Constraints, not suggestions. They outrank everything else here.
- `mood.md` — what this should feel like: references and anti-references. Written before the July research, marked `partial` in the manifest above, and still not revised. Its Rewarding and Kinetic qualities are read as a record of June's intent. Everything else in it stands.

If something you are about to generate conflicts with a settled decision or the mood, say so before proceeding. Do not resolve the conflict silently in either direction, including when precedence makes the answer obvious.
