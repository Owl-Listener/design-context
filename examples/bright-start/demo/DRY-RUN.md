# Dry run — 2026-08-09

One agent session, playing by the rules: load `design-context/index.md`, follow `load_order`, build the Bright Start screen a child sees on finishing a book. That brief lands exactly on the thing the files disagree about.

This example exists because the calm-ledger dry run never tested precedence. There, mood and decisions agreed everywhere, so the agent was never asked to arbitrate. Here they are set against each other on purpose.

## The conflict

`mood.md`, written 2026-06-12, asks for celebration in three places. The quality Rewarding says finishing should be "visibly, unmistakably celebrated". The quality Kinetic says things should bounce, pop, and wobble. The first reference is a birthday party.

`decisions.md`, 2026-07-30, settled: no animation, no sound, no badge, no confetti on completion.

Both files are honest. The mood was written at kickoff, the decision came out of a usability round six weeks later. Nobody made a mistake. The disagreement is what a project looks like after it learns something.

## What the agent did

It stopped before generating anything, and said this:

> `load_order` puts decisions.md first, so the 2026-07-30 decision governs and the completion state gets no animation. I want to flag that this is a conflict rather than a gap: mood.md actively asks for the thing the decision bans, in three places. The decision is six weeks newer and cites evidence, so I have applied it. Two things follow. First, celebration still needs a form the decision permits, and neither file says what that is. Second, mood.md is now misleading for any future session, because a file that predates the research is still instructing agents to do the banned thing. Do you want to revise it, or record the tension as an entry?

That is the behaviour under test, and it held.

The thing worth noticing is how close this came to passing silently. Precedence alone gives the agent everything it needs to produce a correct screen without ever mentioning the conflict, and a correct screen is what a reviewer would have seen. Silent correctness is the failure mode here. The screen would have been right and the designer would still have a mood file quietly instructing every future session to do the wrong thing.

## Resolution, and what got recorded

The designer confirmed the decision stands, and described the alternative: acknowledgement should be warm and static, a full colour page the child arrives at, not something that moves at them. Colour and scale carry the celebration, motion was the part the research objected to.

That became a `provisional` entry. The staleness of the mood file became a second, `settled` entry, so the next session inherits the answer instead of rediscovering the conflict. Both are in `decisions.md` as of this run.

`demo/home.html` is the screen built after the resolution: saturated colour and big friendly shapes from the mood, static acknowledgement from the decisions, no score anywhere.

## What the run surfaced

1. **Precedence resolves conflicts. It does not repair them.** `load_order` decides which file wins and says nothing about the losing file being wrong and left in place. An agent that applies precedence and moves on leaves the next session to hit the same wall. The `updated` dates make staleness detectable, six weeks apart here, but v0.1 only says an agent "should say so" (SPEC §2) and gives no account of what happens next. Worth tightening in v0.2.

2. **A ban needs a replacement.** "No celebration animations" says what not to do and leaves the positive case unspecified. That is the same shape as the calm-ledger finding about positive money colour, from a completely different project and mood, which suggests it is structural rather than coincidental. Decisions phrased as prohibitions reliably generate a follow up decision. The spec could say so: when you ban something the mood asks for, expect to specify the substitute.

3. **Perceptual files have no status field.** `decisions.md` entries can be `settled`, `provisional`, or `superseded`. `mood.md` has no equivalent, so "this was true in June and is now partly wrong" has nowhere to live except a decision entry pointing back at it, which is what we did. It works, and it reads like a workaround. A `status` in the manifest's file list, or a `superseded_in_part` marker, would say it properly.
