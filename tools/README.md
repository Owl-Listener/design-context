# tools

One tool. It checks that a `design-context/` directory says what the spec says it should say.

```
python3 tools/lint_design_context.py path/to/your-project
```

Point it at a project root or at the `design-context/` directory itself. No arguments means the current directory. Python 3.8 or later, standard library only, no install step. A conformance checker that needs a package manager is a conformance checker people skip.

## What it checks

**`index.md`** — frontmatter parses; `spec`, `project`, `updated`, `files` and `load_order` are all present; dates are real ISO dates; every `role` is in the controlled list; `decisions.md` is listed and loads first; `load_order` and `files` name exactly the same set; every listed file exists on disk; every markdown file on disk is listed; nothing but markdown is in the directory; `status` and `governed_by` are used only under v0.2 and only together.

**`decisions.md`** — every heading reads `## YYYY-MM-DD — Title`; every entry has a Decision, a Because, a Supersedes and a Status; Status is one of the three permitted values; entries run newest first; no two entries share a date and title, because that pair is how entries are referenced; every `Supersedes` names a real, older entry; every superseded entry has actually had its Status flipped, and every flipped entry has something that superseded it.

## Three levels

```
error    the directory does not conform. Exit code 1.
warning  conforming but probably a mistake. Exit code 1 only under --strict.
note     worth knowing. Never changes the exit code.
```

Notes are where the spec's softer advice lives. The main one: under v0.2, a decision whose first sentence is a prohibition and which carries no `**Instead:**` field gets a note saying so. That is a heuristic, not a rule — see the comment above `PROHIBITION_RE` for what it looks at and what it misses. A ban with no substitute is legal and sometimes correct; it just reliably generates a second decision later, and it is better to know that now.

## Options

```
--strict              treat warnings as errors
--allow-placeholders  accept PROJECT_NAME, YYYY-MM-DD and WRITE_ME as valid,
                      for linting the unfilled template
--quiet               print only the summary line
```

## Tests

```
python3 tools/test_lint.py
```

Every rule has a case and a counterexample. If you add a rule, add both.

## What it does not check

Taste, obviously. Also: whether a Because is a real reason, whether a mood file is honest, whether `load_order` puts things in the order this particular project needs, and whether the decisions in the log are any good. The linter checks that the record is well formed. Whether the record is true is a human's job, and always will be.
