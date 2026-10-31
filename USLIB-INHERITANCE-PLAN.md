# uslib — Recommended Inheritance Tree (draft)

**Status:** Draft for discussion, 2026-10-31. Nothing here is implemented yet.

**Goal:** turn the *chassis* relationships that the uslib documents describe
(`lifelib/libraries/uslib/index.md`, "Chassis relationships") into modelx space
inheritance, so that the code says what the documents say: a shared mechanic is
written once, and each product carries only its own changes.

## 1. The tree

```
USBase                      abstract   library conventions (the "Shared vocabulary" table)
├── SingleLifeBase          abstract   one insured life, with a lapse decrement
│   ├── TradLife            abstract   modal premium billing, annual result frame   [optional, §4.4]
│   │   ├── Term_US_S
│   │   └── WholeLife_US_S
│   ├── ULChassis           abstract   the "UL base chassis"        ← universal_life/technical-notes.md
│   │   ├── UL_US_S                    + declared-rate crediting, UL withdrawal rules
│   │   ├── IUL_US_S                   + index account (cap / participation / floor)
│   │   ├── VUL_US_S                   + unitized separate-account subaccounts, fixed option
│   │   └── ULSG_US_S                  + shadow-account secondary guarantee
│   └── DeferredChassis     abstract   the "deferred base chassis"  ← fixed_deferred_annuity/technical-notes.md
│       ├── MYGA_US_S                  + declared rate, MVA, Model #805 MGSV, annuitization decrement
│       ├── FIA_US_S                   + index credit, bonus vesting, GLWB
│       ├── VA_US_S                    + separate account, GMDB, GLWB
│       └── RILA_US_S                  + buffer/cap terms, AG 54 interim value
└── PayoutChassis           abstract   the "payout chassis"         ← immediate_annuity/technical-notes.md
    ├── SPIA_US_S                      + immediate start, annuity forms, commutation
    └── DIA_US_S                       + deferral phase, paid-up income slices, ROP death benefit, QLAC
```

There are three chassis nodes, matching the three chassis the documents name. Each one is
an **abstract space** that holds what its family shares. All twelve products are leaves.
The rest of this document explains the choices that shape the tree.

## 2. The evidence

The tree is based on the cells the twelve `Projection` spaces define today. Each formula
was parsed with docstrings stripped, then compared by name and by formula body.

**Cells per model:** Term 52, WholeLife 97, UL 107, IUL 156, VUL 148, ULSG 139, MYGA 127,
FIA 168, VA 200, RILA 156, SPIA 72, DIA 113.

**What each child would inherit if the chassis *product* were its base:**

| Base → child | Inherited unchanged | Overridden | New in child | Base-only cells carried into the child |
|---|---:|---:|---:|---:|
| `UL_US_S` → `IUL_US_S`    | 73 | 28 | 55 |  6 |
| `UL_US_S` → `VUL_US_S`    | 60 | 30 | 58 | 17 |
| `UL_US_S` → `ULSG_US_S`   | 54 | 36 | 49 | 17 |
| `MYGA_US_S` → `FIA_US_S`  | 19 | 63 | 86 | 45 |
| `MYGA_US_S` → `VA_US_S`   | 15 | 52 | 133 | 60 |
| `MYGA_US_S` → `RILA_US_S` | 23 | 43 | 90 | 61 |
| `SPIA_US_S` → `DIA_US_S`  | 21 | 36 | 56 | 15 |
| `Term_US_S` → `WholeLife_US_S` | 14 | 19 | 64 | 19 |

**Agreement within each family:**

- **UL family:** 42 cells are identical in all four models. Another 18 are identical in
  three of the four. Examples are `coi_pp`, `mth_deduction_pp`, `csv_pp`, `ncsv_pp`,
  `surr_charge`, `pols_death`, `pols_lapse`, `prem_to_av_pp`, `av_at` and `av_change`.
- **Deferred annuities:** only 10 cells are identical across all four. The decrement
  chain has the same *shape* in all four but not the same text: `pols_if_at` steps
  through `BEF_DECR → BEF_MORT → BEF_LAPSE → AFT_DECR`, and `claims_from_av` is
  `claim_from_av_pp × pols_decr`. The texts differ only in the in-force entry guard
  (`entry_mth()` or `t < 0`) and in MYGA's annuitization decrement.
