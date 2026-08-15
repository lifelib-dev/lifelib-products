"""Structural lint for the country-library markdown, ahead of the MyST build.

Catches the CommonMark/MyST hazards that render *wrongly and silently* rather than
failing the build:

- a ``---`` line directly under a paragraph line, which is a setext H2, not a rule;
- non-consecutive heading level increases, which MyST warns about;
- a document without exactly one H1, which gives the toctree no title to use;
- bracket adjacencies ``][``, which become a single reference link the moment the
  citation link definitions of P5 exist -- see USLIB-MERGE-PLAN.md D4.

Run over a country directory::

    python tools/md_lint.py uslib
    python tools/md_lint.py uslib uk        # both

Exits non-zero if anything is reported, so it can gate a commit.
"""
import re
import sys
import pathlib


FENCE = re.compile(r'^\s*(```|~~~)')
HEADING = re.compile(r'^(#{1,6}) +(\S.*)$')
RULE = re.compile(r'^-{3,}\s*$')
INLINE_CODE = re.compile(r'`[^`\n]*`')
ADJACENCY = re.compile(r'\]\[')
INLINE_LINK = re.compile(r'\[[^\]]*\]\([^)]*\)')


def prose_lines(text):
    """The document's lines with fenced code blanked out, index-aligned to the original."""
    out, in_fence = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return out


def is_rendered(path):
    """True for documents the Sphinx build will see.

    ``_research/`` is shipped but excluded from the build (USLIB-MERGE-PLAN.md D6), and
    it never receives citation link definitions, so its bracket adjacencies stay literal
    text exactly as they read today.  The structural checks still apply to it; the
    adjacency check does not.
    """
    return "_research" not in path.parts


def check(path):
    """Yield ``(line_number, message)`` for one file."""
    lines = prose_lines(path.read_text(encoding="utf-8"))

    headings = [(n, len(m.group(1)))
                for n, line in enumerate(lines, 1)
                if (m := HEADING.match(line))]

    h1 = [n for n, level in headings if level == 1]
    if len(h1) != 1:
        yield 1, f"expected exactly one H1, found {len(h1)}"

    previous = 0
    for n, level in headings:
        if previous and level > previous + 1:
            yield n, f"heading level jumps H{previous} -> H{level}"
        previous = level

    for n, line in enumerate(lines, 1):
        if not RULE.match(line):
            continue
        above = lines[n - 2] if n >= 2 else ""
        # A rule under a blank line is a rule; under text it is a setext H2, and
        # under a list item or table row it belongs to that block.
        if above.strip() and not above.lstrip().startswith(("#", "|", "-", "*", ">")):
            yield n, "'---' directly under text renders that text as an H2 heading"

    if is_rendered(path):
        for n, line in enumerate(lines, 1):
            stripped = INLINE_CODE.sub("`c`", INLINE_LINK.sub("LINK", line))
            for _ in ADJACENCY.finditer(stripped):
                yield n, "bracket adjacency '][' -- becomes one reference link once P5 lands"


def main(argv):
    roots = [pathlib.Path(a) for a in argv] or [pathlib.Path("us")]
    counts, total = {}, 0
    for root in roots:
        for path in sorted(root.rglob("*.md")):
            for line_no, message in check(path):
                key = message.split("--")[0].strip().rstrip(":")
                key = re.sub(r'H\d+ -> H\d+', 'H<n> -> H<m>', key)
                key = re.sub(r'found \d+', 'found <n>', key)
                counts[key] = counts.get(key, 0) + 1
                total += 1
                if counts[key] <= 6:
                    print(f"{path}:{line_no}: {message}")
                elif counts[key] == 7:
                    print(f"{path}: ... further '{key}' reports suppressed")

    print()
    for key, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"{n:6}  {key}")
    print(f"{total:6}  TOTAL")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
