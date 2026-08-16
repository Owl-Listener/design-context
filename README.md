# design-context

> How to start a session where an agent is going to design something.

Before an agent generates a single component, page, or flow, it needs more than a design system to work from. A design system tells it what a button looks like but it doesn't tell it the mood you're going for, the vocabulary you'd use to describe the interface, the voice the copy should have, or the decisions you've already made that you don't want relitigated. That gap is easy to ignore when everything is a static screen in a deterministic system, and impossible to ignore once UI starts being hydrated or assembled on the fly, where there's no fixed layout for the agent to copy and it's making real interface judgement calls in the moment.

design-context is that setup, done once, before the session starts. One directory, `design-context/`, that holds your project's design intent in files any agent can read: the mood, the shared vocabulary, the voice, the token intent, and, crucially, the running log of what you've already decided. It loads at session start, before the agent generates anything. It updates as you critique. Git can diff your taste, and your agent stops starting from zero.

---

## How it works

```
your-project/
└── design-context/
    ├── index.md        ← the manifest: what's here, when to read it
    ├── mood.md         ← aesthetic intent (from mood-protocol)
    ├── vocab.md        ← shared aesthetic vocabulary (from vocab-protocol)
    ├── voice.md        ← verbal identity (from voice-protocol)
    ├── tokens.md       ← token intent annotations (from tokens-protocol)
    ├── trace.md        ← a cold read of what the product feels like now (from trace-protocol)
    └── decisions.md    ← the memory: every design decision, dated, with reasons
```

The agent reads `index.md` first. It tells the agent what exists, what order to read it in, and when each file was last touched. The perceptual files carry intent. `decisions.md` carries memory. Together they mean a session can begin where the last one ended, not at zero.

None of the individual formats are new. mood, vocab, voice, and tokens come from the existing protocols, this project doesn't replace them, it gives them a shared home and a load order. What's new is the manifest, the decision log, and the discipline of treating design intent as project infrastructure.

Only `index.md` and `decisions.md` are required, and only those two ship in the template: a mood file with nothing in it is worse than no mood file, because an agent will read it. [SPEC section 4](SPEC.md#4-the-optional-files) describes what each of the others looks like when it's filled, so you can tell whether one you already have will slot in without going and reading five other repositories.

## Quick start

Sixty seconds, no setup, the AI subscription you already have.

1. Copy the `template/design-context/` folder into your project root.
2. Open your agent and say: "Read design-context/index.md, then interview me to fill in the missing files." (Or install the `init-design-context` skill and it does this properly.)
3. Add one line to your CLAUDE.md, AGENTS.md, or cursor rules:

```
At the start of every session, read design-context/index.md and load the files it lists. Record design decisions in design-context/decisions.md as they happen.
```

That's it. From now on, every agent that can read your project can read your intent, and your decisions accumulate instead of evaporating.

## The decision log is the point

`decisions.md` is the file that attacks the forgetting problem directly. Every time you steer the agent, "no rounded cards," "warmer neutrals," "the empty state should feel like an invitation, not an apology," the decision gets recorded with a date and a reason. Next session, the agent reads it before it generates anything.

This turns critique from a conversation that evaporates into memory that compounds. Six weeks in, your `decisions.md` is the most honest design rationale document your project has, and you never sat down to write it.

## The skills

Two skills ship with this repo (`skills/`):

- **init-design-context** — generates the directory and fills it. Two paths: interview-first for a new project, and read-the-product-first for an existing one, where the intent is in the codebase and the pull request history rather than in anyone's head. For starting well, or starting late.
- **update-design-context** — invoked when a decision is made mid-session ("record that"), or at session end to sweep the conversation for decisions worth keeping. For not forgetting.

Both are plain SKILL.md files. Claude Code, Gemini CLI, Cursor, anywhere the skills format works.

## The examples

Three worked examples live in `examples/`, each with a filled `design-context/`, a screen, and a dry run reporting what held.

- **calm-ledger** — a personal finance app whose mood and decisions agree everywhere. The run tests whether a Because field generalises to cases the decision never explicitly mentioned.
- **bright-start** — a children's reading app whose mood and decisions genuinely conflict, because a usability round overturned the kickoff mood six weeks after it was written. The run tests whether an agent flags that conflict or resolves it silently.
- **switchboard** — a four year old internal dispatch tool with three stylesheets, no designer since 2024, and nobody left who remembers why it looks like this. The run tests adoption: what you can reconstruct from a product when there's no one to interview, and how to tell a decision apart from an accident that hardened into one.

The first two are greenfield, which is the easy case. switchboard is the common one.

The dry runs are the useful part. All three end with findings that became new entries in the example's own `decisions.md`, or in the spec. Two of bright-start's findings are why there's a v0.2.

## The linter

```
python3 tools/lint_design_context.py path/to/your-project
```

Checks that a `design-context/` directory says what the spec says it should: frontmatter parses, roles are real, `load_order` matches `files`, every listed file exists, every entry has a Because, entries run newest first, supersessions hang together in both directions. Python 3, standard library, no install, runs in CI here over the template and all three examples.

It checks that the record is well formed. Whether the record is *true* is a human's job and always will be. [tools/README.md](tools/README.md) has the full list of what it deliberately doesn't check.

## Relationship to the family

[perceptual-protocols](https://github.com/Owl-Listener/perceptual-protocols) defines the perceptual formats: mood, vocab, trace, and the planned critique and taste. design-context is the harness that carries them across sessions. If SKILL.md is the protocol for craft and the perceptual protocols are the format for intent, design-context is the memory that makes both persistent.

Procedural files tell the agent how to do the work. Perceptual files tell it what the work should feel like. The decision log tells it what you've already settled. An agent with all three starts to feel less like a tool you configure and more like a colleague who was here last week.

## Status

v0.2. The manifest format, the decision log format, both skills, the linter and three worked examples are usable today. v0.1 directories stay valid and migration is opt-in; [MIGRATION.md](MIGRATION.md) has the path and the versioning promise.

v0.2 answered two questions v0.1 left open: how to mark a perceptual file that has aged in part, and how to phrase a ban so it doesn't quietly generate the next ambiguity. Both came out of the dry runs rather than out of theory.

What's still not built: roles for the rest of the protocol family, a critique-protocol integration, any real account of what happens when a decision log gets long, and any evidence from a project that isn't mine. Those and the rest live in [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md), with what it would take to close each one. Build what's needed, ship it small, learn, keep going.

## License

MIT.

---

Built by [MC Dean](https://marieclairedean.substack.com), part of the [Owl-Listener](https://github.com/Owl-Listener) collection. If you make something with this, I want to hear what happens.
