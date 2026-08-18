"""Turn the *regulatory* citation tags into links, without touching the prose.

``[R18]`` stays ``[R18]``.  What changes is that each document grows a generated block of
CommonMark *link reference definitions* at its foot::

    [R1]: #uslib-term_life-r1
    [REG-R18]: #uslib-reg-r18
    [std]: #uslib-std

A bare ``[R18]`` is then a shortcut reference link, and renders as one.  Definitions are
per-document, which is what makes the per-product numbering work: ``R1`` is a different
regulation in each product, and each document's block points at its own product's anchors
(USLIB-MERGE-PLAN.md D4/C11).

**``S#`` is not in that list, and that is the point.**  A primary product source is a
specification citation -- a brochure, a specimen policy, a prospectus -- not an authority
to be followed, so it is written plainly and reads as ``[S6]`` on the page, brackets and
all.  A regulatory tag is a link; a product-source tag is bracketed text.  One narrowing of
:data:`TAG` withdraws all three link mechanisms from ``S#`` together, so they cannot drift
apart, and an undefined shortcut reference is left as literal text by CommonMark (C8) --
which is what puts the brackets back.

Two further forms are handled here because they are not bare labels and so cannot be
covered by a definition (D5):

* **comma lists** -- ``[R3, R7]`` is split into ``[R3], [R7]``, after which both link;
* **pinpoint cites** -- ``[R1 §4.B]`` becomes an explicit inline link to the entry named by
  its leading tag, keeping the pinpoint text visible.

A tag is only ever defined if its anchor actually exists.  Tags used but not defined
anywhere are reported rather than pointed at a target that is not there -- that report is
the integrity check on the whole citation layer, and ``S#`` is still *checked* against the
anchors even though it is never defined, so a typo in one is still caught.

Usage::

    python tools/gen_citation_links.py lifelib/libraries/uslib --dry-run
    python tools/gen_citation_links.py lifelib/libraries/uslib
"""
import re
import sys
import pathlib
import collections

from mdspans import prose_spans


BEGIN = "<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->"
END = "<!-- END generated citation links -->"
BLOCK = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n*", re.S)

# The tags this tool links.  `S#` is deliberately absent: a primary product source is a
# specification citation, not an authority, and D4's mechanism is switched off for it here
# -- one narrowing that stops the definitions, the comma splitting and the pinpoint links
# together, so they cannot drift apart.  Everything downstream derives from this.
TAG = r'(?:R|REG-R)\d+[a-z]?'

# Every tag, `S#` included.  Only the repair below uses this: it has to recognise what
# earlier runs of this tool wrote, and those runs covered S.
ANY_TAG = r'(?:S|R|REG-R)\d+[a-z]?'
ANCHOR = re.compile(r'^\(([\w.-]+)\)=\s*$', re.M)
INLINE_CODE = re.compile(r'`[^`\n]*`')
# Link text may itself contain a bracketed marker -- [REG-R17; exact table mapping
# [unverified]](#...) -- so one level of nesting has to be allowed here, or a second run
# fails to recognise its own output as a link and wraps it again.
INLINE_LINK = re.compile(r'\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]\([^()]*\)')

BARE = re.compile(rf'\[({TAG}|std|unverified)\]')
# `S#` is resolved but never defined.  No definition is emitted for it any more, so this
# check is the *only* thing standing between an `[S99]` and a published document: the tag
# does not become a link, so nothing downstream has a link to follow and fail on.
#
# It reads whole bracketed runs rather than just the opening tag, because the corpus writes
# these three shapes and a leading-position pattern would only cover the first two:
#     [S6]                                    bare
#     [S6 §4.B]                               pinpoint
#     [S2, S3, S9 guarantee behavior; ...]    several tags in one bracket
# One level of nesting is allowed for the same reason it is in PINPOINT -- the pinpoint text
# may carry a `[std]` marker.
BRACKETED = re.compile(r'\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]')
SOURCE = re.compile(r'(?<![\w-])S(\d+[a-z]?)(?![\w-])')
COMMA_LIST = re.compile(rf'\[({TAG}(?:\s*,\s*{TAG})+)\]')
# The separator between a tag and its pinpoint is not always whitespace -- semicolons and
# dashes both occur -- and the pinpoint text may itself contain a bracketed marker, as in
# ``[REG-R17; exact table mapping [unverified]]``.
PINPOINT = re.compile(rf'\[({TAG})([\s,;:—–][^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*)\]')
# An earlier `split_comma_lists` bracketed each tag *and* then joined the bracketed tokens
# with the separator meant for bare ones, so `[S3, S7]` came out as `[S3]], [[S7]` -- one
# stray bracket on each side of every join.  It went unnoticed because the tags kept
# working: `[S3]` is still a shortcut reference, and the extra `]` and `[` merely sat
# beside it as text.  Withdrawing the `S#` definitions removes that cover and leaves the
# whole run as literal junk, so the 50 groups that reached the documents are normalised
# here rather than left for a reader to trip over.
# The lookbehind keeps this off ordinary double-bracketed text -- `[[X]], [[Y]]` ends in the
# same characters and is not this bug's output.  Nothing in the corpus matches either way;
# the guard is here so the repair cannot acquire a victim later.
MALFORMED_LIST = re.compile(rf'(?<!\[)\[{ANY_TAG}\](?:\], \[\[{ANY_TAG}\])+')


