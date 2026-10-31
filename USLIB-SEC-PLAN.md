# Plan — `*_US_SEC`: uslib models that run in force, then compile

**Status:** Draft plan, 2026-10-31. Nothing in it is implemented yet. Every number in it
was measured in this repository, or in lifelib 0.17.2, modelx 0.33.0 and modelx-cython
0.1.0 as installed for the purpose, and each is quoted with the experiment that produced it.

**Goal.** For each of the twelve uslib products, add a model `<Name>_US_SEC`, derived from
its `<Name>_US_S`, with two enhancements done **in sequence**:

1. **E — in force at time 0.** Besides new-business model points, the model projects model
   points that are already in force at the valuation date `t = 0`. This follows how
   lifelib's `basiclife/BasicTerm_SE` extends `basiclife/BasicTerm_S`.
2. **C — compilable.** The model's exported pure-Python form compiles under modelx-cython
   into C-typed code. This follows how `basiclife/BasicTerm_SC` is derived from
   `basiclife/BasicTerm_S`: `Projection` is indexed by `idx`, the position of a model point
   in the input vectors; its cells receive inputs from `Data` as numpy vectors, which
   compile to typed memoryviews; and the model-point projection logic uses only C scalars
   (`bint`, `long long`, `double`) and C arrays, held in the compiled space's C struct.

The `_S` models are not touched. They remain the reference: their worked-example goldens
pin the SEC models through the twin identity of §5.2.

---

## 1. What the two lifelib references change

Read from the lifelib 0.17.2 sources.

### 1.1 `BasicTerm_S` → `BasicTerm_SE` (the E step)

| | `BasicTerm_S` | `BasicTerm_SE` |
|---|---|---|
| Time 0 | the issue month of each point | the valuation date, shared by every point |
| Policy clock | `duration(t) = t // 12` | `duration_mth(0)` read from the model point; `duration_mth(t) = duration_mth(t-1) + 1`; **negative** means future new business, issued at `t = -duration_mth(0)` |
| In force at `t = 0` | `pols_if_init() = 1` | `policy_count` if `duration_mth(0) > 0`, else 0 |
| New business | implicit at `t = 0` | `pols_new_biz(t) = policy_count` in the month `duration_mth(t) == 0` |
| Timings | `pols_if(t)` | `pols_if_at(t, timing)`, timing in `BEF_MAT`, `BEF_NB`, `BEF_DECR`; `pols_if(t)` is `BEF_MAT` |
| Activity | — | `is_active(t)`: `0 <= duration_mth(t) <= 12 * policy_term()` |
| Frame | `12 * policy_term() + 1` | `max(12 * policy_term() - duration_mth(0) + 1, 0)` |
| Decrements, expenses | on `pols_if(t)` | on `pols_if_at(t, "BEF_DECR")`; acquisition on `pols_new_biz(t)`; inflation on `t`, the valuation clock |
| Premium | solved per point (`net_premium_pp`) | read from `premium_table`: an in-force point cannot re-solve a premium fixed at issue |
| Reporting | `result_cf()` | adds `result_pols()` with the timings and new business |

### 1.2 `BasicTerm_S` → `BasicTerm_SC` (the C step)

| | `BasicTerm_S` | `BasicTerm_SC` |
|---|---|---|
| Spaces | `Projection` holds data (IOSpec) | `Data` + `Projection`; `Projection` reaches `Data` as `data` |
| Parameter | `point_id`, the table label | `idx`, the 0-based array position |
| Attributes | `model_point()["x"]`, a Series lookup | `data.x()[idx]`; `Data.x()` returns an int64 or float64 numpy vector |
| Tables | `mort_table[str(dur)][age]` | `data.mort_table_array()[age, dur]`, padded with NaN rows so the row index **is** the age |
| Discounting | `disc_factors()` returns a vector | `disc_factor(t)`, a scalar per `t` |
| Present values | `sum(list(...) * vector)` | explicit `for` loops accumulating a float |
| Compile inputs | — | `spec.py` (cache size for `t`: 241), `sample.py` (projects 10 points for type tracing) |

---

## 2. Findings that shape the plan

**F1 — The twelve S models have three time axes, not one.** Term, MYGA, RILA, SPIA and DIA
project new business only (Term's `duration_inforce` column exists, but no formula reads
it). UL, IUL, ULSG, VUL and VA already put `t = 0` at the projection start, with a
`duration_mth_init()` offset and `*_init` opening balances, which is BasicTerm_SE's shape
minus new-business timing. WholeLife and FIA keep the **policy** clock and open an in-force
frame late — `proj_start() = 12 * duration_inforce()`, `entry_mth()` — so their in-force
`result_cf()` starts at `t_first > 0`. So E is a different amount of work for each family;
§7 has the per-model detail.

**F2 — Compiling alone gains almost nothing; the representation is what gains.** Measured
on `UL_US_S`, unmodified, exported and compiled with mx2cy (59 s to build): 25 of its 107
`Projection` cells still return `object`/`str`, 16 keep Python dict caches (every
string-keyed cell: `av_pp_at(t, timing)`, `pols_if_at`, `claims(t, kind)`, …), and most of
the cells typed `double` still call pandas inside their bodies. Over 90 projections the
compiled model ran **1.18×** faster than its own export (15.7 s → 13.3 s), and profiling the
export puts **65 % of its run time inside pandas** (`model_point()[...]` and per-`t` `.loc`
lookups). `BasicTerm_SC`, which has the SC representation, compiles to **7.8×** its export
(1,000 points, 1.49 s → 0.19 s). Phase 2 is the representation change; the compiler only
collects the benefit.

**F3 — How modelx-cython types a cell, verified on a prototype.** mx2cy traces a sample run
of the *exported* model and types each cell from the values it saw:

| Pattern in a formula (as traced) | Generated C |
|---|---|
| returns `int` / `float` / `bool`; all parameters `int` | `long long` / `double` / `bint`, cached in a C array of that type, `[N]` (or `[N][M]` for two int parameters) |
| `data.x()` returns an int64 / float64 array, 1-D or 2-D | `const long long[:]` / `const double[:, :]` memoryview; `data.x()[idx]` is a C load |
| `data.x()` returns a **bool** array | `object` — numpy bool is not a memoryview type |
| returns `numpy.bool_`, e.g. a comparison of two values read from arrays | `object` **and** a dict cache, because the return is not "real" |
| the same comparison wrapped in `bool(...)` | `bint`, C-array cache; the generated C makes no Python API call |
| a parameter that is a string (`timing="BEF_DECR"`) | `str` parameter, **dict cache** |
| the same parameter as a named int Reference (`BEF_DECR = 2`) | `long long`, cache `double[N][3]` |
| returns a tuple, list, Series, DataFrame or `None` | `object`, dict cache |
| `o == o` on a `numpy.float64` (a NaN test) | `object` (traces as `numpy.bool_`) |
| a cell the sample never calls | `object` everywhere — untraced is untyped |
| a `Data` array used other than by element subscript anywhere (`len`, a slice, iteration, a numpy call) | the `Data` cell falls back to `object` — mx2cy's usage analysis must prove every use is element access |
| local `pv = 0.0; pv += ...` in a loop | inferred C `double`; an annotation `pv: float` stays a Python float (it does in `BasicTerm_SC.check_pv_net_cf`) |
| generator expression, `math.isclose`, any module call | compiles, but as Python calls |
| a call with keyword arguments | the callee stays a plain Python method |

**F4 — Caches are fixed C arrays, and they are bounds-checked.** A cell with integer
parameters gets `double[N]` storage sized by `spec.py`'s `cells_param_size` (or by the
largest argument the sample used, plus one), and its generated wrapper raises `IndexError`
for any argument outside `[0, N)`. Two consequences: a formula may never call a cell at
`t < 0` — modelx evaluates negative `t` without complaint, the compiled model does not —
and `N` must cover the product's **contractual** maximum frame plus one for `t + 1`
look-aheads, not merely the shipped points. The reverse holds for **array** reads: mx2cy
sets no `wraparound` directive, so a memoryview read at index −1 — a policy-year column read
before issue — silently returns the last element rather than failing.

**F5 — Memory is per ItemSpace, and large.** Each cached cell embeds its arrays in the
compiled space's C struct: about 12 bytes per cell per month. The prototype's struct is
138 KB for eight cells at `N = 1,500`. `BasicTerm_SC` grows the process by 476 MB over
10,000 points at `N = 241`. A ~150-cell uslib model at `N ≈ 1,460` is ~2.6 MB per model
point, so a block run must release each ItemSpace once read (`del model.Projection[i]`,
which the export supports), or run in batches.

**F6 — `input_dir()` survives export and compilation.** An exported package defines
`BaseModel.path` as its own directory, compiled or not, so `Data.input_dir()`'s
`_model.path.parent` resolves to the directory that **contains** the package. A
`<Model>_nomx/` or `<Model>_nomx_cy/` package placed beside the CSVs needs no formula
change (verified on the compiled `UL_US_S`).

