#!/usr/bin/env python3
"""Tests for lint_design_context.py.

    python3 tools/test_lint.py

Standard library only. Each test builds a design-context/ directory in a
temporary folder, lints it, and asserts on the findings. The fixtures are
inline rather than on disk so that a rule and its counterexample can be
read in one screen.
"""

import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lint_design_context as lint  # noqa: E402


GOOD_INDEX = """---
spec: design-context/v0.2
project: Test Project
updated: 2026-08-16
files:
  - path: decisions.md
    role: memory
    source: design-context
    updated: 2026-08-16
  - path: mood.md
    role: aesthetic-intent
    source: mood-protocol
    updated: 2026-08-01
load_order: [decisions.md, mood.md]
---

# Design context for Test Project

One line on what this project is.
"""

GOOD_DECISIONS = """# Design decisions — Test Project

Append-only. Newest first.

## 2026-08-16 — Cards are square-cornered
**Decision:** Cards use a 0px radius everywhere.
**Because:** Rounded corners read as consumer-app friendly.
**Supersedes:** none
**Status:** settled
"""

GOOD_MOOD = "# Mood — Test Project\n\nQuiet competence.\n"


class LintCase(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.dir = os.path.join(self.root, "design-context")
        os.makedirs(self.dir)
        self.write("index.md", GOOD_INDEX)
        self.write("decisions.md", GOOD_DECISIONS)
        self.write("mood.md", GOOD_MOOD)

    def tearDown(self):
        shutil.rmtree(self.root)

    def write(self, name, text):
        with open(os.path.join(self.dir, name), "w", encoding="utf-8") as handle:
            handle.write(text)

    def run_lint(self, allow_placeholders=False):
        report = lint.Report()
        lint.check_directory(self.root, report, allow_placeholders)
        return report

    def messages(self, level=None):
        return [
            f.message
            for f in self.run_lint().findings
            if level is None or f.level == level
        ]

    def assertClean(self):
        report = self.run_lint()
        problems = [str(f) for f in report.findings if f.level in ("error", "warning")]
        self.assertEqual(problems, [], "expected no errors or warnings")

    def assertFinding(self, level, fragment):
        found = [f.message for f in self.run_lint().findings if f.level == level]
        self.assertTrue(
            any(fragment in m for m in found),
            "expected a %s containing %r, got: %s" % (level, fragment, found),
        )

    def assertNoFinding(self, level, fragment):
        found = [f.message for f in self.run_lint().findings if f.level == level]
        self.assertFalse(
            any(fragment in m for m in found),
            "unexpected %s containing %r" % (level, fragment),
        )


class TestValidDirectory(LintCase):
    def test_the_fixture_is_clean(self):
        self.assertClean()

    def test_v01_directory_is_still_valid(self):
        self.write("index.md", GOOD_INDEX.replace("v0.2", "v0.1"))
        self.assertClean()
        self.assertFinding("note", "v0.1")


class TestManifest(LintCase):
    def test_missing_frontmatter(self):
        self.write("index.md", "# No frontmatter here\n")
        self.assertFinding("error", "no YAML frontmatter")

    def test_missing_required_key(self):
        self.write("index.md", GOOD_INDEX.replace("project: Test Project\n", ""))
        self.assertFinding("error", "missing required key 'project'")

    def test_unknown_spec_version(self):
        self.write("index.md", GOOD_INDEX.replace("v0.2", "v9.9"))
        self.assertFinding("error", "unknown spec version")

    def test_bad_date(self):
        self.write("index.md", GOOD_INDEX.replace("updated: 2026-08-16", "updated: August 2026", 1))
        self.assertFinding("error", "not an ISO date")

    def test_role_outside_the_controlled_list(self):
        self.write("index.md", GOOD_INDEX.replace("role: aesthetic-intent", "role: vibes"))
        self.assertFinding("error", "not in the controlled list")

    def test_decisions_must_load_first(self):
        self.write("index.md", GOOD_INDEX.replace(
            "load_order: [decisions.md, mood.md]", "load_order: [mood.md, decisions.md]"))
        self.assertFinding("error", "decisions.md must load first")

    def test_load_order_names_an_unlisted_file(self):
        self.write("index.md", GOOD_INDEX.replace(
            "load_order: [decisions.md, mood.md]", "load_order: [decisions.md, mood.md, voice.md]"))
        self.assertFinding("error", "load_order names 'voice.md'")

    def test_listed_file_missing_from_load_order(self):
        self.write("index.md", GOOD_INDEX.replace(
            "load_order: [decisions.md, mood.md]", "load_order: [decisions.md]"))
        self.assertFinding("error", "missing from load_order")

    def test_listed_file_absent_from_disk(self):
        os.remove(os.path.join(self.dir, "mood.md"))
        self.assertFinding("error", "does not exist on disk")

    def test_file_on_disk_absent_from_manifest(self):
        self.write("voice.md", "# Voice\n")
        self.assertFinding("warning", "not listed in the manifest")

    def test_index_may_not_list_itself(self):
        self.write("index.md", GOOD_INDEX.replace(
            "  - path: decisions.md",
            "  - path: index.md\n    role: memory\n    source: design-context\n"
            "    updated: 2026-08-16\n  - path: decisions.md"))
        self.assertFinding("error", "must not list itself")

    def test_non_markdown_file_is_rejected(self):
        with open(os.path.join(self.dir, "tokens.json"), "w", encoding="utf-8") as handle:
            handle.write("{}\n")
        self.assertFinding("error", "only markdown files are permitted")

    def test_tab_in_frontmatter(self):
        self.write("index.md", GOOD_INDEX.replace("  - path: mood.md", "\t- path: mood.md"))
        self.assertFinding("error", "tab in frontmatter")

    def test_placeholders_rejected_unless_allowed(self):
        self.write("index.md", GOOD_INDEX.replace("project: Test Project", "project: PROJECT_NAME"))
        self.assertFinding("error", "template placeholder")
        report = lint.Report()
        lint.check_directory(self.root, report, True)
        self.assertEqual([f.message for f in report.findings if f.level == "error"], [])


class TestFileStatus(LintCase):
    def with_status(self, status, governed_by=None):
        extra = "    status: %s\n" % status
        if governed_by:
            extra += "    governed_by: %s\n" % governed_by
        self.write("index.md", GOOD_INDEX.replace(
            "    updated: 2026-08-01\n", "    updated: 2026-08-01\n" + extra))

    def test_partial_requires_governed_by(self):
        self.with_status("partial")
        self.assertFinding("error", "requires 'governed_by'")

    def test_partial_with_governed_by_is_clean(self):
        self.with_status("partial", "2026-08-16 — Cards are square-cornered")
        self.assertClean()

    def test_unknown_status(self):
        self.with_status("mostly-fine", "2026-08-16 — Cards are square-cornered")
        self.assertFinding("error", "is not one of")

    def test_governed_by_must_name_a_real_entry(self):
        self.with_status("partial", "2026-01-01 — A decision nobody made")
        self.assertFinding("error", "which is not an entry in decisions.md")

    def test_status_is_not_available_in_v01(self):
        self.with_status("partial", "2026-08-16 — Cards are square-cornered")
        with open(os.path.join(self.dir, "index.md"), encoding="utf-8") as handle:
            text = handle.read()
        self.write("index.md", text.replace("v0.2", "v0.1"))
        self.assertFinding("error", "introduced in v0.2")

    def test_governed_by_without_status_is_a_warning(self):
        self.write("index.md", GOOD_INDEX.replace(
            "    updated: 2026-08-01\n",
            "    updated: 2026-08-01\n    governed_by: 2026-08-16 — Cards are square-cornered\n"))
        self.assertFinding("warning", "says nothing")

    def test_decisions_cannot_be_stale(self):
        self.write("index.md", GOOD_INDEX.replace(
            "  - path: decisions.md\n    role: memory\n    source: design-context\n"
            "    updated: 2026-08-16\n",
            "  - path: decisions.md\n    role: memory\n    source: design-context\n"
            "    updated: 2026-08-16\n    status: partial\n"
            "    governed_by: 2026-08-16 — Cards are square-cornered\n"))
        self.assertFinding("error", "decisions.md cannot be stale")


class TestDecisions(LintCase):
    def test_missing_because(self):
        self.write("decisions.md", GOOD_DECISIONS.replace(
            "**Because:** Rounded corners read as consumer-app friendly.\n", ""))
        self.assertFinding("error", "missing **Because:**")

    def test_empty_because(self):
        self.write("decisions.md", GOOD_DECISIONS.replace(
            "**Because:** Rounded corners read as consumer-app friendly.", "**Because:**"))
        self.assertFinding("error", "**Because:** is empty")

    def test_hyphen_instead_of_em_dash_in_heading(self):
        self.write("decisions.md", GOOD_DECISIONS.replace(
            "## 2026-08-16 — Cards", "## 2026-08-16 - Cards"))
        self.assertFinding("error", "em dash")

    def test_unknown_status(self):
        self.write("decisions.md", GOOD_DECISIONS.replace("**Status:** settled", "**Status:** final"))
        self.assertFinding("error", "Status 'final' is not one of")

    def test_entries_must_run_newest_first(self):
        self.write("decisions.md", GOOD_DECISIONS + """
## 2026-09-01 — A later decision
**Decision:** Something else.
**Because:** A reason.
**Supersedes:** none
**Status:** settled
""")
        self.assertFinding("error", "newest first")

    def test_supersedes_must_name_a_real_entry(self):
        self.write("decisions.md", GOOD_DECISIONS.replace(
            "**Supersedes:** none", "**Supersedes:** 2026-01-01 — Something that never existed"))
        self.assertFinding("error", "which is not an entry in this file")

    def test_superseded_target_must_be_flipped(self):
        self.write("decisions.md", """# Design decisions

## 2026-08-16 — Cards are square-cornered
**Decision:** Cards use a 0px radius everywhere.
**Because:** A reason.
**Supersedes:** 2026-08-01 — Cards are rounded
**Status:** settled

## 2026-08-01 — Cards are rounded
**Decision:** Cards use an 8px radius.
**Because:** Trying the softer look.
**Supersedes:** none
**Status:** settled
""")
        self.assertFinding("error", "must read 'superseded'")

    def test_a_well_formed_reversal_is_clean(self):
        self.write("decisions.md", """# Design decisions

## 2026-08-16 — Cards are square-cornered
**Decision:** Cards use a 0px radius everywhere.
**Because:** A reason.
**Supersedes:** 2026-08-01 — Cards are rounded
**Status:** settled

## 2026-08-01 — Cards are rounded
**Decision:** Cards use an 8px radius.
**Because:** Trying the softer look.
**Supersedes:** none
**Status:** superseded
""")
        self.assertClean()

    def test_orphan_superseded_entry_warns(self):
        self.write("decisions.md", GOOD_DECISIONS.replace("**Status:** settled", "**Status:** superseded"))
        self.assertFinding("warning", "no entry names it in Supersedes")

    def test_duplicate_reference(self):
        self.write("decisions.md", GOOD_DECISIONS + """
## 2026-08-16 — Cards are square-cornered
**Decision:** Again.
**Because:** A reason.
**Supersedes:** none
**Status:** settled
""")
        self.assertFinding("error", "share the date and title")

    def test_template_comment_is_not_parsed_as_an_entry(self):
        self.write("decisions.md", """# Design decisions

<!-- Template entry, copy and fill:

## YYYY-MM-DD — Short decision title
**Decision:** The decision.
**Because:** The reason.
**Supersedes:** none
**Status:** settled

-->
""")
        self.assertClean()


class TestProhibitionNote(LintCase):
    BAN = """# Design decisions

## 2026-08-16 — No celebration animations
**Decision:** Finishing a book produces no animation, no sound, and no badge.
**Because:** The reward competed with the reading.
**Supersedes:** none
**Status:** settled
"""

    def test_ban_without_instead_gets_a_note(self):
        self.write("decisions.md", self.BAN)
        self.assertFinding("note", "names no **Instead:**")
        self.assertClean()  # a note never fails the run

    def test_instead_silences_it(self):
        self.write("decisions.md", self.BAN.replace(
            "**Supersedes:** none",
            "**Instead:** Completion opens a static full-bleed page.\n**Supersedes:** none"))
        self.assertNoFinding("note", "names no **Instead:**")

    def test_instead_open_also_silences_it(self):
        self.write("decisions.md", self.BAN.replace(
            "**Supersedes:** none",
            "**Instead:** open — nobody has hit the case yet.\n**Supersedes:** none"))
        self.assertNoFinding("note", "names no **Instead:**")

    def test_no_note_under_v01(self):
        self.write("index.md", GOOD_INDEX.replace("v0.2", "v0.1"))
        self.write("decisions.md", self.BAN)
        self.assertNoFinding("note", "names no **Instead:**")

    def test_a_plain_decision_gets_no_note(self):
        self.assertNoFinding("note", "names no **Instead:**")

    def test_a_positive_decision_that_rules_out_near_misses_gets_no_note(self):
        # The substitute is the first thing the decision says. The bans that
        # follow are fencing, not the decision.
        self.write("decisions.md", """# Design decisions

## 2026-08-16 — Outgoing amounts are marked with the minus sign
**Decision:** Outgoing amounts carry the minus sign before the figure. Not brackets, not a downward arrow, not a triangle.
**Because:** Minus is arithmetic rather than editorial.
**Supersedes:** none
**Status:** provisional
""")
        self.assertNoFinding("note", "names no **Instead:**")

    def test_a_quoted_reference_to_a_ban_is_not_a_ban(self):
        self.write("decisions.md", """# Design decisions

## 2026-08-16 — Staleness is recorded in the manifest
**Decision:** `mood.md` carries `status: partial` and `governed_by: 2026-08-01 — No celebration animations` in `index.md`.
**Because:** A fact about a file belongs where an agent reads it first.
**Supersedes:** 2026-08-01 — No celebration animations
**Status:** settled

## 2026-08-01 — No celebration animations
**Decision:** Finishing a book produces no animation and no sound.
**Because:** The reward competed with the reading.
**Supersedes:** none
**Status:** superseded
""")
        self.assertNoFinding("note", "names no **Instead:**")

    def test_a_superseded_ban_gets_no_note(self):
        self.write("decisions.md", """# Design decisions

## 2026-08-16 — Completion opens a full page illustration
**Decision:** Completion is acknowledged with a static full-bleed page.
**Because:** Colour and scale can carry celebration.
**Supersedes:** 2026-08-01 — No celebration animations
**Status:** settled

## 2026-08-01 — No celebration animations
**Decision:** Finishing a book produces no animation and no sound.
**Because:** The reward competed with the reading.
**Supersedes:** none
**Status:** superseded
""")
        self.assertNoFinding("note", "names no **Instead:**")


class TestExitCodes(LintCase):
    def test_clean_run_exits_zero(self):
        self.assertEqual(lint.main([self.root, "--quiet"]), 0)

    def test_error_exits_one(self):
        self.write("decisions.md", GOOD_DECISIONS.replace("**Status:** settled", "**Status:** final"))
        self.assertEqual(lint.main([self.root, "--quiet"]), 1)

    def test_warning_passes_but_fails_under_strict(self):
        self.write("voice.md", "# Voice\n")
        self.assertEqual(lint.main([self.root, "--quiet"]), 0)
        self.assertEqual(lint.main([self.root, "--quiet", "--strict"]), 1)

    def test_missing_directory_exits_one(self):
        shutil.rmtree(self.dir)
        self.assertEqual(lint.main([self.root, "--quiet"]), 1)

    def test_the_design_context_directory_can_be_named_directly(self):
        self.assertEqual(lint.main([self.dir, "--quiet"]), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
