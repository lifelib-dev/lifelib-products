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
today and are left alone.

Usage::

    python tools/separate_citations.py us --dry-run
    python tools/separate_citations.py us
"""
import re
import sys
import pathlib
import collections


TAG = r'(?:S|R|REG-R)\d+[a-z]?'
BRACKET = re.compile(r'\[([^\[\]]*)\]')
FENCE = re.compile(r'^\s*(```|~~~)', re.M)

# A citation-ish bracket: a bare tag, a tag carrying a pinpoint or a comma list, or one of
# the two convention markers with or without a qualifier.
CITATION = re.compile(rf'^(?:{TAG}(?:[\s,][^\[\]]*)?|std(?:\s[^\[\]]*)?'
                      rf'|unverified(?:[\s,][^\[\]]*)?)$', re.S)


def prose_spans(text):
    """Yield (start, end) of the regions outside fenced code blocks."""
    edges, fenced = [0], False
    for m in FENCE.finditer(text):
        edges.append(m.start())
        fenced = not fenced
    edges.append(len(text))
    for i in range(len(edges) - 1):
        if i % 2 == 0:
            yield edges[i], edges[i + 1]


def separate(text):
    """Return (new_text, separated, list of unclassified adjacencies)."""
    keep, unknown = [], []
    result = []
    cursor = 0
    separated = 0

    for start, end in prose_spans(text):
        result.append(text[cursor:start])
        chunk = text[start:end]
        tokens = list(BRACKET.finditer(chunk))
        insert_at = set()
        for a, b in zip(tokens, tokens[1:]):
            if a.end() != b.start():
                continue
            if CITATION.match(a.group(1)) and CITATION.match(b.group(1)):
                insert_at.add(a.end())
                separated += 1
            else:
                unknown.append(f"[{a.group(1)}][{b.group(1)}]".replace("\n", " "))
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
    library = pathlib.Path(args[0] if args else "us")

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
