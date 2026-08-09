# Design decisions — Calm Ledger

Append-only. Newest first. Never edit or delete an entry: reversals are new entries that supersede old ones.

## 2026-08-09 — Components come from shadcn/ui
**Decision:** Interactive components (dialogs, selects, form controls, menus) are copied in from shadcn/ui and modified in place. Do not hand-roll a primitive the library already ships. Static presentational screens, like the monthly summary, are written directly.
**Because:** Two people build this. Time spent reimplementing focus management, keyboard handling, and ARIA is time not spent on the part of this product nobody else has built. shadcn is copy-in rather than a dependency, so we own every component and can take it as far from the default as this product needs.
**Supersedes:** none
**Status:** settled

## 2026-08-09 — The shadcn defaults we override
**Decision:** Three overrides, applied to every component we copy in. `--radius` is set to the project's 8px rather than the library default. The `destructive` variant is reserved for genuine system errors and is never applied to money. Dialog and popover entrance animations are stripped back to the opacity fade.
**Because:** The library's defaults are tuned for a consumer SaaS register and this product is closer to a passbook than an app. The radius, the red, and the motion are the three places where accepting a default would quietly undo a decision we have already made here, and none of them look like a mistake at the moment they happen. Writing them down means the next session overrides them on purpose rather than rediscovering why the screen stopped feeling right.
**Supersedes:** none
**Status:** settled

## 2026-08-09 — Outgoing amounts are marked with the minus sign
**Decision:** Outgoing and negative amounts carry the minus sign (U+2212) before the figure, set in the soft ink tone. Not brackets, not a downward arrow, not a triangle.
**Because:** The "red is for errors only" decision said "a small glyph" without saying which one, so the first build chose on our behalf. Minus is arithmetic rather than editorial: arrows imply a trend we are not claiming, and brackets carry an accountancy formality that pulls against the paperback feeling. Naming it means the next session inherits the choice instead of remaking it.
**Supersedes:** none
**Status:** provisional

## 2026-08-09 — Positive amounts are sage, never green
**Decision:** Incoming and positive amounts use the sage accent (#7A8B6F). Green is not used for money anywhere in the product.
**Because:** The red decision constrained negative amounts and left positive ones open, so the first build made a silent judgement call. Sage follows from the warm neutrals in the mood and keeps us clear of the red and green semantics the anti-references reject. Money coming in should read as steady, not as a win.
**Supersedes:** none
**Status:** provisional

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
