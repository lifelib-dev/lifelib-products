"""Check that every internal anchor link in the built HTML **arrives**.

``sphinx-build -n -W`` proves the links exist.  It does not prove they land: an anchor is
just a string, and a link to an id no page carries is a silent no-op in the browser.  With
12,000-odd citation links, all generated from the same template, a systematic mismatch would
look right everywhere and work nowhere.

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
TAG = re.compile(r'\[(?:(?:S|R|REG-R)\d+[a-z]?|std|unverified)\]')

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
    # one.  A bare tag still sitting in the rendered prose is a citation that did not link.
    #
    # Autodoc pages are excluded, and deliberately.  They render the models' docstrings,
    # which are RST: `[S1]` there has no link meaning, no definition block reaches it, and
    # D4 covers the documents.  Both libraries carry ~2,350 such tags and always have.  A
    # page is autodoc if `automodule` gave it a `module-…` id, which no document page has.
    plain, in_docstrings = collections.Counter(), 0
    for path, page in pages.items():
        n = len(TAG.findall("".join(page.prose)))
        if not n:
            continue
        if any(i.startswith("module-") for i in page.ids):
            in_docstrings += n
        else:
            plain[path.relative_to(root)] = n
    print(f"\n  {sum(plain.values())} bare citation tags left as plain text on document "
          f"pages ({in_docstrings} in model docstrings, out of scope)")
    for path, n in plain.most_common(15):
        print(f"     {n:4}x  {path}")

    return 1 if broken or plain else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
