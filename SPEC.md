# design-context specification (v0.1)

The formal contract. If you're building tooling against design-context, build against this file.

## 1. The directory

A conforming project contains a directory named `design-context/` at the project root. All files are plain markdown, UTF-8. No other formats are permitted in v0.1: portability is the point.

Required files: `index.md`, `decisions.md`.
Optional files: `mood.md`, `vocab.md`, `voice.md`, `tokens.md`, `trace.md`, plus any future perceptual-protocol outputs.

A missing optional file is fine. A file the manifest doesn't list is invisible: agents read what `index.md` tells them to read, nothing else.

## 2. index.md — the manifest

The manifest has YAML frontmatter and a body. The frontmatter is machine-facing, the body is a short human-facing orientation.

```yaml
---
spec: design-context/v0.1
project: <project name>
updated: <ISO date of last change to any listed file>
files:
  - path: mood.md
    role: aesthetic-intent
    source: mood-protocol
    updated: <ISO date>
  - path: vocab.md
    role: vocabulary
    source: vocab-protocol
    updated: <ISO date>
  - path: decisions.md
    role: memory
    source: design-context
    updated: <ISO date>
load_order: [decisions.md, mood.md, vocab.md, voice.md, tokens.md]
---
```

Rules:

- `load_order` is authoritative. `decisions.md` always loads first: settled decisions outrank general intent. If a mood suggests soft shadows and a decision says "no shadows, decided 2026-08-02," the decision wins.
- `role` is from a small controlled list: `aesthetic-intent`, `vocabulary`, `verbal-identity`, `token-intent`, `trace`, `memory`. New roles require a spec revision.
- `updated` dates exist so agents (and future tooling) can flag staleness. An agent noticing that `mood.md` predates a major visual pivot should say so rather than silently obeying it.

The body of `index.md` is at most a few paragraphs: what this project is, one line per file on what it captures, anything an agent should know before generating. It is not a second mood board. Keep it lean; the manifest is a table of contents, not a summary.

## 3. decisions.md — the memory

An append-only log, newest entries at the top. Each entry:

```markdown
## 2026-08-09 — No rounded cards
**Decision:** Cards are square-cornered throughout.
**Because:** Rounded corners read as consumer-app friendly; this product's mood is "calm instrument, not companion."
**Supersedes:** none
**Status:** settled
```

Rules:

- `Status` is `settled`, `provisional`, or `superseded`. Agents treat `settled` as binding, `provisional` as a strong default worth confirming before large investments, `superseded` as historical context only.
- Entries are never edited or deleted, with a single exception: when an entry is reversed, its `Status` field flips to `superseded`. That flip is the only permitted modification to an existing entry, and the entry's text is left untouched. A reversal is a new entry whose `Supersedes` field names the old one. The history of changed minds is part of the record: it tells an agent (and a new team member) where the project's judgement has been tender.
- `Because` is required. A decision without a reason can't be applied to a case the decision didn't anticipate, and generalising to unanticipated cases is most of what we need agents to do well.

## 4. Agent behaviour

A conforming agent, at session start:

1. Reads `index.md`.
2. Loads files in `load_order`.
3. Treats `settled` decisions as constraints, perceptual files as intent, and flags conflicts between them to the human instead of resolving silently.

During a session, when the human makes a design decision (explicitly, "record that," or implicitly through repeated correction), the agent appends a properly formatted entry to `decisions.md` and updates the manifest's `updated` fields.

At session end (or on request), the agent offers a sweep: proposed entries for decisions made in conversation but not yet recorded. The human approves before anything is written. Curation stays human; that principle is inherited from the perceptual protocols and is not negotiable.

## 5. What this spec deliberately excludes

No JSON. No database. No server. No per-agent dialects. The whole bet is that plain markdown in git is the most durable, portable, inspectable memory substrate available, and that anything richer can be layered on later without breaking what exists.
