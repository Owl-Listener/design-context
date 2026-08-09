---
spec: design-context/v0.1
project: Bright Start
updated: 2026-08-09
files:
  - path: decisions.md
    role: memory
    source: design-context
    updated: 2026-08-09
  - path: mood.md
    role: aesthetic-intent
    source: mood-protocol
    updated: 2026-06-12
load_order: [decisions.md, mood.md]
---

# Design context for Bright Start

Bright Start is a reading app for children aged five to eight, used at home alongside a parent. Load the files above in order before generating or modifying any interface, copy, or visual output.

This example exists to test precedence. `mood.md` was written at kickoff in June and asks for visible celebration. A settled decision from July, taken after a usability round, bans exactly that. The two files disagree, on purpose. The six week gap between their `updated` dates is the signal that one of them has aged.

What each file captures:

- `decisions.md` — settled design decisions with reasons. Constraints, not suggestions. They outrank everything else here.
- `mood.md` — what this should feel like: references and anti-references. Written before the July research and not yet revised.

If something you are about to generate conflicts with a settled decision or the mood, say so before proceeding. Do not resolve the conflict silently in either direction, including when precedence makes the answer obvious.