- **Payout:** SPIA and DIA share an identical 21-cell survival-and-payment engine:
  `lives_death`, `lives_death_last`, `mort_rate_base`, `improvement_rate`, `cola_rate`,
  `payment_freq`, `payment_timing`, `survivor_pct`, `is_joint`, `annuity_pp_paid`, …
- **All twelve:** 18 cell names are common to every model, but only 2 have identical
  formulas (`model_point`, `pols_if_init`).

**Cross-model references in the docstrings** (`:mod:` roles that name another model):

| Model | Refers to |
|---|---|
| `VUL_US_S`, `ULSG_US_S`, `RILA_US_S` | `UL_US_S` (the IUL refers to it only in `model.md`) |
| `FIA_US_S`, `VA_US_S`, `RILA_US_S` | `MYGA_US_S` |
| `DIA_US_S` | `SPIA_US_S` |
| `MYGA_US_S`, `FIA_US_S`, `VA_US_S`, `RILA_US_S` | `Term_US_S`, always for a *library convention*: the time grid, `pols_if` at the start of the period, `age(t)` |

The first three rows are the chassis edges. The last row is not a chassis edge. It cites
`USBase`, which does not exist yet, so the models cite the first model that happened to
set the convention.

## 3. Design decisions

### 3.1 A chassis is an abstract space, not the chassis product

The documents say "`UL_US_S` is the base chassis" and describe the IUL as "UL chassis +
index account". Read literally, that makes `IUL_US_S` a subclass of `UL_US_S`. **I
recommend against inheriting from the product itself:**

- **The UL family would work either way, but not cleanly.** Each child would override
  28–36 of UL's cells. VUL and ULSG would also carry 17 UL-only cells they never use
  (`av_pp_db_basis`, `wd_used_year`, `wd_free_pp`, `loan_bal_pp_bom`, …). Those cells
  would show up in their namespaces, their API pages and their conventions tests.
- **The deferred family would not work.** Each child would override 43–63 MYGA cells and
  carry 45–61 it does not use. The documents already say this in their own words: FIA and
  VA "inherit the *structure* … while carrying their own recursions". The FIA notes warn
  against carrying the chassis recursions across. RILA and VA say the MVA and the
  Model #805 floor are **absent by design**. If MYGA were the base, those absences would
  be inherited cells that each child has to stub out.
- **The documents' wording fits the abstract design better.** "UL chassis + index
  account" becomes `IUL_US_S(ULChassis)` plus the index account. `UL_US_S` becomes
  `UL_US_S(ULChassis)` plus declared-rate crediting. Every family member, including the
  chassis product, is then *chassis + its own crediting mechanism*.

**What the documents would need to say:** the chassis is *specified* in the chassis
product's technical notes and *implemented* as the `ULChassis` / `DeferredChassis` /
`PayoutChassis` space. The chassis product is the family member that adds the least.

### 3.2 The first split is single life versus payout, not life versus annuity

The documents group the products as Life and Annuity. The code splits them differently:

- In the payout models, `age`, `age_at_entry`, `sex` and `mort_rate` take a **`life`
  argument**: `age(t, life)`, `mort_rate(t, life)`. A base cell that calls `age(t)`
  cannot be shared with them.
- The payout models have **no lapse decrement**, and they track `lives_if` alongside
  `pols_if`. The documents call these absences "product facts, not gaps".
- The other ten models (all six life models and the four deferred annuities) agree
  exactly on `age(t) = age_at_entry() + duration(t)`, `sex()`, `age_at_entry()` and the
  monthly conversion in `mort_rate_mth` / `lapse_rate_mth`.

So `SingleLifeBase` holds real cells. A `LifeBase` or `AnnuityBase` node would hold
almost none: the six life models share 6 identical cells and the six annuities share 2.
**Life and Annuity stay as a grouping in the documents. They are not spaces.**

This also matches the documents' "Across families" rule. COI, NAAR and the corridor live
in `ULChassis`, so the annuities never inherit them and never need to suppress them.

### 3.3 RILA annuitization is a document reference, not an edge

The index says the RILA's annuitization phase references the payout chassis. But the
model ends at the Maturity Date: `pols_maturity` carries the survivors out, and no payout
is projected. The RILA *notes* borrow the payout chassis, but the *model* does not, so
the RILA has no `PayoutChassis` base. If the RILA later projects its payout phase, the
right design is composition (a payout child space), not a second base.

