#!/usr/bin/env python3
"""Check a design-context/ directory against the specification.

Usage:
    lint_design_context.py [PATH ...] [options]

PATH is a project root (containing design-context/) or the design-context/
directory itself. Defaults to the current directory.

Options:
    --strict              Treat warnings as errors.
    --allow-placeholders  Accept template placeholders (PROJECT_NAME,
                          YYYY-MM-DD, WRITE_ME) as valid values. Use this
                          when linting the unfilled template.
    --quiet               Print only the summary line.
    -h, --help            Show this message.

Exit codes:
    0  no errors (warnings may have been printed)
    1  at least one error, or a warning under --strict
    2  the linter could not run (bad arguments, unreadable path)

Standard library only, Python 3.8+. No dependencies is a deliberate
constraint: a spec whose conformance checker needs an install is a spec
people check by eye.

Three levels of finding:

    error    the directory does not conform. Fix it.
    warning  conforming but very likely a mistake. --strict fails on these.
    note     worth knowing. Never fails, including under --strict.

See SPEC.md for the rules. Where this file and SPEC.md disagree, SPEC.md
is right and this file has a bug.
"""

import os
import re
import sys

KNOWN_SPECS = ("design-context/v0.1", "design-context/v0.2")
CURRENT_SPEC = "design-context/v0.2"

# SPEC 2: the controlled role list.
ROLES = {
    "aesthetic-intent",
    "vocabulary",
    "verbal-identity",
    "token-intent",
    "trace",
    "memory",
}

# SPEC 2: file status, v0.2 and later. Absent means "current".
FILE_STATUSES = ("current", "partial", "superseded")

# SPEC 3: decision status.
DECISION_STATUSES = ("settled", "provisional", "superseded")

REQUIRED_FILES = ("index.md", "decisions.md")

ENTRY_FIELDS = ("Decision", "Because", "Supersedes", "Status", "Instead")
REQUIRED_ENTRY_FIELDS = ("Decision", "Because", "Supersedes", "Status")

MANIFEST_KEYS = ("spec", "project", "updated", "files", "load_order")
FILE_ENTRY_KEYS = ("path", "role", "source", "updated", "status", "governed_by")

PLACEHOLDERS = ("PROJECT_NAME", "YYYY-MM-DD", "WRITE_ME")

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
HEADING_RE = re.compile(r"^##\s+(\S+)\s+—\s+(.+?)\s*$")
LOOSE_HEADING_RE = re.compile(r"^##\s+(.*)$")
FIELD_RE = re.compile(r"^\*\*([A-Za-z]+):\*\*\s*(.*)$")
REFERENCE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\s*—\s*(.+?)\s*$")

# The heuristic behind the "names no substitute" note. It reads the first
# sentence of the Decision only, because that is where a decision says what it
# is: a ban that opens "no animation, no sound, no badge" is a different shape
# from one that states a positive and rules out the near misses afterwards
# ("use the minus sign. Not brackets, not an arrow."). Checking the whole field
# cannot tell those apart and flags both.
#
# It will still occasionally point at a decision that does name its substitute
# in prose. That is a cheap miss: the fix is to lift the substitute into an
# **Instead:** field, which is where tooling and agents can find it anyway.
PROHIBITION_RE = re.compile(
    r"\b(no|not|never|none|nothing|nowhere)\b"
    r"|\bavoid\b|\bban(ned)?\b|\bforbidden\b",
    re.IGNORECASE,
)

SENTENCE_END_RE = re.compile(r"(?<=[.!?])\s")

# Code spans and quoted references to other entries are not this decision's own
# words. An entry that says it supersedes "2026-07-30 — No celebration
# animations" is not itself banning anything.
CODE_SPAN_RE = re.compile(r"`[^`]*`")
INLINE_REFERENCE_RE = re.compile(r"\d{4}-\d{2}-\d{2}\s*—[^.,;)]*")


def first_sentence(text):
    text = CODE_SPAN_RE.sub(" ", text)
    text = INLINE_REFERENCE_RE.sub(" ", text)
    return SENTENCE_END_RE.split(text.strip(), 1)[0]


class Finding:
    def __init__(self, level, path, line, message):
        self.level = level
        self.path = path
        self.line = line
        self.message = message

    def __str__(self):
        where = self.path if self.line is None else "%s:%d" % (self.path, self.line)
        return "%s: %s: %s" % (where, self.level, self.message)