**F7 — Recursion depth is the runner's problem outside modelx.** modelx raises the
interpreter's recursion limit to 10⁶ (and on Linux the stack limit); the exported package
does neither, and a compiled model recurses on the C stack, which is 1 MB on Windows' main
thread. uslib frames run to ~1,460 months, against `BasicTerm`'s 241. No S model has a frame-long
backward recursion, and evaluating in ascending `t` keeps most recursions one step deep.
**Not all of them:** DIA prices at month 0 on survival read out to the payout date, so in
its export `net_cf(0)` alone needs a call depth of 517, and point 5 raises `RecursionError`
at the default limit even when swept in ascending order (verified). Runners and samples must
set `sys.setrecursionlimit`, and far-ahead reads need a non-recursive form (R2).

**F8 — The tooling assumes one model per product directory.**
`tools/gen_scaffolding.py` takes `next()` over the directory's model folders, so with two
models the result depends on filesystem order, and it writes `Data.rst` and
`Projection.rst` flat into the product page, where two models would collide.
`tests/test_model_conventions.py` asserts an `_S` suffix, a `point_id` parameter, and that
every CSV beside a model is read by *that* model. `.gitignore` already anticipates
`*_nomx/` and `*_nomx_cy/`.

---

## 3. Decisions

### D1 — Name, place, derivation

`<Name>_US_SEC` lives in `products/<product>/`, beside `<Name>_US_S`. It is created by
reading the S model and writing it back under the new name, so its **first commit is the S
model with only `_name` changed**: every later diff in that folder is an enhancement, and
nothing else. It reads the same assumption CSVs as the S model — one copy of each table —
and adds its own model point table, `model_point_table_sec.csv`.

*Rejected:* modelx space inheritance from the S model (bases must live in the same model);
a separate product directory with copied CSVs (two copies of every table drift apart).

### D2 — Strict sequence: E for all twelve, then C for all twelve

Phase 1 (E) is completed and merged for every product before Phase 2 (C) starts on any.
Phase 1 changes semantics and no representation; Phase 2 changes representation and **no
number**. Within each phase Term goes first, as the template, and the others follow in
chassis order (§5.3). Between the phases the `_SEC` models carry `stage: "E"` in the
registry, and the C-only conventions switch on at `stage: "EC"`.

*Why:* two reviewable diffs per product — "what running in force needs" and "how it is made
C" — and Phase 2 is gated by the Phase 1 suite, unchanged in substance. Phase 1 nonetheless
obeys the compile-neutral rules R1–R3 and R1a (D11), which constrain how in-force logic is
written without changing what it computes, so Phase 2 never has to restructure a recursion.

*Rejected:* an intermediate `_SE` model per product. It would put 36 models in the library
for a final state of 24; the stage key carries the same information.

### D3 — Time axis: the valuation clock

`t = 0` is the valuation date for every point and `t` counts projection months. The policy
clock is `duration_mth(t) = duration_mth_init() + t` — the closed form the UL family and VA
already use, not BasicTerm_SE's recursion, which would be one more recursion chain in the
compiled model. `duration(t)`, `policy_year(t)` and `age(t)` keep their S definitions on top
of it, and `result_cf()` always covers `t = 0 .. proj_len() - 1`.

On a new-business point issued at `t = 0` the two clocks coincide. That is what turns every
S worked example into an SEC test case without restating it.

This amends the library's settled convention — "`t` counts policy months, `t = 0` is the
issue month", "`t_first` is the elapsed periods for an in-force point" — for the SEC family
only. `index.md`'s convention table gets an SEC column rather than a footnote.

### D4 — New business at `t = 0` and after, as in BasicTerm_SE

The model point's `duration_mth` is positive for a policy in force, 0 for one issued at
`t = 0`, and negative for future new business issued at `t = -duration_mth`. Every state
variable is zero before issue. `t_entry() = max(0, -duration_mth_init())` is the first
month the policy is on the books, and every recursion's base moves from S's `t == 0` to
`t == t_entry()`: the opening state from the model point when in force, the issue values
otherwise. `is_active(t)` is false before issue and after cover ends.

*Fallback:* if future new business proves disproportionate for a product (§8, risk K4),
that product's `Data` rejects `duration_mth < 0` with a clear error and its `model-sec.md`
says so. The rest of the design is unaffected.

### D5 — Counts: BasicTerm_SE's entry, uslib's row weight

- Model point columns `policy_count` and `duration_mth`, as in BasicTerm_SE.
- `pols_if_init()` is `policy_count` if the point is in force at `t = 0`, else 0;
  `pols_new_biz(t)` is `policy_count` in the issue month; both as in BasicTerm_SE.
- `pols_if_at(t, "BEF_NB")` is the count carried in from `t - 1` (`pols_if_init()` at
  `t = 0`), and `pols_if_at(t, "BEF_DECR")` adds new business.
- **`pols_if(t)` is `pols_if_at(t, "BEF_DECR")`**, not BasicTerm_SE's `BEF_MAT`. The
  library settled `pols_if(t)` as the count that weights row `t`, and this is the definition
  under which it equals the S model's `pols_if` on every new-business point.
- Each S model's own later timings (`BEF_SURR`, `AFT_DECR`, …) and its maturity rule
  (survivors exit at the end of the last month) are kept. BasicTerm_SE's start-of-period
  `BEF_MAT` maturity is not adopted: the S goldens put expiry at the end of the final
  month. Nor is the **name**: WholeLife already has a `BEF_MAT` that means the end of the
  month after surrenders, the opposite end of the month from BasicTerm_SE's. `BEF_NB` is the
  only timing SEC introduces, plus `BEF_DECR` where an S model lacks it.
- SPIA is the one exception to the row-weight rule. Its `pols_if` is a closing measure —
  contracts with an obligation still open — so `pols_if(0) != pols_if_init()` even in S
  (0.99999986 on point 8). It keeps its S definition, new business enters through
  `lives_if`'s opening, and the registry marks it so the `pols_if == BEF_DECR` convention
  skips it. DIA's `pols_if` (`pols_if_init * l_last`) is a start-of-month count and follows
  the rule.
- `result_cf()` keeps the S columns exactly; the SEC-only quantities go in a new
  `result_pols()`, as BasicTerm_SE does it.

### D6 — The opening state of an in-force point

Each state variable gets one model point column, `<cell>_init`, per policy. It holds the
value at the **start of month 0, before any month-0 event**: the `BEF_NB` instant, which
for an account value is the `BEF_PREM` instant of the CashValue_SE timing vocabulary. The
defining property is operational: it is exactly what the S model carries into month `d`,
and the splice identity of §5.2 tests it.

- A quantity fixed at issue and not re-derivable from static data (a payout amount, a
  locked rate, a solved premium, an index level at term start) is a column too, for the
  reason BasicTerm_SE reads its premium from a table.
- `Data` validates the in-force columns on read, vectorized, and raises naming the
  offending `point_id`: no negative balances, flags consistent with balances, a phase
  consistent with the account value.
- The S tables' mixed spellings — `_init`, `_initial`, `_inforce`, `duration_inforce`
  (years), `duration_mth_init`, `entry_year` — become this one vocabulary in the SEC tables.
  Each `model-sec.md` records the mapping.

### D7 — Two clocks for inputs

- **Contractual schedules** — premium and cash value tables, COI and surrender charges by
  policy year, guarantee periods, rider charges — are read on the **policy** clock,
  `duration_mth(t)` and `policy_year(t)`, as in S.
- **Economic inputs** — rate, yield, fund return and index paths, and expense inflation —
  are read on the **valuation** clock `t`, shared by every point in a block.

Expense inflation shows what moves. The S models carry three conventions —
`(1+i)^(t/12)` (Term, WholeLife, FIA), `(1+i)^(policy_year - 1)` (UL, IUL, VUL, ULSG, SPIA,
DIA) and `(1+i)^duration(t)` (MYGA, RILA) — all on the policy clock. Each keeps its step
shape but moves onto `t`, as BasicTerm_SE inflates on `t`: unit costs are then in
valuation-date dollars, and on new business at `t = 0` nothing changes.

What *does* change is every S row that is already in force. S inflates FIA's in-force points
from issue (their `expenses(84)` carries `1.025^7`), and its scenarios for those rows are
read from the policy month they entered at. Under D7 their SEC twins differ by design. So
the twin identity is asserted exactly on new-business twins only, and S's in-force rows are
verified by the splice harness, with valuation-clock inputs neutralized or re-based (§5.2).
Mortality improvement measured from the projection start, as ULSG does, is the same kind of
input.

A point-to-point quantity measured on a market path whose term began before `t = 0` needs
the path's value at term start. That value is an opening-state column under D6.

