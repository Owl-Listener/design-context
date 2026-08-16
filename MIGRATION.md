# Migration

What happens to a `design-context/` directory when the spec moves.

## The promise

**A conforming directory does not stop conforming because the spec moved.** Your `design-context/` is a record of decisions your team actually made. A format change is not a reason to invalidate it, and a spec that makes you rewrite your history to keep using it has misunderstood what it is for.

Concretely, within the 0.x line:

1. **Additive only.** A new version may add optional fields and new rules for what you write next. It may not remove a field, rename one, or change what an existing field means.
2. **Old versions stay readable.** A tool built for the current spec reads every earlier version. The linter in this repo accepts v0.1 and v0.2 and will accept v0.1 for as long as this repo exists.
3. **Migration is opt-in.** Nothing expires. A directory that declares `spec: design-context/v0.1` in 2029 is a valid directory.
4. **The `spec:` field is the switch.** Fields introduced in v0.2 are errors in a directory that declares v0.1 — not because they would break anything, but because a manifest claiming v0.1 while using v0.2 fields lies to every tool that reads it. Bump the version in the same commit that starts using the fields.
5. **Migration never rewrites history.** `decisions.md` is append-only, and that outranks the spec. Migrating does not mean retrofitting new fields into old entries. New rules apply to what you write from the migration onwards.

Rule 5 is the one that matters most, and it is the reason migrating is cheap. Every migration touches `index.md`, which is a live manifest and rewritable, and leaves the log alone.

If a 1.0 ever needs a breaking change, it ships with a script that performs it and a version of this document that says exactly what it does to your files before it does it.

## v0.1 → v0.2

Ten minutes, and most of it is optional. Nothing here is required: a v0.1 directory works untouched.

### 1. Check that you conform to v0.1 first

```
python3 tools/lint_design_context.py path/to/your-project
```

Fix anything it calls an error before changing the version. Migrating a directory that was already drifting means you cannot tell which failures came from the move.

The most likely finding is that `load_order` and `files` disagree. v0.1 never said they had to match, so directories built from the v0.1 example often list three files and order five. Make them the same set.

### 2. Bump the version

```yaml
spec: design-context/v0.2
```

That is the whole required migration. Stop here and everything still works; you have simply opted into the new rules for what you write next.

### 3. Mark any perceptual file that has aged (optional)

If a decision has overtaken part of a mood, vocab or voice file — and if you have been recording decisions for more than a month or two, one has — say so in the manifest:

```yaml
  - path: mood.md
    role: aesthetic-intent
    source: mood-protocol
    updated: 2026-06-12
    status: partial
    governed_by: 2026-07-30 — No celebration animations
```

If you had recorded that staleness as a decision entry, the v0.1 workaround, that entry has now been replaced by a field. Do not delete it. Append a new entry that supersedes it and flip the old one's `Status` to `superseded`, which is how every reversal works. `examples/bright-start` does exactly this, and the diff is worth reading: [`decisions.md`](examples/bright-start/design-context/decisions.md), top two entries.

### 4. Start writing `Instead:` on prohibitions (optional, and going forward only)

New bans name their substitute, or record that the substitute is open. Old entries stay exactly as they are. The linter will emit notes on old prohibitions that lack the field; that is a reading of your log, not a to-do list. Notes never fail a run, including under `--strict`.

If one of those notes points at a ban whose substitute you have since settled in practice but never wrote down, the right move is a new entry recording the substitute, not an edit to the old one.

### 5. Re-lint

```
python3 tools/lint_design_context.py path/to/your-project --strict
```

## What migration will never ask you to do

- Rewrite or delete a decision entry.
- Re-run a protocol to regenerate a perceptual file in a new format. design-context does not own those formats and cannot change them; if `mood-protocol` revises `mood.md`, that migration is theirs and lives in their repo.
- Convert anything to JSON, YAML-beyond-the-frontmatter, or a database.
- Adopt a new optional file. Empty scaffolds were noise in v0.1 and are noise in v0.2.
