"""Insert MyST targets above every citation entry, so citations have somewhere to land.

Two families of anchor, both namespaced by library because Sphinx labels are global and
``S1`` means a different source in every product (USLIB-MERGE-PLAN.md C11/D4):

===============================================  =========================================
``<lib>-<product>-s<n>`` / ``-r<n>``             each entry in ``products/<p>/sources.md``
``<lib>-reg-r<n>``                               each entry in the reference library
===============================================  =========================================

**Section-aware, and that is the whole difficulty.**  A product's ``sources.md`` also
reprints entries from the cross-product library under a *Cross-product regulatory
references* heading.  Those are aliases -- they are cited as ``[REG-R#]`` and must resolve
to the reference library's copy -- so they get no target here.  Giving them one would
create a second definition of the same reference under a product-local name, and the two
would drift.

Entry headings come in two spellings, ``### S1. Title`` and ``### S1 — Title``, split
across the twelve products (and the same split exists in ``uk/``), so both are matched and
the totals are the check that neither was missed.

Idempotent: a heading that already carries a target is left alone.

Usage::

    python tools/add_citation_anchors.py us --dry-run
    python tools/add_citation_anchors.py us
"""
import re
import sys
import pathlib
import collections


# "### S1. Title", "### S1 — Title", "#### R12a. Title".  REG-R entries never match:
# after the marker comes "REG-R151", whose second character is not a digit.
ENTRY = re.compile(r'^(#{2,4}) +(S|R)(\d+)([a-z]?)\s*(?:[.—–-]|$)')
H2 = re.compile(r'^## +(.*)$')
TARGET = re.compile(r'^\(([\w.-]+)\)=\s*$')
CROSS_PRODUCT = re.compile(r'cross-product|cross product', re.I)


def anchor_lines(text, name_for):
    """Insert ``(target)=`` above each entry heading.  Returns (new_text, inserted)."""
    out, inserted, section = [], 0, ""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if (m := H2.match(line)):
            section = m.group(1)
        entry = ENTRY.match(line)
        if entry and not CROSS_PRODUCT.search(section):
            # Look back past the blank line this inserts, or a re-run doubles every target.
            previous = next((ln for ln in reversed(out) if ln.strip()), "")
            if not TARGET.match(previous.strip()):
                target = name_for(entry.group(2), entry.group(3), entry.group(4))
                out.append(f"({target})=")
                out.append("")
                inserted += 1
        out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else ""), inserted


def main(argv):
    dry = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("-")]
    library = pathlib.Path(args[0] if args else "us")
    lib = f"{library.name}lib"

    counts = collections.Counter()

    for sources in sorted((library / "products").glob("*/sources.md")):
        product = sources.parent.name
        text = sources.read_text(encoding="utf-8")
        new, n = anchor_lines(
            text, lambda kind, num, suf: f"{lib}-{product}-{kind.lower()}{num}{suf}")
        counts[product] = n
        if new != text and not dry:
            sources.write_text(new, encoding="utf-8")

    refs = library / "references" / "regulatory-and-actuarial-references.md"
    text = refs.read_text(encoding="utf-8")
    new, n = anchor_lines(
        text, lambda kind, num, suf: f"{lib}-reg-{kind.lower()}{num}{suf}")
    counts["<reference library>"] = n
    if new != text and not dry:
        refs.write_text(new, encoding="utf-8")

    for name, n in sorted(counts.items()):
        print(f"  {n:4}  {name}")
    products_total = sum(v for k, v in counts.items() if not k.startswith("<"))
    print(f"\n  {products_total} product entries + {counts['<reference library>']} "
          f"reference-library entries{' (dry run)' if dry else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