### 3.4 Retarget the convention references from `Term_US_S` to `USBase`

The 27 `:mod:`.Term_US_S`` references in annuity docstrings cite a convention, not a
chassis. They should point at `USBase`, which is where the convention will live. Several
docstrings currently explain a cell by citing a *life* model.

## 4. What each abstract node owns (first cut)

### 4.1 `USBase`

The "Shared vocabulary" table in `index.md` becomes this space's contract:

- `model_point`, `pols_if_init`
- `duration_mth_init()` (default 0), `duration_mth(t) = duration_mth_init() + t`,
  `duration(t) = duration_mth(t) // 12`, `policy_year(t) = duration(t) + 1`
- `entry_mth()` (default 0), the in-force entry hook. Today this is written as
  `entry_mth()` in FIA, `t < 0` in VA, and `proj_start()` in WholeLife.
- Abstract, defined lower in the tree: `proj_len`, `pols_if`, `premium_pp`, `claims`,
  `expenses`, `net_cf`, `result_cf`

**Rulings needed before this node can exist** (each one changes numbers in at least one
model):

| Cell | Forms in use today |
|---|---|
| `inflation_factor` | `(1+i)^(t/12)` (Term, WL, FIA) · `(1+i)^duration(t)` (MYGA, RILA) · `(1+i)^(policy_year−1)` (UL family, SPIA, DIA) · VA's calendar-based form |
| `duration` | `t // 12` (MYGA, RILA, SPIA, DIA) or `duration_mth(t) // 12`. These are equal while `duration_mth_init() == 0`, so this needs no ruling, only consolidation |
| `policy_year` | `duration(t)+1` in nine models. MYGA writes it as `t//12+1`, VA as `duration_mth(t)//12+1`, RILA as `duration_eom(t)+1`. Only RILA's form is a real difference |

`inflation_factor` is a real disagreement: a smooth monthly factor versus an annual step.
The worked examples assert expenses to the precision the notes print, so this ruling
belongs in the technical notes first. Until it is made, `inflation_factor` stays per
family.

### 4.2 `SingleLifeBase`

`sex()`, `age_at_entry()`, `age(t)`, `mort_rate_mth(t)`, `lapse_rate_mth(t)` (the
`1 − (1 − w)^(1/12)` conversion; Term and FIA override it for the shock lapse and the
anniversary lapse), and the decrement vocabulary `pols_death`, `pols_lapse`,
`pols_maturity`, `pols_if_at`.

### 4.3 The three chassis

- **`ULChassis`:** the 42 cells identical across the family, plus the 18 cells where three
  of four agree (the fourth model overrides). This covers the monthly deduction (`coi_pp`,
  `mth_deduction_pp`, `rider_charge_pp`), the surrender-charge schedule and `csv_pp` /
  `ncsv_pp`, `prem_to_av_pp`, `av_at`, `av_change`, the loan opening balance and the
  margin cells. Where none of the four agree (`coi_rate`, `db_pp`, `net_amt_at_risk`,
  `inv_return_mth`, `av_pp_at`, …), the chassis declares the cell and each leaf defines
  it.
- **`DeferredChassis`:** the decrement chain and its bookkeeping (`pols_if_at` with the
  `BEF_DECR → BEF_MORT → BEF_LAPSE → AFT_DECR` stops, `pols_decr`, `pols_death`,
  `pols_lapse`, `pols_maturity`, `claims_from_av`, the roll-forward checks). It also holds
  the **composition** of the surrender benefit, with hooks: `mva_pp` and the MGSV floor
  default to "absent" and only MYGA (and FIA, for its own floor) overrides them. Finally,
  the free-withdrawal base and its annual reset. The recursions themselves stay in the
  leaves, as the notes require. `annuitization_rate(t)` is a hook that defaults to 0, and
  MYGA overrides it.
- **`PayoutChassis`:** the 21-cell survival and payment engine SPIA and DIA already share,
  using SPIA's names, as the DIA notes require ("this model carries that model's names
  for every shared concept").

### 4.4 `TradLife` (optional)

Term and WholeLife share the modal-premium machinery identically: `premium_mode`,
`prem_cycle`, `prem_due`, `premium_pp` and `result_cf_annual`. The documents never call
this a chassis. Either add the node and add a line to "Chassis relationships", or attach
both models directly to `SingleLifeBase` and accept five duplicated cells. **I lean
towards adding it**, because it is the only shared mechanic left outside a node.

