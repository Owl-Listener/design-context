---
name: init-design-context
description: Set up a design-context directory for a project — the persistent design-intent harness any agent loads at session start. Works for a new project or for adopting an existing codebase that has design intent buried in it. Use when the user wants to initialise design context, set up design memory, adopt design context in an existing project, reconstruct the design decisions behind a product nobody documented, make a project remember design decisions, give agents persistent design intent, or says "init design context", "set up design context", or "make this project remember my design decisions".
---

# Initialise design-context

You are setting up the `design-context/` directory for this project: the files that let any agent, in any future session, start from the project's accumulated design intent instead of from zero.

## Principles (do not violate)

- **Human-curated, not AI-generated.** You are capturing the taste the designer already has, never inventing taste for them. Every file you write is built from their answers, their references, their words.
- **Sixty seconds to value.** Ask the minimum. A thin, honest design-context beats a thick, padded one. Files can grow later through use.
- **Markdown only.** Plain `.md`, portable, versionable. Follow the design-context SPEC (v0.2) for `index.md` and `decisions.md` formats exactly.

## Which path

Ask one question before anything else: **does this project already exist?**

A project with screens has intent in it, whether or not anyone can articulate it. A project without screens has intent only in the designer's head. Those need opposite orders of operation, and running the wrong one wastes everybody's time — the interview below produces shrugs when there is a four-year-old product sitting right there, and the archaeology below produces nothing at all when there isn't.

- **Nothing built yet, or a designer with a clear brief** → the greenfield steps.
- **An existing product, especially one older than its current team** → the brownfield steps.

## Greenfield steps

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

## Brownfield steps

For a product that already exists. Read first, ask last. The worked example is `examples/switchboard`.

The sixty-second promise does not hold here, and pretending otherwise produces a directory full of guesses. Adoption is closer to an hour — but most of it is your reading time, not theirs. Protect the human's twenty minutes by spending your own first.

1. **Cold read the product before you talk to anyone.** Run trace-protocol over three or four real screens with no brief, and write `trace.md`. This costs the team nothing and it is the only file a project like this can write honestly on day one. It is also what makes the conversation possible: people who cannot answer "what should this feel like" will react immediately to an accurate description of what it feels like now.

   Say clearly, in `index.md` and in the file, that a trace is description and never instruction. An agent that reads a trace as direction will faithfully reproduce every accident in the product.

2. **Do the archaeology.** Design decisions in an old project live in pull request arguments, incident reports, code comments, and one channel thread nobody can find. Reconstruct what you can and bring it as a list with its evidence attached. Write the evidence into the `Because` — the spec has no provenance field yet — so a reader in a year knows which entries are testimony and which are inference.

3. **Separate decisions from accidents.** This is the whole job, and getting it wrong is worse than doing nothing: recording an accident as a decision enshrines a mistake in the file agents treat as binding. The test that works is *if this were different, would anyone object?* Three near-identical greys have no objector; they are sediment, and they belong in a `provisional` cleanup entry that says which one to keep. A density nobody may touch has six objectors; that is a decision.

4. **Interview last, and only for what the artefacts could not answer.** By now the questions are specific enough to be answerable in twenty minutes. The useful ones are usually: is this deliberate or leftover? Is this direction or abandoned? Is anyone planning to change it? And the most valuable question in a brownfield project, which is not about looks at all: *what makes this tool good for the people who use it?* The answer to that is often the entry that protects the product from its next improvement.

5. **Record what is already right.** In greenfield, decisions steer. In brownfield, half of them protect. An agent let loose on an old internal tool will improve it toward the mean — more whitespace, softer corners, a component library — and every one of those changes is defensible in isolation. The entries that stop it have to exist before the first session, not after the first regression.

6. **Generate the directory.** `index.md` and `decisions.md` per SPEC, plus the `trace.md` you already have. Add `tokens.md` if the project has more than one stylesheet or more than one value for the same thing — in a codebase this age it earns its place faster than any other optional file, because "which grey is the real grey" is a question an agent asks on its first edit and cannot answer from the CSS. The manifest lists `trace.md` last in `load_order`.

7. **Write `mood.md` last, thin, and provisional.** Say in the provenance line where it came from and what it is a translation of. A confident mood file for a project with no designer is you inventing taste on someone's behalf, which is the one thing this format exists to prevent.

8. **Wire it in and prove it**, as in the greenfield steps. For the demonstration, use a protective decision rather than a steering one — restate the thing you will now *not* do. That is the part that surprises people, and it is what makes the directory feel worth keeping.

## Before you finish, either path

Run the linter if the repo has it, or read the spec against what you wrote if it doesn't:

```
python3 tools/lint_design_context.py .
```

Fix errors. Read the notes out loud to the user rather than acting on them — a note about a ban with no stated substitute is a question for them, not a task for you.

## Tone

Warm, brief, no ceremony. This should feel like a colleague setting up a shared notebook, not a configuration wizard.