### D8 — Files per product

Beside the S files: `<Name>_US_SEC/` (formulas only, `Data` and `Projection`),
`model_point_table_sec.csv`, `run_sec.py` and `model-sec.md`; at Phase 2, `sample_sec.py`
and `spec_sec.py`, mx2cy's two inputs. The SEC table holds:

1. **every S row**, with the same `policy_id` — the twins of §5.2. An S row that is in force
   on the policy clock (WholeLife's `duration_inforce = 9`, FIA's `entry_year = 7`) becomes
   an in-force SEC row at `duration_mth = 108` / `84`;
2. **derived in-force rows**: S new-business points restated at chosen months `d`, with
   provenance columns `source_policy_id` and `source_mth`;
3. at least one **future-new-business** row.

Rows of the second kind are written by `tools/gen_sec_points.py` from state definitions
that live in the test helpers, and a test regenerates them and compares, so the committed
table cannot drift from what the S model computes. The generator writes the other two kinds
too, from the S model and its table as they stand: a twin from its S row, a future row from
an S new-business row. No row is typed by hand, so the test covers the whole table, text
included.

This matters because S rows do change after the fact. MYGA points 5 and 6, RILA point 9 and
VA point 6 have had their `provenance` reworded under `CLAUDE.md`'s rule, and FIA point 3's
roll-up key has been renamed. A hand-copied twin of FIA point 3 would now raise `KeyError`
against the shared roll-up table, and no projected number would ever reveal the four stale
`provenance` cells.

Some SEC rows need inputs S never had:
- a scenario re-based to the row's valuation date (VA, FIA);
- an in-force ladder (IUL).

These go in SEC-only companion files (`*_sec.csv`), never into the shared S inputs. Where
they derive from S data they are generated the same way, under the same test.

The SEC table and its companions are input files as `CLAUDE.md` defines them, so none of
their columns may name a company or product. Every text cell the generator writes — id,
label or `provenance` — is either copied from S, a copy T6 keeps current, or composed from
S's own keys (an S `policy_id` or scenario id) and a month. It adds no name of its own.

### D9 — Documentation

Each product gets `model-sec.md`: the in-force interface (columns, units, the instant each
is measured at), the two clocks, the departures from S, and from Phase 2 on the C
representation, how to compile, and measured speed. `gen_scaffolding.py` learns to handle
several models per product. The product landing page lists both, and the autodoc pages move
under per-model folders (`products/<slug>/<Model>/{<Model>,Data,Projection}.rst`) for S and
SEC alike. This is a one-time URL change, taken now, before the lifelib merge, while it
costs nothing. `index.md` gains the SEC family in its models table and its convention table.

### D10 — Registry and conventions

`us_registry.MODELS` gains twelve SEC entries whose metadata adds `"twin"` (the S name),
`"param"` (`"point_id"`, then `"idx"`) and `"stage"` (`"E"`, then `"EC"`), and
`INPUT_FILES` gains their file sets. `test_model_conventions.py` is generalized rather than
forked:

- the suffix rule becomes `_S` followed by the capability letters the metadata grants;
- the parameter is the one the metadata names;
- model points are enumerated through one helper that yields labels or positions;
- "every CSV beside the model is read" becomes "by some model in the directory";
- "a runner and a `model.md`" becomes "and, for SEC, a `run_sec.py` and a `model-sec.md`";
- `model_point()` stays in the shared vocabulary, as a reporting accessor
  (`data.model_point_table().iloc[idx]` after Phase 2). C5 forbids projection cells from
  calling it.

New conventions for the SEC family:
- the frame starts at `t = 0`;
- `pols_if(t)` equals `pols_if_at(t, "BEF_DECR")`, except on SPIA (D5);
- the `pols_new_biz` column sums to the new-business `policy_count`;
- nothing is active before issue, and the pre-issue rows are zeros, not NaN;
- the in-force columns are present;
- the twin identity of §5.2 holds.

### D11 — Rules for the C representation

R1–R3 and R1a bind from Phase 1 on; R4–R17 are Phase 2's work.

- **R1** No cell is called with a negative argument. Look-back stops at `t_entry()`, and
  anything earlier is opening state (F4). A table read whose index is a policy year or an
  attained age is guarded by `is_active(t)` or clamped, because before issue it would
  wrap rather than fail.
- **R1a** No call passes a **policy month** as `t`. On the valuation clock `t` is not a
  policy month, so S idioms that were harmless become silent errors:
  - Term's `jump_ratio()` reads `premium_pp_ann(12 * n)`;
  - WholeLife's `div_prev_anniv` indexes `12 * duration(t) - 1` and `anniv_mth()` returns
    `12 * duration(t) + 11`;
  - `cv_pp(t - 12)` stands in for last anniversary's value.

  These become policy-year-keyed cells — `premium_pp_ann_py(y)`, `cv_pp_anniv(y)` — or
  opening state. The twin identity cannot catch a violation, because on new business the
  two clocks coincide; the splice identity of §5.2 is the test that does.
- **R2** Recursions run forward: bases at `t_entry()`, look-ahead at most `t + 1`, and no
  backward recursion over the frame (F7). A formula that needs a value far ahead of its own
  `t` takes it from a non-recursive form — an explicit loop in one cell, or a vector built
  in `Data` — as DIA's month-0 pricing must, since it reads survival out to the payout
  date.
- **R3** Phase 1 adds no new Python-object machinery: no new string-valued cells, no new
  Series or tuple returns, no new pandas lookups in `Projection`.
- **R4** `Projection` is parameterized by `idx`, and `point_id()` returns the label for
  reporting.
- **R5** `Data` keeps the S CSV readers unchanged (read once, `object`-typed) and adds one
  array cell per input the projection uses: int64 for ages, durations, counts, codes and
  flags; float64 for amounts and rates. Never bool, object or string dtypes.
- **R6** Decode in `Data`, to the number the formula needs. A categorical string becomes
  the quantity it selects — `premium_mode` becomes `prem_cycle` and `modal_factor`,
  `rate_class` becomes the class factor, `plan` becomes `policy_term`. Where a code must
  survive, it is an int code with named int References in `Projection`.
- **R7** Tables become integer-indexed arrays. Age-keyed tables are padded from age 0, as
  `mort_table_array` is. String-keyed multi-key tables are pre-joined per point into
  `[idx, policy_year]` arrays. Scenarios become `[scenario, t]` arrays, with a per-point
  scenario index.
- **R8** A blank override becomes a value array plus a 0/1 flag array; no `pd.isna` or NaN
  test runs in `Projection`.
- **R9** String parameters become named int References: `pols_if_at(t, BEF_DECR)` with
  `BEF_DECR = 2`, `claims(t, DEATH)`. The names stay those of the strings, so call sites
  read the same minus the quotes.
- **R10** No projection cell returns a str, tuple, list, dict, Series or `None`. Status
  strings such as a phase become int codes, and the labels appear only in reporting cells.
- **R11** Scalars entering `Projection` are converted once, in accessor cells (`int(...)`,
  `float(...)`), and every boolean cell returns `bool(...)`, so tracing sees Python types
  (F3).
- **R12** Aggregations are explicit loops with plain accumulators. No generator
  expressions, `float` annotations or `math.isclose` in per-`t` cells, and no keyword-argument
  calls between cells. A `kind=None` "total" default becomes an explicit total cell. Seven
  models' `claims(t, kind=None)` traces `kind` as both `str` and `None`, so it compiles with
  an `object` parameter and a dict cache on `net_cf`'s hot path, and its generator sums at
  Python speed.
- **R13** `Data` arrays are read only by element subscript (F3): no `len()`, slicing,
  iteration or numpy calls in `Projection`. A size it needs is its own int cell.
- **R14** Cells with float parameters are engine functions, not cached cells. IUL's
  `index_credit_rate(..., cap=None)` and ULSG's `sg_pp_solve(t, prem)` build float-keyed dict
  caches of 900 to 18,300 entries. They become uncached cells (`is_cached = False`, which
  modelx 0.33 serializes and its exporter emits without cache storage) or are inlined.
  `None` sentinels become float sentinels or int codes.
- **R15** A banded two-parameter cell is re-keyed to the band. IUL's six `(t, m)` segment
  cells are live only for `m <= t <= m + 11`, yet would compile to 912 × 912 arrays,
  ~50 MB per ItemSpace. Keyed by slot `k = t - m` in `0..11`, the cache is 912 × 12 —
  the same shape as the in-force ladder of D6.
- **R16** Python rounding is precomputed in `Data` with the built-in `round`, element by
  element, never `numpy.round`, whose half-way rule differs. ULSG rounds its COI scales
  with `round(r, dp)`.
- **R17** Reporting cells (`result_*`, `model_point()`) may stay Python. They are the
  typing guard's allowlist (§6.2).

### D12 — Compiled artifacts are built, never committed

