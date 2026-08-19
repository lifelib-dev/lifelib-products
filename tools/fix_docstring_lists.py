"""Turn the aligned two-column blocks in model docstrings into RST definition lists.

A cells whose argument is a timing string or a benefit kind documents its values like this,
which reads perfectly in an editor::

    ``"BEF_DECR"``  the start of the month, before any decrement.
    ``"BEF_SURR"``  after deaths, before surrenders - the processing order is
                    **death before surrender**.
    ``"AFT_DECR"``  the end-of-month count.

RST has no aligned two-column construct, so docutils reads that as a paragraph followed by
an over-indented block.  Two outcomes, both wrong, and which one you get depends on
something the author cannot see:

* if the block is one term with a wrapped description, it parses **silently** as a
  definition list whose *term* is the whole first line -- description included;
* if it is several terms and any of them wraps, it is an "Unexpected indentation" error
  and the alignment is lost anyway.

uklib has 58 of these lines in 21 docstrings and 9 of them warn.  uslib has 14 more in 10
docstrings, none of which warn -- they are all the silent first kind, which is why a build
at zero warnings does not mean this is absent.

The construct RST does have is the definition list, and it is what the rest of the corpus
already uses::

    ``"BEF_DECR"``
        the start of the month, before any decrement.

    ``"BEF_SURR"``
        after deaths, before surrenders - the processing order is
        **death before surrender**.

Only inline-literal terms are rewritten.  A bold lead-in followed by wide spacing --
``**Floored at zero.**   The charges are deducted...`` -- is a sentence, not a term, and
renders correctly as the paragraph it is.

Usage::

    python tools/fix_docstring_lists.py lifelib/libraries/uklib --dry-run
    python tools/fix_docstring_lists.py lifelib/libraries/uklib
"""
import re
import sys
import pathlib
import collections


# A term is one or more inline literals; the description begins after two or more spaces on
# the same line.  Bold is deliberately excluded -- see the module docstring.
TERM = re.compile(r'^(\s+)(``[^`]+``(?:\s+``[^`]+``)*)(\s{2,})(\S.*)$')


def group_at(lines, start):
    """The run of aligned items beginning at ``lines[start]``.

    Returns ``(items, end)`` where each item is ``(term, [description lines])`` and ``end``
    is the index one past the run.  An item continues through every following line indented
    deeper than the term; a blank line or a line at the term's own indent that is not
    itself a term ends the run.
    """
    base = len(lines[start]) - len(lines[start].lstrip())
    items, i = [], start
    while i < len(lines):
        match = TERM.match(lines[i])
        if not match or len(match.group(1)) != base:
            break
        body = [match.group(4)]
        i += 1
        while i < len(lines) and lines[i].strip() and not TERM.match(lines[i]):
            if len(lines[i]) - len(lines[i].lstrip()) <= base:
                break
            body.append(lines[i].strip())
            i += 1
        items.append((match.group(2), body))
    return items, i


def process(text):
    """Return ``(new_text, groups_rewritten)``."""
    lines = text.splitlines()
    out, i, rewritten = [], 0, 0

    while i < len(lines):
        if not TERM.match(lines[i]):
            out.append(lines[i])
            i += 1
            continue

        base = len(lines[i]) - len(lines[i].lstrip())
        items, end = group_at(lines, i)
        pad = " " * base
        for n, (term, body) in enumerate(items):
            if n:
                out.append("")
            out.append(f"{pad}{term}")
            out.extend(f"{pad}    {line}" for line in body)
        rewritten += 1
        i = end

    return "\n".join(out) + ("\n" if text.endswith("\n") else ""), rewritten


def main(argv):
    dry = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("-")]
    library = pathlib.Path(args[0] if args else "lifelib/libraries/uklib")

    total = collections.Counter()
    for path in sorted((library / "products").rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        new, n = process(text)
        if n:
            total[str(path)] = n
            if not dry:
                path.write_text(new, encoding="utf-8")
    for path, n in total.items():
        print(f"  {n:3}  {path}")
    print(f"\n{sum(total.values())} blocks converted to definition lists"
          f"{' (dry run)' if dry else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