def map_prose(text, fn):
    """Apply ``fn`` to the prose regions of ``text``, leaving code blocks alone."""
    out, cursor = [], 0
    for start, end in prose_spans(text):
        out.append(text[cursor:start])
        out.append(fn(text[start:end]))
        cursor = end
    out.append(text[cursor:])
    return "".join(out)


def masked(chunk):
    """``chunk`` with inline code and existing inline links blanked to same-length filler.

    Positions are preserved so matches found in the mask apply to the real text.
    """
    chunk = INLINE_CODE.sub(lambda m: "`" * len(m.group(0)), chunk)
    return INLINE_LINK.sub(lambda m: "L" * len(m.group(0)), chunk)


def anchors_in(path):
    return set(ANCHOR.findall(path.read_text(encoding="utf-8")))


def targets_for(tag, product, lib):
    """Candidate anchors for a tag, best first.

    Two fallbacks, both drawn from how the corpus actually cites:

    * A bare ``[R41]`` in a product document means that product's R41 -- unless the product
      has no R41, in which case it means the cross-product library's, as in the deferred
      income annuity's ``verified from the Valuation Manual's VM-C index [R41]``.  Numbering
      is per product, so the product's own entry always wins when it exists.
    * A letter-suffixed tag like ``[R49b]`` is not a separate entry.  It marks a corroborating
      source *within* entry R49 -- the GAO rule report behind the SEC release -- so it lands
      on R49, where that corroboration is described.
    """
    if tag in ("std", "unverified"):
        return [f"{lib}-{tag}"]

    bare = tag[4:] if tag.startswith("REG-") else tag
    stem = bare.rstrip("abcdefghijklmnopqrstuvwxyz")

    out = []
    if not tag.startswith("REG-") and product is not None:
        out += [f"{lib}-{product}-{bare.lower()}", f"{lib}-{product}-{stem.lower()}"]
    out += [f"{lib}-reg-{bare.lower()}", f"{lib}-reg-{stem.lower()}"]
    return list(dict.fromkeys(out))


def target_for(tag, product, lib, available):
    """The first candidate anchor that exists, or None."""
    for candidate in targets_for(tag, product, lib):
        if candidate in available:
            return candidate
    return None


def split_comma_lists(text):
    """``text`` with malformed runs repaired and comma lists split.

    Returns ``(new_text, repairs)``.  Both rewrites are collected against a mask and
    applied in reverse, so inline code and existing inline links are left alone and the
    offsets stay valid as the chunk changes under them.
    """
    repairs = 0

    def fix(chunk):
        nonlocal repairs
        mask = masked(chunk)
        edits = [(m.start(), m.end(),
                  ", ".join(f"[{t}]" for t in re.findall(ANY_TAG, m.group(0))))
                 for m in MALFORMED_LIST.finditer(mask)]
        repairs += len(edits)
        for start, end, replacement in reversed(edits):
            chunk = chunk[:start] + replacement + chunk[end:]

        # Re-masked, because the repair above moved everything after it.
        mask = masked(chunk)
        edits = [(m.start(), m.end(),
                  ", ".join(f"[{t.strip()}]" for t in m.group(1).split(",")))
                 for m in COMMA_LIST.finditer(mask)]
        for start, end, replacement in reversed(edits):
            chunk = chunk[:start] + replacement + chunk[end:]
        return chunk

    return map_prose(text, fix), repairs


