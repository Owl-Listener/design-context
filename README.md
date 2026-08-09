# design-context

> How to start a session where an agent is going to design something.

Before an agent generates a single component, page, or flow, it needs more than a design system to work from. A design system tells it what a button looks like but it doesn't tell it the mood you're going for, the vocabulary you'd use to describe the interface, the voice the copy should have, or the decisions you've already made that you don't want relitigated. That gap is easy to ignore when everything is a static screen in a deterministic system, and impossible to ignore once UI starts being hydrated or assembled on the fly, where there's no fixed layout for the agent to copy and it's making real interface judgment calls in the moment.

design-context is that setup, done once, before the session starts. One directory, design-context/, that holds your project's design intent in files any agent can read: the mood, the shared vocabulary, the voice, the token intent, and, crucially, the running log of what you've already decided. It loads at session start, before the agent generates anything. It updates as you critique. Git can diff your taste, and your agent stops starting from zero.

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
    └── decisions.md    ← the memory: every design decision, dated, with reasons
```

The agent reads `index.md` first. It tells the agent what exists, what order to read it in, and when each file was last touched. The perceptual files carry intent. `decisions.md` carries memory. Together they mean a session can begin where the last one ended, not at zero.

None of the individual formats are new. mood, vocab, voice, and tokens come from the existing protocols, this project doesn't replace them, it gives them a shared home and a load order. What's new is the manifest, the decision log, and the discipline of treating design intent as project infrastructure.

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

- **init-design-context** — interviews you about the project, generates the directory, and runs the mood and vocab protocols to fill it. For starting well.
- **update-design-context** — invoked when a decision is made mid-session ("record that"), or at session end to sweep the conversation for decisions worth keeping. For not forgetting.

Both are plain SKILL.md files. Claude Code, Gemini CLI, Cursor, anywhere the skills format works.

## The examples

Two worked examples live in `examples/`, each with a filled `design-context/`, a screen built from it, and a dry run reporting what held.

- **calm-ledger** — a personal finance app whose mood and decisions agree everywhere. The run tests whether a Because field generalises to cases the decision never explicitly mentioned.
- **bright-start** — a children's reading app whose mood and decisions genuinely conflict, because a usability round overturned the kickoff mood six weeks after it was written. The run tests whether an agent flags that conflict or resolves it silently.

The dry runs are the useful part. Both end with findings that became new entries in the example's own `decisions.md`, which is the loop this repo is arguing for.

## Relationship to the family

[perceptual-protocols](https://github.com/Owl-Listener/perceptual-protocols) defines the perceptual formats: mood, vocab, trace, and the planned critique and taste. design-context is the harness that carries them across sessions. If SKILL.md is the protocol for craft and the perceptual protocols are the format for intent, design-context is the memory that makes both persistent.

Procedural files tell the agent how to do the work. Perceptual files tell it what the work should feel like. The decision log tells it what you've already settled. An agent with all three starts to feel less like a tool you configure and more like a colleague who was here last week.

## Status

v0.1. The manifest format, the decision log format, and both skills are usable today. What's not yet built: staleness warnings, a critique-protocol integration once that protocol ships, and worked examples from real projects. Build what's needed, ship it small, learn, keep going.

## License

MIT.

---

Built by [MC Dean](https://marieclairedean.substack.com), part of the [Owl-Listener](https://github.com/Owl-Listener) collection. If you make something with this, I want to hear what happens.
