# Design decisions — Switchboard

Append-only. Newest first. Never edit or delete an entry: reversals are new entries that supersede old ones. See design-context SPEC.md section 3 for the format rules.

Entries dated before 2026-08-16 were reconstructed during adoption from pull requests, an incident report and one long argument in a channel. Their dates are when the decision was made, not when it was written down. Their Because fields say where they came from, because v0.2 has no provenance field and the reason is the honest place to put it.

## 2026-08-16 — Three greys collapse to two
**Decision:** `#6E7076`, `#71737A` and `#6F7278` are the same grey with three histories. New work uses `--text-secondary` only. The other two get replaced file by file as we touch them, not in one sweep.
**Because:** Nobody chose three greys. Three greys are what happens when three people each match a screenshot by eye across four years. This is cleanup, not taste, and it is recorded here so that an agent editing a component knows which one to keep rather than preserving whichever it found.
**Supersedes:** none
**Status:** provisional

## 2026-08-16 — New work uses refresh.css; bootstrap-legacy.css is frozen
**Decision:** All new and modified components take their tokens and classes from `refresh.css`. `bootstrap-legacy.css` is frozen: no new rules, no edits except security fixes, deletions welcome.
**Because:** Three generations of styling are live at once and each one was added by someone reasonably avoiding the previous mess. Freezing the oldest is the only thing that stops a fourth generation appearing. Not a redesign: a rule about where new lines of CSS go.
**Instead:** When a legacy class is in the way, port that one component to `refresh.css` and delete the legacy rule in the same commit. Small and local, never a migration project.
**Supersedes:** none
**Status:** settled

## 2026-08-16 — Red means undo-in-progress and nothing else
**Decision:** Red is reserved for the five-second undo window after a reassignment commits. It does not mark late routes, unavailable drivers, row status, or validation errors.
**Because:** The cold read found red doing four unrelated jobs on one screen, so it had stopped meaning anything. A coordinator described the board as "red when it's busy", which is the sound of a colour that carries no information. Reserving it for the one moment that is genuinely reversible gives it a job back.
**Instead:** Late routes take the amber left border. Unavailable drivers take an outlined pill with the word, not a colour alone. Validation errors take the message under the field, which is where the eye already goes.
**Supersedes:** none
**Status:** settled

## 2026-08-16 — The dispatch board stays dense
**Decision:** The board shows sixty rows without scrolling on a 1080p screen and continues to. Row height, font size and vertical padding are not to be increased for the sake of breathing room.
**Because:** Coordinators scan the whole board at once and act on what they see; a scroll is a phone call they make late. Density here is not a legacy compromise waiting to be fixed, it is the product working. Every designer who has looked at this screen has wanted to open it up, and this entry exists to stop the seventh one.
**Supersedes:** none
**Status:** settled

## 2026-08-16 — Switchboard is not being redesigned
**Decision:** No visual refresh, no new design language, no component library adoption. This directory exists to make small changes safe, not to license a rewrite.
**Because:** Two people maintain this and six people depend on it every working hour. The last refresh was abandoned half done in 2024 and its remains are the reason there are three stylesheets. A tool this fast, this ugly and this trusted is worth more than a coherent one.
**Instead:** Change lands where a coordinator is confused, blocked, or making an error, one screen at a time, and each change has to survive the dense board it lands in.
**Supersedes:** none
**Status:** settled

## 2026-06-02 — The reassign dialog confirms before it commits
**Decision:** Reassigning a driver who is mid-route requires an explicit confirmation naming the driver and the route. Reassigning an idle driver commits immediately.
**Because:** Reconstructed from the incident report of 2026-06-01, when a driver forty minutes into a route was reassigned by a mis-click and nobody noticed for two hours. The confirmation is deliberately asymmetric: the risky case is interrupted, the common case is not, because a dialog on every action is a dialog nobody reads.
**Supersedes:** none
**Status:** settled

## 2025-11-10 — Driver names are never truncated
**Decision:** Driver names render in full, wrapping to a second line where the column is narrow. No ellipsis, no initials, no hover-to-reveal.
**Because:** Reconstructed from the argument on PR #412. Two drivers share the surname Okonkwo and one truncation sent a van to the wrong depot. The person who filed that PR has left; the rule survived in the code with no comment explaining it, one refactor away from being tidied out.
**Supersedes:** none
**Status:** settled

## 2025-04-22 — Filters live in the toolbar above the board
**Decision:** Board filters are a single row of controls above the table.
**Because:** Reconstructed from the 2024 refresh commits. The sidebar cost 240px of horizontal space that the board needed for the route column, and coordinators set filters once at the start of a shift and then never touch them, so the controls did not deserve permanent real estate.
**Supersedes:** 2024-09-03 — Filters live in a left sidebar
**Status:** settled

## 2024-09-03 — Filters live in a left sidebar
**Decision:** Board filters are a persistent left sidebar, always visible.
**Because:** Reconstructed from the original build. The reasoning is not recorded anywhere and nobody remaining remembers it; the best available guess is that it came with the admin template the tool was started from. Recorded because the pattern is still in two other screens, and knowing it was reversed here is what tells the next session those two are the leftovers rather than the standard.
**Supersedes:** none
**Status:** superseded
