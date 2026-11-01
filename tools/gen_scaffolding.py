"""Generate the Sphinx page tree for a country library.

Everything this writes lives under ``doc/source/libraries/<lib>/`` and **nothing goes into
the library**.  The library holds documents; this holds the pages that render them, and the
scaffolding that only Sphinx cares about:

``product-spec.md``, ``technical-notes.md``, ``model.md``, ``sources.md``
    a one-line ``{include}`` of the library file.  The stub tree *mirrors* the library tree,
    which is what keeps the authored relative links working: ``[sources](sources.md)`` in
    ``technical-notes.md`` resolves against the stub's own location, and the sibling stub is
    there.  Citation links survive too -- a document's link reference definitions and the
    tags that use them are in the same included file, so they resolve together.  A product
    with an SEC model also has a ``model-sec.md`` beside its ``model.md``, stubbed the same
    way.

``products/<slug>/index.md``
    the product landing page, written **in place** rather than included.  It is a title, a
    paragraph of orientation and a toctree -- Sphinx scaffolding with nothing in it a reader
    of a ``lifelib.create()`` copy would want.

``products/<slug>/<Model>/<Model>.rst`` and ``products/<slug>/<Model>/<Space>.rst``
    the autodoc pages, following ``annuallife/TradLife_A.rst``: the model page carries the
    model docstring and a hidden toctree of its Spaces, and each Space page carries the
    Space docstring followed by one ``autofunction`` per cells.

The autodoc pages are RST for the same reason the landing pages are written in place: they
are Sphinx plumbing, not library content -- a reader wants the model, not a file whose whole
purpose is to tell Sphinx how to render it.

**A folder per model.**  A product can hold two models.  Under USLIB-SEC-PLAN.md each
uslib product keeps its ``<Name>_US_S`` and gains, beside it, the ``<Name>_US_SEC`` derived
from it, which also projects model points already in force and compiles (D1).  Both have a
``Data`` and a ``Projection`` Space, so pages written flat into the product directory, as
they were until then, would collide: the second model's ``Data.rst`` would overwrite the
first's.  In a folder of its own, no model's pages can meet another's, and a page's URL
names the model it documents.

The folders are the layout for every model, including every product that has only one.
The layout belongs to this tool, which writes all six libraries' page trees, and one rule
is simpler to read, to link to and to merge than a rule with an exception.  Adopting it
moved every autodoc page once -- ``products/<slug>/<Model>.html`` became
``products/<slug>/<Model>/<Model>.html``, and each Space page moved into the folder with
it -- and it was done before the lifelib merge, while nothing linked to the pages by path
and the move cost nothing (USLIB-SEC-PLAN.md D9).

The models are the directories holding a ``_system.json``, sorted by name, which puts
``_S`` before ``_SEC``.  This used to take ``next()`` over the product directory, which is
filesystem order: harmless with one model, but with two the page tree would have depended
on the machine that generated it (USLIB-SEC-PLAN.md F8).  The landing page lists the S
model's notes and cells reference, then the SEC model's, then the sources.

Usage::

    python tools/gen_scaffolding.py lifelib/libraries/uslib --dry-run
    python tools/gen_scaffolding.py lifelib/libraries/uslib

A dry run lists the files that would be written and the files that would be removed, so a
change of layout shows up as the move it is rather than as a set of additions.  A run that
cannot remove a stale page -- a file Windows is still holding -- lists it as
``NOT removed`` and exits 1: Sphinx would build it beside the page that replaced it.
"""
import ast
import os
import re
import shutil
import sys
import textwrap
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
    # jplib.  The English name leads, so the page titles read as the sister libraries' do;
    # the Japanese name -- what the product is actually called, and what every document in
    # the library uses -- follows it in parentheses.
    ("jplib", "term_life"): "Level Term Life (定期保険)",
    ("jplib", "income_guarantee"): "Survivor Income Term (収入保障保険)",
    ("jplib", "whole_life"): "Whole Life (終身保険)",
    ("jplib", "endowment"): "Endowment (養老保険), with 学資保険",
    ("jplib", "medical"): "Medical (医療保険)",
    ("jplib", "cancer"): "Cancer (がん保険)",
    ("jplib", "nursing_care"): "Nursing Care (介護保険)",
    ("jplib", "individual_annuity"): "Individual Annuity (個人年金保険)",
    ("jplib", "fx_whole_life"): "Foreign-Currency Whole Life (外貨建終身保険)",
    # frlib.  Same arrangement as jplib: the English name leads and the French name --
    # what the product is called, and what every document in the library uses -- follows
    # it in parentheses.
    ("frlib", "assurance_vie_euro"): "Euro-Fund Savings (assurance vie, fonds en euros)",
    ("frlib", "assurance_vie_uc"): "Unit-Linked Savings (assurance vie multisupport, unités de compte)",
    ("frlib", "eurocroissance"): "Eurocroissance",
    ("frlib", "per_assurance"): "Retirement Savings Plan (PER assurantiel)",
    ("frlib", "rente_viagere"): "Immediate Life Annuity (rente viagère immédiate)",
    ("frlib", "temporaire_deces"): "Term Life (assurance temporaire décès)",
    ("frlib", "assurance_emprunteur"): "Borrower's Protection (assurance emprunteur, ADE)",
    ("frlib", "obseques"): "Funeral Cover (contrat obsèques)",
    ("frlib", "dependance"): "Long-Term Care (assurance dépendance)",
    # delib.  Same arrangement as jplib and frlib: the English name leads and the German
    # name -- what the product is called, and what every document in the library uses --
    # follows it in parentheses.
    ("delib", "kapitallebensversicherung"):
        "Endowment (kapitalbildende Lebensversicherung)",
    ("delib", "klassische_rentenversicherung"):
        "Deferred Annuity, classic (klassische private Rentenversicherung)",
    ("delib", "fondsgebundene_rentenversicherung"):
        "Unit-Linked Deferred Annuity (fondsgebundene Rentenversicherung)",
    ("delib", "indexpolice"):
        "Index-Participation Annuity (indexgebundene Rentenversicherung, Indexpolice)",
    ("delib", "basisrente"): "Basisrente (Rürup), Schicht 1",
    ("delib", "riester_rente"): "Riester-Rente, Schicht 2",
    ("delib", "sofortrente"):
        "Immediate Life Annuity (sofortbeginnende Rentenversicherung)",
    ("delib", "risikolebensversicherung"): "Term Life (Risikolebensversicherung)",
    ("delib", "berufsunfaehigkeit"):
        "Occupational Disability (selbständige Berufsunfähigkeitsversicherung)",
    ("delib", "pflegerentenversicherung"):
        "Long-Term Care Annuity (Pflegerentenversicherung)",
    # krlib.  Same arrangement as jplib, frlib and delib: the English name leads and the
    # Korean name -- what the product is called, and what every document in the library
    # uses -- follows it in parentheses.
    ("krlib", "whole_life"): "Whole Life (종신보험)",
    ("krlib", "term_life"): "Term Life (정기보험)",
    ("krlib", "ci_insurance"): "Critical Illness (CI보험)",
    ("krlib", "child"): "Children's Insurance (어린이보험), with 태아가입",
    ("krlib", "indemnity_medical"):
        "Indemnity Medical, 4th generation (실손의료보험, 4세대)",
    ("krlib", "cancer"): "Cancer (암보험)",
    ("krlib", "long_term_care"): "Long-Term Care (간병보험)",
    ("krlib", "pension_savings"):
        "Tax-Qualified Pension Savings (연금저축보험)",
    ("krlib", "variable_annuity"): "Variable Annuity (변액연금보험)",
    ("krlib", "immediate_annuity"): "Immediate Annuity (즉시연금)",
}


