# design-context specification (v0.2)

The formal contract. If you're building tooling against design-context, build against this file.

v0.1 directories remain conforming. v0.2 is additive: it introduces two fields and one new rule, and changes nothing that already worked. [MIGRATION.md](MIGRATION.md) has the upgrade path and the versioning policy. `tools/lint_design_context.py` checks a directory against this document and accepts both versions.

## 1. The directory

A conforming project contains a directory named `design-context/` at the project root. All files are plain markdown, UTF-8. No other formats are permitted: portability is the point.

Required files: `index.md`, `decisions.md`.
Optional files: `mood.md`, `vocab.md`, `voice.md`, `tokens.md`, `trace.md`, plus any future perceptual-protocol outputs.

A missing optional file is fine. A file the manifest doesn't list is invisible: agents read what `index.md` tells them to read, nothing else. Section 4 describes what the optional files look like when they are there.

## 2. index.md — the manifest

The manifest has YAML frontmatter and a body. The frontmatter is machine-facing, the body is a short human-facing orientation.

```yaml
---
spec: design-context/v0.2
project: <project name>
updated: <ISO date of last change to any listed file>
files:
  - path: mood.md
    role: aesthetic-intent
    source: mood-protocol
    updated: <ISO date>
    status: partial
    governed_by: <ISO date> — <decision title>
  - path: vocab.md
    role: vocabulary
    source: vocab-protocol
    updated: <ISO date>
  - path: decisions.md
    role: memory
    source: design-context
    updated: <ISO date>
load_order: [decisions.md, mood.md, vocab.md]
---
```

Rules:

- `load_order` is authoritative, and names exactly the files that `files` lists — no more, no fewer. `decisions.md` always loads first: settled decisions outrank general intent. If a mood suggests soft shadows and a decision says "no shadows, decided 2026-08-02," the decision wins.
- `role` is from a small controlled list: `aesthetic-intent`, `vocabulary`, `verbal-identity`, `token-intent`, `trace`, `memory`. New roles require a spec revision. The perceptual-protocols family has released more formats than this list covers; see [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md).
- `updated` dates exist so agents (and tooling) can flag staleness. An agent noticing that `mood.md` predates a major visual pivot should say so rather than silently obeying it.
- `index.md` never lists itself. It is the table of contents, not an entry in it.

### status and governed_by (new in v0.2)

`status` is optional and applies to perceptual files only. Absent means `current`.

| value | meaning |
| --- | --- |
| `current` | the file says what the project still means. The default. |
| `partial` | parts of this file have been overtaken. The rest stands. |
| `superseded` | the whole file is history. Read it to understand where the project has been, not to decide anything. |

`partial` and `superseded` require `governed_by`, naming the `decisions.md` entry that governs the overtaken part, in the form `YYYY-MM-DD — Title`. A status without that pointer is a shrug; the pointer is what makes it actionable. `decisions.md` itself cannot carry a status, because its entries carry their own.

This exists because perceptual files age unevenly. A mood written at kickoff is rarely wrong so much as wrong in two places, and before v0.2 there was nowhere to say that. The workaround was a decision entry pointing back at the file, which worked and read like a workaround. Now the manifest says it where the agent is already looking.

An agent reading `status: partial` loads the file, applies the named decision to the part it governs, and treats the rest as current. It says which parts it set aside and why. It does not silently skip the file, and it does not silently obey it.

### The frontmatter subset

The frontmatter is a restricted subset of YAML, so that a conformance checker can be written in any language in an afternoon:

- top-level `key: value` scalars
- one top-level block sequence (`files`), whose items are flat mappings of scalars
- flow sequences of scalars on one line (`load_order: [a.md, b.md]`)
- `#` comments on their own line, spaces for indentation, optional single or double quotes around scalars

Anchors, nested mappings, multi-line scalars, tabs and everything else are out. If your manifest needs them, the manifest is doing too much.

### The body

