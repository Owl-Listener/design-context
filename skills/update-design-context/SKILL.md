---
name: update-design-context
description: Record design decisions into the project's design-context memory. Use when the user says "record that", "remember this decision", "add that to design context", "don't let me forget this", when the user has corrected the same design choice more than once in a session, or at session end to sweep the conversation for unrecorded design decisions.
---

# Update design-context

You are maintaining the project's design memory: `design-context/decisions.md`. Your job is to make sure decisions made in conversation survive the session.

## When this skill fires

- **Explicitly:** the user says "record that" or similar about a design choice just made.
- **Implicitly:** the user has corrected the same thing twice or more this session (a colour, a corner radius, a tone of copy). Repeated correction is a decision the human hasn't noticed they've made. Offer to record it, don't record it silently.
- **At session end:** on request, sweep the conversation for design decisions that were made but not recorded, and propose entries.

## Rules (from the design-context SPEC, v0.1)

1. **Append-only, newest first.** Never edit or delete an existing entry. A reversal is a new entry whose Supersedes field names the old one; flip the old entry's Status to `superseded` (this status flip is the single permitted modification).
2. **Every entry needs a Because.** If the user gave no reason, ask for one in a single short question. The reason is what lets the decision generalise to cases nobody anticipated. If they truly can't articulate it, write "Because: not yet articulated, felt judgement" — honest, and a flag for later.
3. **Propose, then write.** Show the formatted entry and get a yes before appending. Curation stays human. For a session-end sweep, show all proposed entries at once as a list they can approve, trim, or reject.
4. **Status honestly.** `settled` only if the user is clearly done deciding. If there's any "let's try it for now" in their tone, it's `provisional`, and say that's what you're marking it.
5. **Housekeeping.** After appending, update the `updated` dates in `index.md` for `decisions.md` and the manifest itself.

## Entry format

```markdown
## YYYY-MM-DD — Short decision title
**Decision:** Stated so a future agent can apply it without asking.
**Because:** The reason, in the user's own words where possible.
**Supersedes:** none | date + title of the superseded entry
**Status:** settled | provisional
```

## Conflicts

If a new decision contradicts the mood file or an existing settled decision, name the conflict before recording: "this supersedes the square-corners decision from 2026-08-02, and it pulls against the 'calm instrument' line in mood.md, want me to note that tension in the entry?" Never resolve a conflict silently in either direction.

## Tone

Light touch. One question maximum per recording. The value of this skill is that it costs the user almost nothing in the moment and compounds forever.
