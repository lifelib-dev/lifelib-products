"""Separate adjacent citation tags, before they become links.

``[S2][S3]`` is not two citations to CommonMark.  It is a **full reference link**: link
text ``S2``, link label ``S3``.  Today both are undefined so the run renders as literal
text and nobody notices.  The moment P5 adds the link definitions, every one of these
collapses into a single link labelled with the first tag and pointing at the second -- the
first citation silently disappears (USLIB-MERGE-PLAN.md C7/D4).

So each adjacency gets one space.  ``[S2] [S3]`` is two shortcut references, which is what
the text always meant.

Only *citation-ish* brackets are separated, never a blind ``][`` substitution: the corpus
also contains ``[(1+C)/(1+D)]``, ``[N]``, ``[Contract]`` and similar prose brackets that
must not be touched.  Anything adjacent that this cannot classify is reported for a human
rather than guessed at.

Scope is rendered documents only.  ``_research/`` is out of the Sphinx build under D6 and
never receives link definitions, so its adjacencies stay literal exactly as they read
today and are left alone.  Code blocks are left alone for the same reason and are found
the same way the renderer finds them -- see :mod:`mdspans`.

Usage::

    python tools/separate_citations.py uslib --dry-run
    python tools/separate_citations.py uslib
"""
import re
import sys
import pathlib
import collections

from mdspans import prose_spans


TAG = r'(?:S|R|REG-R)\d+[a-z]?'

# A citation-ish bracket: a bare tag, a tag carrying a pinpoint or a comma list, or one of
# the two convention markers with or without a qualifier.  The tail is deliberately
# permissive about brackets, because a pinpoint often carries a nested marker --
# ``[REG-R64 — **[unverified]**]`` and ``[REG-R34 — ..., summary-based]`` both occur.
# The separator after the tag is likewise not just whitespace: ``[REG-R17; exact table
# mapping [unverified]]`` uses a semicolon, and a stricter pattern leaves it behind.
SEP = r'[\s,;:—–]'
CITATION = re.compile(
    rf'^(?:{TAG}(?:{SEP}.*)?|std(?:{SEP}.*)?|unverified(?:{SEP}.*)?)$', re.S)


class Span:
    """A top-level bracketed run, with the text between its brackets."""

    __slots__ = ("start", "end", "body")

    def __init__(self, start, end, body):
        self.start, self.end, self.body = start, end, body


def brackets(text):
    """Top-level ``[...]`` spans, tracking nesting.

    A regex cannot do this: ``[REG-R64 — **[unverified]**]`` is one citation containing
    another marker, and a non-nesting scan sees only the inner one -- so the adjacency that
    follows the *outer* bracket goes unnoticed.  Those are the ones that survived the first
    pass and had to be found by hand.
    """
    spans, stack = [], []
    for i, ch in enumerate(text):
        if ch == "[":
            stack.append(i)
        elif ch == "]" and stack:
            start = stack.pop()
            if not stack:
                spans.append(Span(start, i + 1, text[start + 1:i]))
    return spans


def separate(text):
    """Return (new_text, separated, list of unclassified adjacencies)."""
    unknown = []
    result = []
    cursor = 0
    separated = 0

    for start, end in prose_spans(text):
        result.append(text[cursor:start])
        chunk = text[start:end]
        tokens = brackets(chunk)
        insert_at = set()
        for a, b in zip(tokens, tokens[1:]):
            if a.end != b.start:
                continue
            if CITATION.match(a.body) and CITATION.match(b.body):
                insert_at.add(a.end)
                separated += 1
            else:
                unknown.append(f"[{a.body}][{b.body}]".replace("\n", " "))
        out, last = [], 0
        for pos in sorted(insert_at):
            out.append(chunk[last:pos])
            out.append(" ")
            last = pos
        out.append(chunk[last:])
        result.append("".join(out))
        cursor = end

    result.append(text[cursor:])
    return "".join(result), separated, unknown


def main(argv):
    dry = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("-")]
    library = pathlib.Path(args[0] if args else "uslib")

    total, unknown_all = 0, collections.Counter()
    files = 0
    for path in sorted(library.rglob("*.md")):
        if "_research" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        new, n, unknown = separate(text)
        # A run of three tags needs two passes: separating the first pair shifts the
        # second, and the scan above only sees non-overlapping neighbours once.
        while True:
            new2, extra, _ = separate(new)
            if not extra:
                break
            new, n = new2, n + extra
        total += n
        unknown_all.update(unknown)
        if new != text:
            files += 1
            if not dry:
                path.write_text(new, encoding="utf-8")

    print(f"{total} separators inserted across {files} files"
          f"{' (dry run)' if dry else ''}")
    if unknown_all:
        print("\nadjacencies left for manual review:")
        for s, n in unknown_all.most_common():
            print(f"  {n:3}x  {s}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
