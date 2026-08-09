# Dry run — 2026-08-09

One agent session, playing by the rules: load `design-context/index.md`, follow `load_order`, build the Calm Ledger home screen. The screen deliberately includes the two cases where finance-app convention pulls hardest against this project's decisions: a negative monthly balance, and a savings goal being reached.

## Conformance check

**Decision 2026-08-09 (red is for errors only, never money) — held.** The negative balance and all outgoing amounts render in ink with a small outgoing glyph (−). No red appears anywhere in the file. The temptation case: convention says a negative month is red and bold. The decision's Because ("a negative balance is information, not an alarm") generalised cleanly to the tabular rows too, which the decision never explicitly mentioned. This is the Because field doing its job.

**Decision 2026-08-04 (no celebration mechanics) — held.** The reached goal is one quiet line in a card: "Your holiday fund reached its goal this week." No animation, no badge, no exclamation mark. The mood's anti-reference ("NOT a gamified fintech app") and the decision reinforced each other; the agent never had to arbitrate between files.

**Decision 2026-08-01 (8px corners, provisional) — held, and correctly annotated.** All cards use the 8px radius, and the CSS comment marks it provisional, so a future session inheriting this file knows the corner radius is still on trial.

**Mood conformance.** Warm paper neutrals, ink not black, generous line height, serif set like a paperback page, one slow fade and no other motion, fewer numbers than a finance screen "should" have, no deltas or arrows. Anti-references respected: nothing here reads as trading terminal, gamified fintech, or KPI dashboard.

## What the run surfaced (for the spec's issue list)

1. **Precedence never got tested.** Mood and decisions agreed everywhere. A better stress test would set them in conflict, e.g. a mood that says "playful" against a decision that bans celebration, to verify the agent flags rather than silently resolves. Worth adding as a second example.
2. **The glyph choice was unspecified.** The decision says "ink with a small glyph" but not which glyph. The agent chose − (minus). Fine, but two sessions could choose differently; the decision should be tightened or the choice recorded as a new entry.
3. **Positive money colour was a judgement call.** The decisions constrain negative amounts; nothing constrains positive ones. The agent used a quiet sage. Defensible from the mood, but it's exactly the kind of silent judgement that should become a `provisional` entry via update-design-context.

Findings 2 and 3 are the system working as intended: the run didn't just pass, it generated the next two candidate entries for `decisions.md`.
