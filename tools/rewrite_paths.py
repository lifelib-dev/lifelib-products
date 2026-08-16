"""Rewrite intra-library path references for the uslib layout.

Two things change under P1: the product slugs are underscored, and each model moved from
``<lib>/models/<slug>/`` to ``<lib>/products/<slug>/`` beside the documents that specify
it.  Every path string in the models, the tests and the prose has to follow.

**Paths become library-root-relative.**  ``us/_research/term-life.md`` becomes
``_research/term-life.md``, not ``uslib/_research/term-life.md`` as the first draft of the
plan proposed.  A path relative to the library root is correct in this repository *and*
after the move into ``lifelib/libraries/uslib/``, and it is the same string uklib will
want -- so it survives both moves untouched, which an absolute prefix would not.

``regulatory/`` references are deliberately left alone: they appear only in ``_research/``
and name a statutory-framework stream that was removed from the library in 832247f.  There
is nothing to point them at, and rewriting them would falsify a provenance record.

Usage::

    python tools/rewrite_paths.py uslib --dry-run
    python tools/rewrite_paths.py uslib
"""
import re
import sys
import pathlib
import collections


def slug_map(library):
    """``{'term-life': 'term_life', ...}`` for the products present on disk."""
    products = library / "products"
    return {d.name.replace("_", "-"): d.name
            for d in sorted(products.iterdir()) if d.is_dir()}


# "us/" also occurs inside third-party URLs -- prudential.com/content/dam/us/sites/...,
# pennmutual.com/about-us/news/..., viewpoint.pwc.com/dt/us/en/...  None of those continue
# with one of our directory names today, but a source list grows, so the boundary is
# enforced rather than left to luck: a library path may not be preceded by a path
# separator, a word character, a dot or a hyphen.
START = r'(?<![/\w.-])us/'


def rules(slugs):
    """Ordered (pattern, replacement) pairs.  Most specific first."""
    out = []
    for hyphen, under in slugs.items():
        # The model's README became model.md; it must be rewritten before the bare
        # directory rule below swallows the prefix.
        out.append((rf'{START}models/{re.escape(hyphen)}/README\.md',
                    f'products/{under}/model.md'))
        out.append((rf'{START}models/{re.escape(hyphen)}\b', f'products/{under}'))
        out.append((rf'{START}products/{re.escape(hyphen)}\b', f'products/{under}'))
    out += [
        (rf'{START}models\b', 'products'),
        (rf'{START}products\b', 'products'),
        (rf'{START}_research\b', '_research'),
        (rf'{START}references\b', 'references'),
        (rf'{START}tests\b', 'tests'),
        (rf'{START}README\.md', 'README.md'),
    ]
    return [(re.compile(p), r) for p, r in out]


UNHANDLED = re.compile(START + r'(?!regulatory\b)[A-Za-z0-9_.-]*')


def main(argv):
    dry = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("-")]
    library = pathlib.Path(args[0] if args else "uslib")

    compiled = rules(slug_map(library))
    counts = collections.Counter()
    rewritten = {}
    touched = 0

    for path in sorted(library.rglob("*")):
        if path.suffix not in (".py", ".md") or "__pycache__" in path.parts:
            continue
        original = path.read_text(encoding="utf-8")
        text = original
        for pattern, replacement in compiled:
            text, n = pattern.subn(replacement, text)
            counts[pattern.pattern] += n
        # The tests import the library-root anchor, renamed with the paths it builds.
        if path.suffix == ".py":
            text, n = re.subn(r'\bREPO\b', 'LIB', text)
            counts['REPO -> LIB'] += n
        if text != original:
            touched += 1
            if not dry:
                path.write_text(text, encoding="utf-8")
        rewritten[path] = text

    total = sum(counts.values())
    for pattern, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        if n:
            print(f"{n:5}  {pattern}")
    print(f"\n{total} replacements in {touched} files{' (dry run)' if dry else ''}")

    # Report against the rewritten text, so a dry run tells the truth about what would
    # be left over rather than restating the input.
    leftovers = collections.Counter()
    for text in rewritten.values():
        for m in UNHANDLED.finditer(text):
            leftovers[m.group(0)] += 1
    if leftovers:
        print("\nunhandled 'us/...' strings still present:")
        for s, n in leftovers.most_common(20):
            print(f"  {n:4}  {s}")
    else:
        print("\nno unhandled 'us/...' strings remain (regulatory/ excluded by design)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
