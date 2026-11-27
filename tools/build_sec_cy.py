"""Compile a uslib or uklib SEC model: a command line over the library's own build tool.

The build tool ships with each library that holds SEC models, at the library's root:
``lifelib/libraries/uslib/build_sec_cy.py`` and
``lifelib/libraries/uklib/build_sec_cy.py``, one file in both, held so by uklib's tests.
It lives there, and not here, because lifelib takes a library and not this repository's
``tools/``: while the tool lived here, the libraries' ``run_sec.py --cython`` and the build
commands their ``model-sec.md`` pages give named a script that lifelib does not have, and
nothing in lifelib could build a model (lifelib-dev/lifelib issue 195).  Everything a build
does, and why, is that tool's docstring.

This is a thin command line over it, as ``tools/gen_sec_points.py`` is over a library's
harness.  It takes a product as this repository's tools take one, from any working
directory: a product directory of one of the libraries here, ``<lib>/<product>``, as
``uklib/term_assurance``, or a product's folder name alone where only one library's product
of that name holds a ``*_SEC`` model, as ``term_life`` names uslib's, since jplib's and
krlib's hold none (:func:`product_directory`).  It then runs the tool of the product's
library, with the same options (:func:`library_tool`).  A product directory outside the
libraries here, a copy of one, is built by a library's tool run as a script, which takes
any product directory.  ``tools/bench_sec_cy.py`` reads products through it too.

Usage::

    python tools/build_sec_cy.py term_life                  # Term_US_SEC, in place
    python tools/build_sec_cy.py term_life --out /tmp/term  # elsewhere, with the CSVs
    python tools/build_sec_cy.py uklib/term_assurance       # the product, by its library
    python tools/build_sec_cy.py lifelib/libraries/uslib/products/term_life \\
        --model Term_US_S --sample my_sample.py --spec my_spec.py

It exits as the library's tool exits, 0 with the compiled package's path printed, 1 when a
step fails and 2 when it cannot start; and 2, too, for a product it cannot find, or one
whose library carries no tool.
"""
import argparse
import importlib.util
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
LIBRARIES = REPO / "lifelib" / "libraries"

# The tool's file name in each library that carries one, at the library's root.
TOOL = "build_sec_cy.py"


def products():
    """Every product directory of this repository, ``{(library, product): directory}``.

    A library is a folder of ``lifelib/libraries/`` that holds ``products/``, and its
    products are the folders in that, each in name order.
    """
    found = {}
    for lib in sorted(LIBRARIES.iterdir()) if LIBRARIES.is_dir() else ():
        if (lib / "products").is_dir():
            for product in sorted((lib / "products").iterdir()):
                if product.is_dir():
                    found[lib.name, product.name] = product
    return found


def _holds_sec(product_dir):
    """Whether the product directory holds a ``*_SEC`` model: a folder of that suffix
    holding a ``_system.json``, as the library's tool recognizes one."""
    return any(d.is_dir() and d.name.endswith("_SEC") and (d / "_system.json").is_file()
               for d in pathlib.Path(product_dir).iterdir())


