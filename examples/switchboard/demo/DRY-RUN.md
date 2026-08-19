# Dry run — 2026-08-16

Two sessions, not one. The other examples in this repo start from nothing and interview a designer. This one starts from a four-year-old internal tool with no designer, no moodboard, and no living memory of why most of it looks the way it does, which is the harder case and much the more common one.

**Session one: adoption.** Forty minutes, agent plus the two engineers who maintain Switchboard plus one coordinator. Produced the `design-context/` directory.

**Session two: the first change.** One brief — "red is doing four jobs on this board, fix it" — run with the directory loaded. Produced `demo/home.html`.

## Session one: what adoption actually looked like

The `init-design-context` interview does not survive contact with a project like this. Half its questions have no one to answer them. "What should this feel like?" produced a shrug and then, from the coordinator, "fast, I suppose", which is true and which no amount of follow-up would have turned into a mood file.

What worked was inverting the order: read the product first, ask second.

**1. Cold read before conversation (40 minutes of agent time, none of anyone else's).** The agent ran trace-protocol over three screens with no brief and produced `trace.md`. This is the file a brownfield project can write honestly on day one, because the product is right there and the intent is not. It is also the only artefact that got an unprompted reaction: the "red when it's busy" line in the Qualities section is a coordinator's own phrase, quoted back, and it is what made the colour problem discussable. Nobody had been able to name it before, because everybody had stopped seeing it.

**2. Archaeology, with the trace as the map.** Four decisions came out of pull requests, one incident report and one long channel argument. The reconstructed ones say so in their `Because`, along with what evidence they came from, because someone reading this log in a year needs to know which entries are testimony and which are inference.

**3. The interview, narrowed to what the artefacts could not answer.** By this point the questions were specific enough to be answerable: is the density deliberate? Is the 2024 refresh a direction or a leftover? Is anyone going to redesign this? Twenty minutes, three answers, three of the most useful entries in the log.

**4. The mood file last, and thin.** `mood.md` is three qualities and a warning that it is a translation of things people said about work, not about looks. It is marked provisional and it will be wrong somewhere. Writing a confident mood file for a project with no designer would have been inventing taste on someone's behalf, which is the one thing this repo says not to do.

## What the log had to hold that a greenfield log does not

**Decisions that record what is already right.** The dense-board entry is the most valuable thing in the directory and it changes nothing about the product. Without it, session two's first instinct was to add vertical padding while it was in there — a sincere, small, plausible improvement that would have cost the board eight rows. In greenfield, decisions are steering. In brownfield, half of them are protection.

**The difference between a decision and an accident.** Three greys within four hex points of each other are not a decision. Nobody chose them, nobody would defend them, and recording them as intent would have enshrined a mistake in the file that agents treat as binding. The test that worked: *if this were different, would anyone object?* The density has six objectors. The greys have none, so they went in as a provisional cleanup entry that tells an agent which grey to keep, rather than as a decision to preserve all three.

**A reversal nobody had written down.** The filters moved from a sidebar to a toolbar in 2024 and two other screens never got the memo. Recorded as a supersession — the 2025 entry naming the 2024 one, the old entry's Status flipped and its text left alone — which is what tells the next session those two screens are leftovers rather than the standard. That pair was reconstructed entirely from commits; neither decision was ever stated anywhere by a person.

## Session two: the change

The brief was the red audit. With the directory loaded, the agent applied the new colour decision, moved late routes to the amber left border and unavailable drivers to an outlined pill, and left everything else alone. `demo/home.html` is the result: the same board, one colour doing one job.

Three things about how it went.

**The `Instead:` field did the work.** "Red is not used for row status, overdue flags, or validation errors" would have produced three inventions. The field named all three substitutes, and the agent implemented them rather than choosing. This is the v0.2 rule paying for itself on its first real use, in a project where the substitutes were the entire content of the change.

**The trace nearly caused the mistake it was written to prevent.** Early in the session the agent cited the trace's "red-saturated" quality as though it were direction. It caught itself, because `index.md` says in as many words that the trace is description and not instruction, and because the trace's own `status: partial` names the decision that overrides it. Both of those were needed. Precedence alone would not have been enough: a trace does not read like a stale mood, it reads like evidence.

**The restraint held.** No whitespace added, no cards, no component library, no tidying of the two Okonkwos into initials. The redesign entry and the density entry are both phrased as protection, and both were cited unprompted.

## What the run surfaced

1. **Reconstructed entries have nowhere to put their provenance.** "Reconstructed from PR #412" is currently in the `Because`, which means the reason field is carrying two jobs: why the decision holds, and where the claim came from. They are different things, and they age differently — the reasoning may stay true after the evidence is deleted. A `Source:` field would say it properly. Added to [OPEN-QUESTIONS.md](../../../OPEN-QUESTIONS.md); not worth a spec change on one project's evidence.

2. **`init-design-context` needed a second path, and now has one.** The interview-first flow assumes an intent that exists somewhere in a person. The brownfield flow is read, reconstruct, then ask what's left, and the skill now says so.

3. **A trace goes stale faster than a mood.** This one was accurate for two days. That is not a flaw: a trace is a photograph, and the value is in the comparison, not the currency. But it means `status: partial` is going to be load-bearing on trace files specifically, and it means a project should expect to re-run the trace rather than to maintain it.

4. **The density decision would not have been recorded by any process that asks about aesthetics.** It came out of asking why the tool is fast. The most important entry in this directory is not a design decision in the sense anyone would recognise; it is an operational fact about how six people work, written down where an agent will read it before it touches the CSS.

**Recorded 2026-08-16.** Finding 1 is now an open question. Finding 2 is now in the skill.
