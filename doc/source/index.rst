lifelib-products
================

Product specifications for major life insurance products, organized by country, together
with the executable liability cash flow models built from them.

This site is built from the documents inside each country library — they live beside the
models they describe, not under ``doc/``. Each library document is rendered by a one-line
``{include}`` page here, so no document is copied; alongside them are the autodoc pages,
which Sphinx builds from the models' own docstrings.

.. toctree::
   :maxdepth: 2

   libraries/uslib/index
   libraries/uklib/index
   libraries/jplib/index
   libraries/frlib/index
   libraries/delib/index
   libraries/krlib/index

The **uslib** library covers twelve U.S. individual life and annuity product types; the
**uklib** library covers seven UK ones, including the pension annuity; the **jplib**
library covers nine Japanese ones, three of which are 第三分野 (third-sector) health
products — medical, cancer and nursing care — which is what Japanese households buy most;
the **frlib** library covers nine French ones, five of them built on *assurance vie*
and its *participation aux bénéfices*, which is the French savings vehicle, and one of them
*assurance emprunteur*, the cover a French borrower buys with a mortgage and the largest
individual protection market in the country; the **delib** library covers ten German
ones, organised on the *Drei-Schichten-Modell* the *Alterseinkünftegesetz* imposed on
German retirement saving, with the *Berufsunfähigkeitsversicherung* that is the country's
flagship protection product; and the **krlib** library covers ten Korean ones, four of them
제3보험 (third-insurance) products — indemnity medical, cancer, long-term care and
children's cover — which is the statutory 상해·질병·간병 category Korean households buy,
one of those four being 실손의료보험, the only indemnity contract in this repository. Each
product directory holds its representative specification, the liability cash flow model
derived from it, the modelx model itself, the cells reference generated from that model's
docstrings, and the source list every citation resolves against.

.. _create-a-project:

Getting a copy
--------------

Inside lifelib this label belongs to the *quickstart* page, where ``lifelib.create()`` is
introduced. It is defined here so the library's own pages resolve while they still live in
this repository, and it does not travel with them: this page stays behind at the merge.

Until then, each library is simply a directory — clone the repository and work in
``lifelib/libraries/uslib/``, ``lifelib/libraries/uklib/``, ``lifelib/libraries/jplib/``,
``lifelib/libraries/frlib/``, ``lifelib/libraries/delib/`` or
``lifelib/libraries/krlib/`` directly, which is where lifelib itself keeps them. Each
model reads its inputs from its own product directory, so it runs in place::

    python lifelib/libraries/uslib/products/term_life/run.py
    python lifelib/libraries/uklib/products/term_assurance/run.py
    python lifelib/libraries/jplib/products/term_life/run.py
    python lifelib/libraries/frlib/products/assurance_vie_euro/run.py
    python lifelib/libraries/delib/products/klassische_rentenversicherung/run.py
    python lifelib/libraries/krlib/products/term_life/run.py

.. note::

   Whether a citation tag is a link says what kind of source it is. ``[R1]`` and
   ``[REG-R18]`` are links: the first lands on entry R1 in *that product's* source list,
   the second on entry R18 of the shared reference library. ``[S6]`` is not a link — a
   primary product source is a specification citation rather than an authority, so it
   stays on the page as bracketed text naming the entry to look up. Numbering is per
   product, so ``S1`` means a different source in each.
