"""Repair the relative markdown links the restructure invalidated, and prove they resolve.

Two things broke them.  The product slugs were underscored, and each model's ``README.md``
moved from ``models/<slug>/`` up into ``products/<slug>/`` as ``model.md`` -- so links it
wrote as ``../../products/<slug>/technical-notes.md`` now have two levels too many and a
hyphen too few.

Rather than pattern-match the breakage, this **resolves every relative link against the
filesystem** and only rewrites the ones that do not exist, trying a small ordered set of
repairs.  The report at the end is the acceptance test: a link this cannot resolve is
printed, not silently left.

The candidate repairs, in order:

1. underscore the slug in the path;
2. re-anchor a ``…/products/<slug>/…`` target at the library's real products directory,
   which fixes both the depth and the stale ``models/`` origin;
3. ``README.md`` -> ``index.md``, for the library root page P6 renames;
4. a bare directory -> that directory's ``index.md``.

A target that exists only under ``doc/source/libraries/`` is accepted as-is: the product
landing pages and the autodoc pages are Sphinx scaffolding and are deliberately not shipped
with the library, so a link to one is right even though nothing is there on disk.

Code is excluded from the scan in all three of its forms -- fenced blocks, four-space
indented blocks, and inline spans.  Notation like ``E[death outgo](t)`` appears in each,
and is a markdown link to any scanner that cannot see what encloses it.

Usage::

    python tools/fix_relative_links.py uslib --dry-run
    python tools/fix_relative_links.py uslib
"""
import re
import sys
import os
import pathlib
import collections


LINK = re.compile(r'\]\(([^)\s#]+)(#[^)\s]*)?\)')
FENCE = re.compile(r'^\s*(```|~~~)', re.M)
EXTERNAL = re.compile(r'^(?:[a-z][a-z0-9+.-]*:|//|#)')


CODE_SPAN = re.compile(r'(`+)(?:(?!\1).)*?\1', re.S)


def blank_code(text):
    """A copy of ``text`` with non-fenced code blanked, offsets preserved.

    Two things a link scanner must not read as prose, neither of them a fence:

    * a **four-space indented block**, which is a code block in CommonMark exactly as a
      fenced one is.  Formula notation inside one -- ``E[death outgo](t)`` in the
      whole-of-life notes -- looks precisely like a markdown link to a scanner that
      cannot see the indentation.
    * an **inline code span**.  The same notation appears in prose, backticked, and the
      backticks are what stop CommonMark reading it as a link -- so a scanner that
      ignores them contradicts the renderer.  (P0 hit this in a different scan: four
      angle-bracket tokens flagged in a README were already inside backticks.)

    Reporting either wastes a reviewer's time; *repairing* one would rewrite a path
    inside a code sample, which is worse.  Offsets are preserved rather than the text
    removed, because the caller indexes back into the original to place its edits.
    """
    out, in_fence, blank_before = [], False, True
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            out.append(line)
            blank_before = False
            continue
        indented = line.startswith(("    ", "\t"))
        if not in_fence and indented and blank_before:
            out.append(" " * (len(line) - 1) + line[-1] if line.endswith("\n")
                       else " " * len(line))
        else:
            out.append(line)
        if not in_fence and not indented:
            blank_before = not line.strip()
    return CODE_SPAN.sub(lambda m: " " * (m.end() - m.start()), "".join(out))


def prose_spans(text):
    edges = [0]
    for m in FENCE.finditer(text):
        edges.append(m.start())
    edges.append(len(text))
    for i in range(0, len(edges) - 1, 2):
        yield edges[i], edges[i + 1]


DOC_ROOT = pathlib.Path("doc") / "source" / "libraries"


def doc_here(path, library):
    """Where ``path``'s Sphinx page sits, for links whose target lives only there."""
    return DOC_ROOT / library.name / path.parent.relative_to(library)


def relative(absolute, source_dir):
    """``absolute`` expressed relative to ``source_dir``, POSIX-style, or None.

    ``os.path.relpath`` rather than ``Path.relative_to(..., walk_up=True)``, which needs
    Python 3.12 -- the library floor is set by modelx and pandas, and there is no reason
    for a link fixer to raise it.  The two agree on every path that has an answer; both
    fail on paths with no common anchor, which is what the guard is for.
    """
    try:
        parts = pathlib.Path(
            os.path.relpath(pathlib.Path(absolute).resolve(),
                            source_dir.resolve())).parts
    except (ValueError, OSError):
        return None
    return str(pathlib.PurePosixPath(*parts))