At most a few paragraphs: what this project is, one line per file on what it captures, anything an agent should know before generating. It is not a second mood board. Keep it lean; the manifest is a table of contents, not a summary.

## 3. decisions.md — the memory

An append-only log, newest entries at the top. Each entry:

```markdown
## 2026-08-09 — No rounded cards
**Decision:** Cards are square-cornered throughout.
**Because:** Rounded corners read as consumer-app friendly; this product's mood is "calm instrument, not companion."
**Instead:** Softness comes from the warm paper background and the type, not from the corner radius.
**Supersedes:** none
**Status:** settled
```

`Decision`, `Because`, `Supersedes` and `Status` are required. `Instead` is optional in general and expected for prohibitions; see below.

Rules:

- `Status` is `settled`, `provisional`, or `superseded`. Agents treat `settled` as binding, `provisional` as a strong default worth confirming before large investments, `superseded` as historical context only.
- Entries are never edited or deleted, with a single exception: when an entry is reversed, its `Status` field flips to `superseded`. That flip is the only permitted modification to an existing entry, and the entry's text is left untouched. A reversal is a new entry whose `Supersedes` field names the old one. The history of changed minds is part of the record: it tells an agent (and a new team member) where the project's judgement has been tender.
- The date and title together are how an entry is referenced, so no two entries share both.
- `Because` is required. A decision without a reason can't be applied to a case the decision didn't anticipate, and generalising to unanticipated cases is most of what we need agents to do well.

### Prohibitions name their substitute (new in v0.2)

A decision that bans something says what happens instead, in an `Instead:` field.

Both dry runs in `examples/` hit this from different directions. "No celebration animations" left "so how do we mark finishing at all" open, and the next session invented an answer. "Red is for errors only" left the colour of positive amounts open, and the next session invented that too. Two unrelated projects, same shape: a ban settles one case and opens another, and the opened one gets filled in silently by whoever is next at the keyboard.

So: when you ban something the design still needs a form for, name the form.

```markdown
**Instead:** Completion opens a static full-bleed illustrated page in the saturated palette, carrying one line of warm copy.
```

When you genuinely don't know yet, say that, in the field:

```markdown
**Instead:** open — no one has hit the case yet. Decide it when it comes up and record it here.
```

That is not a cop-out, it is the whole point. The failure mode isn't a ban with an open substitute; it's a ban whose substitute *looks* settled because nobody wrote down that it wasn't. `Instead: open` tells the next agent it is allowed to propose, and must ask. A missing `Instead` tells it nothing, so it guesses and moves on.

A prohibition without any `Instead` is still conforming. The linter emits a note rather than an error, because sometimes a ban really does close the question, and because entries are append-only: the rule applies to what you write from here, and nobody should be going back to retrofit the field into old entries.

## 4. The optional files