`tools/build_sec_cy.py <product> [--out DIR]` exports the SEC model to
`<out>/<Model>_nomx/`, copies the CSVs to `<out>` when it is not the product directory, and
runs mx2cy with the product's `sample_sec.py` and `spec_sec.py`, writing `setup.py` to
`<out>`. The default `<out>` is the product directory, which `.gitignore` already covers
for `*_nomx/` and `*_nomx_cy/`; add `build/`, `setup.py` beside a model, and `*.so`. Tests
build into a temporary directory, which keeps the tree clean, exactly as
`test_round_trip_is_stable` already copies CSVs. modelx-cython goes in a new
`requirements-cython.txt`, because it needs a C compiler; `requirements.txt` is unchanged.

### D13 — CI

The existing matrix runs every pure-modelx suite, S and SEC alike. A new `cython` job —
ubuntu-latest and windows-latest, one Python each — installs `requirements-cython.txt` and
runs `pytest -m cython`. The compile tests **skip** when modelx-cython or a compiler is
absent, so lifelib's own bare `pytest` stays green after the merge.

---

## 4. Phase 0 — shared infrastructure

One PR, before any model:

1. **Registry**: metadata keys of D10, plus helpers `point_keys(model)` and
   `projection(model, key)` so no test indexes `Projection` by hand.
2. **Conventions**: the generalizations of D10, with every S model still passing them
   unchanged.
3. **`tests/sec_support.py`**:
   - the twin comparison: every shared cell, at every argument tuple the S cell cached
     (T1);
   - a splice helper that writes a temporary input directory: the SEC model, the CSVs,
     extra model points, and valuation-clock inputs shifted by `d`;
   - the per-product state-extraction registry that `tools/gen_sec_points.py` also uses.
4. **`tools/gen_scaffolding.py`**: several models per product, and per-model autodoc
   folders (D9).
5. **`tools/gen_sec_points.py`**, and **`tools/build_sec_cy.py`**, which stays inert until
   Phase 2.
6. **Housekeeping**: `.gitignore` additions; `requirements-cython.txt`; a `cython` pytest
   marker registered in `uslib/tests/conftest.py`; the CI job, defined but allowed to find
   no tests.

---

## 5. Phase 1 — E: in force at time 0

### 5.1 The recipe, per model

1. Copy S to SEC, renaming only (D1). Commit.
2. `Data`: point `model_point_file` at `model_point_table_sec.csv`; validate the in-force
   columns (D6).
3. Clock and counts: `duration_mth_init()`, closed-form `duration_mth(t)`, `t_entry()`,
   `is_active(t)`, `pols_if_init()`, `pols_new_biz(t)`, the `BEF_NB` and `BEF_DECR` timings,
   `pols_if(t)` (D5). `proj_len()` becomes the S frame from issue less
   `duration_mth_init()`.
4. State: every recursive cell's base reads `<cell>_init()` for a point in force at `t = 0`
   and the issue value at `t_entry()` for new business. Everything is zero before issue.
5. Anniversary and term logic that looked back across `t = 0` takes opening-state columns
   instead (R1).
6. Inputs: assign each input to its clock (D7).
7. Reporting: `result_cf()` with the S columns; `result_pols()`.
8. Docstrings: rewrite the time-axis prose — every "t = 0 is the issue month" — add the
   new cells to the symbol map, and keep the house disclaimers the conventions assert.
9. `model-sec.md`, `run_sec.py` and the SEC input files: `model_point_table_sec.csv` and
   any `*_sec.csv` companion (D8). Before each commit that adds or changes one, search it
   case-insensitively for every publisher and product the product's `sources.md` cites, as
   `CLAUDE.md` requires. T6 keeps the files in step with S, but it does not look for names.

### 5.2 Tests

Each product gets `tests/test_<product>_us_sec.py`; T1 is generic and lives in the
conventions suite.

- **T1 — Twin identity, cell by cell.** Run the S model's own sweep first. Then, for every
  SEC row whose S twin is new business, every cell the two models share must agree at every
  argument tuple the S cell has cached, enumerated with modelx's `Cells.keys()`. Through it,
  every S worked example is an SEC assertion with no golden restated, including the many
  goldens on intermediate cells (MYGA's surrender traces, WholeLife's dividend steps) that a
  `result_cf()` comparison would miss. In Phase 2 the comparison maps string arguments to
  the int References of the same name (R9).
- **T2 — Splice identity.** The test that says the opening state is complete. For S
  new-business points, at months `d` chosen to straddle each product's events (§7), an SEC
  point opened with the S state at `d` reproduces S from `d` on, for every result column
  and every state cell, to 1e-9. Valuation-clock inputs are shifted by `d` in the temporary
  input directory, and `inflation_rate` is set to 0 in both models (D7), as is mortality
  improvement where it runs from the projection start. A missing state variable fails here
  and nowhere else.

  **S's own in-force rows are splice cases too.** On the policy-clock models their frames
  align at offset `d`: WholeLife at 108, FIA at 84. On the projection-clock models they
  align at offset 0: UL at 120, ULSG at 300, VUL at 24 and 120, VA at 26. Any input S read
  on the policy clock is re-based by the months already elapsed — VA's scenarios by 26 —
  so those goldens carry over as well.
- **T3 — Future new business.** `duration_mth = -k` reproduces the new-business frame
  shifted by `k`, with zeros before issue, given inputs shifted by `-k`.
- **T4 — Count algebra.** `BEF_DECR = BEF_NB + pols_new_biz`; the roll-forward closes;
  doubling `policy_count` doubles every cash flow and leaves every per-policy value alone.
- **T5 — Validation.** Each malformed in-force row raises in `Data`, naming its point.
- **T6 — Regeneration.** The committed SEC table and its generated companions, every row
  and column, equal what `gen_sec_points.py` produces from the S model and its inputs as
  committed. So an edit to an S row that an SEC file copies or derives from — a reworded
  `provenance` cell, a renamed lookup key — fails T6 until the SEC files are regenerated,
  in the same commit.

### 5.3 Order

Term → WholeLife → UL → VUL → ULSG → IUL → MYGA → FIA → VA → RILA → SPIA → DIA.

- The template goes first.
- Then each chassis — life, deferred annuity, payout — comes before the products that
  build on it.
- Within a chassis, the product nearest to BasicTerm_SE comes first and the largest last.
  VUL already keys issue events on `duration_mth`; IUL needs the segment ladder.

One PR per product. §7 gives each product's size.

### 5.4 Exit criteria

- All twelve pass T1–T6 and the generalized conventions.
- `python tools/doccheck.py` reports zero.
- The existing CI matrix is green inside its 90-minute timeout. The SEC suites roughly
  double the projected volume, so §8's K6 measures that before the timeout is touched.
- A compact fingerprint per SEC point is frozen: each result column's sum and its values at
  five fixed months, hard-coded so a reviewer can read them. Phase 2 must reproduce it.

---

## 6. Phase 2 — C: compiled

### 6.1 The recipe, per model

1. `point_id` → `idx` (R4).
2. `Data` array cells and decoding (R5–R8). §7 lists the tables each product turns into
   arrays.
3. `Projection` accessors and lookups rewritten onto `data.x()[idx]` (R11).
4. Timings, kinds and phases as named int References (R9, R10).
5. Aggregations rewritten as loops (R12); float-parameter engine cells uncached (R14);
   banded caches re-keyed (R15); rounding precomputed (R16).
6. `sample_sec.py`: set the recursion limit, then call every `Projection` cell at least
   once over points that take every branch — `result_cf()`, `result_pols()`, every
   `check_*`, every timing of every `*_at` cell. Untraced means untyped (F3).
   `spec_sec.py`: `cells_param_size` for `t`, and for each multi-parameter tuple, from the
   product's contractual maximum frame, plus one for the `t + 1` look-ahead and one of
   headroom, with the derivation in a comment (F4).
7. Docstrings, `model-sec.md`'s compiled-model section, and `run_sec.py --cython`, which
   builds through `build_sec_cy.py` and releases ItemSpaces in block runs (F5).

### 6.2 Tests

All marked `cython` unless noted.

- **C1 — The Phase 1 suite still passes** (not marked `cython`). Only call syntax changes:
  positions instead of labels, timing References instead of strings.
- **C2 — Fingerprints.** The Phase 1 freeze reproduces to 1e-12 relative (not marked
  `cython`).
- **C3 — Typing guard.** Read the generated `_mx_classes.pxd`. Every `Projection` cell
  outside the R17 allowlist must return `bint`, `long long` or `double`; no `Projection`
  cache may be a `dict`; every `Data` cell the S twin does not have must return a typed
  memoryview or a C scalar. This guard is what "expressed in primitive C types" means in practice.
- **C4 — Compiled equals modelx.** On every point, every result column and every timing,
  to 1e-12 relative.