def candidates(target, source_dir, library):
    """Ordered repair attempts for a broken relative target.

    Each is a guess; the caller keeps the first that exists on disk, so a wrong guess
    costs nothing and an unguessable link is reported rather than mangled.
    """
    slugs = sorted(((d.name.replace("_", "-"), d.name)
                    for d in (library / "products").iterdir() if d.is_dir()),
                   key=lambda kv: -len(kv[0]))

    underscored = target
    for hyphen, name in slugs:
        underscored = underscored.replace(hyphen, name)

    forms = []
    for base in dict.fromkeys((underscored, target)):
        # The models/ directory was folded into products/ (P1) ...
        for b in dict.fromkeys((base, base.replace("models/", "products/"))):
            # ... and each model's README.md became model.md there.
            for c in dict.fromkeys((b,
                                    b.replace("README.md", "model.md"),
                                    b.replace("README.md", "index.md"))):
                forms.append(c)
                if not c.endswith(".md"):
                    forms.append(c.rstrip("/") + "/index.md")

    for form in dict.fromkeys(forms):
        yield form

    # Anything still unresolved is most likely a depth problem: the document moved, so a
    # target written relative to its old home now points somewhere else entirely.  Re-anchor
    # it at the library root and recompute the hops.
    for form in dict.fromkeys(forms):
        stripped = re.sub(r'^(?:\.\./)+', '', form)
        if (library / stripped).exists():
            if (rel := relative(library / stripped, source_dir)):
                yield rel


def main(argv):
    dry = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("-")]
    library = pathlib.Path(args[0] if args else "uslib")

    stats = collections.Counter()
    unresolved = []

    for path in sorted(library.rglob("*.md")):
        text = original = path.read_text(encoding="utf-8")
        # Scan a copy with indented code blocks blanked, but edit the original: the two
        # are the same length, so an offset means the same thing in both.
        scan = blank_code(text)
        edits = []
        for start, end in prose_spans(scan):
            for m in LINK.finditer(scan, start, end):
                target = m.group(1)
                if EXTERNAL.match(target):
                    continue
                here = path.parent
                resolved = None
                if (here / target).exists() and not (here / target).is_dir():
                    resolved = here / target
                elif (doc_here(path, library) / target).exists():
                    # Some pages exist only in the doc tree -- the product landing pages
                    # and the autodoc pages are Sphinx scaffolding, deliberately not
                    # shipped with the library.  A link to one resolves when the document
                    # is included into its page, which is the only place it is read as a
                    # document, so it is correct even though nothing is there on disk.
                    stats["resolve in the doc tree only"] += 1
                    continue
                if resolved is None:
                    for candidate in candidates(target, here, library):
                        if candidate and (here / candidate).exists():
                            resolved = here / candidate
                            break
                if resolved is None:
                    stats["unresolved"] += 1
                    unresolved.append(f"{path}: {target}")
                    continue
                # Normalise to the shortest path that reaches the file.  Repairs often
                # land on a technically-correct detour -- a sibling document reached as
                # ../../products/<own slug>/x.md -- and those are the links that break
                # again at the next move.
                canonical = relative(resolved, here)
                if canonical and canonical != target:
                    edits.append((m.start(1), m.end(1), canonical))
                    stats["repaired"] += 1
                else:
                    stats["already resolve"] += 1
        for start, end, replacement in reversed(edits):
            text = text[:start] + replacement + text[end:]
        if text != original and not dry:
            path.write_text(text, encoding="utf-8")

    for key in ("already resolve", "resolve in the doc tree only", "repaired",
                "unresolved"):
        print(f"  {stats[key]:5}  {key}")
    for line in unresolved[:30]:
        print(f"     ! {line}")
    if len(unresolved) > 30:
        print(f"     ... and {len(unresolved) - 30} more")
    print(f"\n{'(dry run)' if dry else 'written'}")
    return 1 if unresolved else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