design-context does not define these formats and must not fork them. Each belongs to a protocol in the [perceptual-protocols](https://github.com/Owl-Listener/perceptual-protocols) family, and that repo is authoritative for the shape of each file, the prompt that produces it, and its own versioning.

What follows is the shape you can expect, so that this repo can be evaluated without opening five others, and so you can tell at a glance whether a file you already have will slot in. The filled examples in `examples/` are the other half of that: `switchboard` ships a `trace.md`, a `mood.md` and a `tokens.md`, all short.

**`mood.md`** — role `aesthetic-intent`, source `mood-protocol`. What the thing should feel like, and what it should never feel like. The protocol's full format runs to sections for essence, colour, typography, space, texture, emotional register, principles, anti-references and a closing paragraph of agent instructions. The short form the examples here use keeps the load small:

```markdown
# Mood — <project>

*Produced with mood-protocol v0.1 from <source>, <date>.*

## In three lines
...

## Qualities
- **Steady** — nothing pulses, bounces, or urges.

## References
- Muji stationery: utility with softness.

## Anti-references
- NOT a trading terminal: no dense grids, no red/green semantics.
```

The anti-references carry at least as much information as the positives, and are the part agents most reliably act on. Do not drop them to save room.

**`vocab.md`** — role `vocabulary`, source `vocab-protocol`. The shared terms, so that "warmth" means one thing across the project and across sessions. The protocol ships ten canonical terms; a project adds its own. Each term gets a definition, a paragraph, two or three references and two or three anti-references. Worth having as soon as two people are giving the agent feedback in the same week.

**`voice.md`** — role `verbal-identity`, source `voice-protocol`. Five sections: personality (three to five descriptors, each with a clarifying contrast), tonal range (how the voice shifts by context), mechanics (specific, enforceable writing rules), vocabulary (words to use, words to avoid, brand terms), reference (one example done right, one done wrong). Enforceable rules, not adjectives: "sentences under twenty words, never an exclamation mark" beats "friendly but professional".

**`tokens.md`** — role `token-intent`, source `tokens-protocol`. An annotation layer over the token system you already have, not a copy of it. Sections for colour, typography, spacing, elevation, motion, radius, and a source line pointing at where the real values live. Each section records what a token is *for* and what it is *not* for, which is the part your CSS custom properties cannot say.

**`trace.md`** — role `trace`, source `trace-protocol`. The output of cold-reading what a product currently looks like, with the brief hidden. Same shape as `mood.md`. Its use here is comparison: put the trace of what you built next to the mood of what you meant and read them quality by quality. It is also, in practice, the first file a pre-existing project can honestly write, because the product is right there to be read and the intent is scattered across four years of pull requests. See `examples/switchboard`.

Every one of these files opens with a provenance line: what produced it, from what, on what date. That line is how a human reading the directory a year later knows whether to trust it, and it is the human-readable twin of the manifest's `updated`.

## 5. Agent behaviour

A conforming agent, at session start:

1. Reads `index.md`.
2. Loads files in `load_order`.
3. Treats `settled` decisions as constraints, perceptual files as intent, and flags conflicts between them to the human instead of resolving silently.
4. Respects `status`: a `partial` file is applied except where the `governed_by` decision overrides it, and the agent says which parts it set aside.

During a session, when the human makes a design decision (explicitly, "record that," or implicitly through repeated correction), the agent appends a properly formatted entry to `decisions.md` and updates the manifest's `updated` fields.

When a new decision overtakes part of a perceptual file, the agent offers to set that file's `status` and `governed_by` at the same time. Recording the decision and leaving the mood file silently wrong is half a job: the next session will hit the same wall.

At session end (or on request), the agent offers a sweep: proposed entries for decisions made in conversation but not yet recorded. The human approves before anything is written. Curation stays human; that principle is inherited from the perceptual protocols and is not negotiable.

## 6. Conformance

A directory conforms if it satisfies sections 1 to 3. `tools/lint_design_context.py` checks that mechanically, exits non-zero on failure, and is the reference implementation of everything in those sections that can be checked without judgement.

Nothing in section 5 is machine-checkable, and no linter will ever tell you whether a `Because` is a real reason or a shrug in a suit. Conformance is the floor.

## 7. What this spec deliberately excludes

No JSON. No database. No server. No per-agent dialects. The whole bet is that plain markdown in git is the most durable, portable, inspectable memory substrate available, and that anything richer can be layered on later without breaking what exists.

## 8. Changes in v0.2

- `status` and `governed_by` on manifest file entries, for perceptual files that have aged in part (§2).
- `Instead:` on decision entries, expected where a decision is a prohibition (§3).
- The frontmatter YAML subset is written down, so checkers can be written against it (§2).
- The shape of each optional file is described here rather than only in the sibling repos (§4).
- `load_order` must match `files` exactly. v0.1 said `load_order` was authoritative but never said the two had to agree; the v0.1 example in this file listed three files and ordered five, which is exactly the ambiguity that produced the rule.
- Agent behaviour gains the staleness step (§5).

Unresolved questions, including the ones these changes did not answer, live in [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md).
