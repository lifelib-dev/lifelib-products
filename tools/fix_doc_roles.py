"""Make the model docstrings' RST cross-references survive the move into lifelib.

The 1,581 cells docstrings were written when a model was a top-level module, so they say
``:mod:`Term_US_A``` and ``:mod:`~Term_US_A.Projection```.  Under lifelib the model sits at
``uslib.products.term_life.Term_US_A``, and role resolution is relative to the current
module -- so a bare ``Term_US_A`` names nothing and Sphinx **silently drops the role and
renders plain text**.  No warning, unless the build runs with ``-n``.

The fix is a leading dot, which makes the lookup *refspecific*: it matches any module whose
dotted path ends that way.  ``:mod:`.Term_US_A``` and ``:mod:`~.Term_US_A.Projection```
both resolve, the ``~`` still trims the displayed text, and the rendered page is unchanged.

It is also depth- and library-agnostic, so the same docstrings work in uslib, in uklib, and
in a copy made by ``lifelib.create()`` -- which an absolute ``uslib.products.…`` prefix
would not.

**The name universe is every library, not the one being fixed.**  uklib's docstrings name
uslib models: the pension annuity states its deltas against ``SPIA_US_S``, UK term against
``Term_US_A``, UK whole of life against ``WholeLife_US_A``.  Those are the same chassis
pointers the plan describes between siblings *inside* uslib, one level out, and they break
the same way -- but a tool that only knew its own library's model names would leave every
one of them dead, silently.  So model names are collected from every sibling library and
the target library's files are the only ones edited.

Same-Space ``:func:``/``:attr:`` roles are left alone: they already resolve relative to the
current module at any depth.  Only the ones naming a cells in the *other* Space need the
dot, and they are found by looking, not guessed.

Usage::

    python tools/fix_doc_roles.py lifelib/libraries/uslib --dry-run
    python tools/fix_doc_roles.py lifelib/libraries/uslib
"""
import ast
import re
import sys
import pathlib
import collections


def spaces(model_dir):
    """``{'Projection': {'pols_if', ...}, 'Data': {...}}`` for one model folder."""
    found = {}
    for sub in sorted(model_dir.iterdir()):
        init = sub / "__init__.py"
        if sub.is_dir() and init.exists():
            tree = ast.parse(init.read_text(encoding="utf-8"))
            found[sub.name] = {n.name for n in tree.body
                               if isinstance(n, ast.FunctionDef)}
    return found


def fix_text(text, models, this_model, own_cells, other_cells, other_space, local):
    """Return (new_text, counts) for one module's source.

    ``models`` is every model name in every library, not just this file's own.  A third of
    these references are chassis pointers between siblings -- the variable annuity naming
    the MYGA deferred chassis, the DIA naming the SPIA payout chassis -- and some point at
    another library entirely.  They break in exactly the same way, so they are fixed the
    same way.  ``local`` is the target library's own model names, which is all that
    separates a sibling reference from a cross-library one in the report.
    """
    counts = collections.Counter()
    alternatives = "|".join(re.escape(m) for m in sorted(models, key=len, reverse=True))

    # :mod:`Model`, :mod:`~Model`, :mod:`Model.Space`, :mod:`~Model.Space`
    def mod_sub(m):
        head = m.group(2).split(".")[0]
        counts["own model" if head == this_model
               else "sibling model" if head in local
               else "cross-library"] += 1
        return f":mod:`{m.group(1)}.{m.group(2)}`"

    text = re.sub(rf':mod:`(~?)((?:{alternatives})(?:\.\w+)*)`', mod_sub, text)

    # :func:/:attr: written as a path through a model -- Term_US_A.Projection.pols_if.
    # Same breakage as the module roles and the same one-character fix.
    def dotted_sub(m):
        # The prefix is "", "~", "." or "~." -- test for the dot anywhere in it, not at the
        # front, or a second run re-dots the "~." form the cross-Space rule below produces.
        if "." in m.group(2):
            return m.group(0)
        counts["dotted path"] += 1
        return f":{m.group(1)}:`{m.group(2)}.{m.group(3)}`"

    text = re.sub(rf':(func|attr):`(~?\.?)((?:{alternatives})\.[\w.]+)`', dotted_sub, text)

    # :func:/:attr: naming a cells that lives in the *other* Space of this model.  These
    # must be spelled out in full: every model has a Data.input_dir, so a bare `.input_dir`
    # is refspecific enough to find twelve of them and Sphinx reports the ambiguity.  The
    # ~ keeps the rendered text as the plain cells name.
    def ref_sub(m):
        role, tilde, name = m.group(1), m.group(2), m.group(3)
        if name in own_cells or name not in other_cells:
            return m.group(0)
        counts["cross-Space"] += 1
        return f":{role}:`~.{this_model}.{other_space[name]}.{name}`"

    text = re.sub(r':(func|attr):`(~?\.?)(\w+)`', ref_sub, text)
    return text, counts


def main(argv):
    dry = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("-")]
    library = pathlib.Path(args[0] if args else "lifelib/libraries/uslib")

    def models_under(root):
        found = {}
        for product in sorted((root / "products").iterdir()):
            if not product.is_dir():
                continue
            model = next((d for d in product.iterdir()
                          if d.is_dir() and (d / "_system.json").exists()), None)
            if model is not None:
                found[product.name] = model
        return found

    model_dirs = models_under(library)
    local = {d.name for d in model_dirs.values()}

    # Every sibling library's models too, so a cross-library chassis pointer is recognised
    # rather than left dead.  A sibling is any directory beside this one with products/.
    models = set(local)
    for sibling in sorted(library.resolve().parent.iterdir()):
        if sibling.is_dir() and sibling != library.resolve() and (sibling / "products").is_dir():
            models |= {d.name for d in models_under(sibling).values()}

    totals = collections.Counter()
    for model_dir in model_dirs.values():
        by_space = spaces(model_dir)
        all_cells = set().union(*by_space.values()) if by_space else set()

        targets = [model_dir / "__init__.py"]
        targets += [model_dir / s / "__init__.py" for s in by_space]
        for path in targets:
            own = by_space.get(path.parent.name, set())
            original = path.read_text(encoding="utf-8")
            other_space = {name: space
                           for space, cells in by_space.items() if space != path.parent.name
                           for name in cells}
            text, counts = fix_text(original, models, model_dir.name,
                                    own, all_cells - own, other_space, local)
            totals.update(counts)
            if text != original and not dry:
                path.write_text(text, encoding="utf-8")

    for key in ("own model", "sibling model", "cross-library", "dotted path",
                "cross-Space"):
        print(f"  {totals[key]:4}  {key} references given a leading dot")
    print(f"\n{sum(totals.values())} roles fixed{' (dry run)' if dry else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
