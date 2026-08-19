"""Which regions of a markdown document are verbatim, decided by the real parser.

Every tool that rewrites citations has to know where the code is, because a citation
inside a code block is *displayed*, not resolved: a link reference definition does not
reach it, and an inserted ``(#anchor)`` shows up as literal text on the page.

A regex covers fenced code and stops there.  CommonMark also has **indented** code -- a
four-space run opening after a blank line -- and this corpus is full of it: the technical
notes lay their recursions out as indented blocks, and 47 of those blocks carry citation
tags.  In ``uslib`` all but one of them is a bare ``[S1]``, which is inert either way, so
the gap all but never showed: the exception is ``immediate_annuity/technical-notes.md``,
where P5 rewrote a pinpoint inside an indented block and the page printed the raw
``](#uslib-immediate_annuity-s5)`` at the reader until it was reverted.  In ``uklib`` they
carry pinpoint cites throughout -- ``[S2 §6]``, ``[S1 p11]``, ``[S5 §7.1.4]`` -- which is
the one form that rewrites the text, so there the gap is visible corruption at scale.  That
asymmetry is USLIB-MERGE-PLAN.md's own warning about D5: uk has roughly twice the pinpoint
cites of us despite being half the size.

Telling indented code from an indented list continuation is not a heuristic worth writing
by hand -- ``- item`` followed by a blank line and four spaces is a paragraph in that item,
not code -- so this asks markdown-it, which is the parser MyST is built on and is already
installed as its dependency.  Same reasoning as ``tools/doccheck.py`` running the real
``conf.py``: ask the thing that will actually render the page.

Fenced directives (```{note}, ```{list-table}) count as code here, exactly as they did
under the regex this replaces.  Their content is not citation-processed today and this
keeps it that way.
"""
from markdown_it import MarkdownIt


_MD = MarkdownIt("commonmark")


def code_lines(text):
    """0-based line numbers belonging to a fenced or indented code block."""
    lines = set()
    for token in _MD.parse(text):
        if token.type in ("fence", "code_block") and token.map:
            lines.update(range(*token.map))
    return lines


def prose_spans(text):
    """Yield ``(start, end)`` character offsets of the regions outside code blocks.

    The spans tile the document in order, so a caller can rebuild it by interleaving the
    untouched gaps -- which is what every caller does.
    """
    code = code_lines(text)
    lines = text.splitlines(keepends=True)

    offset, start, run = 0, None, False
    for n, line in enumerate(lines):
        if n in code:
            if run:
                yield start, offset
                run = False
        elif not run:
            start, run = offset, True
        offset += len(line)
    if run:
        yield start, len(text)
    elif not lines:
        yield 0, 0
