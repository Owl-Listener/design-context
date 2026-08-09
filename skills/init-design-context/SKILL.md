---
name: init-design-context
description: Set up a design-context directory for a project — the persistent design-intent harness any agent loads at session start. Use when the user wants to initialise design context, set up design memory, make a project remember design decisions, give agents persistent design intent, or says "init design context", "set up design context", or "make this project remember my design decisions".
---

# Initialise design-context

You are setting up the `design-context/` directory for this project: the files that let any agent, in any future session, start from the project's accumulated design intent instead of from zero.

## Principles (do not violate)

- **Human-curated, not AI-generated.** You are capturing the taste the designer already has, never inventing taste for them. Every file you write is built from their answers, their references, their words.
- **Sixty seconds to value.** Ask the minimum. A thin, honest design-context beats a thick, padded one. Files can grow later through use.
- **Markdown only.** Plain `.md`, portable, versionable. Follow the design-context SPEC (v0.1) for `index.md` and `decisions.md` formats exactly.

## Steps

1. **Look before asking.** Scan the project: existing styles, tokens, README, any current `mood.md` or brand files. Summarise what you can infer about the design direction in three or four sentences and show the user, so the interview starts from evidence rather than a blank page.

2. **Interview, briefly.** Ask only what you cannot infer, in one batch, not a drip:
   - What should this feel like? (three adjectives, or a reference: "like X, never like Y")
   - Anti-references: what should this never feel like? These carry as much information as the positives.
   - Any decisions already settled that agents keep getting wrong?
   - Do they have a moodboard? If yes, ask them to share a screenshot and apply the mood-protocol prompt to produce `mood.md`. If no, write a minimal `mood.md` from their adjectives and references, marked as provisional.

3. **Generate the directory.** Create `design-context/` at the project root:
   - `index.md` — manifest per SPEC, listing only files that actually exist, with today's date and correct `load_order` (decisions first, always).
   - `decisions.md` — seeded with any already-settled decisions from the interview, properly formatted with Because and Status fields.
   - `mood.md` — from the moodboard or the interview, including anti-references.
   - Only create `vocab.md`, `voice.md`, or `tokens.md` if the interview surfaced real content for them. Empty scaffolds are noise.

4. **Wire it in.** Add the session-start instruction to the project's agent config (CLAUDE.md, AGENTS.md, or equivalent — create it if absent):

   > At the start of every session, read design-context/index.md and load the files it lists in load_order. Treat settled decisions as constraints. Record new design decisions in design-context/decisions.md as they happen.

5. **Prove it works.** End by demonstrating the loop once: restate one of their settled decisions back to them as you would apply it ("so if I'm generating a card component in this project, it gets square corners, because the mood is calm instrument, not companion"). This shows the memory is live and gives them the feel of what future sessions will be like.

## Tone

Warm, brief, no ceremony. This should feel like a colleague setting up a shared notebook, not a configuration wizard.
