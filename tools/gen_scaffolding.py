"""Generate the Sphinx scaffolding that lives inside the library.

Three kinds of page, all authored in the library tree so D3's ``*.md`` mirror carries them
into the doc build with no extra mechanism:

``products/<slug>/index.md``
    the per-product toctree: spec, notes, model narrative, cells reference, sources.

``products/<slug>/model-api.md``
    the autodoc cells reference (D9).  MyST prose framing an ``{eval-rst}`` block, which is
    what lets a markdown page host ``automodule`` -- verified before this was chosen.

``products/index.md``
    the taxonomy landing page.

and a **Verifying this copy** section appended to each ``model.md``, which D7 requires: the
suite ships inside the library, so a reader who edits an assumption can find out whether
they broke the documented example -- but only if the documents say so.

Existing generated blocks are replaced, so this is safe to re-run.

Usage::

    python tools/gen_scaffolding.py uslib --dry-run
    python tools/gen_scaffolding.py uslib
"""
import re
import sys
import pathlib


BEGIN = "<!-- BEGIN generated: tools/gen_scaffolding.py -->"
END = "<!-- END generated -->"
BLOCK = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n*", re.S)

PRODUCT_INDEX = """\
# {title}

```{{toctree}}
:maxdepth: 1

product-spec
technical-notes
model
model-api
sources
```

The representative specification is in [product-spec.md](product-spec.md) and the liability
cash flow model it implies is in [technical-notes.md](technical-notes.md).
[model.md](model.md) explains how `{model}` implements those notes and what was
standardised to do so; [model-api.md](model-api.md) is the cells reference generated from
the model's own docstrings. Every source cited by any of them is listed in
[sources.md](sources.md).
"""

MODEL_API = """\
# `{model}` — cells reference

Generated from the model's own docstrings. The narrative companion — why the model is
shaped this way, which parameters are **[std]**, and what the tests cover — is
[model.md](model.md).

The `Projection` docstring below carries the mapping from the technical notes' actuarial
symbols to these cells names, which is the table to read first if you arrived from
[technical-notes.md](technical-notes.md).

## The model

```{{eval-rst}}
.. automodule:: {lib}.products.{slug}.{model}
```

## `Projection`

```{{eval-rst}}
.. automodule:: {lib}.products.{slug}.{model}.Projection
   :members:
```

## `Data`

```{{eval-rst}}
.. automodule:: {lib}.products.{slug}.{model}.Data
   :members:
```
"""

VERIFY = """\
## Verifying this copy

`{test}` asserts this model against the worked example in
[technical-notes.md](technical-notes.md), and it ships **inside this library** — so it runs
against the copy you are holding, including any changes you have made to it:

```bash
python -m pytest tests/{test_name} -q
```

The whole suite, all twelve models and the shared conventions, is `python -m pytest tests -q`.
If you change an assumption and a test goes red, the worked example in the notes and the
model have parted company — which is the question this library exists to let you ask.
"""

PRODUCTS_INDEX = """\
# Products

Each product directory holds the representative specification, the liability cash flow
model derived from it, the executable model itself, and the source list every citation in
those documents resolves against.

```{{toctree}}
:maxdepth: 1

{entries}
```
"""


def title_of(spec):
    """The product's name, without the '— Representative Product Specification' tail."""
    head = spec.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
    return re.split(r'\s+[—–-]\s+', head)[0].strip()


def write(path, text, dry, made):
    if dry or (path.exists() and path.read_text(encoding="utf-8") == text):
        made.append(f"{'would write' if dry else 'unchanged  '} {path}")
        return
    path.write_text(text, encoding="utf-8")
    made.append(f"wrote      {path}")


def main(argv):
    dry = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("-")]
    library = pathlib.Path(args[0] if args else "uslib")
    # The directory *is* the library: uslib/ here, lifelib/libraries/uslib/ after the
    # merge, and uklib/ when the UK section follows.  Deriving the name any other way
    # would make the anchors and module paths disagree with where the files actually are.
    lib = library.name
    made = []

    slugs = sorted(d.name for d in (library / "products").iterdir() if d.is_dir())
    for slug in slugs:
        product = library / "products" / slug
        model = next(d.name for d in product.iterdir()
                     if d.is_dir() and (d / "_system.json").exists())
        title = title_of(product / "product-spec.md")

        write(product / "index.md",
              PRODUCT_INDEX.format(title=title, model=model), dry, made)
        write(product / "model-api.md",
              MODEL_API.format(lib=lib, slug=slug, model=model), dry, made)

        test_name = f"test_{slug}_us.py"
        section = VERIFY.format(test=f"tests/{test_name}", test_name=test_name)
        model_md = product / "model.md"
        text = BLOCK.sub("", model_md.read_text(encoding="utf-8")).rstrip()
        text = f"{text}\n\n{BEGIN}\n{section}{END}\n"
        write(model_md, text, dry, made)

    entries = "\n".join(f"{s}/index" for s in slugs)
    write(library / "products" / "index.md",
          PRODUCTS_INDEX.format(entries=entries), dry, made)

    for line in made:
        print(f"  {line}")
    print(f"\n{len(made)} files{' (dry run)' if dry else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