def product_directory(arg):
    """The product directory a command-line argument names.

    An existing directory is taken as it is.  Anything else names a product of a library in
    this repository, from any working directory.  ``<lib>/<product>`` names that library's,
    as ``uklib/term_assurance`` does, with an SEC model or without.  A product's folder name
    alone names the product of that name in the one library where it holds a ``*_SEC``
    model, so ``term_life`` is uslib's: jplib and krlib have a ``term_life`` too, and
    neither holds one.

    Anything else raises ``ValueError``, listing the candidates.  For ``<lib>/<product>``
    they are the libraries, or that library's products.  For a folder name they are the
    products of that name with a ``*_SEC`` model, when more than one library has one; or
    else every library's product of that name, to be named with its library; or else, when
    no library has one, every product a folder name alone finds.
    """
    path = pathlib.Path(arg)
    if path.is_dir():
        return path
    known = products()
    given = pathlib.PurePath(arg)
    parts = () if given.anchor else given.parts
    if len(parts) == 2:
        if parts in known:
            return known[parts]
        lib, product = parts
        libraries = sorted({name for name, _ in known})
        if lib not in libraries:
            raise ValueError(f"{arg!r} is not a directory, and {lib!r} is no library in "
                             f"{LIBRARIES}: they are {', '.join(libraries)}")
        theirs = ", ".join(name for owner, name in known if owner == lib)
        raise ValueError(f"{arg!r} is not a directory, and {lib} has no product "
                         f"{product!r}: its products are {theirs}")
    if len(parts) == 1:
        name = parts[0]
        held = [lib for lib, product in known if product == name]
        with_sec = [lib for lib in held if _holds_sec(known[lib, name])]
        if len(with_sec) == 1:
            return known[with_sec[0], name]
        if with_sec:
            raise ValueError(
                f"{arg!r} is a product with a *_SEC model in {len(with_sec)} libraries, so "
                f"the name alone is ambiguous: name one, as "
                f"{' or '.join(f'{lib}/{name}' for lib in with_sec)}")
        if held:
            raise ValueError(
                f"{arg!r} is not a directory, and no product of that name holds a *_SEC "
                f"model, which a name alone must find: name it with its library, as "
                f"{' or '.join(f'{lib}/{name}' for lib in held)}")
    found = ", ".join(f"{lib}/{product}" for (lib, product), folder in known.items()
                      if _holds_sec(folder))
    raise ValueError(f"{arg!r} is neither a directory, nor <lib>/<product>, nor the folder "
                     f"name of a product with a *_SEC model, which are {found or 'none'}")


def library_tool(product_dir):
    """The build tool of the library ``product_dir`` belongs to, imported as a module.

    The library is the one whose ``products/`` holds the directory, and its tool is the
    ``build_sec_cy.py`` at its root, imported under a name of its own,
    ``build_sec_cy_<lib>``, so that two libraries' tools never share one.  Raises
    ``ValueError`` for a directory that is no product of a library here, and for a library
    that carries no tool, having no SEC model.
    """
    product_dir = pathlib.Path(product_dir).resolve()
    owner = next((lib for (lib, _), folder in products().items()
                  if folder.resolve() == product_dir), None)
    if owner is None:
        raise ValueError(
            f"{product_dir} is no product of a library in {LIBRARIES}: build a copy with "
            f"its library's own tool, python lifelib/libraries/<lib>/{TOOL} "
            f"{product_dir}")
    path = LIBRARIES / owner / TOOL
    if not path.is_file():
        raise ValueError(f"{owner} carries no {TOOL}: it holds no SEC model to build")
    spec = importlib.util.spec_from_file_location(f"build_sec_cy_{owner}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv):
    parser = argparse.ArgumentParser(
        prog="python tools/build_sec_cy.py",
        description="Compile a uslib or uklib SEC model with modelx-cython, by the "
                    "library's own build_sec_cy.py (USLIB-SEC-PLAN.md D12, "
                    "UKLIB-SEC-PLAN.md U4).")
    parser.add_argument(
        "product", help="a product directory, or a uslib or uklib product: "
                        "<lib>/<product>, or its folder name where only one library's "
                        "product of that name holds a *_SEC model")
    parser.add_argument(
        "--model", help="the model folder to compile (default: the product's *_SEC model)")
    parser.add_argument(
        "--out", help="the directory to build in (default: the product directory)")
    parser.add_argument(
        "--sample", help="mx2cy's sample script (default: <product>/sample_sec.py)")
    parser.add_argument(
        "--spec", help="mx2cy's spec file (default: <product>/spec_sec.py)")
    args = parser.parse_args(argv)

    try:
        product = product_directory(args.product)
        tool = library_tool(product)
    except ValueError as err:
        parser.error(str(err))
    passed = [str(product)] + [f"--{option}={value}"
                               for option in ("model", "out", "sample", "spec")
                               if (value := getattr(args, option)) is not None]
    return tool.main(passed, prog=parser.prog)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