class Report:
    def __init__(self):
        self.findings = []

    def add(self, level, path, line, message):
        self.findings.append(Finding(level, path, line, message))

    def error(self, path, line, message):
        self.add("error", path, line, message)

    def warning(self, path, line, message):
        self.add("warning", path, line, message)

    def note(self, path, line, message):
        self.add("note", path, line, message)

    def count(self, level):
        return sum(1 for f in self.findings if f.level == level)


# --------------------------------------------------------------------------
# Frontmatter
# --------------------------------------------------------------------------

# SPEC 2 constrains the manifest frontmatter to a small YAML subset so that a
# checker can be written in any language in an afternoon. This parser accepts
# exactly that subset and refuses the rest rather than guessing.


def split_frontmatter(text):
    """Return (frontmatter_lines, first_line_number, body_lines) or None."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], 2, lines[i + 1:]
    return None


def _strip_scalar(raw):
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        value = value[1:-1]
    return value


def parse_frontmatter(lines, first_line, path, report):
    """Parse the permitted subset. Returns (data, linenos).

    data maps top-level keys to a string, a list of strings (flow sequence),
    or a list of dicts (block sequence of mappings). Each dict carries a
    '__line__' key with the line its first field appeared on, and a
    '__lines__' dict mapping its keys to line numbers.
    """
    data = {}
    linenos = {}
    key = None
    entries = None
    entry = None

    for offset, raw in enumerate(lines):
        lineno = first_line + offset
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue

        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()

        if "\t" in raw:
            report.error(path, lineno, "tab in frontmatter; the spec permits spaces only")
            continue

        if indent == 0:
            if ":" not in stripped:
                report.error(path, lineno, "not a 'key: value' line: %r" % stripped)
                continue
            key, _, rest = stripped.partition(":")
            key = key.strip()
            rest = rest.strip()
            linenos[key] = lineno
            if key in data:
                report.error(path, lineno, "duplicate key %r" % key)
            if rest.startswith("[") and rest.endswith("]"):
                inner = rest[1:-1].strip()
                items = [_strip_scalar(p) for p in inner.split(",")] if inner else []
                data[key] = [i for i in items if i != ""]
                entries = None
            elif rest == "":
                entries = []
                data[key] = entries
            else:
                data[key] = _strip_scalar(rest)
                entries = None
            entry = None
            continue

        if entries is None:
            report.error(
                path,
                lineno,
                "indented line under a key that is not a sequence: %r" % stripped,
            )
            continue

        if stripped.startswith("- "):
            item = stripped[2:].strip()
            if ":" not in item:
                report.error(path, lineno, "sequence item is not a mapping: %r" % item)
                continue
            k, _, v = item.partition(":")
            entry = {"__line__": lineno, "__lines__": {}}
            entry[k.strip()] = _strip_scalar(v)
            entry["__lines__"][k.strip()] = lineno
            entries.append(entry)
            continue

        if entry is None:
            report.error(path, lineno, "continuation line before any '- ' item: %r" % stripped)
            continue

        if ":" not in stripped:
            report.error(path, lineno, "not a 'key: value' line: %r" % stripped)
            continue
        k, _, v = stripped.partition(":")
        k = k.strip()
        if k in entry:
            report.error(path, lineno, "duplicate key %r in this file entry" % k)
        entry[k] = _strip_scalar(v)
        entry["__lines__"][k] = lineno

    return data, linenos


# --------------------------------------------------------------------------
# index.md
# --------------------------------------------------------------------------


def check_date(value, path, line, report, label, allow_placeholders):
    if allow_placeholders and value == "YYYY-MM-DD":
        return
    if not DATE_RE.match(value or ""):
        report.error(path, line, "%s is not an ISO date (YYYY-MM-DD): %r" % (label, value))
        return
    year, month, day = (int(p) for p in value.split("-"))
    if not (1 <= month <= 12 and 1 <= day <= 31):
        report.error(path, line, "%s is not a real date: %r" % (label, value))


def check_index(directory, report, allow_placeholders):
    """Validate index.md. Returns (spec_version, listed_paths, file_entries)."""
    path = os.path.join(directory, "index.md")
    rel = os.path.relpath(path)
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except OSError as exc:
        report.error(rel, None, "cannot read: %s" % exc)
        return None, [], []

    split = split_frontmatter(text)
    if split is None:
        report.error(rel, 1, "no YAML frontmatter; index.md must open with a '---' fence")
        return None, [], []

    fm_lines, first_line, body = split
    data, linenos = parse_frontmatter(fm_lines, first_line, rel, report)

    for key in MANIFEST_KEYS:
        if key not in data:
            report.error(rel, 1, "frontmatter is missing required key %r" % key)
    for key in data:
        if key not in MANIFEST_KEYS:
            report.warning(rel, linenos.get(key, 1), "unrecognised manifest key %r" % key)

    spec = data.get("spec")
    if isinstance(spec, str):
        if spec not in KNOWN_SPECS:
            report.error(
                rel,
                linenos.get("spec"),
                "unknown spec version %r; this linter knows %s"
                % (spec, ", ".join(KNOWN_SPECS)),
            )
            spec = None
        elif spec != CURRENT_SPEC:
            report.note(
                rel,
                linenos.get("spec"),
                "declares %s; %s is current. See MIGRATION.md — v0.1 stays valid, "
                "migrating is opt-in." % (spec, CURRENT_SPEC),
            )
    elif spec is not None:
        report.error(rel, linenos.get("spec"), "'spec' must be a single value")
        spec = None

    project = data.get("project")
    if isinstance(project, str):
        if not project:
            report.error(rel, linenos.get("project"), "'project' is empty")
        elif project in PLACEHOLDERS and not allow_placeholders:
            report.error(
                rel,
                linenos.get("project"),
                "'project' is still the template placeholder %r" % project,
            )

    if isinstance(data.get("updated"), str):
        check_date(data["updated"], rel, linenos.get("updated"), report, "'updated'", allow_placeholders)

    files = data.get("files")
    entries = []
    if not isinstance(files, list):
        report.error(rel, linenos.get("files"), "'files' must be a sequence of mappings")
    elif not files:
        report.error(rel, linenos.get("files"), "'files' is empty; decisions.md is required")
    elif not all(isinstance(f, dict) for f in files):
        report.error(rel, linenos.get("files"), "'files' must be a sequence of mappings")
    else:
        entries = files

    listed = []
    for entry in entries:
        line = entry.get("__line__")
        entry_path = entry.get("path")
        for key in entry:
            if key.startswith("__"):
                continue
            if key not in FILE_ENTRY_KEYS:
                report.warning(rel, entry["__lines__"].get(key, line), "unrecognised file-entry key %r" % key)

        if not entry_path:
            report.error(rel, line, "file entry has no 'path'")
            continue
        listed.append(entry_path)

        if entry_path == "index.md":
            report.error(rel, line, "index.md must not list itself; it is the manifest")
        if "/" in entry_path or entry_path.startswith("."):
            report.error(rel, line, "'path' must be a bare filename in this directory: %r" % entry_path)
        if not entry_path.endswith(".md"):
            report.error(rel, line, "'path' must be a .md file: %r" % entry_path)

        role = entry.get("role")
        if role is None:
            report.error(rel, line, "%s: file entry has no 'role'" % entry_path)
        elif role not in ROLES:
            report.error(
                rel,
                entry["__lines__"].get("role", line),
                "%s: role %r is not in the controlled list (%s)"
                % (entry_path, role, ", ".join(sorted(ROLES))),
            )
        if entry_path == "decisions.md" and role not in (None, "memory"):
            report.error(rel, line, "decisions.md must have role 'memory'")

        if not entry.get("source"):
            report.error(rel, line, "%s: file entry has no 'source'" % entry_path)

        if "updated" not in entry:
            report.error(rel, line, "%s: file entry has no 'updated'" % entry_path)
        else:
            check_date(
                entry["updated"],
                rel,
                entry["__lines__"].get("updated", line),
                report,
                "%s: 'updated'" % entry_path,
                allow_placeholders,
            )

        status = entry.get("status")
        status_line = entry["__lines__"].get("status", line)
        if status is not None:
            if spec == "design-context/v0.1":
                report.error(
                    rel,
                    status_line,
                    "'status' on a file entry was introduced in v0.2; this manifest declares v0.1",
                )
            elif status not in FILE_STATUSES:
                report.error(
                    rel,
                    status_line,
                    "%s: status %r is not one of %s"
                    % (entry_path, status, ", ".join(FILE_STATUSES)),
                )
            elif status != "current" and not entry.get("governed_by"):
                report.error(
                    rel,
                    status_line,
                    "%s: status %r requires 'governed_by' naming the decisions.md "
                    "entry that governs the aged part" % (entry_path, status),
                )
            if entry_path == "decisions.md" and status not in (None, "current"):
                report.error(
                    rel,
                    status_line,
                    "decisions.md cannot be stale; individual entries carry their own status",
                )

        if entry.get("governed_by") and spec == "design-context/v0.1":
            report.error(
                rel,
                entry["__lines__"].get("governed_by", line),
                "'governed_by' was introduced in v0.2; this manifest declares v0.1",
            )
        if entry.get("governed_by") and not status:
            report.warning(
                rel,
                entry["__lines__"].get("governed_by", line),
                "%s: 'governed_by' without a 'status' says nothing; the file reads as current"
                % entry_path,
            )

    seen = set()
    for entry_path in listed:
        if entry_path in seen:
            report.error(rel, linenos.get("files"), "%s is listed twice" % entry_path)
        seen.add(entry_path)

    if "decisions.md" not in listed:
        report.error(rel, linenos.get("files"), "decisions.md is required and is not listed")

    load_order = data.get("load_order")
    if not isinstance(load_order, list):
        report.error(rel, linenos.get("load_order"), "'load_order' must be a flow sequence, e.g. [decisions.md]")
    else:
        if load_order and load_order[0] != "decisions.md":
            report.error(
                rel,
                linenos.get("load_order"),
                "decisions.md must load first; settled decisions outrank general intent",
            )
        for name in load_order:
            if name not in listed:
                report.error(
                    rel,
                    linenos.get("load_order"),
                    "load_order names %r, which is not in 'files'. A manifest entry for a "
                    "file that is not there sends the agent looking for something it cannot read."
                    % name,
                )
        for name in listed:
            if name not in load_order:
                report.error(
                    rel,
                    linenos.get("load_order"),
                    "%s is listed in 'files' but missing from load_order" % name,
                )
        if len(set(load_order)) != len(load_order):
            report.error(rel, linenos.get("load_order"), "load_order repeats a file")

    body_text = "\n".join(body).strip()
    if not body_text:
        report.warning(rel, None, "index.md has no body; a few lines of orientation belong under the frontmatter")
    elif not allow_placeholders:
        for placeholder in PLACEHOLDERS:
            if placeholder in body_text:
                report.warning(rel, None, "body still contains the template placeholder %r" % placeholder)
                break

    return spec, listed, entries


# --------------------------------------------------------------------------
# decisions.md
# --------------------------------------------------------------------------


class Entry:
    def __init__(self, date, title, line):
        self.date = date
        self.title = title
        self.line = line
        self.fields = {}
        self.field_lines = {}

    @property
    def reference(self):
        return "%s — %s" % (self.date, self.title)


def parse_decisions(path, rel, report):
    try:
        with open(path, encoding="utf-8") as handle:
            lines = handle.read().split("\n")
    except OSError as exc:
        report.error(rel, None, "cannot read: %s" % exc)
        return None

    entries = []
    current = None
    field = None
    in_comment = False

    for index, raw in enumerate(lines):
        lineno = index + 1
        stripped = raw.strip()

        if in_comment:
            if "-->" in stripped:
                in_comment = False
            continue
        if stripped.startswith("<!--"):
            if "-->" not in stripped:
                in_comment = True
            continue

        if stripped.startswith("## "):
            match = HEADING_RE.match(stripped)
            if not match:
                loose = LOOSE_HEADING_RE.match(stripped)
                hint = ""
                if loose and " - " in loose.group(1):
                    hint = " (found '-', the spec uses an em dash '—')"
                elif loose and " – " in loose.group(1):
                    hint = " (found an en dash '–', the spec uses an em dash '—')"
                report.error(
                    rel,
                    lineno,
                    "entry heading must read '## YYYY-MM-DD — Title'%s" % hint,
                )
                current = None
                field = None
                continue
            date, title = match.group(1), match.group(2)
            if not DATE_RE.match(date):
                report.error(rel, lineno, "entry heading does not start with an ISO date: %r" % date)
            current = Entry(date, title, lineno)
            entries.append(current)
            field = None
            continue

        match = FIELD_RE.match(stripped)
        if match:
            name, value = match.group(1), match.group(2).strip()
            if current is None:
                report.error(rel, lineno, "field **%s:** appears before any entry heading" % name)
                continue
            if name not in ENTRY_FIELDS:
                report.warning(rel, lineno, "unrecognised entry field **%s:**" % name)
            if name in current.fields:
                report.error(rel, lineno, "%s: duplicate **%s:** field" % (current.reference, name))
            current.fields[name] = value
            current.field_lines[name] = lineno
            field = name
            continue

        if current is not None and field is not None and stripped:
            current.fields[field] = (current.fields[field] + " " + stripped).strip()
        elif not stripped:
            field = None

    return entries


def check_decisions(directory, spec, report):
    """Validate decisions.md. Returns the set of entry references it defines."""
    path = os.path.join(directory, "decisions.md")
    rel = os.path.relpath(path)
    if not os.path.exists(path):
        report.error(rel, None, "required file is missing")
        return set()

    entries = parse_decisions(path, rel, report)
    if entries is None:
        return set()
    if not entries:
        report.note(rel, None, "no entries yet; the log is empty")
        return set()

    by_reference = {}
    for entry in entries:
        if entry.reference in by_reference:
            report.error(
                rel,
                entry.line,
                "two entries share the date and title %r; references cannot tell them apart"
                % entry.reference,
            )
        else:
            by_reference[entry.reference] = entry

    previous = None
    for entry in entries:
        if previous is not None and entry.date > previous.date:
            report.error(
                rel,
                entry.line,
                "entries run newest first; %s appears below the older %s"
                % (entry.date, previous.date),
            )
        previous = entry

        for name in REQUIRED_ENTRY_FIELDS:
            if name not in entry.fields:
                report.error(rel, entry.line, "%s: missing **%s:**" % (entry.reference, name))
            elif not entry.fields[name]:
                report.error(rel, entry.field_lines[name], "%s: **%s:** is empty" % (entry.reference, name))

        status = entry.fields.get("Status", "").strip().lower().rstrip(".")
        if status and status not in DECISION_STATUSES:
            report.error(
                rel,
                entry.field_lines.get("Status", entry.line),
                "%s: Status %r is not one of %s"
                % (entry.reference, entry.fields["Status"], ", ".join(DECISION_STATUSES)),
            )

        if "Instead" in entry.fields and spec == "design-context/v0.1":
            report.error(
                rel,
                entry.field_lines["Instead"],
                "**Instead:** was introduced in v0.2; the manifest declares v0.1",
            )

    # Supersession has to hang together in both directions.
    superseded_by = {}
    for entry in entries:
        raw = entry.fields.get("Supersedes", "").strip().rstrip(".")
        if not raw or raw.lower() == "none":
            continue
        target = by_reference.get(raw)
        if target is None:
            match = REFERENCE_RE.match(raw)
            hint = "" if match else " (expected 'YYYY-MM-DD — Title')"
            report.error(
                rel,
                entry.field_lines.get("Supersedes", entry.line),
                "%s: Supersedes names %r, which is not an entry in this file%s"
                % (entry.reference, raw, hint),
            )
            continue
        if target.date > entry.date:
            report.error(
                rel,
                entry.field_lines.get("Supersedes", entry.line),
                "%s: supersedes %s, which is newer than it" % (entry.reference, target.reference),
            )
        if target.fields.get("Status", "").strip().lower().rstrip(".") != "superseded":
            report.error(
                rel,
                target.field_lines.get("Status", target.line),
                "%s is superseded by %s, so its Status must read 'superseded'. Flipping "
                "that field is the only edit the spec permits to an existing entry."
                % (target.reference, entry.reference),
            )
        superseded_by.setdefault(target.reference, []).append(entry.reference)

    for entry in entries:
        status = entry.fields.get("Status", "").strip().lower().rstrip(".")
        if status == "superseded" and entry.reference not in superseded_by:
            report.warning(
                rel,
                entry.field_lines.get("Status", entry.line),
                "%s is marked superseded, but no entry names it in Supersedes. A reversal "
                "is a new entry; without one the record does not say what replaced this."
                % entry.reference,
            )

    if spec != "design-context/v0.1":
        for entry in entries:
            decision = entry.fields.get("Decision", "")
            if not decision or "Instead" in entry.fields:
                continue
            if entry.fields.get("Status", "").strip().lower().rstrip(".") == "superseded":
                continue
            if PROHIBITION_RE.search(first_sentence(decision)):
                report.note(
                    rel,
                    entry.field_lines.get("Decision", entry.line),
                    "%s reads as a prohibition and names no **Instead:**. A ban leaves the "
                    "positive case open, and the next session will fill it in for you."
                    % entry.reference,
                )

    return set(by_reference)


# --------------------------------------------------------------------------
# Directory
# --------------------------------------------------------------------------


def resolve(target):
    if os.path.basename(os.path.normpath(target)) == "design-context":
        return target
    nested = os.path.join(target, "design-context")
    if os.path.isdir(nested):
        return nested
    return target


def check_directory(target, report, allow_placeholders):
    directory = resolve(target)
    if not os.path.isdir(directory):
        report.error(os.path.relpath(target), None, "no design-context/ directory here")
        return

    rel_dir = os.path.relpath(directory)
    for name in REQUIRED_FILES:
        if not os.path.exists(os.path.join(directory, name)):
            report.error(os.path.join(rel_dir, name), None, "required file is missing")

    if not os.path.exists(os.path.join(directory, "index.md")):
        return

    spec, listed, file_entries = check_index(directory, report, allow_placeholders)

    for name in listed:
        if not os.path.exists(os.path.join(directory, name)):
            report.error(
                os.path.join(rel_dir, "index.md"),
                None,
                "the manifest lists %s, which does not exist on disk" % name,
            )

    on_disk = sorted(
        n for n in os.listdir(directory)
        if n.endswith(".md") and n != "index.md" and os.path.isfile(os.path.join(directory, n))
    )
    for name in on_disk:
        if name not in listed:
            report.warning(
                os.path.join(rel_dir, name),
                None,
                "present but not listed in the manifest, so no agent will read it. "
                "List it or delete it.",
            )

    for name in sorted(os.listdir(directory)):
        full = os.path.join(directory, name)
        if os.path.isfile(full) and not name.endswith(".md"):
            report.error(
                os.path.join(rel_dir, name),
                None,
                "only markdown files are permitted in design-context/",
            )

    references = check_decisions(directory, spec, report)

    # A governed_by that names nothing is worse than no governed_by: it reads
    # as an answer and sends the agent to a decision that is not there.
    for entry in file_entries:
        reference = entry.get("governed_by")
        if not reference:
            continue
        if reference not in references:
            report.error(
                os.path.join(rel_dir, "index.md"),
                entry["__lines__"].get("governed_by", entry.get("__line__")),
                "%s: governed_by names %r, which is not an entry in decisions.md"
                % (entry.get("path"), reference),
            )


def main(argv):
    targets = []
    strict = False
    allow_placeholders = False
    quiet = False

    for arg in argv:
        if arg in ("-h", "--help"):
            sys.stdout.write(__doc__)
            return 0
        if arg == "--strict":
            strict = True
        elif arg == "--allow-placeholders":
            allow_placeholders = True
        elif arg == "--quiet":
            quiet = True
        elif arg.startswith("-"):
            sys.stderr.write("unknown option: %s\n" % arg)
            return 2
        else:
            targets.append(arg)

    if not targets:
        targets = ["."]

    report = Report()
    for target in targets:
        check_directory(target, report, allow_placeholders)

    if not quiet:
        for finding in report.findings:
            stream = sys.stderr if finding.level == "error" else sys.stdout
            stream.write(str(finding) + "\n")

    errors = report.count("error")
    warnings = report.count("warning")
    notes = report.count("note")

    checked = ", ".join(os.path.relpath(resolve(t)) for t in targets)
    summary = "%s: %d error%s, %d warning%s, %d note%s" % (
        checked,
        errors, "" if errors == 1 else "s",
        warnings, "" if warnings == 1 else "s",
        notes, "" if notes == 1 else "s",
    )
    sys.stdout.write(summary + "\n")

    if errors:
        return 1
    if strict and warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
