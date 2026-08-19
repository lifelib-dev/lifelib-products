"""Check that every internal anchor link in the built HTML **arrives**.

``sphinx-build -n -W`` proves the links exist.  It does not prove they land: an anchor is
just a string, and a link to an id no page carries is a silent no-op in the browser.  With
16,000-odd internal anchor links across the two libraries -- some 5,300 of them citation
links, all generated from the same template -- a systematic mismatch would look right
everywhere and work nowhere.

The mismatch to watch for is real.  Sphinx **normalises label underscores to hyphens** when
it emits ids, so the MyST target ``(uklib-term_assurance-s1)=`` becomes
``id="uklib-term-assurance-s1"`` in the HTML.  A check written against the label text --
against what the generator wrote into the markdown -- passes while every link goes nowhere.
So this reads the ids out of the built pages and nothing else.

Run it against a build tree::

    python tools/doccheck.py --keep
    python tools/check_anchors.py doc/build/check
"""
import collections
import html.parser
import re
import sys
import pathlib
import urllib.parse


# A bare citation tag, which is exactly the form that should have become a link.  Qualified
# forms -- ``[std illustrative]``, ``[REG-R17 §3]`` -- are deliberately not bare labels and
# are out of scope here, as they are for the generator (D5a).
#
# The two families are counted apart because they are now meant to render differently.  A
# regulatory tag must be a link, so one left as text is a fault.  A product-source tag must
# *not* be a link -- ``[S6]`` reads as bracketed text on the page -- so counting those is a
# report, not a complaint, and the number is expected to be large.
LINKED = re.compile(r'\[(?:(?:R|REG-R)\d+[a-z]?|std|unverified)\]')
# Both forms a source tag is written in: bare ``[S6]`` and pinpoint ``[S6 §4.B]``.  The
# pinpoints matter here -- 512 of them were reverted from links to text -- and a pattern
# anchored on ``]`` alone would miss every one.
SOURCE = re.compile(r'\[S\d+[a-z]?(?=[\]\s,;:—–])')
# Link syntax that reached the page as text.  If ``](#anchor)`` is visible in the rendered
# prose then the link did not parse, and no amount of checking ids will notice: there is no
# ``<a>`` to follow, so it is not among the links counted above and cannot be "broken".
# This is how a pinpoint carrying a nested marker fails -- ``[REG-R34 — ... [unverified]]``
# -- because CommonMark forbids a link inside link text, so the inner marker links and the
# outer pinpoint is left as literal characters.
RAW_LINK = re.compile(r'\]\(#[^()\s]*\)')

# Where a tag is *meant* to read as text: inside code, and inside the generated definition
# block, which Sphinx does not render but which the conventions tables quote.
OPAQUE = {"a", "code", "pre", "tt", "kbd", "samp"}


