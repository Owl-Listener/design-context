# Contributing

The most useful contributions, in order:

**Worked examples.** A real project's `design-context/` directory (anonymised is fine) is worth more than any spec change. Especially valuable: a `decisions.md` that has lived long enough to contain superseded entries, so people can see what changed minds look like in the format.

**Field reports.** You ran the harness with an agent for a week. What held? What did the agent ignore? Where did `load_order` produce the wrong precedence? Open an issue with the story. The spec is v0.1 and use decides what v0.2 fixes.

**Spec proposals.** New roles for the manifest, staleness behaviour, critique-protocol integration. Sketch the change and the case for it in an issue before writing a PR. Small and single-purpose beats comprehensive.

Two principles are not up for revision: output stays plain markdown, and curation stays human. Proposals that generate taste on the designer's behalf, or that move the format to JSON or a database, belong in a different project.

See the [perceptual-protocols](https://github.com/Owl-Listener/perceptual-protocols) family for the sibling formats this harness carries.
