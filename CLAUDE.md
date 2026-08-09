# CLAUDE.md — design-context

## What this project is

design-context is a persistent design-intent harness: one `design-context/` directory per project, holding perceptual files (mood, vocab, voice, tokens) and an append-only decision log, loaded by any agent at session start. It attacks the "agents forget design intent" problem. Read `README.md` for the pitch and `SPEC.md` for the formal contract before changing anything.

This repo is part of the Owl-Listener collection (github.com/Owl-Listener) and a sibling of perceptual-protocols, which defines the mood/vocab/trace formats this harness carries.

## Current state (v0.1, complete)

- `README.md`, `SPEC.md`, `LICENSE` (MIT), `CONTRIBUTING.md` — written and final for v0.1.
- `skills/init-design-context/` and `skills/update-design-context/` — both SKILL.md files written, not yet tested in a real Claude Code session.
- `template/design-context/` — the copy-in starter.
- `examples/calm-ledger/` — worked example with a filled design-context, a demo screen (`demo/home.html`), and a conformance report (`demo/DRY-RUN.md`).

## Non-negotiable principles

These are settled. Do not propose changes to them:

1. Output is plain markdown, always. No JSON, no database, no server.
2. Curation stays human. Skills propose; the human approves before anything is written to `decisions.md`.
3. Sixty seconds to value. The prompt-and-template path must work with zero setup; scripts are convenience, never the canonical path.
4. `decisions.md` is append-only and loads first; settled decisions outrank mood.

## Writing style for any docs you touch

UK spelling. No em dashes (use commas). No italics, no all caps. Warm, plain, first person where natural. Short claim, then expansion. Never describe AI as "just a tool". Match the register of the existing README.

## Backlog (in order)

1. **Publish.** Init git, sensible .gitignore (macOS junk: .DS_Store), initial commit, create the public repo `Owl-Listener/design-context` on GitHub, push. Add topics: design, ai, ai-agents, design-context, agent-skills, design-systems.
2. **Test the skills for real.** Install both skills into this Claude Code environment, create a scratch project, run init-design-context end to end (interview MC properly, keep it brief), then make two or three design decisions in conversation and verify update-design-context records them per SPEC. Fix whatever the test breaks.
3. **The conflict example.** DRY-RUN.md finding 1: build a second example where mood and decisions genuinely conflict (e.g. a playful mood against a no-celebration decision) and verify an agent flags the conflict rather than silently resolving it. Document the result the way DRY-RUN.md does.
4. **Tighten the dry-run findings.** Findings 2 and 3 in `examples/calm-ledger/demo/DRY-RUN.md`: record the glyph choice and the positive-money colour as new provisional entries in the example's decisions.md, dated today, so the example demonstrates the update loop.
5. **Cross-link.** Once published, PR a link into the perceptual-protocols README ("the harness that carries these across sessions") and add design-context to the Owl-Listener profile README under a sensible section. Ask MC before opening anything public-facing.

Work the backlog top to bottom. Ask MC before anything irreversible: repo creation, pushes to existing repos, anything public.
