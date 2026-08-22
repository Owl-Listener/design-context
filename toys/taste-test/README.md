# The Taste Test

A taste analyser for designers. Twenty forced choices between unlabelled
specimens, and it hands back your position on five axes plus a filled-in
`mood.md` you can drop into `design-context/`.

Open `index.html`. No build, no dependencies, one file.

## What it does

Every round shows the same component twice, under two different token sets,
with the style names hidden. You pick the one you'd ship. Each pair is
constructed to differ hard on one axis and as little as possible everywhere
else, so a choice is a signal about that axis rather than a general vote.

The five axes:

| axis | poles |
| --- | --- |
| temperature | cool ↔ warm |
| density | airy ↔ dense |
| edge | soft ↔ sharp |
| ornament | restrained ↔ expressive |
| energy | still ↔ kinetic |

At the end it reports where you landed, how consistent you were, which
styles you kept choosing, and the mood file itself.

## Why it emits a real file

A quiz that ends in a badge is a quiz. This one ends in
`design-context/mood.md`, in mood-protocol shape: three lines, three
qualities, references, anti-references. An agent that reads your
`design-context/index.md` at session start loads it before it generates
anything, which is the whole point of the repo it sits in.

Two things it does deliberately:

- **An axis you split evenly on is reported as open, not as balance.** It
  is named once, in the qualities, and never cited as intent. A ban or a
  lean you didn't actually express should not turn up in a file an agent
  will treat as binding.
- **The provenance line says what the file is.** It is a record of
  preference, taken from specimens, not a reading of your product. The file
  says so in its first line so nobody has to remember.

## The specimen library

Twelve styles — Passbook, Terminal, Bauhaus, Lozenge, Swiss, Neon, Reading
Room, Brutalist, Clinical, Sunset, Blueprint, Velvet — across six
components. Every style is the same markup under a different set of CSS
custom properties; nothing is a screenshot. "All 12 styles" in the header
browses the whole grid, which is useful on its own for arguing that style
is a variable.

## Swapping the styles

`STYLES` in `index.html` is the whole library. Each entry is a token bundle
plus a position `at: [temperature, density, edge, ornament, energy]`, each
from −1 to +1. Replace the array and the instrument re-tunes itself: round
construction, scoring and the gallery all read from it. Keep at least one
pair separated by ≥ 0.95 on every axis or that axis can't be tested.

`POLES` holds the language each pole contributes to the mood file. That is
the part worth rewriting if you want the output to sound like your team.