- **C5 — No pandas in `Projection`** (static, not marked `cython`). Outside the allowlist,
  no `Projection` formula refers to `pd`, `np`, `model_point`, `.loc`, `.iloc` or
  `iterrows`, or returns a string literal.
- **C6 — Benchmark** (a script, not a test). modelx, export and compiled timings on a
  replicated table, recorded in `model-sec.md`. The target is BasicTerm_SC's order of
  magnitude; a shortfall is reported, not hidden.

### 6.3 Exit criteria

- All twelve at `stage: "EC"`, passing C1–C5 on Linux and Windows in the `cython` job.
- C6 recorded for each.
- `doccheck` reports zero.

---

## 7. Per-product notes

These notes come from a read of every S model's `Projection` and `Data`, its notes and its
test module. Every point in each shipped table was projected with caches harvested, and
**re-opening experiments** were run: an S new-business point restated as in force at
month `d`, from its own state, and compared row by row. The experiments are what turned
several "accepts an opening value" claims into "accepts it, but…".

| Model | S clock today | In force in S | E | C | The crux |
|---|---|---|---|---|---|
| Term | policy | — | S | S | `jump_ratio()` passes policy months as `t` |
| WholeLife | policy, late frame | whole years | L | M | dividend accumulation and last dividend; four `t`-index idioms |
| UL | projection | yes | S | M | four accumulators restart at `t = 0` |
| VUL | projection | yes | S | L | loan collateral ≠ debt; ~60 timing call sites |
| ULSG | projection | yes | M | M | grace counter; improvement clock; solver off the hot path |
| IUL | projection | lossy | L | L | 12-segment ladder; `(t, m)` caches |
| MYGA | policy | — | M | M | four anniversary-dated values; four R1a violations |
| FIA | policy, late frame | anniversaries | M | L | fixed account; month-resolved scenario; phase strings |
| VA | projection | partial | L | L | ten missing state items; scenarios keyed by policy month |
| RILA | policy | — | L | L | everything: term-start market state; Black–Scholes engine |
| SPIA | policy | — | L | M | per-life status; commutation; the `pols_new_biz` ban |
| DIA | policy | — | L | L | pricing and projection survival must part |

Each note gives a size for Phase 1 and for Phase 2, where **S**, **M** and **L** are small,
medium and large. The splice months are the T2 months, chosen to straddle the product's
events. "Never reached" lists cells that `result_cf()` and the checks do not evaluate:
`sample_sec.py` must call them, or they compile as `object` (F3).

### 7.1 Term — `Term_US_SEC` (E: S, C: S)

*Today:* policy clock, new business only. A `duration_inforce` column (in years) is read by
no formula.

*E:*
- The only state is `pols_if`, so the in-force interface is just `policy_count` and
  `duration_mth` (months).
- Rebase every test of the frame index (R1a):
  - the shock month `t == 12n - 1`;
  - `jump_ratio()`, which reads `premium_pp_ann(12n)` / `premium_pp_ann(12n - 1)` with
    policy months passed as `t`, becomes a ratio of `premium_pp_ann_py` on policy years
    `n + 1` and `n`;
  - expiry in `pols_if`, `pols_maturity` and `phase`;
  - acquisition at `t == 0`, which S charges flat regardless of count, becomes
    `expense_acq * pols_new_biz(t)`.
- Inflation moves to `t` (D7).
- Splice months: 1, 12, 119 (the shock), 120 (first ART premium), 121, 719 (the last).

*C:*
- To arrays: the premium schedule, a 5-key `.loc` per `t`, becomes `[idx, policy_year]`;
  base mortality `[age]`; the class factor and the shock lapse rate (`iterrows` today) are
  computed per point in `Data`.
- Decoded: `plan` to `policy_term`; `premium_mode` to `prem_cycle` and `modal_factor`; the
  M(1) override to a value plus a flag; `phase` to a code.
- Never reached: `pols_lapse`, `pols_maturity`, `phase`.

### 7.2 Whole life — `WholeLife_US_SEC` (E: L, C: M)

*Today:* policy clock, with in-force support in whole years only. `proj_start()` is
`12 * duration_inforce`, the frame is `proj_start() .. proj_len() - 1`, and
`proj_len() = 12 * (100 - x)` is not net of elapsed months. Point 1 is in force at year 9
(frame 108..659).

*E — what the re-opening experiment at year 9 found:* PUA, a 20 % loan, the PUA rider, the
term blend and final expense reproduce exactly. Dividend **accumulation** and **reduce
premium** do not:
- `div_accum_init`: the opening balance is hard-coded to 0, and the ACCUM copy's maturity
  claim is off by 1,060.82;
- `div_prev_init`, last anniversary's dividend: REDUCE_PREM collects 1,800 instead of
  1,511.34 at the first projected month;
- `prem_cum_init`, for final expense's graded benefit, because `prem_cum` recurses to
  issue;
- `puaf_inforce` and `loan_inforce` are renamed `pua_face_init` and `loan_bal_init`;
- a mid-year valuation, impossible in S, also needs the PUA face and the loan at the start
  of the policy year.

*E — rebase (R1a):*
- acquisition at `t == 0`, which on the valuation clock would charge every in-force point
  0.9G + 250;
- `div_prev_anniv`'s `12 * duration(t) - 1` and `anniv_mth()`'s `12 * duration(t) + 11`,
  both used as `t`;
- `div_int`'s `cv_pp(t - 12)`, which becomes `cv_pp_anniv(duration(t))`;
- `pua_face_rider`'s `nsp_mth(t - 1)` at `t = 0`;
- `lapse_rate` and `cv_pp_anniv`, which take `proj_len() // 12` as the years to maturity —
  `proj_len()` changes meaning.

The S goldens read pre-frame values (`pua_face(107)`, `loan_bal(107)`, `cv_pp(107)`,
`pua_cv(107)`); in SEC these are opening-state cells at `t = 0`.

Splice months: 12, 108, 120, 600, and one mid-year month.

*C:*
- To arrays:
  - premium rates (product, sex, class, age);
  - cash values (period, sex, age, y) to `[idx, policy_year]`;
  - NSP and guaranteed mortality (sex, y) to `[sex, age]`;
  - two `model_point()` reads made per `t`.
- Six string attributes decoded.
- The hot `pols_if_at(t, timing)` (`BEF_DECR`, `BEF_SURR`, `BEF_MAT`, `AFT_DECR`) moves to
  int References.
- `claims(t, kind=None)`, on `liability_cf`'s hot path, splits into `claims_death`,
  `claims_lapse` and `claims_maturity` — the existing column names — plus a total.
- `div_round_digits = None` becomes an int sentinel.
- `cv_pp_anniv` (y 0..55) and `nsp` (y 45..100) share the `('y',)` cache, so one size
  covers both. A test calls `cv_pp_anniv(-1)`.

### 7.3 Universal life — `UL_US_SEC` (E: S, C: M)

*Today:* already on the projection clock, with `duration_mth_init()` and `av_pp_init` /
`loan_bal_init`, and point 3 is in force at `d = 120`. Re-opening point 1 at `d = 120` and
`125` reproduces S to 3e-13, except for the accumulators below. A negative duration fails
(`KeyError` on policy year 0). `pols_if_at` exists but returns `pols_if` for every timing,
and nothing calls it.

*E:*
- New opening state:
  - `sum_assured_init`, the current face; the original stays the surrender-charge base;
  - `wd_used_year_init`, which S forces to 0 at `t = 0`;
  - `cum_prem_init`, which restarts at 0 in force although the TARGET premium cap uses it;
  - `is_mec_init`, because the latch's base is `t > 0`.
- `crediting_rate_ann` and `comp_rate_ann` move to `t` (D7).
- Splice months: 1, 11, 12, 13, 107–120 (the lapse-shock window), 125.

*C:*
- `model_point()` sits behind about 20 attribute cells; six strings are decoded.
- Per-`t` pandas in `prem_persistency`, `corridor_factor`, `class_factor`, `mort_rate`,
  `lapse_rate_base` and `coi_rate_scale` (a Series) become age and policy-year arrays and a
  per-point `coi[idx, y]`.
- Timing and kind cells: `av_pp_at`, `av_at` (+`EOM`), `pols_if_at`, `claim_pp`,
  `claims_from_av`, and `claims(t, kind=None)`.
- Never reached: `gsp`, `glp`, `seven_pay_prem`, `wd_used_year`, `wd_free_pp`,
  `is_shortfall`, `cure_premium_pp`, `cum_prem_pp`, `gpt_limit`, `gpt_ok`,
  `seven_pay_limit`, `is_mec`, `pols_if_at`.
- `t` reaches 1,032. Two test fixtures override formulas, so they stay on modelx (C1).

### 7.4 Indexed UL — `IUL_US_SEC` (E: L, C: L)

