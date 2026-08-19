# Open questions

Everything the spec doesn't answer yet, in one place, with what it would take to close each one.

This file exists because the answers were previously scattered across two dry runs and a README status line, which meant that reading the repo told you less about its state than talking to the person who wrote it. Every question here came out of an actual run or an actual review, not from imagining what might go wrong.

If you have hit one of these in real use, that is the most valuable thing you can bring: open an issue with what happened. Use decides what v0.3 fixes.

---

## Answered in v0.2

**How do you phrase a ban so it doesn't just generate a new ambiguity?**
Answered by the `Instead:` field ([SPEC §3](SPEC.md#prohibitions-name-their-substitute-new-in-v02)). Both dry runs produced the same shape from unrelated projects: a ban settles one case and silently opens another. The field makes the substitute explicit, and `Instead: open` makes "we don't know yet" explicit too, which is the case that was actually causing the damage.

*Residual:* nothing enforces that the substitute is any good, and nothing stops `Instead: open` becoming a habit that defers every hard call. The linter's note is a reading of your log, not a check. It also can't tell a ban that closes a question from a ban that opens one — the heuristic reads the first sentence of the decision, which is a guess, and a good one only most of the time.

**How do you mark a perceptual file as partially stale?**
Answered by `status: partial` and `governed_by` on the manifest file entry ([SPEC §2](SPEC.md#status-and-governed_by-new-in-v02)). `examples/bright-start` was the case that forced it and is now the worked example of the fix.

*Residual:* `governed_by` takes one reference. A mood file overtaken in three places by three separate decisions can only name one of them, and the honest answer today is to name the one that matters most and let the agent read the rest of the log. If that turns out to bite in practice, the field becomes a list in v0.3 — which is an additive change, so it costs nothing to wait for evidence.

**Is there anything mechanical checking conformance?**
Yes, as of this version: `tools/lint_design_context.py`, with tests, run in CI over the template and every example. See [tools/README.md](tools/README.md) for what it checks and, more usefully, what it doesn't.

---

## Open

**Roles for the rest of the protocol family.**
The controlled role list covers `mood.md`, `vocab.md`, `voice.md`, `tokens.md` and `trace.md`. The [perceptual-protocols](https://github.com/Owl-Listener/perceptual-protocols) family has also released `motion.md`, `listen.md`/`sound.md`, `situation.md` and `critique.md`, and has `taste.md` planned. None of them can be listed in a manifest today, because `role` is a closed list and adding to it takes a spec revision.

They are not in v0.2 because a role name is a contract about where a file sits in the load order and how an agent should weigh it, and writing those contracts from the outside, without having run each protocol on a real project, is how you get a list of plausible words that nobody's tooling agrees on. *To close:* run each protocol on a project that has a `design-context/`, and propose the roles that survive.

**Where does `trace.md` belong in `load_order`?**
A trace describes what the product currently feels like. A mood describes what it should feel like. They are different kinds of claim, and if an agent reads them as peers it will average them, which is the worst available outcome. The current recommendation is last, after every intent file, read as description rather than instruction — but v0.2 does not mandate it, and "recommended" is thin protection against an agent that treats position in a list as unimportant. *To close:* a dry run where the trace and the mood disagree, to see what an agent actually does with it.

**What should an agent *do* about staleness, beyond saying so?**
`updated` dates make staleness detectable and `status` makes it declarable, but both need a human to have noticed first. Nothing detects that a mood file has drifted from the product; the bright-start conflict was found because someone set it up deliberately. *To close:* probably the trace loop — cold-read the product, compare to the mood, report the deltas — which would make staleness a thing you can run rather than a thing you must remember.

**Two settled decisions that quietly contradict each other.**
`load_order` resolves conflicts *between files*. Inside `decisions.md` there is no precedence rule except supersession, which requires someone to have noticed the reversal and written it down. A log with forty entries can hold a contradiction for months. The linter cannot help: it checks that entries are well formed, and "these two well-formed entries disagree" needs a reader. *To close:* possibly a periodic agent pass over the log looking for tension, proposing supersessions for a human to approve. Possibly nothing — this may just be what a design record is.

**Where does a reconstructed decision record its evidence?**
Surfaced by `examples/switchboard`, where four of nine entries were rebuilt from pull requests, an incident report and a channel argument rather than stated by a person. Those entries currently carry "reconstructed from PR #412" inside the `Because`, which makes the reason field do two jobs: why the decision holds, and where the claim came from. The two age differently — the reasoning can stay true long after the pull request is unreachable — and only one of them is what an agent needs when generalising. A `Source:` field would say it properly. *To close:* a second project that reconstructs a log and hits the same thing. One project's evidence is not enough to add a field that every future reader has to learn.

**Scope inside one repository.**
Every decision currently applies to the whole project. Real products have a marketing site whose voice is nothing like the product's, or a design system consumed by three apps that agree on tokens and nothing else. Options are a `scope:` field on entries, several `design-context/` directories with an inheritance rule, or a flat refusal to model it. *To close:* one real monorepo trying it and reporting what broke.

**What happens when `decisions.md` gets long.**
Append-only and load-everything are both correct at forty entries. At four hundred, one of them has to give, and compaction is exactly the operation this format was designed to make impossible. The likely answer is that `load_order` stops meaning "read all of it" and starts meaning "read the settled entries and the last N", with the full log always on disk. That is a real change and wants evidence first. *To close:* someone's log crossing two hundred entries. Nobody's has yet.

**Critique-protocol integration.**
`critique.md` shipped in the family after design-context v0.1 was written. Critique output is the most natural source of new decision entries there is — it is literally a record of judgements about a specific artefact — and there is currently no defined path from one to the other. *To close:* a role for `critique.md`, and a worked run of critique output becoming decision entries.

**Who else maintains this.**
One author, v0.2, no outside contributions yet. That is a real risk to anyone adopting the format, and it is not a risk a commit can fix. What it can do is make the project legible without its author: the spec is written to be implementable from the document alone, the linter is the executable half of that, the open questions are in this file instead of in someone's head, and the format is plain markdown in your own repository, which means the worst case if this project goes quiet is that you keep the files and lose the linter. *To close:* other people using it, and one of them disagreeing with me in public.

---

## Deliberately unanswered

Not gaps. Positions.

**Generating taste.** Nothing here will ever write a mood file from a product description, propose decisions the human didn't make, or fill in a `Because` on the designer's behalf. Curation stays human. A design memory that invents its own contents is not a memory.

**Richer formats.** No JSON, no database, no server, no per-agent dialect. Markdown in git diffs, survives its tooling, and can be read by a person in five years. Everything richer can be layered on top by whoever wants it, without changing what is written here.

**Enforcement beyond well-formedness.** The linter will not grow opinions about whether your decisions are good ones. There is no lint rule for taste and there should not be one.
