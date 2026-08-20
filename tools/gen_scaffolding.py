"""Generate the Sphinx page tree for a country library.

Everything this writes lives under ``doc/source/libraries/<lib>/`` and **nothing goes into
the library**.  The library holds documents; this holds the pages that render them, and the
scaffolding that only Sphinx cares about:

``product-spec.md``, ``technical-notes.md``, ``model.md``, ``sources.md``
    a one-line ``{include}`` of the library file.  The stub tree *mirrors* the library tree,
    which is what keeps the authored relative links working: ``[sources](sources.md)`` in
    ``technical-notes.md`` resolves against the stub's own location, and the sibling stub is
    there.  Citation links survive too -- a document's link reference definitions and the
    tags that use them are in the same included file, so they resolve together.

``products/<slug>/index.md``
    the product landing page, written **in place** rather than included.  It is a title, a
    sentence of orientation and a toctree -- Sphinx scaffolding with nothing in it a reader
    of a ``lifelib.create()`` copy would want.

``<Model>.rst`` and ``<Space>.rst``
    the autodoc pages, following ``annuallife/TradLife_A.rst``: the model page carries the
    model docstring and a hidden toctree of its Spaces, and each Space page carries the
    Space docstring followed by one ``autofunction`` per cells.

The autodoc pages are RST for the same reason the landing pages are written in place: they
are Sphinx plumbing, not library content -- a reader wants the model, not a file whose whole
purpose is to tell Sphinx how to render it.

Usage::

    python tools/gen_scaffolding.py lifelib/libraries/uslib --dry-run
    python tools/gen_scaffolding.py lifelib/libraries/uslib
"""
import ast
import os
import shutil
import sys
import pathlib


# The product's display name.  This is editorial and not derivable from the folder --
# "registered_index_linked_annuity" is unusable and the industry says RILA -- so it is
# written down once, exactly as the model-name registry is written down in each library's
# test registry.
#
# Keyed by (library, slug) rather than by slug alone.  Slugs were unique across the first
# two libraries and a single flat map served both; jplib ends that, because Japan sells a
# 定期保険 and a 終身保険 and the honest slugs for them are `term_life` and `whole_life`,
# which uslib already uses for different products.  The library name was available here all
# along -- `main` derives it from the argument -- so the key carries it.
TITLES = {
    ("uslib", "term_life"): "Level Premium Term Life",
    ("uslib", "whole_life"): "Whole Life",
    ("uslib", "universal_life"): "Universal Life (current assumption)",
    ("uslib", "indexed_ul"): "Indexed Universal Life (IUL)",
    ("uslib", "variable_ul"): "Variable Universal Life (VUL)",
    ("uslib", "guaranteed_ul"): "Guaranteed Universal Life (ULSG)",
    ("uslib", "fixed_deferred_annuity"): "Fixed Deferred Annuity (MYGA)",
    ("uslib", "fixed_indexed_annuity"):
        "Fixed Indexed Annuity (FIA) with Guaranteed Lifetime Withdrawal Benefit",
    ("uslib", "variable_annuity"): "Variable Annuity with Living and Death Benefit Guarantees",
    ("uslib", "registered_index_linked_annuity"): "Registered Index-Linked Annuity (RILA)",
    ("uslib", "immediate_annuity"): "Single Premium Immediate Annuity (SPIA)",
    ("uslib", "deferred_income_annuity"):
        "Deferred Income Annuity (DIA) and Qualified Longevity Annuity Contract (QLAC)",
    # uklib
    ("uklib", "term_assurance"): "Term Assurance",
    ("uklib", "critical_illness"): "Critical Illness Cover (CI)",
    ("uklib", "income_protection"): "Income Protection (IP)",
    ("uklib", "whole_of_life"): "Whole of Life (WOL)",
    ("uklib", "with_profits"): "With-Profits (WP)",
    ("uklib", "unit_linked_bond"): "Unit-Linked Investment Bond (ULB)",
    ("uklib", "pension_annuity"): "Pension Annuity (PA)",
    # jplib.  The Japanese name leads, because it is what the product is called and what
    # every document in the library uses; the English gloss follows it.
    ("jplib", "term_life"): "定期保険 — Level Term Life",
    ("jplib", "income_guarantee"): "収入保障保険 — Survivor Income Term",
    ("jplib", "whole_life"): "終身保険 — Whole Life",
    ("jplib", "endowment"): "養老保険 — Endowment, with 学資保険",
    ("jplib", "medical"): "医療保険 — Medical (third sector)",
    ("jplib", "cancer"): "がん保険 — Cancer (third sector)",
    ("jplib", "nursing_care"): "介護保険 — Nursing Care (third sector)",
    ("jplib", "individual_annuity"): "個人年金保険 — Individual Annuity",
    ("jplib", "fx_whole_life"): "外貨建終身保険 — Foreign-Currency Whole Life",
}


DOC_ROOT = pathlib.Path("doc") / "source" / "libraries"