*Today:* UL's clock, but no in-force point, and S's in-force entry **loses information**:
- `fa_pp_at(0)` is `av_pp_init - loan_bal_init`;
- the loan collateral opens at `loan_bal_init`;
- no index segment can predate `t = 0`.

Re-opening points 4 and 1 at `d = 60` and `65` misses the account value by about 5 % within
a year (50,922 against 53,730) and flips `nlg_in_effect`.

*E:*
- `fa_init`.
- The **segment ladder**: up to 12 live segments, each with its balance, months since
  creation, cumulative deductions and withdrawals (the credit base), the index level at
  creation, and the cap declared then if caps vary. It goes in a long companion table
  `inforce_segments_sec.csv` keyed `(point_id, slot)`, not 60 columns.
- `lca_init`, separately from the loan; both faces; `cum_prem_init` and
  `cum_prem_net_init`, the NLG accumulator.
- The MEC test: UL latches it and IUL does not. SEC adopts UL's latch and says so.
- At a mid-year valuation the current year's anniversary premium and loan draw are already
  inside the accumulators.
- Clocks:
  - `index_level(t)`, read on `duration_mth` today, moves to `t`;
  - `index_cap_at` and `fixed_rate_ann` also move to `t`;
  - `loan_credit_rate_ann` stays on the policy year;
  - `cred_rate_ann`'s `t < 12`, a projection-clock test, becomes a policy-clock one.
- Splice months: 1, 11, 12, 13, 60, 65, and point 4 (monthly premium, a full ladder).

*C:*
- R15: six `(t, m)` segment cells (`seg_share`, `seg_wd_pp`, `seg_ded_pp`, `seg_bal_pp`,
  `seg_ded_cum_pp`, `seg_wd_cum_pp`) are re-keyed by slot. This is the one Phase 2 change
  that restructures a family of cells, and the fingerprints and the Phase 1 suite gate it.
  A test calls `seg_bal_pp(0, -1)`.
- R14: `index_change`, `index_credit_rate(..., cap=None)`, `seg_credit_base(..., conv=None)`,
  `index_credit` and `seg_matured_value` become uncached. The `cap` sentinel becomes a
  float, `conv` an int code.
- Other strings: the References `basis` and `seg_credit_base_conv`, and `premium_mode`.
- Generator expressions in `seg_bal_active_pp`, `seg_bal_tot_pp`, `seg_count` and `claims`.
- Timing cells: `fa_pp_at` (6 timings), `lca_pp_at` (2), `av_pp_at` (5).

### 7.5 Guaranteed UL — `ULSG_US_SEC` (E: M, C: M)

*Today:* UL's clock. Point 1 **is** the in-force worked example (`d = 300`, AV 2,400,
SG 118,000, cumulative premium 270,000), so its golden table is already an SEC golden at
`t = 0..4`.

*E:*
- Already accepted: the account value (floored), the shadow account (never floored), the
  loan and `cum_prem_init`. Add `grace_mth_init`: the grace counter reads the month before
  `t = 0` as 0.
- **Mortality improvement already runs from the projection start** (`t // 12`, capped at 20
  years): a valuation-clock input under D7.
  - Re-opening point 2 at `d = 300` matches AV and SG exactly, but misses `pols_if` by 0.057
    and `net_cf` by up to 746 with improvement on, and is exact with it off. So T2
    neutralizes improvement, as it does inflation.
  - SEC keeps improvement from the valuation date, which is what S already does for its own
    in-force point.
- The no-lapse premium **solve** (`no_lapse_premium`, `sg_pp_solve`) is an issue-time
  computation. In SEC the premium is an input (already a column), and the solve is a
  Python-side utility outside the projection.
- The ROP window falls on policy anniversaries, so T2 includes a non-anniversary `d`, where
  improvement and policy anniversaries part.
- Splice months: 80, 81, 82 (grace, then lapse), 240, 300 (ROP windows), 305.

*C:*
- `premium_type` and `premium_mode`; `pd.isna` on `coi_rate_dp`, and on the persistency
  override inside a per-`t` cell.
- `round(r, dp)` (R16); `y in rop_table().index` becomes a zero-padded array; `status`
  becomes a code.
- Timing cells `av_pp_at`, `sg_pp_at`, `loan_bal_pp_at`; claim kinds DEATH, LAPSE, REFUND,
  WITHDRAWAL and GRACE, plus `None`; generator expressions in `claims` and `guar_min_sg`.
- The solver's float-parameter cells, with dict caches of 7,900 to 18,300 entries, become
  uncached and leave the hot path (R14).
- `t` reaches 732 through `is_lapsed(t + 1)`.

### 7.6 Variable UL — `VUL_US_SEC` (E: S, C: L)

*Today:* the closest to BasicTerm_SE. It runs on the projection clock with issue events
already keyed on `duration_mth == 0`. Points 1–2 are in force at 24 months and point 4 at
120 (with a fixed account and a loan); point 3 is new business. Re-opening point 3 at
`d = 37` and `200` reproduces S to 1e-9.

*E:*
- `la_init`: the loan collateral opens at `loan_bal_init` by a [std] assumption, and once
  interest accrues the two part (point 4: 0.015 a month in `net_cf`).
- `face_init`, the current face; the initial face stays in `units()` and the charges.
- The pricing path (`sa_pricing_pp(m, i)` …) is recomputed from issue, which is
  deterministic and needs no state, but its `m = duration_mth(t)` goes negative for future
  new business (R1).
- The first-month pins (`corridor_override_m1`, `coi_rate_override_m1`) keep `t == 0`. In
  SEC that is the valuation month, which is what the worked example — asserted at `t = 0` on
  in-force point 1 — means.
- The scenario table is keyed by projected `t`, so it is already on the valuation clock.
  T2 shifts it: point 1 re-opened at `d = 12` is off by 0.115 otherwise. Alternatively, T2
  uses the flat `LEVEL6` scenario.
- Splice months: 12, 37, 96, 108, 200.

*C:*
- `subaccount_ids()` returns a list and `"alloc_" + str(i)` names columns; these become an
  `n_sa` int and `alloc[idx, i]` / `sa_init[idx, i]`, 0-based.
- Returns become a dense `ret[scen, sa, t]`; COI a per-point `coi_guar[idx, py]`; corridor
  and mortality by age; lapse and persistency by policy year, clamped; the surrender charge
  per point.
- About 60 timing call sites (eleven `*_at` cells, including tuple-membership tests on the
  timing), plus kinds.
- `None` defaults on `claims` and `me_charge_pp(t, i=None)` become total cells.
- Nine cells carry generator expressions, which become loops over `range(n_sa)`.
- Never reached in the base run: the pricing path, `funding_ratio`, `prem_persistency_base`,
  `inv_return_mth`, `pols_if_at`. The sample sets `dyn_behavior_on = True`.
- The `_rejects` test matches the source text `raise ValueError("invalid timing")` and is
  rewritten.

### 7.7 Variable annuity — `VA_US_SEC` (E: L, C: L)

*Today:* the projection clock, but issue events are keyed on `t == 0` — the premium, the
acquisition expense and `av_change`'s opening — and these move to the issue month (D4).
Point 2 is in force at 26 months, carrying GWB, BB, RB, NP, RP, ADJ and the bonus end.

*E:* re-opening points at `d = 40` and `125` puts `net_cf` off by up to 156 and 773,
because these are missing:
- per-fund values `sa_init_i`: S splits the opening AV by the target allocation;
- contract-year-to-date accumulators that S resets at `t = 0` as though a year began:
  `sum_wd_pp`, `free_wd_used_cum_pp`, `gmdb_dfd_acc_pp` and `gmdb_factor_acc`, as
  `*_ytd_init`;
- `wd_this_year_init`, because `is_wd_year` scans `t >= 0` only;
- `rb_prior_anniv_init`;
- the highest quarterly contract value so far this contract year, the step-up base;
- `phi_glwb_init`, the VIX-linked fee in force, which S recurses from quarter 1;
- `depleted_init`. S opens through `depleted_flag(-1)`, which is also an `IndexError` once
  compiled.

*E — clocks:*
- The return and rate scenarios are keyed by elapsed **policy** month in S and move to `t`
  (D7); the transaction table stays on the policy clock.
- Inflation (`valuation_year + duration(t)`) mixes the clocks and moves to projection
  years.
- So the worked example's two readings — point 1 at `t = 26` equals point 2 at `t = 0` —
  hold in SEC only on a scenario re-based by 26 months. That scenario is a generated,
  SEC-only companion (D8).
- Splice months: 26, 40, 60, 71, 125, 131, 143, and a depleted month.

*C:*
- 13 string attributes and `phase(t)` are decoded.
- To arrays:
  - fund set to `alloc[idx, i]`;
  - returns, VIX and CMT, which S finds by a step search on every call, to
    `[scen, sub, month]`;
  - the premium and withdrawal schedules to `[idx, month]`;
  - GAWA% bands to `[grid, age]`;
  - CDSC to `[sched, yr]`.
