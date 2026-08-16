lifelib-products
================

Product specifications for major life insurance products, organized by country, together
with the executable liability cash flow models built from them.

This site is built from the documents inside each country library — they live beside the
models they describe, not under ``doc/``, and are mirrored into the doc tree at build time.

.. toctree::
   :maxdepth: 2

   libraries/uslib/index

The **uslib** library covers twelve U.S. individual life and annuity product types. Each
product directory holds its representative specification, the liability cash flow model
derived from it, the modelx model itself, the cells reference generated from that model's
docstrings, and the source list every citation resolves against.

The United Kingdom section is not yet a library — it is still a country section in the
older layout and is not built here. See ``uk/`` in the repository.

.. _create-a-project:

Getting a copy
--------------

Inside lifelib this label belongs to the *quickstart* page, where ``lifelib.create()`` is
introduced. It is defined here so the library's own pages resolve while they still live in
this repository, and it does not travel with them: this page stays behind at the merge.

Until then, the library is simply a directory — clone the repository and work in ``uslib/``
directly. Each model reads its inputs from its own product directory, so it runs in place::

    python uslib/products/term_life/run.py

.. note::

   Every citation tag is a link. ``[S6]`` in a product document lands on entry S6 in *that
   product's* source list, and ``[REG-R18]`` lands on entry R18 of the shared reference
   library. Numbering is per product, so ``S1`` means a different source in each.
