"""Turn the citation tags into links, without touching the prose.

``[S6]`` stays ``[S6]``.  What changes is that each document grows a generated block of
CommonMark *link reference definitions* at its foot::

    [S6]: #uslib-term_life-s6
    [REG-R18]: #uslib-reg-r18
    [std]: #uslib-std

A bare ``[S6]`` is then a shortcut reference link, and renders as one.  Definitions are
per-document, which is what makes the per-product numbering work: ``S1`` is Protective Life
in ``term_life`` and Symetra in ``universal_life``, and each document's block points at its
own product's anchors (USLIB-MERGE-PLAN.md D4/C11).

Two further forms are handled here because they are not bare labels and so cannot be
covered by a definition (D5):

* **comma lists** -- ``[S3, S7]`` is split into ``[S3], [S7]``, after which both link;
* **pinpoint cites** -- ``[R1 §4.B]`` becomes an explicit inline link to the entry named by
  its leading tag, keeping the pinpoint text visible.

A tag is only ever defined if its anchor actually exists.  Tags used but not defined
anywhere are reported rather than pointed at a target that is not there -- that report is
the integrity check on the whole citation layer.

Usage::

    python tools/gen_citation_links.py uslib --dry-run
    python tools/gen_citation_links.py uslib
"""
import re
import sys
import pathlib
import collections


BEGIN = "<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->"
END = "<!-- END generated citation links -->"
BLOCK = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n*", re.S)

TAG = r'(?:S|R|REG-R)\d+[a-z]?'
ANCHOR = re.compile(r'^\(([\w.-]+)\)=\s*$', re.M)
FENCE = re.compile(r'^\s*(```|~~~)', re.M)
INLINE_CODE = re.compile(r'`[^`\n]*`')
# Link text may itself contain a bracketed marker -- [REG-R17; exact table mapping
# [unverified]](#...) -- so one level of nesting has to be allowed here, or a second run
# fails to recognise its own output as a link and wraps it again.
INLINE_LINK = re.compile(r'\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]\([^()]*\)')

BARE = re.compile(rf'\[({TAG}|std|unverified)\]')
COMMA_LIST = re.compile(rf'\[({TAG}(?:\s*,\s*{TAG})+)\]')
# The separator between a tag and its pinpoint is not always whitespace -- semicolons and
# dashes both occur -- and the pinpoint text may itself contain a bracketed marker, as in
# ``[REG-R17; exact table mapping [unverified]]``.
PINPOINT = re.compile(rf'\[({TAG})([\s,;:—–][^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*)\]')


def prose_spans(text):
    """(start, end) of the regions outside fenced code blocks."""
    edges, = [[0]]
    for m in FENCE.finditer(text):
        edges.append(m.start())
    edges.append(len(text))
    for i in range(0, len(edges) - 1, 2):
        yield edges[i], edges[i + 1]


def map_prose(text, fn):
    """Apply ``fn`` to the prose regions of ``text``, leaving fenced code alone."""
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
    def fix(chunk):
        mask = masked(chunk)
        edits = [(m.start(), m.end(), "], [".join(
            f"[{t.strip()}]" for t in m.group(1).split(","))[1:-1])
            for m in COMMA_LIST.finditer(mask)]
        for start, end, replacement in reversed(edits):
            chunk = chunk[:start] + "[" + replacement + "]" + chunk[end:]
        return chunk
    return map_prose(text, fix)


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


def main(argv):
    dry = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("-")]
    library = pathlib.Path(args[0] if args else "uslib")
    # The directory *is* the library: uslib/ here, lifelib/libraries/uslib/ after the
    # merge, and uklib/ when the UK section follows.  Deriving the name any other way
    # would make the anchors and module paths disagree with where the files actually are.
    lib = library.name

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
        text = split_comma_lists(text)
        stats["comma lists split"] += before

        text, n = linkify_pinpoints(text, product, lib, available)
        stats["pinpoint cites linked"] += n

        definitions = []
        for tag in sorted(used_tags(text), key=lambda t: (t[0].isalpha() and t[0].islower(), t)):
            target = target_for(tag, product, lib, available)
            if target:
                definitions.append(f"[{tag}]: #{target}")
            else:
                missing[f"{path.parent.name}/{path.name}: [{tag}]"] += 1

        if definitions:
            text = f"{text.rstrip()}\n\n{BEGIN}\n" + "\n".join(definitions) + f"\n{END}\n"
            stats["definitions written"] += len(definitions)
            stats["documents"] += 1

        if text != original and not dry:
            path.write_text(text, encoding="utf-8")

    for key in ("documents", "definitions written", "comma lists split",
                "pinpoint cites linked"):
        print(f"  {stats[key]:5}  {key}")
    if missing:
        print(f"\n  {sum(missing.values())} tags used with no anchor "
              f"({len(missing)} distinct) -- left as plain text:")
        for s, n in missing.most_common(25):
            print(f"     {n:3}x  {s}")
    print(f"\n{'(dry run)' if dry else 'written'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
