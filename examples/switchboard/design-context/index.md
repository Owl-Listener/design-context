---
spec: design-context/v0.2
project: Switchboard
updated: 2026-08-16
files:
  - path: decisions.md
    role: memory
    source: design-context
    updated: 2026-08-16
  - path: mood.md
    role: aesthetic-intent
    source: mood-protocol
    updated: 2026-08-16
  - path: tokens.md
    role: token-intent
    source: tokens-protocol
    updated: 2026-08-16
  - path: trace.md
    role: trace
    source: trace-protocol
    updated: 2026-08-14
    status: partial
    governed_by: 2026-08-16 — Red means undo-in-progress and nothing else
load_order: [decisions.md, mood.md, tokens.md, trace.md]
---

# Design context for Switchboard

Switchboard is the internal tool our dispatch coordinators use to move drivers between routes. Four years old, three visual generations deep, no designer since 2024. Six coordinators use it for seven hours a day and it is the fastest tool any of them has ever used, which is not a compliment anyone has paid it in writing before now.

This example exists because both of the other examples in this repo are greenfield, and greenfield is the easy case. Here there was no moodboard, no brand, and nobody to interview about original intent, because the people who had it have left. Everything in this directory was either reconstructed from the product and the pull request history, or decided for the first time during a forty-minute adoption session on 2026-08-16.

What each file captures:

- `decisions.md` — settled design decisions with reasons. Constraints, not suggestions. Four were decided during adoption; four were reconstructed from arguments already had, and say so in their Because; one is a supersession found in the archaeology.
- `mood.md` — what this should feel like. Thin and provisional. It came out of one conversation, not a moodboard, and it will be wrong in places until we sit with a coordinator through a shift.
- `tokens.md` — what the existing tokens are for, across three stylesheets that disagree. This is the file that earns its place fastest in a project this age.
- `trace.md` — a cold read of what Switchboard currently feels like, taken before any of the above existed. Marked `partial`: the colour section already describes a product that changed the day after it was written.

Read `trace.md` as description, never as instruction. It is the record of what four years produced, including the parts we are fixing.

If something you are about to generate conflicts with a settled decision, the mood, or the token intent, say so before proceeding. In this project the most likely conflict is the least obvious one: the board is deliberately dense, and almost every instinct about improving it is wrong here.
