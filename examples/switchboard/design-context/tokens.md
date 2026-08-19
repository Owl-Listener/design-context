# Tokens — Switchboard

*Produced with tokens-protocol v0.1 on 2026-08-16. This annotates the tokens that exist; it does not define new ones and it is not a proposal. Where two stylesheets disagree, the entry says which one wins and why, because that is the question an agent actually has.*

## Source

Three stylesheets are live:

- `static/css/refresh.css` — the 2024 refresh, custom properties, **authoritative for all new work**.
- `static/css/bootstrap-legacy.css` — the original build. Frozen (decision 2026-08-16). Still styles roughly half the driver list.
- `static/css/overrides.css` — 340 lines of specificity fights, loaded last. Nothing new goes here, ever.

If a value appears in more than one file, `refresh.css` is the intended one, whatever the cascade currently does.

## Color

`--text-primary: #1A1C1F`, `--text-secondary: #6E7076`, `--surface: #FFFFFF`, `--rule: #E3E5E8`.

`--danger: #C2372D` is for the undo window and nothing else (decision 2026-08-16). `--warning: #B4700A` is the amber that carries late routes, used as a 3px left border on the row, never as a fill: a filled row at this density reads as a block of colour rather than a row.

`#71737A` and `#6F7278` appear in legacy files and are the same grey as `--text-secondary` by accident of history. Do not preserve them when you touch a component.

There is no success colour. Nothing here needs one; a reassignment that worked shows the driver in the new row, which is better evidence than green.

## Typography

One family, the system stack, at three sizes: 11px for board rows, 13px for everything else, 15px for the dialog heading. The 11px is deliberate and load-bearing (decision 2026-08-16) — it is what makes sixty rows fit — and it is the value most likely to be "fixed" by someone acting in good faith.

`bootstrap-legacy.css` still sets a serif stack on `<h2>` in two places. That is a leftover, not a rule.

## Spacing

A 4px scale: 4, 8, 12, 16, 24. Board rows use 4px vertical padding, which is the tightest value in the system and the reason the board works.

Legacy screens use a 5px scale inherited from the original template. Port to the 4px scale when you touch a component; do not sweep.

## Elevation

Two levels. Flat for everything on the board. One shadow, `0 2px 8px rgba(0,0,0,0.15)`, for the reassign dialog and the driver popover — the only two things in the product that sit above the page. Elevation here means "this is modal and you are stuck with it until you deal with it", not "this is important".

## Motion

None, except the undo countdown, which is a five-second linear bar and is the only animation in the product. That is not an oversight to correct: instant response is the tool's most trusted quality (`trace.md`, Qualities). Adding transitions to rows, filters or dialogs would make the tool feel slower while making it measurably not.

## Radius

`--radius: 3px` on buttons, inputs and the dialog. Legacy components carry 4px and 6px from two different template eras. Not worth a sweep; align when you touch one.