## 5. Not recommended now: feature mixins

modelx supports multiple bases, and three cross-family features look like candidates:

| Mixin | Members | Shared today |
|---|---|---|
| `GLWBRider` | FIA, VA | 16 identical cells, but most are generic (`commissions`, `tax_status`, `pols_decr`). The GLWB recursions themselves differ |
| `SeparateAccount` | VUL, VA | names only (`alloc`, `sa_pp`, `net_cf_ga`), 8 identical cells, all generic |
| `IndexCredit` | IUL, FIA, RILA | `index_level` by name, 6 identical cells, all generic |

The cells these models share are names, not formulas, and the documents describe none of
these features as a chassis. Revisit once the single-inheritance tree is in place. Each
mixin would need its own "Chassis relationships" entry first.

## 6. How it maps onto modelx

**Inheritance is within one model.** A space's `_bases` can only name spaces in the same
model, for example `_bases = [".ULChassis"]`. Every uslib product is its own model, and
that is asserted (`tests/test_model_conventions.py`, `us_registry.py`). So:

- **Each product model carries its ancestor chain as spaces.** For example, `IUL_US_S/`
  holds `USBase`, `SingleLifeBase`, `ULChassis`, `Data` and `Projection`, and
  `Projection._bases` names `.ULChassis`. modelx resolves the rest of the chain.
- **Each chassis has one canonical source**, for example
  `lifelib/libraries/uslib/chassis/ULChassis/__init__.py`. A
  `tools/sync_chassis.py` script copies it into each model, following the same pattern as
  `tools/gen_citation_links.py`. A conventions test asserts that every copy is
  byte-identical to its source and that each model's chain matches the registry.
- **`us_registry.py` gains a `chassis` entry per model**, the leaf's parent. The tree is
  then declared once and asserted, the same way the folder ↔ name pairing is.
- **`test_the_data_projection_split`** (`set(model.spaces) == {"Data", "Projection"}`)
  becomes "`Data`, `Projection`, plus exactly the registered chain".
- **The rejected alternative** is one combined `USLib` model holding every space. It
  breaks one model per product folder, `run.py`, the registry, and `lifelib.create()`
  copies of a single product.

**Verify these by spike before committing to them**, as the merge plan did for D9:

1. A parameterized `Projection` (`point_id`) inherits correctly from unparameterized base
   spaces, and the `data` reference resolves from inherited cells.
2. A base cell overridden in `Projection` with a **different signature** behaves as
   expected. This matters wherever a hook changes its arguments.
3. `write_model` → `read_model` round-trips `_bases` (`test_round_trip_is_stable`).
4. autodoc renders inherited cells on the leaf's API page, or links to the chassis page.
   Decide which the docs want.

## 7. Migration order

Each step keeps every worked-example test green. Formulas that are already identical move
up with no numeric change. Formulas that are equivalent but written differently are
unified only where the tests stay green.

1. **`PayoutChassis`** comes first: the smallest family (two models), 21 identical cells,
   and a clean signature. It proves the modelx mechanics in §6.
2. **`ULChassis`:** move the unanimous cells up, then the three-of-four cells, with the
   remaining model overriding.
3. **`DeferredChassis`:** the most refactoring, because the shared cells share a shape,
   not text. Introduce the `entry_mth()` / `annuitization_rate()` / `mva_pp` hooks first,
   then lift the decrement chain.
4. **`SingleLifeBase`, then `USBase`:** lift the cells the chassis spaces now share. Make
   the `inflation_factor` ruling, in the notes first.
5. **`TradLife`**, if adopted.
6. **Documents:** rewrite `index.md` "Chassis relationships" around the tree, retarget the
   `Term_US_S` convention references (§3.4), and add RILA to the deferred-chassis list
   (the index currently names only FIA and VA, though `RILA_US_S/model.md` says it is
   built on that chassis).

## 8. Open questions

1. Should the chassis be an abstract space (recommended, §3.1), or is the literal reading
   wanted, with the chassis product as the base? The second is workable for the UL family
   only.
2. Should the `inflation_factor` ruling be smooth monthly or an annual step (§4.1)?
3. Should `TradLife` be added (§4.4)?
4. Where should the canonical chassis sources live: `uslib/chassis/`, or each family's
   chassis-product folder?