def linkify_pinpoints(text, product, lib, available):
    count = 0

    def fix(chunk):
        nonlocal count
        mask = masked(chunk)
        edits = []
        for m in PINPOINT.finditer(mask):
            target = target_for(m.group(1), product, lib, available)
            if target:
                edits.append((m.start(), m.end(), target))
        for start, end, target in reversed(edits):
            body = chunk[start:end]
            chunk = chunk[:start] + f"{body}(#{target})" + chunk[end:]
            count += 1
        return chunk

    return map_prose(text, fix), count


def used_tags(text):
    tags = set()

    def collect(chunk):
        for m in BARE.finditer(masked(chunk)):
            tags.add(m.group(1))
        return chunk

    map_prose(text, collect)
    return tags


def source_tags(text):
    """Every ``S#`` tag a document uses, wherever it sits in its bracket.

    Checked against the anchors, never defined -- see :data:`SOURCE`.
    """
    tags = set()

    def collect(chunk):
        for bracket in BRACKETED.finditer(masked(chunk)):
            for m in SOURCE.finditer(bracket.group(0)):
                tags.add(f"S{m.group(1)}")
        return chunk

    map_prose(text, collect)
    return tags


def main(argv):
    dry = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("-")]
    library = pathlib.Path(args[0] if args else "lifelib/libraries/uslib")
    # The directory *is* the library: uslib/ here, lifelib/libraries/uslib/ after the
    # merge, and uklib/ when the UK section follows.  Deriving the name any other way
    # would make the anchors and module paths disagree with where the files actually are.
    lib = library.name
    # `rglob` on a directory that is not there yields nothing rather than raising, and the
    # report that follows is all zeros -- which reads exactly like a corpus with nothing to
    # do.  After the libraries moved under `lifelib/libraries/`, the old top-level path is
    # the natural thing to type, so say so instead of exiting 0 having done nothing.
    if not (library / "products").is_dir():
        sys.exit(f"no library at {library} -- expected a products/ directory under it")

    available = set()
    for path in library.rglob("*.md"):
        if "_research" not in path.parts:
            available |= anchors_in(path)

    stats = collections.Counter()
    missing = collections.Counter()

    docs = [p for p in sorted(library.rglob("*.md")) if "_research" not in p.parts]
    for path in docs:
        product = path.parent.name if path.parent.parent.name == "products" else None
        text = original = path.read_text(encoding="utf-8")
        text = BLOCK.sub("", text).rstrip() + "\n"

        before = len(COMMA_LIST.findall(masked(text)))
        text, repairs = split_comma_lists(text)
        stats["comma lists split"] += before
        stats["malformed lists repaired"] += repairs

        text, n = linkify_pinpoints(text, product, lib, available)
        stats["pinpoint cites linked"] += n

        definitions = []
        for tag in sorted(used_tags(text), key=lambda t: (t[0].isalpha() and t[0].islower(), t)):
            target = target_for(tag, product, lib, available)
            if target:
                definitions.append(f"[{tag}]: #{target}")
            else:
                missing[f"{path.parent.name}/{path.name}: [{tag}]"] += 1

        # `S#` gets no definition, but it is still held to naming an entry that exists.
        for tag in sorted(source_tags(text)):
            stats["source tags checked"] += 1
            if not target_for(tag, product, lib, available):
                missing[f"{path.parent.name}/{path.name}: [{tag}]"] += 1

        if definitions:
            text = f"{text.rstrip()}\n\n{BEGIN}\n" + "\n".join(definitions) + f"\n{END}\n"
            stats["definitions written"] += len(definitions)
            stats["documents"] += 1

        if text != original and not dry:
            path.write_text(text, encoding="utf-8")

    for key in ("documents", "definitions written", "comma lists split",
                "pinpoint cites linked", "malformed lists repaired",
                "source tags checked"):
        print(f"  {stats[key]:5}  {key}")
    if missing:
        print(f"\n  {sum(missing.values())} tags used with no anchor "
              f"({len(missing)} distinct) -- left as plain text:")
        for s, n in missing.most_common(25):
            print(f"     {n:3}x  {s}")
    print(f"\n{'(dry run)' if dry else 'written'}")
    # Non-zero on an unresolvable tag, so this can gate.  It matters most for `S#`, which
    # is now the *only* place a bad source number is caught at all: the tag no longer
    # becomes a link, so `tools/check_anchors.py` cannot see it downstream -- it has no
    # link to follow and nothing to fail on.  Reporting alone would have left an `[S99]`
    # passing every check in the repository.
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