DOC_ROOT = pathlib.Path("doc") / "source" / "libraries"

PRODUCT_INDEX = """\
# {title}

{blurb}

```{{toctree}}
:maxdepth: 1

{entries}
```
"""

# The landing page's paragraph is the S model's text and then the sentence on the sources,
# which comes last because every document before it cites into them.  A product with an SEC
# model gets one sentence more, between the two, so the paragraph reads in the toctree's
# order; without one, the two pieces join into exactly the text the page had before SEC
# models existed.
BLURB = """\
[Product Specification](product-spec.md) defines the representative product and
[Technical Notes](technical-notes.md) derive its liability cash flow model.
[Implementation Notes](model.md) explain how `{model}` implements those notes and what was
standardized to do so; the cells reference generated from the model's own docstrings
follows it."""

# Worded so that no verb has to agree with `{title}`: the title is model-sec.md's own H1,
# which Phase 1 chooses, and it may be singular or plural.
SEC_BLURB = (
    "How `{sec}` extends `{model}` is explained in [{title}](model-sec.md), and the cells "
    "reference of `{sec}` follows it.")

SOURCES_BLURB = "Every source any of them cites is in [Sources](sources.md)."

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

H1 = re.compile(r"^# +(.+?)(?: +#+)? *$")


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


def models_of(product):
    """The product's S model folder, and its SEC sibling or ``None``.

    The models are the directories holding a ``_system.json``, sorted by name -- never
    taken in filesystem order, which differs between machines -- and the sort puts
    ``<Name>_S`` before ``<Name>_SEC``.  Anything else stops the run: no model, two S
    models, an SEC model whose name is not its S model's plus ``EC``, or a suffix this does
    not know.  What a landing page says about a model is editorial, and the blurb states
    that the SEC model extends the S one, so a pairing the names do not show is not
    guessed at.

    An SEC model and its ``model-sec.md`` come together (USLIB-SEC-PLAN.md D8, D9), and
    one without the other stops the run too.  The landing page links the notes and lists
    the model's pages, so the model alone would leave it linking notes that are not there,
    and the notes alone would put a page about a missing model in front of a reader.
    """
    models = sorted((d for d in product.iterdir()
                     if d.is_dir() and (d / "_system.json").exists()),
                    key=lambda d: d.name)
    names = [d.name for d in models]
    if not (names and names[0].endswith("_S")
            and names[1:] in ([], [names[0] + "EC"])):
        sys.exit(f"{product}: expected one *_S model, alone or with its *_SEC beside it;"
                 f" found {', '.join(names) or 'no model'}")
    sec = models[1] if len(models) > 1 else None
    notes = (product / "model-sec.md").exists()
    if sec and not notes:
        sys.exit(f"{product}: {sec.name} has no model-sec.md beside it -- write the notes"
                 " that explain it, and its pages come with them")
    if notes and not sec:
        sys.exit(f"{product}: model-sec.md is there but no *_SEC model is -- the notes"
                 " would explain a model the page tree does not have")
    return models[0], sec


