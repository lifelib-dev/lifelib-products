"""Revert the ``[S#]`` pinpoint cites to plain text, leaving ``[R#]``/``[REG-R#]`` alone.

``tools/gen_citation_links.py`` builds its three link mechanisms off one :data:`TAG`
pattern, and narrowing that pattern is enough to stop it *emitting* anything for ``S#``:
the definition blocks are rebuilt wholesale on every run, so the ``[S#]:`` lines simply
stop being written.

Pinpoint cites are the exception, and the reason this file exists.  A pinpoint cite is not
a bare label -- ``[S4 p.12]`` cannot be covered by a link reference definition (D5) -- so
the generator materialised it as an **explicit inline link** in the source::

    [S4 p.12](#uslib-term_life-s4)

That edit is already in the documents.  Narrowing :data:`TAG` stops new ones being written
but does not undo the old ones, so they are reverted here, once::

    [S4 p.12](#uslib-term_life-s4)   ->   [S4 p.12]

**What is in scope.**  A link is reverted only when *both* halves say "primary product
source": the target is a product's ``s``-anchor, and the link text opens with that same
``S<n>``.  Requiring both is what keeps the pass off the four ``[below](#…)`` navigation
links in ``whole_life/model.md`` and the four cross-document links on ``uklib/index.md`` --
including ``#uslib-one-shape`` and ``#uslib-shared-vocabulary``, D8's shared rulings, which
are ordinary prose links that happen to point at an anchor.

**Why this reads the whole file and not just the prose.**  ``tools/mdspans.py`` keeps the
generator out of code blocks, but one of these links was written before it did and sits
inside an indented block, where markdown is *displayed* rather than resolved -- so the page
prints the raw ``](#uslib-immediate_annuity-s5)`` at the reader.  Reverting there restores
the line the author wrote.  It is counted separately so the number stays visible.

This is a one-time pass in the sense that it has one corpus to correct, but it is written
as a tool rather than done by hand for the same reason the definitions are generated: so
the edit can be re-derived and checked, not just believed.  Run twice it is a no-op.

Usage::

    python tools/unlink_spec_citations.py lifelib/libraries/uslib --dry-run
    python tools/unlink_spec_citations.py lifelib/libraries/uslib
"""
import re
import sys
import pathlib
import collections

from mdspans import code_lines


# One level of bracket nesting is allowed in the link text, and it is not decorative: six
# of these cites carry a ``[std]`` or ``[unverified]`` marker inside the pinpoint, as in
# ``[S7; R1 example 7; formula **[std]**]``.  ``re.S`` because twelve of them wrap across
# source lines, which is also why a per-line grep undercounts them.
LINK = re.compile(r'\[([^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*)\]\((#[^()]*)\)', re.S)

# A product source anchor: ``#uslib-term_life-s4``.  The reference library's
# ``#uslib-reg-r18`` and plain targets like ``#uslib-one-shape`` both fail this
# deliberately.
S_ANCHOR = re.compile(r'^#(?:uslib|uklib)-[a-z_]+-s(\d+[a-z]?)$')

# The text has to open with the tag it points at, which is the form the generator wrote.
S_LEAD = re.compile(r'^S(\d+[a-z]?)\b')


def revert(text, code):
    """``text`` with its S-anchor pinpoint links reduced to ``[text]``.

    Returns ``(new_text, sites)``, each site ``(line_number, in_code, first_line_of_text)``.
    """
    sites, edits = [], []
    for m in LINK.finditer(text):
        body, target = m.group(1), m.group(2)
        anchor = S_ANCHOR.match(target)
        lead = S_LEAD.match(body)
        # Both halves must name the same source entry.  Anything else is either not a
        # citation or not this tool's output, and is left for a human to look at.
        if not (anchor and lead and anchor.group(1) == lead.group(1)):
            continue
        line = text.count("\n", 0, m.start())
        sites.append((line + 1, line in code, body.split("\n")[0][:60]))
        edits.append((m.start(), m.end(), f"[{body}]"))

    for start, end, replacement in reversed(edits):
        text = text[:start] + replacement + text[end:]
    return text, sites


def main(argv):
    dry = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("-")]
    library = pathlib.Path(args[0] if args else "lifelib/libraries/uslib")
    # `rglob` on a directory that is not there yields nothing rather than raising, which
    # would report "0 reverted" and exit 0 -- indistinguishable from a finished corpus.
    if not (library / "products").is_dir():
        sys.exit(f"no library at {library} -- expected a products/ directory under it")

    stats = collections.Counter()
    in_code = []

    for path in sorted(library.rglob("*.md")):
        if "_research" in path.parts:
            continue
        original = path.read_text(encoding="utf-8")
        text, sites = revert(original, code_lines(original))
        if not sites:
            continue
        stats["documents"] += 1
        stats["pinpoint cites reverted"] += len(sites)
        for line, code, snippet in sites:
            if code:
                stats["of which inside code blocks"] += 1
                in_code.append(f"{path.as_posix()}:{line}  [{snippet}]")
        if text != original and not dry:
            path.write_text(text, encoding="utf-8")

    for key in ("documents", "pinpoint cites reverted", "of which inside code blocks"):
        print(f"  {stats[key]:5}  {key}")
    for line in in_code:
        print(f"     {line}")
    print(f"\n{'(dry run)' if dry else 'written'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