- R14 for `lapse_itm_mult(m)` (5,435 cache entries), `fee_rate_vix_raw` and
  `fee_rate_vix_clip`.
- Generator expressions in eight cells, including the hot `av_pp_at`.
- `t_of_month` returns negative `t` before entry, unguarded on `vix_sq`'s path.
- Never reached: `charge_income_pp`, `claims_over_av`, `gmdb_claims`, `net_cf_ga`,
  `wd_charges`, `sa_weight`, `phase`, and three string attributes.
- S's `test_every_switch_is_exercised_by_a_model_point` pins `duration_mth_init` to
  `{0, 26}`; the conventions suite's `_va_residuals` samples `t = 0, 60, 120, 299`.

### 7.8 RILA — `RILA_US_SEC` (E: L, C: L)

*Today:* the policy clock from issue, with no in-force mechanism at all. All 15 points are
new business. `pols_if(t <= 0)` returns the opening count, so a negative `t` counts as in
force, and the premium and acquisition sit on `t == 0`. **The technical notes already list
the in-force attributes** — `term_start_index`, `term_start_mvr`, the investment amount,
the fixed and holding accounts, `rop_base`, and `lock_flag` / `lock_value` — but the model
ignores them, and the Performance Lock is not implemented.

*E:*
- Opening state:
  - `ia_init`, with its basis;
  - `term_start_index` and `term_start_mvr`;
  - the term-start option-pricing inputs — rate, dividend yield and volatility, or the
    budget alone under straight-line amortisation;
  - `cap_init`, because the cap is re-solved at renewal under `nge_reset`;
  - `fa_init`, `ha_init`, `rop_init`;
  - `av_anniv_init`, because the free-withdrawal base reads the absolute month `12*cy - 1`;
  - `fw_remain_init`, `av_init`;
  - a term-start month, if terms need not align with issue.
- The market scenario, keyed from issue in S, moves to `t`, with term-start values from the
  model point for terms that began before `t = 0`. `market_state(k < 0)` would fail on
  `max([])`. Withdrawals stay on the policy clock.
- Splice months: 35, 36, 59, 60, 71, 72 (term ends and the renewal), and one mid-term month.

*C:*
- Strings: six, plus `opt_legs()`, which returns a tuple of strings, and becomes int leg
  codes. `pd.isna` in `is_uncapped`.
- `market_state` builds a list on every call (12,602 cache entries) and becomes per-field
  `market[scen, k]`.
- Timing (14 cells), kind, bucket, leg, market and name parameters.
- Float-parameter cells: `norm_cdf` (5,838 entries), five Black–Scholes cells with six float
  parameters each, `opt_component`, `opt_portfolio`, `credit_rate_at(t, accrual)` and
  `opt_budget_at_cap`. The pure ones become uncached. Spot and tau become codes — current or
  term-start market, τ(t) or T — so `(t, leg)` caches become C arrays.
- `declared_cap_solved` repeats an 80-step bisection in every month of a renewal term; it is
  keyed on the term start, a speed-up that changes no number.
- **Existing defect to fix in S first:** the Projection docstring's `\|` (line 150) is an
  invalid escape. It raises a `SyntaxWarning` on every import, the only such case in the six
  libraries, and the SEC copy would inherit it.

### 7.9 SPIA — `SPIA_US_SEC` (E: L, C: M)

*Today:* months from the annuity date, with no in-force support. `pols_if` is a closing
measure (D5). Improvement is calendar-dated, from `annuity_year + duration(t)`.