def title_of(path):
    """The H1 of a markdown document: the title its toctree entry shows.

    Fenced code is skipped, since a ``# comment`` in a shell block is not a heading.  A
    document without an H1 stops the run; ``md_lint.py`` requires exactly one, and the
    toctree would have no title to show for it either.
    """
    fenced = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
        elif not fenced and (m := H1.match(line)):
            return m.group(1)
    sys.exit(f"{path} has no H1 -- the landing page links it by its title")


def blurb(model, sec=None, sec_title=None):
    """The landing page's paragraph of orientation.

    With one model it is the text the landing pages had before SEC models existed, byte
    for byte, so a product without one regenerates unchanged.  With an SEC model, the
    paragraph's last line is refilled to take the SEC sentence ahead of the sources.
    ``break_on_hyphens`` is off because a line break after the hyphen of ``in-force``
    renders as a space, and inside ``(model-sec.md)`` it would end the link.
    """
    text = BLURB.format(model=model)
    if sec is None:
        return f"{text} {SOURCES_BLURB}"
    head, last = text.rsplit("\n", 1)
    tail = " ".join([last, SEC_BLURB.format(sec=sec, model=model, title=sec_title),
                     SOURCES_BLURB])
    return head + "\n" + textwrap.fill(tail, width=92, break_long_words=False,
                                       break_on_hyphens=False)