class Page(html.parser.HTMLParser):
    """Every ``id`` a page carries, every internal link it makes, and its plain prose."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.prose = []
        self._opaque = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if (value := attrs.get("id")):
            self.ids.add(value)
        # Sphinx also emits bare <span id="..."> and <section id="...">, both caught above.
        # Footnote back-references use name= on <a>, which is an id for fragment purposes.
        if tag == "a" and (name := attrs.get("name")):
            self.ids.add(name)
        if tag == "a" and (href := attrs.get("href")):
            self.links.append(href)
        if tag in OPAQUE:
            self._opaque += 1

    def handle_endtag(self, tag):
        if tag in OPAQUE and self._opaque:
            self._opaque -= 1

    def handle_data(self, data):
        if not self._opaque:
            self.prose.append(data)


def main(argv):
    root = pathlib.Path(argv[0] if argv else "doc/build/check").resolve()
    if not root.is_dir():
        print(f"no build tree at {root}")
        return 2

    pages = {}
    for path in sorted(root.rglob("*.html")):
        page = Page()
        page.feed(path.read_text(encoding="utf-8", errors="replace"))
        pages[path.resolve()] = page

    resolving = collections.Counter()
    broken = []
    for path, page in pages.items():
        for href in page.links:
            if "#" not in href:
                continue
            target, _, anchor = href.partition("#")
            if not anchor or urllib.parse.urlparse(href).scheme:
                continue
            where = path if not target else (path.parent / urllib.parse.unquote(target))
            where = where.resolve()
            anchor = urllib.parse.unquote(anchor)
            if where not in pages:
                broken.append((path, href, "no such page"))
            elif anchor not in pages[where].ids:
                broken.append((path, href, "no such id on target page"))
            else:
                # Group by library, so each one's citation layer is counted on its own.
                parts = where.relative_to(root).parts
                resolving["/".join(parts[:2]) if parts[0] == "libraries"
                          else parts[0]] += 1

    total = sum(resolving.values())
    for group, n in sorted(resolving.items()):
        print(f"  {n:6}  {group}")
    print(f"\n  {total} internal anchor links resolve, {len(broken)} broken")
    for path, href, why in broken[:30]:
        print(f"     {path.relative_to(root)} -> {href}   ({why})")
    if len(broken) > 30:
        print(f"     ... and {len(broken) - 30} more")

    # The other half of the claim: a link that arrives is no use if the tag never became
    # one.  A bare regulatory tag still sitting in the rendered prose is a citation that
    # did not link.
    #
    # Autodoc pages are excluded, and deliberately.  They render the models' docstrings,
    # which are RST: `[R1]` there has no link meaning, no definition block reaches it, and
    # D4 covers the documents.  Both libraries carry ~2,350 such tags and always have.
    #
    # "Autodoc page" has to mean the page `automodule` built, not merely a page carrying a
    # `module-…` id: each library's own `index.md` opens with a ```{module}``` directive
    # and so carries a bare `module-uslib`, which would exempt the two landing pages from
    # this check -- and they are documents, with `[std]` and `[unverified]` tags on them.
    # `automodule` ids are dotted (`module-uslib.products.term_life.Term_US_A`) because
    # they name a submodule; the directive's is not.  That is the discriminator.
    plain, sources, in_docstrings = collections.Counter(), collections.Counter(), 0
    unparsed = collections.Counter()
    for path, page in pages.items():
        prose = "".join(page.prose)
        if n := len(RAW_LINK.findall(prose)):
            unparsed[path.relative_to(root)] = n
        linked, source = len(LINKED.findall(prose)), len(SOURCE.findall(prose))
        if not (linked or source):
            continue
        if any("." in i for i in page.ids if i.startswith("module-")):
            in_docstrings += linked + source
        else:
            if linked:
                plain[path.relative_to(root)] = linked
            if source:
                sources[path.relative_to(root)] = source

    print(f"\n  {sum(sources.values())} product-source tags read as text on document pages "
          f"-- expected: [S#] is not a link")
    print(f"  {sum(plain.values())} regulatory tags left as plain text on document "
          f"pages ({in_docstrings} tags in model docstrings, out of scope)")
    for path, n in plain.most_common(15):
        print(f"     {n:4}x  {path}")

    # Enforced.  These are links that never parsed, so they are invisible to every other
    # check in the repository: `sphinx-build -n -W` sees valid markup, and the count above
    # counts `<a>` elements, of which a failed link has none.  The corpus carried eighteen
    # of them -- pinpoints whose text nested a `[std]`/`[unverified]` marker, which
    # CommonMark resolves in favour of the inner marker -- until this scan found them.  The
    # count is zero now, `PINPOINT` in tools/gen_citation_links.py no longer wraps a
    # pinpoint that would produce one, and this keeps it that way.
    if unparsed:
        print(f"\n  {sum(unparsed.values())} links did not parse and printed their raw "
              f"markup on the page -- move the nested [std]/[unverified] marker out of the "
              f"pinpoint text and put it after the link")
        for path, n in unparsed.most_common(15):
            print(f"     {n:4}x  {path}")

    return 1 if broken or plain or unparsed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