*E:*
- Survival status per life at valuation, as a probability in `[0, 1]`. The same column
  serves a real record (1 or 0: a joint contract may have one life already dead) and the
  splice test (S's `lives_if(d, i)`). S treats the lives as independent, so per-life
  probabilities suffice.
- `commute_frac_cum_init`, which is path-dependent.
- Payments to date, for the refund forms. They are deterministic, so they may stay on the
  annuity-date clock with `k >= 0`.
- The certain months left follow from `duration_mth`.
- Future new business is an annuity commencing later. S deliberately excludes the single
  premium, and SEC keeps that.
- **A name clash to resolve:** S's tests forbid `pols_new_biz`, `pols_lapse` and
  `lapse_rate` on a SPIA. In SEC, `pols_new_biz` exists by D5, meaning annuities commencing
  in the month, and the SEC module keeps the ban on the other two.
- Splice months: 11, 12, 13, 24, the end of point 5's certain period (120), and the month
  after a scenario death.

*C:*
- Six string enums validated by tuple membership.
- `bool(model_point()[...])` on numpy-bool columns.
- NaN joint-life columns; `death_mth` via `pd.isna` and a built string key, which becomes a
  −1 sentinel.
- `commute_disc_convention`, a string Reference.
- Per-`(t, life)` `.loc` in `mort_rate_base` and `improvement_rate` becomes `[sex, age]`; the
  surrender charge becomes a clamped vector; the lists in `horizon_mths` and
  `commute_amount` go.
- Never reached: `duration_mth`, `lives_death`, `premium_net_pp`, `premium_tax_rate`,
  `qualified`, `surr_charge`.

### 7.10 MYGA — `MYGA_US_SEC` (E: M, C: M)

*Today:* the policy clock, new business only. `duration_mth(t) = t` exists but nothing calls
it. The premium, commission, acquisition expense and `prem_to_av` sit on `t == 0`, and
maturity on `t == proj_len() - 1`. Timings: `BEF_DECR`, `BEF_MORT` (after annuitization),
`BEF_LAPSE`, `AFT_DECR`.

*E:*
- Opening state:
  - `av_init`; `mgsv_init` (S starts it at 0.875 P); `prem_accum_gmir_init`;
  - `tax_basis_init` — the one input S already takes, as `tax_basis_initial`;
  - interest credited, both cumulative and as at the last anniversary: the interest-only
    free withdrawal is last year's interest, while the minimum-interest surrender cap uses
    the cumulative;
  - this year's free-withdrawal allowance, or the anniversary AV it is based on, and the
    unused remainder;
  - the declared rate in force and the MVA reference yield `i0` in force, when the
    redeclaration or the period start precedes `t = 0`.
- The guarantee-period position, surrender-charge clock, window, base lapse and age derive
  from `duration_mth`, on the assumption, which holds for the product, that every renewal
  period is `n` years.
- R1a, four violations:
  - `free_wd_base` reads `av_pp_at(12(y-1))`;
  - `free_wd_allow` reads `interest_credited_pp(12(y-1) - 1)`;
  - `credit_rate` reads `market_rate(redeclare_month)`;
  - `mva_ref_yield_locked` reads `mva_ref_yield(gp_start_month)`.
- Clocks: the rate scenario moves to `t`. All three shipped scenarios are one flat row, so
  no shipped number moves. Withdrawals stay on the policy clock.
- Splice months: 12; 30, after point 5's excess withdrawal; 60, the window; 61 and 89, a
  renewal period with `i0` re-locked (point 3 redeclares every anniversary).

*C:*
- 23 attribute cells. `free_wd_mva_exempt` becomes an int, not a numpy bool.
- To arrays: scenario rates (`.loc`, a list comprehension and `max` per call) step-filled
  into `[scenario, month]`; withdrawals into `[schedule, month]`; surrender charges into
  `[schedule, year]`; the age cap into `[age]`; the MVA duration factor into a 2-D array;
  mortality into `[age, sex]`.
- Eleven string cells, including `surr_charge_id(t)`. Timing and kind parameters, and
  `scenario_rate(t, name)`.
- `claims(t)` called from `net_cf` with `kind=None` becomes an explicit `ALL` kind.
- R14: `mva_pp_on`, `mva_factor_geometric`, `mgsv_rate_statutory`, `mva_ref_term_years`.
- Never reached: `tax_basis_pp`, `taxable_wd_pp`, `claims_over_av`, `gp_end`,
  `duration_mth`, `mgsv_rate_statutory`, `mva_ref_term_years`, `policy_id`, `tax_status`.

### 7.11 FIA — `FIA_US_SEC` (E: M, C: L)

*Today:* the policy clock with a late-opening frame. `entry_mth() = 12 * entry_year()`, so
entry falls on anniversaries only. 55 cells guard `t < entry_mth()` and fall back to the
`*_init` cells. Points 1, 3 and 7 enter at `t = 84`; the other six are new business.

**Re-entry already works:** a point re-entered at an anniversary from its own S state
reproduces S to 1e-6 across phases — INCOME, DEPLETED, joint, years 5 to 21 — with one
exception. Point 4, with 20 % in the fixed account, gets `av_fixed_pp_init = alloc_fixed * AV`
(22,700.40 against an actual 16,002.31), and its withdrawals are then off by up to 31.80.

*E:*
- Opening state:
  - `av_fixed_init`;
  - the phase as at the last anniversary, as a code (S reads the string `phase_initial`);
  - rider status;
  - the existing `*_initial` columns, renamed under D6.
- A mid-year valuation, which S cannot express, also needs the year-open AV and F — the
  credit, free-withdrawal and fixed-interest bases — and the index level at segment start.
- Rebase onto the policy clock: `mva_term` and the premium cells on raw `t`, and the
  `proj_len()` guards. `lapse_rate` looks up to 11 months ahead to `anniv_mth(t)`, which is
  harmless.
- Clocks:
  - The rate scenario is keyed by anniversary number from issue, and it is **not** flat:
    `worked` steps at anniversary 8. On `t`, new-business point 2 and in-force point 1 need
    the step at different months, so the SEC table uses re-based, month-resolved
    companions, step-filled from the anniversary levels so that S is reproduced at every
    anniversary.
  - Withdrawals, keyed by contract year, stay on the policy clock.
- S's goldens all sit on in-force point 1, at policy month 95; in SEC they are `t = 11`.
- Splice months: 60, 84, 95 (mid-year), 96, 144, 240.

*C:*
- 29 attribute cells and `pd.isna` ×7.
- Phase strings are returned and compared in about 25 cells, some by tuple membership.
  They become codes, and `result_glwb()` decodes them back to labels for the conventions
  suite's phase check.
- To arrays: `payout_rate(a, basis)` (`iterrows`) into `[age, basis]`; roll-up and
  withdrawals into `[id, year]`; surrender charge and vesting into `[year]`.
- String References `step_up_mode`, `rb_wd_convention` and `mva_collar_basis` (a test
  assigns the last of these) become int codes.
- Timing parameters on seven `*_at` cells, `credit_rate_on(r, method)`, and R14 for four
  float-parameter cells.
- Never reached: `wd_cum_pp`, `av_indexed_pp*`, `activation_rate`, `payout_rate_init`,
  `bonus_factor`, `claims_over_av`.

### 7.12 DIA — `DIA_US_SEC` (E: L, C: L)

*Today:* the policy clock, new business only. The payout date `T`, the premium months and
the option months (adjust, accelerate, commute) are policy-month indices compared with `t`
directly — R1a throughout. `pols_if = pols_if_init * l_last` is a start-of-month count
(D5).

*E — the one structural change in Phase 1.* S uses one survival curve, `lives_if`, for two
jobs: **pricing** each premium's paid-up slice at its own date, and **projecting**. On the
valuation clock these part.
- Pricing stays anchored at issue and premium dates. It is deterministic from static data
  and becomes a non-recursive vector (R2), which also removes the 517-deep recursion of
  F7.
- Projection opens at valuation from per-life probabilities.
- So the opening state is:
  - per-life survival probabilities;
  - cumulative premium CP (the ROP base, the refund base and QLAC room), the purchased
    income B, and the payments-as-if-alive G;
  - the frozen weights `surv_to_payout = l_last(T)`, `commute_weight` and the acceleration
    factor, wherever their dates precede `t = 0`.
- **"Contract open" is not "life alive"** in a certain period. S's certain-floor weight
  `l_last(T)` (0.715 on point 7 at `t = 300`) exceeds survivors (0.5577), because the open
  cohort includes beneficiary continuations. The in-force interface carries the
  continuation explicitly.
- Option months stay on the policy clock, compared with `duration_mth(t)`. Converted to `t`
  they would collide with the `-1` "never" sentinel.
- Splice months: 59, 60 and 61 around point 14's second slice; `T - 1`, `T`, `T + 1`; the
  option months of points 13–15.

*C:*
- To arrays: the premium schedule — filtered and sorted per call, then an `iterrows`-built
  dict and `dict.get` — becomes a dense `[idx, month]` array; the ROP factor a 3-D
  `[age, sex, years]` array; the payout factor, keyed by a string tuple, a per-point value
  from `Data`.
- Ten strings, plus `qlac_flags()`, which returns a list of strings.
- `annuity_factor` mixes int and float parameters, so it is R14.
- S's tests assert the dict and DataFrame returns of `premium_by_mth()` and
  `premium_schedule()`, so those readers stay in `Data` beside the arrays.
- Never reached: `guarantee_yrs`, `qlac_room`, `qlac_flags`, `accel_cost`,
  `payout_factor_calc`, `phase`, `market_type`, `is_qlac`, `other_qlac_premium`.

---

## 8. Risks and open questions

### 8.1 Risks

- **K1 — modelx-cython is at 0.1.0.**
  - Pin it in `requirements-cython.txt`.
  - C3 catches any regression in typing; the `cython` CI job catches compile failures on
    MSVC.
- **K2 — Memory (F5).**
  - A compiled block run that keeps its ItemSpaces holds ~2.6 MB per point.
  - `run_sec.py --block` releases each one as it goes, and `model-sec.md` says why.
  - The benchmark records peak RSS beside time.
- **K3 — Branch flips at knife edges.**
  - Floors such as `max(0, AV)`, depletion flags and NLG tests can turn a 1e-15 difference
    into a different branch.
  - The splice and C4 tolerances are relative, and the splice months avoid exact
    thresholds.
  - A flip that does occur is investigated, never loosened away.
- **K4 — Future new business on market products.** Each future point needs its inputs
  re-based in T3; RILA and VA carry the most. D4's fallback exists for exactly this.
- **K5 — A wide in-force interface.**
  - VA adds about ten opening-state columns, RILA about twelve, and IUL a 12-slot ladder.
  - Each must come from an administration extract that may not carry it — a VA's highest
    quarterly value this contract year, a RILA's term-start volatility.
  - Ladders go in long companion tables keyed `(point_id, slot)`. Two or three funds stay
    as wide `_init_<i>` columns, as VUL's are today.
  - Each `model-sec.md` documents, column by column, what the field is and the instant it is
    measured at. Where an approximation is defensible, its consequence is stated, and it
    stays out of the model.
- **K6 — CI time.**
  - The matrix already takes up to 33 minutes against a 90-minute limit, and the SEC suites
    roughly double the projected volume.
  - Measure it on Term in Phase 0. If it threatens the limit, the splice sweeps move behind
    an opt-in marker before the timeout is raised.
- **K7 — Tests that need modelx.** S tests that override formulas, reassign References and
  `clear_all`, or match `raise` source text, have no compiled equivalent. They stay in C1,
  and C4 compares numbers only.
- **K8 — Upstream packaging.**
  - lifelib's CI will not install modelx-cython, so the compile tests must skip (D13).
  - No build output may reach the wheel or sdist: `MANIFEST.in` should prune `*_nomx*` as
    it prunes `_research/` (MERGE.md §2).
- **K9 — DIA's two survival curves.** Separating pricing from projection survival is the
  only Phase 1 change that restructures a model rather than extending it. It goes last, on
  the most mature harness.

### 8.2 To confirm

Each of these is decided above with a recommendation. A different answer changes the
plan's shape, so it should be confirmed before Phase 0.

1. **Future new business (D4).** Support it, as BasicTerm_SE does? *Recommended: yes, with
   D4's per-product fallback.*
2. **Economic inputs on the valuation clock (D7).** Expense inflation and mortality
   improvement run from the valuation date, so unit costs are in valuation-date dollars.
   *Recommended: yes; it is BasicTerm_SE's choice, and changes nothing on new business.*
3. **Doc layout (D9).** Per-model autodoc folders for S and SEC alike, a one-time URL change
   for the S pages before the merge. *Recommended: yes.*
4. **Small S fixes found on the way** — RILA's invalid escape, the `pols_if_at` stubs in UL
   and VUL that return `pols_if` for every timing. Separate PRs on the S models, ahead of
   Phase 1? *Recommended: the escape, yes; the stubs are superseded in SEC and can stay.*
5. **The `cython` CI job on Windows from the start (D13)?** *Recommended: yes. MSVC and the
   1 MB main-thread stack are where a compiled model differs most.*

---

## 9. Milestones

| # | Milestone | Content | Gate |
|---|---|---|---|
| M0 | Phase 0 | Registry, conventions, scaffolding, `sec_support.py`, tools, CI job (§4) | every S model still green; Term's suite time measured (K6) |
| M1–M12 | Phase 1, one PR per product, in §5.3's order | §5.1 recipe, T2–T6, `model-sec.md`, `run_sec.py` | T1–T6 and conventions green; doccheck zero |
| M13 | Phase 1 freeze | Fingerprints for every SEC point; `index.md`'s SEC conventions | the whole matrix green under its timeout |
| M14–M25 | Phase 2, one PR per product, same order | §6.1 recipe, `sample_sec.py`, `spec_sec.py` | C1–C5 green on Linux and Windows; C6 recorded |
| M26 | Close | The `cython` job made required; a benchmark table in `index.md` | — |
