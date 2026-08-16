# Contributing

The most useful contributions, in order:

**Worked examples.** A real project's `design-context/` directory (anonymised is fine) is worth more than any spec change. Especially valuable: a `decisions.md` that has lived long enough to contain superseded entries, so people can see what changed minds look like in the format.

**Field reports.** You ran the harness with an agent for a week. What held? What did the agent ignore? Where did `load_order` produce the wrong precedence? Open an issue with the story. The spec is v0.1 and use decides what v0.2 fixes.

**Spec proposals.** [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) lists what's unresolved and what it would take to close each one — start there. Sketch the change and the case for it in an issue before writing a PR. Small and single-purpose beats comprehensive, and evidence from one real project beats a well-argued hypothetical.

## Before you open a PR

```
python3 tools/lint_design_context.py examples/* --strict
python3 tools/test_lint.py
```

Both run in CI. If you add a linter rule, add a case and a counterexample for it; if you add an example, it has to lint clean. Notes are not failures — a note is the linter reading your log, not a to-do list.

Changing the spec means changing four things together: `SPEC.md`, the linter, `MIGRATION.md`, and whichever example demonstrates the new behaviour. A spec change with no worked example is a proposal, not a version.

Two principles are not up for revision: output stays plain markdown, and curation stays human. Proposals that generate taste on the designer's behalf, or that move the format to JSON or a database, belong in a different project.

See the [perceptual-protocols](https://github.com/Owl-Listener/perceptual-protocols) family for the sibling formats this harness carries.