# The documents each product page lists, in reading order.  `_MODEL_` stands in for the
# model's own name, which is only known per product.
PRODUCT_PAGES = ["product-spec", "technical-notes", "model", "_MODEL_", "sources"]

PRODUCT_INDEX = """\
# {title}

{blurb}

```{{toctree}}
:maxdepth: 1

{entries}
```
"""

BLURB = """\
[Product Specification](product-spec.md) defines the representative product and
[Technical Notes](technical-notes.md) derive its liability cash flow model.
[Implementation Notes](model.md) explain how `{model}` implements those notes and what was
standardized to do so; the cells reference generated from the model's own docstrings
follows it. Every source any of them cites is in [Sources](sources.md)."""

STUB = "```{{include}} {relpath}\n```\n"

MODEL_PAGE = """\
The **{model}** Model
{underline}

.. automodule:: {dotted}

.. toctree::
   :hidden:
   :maxdepth: 1

{spaces}
"""

SPACE_PAGE = """\
The **{space}** Space
{underline}

.. automodule:: {dotted}

Cells Descriptions
------------------

{cells}
"""


def cells_of(space_dir):
    """Cells names in definition order -- `autodoc_member_order` is 'bysource'."""
    tree = ast.parse((space_dir / "__init__.py").read_text(encoding="utf-8"))
    return [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]


def relative(target, start):
    """``target`` as a POSIX path relative to ``start``.

    Counted by the filesystem rather than by hand, which is what makes the result the
    string lifelib needs rather than merely one that works here: both repositories keep
    their libraries at ``lifelib/libraries/<lib>/`` and their pages at
    ``doc/source/libraries/<lib>/``, so the same relative path is correct in both, and the
    page tree merges without being regenerated.
    """
    return pathlib.PurePath(os.path.relpath(target, start)).as_posix()


def spaces_of(model_dir):
    return [d for d in sorted(model_dir.iterdir())
            if d.is_dir() and (d / "__init__.py").exists()]


def write(path, text, dry, log):
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    log.append(("would write" if dry else "wrote", path))
    if not dry:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def main(argv):
    dry = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("-")]
    library = pathlib.Path(args[0] if args else "lifelib/libraries/uslib")
    lib = library.name
    docs = DOC_ROOT / lib
    log = []

    # Before the rmtree below, and not after.  `docs` is derived from `library.name`, so a
    # stale `uslib` -- the argument that was correct before the libraries moved under
    # `lifelib/libraries/`, and still the natural thing to type -- resolves `docs` to the
    # real, committed page tree.  Without this the tool would delete it and only then fail
    # on the missing products directory.
    if not (library / "products").is_dir():
        sys.exit(f"no library at {library} -- expected a products/ directory under it")

    if not dry:
        # Regenerated wholesale; nothing here is hand-edited.  Removal must not be fatal:
        # a previous doc build leaves files Windows can still be holding.
        for _ in range(3):
            shutil.rmtree(docs, ignore_errors=True)
            if not docs.exists():
                break

    products = sorted(d for d in (library / "products").iterdir() if d.is_dir())

    for product in products:
        model_dir = next(d for d in product.iterdir()
                         if d.is_dir() and (d / "_system.json").exists())
        model = model_dir.name
        spaces = spaces_of(model_dir)

        page_dir = docs / "products" / product.name
        entries = "\n".join(model if page == "_MODEL_" else page
                            for page in PRODUCT_PAGES)
        # Written in place, not included: the landing page is scaffolding, and the library
        # is better off without it.
        write(page_dir / "index.md",
              PRODUCT_INDEX.format(title=TITLES[(lib, product.name)],
                                   blurb=BLURB.format(model=model),
                                   entries=entries),
              dry, log)

        for name in ("product-spec", "technical-notes", "model", "sources"):
            write(page_dir / f"{name}.md",
                  STUB.format(relpath=relative(
                      product / f"{name}.md", page_dir)), dry, log)

        dotted = f"{lib}.products.{product.name}.{model}"
        write(page_dir / f"{model}.rst",
              MODEL_PAGE.format(model=model, underline="=" * (len(model) + 14),
                                dotted=dotted,
                                spaces="\n".join(f"   {s.name}" for s in spaces)),
              dry, log)
        for space in spaces:
            cells = "\n\n".join(f".. autofunction:: {c}" for c in cells_of(space))
            write(page_dir / f"{space.name}.rst",
                  SPACE_PAGE.format(space=space.name,
                                    underline="=" * (len(space.name) + 14),
                                    dotted=f"{dotted}.{space.name}", cells=cells),
                  dry, log)

    # The library index and the reference bibliography sit at the library root.
    write(docs / "index.md",
          STUB.format(relpath=relative(library / "index.md", docs)), dry, log)
    refs = pathlib.PurePosixPath("references/regulatory-and-actuarial-references.md")
    write(docs / refs,
          STUB.format(relpath=relative(library / refs, (docs / refs).parent)), dry, log)

    for action, path in log:
        print(f"  {action:11} {path}")
    print(f"\n{len(log)} files{' (dry run)' if dry else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