def model_pages(lib, product, model_dir, out):
    """One model's autodoc pages, as ``{path: text}``: the model page, then one per Space.

    ``out`` is the model's own folder.  The model page's toctree names its Spaces
    unqualified -- ``Data``, ``Projection`` -- and Sphinx resolves a toctree entry against
    the page that holds it, so each model's entries find that model's pages and no other's.
    """
    model = model_dir.name
    spaces = spaces_of(model_dir)
    dotted = f"{lib}.products.{product.name}.{model}"
    pages = {out / f"{model}.rst": MODEL_PAGE.format(
        model=model, underline="=" * (len(model) + 14), dotted=dotted,
        spaces="\n".join(f"   {s.name}" for s in spaces))}
    for space in spaces:
        cells = "\n\n".join(f".. autofunction:: {c}" for c in cells_of(space))
        pages[out / f"{space.name}.rst"] = SPACE_PAGE.format(
            space=space.name, underline="=" * (len(space.name) + 14),
            dotted=f"{dotted}.{space.name}", cells=cells)
    return pages


def product_pages(lib, product, docs):
    """Every page of one product, as ``{path: text}``, in the order they are written."""
    s_model, sec_model = models_of(product)
    page_dir = docs / "products" / product.name

    # The toctree, in reading order: the product's documents, then each model's notes
    # followed by its cells reference -- the S model, then the SEC model derived from it --
    # and the sources last.  An entry with a slash is a model page in the model's folder;
    # every other entry is a library document, and its page is an include stub.
    entries = ["product-spec", "technical-notes", "model", f"{s_model.name}/{s_model.name}"]
    if sec_model:
        entries += ["model-sec", f"{sec_model.name}/{sec_model.name}"]
    entries.append("sources")

    if sec_model:
        about = blurb(s_model.name, sec_model.name, title_of(product / "model-sec.md"))
    else:
        about = blurb(s_model.name)

    # Written in place, not included: the landing page is scaffolding, and the library is
    # better off without it.
    pages = {page_dir / "index.md": PRODUCT_INDEX.format(
        title=TITLES[(lib, product.name)], blurb=about, entries="\n".join(entries))}
    for name in (e for e in entries if "/" not in e):
        pages[page_dir / f"{name}.md"] = STUB.format(
            relpath=relative(product / f"{name}.md", page_dir))
    for model_dir in filter(None, (s_model, sec_model)):
        pages.update(model_pages(lib, product, model_dir, page_dir / model_dir.name))
    return pages


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

    # Every page is composed before the old tree is removed, for the same reason.  Whatever
    # stops the run -- a model folder `models_of` will not guess about, notes without a
    # title, a product with no entry in TITLES, a formula file that does not parse -- stops
    # it here, while the committed tree is still whole.
    pages = {}
    for product in sorted(d for d in (library / "products").iterdir() if d.is_dir()):
        pages.update(product_pages(lib, product, docs))
    # The library index and the reference bibliography sit at the library root.
    pages[docs / "index.md"] = STUB.format(relpath=relative(library / "index.md", docs))
    refs = pathlib.PurePosixPath("references/regulatory-and-actuarial-references.md")
    pages[docs / refs] = STUB.format(
        relpath=relative(library / refs, (docs / refs).parent))

    # What regenerating deletes: the files of the current tree that the new one does not
    # have.  Listed in a dry run as well, so that a change of layout previews as a move,
    # from the old paths to the new, and not as additions alone.
    stale = sorted(p for p in docs.rglob("*") if p.is_file() and p not in pages)

    if not dry:
        # Regenerated wholesale; nothing here is hand-edited.  Removal must not be fatal:
        # a previous doc build leaves files Windows can still be holding.
        for _ in range(3):
            shutil.rmtree(docs, ignore_errors=True)
            if not docs.exists():
                break

    for path, text in pages.items():
        write(path, text, dry, log)

    # Removal is not fatal, but a stale page that survives it is.  Sphinx builds every page
    # it finds, so a page left behind is built as if it were current -- an old model page
    # beside its replacement documents the same module twice -- and the strict build fails
    # on it.  Every new page is written either way; the status says the tree on disk is
    # not yet the one composed above.
    left = set() if dry else {path for path in stale if path.exists()}
    for action, path in log:
        print(f"  {action:12} {path}")
    for path in stale:
        action = "would remove" if dry else "NOT removed" if path in left else "removed"
        print(f"  {action:12} {path}")
    removed = len(stale) - len(left)
    removed = f", {removed} removed" if removed else ""
    print(f"\n{len(log)} files{removed}{' (dry run)' if dry else ''}")
    if left:
        print(f"{len(left)} stale files could not be removed -- delete them before"
              " building", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
