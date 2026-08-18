"""Structural lint for the country-library markdown, ahead of the MyST build.

Catches the CommonMark/MyST hazards that render *wrongly and silently* rather than
failing the build:

- a ``---`` line directly under a paragraph line, which is a setext H2, not a rule;
- non-consecutive heading level increases, which MyST warns about;
- a document without exactly one H1, which gives the toctree no title to use;
- bracket adjacencies ``][``, which CommonMark reads as one full reference link -- text
  from the first pair, target from the second -- swallowing the first citation whole.

That last check matters *more* now that ``[S#]`` no longer links, not less.  It would be
easy to read the withdrawal of the ``S`` definitions as removing the hazard; it removes it
only for ``S``-on-``S``.  ``[S1][R2]`` still collapses, because ``R2`` still has a
definition, and it collapses into a link labelled ``S1`` pointing at R2's entry -- losing
the S1 citation silently.  Every ``R``/``REG-R`` combination is untouched too.  Both
libraries are at zero adjacencies and this is what holds them there.

Run over a country directory::

    python tools/md_lint.py lifelib/libraries/uslib
    python tools/md_lint.py lifelib/libraries/uslib lifelib/libraries/uklib   # both

Exits non-zero if anything is reported, so it can gate a commit.
"""
import re
import sys
import pathlib

from mdspans import code_lines


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
    text = path.read_text(encoding="utf-8")
    lines = prose_lines(text)
    # The structural checks read the fence-blanked lines above.  The adjacency check
    # needs the *indented* code blocks out too: an adjacency there is displayed, never
    # resolved, so P5 cannot turn it into a link and there is nothing to separate.
    code = code_lines(text)

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
            if n - 1 in code:
                continue
            stripped = INLINE_CODE.sub("`c`", INLINE_LINK.sub("LINK", line))
            for _ in ADJACENCY.finditer(stripped):
                yield n, "bracket adjacency '][' -- CommonMark reads this as one reference link"


def main(argv):
    roots = [pathlib.Path(a) for a in argv] or [pathlib.Path("lifelib/libraries/uslib")]
    # A gate that cannot find its input must not report success.  `rglob` on a missing
    # directory yields nothing, `total` stays 0, and "0 TOTAL" reads exactly like a clean
    # library -- the same silent pass `tools/doccheck.py` guards against at its own end.
    if missing := [r for r in roots if not r.is_dir()]:
        sys.exit(f"no directory at {', '.join(str(r) for r in missing)}")
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
