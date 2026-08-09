# Design decisions — Calm Ledger

Append-only. Newest first. Never edit or delete an entry: reversals are new entries that supersede old ones.

## 2026-08-09 — Red is for errors only, never for money
**Decision:** Negative balances and overspending are shown in the ink colour with a small glyph, never in red. Red appears only for system errors.
**Because:** Red numbers are the single biggest heart-rate spike in finance apps. The product exists to remove that spike. A negative balance is information, not an alarm.
**Supersedes:** none
**Status:** settled

## 2026-08-04 — No confetti, no streaks, no celebration animations
**Decision:** Reaching a savings goal gets one quiet line of acknowledgement. No animation, no gamification mechanics anywhere.
**Because:** Gamified finance apps borrow casino grammar. Our mood is "a walk after dinner, not a fruit machine." Users should feel steady, not rewarded.
**Supersedes:** none
**Status:** settled

## 2026-08-01 — Rounded corners, 8px, everywhere
**Decision:** All cards and inputs use an 8px corner radius.
**Because:** Trying the softer look for the calm register. Revisit after the first usability round.
**Supersedes:** none
**Status:** provisional
