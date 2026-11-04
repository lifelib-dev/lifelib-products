# Plan — `*_US_SEC`: uslib models that run in force, then compile

**Status:** Accepted, 2026-11-01; drafted 2026-10-31. Phase 0 (M0) is done (§4, *Record*),
and so are Term and WholeLife, the first two of Phase 1 (M1 and M2, the *Records* of §7.1
and §7.2). The other ten run in three streams (§5.3). The Payout stream is complete: SPIA,
DIA and RILA are done (M11, M12 and M10, the *Records* of §7.9, §7.12 and §7.8). In each
of the other two the first two products are done: UL and VUL in the Life stream, and MYGA
and FIA in the Deferred annuity stream (M3 and M4, and M7 and M8, the *Records* of §7.3
and §7.6, and §7.10 and §7.11). Term's compile step, M14, brought forward to run beside
the streams (D2), is done on Linux, 2026-11-02; its Windows gate awaits the `cython` job's
first run (§7.1, *Record — M14*). The open decisions of §8.2 are settled, the last of
them, item 4, on 2026-11-03.
Like USLIB-MERGE-PLAN.md, this document is both the specification and the record: each
phase records what it actually did, including where the implementation departed from the
plan.

Every number in it was measured in this repository, or in lifelib 0.17.2, modelx 0.33.0 and
modelx-cython 0.1.0 as installed for the purpose, and each is quoted with the experiment
that produced it.

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
collects the benefit. M14: `Term_US_SEC` compiled runs 9.5 to 10.7 times its export on the
projection alone (6,000 points; 0.47 to 0.50 ms a point against 4.7 to 5.0, two runs on
2026-11-02 under loads of 0.9 to 3.0) and 4.7 to 4.9 times on `result_cf`, where building
the DataFrame dominates; `BasicTerm_SC`, timed on 2026-11-01 on its `pv_net_cf()`, 8.7
times; Term as Phase 1 left it, compiled by the same tool and timed the same day, 1.4
times (21.2 against 29.0 ms).

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
| the same parameter as a named int Reference (`BEF_NB = 0`, `BEF_DECR = 1`, dense from 0) | `long long`, cache `double[N][k]` for `k` codes: Term's `pols_if_at` `[1,046][2]` |
| returns a tuple, list, Series, DataFrame or `None` | `object`, dict cache |
| `o == o` on a `numpy.float64` (a NaN test) | `object` (traces as `numpy.bool_`) |
| a cell the sample never calls | `object` everywhere — untraced is untyped |
| a `Data` array used other than by element subscript anywhere (`len`, a slice, iteration, a numpy call) | the `Data` cell falls back to `object` — mx2cy's usage analysis must prove every use is element access |
| local `pv = 0.0; pv += ...` in a loop | inferred C `double`; an annotation `pv: float` stays a Python float (it does in `BasicTerm_SC.check_pv_net_cf`) |
| a generator, a comprehension, a module call (`math.erf`, `log`, `exp`, `sqrt` and `isclose` among them: Cython 3.3.0 maps no `math` function to C), a builtin other than `int`, `float`, `bool`, `abs`, `min`, `max` and `range` (`round`, `sum`), a list, dict or set built | compiles, as calls into Python inside a cell its declaration types as C; C5 reads them from the formula and C3 from the generated C (M14) |
| a call with keyword arguments anywhere in the model | every cell named like the callee stays a plain Python method (M14) |
| an uncached cell (`is_cached = False`), whatever its formula | `cpdef object f(object ...)`, whatever the spec says: mx2cy 0.1.0 traces only `_f_` formulas, `_mx_assign_refs` and `__call__` (`tracer.py`'s `MxCodeFilter`), an uncached cell has no `_f_` formula, and a spec `return_type` takes effect only on a traced cell (`config.py`); C3 rejects it, and C5 refuses it before any compile. With a generator, a lambda or a nested `def` in its formula it is a plain Python method instead, missing from the `.pxd` (M14) |
| a cached cell with a float parameter | the parameter `double`, the cache a Python dict: mx2cy gives a C array only to a cell whose parameters are all integers (`builder.py`'s `is_arrayable`), and C3 rejects a dict cache (M14) |
| a cached cell whose formula holds a generator, a lambda or a nested `def` | compiles, the closure running as Python inside its `cdef` `_f_` formula; C5 forbids it outside the allowlist (M14) |
| an integer local used in arithmetic, or any `for`/`while` counter, under Cython's default inference | a Python object even in a cell typed `double`; `build_sec_cy.py` marks each translated module `infer_types=True`, after which each is the C type of what is assigned to it, and one assigned only from int literals is a C `long`, 32 bits on Windows, which wraps (M14) |
| `x ** y` on two doubles under Cython's default `cpow=False` | a soft complex power, which gcc and clang compute with C99 `cpow`: 240 of Term's splice-grid values drifted by up to 2.4e-15, and `x < 0` raises `TypeError`; with `cpow=True`, C's `pow` on every compiler, bit for bit with Python on x86-64, NaN for `x < 0`, an int to a negative int truncating (M14) |
| `a * b + c` compiled for a target with fused multiply-add (`-march=native` or `haswell`, or an interpreter whose own `CFLAGS` target x86-64-v3) | one fused operation, one rounding where Python rounds twice, under gcc's default `-ffp-contract=fast` and clang's `on`: Term built with `-march=native` gave `plt_mort_factor(10)` 2.15 where modelx gives 2.1500000000000004; `build_sec_cy.py` appends `-ffp-contract=off` to `CFLAGS` off Windows, and MSVC emits none for x64 without `/arch:AVX2` (M14) |
| a flag returning `0` in one branch and a `bool` in another | `long long`, 0/1 where modelx returns `False`/`True` |
| a float in a branch the sample never takes, in a cell traced as `int` | does not compile |
| `int(x[i])` or `float(x[i])` on a memoryview element | a C load and cast |
| a `numpy.int64` or `numpy.float64` returned or passed | `long long` / `double`: mx2cy classifies a traced type by `numbers.Integral` and `numbers.Real`; `numpy.bool_` is neither, hence `object` (M14) |
| a `Data` array no formula reads | `object`: an array is typed from its uses, which C3 reports for a `Data` cell the twin lacks unless it reads a file (M14) |
| a `Data` array used whole by another `Data` cell | `object` |

In M1's representation 53 of Term's 62 cells already typed as C scalars while their bodies
called pandas, and the compiled model ran 1.4 times its export: typing is necessary and not
sufficient, which is why C5, and C3's reading of the generated C, exist (M14).

**F4 — Caches are fixed C arrays, and they are bounds-checked.** A cell with integer
parameters gets `double[N]` storage sized by `spec.py`'s `cells_param_size` (or by the
largest argument the sample used, plus one), and its generated wrapper raises `IndexError`
for any argument outside `[0, N)`. Two consequences: a formula may never call a cell at
`t < 0` — modelx evaluates negative `t` without complaint, the compiled model does not —
and `N` must cover the product's **contractual** maximum frame plus one for `t + 1`
look-aheads, not merely the shipped points. The reverse holds for **array** reads: the
generated C keeps Cython's `boundscheck` and `wraparound`, so a memoryview read at
index −1, a policy-year column read before issue, silently returns the last element rather
than failing, and one past the end raises `IndexError` (M14: `Projection[-1]` is the
table's last point in both engines). `N` must also cover every argument a cell is called
with in the month after the frame, `t = proj_len()`, which the roll-forward reads and C4's
full sweep evaluates every monthly cell at: Term's `mort_rate` reads PLT duration 68
there. And the sizes hold only the contract they are derived from, so `proj_len()` refuses
a point outside it, naming it, through a Reference for each bound: Term's `issue_age_min`,
`policy_term_min` and `expiry_age`, beside `Data`'s horizon; before `policy_term_min`, a
five-year plan issued at 18 read PLT duration 72 against a cache of 69 (M14).

**F5 — Memory is per ItemSpace, and large.** Each cached cell embeds its arrays in the
compiled space's C struct: about 12 bytes per cell per month. The prototype's struct is
138 KB for eight cells at `N = 1,500`. `BasicTerm_SC` grows the process by 476 MB over
10,000 points at `N = 241`. A ~150-cell uslib model at `N ≈ 1,460` is ~2.6 MB per model
point (Term at `N = 1,046`: 429,896 bytes, the type's basic size), so a block run must
release each ItemSpace once read. `del model.Projection[i]` alone frees nothing: a compiled
or exported ItemSpace sits in reference cycles, its own `_mx_roots` list among them, so
only the cyclic collector frees it. The release is `gc.freeze()` once the model and its
table are read, `del model.Projection[i]` and a full `gc.collect()` after each point, in
the frame pass and in the projections, and `gc.freeze()` again between them (M14, 600
compiled Term points, under load: no unfrozen ItemSpace alive after any release, 71 MB,
1.35 to 1.40 s; without the collection all 600 frame-pass ItemSpaces stay alive and are
frozen for good, 349 MB; with the first freeze after the frame pass, 10.4 to 11.7 s, each
of its collections scanning everything alive).

**F6 — `input_dir()` survives export and compilation.** An exported package defines
`BaseModel.path` as its own directory, compiled or not, so `Data.input_dir()`'s
`_model.path.parent` resolves to the directory that **contains** the package. A
`<Model>_nomx/` or `<Model>_nomx_cy/` package placed beside the CSVs needs no formula
change (verified on the compiled `UL_US_S`).

**F7 — Recursion depth is the runner's problem outside modelx.** modelx raises the
interpreter's recursion limit to 10⁶ (and on Linux the stack limit); the exported package
does neither, and a compiled model recurses on the C stack, which is 1 MB on the main
thread of a Windows host that asks for no more (`python.exe` asks for 2,000,000 bytes,
below). uslib frames run to ~1,460 months, against `BasicTerm`'s 241. No S model has a
frame-long backward recursion, and evaluating in ascending `t` keeps most recursions one
step deep.
**Not all of them:** DIA prices at month 0 on survival read out to the payout date, so in
its export `net_cf(0)` alone needs a call depth of 517, and point 5 raises `RecursionError`
at the default limit even when swept in ascending order (verified). Runners and samples must
set `sys.setrecursionlimit`, and far-ahead reads need a non-recursive form (R2).

*M12:* `DIA_US_SEC` prices on a survival curve of its own, one explicit loop from issue
(`lives_if_pm`); its payout schedule is keyed by policy month, and no pricing cell reads
the projection. Its cold `net_cf(0)` runs 12 or 13 cells deep on the committed points, 21
on the installment refund's twin, and 8 on the point issued later once `Data`'s table is
read (10 before). `DIA_US_S`'s runs 251 on point 1 and 311 on point 13. Its cold
`net_cf(proj_len() - 1)` runs one cell a month back to `t_entry()` plus 7 to 9 (12 in all
on a one-row frame): 726 to 728 on the 720-month twins, and at the longest cover (1,176
months from issue age 22) 1,182 on an installment refund and 1,184 on a cash refund. An
ascending sweep runs at most 16 deep. Each figure counts the count cell a table's join
asks first. In `model.export()`, the cold last month needs a Python recursion limit of
1,482 on the anchor twin, 1,454 on the installment refund's twin, 1,000 on the cash refund
in force 241 months and 2,366 at the longest cover; the ascending sweep needs 52 on the
committed points and 62 on the longest-cover rows (measured at M12's fix, under load). The
module asserts a cold `net_cf(0)` within 32 cells and a cold last month within 16 of its
chain.

A compiled chain runs on the C stack, which the interpreter's recursion limit does not
count. Term's cold call at its contractual maximum, 932 cells deep in modelx on a model just
read, one a month back to `t_entry()` and 9 more, needs 232 to 236 KiB with gcc, about 255
bytes a level; 384 to 448 KiB with a count chain of two cells a month, and 256 to 384 KiB
once a keyword call has turned its chain cell into a Python method. The depth follows the
cover from issue, not the frame. 1 MB is the stack MSVC gives an executable's main thread
unless the executable asks for more, as a host embedding Python may not; `python.exe` asks
for 2,000,000 bytes. The compile tests use a thread whose stack is reserved at 1 MiB as a
stand-in on every platform: `threading.stack_size` cannot reserve on Windows, where it sets
only the stack a thread commits, so the test child creates the thread with
`CreateThread(STACK_SIZE_PARAM_IS_A_RESERVATION)` there, and reads the stack back from
Windows or glibc. The export needs a recursion limit of 1,881 for the cold call and 48 for
the reports. MSVC's bytes per level come from the first Windows run (M14).

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
copying the S model's folder, without `__pycache__`, and changing `_name` in its top-level
`__init__.py`, so its **first commit is the S model with only `_name` changed**: every later
diff in that folder is an enhancement, and nothing else. (Reading the S model and writing it
back under the new name, as first planned, does more: under modelx 0.33.0 it also restamps
`_system.json` from modelx 0.31.1 to 0.33.0 and rewrites the trailing newlines of two
`__init__.py` files. The first write by modelx, in a later commit, brings that restamp,
where it is one line among real changes.) It reads the same assumption CSVs as the S model
— one copy of each table — and adds its own model point table, `model_point_table_sec.csv`.

*Rejected:* modelx space inheritance from the S model (bases must live in the same model);
a separate product directory with copied CSVs (two copies of every table drift apart).

### D2 — Sequence: E before C, Term's C first

A product's Phase 1 (E) lands before its Phase 2 (C) starts. Phase 1 changes semantics and
no representation; Phase 2 changes representation and **no number**. Phase 2 starts on the
other eleven products once Phase 1 is complete and frozen for all twelve (M13). Within each
phase Term goes first, as the template, and the others follow the streams of §5.3. Between
the phases the `_SEC` models carry `stage: "E"` in the registry, and the C-only conventions
switch on at `stage: "EC"`.

Term's C step (M14) is brought forward (changed at M2): it runs beside Phase 1's streams,
not after M13. Its first commit freezes Term's Phase 1 fingerprint, as M13 freezes the
others', and the compiled Term must reproduce it (C2). A finding of M14's that a Phase 1
model must follow goes to the products in progress as it is made, and binds every product
that lands after it. A product that landed before it takes it up in its own C step. M14 is
done on Linux, 2026-11-02; its Windows gate awaits the `cython` job's first run (§7.1,
*Record — M14*). What it found that the Phase 1 products follow is listed there, under
*Carried into Phase 1*.

*Why:* two reviewable diffs per product — "what running in force needs" and "how it is made
C" — and Phase 2 is gated by the Phase 1 suite, unchanged in substance. Phase 1 nonetheless
obeys the compile-neutral rules R1–R3 and R1a (D11), which constrain how in-force logic is
written without changing what it computes, so Phase 2 never has to restructure a recursion.
Those rules were written before any SEC model compiled. Compiling Term while the other
products are written tests them on a real model while a gap still costs a change to the
products in progress, not a restructure of ten finished ones.

*Rejected:* an intermediate `_SE` model per product. It would put 36 models in the library
for a final state of 24; the stage key carries the same information.

### D3 — Time axis: the valuation clock

The SEC models run on two clocks:

- **`t`, the projection clock.** It counts months from the valuation date. `t = 0` is the
  valuation date for every model point, however old the policy is.
- **`duration_mth(t)`, the policy clock.** It counts how many months the policy has been in
  force at time `t`. Everything contractual reads it: premium schedules, surrender charges,
  anniversaries.

The policy clock is plain addition, `duration_mth(t) = duration_mth_init() + t`.
`duration_mth_init()` is read from the model point: the policy's age in months at the
valuation date. It is 26 for a policy issued 26 months before the valuation date, 0 for one
issued at it, and −15 for one to be issued 15 months later (D4). Ten months after the
valuation date, the first of these is 36 months old.

BasicTerm_SE reaches the same numbers by recursion instead. Month 0 comes from the model
point and every later month is "last month plus one", so asking for month 500 first asks for
month 499, then 498, back to 0. The SEC models use the addition, as UL_US_S and VA_US_S
already do: the numbers are identical, without a 500-deep chain of calls. That matters once
the model is compiled. Every such chain runs on the C stack, which is 1 MB on the main
thread of a Windows host that asks for no more (F7), and the models already carry the
chains they cannot avoid, such as the in-force count.

The cells built on the policy clock keep their S formulas unchanged:
- `duration(t) = duration_mth(t) // 12`, the completed policy years;
- `policy_year(t) = duration(t) + 1`;
- `age(t) = age_at_entry() + duration(t)`.

For the 26-month-old policy, issued at age 60, `t = 10` gives 36 months, 3 completed years,
policy year 4 and age 63. Only the base changed, so nothing built on it needs rewriting to
handle a policy already in force.

`result_cf()` has one row per month, from `t = 0`, the valuation month, to `proj_len() - 1`.
`proj_len()` counts the months from the valuation date to the end of cover. A policy with 720
months of cover from issue and 26 months behind it has 694 left, so its frame runs from row
0 to row 693.

Row 0 always means the valuation month, so every point's frame lines up with every other's,
and they sum row by row into a block. This is the change from WholeLife_US_S and FIA_US_S,
whose in-force frames start at row 108 or 84 because their `t` is the policy's own age. A
point not yet issued has zero rows until its issue month.

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

Future new business is written over a stated horizon: `Data` refuses a `duration_mth`
below `-future_horizon_mth`, a Reference of 120 months on Term. So no frame runs longer than
cover from issue plus the horizon, and Phase 2's `t` caches have a contractual size (F4). A
negative horizon is itself refused (precised at M1).

*Fallback:* if future new business proves disproportionate for a product (§8, risk K4),
that product's `Data` rejects `duration_mth < 0` with a clear error and its `model-sec.md`
says so. The rest of the design is unaffected. The horizon set to 0 is that fallback, with
a message of its own (precised at M1).

### D5 — Counts: BasicTerm_SE's entry, uslib's row weight

- Model point columns `policy_count` and `duration_mth`, as in BasicTerm_SE.
- `pols_if_init()` is `policy_count` if the point is in force at `t = 0`, else 0;
  `pols_new_biz(t)` is `policy_count` in the issue month; both as in BasicTerm_SE.
- `pols_if_at(t, "BEF_NB")` is the count carried in from `t - 1` (`pols_if_init()` at
  `t_entry()`, D4), and `pols_if_at(t, "BEF_DECR")` adds new business. `BEF_NB` forms
  month `t - 1`'s `BEF_DECR` count itself, as its own value at `t - 1` plus that month's
  new business, rather than calling for it. That is the same sum in the same order, so the
  results are identical, and the chain of calls back to `t_entry()` is one cell a month,
  no deeper than S's (F7; precised at M1). A test bounds the cold depth on a model just
  read, by modelx's stack trace, at one cell a month back to `t_entry()` and a fixed
  overhead that each product measures and records. The overhead leaves a few levels for
  Phase 2's `Data` cell under each table reader: Term 16 (8 measured at M1, 9 at stage
  EC); UL 20 (16 measured); VUL 25 (20 or 21 measured, since its cold `net_cf` ends in the
  first month's deduction, whose cost of insurance reads the death benefit's corridor,
  down to `corridor_factor_at`, `Data.corridor_age_last` and `Data.corridor_factors`);
  RILA 24 (13 to 21 measured on its committed points, since its month 0 prices its term's
  option under the interim value, and 21 where a renewal under `nge_reset` re-solves the
  cap there; precised at M10). MYGA's 16 leaves none: on a model just read, twin 3's cold
  `net_cf` runs 16 over, down to `Data`'s first read of the age-cap table (§7.10, *Record
  — M7*), so MYGA's C step raises it. The bound holds on the committed points, their
  deepest among them, and at the contract's maximum, since the 1 MiB stack test has a
  fourfold margin under gcc and passes a chain of two cells a month (M14; precised at M4
  and M10). A chain whose first month makes R2's admitted read may run up to 11 more
  again, the read's state chain opening beneath it, as FIA's count does: a cold `pols_if`
  alone runs 25 over its months, 997 levels at the longest cover, where a cold `net_cf`
  runs 7 to 10 over (precised at M8).
- **`pols_if(t)` is `pols_if_at(t, "BEF_DECR")`**, not BasicTerm_SE's `BEF_MAT`. The
  library settled `pols_if(t)` as the count that weights row `t`, and this is the definition
  under which it equals the S model's `pols_if` on every new-business point.
- Each S model's own later timings (`BEF_SURR`, `AFT_DECR`, …) and its maturity rule
  (survivors exit at the end of the last month) are kept. BasicTerm_SE's start-of-period
  `BEF_MAT` maturity is not adopted: the S goldens put expiry at the end of the final
  month. Nor is the **name**: WholeLife already has a `BEF_MAT` that means the end of the
  month after surrenders, the opposite end of the month from BasicTerm_SE's. `BEF_NB` is
  the only timing SEC introduces, plus `BEF_DECR` where an S model lacks it. Where an S
  model names CashValue_SE's three timings in a stub that returns `pols_if` for each, as
  `UL_US_S`, `VUL_US_S`, `ULSG_US_S` and `IUL_US_S` do, SEC keeps the stub's meaning for
  `"BEF_DECR"` and `"BEF_MAT"`, the count after the month's new business, since none of
  the four matures a policy, and gives `"BEF_NB"` D5's meaning. The model then differs
  from the stub in `"BEF_NB"` alone, in the issue month, and T3 compares the cell with the
  stub at every other key, through an `arg_map`, rather than exempting it. Each S model's
  `"BEF_MAT"` thus keeps its own meaning: the end of the month in WholeLife, the count
  that weights the month in the UL family (precised at M3).
- SPIA and DIA are the two exceptions to the row-weight rule. SPIA's count on the books,
  `pols_if_at(t, "BEF_DECR")`, is `policy_count` from the annuity date to the stop rule:
  mortality decrements each life's `lives_if`, never the count, and every flow is that
  count times a per-contract amount weighted by survival, as S weights every flow by its
  constant `pols_if_init`. So `BEF_NB` is a closed form, `pols_if_init()` at `t_entry()`
  and `policy_count` after it, with no chain behind it. `pols_if` keeps its S definition
  on that count, a closing measure (the contracts with an obligation still open at the end
  of the month), so `pols_if(0) != pols_if_init()` even in S (0.99999986 on point 8), and
  the registry marks it `closing_pols_if` so the `pols_if == BEF_DECR` convention skips it
  (precised at M11). `DIA_US_S` weights its flows by a constant `pols_if_init` the same
  way, and `DIA_US_SEC` copies SPIA's count chassis. Its `pols_if` keeps S's definition on
  the count on the books, `pols_if_at(t, "BEF_DECR") * lives_if_last(t)`: the count
  weighted by the probability that a covered life is alive at the start of month `t`, S's
  `pols_if_init * l_last` bit for bit on every twin. That is neither `BEF_DECR` nor SPIA's
  closing measure, so the registry marks it with a key of its own, `survival_pols_if`,
  confined to `DIA_US_SEC` by the registry test (`SURVIVAL_POLS_IF`); the
  `pols_if == BEF_DECR` convention skips it and the module asserts the definition (settled
  at M12).
- `result_cf()` keeps the S columns exactly; the SEC-only quantities go in a new
  `result_pols()`, as BasicTerm_SE does it.

### D6 — The opening state of an in-force point

Each state variable gets one model point column, `<cell>_init`, per policy. It holds the
value at the **start of month 0, before any month-0 event**: the `BEF_NB` instant, which
for an account value is the `BEF_PREM` instant of the CashValue_SE timing vocabulary. The
defining property is operational: it is exactly what the S model carries into month `d`,
and the splice identity of §5.2 tests it.

- A product whose annual quantities read the balance entering the policy year, as
  WholeLife's dividend, term blend and loan interest do, needs that balance at a second
  instant (precised at M2): **the anniversary on or before the valuation date**, the one
  that opened the policy year under way. Its column is `<cell>_prev_anniv_init`, after
  `WholeLife_US_S`'s `div_prev_anniv`, where `prev_anniv` is the anniversary that opened
  the year and `anniv` alone the one that ends it. On a point valued on an anniversary the
  two instants are one, and `Data` checks that the columns agree, unless the year-opening
  value is taken before the anniversary month's transactions, as RILA's free-withdrawal
  base is, where `Data` checks it is at least the opening value, to a cent (precised at
  M10). In the first policy year the year opened at issue, so each such column equals the
  issue value: 0 for WholeLife's additions and loan, the premium for an account value. A
  contract-year-to-date accumulator is measured at the start of month 0 like any balance,
  and where its cell's name does not say that it restarts each year, its column adds
  `_ytd_init`, as VA's do (§7.7). WholeLife's dividend credited at the anniversary, which
  `div_prev_anniv` returns through the year under way, is `div_prev_anniv_init`, a
  `<cell>_init` like the others (§7.2 names it `div_prev_init`).
- A quantity fixed at issue and not re-derivable from static data (a payout amount, a
  locked rate, a solved premium, an index level at term start) is a column too, for the
  reason BasicTerm_SE reads its premium from a table.
- A rate fixed at a past date that is not issue, such as a declared rate or a yield locked
  at the start of the period under way, is a column too, `<cell>_init`, the value in force
  entering month 0. It is read only where the fixing month precedes `t_entry()`; a fixing
  at month 0 itself reads the scenario at the valuation date (precised at M7). In each
  product still to come, a value fixed at a term's or a segment's start takes DIA's
  frozen-weight shape instead, as RILA's do: a column, or a row of IUL's segment ladder
  (§7.4), only where the period began before the valuation month, blank or absent
  otherwise, and checked present exactly where it is read (§7.12, *Record — M12*; precised
  at M10).
- Where S computes an issue value by rule rather than reading it, as MYGA's `av_pp_init()`
  and `mgsv_pp_init()` do, the rule moves into the issue month's credit and the cell
  becomes the in-force accessor, 0 on new business; T1 exempts the cell with that reason.
  An S column that is a value at issue, as MYGA's `tax_basis_initial` is, takes the D6
  name and keeps its issue meaning on new business, so `Data`'s check that a point not yet
  in force has no opening state exempts it (precised at M7).
- The remainder of an annual allowance, which each anniversary resets, is not an
  accumulator and takes no `_ytd`, as MYGA's `free_wd_remain_init` does not; an
  accumulator of use does, as VA's do (precised at M7).
- `Data` validates the in-force columns on read, vectorized, and raises naming the
  offending `point_id`: no negative balances, flags consistent with balances, a phase
  consistent with the account value. A rule of the product rather than of the table,
  such as whether a point is still in cover, needs a `Projection` Reference, so it is
  checked where the frame is defined, in `proj_len()`, which raises naming the point.
  Such a row reads, and a loop over the block meets it only when it reaches it, so
  `run_sec.py --block` asks every point for its frame before it projects any (precised
  at M1).
- No balance a policy holds, such as an account value or a loan, is negative in force, so
  a point the S model carries into a negative one, as `UL_US_S` carries its account value
  in permanent shortfall, is restated no later than the last month it is still zero or
  more. A measure that is not such a balance may take either sign: a tax measure such as
  premiums less withdrawals, or the shadow account, which `ULSG_US_S` never floors (§7.5).
  A quantity every policy in force holds, such as UL's face, is refused at zero (precised
  at M3). A product whose account value is a market valuation the contract lets fall below
  0, as RILA's interim value is [S2], accepts any finite value and refuses instead a
  contract in force that holds no balance, a state `RILA_US_S` reaches only by a full
  withdrawal, which it keeps in force (precised at M10).
- A `Data` rule that ties one amount of money to another, as an allowance to the base it
  is a share of, compares to a cent, so that an extract may carry each amount to the cent:
  each amount so carried is within half a cent of its exact value, so the rule can miss by
  half a cent from each, the base's scaled by the rate, and at half a cent ties fall to
  floating point. An amount held exactly, as a premium paid or a programme's amount, adds
  nothing to a miss. A rule whose carried amounts can miss by a whole cent, as one that
  ties more than two, or adds an exact amount to one of two, allows half a cent from each
  and half a cent more, so that such a miss never falls to floating point: on a valuation
  at a renewal, whose month before closed a term, RILA's opening Account Value is its
  Investment Amount plus its two accounts to two and a half cents, since the four, carried
  to the cent, can miss by two cents, which half-even rounding reaches at exact ties
  (100.125, 200.125 and 300.125 against 600.375), and a miss of one cent reads
  0.010000000009 (precised at M10). Each such rule is tested on an extract with every
  amount carried to the cent, not only with one column moved. Two columns that hold one
  amount at instants that coincide may still be compared exactly, as WholeLife's are on an
  anniversary. `Data` holds a carried allowance to what makes it, as MYGA's does: the
  issue allowance in the first contract year; on an anniversary under `pct_av`, the rate
  times the account value; and under `interest_only`, at most the interest to the
  anniversary that opened the year, exactly that in the second year. A balance S lets fall
  below 0, as MYGA's floor and `P_accum`, is checked only as a finite number (precised at
  M7).
- A contract in force whose benefits all rest on its account value has an account value
  above 0, and `Data` refuses 0, naming the point, as MYGA's does (precised at M7). A
  product whose rider pays on after the account value is exhausted, as FIA's and VA's
  lifetime withdrawals do, accepts 0 and guards its ratios instead; and one whose account
  value can fall below 0 under the contract, as RILA's can, accepts any finite value and
  refuses instead a contract in force that holds nothing (above; precised at M10).
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
input. Improvement dated by the calendar from the contract's own start, as SPIA's is
through `annuity_year + duration(t)`, is not: it reads the calendar years the contract
reaches, whatever the valuation date, so it stays on the policy clock, and the splice does
not neutralize it (precised at M11).

A point-to-point quantity measured on a market path whose term began before `t = 0` needs
the path's value at term start. That value is an opening-state column under D6.

Where an S model carries a market's change since a term's start as one level Reference
rather than a path, as SPIA's `cmt10_shift` and DIA's `ref_rate_shift` do, the column is
the change seen by the valuation date, `<reference>_init`, and the Reference is the change
made at the valuation date, on the one path every point shares. A term that starts after
`t = 0` measures the change from its own start on that path, so it has seen none of a
change made at the valuation date: `SPIA_US_SEC` discounts a commutation at
`j0 + cmt10_shift_init() + cmt10_shift` on a contract on the books at the valuation date
and at `j0` on one commencing later. One Reference cannot stand for each contract's change
since its own start, since contracts that started at different dates have seen different
changes. A path, were it an input, would be read on the valuation clock, each contract
taking the change on it from the later of its term's start and the valuation date
(precised at M11).

### D8 — Files per product

Beside the S files: `<Name>_US_SEC/` (formulas only, `Data` and `Projection`),
`model_point_table_sec.csv`, `run_sec.py` and `model-sec.md`; at Phase 2, `sample_sec.py`
and `spec_sec.py`, mx2cy's two inputs. The SEC table holds:

1. **every S row**, with the same `policy_id` and `point_id` — the twins of §5.2. An S row that is in force
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

This matters because S rows do change after the fact. MYGA points 5 and 6, RILA points 4,
5, 7, 9 and 12 and VA point 6 have had their `provenance` reworded under `CLAUDE.md`'s
rule, RILA's 4, 5, 7 and 12 at M10's landing, and FIA point 3's roll-up key has been
renamed. A hand-copied twin of FIA point 3 would now raise `KeyError` against the shared
roll-up table, and no projected number would ever reveal the eight stale `provenance`
cells.

Some SEC rows need inputs S never had:
- a scenario re-based to each row's valuation date by its `duration_mth` (FIA, VA, RILA);
- an in-force ladder (IUL);
- premium schedule rows (DIA), whose shared `premium_schedule.csv` is keyed by `point_id` and
  knows no derived or future point (§7.12).

These go in SEC-only companion files (`*_sec.csv`), never into the shared S inputs. Where
they derive from S data they are generated the same way, under the same test. A companion
is read by a reader of its own, a `Data` cell naming its `*_file` Reference, which stays
Python as S's readers do; C3 exempts readers from its `Data` rule (M14).

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
costs nothing. The layout belongs to the tool, which writes all six libraries' page trees, so
every library's model pages move with uslib's. Nothing links to them by path; `conf.py`,
`MERGE.md` and the tool's own docstring describe the layout, and change with it. `index.md` gains the SEC family in its models table and its convention table.

### D10 — Registry and conventions

`us_registry.MODELS` gains twelve SEC entries whose metadata adds `"twin"` (the S name),
`"param"` (`"point_id"`, then `"idx"`) and `"stage"` (`"E"`, then `"EC"`), and
`INPUT_FILES` gains their file sets. SPIA's entry also carries D5's `"closing_pols_if"`,
and DIA's its `"survival_pols_if"`, each confined to its one model by the registry test.
`test_model_conventions.py` is generalized rather than forked:

- the suffix is `_S`, or `_SEC` for a model registered with a `"twin"`, at either stage:
  the name is the family's from the first commit and never moves with the stage (D2);
- the parameter is the one the metadata names;
- model points are enumerated through one helper that yields labels or positions;
- "every CSV beside the model is read" becomes "by some model in the directory";
- "a runner and a `model.md`" becomes "and, for SEC, a `run_sec.py` and a `model-sec.md`";
- `model_point()` stays in the shared vocabulary, as a reporting accessor
  (`data.model_point_table().iloc[idx]` after Phase 2). C5 forbids projection cells from
  calling it.

New conventions for the SEC family:
- the frame starts at `t = 0`;
- `pols_if(t)` equals `pols_if_at(t, "BEF_DECR")`, except on SPIA and DIA (D5);
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
  backward recursion over the frame (F7). A formula that needs a value far ahead of its
  own `t` takes it from a non-recursive form — an explicit loop in one cell, or a vector
  built in `Data` — as DIA's month-0 pricing does, since it reads survival out to the
  payout date: `DIA_US_SEC`'s survival from issue is one loop in `lives_if_pm(k, life)`
  (M12).

  A recursion over a deterministic schedule on the policy clock may keep its key and be
  based at the valuation date's key instead of at issue, one loop there summing what
  precedes it in S's order, as SPIA's payments to date, `cum_annuity_pp(k)`, and its
  income by policy year, `annual_income(y)`, are. SPIA's test asserts the payments to date
  equal S's at every key, bit for bit, and a contract valued late in its term recurses
  forward from the valuation date only: a cash refund in payment 600 months computes its
  whole `result_cf()` 9 cells deep, where S's cold `G(600)` runs 606 (precised at M11). A
  deterministic schedule whose state is a vector of balances coupled within the month, as
  VUL's pricing path, keeps its key from issue, one cell a month: a loop at the valuation
  date's key would return the vector of balances from one cell, which no Phase 1 cell may
  (§7.1, *Record — M14*). Its cold depth is then its cover from issue, and the depth test
  bounds it so. While such a path is read, an ascending sweep of a point in force at
  policy month `d` also runs about `d` cells deep, because its first month reads the path
  cold. VUL's runs about `d + 15` under modelx, 135 on twin 4 and 1,477 on a point in
  force in its last covered month, 1,463, at issue age 0, against 14 there with the path
  unread and 18 on every committed point. So `sample_sec.py`'s and `run_sec.py --cython`'s
  recursion limits are sized from the cover from issue. In VUL's modelx export, measured
  at M4's review and again on the fixed model at its re-review, the committed points'
  reports and checks need 1,821 and a point in force in its last covered month at issue
  age 0 needs 2,981, against 61 and 44 with the path unread. The depth test sweeps the
  in-force twins ascending under `d` plus the overhead, and the points not yet in force
  under the module-off limit, `CALL_DEPTH` (precised at M4).

  A check whose S form sums a period's flows ahead of its own month is measured at the
  month the period ends, reading back. `DIA_US_SEC`'s commutation residual equals S's at
  the exercise, bit for bit, on every row valued at or before the exercise, and is 0.0 in
  every month on a row valued later, the exchange having closed before `t_entry()`, where
  look-back stops (R1); its module asserts both. A schedule recursion's base key reads no
  clock: `DIA_US_SEC`'s `G`, a closing balance, is based at
  `max(duration_mth_init(), 0) - 1`, not `duration_mth(t_entry()) - 1`. SPIA's two cells
  above, built before this, still base on clock reads at `t_entry()`, which no month-keyed
  cell reaches before `t_entry()`: each that reaches them is `is_active(t)`, which reads
  `stop_mth()` only from `t_entry()` on, or a cell it guards. SPIA's C step moves them
  onto static keys (§7.9, *Record — M11*). The rules test follows precedents keyed by no
  month to the month-keyed calls they read (precised at M12).

  One read further ahead is allowed (precised at M2): a cell may read a per-policy
  quantity at `anniv_mth(t)`, the anniversary that closes the policy year of `t`, so at
  most 11 months ahead, where that quantity depends on no count, on nothing after the
  anniversary, and not on what the reading cell holds in that policy year; what it held in
  earlier years may reach the quantity. Such a read opens no chain past the anniversary.
  Called cold, the depth it adds is bounded by the policy year. In an ascending sweep the
  admitted read can first open a cold chain of the state it reads, back to `t_entry()`,
  still one cell a month, so the sweep's depth is that chain's (precised at M8: FIA's
  sweep reaches 371 on point 9, where the account value runs out and the floor's chain is
  first read, against S's 370; exported, the same sweep needs a recursion limit of 747,
  against Term's 51 and WholeLife's 128). Each product's rules test admits it by its
  reader and the cell it reads, at `anniv_mth(t)` and nowhere else, and checks that the
  month read is inside the frame, so `spec_sec.py` sizes no cache beyond the frame for it.
  WholeLife's term-blend layer reads the year's dividend so (`oyt_face` reads
  `div_credited`, §7.2), and FIA's `lapse_rate` and `lapse_moneyness_factor` the state
  closing the contract year (§7.11). Under `pua_div_on = True`, the layers of WholeLife's
  earlier years reach that dividend through the paid-up additions entering the year, which
  their cost reduced.
- **R3** Phase 1 adds no new Python-object machinery: no new string-valued cells, no new
  Series or tuple returns, no new per-`t` pandas lookup in `Projection`. A model-point
  accessor cell, one `int(...)` or `float(...)` of one `model_point()` subscript, is S's
  own pattern and is allowed for each new in-force column; R11 rewrites it in Phase 2 with
  the rest (precised at M1).
- **R4** `Projection` is parameterized by `idx`, and `point_id()` returns the label for
  reporting. A runner takes `Projection`'s key from the model, the position where it takes
  `idx` and the label where it takes `point_id`; and a test projects a table whose labels
  are not its positions plus one, asserting `point_id()`, a refusal naming a label, and the
  runner's output (M14).
- **R5** `Data` keeps the S CSV readers unchanged (read once, `object`-typed) and adds one
  array cell per input the projection uses: int64 for ages, durations, codes, flags and
  counts of buckets; float64 for policy counts, which Phase 1 admits fractional, amounts
  and rates. Never bool, object or string dtypes.
- **R6** Decode in `Data`, to the number the formula needs. A categorical string becomes
  the quantity it selects — `premium_mode` becomes `prem_cycle` and `modal_factor`,
  `rate_class` becomes the class factor, `plan` becomes `policy_term`. Where a code must
  survive, it is an int code with named int References in `Projection`. A decoding reads
  the text as the S model does, element by element, accepting what S accepts: Term's plan
  is `int(plan[1:])` on each point, its band S's own boundaries. A numeric key is read by
  its value, as S's `.loc` matches 1 against 1.0, in every cell that reads it, a table's
  extents among them, so a key column pandas reads as floats, once one cell is written 1.0
  or blank, decodes as it does written in ints, and a key that is not whole, text among
  them, is refused by name, through a projection as at the first read (M14).
- **R7** Tables become integer-indexed arrays. Age-keyed tables are padded from age 0, as
  `mort_table_array` is. A string-keyed table many points share becomes an array by
  schedule and key, `[schedule, policy_year]`, with each point's schedule number an int64
  vector and each schedule's first and last key int vectors; a genuinely per-point table
  stays `[idx, policy_year]`. Scenarios become `[scenario, t]` arrays, with a per-point
  scenario index. Padding holds NaN and is never read: each padded table has one reader in
  `Projection`, which checks its key against both ends of the table's extent and raises
  naming the point and the key where S's `.loc` raised `KeyError`. Phase 2 refuses at the
  first read a table with a gap, a repeat, a key that is not whole or a blank, naming it,
  where S raised or returned NaN only when a projection reached it, and one `Data` cell
  holds each table's check, from which its array and its extents are sized, so that a
  projection, which reads an extent first, meets the same refusal (Term's
  `premium_schedules`; precised at M14). Each array, and each point's index into it, is
  built from keys `Data` has checked, and a point whose key its table lacks is refused, by
  point, rather than read as padding (precised at M7). MYGA's mortality, padded from age
  0, holds padding below the table's first age, where `Data` refuses a point's attained
  age in its first month on the books, and ends at the table's last age, 120 as shipped,
  which a point can pass before maturity on a shorter table: the maturity age is a
  `Projection` Reference that `Data` cannot read, so Phase 2 checks that bound in
  `proj_len()` against an int `Data` cell of the table's last age by sex (§7.10,
  *Record — M7*), where Phase 1 leaves S's `KeyError`. A scenario step-filled into
  `[scenario, month]` keeps the months before its first level unreadable: T3's re-based
  scenarios have none before issue, and a read there must fail.
- **R8** A blank override becomes a value array plus a 0/1 flag array; no `pd.isna` or NaN
  test runs in `Projection`.
- **R9** String parameters become named int References: `pols_if_at(t, BEF_DECR)` with
  `BEF_DECR = 1`, `claims(t, DEATH)`. The names stay those of the strings, so call sites
  read the same minus the quotes. A code that indexes a cache is dense from 0: timings by
  instant, `BEF_NB = 0` and `BEF_DECR = 1` in every product, then the product's own in
  processing order; phases and kinds in their natural order. Every other constant
  Reference is named in lower case, since `sec_support.codes` reads an all-capital int
  Reference as a code, and T1 maps S's strings onto the codes through it (precised at M14).
- **R10** No projection cell returns a str, tuple, list, dict, Series or `None`. Status
  strings such as a phase become int codes, and the labels appear only in reporting cells.
- **R11** Scalars entering `Projection` are converted once, in accessor cells (`int(...)`,
  `float(...)`), and a boolean cell returns a Python bool, a comparison of Python numbers,
  or `bool(...)` of anything else, a numpy scalar or an element read from a `Data` array
  among them, so tracing sees Python types (F3).
- **R12** Aggregations are explicit loops with plain accumulators. No generator
  expressions, `float` annotations or `math.isclose` in per-`t` cells, and no
  keyword-argument call to a cell anywhere in the model, reporting cells included, nor a
  cell named like any function or method a keyword call names anywhere in the model,
  pandas' and numpy's included: mx2cy demotes every cell whose name a keyword call uses.
  An explicit loop's counter and accumulators compile to C under the build's
  `infer_types=True`. A `kind=None` "total" default becomes an explicit total cell. Seven
  models' `claims(t, kind=None)` traces `kind` as both `str` and `None`, so it compiles with
  an `object` parameter and a dict cache on `net_cf`'s hot path, and its generator sums at
  Python speed. T1 reaches an explicit total through the spec's `twin_arg_map`, S's `None`
  passed as the total's code, or exempts S's cell with its reason (M14).
- **R13** `Data` arrays are read only by element subscript (F3): no `len()`, slicing,
  iteration or numpy calls in `Projection`. A size it needs is its own int cell. The rule
  holds in `Data` too: a vector derived from another reads the DataFrame column, or the
  other cell element by element; a width comes from a table, or a count cell, never from
  another cell's array (precised at M14).
- **R14** Cells with float parameters are engine functions, and under modelx-cython 0.1.0
  none stays a cell of its own in the projection. Cached, a float-keyed cell compiles with
  a Python dict for a cache: IUL's `index_credit_rate(..., cap=None)` and ULSG's
  `sg_pp_solve(t, prem)` build 900 to 18,300 entries. Uncached (`is_cached = False`), it
  compiles as `cpdef object f(object ...)`, whatever the spec says, because mx2cy traces
  only `_f_` formulas and an uncached cell has none (F3, M14). C3 rejects both, and C5
  refuses an uncached cell before any compile. So each is inlined into the cached,
  int-keyed cell that calls it, or its float argument becomes an int code or an index into
  a `Data` vector (a segment's slot, a scenario's month, a table's row), so that it is a
  cached cell with a C-array cache. `None` sentinels become float sentinels or int codes.
  Where S's tests or T1 call the engine function itself, as IUL's worked example prices
  `index_credit_rate` at a 10.00% and a 2.00% cap, SEC either keeps S's cell for them,
  called by no projection cell and admitted by name to C3 and C5 through a registry key
  the first product to need it adds, or drops it, T1 exempting it with its reason and the
  tests calling the inlined form.
- **R15** A banded two-parameter cell is re-keyed to the band. IUL's six `(t, m)` segment
  cells are live only for `m <= t <= m + 11`, yet would compile to 912 × 912 arrays,
  ~50 MB per ItemSpace. Keyed by slot `k = t - m` in `0..11`, the cache is 912 × 12 —
  the same shape as the in-force ladder of D6. T1 re-keys S's `(t, m)` to `(t, t - m)`
  through the spec's `twin_arg_map` (M14).
- **R16** Python rounding is precomputed in `Data` with the built-in `round`, element by
  element, never `numpy.round`, whose half-way rule differs. ULSG rounds its COI scales
  with `round(r, dp)`. A projection formula calls no Python builtin but `int`, `float`,
  `bool`, `abs`, `min`, `max` and `range`, which Cython turns into C, and no module,
  `math` included, whose calls Cython leaves to Python; C5 and C3 hold that (M14).
  Rounding a projected amount, as WholeLife's dividend does, stays `builtins.round`, the
  one Python call R16 keeps, with an int sentinel for its digits; the product that needs
  it admits the cell by name in C3 and C5 at its own Phase 2, as RILA may admit its
  Black–Scholes math.
- **R17** Reporting cells may stay Python: `model_point()`, every `result_*` and `check_*`
  (not the per-`t` `*_resid` cells a check reads, which compile), and the label accessors
  a product declares in its registry entry's `"reporting"`, each returning its point's
  column of the same name on every point, which C5 checks. No other cell calls a reporting
  cell. They are the typing guard's allowlist (§6.2), and C5 lets them run Python: a
  `check_*` may keep S's generators as a verification cell; cached, it compiles all the
  same, its closure running as Python inside its `_f_` formula, and uncached it would
  compile untyped (F3, R14).

### D12 — Compiled artifacts are built, never committed

`tools/build_sec_cy.py <product> [--out DIR]` exports the SEC model to
`<out>/<Model>_nomx/`, copies the CSVs to `<out>` when it is not the product directory, and
runs mx2cy with the product's `sample_sec.py` and `spec_sec.py`, writing `setup.py` to
`<out>`. The default `<out>` is the product directory, which `.gitignore` already covers
for `*_nomx/` and `*_nomx_cy/`; add `build/`, `setup.py` beside a model, and `*.so`. Tests
build into a temporary directory, which keeps the tree clean, exactly as
`test_round_trip_is_stable` already copies CSVs. modelx-cython goes in a new
`requirements-cython.txt`, because it needs a C compiler; `requirements.txt` is unchanged.

As built (§4, *Record*), the tool refuses an `<out>` inside the repository, other than the
product directory itself, and any `<out>` that holds a modelx model: copying the CSVs there
once overwrote another product's tracked inputs. It exports and compiles in child processes,
and clears its previous outputs before a rebuild.

### D13 — CI

The existing matrix runs every pure-modelx suite, S and SEC alike. A new `cython` job —
ubuntu-latest and windows-latest, one Python each — installs `requirements-cython.txt` and
runs `pytest -m cython`. The compile tests **skip** when modelx-cython or a compiler is
absent, so lifelib's own bare `pytest` stays green after the merge. In the `cython` job
itself, which installs both, a skip is a failure (`USLIB_REQUIRE_CYTHON=1`), and so is a run
that selects no test. As built at M14, `conftest.py` turns any skip of a `cython` test into
a failure under `USLIB_REQUIRE_CYTHON=1`, an empty parameter set included, which
`require_cython` in a test body cannot see.

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

### Record — M0, done 2026-11-01

Built as specified, in one commit. Each component was written by one agent and reviewed by a
second, which re-ran its checks and tried to break it. The reviews found 22 defects, 13 in
behaviour and 9 in wording, and all were fixed before the commit.

**What exists now.**
- `us_registry.py`: the SEC keys (D10, and D5's `closing_pols_if`), plus `meta`, `is_sec`,
  `point_keys` and `projection`. No SEC model is registered yet.
- `test_model_conventions.py`: generalized as D10 says, with every S model passing unchanged
  (289 passed before and after). Its SEC section, conventions (a)–(h) with T1 among them, is
  parametrized over the registered SEC models, so it stays inert until M1. It was exercised
  on a stand-in library, Term_US_S beside a crude Term_US_SEC at stage E and at stage EC,
  where each of six injected faults failed the test meant to catch it.
- `tests/sec_support.py`, with its own suite `test_sec_support.py` (35 tests, about 16 s, on
  Term_US_S and synthetic models): `sweep` and `twin_mismatches` (T1); `temp_inputs`,
  `shift_months` and `frame_mismatches` (T2, T3); `SecSpec`, `SEC_SPECS`, `build_sec_table`,
  `write_generated` and `check_generated` (T6). Each S model compared with a second read of
  itself, on every point of all twelve, gives 0 mismatches over 5.4 million cached values.
- `tools/gen_sec_points.py <SEC model> [--check]`, a command line over the T6 functions.
  Those live in the tests because `lifelib.create()` copies `tests/` but not `tools/`, and
  T6 must run in such a copy too.
- `tools/gen_scaffolding.py`: several models per product, taken in name order, and
  per-model page folders in all six libraries. 171 pages moved byte for byte, and 57 landing
  pages changed by their one toctree line. doccheck reports 473 pages and 0 warnings, as
  before, and all 65,255 internal anchors still resolve.
- `tools/build_sec_cy.py`, `requirements-cython.txt` (modelx-cython 0.1.0), the ignore
  rules, and the `cython` CI job. `test_cython_toolchain.py` gives the job a test from the
  start: it compiles Term_US_S and checks it against modelx on both points (largest
  difference 0.0), in about 31 s on Linux with gcc. It also checks that the spec's cache
  sizes reached the generated `.pxd`, since mx2cy ignores a misspelled spec key without a
  word.

**Departures and precisions.**
- The `cython` job is stricter than item 6 allows: it fails on a skip and on a run that
  selects nothing (D13).
- D1's derivation is a folder copy and an edit of `_name`, not a read and write (D1).
- The suffix rule is the family's: `_SEC` at either stage (D10).
- `build_sec_cy.py` refuses an `<out>` where copying the CSVs could overwrite inputs (D12).
- T6 reads a float cell by its value, to 1e-12 (§5.2). The generator writes each float as
  text that the models' own parser reads back exactly, wherever such text exists. For some
  computed doubles none does: about one count in six between 0.9 and 1, under pandas 3.0.5.
  Those come back within two ulps. The chosen text also depends on the platform's parser and
  libm, so a byte comparison would fail, on macOS, a file written on Linux.
- `source_mth` and `t_offset` run one way throughout: SEC month `t` is S month
  `t + source_mth`, and `twin_mismatches` and `frame_mismatches` both take the row's
  `source_mth` as `t_offset`. A twin's `source_mth` is the first row of its S frame, which
  is 108 for WholeLife point 1. A derived row's `duration_mth` is its twin's plus
  `d - source_mth`. A future row's `duration_mth` and `source_mth` are both `-k`.
- `SecSpec.twin_state` fills the opening-state columns S lacks on twin rows, such as UL's
  `cum_prem_init`, and may replace one S has, as FIA's gives its in-force twins their
  re-based scenario ids (precised at M8). A spec may not write `provenance`, or any column
  the generator owns.
- `SecSpec.future_state` (added at M8, appended after `twin_arg_map`) sets columns of the
  future rows from S's point and `k`, FIA's re-based scenario id among them; it may not
  set `policy_count` or the generator's columns, and a column it names that S lacks, and
  that neither `state` nor `twin_state` sets, is blank on the twins and the derived rows.
- `frame_mismatches` also fails frames that end apart. Both run to the end of cover, so a
  differing end means `proj_len()` is wrong.
- T1 removes its own reads from the read-once log. Under pytest older than 9.2 the SEC
  section runs before its model's generic tests, and T1, which evaluates beyond the base
  sweep, would otherwise change what the read-once test sees.

**Measured for K6.** T1 costs one more sweep of the paired S points plus the comparison,
measured S against S. Term: 0.6–0.8 s of sweep and 0.17 s comparing 40,361 cached values.
WholeLife: 7–8 s and 3.1 s over 524,780 values. UL: 4.3–7.5 s and 1.2 s over 217,341. So T1
about doubles the sweep of the points it pairs. The splice sweeps of T2 are the larger
unknown; they are measured on Term at M1. The uslib suite went from 1,025 passed and
11 skipped in 4 min 26 s to 1,061 passed and 19 skipped in 4 min 53 s. The new passes are
the 35 harness tests and the compile test, which accounts for 32 s of the difference. The
new skips are the eight SEC conventions, each skipped for want of a model.

**Carried into Phase 1.**
- `CHECK_EXEMPTIONS` and `EXTRA_POINT_ASSERTIONS` are keyed by model name, so an SEC model
  inherits neither of them:
  - IUL_US_SEC's twin of point 5 needs its own `check_margin` exemption.
  - The DIA, FIA, SPIA and VA product facts need SEC entries. SPIA's has one,
    `EXTRA_POINT_ASSERTIONS["SPIA_US_SEC"]` (M11), DIA's one,
    `EXTRA_POINT_ASSERTIONS["DIA_US_SEC"]` (M12), and FIA's one,
    `EXTRA_POINT_ASSERTIONS["FIA_US_SEC"]`, S's four phases in cover and `PRE_ISSUE`
    before `t_entry()` (M8).
  - DIA's check reads `income_start_mth()`, a policy month (R1a), so it needs an SEC form.
    `DIA_US_SEC`'s reads the income at `max(T - duration_mth_init(), t_entry())` on the
    valuation clock, positive and the payout schedule's (M12).
- `gen_scaffolding.py` refuses a library in which an SEC folder lacks a `model-sec.md`, so
  regenerate the pages once that file exists. Its H1 becomes the landing page's link text.
- The first `gen_input_files.py --write` rewraps the ULSG and WholeLife entries, a cosmetic
  change.
- T6 projects every S point unless it is handed the S model T1 has already swept, through
  `s_model=`.
- At stage EC:
  - T1 needs an `arg_map` (R9).
  - The skip-or-fail logic of `USLIB_REQUIRE_CYTHON` moves into `sec_support.py`, for the
    per-product compile tests.
  - Term's `spec_sec.py` sizes the `plt_mort_factor` cache from the contract, not from
    the sample.

  *Discharged at M14:* T1 maps S's strings through `sec_support.codes` and any other
  argument through the spec's `twin_arg_map`; the skip-or-fail logic is
  `sec_support.require_cython()` and the conftest hook; Term's spec sizes
  `plt_mort_factor` at 69, from the 68 `mort_rate` reads in the month after the longest
  frame of the shortest plan, which `proj_len` holds every point to.
- The `cython` job has not yet run on GitHub. It runs on a pull request to `main` or on a
  manual dispatch, and its first Windows run is the outstanding check on MSVC and the 1 MB
  stack.

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
6. Rates: an annual mortality rate `q` built as a product of factors (base × class ×
   improvement or PLT factor) is capped at 1, written `min(q, 1.0)`: the product first,
   the float bound second, as each S model whose mortality is such a product writes it
   since §8.2 item 4's fix. Python's `min` and the compiled cell alike keep their first
   argument unless a later one compares smaller, and no comparison with NaN holds, so
   `min(1.0, q)` is 1.0 where `q` is NaN, in both engines: a blank input read as certain
   death, every flow finite. `min(q, 1.0)` is NaN there, and wherever `q` is any other
   float it is the float `min(1.0, q)` is, 1.0 included, so the order changes no number.
   A `min` or a `max` that bounds a value that is always a float may be written the same
   way, the value first, as Term's M(1) rule and PLT floor are. Where the value can be an
   int equal to the bound, or −0.0 against a bound of 0.0, the value-first form returns
   the value, of another kind or sign than the bound, so there the order stays as S has
   it, and `Data`'s refusals, below, keep a NaN from it (precised at Term's cap fix). A
   lapse rate's bound, at 1 or below it, is such a `min` or `max` and not the cap, which
   is mortality's: §8.2 item 4's fix left the S models' lapse bounds in S's order,
   `VA_US_S`'s `min(1.0, ...)` and `IUL_US_S`'s `min(lapse_rate_cap, rate)`, both at 1,
   among them, and `UL_US_SEC` and `MYGA_US_SEC` keep S's (precised at that fix). The
   cap is on the annual rate, and it is the float `1.0`. A cap on the monthly rate's
   result instead would compile to NaN, or with its bound first to 1.0, where modelx
   raises on the complex rate. Where the S model does not cap, as `Term_US_S` and
   `UL_US_S` did not before §8.2 item 4's fix, SEC caps as a recorded departure from S.
   That changes no value S computes as a real number but the annual rate itself: past 1,
   S's monthly rate `1 - (1 - q)^(1/12)` is complex in modelx, and so is every count and
   cash flow that reads it, while an SEC model's uncapped monthly rate is NaN compiled,
   silently. At 1 the monthly rate is exactly 1.0 in both engines, so every policy in
   force at the start of the month dies in it, and the count is 0.0 from the next.

   So that no blank is lost in a `min` or a `max`, and no infinity is read by a cap as 1,
   which it is in either order, `Data` refuses, by name, a blank, text or infinite value,
   not only a key, wherever a capped rate, or a `min` or a `max` in a projection cell,
   reads it as a number, through a product or a ratio included. A column such a cell
   reads only as a key is decoded as S decodes it: Term bands a blank face as S does, and
   refuses by name a blank, text or infinite issue age, from which the mortality table is
   read, where S's `int` raises. `Data` refuses a value when its array is first read, over
   the whole column, a value no point reads included, naming the file, the column and
   every line or point at fault, in the style of its other refusals: Term's
   `mort_table.csv: mort_rate must be a finite number; it is not at age [50]`. A value
   legitimately absent is said so and left: padding, which no formula reads, and an
   optional column whose blank has a meaning, as a blank M(1) override is the notes' rule
   (R8). Each refusal is a table-driven case on its own inputs, a blank, a text and an
   infinite value among them, a value no point reads and two lines at fault in one column
   too, refused by that rule alone and through a projection, and the same cases run
   compiled in the refusal test (§6.2).

   A point where the cap binds is compared with S as new business and restated in force
   the month before the cap, in the splice grid or in a case of its own, as Term's is: in
   every cell, the capped months included, where S caps, and otherwise wherever S's value
   is real, the capped rate excepted. Its test asserts the capped rate's type as well as
   its value, since `1 == 1.0`, in each model that caps, and asserts the capped rate on
   the rows in force too: where S does not cap, a cap applied to new business only passes
   both comparisons, which leave out that rate and S's complex values. A test sends the
   cap, and each `min` or `max` written with its bound second, a NaN, and asserts the
   float NaN, not the bound. It sends it either by setting a Reference that feeds the cap,
   on a model read for the test, before the model computes anything, as `DIA_US_SEC`'s cap
   and residual tests set `mort_ae_factor`, or by replacing in such a model the formula of
   the cell that feeds it. The first is the form that runs compiled unchanged, since a
   compiled ItemSpace takes the References when it is made; the second needs modelx (K7;
   precised at M12). Decided at M14's landing, when Term's SEC model capped; the cap's
   order and the `Data` rule decided at Term's cap fix (§7.1); and the cap made in the S
   models at §8.2 item 4's fix, 2026-11-03, when `WholeLife_US_SEC` took
   `WholeLife_US_S`'s and `SPIA_US_SEC` reordered its two caps with `SPIA_US_S`'s. At M12,
   `DIA_US_SEC` caps as `DIA_US_S` does since that fix, the bound second, and checks its
   four assumption tables in count cells beside S's unchanged readers (§7.1, *Precised at
   M3*, item 9), and its `survivor_pct`, `cola_rate`, `commute_frac` and
   `other_qlac_premium` in `Data`.

   A value whose range is the quantity's own is refused outside it, in the rule that
   refuses the column's blanks, with one message: a probability, or a share of an amount,
   as a premium load or an allocation, outside 0 to 1, and, below 0, a quantity that
   cannot be negative: a multiple of a decrement, a charge, a fee ratio or a fraction of
   the premium paid. Below 0 a probability or such a quantity would otherwise project,
   every check passing, a count, a premium or a charge no policy can have. Past 1, VUL's
   lapse rate makes every count after it complex in modelx, which only the checks catch,
   by raising, and its mortality, capped at 1, can read a rate past 1 as certain death,
   every check passing. A share past 1 can pass every check too: at a load of 1.5, VUL's
   point 3 would credit its account −250.00 of a 500.00 premium in month 0, and
   `IUL_US_S`'s point 1, at an `index_alloc_rate` of 1.5, sweeps 14,075.46 out of a fixed
   account of 9,383.64, where an allocation of VUL's past 1 would fail its three checks on
   points 3 and 4, since the allocations then sum past 1. VUL's `lapse_rate_ann` and
   `mort_rate` "must be a number from 0 to 1", and its `factor`, `coi_rate_guar`,
   `fund_expense_ann`, `prem_persistency` and `sc_per_1000_init` "must be a number, zero
   or more", and its `load_prem_rate`, `alloc_<i>` and `alloc_fixed` "must be a number
   from 0 to 1". Its returns and corridor factors need only be numbers: a return may be
   negative, and a corridor factor below 1, or below 0, only makes the corridor bind
   later, or never. The range's bounds are read, and a test reads each one. A charge per
   $1,000, as a COI rate, is no decrement and has no upper bound: VUL's current scale
   passes 1 from attained age 72 (precised at M4).
7. Inputs: assign each input to its clock (D7).
8. Reporting: `result_cf()` with the S columns; `result_pols()`.
9. Docstrings: rewrite the time-axis prose — every "t = 0 is the issue month" — add the
   new cells to the symbol map, and keep the house disclaimers the conventions assert.
10. `model-sec.md`, `run_sec.py` and the SEC input files: `model_point_table_sec.csv` and
    any `*_sec.csv` companion (D8). Before each commit that adds or changes one, search it
    case-insensitively for every publisher and product the product's `sources.md` cites,
    as `CLAUDE.md` requires. T6 keeps the files in step with S, but it does not look for
    names.

M1 settled how each step is written, and the later products copy it: §7.1's *Record* lists
the template item by item.

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

  Two precisions (M1). The comparison covers every cell of the S model, and an S cell the
  SEC model lacks fails unless its spec exempts it with a reason, so a renamed cell cannot
  take its goldens out unseen. And it covers S's own frame only. A formula that reads ahead
  of its frame, as Term's `jump_ratio()` does when cover ends with the level period, gets
  an answer from S's tables as though cover went on, where an SEC model answers that the
  month is outside cover (R1). The two frames' ends are held together by
  `frame_mismatches`.

  At stage EC (M14), `sec_support.codes` maps S's strings onto SEC's int References in S's
  arguments and values, and the spec's `twin_arg_map` maps first any argument SEC takes
  otherwise, a total's code for S's `None` or a slot for S's month (R12, R15).
- **T2 — Splice identity.** The test that says the opening state is complete. For S
  new-business points, at months `d` chosen to straddle each product's events (§7), an SEC
  point opened with the S state at `d` reproduces S from `d` on, for every result column
  and every state cell, to 1e-9 relative. Where a compared value can fall far below 1, as
  survival does where a cap on mortality binds, the comparison takes no absolute floor: a
  floor of 1e-9 hides a 1% error in any value below 1e-7. A cell whose exact value is 0
  and whose computed value is rounding around it keeps the 1e-9 floor: the roll-forward
  residuals, the `check_*_resid` cells, move by an ulp of what they close when an opening
  state comes back from the CSV one ulp off, and with no floor on them
  `WholeLife_US_SEC`'s splice fails 13 of its 105 rows there and nowhere else (precised at
  M11). Valuation-clock inputs are shifted by `d` in the temporary input directory, and
  `inflation_rate` is set to 0 in both models (D7), as is mortality improvement where it
  runs from the projection start; improvement dated by the calendar on the policy clock,
  as SPIA's is, is not neutralized (precised at M11). A missing state variable fails here
  and nowhere else. Every assumption that ships at zero is switched on, in both models
  alike but for a market's change since a term's start (below), so the splice can see it.
  Where the shipped points leave a branch unreached, a variant S point is spliced too,
  added to a temporary copy of S's table (precised at M1). A variant changes S's columns,
  never a formula, wherever S has a column for the behaviour, as UL's withdrawals and
  over-funding do, so that the splice runs unchanged once the model compiles (K7; precised
  at M3).

  A market's change since a term's start that S carries as one Reference (D7) is switched
  on in S, where it is each point's change since its own start. The SEC table is read
  once, as a block is: the rows restated in force carry the change as their column, with
  the SEC Reference, the change made at the valuation date, at 0, and the rows issued
  later, which on that path have seen no change, are compared with S read with the change
  at 0. A test of the product's own reads one table holding a point in force, one issued
  at the valuation date and one issued later, at two values of the SEC Reference (precised
  at M11).

  Where spliced rows at different months share one S scenario, each row reads its own
  copy, re-based to its month as a step function under an id of its own, so the comparison
  exempts `scenario_id`. A future row's copy holds no level before issue, so a read there
  raises, and Phase 2's full sweep starts each scenario reader at `t_entry()` on such
  rows. Where S keys a state cell by contract year, the comparison skips, through
  `twin_mismatches`'s `arg_map`, each year that closed before the restated month, and each
  value of the year under way that the opening state stands in for, as MYGA's base of a
  year opened before that month, whose allowance is a column; the rules test asserts that
  the model asks about no year closed before the valuation date. And the rules test judges
  each read through a cell keyed by no month, a contract year, an age or nothing, against
  the month that asked (precised at M7). A recursion keyed by policy month from issue, as
  VUL's pricing path, is judged on the valuation clock at `m - duration_mth_init()`: R1
  and R2's look-ahead hold for it, and the look-back does not, since it reads no balance
  of the books. Where a product has such a recursion, its rules test asserts the premise:
  no call of the recursion reads a cell keyed by `t`, itself or through cells without a
  `t`. VUL's asserts more, that no cached call of a cell without a `t`, the loops over the
  frame excepted, has a precedent keyed by `t`, since its scan follows no such cell to
  what it reads. A scan that follows such cells to what they read asserts the premise of
  the recursion alone: a cell without a `t` may read one keyed by `t`, as MYGA's
  `free_wd_allow(y)` reads `interest_credited_pp` and DIA's `surv_to_payout()`
  `lives_if_last`, which their scans follow (R2, precised at M12). Each row is scanned
  once it has run on the books, its loops over the frame and then every monthly cell at
  every month from `t_entry()` to `proj_len() - 1` at every subaccount, timing and kind,
  as Phase 2's sweep, and before it is compared with S: no report of VUL's reads the
  account value's opening balance in a later point's issue month, and a base at `t == 0`
  there passed every test while the scan saw the reports alone (precised at M4).

  **S's own in-force rows are splice cases too.** On the policy-clock models their frames
  align at offset `d`: WholeLife at 108, FIA at 84 (FIA's in-force twins read their
  scenario re-based to 84 from the committed companion). On the projection-clock models
  they align at offset 0: UL at 120, ULSG at 300, VUL at 24 and 120, VA at 26. Any input S
  read on the policy clock is re-based by the months already elapsed — VA's scenarios by
  26 — so those goldens carry over as well.
- **T3 — Future new business.** `duration_mth = -k` reproduces the new-business frame
  shifted by `k`, with zeros before issue, given inputs shifted by `-k`. A step in an
  economic input at the valuation date, shifted by `-k`, falls before S's issue date, so
  S's twin of such a row reads no change since its own start (precised at M11).
- **T4 — Count algebra.** `BEF_DECR = BEF_NB + pols_new_biz`; the roll-forward closes;
  multiplying `policy_count` by a factor that is not a whole number, such as 2.5,
  multiplies every cash flow and leaves every per-policy value alone, with every
  assumption that ships at zero switched on at the value T2 gives it, in the SEC model
  itself, so that every flow is nonzero on some point. Doubling it, with those assumptions
  at zero, missed a count dropped from SPIA's commutations and surrender charge, and a
  count truncated to whole contracts (precised at M11). Each counted cell and counted
  report column is held to 1e-12 relative, value by value, except a difference of two
  scaled products, whose sides round apart where they nearly cancel: VUL's `av_change`,
  `net_cf`, `net_cf_ga`, `margin_expense` and `margin_mortality` are held to 1e-12 of
  their largest magnitude on the point (`av_change` moves by up to 1.7e-8 of itself at 95
  keys, each within 1.2e-13 of its peak; precised at M4). A counted cell that is a
  difference of counted values, as RILA's `av_change`, `net_cf`, `claims_over_av` and two
  aggregate residuals are, may instead be held to the residuals' 1e-9 floor, since
  cancellation leaves it ulps of its operands off the exact multiple, past 1e-12 of
  itself: on RILA's `av_change` on row 21 at `t = 1` by 6.5e-11 against an exact multiple
  of −17.38, and on its Account Value residual on row 16 at `t = 0` by 1.1e-10 against an
  exact multiple of 2.7e-11. A check whose tolerance scales with the count is shown at a
  count where each residual exceeds its unscaled tolerance on some row: RILA's Account
  Value residual is 2.4e-5 at a million contracts and 9.9e-5 at 3e6, inside its unscaled
  1e-4, and 2.9e-4, past it, at 1e7 (precised at M10).
- **T5 — Validation.** Each malformed in-force row raises in `Data`, naming its point. A
  row malformed only against a rule of the product, such as a point past its cover, raises
  in `proj_len()`, naming it too (D6). Each rule over a window of contract months is
  refused just inside each end of the window, its first month as well as its last, and
  accepted just outside, and each tolerance is pinned from both sides: RILA's maturity
  month, the first anniversary for its remainder and anniversary rules, months 1 and 11
  for its first-year rules, the remainder's cent and the renewal identity's two and a half
  cents. And every state the S model reaches on the splice's inputs, restated in force at
  its month, is accepted, at each window's edges by default (RILA's: every month of the
  first contract year, every sixth month, each anniversary and renewal among them, and
  every year's last month) and at every month on the full grid, except a state the product
  refuses by name, which the test sets aside and shows refused: RILA's contract emptied by
  a full withdrawal, which `RILA_US_S` keeps in force holding nothing (precised at M10).
- **T6 — Regeneration.** The committed SEC table and its generated companions, every row
  and column, equal what `gen_sec_points.py` produces from the S model and its inputs as
  committed. So an edit to an S row that an SEC file copies or derives from — a reworded
  `provenance` cell, a renamed lookup key — fails T6 until the SEC files are regenerated,
  in the same commit. "Equal" is exact for text and integers, and to 1e-12 for a float
  cell, which is read by its value: the text chosen for a computed float depends on the
  platform's pandas parser and libm (§4, *Record*).

### 5.3 Order

Term goes first, as the template, then WholeLife, the first product with an opening state
beyond its count (M1, M2). The other ten then run in three streams, one product at a time
in each (changed at M2):

- **Life:** UL → VUL → ULSG → IUL (M3–M6).
- **Deferred annuity:** MYGA → FIA → VA (M7–M9).
- **Payout:** SPIA → DIA → RILA (M11, M12, M10).

The M-numbers stay as identifiers, so RILA keeps M10. The order within a stream is set by
these reasons:

- Each chassis — UL for life, MYGA for the deferred annuities, SPIA for payout — comes
  before the products that build on it.
- Within a chassis, the product nearest to BasicTerm_SE comes first and the largest last.
  VUL already keys issue events on `duration_mth`; IUL needs the segment ladder.
- RILA closes the payout stream. Its annuitization builds on SPIA's chassis, and the
  deferred chassis it accumulates on, MYGA's, lands first in its own stream.

Until M2 a single chain ran the twelve: Term → WholeLife → UL → VUL → ULSG → IUL → MYGA →
FIA → VA → RILA → SPIA → DIA. Its reasons order a product after its own chassis, and
nothing in them orders products on different chassis: a deferred annuity reads nothing a
life product builds. Three things do tie the products together, and the streams keep each:

- *The template.* Each product follows the *Records* of §7.1 and §7.2, and each later
  record lists what it carries forward. A finding that binds later products goes to the
  products in progress as it is made, not only when its own product lands.
- *Shared files.* A product adds what it needs to the shared files — `sec_support.py`,
  `us_registry.py`, `conftest.py`, `test_model_conventions.py`, uslib's `index.md` and
  `README.md` — where it belongs, and reformats, reorders or changes nothing already there.
- *Landing.* Products land one at a time, each in its own two commits (D1). A product is
  rebased onto the branch as it then stands, keeping every product's additions to a shared
  file. Before it is pushed, the full uslib suite, doccheck and `gen_sec_points.py --check`
  for every registered SEC model run on the rebased tree.

Term's C step (M14) runs beside the streams (D2). One PR per product. §7 gives each
product's size. Times taken while the streams share a machine are noisy, so each record
says when it measured under load, and K6 is measured again on the merged branch at M13.

### 5.4 Exit criteria

- All twelve pass T1–T6, as §5.2 now states them, and the generalized conventions. M11's
  precisions of T2, T3 and T4, no absolute floor where a compared value falls far below 1
  and a count factor that is not whole with every zero-shipped assumption switched on, are
  taken at M13 into the four products built before them, Term, WholeLife, MYGA and UL,
  before the last three's fingerprints are frozen; a fix they force that moves a number of
  Term's regenerates Term's M14 fingerprint, committed alone (decided at M7's landing).
  §7.1's *Precised at M3*, item 11's comparison of the committed future row with its S
  point, frame by frame, is taken into FIA at M13 too, before its fingerprint is frozen
  (§7.11, *Record — M8*). M10's precisions of T4 and T5 are taken at M13 too, not at a C
  step, since they gate Phase 1. T5's window rules and tolerances, each pinned at its
  edges, and its every-state test go into the eight products landed before RILA, Term,
  WholeLife, UL, VUL, MYGA, FIA, SPIA and DIA, none of which has an every-state test; and
  RILA pins from both sides its first-year and first-term tolerances, which its module
  accepts only where they hold exactly, and refuses its first-term rule at month 1, its
  first, where its module has no case. T4's scaled check, shown at a count where a
  residual exceeds its unscaled tolerance, goes into WholeLife, whose count check scales
  with the count and whose residual exceeds the unscaled 1e-10 on 18 of its 22 rows at a
  millionfold count, which no test shows. A product that lands short of either takes it up
  at M13 too (decided at M10's landing).
- `python tools/doccheck.py` reports zero.
- The existing CI matrix is green inside its 90-minute timeout. The SEC suites roughly
  double the projected volume, so §8's K6 measures that before the timeout is touched.
- A compact fingerprint of each SEC model is frozen in its own test module before that
  product's Phase 2 changes anything, Term's at M14 and the others' at M13 (D2): for each
  point, each column of `result_cf()` and `result_pols()`, its sum, its largest absolute
  value and its values at the frame's first, last and three quartile months. It is a
  literal between marker lines written by `tools/gen_sec_fingerprint.py`, so a reviewer
  can read it, and it is committed alone. Phase 2 must reproduce it to 1e-12 relative,
  floored at 1e-12 of the column's scale.

---

## 6. Phase 2 — C: compiled

### 6.1 The recipe, per model

1. `point_id` → `idx` (R4).
2. `Data` array cells and decoding (R5–R8). §7 lists the tables each product turns into
   arrays.
3. `Projection` accessors and lookups rewritten onto `data.x()[idx]` (R11).
4. Timings, kinds and phases as named int References (R9, R10).
5. Aggregations rewritten as loops (R12); float-parameter engine cells inlined into the
   cached, int-keyed cells that call them, or keyed by an int instead, and none left
   uncached (R14); banded caches re-keyed (R15); rounding precomputed (R16).
6. `sample_sec.py`: set the recursion limit, then call every `Projection` cell at least
   once — `result_cf()`, `result_pols()`, every `check_*`, every timing of every `*_at`
   cell — over the committed points: every report, then each cell no report reaches.
   Untraced means untyped (F3). Every branch of a cell returns the one type its others
   return (F3), and the branches the committed points miss are verified by C4 on the
   splice grid, which runs the compiled model on them: typing follows a cell's values,
   not its branches.
   `spec_sec.py`: `cells_param_size` for `t`, and for each other integer-parameter tuple,
   covering every argument a cell is called with on a point the contract allows, in its
   frame and in the month after it, `t = proj_len()`, which the roll-forward reads and
   C4's full sweep evaluates every monthly cell at (Term's `mort_rate` reads PLT duration
   68 there), plus one for the 0 index and one of headroom where that leaves room, with
   the derivation in a comment naming the References it holds (F4). `proj_len()` refuses a
   point outside that contract, naming it, through a lower-case Reference for each bound a
   size is derived from: the youngest issue age, the shortest term, the expiry age, beside
   `Data`'s horizon (M14).
7. Docstrings, `model-sec.md`'s compiled-model section, and `run_sec.py --cython`, which
   builds through `build_sec_cy.py` and releases ItemSpaces in block runs (F5): it freezes
   what is alive once the model and its table are read and again after the frame pass,
   deletes and fully collects each ItemSpace in both passes, and keeps the block's sum
   compensated, as pandas' groupby sum is, so that it is M1's block bit for bit. It takes
   `Projection`'s key from the model, so it runs at either stage, and finds the build tool
   only under the repository's `lifelib/libraries/`, saying otherwise that it cannot
   build. `build_sec_cy.py` marks each translated module `infer_types=True`,
   `cpow=True`, and compiles with `-ffp-contract=off` on every platform but Windows
   (F3, M14).

### 6.2 Tests

All marked `cython` unless noted.

- **C1 — The Phase 1 suite still passes** (not marked `cython`). Only call syntax changes:
  positions instead of labels, timing References instead of strings.
- **C2 — Fingerprints.** The Phase 1 freeze reproduces to 1e-12 relative (§5.4's form;
  `gen_sec_fingerprint.py --check` makes the same comparison; not marked `cython`).
- **C3 — Typing guard** (`test_compiled_conventions.py`, `cython`). From the generated
  `_mx_classes.pxd`: every `Projection` cell outside the R17 allowlist is compiled, returns
  and takes only `bint`, `long long` or `double`, and keeps no dict cache, an uncached
  cell, which mx2cy leaves taking and returning `object`, failing it; every `Data` cell the
  S twin lacks, but a reader of a file, returns a typed memoryview of int64 or float64, or
  a C scalar. Every integer-parameter tuple has a size in `spec_sec.py` that its caches
  carry exactly, and every size is taken. In the generated C no projection formula outside
  the allowlist declares a Python-object local, calls a Python builtin other than an
  exception it raises, or builds a list, dict or set, and each translated module begins
  with `infer_types=True` and `cpow=True`.
- **C4 — Compiled equals modelx, cell by cell** (`cython`). After a full modelx sweep,
  every `Projection` cell at every argument modelx caches matches the compiled model:
  identically on x86-64, where `build_sec_cy.py` compiles with `-ffp-contract=off` off
  Windows, so that gcc and clang fuse no multiply and add whatever `-march` gives, MSVC
  emits no fused multiply-add for x64 without `/arch:AVX2`, and `cpow=True` makes the
  compiled power C's `pow`, which Python's calls; elsewhere to 1e-12 relative, floored at
  the cell's magnitude on the point. A bool and an int keep their kind, every raise has the
  same type and message, and every `Data` array is exact. Run on the committed points
  (`test_compiled_conventions.py`), and on the product's splice grid and at its contract's
  extremes (the product module). The toolchain test checks the flag on the compiler's
  command lines.
- **C5 — No Python machinery in `Projection`** (static, not marked `cython`;
  `test_compiled_conventions.py`). Outside the allowlist no formula refers to a module,
  reads `.loc`, `.iloc`, `.at`, `.iat`, `.values`, `.to_numpy`, `iterrows`, `itertuples` or
  `apply`, refers to a reporting cell, holds text outside its docstring and raise
  messages, reads a Reference holding text, calls `len()`, or holds a generator,
  comprehension, lambda or nested `def`; outside its raise statements it calls nothing but
  a cell, a `Data` vector and `int`, `float`, `bool`, `abs`, `min`, `max` and `range`, no
  method, and builds no list, dict, set or tuple but a table read's index. No cell outside
  the allowlist is uncached (R14). Every `Data` cell such a formula calls returns an int64
  or float64 array or a Python int or float, and an array is read at once by element; the
  same holds for every `Data` array another `Data` cell reads. No cell outside the
  allowlist shares its name with what a keyword call calls anywhere in the model. Every
  cell the registry declares reporting returns its point's column of the same name.
- **Release, stack, refusals and References** (`cython`). `run_sec.py --block`, compiled,
  leaves no ItemSpace but the base alive after any collection it makes once frozen,
  collects at least once per point, and leaves none alive at the end
  (`test_compiled_conventions.py`). The longest contractual cover's cold call runs in a
  thread reserved at 1 MiB and on the main thread; the compiled model refuses what modelx
  refuses, with modelx's message, the only guard on its raises, the contract's own
  refusals and text keys among them; and a Reference set late changes no value it has
  cached (the product module). They gate a milestone as C1–C5 do (§6.3).
- **C6 — Benchmark** (`tools/bench_sec_cy.py <product>`, a script, not a test). modelx,
  export and compiled timings on a replicated table, recorded in `model-sec.md`. The
  target is BasicTerm_SC's order of magnitude; a shortfall is reported, not hidden.

### 6.3 Exit criteria

- All twelve at `stage: "EC"`, passing C1–C5 and §6.2's release, stack, refusal and
  Reference tests on Linux and Windows in the `cython` job.
- C6 recorded for each.
- `doccheck` reports zero.

A milestone whose gate is met on Linux alone is done on Linux, and stays open until the
`cython` job has run its tests on Windows (M14).

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
- To arrays: the premium schedule, a 5-key `.loc` per `t`, becomes
  `[schedule, policy_year]`, with a per-point schedule number and each schedule's first
  and last year, sized by one checking cell; base mortality `[age]`; the class factor is
  joined per point in `Data`; the shock-lapse bucket lookup becomes a loop over three
  `Data` vectors, keeping `jump_ratio` the one definition (M14).
- Decoded: `plan` to `policy_term`; `premium_mode` to `prem_cycle` and `modal_factor`; the
  M(1) override to a value plus a flag; `phase` to a code.
- Never reached by `result_cf`: `pols_lapse`, `pols_maturity`, `phase`; by the three SEC
  reports, `phase` alone; after Phase 2 also `band`, `model_point`, the four label
  accessors and `point_id`, which `sample_sec.py` calls (M14).

#### Record — M1, done 2026-11-01

Built in two commits, as D1 requires: `Term_US_S` copied with only `_name` changed, then
the enhancement. A design was prototyped and critiqued before the build. The tests were
written against the build and checked by injecting faults. The whole was then reviewed
under three lenses: the numbers, the plan's rules, and the tests with the docs. The review
found 21 defects, 4 of them major, and a re-review of the fixes found 2 more. All 23 are
fixed in `Term_US_SEC`. The one that `Term_US_S` shares is carried below.

**What exists now.**
- `Term_US_SEC` at stage `E`. `Projection` keeps all 52 of `Term_US_S`'s cells: 24
  unchanged, 8 with a new docstring only, and 20 rewritten. It adds 10: `policy_count`,
  `duration_mth_init`, `t_entry`, `is_active`, `expiry_mth`, `pols_if_at`, `pols_new_biz`,
  `premium_pp_ann_py`, `conv_elig_py` and `result_pols`. `Data` reads its own model point
  table and `Term_US_S`'s four assumption tables in place, and checks the table as it reads
  it.
- `model_point_table_sec.csv`, six rows generated from Term's `SecSpec`. They are S's two
  points as twins, S point 2 at month 12, S point 1 at months 126 and 719, and S point 1
  issued 3 months after the valuation date. A case-insensitive search for every publisher,
  product and form number `term_life/sources.md` cites finds none of them in it.
- `tests/test_term_life_us_sec.py`, 59 tests: T2 on 23 splices, T3 on 7 future points, T4,
  T5 on 12 malformed tables and its edges, T6, a test of how the model computes (R1, R2 and
  D3), and the product's own facts. The SEC conventions, T1 among them, now run on a model:
  32 pass, and `test_net_cf_is_income_positive` is skipped, as it is for `Term_US_S`.
- `run_sec.py`, for one point or `--block`; `model-sec.md`; the registry entry with its
  `INPUT_FILES`; and five generated pages. doccheck reports 477 pages and 0 warnings.
- Of §4's items carried into Phase 1, three are discharged: the pages were regenerated once
  `model-sec.md` existed, `gen_input_files.py --write` rewrapped the ULSG and WholeLife
  entries and changed no value, and T6 takes the module's swept S model through `s_model=`.

**Departures and precisions.**
- *The cover check* is in `proj_len()`, not `Data`, because the end of cover needs
  `expiry_age`, a `Projection` Reference. A point past its cover reads, and `proj_len()`
  refuses it, naming the point. `run_sec.py --block` asks every point for its frame before
  it projects any. D6 and T5 are precised in place.
- *The future horizon* was settled here rather than at M14:
  `Data.future_horizon_mth = 120` (D4, precised in place).
- *R3* is precised in place: a model-point accessor cell is allowed, a per-`t` lookup is
  not.
- *One more R1a site.* Beyond the list above, `conv_rate` found the final eligible year by
  asking `conv_elig(t + 12)`, twelve months ahead of its own (R2). It now asks
  `conv_elig_py(policy_year(t) + 1)`. The expiry tests in `pols_maturity` and `phase` were
  still correct on the valuation clock. They moved to the policy clock anyway, so that
  cover has one definition, and `phase` gains `PRE_ISSUE`.
- *Guards outside cover* (R1). `prem_due`, `premium_pp_ann`, `mort_rate_base`, `conv_elig`,
  `comm_rate` and every count return zero or `False` outside cover, before any table or
  rate is read. The review found `comm_rate`: before issue `duration(t)` is negative, and
  the commission scale read it as a year of the level period.
- *Acquisition* is `expense_acq * pols_new_biz(t)`, per policy issued and not inflated, as
  in BasicTerm_SE. On a point issued at `t = 0` it is the one designed difference from S,
  which charges $300 once per model point, whatever the count. So T1 holds on Term only
  while each S point counts one policy. Every point of all twelve S tables does, and the
  Term module asserts it of Term's.
- *The count chain* is one cell a month (D5, precised in place).
- *`result_cf_annual`* leaves out the months before issue. An in-force point's first row
  holds the rest of its current policy year.
- *The Phase 0 harness changed* (§5.2, precised in place). `twin_mismatches` compares S's
  own frame only, and reports an S cell the SEC model lacks. Before the change, a point
  whose cover ends with the level period failed T2 falsely, and a renamed cell passed T1.
  `test_sec_support.py` has 37 tests.
- *T2 switches conversion on* in both models, at the notes' standardized 1% a year and 2%
  in the final eligible year: at the shipped zeros the conversion window is invisible to
  any comparison. It also splices three variants of S's points, added to a temporary copy
  of S's table, for branches the shipped points never reach:
  - issue age 65 paying quarterly, for the window's age limit and a three-month cycle;
  - T20 at 45 paying semi-annually, for a level period of another length, with its premium
    scale added to the copies only;
  - age 85 paying monthly, for cover that ends with the level period.
- *How the model computes is tested.* On the splice grid no cell is called at a negative
  month and none reads beyond `t + 1`. On the committed points `duration_mth` is a closed
  form, and the reports run under a recursion limit of 40. No number shows any of these,
  and Phase 2 needs each.

**Measured for K6 and F7.**
- *Time.* The module runs its 59 tests in 32 to 37 s over two runs. In the slower run, T2's
  23 splices take 9.1 s, plus 1.8 s for their fixture. The rules test takes 6.9 s, T3 3.4 s,
  and the three tests that start an interpreter 8.4 s together. The uslib suite went from
  1,061 passed and 19 skipped in 4 min 53 s (M0) to 1,154 passed and 12 skipped in
  5 min 54 s. The new passes are the
  module's 59, the SEC conventions' 32 and the harness's 2. The eight skips for an empty SEC
  section became one. The splice stays in the default run; WholeLife, whose sweep is about
  ten times Term's (§4, *Record*), is the next measurement.
- *Depth.* A cold `net_cf` of the last month runs 727 cells deep on a 720-month frame,
  against 726 in `Term_US_S`. On the longest frame the contract allows, issue age 18 and
  issued 120 months on, it runs 931 deep. An ascending sweep stays at 10. In the modelx
  export the cold call needs a recursion limit of 1,469 (S: 1,465), or 1,877 on the longest
  frame, and the ascending sweep 51. With the two-cell count chain, the 720-month figures
  were 1,445 cells and a limit of 2,905.

**Faults.** 63 faults were run against the module, the conventions and the harness suite,
each injected alone into its own copy of the library. 62 fail at least one test. The 63rd
is a control, the two-cell count chain, which changes no value. After the re-review, a
recursion backward over the frame through `t + 1`, which also gives the same numbers,
fails the rules test too.

**Carried into M2 and after: the template.**
1. *Derivation.* Commit 1 is the S folder copied, with `_name` edited and nothing else.
2. *The policy clock.* `duration_mth_init()` is an `int` accessor of `duration_mth`.
   `duration_mth(t) = duration_mth_init() + t`, never a recursion.
   `t_entry() = max(0, -duration_mth_init())`. `is_active(t)` is
   `0 <= duration_mth(t) < <end>`, where `<end>` is S's frame from issue as a policy-clock
   cell named for the event that ends cover: `expiry_mth()` here, `maturity_mth()` where the
   contract matures.
3. *The frame.* `proj_len() = <end> - duration_mth_init()`, raising `ValueError` naming
   the point when that is not positive.
4. *Counts.* `policy_count()` is a `float` accessor. `pols_if_init()`, `pols_new_biz(t)`
   and the two timings are as D5 has them, the chain one cell a month. S's later timings
   and maturity rule are kept, and every count is a `float` in every branch.
5. *Outside cover.* Every count returns 0.0 before it evaluates a rate. Every read at a
   policy year, a PLT duration or an attained age is guarded by `is_active(t)`, and so is a
   contractual scale such as a commission rate. A contractual boolean is `False` there.
6. *S's tests of the frame index.*
   - Each test of `t` against a contractual event becomes a test of `duration_mth(t)` or
     `policy_year(t)`, even where the old test stays correct.
   - Each read of a schedule at a policy month passed as `t` becomes a policy-year cell,
     `<cell>_py(y)`.
   - A question about the next policy year, asked twelve months ahead, becomes
     `<cell>_py(policy_year(t) + 1)`.
7. *Expenses.* Acquisition is charged per policy issued, uninflated. Expense inflation
   keeps S's formula, on `t`. Where SEC charges per policy what S charges per model point,
   T1 holds only while the S points count one policy: the spec's comment says so, and the
   module asserts it.
8. *Reporting.* `result_cf()` keeps S's columns. `result_pols()` is `pols_if`,
   `pols_new_biz`, the decrements in S's processing order, then the maturities, indexed
   `t`. A report keyed on the policy clock keeps S's key and drops the months before issue,
   and a phase cell gains `PRE_ISSUE`.
9. *Data.* `model_point_file = "model_point_table_sec.csv"`, with S's readers unchanged.
   The table is checked as it is read, vectorized, and the first check that fails raises,
   naming the column or every point at fault. The checks, in order: the in-force columns
   are present, `point_id` is unique, `policy_count` is a number zero or more,
   `duration_mth` is whole and within the horizon, then the product's own state columns
   (D6). A rule of the product is checked in `proj_len()`.
10. *The table.* The committed rows are the twins, a few derived rows for distinct cases
    (an anniversary, mid-year after the product's main event, the last covered month) and
    one future row. The full splice grid is built in the tests from the same spec.
11. *The test module.*
    - Fixtures `sec_model`, `s_model` (swept, and handed to T6 as `s_model=`) and
      `spliced`. Each model is read under a name of its own, nothing is written inside the
      library tree, and a row is found by its kind, S point and month.
    - T2 runs over `SPLICES + IN_FORCE_TWINS`. Term has no in-force twin. WholeLife's is
      `("twin", 1, 108)`, and §5.2 lists the rest.
    - Variants cover every branch the shipped points hide: another level period, every
      premium mode, cover that ends with a contractual period.
    - Every assumption that ships at zero is switched on in both models. Valuation-clock
      inputs are neutralized by Reference, or by `shift_months` where they are tables, and
      a separate test asserts the valuation clock on the shipped inputs.
    - Each product keeps its own lists: the S cells its sweep never reaches (`_sweep_s`),
      and `OUTSIDE_COVER` and `IN_COVER_ONLY` for the guard test.
    - The rules test makes its negative-argument and look-ahead checks on the splice grid,
      after the reports. It checks the closed-form clock and the lowered recursion limit on
      a fresh read of the committed points. Each product sets the limit from its measured
      depth: Term's reports reach 10 cells on the committed points and 13 on the grid,
      under a limit of 40.
12. *The runner.* `run_sec.py [point_id | --block]`, point 1 by default. `--block` asks
    every point for its frame first, sums the frames with
    `pd.concat(frames).groupby(level="t").sum()`, and releases each ItemSpace once read.
    Output is ASCII, and the generator's columns are optional. A test runs it and checks
    its numbers.
13. *The notes.* `model-sec.md` has the H1 *In-Force Implementation Notes* and Term's
    sections: running it, the two clocks, the in-force interface, the model points, counts
    and timings, the departures, the tests.
14. *Registry.* The SEC entry goes directly after its twin, with `INPUT_FILES` written by
    `tools/gen_input_files.py --write`.

*Precised at M3*, for every product that lands after it:
- Item 5, *Outside cover*. Where a frame ends at a horizon rather than at an event that
  ends cover, as in the UL family, whose four S models mature nothing, the count and the
  balances the roll-forwards read at `t + 1` are carried into `t = proj_len()`, so that
  those roll-forwards close with survivors left. Every other count, balance, flow and
  charge is zero there, the cells that read `t + 1` included, as is every rate read at a
  policy year or an age, and every flag is false; the clocks and the valuation-clock
  inputs keep their values. Every per-policy flow and charge is guarded by `is_active(t)`,
  never left to a contractual age to reach zero at the horizon.
- Item 9, the assumption tables. `Data` checks each table a projection reads, its keys and
  every value a reader reads, once and before any reader reads a value, at stage `E`,
  which brings R7's refusal at the first read forward and extends it to values. It does so
  either in the cell a keyed reader takes its extent from, which reads the key column by
  value once, as in UL, or in a checked copy of the table that the projection reads alone,
  as in MYGA (§7.10). In UL's form a table read by a per-point join gets a count cell that
  the join asks first, as UL's `class_count()` and `surr_charge_count()` are. A key that
  is blank, text or not whole is refused, naming the file, the column and its lines; keys
  that repeat, or leave a gap where a reader reads every key between the first and the
  last, naming each repeated key with its lines and each missing key or span; a text key
  that is blank or repeated, naming its lines. A value that is blank, text or infinite is
  refused, naming the column and its lines, in every column a reader reads, every table a
  cap, a `min` or a `max` reads among them: an S model reads a blank as a missing value,
  which its own `min` and `max` can lose without a word.
- Item 11, the test module. Each such refusal is a case of a table-driven list, read
  through a projection as well, its message matched whole, and the accepted edges write
  every keyed table's keys as floats. An S text value no decode knows raises S's message,
  in a table-driven `UNDECODABLE` list. Each committed derived and future row is compared
  with its S point frame by frame, since T6 compares a float to 1e-12 and so pins UL's
  smallest committed count, 1.8e-10, only to 0.57%. Where S's check is a `math.isclose`
  loop with no residual cell, as in the UL family, its per-month residual becomes a
  `*_resid(t)` cell relative to the larger side, floored at `abs_tol / rel_tol`, 1 in UL
  and 10 in IUL, so that S's tolerances hold; where S has `*_resid` cells of its own, as
  the annuities and WholeLife do, SEC keeps them and their tolerances, which T1 compares.
  Either way the check fails a residual that is not a number, which a test shows.

**Carried into Phase 2.**
- Term's `spec_sec.py` sizes its caches from the contract:
  - `premium_pp_ann_py` and `conv_elig_py` by policy years 1 to 77 (issue age 18);
  - `plt_mort_factor` by PLT durations 1 to 67;
  - `t` from 0 to 1,044: the longest frame's 1,044 months (12 × 77 + 120), and the month
    after, which the roll-forward check reads.
- `proj_len()` names `point_id` when it refuses a point. At stage EC it names `point_id()`,
  and a test checks that the compiled cell still raises.
- The recursion limits above size `sample_sec.py`, `run_sec.py --cython` and the Windows
  job's stack.
- No test checks that `run_sec.py --block` releases each ItemSpace, since that changes no
  number. Phase 2's memory test (F5, K2) should.

*Discharged at M14:* the spec sizes (`t` 1,046, `(t, timing)` (1,046, 2), `y` 79, `d` 69,
the last from the 68 read in the month after the frame on the shortest plan), read back
from the `.pxd`; the compiled `proj_len()` refusal test; the recursion limits (sample
10,000 against 1,881 measured; the compiled model needs none; the 1 MiB stack test); and
the memory test,
`test_compiled_conventions.py::test_a_block_run_releases_each_compiled_point`, run
against the product's own runner, which catches a runner that does not collect, does not
release, or keeps a point.

**Carried, outside the SEC models.**
- `tools/fix_doc_roles.py` takes the first model folder in each product directory, in
  directory order, so in `term_life` it would fix one of the two models. No test or step
  runs it, but it must take every model folder before its next use.
- Two S-side items for §8.2 item 4:
  - `test_term_life_us.py`'s `test_an_input_can_be_swapped_without_touching_formulas`
    writes `mort_table_doubled.csv` beside the models while it runs, where a concurrent
    `test_every_csv_beside_the_model_is_actually_read` would see it.
  - `Term_US_S`'s Projection docstring, under *Premium mode*, reads "six two semi-annual
    instalments". The slip is fixed in `Term_US_SEC` only.

#### Record — M14, done on Linux 2026-11-02

M14 is Term's compile step: Phase 2 for `Term_US_SEC`, brought forward to run beside
Phase 1's streams (D2). A design was prototyped and critiqued first. Term's Phase 1
fingerprint was then frozen and committed alone (§5.4, C2), and the compile step followed
in a second commit: the build, tests written against it and checked by injecting faults,
and the docs. The whole was reviewed under three lenses: the numbers, the plan's rules,
and the tests with the docs. The review found 33 defects, 10 of them major; two of the 33
were found under two lenses each. A fix stage fixed 31 and recorded 2: the q > 1 domain,
which the landing settles (below), and a future horizon raised past 120 months, a
compiled-only `IndexError` the docs state. It rejected four parts of findings, each with
its reason. A re-review of the fixes found 6 more, 1 of them major, and a second fix stage
fixed all 6. C1–C5 and §6.2's release, stack, refusal and Reference tests pass on Linux,
and C6 is recorded. The gate also needs Windows, where the `cython` job has not yet run,
so M14 stays open (§6.3, §9).

**What exists now.**
- `Term_US_SEC` at stage `EC`, compiled and checked against modelx. `Projection` has 64
  cells, keyed by `idx`, with a Reference `idx = 0`. 56 compile to `bint`, `long long` or
  `double`; the 8 that stay Python are `model_point`, the four label accessors and the
  three reports. No cache is a dict, and no cell is uncached.
- Codes, named after S's strings: `BEF_NB` 0 and `BEF_DECR` 1, and the phases `PRE_ISSUE`
  0, `LEVEL` 1, `PLT` 2 and `EXPIRED` 3. The contract the caches hold is three lower-case
  References that `proj_len()` checks: `expiry_age` 95, `issue_age_min` 18 and
  `policy_term_min` 10.
- `Data` keeps S's five readers unchanged and adds 23 cells, each an int64 or float64 array
  or an int, among them `premium_schedules()`, the premium table's one check.
- A compiled `Projection` ItemSpace is 429,896 bytes, the type's basic size (429,912 by
  `sys.getsizeof`).
- Beside the model: `sample_sec.py` and `spec_sec.py`; `run_sec.py` with `--cython` and
  `--build DIR`; and in `model-sec.md` a part of seven subsections, *The compiled model*.
  `tools/build_sec_cy.py` builds the model with two directives and, off Windows,
  `-ffp-contract=off`; `tools/bench_sec_cy.py` is C6; and `tools/gen_sec_fingerprint.py`
  came with the freeze.
- Tests, as landed: `test_term_life_us_sec.py` has 106 (99 modelx, 7 compile, the cap's
  two among them), `test_compiled_conventions.py` 6 (3 modelx, 3 compile; its
  reporting-key test runs on `WholeLife_US_SEC` too), `test_sec_support.py` 50 and
  `test_cython_toolchain.py` 1 (compile). On M14's tree before its rebase onto M2 and the
  cap, the uslib suite gave 1,217 passed and 12 skipped, the `cython` selection 10 passed
  and none skipped under `USLIB_REQUIRE_CYTHON=1`, and doccheck 477 pages and 0 warnings.
- Shared files, added to in place: `sec_support.py` (`codes`, `twin_mismatches`'
  `codes=`, `SecSpec.twin_arg_map`, `reporting_cells`, the compile helpers
  `require_cython`, `compiled_case` and `run_compiled`, and the C3, C4, C5 and release
  checks; `SEC_SPECS` untouched); `us_registry.py` (Term's entry at `EC`, with `idx` and
  `"reporting"`); `conftest.py` (the `sec_build` fixture and the hook that fails a skipped
  compile test); `test_model_conventions.py` (T1's `codes=` and `arg_map=`, and the
  check of an `EC` model's companion files); uslib's `index.md` and `README.md`; and a
  comment in `tests.yml`.
- What it discharges of the items §4's and M1's records carry forward is marked in place.

**Departures and precisions.**
- *The build* puts two compiler directives, `infer_types=True` and `cpow=True`, on each
  translated module between mx2cy's translate and compile, which C3 requires, and appends
  `-ffp-contract=off` to `CFLAGS` on every platform but Windows, which the toolchain test
  reads from the compiler's command lines (F3, K1).
- *The premium table* is per schedule, `[schedule, policy_year]`, with a per-point schedule
  number and each schedule's first and last year, all three sized by
  `premium_schedules()`, the table's one check; not per point (R7, precised in place).
- *Decoding follows S on each element*: the plan is `int(plan[1:])`, the band S's own
  if-chain. Every key is read by its value in every cell that reads it, the extents
  included: a policy year 1.0 is year 1, and a key that is not whole, text among them, is
  refused with the table's message (R6, precised in place).
- *Refusals at the first read*, naming every point, the schedule or the table, where S
  failed only when a projection reached the value: a `point_id` not whole, a plan it cannot
  read, an unknown mode or class, an override neither a number nor blank; a schedule whose
  years are not whole, gapped, repeated or below 1, or with a blank premium; a mortality
  age not whole, gapped, repeated or negative, or a blank rate; no shock bucket. They are
  19 `UNDECODABLE` cases, each but the label's also reached by a projection.
- *The contract's bounds* (F4, precised in place). Besides a point past cover,
  `proj_len()` refuses a level period below `policy_term_min = 10`, the shortest plan in
  `product-spec.md` (plans T5, T0 and T-5 in the tests), and an issue age below
  `issue_age_min = 18`, in both engines. M1's `proj_len()` refused neither: in modelx it
  projected the T5 point, given a schedule of its own, in 720 rows, as this model does
  once `policy_term_min` is lowered to 5, and raised `KeyError` on T0, T-5 and age 17,
  where a shipped table lacks the key.
- *The reporting cells* are declared in the registry's `"reporting"`, not in `SecSpec`, and
  `SEC_SPECS` is untouched; `SecSpec` gains `twin_arg_map` (§5.2, T1).
- *The runner* (§6.1, step 7) takes its key from the model's parameter. `--cython` builds
  in place when the build is stale, with its message on stderr, and stops, saying it
  cannot build, where the product does not sit under a repository's `lifelib/libraries/`:
  a `lifelib.create()` copy, or a path too shallow to hold one. `--build DIR` refuses a
  directory without a build. The release and the compensated sum are as F5 and step 7
  say, bit for bit with M1's `groupby` sum.
- *C3* exempts `Data` readers; it reads the generated C for Python-object locals, for
  Python builtins other than exceptions and for list, dict and set construction; and its
  messages name an uncached cell among those mx2cy has no trace of.
- *C4* is exact on x86-64, resting on `cpow=True` and `-ffp-contract=off`, and to 1e-12,
  floored, elsewhere. The 1 MiB stack and stale-Reference tests compare compiled values
  with modelx's the same way.
- *C5* forbids calls other than to cells, `Data` vectors and `int`, `float`, `bool`,
  `abs`, `min`, `max` and `range`, method calls, container displays outside raise
  statements, and any uncached `Projection` cell outside the allowlist.
- *`conftest.py`* fails any skipped compile test under `USLIB_REQUIRE_CYTHON=1` (D13,
  precised in place).
- *The compiled refusal test's* compiled-only case is a call past the caches,
  `net_cf(1046)`, since a frame the contract does not allow is refused by `proj_len()` in
  both engines. It also runs the four `NOT_ISSUED` cases with their own inputs, and a text
  policy year.
- *Contract-extreme inputs* extend the tables with a distinct value per added key.
- *The fingerprint literal* sits at the end of the module, byte for byte the freeze
  commit's.
- *`model-sec.md`* gains *The compiled model*, seven subsections, among them the flag
  beside the two directives, the four bounds the caches are sized from, text keys, the
  cap on mortality and the cache-clearing caveat. Its speed section quotes the second fix
  stage's run.
- *The mortality cap, made at landing* (§5.1, step 6). `mort_rate` becomes
  `min(1.0, base × class factor × PLT factor)`, as `SPIA_US_S` caps `q_be` and `q_rated`
  and `DIA_US_S`, `FIA_US_S` and `ULSG_US_S` cap their mortality. Compiled, it is an
  inline comparison of two doubles, which C3 and C5 accept unchanged. With the annual
  rate at 1, `mort_rate_mth` is exactly 1.0, so every policy in force at the start of the
  first month where the cap binds dies in that month, and the count is 0.0 after it.
  `Term_US_S` does not cap. Past 1 its monthly rate is complex in modelx, and so is every
  count and cash flow that reads it, so the cap changes no value S computes as a real
  number but the annual rate itself; uncapped, the compiled monthly rate there is NaN.
  The cap is a recorded departure from S, and `Term_US_S` goes on §8.2 item 4's list. No
  other Term decrement can pass 1, and none is capped: the lapse rate is a constant by
  policy year, or in the shock month the bucket's rate, at most 0.90, applied in full;
  the conversion rate is one of two References, 0 as shipped; none is a product of
  factors. No committed point, splice-grid point or contract extreme comes near the cap.
  Their largest annual rates are 0.2503, 0.4381 (the grid's tobacco variant) and 0.2503,
  all at attained age 94, and `Term_US_S`'s own two points also peak at 0.2503, so a cap
  in S changes no shipped number. The fingerprint reproduces (C2), and the committed
  table is current.
- *Where the cap first binds.* On the shipped tables the uncapped rate passes 1 only after
  the level period, in which it is at most 0.219. At the issue ages `product-spec.md`
  admits, it first does so in the tobacco class on the twenty-year plan issued at 65, at
  attained age 94, once M(1) passes 5.9152, which the notes' rule gives at a jump ratio
  past 9.9367; a non-tobacco class there needs an M(1) above 8, the most the rule gives.
  The model does not refuse an older issue age. Where a point's first PLT year falls at
  attained age 94 (T10 issued at 84, T20 at 74, T30 at 64), the rate passes 1 there once
  M(1) passes 4.5652 in the tobacco class and 7.9891 in StdNT, the least of any point the
  model projects. The "5.9 or more" and "a jump ratio of 9.9" of `model-sec.md` as the
  second fix stage left it were slightly low.
- *The cap's tests*, in `test_term_life_us_sec.py`. Their point is S's anchor cell in the
  tobacco class, issued at 70, with M(1) 8.0 as its override; its rate first passes 1 at
  t = 240 (age 90, policy year 21). In modelx, under the splice's References, S's monthly
  rate is complex from there to the end of cover, this model's annual and monthly rates
  are `(float, 1.0)`, every policy in force dies at 240, and the three reports hold finite
  float64 values. The point is compared with S wherever S's value is real, the capped
  rate and S's reports excepted, at 1e-9 relative with no absolute floor, since the counts
  there are near 1e-8: as new business, and restated in force from t = 239 with S's count,
  as the splice compares a restated row. A third row, in force from five months into
  policy year 21, loses every policy in its first month. At the cap's fix stage a probe
  found both comparisons bit for bit, at rtol 0 and atol 0. Compiled, C4 runs on all three
  rows under the shipped References, the row from t = 239 opened with one policy.

**Measured for K6, F2 and C6, F5 and F7.** On the shared 4-CPU Xeon (2.10 GHz), with other
workflows running; on the second fix stage's tree, before the rebase onto M2 and the cap,
unless a stage is named.
- *Time (K6).* The uslib suite, with modelx-cython installed and so the compile tests
  included, ran 1,217 passed and 12 skipped in 514 s (8 min 34 s; load 1.8 to 3.0). It
  was 1,154 and 12 in 5 min 54 s at M1, 1,201 and 12 in 8 min 12 s at the tests stage,
  and 1,210 and 12 in 500 s and 517 s at the fix stage. The `cython` selection ran 10
  tests in 162 s (load 3.0 to 3.2): Term's compile 66.5 s inside C3's test, the toolchain
  test 38.2 s, C4 on the 55-point grid 27.3 s plus 8.7 s of setup, the refusal test
  7.6 s, the compiled runner test 4.5 s, C4 on the committed points 3.5 s and at the
  extremes 1.6 s, the 1 MiB stack 1.5 s, the release 1.2 s and the stale-Reference pin
  0.6 s. Without compiling, Term's module (98 tests), the harness suite (50) and the two
  modelx tests of `test_compiled_conventions.py` ran 150 tests in 91 s; WholeLife's
  module alone runs 2 min 46 s to 3 min 01 s by default (§7.2). doccheck took 203 s and
  190 s. At the fix stage, the compile took 52.98 s standalone and 53.5 to 59.1 s inside
  C3's test, and the selection 140 and 144 s. With the cap's compile test, the selection
  ran 11 tests in 144 to 201 s over four runs at the cap's stages, and in 259 s at landing
  (*Verified at landing*, below).
- *Speed (F2, C6).* `tools/bench_sec_cy.py term_life`, three runs of each engine, the
  fastest given with the loop's spread (load 1.6 to 3.0, 281 s in all). Compiled, 6,000
  points: 0.496 ms a point on `net_cf` (2.98 to 3.20 s) and 1.26 ms on `result_cf` (7.57
  to 8.02 s), 84 MB, flat. The export, 600 points: 4.73 ms (2.84 to 3.32 s) and 5.88 ms
  (3.53 to 4.04 s), 84 MB. modelx, 120 points: 196 ms (23.47 to 26.00 s) and 223 ms
  (26.81 to 27.65 s), 116 MB, so the compiled model runs 394 and 177 times modelx; `Data`
  takes 0.032 s and the frame pass 0.08 s, and `net_cf` sums to 2334.089393 on every
  engine. The fix stage's run, under a lighter load (0.9 to 1.4) and before
  `policy_term_min` and `premium_schedules`, gave 0.468 and 1.27 ms compiled, 4.99 and
  6.23 ms exported and 445 and 179 times modelx. Neither change runs per month, so the
  gap is the load's. F2 gives both runs' ratios to the export, and the ratios of
  `BasicTerm_SC` and of Term as Phase 1 left it, both timed on 2026-11-01, the second at
  the docs stage.
- *Memory (F5).* A compiled ItemSpace is 429,896 bytes. Releasing 600 compiled points
  (fix stage) took 1.35 to 1.40 s and 71 MB as the runner is written, 349 MB without the
  collection, and 10.38 to 11.71 s with the first freeze after the frame pass. With the
  old freeze order the frame pass of 6,000 compiled points took 65.65 s (docs stage), and
  the benchmark 12 min 46 s (review).
- *Depth (F7).* At the fix stage, modelx's cold `net_cf(proj_len() - 1)` on fresh reads
  ran 728 cells deep on the committed 720-month twin (M1: 727), and F7's 932 at both
  contract extremes, frames of 1,044 months with 924 months of cover from `t_entry()` 120
  (M1: 931), which `test_the_deepest_cold_call_runs_one_cell_a_month` bounds at 16 more
  than one a month back to `t_entry()`; a two-cell count chain ran 1,446 and 1,854. F7
  gives the C stack each takes compiled with gcc (docs, tests and review stages) and the
  export's recursion limits. The compiled cold call runs under a recursion limit of 60,
  and `sample_sec.py` sets 10,000. In ascending sweeps the reports run under modelx's
  limit of 40, 10 cells deep on the committed points and 13 on the grid. WholeLife, built
  from M2's tree at the review: 669 cells on a 663-month frame, in 160 to 176 KiB, about
  255 bytes a level; its contract reaches about 1,210 levels. No change after the tests
  stage touched a chain, and as landed the depth test and the runs on a 1 MiB thread and
  on the main thread pass. MSVC's bytes per level come from the first Windows run.

**Faults.** The tests stage injected 20 faults, each failing at least one test, and checked
5 runner faults with the release probe. At the review, two compiled-only faults in the tail,
from the numbers lens, failed C4 at the extremes. Of the tests-docs lens's 23 faults, 7
passed every test (`point_id_by_position`, `cpow_dropped`, `count_chain_two_cells`,
`mort_padding_zero`, `accessor_numpy_int`, `numpy_int_argument` and `sample_no_limit`),
and 8 failed one test alone, among them `runner_ignores_cython`, which the release test
failed and the compiled runner test passed, and `spec_d_68`, which C4 at the extremes
failed. The rules lens's probe of builtins passed C3 and C5. After the fix stage,
each fails, in a copy of its own or on a build: `point_id_by_position` the extract test;
`count_chain_two_cells` the depth test, at 1,446 and 1,854 cells; `mort_padding_zero` and
`premium_padding_zero` the beyond-a-table test; years read by their type the float-key test;
`level_period_unchecked` and `issue_age_unchecked` the contract-refusal test;
`label_derived` C5's label check; `runner_ignores_cython` the runner test's refusal leg;
`cpow_dropped` C4 on the grid at tolerance 0 (240 values) and C3's directive parse; `round`,
a list for `sum` and a dict, C5 and C3, 4 lines each; and an empty parameter set, the
`conftest.py` hook. The re-review's probes: an uncached `premium_taxes` passed every check
but C3 (2 lines); a `-march=native` build failed exact C4 (3 FMA instructions); a point on
plan T5 issued at 18 projected in modelx and raised `IndexError` compiled; text keys gave
`int()`'s message or a wrong extent; and `run_sec.py --cython` at a shallow path raised
`IndexError: 4`. After the second fix stage, each fails, in a copy of its own or on a build:
`level_period_under_a_year` `NOT_ISSUED`'s five-year case alone; `first_year_raw` the
`UNDECODABLE` case of a policy year written as text at the first year; `last_age_raw` the
case of an age that is not whole; `runner_tool_unguarded` the `create()`-copy runner test,
on an `IndexError`; `premium_taxes_uncached` C5 in the default suite, before any compile;
`c5_uncached_unchecked` the harness's static test; and `no_contract_dropped` the toolchain
test's compile-line check. A `-march=native` build with gcc's default contraction fails
exact C4 on the committed points and at the extremes, and with the tool's flag passes. Two
pass by design, `accessor_numpy_int` and `numpy_int_argument`: their numpy integers
compile as `long long` and change no number. `sample_no_limit` passed because the
sample's calls run in ascending `t` and need a limit of 48, below Python's default of
1,000. At the cap's fix stage, each in a copy of its own, on the final cap tests: the cap
removed, an int cap `min(1, ...)`, the cap on the monthly result and the cap on new
business only each fail both cap tests, the last through the rows in force alone; a cap at
0.99, or one on `q` inside `mort_rate_mth`, fails the modelx test, which alone holds the
cap's value, type and place. On the cap stage's tests, the cap's review found the int cap
failing the compiled test alone.

**Carried into Phase 1.** Each item goes to the products in progress, as D2 says, and binds
every product that lands after M14; WholeLife, which landed before it, takes them up in its
own C step. The list is the final one. Where the plan now holds the rule, its number
follows.

*Runner and tests.*
- Index `Projection` only through the key the runner takes from the model, as Term's
  `run_sec.py` does. Copy that runner as it stands, `_tool()` included, with its
  `create()`-copy test, and add the compiled runner test with its refusal leg at the C
  step (R4; §6.1, step 7).
- Freeze, release and collect as F5 says, and sum a block compensated, as Term's `add()`
  does, or as M1's `groupby` does, never by a plain running sum (§6.1, step 7).
- Project a table whose labels are not its positions plus one, and assert the label that
  the runner and a refusal name (R4).
- Pass timings, kinds and phases through the model's References, as the conventions'
  `_timing` does, compare phases with them, and give every `twin_mismatches` call
  `codes=codes(sec_proj)`, `{}` at stage E unless the product brings a code forward, as
  FIA does its phases (precised at M8), through one helper of the module's own (§5.2, T1).
- Bound the cold depth by a test on a fresh read at the longest cover: one cell a month
  back to `t_entry()` plus the product's own fixed overhead, Term's 16, UL's 20, VUL's 25
  and RILA's 24, measured on every committed point and asserted on the deepest among them,
  and no fixed level ceiling (D5, F7; precised at M4 and M10).
- Set every Reference, `Data`'s included, on a model just read and before any call: a
  compiled model clears no cache (K7).
- Each refusal is a `raise ValueError` naming the point, in table-driven lists whose cases
  carry their own inputs; the compiled refusal test is the only guard on raises (§6.2).
- `result_cf()` and `result_pols()` stay on the valuation clock for every point, indexed
  `t = 0 .. rows - 1` with the same row count, pre-issue zeros included: the fingerprint
  reads both (§5.4).
- A point-keyed companion holds its key in a column named `point_id`, and nothing else in
  it names a point, so that a benchmark can renumber table and companions together.

*How cells are written.*
- Every branch of a cell returns the cell's one type, `0.0` or `False` outside cover, and a
  test asserts the types there (F3; §6.1, step 6).
- Every chain is one cell a month (D5), and calls a per-`t` cell for any table value: in
  the design stage's synthetic compile, a chain body that read a `Data` array took 485
  bytes of C stack a level, against 131 without.
- One policy-year- or age-keyed cell reads each table, and no string-keyed join goes into a
  per-`t` cell (R7).
- Cells are called positionally everywhere, and no cell is named like anything a keyword
  call names anywhere in the model (R12).
- Branch on numbers: no projection cell calls a text accessor, and a new switch is a
  number, a bool or an int code (R6, C5).
- No new cell takes a float parameter and none is uncached: a float quantity is computed
  inline in the int-keyed cell that needs it, so that Phase 2 can inline S's (R14).
- Every constant Reference that is not a code is named in lower case (R9).
- No new `Projection` cell returns a list, dict, tuple, array, Series or `None` (R10); a
  vector is a loop in one cell, or built in `Data` from inputs `Data` can see (R2).
- A new per-`t` cell calls only cells, `Data` vectors and `int`, `float`, `bool`, `abs`,
  `min`, `max` and `range`, builds no list, dict or set, and calls no `math`; S's rounding
  and `math` calls stay (R16, C5).
- Every call to a cell keyed by a policy year, a duration or an attained age is guarded by
  `is_active(t)`, and the guard test calls every monthly cell at `t = proj_len()` (F4).
- No new caller of a `kind=None` default (R12).
- `bool(...)` goes around every comparison that can involve a numpy scalar or a `Data`
  element (R11).
- Integer locals and counters compile to C, but one assigned only from int literals is 32
  bits on Windows, so amounts accumulate in floats (F3).
- A power's base is a float expression; no base that can be negative is raised to a
  non-integer power, nor an int to a negative int (F3). A rate S leaves without a bound
  keeps S's power, as `VUL_US_SEC`'s lapse rate does: its base falls below 0 only past a
  rate of 1, where SEC's checks raise as S's do, and return False compiled (§7.6, *E*;
  precised at M4).
- Formulas keep the order S evaluates them in. The build's `cpow=True` and
  `-ffp-contract=off` stay, and no fast-math or FMA-enabling flag is passed after them, so
  C4 is exact on x86-64 and a last-bit difference is a finding (C4, K3).
- Every contract bound a cache size depends on is a lower-case `Projection` Reference that
  `proj_len()` checks, naming the point, with its `NOT_ISSUED` cases (F4; §6.1, step 6).
- An annual mortality rate built as a product of factors is capped with the float 1.0,
  `min(q, 1.0)`, the bound second, never on the monthly rate's result; a `min` or a `max`
  that bounds a value that is always a float may put its bound second too, as Term's
  M(1) rule and PLT floor do, and a lapse rate's bound is such a `min` or `max`, not the
  cap. `Data` refuses, by name, a blank, text or infinite value wherever a cap, a `min` or
  a `max` reads it as a number, and decodes a column such a cell reads only as a key as S
  decodes it. A point where the cap binds is compared with S as new business and restated
  in force the month before the cap, in the splice grid or in a case of its own, as Term's
  is: in every cell, the capped months included, where S caps, as every S model whose
  mortality is such a product does since §8.2 item 4's fix, and otherwise wherever S's
  value is real, the capped rate excepted. Its test asserts the capped rate's type as
  well as its value, and asserts the capped rate on the rows in force too, since where S
  does not cap a cap applied to new business only passes both comparisons; a test sends
  the cap, and each bound put second, a NaN: through a Reference set before the model
  computes anything, which runs compiled, or a replaced formula, which needs modelx (§5.1,
  step 6, precised at M12; §8.2, item 4; changed at Term's cap fix and at §8.2 item 4's
  fix).
- `check_*` cells stay Python, each a `bool` over `*_resid` cells that compile; a label
  accessor stays S's, and no projection cell calls it (R17). A `*_resid(t)` cell SEC adds
  for an S check that is a `math.isclose` loop with no residual cell, as the UL family's
  checks are, returns `float(...)` of its ratio. A rate past 1 makes the monthly rate
  `1 - (1 - q)^(1/12)` complex in modelx, and a complex residual's magnitude is real, so a
  residual left complex would pass its check where S's `math.isclose` raises. Returned as
  a float, it raises as S's does. Compiled, the power is NaN and the check returns False
  (precised at M4). An S model's own `*_resid` cells, the annuities' and WholeLife's, stay
  signed differences with their tolerances (§7.1, *Precised at M3*, item 11), and take no
  `float(...)` where S's check judges a complex residual by its magnitude, as `VA_US_S`'s
  `abs(r) < tol` and `RILA_US_S`'s `abs(r) <= tol` do: a float would raise where S's check
  returns a bool.
- WholeLife's Phase 1 patterns compile without restructuring: at the review 92 of its 106
  `Projection` cells typed as C scalars, and 908,624 values matched modelx bit for bit.

*Inputs.*
- Every new in-force column is a number or an int code, the codes' labels listed in
  `model-sec.md` (R6).
- A numeric key is read by its value everywhere, extents included, 12.0 as 12, and a key
  that is not whole, text among them, is refused by name; tests write keys both ways (R6).
- At Phase 2 one `Data` cell holds each table's check and sizes its array and its extents
  (R7).
- A companion is read by a reader of its own, or through an S reader's `*_file` Reference
  (D8).
- Contract-extreme inputs get a distinct value per added key, never a flat extension.

*Splice grid.*
- In the copies only, a T2 variant for every category of every text column S branches or
  joins on, each key with input rows at a scale of its own (§5.2, T2).
- A row issued more than 12 months after the valuation date, and every policy-year- or
  age-keyed cell listed in `OUTSIDE_COVER` or `IN_COVER_ONLY`.
- A grid sized for what T2 and C4 both need: C4 sweeps every cell of every grid point,
  1,067,350 values on Term's 55.

**The Phase 2 template, carried into M15–M25.** Term's C step is the template, item by
item:
1. *Freeze.* Each product's fingerprint is frozen at M13 into an empty marker block by
   `gen_sec_fingerprint.py`, and committed alone, as Term's was at M14.
2. *Registry.* The entry at `"stage": "EC"` and `"param": "idx"`, its `"reporting"` naming
   S's label accessors; `sample_sec.py` and `spec_sec.py` beside the model.
3. *`Projection`.* Keyed by `idx`, with a Reference `idx = 0`; `point_id()` from
   `Data.point_id`; timings, kinds and phases as int References named as S's strings,
   dense from 0, timings by instant; every other constant Reference in lower case; every
   contract bound a cache size is derived from (the youngest issue age, the shortest term
   a duration cache depends on, the expiry age) a lower-case Reference that `proj_len()`
   checks with the cover check, naming the point; no uncached cell and no float-keyed cell
   (R14).
4. *`Data`.* S's readers unchanged; one int64 or float64 array per input a projection
   formula reads, read by element; decoders element by element, as S reads; keys by value
   in every cell that reads them, and a key that is not whole, text among them, refused by
   name; padding NaN; a shared string-keyed table as `[schedule, key]`, with first- and
   last-key vectors; one checking cell per table, an int its array and extents are sized
   from; refusals at the first read, naming points, schedule or table; companions through
   readers of their own.
5. One reader per padded table, with a two-sided extent check naming the point and the
   key.
6. *Accessors.* `int(...)` or `float(...)` of `data.x()[idx]`; label accessors kept as
   reporting cells nothing calls; booleans as Python bools.
7. *`sample_sec.py`.* The recursion limit from the export's measured need, the reports on
   every committed point, then every cell no report reaches.
8. *`spec_sec.py`.* Every integer-parameter tuple sized from the contract, in the frame and
   in the month after it, with the derivation in a comment naming the References it holds,
   and no size left untaken.
9. *Tests.* C1, changed in call syntax only; C2; C4 on the grid, at the extremes and where
   a cap binds, inputs extended with a distinct value per key; the compiled refusals, on
   a relabelled table, with `NOT_ISSUED`'s cases on their own inputs and text keys;
   `NOT_ISSUED` with a case that projects once its bound is lowered; `UNDECODABLE` with
   text keys, each reached by a projection; the 1 MiB stack and the main thread at the
   longest cover; a modelx depth bound on a fresh read; the compiled runner with its
   refusal leg, and the `create()`-copy runner test; keys written as floats accepted; NaN
   padding; the extract labelled otherwise than by position.
10. *Runner.* Term's `run_sec.py` as it stands: the key from the model, the tool found only
    under `lifelib/libraries/`.
11. *`model-sec.md`.* *The compiled model*: building, what changed, sample and spec, the
    directives and the flag, memory and stack, refusals and domains, the bounds the caches
    hold, and speed with its date, load and versions.
12. *Docstrings.* The *Compiled* paragraph with the cache caveat, the *Codes* and
    *Reporting cells* rubrics, and the `Data` vector table.
13. *C4* exact on x86-64, resting on `cpow=True` and `-ffp-contract=off`: a difference is
    a finding (K3).

**Carried into M15 or later.**
- *Phase 2's start for the other eleven*, left open by the second fix stage, was settled at
  landing: D2 stays as landed, so their Phase 2 starts after M13, and the build stage's
  proposal to start each product's Phase 2 once its own Phase 1 has landed stays
  withdrawn.
- *The q > 1 domain*, left open too, was settled at landing: capped, `min(1.0, q)` then,
  `min(q, 1.0)` since Term's cap fix (§5.1, step 6), Term's at landing (above),
  WholeLife's with `WholeLife_US_S`'s at §8.2 item 4's fix (§7.2, *C*), and the products
  still in Phase 1 in Phase 1, where, since that fix, SEC caps as its S model does.
- R16's `round` for a projected amount, WholeLife's dividend, is flagged by C3 and C5
  today. WholeLife's Phase 2 (M15) adds an admission by cell, such as a registry key
  naming the cells, with a test.
- S's `claims(t, None)`: MYGA's `ALL` code goes through `SecSpec.twin_arg_map`, and
  WholeLife's split exempts S's `claims`.
- R14 at each product's Phase 2: each float engine function inlined, or its float argument
  made an int code or an index. Where S's tests or T1 call the function itself (IUL's
  worked example prices `index_credit_rate` at a 10.00% and a 2.00% cap), SEC keeps S's
  cell, called by no projection cell, through a registry key admitting it by name to C3
  and C5, which the first product to need it adds with a harness test (`"reporting"` will
  not do, since C5 holds each reporting cell to its point's column), or drops it with a T1
  exemption and moves its tests to the inlined form. S's tests call such functions in
  ULSG, MYGA, FIA, VA and RILA too, so in §5.3's order MYGA or ULSG decides first, not
  IUL.
- RILA's 16 `math` calls in its Black–Scholes engine compile as Python calls, and C5
  refuses the module: an admission by cell, or a C form, is decided at RILA's Phase 2.
  MYGA's, FIA's and VA's `floor` and `ceil` become integer arithmetic, and `isclose` goes
  (R12).
- Windows: the `cython` job's first run (below). M14 stays open until it reports.
- `MANIFEST.in` must prune `*_nomx*`, a `setup.py` beside a model and `build/` at the merge
  (K8).
- The in-place `run_sec.py --cython` build was exercised only in copies of the layout
  (1 min 32 s in a copy of the tree, review); no test covers it, as it writes in the tree.
- C4 on the committed points took 3.6 s alone but 13 s after the product module in one
  session (tests stage), and 3.0 to 3.5 s in the `cython` selection since; not
  investigated.
- The release control's failure branch cannot be made to fire from Python (tests stage).
- A future horizon raised past 120 months, `expiry_age` raised, or `issue_age_min` or
  `policy_term_min` lowered still runs a report past the caches in the compiled model
  alone: a bare `IndexError` at the first key past them, where modelx projects. Each is
  documented (`Data`'s and `proj_len()`'s docstrings, `spec_sec.py`, `model-sec.md`), not
  refused, being a Reference a user sets on purpose.
- A level period that outlasts cover, 78 years or more at 18, is not refused, being outside
  the plan menu. No report reads past the caches there, but C4's sweep of the
  parameterless `jump_ratio` reads year n + 1 past the `y` cache; a `policy_term_max` would
  refuse it, should a product need that sweep.
- arm64 and macOS: `exact_here()` stays false there. With `-ffp-contract=off` the compiled
  model may well be exact on them, but the `cython` job has no arm64 or macOS runner, and
  `exact_here()` is widened only when a run shows it.
- A `CL` environment variable adding `/arch:AVX2` to MSVC would make a build whose
  exactness C4's premise does not cover; nothing in the job sets one.
- `tools/fix_doc_roles.py`'s first-model-folder issue, carried from M1, is untouched.

**Windows.** Not yet run. The `cython` job runs only on a pull request to `main` or on a
manual dispatch, and neither has run, so M14's gate is met on Linux only. The risks the
first run tests, and how each is covered:
- MSVC compiling the generated C with both directives: `sec_build` in every compile test
  and the toolchain test. A `BuildError` quotes the log, and a failed build is reported
  once to every test that asks for it.
- The 1 MiB main-thread stack: the test child creates its thread with
  `CreateThread(STACK_SIZE_PARAM_IS_A_RESERVATION)` and reads
  `GetCurrentThreadStackLimits` back, failing above 1 MiB plus 4 KiB. The calls run again
  on the main thread, where `python.exe` reserves 2,000,000 bytes, so the thread is the
  stricter test. MSVC's bytes per level are unmeasured.
- Exact C4 on AMD64, for the reasons C4 gives: the tool passes no flag there, since MSVC
  reads no `CFLAGS`, and Python's float `pow` and the compiled `pow` both call the UCRT's.
  A last-bit difference in the first run is investigated (K3), and `exact_here()` is
  narrowed only if the difference is benign.
- Path lengths: about 163 to 170 characters at most, the `.obj` under the session's build
  and the `.pyd` in a test case.
- A `.pyd` held open: compiled packages are imported in child processes only.
- Line endings: the readers of the `.pxd` and the C use universal newlines.
- `infer_types`: a local assigned only from int literals is a 32-bit C `long`; no Term
  local comes near its range.
- A skip of any compile test fails under `USLIB_REQUIRE_CYTHON=1`, an empty parameter set
  included.
- The toolchain test's compile-line check is skipped on Windows (`os.name == "nt"`), where
  setuptools prints MSVC's command lines, which carry no `-ffp-contract`.
- The `create()`-copy runner test is a modelx test, so the test job runs it on Windows and
  macOS too. It compiles the runner under `/m/products/term_life/run_sec.py`, which
  Windows resolves on the current drive, three parents deep, and globs a folder that does
  not exist, which yields nothing on every platform; it needs no compiler.

**Landing.** Rebased onto bbb99a9 (M2) without a conflict; the two sentences `index.md` had
on the C step, M2's and M14's, merged into one. Then the mortality cap and its two tests
(*Departures and precisions*, above).

**Verified at landing**, on the tree as committed, with the three Phase 1 streams' tests
sharing the machine. The uslib suite, with modelx-cython installed and so the compile
tests included, gave 1,364 passed and 109 skipped in 905.55 s (15 min 05 s). The `cython`
selection gave 11 passed and none skipped under `USLIB_REQUIRE_CYTHON=1`, in 259.12 s:
Term's compile took 142.6 s inside C3's test, and the cap's compile test 1.9 s. doccheck
built 481 pages with 0 warnings. `gen_sec_points.py --check` found `Term_US_SEC`'s and
`WholeLife_US_SEC`'s files current, and `gen_sec_fingerprint.py Term_US_SEC --check`
reproduced the fingerprint. md_lint reported 0, and `gen_scaffolding.py --dry-run` 0
files in each of the six libraries. Before the cap, the rebased tree gave 1,362 passed
and 109 skipped in 907.73 s, and the selection 10 passed in 245.86 s.

**The cap's fix, after landing.** The cap as landed, `min(1.0, q)`, lost a NaN: Python's
`min` and the compiled cell keep their first argument unless a later one compares
smaller, so `min(1.0, nan)` is 1.0. With StdNT's factor blanked in a copy of
`class_factor_table.csv`, `class_factor()` was NaN, `mort_rate(0)` 1.0 and `pols_if(1)`
0.0, every flow finite, where `Term_US_S` projects NaN. The fix follows §5.1, step 6, as
revised, and changes no number: the fingerprint reproduces, the committed table is
current, and C4 is exact on the grid, at the extremes and where the cap binds.
- *The order.* `mort_rate` returns `min(q, 1.0)`, the product computed first, as before.
  The notes' M(1) rule and the PLT grading put their bounds second too, `min(…, 8.0)` and
  `max(…, 2.0)`, where a NaN jump ratio and a NaN M(1) had given 8.0 and 2.0;
  `t_entry()`'s `max(0, …)` takes ints alone and stays. The generated C tests
  `bound < value`, or `>`, and keeps the value otherwise, so a NaN stays NaN compiled.
- *The refusals*, when the array is first read, over the whole column, naming the file,
  the column and every line or point at fault, a premium by every schedule at fault and
  every policy year in it: a class factor, a base rate, a premium, an `age_at_entry` and
  an M(1) override that is blank, text or infinite, a blank override excepted, the
  notes' rule. Before, a blank rate or premium was refused by its table's message,
  naming neither column nor age or year; a text factor, rate or premium raised numpy's
  error and a text age `int`'s, naming nothing, a text override being refused by name
  already; a blank factor, and a +∞ factor, rate or override, passed, the cap reading
  each as certain death, and a −∞ override passed, the grading's `max` reading it as
  2.0; an infinite premium passed, and an infinite jump ratio was read by the M(1) rule
  as 8; a blank or infinite age became the least int64, which modelx's `proj_len()`
  refused as an issue age below 18. The schedule's and the mortality table's messages
  drop their value clauses.
- *Left, with reasons:* the shock-lapse table, which no cap, `min` or `max` reads, where
  a blank bound skips its bucket in `shock_lapse_rate`'s comparison and an infinite
  bound is a legitimate open bucket; `sum_assured`, which reaches the cap only as a band,
  a blank face in band 4 as in `Term_US_S` (`DECODED`), its number read by `claims`
  alone; the padding and a blank override, legitimately absent.
- *Tests:* `NOT_FINITE`, 22 cases beside `UNDECODABLE`, 3 of them moved from it, each on
  its own inputs, refused by its rule alone, by a projection and compiled: each column
  blank, as text and infinite, the override's −∞ too and its blank excepted; a factor
  and a premium no point reads; and two lines at fault in each column, and two
  schedules. `test_a_nan_that_reaches_a_bound_stays_nan`, 3 cases, sends each bound a
  NaN through a replaced formula (K7). The module has 128 tests, 121 modelx and 7
  compile. 24 faults, each alone in a copy, each failed some test: the three bounds put
  first again; each refusal dropped; each refusal accepting an infinity, the override's
  −∞ too; the override refusing a blank, the rate check reading the padding, the factor
  check refusing a factor above 1; the factor and the premium checks reading only what
  points carry; the factor, rate, premium and age refusals each naming its first line
  alone, and the premium refusal its first schedule alone; and a guard turning the M(1)
  rule's NaN into 8. Five of them, the premium check reading only the schedules points
  carry and the four naming the first line alone, passed every test until the fix's
  review asked for the cases of a premium no point reads and of two lines in each
  column, and the premium refusal, which then named the first schedule at fault alone,
  came to name every one.
- *Verified* under load. At the fix's last stage, on M11's tip: the module, 128 passed in
  223 s; the conventions on `Term_US_SEC`, 37 passed and 1 skipped; the uslib suite,
  1,557 passed and 163 skipped in 1,044 s (17 min 24 s). At landing, rebased onto M7's
  tip without a conflict, under `USLIB_REQUIRE_CYTHON=1`: the uslib suite, 1,746 passed
  and 231 skipped in 1,297.94 s (21 min 38 s); the `cython` selection, 11 passed and none
  skipped, in 182.06 s; doccheck 489 pages and 0 warnings; md_lint 0; the generated files
  of the four SEC models current; Term's fingerprint reproduced; and
  `gen_scaffolding.py --dry-run` 0 files in each of the six libraries.
- *Carried:* `SPIA_US_SEC`, landed before the fix, caps `q_be` and `q_rated` with the
  bound first, as `SPIA_US_S`, `DIA_US_S`, `FIA_US_S` and `ULSG_US_S` do (§8.2, item 4).
  *Fixed on 2026-11-03 (§8.2, item 4): each of these caps now puts its bound second.*

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
  - cash values (period, sex, age, y) to `[schedule, policy_year]`, with a per-point
    schedule number (R7);
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
- `Data`'s refusal, by name, of a blank, text or infinite value wherever the capped
  mortality rate reads it as a number (§5.1, step 6; decided at M14's landing, the order
  and the refusals at Term's cap fix). The cap itself, `min(q, 1.0)`, came into
  `WholeLife_US_SEC` with `WholeLife_US_S`'s at §8.2 item 4's fix, with its cap and NaN
  tests.

#### Record — M2, done 2026-11-01

Built in two commits, as D1 requires: `WholeLife_US_S` copied with only `_name` changed,
then the enhancement, by M1's process: a design prototyped and critiqued before the build,
tests written against the build and checked by injected faults, then a review under the
three lenses. The review found 22 defects, 5 of them major, and a re-review of the fixes
found one more, in the R2 text the fixes had added to this plan. All 23 are fixed. Those
that `WholeLife_US_S` shares are fixed in `WholeLife_US_SEC` only, and carried below.

**What exists now.**
- `WholeLife_US_SEC` at stage `E`. Of `WholeLife_US_S`'s 97 `Projection` cells, 40 are
  unchanged, 9 have a new docstring only, 44 are rewritten, 2 are renamed and 2 removed.
  It adds 11: `policy_count`, `duration_mth_init`, `t_entry`, `is_active`, `maturity_mth`,
  `pols_new_biz` and five opening-state accessors, 106 cells in all. `Data` keeps S's
  seven cells, adds `future_horizon_mth = 120`, and checks its own table as it reads it.
- `model_point_table_sec.csv`, 22 rows generated from WholeLife's `SecSpec`:
  - S's 15 points as twins, S's in-force point 1 among them at its month 108;
  - six derived rows: ACCUM (S point 4) and REDUCE_PREM (5) on the anniversary at month
    108, the funded term blend (8) at 78, the loan variant (6) at 114, graded final
    expense (12) at 18, and REDUCE_PREM in its last covered month, 659;
  - S point 2 issued 3 months after the valuation date.
  A case-insensitive search for every publisher, product, form number and host that
  `whole_life/sources.md` cites finds none of them in it.
- `tests/test_whole_life_us_sec.py`, 27 tests and 208 cases: T2 on 105 splices, the
  in-force twin among them, T3 on 31 future points, T4, T5 on 47 malformed rows and its
  edges, T6, the rules test, and the product's own facts. By default a core of 32 splices
  and 8 future points runs, and a test asserts that the core reaches every branch the full
  grid does; the other cases carry `sec_full` (K6). The SEC conventions pass on the model.
- `run_sec.py`; `model-sec.md`, with a section of its own, *The opening state*; the
  registry entry with its `INPUT_FILES`; and four generated pages. doccheck reports 481
  pages and 0 warnings.
- Shared files, added to in place: WholeLife's spec and its state extractors in
  `sec_support.py`; the `sec_full` marker in `conftest.py`; the entry in `us_registry.py`;
  the models table and the SEC sentences of uslib's `index.md`; and one leg of
  `.github/workflows/tests.yml` that sets `USLIB_SEC_FULL=1`.

**Departures and precisions.**
- *The opening state* is seven columns, three of them at a second instant that D6 now
  names (precised in place):
  - the paid-up additions, the loan and the accumulation balance entering month 0,
    `pua_face_init`, `loan_bal_init` and `div_accum_init`;
  - the additions and the loan at the anniversary on or before the valuation date,
    `pua_face_prev_anniv_init` and `loan_bal_prev_anniv_init`, which the year's dividend,
    term-blend gap and loan interest read, and the dividend credited there,
    `div_prev_anniv_init`, which this section calls `div_prev_init`;
  - the gross premium paid before the valuation date, `prem_cum_init`.
  D6's `<cell>_prev_anniv_init` renames VA's and RILA's year-opening columns too (§7.7,
  §7.8). `SecSpec.state` reads each column off S as S's own formulas read it. A balance
  entering month `d` is the close of month `d - 1`, or S's opening value where month `d`
  opens S's frame, and a balance at the year's opening anniversary is read the same way
  at the month whose close opened the year.
- *Two S cells are removed, and two renamed.* `proj_start()` goes, because every SEC frame
  opens at `t = 0` (D3), so the reports and checks run over `range(proj_len())`, as
  Term's do. `duration_inforce()` goes, replaced by `duration_mth` (D6). `puaf_inforce`
  and `loan_inforce` become `pua_face_init` and `loan_bal_init`, so that the seven
  accessors share one vocabulary. T1 exempts all four, and `result_pols`, each with its
  reason in the spec.
- *Twelve sites rebased* (R1, R1a): §7.2's seven, and five more found by reading every cell:
  `prem_cum` bases at `t_entry()` on `prem_cum_init`; `premium_pp_ann`, `cv_pp` and
  `pua_cv` test `is_active(t)`, not `t < 0`; the maturity tests in `div_to_pua`,
  `claim_pp`, `pols_maturity` and `pols_if_at` move to the policy clock, though still
  correct on the valuation clock; the nine cells that S guards by its frame,
  `t < proj_start() or t >= proj_len()`, are guarded by cover; and
  `check_pols_roll_fwd_resid` reads the next month's `BEF_NB`. Of §7.2's own,
  `pua_face_rider`'s `nsp_mth(t - 1)` is inlined, the same arithmetic bit for bit, so
  that a mid-year valuation reads no month `-1`.
- *Reads at the last anniversary.* A balance as it stood at the anniversary that opened
  the year (`pua_face`, `loan_bal`, `div_credited`) is read at `anniv_mth(t) - 12`, or from
  its `_prev_anniv_init` column where that month is before `t_entry()`. A schedule stays a
  policy-year cell: `div_int` reads `cv_pp_anniv(duration(t))`, and is 0 off the
  anniversary, where S's gives a value that nothing reads.
- *One read 11 months ahead* (R2, precised in place). The term-blend layer `oyt_face(t)`
  reads the dividend at the anniversary that closes its policy year,
  `div_credited(anniv_mth(t))`, because the layer in force through a year is bought with
  that year's dividend. The rules test admits that read alone, by reader, cell and month,
  inside the frame. The re-review corrected R2's condition: the quantity read may depend on
  what the reader held in earlier years, as WholeLife's does through the additions
  entering the year.
- *Acquisition* is per policy issued, as M1 made it. S already weights its acquisition by
  the count issued, so T1 holds at any count, and M1's one-policy caveat does not apply.
- *`result_pols`* exists in S. SEC's keeps the template's columns, with `pols_new_biz`
  second, then S's four decrement rates, written 0 outside cover. T1 exempts the report,
  and the module compares it with S's, column by column.
- *Data's checks.* Six of the product's follow the template's five:
  - each opening-state column is a number, zero or more;
  - a point not yet in force has no opening state;
  - final expense has no additions and no dividend;
  - only the ACCUM option has an accumulation balance;
  - on an anniversary valuation the year-opening columns equal the entering ones;
  - in the first policy year they, and `div_accum_init`, hold their issue values, 0.
  A row whose additions at the anniversary exceed those entering month 0 is accepted, as a
  partial surrender the model does not implement, and a test pins that.
- *The splice* (§5.2). `SPLICED_REFS` also switches on `pua_div_on`, `prem_offset_on` and
  `dyn_lapse_on`, with `competitor_rate` 0.08. It sets `int_rate_loan` to 0.08, apart from
  the dividend rate, so that direct recognition, zero at S's shipped rates, shows, and
  inflation to 0. T2 and T3 also exempt `anniv_mth`, a month on the valuation clock. Three
  variants are spliced: the PUA rider paid monthly, REDUCE_PREM semi-annually and the graded
  plan quarterly. This section's "one mid-year month" became 115 and 119, so the months
  are:
  - 12, 108, 115, 119, 120 and 600 for the participating points;
  - 12, 18, 23, 24, 115 and 400 for final expense;
  - 78 and 83 as well for the funded blend;
  - the last covered month for ACCUM, REDUCE_PREM and level final expense.
  Future business is issued 1 and 12 months on.
- *The K6 remedy* (K6, *M2*): the core grid by default, the rest behind `sec_full`, and
  one CI leg that runs it. The design left the leg to M3; the review asked for it now.
- *`model-sec.md`*'s new section shows each opening-state column on a derived row, with
  what the row gives when the column is zeroed: REDUCE_PREM then collects 1,800.00 instead
  of 1,511.34, and the ACCUM point's maturity claims fall 1,060.82 short.

**Measured for K6 and F7.** Every time below was taken with other workflows' builds and
tests sharing the machine.
- *Time.* By default the module ran 111 passed and 97 skipped in 2 min 46 s to 3 min 01 s
  over three runs, and over its full grid 208 passed in 4 min 57 s and 4 min 59 s. Its peak
  is 2.7 GB in one process, because each splice row is released once compared; before
  that change it was 5.4 GB. Beyond the splices, four tests take about 96 s together: the
  count doubling, the extract, the clock test's fresh read and `run_sec.py`'s
  subprocesses. The uslib suite went from 1,154 passed and 12 skipped in 5 min 54 s (M1)
  to 1,298 passed and 109 skipped in 9 min 02 s to 9 min 18 s over four runs, the last
  on the tree as it landed.
- *Depth.* A cold `net_cf` of the last month runs 669 cells deep on a 660-month frame,
  against 3,304 in `WholeLife_US_S`, and 669 too on the 780-month frame of a point issued
  120 months on, because every chain starts at `t_entry()`. An ascending sweep reaches 29
  cells, on graded final expense, and runs under a recursion limit of 28, as S's reports
  do; `CALL_DEPTH` is 60. In the modelx export the cold call needs a recursion limit of
  1,361, or 1,145 on the in-force twin, and the ascending sweep 128.

**Faults.** The tests stage injected 67 faults and the review 74, each alone into its own
copy of the library. Ten of the review's survived the default grid. After the fixes, the
fix stage ran 86 faults, those ten among them, and all 86 fail the default run; the
re-review re-ran the ten and two more, and all fail. A control that changes no value, the
`BEF_DECR` count formed by a second cell, passes.

**Carried into M3 and after: the template.** M1's fourteen items stand, with these
changes:
- Item 6 gains the year-opening read: a balance at the last anniversary is read at
  `anniv_mth(t) - 12`, or from its `<cell>_prev_anniv_init` column before `t_entry()`
  (D6). A read at `anniv_mth(t)` itself is allowed only as R2 now says, and the rules test
  admits it by name.
- Item 7: where S already charges acquisition per policy issued, T1 holds at any count.
- Item 9: the product's state checks follow the template's five. The year-opening columns
  equal the entering ones on an anniversary, and hold their issue values in the first
  policy year.
- Item 11 gains the K6 pattern and its memory rule:
  - a core grid runs by default, and a test asserts that it reaches every branch,
    opening-state column, kind of valuation month and premium mode the full grid reaches;
  - the other cases carry `sec_full` and skip, with the reason, unless `USLIB_SEC_FULL=1`,
    which the CI leg sets; `SEC_FULL`, `FULL_ONLY` and `_case` in
    `test_whole_life_us_sec.py` are the code to copy;
  - each splice row is released once compared.
- Item 13: `model-sec.md` gains *The opening state* wherever the state is more than the
  count.
- S cells that the valuation clock makes redundant, such as `proj_start` and
  `duration_inforce`, are removed and exempted from T1 with their reasons, and an S column
  that becomes an opening-state accessor takes D6's name.

**Carried into Phase 2.**
- `spec_sec.py` sizes `t` from the contract. Level pay issues from age 0 (product-spec),
  so the longest frame is 12 × 100 + 120 = 1,320 months, plus one month for the `t + 1`
  read. The shipped mortality and NSP tables start at age 18, so they price frames of at
  most 1,104 months. The anniversary read stays inside the frame and needs no cache beyond
  it.
- The C note above that a test calls `cv_pp_anniv(-1)` is about S's tests. SEC calls it
  at no negative year (R1): on the committed points its keys run from 0 to 55, and those
  of `nsp` from 45 to 100, so the shared `('y',)` cache starts at 0.
- The cells meant to run only in cover (`IN_COVER_ONLY`) have no guard of their own. No
  formula reaches them outside cover, and a caller must not either (F4).
- The depths above size `sample_sec.py`, `run_sec.py --cython` and the Windows job's
  stack.
- M14's critique read this model for Phase 2: `run_sec.py` indexes `Projection` by label
  at five sites, and the test module passes 25 timing and kind strings literally. Both
  change in WholeLife's own C step (D2); the products after M2 write them for both stages
  from the start.

**Carried, outside the SEC models.** Three S-side items for §8.2 item 4, all in
`WholeLife_US_S`'s `Projection` docstrings and fixed in `WholeLife_US_SEC` only:
- `claim_pp`'s three kinds render as a broken definition list;
- three lines exceed 92 characters, the summaries of `mort_rate_guar_at` and `mort_rate`
  and `dyn_lapse_factor`'s return;
- "this cells", in `oyt_face` and in `pols_if`.

### 7.3 Universal life — `UL_US_SEC` (E: S, C: M)

*Today:* already on the projection clock, with `duration_mth_init()` and `av_pp_init` /
`loan_bal_init`, and point 3 is in force at `d = 120`. Re-opening point 1 at `d = 120` and
`125` reproduces S to 3e-13, except for the accumulators below. A negative duration fails
(`KeyError` on policy year 0). `pols_if_at` exists but returns `pols_if` for every timing,
and nothing calls it.

*E:*
- Opening state (D6): S's `av_pp_init` and `loan_bal_init`, unrenamed, and four new
  columns:
  - `sum_assured_init`, the face in force; the face at issue stays the surrender-charge
    base, and `Data` refuses a face above it, or of 0 in force;
  - `wd_used_year_init`, which S forces to 0 at `t = 0`, and which is 0 on an anniversary
    valuation;
  - `cum_prem_init`, which S restarts at 0 in force although the TARGET premium cap reads
    it, of either sign;
  - `is_mec_init`, an int code, because the latch's base is `t > 0`.

  Reading every recursive cell found no other state. `Data` refuses a negative account
  value, so a point in permanent shortfall is restated no later than the last month its
  account value is still zero or more: without a loan, the month its shortfall begins (S
  point 2 at 676).
- Every chain is one cell a month (D5): `av_pp_at(t, "BEF_PREM")` and `loan_bal_pp_bom(t)`
  form the previous month's close themselves, S's arithmetic in S's order, where S's
  chains run through five cells a month and two. `is_mec` runs its in-year test before its
  base, as S's does.
- Rebase (R1a): eight bases move from `t == 0` to `t_entry()`, those of `av_pp_at`,
  `loan_bal_pp_bom`, `sum_assured_at`, `wd_used_year`, `cum_prem_pp`, the TARGET cap in
  `premium_pp`, `is_mec` and the count.
- Guards (R1) cover every per-`t` cell that turns `t` into a policy year or an age, and
  every per-policy flow and charge. `lapse_rate_sc_mult` is guarded because S's
  no-schedule sentinel, shock year 0, is the policy year of the twelve months before
  issue.
- The frame ends at a horizon, `omega_mth()`, the first policy month at attained age 121,
  not at an event: the count and the account value carried into `t = proj_len()` are kept,
  and every other count, balance, flow and charge is zero there (§7.1, *Precised at M3*).
- Tables: each policy-year or age table has one keyed reader, which takes its extent from
  a `Data` cell that reads the key column by value once and checks the table before any
  value is read; the COI scale's extent is per issue-age cell, read per point. A key that
  is blank, text or not whole is refused, naming the file, the column and its lines. So
  are keys that do not run one row a year or an age, without a gap or a repeat, policy
  years from 1, naming each key that repeats, with its lines, and each missing key or
  span; and a value that is blank, text or infinite, naming the column and its lines.
  `class_count()` and `surr_charge_count()` check the two tables read by point, and
  `class_factor()` and the schedule's two readers ask them first. `UL_US_S` reads a blank
  as a missing value, which its own `min` and `max` lose without a word: a blank lapse
  rate reads as the cap of 0.35, a blank corridor factor as no corridor, a blank surrender
  charge as none.
- Text: six bool decodes carry every branch on S's text columns, and a value none of them
  knows raises S's message in the cell that branches, as in S. Only the decodes and five
  per-point joins, `coi_rate_scale`, `coi_rate_last_year`, `class_factor`,
  `surr_charge_rate_max` and `surr_charge_runoff_years`, call S's label accessors, a
  departure from M14's carried rule (*Record — M3*); no monthly cell does.
- `crediting_rate_ann` and `comp_rate_ann` are read on `t`, the valuation clock (D7), as
  `UL_US_S` reads them on its projection clock. They are flat as shipped, so a test moves
  them by formula override; on those paths the account value's close, both checks and the
  twins' match with S hold. Expense inflation keeps S's annual steps, on `t`,
  `(1 + i) ** (t // 12)`.
- `mort_rate` is capped at 1.0, `min(q, 1.0)` (§5.1, step 6): at the shipped A/E, the
  tobacco classes' product passes 1 from attained age 113 (StdTob) and 114 (PTob), where
  `UL_US_S` turned complex before §8.2 item 4's fix and caps since. The cap test follows
  Term's.
- `pols_if_at`'s `"BEF_MAT"` keeps S's meaning, the `"BEF_DECR"` count, and T3 compares
  the cell with S's stub at every key but `"BEF_NB"` in the issue month (D5, precised at
  M3).
- `check_margin`'s loan term is the loan a surrender recovers,
  `min(loan_bal_pp(t), csv_pp(t)) * pols_lapse(t)`: with S's whole loan the check fails
  once a loan exceeds the cash value.
- `expenses` is S's formula in S's order, behind the guard.
- Splice months, by event:
  - on S points 1 and 2: 1, 11, 12 and 13; 107, the first month without a surrender
    charge; the lapse shock's year at 108, 113 and 119, and 120, where it ends; and 125;
  - point 1's last covered month, 1031, a one-row frame whose `t = 1` is the month carried
    into, and 779 and 780, either side of the splice's charges ceasing at age 100; point
    2's 676, where its shortfall begins;
  - S point 3 at 1, 6 and 12 after its own month 120, and as its own twin at offset 0;
  - seven variants, each with COI rows of its own: withdrawals on A (12, 13, 15, 23, 24);
    withdrawals on B (13, 24); a single premium without a surrender charge (1, 12, 85);
    TARGET on a second schedule, UL7 (70, 71, 72, 83, 84, 144); over-funded LEVEL (1, 3,
    11, 84; at 3 the 7-pay test first fails in the valuation month); issue age 18 (12,
    1235); and LEVEL at $24,000 a year on B, whose corridor binds (33, 34, 479, 480).

  Future rows are issued 1 and 12 months on, and the variants 13 months on. The core is 20
  splices and 5 future rows, the full grid 54, the in-force twin among them, and 11.
- The splice's References, in both models: inflation 0, acquisition $250, A/E 0.56,
  charges ceasing at attained age 100, and a lapse shock of 10 times, so that the shock
  year's 0.04 meets the lapse rate's cap of 0.35.

*C:*
- `model_point()` sits behind 23 accessor cells, each read once a point. Six of the
  columns are text: three decoded into bools at stage `E`, and `sex`, `rate_class` and
  `surr_charge_id`, the per-point joins' keys.
- The keyed readers `prem_persistency_py`, `coi_rate_guar_py`, `lapse_rate_base_py`,
  `corridor_factor_at` and `mort_rate_base_at` are the arrays' one reader each, and
  already take their extents from `Data` cells that check each table's keys and values.
  `coi_rate_scale`, `coi_rate_last_year`, `class_factor`, `surr_charge_rate_max` and
  `surr_charge_runoff_years` are per-point joins keyed by text, and the six bool decodes
  read text columns. `Data` decodes them all (R6, R7): the extents become int scalars or
  vectors by point, `coi_rate_last_years`, a Series at stage `E`, among them; the COI
  scale becomes `coi[schedule, y]` with a per-point schedule number; and `class_count`'s
  and `surr_charge_count`'s checks move into the class factor's and the schedule's vectors
  by point, which refuse a blank value as they do now.
- Timing and kind cells: `av_pp_at`, `av_at` (+`EOM`), `pols_if_at`, `claim_pp`,
  `claims_from_av`, and `claims(t, kind=None)`, which S's `net_cf` caches under
  `(t, None)`, so T1 needs an `arg_map` for it at stage `EC` (R12).
- No report or check reaches, on the committed points, `gsp`, `glp`, `seven_pay_prem`,
  `wd_used_year`, `wd_free_pp`, `is_shortfall`, `cure_premium_pp`, `cum_prem_pp`,
  `gpt_limit`, `gpt_ok`, `seven_pay_limit` or `is_mec`, as in S, nor four new cells:
  `is_target_premium`, which no committed point's premium asks, and the opening-state
  accessors `wd_used_year_init`, `cum_prem_init` and `is_mec_init`; `sample_sec.py` must
  call each. `pols_if_at`, which S never reached, now carries the count.
- `t` runs from 0 to 1,356 at the contractual maximum, issue age 18 with 1,236 months of
  cover, issued 120 months on, and the month after the frame, so `spec_sec.py` sizes `t`
  at 1,358. Policy years run 1 to 103 and attained ages 18 to 120, each read only in
  cover. Phase 2's `proj_len()` refuses an issue age below 18, the youngest
  `product-spec.md` admits; at stage `E` UL's `SecSpec` comment in `sec_support.py` lists
  the bound, and nothing refuses it.
- Depth (F7): a cold `net_cf` runs one cell a month back to `t_entry()` and 16 more, 1,251
  cells at the longest cover, and needs 2,529 Python frames in the modelx export. At gcc's
  255 bytes a level, 1,251 levels are about 311 KiB.
- Two product tests override formulas, the declared-rates test and the NaN-residual test,
  so they stay on modelx (C1); the splice sets References only, and its variants are S's
  columns.

#### Record — M3, done 2026-11-02

Built in two commits, as D1 requires: `UL_US_S` copied with only `_name` changed, then the
enhancement, by M1's process: a design prototyped and critiqued before the build, tests
written against the build and checked by injected faults, then a review under the three
lenses. The review made 28 findings, 1 a blocker and 5 major, some of them one defect seen
under two lenses. The blocker and one major were the cap test, which a cap on new business
only and an int cap both passed. Two more were the assumption tables' extents, taken from
the key column as pandas reads it, so that a blank last key cut a table short without a
word. The other two were gaps in the tests: nothing pinned the month whose credited rate
the account value's close reads, and nothing showed a residual that is not a number
failing a check. A re-review of the fixes made 5 more, all minor, among them a blank rate
that the cap read as 1.0. All are fixed in `UL_US_SEC` and its tests but one, which asked
the plan to let the decodes and per-point joins call S's label accessors at stage `E`; the
record states that as a departure from M14's carried rule instead (*Departures and
precisions*, *Text*). The fixes rejected only what reached outside `UL_US_SEC`: the S
halves of three findings, since `UL_US_S` is left untouched and its defects are carried
below, and a relative float comparison in T6, which would change the shared harness for
every product; the second fix rejected nothing. M3 was built on M2's tip and rebased at
landing onto Term's cap fix, which followed M7 (*Landing*, below).

**What exists now.**
- `UL_US_SEC` at stage `E`. Of `UL_US_S`'s 107 `Projection` cells, 44 are unchanged, one
  more has a line rewrapped, 26 have a new docstring only and 36 are rewritten; none is
  removed or renamed. It adds 26 cells, 133 in all: `policy_count`, `omega_mth`,
  `t_entry`, `is_active` and `pols_new_biz`; four opening-state accessors,
  `sum_assured_init`, `wd_used_year_init`, `cum_prem_init` and `is_mec_init`, and
  `wd_pp_mth`; six bool decodes; five keyed readers, `prem_persistency_py`,
  `coi_rate_guar_py`, `lapse_rate_base_py`, `corridor_factor_at` and `mort_rate_base_at`,
  and `coi_rate_last_year`, a point's COI extent; the schedule's two readers,
  `surr_charge_rate_max` and `surr_charge_runoff_years`; and the residual cells
  `check_av_roll_fwd_resid` and `check_margin_resid`. S's `math` Reference is dropped.
  `Data` rewrites S's table reader, which now checks the table as it reads it, keeps S's
  other eight cells, six of them rewrapped and two of those with a shortened docstring
  line, and adds nine, 18 in all: seven that check a keyed table and give its extent, and
  `class_count` and `surr_charge_count`, which check the two tables read by point. It adds
  the Reference `future_horizon_mth = 120`.
- `model_point_table_sec.csv` holds nine rows generated from UL's `SecSpec`. Three are S's
  points as twins, point 3 in force at its own month 120, at offset 0. Five are derived: S
  point 1 at months 12, 113 and 1008, S point 3 six months on, and S point 2 at 676, the
  month its shortfall begins. The last is S point 1 issued 25 months on. The table has no
  `provenance` column. A case-insensitive search for the publishers, products, form
  numbers and hosts that `universal_life/sources.md` cites finds none of them in it.
- `tests/test_universal_life_us_sec.py` has 34 tests and 200 cases: T2 on 54 splices, the
  in-force twin among them; T3 on 11 future rows; T4; T5 on 50 malformed rows, 33
  malformed keys, 15 values that are not numbers and 4 blank or repeated text keys, 3
  values no decode knows, 2 points past cover, the horizon and the accepted edges; T6, and
  the committed rows against S; the rules, depth and guard tests; and the product's own
  facts. By default a core of 20 splices and 5 future rows runs, 159 cases in all, and a
  test asserts that the core reaches every branch, opening-state column and kind of
  valuation month the full grid reaches. The other 41 carry `sec_full` (K6). On M2's tip
  the SEC conventions pass, 32 of them, and one is skipped, as it is for `UL_US_S`.
- `run_sec.py`, which prints a point's account value roll-forward beside its cash flows;
  `model-sec.md`, with *The opening state*, which shows each new column on a splice
  variant beside the same row with the column as `UL_US_S` assumes it: 388.15 of TARGET
  premium against 450.00, the MEC latch on against off, a free amount of 82.39 against
  142.39, and a death benefit of 99,442.27 against 100,000.00; the registry entry with its
  `INPUT_FILES`; and four generated pages. doccheck reported 485 pages and 0 warnings on
  M2's tip with UL added.
- Shared files, added to in place: UL's spec and its state extractors in `sec_support.py`;
  the entry in `us_registry.py`; and the models table's Universal life row and the
  sentence on the SEC models in uslib's `index.md`.

**Departures and precisions.**
- *The opening state* (D6, precised). S's `av_pp_init` and `loan_bal_init` keep their
  names, since they already measure D6's instant, and four columns are new. `Data` refuses
  a negative account value and a face of 0 in force, and accepts a negative
  `cum_prem_init`, a tax measure rather than a balance. So a point in permanent shortfall
  is restated no later than the last month its account value is still zero or more:
  without a loan, the month its shortfall begins, as committed point 7 is.
- *Chains of one cell a month* (D5). `av_pp_at(t, "BEF_PREM")` and `loan_bal_pp_bom(t)`
  form the previous month's close themselves, S's arithmetic in S's order, where
  `UL_US_S`'s chains run through five cells a month and two. `is_mec` runs its in-year
  test before its base, as S's does, so a point that fails the 7-pay test at `t = 0` is a
  MEC whatever `is_mec_init` says.
- *Eight bases at `t_entry()`* (R1a): those of `av_pp_at`, `loan_bal_pp_bom`,
  `sum_assured_at`, `wd_used_year`, `cum_prem_pp`, `premium_pp`'s TARGET cap, `is_mec` and
  the count, which S bases at `t == 0`. No cell passes a policy month as `t`.
- *Guards* (R1). Every per-`t` cell that turns `t` into a policy year or an age is guarded
  by `is_active(t)`, and so is every per-policy flow and charge, `wd_pp` among them,
  rather than left to a contractual age to reach zero. So is `lapse_rate_sc_mult`: without
  a schedule S's `lapse_shock_year()` is 0, the policy year of the twelve months before
  issue, where the multiplier was 2.0.
- *The frame's end* (§7.1, item 5, precised). The frame ends at a horizon, `omega_mth()`,
  the first policy month at attained age 121. The count and the account value are carried
  into `t = proj_len()`, because S's roll-forwards read them there and survivors remain.
  Every other count, balance, flow and charge is zero there, `av_change` and both residual
  cells included, so no cell reads past `proj_len()`. At the splice's A/E of 0.56, 4.0e-6
  of a policy survives to the end on points 1 and 2, and 9.3e-6 on point 3.
- *The tables* (§7.1, item 9, precised). The five keyed readers take their extents from
  seven `Data` cells, `prem_persistency_last_year`, `lapse_last_year`,
  `corridor_age_first`, `corridor_age_last`, `mort_age_first`, `mort_age_last` and
  `coi_rate_last_years`, which `coi_rate_last_year` reads per point; `class_count()` and
  `surr_charge_count()` check the two tables read by point. Each reader asks its cell
  before it reads a value, so a projection meets the checks first. A message names each
  key that repeats, with its lines, and each missing key or span, so it stays short on
  `mort_table.csv`'s 103 rows; in the COI scale each clause names its issue-age cell.
- *Text.* Six bool decodes, `is_db_option_a`, `is_db_option_b`, `is_gpt`,
  `is_level_premium`, `is_single_premium` and `is_target_premium`, carry every branch on
  S's text columns, and a value none of them knows raises S's message in the cell that
  branches, as in S. The six decodes and the five per-point joins keyed by text call S's
  label accessors, where M14's carried rule has no projection cell call one. No monthly
  cell calls one, and R6 and R7 move both onto `Data` in Phase 2. The products after UL
  keep M14's rule, as SPIA and MYGA do (the life chassis, *Text*, below).
- *The checks* run over relative `*_resid(t)` cells, which keep S's `isclose` tolerance.
  Each check fails a residual that is not a number, as `math.isclose` does, and the `math`
  Reference is dropped.
- *The cap on mortality* (§5.1, step 6). `mort_rate` is `min(q, 1.0)`, which keeps a NaN
  as NaN in both engines; the build wrote `min(1.0, q)`, and the landing changed it
  (*Landing*). The cap changes S's annual rate where it passes 1, and no monthly rate,
  count or flow that S computes as a real number. Its test, on Term's form, takes S's
  anchor cell in StdTob at the shipped A/E, whose rate first passes 1 at `t = 936`,
  attained age 113, at 1.095. It reads four rows: the twin, the point issued 25 months on,
  and the point restated at 935 with S's count and at 941 with one policy. The first three
  are compared with S wherever S's value is real, at 1e-9 relative with no absolute floor.
  On all four the capped rate is `(float, 1.0)`, every policy in force there dies in that
  month, the reports are finite float64 and both checks hold.
- *`check_margin`*'s loan term is the loan a surrender recovers,
  `min(loan_bal_pp(t), csv_pp(t)) * pols_lapse(t)`. With `UL_US_S`'s whole loan the check
  fails once a loan exceeds the cash value, since the lapse claim is floored at 0. A test
  restates S point 3 withdrawing on Option B the month before its loan passes its cash
  value: its reports equal S's, S's check fails and this model's holds.
- *`pols_if_at`* (D5, precised). `"BEF_MAT"` keeps S's meaning, the `"BEF_DECR"` count, as
  WholeLife's keeps its S model's, and `"BEF_NB"` alone takes a new one. T3 compares the
  cell through an `arg_map`, `_issued_later`, which leaves out S's
  `pols_if_at(0, "BEF_NB")` alone.
- *Expenses.* `expenses` is S's formula in S's order, behind the guard. S charges
  acquisition on the count in force in the issue month, the policies issued, so T1 holds
  at any count; a test checks it bit for bit against S at counts 3.7 times the table's.
  Inflation keeps S's annual steps, on `t`. The declared rates are read on `t`, and a test
  moves them by formula override.
- *The committed table* has S point 1 at 1008, the first month at attained age 119, in
  place of template item 10's last covered month, 1031: at the shipped A/E the table's
  rate of 1.0 at 119 ends every policy in force, and no policy reaches 1031. The splice
  restates 1031 at its A/E of 0.56.
- *`result_pols`* gives `pols_if` and then `pols_new_biz`, then S's five columns, the
  rates written 0 outside cover. T1 exempts it, and the module compares it with S's column
  by column.
- *The splice* switches on charges ceasing at attained age 100 and a lapse shock that
  meets the lapse rate's cap, sets acquisition at $250 and A/E at 0.56, and sets inflation
  to 0, in both models. Its variants change S's columns only, each with COI rows at a
  scale of its own in the copies, and the copies add a second surrender-charge schedule.
  The heap is frozen once S is swept, and each row is released once compared. T2 and T3
  exempt `proj_len` and `duration_mth_init`, T2 also S's two opening columns.
- *The rules test* has no `LOOK_AHEAD`: UL reads nothing beyond `t + 1`. Its scan counts
  the precedent edges it reads, and fails a row that read none.
- *No S cell is removed or renamed*, and S's lines over 92 characters are wrapped.
- *The runner* takes `Projection`'s key from the model, freezes the collector once the
  table is read and again before the projections, releases and collects each point in both
  passes, and sums the block with M1's `groupby`. An unknown label exits naming the
  table's labels.
- *M14's carried items not yet taken.* Built on M2's tip, UL took `codes=` at landing, but
  its runner does not yet carry Term's `--cython`, `--build` and `_tool()`, nor its module
  the `create()`-copy test, and `proj_len()` does not yet refuse an issue age below 18,
  the bound §7.3 *C* names; UL's C step takes them up.

**Measured for K6 and F7.** Every time below but the landing's was taken with other
workflows sharing the machine. The second fix's runs of the module, of its full grid and
of the uslib suite were at a load average of 1.5 to 2.8; the SEC conventions' times are
the build's, the docs stage's and the fix stage's.
- *Time.* By default the module ran 159 passed and 41 skipped in 3 min 39 s and
  3 min 50 s, and over the full grid 200 passed in 5 min 30 s, peaking at 2.45 GB and
  2.52 GB in one process. A splice or future case took up to 4.5 s. The splice fixture
  costs 20 s, and by default the count doubling, the runner's subprocesses, the extract,
  the cap test, the declared-rates test, the cold-depth test and the clock test's fresh
  read 10 to 16 s each. The 52 key and value refusals and the accepted-edges test ran in
  21 s together, in the control run of the second fix's fault sweep. The SEC conventions,
  32 passed and 1 skipped, took 17 to 19 s. By default the module costs about 40 s to
  1 min more than WholeLife's, and over the full grid about 30 s more. On M2's tip with UL
  added, the uslib suite ran 1,489 passed and 151 skipped in 13 min 54 s and 14 min 14 s,
  peaking at 2.75 GB to 2.76 GB; UL's own share is about 4 minutes, from its module and
  conventions measured alone. As landed, after M7 and Term's cap fix, it ran 1,938 passed
  and 273 skipped in 17 min 55 s (*Verified at landing*, below).
- *Depth.* A cold `net_cf` of the last month runs one cell a month back to `t_entry()` and
  16 more. On twin 1's 1,032-month frame it runs 1,047 cells deep, a recursion limit of
  1,046, against 5,167 and 5,166 on `UL_US_S`'s point 1. It runs 927 on twin 3's 912
  months, and 1,251 at the longest cover, issue age 18 and 1,236 months, both at the
  valuation date and issued 120 months on. The 16 end in month 0's COI rate:
  `coi_rate_guar_py`, `coi_rate_last_year`, `Data.coi_rate_last_years` and
  `Data.coi_rates`. Each chain head called alone runs at most 8 above its chain: the
  account value 8, the count 7, the premiums to date 6, the loan 4, the face 4 or 5 and
  the latch 2. `CHAIN_OVERHEAD` is 20 and `CALL_DEPTH` 40, and an ascending sweep needs a
  limit of 15, as `UL_US_S`'s does. In the modelx export the cold call needs a recursion
  limit of 2,121 on twin 1, 1,881 on twin 3 and 2,529 at the longest cover; the sweep with
  its checks needs 128, which the import itself needs, and the ascending sweep, with the
  limit set after the import, 58.

**Faults.** Each fault went alone into its own copy of the library, and the tests aimed at
it ran through the gate.
- *Tests stage:* 56 faults and a control: 30 runs of the whole default module, the control
  among them, and 27 of the tests aimed at a fault. 55 faults failed some test, and each
  of the module's 28 test functions of the time failed under at least one. The year's
  usage based at `t == 0` rather than at `t_entry()` passed, an equivalent mutation:
  `t_entry()` is 0 on a point in force, and on a point issued later the issue month is an
  anniversary, where the usage restarts first. Chains of two or more cells a month, for
  the loan, the account value and the count, each failed the cold-depth test, the only
  test run on them, since no number shows a chain's length. The control passed.
- *Review:* the tests lens ran 20 faults and a control, and 6 survived the default module:
  a cap on new business only, the cap as the int 1, the account value's close crediting
  the next month's rate, a residual that is not a number passing both checks, an infinite
  `av_pp_init` accepted, and an unknown `db_option` projected as Option B. The numbers
  lens's two cap faults passed too.
- *Fix stage:* 18 faults and a control, the review's six survivors among them; all 18 fail
  and the control passes. Among the rest: the extents taken from the raw key column, a
  zero face accepted, the margin identity's whole loan, committed row 8's count 0.5% off,
  which T6 passed and the committed-rows test fails, and three on the branches the new
  splice rows reach: Option B without its corridor, no cap on the lapse rate, and a COI
  charged after charges cease. Two faults of the tests stage and the review no longer
  apply: the form of acquisition they edited is gone, and `BEF_MAT` returning the
  `BEF_DECR` count is now the shipped behaviour; two of this stage's replace them.
- *Re-review:* re-ran five of the review's survivors, all failing, and made one that
  passed 25 key cases of 25: the COI scale's run check counting repeats alone, with the
  policy-year tables run from their first key rather than from 1.
- *Second fix:* 10 faults and a control; all 10 fail and the control passes. The
  re-review's fault fails 6 cases. A repeat named by its later line alone fails 1, a gap
  named one age off 2, mortality rates left unchecked 3, `class_factor` not asking
  `class_count` 4, an infinite rate accepted 1, the schedule's readers not asking
  `surr_charge_count` 4, and the schedule's values unchecked 2. Keys written as floats
  refused fail the edges test, the only test run on that fault. `BEF_MAT` back to the
  count before new business, which T3 passed while it exempted `pols_if_at`, now fails T3
  on S point 1 issued a month on.

**Carried into VUL (M4), ULSG (M5) and IUL (M6): the life chassis.** Each item goes to the
Life stream from this landing, and each record says what it took. §7.1's *Precised at M3*
and §7.9's *Carried into every product still to come* bind them too. Where UL's module
departs from §7.9, as *Carried into Phase 2* lists below, they follow §7.9, not UL.
- *Chains.* Make every opening-timing and loan chain form the previous month's close
  itself, in S's order, so that each is one cell a month: VUL's `sa_pp_at`, `fa_pp_at`,
  `la_pp_at` and `loan_bal_pp_at`; ULSG's `av_pp_at`, `sg_pp_at`, `loan_bal_pp_at` and
  `grace_mth`; IUL's `fa_pp_at`, `lca_pp_at` and `av_pp_at`, and the segment ladder. Probe
  every chain head cold, on a read of its own, in an order that leaves each chain cold
  until its head is called, since a cold `net_cf` sees only the chain it descends first.
  At the build, with S's two-cell loan, a cold `loan_bal_pp` on twin 3 needed a recursion
  limit of 1,825, where a cold `net_cf` needed 925.
- *The frame's end.* None of the three S models matures a policy (`pols_maturity` is 0.0
  in each), and each frame ends at a horizon: VUL's at attained age 122, `omega_age` 121
  plus one, ULSG's at `charges_cease_age` 121 and IUL's at `maturity_age` 121. Copy UL's
  carry into `t = proj_len()` and the guard test's `CARRIED` set, and set the splice's A/E
  below 1, so that survivors reach the end.
- *Guards.* Guard every comparison of `policy_year(t)` with a per-point sentinel.
  `IUL_US_S`'s `lapse_rate_sc_mult` compares it with `lapse_shock_year()`, which is 0
  without a schedule (§7.4); VUL's tests `has_surr_charge()` first and keys its shock on
  `duration_mth(t)`.
- *Opening state.* Keep S's own `*_init` columns, and name a new one `<cell>_init` on S's
  stem, as `sum_assured_init` (VUL's too, §7.6), `cum_prem_init` and `is_mec_init` are;
  give a latch or a category as an int code whose labels `model-sec.md` lists. Where the
  product has them, copy UL's four bases at `t_entry()`, `cum_prem_pp`, the TARGET cap,
  `is_mec` and `wd_used_year`, and `Data`'s checks: no usage on an anniversary, the latch
  where the 7-pay test has failed, a face above 0 and at most the face at issue. IUL's S
  cell `is_mec` does not latch; IUL adopts UL's latch (§7.4), with its in-year test run
  before its base, and splices a month where that test fails at `t = 0`. Splice a face cut
  at `t = 0`.
- *Withdrawals and charges.* All three S models read `model_point()["wd_pp"]` in
  `wd_pp(t)`; read it once a point, as UL's `wd_pp_mth()` does. All three surrender-charge
  tables have UL's columns, `sc_per_1000_init` and `runoff_years`: copy
  `surr_charge_rate_max()` and `surr_charge_runoff_years()`, the table's only readers,
  each reading the schedule's key from `model_point()` (*Text*, below). `VUL_US_S` takes
  `int()` of the run-off, so VUL takes `int()` of `surr_charge_runoff_years()` where S
  does. UL neither refuses a fractional run-off nor reads it one way: `lapse_shock_year`
  takes its `int()` and `surr_charge_rate` amortizes over the float, as `UL_US_S` does, so
  the chassis decides it once. Decided at M4: `surr_charge_count()` refuses a
  `runoff_years` that is not a whole number of years, 1 or more, naming its lines, in one
  rule; VUL takes `int()` of it where S does, which then changes no run-off it reads.
- *Mortality.* Cap `mort_rate` at 1.0 with `min(q, 1.0)` (§5.1, step 6), as `VUL_US_S`,
  `IUL_US_S` and `ULSG_US_S` do since §8.2 item 4's fix, so the cap is no departure from
  S; at this landing VUL's and IUL's S models did not cap, and ULSG's capped by
  `min(1.0, ...)`, which reads a blank rate or class factor as 1.0. Test it as UL's cap
  and NaN tests do: on a tobacco class at the shipped A/E, every cell compared with S, the
  capped months included, and with a NaN sent to the cap, which stays NaN.
- *Tables.* One keyed reader per policy-year or age table, `_py(y)` or `_at(a)`, each
  called only in cover, its extent from a `Data` cell that checks the table (§7.1,
  *Precised at M3*). VUL's subaccount table, whose ids name the model point table's
  columns, is read through a checked copy, `Data.subaccounts()`, indexed by the ids read
  by value as int64, so that an id written `1.0` still names `alloc_1` (§7.1, *Precised at
  M3*, item 9's second form; precised at M4). In a table keyed by text and a number, as
  UL's COI scale, ULSG's COI rates by attained age and VUL's scenario table by scenario,
  subaccount and month are, each clause of a refusal names the cell it is about. The
  clauses are built inline with `for` loops, since a `Data` cell returns a C scalar at
  stage `EC` and no helper cell builds a message. `VUL_US_S`'s `coi_rate_guar_at(y)` is a
  policy-year reader, and VUL keeps S's name so that T1 compares it.
- *Model point values.* `Data` refuses a blank, text or infinite value in every S column
  of the model point table a projection reads as a number, through a floor or a `max`
  included, and one outside the range the quantity can take (§5.1, step 6): VUL's face at
  issue, refused at 0 too, its planned premium and planned withdrawal below 0, and its
  load and allocations outside 0 to 1, as ULSG's and IUL's loads and IUL's
  `index_alloc_rate` are; and a bool flag unless `True` or `False` as pandas reads those
  words, since one text value turns the column into text, where S's `bool()` reads
  `"False"` as true. Of its S columns `UL_US_SEC` checks only `duration_mth`, the two in
  its opening state, `av_pp_init` and `loan_bal_init`, and `sum_assured`, as the bound of
  the face in force: its C step or M13 takes the rule, and ULSG and IUL copy VUL's
  (precised at M4).
- *Text.* A bool decode for each value of each text column a monthly cell branches on,
  each reading its column from `model_point()`, as SPIA's and MYGA's decodes do, while the
  cell that branches keeps S's raise, with a table-driven `UNDECODABLE` list: `db_option`,
  `qual_test` and `premium_type` where the product has them, and IUL's `premium_mode`.
  ULSG's `premium_freq` already decodes its `premium_mode` to a number. Read each join key
  from `model_point()` in the one cell that reads its table. UL's decodes and joins call
  S's label accessors instead, a departure from M14's carried rule (*Departures and
  precisions*, *Text*) that the chassis does not copy.
- *Checks.* Each S check becomes a `bool` over relative `*_resid(t)` cells that keep S's
  own tolerances: IUL's `isclose(rel_tol=1e-9, abs_tol=1e-8)` is a residual floored at 10,
  not 1, or T1 fails where S's check passes. IUL's `check_seg_ladder` tests three bounds
  and a closure per maturing segment, and needs a residual cell for each part. VUL's,
  ULSG's and IUL's margin identities add back the whole loan on a lapse,
  `loan_bal_pp(t) * pols_lapse(t)`, as `UL_US_S`'s does, and VUL's `check_net_view` adds
  it back on a lapse and on a death; check each lapse term against the loan a surrender
  recovers, `min(loan_bal_pp(t), csv_pp(t))`. A residual written as the difference over
  the larger side and its floor, 1 where S's tolerances are both 1e-9, is S's
  `math.isclose` only through that floor, and T2 compares only verdicts that hold in both
  models; so the module moves a cell only the checks read, in both models, by a miss
  inside the absolute tolerance and one outside it, on a point whose sides fall well below
  the floor, below 0.5 in VUL, and asserts each verdict in both. Every check takes a move.
  VUL's `inv_income` reaches its three checks, and ULSG's and IUL's reach
  `check_av_roll_fwd` and `check_margin` alone. ULSG's `check_sg_roll_fwd` and IUL's
  `check_av_components` compare balances per policy, at least 654 and 241 in size in every
  month of S's points, and a move of `sg_deduction_pp` or `seg_bal_tot_pp`, which only
  that check and a report read, decides that check alone on a point in force whose opening
  balance closes month 0 below the floor: point 1 at a `duration_mth` of 305 and a
  `sg_pp_init` of 2,373.57 closes it at 0.25 in ULSG, and at 126 and an `av_pp_init` of
  86.88 at 2.5 in IUL. No cell only the checks and a report read reaches IUL's closure:
  `seg_wd_cum_pp`, which `index_credit_pp` reads too, moved only where the closure reads
  it, `seg_wd_cum_pp(t - 1, t - 12)`, decides the closure alone on IUL's points 1, 2, 3
  and 5, whose empty segments close at 0 (precised at M4).
- *Timings.* `pols_if_at` keeps the stub's meaning for `"BEF_DECR"` and `"BEF_MAT"` and
  gives `"BEF_NB"` D5's (D5, precised at M3). T3 compares it through an `arg_map` such as
  `_issued_later`, and the count test holds `"BEF_MAT"` equal to `"BEF_DECR"`. VUL's test
  module passes every timing and kind through `_code`, as UL's does; VUL's model keeps S's
  strings at its 60 or so timing call sites until R9 (§7.6, *C*).
- *The splice.* Variants from S's columns: withdrawals on each death benefit option, each
  premium type and mode, an over-funded point and an Option B point funded past the face,
  where the corridor binds; every class and sex with COI rows at a scale of its own, the
  copied table sorted; a second surrender-charge schedule and a second issue age. Where
  the product has them, switch on charges ceasing in cover and a lapse shock, by
  References only and in both models, the shock meeting a lapse cap below 1, as UL's 0.35.
  IUL's cap, 1.0, is inert, and a shock that met it would lapse every policy and leave no
  survivor to reach the frame's end, so the splice lowers it first; VUL's lapse rate has
  no cap. Freeze the heap once S is swept and release each row once compared; at teardown
  close the models, then call `gc.unfreeze()` and `gc.collect()` (§7.9). The module puts
  every test that reads the splice in a class, first in the module, with class-scoped
  fixtures, so that the splice's models are closed before the committed model and S are
  read: VUL's module peaks by default at 3.39 GB, in committed-model tests that read two
  more models beside those two swept fixtures, its full-only cases, all but one in the
  class, at 2.72 GB run alone, and the uslib suite with VUL at 3.71 GB (precised at M4).
- *Tests.* Copy UL's: `_settle`'s records, the rules test's taken before the comparison
  (§7.9) and the row released after it; the guard test, whose disjoint sets cover every
  cell whose first parameter is `t`; the cold-depth test, the deepest call on one read and
  each chain head on a second; the rate-path test with its S comparison, through a copy of
  `scenario_table.csv` for VUL's fund returns, which keeps it runnable compiled (K7), and
  under an override of `index_level` for IUL's index path; the NaN-residual test; the
  committed rows against S; the rules scan's edge count; the margin test with a loan above
  its cash value; `MALFORMED_KEYS`, `MALFORMED_RATES` and `_refused_exactly`, each case
  also read through `net_cf(0)` of a point that reads every table; keys written as floats
  among the accepted edges; and acquisition checked bit for bit against S at counts and
  inputs that are not round. A guard whose removal makes a recursion without end, as VUL's
  funding ratio before issue does, is also faulted quietly, with the recursion's base
  widened, so that only the key-range check can see it (precised at M4).
- *Cost.* A UL splice or future case takes up to 4.5 s, and the module's default runs
  about 40 s to 1 min longer than WholeLife's: plan the core and full split from the
  start.

**Carried into Phase 2.**
- *Caches and bounds:* §7.3's *C*. The figures above size `sample_sec.py`,
  `run_sec.py --cython` and the Windows job's stack. `CHAIN_OVERHEAD` 20 leaves 4 levels
  for a `Data` vector read under a table's reader.
- *`Data`:* the nine cells new at M3 become int scalars or vectors by point,
  `coi_rate_last_years` among them, and `class_count`'s and `surr_charge_count`'s checks
  move into the class factor's and the schedule's vectors; the refusal code stays on the
  raise paths, which return nothing. The five per-point joins and the six decodes move
  onto `Data` arrays (R6, R7).
- *T1 and codes:* S's `claims(t, None)` keys need a T1 `arg_map` at stage `EC` (R12).
  `_twin`, the module's one call of `twin_mismatches`, passes `codes=codes(sec_proj)` from
  the landing on, so the splice's comparisons take Phase 2's codes when they come (§5.2,
  T1).
- *Tests on the compiled model:* `_refused` asserts that `ValueError` is in the error's
  text, which a compiled model's bare `ValueError` does not hold; at stage `EC` it reads
  `_raised(err)`, as `_refused_exactly` does. The declared-rates and NaN-residual tests
  override formulas and stay on modelx (C1). C4's grid is the splice's: 54 splices and 11
  future rows in full, 20 and 5 in the core.
- *M14's items for the C step:* the runner's `--cython`, `--build` and `_tool()`, with the
  `create()`-copy test and the compiled runner test's refusal leg; and `proj_len()`'s
  refusal of an issue age below 18 (R4; §6.1, steps 6 and 7).
- *M11's points, not retrofitted at stage `E`* (§7.9, *Carried into every product still to
  come*). UL takes the first two at M13 with Term, WholeLife and MYGA (§5.4), and its C
  step the rest:
  - T4 doubles `policy_count`, a factor of 2, with the assumptions that ship at zero left
    there; acquisition is tested apart, at counts 3.7 times the table's;
  - T2 and T3 compare at `twin_mismatches`' default absolute floor of 1e-9, and the cap
    test at none;
  - each splice row is recorded for the rules test after it is compared with S, in the
    case's `finally`; the rules test passes, so the comparison reached no negative key;
  - the splice fixture calls `gc.unfreeze()` before it closes its models, and no
    `gc.collect()` after;
  - each malformed case carries one fault by design, but no run dropped each rule in turn
    to check that one rule alone refuses it;
  - the core is chosen by the list of branches, opening-state columns and kinds of
    valuation month that a test asserts it reaches, not by line coverage. The same item's
    set-apart edit does not arise: the splice's copies add rows for keys S's tables lack
    and change none of S's.

**Carried, outside the SEC models.**
- *The harness.* T6 compares a float cell to 1e-12, relative and absolute, so it pins
  committed row 8's count of 1.8e-10 only to 0.57%; UL's committed-rows test fails a 0.5%
  change in it. A relative comparison in `sec_support._same_cell` would close the gap for
  every product; it is a change to the shared harness, not made at M3.
- Nine S-side items for §8.2 item 4. The first seven are `UL_US_S`'s, fixed in `UL_US_SEC`
  only; the last two are in the chassis's other S models:
  - `UL_US_S` does not cap `mort_rate` at 1: its StdTob class passes 1 from attained age
    113 and PTob from 114, where its monthly rate is complex (§8.2 item 4 lists it, with
    `VUL_US_S` and `IUL_US_S`);
  - its readers take each table's extent from the key column as pandas reads it, so a
    blank last key cuts the table short without a word: a blank policy year 16 in
    `prem_persistency.csv` reads 0.72 for 0.70 from year 16 on;
  - it reads a blank value as a missing one, which its own `min` and `max` lose without a
    word: a blank lapse rate reads as the cap of 0.35 (`lapse_rate`), a blank corridor
    factor as no corridor (`db_pp`), a blank surrender charge as none
    (`surr_charge_rate`);
  - `check_margin` adds back the whole loan on a lapse, `loan_bal_pp(t) * pols_lapse(t)`,
    and fails once a loan exceeds the cash value, since the lapse claim is floored at 0;
    the term is `min(loan_bal_pp(t), csv_pp(t)) * pols_lapse(t)`;
  - the model docstring says that point 2's Option B makes the corridor live; the corridor
    never binds there, its largest ratio to the death benefit 0.41;
  - `premium_pp`'s docstring renders its three patterns as one paragraph, `wd_pp`'s says
    "not after attained age 121" where the code stops from 121, and `lapse_rate_sc_mult`'s
    says "Applied in `lapse_shock_year` only";
  - seven lines exceed 92 characters: `Data` lines 103, 108, 112, 113 and 122, and
    `Projection` lines 1162 and 1192;
  - `ULSG_US_S` caps its mortality by `min(1.0, ...)`, which reads a blank rate or class
    factor as 1.0;
  - the `pols_if_at` stub that returns `pols_if` for every timing, which §8.2 item 4 lists
    in UL and VUL, is in `ULSG_US_S` and `IUL_US_S` too.

**Landing.** Rebased from bbb99a9 (M2) onto 05b56eb, Term's cap fix, after M7.
`mort_rate`'s cap became `min(q, 1.0)`, where the build wrote `min(1.0, q)`, so that a NaN
stays NaN in both engines (§5.1, step 6). `_twin` took `codes=codes(sec_proj)` (*Carried
into Phase 2*). uslib's `index.md` took the one conflict, the sentence that lists the SEC
models, merged as MYGA left it plus UL, and `sec_support.py` the two conflicts, where UL's
state extractors and spec sit beside SPIA's and MYGA's, keeping all three. Nine texts that
said the cap reads a blank base rate or class factor as 1.0, which `min(q, 1.0)` makes
untrue, now say that it keeps one missing: the docstrings of `class_factor` and
`mort_rate`, three in `Data`, two places in `model-sec.md` and two in the test module; and
a test-module docstring that dated a measurement to the build's design now dates it to M3.

**Verified at landing**, on the tree as committed, with no other workflow sharing the
machine. The uslib suite, with modelx-cython installed and so the compile tests included,
gave 1,938 passed and 273 skipped in 1,074.62 s (17 min 55 s), 192 passes and 42 skips
more than Term's cap fix landed with: UL's module, 159 and 41; its SEC conventions, 32 and
1; and the one compiled convention that reads every SEC model. Over its full grid, UL's
module gave 200 passed in 224.69 s, and the `cython` selection 11 passed and none skipped
under `USLIB_REQUIRE_CYTHON=1`, in 117.15 s. doccheck built 493 pages with 0 warnings.
`gen_sec_points.py --check` found the files of the five SEC models current, and
`gen_sec_fingerprint.py Term_US_SEC --check` reproduced the fingerprint. md_lint reported
0, `gen_scaffolding.py --dry-run` 0 files in each of the six libraries, and
`gen_citation_links.py --dry-run` nothing on its 298 source tags. A case-insensitive
search of `model_point_table_sec.csv` for the names, forms and hosts that
`universal_life/sources.md` cites found none.

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
- `lapse_rate_sc_mult` needs UL's guard: `IUL_US_S`'s `lapse_shock_year` returns 0 without
  a schedule, which is the policy year of the twelve months before issue (M3).
- Splice months: 1, 11, 12, 13, 60, 65, and point 4 (monthly premium, a full ladder).

*C:*
- R15: six `(t, m)` segment cells (`seg_share`, `seg_wd_pp`, `seg_ded_pp`, `seg_bal_pp`,
  `seg_ded_cum_pp`, `seg_wd_cum_pp`) are re-keyed by slot. This is the one Phase 2 change
  that restructures a family of cells, and the fingerprints and the Phase 1 suite gate it.
  A test calls `seg_bal_pp(0, -1)`.
- R14: `index_change`, `index_credit_rate(..., cap=None)`,
  `seg_credit_base(..., conv=None)`, `index_credit` and `seg_matured_value` take floats.
  Each is inlined into the slot-keyed segment cell that calls it (R15), its cap a float
  read from the slot's state and `conv` an int code, so that each credit is a cached cell
  with a C-array cache; none is left uncached, which would compile it untyped. S's worked
  example, which prices `index_credit_rate` at two caps, keeps S's cell outside the
  projection or moves to the inlined form (R14).
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
- The solver's float-parameter cells, with dict caches of 7,900 to 18,300 entries, leave
  the projection: the premium is an input in SEC (E, above), and the solve is a Python
  utility outside the model, or S's cells kept for its tests and called by no projection
  cell (R14).
- `t` reaches 732 through `is_lapsed(t + 1)`.

### 7.6 Variable UL — `VUL_US_SEC` (E: S, C: L)

*Today:* the closest to BasicTerm_SE. It runs on the projection clock with issue events
already keyed on `duration_mth == 0`. Points 1–2 are in force at 24 months and point 4 at
120 (with a fixed account and a loan); point 3 is new business. Re-opening point 3 at
`d = 37` and `200` reproduces S to 1e-9.

*E:*
- `la_pp_init`, D6's name on S's stem, beside S's `sa_pp_init_<i>` and `fa_pp_init`: the
  loan collateral entering month 0. S opens it at `loan_bal_init` by a [std] assumption,
  and once interest accrues the two part: point 4 restated six months on holds 8,039.90 of
  collateral against a debt of 8,041.89, and read as the debt its account value is 1.99
  high and its `net_cf` about 0.005 a month low. `Data` refuses a collateral without a
  loan, or a loan without one.
- `sum_assured_init`, the current face, D6's name for the opening of `VUL_US_S`'s
  `sum_assured_at`, as at M3; the initial face stays in `units()` and the charges.
- The pricing path (`sa_pricing_pp(m, i)` …) is recomputed from issue, which is
  deterministic and needs no state, but its `m = duration_mth(t)` goes negative for future
  new business (R1): `funding_ratio` returns 1.0 outside cover before it reads the path.
  The path keeps its key from issue, one cell a month, so with the behaviour module on a
  cold call runs back to issue, 938 cells on twin 4 (923 months and 15 more) and 1,484 at
  the longest cover, and so, with the module on, does an ascending sweep of a point in
  force, about `d + 15` cells deep, 135 on twin 4 (R2, precised at M4). S's
  `fa_pricing_pp(m)` reads `fixed_return_mth(m)`, the valuation-clock declared rate, at a
  policy month (R1a); SEC credits one pricing rate, `pricing_fixed_return_mth()`, the same
  float while the rate is flat.
- The first-month pins (`corridor_override_m1`, `coi_rate_override_m1`) keep `t == 0`. In
  SEC that is the valuation month, which is what the worked example — asserted at `t = 0` on
  in-force point 1 — means.
- The scenario table is keyed by projected `t`, so it is already on the valuation clock.
  T2 and T3 give each restated or future row its own copy, re-based to its month by
  subaccount (§5.2, precised at M7): point 1 re-opened at `d = 12` on `WE` as shipped
  reads the worked example's month at `t = 0`, closes its first subaccount 174.79 above
  S's and its account value 46.71 below, and its `net_cf` is 0.152 above at `t = 0` and
  0.129 above at `t = 100`. The committed table restates points on the flat `LEVEL6` only,
  which needs no copy.
- `VUL_US_S`'s lapse rate, the base rate times the cliff's spike times the dynamic
  multiplier, has no cap, and SEC keeps it so. `Data` holds each base rate to 0 to 1. With
  `lapse_shock_mult` and `lapse_dyn_cap` at 0 or more, the annual lapse rate is at most
  `max(1, lapse_shock_mult)` × (`lapse_dyn_cap` with the behaviour module on, 1 with it
  off) × the largest base rate, since the spike is 1 outside its month and the multiplier
  is 1 with the module off. It stays at most 1 while that product is at most 1: 0.06 as
  shipped, 0.12 with the module on, 0.36 on the splice. Past 1 the count is complex in
  both models, and SEC's checks raise as S's do: a spike of 40 takes point 3 to 1.2 at
  policy month 168 (precised at M4). The missing bound is an S-side item, fixed in neither
  model: §8.2 item 4's fix is to mortality alone (*Record — M4*, below).
- `Data` also refuses a lapse or mortality rate outside 0 to 1, and a class factor, a
  guaranteed COI rate, a fund expense, a premium persistency factor or an initial
  surrender charge below 0, and in the model point table a premium load or an allocation
  outside 0 to 1 (§5.1, step 6, precised at M4).
- Splice months: 12, 37, 96, 108, 200.

*C:*
- `subaccount_ids()` returns a list and `"alloc_" + str(i)` names columns; these become an
  `n_sa` int and `alloc[idx, i]` / `sa_init[idx, i]`, 0-based.
- Returns become a dense `ret[scen, sa, t]`; COI a `coi_guar[schedule, py]` with a
  per-point schedule number (R7); corridor and mortality by age; lapse and persistency by
  policy year, clamped; the surrender charge per point.
- About 60 timing call sites (eleven `*_at` cells, including tuple-membership tests on the
  timing), plus kinds.
- `None` defaults on `claims` and `me_charge_pp(t, i=None)` become total cells.
- Nine of S's cells carry generator expressions, which become loops over `range(n_sa)`;
  eight still do in `VUL_US_SEC`, whose `av_pp_init` is a loop from M4.
- Never reached by any report or check on the committed points, at the shipped References:
  the pricing path, `funding_ratio`, `prem_persistency_base`, `prem_persistency_py`,
  `pricing_fixed_return_mth`, `inv_return_mth`, and `Data.prem_persistency_last_year` with
  S's `Data.prem_persistency_table`; the default and shortfall tests, `is_default` and
  `is_shortfall`, and their searches, `first_default_month` and `first_shortfall_month`;
  and the label accessors, which no projection cell calls. `pols_if_at` now carries the
  count. The sample sets `dyn_behavior_on = True`, and so sizes its recursion limit from
  the cover from issue (R2, precised at M4).
- The `_rejects` test matches the source text `raise ValueError("invalid timing")` and is
  rewritten.

#### Record — M4, done 2026-11-03

Built in two commits, as D1 requires: `VUL_US_S` copied with only `_name` changed, then
the enhancement, by M1's process: a design prototyped and critiqued before the build,
tests written against the build and checked by injected faults, then a review under the
three lenses. The design departed from §7.6's *E* where reading `VUL_US_S` cell by cell
showed it short: the collateral's column takes S's stem, `la_pp_init`, and reading it as
the debt moves `net_cf` by about 0.005 a month, not 0.015; the pricing path keeps its key
from issue, so that with the behaviour module on a call runs back to issue, cold or swept
in ascending `t`; S's pricing path reads the declared rate at a policy month, a clock
error §7.6 did not list; and the plan's 0.115 for point 1 on the unshifted scenario does
not reproduce. So §7.6's *E* takes three bullets as built and two new ones, and its *C*
the cells no report reaches. The review made 24 findings, 1 a blocker and 5 major, and
three were each made under two lenses. Four caps and floors were never tested where they
bind, and bound on no row of the full grid, so that dropping any one passed the default
module and the conventions; a lapse rate past 1 made the projection complex, and the
checks passed it where `VUL_US_S`'s raise, while `Data` took rates outside 0 to 1; with
the behaviour module on, an ascending sweep of a point in force ran back to issue, and
nothing recorded or bounded it; the two first-month pins always appeared together, so that
a pin tested with the other's flag passed the full grid; no case wrote a policy year below
1 in the COI or the premium persistency scale; and no core row was valued in its lapse
spike's month. The fix stage applied all 24 and rejected three of their details with
evidence: two bounds a splice Reference can bind on one side only are asserted against
`VUL_US_S` in a default test of their own, not listed for the core-reach test; the
reviewer's own better option, S rows with one pin each, replaced a row with the COI pin
alone in the edges test; and the export's recursion limits, which it did not measure
again, are given in R2 as the review measured them, and the re-review measured them again
on the fixed model. That re-review made four more findings, all minor: the lapse rate's
bound was stated in a form neither necessary nor sufficient, in four places; that
paragraph split a list in the shared spec comment; the core-reach check of the face's
floor held where the floor changes nothing; and two value columns the new range rule
covers still took any number. A second fix applied all four. Ten defects found in
`VUL_US_S` are carried below: one was corrected in `VUL_US_S` itself at d3a7be8, after the
build, one, the lapse rate's lack of a bound, is in both models, and the rest are fixed or
refused in `VUL_US_SEC` only. M4 was built on ed73164, the second of §8.2 item 4's
commits, and rebased at landing onto FIA's (*Landing*, below).

**What exists now.**
- `VUL_US_SEC` at stage `E`. Of `VUL_US_S`'s 148 `Projection` cells, 60 are unchanged, 36
  have a new docstring only and 52 are rewritten; none is removed or renamed. It adds 28
  cells, 176 in all: `policy_count`, `omega_mth`, `t_entry`, `is_active` and
  `pols_new_biz`; the opening-state accessors `la_pp_init` and `sum_assured_init`;
  `wd_pp_mth`, the planned withdrawal read once a point; the two first-month pins, each
  read once a point as a value and a flag, `corridor_override_m1` and
  `has_corridor_override_m1`, `coi_rate_override_m1` and `has_coi_rate_override_m1`; five
  bool decodes, `is_db_option_a`, `is_db_option_b`, `is_gpt`, `is_level_premium` and
  `is_single_premium`; three keyed readers, `prem_persistency_py`, `lapse_rate_base_py`
  and `mort_rate_base_at`, beside S's `coi_rate_guar_at` and `corridor_factor_at`,
  rewritten to read so; `coi_rate_last_year`, a point's COI extent, and
  `scenario_last_mth`, a subaccount's last scenario month; the schedule's two readers,
  `surr_charge_rate_max` and `surr_charge_runoff_years`; `pricing_fixed_return_mth`, the
  pricing path's one declared rate; and the residual cells `check_av_roll_fwd_resid`,
  `check_margin_resid` and `check_net_view_resid`. S's `math` Reference is dropped, and
  its other References keep S's values. `Data` keeps S's eleven cells: seven unchanged,
  three of them with their `read_csv` call rewrapped, two with a docstring line added or
  changed and their call rewrapped, `model_point_table` rewritten to check the table as it
  reads it, 20 rules in turn, and `scenario_table` formed from `scenario_rows()`, the same
  frame as S's. It adds twelve, 23 in all: `subaccounts`, a checked copy of the lineup;
  `scenario_rows`, the scenario's one raw read, and `scenario_last_mths`, its check; seven
  that check a keyed table and give its extent, `prem_persistency_last_year`,
  `lapse_last_year`, `corridor_age_first`, `corridor_age_last`, `mort_age_first`,
  `mort_age_last` and `coi_rate_last_years`; and `class_count` and `surr_charge_count`,
  which check the two tables read by point. It adds the Reference
  `future_horizon_mth = 120`.
- `model_point_table_sec.csv` holds nine rows generated from VUL's `SecSpec`. Four are S's
  points as twins at offset 0, since `VUL_US_S` runs on the projection clock already:
  points 1 and 2 in force 24 months, point 1 with the worked example's two first-month
  pins, point 3 new business issued at the valuation date, and point 4 in force 120 months
  with a fixed option and an $8,000 loan. Four are derived: S point 3 on its first
  anniversary, inside the surrender-charge period, at 12; S point 4 six months on,
  mid-year, at 6, its collateral, 8,039.90, parted from its debt, 8,041.89; S point 3 in
  the month its permanent shortfall begins, the last month it can be restated, at 593; and
  S point 4 in the first month at attained age 119, where the table's rate reaches 1.0 and
  its last 4.006e-10 of a policy dies at `t = 0`, at 768, in place of the last covered
  month, which no policy reaches at S's mortality. The last is S point 3 issued 25 months
  on. The derived rows restate S points 3 and 4, which read the flat `LEVEL6` scenario, so
  the table needs no companion. A case-insensitive search of it for 27 terms from the four
  carriers' filings that `variable_ul/sources.md` cites, their names, products,
  registrants, CIKs, forms and file names, found none.
- `tests/test_variable_ul_us_sec.py` has 44 tests in 285 cases, 242 by default and 43
  behind `sec_full` (K6). T2 runs on 54 rows: 48 restated from S's four points and six of
  the nine variants at the months of their events, the anniversaries, the loan's preferred
  tier, the lapse table's last year, the surrender charge's cliff and spike, the
  shortfall's start, charges ceasing, the corridor's first binding month and the last
  covered month; and six in-force twins at offset 0, S's points 1, 2 and 4 and variants 9,
  11 and 12. T3 runs on 9 future rows, S point 3 one, 12 and 13 months on and six variants
  13 months on. The default core is 17 and 5, and a test asserts that it reaches every
  option, premium pattern, class, sex, scenario, schedule and issue age, each kind of
  valuation month, the lapse spike's own among them, and on the splice's model 16
  conditions at the valuation date and 20 in the frame; at the tests stage line coverage
  showed it running all 556 `Projection` lines the full grid then ran. Every test that
  reads the splice sits in one class, first in the module. T4 runs at 2.5 contracts. T5
  covers 77 model point tables, each refused by its own rule, a load and an allocation
  past 1 among them; 53 tables with a malformed key and 45 with a value that is not a
  number or out of its range, a case past each bound of the seven ranges among them, and a
  read of each bound; 3 values no decode knows, each raising S's message; and 2 points
  past cover. The accepted edges write every keyed table's keys as floats and read a load
  of 1. A NaN residual fails every check; a NaN that reaches the cap on mortality, or a
  bound on the COI rate written second, stays NaN; a lapse rate past 1 makes each check
  raise in both models; and each check passes a miss inside S's tolerance and fails one
  outside it. The SEC conventions, 33 cases, pass but for
  `test_net_cf_is_income_positive`, skipped as on `VUL_US_S`, since neither model has the
  notes-orientation companion cells.
- `run_sec.py`; `model-sec.md`, with *The opening state*, which shows each new column
  beside the same row read as `VUL_US_S` opens it: point 6's collateral, its account value
  1.99 high and `net_cf` 0.00496 low in month 0 when read as the debt; its subaccounts,
  the account value 16.12 and 196.05 low at the ends of months 0 and 11 when spread by the
  allocation; and, on S point 3 on Option A withdrawing $100 a month restated at 13, the
  face in force, a death benefit of 169,308.38 in month 0 against 485,274.97 at the face
  at issue; the registry entry with its `INPUT_FILES`; and four generated pages. doccheck
  reported 497 pages and 0 warnings on ed73164 with VUL added.
- Shared files, added to in place: in `sec_support.py`, VUL's state extractors,
  `_vul_entering`, `_vul_sa_entering`, `_vul_no_pin` and `_VUL_STATE`, and its spec, each
  after FIA's, the spec's comment giving the state and the rows, T1's one exemption, the
  keys S caches under `None`, the pins under R8, Phase 2's sizes with their inputs and the
  lapse rate's bound; in `us_registry.py`, the entry directly after `VUL_US_S`'s, with no
  flag of its own, since its `pols_if` is `BEF_DECR`, and its `INPUT_FILES`; and the
  models table's Variable UL row and the sentence on the SEC models in uslib's `index.md`.

**Departures and precisions.**
- *The opening state* (§7.6, *E*; D6) is six columns beside `policy_count` and
  `duration_mth` on the shipped lineup of two subaccounts, each what `VUL_US_S` carries
  into month 0: S's own `sa_pp_init_<i>`, one a subaccount, `fa_pp_init` and
  `loan_bal_init`, under their own names, since they measure D6's instant already; and two
  on S's stems, `la_pp_init`, the loan collateral, which S opens at the debt by a [std]
  assumption, and `sum_assured_init`, the face in force. `av_pp_init` sums the collateral
  where S sums the debt. `Data` refuses a collateral without a loan or a loan without one,
  a face in force of 0 or above the face at issue, and any opening state on a point not
  yet in force.
- *The pins.* The two first-month pins, `corridor_override_m1` and `coi_rate_override_m1`,
  are not state: they keep `t == 0`, the valuation month (§7.6, *E*), read once a point as
  a value and a flag. The generator blanks them on every derived row, a future row copies
  its twin's, which are blank, and `Data` refuses a pin that is neither blank nor a
  number, zero or more, and one on a point issued later, which would never apply.
- *The twins' state* (§4, *Record*). `twin_state` takes the two new columns from
  `_VUL_STATE`: on S's in-force points 1, 2 and 4 the collateral is the debt, 8,000 on
  point 4 and 0 elsewhere, and the face in force the face at issue, each what S itself
  assumes, so each twin reproduces S.
- *`Data` checks the model point table* (§7.1's template, item 9; the life chassis, *Model
  point values*, precised) in 20 rules, in the template's order, the first that fails
  raising and naming the missing column or every point at fault: the columns read, a
  unique `point_id`, the count, a whole duration and the horizon; the issue age, whole and
  0 or more, which UL does not refuse; the face at issue, a number above 0; S's planned
  premium and planned withdrawal, each a number, zero or more; its load and allocations,
  each from 0 to 1; `has_surr_charge`, `True` or `False` as pandas reads those words,
  naming only the points at fault where one text value turns the column into text, which
  S's `bool()` reads as true; the accounts, the collateral, the debt and the face in
  force, zero or more; no opening state on a point not yet in force; the face in force
  above 0 and at most the face at issue; the collateral paired with the loan; and the
  pins.
- *Ranges* (§5.1, step 6, precised). `Data` refuses a lapse or mortality rate outside 0 to
  1, and a class factor, a guaranteed COI rate, a fund expense, a premium persistency
  factor or an initial surrender charge below 0, each in the rule that refuses the
  column's blanks, with one message per column, and a test reads each bound. A return and
  a corridor factor need only be numbers. `VUL_US_S` projects each such value: negative
  deaths, lapses or premiums, a credit for the insurance or the fund, and, for an initial
  surrender charge below 0, no charge through the schedule and a rising one after it, each
  with every check passing, and a lapse rate past 1 as a complex count, which only its
  checks catch, by raising (*Carried, outside the SEC models*). Since the landing's review
  the model point table's load and allocations are held to 0 to 1, in one rule, where they
  were held to 0 or more: at a load of 1.5 point 3's accounts would take −250.00 of its
  500.00 premium in month 0, every check passing, and the accepted edges read a load of 1.
- *The tables* (R5; §7.1, *Precised at M3*, item 9). Each policy-year or age table has one
  keyed reader, which takes its extent from a `Data` cell that checks the table, UL's
  seven, with `class_count` and `surr_charge_count`, which also refuses a run-off that is
  not a whole number of years, 1 or more: S truncates 7.5 to 7 and divides by a run-off of
  0, and VUL takes `int()` of the checked value where S does, the life chassis's decision,
  made here. The lineup, whose ids name the model point table's columns, is a checked
  copy, `Data.subaccounts()`, its ids read by value as int64, so that an id written `1.0`
  still names `alloc_1` and `sa_pp_init_1`, where `VUL_US_S` asks for `sa_pp_init_1.0` and
  raises. The scenario is read once, by `Data.scenario_rows()`, so that a refusal can name
  its lines, which S's sorted index scrambles; S's `scenario_table()` is formed from it,
  the same frame, and `scenario_last_mths()` checks each scenario's and subaccount's
  months, one row a month from 0 or later. No per-point join is checked in `Data`, as in
  UL: a key missing from its table raises at its first read, as in S, until R7.
- *The pricing path* (R1, R1a; R2, precised). The projection made at issue that the
  funding ratio compares the account value with is a vector of balances, the subaccounts'
  and the fixed option's, coupled within the month by the pro-rata deduction, so it keeps
  its key from issue, one cell a month, each opening balance forming the previous month's
  close itself, where S's ran through four cells a month. `funding_ratio` returns 1.0
  outside cover before it computes the policy month: without the guard a future point's
  `funding_ratio(0)` recurses without end. `fa_pricing_pp` credits one pricing rate,
  `pricing_fixed_return_mth()`, where S's credits `fixed_return_mth(m)`, the declared rate
  on the valuation clock, at a policy month (R1a), the same float while the rate is flat,
  as it ships; a test moves the declared rate along `t` by a formula override, which moves
  S's path and leaves SEC's. The rules test judges the path at `m - duration_mth_init()`,
  where R1 and R2's look-ahead hold for it and the look-back does not (§5.2, T2,
  precised). With the behaviour module on, a call runs back to issue, cold or swept in
  ascending `t`, and the depth test bounds both (*Measured for K6 and F7*, below).
- *Chains of one cell a month* (D5). `sa_pp_at`, `fa_pp_at`, `la_pp_at` and
  `loan_bal_pp_at` form the previous month's close themselves, S's arithmetic in S's
  order, where S's ran through six cells a month, five, two and two; the subaccounts and
  the fixed option, which share each month's withdrawal and deduction pro rata, are one
  chain, whichever is called first running the others alongside it. `pols_if_at`'s
  `"BEF_NB"` forms the survivors itself, `"BEF_DECR"` and `"BEF_MAT"` keep the stub's
  meaning, and `pols_if` is `"BEF_DECR"` (D5, precised at M3). `CHAIN_OVERHEAD` is 25,
  against Term's 16 and UL's 20, over a measured 20 or 21 (D5, precised).
- *Guards* (R1). Every flow, charge, rate keyed by a year or an age, decrement and chain
  is guarded by `is_active(t)`, and `lapse_rate_sc_mult` and `funding_ratio` are a neutral
  1.0 outside cover. The count and the account value are carried into `t = proj_len()`,
  and everything else is zero there, `av_change` and the residual cells, which read
  `t + 1`, included (§7.1, *Precised at M3*, item 5). The guard test's disjoint sets hold
  all 100 cells whose first parameter is `t`, on the committed points and on the splice's
  rows.
- *The checks* (§7.1, *Precised at M3*, item 11; §7.1, *Record — M14*, precised). Each S
  check is a `bool` over a relative `*_resid(t)` cell floored at 1, so that S's `isclose`,
  with both tolerances at 1e-9, holds, and each residual returns `float(...)` of its
  ratio: a lapse rate past 1 makes the count complex in both models, and a complex
  residual, whose magnitude is real, passed its check where S's `isclose` raises.
  Compiled, the power is NaN and the check returns False. The lapse terms of
  `check_margin` and `check_net_view` are the loan a surrender recovers,
  `min(loan_bal_pp(t), csv_pp(t))`, and the net view's death term keeps the whole loan:
  once a loan passes its cash value, `VUL_US_S`'s two checks fail on a projection that is
  right, and this model's hold.
- *The lapse rate* (§7.6, *E*, new). `VUL_US_S`'s, the base rate times the cliff's spike
  times the dynamic multiplier, has no cap, and SEC keeps it so, M14's power rule precised
  for it (§7.1, *Record — M14*). The bound under which it stays a rate is stated with its
  premise, `lapse_shock_mult` and `lapse_dyn_cap` at 0 or more, and was checked over every
  month of every point of both models under nine sets of References, met exactly in six of
  the eighteen runs; with both negative it fails, 3.0 against a product of −0.06. A test
  takes point 3 to 1.2 in its cliff month with a spike of 40 and asserts that each check
  raises in both models.
- *Text* (R6). Five bool decodes, `is_db_option_a`, `is_db_option_b`, `is_gpt`,
  `is_level_premium` and `is_single_premium`, carry every branch on S's text columns, each
  reading its column from `model_point()`, as each join reads its key, so that no
  projection cell calls a label accessor, as M14's rule has it, where UL departed from it;
  a value no decode knows raises S's message, in a table-driven `UNDECODABLE` list.
- *The clocks* (D7). The scenario table is keyed by projected `t`, the valuation clock
  already, and T2 and T3 give each restated or future row its own copy, re-based to its
  month by subaccount: point 1 re-opened at 12 on `WE` as shipped reads the worked
  example's month at `t = 0`, where its `net_cf` is 0.152 above S's (§7.6, *E*). Expense
  inflation runs on `t // 12`, where S steps it by policy year, so S's in-force points are
  splice cases with inflation at 0; it ships at 0, and at 2.5% a year point 4's expenses
  are S's divided by `1.025^10` at every `t`. Acquisition is S's formula, charged per
  policy issued, in the issue month and uninflated, which a test checks at inflation of
  2.5%.
- *The first default and shortfall months* count from the valuation date. T2 and T3 exempt
  them, since their values are months on each model's own clock, S point 3 restated at 37
  on the splice finding S's first default at 0 and SEC's at 533, and assert them by their
  formula, the first S month at or after the row's where the flag holds, less it;
  `is_default` and `is_shortfall` are compared month by month.
- *T4* (§5.2, T4, precised). Each counted cell and report column is held to 1e-12
  relative, value by value, but a difference of two scaled products, `av_change`,
  `net_cf`, `net_cf_ga`, `margin_expense` or `margin_mortality`, to 1e-12 of its largest
  magnitude on the point.
- *The rules test* (§5.2, T2, precised). Each row is scanned once it has run on the books,
  its loops over the frame and then every monthly cell at every month from `t_entry()` to
  `proj_len() - 1`, at every subaccount, timing and kind, as Phase 2's sweep will, and
  before it is compared with S: the account value's base at `t == 0`, an R1a fault, passed
  every test while the scan saw the reports alone, since no report reads that balance in a
  later point's issue month. The test asserts its premise, that no cached call of a cell
  keyed by no `t`, the loops excepted, has a precedent keyed by `t`.
- *The splice* (§5.2, T2; the life chassis, *The splice*). Nine variants change S's
  columns only: withdrawals on either option; a single premium with no surrender charge;
  an over-funded Option B point, whose corridor binds; a StdTob point in force 60 months,
  on a second schedule; issue age 10, on COI rows steep enough that the cap binds with an
  effect; the COI pin alone, above the guaranteed rate that bounds it, and the corridor
  pin alone; and Option A withdrawing past its face, whose floor binds in the issue month.
  Each class and sex has COI rows at a scale of its own, and variant 7's stop at policy
  year 50, so that the scale's clamp is read. The splice's References, in both models: the
  behaviour module on, a lapse spike of 3, acquisition at $250, A/E 0.56, charges ceasing
  at attained age 100 and a declared rate of 2.5%, on stepped scenarios, each row's copy
  re-based by subaccount. The two bounds no splice Reference can bind on both sides, the
  guaranteed COI rate over a current scale above it and the declared rate's 1% floor, have
  a default test of their own on the twin of S point 4, which compares every cell of S's
  at atol 0 but S's margin and net-view checks, which fail from `t = 322`, where the loan
  passes the cash value.
- *The cap on mortality* (§5.1, step 6). `mort_rate` caps the annual rate as `VUL_US_S`
  does since §8.2 item 4's fix, `min(q, 1.0)`, the table's rate read at
  `mort_rate_base_at`, so the cap is no departure. Its test takes a StdTob Option A copy
  of S point 3 at A/E 1.0, whose product first passes 1 at `t = 816`, attained age 113, at
  1.09495, and reads it issued at the valuation date and 25 months on, restated the month
  before the cap with S's count, and five months into the capped year with one policy: the
  annual and monthly rates are `(float, 1.0)` there in both models, and every cell agrees
  with S, the capped months included, at 1e-9 relative with no absolute floor. A NaN sent
  through the A/E, a Reference, or through the class factor's formula stays NaN, and so
  does one sent to each bound on the COI rate written second, the scale's and the pin's.
- *Expenses and `result_pols`.* `expenses` is S's formula in S's order behind the guard,
  so T1 holds at any count. `result_pols` gives `pols_if`, then `pols_new_biz`, then S's
  other columns, the rates 0 outside cover; T1 exempts it, and the module compares it with
  S's column by column.
- *The committed rows* (§7.1, *Precised at M3*, item 11). Each derived and future row
  continues its S point from its month, its four reports compared frame by frame to 1e-9
  relative with no absolute floor, which pins point 8's count of 4.006e-10 where T6's
  1e-12 holds it only to about a quarter of a percent, and its first default and shortfall
  months by their formula; the twins are compared cell by cell.
- *The runner* takes `Projection`'s key from the model, freezes the collector before each
  pass, releases and collects each point, in `--block` asks every point for its frame
  first, writes "1 month" in the singular, though no committed row is a month from the
  valuation date to print it, and exits naming the table's labels on a label it does not
  hold, one that is not a number among them, without a traceback.
- *§7.3's carried items* (*Record — M3*), the life chassis, are taken, each in a bullet
  above: the chains one cell a month, the carry into `t = proj_len()` with the splice's
  A/E at 0.56, the guards, S's own `*_init` columns and two on S's stems, `wd_pp_mth()`
  and the schedule's two readers, the cap, the keyed readers and the `Data` cells that
  check their tables, the decodes, the checks' residuals and loan terms, `pols_if_at`'s
  timings, the splice's variants and switches, and UL's tests.
- *§7.9's carried items were taken from the start* (*Record — M11*): T4 at 2.5 contracts
  with every assumption that ships at zero switched on; T2 and T3 at no absolute floor,
  and a fault below it, survival 1% off below 1e-8, caught; each malformed case refused by
  its own rule, which 50 `Data` rules dropped in turn showed, and each read through a
  projection as well; each splice row scanned before it is compared; the collector frozen
  and unfrozen; the core checked by line coverage at the tests stage; and, after the
  review's blocker, each cap or floor bound where it has an effect.
- *Carried items not yet taken.* Built on ed73164, VUL's `_twin` passes
  `codes=codes(sec_proj)` from the build on, but its runner does not carry Term's
  `--cython`, `--build` and `_tool()`, nor its module the `create()`-copy test (§7.1,
  *Record — M14*). §7.12's and §7.11's carried items postdate the build. Of §7.12's five,
  the first, fourth and fifth do not arise: its committed-rows test compares each derived
  and future row's four reports, frame by frame, and its first default and shortfall
  months by their formula, with no exemption set, and VUL sums no payment schedule by a
  loop and keeps no companion. Of §7.11's eight, it meets *Past the frame, and a NaN*, its
  guard test failing a monthly cell read past `t = proj_len()` and each check failing a
  NaN, and *Depth and status*, its ascending sweep measured on both models, a limit of 17
  against S's 16, with no status carried as a column; and *The core by line coverage* but
  for the set-apart edits: at the landing review the core ran all 557 `Projection` lines
  the full grid's 63 rows run, where the tests stage measured 556 on 60, but no run has
  removed the stepped scenarios or the declared rate at 2.5% in turn. Of *Each rule entry
  by entry*, it has the table-driven lists from the start, `MALFORMED`, `UNDECODABLE` and,
  for `NOT_ISSUED`, `PAST_COVER`, since `proj_len()` refuses only a point past its cover,
  the issue age's bound left to its C step (*Carried into Phase 2*). It does not meet
  *Boundaries met exactly*: in one copy, `is_default` at `< 0` for S's `<= 0` and
  `face_reduction_pp`'s guard at `av < 0` for `av <= 0` passed all 285 cases of the
  module, since no row meets those boundaries exactly; and in another, the pins' rule
  refusing a pin at `duration_mth` 0, where it refuses one below 0, passed them and the
  SEC conventions, since no case pins a point issued at the valuation date. The pricing
  path's four shares at `den >= 0` for `den > 0` passed every case, with those two, in the
  landing review's copy. Now its two opening shares, at `BEF_PREM`, each fail the accepted
  edges, whose load of 1 leaves the path's first month nothing to share, so that each
  divides 0 by 0 in policy month 1; its two shares at `BEF_INV`, read only by the path's
  closing balances, `sa_pricing_pp` and `fa_pricing_pp`, which no case reads at a load of
  1, still pass all 285 cases. *`Data`'s state rules against S* was not checked rule by
  rule against S's projections; T2's restated rows read S's own states at the splice's
  References through every rule. The rest it does not yet meet. Its NaN-residual test
  sends the NaN through a Reference, `me_rate_ann`, which runs compiled, but the NaN
  reaches every month's residual, 900 on point 1 and 804 on point 4, so no month shows a
  check failing on the NaN and not on a finite residual; the check-decision test shows
  each check deciding a finite miss as S's does. Its product tests read the committed
  model and `VUL_US_S` in module fixtures, each swept once and held to the module's end,
  where §7.12's record builds those rows in the splice's fixture while S is swept. And its
  module neither records each raise of `model_point_table` and of each table's check entry
  by entry, nor checks its docstrings' tables for text between column spans and its symbol
  map's rows for text in every column, nor parses them with docutils; and it binds the two
  bounds S ships idle in one default test on the twin of S point 4, not in a second splice
  fixture with a core of its own (§7.11). VUL's C step takes them up.

**Measured for K6 and F7.** Every time below was taken with other workflows sharing the
machine's four CPUs, the second fix's at load averages of 1.5 to 3.2.
- *Comparisons.* At the second fix the default module ran 240 passed and its full-only
  cases 43, so each of the full grid's 54 T2 and 9 T3 rows continued S in every cell the
  two share, to 1e-9 relative with no absolute floor, but those a restated or future row
  changes by design, its frame's length, its duration, its opening columns, its scenario's
  id and the first default and shortfall months, these asserted by their formula; the
  in-force twins are compared with T1's exemptions alone.
- *Time.* By default the module ran 240 passed and 43 skipped in 432.05 s and 424.01 s at
  the second fix, peaking at 3.39 GB in one process both times; at the fix stage it ran
  437.8 s and 442.2 s, at the re-review 409.3 s, and at the tests stage, 220 passed and 44
  skipped, in 350.0 s and 384.7 s. Its 43 full-only cases ran alone in 229.7 s, 228.5 s
  and 238.1 s at the fix stage, the re-review and the second fix, peaking at 2.72 GB; over
  the whole grid, at the review, before the fixes added 18 cases, 265 passed in 574.5 s
  and 577.2 s. So the default run takes 424 to 432 s, about 2.4 times the three minutes K6
  projects for each product from WholeLife's module and about 240 to 270 s more than that
  module, with the core already in place. Most of it is fixed: the splice's fixture
  (41.7 s in the second fix's first run), T4 (30.5 s), the committed model's swept fixture
  (27.6 s), the returns and declared-rate test (24.5 s), the accepted edges (20.9 s), the
  runner (18.9 s), the extract (17.2 s), the cap test (15.6 s), the two depth cases
  (13.8 s and 13.0 s) and the bound test (11.5 s), about four minutes together. So a cut
  would come from them, as the fix stage found: from the runner's subprocesses, the second
  half of the returns test or the extract's loop over the points, not from T2 or T3, and
  nothing was moved behind `sec_full`. M13, which measures the matrix, weighs it. The peak
  is reached in committed-model tests that read two more models while the two swept module
  fixtures are alive. The SEC conventions, 32 passed and 1 skipped, took 18.9 s and 21.4 s
  at the docs stage and the review. On ed73164 with VUL added, the uslib suite ran 2,214
  passed and 317 skipped in 1,677.0 s at the fix stage and 1,637.1 s (27 min 17 s) at the
  re-review, and 2,216 passed in 1,651.3 s (27 min 31 s) at the second fix, peaking at
  3.71 GB in one process. On the landing's tree, after d3a7be8, M12 and M8, and before its
  review added two cases to VUL's module, the suite ran 2,798 passed and 459 skipped in
  40 min 08 s (*Verified at landing*, below).
- *Depth.* A cold `net_cf` of the last month runs one cell a month back to `t_entry()` and
  20 or 21 more: 919 cells on point 1's 900-month frame, where `VUL_US_S`'s runs 5,411,
  944 on point 3's and 824 on point 4's. The 20 or 21 end in the first month's deduction,
  `mth_deduction_sa_pp`, `mth_deduction_pp` and `coi_pp`, then the death benefit's
  corridor down to `corridor_factor_at`, `Data.corridor_age_last` and
  `Data.corridor_factors`, or, as deep on point 1, the COI rate down to
  `coi_rate_guar_at`, `Data.coi_rate_last_years` and `Data.coi_rates`. At the longest
  cover, issue age 0 and 1,464 months, it runs 1,484 levels, both at the valuation date
  and issued 120 months on, about 370 KiB of C stack at gcc's 255 bytes a level. Each
  chain's head called alone runs at most 10 above its chain, `sa_pp_at` on point 4. With
  the behaviour module on, the pricing path runs back to issue: a cold `net_cf` runs 938
  on twins 1 and 4, the 923 months from issue and 15 more, and 1,484 at the longest cover.
  Swept in ascending `t`, the committed points run 18 deep with the module off, under a
  recursion limit of 17 (16 fails), where `VUL_US_S`'s need 16 (15 fails); with it on, 39,
  39, 22, 135, 27, 141, 608, 903 and 22 on points 1 to 9, `d + 15` on each point in force
  and 22 on the two whose paths start at issue, the least limits 38 on point 1, 134 on
  point 4 and 21 on points 3 and 9, and at issue age 0, 1,415 on a point in force at 1,400
  and 1,477 on one at 1,463, against 18 and 14 with the module off. `CALL_DEPTH` is 40 and
  `CHAIN_OVERHEAD` 25. In the modelx export the committed points' reports and checks need
  a recursion limit of 61 with the module off and 1,821 with it on, and the longest
  in-force point 44 and 2,981, as the review measured them and the re-review again on the
  fixed model; at the review point 8 alone needed 1,833, and the cold call at the longest
  cover 2,994. The second fix changed no cell's calls (D5 and R2, precised). Phase 2's `t`
  cache is 1,585 values (*Carried into Phase 2*, below).

**Faults.** Each fault went alone into its own copy of the library, and the tests aimed at
it ran through the gate, at most two at a time.
- *Tests stage:* 140 faults and a control. 139 failed some test, each by an assertion:
  among them the collateral restarted at the loan, a subaccount opened from the target
  allocation, the scenario read on the policy clock and the face reverting to the face at
  issue; the pricing path read before issue, both loudly, a recursion without end that ran
  22 minutes before the guard test failed, and quietly, its base widened so that no value
  moved; each opening column ignored; each chain of two or more cells a month, which the
  depth test alone catches; and 50 `Data` rules dropped one at a time, each failing its
  own T5 case. One survived, the core without variant 5's row at 590, since another core
  row also reaches the withdrawal's fallback share; the core without variant 10's row,
  issue age 10, fails the core-reach test. Two faults had passed every test until the
  stage's last changes: the account value's base at `t == 0`, until the rules scan swept
  each row on the books, and a residual floor dropped or raised, until the check-decision
  test.
- *Review (tests lens):* 33 faults and a control. Nine passed the default module, two of
  them the full grid too: the COI scale's run check without its first year (f16); the COI
  pin tested with the corridor pin's flag (f17), over the full grid as well; the COI pin
  unbounded (f23); the current COI rate unbounded by the guaranteed (f24); the declared
  rate's floor dropped (f26); the face's floor dropped (f27); the scenario's extent read
  at subaccount 1 (f28); no spike in the first month on the books (f29), which the full
  grid alone caught; and premium persistency read from policy year 0 (f34), over the full
  grid as well. The corridor pin tested with the COI pin's flag (f25) failed the edges
  test alone.
- *Fix stage:* 18 faults, all caught: the review's ten, the nine survivors and f25, and
  eight of its own. f16 and f34 fail their new `MALFORMED_KEYS` cases; f17 and f25 fail T2
  on variants 11 and 12, each pin alone, f23 on variant 11, and f24 and f26 the bound
  test; f27 fails T3 on variant 13 issued 13 months on, f28 the returns test, the
  subaccounts' paths now ending apart, at 240 and 180, and f29 T2 on S point 3 at 168, now
  in the core. x01, a residual left complex, fails the lapse-past-1 test; x02 to x07, each
  range dropped or its bound made open, the new `MALFORMED_RATES` cases and the at-bounds
  test; and x08, the COI scale's clamp dropped, T2 and T3 on variant 7, whose scale stops
  at policy year 50.
- *Re-review:* nine faults of its own and a control, all caught: the COI pin's bound by
  the guaranteed rate dropped, the pricing rate's floor dropped, the face's floor replaced
  by `abs`, two residuals left complex, the mortality floor made open, the lapse floor
  dropped, the runner's catch of a label that is not a number removed, and the COI floor
  loosened.
- *Second fix:* six faults. y01 and y02, the new floors on premium persistency and on the
  initial surrender charge dropped, fail their `MALFORMED_RATES` cases, and y03 and y04,
  each made open, the at-bounds test. y05, variant 13 withdrawing exactly the issue
  month's account value, so that the cut equals the face, fails the core-reach test; y06,
  the same with the old check, passes it, the gap the re-review found, now closed. f27,
  made again, fails T3 on variant 13 while the core-reach test passes under it, as a reach
  test should. No fault targets the ascending depth's bound alone: each fault of the
  pricing path tried also deepens the cold call, which the depth test catches.

**Carried into ULSG (M5) and IUL (M6).** What VUL adds to the life chassis (§7.3, *Record
— M3*, as this landing precises it). Each item goes to the Life stream from this landing,
with the items *Carried into every product still to come*, below, and each record says
what it took.
- *Pins.* Give each per-point pin a variant of its own, alone, compared with S cell by
  cell, and, where S bounds the pin, as VUL's COI pin by the guaranteed rate, one set past
  that bound (*Every bound binds*, below). S bounds neither of ULSG's, so each takes the
  variant alone: `prem_persistency_override`, read once a point as a value and a flag
  (R8), which `Data` refuses outside its range (§5.1, step 6), and `coi_rate_dp`, the
  decimal places the declared COI scales are quoted to, which S already reads once a point
  as an int, blank as `-1`, exact. Both hold in every month, so a restated or future row
  keeps its S point's value, where VUL's first-month pins keep `t == 0`, are blank on
  restated rows and are refused on a point issued later. VUL's two pins always appeared
  together, and a pin tested with the other's flag passed its full grid; ULSG's point 1
  sets both of its own, and its other points neither.
- *Paths from issue.* Guard a recursion from issue that reads no state, as VUL's pricing
  path, before it computes the policy month, judge it in the rules scan at
  `m - duration_mth_init()` without the look-back, and bound its depth from issue, the
  ascending sweep's as well as the cold call's, with any switch that gates it on (R2 and
  §5.2, T2, precised at M4). Set each keyed reader's range in the guard test from what the
  model itself reads: VUL's pricing path reads `corridor_factor_at` from the issue age,
  and so does T1's comparison, at S's keys. ULSG's shadow account is state, not such a
  path, and keeps its own column.
- *NaNs through References.* Send the cap its NaN through the A/E and the residuals theirs
  through a Reference, each set before the model computes anything, so that both tests run
  compiled, and assert each residual NaN in some month and 0.0, or within its tolerance,
  in every other (§7.12, *Record — M12*): read it where the Reference reaches it only from
  some month on, or on a row issued after the valuation date, whose residuals are 0.0
  before its issue. On S's points, ULSG's `mort_improve_rate_init` reaches the account
  value's and the margin's residuals from `t = 12`, and every Reference that reaches its
  shadow account's, `sg_rate_ann` among them, reaches it from `t = 0`, so that check takes
  its NaN on such a row. IUL's `expense_unit_mth_2` reaches the account value's, the
  components' and the margin's from policy year 11, where the segment ladder's check fails
  too, on its segments' balances, a month before its identity's residual goes NaN. VUL's
  test reads `me_rate_ann` on twins 1 and 4, whose every month it reaches, short of §7.12
  (*Carried items not yet taken*), though on VUL's row issued 25 months on the residuals
  are 0.0 before its issue, at `t = 25`, and NaN from it; and its NaN test of the cap
  keeps a second case, through the class factor's formula, on modelx alone.
- *Lapse.* Where S's lapse rate has no cap, as VUL's has none, test that a rate past 1
  makes the checks raise in both models. ULSG's is capped at 0.5 on its one return,
  `min(lapse_rate_cap, max(lapse_rate_floor, rate))`. IUL's is capped at 1 by
  `min(lapse_rate_cap, rate)` but for the no-lapse guarantee's expiry shock, where
  `lapse_rate` returns the Reference `nlg_shock_lapse` before the cap, so IUL takes the
  test there. None of S's five points takes the shock; point 1 at a premium of 1,000 a
  year takes it in policy year 21, months 240 to 251, every check passing at the shipped
  0.25. A shock of 1.2 is a rate of 1.2 there and the count is complex from month 241:
  `check_av_roll_fwd` and `check_margin` raise, and `check_av_components` and
  `check_seg_ladder`, which read neither the rate nor the count, pass.
- *The cap's month.* On the mortality rates UL, IUL and VUL share, a class factor of 1.75
  at A/E 1.0 first passes 1 at attained age 113, 0.625687 × 1.75 = 1.09495, the month
  VUL's cap test reads on StdTob: IUL's Tob class can take its test there, and ULSG's own
  table needs a month of its own.
- *The COI cap.* Neither `ULSG_US_S` nor `IUL_US_S` caps a COI rate, so neither takes this
  item: ULSG's `coi_taken_pp` bounds the charge taken by the account value, not the rate.
  Where S caps one, as `VUL_US_S` does at `coi_rate_cap`, test the cap with rows steep
  enough to bind before charges cease: VUL's issue age 10, on rows rising 10% a year,
  binds with an effect in 84 months, where rows rising 7.5% a year bind in none.
- *Cost.* A VUL T2 case took 3.9 to 6.8 s at the tests stage and up to 7.2 s at the second
  fix, in the faster of its two runs, the rules scan up to 5 s of it on a full frame at
  the design, and a T3 case 4.6 to 5.1 s, and the module's fixed costs, the splice's
  fixture among them, take about four minutes: time the scan on the prototype, and plan
  the fixed costs with the core from the design (K6).

**Carried into every product still to come.** The first eight came from the review, the
re-review and the fixes they led to, their faults among them, the ninth from the tests
stage's faults, and the last three from the design and the build:
- *Every bound binds.* List every `min` and `max` S writes, and give each a case where it
  binds with an effect, compared with S cell by cell (§7.9, *Record — M11*): a splice
  variant where columns can bind it, and, where a splice Reference can bind only one side,
  a second splice fixture, a pair of models read with References of their own, with its
  own core and reach assertion (§7.11, *Switches and bounds S ships idle*). VUL binds its
  two such bounds in one default test on the twin of S point 4 instead, which asserts that
  both bind, short of that fixture (*Carried items not yet taken*). Four of VUL's bounds
  bound nowhere, the full grid's rows included, so that dropping any one passed the
  default module, its review's blocker.
- *Every value column.* Before writing the record, list every value column of every input
  file a projection reads, the model point table's included, with the rule that holds it
  (§5.1, step 6, precised at M4), and give each column with a range a case past each bound
  among the module's refusals and a read of each bound among its accepted values, as VUL's
  `MALFORMED_RATES` and `AT_BOUNDS` do for its keyed tables: VUL's fix stage held three of
  the five columns that cannot be negative, the re-review found the other two, and the
  landing review the bound at 1 on VUL's load and allocations.
- *Residuals as floats.* Where SEC adds a `*_resid(t)` cell for an S check that is a
  `math.isclose` loop with no residual cell, as the UL family's checks are, return it as
  `float(...)` of its ratio, so that a complex residual raises as S's `isclose` does
  rather than pass its check on its real magnitude (§7.1, *Record — M14*, precised at M4).
  Where S has `*_resid` cells of its own, as `VA_US_S` and `RILA_US_S` do, keep them
  signed differences with their tolerances (§7.1, *Precised at M3*, item 11), with no
  `float(...)`: their checks, `abs(r) < tol` in `VA_US_S` and `abs(r) <= tol` in
  `RILA_US_S`, judge a complex residual by its magnitude, a meaning SEC keeps (§7.11's
  *Checks*): on point 1, a mortality rate past 1 in `VA_US_S`, or a lapse rate past 1 in
  `RILA_US_S`, leaves every S check passing. T1 would not see one made a ratio: S's
  largest on the shipped points, 3.0e-11, is far inside T1's 1e-9 floor.
- *A bound stated only once probed.* State a bound in a docstring, a comment or the plan
  only once a probe has checked it: give the condition with its premises, as a sufficient
  one, and check it over every month of every point of both models under several sets of
  References, the sets that make it bind among them. VUL's first statement of its lapse
  bound was neither necessary nor sufficient, since the spike applies in one month and the
  dynamic cap only with the module on.
- *Reach by the raw value.* In the core-reach test, check each floor and cap by the raw
  value it bounds, a floor at 0 included, never by the bounded output, which equals the
  bound where the bound changes nothing too: a row withdrawing exactly its account value
  kept VUL's check of the face's floor green with the floor idle.
- *Events in their own month.* Put a core row in each event's own month, the spike's, the
  cliff's and an anniversary's, not only the month before: line coverage cannot see a
  branch that differs only in the month it fires, and a spike skipped in the first month
  on the books passed VUL's default run.
- *Keys and clamps.* In every table keyed by policy or completed years, one row a year
  from a fixed first year, add to `MALFORMED_KEYS` a first year written one below it and
  years run from one below it with no gap: 0 for policy years from 1, as VUL's are, and -1
  for completed years from 0, as in `VA_US_S`'s CDSC and `RILA_US_S`'s charge table, keyed
  `contract_year`, where a first year 0 is the shipped form. A table keyed otherwise takes
  the cases its own key rule refuses: RILA's lapse table, also keyed `contract_year`,
  holds band starts, 1, 7 and 8, read at the last on or before the policy year, and ULSG's
  ROP table two anniversaries, 20 and 25, read by membership. Shorten one table below its
  cover, ending on a value other than 0, so that the rule its reader applies past its end
  is read with an effect: VA's CDSC clamps and RILA's charge reads 0 there, but each ends
  on a rate of 0, so that swapping the two rules moves no rate of a shipped point. And end
  one keyed path's subaccounts or segments apart: VUL's module wrote a first year 0 in its
  lapse table alone, and none of the rest, until its review.
- *Shared helpers and the runner.* Give each product's helpers in `sec_support.py` its
  prefix: a later `def` of the same name replaces the earlier one at import, with no merge
  conflict. The runner writes "1 month" in the singular and refuses a label that is not a
  number, naming the table's labels, with no traceback.
- *Core-removal faults.* Drop a core row in a fault only where that row alone reaches some
  branch: VUL's row of variant 5 at 590 shares the withdrawal's fallback share with
  another core row, so dropping it passed, and the fault that shows the core-reach test
  failing drops variant 10's row instead.
- *Policy months in S's cells.* Search every call of an S cell keyed by `t`, whatever the
  calling cell is keyed by, for a policy month or year passed as `t`, not only for a base
  at `t == 0` (R1a): `VUL_US_S`'s `fa_pricing_pp(m)` credits `fixed_return_mth(m)`, which
  a flat input hides, and `RILA_US_S`'s `free_wd_base(t)` reads
  `av_pp_at(12 * cy - 1, "BEF_WD")`, for which §7.8 lists `av_pp_prev_anniv_init`. Test
  each by what it should read. A path made at issue, as VUL's pricing path, takes a
  formula override that moves the rate along `t`, which moves S's path and must leave
  SEC's. A balance at an anniversary takes the year-opening read and a T2 row valued
  mid-year (§7.1's template, item 6, precised at M2; §7.10, *Record — M7*, *Year-opening
  state*), with no override where the balance moves between anniversaries: on
  `RILA_US_S`'s point 3 restated at 18, its month `12 * cy - 1` taken on the valuation
  clock reads policy month 29's 99,123.92 for contract year 2's base, 101,441.58.
- *Months as results.* Exempt a result cell whose value is a month from `twin_mismatches`,
  with its reason, assert it by its formula, compare the flags it searches month by month,
  and let T1 compare it at offset 0: S point 3 restated at 37 on VUL's splice finds its
  first default at S's 0 and SEC's 533.
- *Tables keyed by what the point names.* Where a table's ids name the model point table's
  columns, as VUL's lineup does, read it through a checked copy indexed by the ids read by
  value as int64; and check a scenario keyed by scenario, subaccount and month cell by
  cell, as VUL's `scenario_last_mths()` does, and re-base it per subaccount, as its
  splice's copies do, which VA's return scenario needs (§7.7). Hold a cell's months to
  what its reader reads: VUL's reader reads each month's own row up to the cell's last, so
  its check refuses a gap, where `VA_US_S`'s return and rate scenarios are step functions,
  a row where a level starts, `base`'s returns stepping at months 0, 12, 24, 26 and 27,
  which VUL's check refuses. So VA's check refuses a month below 0 or not whole and a
  repeat in a cell and lets a gap stand, its join refuses a point whose scenario sets no
  level for a subaccount of its fund set by the first month the point is on the books, and
  its reader raises where none is set (§7.11, *Record — M8*, *Scenarios*).

**Carried into Phase 2.**
- *Caches and bounds:* `t` 0..1,584, 1,585 values, the longest frame, issue age 0 issued
  120 months on, and the month after it; the pricing month `m` 0..1,463; policy years
  1..122; attained ages 0..121, ages 0 to 17 read clamped at the mortality and corridor
  tables' first age, 18; the lineup's subaccounts; and each scenario path to its cell's
  last month, read at `min(t, last)`. Issue ages 0 to 85 are the contract's. At stage `E`
  `Data` refuses only one below 0 or not whole, where S refuses none; Phase 2's
  `proj_len()` refuses any outside them, and every size rests on the youngest.
  `sample_sec.py` sets `dyn_behavior_on = True`, so its recursion limit comes from the
  cover from issue: in the export, 2,981 for the ascending sweep of a point in force in
  its last covered month at issue age 0, and 2,994 for the cold call at the longest cover.
  It calls every cell no report reaches (§7.6, *C*).
- *`Data`:* the nine extent and count cells new at M4 become int scalars or vectors by
  point, and `subaccounts`, `scenario_rows` and `scenario_last_mths` arrays by subaccount
  and by scenario (R7); the refusal code stays on the raise paths, the eight value rules
  that now carry a range among them: lapse and mortality, and the model point table's load
  and allocations, from 0 to 1, and `factor`, `coi_rate_guar`, `fund_expense_ann`,
  `prem_persistency` and `sc_per_1000_init` at 0 or more. `gross_return_mth` keeps S's
  per-`t` join keyed by text, reading `scenario_id` from `model_point()`, which R7's
  `ret[scen, sa, t]` replaces, and `subaccount_ids` returns S's list (R10).
- *T1 and codes:* S caches `claims(t, None)` and `me_charge_pp(t, None)`, which need a T1
  `arg_map` at stage `EC` (R12). The two pins' flags call `pd.isna` once a point, and
  become a value array and a 0/1 flag array (R8). S's generator expressions stay in eight
  unchanged or docstring-only cells, the ninth, `av_pp_init`, now a loop (C5, R12).
- *Sums over the subaccounts:* C2 and C4 must not assume that S's `sum()` over the
  subaccounts is a loop's float for a lineup of three or more: Python's `sum()` of floats
  is compensated since 3.12, and on 100,000 random three-balance lineups the two differed
  in the last bit 19,064 times; on the shipped two they agree.
- *A lapse rate past 1* gives NaN and checks that fail compiled, where modelx raises: C4
  must not compare across it.
- *Tests on the compiled model:* the check-decision test moves `inv_income` and the
  returns test the declared rate by formula override, and the NaN test of the COI bounds
  and one case of the cap's replace a formula, so they stay on modelx (C1, K7); the
  residual NaN test and the cap's other case send the NaN through References,
  `me_rate_ann` and `mort_ae_factor`, which run compiled.
- *The corridor's two inputs:* `Data` holds the corridor pin to 0 or more, by the rule it
  shares with the COI pin, and a corridor factor only to be a number, for the reason
  §5.1's step 6 gives; aligning the two, either way, is left open at landing.
- *M14's items for the C step:* the runner's `--cython`, `--build` and `_tool()`, with the
  `create()`-copy test and the compiled runner test's refusal leg; and `proj_len()`'s
  refusal of an issue age outside 0 to 85 (R4; §6.1, steps 6 and 7).

**Carried, outside the SEC models.**
- Ten S-side items for §8.2 item 4, found in `VUL_US_S`, which nothing at M4 edited: the
  last was corrected in `VUL_US_S` at d3a7be8, after the build; the lapse rate's missing
  bound is in both models; and the rest are fixed or refused in `VUL_US_SEC` only:
  - the model docstring says point 3's Option B makes the corridor live; the corridor
    never binds on point 3, the one Option B point S ships, its largest ratio to the death
    benefit 0.287, and binds on the Option A points late, point 1 from `t = 375`;
  - `loan_rate_ann` says "1.05% from the 10th anniversary", where `loan_pref_year = 10`
    gives the preferred rate from policy year 10, at the 9th anniversary; the product spec
    quotes its source as "from 10th anniversary", policy year 11, and the technical notes
    say "from year 10", so if the source means the anniversary, `loan_pref_year` is 11,
    which moves numbers in both models; `VUL_US_SEC`'s docstring says policy year 10, as
    the notes give it;
  - `Projection` says "the cells is kept" at lines 271, 1812 and 1956, and "this cells" at
    line 1298;
  - `premium_pp`'s `LEVEL` and `SINGLE` lines render as one paragraph;
  - `av_pricing_pp` calls itself the denominator of `funding_ratio`, which is the opening
    balance, `av_pricing_pp_at(m, "BEF_PREM")`, and `funding_ratio` says it returns 1.0 in
    the issue month of a new-business point, where it does whenever the path's opening
    balance is at or below 0;
  - `fa_pricing_pp(m)` credits `fixed_return_mth(m)`, the declared rate on the projection
    clock, at the policy month `m` (R1a): on a point in force a declared rate that moved
    would credit the pricing path, a projection made at issue, with rates declared after
    the valuation date; flat as shipped, it changes no number;
  - `check_margin` adds back the whole loan on a lapse, and `check_net_view` on a lapse
    and on a death, so once a loan passes its cash value both fail on a projection that is
    right: with the guaranteed COI scale binding and the declared rate at its floor, twin
    4's loan passes its cash value at `t = 322`, attained age 81, and S's three checks are
    `True`, `False` and `False`;
  - the lapse rate, the base rate times the cliff's spike times the dynamic multiplier,
    has no bound: past 1 the projection turns complex silently and only the checks raise,
    in both models (§7.6, *E*);
  - S checks no input. It reads a negative premium persistency factor as a negative
    premium, point 3's `premium_pp(12)` −250.0 at −0.5 in policy year 2 with the module
    on, every check `True`; a negative initial surrender charge as no charge through the
    schedule and a rising one after it, 1.29 per $1,000 in policy year 16 at −18.00 and
    19.29 by year 30; a run-off of 7.5 years as 7, and one of 0 by dividing by it; a
    `has_surr_charge` of `"False"` as true; ids written `1.0` by raising
    `KeyError: 'sa_pp_init_1.0'`; and a blank face as no death claim on Option A and a
    missing value on Option B. SEC refuses each but the ids, which it reads by value;
    whether S should check its inputs is S's question;
  - `mort_rate` said that no shipped point reaches the cap, where StdNT's rate is exactly
    1.0 at ages 119 to 121; d3a7be8 corrected it, after the build, to say that on every
    shipped point the product reaches 1.0 at attained age 119 and never passes it.

**Landing.** Rebased from ed73164 onto da763e8, after d3a7be8, the third of §8.2 item 4's
commits, M12 and M8. `VUL_US_S` caps its annual mortality with the bound second,
`min(q, 1.0)`, since ed73164, and d3a7be8 corrected its `mort_rate` docstring;
`VUL_US_SEC`'s `mort_rate` caps the same way, `min(q, 1.0)`, through its keyed reader, `q`
being `mort_rate_base_at(age(t)) * class_factor() * mort_ae_factor`, so that fix changed
no formula of `VUL_US_SEC`. uslib's `index.md` took one conflict, the sentence that lists
the SEC models, which now names all eight; `sec_support.py` took two, where VUL's state
extractors and spec follow DIA's and FIA's, all kept; and `VUL_US_SEC`'s `Projection` one,
`mort_rate`, where the enhancement's, which reads `mort_rate_base_at`, replaces the
copy's, `VUL_US_S`'s at the tip. After its review the landing held the premium load and
the allocations to 0 to 1 in `Data`, where they were held to 0 or more only (§5.1,
step 6), with a case past 1 for the load and one for an allocation among the module's
refusals and a load of 1 among its accepted edges, so that `model_point_table` checks the
table by 20 rules and the module has 285 cases, 242 by default, and `Data`'s docstring and
`model-sec.md` give the rule; corrected the comment on VUL's spec in `sec_support.py`,
which said that nothing refuses an issue age outside 0 to 85 at stage `E`, where `Data`
refuses one below 0 or not whole, as *Carried into Phase 2* says; and corrected
`test_mortality_caps.py`'s docstring, which d3a7be8 added after the build's base: among
the SEC cap tests that see their S model's cap and its float bound it now names
`VUL_US_SEC`'s, and `DIA_US_SEC`'s and `FIA_US_SEC`'s, which M12's and M8's landings left
out, and it says that `VUL_US_SEC`'s NaN test, which reads `VUL_US_S` too, sees the order
of `VUL_US_S`'s cap. `INPUT_FILES`, regenerated with
`gen_input_files.py lifelib/libraries/uslib --write` on the merged tree with the review's
fixes, came out unchanged.

**Verified at landing**, with three other workflows, VA's and RILA's builds and the
drafting of this record, sharing the machine. The uslib suite, with modelx-cython
installed and so the compile tests included, gave 2,798 passed and 459 skipped in
2,408.53 s (40 min 08 s), its two warnings modelx's renames of `Term_US_S` and `VUL_US_S`
in the round-trip tests. VUL brings 240 passes and 43 skips in its module, 32 passes and 1
skip in its SEC conventions, the notes-orientation check, which thirteen other models
skip, and one pass in the compiled convention that reads every SEC model. Over its full
grid, VUL's module gave 283 passed in 633.96 s, and the `cython` selection 11 passed and
none skipped under `USLIB_REQUIRE_CYTHON=1`, in 127.24 s. doccheck built 505 pages with 0
warnings. `gen_sec_points.py --check` found the files of the eight SEC models current, and
`gen_sec_fingerprint.py Term_US_SEC --check` reproduced the fingerprint. md_lint reported
0, `gen_scaffolding.py --dry-run` 0 files in each of the six libraries, and
`gen_citation_links.py --dry-run` nothing on its 310 source tags. A case-insensitive
search of `model_point_table_sec.csv` for 39 terms, the build's 27, eight carrier and
product names written out, two of them the build's own in another case, and four host
names of three of the public bodies `variable_ul/sources.md` cites, each name's words
matched also when joined by underscores, dots or hyphens or run together, found none.
These runs came before the landing's review, and before the landing wrote this plan's M4
text, which no test, generator or doccheck reads. With the share rule, its two cases and
the text edits the review led to (*Landing*, above), VUL's module gave 242 passed and 43
skipped in 482.12 s by default and 285 passed in 692.49 s over its full grid, the
conventions of `VUL_US_SEC` and `VUL_US_S` 56 passed and 2 skipped, the notes-orientation
check of each, `test_mortality_caps.py` 32 passed and `test_sec_support.py` 53 passed;
doccheck built 505 pages with 0 warnings, `gen_sec_points.py VUL_US_SEC --check` found its
files current, md_lint reported 0 on uslib, `gen_scaffolding.py --dry-run` 0 files in each
of the six libraries and `gen_citation_links.py --dry-run` nothing on its 310 source tags;
and a case-insensitive search of `model_point_table_sec.csv` for 285 terms that cover
every publisher, product, registrant, form, file and accession number, CIK, host, document
title and file name that `variable_ul/sources.md` cites, each name's words matched as
before, found none. On the tree as committed, md_lint reported 0 on uslib and on this
plan, `gen_sec_points.py --check` found the files of the eight SEC models current,
`gen_scaffolding.py --dry-run` 0 files in each of the six libraries, and doccheck built
505 pages with 0 warnings.

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
- `rb_prev_anniv_init`, the RB at the anniversary on or before the valuation date (D6);
- the highest quarterly contract value so far this contract year, the step-up base;
- `phi_glwb_init`, the VIX-linked fee of the last quarter to end before the valuation
  month, the clip's prior for the first fee on the books, which S recurses from quarter 1
  (precised at M8);
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
  - fund sets to `alloc[fund_set, i]`, with a per-point fund-set number (R7);
  - returns, VIX and CMT, which S finds by a step search on every call, to
    `[scen, sub, month]`;
  - the premium and withdrawal schedules to `[schedule, month]`, with a per-point
    schedule number (R7);
  - GAWA% bands to `[grid, age]`;
  - CDSC to `[sched, yr]`.
- R14 for `lapse_itm_mult(m)` (5,435 cache entries), `fee_rate_vix_raw` and
  `fee_rate_vix_clip`: each inlined into the cached, `t`-keyed cell that calls it, so that
  its float argument, the moneyness or the VIX average, is a local and not a cache key.
  S's tests call all three directly, so S's cells stay for them, admitted by name, or go
  with a T1 exemption (R14). `math.floor` becomes integer arithmetic.
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
- Opening state (D6), thirteen columns beside the count, each what `RILA_US_S` carries
  into month 0: the amounts per contract `inv_amt_pp_init` (also the crediting basis),
  `fixed_acct_pp_init`, `holding_acct_pp_init`, `av_pp_init`, of either sign [S2],
  `av_pp_prev_anniv_init`, the Account Value before withdrawals at the anniversary on or
  before the valuation date, which the free-withdrawal base reads at the absolute month
  `12 cy - 1`, `free_wd_remain_init` and `rop_pp_init`; where the term under way began
  before the valuation month, in DIA's frozen-weight shape (§7.12, *Record — M12*), its
  market, `index_at_term_start_init` (above 0, since `index_perf` divides by it),
  `mvr_at_term_start_init`, `risk_free_at_term_start_init`, `div_yield_at_term_start_init`
  and `impl_vol_at_term_start_init`, under either amortization rule; and `cap_rate_init`
  where that term began at a renewal under `nge_reset`. Terms align with issue, so no
  term-start month is a column, and `RILA_US_S` has no Performance Lock, so no lock is one
  (settled at M10).
- The market scenario, keyed from issue in S, moves to `t` as a companion,
  `market_scenario_sec.csv`, read through S's reader by repointing `market_scenario_file`
  (D8): S's scenarios under their own ids for the twins, and for each derived and future
  row a copy re-based by its `duration_mth`. A term begun before `t = 0` takes its start
  from the model point, one starting at or after it from the scenario. `market_state`'s
  parameter is `t`. Withdrawals, terms, anniversaries and the Maturity Date stay on the
  policy clock, compared with `duration_mth(t)` (settled at M10).
- Splice months: either side of each Term End Date and renewal (35, 36, 59, 60, 71 and 72;
  11, 12, 23 and 24 on a one-year term), months mid-term (5, 30, 40, 59, 80, 107), the
  anniversaries 12 and 24 and a year's last month, the months around each withdrawal and
  the last covered months (119, 359), on stepped copies of the paths in which every field
  steps, each row valued mid-term on a copy whose state at `t = 0` is moved off its five
  term-start columns, its state at `t = 1` written first (§7.11, *Record — M8*), with ten
  variants: a three-year term; a one-year term under `nge_reset`; a behavioural rate above
  the free rate; a Floor option whose cap binds; a crash path, alone, with a behavioural
  rate above the free rate, and with a positive request on a negative account value; a
  withdrawal above the account value; an Edge term ending exactly at its buffer; and a
  withdrawal at a negative interim value on a positive account value, which the accounts
  alone pay (settled at M10).

*C:*
- Strings: six, plus `opt_legs()`, which returns a tuple of strings, and becomes int leg
  codes. `pd.isna` in `is_uncapped`.
- `market_state` builds a list on every call (12,602 cache entries) and becomes per-field
  `market[scen, k]`.
- Timing (14 cells), kind, bucket, leg, market and name parameters.
- Float-parameter cells: `norm_cdf` (5,838 entries), five Black–Scholes cells with six float
  parameters each, `opt_component`, `opt_portfolio`, `credit_rate_at(t, accrual)` and
  `opt_budget_at_cap`. Spot and tau become codes — current or term-start market, τ(t) or
  T — so `(t, leg)` caches become C arrays, and the pure ones are inlined into those cells;
  none is left uncached, which would compile it untyped (R14). S's tests call
  `opt_component`, `opt_portfolio`, `credit_rate_at` and `bs_binary_call` directly, so S's
  cells stay for them, admitted by name, or go with a T1 exemption (R14). Their
  `math.erf`, `log`, `exp` and `sqrt`, 16 uses with `math.inf` and `isinf`, compile as
  Python calls, and C5 refuses the module: RILA's Phase 2 decides between admitting
  `math` by cell in C3 and C5, as WholeLife's dividend admits `round` (R16), and a C form,
  and measures what it keeps.
- `declared_cap_solved` repeats an 80-step bisection in every month of a renewal term; it is
  keyed on the term start, a speed-up that changes no number.
- **Existing defect to fix in S first:** the Projection docstring's `\|` (line 150) is an
  invalid escape. It raises a `SyntaxWarning` on every import, the only such case in the six
  libraries, and the SEC copy would inherit it. *Fixed on 2026-11-03 (§8.2, item 4): the
  docstring is a raw string, the same text at run time.*

#### Record — M10, done 2026-11-04

Built in two commits, as D1 requires: `RILA_US_S` copied with only `_name` changed, then
the enhancement, by M1's process: a design prototyped and critiqued before the build,
tests written against the build and checked by injected faults, then a review under the
three lenses. The design departed from §7.8's *E* where reading `RILA_US_S` cell by cell
showed it short: the term-start market is carried in full under either amortization rule,
not the budget alone, since `updated_expiry` reprices from it; the term-start values and a
re-solved cap are columns only where the term under way began before the valuation month,
in DIA's frozen-weight shape; terms align with issue, so no term-start month is a column;
the account value takes either sign, since the interim value can fall below 0 under the
contract, where D6 refused a negative balance and §7.10's chassis had RILA follow MYGA;
the market is a companion, which D8 listed for VA and FIA alone; and month 0 prices the
term's option, so the depth bound's overhead is 24, not the 16 D5 gave at e011a0c. So
§7.8's *E* takes three bullets as built, and D5, D6, D8, K5 and §5.2's T4 and T5 take
precisions. The review made 25 findings, 4 of them blockers and 3 major, and three were
each made under two lenses. The generated table copied two provenance cells of
`RILA_US_S`'s that named one carrier's crediting option and another carrier's defined
term, which `CLAUDE.md` forbids in an input file, and two crediting-option labels it left
for a ruling; the floor on the option's share of a withdrawal never bound with an effect,
so that dropping it passed every test, the full grid's included; no case was refused at
the Maturity Date itself, nor at the first anniversary, where the remainder and
anniversary rules start, so that moving either window, or admitting the Maturity Date,
passed the default module; the renewal identity refused 8 of 74 renewal valuations carried
to the cent; `nge_reset` written 1 or 0, which `Data` documents, was written by no test,
so that a decode refusing 1 and 0 passed; and the depth test left out the deepest
committed row, under comments that misstated the depths. The fix stage applied all but two
and rejected a detail of a third with evidence: the provenance is S's, which the SEC table
copies and RILA's build could not edit, so a commit of its own at landing rewords all four
cells in `RILA_US_S`'s table (*Landing*, below); running the docutils parse test in CI
changes files shared across products, and is left to M13, as FIA's module leaves it; and a
cent and a half, the review's slack for the renewal identity, would refuse a valid extract
at half-even ties, so the identity holds to two and a half cents. A re-review found every
fix right and complete, and made two more findings, both minor, on the wording of a
carried item and a test's docstring, which a second fix applied. Nine defects found in
`RILA_US_S` are carried below: one, the provenance, is corrected in `RILA_US_S` itself, in
the landing's commit before the copy; three, on a negative account value, are in both
models; and the other five are fixed or refused in `RILA_US_SEC` only. M10 was built on
e011a0c, M12's landing, before M8 and M4 landed, and rebased at landing onto VUL's
(*Landing*, below).

**What exists now.**
- `RILA_US_SEC` at stage `E`. Of `RILA_US_S`'s 156 `Projection` cells, 63 are unchanged,
  21 have new text only and 72 are rewritten; none is removed or renamed. It adds 36
  cells, 192 in all: `policy_count`, `duration_mth_init`, `maturity_mth`, `t_entry`,
  `is_active` and `pols_new_biz`; the thirteen opening-state accessors; ten bool decodes,
  `is_cap_crediting`, `is_step_crediting`, `is_edge_crediting`, `is_floor_crediting`,
  `is_iv_portfolio`, `is_iv_notional`, `is_iv_delta`, `is_iv_legacy`, `is_straight_line`
  and `is_updated_expiry`; four keyed readers, `mort_rate_base_at`, `surr_charge_rate_at`,
  `lapse_rate_base_py` and `wd_amount_pm`; and three readers of a term's start,
  `risk_free_at_term_start`, `div_yield_at_term_start` and `impl_vol_at_term_start`,
  beside S's `index_at_term_start` and `mvr_at_term_start`, rewritten to read so. Its
  References are S's, `math` among them, at S's values. `Data` keeps S's eight cells:
  three unchanged, four with a new docstring and `model_point_table` rewritten to check
  the table as it reads it, in 37 refusals in turn. It adds six count cells, 14 in all,
  `market_scenario_count`, `mort_table_count`, `surr_charge_count`, `guar_min_rate_count`,
  `lapse_table_count` and `withdrawal_count`, each beside S's reader of its table,
  unchanged, and the Reference `future_horizon_mth = 120`; `model_point_file` and
  `market_scenario_file` name the two `_sec` files.
- `model_point_table_sec.csv` holds 24 rows generated from RILA's `SecSpec`. Fifteen are
  S's points as twins, issued at the valuation date, since `RILA_US_S` has no point in
  force. Eight are derived: the anchor, S point 1, in the last month of its first term, at
  71, the Term End Date at +40% falling at `t = 0`; S point 2 on its third anniversary,
  after the $8,000 withdrawal of the month that closed on it, at 36; S point 13, under
  `nge_reset`, mid-term after its first renewal, its cap re-solved there at 99.7038%, at
  80, and valued at that renewal, at 72; S point 4, a Step option on a one-year term, with
  30,835.04 in its Fixed Account from two term ends, at 30; S point 15, the pre-AG 54
  engine, in the month that closes on its fifth anniversary, the [S2] withdrawal charge
  example falling at `t = 0`, at 59; S point 12, the uncapped option at issue age 81,
  mid-term, at 40; and S point 7, interim value family (b), in its last covered month,
  at 119. The last is the anchor issued 13 months on. Its companion,
  `market_scenario_sec.csv`, holds 27 rows: S's four scenarios as they stand, for the
  twins, and for each derived and future row a copy re-based by its `duration_mth`,
  `{id}-M{d}` or `{id}-F{k}`. A case-insensitive search of both files for the publishers,
  products, options, accounts and defined terms that
  `registered_index_linked_annuity/sources.md` and its research notes cite, 116 names at
  the second fix, each name's words matched also when joined or run together, found four
  provenance cells of the table, copied from S's points 4, 5, 7 and 12, that named the
  cited carriers' crediting options and one carrier's defined term; regenerated from S's
  table as the landing's commit rewords it, the table holds none (*Verified at landing*,
  below).
- `tests/test_registered_index_linked_annuity_us_sec.py` has 44 tests in 305 cases, 230 by
  default and 75 behind `sec_full` (K6). T2 runs on 101 rows restated from S's fifteen
  points and ten variants, at the months of their events, a core of 37; T3 on 16 future
  rows, seven S points and seven variants 13 months on and the anchor 1 and 120 months on,
  a core of 6. S has no in-force point, so `IN_FORCE_TWINS` is empty. A test asserts that
  the core reaches every crediting method, interim-value family, amortization rule, sex,
  scenario, programme, term and kind of valuation month, `nge_reset` both ways, an
  uncapped option, participation above 1 and an issue age past the return-of-premium band,
  and on the splice's model 20 conditions at the valuation date and 38 bindings and
  branches in the frame; at the fix stage line coverage showed it running all 641
  `Projection` lines and 273 `Data` lines the full grid runs. T4 runs at 2.5 contracts. T5
  covers 100 malformed model point tables, each refused by its own rule, as a map of each
  case's first raise showed; 41 malformed assumption tables, each refused by its count
  cell naming the file's lines; 5 points `proj_len()` refuses, at and past the Maturity
  Date and with a remainder above the year's allowance, on the first anniversary among
  them; and 3 values no decode knows, each raising S's message. An every-state test
  restates each S point of the splice at every month of its first year, every sixth month
  and every year's last month, and `Data` and `proj_len()` accept each state but a
  contract a full withdrawal emptied, which it shows refused. The accepted edges read a
  renewal valuation with every amount carried to the cent, `nge_reset` written 1 or 0 and
  1.0 or 0.0, and a buffer and a floor of 0. A NaN residual fails every check, a NaN A/E
  stays NaN through the cap, and at 10^8 contracts both roll-forward checks close on their
  scaled tolerance, each residual above its unscaled one on some row. The SEC conventions,
  33 cases, pass but for `test_net_cf_is_income_positive`, skipped as on `RILA_US_S`,
  since neither model has the notes-orientation companion cells.
- `run_sec.py`; `model-sec.md`, with *The opening state*, which shows each column on a
  committed row with what it gives when wrong: point 16's `I_s` of 100 credits 40%, an
  interim value of 140,000.00 at `t = 0`, which 80 would make 75% and 175,000.00; point
  22's `r_0` of 4.00% against a current 5.00% gives its interim value a rate adjustment of
  0.975582 and 78,979.80, where 5.00% would give 81,145.33; point 18's re-solved cap of
  99.7038%, at 20%, would value its short call at the cap at −14,233.12 rather than
  −2,688.05; point 17's remainder of 480.31 of the year's 8,480.31 makes a surrender's
  charge at `t = 0` 3,820.47, against 3,420.47 with the allowance whole; and the two
  columns that reach no report, `av_pp_init` and `av_pp_prev_anniv_init`, which `Data`
  holds instead; the registry entry with its `INPUT_FILES`; and four generated pages.
  doccheck reported 501 pages and 0 warnings on e011a0c with RILA added.
- Shared files, added to in place: in `sec_support.py`, RILA's state extractors,
  `_rila_entering`, `_rila_prev_anniv`, `_rila_mid_term`, `_rila_term_start`, `_rila_cap`
  and `_rila_scenario_id`, its companion's builder, `_rila_rebased_scenarios`, and
  `_RILA_STATE`, after VUL's, and its spec after VUL's, the spec's comment giving the
  state, the rows, the companion, T1's one exemption, the keys S caches under `None`, the
  text still compared, the float-parameter cells and Phase 2's sizes with their inputs;
  FIA's `SecSpec.future_state`, which RILA's future row needs, copied byte for byte from
  FIA's tree before FIA landed and kept once at landing, with FIA's two additions to
  `test_sec_support.py`; in `us_registry.py`, the entry directly after `RILA_US_S`'s, with
  no flag of its own, since its `pols_if` is `BEF_DECR`, and its `INPUT_FILES`; and in
  uslib's `index.md`, the RILA row of the models table, the sentence on the SEC models and
  the inputs row, which names RILA's market scenarios beside FIA's. Outside RILA's files,
  a commit of its own before the copy rewords the provenance of `RILA_US_S`'s points 4, 5,
  7 and 12 by design, each now naming the design its point exercises as the technical
  notes define it, and keeping its source keys, as dd90cfe reworded point 9's provenance;
  no value a model reads moves (*Landing*, below).

**Departures and precisions.**
- *The clocks* (D3, D7; R1a). `duration_mth(t) = duration_mth_init() + t`, a closed form,
  and `maturity_mth()`, new, keeps S's frame from issue, `12 × policy_term()`, so that
  `proj_len()` is the months from the valuation date to the Maturity Date. Every test of a
  month against a contractual date reads the policy clock, the maturity included: the
  terms and their Term Start and End Dates, the anniversaries, the withdrawal programme,
  read by `wd_amount_pm(duration_mth(t) + 1)`, and the free-withdrawal base, which S reads
  as `av_pp_at(12 cy - 1, "BEF_WD")`, a policy month passed as `t`, and SEC at
  `12 cy - 1 - duration_mth_init()`, or from `av_pp_prev_anniv_init()` where that month
  precedes `t_entry()` (§7.6, *Record — M4*, *Policy months in S's cells*). Expense
  inflation is `(1 + i)^(t // 12)` on the valuation clock, where S steps it on the
  contract's anniversaries, so point 16's expenses are S's divided by `1.025^6`, or by
  `1.025^5` at `t = 0, 12, 24, …`; the purchase payment, its premium tax and acquisition
  fall on `pols_new_biz(t)` in the issue month, per contract issued, uninflated.
- *The count* (D5; §7.12, *Record — M12*, *The count*). MYGA's chain, one cell a month,
  where S's ran through two: `"BEF_NB"` forms the survivors of month `t - 1` itself,
  `"BEF_DECR"` adds new business, and S's three later timings are kept, guarded outside
  cover, their branch a comparison chain rather than a tuple display. `pols_if` is
  `"BEF_DECR"`, a decrement chain's count, with no registry flag.
  `check_pols_roll_fwd_resid` and `av_at`'s `"AFT_WD"` read `pols_if_at(t + 1, "BEF_NB")`,
  where S reads `pols_if(t + 1)`, which would count the next month's new business as a
  gain of month `t`.
- *The opening state* (§7.8, *E*; D6) is thirteen columns beside `policy_count` and
  `duration_mth`, each what `RILA_US_S` carries into month 0, read as S's own formulas
  read it: six amounts per contract, S's close of month `d - 1`, `inv_amt_pp_init`, also
  the crediting basis, `fixed_acct_pp_init`, `holding_acct_pp_init`, `av_pp_init`,
  `free_wd_remain_init` and `rop_pp_init`; `av_pp_prev_anniv_init`, S's base at the
  anniversary that opened the contract year, or the purchase payment in the first year;
  and, where the term under way began before the valuation month, its five term-start
  market values and, at a renewal under `nge_reset`, `cap_rate_init`. Those six take DIA's
  frozen-weight shape (§7.12, *Record — M12*, *Term-start inputs*), not M7's value
  entering month 0: a blank is the honest value where the scenario supplies the start, so
  `Data` holds every given index above 0 with no exception; the values are facts fixed at
  a past date, which a change to the market at the valuation date must not move; and their
  presence is checked both ways, so a twin written in M7's form is refused. The full
  term-start market is carried under both amortization rules, since `updated_expiry`
  reprices from it and T1 and T2 read it at S's `"TERM_START"` keys; the cap only where a
  renewal under `nge_reset` re-solved it, since elsewhere it is the model point's rule. No
  term-start month is a column, terms aligning with issue, and no lock is one, `RILA_US_S`
  having no Performance Lock.
- *Either sign* (D6, precised). The interim value can fall below 0 under the contract
  [S2], and S carries a contract through it, so `Data` accepts any finite `av_pp_init` and
  `av_pp_prev_anniv_init`, holds the investment amount, the two accounts, the remainder
  and the return-of-premium base at 0 or more, and refuses instead a contract in force
  that holds no investment amount and no account balance. `RILA_US_S` reaches that state
  only by a full withdrawal, and keeps the contract in force holding nothing, as variant
  21 from policy month 30. `Data` refuses it by design, a departure from S, since a
  contract that holds nothing is no longer in force: the every-state test sets the state
  aside by name and shows it refused (§5.2, T5, precised).
- *The anniversary and renewal rules* (D6, precised). On an anniversary valuation,
  `duration_mth` a positive multiple of 12, `av_pp_prev_anniv_init` is the base before the
  anniversary month's withdrawal and `av_pp_init` the value after it, so `Data` checks
  that the base is at least the value, to a cent, where D6 has the two agree: they differ
  by the withdrawal, as on point 17 by its $8,000. On a renewal valuation, a positive
  multiple of `12 × term_years`, the month before closed a term, where the interim value
  is the Investment Amount, so `av_pp_init` is the investment amount plus the two
  accounts, to two and a half cents, the one rule of RILA's that ties more than two
  amounts; every other rule between amounts holds to a cent.
- *`proj_len()`* refuses, naming the point, a point at or past its Maturity Date, and from
  the second contract year a remainder above the year's Free Withdrawal Amount,
  `free_wd_rate × av_pp_prev_anniv_init()`, to a cent, each a rule that needs a
  `Projection` Reference. The remainder rule applies only where the base is 0 or more: on
  a negative base S's allowance is negative, and a behavioural rate above the free rate
  leaves a positive remainder no allowance bounds, a state S reaches, as variant 22 does,
  restated at 24 and 30 and accepted. With the S-side fix of the negative allowance
  (*Carried, outside the SEC models*), the rule would apply at every base, against the
  floored amount, `free_wd_rate × max(0.0, av_pp_prev_anniv_init())`, and its guard, the
  guard's docstring sentence and `model-sec.md`'s note would go: the guard dropped alone
  would refuse the remainder of 0 the fix leaves on a negative base.
- *`Data` checks the model point table* (§7.1's template, item 9) in 37 refusals, in the
  template's order, the first that fails raising and naming the missing column or every
  point at fault: the fifteen in-force columns, a unique `point_id`, the count, a whole
  duration and the horizon; the terms, `term_years` before every check that reads the term
  clock: the issue age, whole and 0 or more, and the term, whole and 1 or more, each read
  by value where S truncates by `int()`; the premium above 0; the buffer and the floor,
  fractions 0 or more and below 1; the participation above 0; the cap blank or 0 or more;
  the step, the edge and the behavioural rate 0 or more; `nge_reset` read by value, `True`
  or `False`, 1 or 0, 1.0 or 0.0, where S's `bool()` reads any text as `True`; and
  `nge_reset` set only on a capped `CAP` option, which S projects silently, its solver
  pricing the cap portfolio on a Floor option and doing nothing on a Step, an Edge or an
  uncapped one. Then the opening state: the balances 0 or more and the account values
  finite; each term-start value in its range, the index and the volatility above 0, the
  rates above −1; nothing held before issue; the term-start values and the cap given
  exactly where they are read; a contract in force holding something; the
  return-of-premium base at most the premium; in the first contract year a remainder of 0
  and the purchase payment as the base; both accounts 0 before the first Term End Date;
  and the renewal and anniversary rules. Last, each point's keys, each table's count cell
  asked first: its scenario, which must set its levels by the point's first month on the
  books, its programme, its term among the guaranteed minimums, its sex and attained age
  in the mortality table, and a re-solved cap at least its term's guaranteed minimum. Left
  to the projection, as in S: a mortality table that stops before the maturity age.
- *The tables* (§7.1, *Precised at M3*, item 9). Each of the five assumption tables and
  the scenarios has an int count cell beside S's reader, unchanged, as DIA's and UL's do,
  and the one cell that reads the table asks it first: the new keyed readers,
  `mort_rate_base_at(x)`, `surr_charge_rate_at(cy)`, `lapse_rate_base_py(y)` and
  `wd_amount_pm(m)`, and S's `guar_min_rate` and `market_state`, rewritten to. Each count
  cell reads its keys by value once and refuses, naming the file, the column and the
  lines: a key blank, text or not whole, a key on two rows, a gap where its reader reads
  every key, a sex other than `M` or `F`, a surrender charge table whose years do not run
  from 0, one row a year, which S would read as no charge in the missing year, and a lapse
  table whose first year is not 1; and a value blank, text, infinite or out of its range,
  but a mortality rate above 1, which is accepted and capped, where §5.1's step 6,
  precised at M4 after RILA's build, refuses a probability past 1.
- *Text* (R6). The ten decodes carry every branch on `crediting_type`, `iv_family` and
  `amort_rule`, each reading its column from `model_point()`, as each join reads its key,
  so that no projection cell compares the model point's text or calls a label accessor; a
  value no decode knows raises S's message where S raises it, in a table-driven
  `UNDECODABLE` list. The text a projection cell still compares is S's own: the timing,
  kind, bucket, leg and market strings, which R9 numbers, and `opt_legs`' tuple of leg
  names (R10).
- *The market* (D7; D8, precised). The scenario is a path in calendar time, so it moves to
  `t`: `market_state`'s parameter is renamed `t`, as SPIA's time-point cells' were, so
  that the twin comparison shifts it and the rules test reads it as a month, every caller
  passing it by position. It joins on `model_point()['scenario_id']`, after
  `Data.market_scenario_count()`, S's step search kept. Its file is a companion,
  `market_scenario_sec.csv`, read through S's reader by repointing `market_scenario_file`:
  S's four scenarios under their own ids for the twins, and for each derived and future
  row a copy re-based by its `duration_mth`, the future row's named through
  `SecSpec.future_state`. A term begun before `t = 0` takes its start from the model
  point, one starting at or after it from the scenario, at the time its Term Start Date
  falls at.
- *Guards* (R1). Outside cover every count, rate, factor and amount of a month is 0.0 and
  every flag `False`, but the two surrender multipliers, 1.0, each returned before any
  market, rate or table is read; the clock's arithmetic and the six market readers have no
  guard, and no cell calls them there, and `duration_mth` and `inflation_factor`,
  unguarded too, are defined in every month. `result_iv` writes `index_level` 0.0 there,
  since a future row's copy holds no level before issue. `check_pols_roll_fwd_resid` and
  `av_at`'s `"AFT_WD"` are 0.0 outside cover before they read `t + 1` (§7.11, *Record —
  M8*, *Checks*), so every monthly cell holds `t` to `proj_len()`, and only `market_state`
  the instant `proj_len() + 1`, which the five scenario readers read when Phase 2's sweep
  calls them at `t = proj_len()`; the guard test fails a month-keyed cell that holds a
  month past `proj_len()`, and `market_state` an instant past `proj_len() + 1`.
- *The checks* (§7.1, *Precised at M3*, item 11; §7.1, *Record — M14*, precised at M4).
  S's three residual cells stay signed differences with no `float(...)`, and S's
  `all(abs(r) <= tol ...)` is kept, so a NaN fails each check. The two roll-forward
  tolerances scale with `max(policy_count(), 1)`, since each residual is an aggregate over
  the point's contracts: at a million contracts S's fixed 1e-12 on the count fails on 23
  of the 24 committed rows, all but row 23, whose one-month frame closes exactly. The
  term-end identity, per contract, keeps S's tolerance.
- *The cap on mortality* (§5.1, step 6). `mort_rate` caps as `RILA_US_S` does since §8.2
  item 4's fix, `min(rate * mort_ae_factor, 1.0)`, the bound second, behind the guard,
  `rate` read at `mort_rate_base_at(age(t))`, so the cap is no departure. Its test reads
  both models at an A/E of 10.0, under which the product first passes 1 in months 348, 108
  and 96 on points 1, 7 and 12: the annual and monthly rates are `(float, 1.0)` from
  there, every contract in force dies in the capped month, on each point's twin and on the
  point restated the month before the cap, and every cell agrees with S, the capped months
  included, at 1e-9 relative with no absolute floor; read with a NaN A/E, both models'
  rate is NaN.
- *Chains of one cell a month* (D5, precised). The Investment Amount, which ran through
  three cells a month in S, the two accounts and the free-withdrawal carry, which ran
  through two, and the count each form the previous month's close themselves, S's
  arithmetic in S's order. `CHAIN_OVERHEAD` is 24, against Term's 16, UL's 20 and VUL's 25
  (D5, precised at M10): the chains are one cell a month, and the overhead is month 0's
  pricing of the term's option under the interim value, 13 to 21 levels on the committed
  points (*Measured for K6 and F7*, below).
- *T4 and T5* (§5.2, precised). T4 multiplies the count by 2.5 with premium tax and the
  Holding Account's share switched on, and holds `av_change`, `net_cf`, `claims_over_av`
  and the two aggregate residuals, differences of counted values, to the residuals' 1e-9
  floor, every other counted cell to 1e-12 relative and every other cell bit for bit; and
  the roll-forward checks close at 10^8 contracts, where each residual exceeds the
  tolerance it would have had unscaled, as at a million contracts the Account Value's did
  not. T5 refuses each window rule just inside each end of its window and accepts it just
  outside, but for the first-term rule at month 1, its first: the first-year rules at
  months 1 and 11, accepted at 12; the first-term rule at its term's last month, 71, and
  11 on a one-year term, accepted at that term's renewal, 12; the anniversary rule at 12
  and 36, accepted at 11 and 13; and the remainder rule and the cover check at the first
  anniversary and the Maturity Date, where each starts, the cover check accepted at 119.
  It accepts every state S reaches on the splice's inputs but the one set aside by name.
  It pins from both sides the cents of the remainder, the return-of-premium base and the
  anniversary rule, and the renewal identity's two and a half cents; the first-year rules,
  refused at a remainder of 100.00 and at a base two cents off the premium, and the
  first-term rule, refused at an account of 1.00, are accepted only where they hold
  exactly. These and the first-term rule's month 1 are short of T5 as precised, which M13
  takes up (§5.4).
- *The rules test* (§5.2, T2) holds every splice row to R1, R1a and R2: no call at a
  negative month, none from `t_entry()` on reading a month before it, none at `t` reading
  beyond `t + 1`, read directly or through a precedent keyed by no month, followed to
  every month-keyed call it reads (§7.12, *Record — M12*, *Tests*), and no table read at a
  key the contract does not have. RILA admits no look-ahead. Each row is swept and
  recorded before it is compared with S, since the comparison plants S's keys in SEC's
  cache.
- *The splice* (§5.2, T2; §7.8, *E*). Ten variants change S's columns only: a three-year
  term at a 55% cap; a one-year term under `nge_reset`; a behavioural rate of 15%, above
  the free rate; a Floor option on a three-year term whose cap of 8% binds; the crash
  path, alone, with a behavioural rate of 15%, and with a $5,000 request at policy month
  end 22 on a negative account value; a $250,000 withdrawal at month end 30, above the
  account value; an Edge term ending exactly at its 25% buffer; and a $5,000 withdrawal at
  month end 42 at a negative interim value on a positive account value, which the accounts
  alone pay. Its References, in both models: inflation at 0; the Holding Account's share
  of a term end switched on at 4%, the Fixed Account's moved to 11%; premium tax at 2%; an
  A/E of 1.05; a lapse shock of 27.5, which takes the shock year to `lapse_rate_max` where
  the moneyness factor is about 0.91 or more and not elsewhere; the moneyness floor at
  0.9, which binds on the down paths; the trading cost at 0.15% and the interim value's
  expense rate at 0.08%, the credit spread at 1.2% and the free term-end lapse at 12%,
  each set apart from the Reference it ships equal to; and a declared account rate of
  0.5%, so that the account rate's 1% floor binds. Its tables: paths in which every field
  steps; contract year 1's surrender rate at 1.5% and year 0's withdrawal charge at 7.5%,
  each set apart; the one-year term's guaranteed cap, step and edge raised to 11%, 8.5%
  and 6.5%, so that each binds, and the longer terms' edge floors set apart from their
  step floors; and the variants' three programmes. Each row valued mid-term, 78 of the 101
  and 31 of the core's 37, runs on a copy whose state at `t = 0` is moved by a quarter in
  each field off its term-start columns, after that state is written to `t = 1` where the
  copy has no row there, and its comparison leaves out `market_state` at `t = 0` alone.
- *The committed rows* (§7.1, *Precised at M3*, item 11). Each derived and future row
  continues its S point from its month at the shipped assumptions, its four reports frame
  by frame and every other cell at every argument S cached, to 1e-9 relative with no
  absolute floor, the residuals at the floor, on its own copy of its scenario from the
  committed companion, the cells expense inflation moves left out; the future row takes
  T3's exemptions, which the helper takes as a parameter.
- *The runner* takes `Projection`'s key from the model, freezes the collector before each
  pass, releases and collects each point, in `--block` asks every point for its frame
  first and sums the frames by `groupby`, routes every count of months it prints through
  `months()`, and refuses a label the table lacks, naming its labels, and one that is not
  a number with its usage line, without a traceback. It prints the option budget of the
  term in force on the notional entering `t_entry()`, which a withdrawal since the term's
  start reduced.
- *Text-only changes.* S's 38 lines over 92 characters, 2 in `Data` and 36 in
  `Projection`, 33 of them in the symbol map, are wrapped in SEC only, and five inherited
  docstring defects corrected in SEC only (*Carried, outside the SEC models*), and the
  symbol map gives `claim_pp`, `claims_from_av` and `claims_over_av` rows of their own
  (§7.11, *Record — M8*, *Docstring tables*). `result_pols` gives `pols_if`, then
  `pols_new_biz`, then S's columns; T1 exempts it, and the module compares it with S's
  column by column. `INPUT_FILES` was written by `gen_input_files.py --write`.
- *§7.10's carried items* (*Record — M7*), the deferred chassis: every chain one cell a
  month; the past fixings, the term-start market and the re-solved cap, read only where
  their fixing precedes `t_entry()`, with core rows inside a fixed period, the anchor at
  40 and the reset point at 80; the year-opening state as `av_pp_prev_anniv_init` and
  `free_wd_remain_init`, with the anchor in a year's last month, 11, in the core; `Data`'s
  money rules to a cent, the renewal identity's two and a half apart, each carried value
  held where its rule fixes it, each window rule refused just inside each end and accepted
  just outside, but the first-term rule at month 1 (*T4 and T5*, above), and each rule's
  removal run as a fault; each point's join keys checked last, and what `Data` cannot
  check said; the tables through count cells beside S's readers, which §7.1's item 9
  admits beside MYGA's checked copies, with a `TABLES` case for each kind of fault, each
  refused through a projection too, and keys written as floats; the decodes, each join key
  read from `model_point()` in the one cell that reads its table, and the text still
  compared named in the spec's comment; and of its *Tests*, acquisition per contract at
  2.5 contracts, the scaled checks at 10^8 contracts, each spliced row's scenario re-based
  and stepped, S's unreached cells and arguments evaluated in `_sweep`, every per-month
  charge, ratio and clamp guarded, the depth at the longest cover at issue age 0 on
  mortality extended below the table, the cap as `RILA_US_S`'s, each T5 case refused by
  its own rule and every count of months the runner prints through `months()`. It departs
  from *A zero account value* (*Either sign*, above), and its rules test walks precedents
  by a helper of its own, `_months_read`, admitting no look-ahead, where the item copies
  `_month_reads`. Its future rows are seven S points and seven variants 13 months on, with
  the anchor 1 and 120 months on, not every point and variant: RILA's C step probes the
  future rows of the other eight S points and three variants.
- *§7.9's carried items* (*Record — M11*): of the payout chassis, its *RILA (M10)* item,
  SPIA's decodes, the age-keyed reader, valuation-clock inflation and `proj_len()`'s
  refusal of a point at or past its maturity, the maturity kept as RILA's own claim with
  no hand-off to `SPIA_US_SEC`, and the term-start index level and MVR of a term begun
  before `t = 0` as opening-state columns, and of its *Tests* the guard test on future
  rows 13 months on; the rest of the chassis does not arise, RILA's count being a
  decrement chain and RILA having no survival per life, certain period, static schedule,
  payout clock, commutation, reference rate or mortality improvement. And the items every
  product takes: T4 at 2.5 contracts with every assumption that ships at zero switched on,
  asserting every counted cell; T2 and T3 at no absolute floor, the residuals at 1e-9, and
  a fault below the floor, which the cap test catches; each cap or floor bound where it
  has an effect, after the review's blocker, but `roll_fwd_tol`'s floor (*§7.6's carried
  items*, below); each malformed case refused by its own rule, which the drops showed, and
  read through a projection as well; each splice row recorded before it is compared; the
  collector frozen and unfrozen; and the set-apart edits checked to move no branch and the
  core chosen by line coverage. A level change since each point's start does not arise:
  `RILA_US_S` carries none in one Reference, its market being a path.
- *§7.12's carried items* (*Record — M12*): the term-start inputs in DIA's frozen-weight
  shape, above; S's readers unchanged, with a count cell beside each, DIA's form, which
  §7.12 asks the record to name; every flag column validated by value and decoded from the
  checked value, and the option combination the product's interlock forbids refused by
  name; the rules test walking each precedent keyed by no month to the month-keyed calls
  it reads; the cap tested over both models; both of §7.1's item 11's tests from the
  start, every committed derived and future row compared with its S point frame by frame,
  the future row with T3's exemptions, and a residual that is not a number failing each
  check, sent through References set before the model computes anything, `mort_ae_factor`
  and `trading_cost_rate`, each check asserted only where its residual goes NaN; and the
  count a decrement chain, `BEF_DECR`, with no flag. Far-ahead pricing and a residual that
  sums ahead do not arise: RILA prices each month's options in closed form from the
  month's market and the term's start, re-solving a cap by S's bisection in one cell, and
  its residuals are monthly identities. Of the five items every product takes, it meets
  the first, its helper taking the exemption set as a parameter, and the third, the rows
  its product tests read on the splice's inputs built in the splice's fixture while S is
  swept, each S point released after its last T2 case and the collector frozen again after
  the last; the fourth and fifth do not arise, RILA summing no schedule by a loop and its
  companion being a market. It meets the second in part: the term-end identity's residual
  is NaN at every Term End Date and 0.0 in every other month, but the two roll-forward
  residuals are NaN in every month, so no month shows those checks failing on the NaN and
  not on a finite residual. RILA's C step takes up the rest on the row issued 13 months
  on, whose roll-forward residuals, at a NaN A/E, are 0.0 before its issue at `t = 13` and
  NaN from it.
- *§7.11's carried items* (*Record — M8*), read at da763e8, M8's landing, from the tests
  stage on: into RILA, *Checks*, S's `all(...)` kept and the count's residual and
  `av_at`'s `"AFT_WD"` guarded, and *Term-start state*, through the moved copies; into
  every product, *Each rule entry by entry*, a map of each case's first `RAISE` over the
  62 refusal sites in `model_point_table`, the six count cells and `proj_len()`, each
  case's first its own and every column of every looped rule some case's first, with no
  `NOT_ISSUED` list, since RILA adds no issue-age bound at stage `E`; *The core by line
  coverage*, the core running every line the full grid runs and no set-apart edit moving a
  core row's lines; *Boundaries met exactly*, the Edge term ending at its buffer and point
  4's flat Step years, RILA having no banded table; *`Data`'s state rules against S*, the
  every-state test; *Past the frame, and a NaN*; *Docstring tables*, `_table_overruns`,
  `_map_faults` and the docutils parse test, which skips where docutils is absent, as
  FIA's does, and so in CI, which M13 settles across products; and *Depth and status*, the
  ascending sweep measured on both models, RILA having no status column. *Switches and
  bounds S ships idle* it leaves, with reasons: `RILA_US_S` ships no switch, every
  Reference being a number, and each bound S ships idle binds in the main splice,
  `lapse_rate_max` through the shock of 27.5, the account rate's floor through a declared
  rate of 0.5%, the moneyness floor at 0.9 and the guaranteed minimum rates through the
  raised floors, while `db_rop_max_issue_age` and `maturity_min_years` bind on S point 12
  and `nge_cap_search_max` and `nge_solve_iter` are the cap solver's bracket and its
  iteration count, but the cap on mortality, which the splice's A/E of 1.05 leaves idle at
  every covered age and the cap test binds instead, on reads of both models at an A/E of
  10.0, and `roll_fwd_tol`'s floor, which no point's premium binds (*§7.6's carried
  items*, below); so there is no second splice fixture.
- *The template* (§7.1's *Records*, as M2 and M3 precised them) *and M14's carried items*
  (§7.1, *Record — M14*) are taken at stage `E`, among them the runner keyed by the model,
  an extract relabelled and reversed, every Reference set on a model just read, each
  refusal in a table-driven list, the reports on the valuation clock with zeros before
  issue, every branch of a cell returning its one type, which the guard test asserts, no
  new float-parameter or uncached cell, and `codes=codes(sec_proj)` in the module's one
  call of `twin_mismatches`. Not yet: the runner's `--cython`, `--build` and `_tool()`,
  the `create()`-copy test and the compiled runner test's refusal leg, and `proj_len()`'s
  refusal of an issue age outside 0 to 85, which RILA's C step takes up (*Carried into
  Phase 2*, below).
- *§7.6's carried items* (*Record — M4*) postdate the build. It meets *Every bound binds*,
  each floor, cap and clamp S writes bound with an effect in the core's frame, the
  mortality cap in the cap test at an A/E of 10.0, but the floors on the Fixed and Holding
  Accounts' shares of a withdrawal, which no state reaches, neither account falling below
  0, and `roll_fwd_tol`'s floor, `max(1.0, premium_pp())`, which binds only on a premium
  below 1, every point's being 50,000 or more, with no second splice fixture, since every
  other bound S ships idle binds in the main splice (§7.11's, above); *Residuals as
  floats*, S's signed residuals kept with no `float(...)`; *A bound stated only once
  probed*, the shock's binding on some rows and not others, which the module's comment on
  `SPLICED_REFS` states, asserted both ways by the core-reach test, and the depth comments
  corrected to the measurements at the review; *Events in their own month*, core rows at a
  term end, a renewal, an anniversary, a year's last month, a withdrawal and the maturity
  at `t = 0`; *Shared helpers and the runner*, the helpers prefixed `_rila_` and the month
  singular, though a label that is not a number is refused with the usage line, not yet
  with the table's labels, which RILA's C step adds; *Policy months in S's cells*, the
  free-withdrawal base read on the valuation clock and T2 rows valued mid-year; and
  *Tables keyed by what the point names*, the scenario's months held to what its
  step-function reader reads, a repeat refused and a gap let stand. *Months as results*
  does not arise: the cells it shares with S that return a month, `duration_mth`,
  `term_elapsed_mth` and `term_start_month`, count policy months in both models, which T1
  and T2 compare equal at each row's offset, and no cell finds a month by a search of the
  frame, as VUL's first default month does. *Reach by the raw value* it meets but for two
  bounds whose predicates read the bounded value: the surrender rate's, equal to
  `lapse_rate_max`, and the behavioural withdrawal's, equal to its allowance. It does not
  meet *Every value column*: its mortality rate's bound at 1 is no refusal (*The tables*,
  above), every other ranged column has a refusal but not one past each bound, and its
  accepted edges read the bounds of the count, the buffer, the floor and the cap alone;
  nor *Keys and clamps*: no case writes the charge table's first year as −1 or shortens a
  table below its cover; nor *Core-removal faults*: no fault dropped a core row. RILA's C
  step takes up these three; it also takes up the two predicates that read the bounded
  value, and `roll_fwd_tol`'s floor with a case at a premium below 1.

**Measured for K6 and F7.** Every time below was taken with other workflows sharing the
machine's four CPUs, all but the landing's at load averages of 1.1 to 3.6.
- *Comparisons.* At the second fix the default module ran 230 passed, and over the full
  grid at the fix stage 305 passed, so each of the full grid's 101 T2 and 16 T3 rows
  continued S in every cell the two share, at every argument S cached from the row's month
  on, to 1e-9 relative with no absolute floor, the residuals at the 1e-9 floor, but T1's
  exemptions, `result_pols` among them, compared column by column, and the two cells a
  restated or future row changes by design, `proj_len` and `scenario_id`, the row's own
  copy, and on rows valued mid-term `market_state` at `t = 0`, which no cell of theirs
  reads. T1 compares the twins with its exemptions alone.
- *Time.* By default the module ran 230 passed and 75 skipped in four runs at the fix
  stage, on the same code but comments: in 287.12 s and 318.34 s at 2.72 GB before the
  stage's restart, and in 381.96 s and 382.90 s after it, peaking at 2.73 GB and 2.74 GB
  in one process; at the tests stage, 225 passed and 74 skipped, in 318.62 s and 316.02 s.
  Over the full grid it ran 305 passed in 517.07 s and 442.13 s at the fix stage, peaking
  at 3.18 GB, 299 passed in 442.15 s at the tests stage, and 305 passed in 544.08 s at
  landing. So the default run takes 287 to 383 s, 4.8 to 6.4 minutes, about 1.6 to 2.1
  times the three minutes K6 projects for each product from WholeLife's module and past
  the design's five minutes in every run but the fastest, and about 105 to 215 s more than
  WholeLife's module, with the core already in place. In the second fix's suite its tests
  took 384.4 s, the most of any module in a suite that held neither FIA's nor VUL's, ahead
  of the conventions (352.2 s), DIA's (225.3 s), UL's (203.6 s) and MYGA's (200.7 s). Most
  of it is fixed: the splice's fixture, paid by the every-state test (35.4 s of its
  43.4 s), the accepted edges (39.8 s), the guard test (25.2 s), T4 (24.9 s), the
  committed model's cold sweep (23.2 s), the depth test (18.7 s), the runner (17.8 s), the
  cap test (17.1 s) and the extract (15.8 s), about 226 s together, where T2's 37 core
  rows took 53.4 s, 0.12 s to 3.08 s a row. The design's remedy past five minutes,
  thinning the core of 360-month rows that reach no branch another core row lacks, was not
  taken, since the core runs exactly the `Projection` and `Data` lines the full grid runs;
  a cut would come from those rows or from the fixed costs, and nothing was moved behind
  `sec_full`. M13, which measures the matrix, weighs it. The SEC conventions, 32 passed
  and 1 skipped, took 35.78 s alone and 33.7 s in the suite. On e011a0c with RILA added,
  the uslib suite ran 2,524 passed and 441 skipped in 2,041.19 s (34 min 01 s) at the fix
  stage, 1,944.12 s (32 min 24 s) at the re-review and 2,003.85 s (33 min 24 s) at the
  second fix, peaking at 3.72 GB in one process. On the landing's tree, after M8 and M4,
  the suite ran 3,063 passed and 535 skipped in 52 min 31 s (*Verified at landing*,
  below).
- *Depth.* A cold `net_cf` of the last month runs one cell a month back to `t_entry()` and
  13 to 21 more on the committed points: 378 levels on point 1's 360-month frame, where
  `RILA_US_S`'s runs 1,095, 359 Investment Amounts with nine cells above them and ten
  below, where month 0's interim value prices the term's option budget at its Term Start
  Date's market. Over the chain the twins run 16 to 19 and the rows in force 13 to 21, the
  most on row 19, S point 13 valued at its renewal at 72, whose month 0 re-solves the cap
  under the option budget; row 24, issued 13 months on, runs 18, its chains stopping at
  its issue. At the longest cover, issue age 0 and 1,080 months, on mortality extended
  below 40, it runs 1,098 levels, both at the valuation date and issued 120 months on,
  about 273 KiB of C stack at gcc's 255 bytes a level. Called alone, each chain's head
  runs 10 to 16 above its chain, and the depth test bounds each on row 16 under the same
  overhead. Swept in ascending `t`, the committed points run 14 to 19 deep, 19 on twin 13
  and row 19, where `RILA_US_S`'s points run 14 to 18, as deep as SEC's twins but on
  points 4, 5, 12 and 13, one level less: their deepest stack runs under the count, where
  SEC's `pols_if` reads `"BEF_DECR"` and it `"BEF_NB"`. `CALL_DEPTH` is 40 and
  `CHAIN_OVERHEAD` 24, asserted on twins 1 and 3, rows 16, 18 and 19, the future row and
  both frames at issue age 0. Phase 2's `t` cache is 1,202 values (*Carried into Phase 2*,
  below).

**Faults.** Each fault went alone into its own copy of the library, and the tests aimed at
it ran through the gate, at most two at a time but for about two minutes at the tests
stage, when three or four did.
- *Tests stage:* 88 faults, all caught. O01 to O15, each opening column ignored or read
  from the wrong place, each term-start value read from the scenario at `t = 0` and the
  cap read as declared or re-solved among them, were caught by T2 on 14 to 35 rows each,
  the committed rows, the opening-state test and the column-shows test, O15 by the last
  alone. R01 to R36 were R1a's rewrites: the clock and term arithmetic, the programme read
  at `t + 1`, the maturity, new business, the premium and acquisition at `t = 0`, the
  openings at `t > 0`, inflation on the policy clock, which only the inflation test
  catches, the cap's fixing, `k <= t_entry()`, the market keyed from issue, a derived row
  on S's own scenario, nine rewrites of `t > t_entry()` as `t > 0`, six of them caught
  only by the rules test's early-read walk on future rows, and the issue month written as
  `t == 0`. D01 and D02, a term-start value or a cap given where the term starts at or
  after the valuation month, fail `MALFORMED`. X01 to X14 hit the checks and guards: X07,
  a 1% count error below the floor, is caught only by the cap test, and X13, the Account
  Value's tolerance left unscaled, was missed at a million contracts and is caught since
  the test runs at 10^8. Y01 to Y16 are each aimed at a test no other fault reached; Y17
  and Y18 drop the guards before `t + 1`, caught by the guard test, and Y19 reads the
  anniversary rule a month late, caught by the every-state test alone; and Z01 and Z02
  make the Step and Edge boundaries exclusive, Z02 caught only on the Edge term valued at
  its buffer, variant 24 at 23. And 62 rule drops, each run on the cases a map of each
  case's first `RAISE` gave it, each failed every case aimed at it.
- *Review (tests lens):* 37 faults, of which 30, V01 to V24 and N05 to N10, were caught.
  Seven survived the default module and the conventions: the cover check admitting the
  Maturity Date (N01), the remainder rule's window moved off month 12 (N02), `nge_reset`'s
  1 and 0 refused (N03), a buffer or floor of 0 refused (N04), the anniversary rule's
  window moved off month 12 (N11), the remainder rule's cent widened by 1% of the
  allowance (N12), and the option's floor in the withdrawal allocation dropped (N13); N01,
  N02, N11 and N13 together passed the full grid too.
- *Fix stage:* on the final code, each alone in its own copy, all caught: N01 by the
  refusal at the Maturity Date, N02 by the remainder refused on the first anniversary, N03
  and N03b, 1 and 0 refused and swapped, by the accepted edges, N04 by the edges' buffer
  of 0, N11 by the base refused on the first anniversary, N12 by the remainder just over a
  cent, and N13 by T2 on the dip variant at 41; the renewal slack at 1, 1.5 and 2 cents by
  the edges, and at 3.5 cents by `MALFORMED`'s +0.03 case; `BEF_TERM_SURR` dropped from
  `pols_if_at`'s chain by T2 on point 1 at 11; and the five term-start columns read from
  the scenario at `t_entry()`, on the six mid-term rows the review named: the index on all
  six, against two without the moved copies, the MVR on four, the notional family reading
  none, and the rate, the yield and the volatility on all six each.
- *Re-review:* eleven faults re-run on the current tree, each in its own copy, all caught
  by the case aimed at each: N13, N01, N02, N11, N03b, N04 and N12; the slack at 2 and 3.5
  cents; and the MVR and the volatility read from the scenario at `t_entry()`, each by the
  core's T2 row of point 1 at 11. The second fix ran none: it changed one docstring line.

**Carried into every product still to come.** What RILA, the Payout stream's last, adds to
what the earlier records carry. Each item goes to the products in progress from this
landing (§5.3), VA's build among them, which takes what applies, and each record says what
it took. They came from the design and its critique, the tests stage, and the review and
the fixes it led to, its faults among them:
- *Re-based scenarios.* Where S keys a path from issue, re-base it into copies in a
  companion file read through S's reader by repointing its `*_file` Reference, as RILA's
  and FIA's are. Move each row's copy by its `duration_mth`, never its `source_mth`, and
  name it by the months it moves, so that rows moved alike share one: `{id}-M{m}` for a
  `duration_mth` `m` above 0, S's own `{id}` at 0 and `{id}-F{k}` for a row issued `k`
  months on, named through `SecSpec.future_state`. The two months agree only where S keeps
  the policy clock or the row comes from S's new business, as on every row of RILA's and
  FIA's tables, so that their `-M{d}` ids, keyed by `source_mth`, name the months moved:
  on VA's point 2 they differ by 26, so its in-force twin reads `base-M26`, set through
  `SecSpec.twin_state`, not S's own `base`, and a row restated from it at S month 14 reads
  `base-M40`, as a new-business `base` point's row at 40 does (§7.11, *Record — M8*,
  *Scenarios*). `IUL_US_S` reads no file for its index path, which `index_level(t)`
  computes from two References, `index_level_init` and `index_return_ann`, so no reader
  stands to repoint: §7.4 moves the formula itself to `t`, IUL's rate-path test runs under
  an override of `index_level` (§7.3, *Record — M3*, *Tests*), and IUL's record says how a
  row restated at month `d` reproduces S's index credits from `d`.
- *Time-point parameters.* Rename to `t` a parameter that holds a month or an instant on
  the valuation clock, as RILA's `market_state(k, name)` and SPIA's `lives_if(k, life)`
  were, so that the twin comparison shifts it and the rules test reads it as a month, and
  call it by position. Name one on the policy clock otherwise, VA's policy month in
  `t_of_month(m)` and contract quarter in `vix_sq(k)` and `phi_glwb_vix(k)` among them, so
  that neither the comparison shifts it nor the rules test reads it as a valuation month,
  as SPIA's `cum_annuity_pp(k)` and DIA's `lives_if_pm(k, life)` are (R2) and RILA's
  `wd_amount_pm(m)` is. Move a second month beside `t`, as IUL's segment month `m`,
  through `arg_map`.
- *Start values.* Give a term's or a segment's start value DIA's frozen-weight shape
  (§7.12, *Record — M12*): a column, or a row of IUL's ladder (§7.4), only where the
  period began before the valuation month, its presence checked both ways and its value
  above 0 where a cell divides by it. Carry a re-solved rate as a column only where static
  data cannot re-derive it, as RILA's cap re-solved at a renewal under `nge_reset`.
- *Stepped paths and moved copies.* Splice on paths in which every field steps, within
  each period and across its starts: on S's flat fields a start value read from the
  current market passes every comparison. On every row valued mid-period whose state at
  `t = 0` a correct model never reads, as on RILA's mid-term rows and FIA's mid-year rows,
  move the companion's state at `t = 0` off each start column, after writing that state to
  `t = 1` where a month-end reader needs it, and leave that instant out of the comparison
  on those rows alone (§7.11, *Record — M8*, *Term-start state*). Where a correct model
  reads it, leave it unmoved: `IUL_US_S`'s sweep opens a segment every month and
  `seg_return(t)` reads `index_level(t - 12)` and `index_level(t)`, so a row's level at
  `t = 0` closes any segment maturing then and opens the next, and moving it moves both
  credits. Its path moves every month, so a ladder's start read from it in the frame
  misses, and the rules test refuses one read before `t_entry()` (R1); but on its level
  return every segment's return is 6.4%, so splice on a path whose return varies between
  segments, through an override of `index_level`, or else a start derived from the two
  References passes.
- *Binding floors and clamps.* Make each floor and clamp bind with an effect (§7.9,
  *Record — M11*; §7.6, *Record — M4*, *Every bound binds*), a positive request on a
  negative account value among them, and a bucket's floor in a withdrawal allocation,
  which needs that bucket below 0 while the total stays above it, as RILA's dip variant
  takes its interim value below 0 while its accounts keep the account value above it:
  without it, dropping the option's floor passed every test, a blocker of RILA's review.
- *Cent slacks.* Hold a `Data` rule whose carried amounts can miss by a whole cent, as one
  that ties more than two, or adds an exact amount to one of two, to half a cent from each
  and half a cent more, as RILA's renewal identity is held to two and a half cents. An
  amount held exactly, as a premium paid or a programme's amount, adds nothing: a carried
  amount held to such inputs or to 0 stays at a cent, as do an allowance held to its base
  and a bound between two carried amounts (D6, precised at M7 and M10). Test each rule on
  an extract with every amount carried to the cent, not only with one column moved, and
  pin each tolerance from both sides.
- *Window rules.* Test every rule over a window of contract months at both ends, refused
  just inside each and accepted just outside, its first month as well as its last, the
  Maturity Date and the first anniversary among them: RILA's remainder and anniversary
  rules, refused only at month 36, passed every test with their windows moved off month
  12, and its cover check with the Maturity Date admitted, as MYGA's second-year rule,
  tested at month 12 alone, passed narrowed to that month or widened to month 24 (§7.10,
  *Record — M7*, *Data's checks*, precised).
- *Flag spellings.* Validate each flag column on every spelling its `Data` accepts,
  asserting the decoded flags and that the rows reading them project bit for bit: RILA's
  accepts 1 or 0 and 1.0 or 0.0 beside `True` or `False`, and a decode cut to `True` and
  `False`, or with 1 and 0 swapped, passed its module until its fix. The life chassis
  accepts `True` or `False` alone (§7.3, *Record — M3*, *Model point values*), so ULSG and
  IUL show 1, 0, 1.0 and 0.0 refused, of which VUL's module shows 1 alone: the chassis
  keeps S's `bool()`, which reads a `"0"` in a text column as true.
- *Timing branches.* Write a branch over several timings as a comparison chain, never a
  tuple display, which C5 reports as building a Python object.
- *NaN checks.* Keep S's generator, as RILA keeps `all(abs(r) <= tol ...)`, or a loop that
  stops at `if not abs(r) <= tol`, `<` where S has it, as `VA_US_S`'s
  `all(abs(r) < tol ...)` does (§7.11, *Record — M8*, *Past the frame, and a NaN*, and its
  *Carried into VA (M9)*, *Checks*), and send a NaN through a pricing Reference as well as
  through one the counts read: RILA's `trading_cost_rate` reaches the Account Value's
  residual and the term-end identity's, and its `mort_ae_factor` the counts', where S's
  moneyness factor, its bound first, loses a NaN on its way to the count.
- *Reads of `t + 1`.* Guard every read of `t + 1` with `is_active(t)`, as RILA's count
  residual and `av_at`'s `"AFT_WD"` are and VA's `check_pols_roll_fwd_resid` and `av_at`
  must be (§7.11, *Record — M8*), and have the guard test bound month-keyed cells at
  `proj_len()` and instant-keyed readers, as `market_state`, at `proj_len() + 1`.
- *Depth.* Size `CHAIN_OVERHEAD` from the cold depth with the pricing stack under month 0,
  measured on every committed point, and put the deepest in the depth test's bound: RILA's
  month 0 prices its option under the interim value, 13 to 21 levels beyond the chain, and
  its review found the test leaving out row 19, the deepest. Measure the ascending sweep
  on S and SEC alike (§7.11, *Record — M8*, *Depth and status*): `BEF_NB` adds a level
  where the deepest stack runs under the count.
- *The every-state test.* Restate every state S reaches on the splice's inputs, at each
  window's edges by default and at every month on the full grid, and assert that `Data`
  and `proj_len()` accept it, with the product's named exceptions set aside and shown
  refused (§5.2, T5, precised at M10).
- *Coverage and the drop sweep.* Map each malformed case to the refusal it meets first, by
  `sys.monitoring`'s `RAISE` events, before dropping each rule, and run each drop on the
  cases it refuses first; measure line coverage by `LINE` events on the code objects
  registered at each read, since coverage.py attributes no line of a modelx formula, and
  choose the core by it (§7.11, *Record — M8*, *Each rule entry by entry* and *The core by
  line coverage*).
- *States S reaches.* Accept a state S reaches, a negative interim value or a shadow
  account never floored, and refuse instead what no contract in force can be, as a
  contract holding nothing (D6, precised at M10); check every allowance and base that can
  go negative, not only the withdrawal it feeds.
- *Set-apart References.* Set apart the shipped References that rewritten cells read and
  that ship equal, as RILA's trading cost and interim-value expense, its credit spread and
  its account rate's floor, and its free term-end lapse and free withdrawal rate; check
  each set-apart edit by the lines each core row runs as well as by its test; and check
  that no splice shock pins a rate to its bound in every month, as a lapse shock of 30
  pinned RILA's shock year to `lapse_rate_max` on every row.
- *Name search.* Before generating, search every input CSV the generator copies,
  case-insensitively, for the option, account, share-class and defined-term names the
  research notes record, as well as the publishers and products `sources.md` cites, each
  name's words matched also when joined or run together, and reword each hit in the S file
  that holds it, S's table or a file the generator copies into a companion, in a commit of
  its own (`CLAUDE.md`): RILA's twins copied four such cells from S's provenance, and its
  scenario companion keeps S's provenance on every row.
- *Docstring checks.* Copy `_map_faults`, `_table_overruns` and the docutils parse test
  (§7.11, *Record — M8*, *Docstring tables*), give each cell its own row in the symbol
  map, and scan each table for an identifier split across lines, which neither check sees:
  one of RILA's rows rendered `AFT_WD` as two words. `VA_US_S`'s map has run-in rows too
  (§7.11, *Record — M8*).
- *Time the module early.* Time the module on the prototype and split it into a core and a
  full grid from the start (K6): RILA's default run passed three minutes at every stage,
  and five in every run but one.

**Carried into Phase 2.**
- *Caches and bounds:* `t` 0..1,201, 1,202 values: 1,080 months of cover at the youngest
  issue age, 0, to `maturity_age` 90, plus the 120-month horizon, the frame's last month
  1,199; every monthly cell holds `t` to `proj_len()`, 1,200, the count's residual and
  `av_at`'s `"AFT_WD"` being 0.0 there before they read `t + 1`, and `market_state` the
  instant `proj_len() + 1`, 1,201, which `index_level`, `mvr`, `risk_free`, `div_yield`
  and `impl_vol` read unguarded at `t = proj_len()`. `x` (`mort_rate_base_at`) 0..94; `cy`
  (`surr_charge_rate_at`) 0..90; `y` (`lapse_rate_base_py`) 1..91; `m` (`wd_amount_pm`)
  1..1,080; the stack 1,098 levels at issue age 0. These size `sample_sec.py`,
  `run_sec.py --cython` and the Windows job's stack. `sample_sec.py` calls the cells and
  arguments no report or check reaches, which the module's `_sweep` evaluates over each
  frame, `fixed_leg_yield`, `nge_spread_implied`, the free-withdrawal base and allowance
  at every month, the option-pricing market, the decomposition and each leg after the
  withdrawal, `opt_portfolio_abs` at `"TERM_START"` and `claims_over_av` by kind among
  them, and the label accessors, which no projection cell calls (R17).
- *Issue age:* Phase 2's `proj_len()` refuses one outside 0..85, beside the cover check
  (§7.1, *Record — M14*; §6.1, step 6). `Data` refuses one below 0 and one whose attained
  age in the first month on the books the mortality table does not rate, below 40 as
  shipped; nothing refuses one above 85, as in S.
- *M14's items for the C step:* the runner's `--cython`, `--build` and `_tool()`, with the
  `create()`-copy test and the compiled runner test's refusal leg (R4; §6.1, step 7).
- *T1 and codes:* S caches `claims(t, kind=None)` and `claims_over_av(t, kind=None)` under
  `(t, None)`, which need a T1 `arg_map` at stage `EC` (R12). `_mismatches`, the module's
  one call of `twin_mismatches`, passes `codes=codes(sec_proj)`.
- *Engine functions* (R14): the float-parameter cells, all S's, for Phase 2 to inline or
  re-key: `norm_cdf`, `bs_d1`, `bs_d2`, `bs_call`, `bs_put`, `bs_binary_call`,
  `opt_component`, `opt_portfolio`, `opt_portfolio_abs`, `credit_rate_at` and
  `opt_budget_at_cap`. S's tests call `opt_component`, `opt_portfolio`, `credit_rate_at`
  and `bs_binary_call` directly. SEC adds none, and no uncached cell. The Black–Scholes
  cells' `math` calls and `math.inf` are S's, which C5 refuses: RILA's Phase 2 admits them
  by cell or gives them a C form (§7.1, *Record — M14*, *Carried into M15 or later*).
- *`Data`'s share:* `market_state` becomes per-field `[scenario, month]` arrays, each
  future copy's months before issue unreadable; the ten decodes move into `Data` (R6), and
  the six count cells become R7's checking ints.
- *Strings:* R9 numbers the timing, kind, bucket, leg and market strings; `opt_legs`'
  tuple of leg names falls under R10.

**Carried, outside the SEC models.**
- Nine S-side items for §8.2 item 4, found in `RILA_US_S`, which §8.2 item 4's fix, to
  mortality alone, leaves as they were: the first three, on a negative account value, are
  in both models, `RILA_US_SEC` reproducing S; the sixth is corrected in `RILA_US_S` at
  landing; and the rest are fixed or refused in `RILA_US_SEC` only. The figures are on the
  build's probe inputs, a crash path:
  - the Free Withdrawal Amount goes negative on a negative base: at policy month 23 the
    base is −28,760, and the allowance and the behavioural withdrawal are both −2,875.98,
    which `wd_pp`'s clamp passes. The fix is
    `free_wd_allow = free_wd_rate × max(0.0, free_wd_base(t))`, with the behavioural
    withdrawal floored at 0, since flooring the withdrawal alone would charge a withdrawal
    charge on a zero withdrawal; it moves no shipped number. No step makes it, and no
    decision of §8.2 asks for it. Until one does, `RILA_US_SEC` reproduces S, the crash
    variants pin it, and `proj_len()`'s remainder rule applies only where the base is 0 or
    more;
  - `check_av_roll_fwd()` is False on the crash path, −2,738.25 at month 23 and −868.49 at
    35, the negative withdrawal booked while the account is unmoved, in both models;
  - S pays a negative surrender value at a negative Account Value, −30,684.39 at month 19,
    and the death benefit of a contract issued past 80, the Account Value alone, is
    negative there too;
  - `nge_reset` on a Floor option solves the cap portfolio, and on a Step, an Edge or an
    uncapped option does nothing: `RILA_US_SEC`'s `Data` refuses both;
  - `nge_reset()` reads any text as `True`: `RILA_US_SEC`'s `Data` validates the flag by
    value;
  - four provenance cells of S's table, points 4, 5, 7 and 12, named the cited carriers'
    crediting options and one carrier's defined term, which the SEC table's twins copied:
    the landing's commit before the copy rewords them by design (*Landing*, below);
  - 38 lines exceed 92 characters, 2 in `Data` and 36 in `Projection`, 33 of them in the
    symbol map: wrapped in `RILA_US_SEC` only;
  - docstring defects: the *Timing arguments* name `roll_index_share` of `"BEF_ROLL"`, no
    cell, for `roll_share("OPTION")`; `wd_rate_ann` (line 484) and the model docstring
    (line 195) point to a README no folder holds; "this cells" stands in
    `opt_budget_at_cap` (line 820) and `pols_if` (line 1830); and `inv_amt_pp`'s formula
    follows a single colon, so it renders as a blockquote: corrected in `RILA_US_SEC`
    only;
  - the symbol map runs `claim_pp`, `claims_from_av` and `claims_over_av` into `claims`'
    row, which M8's landing found: `RILA_US_SEC` gives each a row of its own.

**Landing.** Rebased from e011a0c onto cf0e402, after M8 and M4. `RILA_US_S` has capped
its annual mortality with the bound second, `min(rate * mort_ae_factor, 1.0)`, since
ed73164, the second of §8.2 item 4's commits, before RILA's build, and `RILA_US_SEC`'s
`mort_rate` caps the same way behind its guard, through its keyed reader, `rate` being
`mort_rate_base_at(age(t))`, so that fix changed no formula of `RILA_US_SEC`. uslib's
`index.md` took two conflicts: the sentence that lists the SEC models, which now names all
nine, and the row on input files, which now names RILA's market scenarios beside DIA's
schedule and the FIA's scenarios. `sec_support.py` took four, where RILA's state
extractors, re-based scenarios, state and spec follow FIA's and VUL's, all kept: RILA,
built on DIA's tip, had put its three helper groups after DIA's, where FIA's went too, so
that the merge set each beside FIA's, and the landing keeps the groups in landing order.
`SecSpec.future_state`, its test and its two refusal cases in `test_sec_support.py`, which
RILA had copied from FIA's build before FIA landed, merged as the tip's, one copy each.
Before the copy, a commit of its own, be7dbd7, rewords the provenance of `RILA_US_S`'s
points 4, 5, 7 and 12, which named the cited carriers' crediting options and one carrier's
defined term, by design, keeping their source keys (CLAUDE.md), and the landing
regenerated `model_point_table_sec.csv` from it, which moved those four twins' provenance
alone. `INPUT_FILES`, regenerated with
`gen_input_files.py lifelib/libraries/uslib --write` on the merged tree, came out
unchanged. The landing also corrected `model-sec.md`'s census of `RILA_US_S`'s cells,
which gave the docs stage's 64 unchanged and 20 with new text only, to 63 and 21, and a
comment in the test module, which put the count at which the Account Value's residual
first passes its unscaled tolerance near 1e8, to between 3e6 and 1e7. After its review the
landing named `RILA_US_SEC` in `test_mortality_caps.py`'s docstring, as M4's landing named
`VUL_US_SEC`, since its cap test sees `RILA_US_S`'s cap and float bound and, reading both
models with a NaN A/E factor, the cap's order; named RILA's market scenarios among the
companions `SecSpec`'s docstring lists, beside DIA's premium schedule and the FIA's rate
scenarios, and the FIA's and RILA's among those `gen_sec_points.py`'s docstring lists,
which had named DIA's and VA's alone; and added month 5 to the months mid-term that the
test module's comment on the splice's months lists.

**Verified at landing**, with three other workflows, VA's and ULSG's builds and the
drafting of this record, sharing the machine. The uslib suite, with modelx-cython
installed and so the compile tests included, gave 3,063 passed and 535 skipped in
3,151.38 s (52 min 31 s), its two warnings modelx's renames of `Term_US_S` and `VUL_US_S`
in the round-trip tests. RILA brings 230 passes and 75 skips in its module, 32 passes and
1 skip in its SEC conventions, the notes-orientation check, which fourteen other models
skip, and one pass in the compiled convention that reads every SEC model. Over its full
grid, RILA's module gave 305 passed in 544.08 s, and the `cython` selection 11 passed and
none skipped under `USLIB_REQUIRE_CYTHON=1`, in 159.97 s. doccheck built 509 pages with 0
warnings. `gen_sec_points.py --check` found the files of the nine SEC models current, and
`gen_sec_fingerprint.py Term_US_SEC --check` reproduced the fingerprint. md_lint reported
0, `gen_scaffolding.py --dry-run` 0 files in each of the six libraries, and
`gen_citation_links.py --dry-run` nothing on its 315 source tags. A case-insensitive
search of `model_point_table_sec.csv`, `market_scenario_sec.csv` and `RILA_US_S`'s
`model_point_table.csv` for 116 names, the publishers, products, options and defined terms
that `registered_index_linked_annuity/sources.md` and the product's research notes cite,
each name's words matched also when joined by spaces, underscores, hyphens or dots or run
together, found none but generic terms: Term Start Date, Investment Amount, index
performance and the header of the `cap_rate_init` column. These runs came before those
text edits (*Landing*, above) and before the landing wrote this plan's M10 text, which no
test, generator or doccheck reads. On the tree as committed, `test_mortality_caps.py` gave
32 passed and `test_sec_support.py` 53 passed, `gen_sec_points.py --check` found the files
of the nine SEC models current, doccheck built 509 pages with 0 warnings, and md_lint
reported 0 on uslib and on this plan.

### 7.9 SPIA — `SPIA_US_SEC` (E: L, C: M)

*Today:* months from the annuity date, with no in-force support. `pols_if` is a closing
measure (D5). Improvement is calendar-dated, from `annuity_year + duration(t)`.

*E:*
- The opening state is four columns per contract, at the start of month 0. Each life's
  survival at the valuation date, `lives_if_init_1` and `lives_if_init_2`, is a
  probability in `[0, 1]`: 1 or 0 on a real record, where a joint contract may carry one
  life already dead, and S's `lives_if(d, i)` on the splice. S treats the lives as
  independent, so per-life probabilities suffice. Then `commute_frac_cum_init`, which is
  path-dependent, and `cmt10_shift_init`, the 10-year CMT's change from the annuity date
  to the valuation date (D7). At the annuity date each covered life is 1 (life 2 is 0 on a
  single-life contract), the fraction 0 and the change 0.
- The CMT's change is read on the one path every point shares (D7, precised at M11): a
  contract on the books at the valuation date discounts a commutation at
  `j0 + cmt10_shift_init() + cmt10_shift`, the Reference being the change made at the
  valuation date, and a contract commencing later, bought after it, at `j0`.
- The payments to date stay on the annuity-date clock, `cum_annuity_pp(k)` with `k >= 0`,
  because they are deterministic. The recursion is based at the valuation date's policy
  month, where one loop sums the instalments before it in S's order, and
  `annual_income(y)` is based the same way at the valuation date's policy year (R2,
  precised at M11).
- The certain months left follow from `duration_mth`.
- The count on the books is `policy_count` from the annuity date to the stop rule:
  mortality decrements each life, never the count, so `BEF_NB` is a closed form, and
  `pols_if`, S's closing measure on that count, is not `BEF_DECR` (D5).
- Improvement is calendar-dated and stays on the policy clock (D7); expense inflation
  keeps S's annual steps, on `t`, `(1 + π)^(t // 12)`. The splice neutralizes inflation
  alone.
- `proj_len()` refuses a point at or past the stop rule, and a contract owing nothing
  after the valuation date.
- Future new business is an annuity commencing later, at most 120 months on. S
  deliberately excludes the single premium, and SEC keeps that: there is no premium and no
  acquisition.
- **The name clash, resolved:** `pols_new_biz` exists by D5, meaning annuities commencing
  in the month, and the SEC module keeps S's ban on `pols_lapse` and `lapse_rate`; no
  convention needed an exception.
- S has no in-force point, so `IN_FORCE_TWINS` is empty.
- Splice months: 11, 12, 13 and 24; the end of point 5's certain period (119, 120); the
  month after a scenario death (14, and 30 with both lives dead); the last month of each
  other certain or refund period and the first after it (199, 200, 249, 250); the trims
  and the month before one (176, 245, 246, 659); the months after the residual floor's cap
  and before a commutation month with nothing left (37, 100); a frame's last month (695,
  659, 359); either side of omega inside a certain period (299, 300); six years in payment
  (72); months between quarterly instalments in advance (1, 2); and a semi-annual payment
  month in arrears (5). The derived rows and eleven variants of S's points reach a joint
  point with one life already dead, every form and refund option, commutation taken and
  barred, a certain period that ends and one that outlasts the age stop, every frequency
  and timing, COLA and a rating.
- T2 and T3 compare to 1e-9 relative with no absolute floor, since a floor of 1e-9 hides
  survival near 1e-10 where a cap on mortality binds, and SPIA's roll-forward residuals
  are exact zeros, so none needs the floor (§5.2, precised at M11). Future rows commence
  13 months on, three of them 12 or 1 month on.

*C:*
- Text is decoded to numbers in Phase 1 (§7.1, *Record — M14*, *Carried into Phase 1*).
  Five of S's six string enums, the `form`, `reduction_trigger`, `timing` and `mort_basis`
  columns and the `commute_disc_convention` Reference, are eight bool decodes
  (`is_period_certain`, `is_certain_only`, `is_cash_refund`, `is_installment_refund`,
  `is_trigger_either`, `is_arrears`, `is_scenario`, `is_disc_compound`), each validating
  its column or Reference as S's accessor does, so no other projection cell compares the
  model point's text; the sixth, `sex`, is the join key the two age readers read.
  `pols_if_at` and `claim_pp` still compare their timing and kind strings, which R9 makes
  int codes. Phase 2 moves the decodes onto `Data` arrays.
- S's label accessors stay for reporting and T1. R17 and C5 admit a label accessor that
  takes no argument and returns its point's column of its own name: `form()`,
  `reduction_trigger()` and `mort_basis()` do, but `payment_timing()` returns `timing` and
  `sex(life)` takes a life and returns `primary_sex` or `joint_sex`, so SPIA's Phase 2
  extends R17 and C5 for those two, or leaves them out of `"reporting"`.
- `bool(model_point()[...])` on numpy-bool columns.
- NaN joint-life columns: `death_mth` returns -1 for a survivor through `pd.isna`, and
  `Data` returns the death columns as the numbers it checked, from which Phase 2 builds a
  -1 sentinel vector.
- `commute_disc_convention` is a string Reference read only by `is_disc_compound()`; it
  becomes an int code (R9).
- The per-`(t, life)` `.loc` in `mort_rate_base` and `improvement_rate` is now one reader
  per table keyed by attained age, `mort_rate_base_at(x, life)` and
  `improvement_rate_at(x, life)`, called only at ages the table holds; Phase 2 makes them
  `[sex, age]` arrays. The surrender charge reads `Data.surr_charge_scale()`, the scale's
  one check, which becomes a clamped vector with its first and last years. The list in
  `horizon_mths` goes; the commuted value and the withdrawal are already loops over policy
  months.
- No report reaches `lives_death`, `premium_net_pp`, `premium_tax_rate`, `qualified` or
  `surr_charge`, nor does T1's sweep; the module's sweep calls each, on the committed
  points, S's points and the splice's rows. `duration_mth` is now the policy clock, which
  every contractual cell reads.
- Caches (precised at M11): `t` 0..1,344, `k` 0..1,224, `y` 1..102 and `x` 18..119. The
  longest frame is 1,344 months: the youngest lifetime issue age is 18, omega is 120, the
  future horizon is 120 months, and `lives_if` reads `t = proj_len()`. The shipped tables
  start at age 40, so on them a frame is at most 960 months of cover. Three inputs those
  sizes rest on are bounded by the product but refused by no cell at stage `E`: a lifetime
  issue age of 18 or more, the `certain_only` issue age, bounded only above, and
  `certain_months`, 0 or 60 to 360. Phase 2 refuses each in `proj_len()` beside the cover
  check, or sizes the caches from the product's limits.
- Depth (F7): a cold `net_cf` runs one cell a month back to `t_entry()`, at most 1,234
  cells at the longest cover, and 2,494 Python frames in the modelx export.
- S's `claims(t, kind=None)` keys: at stage `EC`, T1 needs an `arg_map` for them (R12).
  There are no float-parameter or uncached cells, and S rounds nothing.

#### Record — M11, done 2026-11-02

Built in two commits, as D1 requires: `SPIA_US_S` copied with only `_name` changed, then
the enhancement, by M1's process: a design prototyped and critiqued before the build,
tests written against the build and checked by injected faults, then a review under the
three lenses. The review made 19 findings, 4 of them major, some of them one defect seen
under two or three lenses, and a re-review of the fixes made three more, one of them
major: the first fix still read the CMT's change from each contract's own annuity date, so
an annuity commencing after the valuation date saw a change made at it. All are fixed. The
reading the second fix gave the CMT, one path that every point shares, was confirmed at
landing, and precises D7. Seven defects found in `SPIA_US_S` are carried below: five are
fixed in `SPIA_US_SEC` only, and two in neither model. M11 was built on M2's tip and
rebased onto M14's at landing, where a review of this record corrected it (*Landing*,
below).

**What exists now.**
- `SPIA_US_SEC` at stage `E`. Of `SPIA_US_S`'s 72 `Projection` cells, 22 are unchanged, 14
  have a new docstring only and 36 are rewritten; none is removed or renamed. It adds 23
  cells, 95 in all: `policy_count`, `duration_mth_init`, `t_entry`, `stop_mth`,
  `is_active`, `pols_if_at` and `pols_new_biz`; three opening-state accessors,
  `lives_if_init(life)`, `commute_frac_cum_init` and `cmt10_shift_init`;
  `annual_income_first`; the schedule by policy month, `is_payment_pm(k)` and
  `annuity_pp_sched_pm(k)`; one reader per table keyed by attained age,
  `mort_rate_base_at(x, life)` and `improvement_rate_at(x, life)`; and eight decodes.
  `Data` keeps S's five cells, rewrites the table reader, which now checks the table as it
  reads it, and adds `surr_charge_scale`, which checks the surrender-charge scale, and the
  Reference `future_horizon_mth = 120`.
- `model_point_table_sec.csv` holds 22 rows generated from SPIA's `SecSpec`. Fifteen are
  S's points as twins, commencing at the valuation date. Six are derived in payment: the
  anchor (S point 1) at month 14, the month after its joint annuitant's death; the cash
  refund (6) at 13, its month of death, which pays the refund at `t = 0`; the 10-year
  certain point (5) at 120, where its deferred reduction begins; the certain floor (13) at
  30, with both lives dead; the commuting point on the table basis (9) at 24, its second
  anniversary, with two fractional lives; and the anchor on the table basis (8) at 695, a
  one-row frame. The last row is S point 8 commencing 13 months on. A case-insensitive
  search for the publishers, products, form numbers and hosts that
  `immediate_annuity/sources.md` cites finds none of them in the table.
- `tests/test_immediate_annuity_us_sec.py` has 39 tests and 191 cases: T2 on 62 splices;
  T3 on 29 future points; T4; T5 on 47 malformed rows, 8 malformed surrender-charge
  scales, 6 undecodable values and 5 contracts owing nothing; T6; the rules test; and the
  product's own facts. By default a core of 29 splices and 11 future points runs, 139
  cases in all. A test asserts that the core reaches each form, trigger, basis, timing and
  frequency, each opening-state value and each named branch of the commutation, the trim
  and the refund, and line coverage at the tests stage showed it reaching every
  `Projection` line the full grid reaches. The other 52 cases carry `sec_full` (K6). S has
  no in-force point, so `IN_FORCE_TWINS` is empty. The SEC conventions, 33 cases, pass but
  for two skipped by design: the lapse-rate convention, since SPIA has no lapse, and
  `pols_if == BEF_DECR`, which `closing_pols_if` skips. Of the compiled conventions, the
  one that reads every SEC model passes: a model at stage `E` declares no reporting cells.
- `run_sec.py`; `model-sec.md`, with *The opening state*; the registry entry, with
  `closing_pols_if` among its flags, and its `INPUT_FILES`; and four generated pages.
  doccheck reports 485 pages and 0 warnings.
- Shared files, added to in place: SPIA's spec and its state extractors in
  `sec_support.py`; the entry in `us_registry.py`; `EXTRA_POINT_ASSERTIONS["SPIA_US_SEC"]`
  in `test_model_conventions.py`, S's product fact that the gross outgo is never negative;
  and the models table and the SEC sentence of uslib's `index.md`.

**Departures and precisions.**
- *The count is not decremented* (D5, precised). Mortality decrements each life's
  `lives_if`, never the count. The count on the books is `policy_count` from the annuity
  date to the stop rule, and every flow is that count times a per-contract amount weighted
  by survival. So `BEF_NB` is a closed form with no chain behind it, the count leaves the
  books only at the stop rule, and there is no maturity cell. `pols_if` keeps S's closing
  obligation measure on that count,
  `pols_if_at(t, "BEF_DECR") * max(C(t), l_alive(t + 1))`, 0.99999986 at `t = 0` on point
  8, and the model is registered `closing_pols_if`.
- *The opening state* is four columns per contract at the start of month 0. Each life's
  survival is a probability: 1 or 0 on a real record, and S's `lives_if(d, i)` on the
  splice. `commute_frac_cum_init` is path-dependent. `cmt10_shift_init` is the CMT's
  change from the annuity date to the valuation date. WholeLife's state is 0 at issue, but
  an annuity's survival opens at 1.
- *The CMT on one path* (D7, precised; confirmed at landing). A contract on the books at
  the valuation date discounts a commutation at `j0 + cmt10_shift_init() + cmt10_shift`,
  and one commencing later at `j0`. S's `cmt10_shift` is each contract's change since its
  own annuity date, which one Reference cannot hold for contracts bought at different
  dates. The review found that; the first fix moved the change seen by the valuation date
  into the column, and the re-review found the same mechanism on contracts commencing
  later, which the second fix closed. The splice reads SEC once with the Reference at 0
  and compares future rows with S read at 0, and a test of its own reads one table,
  holding a contract in payment, one commencing at the valuation date and one 13 months
  on, at the Reference 0 and 0.005. Both settings ship at 0, so no shipped number moved.
- *Two things need no column.* The payments to date stay on the annuity-date clock, based
  at the valuation date's policy month by one loop in S's order, bit for bit with S;
  `annual_income(y)` is based the same way (R2, precised). The certain months left are
  `certain_mths_eff() - duration_mth`.
- *R1a, cell by cell.* These cells now test the policy clock: `is_payment_mth`,
  `annuity_pp_sched`, `annuity_pp` (the installment refund's trim), `certain_floor`,
  `commute_elig`, `claim_pp` (the refund balance at `G(duration_mth(t))`, or a month on in
  an advance payment month) and the scenario step in `lives_if`. `commuted_value` and
  `commute_amount` read the schedule by policy month, in one loop each, where S read
  `annuity_pp_sched(s)` at months ahead of `t` (R2). The trim of a refund paid in advance
  below monthly whose first instalment repays the premium reads `G` at
  `max(0, n_R - 12/m)`, where S reads `G(1 - 12/m)`, below 0 (`G(-2)` on a quarterly
  variant) (R1).
- *Cells indexed by a time point* move to the valuation clock with their parameter renamed
  `t`: `lives_if`, `lives_if_last` and `check_lives_roll_fwd_resid`, whose check is
  rebuilt from the opening state.
- *Inputs on their clocks.* Inflation keeps S's annual steps, on `t`. Improvement is
  calendar-dated and stays on the policy clock (D7, precised).
- *Text and tables.* Eight bool decodes, so no other projection cell compares the model
  point's text, and none calls a label accessor. One reader per table, keyed by attained
  age, with the limiting-age test in the monthly cell. `surr_charge_rate(y)` reads
  `Data.surr_charge_scale()`, whose years are read by value once, where S took `int()` of
  the raw years.
- *`proj_len()` refuses* a point at or past the stop rule, and a contract owing nothing,
  with one message per form.
- *Data's checks*, beyond the template's: each life is a probability, and life 2 is 0 on a
  single-life contract; the fraction is 0 or more and below 1; the CMT change is a finite
  number; a contract not yet in payment holds the annuity date's state; each death month
  is blank or whole, read by value on either basis, and returned as the numbers checked;
  on the scenario basis, each life's status matches its month of death; and a fraction
  appears only where a commutation could have been taken.
- *The cap on mortality.* S caps `q_be` and `q_rated`, and SEC keeps both unchanged (§5.1,
  step 6). A test asserts `(float, 1.0)`, the deaths and finite float64 reports where a
  cap binds: at the limiting age on the anchor's twin, and on rows in payment, one of them
  rated past 1 at 117.
- *No premium and no acquisition* on an annuity commencing later, which may commence at
  most 120 months on.
- *The name clash.* `pols_new_biz` exists. The module keeps S's ban on `pols_lapse`,
  `lapse_rate`, `surr_value`, `cash_value` and `av_pp`, and no convention needed an
  exception.
- *`result_pols`.* `pols_if` comes first and `pols_new_biz` second, then S's seven
  columns; T1 exempts it, and the module compares it with S's column by column.
- *The splice.* Inflation is set to 0 and utilization to 0.5 in both models, and
  `cmt10_shift` to 0.005 in S, where it is each point's change since its own annuity date;
  SEC's is 0, the change being in the restated rows' column. The improvement scale is set
  apart by age and sex in both copies, and eleven variants of S's points are added to the
  copy of S's table. T2 and T3 compare to 1e-9 relative with no floor (§5.2, precised),
  and exempt `proj_len` and `payment_surv_mth`. The splice's S sweep leaves out
  `check_lives_roll_fwd`, which is quadratic, about 120 MB per table-basis point.
- *The rules test* adds R1a's ranges, and has no `LOOK_AHEAD`, WholeLife's allowance: SPIA
  admits no read beyond `t + 1`.
- *T5* reads each case with a model of its own, refused by the one rule under test (the
  fraction at the annuity date is the stated exception), and refused again through a
  projection.
- *T4* multiplies the count by 2.5 with the splice's switches on, and asserts every
  counted cell, those no report shows among them (§5.2, precised).
- *The runner* keys each point as M14's `run_sec.py` does, freezes the collector after the
  read and before the projections, releases each point, and in `--block` asks every point
  for its frame first.
- *M14's carried items not yet taken.* Built on M2's tip, SPIA took `codes=` at landing,
  but its runner does not yet carry Term's `--cython`, `--build` and `_tool()`, nor its
  module the `create()`-copy test, and `proj_len()` does not yet check the three bounds
  §7.9 *C* names; SPIA's C step takes them up.

**Measured for K6 and F7.** Every time below was taken with other workflows sharing the
machine.
- *Time.* By default the module ran 139 passed and 52 skipped in 3 min 11 s and 3 min
  16 s, and over the full grid 191 passed in 4 min 03 s and 4 min 25 s, each run peaking
  at 2.72 GB in one process. The core saves about a minute, because most of the module's
  time is fixed: the count scaling (27 s), the splice's fixture (20 s), the clock test's
  fresh sweep (14 s), `run_sec.py`'s subprocesses (13 s), the extract (12 s), the S
  fixture's sweep (10 s) and the edges (9 s). Each future row is compared with S read with
  the CMT's change at 0, its S point swept by the case and released with the row, which
  costs a sweep a row and no memory. The SEC conventions, 31 passed and 2 skipped, take
  44 s and 48 s, of which T1 is 25 s, at 2.26 GB. On M2's tip with SPIA added, the uslib
  suite ran 1,468 passed and 163 skipped in 14 min 30 s and 14 min 53 s, peaking at
  2.90 GB to 2.92 GB; SPIA's own share is about 4 minutes, from its module and conventions
  measured alone. As landed, on M14's tip, it ran 1,535 passed and 163 skipped in 16 min
  36 s (*Verified at landing*, below).
- *Depth.* A cold `net_cf` of the last month runs one cell a month back to `t_entry()`,
  plus a fixed overhead. On the anchor's 696-month table-basis frame it runs 706 cells
  deep, 696 of them `lives_if`, a recursion limit of 705, against 705 cells in
  `SPIA_US_S`. It runs 702 on the scenario basis (695 `commute_frac_cum`), 654 on the cash
  refund in payment 13 months (647 `cum_annuity_pp`), and 706 again on the point
  commencing 13 months on. At the longest cover, issue age 18 and 1,224 months, it runs
  1,234 cells (limit 1,233), both at the valuation date and commencing 120 months on. An
  ascending sweep runs 10 deep (limit 9). `CALL_DEPTH` is 40 and `CHAIN_OVERHEAD` is 16.
  In the modelx export, the cold call needs a recursion limit of 1,438 on the table-basis
  anchor, 1,409 on its scenario twin and 2,494 at the longest cover; the ascending sweep
  needs 128.

**Faults.** Each fault went alone into its own copy of the library, and the tests aimed at
it ran through the gate.
- *Tests stage:* 54 faults and a control, each run on the module or on the tests aimed at
  it. Every fault failed some test, one of them, the scenario step put on `t` in
  `check_lives_roll_fwd_resid`, only the conventions' `test_every_model_point_projects`,
  since the module keeps `check_lives_roll_fwd` out of its sweeps; the control passed.
- *Review (tests lens):* 25 faults, 5 of which survived: the count truncated to whole
  contracts, the commutations and the surrender charge per point instead of by the count,
  the commutation check's certain-period condition dropped, and the rating's cap as the
  int 1. The fix made each fail, through a count of 2.5 times the table's, a case with a
  certain period of 0 months, and the cap's type asserted with its value.
- *Fix stage:* 21 faults and a control; 19 fail and two pass by design. F44, `Data`
  returning the death columns as read, is an equivalent mutant on every table the checks
  accept. F51b moves T2 and T3 back to the default absolute floor of 1e-9 and passes; at
  no floor, the same fault (F51) fails 24 cases, which is why T2 and T3 use no floor.
- *Re-review:* re-ran eight faults, all failing, and found the text death-month case
  refused by two rules.
- *Second fix:* F38 (the CMT column ignored) fails 9 core splices and the CMT,
  commutation-fraction and simple-discount tests. F39 (the Reference ignored), F52 (the
  Reference applied to future business, as before the fix) and F53 (the Reference applied
  to contracts in payment only) each fail the CMT test. F50 (the spec's CMT state at 0)
  fails 9 core splices and two product tests. F43 (`Data`'s death-month check dropped)
  fails all four death-month cases. F49 (a 1% survival error below 1e-8) fails 17 core
  splices and 7 core future rows. The control passes.

**Carried into DIA (M12) and RILA (M10): the payout chassis.** Each item goes to DIA's
stream from this landing, and DIA's record says what it took.
- *The count.* Copy SPIA's: `policy_count` on the books from issue to the stop rule, never
  decremented, with `BEF_NB` a closed form and mortality per life in `lives_if`.
  `DIA_US_S` weights its flows by a constant `pols_if_init` as `SPIA_US_S` does, so its
  `pols_if`, `pols_if_init * l_last`, is weighted by survival on that count and is not
  `BEF_DECR` (D5). Register an exemption of DIA's own, with its reason, rather than widen
  `closing_pols_if` or decrement the count: a decremented count cannot carry two
  independent lives.
- *Survival status per life.* Copy the `lives_if_init_1` and `_2` probabilities (1 at
  issue; life 2 is 0 on a single-life contract), `lives_if` on the valuation clock based
  at `t_entry()` and 0.0 before it, `Data`'s probability, single-life and at-issue checks
  (DIA has no scenario basis), and the roll-forward check rebuilt from the opening state.
  (Precised at M12: `DIA_US_SEC` restates the recursion month by month from the opening
  state instead, so a misindexed or mis-based recursion fails it at a cell a month; it
  shares the monthly rate with `lives_if`, which T1 and T2 check. SPIA's running product
  would hold 70 to 116 MB on each of DIA's 720-month points.) This is §7.12's projection
  survival; DIA's pricing survival stays at issue.
- *Certain periods.* Copy `certain_floor` on the payout clock (below), the certain months
  left read from it, `stop_mth()`, and `proj_len()`'s refusal of a contract owing nothing,
  worded by form and adapted to deferral.
- *Static schedules.* Base a deterministic schedule's recursion at the valuation date's
  key, one loop there and nowhere else (R2, precised): at every key before it the search
  is quadratic. §7.12 carries DIA's CP, B and G as opening state, so the pattern serves
  only a schedule DIA does not carry as a column. Clamp at 0 any read at the previous
  payment point. (Precised at M12: §7.12 now carries CP and B alone, and G is such a
  schedule, which needs no column. An installment refund's derived period `n_R` is a fixed
  point of the whole payout schedule, found by `certain_mths_refund()`'s ascending search
  from the income start month, so a contract long in payout reads G at every key from `T`
  up, a cell deep each. The valuation-date base serves the refund balance, the one other
  reader of G, and a cash refund asks for no key before the valuation date's.)
- *The payout clock.* SPIA's `_pm(k)` cells count months from the annuity date, which is
  DIA's payout clock: key DIA's payment months, COLA and certain floor on
  `duration_mth(t) - income_start_mth()`, keep the policy clock from issue for premiums
  and deferral events, and name each cell's clock. (Precised at M12: `DIA_US_SEC` keys
  them by policy month from issue and forms `k - T` inside, so that S's
  `cum_annuity_pp(t)`, the premium months and the option months compare at S's keys
  unshifted with no `twin_arg_map`; a payout-clock key would be negative in deferral.) `T`
  and the option months stay policy months, compared with `duration_mth(t)`.
- *Commutation.* DIA's is not SPIA's. It is one exercise named on the model point,
  `commute_frac` from `commute_mth` on, so `commute_frac_cum` follows from the policy
  clock, `duration_mth(t) >= commute_mth()`, and takes no column, and there is no
  withdrawal. What an exercise before the valuation date leaves is the frozen weight
  `commute_weight`, `l_last(t_c)`, an opening-state column (§7.12). Key the commuted
  value's loop over the remaining guaranteed payments on the payout clock, as SPIA's
  `annuity_pp_sched_pm(k)` is keyed (R1a). (Precised at M12: `DIA_US_SEC` keys it by
  policy month from issue, as *The payout clock*, above, has it.)
- *The reference rate.* Read `ref_rate_shift` as SPIA's CMT on one path (D7, precised).
  `ref_rate_shift_init` is the change in the reference rate from issue to the valuation
  date, of either sign, and 0 on a contract issued at or after it. The Reference is the
  change made at the valuation date, seen by every contract on the books then and by none
  issued later. DIA's floor applies to the whole change since issue,
  `max(0.0, ref_rate_shift_init() + shift)`, where `shift` is `ref_rate_shift` on a
  contract on the books at the valuation date and 0 on one issued later. It does not apply
  to each part, so `Data` refuses only a column that is not a finite number. Test it as
  SPIA's is tested, at two values of the Reference, and also with the column and the
  Reference of opposite signs, where the two floors differ: a column of -0.01 at the
  Reference 0.005 discounts at `i_p + m_c`, and a column of 0.01 at -0.005 at
  `i_p + 0.005 + m_c`, where a floor on each part would give `i_p + 0.005 + m_c` and
  `i_p + 0.01 + m_c`.
- *Text and tables.* Decode each text column a projection cell branches on into a
  validating bool that reads the model point, one variant per category, with `UNDECODABLE`
  per decode; S's label accessors stay unchanged and uncalled. Route each table through
  one age- or year-keyed reader, with the omega test in the monthly cell. Validate every
  month-valued column DIA reads, the income start month and the option months,
  `adjust_mth`, `adjust_start_mth`, `accel_mth` and `commute_mth`, as whole by value in
  `Data`, a month written as text refused by name, and return it checked.
- *Improvement* is calendar-dated, so it stays on the policy clock and the splice does not
  neutralize it. Check `DIA_US_S`'s caps on `q` and assert `(float, 1.0)` where they bind.
- *Tests.* For each schedule DIA bases at the valuation date's key rather than carrying as
  a column, the static-schedule test: bit for bit against S at every key, with a fresh
  read of a contract in payment reading it from the valuation date's key only. Also the
  depth test with a refund in payment beside the longest cover, futures 13 months on in
  the guard test, and `check_lives_roll_fwd` left out of the swept splice copies.
  (Precised at M12: `DIA_US_SEC`'s check, restated a cell a month, stays in them.)
- *RILA (M10).* `RILA_US_S` projects no payout: its forced annuitization is
  `pols_maturity`, a lump sum at the account value, which it leaves to the
  immediate-annuity chassis. Copy SPIA's patterns, the decodes, the age-keyed readers,
  valuation-clock inflation and `proj_len()`'s refusal of a point at or past its maturity,
  and keep the maturity as RILA's own claim; a hand-off to `SPIA_US_SEC` is outside Phase
  1. Were it made, the hand-off would be `SPIA_US_SEC`'s in-force interface: the survivors
  as `policy_count`, `duration_mth` counted from the annuity date, survival 1 per life,
  and no fraction or CMT change at the annuity date, a contract maturing after the
  valuation date being an annuity commencing later. The term-start index level and MVR of
  a term begun before `t = 0` are opening-state columns (D7), of which `cmt10_shift_init`
  is the level-shift case.

**Carried into every product still to come.** The first, second, fourth and fifth were
found by faults that passed until they were made, the third by the review, and the rest
while building:
- T4 at a factor that is not whole, with every assumption that ships at zero switched on,
  asserting each counted cell no report shows (§5.2, precised).
- T2 and T3 with no absolute floor wherever a compared value can fall below about 1e-7,
  except on the roll-forward residuals, which keep the 1e-9 floor: MYGA's, FIA's, VA's and
  RILA's are rounding, up to about 3e-11, in most months, where SPIA's are exact zeros
  (§5.2, precised). A fault sweep includes a fault below the floor.
- A level change since each point's own start, as S carries it in one Reference, is split
  in two: an `_init` column, the change seen by the valuation date, and the Reference, the
  change made at the valuation date on the one path every point shares, which no contract
  issued later sees (D7, precised).
- Each cap or floor is tested at a value where it binds with an effect: the splice's one
  switch value can leave it idle, as SPIA's residual floor never capped a withdrawal at a
  utilization of 0.5 and was asserted at 1 instead.
- Each malformed case is refused by one rule only, checked by dropping each rule, and each
  refusal is read through a projection as well, through the base `Projection`'s default
  point.
- A splice row is recorded for the rules test before it is compared with S, because the
  comparison evaluates SEC cells at S's cached keys, a negative one among them.
- A module that holds swept models freezes them out of the collector and undoes the freeze
  at teardown, after closing them (`gc.unfreeze()`, then `gc.collect()`); quadratic checks
  stay out of swept splice copies.
- A set-apart edit of an input is checked to move no branch, and the core is chosen by
  line coverage.

**Carried into Phase 2.**
- *Caches and bounds:* §7.9's *C*. The figures above size `sample_sec.py`,
  `run_sec.py --cython` and the Windows job's stack. The monthly survival chain is S's own
  and bit for bit. If the first Windows run fails, the remedy is a survival recursion
  blocked by year.
- *T1 and codes:* S's `claims(t, kind=None)` keys need a T1 `arg_map` at stage `EC`.
  `_mismatches`, the module's one call of `twin_mismatches`, passes
  `codes=codes(sec_proj)` from the landing on, so the splice's comparisons take Phase 2's
  codes when they come; `_code(space, label)` needs the int timing and kind References on
  `Projection`, visible from its ItemSpaces.
- *Accessors and decodes:* S's label accessors stay reporting cells; C5 checks the three
  that return a column of their own name, and R17 and C5 need extending for
  `payment_timing()` and `sex(life)` (§7.9 *C*). The eight decodes and the two age readers
  move onto `Data` arrays, `cmt10_shift_init` becomes a float vector read in the same
  order, and `commute_disc_convention` an int code.
- *`IN_COVER_ONLY`* (`age`, `calendar_year`, the two age readers, `commute_util_rate`,
  `surr_charge_rate`) has no guard of its own. The guard test holds that no formula
  reaches these cells outside cover, before the annuity date or at `t = proj_len()`.
- *Engine functions:* none and no float-parameter cell. The commuted value and the
  withdrawal are loops in int-keyed cells; `horizon_mths` keeps S's two-element list,
  which Phase 2 removes. `commute_disc_rate` reads `t_entry()`, an int comparison.
- *T5 at stage `EC`:* `MALFORMED` reads each refusal through `model.Projection.result_cf`,
  the base Space's default point, which must still read `Data`'s table first.
- *Static bases:* `cum_annuity_pp(k)` is based at `duration_mth(t_entry())` and
  `annual_income(y)` at `policy_year(t_entry())`, clock reads that no month-keyed cell
  reaches before `t_entry()`. The C step bases them at `max(duration_mth_init(), 0)` and
  `max(duration_mth_init(), 0) // 12 + 1`, the same values, so no number moves (R2,
  precised at M12).

**Carried, outside the SEC models.** Seven S-side items for §8.2 item 4, found in
`SPIA_US_S`; the first two are fixed in neither model, the rest in `SPIA_US_SEC` only:
- S nets a cash refund against the unreduced schedule, which is the amount paid only at a
  survivor percentage of 100%, the one percentage [S5] offers a joint cash refund at, and
  neither model refuses a joint cash refund below 100%.
- Where an installment refund never repays at a frequency below monthly in advance, S's
  trim pays `P - G(n_R - step)` in month `n_R - 1`, which has no instalment: S point 7 at
  B(1) 1,500, quarterly in advance, pays 375.00 at month 657 and 17,875.00 at month 659,
  100,375 against a premium of 100,000. SEC reproduces S.
- On a refund paid in advance below monthly whose first instalment repays the premium, S's
  trim reads `cum_annuity_pp(1 - step)`, below 0; SEC reads `G` at 0.
- `surr_charge_rate` takes `int()` of the scale's raw years; SEC checks the scale once in
  `Data.surr_charge_scale` and takes its extents and rates from it.
- `death_mth` truncates a fractional month, so -0.5 is a death in policy month 0, and on a
  month written as text raises `int()`'s own message without naming the point; SEC's
  `Data` refuses both, naming the point.
- 24 docstring lines exceed 92 characters, 23 in `Projection`, 20 of them in the symbol
  map, and one in `Data`.
- The **[std]** marks inside the literal blocks of the `mort_rate` and `commuted_value`
  docstrings render with their asterisks.

**Landing.** Rebased from bbb99a9 (M2) onto 0ac94f1 (M14). uslib's `index.md` took the one
conflict, the sentence that lists the SEC models, merged as M14 left it plus SPIA.
`_mismatches` took `codes=codes(sec_proj)` (*Carried into Phase 2*). Ten comments and
docstrings in the test module that cited a working note no reader can open, and two that
cited the build's design and its critique, now say what they meant without them. A review
of this record, under two lenses, found 24 defects in it, 5 of them major, and each is
corrected above: among them, the DIA hand-off had named SPIA features DIA lacks, and T2's
floor rule had left no floor on roll-forward residuals that are rounding around 0.

**Verified at landing**, on the tree as committed, with two other workflows sharing the
machine. The uslib suite, with modelx-cython installed and so the compile tests included,
gave 1,535 passed and 163 skipped in 996.30 s (16 min 36 s), 171 passes and 54 skips more
than M14 landed with: SPIA's module, 139 and 52; its SEC conventions, 31 and 2; and the
one compiled convention that reads every SEC model. Over its full grid, SPIA's module gave
191 passed in 259.78 s, and the `cython` selection 11 passed and none skipped under
`USLIB_REQUIRE_CYTHON=1`, in 169.29 s. doccheck built 485 pages with 0 warnings.
`gen_sec_points.py --check` found the files of `Term_US_SEC`, `WholeLife_US_SEC` and
`SPIA_US_SEC` current, and `gen_sec_fingerprint.py Term_US_SEC --check` reproduced the
fingerprint. md_lint reported 0, `gen_scaffolding.py --dry-run` 0 files in each of the six
libraries, and `gen_citation_links.py --dry-run` nothing on its 288 source tags. A
case-insensitive search of `model_point_table_sec.csv` for the 134 names, forms and hosts
that `immediate_annuity/sources.md` cites found none. After the last edits, to comments
and docstrings in the test module and a comment in `sec_support.py`, SPIA's module and the
SPIA conventions, the compiled one among them, gave 195 passed and 55 skipped in 256.93 s.

### 7.10 MYGA — `MYGA_US_SEC` (E: M, C: M)

*Today:* the policy clock, new business only. `duration_mth(t) = t` exists but nothing calls
it. The premium, commission, acquisition expense and `prem_to_av` sit on `t == 0`, and
maturity on `t == proj_len() - 1`. Timings: `BEF_DECR`, `BEF_MORT` (after annuitization),
`BEF_LAPSE`, `AFT_DECR`.

*E:*
- The opening state is ten columns, each read off S as S's own formulas read it. Entering
  month 0: `av_pp_init`, above 0 on a contract in force; `mgsv_pp_init` and
  `prem_accum_gmir_pp_init`, the Model #805 floor and `P_accum@GMIR`, either of which may
  be negative, since S floors neither; `interest_credited_pp_init`, which the
  minimum-interest cap and the interest-only allowance read; and `free_wd_remain_init`,
  the allowance unused, which the projection reads off an anniversary.
- At the anniversary on or before the valuation date (D6):
  `interest_credited_pp_prev_anniv_init`, which next year's interest-only allowance reads,
  and `free_wd_allow_init`, the allowance of the contract year under way: under `pct_av`
  `free_wd_rate` times that anniversary's account value, under `interest_only` the
  interest of the year before, which no anniversary value gives. The projection reads the
  allowance only on a valuation on an anniversary; off one, only `Data`'s remainder check
  reads it.
- `tax_basis_pp_init` is S's `tax_basis_initial` renamed: the basis entering month 0, or
  at issue on new business, where it keeps S's meaning. `credit_rate_init` and
  `mva_ref_yield_locked_init` are the declared rate and `i0` in force entering month 0,
  read where the redeclaration or the period start precedes `t_entry()`; one at month 0
  reads the scenario (D6, precised at M7).
- S's `av_pp_init()` and `mgsv_pp_init()` compute `P (1 - load_prem_rate)` and `0.875 P`.
  In SEC they read the columns, and the two rules credit the issue month, through
  `prem_to_av_pp` and the new `prem_to_mgsv_pp` (D6, precised at M7). `Data` compares
  amounts of money to a cent, so that an extract may carry each to the cent, and the
  projection starts from the amounts as carried.
- The guarantee-period position, the surrender-charge clock, the window, the base lapse
  and the age derive from `duration_mth`, every renewal period being `n` years.
- R1a, four violations in the model and one in S's runner, whose `lapse_rate(12 n)` takes
  a policy month as `t`:
  - `free_wd_base` reads `av_pp_at(12(y-1))`;
  - `free_wd_allow` reads `interest_credited_pp(12(y-1) - 1)`;
  - `credit_rate` reads `market_rate(redeclare_month)`;
  - `mva_ref_yield_locked` reads `mva_ref_yield(gp_start_month)`.
  `redeclare_month` and `gp_start_month` keep returning policy months, and the two cells
  that read them turn each into a valuation month once. Every other test of `t` against a
  contractual event, every recursion's base and the guards outside cover follow template
  items 3 to 6, D4 and D7, and `model-sec.md`'s *Departures* lists each cell.
- Counts: `BEF_NB` is the one timing added. S's `BEF_MORT` means "before mortality", so no
  S timing clashes with BasicTerm_SE's.
- Clocks: the rate scenario moves to `t`, and each of its three shipped scenarios is one
  flat row, so the move changes no shipped number. Expense inflation moves to `t` too,
  `(1 + i)^(t // 12)`, so a point in force carries its expenses in valuation-date dollars
  (D7). Withdrawals stay on the policy clock.
- Chains: every chain is one cell a month. A cold `net_cf` of the last month runs one cell
  a month back to `t_entry()` and at most 16 more: 494 to 496 cells on a 480-month frame,
  against 1,437 in S, and 1,214 at issue age 0.
- Text: the five categorical columns S branches on, `renewal_architecture`,
  `free_wd_rule`, `mva_family`, `mva_cap_rule` and `mgsv_wd_convention`, are decoded once
  a point into fourteen bools, the `is_*` cells, each read where S asks its question, so
  that a value S does not know is answered as S answers it; R6 moves the decodes into
  `Data`. No other projection cell compares a model point column's text, and none calls a
  label accessor, which are left to reporting. The text a projection cell still compares
  in a branch is S's own: the timing and kind strings, which Phase 1 keeps and R9 numbers,
  and `surr_charge_rate`'s test for `"none"` on the schedule `surr_charge_id(t)` names,
  part of the surrender-charge join that R7 re-keys. The four joins on text keys stay S's
  for R7, each in the one cell that reads its table: mortality on the point's `sex`, the
  scenario on its `scenario_id`, the withdrawals on its `wd_schedule_id`, and the
  surrender charge on that schedule. `Data` checks each key before a projection joins on
  it (*Record — M7*, *Data's checks*).
- Tables: S's six readers keep their code. Beside each, a `Data` cell reads the table's
  keys by value, once, checks them and the values, and returns the table indexed by the
  checked keys, and the projection reads the table there alone: `mort_rates`,
  `surr_charge_scales`, `surr_charge_age_caps`, `rate_scenario_steps`, `wd_schedules` and
  `mva_factors`. A key that is not a whole number, text and a blank among them, a blank
  text key, a value out of its range, a repeated key, and a gap where the projection reads
  every year or age between a table's first and last are refused, naming the file, the
  column and the lines, and so is a surrender charge table without the `initial` and
  `renewal` schedules. The age cap's extents and the duration factors' last year are int
  cells from the same keys, and those two tables are read through cells keyed by the age
  and the whole year, `surr_charge_age_cap_at(a)` and `mva_factor_at(k, column)`. No
  mortality cap: no factor multiplies the table rate, and `Data` refuses a rate outside 0
  to 1.
- Splice months: 11 and 12, either side of the first anniversary; 30, after point 5's
  excess withdrawal; 59 and 60, the initial term's last month and its window, where the
  rate is redeclared and `i0` re-locked at `t = 1` and at `t = 0`; 61 and 89, a renewal
  period whose rate and `i0` were fixed before the valuation date (point 3, which
  redeclares at each anniversary, last at 60 and at 84); and 479, the last covered month.
  Four variants, in the splice's copy of S's table only, carry the categories S's points
  do not: point 1 female at a GMIR of 2%, with the floor's $50 charge and 2% premium tax,
  at 12, 30 and 61; point 3 at a GMIR of 3% as an IRA with no basis, at 61, 72 and 89;
  point 5 with a seven-year guarantee period, at 30, 83 to 85 and 100; and point 4 issued
  at 85, under the attained-age cap, at 59 to 61, 125 and 179. Future rows are issued 1
  and 15 months on, the variants 1 month on. The full grid is 72 T2 and 18 T3 cases, and a
  core of 17 and 7 runs by default (*Record — M7*). Two core rows are each the only one to
  show a fault: point 5 at 11, interest-only in a contract year's last month, which
  measures the allowance of the year after next from the interest at frame month 0, and
  point 4 at 89, a renewal period under way, whose `i0` stands apart from the yield at the
  valuation date.

*C:*
- 33 attribute cells, ten more than S's 23: `policy_count` in place of `pols_if_init`,
  `duration_mth_init` and nine opening-state accessors. `free_wd_mva_exempt` becomes an
  int, not a numpy bool.
- To arrays, each from the checked table `Data` already returns, its keys read by value
  and refused by name: scenario rates step-filled into `[scenario, month]`; withdrawals
  into `[schedule, month]`; surrender charges into `[schedule, year]`; the age cap into
  `[age]`, its extents already int cells; the MVA duration factor into `[year, column]`,
  read through `mva_factor_at`; mortality into `[age, sex]`.
- The fourteen `is_*` decodes move into `Data` (R6). `surr_charge_id(t)`, a string cell,
  becomes an int code, and the four joins on text keys are re-keyed (R7). Timing, kind and
  `scenario_rate`'s column name become codes (R9), and its list comprehension and `max`,
  kept from S, a loop (R12).
- `claims(t)` called from `net_cf` with `kind=None` becomes an explicit `ALL` kind.
- R14: `mva_pp_on` and `mva_factor_geometric`, each inlined into the cached cell that
  calls it, or keyed by an int code. `mgsv_rate_statutory`, `mva_ref_term_years` and
  `mgsv_rate_is_compliant` are never reached (below). S's tests call those three and
  `mva_factor_geometric` directly, so S's cells stay for them, admitted by name, or go
  with a T1 exemption (R14). `math.floor` and `math.ceil` become integer arithmetic (C5).
- Never reached in S: `tax_basis_pp`, `taxable_wd_pp`, `tax_basis_pp_init`,
  `claims_over_av`, `gp_end`, `duration_mth`, `mgsv_rate_statutory`,
  `mgsv_rate_is_compliant`, `mva_ref_term_years`, `policy_id` and `tax_status`;
  `tax_basis_pp_init`, the cell that reads S's `tax_basis_initial`, was found at M7. In
  SEC `duration_mth` is the clock, which every contractual cell reads. The other ten stay
  unreached on the committed rows, and so do eight of S's label accessors that no
  projection cell calls any more, `sex`, `renewal_architecture`, `free_wd_rule`,
  `mva_family`, `mva_cap_rule`, `mgsv_wd_convention`, `scenario_id` and `wd_schedule_id`:
  `sample_sec.py` must call each, or the registry's `"reporting"` name it (R17).

#### Record — M7, done 2026-11-02

Built in two commits, as D1 requires: `MYGA_US_S` copied with only `_name` changed, then
the enhancement, by M1's process: a design prototyped and critiqued before the build,
tests written against the build and checked by injected faults, then a review under the
three lenses. The review made 30 findings, one a blocker and 11 major, some of them one
defect seen under two or three lenses. The blocker was that a key written as text in an
assumption table silently zeroed every surrender charge or every withdrawal, or removed
the age cap, and the fix has `Data` check every table's keys. The first fix took 29 of the
findings. For the 30th, that no test tells the block's `groupby` sum from a plain running
sum, it took the finding's own alternative and recorded the rule as review-only, since the
runner prints to the cent, where a running sum's last-bit differences cannot show. A
re-review of the fixes made five findings, one of them major: the half-cent tolerance the
first fix gave `Data`'s money rules equalled the largest error that carrying one amount to
the cent makes, so ties fell to floating point, and 5.1% to 5.3% of correctly rounded
anniversary allowances, in a sample of 200,000, were refused. The second fix compares
those rules to a cent, prints "1 month" where a point is a month from the valuation date,
tests the second-year interest-only rule at both ends of its window, says which text a
branch still compares, and has `Data` check each point's join keys. It rejected one
instruction as given, that a scenario must set a level by `t = 0`: T3's scenarios,
re-based to their issue months, set none before issue, and under that rule all seven core
T3 cases failed. The check is made per point instead, against the point's first month on
the books. Eleven defects found in `MYGA_US_S` are carried below: eight are fixed in
`MYGA_US_SEC` only, and three in neither model. M7 was built on M2's tip and rebased onto
M11's at landing (*Landing*, below).

**What exists now.**
- `MYGA_US_SEC` at stage `E`. Of `MYGA_US_S`'s 127 `Projection` cells, 53 are unchanged,
  13 have a new docstring only and 61 are rewritten; none is removed or renamed. It adds
  30 cells, 157 in all: `policy_count`, `duration_mth_init`, `maturity_mth`, `t_entry`,
  `is_active` and `pols_new_biz`; seven opening-state accessors; `prem_to_mgsv_pp`, which
  credits the floor's issue value; a reader keyed by age and one keyed by whole year,
  `surr_charge_age_cap_at(a)` and `mva_factor_at(k, column)`; and fourteen decodes. `Data`
  keeps S's eight cells, rewrites the table reader, which now checks the table as it reads
  it, and gives four readers new docstrings. It adds nine cells, the six checked tables
  and three int extents, and the Reference `future_horizon_mth = 120`.
- `model_point_table_sec.csv` holds 14 rows generated from MYGA's `SecSpec`. Seven are S's
  points as twins, issued at the valuation date. Six are derived: the anchor (S point 1)
  on its first anniversary, month 12, with year 2's allowance; the interest-only point (5)
  at 30, the month after its excess withdrawal; Camp B (3) at 30, inside its initial term;
  the registered-contract point (4) at 60, in its window; the stress trace (2) at 61, the
  month after its window; and Camp B at 479, its last covered month. The last row is S
  point 1 issued 15 months on. A case-insensitive search for the publishers, products,
  form numbers, hosts and towns that `fixed_deferred_annuity/sources.md` cites finds none
  of them in the table.
- `tests/test_fixed_deferred_annuity_us_sec.py` has 34 tests and 223 cases: T2 on 72
  splices; T3 on 18 future points; T5 on 84 malformed rows and 18 malformed assumption
  tables; the rules test, core and full; and 29 tests of one case each, T4, T6, the depth
  test, the clocks, the opening state, the runner and the product's own facts among them.
  By default a core of 17 splices and 7 future points runs, 156 cases in all. A test
  asserts that the core reaches each category of the five text columns, each kind of
  valuation month, each opening-state column and each branch it names in the frame; one
  branch, the dynamic lapse switched off by a surrender haircut of 20% or more, is reached
  by no grid. The other 67 cases carry `sec_full` (K6). S has no in-force point, so
  `IN_FORCE_TWINS` is empty. The SEC conventions, 33 cases, pass but for
  `test_net_cf_is_income_positive`, which skips, as it does for `MYGA_US_S`, since neither
  has a `liability_cf`.
- `run_sec.py`; `model-sec.md`, with *The opening state*; the registry entry with its
  `INPUT_FILES`; and four generated pages, with the product page's toctree. doccheck
  reports 489 pages and 0 warnings as landed, 485 on M2's tip.
- Shared files, added to in place: MYGA's spec and its state extractors in
  `sec_support.py`; the entry in `us_registry.py`; and MYGA's row of the models table in
  uslib's `index.md`, with the sentence that lists the SEC models at landing.

**Departures and precisions from `MYGA_US_S`.**
- *The clock and the frame* (D3). `duration_mth(t) = duration_mth_init() + t`, a closed
  form, and `proj_len() = maturity_mth() - duration_mth_init()`, which refuses by name a
  point at or past maturity. `maturity_mth()` is new and keeps S's frame from issue,
  `12 (100 - age_at_entry)`. Every contractual test moves to the policy clock, §7.10's
  four R1a sites among them.
- *Counts* on BasicTerm_SE's pattern (D5). `pols_if_at` gains `BEF_NB` beside S's four
  timings, `pols_new_biz` is new, and `result_pols` puts it second. The count's chain is
  one cell a month, where S's ran two.
- *The opening state* is ten columns (§7.10, *E*). The issue rules of S's `av_pp_init()`
  and `mgsv_pp_init()` credit the issue month, and the two cells read the columns, 0 on
  new business; T1 exempts both. `tax_basis_initial` is renamed `tax_basis_pp_init`
  through the spec's `column_map`, and `Data`'s no-state check exempts it (D6, precised).
- *The allowance of the year under way* is carried, with the interest at its anniversary,
  rather than the anniversary's account value, because the interest-only allowance is the
  interest of the year before, which no anniversary value gives.
- *One cell a month.* S's account value ran three cells a month and its free-withdrawal
  carry two; each now runs one. On the twins every account value, floor, `P_accum`,
  interest, basis, allowance, count and `net_cf` is S's bit for bit at every month.
- *Contract-year state* keeps S's keys, `free_wd_base(y)` and `free_wd_allow(y)`, so T1
  compares S's goldens on them. T2 skips each contract year that closed before a restated
  row's month, and the base of one under way that opened before it, whose allowance the
  row carries, and the rules test asserts that no year closed before the valuation date is
  asked for (§5.2, precised).
- *Inputs on their clocks* (D7). The rate scenario is read on `t` and the withdrawals on
  `duration_mth(t)`. Expense inflation is `(1 + i)^(t // 12)` from the valuation date, so
  point 8's maintenance expense is S's divided by 1.025. Acquisition is charged per
  contract issued, in the issue month, uninflated.
- *Guards outside cover.* Fifteen cells that S leaves unguarded, the decrements, the
  withdrawals, the table and lapse readers and the floor's charge among them, return zero
  or `False` outside cover before any table or rate is read.
- *Text and tables* (§7.10, *E*). Fourteen bool decodes; every table read through `Data`'s
  checked copy; the age cap and the duration factors read through cells keyed by the age
  and the whole year.
- *The checks* scale their tolerances by `max(policy_count, 1)`, since a residual is
  rounding on that many contracts, and their verdicts are loops.
- *No mortality cap* (§5.1, step 6). No factor multiplies MYGA's table rate, which is
  0.263 at most in cover, and `Data` refuses a rate outside 0 to 1.

**Departures and precisions from the template** (§7.1 and §7.2, *Records*).
- *No `LOOK_AHEAD`*: no read goes beyond `t + 1`.
- *The future row* is issued 15 months on, so that a missing guard reads contract year -1
  before issue. T3 issues every S point 1 and 15 months on.
- *Signed and issue-dated state.* The floor and `P_accum` may be negative, and
  `tax_basis_pp_init` is not 0 on new business.
- *The splice* switches on `free_wd_util` 0.5, `renewal_spread` 0.75%, `expense_acq` 150
  and `load_prem_rate` 1% in both models and sets inflation to 0. Its copies step the
  scenarios, raise the renewal surrender charges by 0.5% and cut the duration factors to
  years 0 to 3, and each spliced row reads its own re-based copy of its scenario, so T2
  and T3 exempt `scenario_id` (§5.2, precised). `_sweep_s` evaluates the cells S's sweep
  never reaches.
- *T5* reads each case with a model of its own, and each refusal again through a
  projection.
- *T2 and T3* compare to 1e-9 relative over the harness's absolute floor of 1e-9. M7 was
  built before §5.2 dropped that floor wherever a compared value can fall below about 1e-7
  (precised at M11). On the committed points, 12,927 of the 596,161 numbers cached outside
  the reports and the checks are nonzero and below 1e-7 in magnitude, every one a count or
  an expense.
- *T4* doubles the count at the shipped assumptions, as M2's does, and asserts both
  reports doubled and every uncounted cell unchanged. Acquisition per contract issued is
  asserted on its own, at 2.5 contracts with `expense_acq` 150, and both roll-forward
  checks at a million contracts. §5.2's T4, a factor that is not whole with every
  assumption that ships at zero switched on, was precised at M11, after M7 was built.
- *M14's and M11's carried items not yet taken.* Built on M2's tip, MYGA took `codes=` at
  landing, but its runner does not yet carry Term's `--cython`, `--build` and `_tool()`,
  nor its module the `create()`-copy test. `proj_len()` checks no contract bound.
  Mortality, the scenario, the withdrawals and the surrender charge are read in S's
  per-`t` cells, joined on text keys, not each through one age- or year-keyed cell (R7).
  The module freezes no swept model out of the collector. It records each splice row for
  the rules test after comparing it, in `_settle`, where M11's item records it before, so
  the rules test judges what the comparison evaluated too. Its core was chosen by branch
  and fault reach rather than by line coverage. Its malformed cases are each built so that
  the check it names fails first, not so that it alone refuses them, and no run dropped
  each rule in turn: with its own check dropped, a blank or a text `duration_mth` is still
  refused, by the scenario check, and the text `age_at_entry` added at landing by the
  mortality check. MYGA's C step takes up the runner's options, the copy test, the bounds,
  the keyed readers, the freeze and the malformed cases' single rule. T2's and T3's floor
  and T4, above, are §5.2's Phase 1 rules, and MYGA takes them before Phase 1 closes
  (§5.4).
- *The rules test* judges what a call reads through a cell keyed by no month against the
  month that asked (§5.2, precised).
- *The depth test* makes six cold calls on the committed model, each on an ItemSpace of
  its own: `net_cf` on twins 1, 3 and 5 and on the point issued 15 months on, and the
  floor's chain and the basis's alone. It repeats the anchor at issue age 0, on a copy
  whose mortality is extended below 40, at the valuation date and 120 months on. Each
  asserts one cell a month back to `t_entry()` and at most `CHAIN_OVERHEAD`, 16, more.

**Data's checks.** `model_point_table()` runs these in turn and refuses on the first that
fails, naming the missing column or every point that fails it:
- a missing in-force column;
- a repeated `point_id`;
- a `policy_count` that is not a number, zero or more;
- a `duration_mth` that is not a whole number, 12.0 read as 12;
- an `age_at_entry` or a `guar_period` that is not a whole number of years: S reads both
  by `int()`, which truncates a fraction without a word, and the initial-term check reads
  `guar_period` as written;
- a `guar_period` below 1 year: at 0 the guarantee-period index divides by zero, naming no
  point, and below it the projection runs a period no contract has;
- a contract issued more than `future_horizon_mth` months on: at 0, any future business,
  and the message says so; a negative horizon is itself refused;
- an account value, interest, allowance, remainder or basis that is not a finite number,
  zero or more;
- a floor, `P_accum`, declared rate or `i0` that is not a finite number;
- any opening state but the basis on a point not yet in force;
- an account value not above 0 on a point in force;
- in the first contract year, interest at the anniversary, or an allowance other than the
  issue allowance;
- on an anniversary, the two interest columns apart;
- interest at the anniversary above the interest to date;
- under `interest_only` from year 2, an allowance above the interest at its anniversary,
  and in year 2 one apart from it;
- off an anniversary, a remainder above the allowance;
- in the initial term, the first renewal month included, a rate or `i0` other than the
  issue ones;
- after it, a rate below the GMIR;
- on an anniversary under `pct_av`, an allowance other than `free_wd_rate` times
  `av_pp_init`;
- last, a `scenario_id` that is not a scenario of `rate_scenario.csv` setting its levels
  by the point's first month on the books, `t = 0` or its issue month if later; a
  `wd_schedule_id` the withdrawal table lacks; and a sex and attained age in that first
  month that `mort_table.csv` does not rate.

Every rule between two amounts of money holds to a cent (D6, precised): carried to the
cent, each amount is within half a cent of its exact value, and an allowance can miss its
base's share by half a cent plus `free_wd_rate` times half a cent, 0.0055 at the product's
10%. The six assumption tables are checked in their own cells (§7.10, *E*). Accepted,
because a contract can be in each state: a negative floor or `P_accum`; any basis at
issue, zero or more, on a point not yet in force; on an anniversary, a remainder above the
allowance, last year's; and a `duration_mth`, an `age_at_entry` or a `guar_period` written
as a float. Left to the projection, as in S: an attained age past the mortality table's
last before maturity, which raises a `KeyError`, since the maturity age is a `Projection`
Reference that `Data` cannot read, and the shipped table runs to 120, past every cover.

**Measured for K6 and F7.** Every time below was taken with other workflows sharing the
machine.
- *Time.* After the second fix, the module ran 150 passed and 67 skipped in 4 min 31 s by
  default, at a peak of 2.33 GB in one process, and 217 passed in 7 min 17 s over its full
  grid, at 2.52 GB. Before it, it ran 140 passed and 67 skipped in 3 min 58 s and
  4 min 41 s, at 2.38 GB, and 207 passed in 7 min 14 s and 6 min 55 s over the full grid,
  at 2.35 GB. Most of the default run is fixed: the extract (26 s), the committed sweep's
  fixture (25 s), the count doubling (25 s), `run_sec.py`'s subprocesses (20 s), the S
  fixture's sweep (17 s), the splice's fixture (15 s), the edges (15 s) and the depth test
  (12 s), about 156 s together. A T2 or T3 case takes up to 5 s, and the 24 core cases
  took 55 s of one suite run. In that run the module took 3 min 54 s of test time, where
  WholeLife's took 2 min 40 s, and the SEC conventions, 32 passed and 1 skipped, 37 s. On
  M2's tip with MYGA added, the uslib suite ran 1,480 passed and 177 skipped in
  14 min 50 s after the second fix, and 1,470 passed and 177 skipped in 14 min 44 s and
  16 min 29 s before it, each at a peak of 2.69 GB. As landed, on M11's tip, it ran 1,722
  passed and 231 skipped in 21 min 45 s (*Verified at landing*, below).
- *Depth.* A cold `net_cf` of the last month runs one cell a month back to `t_entry()`,
  plus an overhead of 14: 494 cells deep on the 480-month frames of twins 1, 3 and 5, 482
  on the anchor's 468 months at its first anniversary, and 494 on the point issued 15
  months on, against 1,437 in `MYGA_US_S`. On a model just read, twin 3's runs 496: its
  deepest frames are `Data`'s first read of the age-cap table, which takes its overhead to
  16, `CHAIN_OVERHEAD` itself. The floor's chain alone runs 483 and the basis's 485. At
  the longest cover, issue age 0 and 1,200 months, on a copy whose mortality is extended
  below 40, it runs 1,214, both at the valuation date and issued 120 months on, in a frame
  of 1,320. An ascending sweep of the committed points runs 17 deep, on the anchor's twin
  as it first reads the age-cap table, so under a recursion limit of 16; `CALL_DEPTH` is
  40. In the modelx export, with the limit set after the package is imported, as M1
  measured, the cold call needs a recursion limit of 1,003 on the anchor's twin, 1,012 on
  twin 3 and 2,443 at the longest cover, and the ascending sweep 54. Set before the
  import, as §7.2's and §7.9's records set it for their sweeps, the sweep's limit is the
  import's own, 128.

**Faults.** Each fault went alone into its own copy of the library, and the tests aimed at
it ran through the gate.
- *Tests stage:* 49 faults, all caught; each of the module's 29 tests of the time failed
  under at least one.
- *Review (tests lens):* 26 faults, 7 of which survived the default grid: acquisition
  charged once per model point, `free_wd_allow_init` exempted from the no-state check, the
  interest-only look-back off by one, the roll-forward tolerance unscaled, an infinite
  balance accepted, the look-back based at 0, and a plain running sum in `--block`.
- *Fix stage:* the seven again and nine of its own. All fail but the running sum, which
  survives by construction: the rule is review-only, and MYGA's C step copies Term's
  compensated `add()`.
- *Re-review:* four faults, of which two survived: the second-year interest-only rule
  narrowed to the anniversary, and widened to month 24.
- *Second fix:* 14 faults, each failing a test. The two survivors fail at months 23 and
  24. Every money rule at half a cent, the anniversary `pct_av` rule alone and the
  first-year rule alone each fail the edges test. Each join-key check dropped or misplaced
  fails, among them a scenario required by `t = 0` for every point, which fails all seven
  core T3 cases. The runner's plural restored fails the one-month runner test.

**Carried into FIA (M8), VA (M9) and RILA (M10): the deferred chassis.** Each item goes to
the products in progress from this landing (§5.3), and each record says what it took.
- *Chains.* Write every chain one cell a month, its opening inline, the account value and
  each in-year carry alike: `MYGA_US_S`'s account value ran three cells a month and its
  free-withdrawal carry two, and a cold last-month `net_cf` fell from 1,437 cells to 494
  with every value S's. FIA's account value, VA's per-fund values and RILA's accounts
  follow (D5, F7).
- *Issue values and past fixings* (D6, precised). An issue value S computes by rule stays
  a rule, credited in the issue month, and its cell becomes the in-force accessor, T1
  exempting it. A rate fixed at a past date is a `<cell>_init` column, read only where its
  fixing month precedes `t_entry()`, as MYGA's `credit_rate_init` is, with a core row
  inside each fixed period, as MYGA's at 61 and 89 are. In each product still to come, a
  value fixed at a term's or a segment's start takes DIA's frozen-weight shape instead, as
  RILA's `cap_rate_init` and its five term-start market values do (D6, precised at M10).
  Keep S's month-valued cells, as MYGA keeps `redeclare_month` and `gp_start_month`, and
  convert once in each reader.
- *Year-opening state.* Keep S's contract-year keys, with T2's `_on_the_books` and the
  rules test's year check, and carry each product's own state: FIA's year-open account
  value and F, VA's withdrawals used this year, RILA's `av_pp_prev_anniv_init` and
  `free_wd_remain_init` (as named at M10). MYGA's allowance column fits only where the
  allowance is read at the anniversary alone. For each year-keyed state read from the
  frame, put a row valued in a year's last month, `d % 12 == 11`, in the core, with an
  `AT_VALUATION` entry: MYGA's interest-only look-back one month off passed the core until
  point 5 at 11 joined it.
- *Data's checks.* Compare to a cent each rule that ties one amount of money to another
  (D6, precised). Hold each carried value to what makes it where its rule fixes it: FIA's
  F and year-open account value to the anniversary rules, and RILA's
  `av_pp_prev_anniv_init` likewise, at least the account value on an anniversary, the base
  being taken before that month's withdrawal (D6, precised at M10). VA's withdrawals used
  this year are checked as zero or more and no further: VA recomputes its allowance every
  month from the earnings and the remaining premium, so the amount used can exceed the
  allowance at the valuation date. Test a rule on a window of contract months at both
  ends, refused just inside and accepted just outside: MYGA's second-year rule passed
  every test while it was tested at month 12 alone. Run each new check's removal as a
  fault.
- *Join keys.* Check each point's text keys against the tables they key, by point, last in
  `model_point_table`. A scenario must set its levels by the point's first month on the
  books, `t = 0` or its issue month if later, never by `t = 0` for every point, since T3's
  re-based scenarios start at the issue month. A programme, fund, strategy or scenario id
  must be in its table, mortality must rate the point's sex and its attained age in that
  first month, and a schedule name the projection hard-codes must be in its table. Say
  what `Data` cannot check, a bound that needs a `Projection` Reference such as the
  maturity age.
- *A zero account value.* MYGA refuses it in force. FIA's and VA's lifetime withdrawals go
  on after the account value is exhausted, so both accept 0 with a live rider, keep a
  guard on every ratio over the account value, as their S moneyness factors already have,
  and test a row in force at 0 that projects its whole frame (D6, precised). RILA's account
  value, which its interim value can take below 0, is accepted at any sign, and a contract
  holding nothing is refused instead (D6, precised at M10).
- *Tables and text.* Read every assumption table through a checked `Data` cell beside S's
  unchanged reader (§7.10, *E*), with its extents as int `Data` cells, a `TABLE_FAULTS`
  case per table with a key written as text, each refused through a projection too, and a
  test of keys written as floats. Give each table an age- or year-keyed reader. Decode
  each categorical column S branches on, once a point, into bools, one per value S tests,
  read where S asks, and read each join key from `model_point()` in the one cell that
  reads its table: RILA's buffer and cap types and FIA's crediting strategies are the
  obvious cases. Where a model says it compares no text, name what it still compares: S's
  timing and kind strings, and any string-valued join key S branches on, as MYGA's
  `surr_charge_id` is.
- *Tests.* Copy `_month_reads` into the rules test, admitting FIA's `lapse_rate`
  look-ahead by reader, cell and month (R2). Test acquisition per contract at a count
  other than 1, and the scaled roll-forward tolerance at a million contracts. Re-base each
  spliced row's scenario copy, stepped at levels of its own. Evaluate S's unreached cells
  in `_sweep_s`. Guard every per-month charge, ratio and clamp, and probe the future rows
  of every point and variant. Measure the depth at the longest cover, the youngest issue
  age the product allows, on mortality extended below the table, and assert it as a bound.
  Cap `mort_rate` at 1.0 with `min(q, 1.0)` (§5.1, step 6) in FIA and RILA, as `FIA_US_S`
  and `RILA_US_S` do since §8.2 item 4's fix, so the cap is no departure from S; `VA_US_S`,
  like `MYGA_US_S`, reads the table's rate with no factor and needs no cap. At this landing
  `FIA_US_S` capped by `min(1.0, ...)`, and VA and RILA were to check for a factor. Build
  each T5 case so that only the check it names fails, since a move to an anniversary brings
  every anniversary check into play. Route every count of months the runner prints through
  `months()`, on both sides of the valuation date.

**Carried into Phase 2.**
- *Caches and bounds:* `t` from 0 to 1,320, and the month after for the `t + 1` reads:
  1,200 months of cover at the youngest issue age, 0, and the 120-month horizon. Contract
  years 1 to 100 for `free_wd_base` and `free_wd_allow`, attained ages 0 to 99 for
  `surr_charge_age_cap_at`, and whole years remaining 0 to `mva_factor_last_year`, 10 as
  shipped, by column, for `mva_factor_at`. The figures above size `sample_sec.py`,
  `run_sec.py --cython` and the Windows job's stack: 1,214 levels at gcc's 255 bytes a
  level is about 300 KiB, and MSVC's cost waits for the first Windows run. No `Projection`
  Reference bounds the issue age to the product's 0 to 85, and `proj_len()` checks no such
  bound, as in S; of the inputs those sizes rest on, `Data` refuses only a contract issued
  past the horizon, an issue age that is not a whole number of years and an attained age
  the mortality table does not rate, below 40 as shipped. Phase 2 makes each bound a
  Reference that `proj_len()` checks, as M14's item asks.
- *The mortality table's last age* before maturity needs `maturity_age`, so Phase 2 checks
  it in `proj_len()` against an int `Data` cell of the table's last age by sex, as Term's
  `issue_age_min` is checked, with a table-driven refusal.
- *Decodes and joins:* the fourteen decodes move to `Data` vectors (R6).
  `surr_charge_rate`'s test for `"none"` goes with its join into R7's array, and
  `surr_charge_id`, which returns text (R10), leaves with them. `model_point_table` reads
  the scenario, withdrawal and mortality tables, so the model point table is refused with
  an unreadable one of those, compiled or not.
- *Engine functions:* S's float-parameter cells, `mva_pp_on` and `mva_factor_geometric`,
  and `mgsv_rate_statutory`, `mgsv_rate_is_compliant` and `mva_ref_term_years`, which no
  report or check reaches, are inlined or re-keyed (R14). SEC adds none, and no uncached
  cell.
- *T1 and codes:* `_mismatches`, the module's one call of `twin_mismatches`, passes
  `codes=codes(sec_proj)` from the landing on, and S's `claims(t, None)` and
  `claims_over_av(t, None)` keys need a T1 mapping at stage `EC` (R9, R12).
- *The runner:* MYGA's C step copies Term's, with its compensated `add()`; until then the
  rule against summing the block by a plain running sum is checked by review only.
- *`IN_COVER_ONLY`*, 16 cells, has no guard of its own. The guard test holds that no
  formula reaches these cells outside cover, and that the three scenario readers raise
  before issue on T3's re-based copies.

**Carried, outside the SEC models.** Eleven S-side items for §8.2 item 4, found in
`MYGA_US_S`; the first three are fixed in neither model, the rest in `MYGA_US_SEC` only:
- Under `gmir_floor`, `mva_pp_on` returns `max(raw, P_accum - AV)` whatever its base, so
  once a premium load is set a withdrawal of 0 pays: at `load_prem_rate` 1%, point 3 pays
  660.97 at month 0 and 320.63 at month 1. The splice's load shows it, alike in both
  models.
- `wd_pp` takes any scheduled amount, one above the opening account value too: the
  anchor's $4,000 raised to $200,000 leaves an account value of -95,897.30, and a
  withdrawal of exactly the account value makes `lapse_dyn_rate` divide by zero.
- Point 5's `provenance` and two `rate_scenario.csv` `provenance` cells give 1-based
  months, the month-30 surrender and month 6, for events the model has at `t = 29` and
  `t = 5`, and `MYGA_US_SEC`'s twin of point 5 copies the first.
- `age_at_entry` and `guar_period` are read by `int()`, so a fraction truncates silently:
  `guar_period` 5.5 projects as 5. `MYGA_US_SEC`'s `Data` refuses a fraction in either by
  name, since its initial-term check reads `guar_period` as written: 5.5 there counts 66
  months of initial term where the projection counts 60.
- A `guar_period` of 0 or below is accepted: at 0 the guarantee-period index divides by
  zero, a `ZeroDivisionError` that names no point, and below it the projection runs a
  period no contract has. `MYGA_US_SEC`'s `Data` refuses one below 1 year by name.
- Each reader takes its table's keys as pandas reads them. One key written as text
  silently zeroes every surrender charge or every withdrawal, removes the attained-age
  cap, or raises a `KeyError` or `TypeError` that names no file; a blank or fractional key
  drops its row silently, and a blank scenario month is a level that never holds.
- A key its tables lack is met only as S projects, and names no file: a `scenario_id`, a
  sex or an attained age the tables lack raises a `KeyError`, a scenario whose first row
  comes after a point's first month raises `max()`'s `ValueError`, and a `wd_schedule_id`
  the withdrawal table lacks, or a renewal schedule spelt `Renewal`, gives no withdrawal
  or no renewal charge, without a word. `MYGA_US_SEC`'s `Data` refuses each by name,
  except an attained age past the mortality table's last before maturity.
- A mortality or surrender-charge rate outside 0 to 1 is accepted from its table.
- 98 docstring lines exceed 92 characters, 96 in `Projection`, 84 of them in its module
  docstring, and two in `Data`; one line of `expenses`' code does too.
- The symbol map's three rows with a blank first column render as continuation lines, and
  under *pols_maturity and the projection horizon* the roll-forward identity, after a "so
  that" with no `::`, renders as a definition list that loses its `+`.
- `annuitization_pp` says "This cells", and `Data` says "then clear the cache". `Data`'s
  "Three of these carry a compound key" leaves out the mortality table. `wd_pp` says the
  account value runs unbroken on every point but the anchor, though point 5 takes $20,000
  at policy month 29. The within-month order leaves out the annuitization elections, and
  `result_av`'s `free_wd_avail` column holds `free_wd_remain(t)`, which its docstring does
  not say.

**Landing.** Rebased from bbb99a9 (M2) onto 244360e (M11). `sec_support.py` took the two
conflicts, where MYGA's state extractors and its spec sit beside SPIA's, keeping both, and
uslib's `index.md` took MYGA in the sentence that lists the SEC models. `_mismatches` took
`codes=codes(sec_proj)` (*Carried into Phase 2*), and twelve comments and docstrings in
the test module that cited a working note no reader can open now say what they meant
without it. `Data` took the refusal of an `age_at_entry` or a `guar_period` that is not a
whole number of years, and of a `guar_period` below 1 year, with six malformed cases, and
the edges test reads both written as floats (*Data's checks*). Six texts in the tree now
give what this record measures: the sweep's recursion limit, 16, in the `CALL_DEPTH`
comment and in `model-sec.md`; the cold call's depth on a model just read, 496, and its
recursion limit, 495, in `model-sec.md`; the cold chains' overheads in the
`CHAIN_OVERHEAD` comment; and the cent in `model-sec.md` and in `free_wd_allow_init`'s
docstring. `_sweep_s`'s docstring no longer says that §7.10's list of the cells S never
reaches lacks two of them.

**Verified at landing**, on the tree as committed, with three other workflows sharing the
machine. The uslib suite, with modelx-cython installed and so the compile tests included,
gave 1,722 passed and 231 skipped in 1,305.54 s (21 min 45 s), 187 passes and 68 skips
more than M11 landed with: MYGA's module, 154 and 67; its SEC conventions, 32 and 1; and
the one compiled convention that reads every SEC model. Over its full grid, MYGA's module
gave 221 passed in 445.53 s, and the `cython` selection 11 passed and none skipped under
`USLIB_REQUIRE_CYTHON=1`, in 171.87 s. doccheck built 489 pages with 0 warnings.
`gen_sec_points.py --check` found the files of `Term_US_SEC`, `WholeLife_US_SEC`,
`SPIA_US_SEC` and `MYGA_US_SEC` current, and `gen_sec_fingerprint.py Term_US_SEC --check`
reproduced the fingerprint. md_lint reported 0, `gen_scaffolding.py --dry-run` 0 files in
each of the six libraries, and `gen_citation_links.py --dry-run` nothing on its 297 source
tags. A case-insensitive search of `model_point_table_sec.csv` for the 115 names, forms
and hosts that `fixed_deferred_annuity/sources.md` cites found only the design label Camp
B and the product type MYGA, neither a company nor a product. After the text corrections,
MYGA's module and the conventions of `MYGA_US_S` and `MYGA_US_SEC`, the compiled one among
them, gave 211 passed and 69 skipped in 298.22 s, doccheck 489 pages with 0 warnings, and
md_lint 0. The suite and the generator checks ran before the last edit, the guarantee
period's floor and its two malformed cases, which a review of this landing asked for;
after it, the same selection gave 213 passed and 69 skipped in 364.54 s, and the full grid
223 passed in 469.79 s; doccheck again built 489 pages with 0 warnings, md_lint reported
0, `MYGA_US_SEC`'s generated files were current, and `gen_scaffolding.py --dry-run` wrote
0 files.

### 7.11 FIA — `FIA_US_SEC` (E: M, C: L)

*Today:* the policy clock with a late-opening frame. `entry_mth() = 12 * entry_year()`, so
entry falls on anniversaries only. 55 cells guard `t < entry_mth()` and fall back to the
`*_init` cells. Points 1, 3 and 7 enter at `t = 84`; the other six are new business.

**Re-entry already works:** a point re-entered at an anniversary from its own S state
reproduces S to 1e-6 across phases — INCOME, DEPLETED, joint, years 5 to 21 — with one
exception. Point 4, with 20 % in the fixed account, gets `av_fixed_pp_init = alloc_fixed * AV`
(22,700.40 against an actual 16,002.31), and its withdrawals are then off by up to 31.80.

*E (as built, M8):*
- Opening state, under D6's names: `policy_count` and `duration_mth`; entering month 0,
  `av_pp_init`, `av_fixed_pp_init` (the fixed account, which S derived as
  `alloc_fixed × AV`), `benefit_base_pp_init`, `rollup_base_pp_init`, `mgsv_pp_init`,
  `lw_pp_init` and `wd_cum_pp_init` (the withdrawals to date, which this list first
  missed); and at the anniversary on or before the valuation date,
  `av_pp_prev_anniv_init`, `av_fixed_pp_prev_anniv_init`, `phase_prev_anniv_init` (an int
  code, 1 to 3 in force), `payout_rate_locked_prev_anniv_init` and
  `index_level_prev_anniv_init` (the level the year's index segment started at). BB, RB
  and LW are flat between anniversaries, so one column each serves. No rider-status
  column: the rider is in force exactly when elected, because `Data` refuses `TERMINATED`
  in force and a benefit base of 0 under the rider.
- `Data` checks 38 rules over the table, each refusal naming the missing column or every
  point it fails on. In `INCOME` or `DEPLETED` it refuses a lifetime withdrawal of 0 on a
  locked percentage above 0, and one above 0 on a percentage of 0: under a live rider the
  withdrawal is the locked percentage of a benefit base above 0. Both at 0 is read, in
  either phase: a contract that exercises below the first age band, as it can where
  `min_income_age` sits below it, or in a band at 0%, locks 0 in both models and takes a
  lifetime withdrawal of 0 for life, in `DEPLETED` too once its account value is exhausted
  (M8's fix stages: the rule the design's critique proposed, both above 0, refused those
  states, which S reaches). `mort_rates`, `surr_charge_scale` and `payout_rates` name each
  repeated key with its lines, each missing key or span, and each payout band that ends
  below its start. `proj_len()` refuses a point at or past maturity and one whose cover
  from issue is empty, naming it.
- The phase is an int code from stage E (`PRE_ISSUE` 0 … `MATURED` 5); `result_glwb()`
  decodes it, and `sec_support.codes` maps S's strings in T1 and T2.
- Year-open quantities are read three ways: from the frame where the year opened on the
  books; in force, from the `_prev_anniv_init` column, or, for BB, RB and LW, flat between
  anniversaries, from the `_init` column; and by the issue rule on new business. The level
  the year's index segment starts at is the scenario's but for the year under way on a
  contract valued mid-year, which reads `index_level_prev_anniv_init`.
- Rebased onto the policy clock: `mva_term`, the premium cells, `pols_maturity` and the
  guards (R1a). `lapse_rate` and `lapse_moneyness_factor` read the closing anniversary,
  R2's admitted exception, asserted by reader, cell and month with its dependency
  condition walked.
- Clocks: the rate scenario is a generated companion, `rate_scenario_sec.csv`, on the
  valuation clock, read through S's reader, with a copy re-based to each row's month
  (`-M{d}`, `-F{k}`; `SecSpec.future_state` names a future row's). Withdrawals, keyed by
  contract year, stay on the policy clock. Expense inflation runs on the valuation clock
  (D7), so S's in-force points, which S inflates from issue, are splice cases with
  inflation at 0.
- S's goldens sit on in-force point 1 at policy month 95; in SEC they are `t = 11`.
- The committed table: the twins of S's nine points; eight rows restated in force, 4 at
  60, 1 at 95, 5 at 150, 7 at 216, 2 at 240, 8 at 6, 6 at 696 and 4 at 100; and 2 issued
  15 months on.
- The splice (T2) runs on 44 rows: S's in-force twins 1, 3 and 7 at 84; those three points
  restated at 95, 96 and 216; the anchor at 60, 84, 95 (the last month of contract year 8,
  whose closing anniversary is the exercise), 96, 144, 216 and 240; 23 rows over S's other
  new-business points, either side of their events; and 8 over five variants, which add
  the participation, spread and trigger methods, the female table and two withdrawal
  programmes. T3 runs on 15 future rows, and a switched fixture on 9 rows for the
  Reference-level switches and the bounds S ships idle; a core of 12, 5 and 5 of them runs
  by default.

*C:*
- 41 attribute cells, twelve more than S's 29: `policy_count` and `duration_mth_init`,
  seven opening-state accessors (`av_fixed_pp_init`, now a column, among them) and seven
  decodes of `glwb_basis` and `credit_method`, less S's `entry_year`, `payout_rate_init`,
  `phase_init` and `pols_if_init`, which now reads `policy_count`; `pd.isna` ×1
  (`joint_age`).
- Phase codes arrived at stage E (M8). Text a projection cell still compares: S's timing
  and kind strings; each of the thirteen decodes compares its column or Reference once;
  the four joins sit each in its keyed reader.
- To arrays, each from the checked table `Data` already returns (precised at M8):
  `payout_rates` into `[age, basis]`, read through `payout_rate_at`, where S's
  `payout_rate(a, basis)` iterates its rows; `rollup_steps` and `wd_schedules` into
  `[id, year]`; and `surr_charge_scale`, the surrender charge and vesting, into `[year]`.
- String References `step_up_mode`, `rb_wd_convention` and `mva_collar_basis` (a test
  assigns the last of these) become int codes.
- Timing parameters on seven `*_at` cells, `credit_rate_on(r, method)`, and R14 for three
  float-parameter cells, `bonus_clawback_on`, `mva_pp_on` and `wd_reduction_rate_on`, each
  inlined into the cached cell that calls it or keyed by an int code. Two more,
  `mgsv_rate_statutory(cmt5, option_cost)` and `mgsv_rate_is_compliant`, are never
  reached (below): the second is the first's only caller, and no cell calls it. S's
  tests call all five directly, and `credit_rate_on`, so S's cells stay for them,
  admitted by name, or go with a T1 exemption (R14). `math.floor` becomes integer
  arithmetic and `math.isclose` goes (R12).
- Never reached by any report or check on the committed points: `wd_cum_pp`,
  `av_indexed_pp*`, `activation_rate`, `bonus_factor`, `claims_over_av`,
  `mgsv_rate_statutory`, `mgsv_rate_is_compliant`; in `FIA_US_SEC` also `wd_cum_pp_init`,
  which only `wd_cum_pp` reads, S's `payout_rate` and `credit_rate_on`, kept for S's
  tests, the label accessors, which no projection cell calls, and the five decodes of
  values no committed point and no shipped Reference holds, `is_credit_spread`,
  `is_credit_trigger`, `is_step_up_at_exercise`, `is_rb_dollar` and
  `is_collar_surrender_value`, each asked only where the decodes before it in its cell
  answer False. S's `payout_rate_init` is removed (precised at M8).

#### Record — M8, done 2026-11-03

Built in two commits, as D1 requires: `FIA_US_S` copied with only `_name` changed, then
the enhancement, by M1's process: a design prototyped and critiqued before the build,
tests written against the build and checked by injected faults, then a review under the
three lenses. The design departed from §7.11's *E* where reading `FIA_US_S` cell by cell
showed it short: the opening state is twelve columns, `wd_cum_pp_init` among them, which
§7.11 lacked, and no column for the rider's status, which `Data`'s checks make derivable;
the scenario is a generated companion; and the phase is an int code from stage `E`. So
§7.11's *E* is rewritten as built, with four bullets of its *C*. The review made 24
findings, 2 of them blockers and 7 major, two defects each seen under two lenses among
them. A NaN residual passed both roll-forward checks, where `FIA_US_S`'s `math.isclose`
fails it; one symbol-map label a character too wide made the `Projection` docstring's
table malformed, so doccheck failed and the rendered page lost the whole map; `Data`
refused the lifetime withdrawal of 0 that both models reach after an exercise below the
first age band; the count's residual read a month past the frame, past the cache Phase 2
sizes; the thirteen decodes had no `UNDECODABLE` list; three tables' gap and repeat
messages named no key; and two first-year rules and the trigger's boundary at a zero net
return were pinned by no test. The fix stage applied all 24 and rejected two details with
evidence: a rounding figure that did not reproduce, and the income start ages proposed for
the band variants, since the exercise age is the income start age itself. A re-review of
the fixes made two more findings, both minor: the both-0 lifetime withdrawal was held in
`INCOME` alone, though S reaches it in `DEPLETED` too, and the fix stage's texts had three
slips. A second fix applied both, with six docstring corrections the docs stage had listed
and no stage had applied. Fourteen defects found in `FIA_US_S` are carried below: twelve
are fixed in `FIA_US_SEC` only, and two in neither model. M8 was built on M7's tip and
rebased at landing onto M12's, after Term's cap fix, M3 and §8.2 item 4's fix (*Landing*,
below).

**What exists now.**
- `FIA_US_SEC` at stage `E`. Of `FIA_US_S`'s 168 `Projection` cells, 62 are unchanged, 12
  have a new docstring only, 90 are rewritten and 4 are removed: `entry_year` and
  `entry_mth`, S's late frame, which `duration_mth_init` and `t_entry` replace, and
  `payout_rate_init` and `phase_init`, whose year-open values `payout_rate_locked` and
  `phase_year_open` read from their columns. It adds 34 cells, 198 in all: `policy_count`,
  `duration_mth_init`, `maturity_mth`, `t_entry`, `is_active` and `pols_new_biz`; six
  opening-state accessors, `wd_cum_pp_init` and the five that read the `_prev_anniv_init`
  columns; thirteen decodes, two of `glwb_basis`, five of `credit_method` and six of the
  string References `step_up_mode`, `rb_wd_convention` and `mva_collar_basis`; six readers
  keyed by a contract year, an attained age or a count of contract years,
  `surr_charge_rate_py`, `vest_rate_py`, `rollup_rate_py`, `payout_rate_at`,
  `mort_rate_base_at` and `wd_scheduled_at`; and `phase_year_open`,
  `rollup_base_pp_year_open` and `prem_to_mgsv_pp`, which credits the floor's issue value.
  Eight References are new, the phase codes `PRE_ISSUE` 0 to `MATURED` 5 and the checks'
  tolerances, `check_tol_av` and `check_tol_pols`. `Data` keeps S's eight cells: five
  unchanged, `rate_scenario` and `withdrawal_table` with new docstrings, and
  `model_point_table` rewritten to check the table as it reads it, 38 rules in turn. It
  adds nine cells, 17 in all, the six checked tables, `mort_rates`, `surr_charge_scale`,
  `payout_rates`, `rate_scenario_steps`, `rollup_steps` and `wd_schedules`, and three int
  extents, `payout_rate_first_age`, `payout_rate_last_age` and `surr_charge_last_year`;
  and one Reference, `future_horizon_mth = 120`.
- `model_point_table_sec.csv` holds 18 rows generated from FIA's `SecSpec`. Nine are S's
  points as twins: the six new-business points, issued at the valuation date, and points
  1, 3 and 7 in force at 84, as S has them. Eight are derived: the fixed account on an
  anniversary (S point 4 at month 60); the anchor's exercise month read mid-year (1 at
  95); joint income in force mid-year (5 at 150); the overdrawn anchor near exhaustion (7
  at 216); a zero account value with the rider live (2 at 240); the first policy year (8
  at 6); the last policy year, entered at 120 (6 at 696); and income in force mid-year
  with the fixed account accrued since its anniversary (4 at 100). The last row is the
  anchor, S point 2, issued 15 months on. No row sits in the last covered month: at the
  shipped mortality, 1.0 at age 120, S's count after month 696 is exactly 0, so a row at
  707 would project zeros, and the splice reaches that month on mortality cut at 120.
  `rate_scenario_sec.csv` holds 91 rows in 12 scenarios: S's two on the valuation clock,
  anniversary `y` at month `12 * y`, and ten copies re-based to the months the rows are
  valued or issued at. A case-insensitive search of both files for the publishers,
  products, riders, form numbers and hosts that `fixed_indexed_annuity/sources.md` cites,
  each name's words joined by any run of spaces, underscores, dots or hyphens or by
  nothing, finds no name, only digits inside two numbers, row 14's withdrawals to date,
  `wd_cum_pp_init`, and a scenario month.
- `tests/test_fixed_indexed_annuity_us_sec.py` has 46 tests in 280 cases, 231 by default
  and 49 behind `sec_full` (K6). T2 runs on 44 rows: S's in-force twins 1, 3 and 7 at 84
  (`IN_FORCE_TWINS`); those three points restated at 95, 96 and 216; 30 rows restated from
  S's six new-business points; and 8 from five variants. T3 runs on 15: four of S's
  new-business points and the eight variants a month on, three of the variants exercising
  the anchor at 69, 79 and 80, either side of two payout band boundaries, and three S
  points 13 and 15 months on. Both run on 9 rows under the switched References, which put
  the index cost at 0 so that a trigger meets a net return of exactly 0. Each in-force
  mid-year row's companion level at `t = 0` is moved off the opening level the row
  carries. The default core is 12, 5 and 5. Its reach is asserted on 24 valuation-date, 40
  in-frame and 12 switched conditions, and line coverage showed it running all 706
  `Projection` lines the full grid's rows run; removing a set-apart edit moved no row's
  lines. T4 runs at 2.5 contracts. T5 covers 118 model point tables, each refused by its
  one rule or, where a fault breaks two rules by nature, by the earlier, with every entry
  of every column loop pinned and each read through a projection. It also covers 41
  assumption tables, each fault named with its lines or span; 5 undecodable values, each
  raising S's message in both models; and 5 `proj_len()` cases, two of which project. The
  accepted edges hold a lifetime withdrawal and a locked percentage of 0 in `INCOME` and
  in `DEPLETED`, each paying nothing at its next anniversary. A NaN residual fails both
  checks, and a NaN that reaches the mortality cap or the rider charge's cap stays NaN.
  Docstring tables are column-checked, and every docstring parses under docutils where it
  is installed. Each of the fix stages' 25 faults fails a test; the tests stage's 88
  failed 86, the other two equivalent. The SEC conventions, 33 cases, pass but for
  `test_net_cf_is_income_positive`, skipped as on `FIA_US_S`, since neither model has the
  notes-orientation companion cells.
- `run_sec.py`; `model-sec.md`, in MYGA's outline, with *The in-force interface*, *The
  opening state* and *Departures from FIA_US_S*; the registry entry, with no flag of its
  own, since its `pols_if` is `BEF_DECR`, and its `INPUT_FILES`, which name
  `rate_scenario_sec.csv`; and four generated pages. doccheck reported 493 pages and 0
  warnings on M7's tip with FIA added.
- Shared files, added to in place: in `sec_support.py`, `SecSpec.future_state`, appended
  after `twin_arg_map`, which sets a future row's columns from S's point and `k`, with its
  refusal of `policy_count` and the generator's columns (§4, *Record*, precised); FIA's
  state extractors, its companion's builder, `_fia_rebased_scenarios`, and its spec; and
  the `codes()` docstring, which says a product may bring a code forward to stage `E`, as
  FIA does its phases. In `test_sec_support.py`, two refusal cases for `future_state` and
  `test_future_state_sets_a_future_rows_columns_from_s_and_k`. In `us_registry.py`, the
  entry directly after `FIA_US_S`'s, and its `INPUT_FILES`. In
  `test_model_conventions.py`, `EXTRA_POINT_ASSERTIONS["FIA_US_SEC"]`, S's product fact
  that every month in cover sits in one of the four phases, with `PRE_ISSUE` before
  `t_entry()`. And in uslib's `index.md`, the models table's FIA row, the SEC sentence,
  the file table's row on the `*_sec.csv` companions, and the `result_cf_annual()`
  paragraph, which named only `Term_US_S` and `WholeLife_US_S`, though `FIA_US_S`
  publishes it too.

**Departures and precisions.**
- *The opening state* (§7.11, *E*, rewritten as built; D6) is twelve columns beside
  `policy_count` and `duration_mth`, seven entering month 0 and five at the anniversary on
  or before the valuation date. S's five balance columns become the `_init` of the cell
  each opens, `phase_initial`, text in S, becomes the code `phase_prev_anniv_init`, and
  `payout_rate_initial` the locked rate, `payout_rate_locked_prev_anniv_init`.
  `av_fixed_pp_init` is a column where S derives `alloc_fixed × AV`, wrong once the two
  accounts have grown apart (§7.11, point 4), and `wd_cum_pp_init`, the withdrawals to
  date, is one §7.11 lacked, which T2 showed only once `_sweep_s` evaluated S's unreached
  cells. The year-open account value and fixed account, `av_pp_prev_anniv_init` and
  `av_fixed_pp_prev_anniv_init`, are read where the year opened before `t_entry()`; in the
  frame they are read from the month the year opened, and on new business the issue rule
  credits them in the issue month. The level the year's index segment started at,
  `index_level_prev_anniv_init`, is read only for the year under way on a contract valued
  mid-year; every other anniversary's level, an anniversary valuation's included, is the
  scenario's, and on an anniversary valuation `Data` holds the unread column to the
  scenario's level at `t = 0`. No column carries the rider's status: `Data` refuses
  `TERMINATED` in force and a benefit base of 0 under the rider, so the rider is in force
  exactly where it is elected.
- *The twins' state* (§4, *Record*). `twin_state` is `state`, `_FIA_STATE`, where MYGA's
  leaves out the tax basis: on S's in-force points 1, 3 and 7, each column S has none for
  takes what S itself assumes, a fixed account of `alloc_fixed × AV`, the year-open values
  equal to the entering ones, withdrawals to date of 0 and the index level of
  anniversary 7.
- *The phase is an int code from stage `E`* (§7.11, *C*, brought forward): `PRE_ISSUE` 0,
  `ACCUM` 1, `INCOME` 2, `DEPLETED` 3, `TERMINATED` 4 and `MATURED` 5, all-capital int
  References, so `codes()` is not empty at stage `E`, as its docstring now says, and maps
  S's strings in T1 and T2. `result_glwb()` decodes the codes to S's labels.
- *`Data` checks 38 rules in turn* (§7.1's template, item 9), the first that fails raising
  and naming the missing column or every point at fault. Two have no counterpart in
  MYGA's: on an anniversary valuation the index level equals the scenario's at `t = 0`,
  which supplies the level there, so that an unread column cannot carry a wrong value; and
  under the rider in force the benefit base is above 0, which makes the rider's status
  derivable. The lifetime-withdrawal rule is an equivalence: in `INCOME` or `DEPLETED`,
  `lw_pp_init` is 0 exactly where the locked percentage is, and both at 0 is read in
  either phase, the state of a contract that exercised below the first age band or in a
  band at 0% (*Carried, outside the SEC models*). `glwb_elected` is read by value, True
  and False as bools or as text, and comes back as bools, where S's `bool()` reads
  `"False"` as elected; and `age_at_entry`, `income_start_age` and `joint_age` must be
  whole, where S's `int()` truncates.
- *`proj_len()` refuses* a point at or past maturity and, before that, one whose cover
  from issue is empty, `maturity_mth()` 0 or less, each naming the point, so that a future
  row past `maturity_age` no longer projects a frame of zeros.
- *The tables* (R5; §7.1, *Precised at M3*, item 9). FIA took MYGA's form: S's six readers
  unchanged, and beside them six checked tables, `mort_rates`, `surr_charge_scale`,
  `payout_rates`, `rate_scenario_steps`, `rollup_steps` and `wd_schedules`, each indexed
  by its keys read by value, with three int extents. Every projection cell reads the
  tables there, through the keyed readers, but S's `payout_rate`, kept for S's tests and
  called by no projection cell. `mort_rates`, `surr_charge_scale` and `payout_rates` name
  every fault in one message: each repeated key with its lines and each missing key or
  span, and in the payout bands each age span two bands hold, each span none holds and
  each band that ends below its start.
- *The scenario* (D7, D8). The rate scenario is a generated companion on the valuation
  clock, `rate_scenario_sec.csv`, read through S's reader by repointing
  `rate_scenario_file`, so two filename References differ from S's, where MYGA's one does;
  each row reads a copy of S's scenario re-based to its month, `-M{d}` in force and
  `-F{k}` issued later. `scenario_value` reads it by an explicit loop that raises where no
  level is set, where S reads an anniversary before the first row at the first row's
  level, and `Data` refuses a point whose scenario sets no level by its first month on the
  books. Withdrawals, keyed by contract year, stay on the policy clock. Expense inflation
  runs on the valuation clock (D7): S inflates its in-force points from issue, so the
  splice sets inflation to 0, and the committed rows continue S in every cell but those
  inflation moves.
- *R2's admitted read.* `lapse_rate` and `lapse_moneyness_factor` read the state at
  `anniv_mth(t)`, the anniversary closing the contract year, up to 11 months on: the rules
  test admits each read by reader, cell and month (`LOOK_AHEAD`) and walks its dependency
  condition, no count, no rate and no month after the read. Its state chain sets the depth
  of a cold count and of the ascending sweep (D5 and R2, precised; *Measured for K6 and
  F7*, below).
- *Guards* (R1). Twelve cells are guarded where S has none: `index_return`, `credit_rate`,
  `surr_charge_rate`, `vest_rate`, `rollup_rate`, `step_up_applies`, `wd_scheduled_pp`,
  `mva_term`, `mort_rate`, `shock_lapse_rate`, `lapse_rate_base` and
  `lapse_moneyness_factor`, a factor, which is 1.0 outside cover, its neutral value. The
  count's roll-forward residual is 0 outside cover before it reads `t + 1`, as S guards it
  before its frame, so that no cell reads past `proj_len()`, and the guard test fails any
  cell keyed by `t` that holds a key past it after Phase 2's sweep. `is_anniv` is read in
  every month, since `stack_pp` and `rollup_pp` test it first, in S's order, which is
  kept.
- *The checks fail a NaN residual*, as S's `math.isclose` does (§7.1, *Precised at M3*,
  item 11): each stops at `if not abs(r) <= tol: return False`, as UL's do, where the
  build's `abs(r) > tol` passed one, and each scales its tolerance, `check_tol_av` or
  `check_tol_pols`, by the count.
- *The policy clock* (R1a). `mva_term`, the premium cells, `pols_maturity` and the guards
  are rebased onto it, and `av_pp_at` and `av_fixed_pp_at` keep S's one-frame form, each
  timing built from the month's opening in one formula.
- *The cap on mortality* (§5.1, step 6). `mort_rate` caps the annual rate as `FIA_US_S`
  does since §8.2 item 4's fix, `min(mort_ae_factor * base, 1.0)`, the table's rate read
  at `mort_rate_base_at`, so the cap is no departure. At an A/E of 1.25, S's own product
  passes 1 at month 636, attained age 115: the cap test asserts both models' annual and
  monthly rates `(float, 1.0)` in every capped month and floats below 1 before, compares
  every cell of the twin with S, the capped months included, with no absolute floor and no
  `arg_map`, and restates the point the month before the cap and five months into the
  capped year. The NaN test replaces `mort_rate_base_at`'s formula and finds the annual
  and monthly rates and the next month's count NaN; set to NaN, `rider_charge_rate`
  reaches the one other bound written second that a NaN can reach, S's own
  `min(rider_charge_rate, rider_charge_rate_max)`, and the rider charge is NaN.
- *Text* (R6). The thirteen decodes carry every branch on `glwb_basis`, `credit_method`
  and the three string References, each read where S asks its question, so that no
  projection cell compares the model point's text or calls a label accessor, and a value S
  does not know raises S's message in both models. The text a projection cell still
  compares is S's timing and kind strings, and the four joins on text keys, mortality on
  `sex`, the rollup on `rollup_id`, the withdrawals on `wd_schedule_id` and the scenario
  on `scenario_id`, sit each in its keyed reader for R7 (§7.11, *C*).
- *The splice* (§5.2, T2). S's in-force points 1, 3 and 7 are T2 cases at 84, on their
  scenario re-based to 84. A second set of References, read into a pair of models of their
  own, switches what S sets model-wide and the bounds it ships idle: the at-exercise
  step-up, the dollar rollup-base reduction, the surrender-value collar, the lapse and
  rider-charge caps, the fixed rate's floor, `floor_rate` at 0.001, apart from
  `cap_rate_min`, `min_income_age` 71, where the exercise-age floor binds, and the index
  cost at 0, so that a trigger meets a net return of exactly 0; with a variant capped at
  0.1%, below `cap_rate_min`, it runs on 9 rows with a core of 5. T1 also runs under
  `use_guaranteed_scale = True`, a switch S ships False. Each in-force mid-year row's
  companion level at `t = 0` is moved off the opening level its column carries, so that T2
  compares the column and not the scenario's copy of it. The set-apart edits, `mgsv_rate`
  at 3%, the stepped scenarios, mortality cut at 120 and the raised floor, each removed in
  turn, move no row's lines.
- *M11's precisions were taken from the start* (§7.9, *Record — M11*): T4 at 2.5 contracts
  with every assumption that ships at zero switched on and mortality cut at 120, and the
  roll-forward checks at a million contracts; T2 and T3 at no absolute floor, the
  residuals at 1e-9; one rule per malformed case, or the earlier of two where a fault
  breaks both by nature, each read through a projection as well; and the core confirmed by
  line coverage at the fix stage.
- *§7.10's carried items* (*Record — M7*), the deferred chassis, are taken: every chain
  one cell a month; the issue values credited by rule in the issue month, through
  `prem_to_av_pp`, `prem_to_mgsv_pp`, `rollup_base_pp_year_open` and `benefit_base_pp_at`,
  their columns 0 on new business and exempt from T1; the year's opening state under S's
  contract-year keys, `_on_the_books` keyed by anniversary number, with core rows valued
  in a year's last month, points 4 and 5 at 95; the money rules to a cent; each point's
  join keys checked against its tables; a zero account value accepted under a live rider,
  which row 14 projects for its whole frame; and `_month_reads` in the rules test, with
  the look-ahead admitted by reader, cell and month, acquisition per contract at a count
  other than 1, and the depth at the longest cover, issue age 40.
- *The committed rows* (§7.1, *Precised at M3*, item 11). Each derived row and each
  in-force twin continues its S point from its month, cell by cell at the shipped
  assumptions, but for the cells expense inflation moves, and the worked example's
  anniversary 8, S's month 95, is the twin's `t = 11` exactly.
- *The runner* keys each point by its label, or by its position where `Projection` takes
  `idx`, freezes the collector before each pass, releases and collects each point, in
  `--block` asks every point for its frame first, reports month 0's phase by its label,
  says "before the valuation date" of a first lifetime withdrawal or an exhaustion that
  preceded it, and ends with `gc.unfreeze()`.
- *Carried items not yet taken.* Built on M7's tip, FIA's `_mismatches` passes
  `codes=codes(sec_proj)` from the build on, but its runner does not yet carry Term's
  `--cython`, `--build` and `_tool()`, nor its module the `create()`-copy test (§7.1,
  *Record — M14*). §7.12's carried items postdate the build, and three of them it does not
  yet meet. The NaN-residual test replaces `mort_rate_base_at`'s formula, which needs
  modelx (K7), though a Reference, `mort_ae_factor`, feeds the same rate (the cap's NaN
  test replaces it too, which §5.1's step 6 admits), and it asserts the NaN at `t = 0`
  alone: a NaN mortality rate, by either route, makes both residuals NaN in every month of
  the frame, so no month shows the check passing a finite residual. The committed future
  row is compared with S only in the block's sum, beside the anchor's twin and its row at
  240, column by column of `result_cf`, not alone and cell by cell. And the product tests
  read the committed model and `FIA_US_S`, each swept once and held to the module's end,
  about 1.0 GB each at the tests stage, where §7.12's record has those rows built in the
  splice's fixture while S is swept and each S point released after its last T2 case. M13
  takes up the future row's comparison, before FIA's fingerprint is frozen (§5.4), and
  FIA's C step the rest, M14's runner items and `create()`-copy test among them.

**Measured for K6 and F7.** Every time below was taken with other workflows sharing the
machine, the second fix's at load averages of 2.1 to 3.2.
- *Comparisons.* At the fix stage, at the re-review and at landing, over the full grid,
  279 passed, and then 280 with the case the landing added: the 44 T2 rows, the 15 T3 rows
  and the 9 switched rows each continued S in every cell the two share but those a
  restated or future row changes by design, with no mismatch at atol 0 and the
  roll-forward residuals within 1e-9.
- *Time.* By default the module ran 230 passed and 49 skipped in 326.17 s and 330.02 s at
  the second fix, peaking at 3.15 GB in one process both times, and 231 passed and 49
  skipped in 316.52 s with the case the landing added; at the fix stage it ran 308.9 s and
  314.3 s, and at the tests stage, 201 passed and 48 skipped, 282.8 s and 303.2 s. Over
  the full grid it ran 279 passed in 452.34 s at the fix stage, 457.30 s at the re-review
  and 470.90 s at landing, and 280 passed in 455.89 s with the added case, about 1.4 times
  the default run; the second fix touched no case the full grid adds. So the default run
  takes 317 to 330 s, about 135 to 165 s more than WholeLife's module, and the full grid
  about 155 to 175 s more. Most of it is fixed: the switched References' first core case
  with its pair's read (29.2 to 30.7 s), the cold sweep of the committed points (24.9 to
  26.2 s), T4 (23.6 to 26.4 s), the guaranteed scale (20.4 to 23.9 s), the extract (19.1
  to 20.4 s), T2's first core case with its pair's read (17.9 to 19.0 s), `FIA_US_S`'s
  sweep (14.9 to 20.3 s), the runner (15.0 to 15.9 s) and the cap test (11.2 to 12.0 s),
  about three minutes together. The peak is mostly two module fixtures held to the end,
  the committed points swept cold and `FIA_US_S` swept, about 1.0 GB each at the tests
  stage. The SEC conventions, 32 passed and 1 skipped, took 37.05 s at the fix stage and
  34.0 s at the second fix. On M7's tip with FIA added, the uslib suite ran 1,990 passed
  and 281 skipped in 1,317.5 s (21 min 58 s) at the fix stage, 1,361.4 s at the re-review
  and 1,368.0 s (22 min 48 s) at the second fix, peaking at 3.86 GB in one process. On the
  landing's tree, after Term's cap fix, M3, §8.2 item 4's fix and M12, and before its
  review added one case to FIA's module, the suite ran 2,524 passed and 415 skipped in
  31 min 18 s (*Verified at landing*, below).
- *Depth.* A cold `net_cf` runs one cell a month back to `t_entry()` and at most 10 more
  on the committed points: 715 on a 708-month frame, where `FIA_US_S`'s runs 1,420, and
  631 on point 1, where S's runs 1,252. At the longest cover, issue age 40 and 972 months,
  it runs 979 levels, both at the valuation date and issued 120 months on. `mgsv_pp` and
  `wd_cum_pp` run at most 12 over, `av_pp` 9, `av_fixed_pp` 8 and `result_cf` 12. A cold
  `pols_if` alone runs 25 over, 997 levels at the longest cover: its first month reads
  R2's admitted read at the closing anniversary, which opens the account value's chain of
  up to 11 months beneath it. The ascending sweep of the committed points reaches 371 on
  point 9, where the account value runs out at month 359 and the floor's chain is first
  read, against `FIA_US_S`'s 370 on the same point; it passes under a recursion limit of
  400 and fails under 360. `CALL_DEPTH` is 400, `CHAIN_OVERHEAD` 16 and
  `LOOK_AHEAD_MTHS` 11. In the modelx export the sweep needs a recursion limit of 747,
  against Term's 51 and WholeLife's 128 (D5 and R2, precised). Phase 2's `t` cache is
  1,093 values (*Carried into Phase 2*, below).

**Faults.** Each fault went alone into its own copy of the library, and the tests aimed at
it ran through the gate, at most two at a time.
- *Tests stage:* 88 faults, F01 to F88, each caught but two equivalent mutants: F17,
  `pols_maturity` on `t == proj_len() - 1`, the same test on the valuation clock as
  `duration_mth(t) == maturity_mth() - 1`, and F28, the moneyness factor reading the count
  backward, which breaks no rule, since the state its admitted read rests on is unchanged.
  Each of the module's 42 tests of the time failed under some fault.
- *Review (tests lens):* 25 faults, M01 to M25, beside an unchanged copy. 21 were caught,
  M09, the locked rate re-read at the exercise age, and M11, the opening index level read
  from the scenario, only outside T2. Four passed every test: M18 and M19, the first-year
  fixed account and rollup base dropped from the first-year rule; M23, the payout rate
  dropped from the no-rider rule; and M25, the trigger's boundary moved to `net > 0.0`,
  which no row at a zero net return reached.
- *Fix stage:* 24 faults, all caught. M09 fails six tests, T2 point2-d216 and point6-d125
  among them, and M11 fourteen, six T2 rows and four switched rows among them; M18, M19
  and M23 fail their new cases, and M25 the switched point12-d125. N01 and N02, each check
  in its old form, fail the NaN-residual test; N03, the residual unguarded, the guard
  test, past `proj_len()` on every point; N04, the rule that both are above 0, the
  accepted edge; N05, the lifetime-withdrawal rule dropped, its five cases; N06 to N10,
  each decode answering an unknown value as its last known one, their `UNDECODABLE` cases;
  N11, the no-cover refusal dropped, its `NOT_ISSUED` case; N12 and N13, `DEPLETED`'s
  fixed-account entry and the fixed-account rule at the anniversary, their cases; N14 to
  N16, the tables' messages, their `TABLE_FAULTS` cases; N17, the symbol map's wide label
  restored, both docstring tests; and N18, the no-rider shock at the idle rate, T2
  point6-d125. A sweep that recorded each raise of `model_point_table` as its rule and
  column and ran every malformed case through it found four more entries no case pinned,
  `DEPLETED`'s `av_fixed_pp_init`, `av_pp_prev_anniv_init` and
  `av_fixed_pp_prev_anniv_init` and the fixed-account rule at the anniversary, which now
  have cases: of the 118, 89 are refused by one rule alone, and the other 29 are the 14
  missing columns and the documented order pins. Every entry is the first refusal of some
  case, but the horizon's two rules, which the horizon test holds.
- *Re-review:* re-made M25, M11, M09 and N03 on the fixed tree, each caught, and found the
  both-0 lifetime withdrawal pinned in `INCOME` alone.
- *Second fix:* P01, the rule written as the equivalence in `INCOME` and both above 0 in
  `DEPLETED`, had passed the whole default module on the re-review's tree, 230 passed and
  49 skipped; it now fails the edges test, refusing copy 111, and no other of the 174
  cases run with it. N04, made again, fails the edges test, refusing copies 110 and 111.

**Carried into VA (M9).** What FIA adds to what §7.10's *Record — M7* carries into VA with
the deferred chassis. Each item goes to VA's stream from this landing, with the items
*Carried into every product still to come*, below, and VA's record says what it took.
- *Year-open reads and phases.* Copy FIA's three-way year-open read: from the frame where
  the year opened on the books; in force, from a `_prev_anniv_init` column, or an `_init`
  one for a value flat between anniversaries; and by the issue rule on new business.
  `rb_prior_anniv_pp`, which only the `rollup` election reads, and only in a withdrawal
  month, falls back, wherever the year opened before the frame, to its value at `t = 0`
  before the withdrawals, the carried-in base plus the first month's premium: wrong
  wherever a premium after issue was credited in the year under way at or before the
  valuation month, so it takes such a column. No shipped point pays a premium after issue
  in a contract year it withdraws in, so the fallback kept in place of the column passes
  every T2 case restated from them: a `rollup` variant pays one and then withdraws in the
  same contract year, and a core row values it from the premium's month to the
  withdrawal's. Keep VA's phase as S's strings at stage `E`. FIA's became a code there
  because about 25 of its cells compare it and its in-force column must be a number or an
  int code (§7.1, *Record — M14*, *Inputs*), but `VA_US_S`'s `phase(t)` is a leaf that no
  cell, report, check, runner or test reads, and VA's state in force is its depletion
  (*Depletion*, below). It gains `PRE_ISSUE` before issue (§7.1's template, item 8), as
  `DIA_US_SEC`'s does, and `codes()` stays `{}`; R10 codes it at Phase 2 (§6.1, step 4;
  §7.7, *C*), and no report decodes it, since `VA_US_S` shows no phase.
- *Openings and the year to date.* Every opening `VA_US_S` reads as `S_init() if t == 0`
  moves to `t_entry()`. `sum_wd_pp`, `free_wd_used_cum_pp`, `gmdb_dfd_acc_pp` and
  `gmdb_factor_acc` restart at `t == 0` as at a year start, so a contract valued mid-year
  needs each one's value for the year under way as a column. `sa_pp_at` splits
  `av_pp_init` by `alloc(i)`, FIA's `alloc_fixed × AV` error in another form once the
  funds drift apart: the per-fund values are opening state, wide `_init_<i>` columns for
  its two subaccounts, as K5 and §7.7 have them, or a companion keyed by `point_id` for a
  wider fund set (§7.1, *Record — M14*). `phi_glwb_vix(k)` recurses over contract quarters
  from the first, and the highest-quarterly step-up takes the largest account value at
  `t`, `t - 3`, `t - 6` and `t - 9`, leaving out any before `t = 0`. So the rate of the
  last quarter to end before the valuation month, the clip's prior for the first fee on
  the books, is a column, `phi_glwb_init` (§7.7), and the largest account value at the
  year's quarterly anniversaries before the valuation month is one more, as §7.7 and K5
  have it, read at the anniversary closing the year under way alone (§7.10, *Record — M7*,
  *Issue values and past fixings*).
- *Depletion.* `depleted_flag` is absorbing, and from the month after it is set `sa_pp_at`
  holds every fund at 0, so at each month end the flag is set exactly where `av_pp(t)` is
  at or below `av_depletion_threshold`, as in every month of S's nine points, eight of
  which deplete. So §7.7's `depleted_init` is a status the opening account value makes
  exact, and takes no column (*Depth and status*, below): a contract in force at the
  valuation date enters month 0 depleted exactly where `av_pp_init()` is at or below the
  threshold, and new business, whose `av_pp_init()` is 0, never does. A depleted opening
  makes `glwb_payment_pp` read `gawa_pp(t - 1)` and `gwb_pp(t - 1)` at `t = 0`, which S
  never does: read `gawa_pp_init()` and `gwb_pp_init()` there, since, as S's cells stand,
  a depleted point valued at a contract-year start recurses below `t = 0` without end, and
  put such a row in the core.
- *Scenarios.* `inv_return_mth` and `scenario_rate` key VA's scenarios by elapsed policy
  month and read `max(duration_mth(t), 0)` inside a list comprehension. Copy FIA's
  companion: `*_sec.csv` scenarios read through S's readers by repointing their `*_file`
  References, a reader written as an explicit loop that raises where no level is set, and
  `Data`'s join on the point's first month on the books. But re-base each row's copy by
  `shift_months` to its `duration_mth`, the policy months elapsed at the valuation date,
  not to its `source_mth`, on which FIA's builder re-bases and FIA's `-M{d}` ids are
  keyed: the two agree only where S keeps the policy clock or the row comes from S's new
  business. `VA_US_S` projects its in-force point 2 from the valuation date, so that
  twin's `source_mth` is 0 while its scenario moves by 26 (§5.2), and a row restated from
  it at S month `d` moves by `26 + d`. Name each copy by the months it moves, `-M{m}` for
  a `duration_mth` `m` above 0, so that rows moved alike share one: FIA's rule, keyed by
  `source_mth`, would give S's own `base`, unmoved, to the twins of points 1 and 2 alike.
  `SecSpec.future_state` names a future row's `-F{k}`, and the return scenario is re-based
  with `by="sub_id"`, since S's reader steps each subaccount on its own rows. VA needs no
  column holding a level a scenario also sets, so the splice moves no companion value: a
  past VIX reaches the fee only through the clip's prior, the rate of the quarter before,
  which `phi_glwb_init` carries (§7.7) and which, from the contract's second quarter on,
  the first fee a `vix` row charges on the books reads, at `t = 0` on a row valued in a
  quarter's last month.
- *Checks.* `VA_US_S`'s checks are `all(abs(r) < tol ...)` over a generator, which fails a
  NaN: keep that meaning, the strict bound included, in S's generator, which R17 admits,
  or in a loop, never in FIA's first form, `abs(r) > tol`, which passed one.
  `check_pols_roll_fwd_resid` and `av_at`'s `EOM` branch read `pols_if(t + 1)` and are
  guarded only below 0: guard both with `is_active(t)`.
- *The withdrawal year's look-ahead.* VA's lapse reads its moneyness in month `t`, but its
  withdrawal factor reads ahead: `lapse_wd_factor(t)` asks `is_wd_year(t)`, which scans
  `is_wd_taken(u)` over the contract year, up to 11 months on, 421 to 3,300 reads beyond
  `t + 1` on each of `VA_US_S`'s nine points. R2 admits one read, at `anniv_mth(t)`, not a
  scan, so `lapse_wd_factor(t)` reads `is_wd_year(anniv_mth(t))`, the same value, since it
  depends on the contract year alone; `bonus_pp` already reads it at the anniversary, so
  no scan then reads past its own month. Admit that read as FIA's `LOOK_AHEAD` does, by
  reader, cell and month, and walk its dependency condition, `lapse_wd_factor` the reader:
  on S the year's answer at its anniversary rests on no count, decrement or lapse cell and
  on no later month, but on `is_wd_year` at earlier anniversaries, through the bonus, the
  benefit base and the rider fee, which R2 allows and FIA's walk, holding the reader by
  name, does not, so `is_wd_year` is not the reader. Every withdrawal S's points take
  falls in a contract year's first month, where a scan cut at `t + 1` agrees with S's:
  give T2 a row that withdraws mid-year, which moves S's lapse in the months before it.
  Measure a cold count's depth before bounding it (D5, precised at M8): on a copy of S
  that reads so, a cold `pols_if` runs exactly as deep as S's on all nine points.

**Carried into RILA (M10).** RILA, the Payout stream's last, accumulates on the deferred
chassis (§5.3) and may be under way as this lands. Beside what §7.10's *Record — M7*,
§7.9's *Record — M11* and §7.12's *Record — M12* carry into it, and the items *Carried
into every product still to come*, below, these bind it, and RILA's record says what it
took:
- *Checks.* `RILA_US_S`'s three checks are `all(abs(r) <= tol ...)` over a generator,
  which fails a NaN: keep that meaning, in S's generator, which R17 admits, or in a loop
  that stops at `if not abs(r) <= tol: return False`, never in FIA's first form,
  `abs(r) > tol`, which passed one. Its `check_pols_roll_fwd_resid` and `av_at`'s `AFT_WD`
  branch, which `av_change` reads, each read `pols_if(t + 1)` with no guard: guard both
  with `is_active(t)`, as `FIA_US_SEC` guards its residual and `av_at`, so that nothing
  reads the count past `proj_len()`.
- *Term-start state.* `RILA_US_S` locks five market inputs at a term's start: the index
  level, the MVR, and the risk-free rate, dividend yield and volatility that
  `opt_component`'s `"TERM_START"` branch and `opt_budget_at_cap` read. Of a term begun
  before `t = 0` each is an opening-state column (§7.8, *E*; §7.9, *Record — M11*), the
  last three under either amortization rule (§7.8). On every row valued inside a term the
  splice moves the generated companion's value of each at `t = 0` off the term's start, so
  that T2 compares the columns and not the scenario's copy of them: FIA's fault M11, the
  year's opening index level read from the scenario, passed every T2 case until its splice
  did so, and every shipped scenario holds the last three flat, so that a read of them at
  `t = 0` matches its column on every row. RILA reads month `t`'s market at its month end,
  `market_state(t + 1, ...)`, a step function, so the splice first copies the state at
  `t = 0` to `t = 1` where the copy has no row there, as FIA's `_moved_opening_levels`
  first writes the level its next anniversary reads: otherwise month 0, and each later
  month whose month end precedes the copy's next row, reads the moved state, and T2 fails
  a correct model. On a row valued at a term's start the scenario at `t = 0` supplies the
  values and the columns go unread. They are blank there in DIA's form and the expiring
  term's in M7's (§7.10, *Record — M7*; §7.12, *Record — M12*; D6), so `Data` holds them
  to the scenario only in a form that writes the new term's state there, as FIA's
  `index_level_prev_anniv_init` is held on an anniversary valuation.

**Carried into every product still to come.** All but the last two came from the review
and the fixes it led to, the review's and the re-review's faults among them; the last two
came from the design and its critique:
- *Each rule entry by entry.* A rule that reads several columns in turn hides an entry
  dropped from inside it, which a sweep dropping whole rules (§7.9, *Record — M11*) does
  not see. In every reader that refuses an input, `model_point_table`, each companion's,
  as IUL's segment ladder's (§7.4), and the cell that checks each assumption table, record
  each raise as its rule and column, run the reader's malformed cases through the
  rewritten reader, and check that each case's first record is its own and that every
  entry is the first record of some case. In FIA the review's faults found three entries
  no case pinned, and the sweep four more, but it ran on `model_point_table` alone: no
  case wrote an `age_hi` that is not whole, so dropping it from `payout_rates`' loop over
  the two age bounds passed the whole default module until the landing gave it a case.
  Build the table-driven lists, `MALFORMED`, `UNDECODABLE` and `NOT_ISSUED`, from the
  start (§7.1, *Precised at M3*, item 11; §7.1, *Record — M14*): FIA's review found the
  second missing and the third written inline.
- *The core by line coverage* (§7.9, *Record — M11*). Record, with `sys.monitoring`'s
  `LINE` events, the `Projection` formula lines each row of the full grids runs as the
  module sweeps it, returning `DISABLE` from the callback at each location once seen and
  calling `restart_events()` before each row, which costs almost nothing: the core runs
  every line the full grid runs, and each set-apart edit, removed in turn, moves no row's
  lines. A reach predicate requires that its branch ran: FIA's "no-rider shock" held on a
  contract that had terminated, where the lapse rate returns before it reads the shock.
- *Boundaries met exactly.* Put a switched row where a branch's boundary is met exactly,
  as FIA's trigger meets a net return of exactly 0 at an index cost of 0: a cost switched
  on everywhere hides the boundary, and moving it passed every test (M25). In a banded
  table, name each age span two bands hold, each span none holds and each band that ends
  below its start (§7.1, *Precised at M3*, item 9), and put exercise ages on both sides of
  each band boundary the issue age allows, leaving the rest to C4's run of the
  keyed-reader test.
- *`Data`'s state rules against S.* Test each state rule against S's own projections at
  References off their shipped values; where a rule relates two columns in several phases,
  give the accepted edges a copy of each edge state in every phase that reaches it, and
  name every route to it in each text. FIA's first lifetime-withdrawal rule refused the 0
  that S locks below the first age band, and while its accepted edges held that 0 in
  `INCOME` alone, a rule refusing it in `DEPLETED` passed every test (P01).
- *Past the frame, and a NaN.* Guard with `is_active(t)` every residual or cell that reads
  `t + 1`, and have the guard test fail any cell keyed by `t` that holds a key past
  `proj_len()` after Phase 2's sweep: FIA's count residual read
  `pols_if_at(proj_len() + 1, "BEF_NB")`, a month past the cache Phase 2 sizes. Make each
  check fail a NaN at S's own bound: in S's generator, which R17 admits, where it already
  does, or in a loop that stops at `if not abs(r) <= tol: return False`, `<` where S has
  it. FIA's first form, `abs(r) > tol`, passed a NaN, a blocker of its review.
- *Docstring tables.* Check every simple table in a docstring for text in the gap between
  two column spans, as FIA's `_table_overruns` does, and parse every docstring with
  docutils where it is installed: one label a character too wide dropped FIA's whole
  symbol map from its rendered page, and no test that reads the raw text saw it. Neither
  check sees a row that docutils reads into the wrong cells, which the landing found in
  `VA_US_S` and `RILA_US_S`. In a symbol map, check too that each row, with the lines
  under it whose first column is blank, has text in every column: five rows of `VA_US_S`'s
  run the cell into the symbol's column and the meaning into the cell's, leaving the last
  blank. And give each cell with a meaning of its own a row with a symbol, a parenthesis
  where the notes have none, as `FIA_US_SEC` does: a line with a blank symbol continues
  the row above, so that `RILA_US_S`'s `claim_pp`, `claims_from_av` and `claims_over_av`
  run into the row of `claims`, as `FIA_US_S`'s and `MYGA_US_S`'s do.
- *Switches and bounds S ships idle.* Run each Reference-level switch and each bound S
  ships idle that the main splice leaves at S's value in a second splice fixture, a pair
  of models read with References of their own, with its own core and reach assertion, and
  T1 under each switch S ships False, as FIA's switched References and
  `use_guaranteed_scale = True` are. What §5.2's T2 and §7.3's *The splice* switch on in
  the main splice stays there: FIA's `rider_charge_from_mgsv`, a switch S ships False,
  and, where a UL-family product has them, the lapse shock, the cap below 1 it meets,
  IUL's 1.0 lowered first, and charges ceasing in cover. Set a floor raised for the test
  strictly apart from every bound it could be read as: FIA's `floor_rate`, 0.001, sits
  between 0 and `cap_rate_min`, 0.0025, so that a credit floor written as 0.0, or read
  from the cap's floor, fails.
- *Depth and status.* Measure the ascending sweep's depth on SEC and on S before setting
  `CALL_DEPTH`: where the two agree, the depth is S's order of evaluation, not an SEC
  fault. And derive a status that `Data` makes exact rather than carry it as a column, as
  FIA's rider status is.

**Carried into Phase 2.**
- *Caches and bounds:* `t` 0..1,092, 1,093 values, which hold because the count's residual
  is guarded at `t = proj_len()`; contract years 1..81, attained ages 40..120,
  contract-year counts 0..80 and anniversaries 0..81; and `payout_rate_at`'s age from
  `min_income_age`, 50 as shipped, to 121, clamped inside to the bands' last age, 120. The
  deepest cold call at the longest cover is a count's, `pols_if` at 997 levels (`net_cf`
  979), and the export's limits above size `sample_sec.py` and `run_sec.py --cython`. No
  `Projection` Reference bounds the issue age to the product's 40 to 80: the mortality
  join refuses an age below 40, an age above 80 projects, as in S, and `proj_len()`
  refuses one past `maturity_age`. Phase 2 makes each bound a Reference that `proj_len()`
  checks.
- *The mortality table's last age:* a substituted table that stops below `maturity_age`
  raises a bare `KeyError` from `mort_rate_base_at`, naming no file, since `Data`'s join
  checks only the first month on the books; Phase 2 checks it in `proj_len()`, as §7.10's
  *Record — M7* carries for MYGA.
- *T1 and codes:* `scenario_value(y, name)`'s text parameter becomes a code (R9), as
  MYGA's scenario column name does; the six decodes of the three string References become
  int codes; and S's `claims(t, None)` and `claims_over_av(t, None)` keys need a T1
  mapping at stage `EC` (R12).
- *Engine functions* (R14): `bonus_clawback_on`, `mva_pp_on` and `wd_reduction_rate_on`,
  still called at stage `E`, are Phase 2's to inline; `credit_rate_on` and `payout_rate`,
  kept for S's tests, are called by no projection cell; and `mgsv_rate_statutory` and
  `mgsv_rate_is_compliant` are reached by nothing. SEC adds none, and no uncached cell.
- *Tests on the compiled model:* C4 runs `test_each_keyed_reader_is_s_lookup_at_every_key`
  compiled for the 54/55 and 59/60 payout boundaries, which no exercise from the anchor's
  issue age, 62, reaches. `test_the_docstrings_parse_as_rst` needs docutils, which no CI
  test leg installs. The NaN-residual test and the cap's NaN test replace
  `mort_rate_base_at`'s formula, which needs modelx (K7); the rider charge's NaN case sets
  a Reference, but on a second model read inside the cap's NaN test, so it runs compiled
  only once it is a test of its own. FIA's C step sends the residual test's NaN through a
  Reference instead, set before the model computes anything, as §7.12's *Record — M12*
  carries, and the cap's either so, through `mort_ae_factor`, or kept in C1 (§5.1,
  step 6).

**Carried, outside the SEC models.**
- Fourteen S-side items for §8.2 item 4, found in `FIA_US_S`; the first two are fixed in
  neither model, the rest in `FIA_US_SEC` only, refused there, replaced by a column or
  corrected in its docstrings:
  - `is_exercise` allows exercise at `max(min_income_age, income_start_age)`, below the
    payout bands' first age, where the percentage is 0, and `payout_rate_table.csv` may
    hold a band at 0%: either way the contract locks 0 and pays a lifetime withdrawal of 0
    for life, in `INCOME` and, once the rider charge has spent its account value, in
    `DEPLETED`. Under `min_income_age` 45 the anchor issued at 40 with income from 45
    exercises at 45; at the shipped minimum, 50, it exercises at 50 issued at 45 with
    income from 50 under bands that start at 55, and issued at 40 with income from 50
    under a first band at 0%; at a rider charge raised to its cap, 1.5%, the first and the
    third reach `DEPLETED`, at months 731 and 599. SEC reads each such state and continues
    S from it with no mismatch at atol 0. Whether S should refuse such an exercise, start
    the income at the first band above 0, or refuse a band at 0%, is S's question;
  - the index credit's base is `AV - F`, so on a contract wholly in the fixed account it
    is rounding of 0: in S from 0 to 7.3e-12, with a credit from 0 to 1.0e-12, and on a
    row restated at month 6, whose opening columns come back from the CSV an ulp off, as
    low as -1.1e-11 for the account and -1.4e-12 for the credit, since the 0% floor
    applies to the rate, not to the base;
  - 150 lines over 92 characters: 145 in the `Projection` symbol map, 4 cell summaries,
    `anniv_mth`, `scenario_value`, `wd_scheduled_pp` and `wd_free_pp`, and 1 in the model
    docstring;
  - "cells" slips in `duration_mth`, `year_open_mth`, `av_pp_year_open`, `mort_rate`,
    `activation_rate` and `rider_in_force_open`;
  - `Data`'s "then clear the cache";
  - the symbol map's three rows with a blank symbol, `claim_pp`, `claims_from_av` and
    `claims_over_av`, which render as continuation lines;
  - the scenario's first-row fallback, which reads an anniversary before the scenario at
    the first row's level;
  - `int()` of raw table keys, so that a text key raises Python's own message and a gap
    between payout bands reads 0;
  - `alloc_fixed × AV` for the fixed account in force;
  - the `Projection` docstring's rubric "The three phases, and why the cause of depletion
    matters" introduces four, as `FIA_US_S`'s `model.md` heading has them;
  - `wd_charge_base_pp` nests an inline literal in strong emphasis, which renders with its
    backticks;
  - the model docstring has no blank line before its bold disclaimer, so the disclaimer
    renders inside the paragraph above, and its first sentence nests one pair of dashes
    inside another;
  - `mva_term`'s docstring says a transaction in contract year 10 carries no MVA; it
    carries the months left, and only the anniversary month, 119, carries none;
  - `rider_in_force_open`'s docstring counts four formulas; five call it.

**Landing.** Rebased from a17b822 (M7) onto e011a0c, after Term's cap fix, M3, §8.2
item 4's fix and M12. `FIA_US_S` there caps its annual mortality with the bound second,
`min(mort_ae_factor * base, 1.0)`, as `FIA_US_SEC`'s `mort_rate` already did through its
keyed reader, `min(mort_ae_factor * mort_rate_base_at(age(t)), 1.0)`, so that fix changed
no formula of `FIA_US_SEC`. uslib's `index.md` took two conflicts, the sentence that lists
the SEC models, which now names all seven, and the row on input files, which now names
DIA's companion beside FIA's; `sec_support.py` took two, where FIA's state extractors and
spec follow UL's and DIA's, all kept; and `FIA_US_SEC`'s `Projection` one, `mort_rate`,
where the enhancement's, which reads `mort_rate_base_at`, replaces the copy's.
`INPUT_FILES`, regenerated with `gen_input_files.py --write` on the merged tree, came out
unchanged. `index.md`'s sentence on worked examples already in force now names the FIA's
beside whole life's, since FIA's twins 1, 3 and 7 continue S from month 84. After its
review the landing gave `TABLE_FAULTS` a case that writes a fractional `age_hi`, an entry
of `payout_rates`' check that no case had pinned (*Each rule entry by entry*, above), so
that the module has 280 cases, 231 by default, and `model-sec.md` counts 41 assumption
tables; and `SecSpec`'s docstring now names FIA's companion beside DIA's and VA's.

**Verified at landing**, with two other workflows, VUL's and RILA's builds, sharing the
machine. The uslib suite, with modelx-cython installed and so the compile tests included,
gave 2,524 passed and 415 skipped in 1,878.46 s (31 min 18 s), its two warnings modelx's
renames of `Term_US_S` and `VUL_US_S` in the round-trip tests. FIA brings 230 passes and
49 skips in its module, 32 passes and 1 skip in its SEC conventions, the notes-orientation
check, which twelve other models skip, 3 passes in `test_sec_support.py`'s cases of
`future_state`, and one pass in the compiled convention that reads every SEC model. Over
its full grid, FIA's module gave 279 passed in 470.90 s, and the `cython` selection 11
passed and none skipped under `USLIB_REQUIRE_CYTHON=1`, in 124.57 s. doccheck built 501
pages with 0 warnings. `gen_sec_points.py --check` found the files of the seven SEC models
current, and `gen_sec_fingerprint.py Term_US_SEC --check` reproduced the fingerprint.
md_lint reported 0, `gen_scaffolding.py --dry-run` 0 files in each of the six libraries,
and `gen_citation_links.py --dry-run` nothing on its 306 source tags. A case-insensitive
search of `model_point_table_sec.csv` and `rate_scenario_sec.csv` for every publisher,
product, rider, form number and host that `fixed_indexed_annuity/sources.md` cites, each
name's words matched also when joined by underscores, dots or hyphens or run together,
found no name, only digits inside two numbers, a withdrawals-to-date value and a scenario
month. These runs came before the landing's review, and before the landing wrote this
plan's M8 text, which no test, generator or doccheck reads. With the case and the two text
edits the review led to (*Landing*, above), FIA's module gave 231 passed and 49 skipped in
316.52 s by default and 280 passed in 455.89 s over its full grid, and
`test_sec_support.py` 53 passed; doccheck, the two generators' checks,
`gen_scaffolding.py --dry-run`, `gen_citation_links.py --dry-run` and md_lint, run again
on the tree as committed, reported as above, md_lint 0 on uslib and on this plan.

### 7.12 DIA — `DIA_US_SEC` (E: L, C: L)

*Today:* the policy clock, new business only. The payout date `T`, the premium months and
the option months (adjust, accelerate, commute) are policy-month indices compared with `t`
directly — R1a throughout. `pols_if = pols_if_init * l_last` is a start-of-month count
weighted by survival, on a constant `pols_if_init` (D5, precised at M11).

*E — the one structural change in Phase 1.* S uses one survival curve, `lives_if`, for two
jobs: **pricing** each premium's paid-up slice at its own date, and **projecting**. On the
valuation clock these part.
- Pricing stays anchored at issue and premium dates. It is deterministic from the
  contract's terms and the model's mortality basis, and takes a non-recursive form (R2):
  survival from issue by one explicit loop, `lives_if_pm(k, life)`, which is S's recursion
  bit for bit; the annual rate in one policy-year cell, `mort_rate_py(y, life)`, which the
  projection's `mort_rate` reads too; and the pricing cells keyed by policy month `k`.
  That removes F7's 517-deep recursion. Pricing shares the valuation's mortality basis,
  its A/E and its improvement, as S's one curve does. A mortality sensitivity therefore
  moves the purchase rate of every premium still due and every twin's and future row's
  `n_g` and income, while a contract in force keeps the `n_g` it was priced with (precised
  at M12).
- Projection opens at valuation from per-life probabilities.
- So the opening state is eight columns (precised at M12):
  - per-life survival probabilities, `lives_if_init_1` and `lives_if_init_2` (0 on a
    single life);
  - the cumulative premium CP (the ROP base, the refund base and QLAC room) and the
    purchased income B entering month 0, `cum_premium_pp_init` and `annual_income_init`,
    S's values of month `d - 1`;
  - `guarantee_mths_pricing_init`, the `n_g` with which S prices every slice of a cash or
    installment refund. It is a fixed point over the whole schedule, which the premiums
    still due cannot recover; required on every refund form in force and blank otherwise;
  - the frozen weights `surv_to_payout_init` (`l_last(T)`) and `commute_weight_init`
    (`l_last(t_c)`), each given exactly where its month precedes the valuation month and
    derived bit for bit otherwise. `Data` checks presence both ways, the second at most
    the first, each at least the probability that a covered life is alive, and each above
    0: a contract past `T` reached it and a commutation needs an owner alive to exercise
    it, and at 0 a contract whose lives have all died would owe its guarantee and pay
    nothing;
  - `ref_rate_shift_init` (§7.9, *Record — M11*).
- The payments-as-if-alive G need no column. B is level from `T`, because `Data` refuses a
  premium at or after `T`, an adjustment not followed by its new start month, and an
  adjustment at or after `T`. G is therefore a static schedule, summed by policy month and
  based at `max(duration_mth_init(), 0) - 1`, a key the model point fixes and no clock
  read gives (R2). Nor does the acceleration factor need one: S reads it only in the
  exercise month.
- **"Contract open" is not "life alive"** in a certain period. S's certain-floor weight
  `l_last(T)` (0.715 on point 7 at `t = 300`) exceeds survivors (0.5577), because the open
  cohort includes beneficiary continuations. The in-force interface carries the
  continuation explicitly.
- Option months stay on the policy clock, compared with `duration_mth(t)`. Converted to `t`
  they would collide with the `-1` "never" sentinel.
- **Premium schedule.** S reads a point's premiums from the shared `premium_schedule.csv`,
  matching rows by `point_id`, and a point with no rows projects **silently**, with no
  premium and no income. A copy of point 1 under a new id, verified, totals −1,985 in
  `net_cf`, which is its expenses, against point 1's −277,364.
  - The SEC model therefore reads its own `premium_schedule_sec.csv`, generated from S's
    schedule and read through S's `premium_schedule_file` Reference. It opens with S's
    file as it stands, in its order, so each twin keeps S's rows and row labels and T1
    compares the reader's frame exactly; then, in the table's order, a derived row's
    source premiums due at or after `d`, because those paid earlier are already in the
    opening state as CP and B, and a future row's whole schedule. Its reader checks it
    against the checked table, naming the point: each `point_id` whole and in the table,
    each month whole and not negative, each amount a finite number not negative, no
    premium before `duration_mth` on a point in force or at or after the income start
    month in force, and no point with neither a positive premium due nor income bought,
    S's silent case (precised at M12).
  - Premium months stay policy months.
- Splice months are chosen on the splice's edited inputs:
  - 59, 60 and 61 around point 14's second slice;
  - `T - 1`, `T` and `T + 1`;
  - each option month of points 13 to 15, and either side;
  - an acceleration inside a guarantee, valued at its income start month and issued 13
    months on, where `l_last(T)` is derived rather than read;
  - a half commutation with an acceleration in its guarantee's last month, valued at the
    commutation;
  - the last month of each refund period, derived period and guarantee, and the first
    after;
  - the month before mortality's cap binds, and the month after a life dies with
    certainty;
  - the frame's last month.

  Eighteen variants of S's points reach every category of every text column S branches or
  joins on. `SPLICE_MTHS` records 112 cases with a core of 36, and `FUTURES` 21 rows with
  a core of 8. At M12's fix, line coverage showed the core executing 660 of the 660
  `Projection` lines the full grid executes (precised at M12).

*C:*
- To arrays: the premium schedule — filtered and sorted per call, then an `iterrows`-built
  dict and `dict.get` — becomes a dense `[idx, month]` array; the ROP factor a 3-D
  `[age, sex, years]` array; the payout factor, keyed by a string tuple, a per-point value
  from `Data`.
- Ten strings, plus `qlac_flags()`, which returns a list of strings.
- `annuity_factor` mixes int and float parameters, so it is R14: inlined into the cached
  cells that call it, or its rate replaced by a code for the basis the rate comes from, so
  that it is int-keyed.
- S's tests assert the dict and DataFrame returns of `premium_by_mth()` and
  `premium_schedule()`, so those readers stay in `Data` beside the arrays.
- Never reached by any report or check: `guarantee_yrs`, `qlac_room`, `qlac_flags`,
  `accel_cost`, `payout_factor_calc`, `phase`, `market_type`, `is_qlac`,
  `other_qlac_premium`; in `DIA_US_SEC` also `accel_payment_factor`, whose exercise-month
  block reads the schedule by policy month, each life's `lives_death`, `cola_factor`, now
  read through `cola_factor_pm(k)`, `calendar_year` and `age`, the per-`t`
  `mort_rate_base` and `improvement_rate`, now that the rate is built once per policy year
  (`mort_rate_py`), and the label accessors (`sex`, `reduction_trigger`, `market_type`,
  `income_form`, `payout_form`, `db_form`, `payment_timing`, `mort_basis`,
  `factor_basis`). The module's sweep calls each (precised at M12).

#### Record — M12, done 2026-11-03

Built in two commits, as D1 requires: `DIA_US_S` copied with only `_name` changed, then
the enhancement, by M1's process: a design prototyped and critiqued before the build,
tests written against the build and checked by injected faults, then a review under the
three lenses. The design departed from §7.12's *E* where reading `DIA_US_S` cell by cell
showed it short: the opening state is eight columns, one of them
`guarantee_mths_pricing_init`, which §7.12 lacked, and G and the acceleration factor need
none, so §7.12's *E* and *C* are rewritten to match. The review made 24 findings, 5 of
them major, one defect seen under two lenses among them. An acceleration inside a commuted
guarantee paid the commuted cohort its pulled-forward instalments again; a frozen weight
of 0 let a contract whose lives had all died inside its guarantee pay nothing; the four
assumption tables' keys were never checked, so a key written as text ended in a bare
`KeyError` that named no file; and no row reached an acceleration on guaranteed
instalments where `l_last(T)` is derived, so a fault that turned it NaN passed every test.
A re-review of the fixes made three more, all minor: §7.1's *Precised at M3*, item 11, was
half met, three lines of `model-sec.md` ran past 92 characters, and the proposed K6 text
misstated the default run's cost and where the uslib suite's peak memory is reached. All
are fixed, in `DIA_US_SEC`, its tests and its notes, or recorded here where they asked for
a record, and neither fix stage rejected a finding. Fifteen defects found in `DIA_US_S`
are carried below: fourteen are fixed in `DIA_US_SEC` only, and one in neither model. M12
was built on M11's tip and rebased at landing onto §8.2 item 4's fix, after M3 (*Landing*,
below).

**What exists now.**
- `DIA_US_SEC` at stage `E`. Of `DIA_US_S`'s 113 `Projection` cells, 26 are unchanged, 24
  have a new docstring only and 63 are rewritten; none is removed or renamed. It adds 36
  cells, 149 in all: `policy_count`, `duration_mth_init`, `t_entry`, `stop_mth`,
  `is_active`, `pols_if_at` and `pols_new_biz`; seven opening-state accessors,
  `lives_if_init(life)`, `cum_premium_pp_init`, `annual_income_init`,
  `guarantee_mths_pricing_init`, `surv_to_payout_init`, `commute_weight_init` and
  `ref_rate_shift_init`; the pricing curve, `lives_if_pm(k, life)` and
  `lives_if_last_pm(k)`, and the one rate cell, `mort_rate_py(y, life)`, with its monthly
  rate `mort_rate_mth_py(y, life)`; one reader per table keyed by attained age,
  `mort_rate_base_at(x, life)` and `improvement_rate_at(x, life)`; the premium of a policy
  month, `premium_pm(k)`; the payout schedule fixed at the income start month,
  `annual_income_payout` and `cum_premium_payout`, with `is_payment_pm(k)`,
  `cola_factor_pm(k)`, `annuity_pp_sched_pm(k)` and `certain_floor_pm(k)`; and nine
  decodes. `Data` keeps five of S's seven cells, `input_dir` and the four assumption
  readers, rewrites the readers of this model's two files, `model_point_table` and
  `premium_schedule_table`, which now check them as they read them, and adds four count
  cells, `mort_table_count`, `improvement_scale_count`, `payout_factor_count` and
  `rop_factor_count`, and the Reference `future_horizon_mth = 120`.
- `model_point_table_sec.csv` holds 26 rows generated from DIA's `SecSpec`. Seventeen are
  S's points as twins, issued at the valuation date. Eight are derived: the
  payment-acceleration point (S point 14) at month 59, in its deferral the month before
  its second premium; the anchor (1) at 241, a month into its income phase, its cash
  refund running; the 10-year period certain (7) at 300, inside its guarantee, where the
  contract open exceeds the life alive; the commuting point (15) at 253, the month after
  its full commutation; the start-date adjustment (13) at 121, the month after it; the
  joint point (8) at 672, its joint annuitant dead with certainty; the installment refund
  (5) at 270, inside its derived period; and the anchor at 719, its last month, a one-row
  frame. The last row is S point 8 issued 13 months on. `premium_schedule_sec.csv` holds
  34 rows: S's 31 as they stand, then the premium the payment-acceleration row still owes
  and the future row's two. A case-insensitive search for the publishers, products, form
  numbers and hosts that `deferred_income_annuity/sources.md` cites finds none of them in
  either file.
- `tests/test_deferred_income_annuity_us_sec.py` has 46 tests and 341 cases: T2 on 112
  splices; T3 on 21 future rows; T4; T5 on 96 malformed rows, 17 malformed premium
  schedules, 38 malformed assumption tables, 9 points `proj_len()` refuses and 8
  undecodable values; T6, and the committed rows against S; the rules test, core and full,
  and the clock, depth and guard tests; and the product's own facts. By default a core of
  36 splices and 8 future rows runs, 251 cases in all. A test asserts that the core
  reaches each listed branch, and line coverage at the fix stage showed it executing all
  660 `Projection` lines the full grid executes. The other 90 cases carry `sec_full` (K6).
  S has no in-force point, so `IN_FORCE_TWINS` is empty. The SEC conventions, 33 cases,
  pass but for two skipped by design: the lapse-rate convention, since DIA has no lapse,
  and `pols_if == BEF_DECR`, which `survival_pols_if` skips.
- `run_sec.py`; `model-sec.md`, with *The opening state*, *The premium schedule* and
  *Pricing on the policy clock*; the registry entry, with `survival_pols_if` among its
  flags, and its `INPUT_FILES`, which name `premium_schedule_sec.csv`; and four generated
  pages. doccheck reported 489 pages and 0 warnings on M11's tip with DIA added.
- Shared files, added to in place: DIA's spec, its state extractors and its companion's
  builder, `_dia_premium_schedule`, in `sec_support.py`; the entry in `us_registry.py`,
  with a sentence on `survival_pols_if` in its docstring; in `test_model_conventions.py`,
  `EXTRA_POINT_ASSERTIONS["DIA_US_SEC"]`, S's product fact that the income starts, read on
  the valuation clock, and `SURVIVAL_POLS_IF`, the skip the flag keys and the confinement
  of the flag to `DIA_US_SEC`; and the models table, the SEC sentence and the file table's
  row on the `*_sec.csv` companions in uslib's `index.md`.

**Departures and precisions.**
- *The count is not decremented* (D5, settled at M12). `DIA_US_SEC` copies SPIA's count
  chassis: `policy_count` on the books from issue to the stop rule, never decremented,
  with `BEF_NB` a closed form and mortality per life in `lives_if`. `pols_if` keeps S's
  definition on that count, `pols_if_at(t, "BEF_DECR") * lives_if_last(t)`, S's
  `pols_if_init * l_last` bit for bit on every twin, which is neither `BEF_DECR` nor
  SPIA's closing measure. The registry marks it `survival_pols_if`, a key the registry
  test confines to `DIA_US_SEC` (`SURVIVAL_POLS_IF`), the `pols_if == BEF_DECR` convention
  skips it, and the module asserts the definition; `closing_pols_if` is not widened.
- *The opening state* (§7.12, *E*, precised) is eight columns: each life's survival,
  `lives_if_init_1` and `_2`; CP and B entering month 0, `cum_premium_pp_init` and
  `annual_income_init`, S's values of month `d - 1`; `guarantee_mths_pricing_init`, the
  `n_g` with which S prices each slice of a refund form, a fixed point over the whole
  premium schedule that the premiums still due cannot recover; the frozen weights
  `surv_to_payout_init` and `commute_weight_init`, each given exactly where its month
  precedes the valuation month and derived bit for bit otherwise; and
  `ref_rate_shift_init`. `Data` holds the weights to presence both ways, the second at
  most the first, each at least the survivors and each above 0. G and the acceleration
  factor take no column.
- *Pricing on a curve of its own* (§7.12, *E*; R2; F7). `lives_if_pm(k, life)` is one
  explicit loop from issue, S's recursion bit for bit at every key of all seventeen twins;
  `mort_rate_py(y, life)` is the one place the annual rate is built, which the
  projection's `mort_rate` reads too; and the pricing cells, `income_start_mth_at`,
  `deferral_yrs`, `surv_to_income_start`, `rop_factor_calc`, `rop_factor`,
  `annuity_factor_def` and `purchase_rate`, are keyed by policy month `k`, S's `t`
  renamed, so T1 and the splice compare them unshifted. Pricing shares the valuation's
  mortality basis, its A/E and its improvement, as S's one curve does: at an A/E of 0.9
  the slice point 18 still owes buys 0.229129 a year per dollar rather than 0.241650,
  while its column keeps the 40.810288 months priced at the shipped 1.0.
- *The payout schedule is fixed at the income start month* (R2, precised).
  `annual_income_payout()`, `B(T)`, and `cum_premium_payout()`, `CP(T)`, are one loop each
  from the valuation date's policy month, bit for bit S's. `is_payment_pm(k)`,
  `cola_factor_pm(k)`, the one COLA formula, `annuity_pp_sched_pm(k)` and
  `certain_floor_pm(k)` take a policy month and form `k - T` inside, so S's keys compare
  unshifted, and `cum_annuity_pp(k)`, S's `G`, is based at
  `max(duration_mth_init(), 0) - 1`, a key the model point fixes and no clock read gives.
  The schedule rests on `B` level from `T`, which `Data` enforces (below). An installment
  refund's derived period `n_R` is a fixed point of the whole payout schedule, so
  `certain_mths_refund()` searches `G` upward from `T`, a cell deep each: point 24 reads
  `G` at keys 240 to 280 and no other, which the test asserts. A cash refund asks for no
  key before the valuation date's: point 19 reads `G` at 240 to 718 alone.
- *Two residuals restated.* `check_lives_roll_fwd_resid` restates the recursion month by
  month from the opening state, so that a misindexed or mis-based recursion fails it,
  where S's is the telescoping identity, zero whatever `lives_if` returns, and SPIA's
  rebuild as a running product would hold 70 to 116 MB on each of DIA's 720-month points
  (§7.9, precised). `check_commutation_value_resid` is measured at the guarantee's last
  month, reading back to the exercise, where S's reads the guaranteed months ahead of it:
  on every row valued at or before the exercise it is S's residual at the exercise, bit
  for bit, which the module asserts, since a residual moved to the wrong month is 0 there
  and passes every comparison at the floor (R2, precised).
- *§7.9's carried items* (*Record — M11*) are taken, with the precisions recorded there:
  the payout schedule's cells and the commuted value's loop keyed by policy month from
  issue; the survival check restated rather than rebuilt, which at a cell a month stays in
  the swept splice copies; and an installment refund's search reading `G` from `T`.
- *Guards* (R1). Outside cover every count and flow is zero, as is every rate read at a
  policy year or an age, every flag is false, and no cell reads a rate, a policy year or
  an age the contract does not have. `cola_factor`, a factor, is 1.0 there, its neutral
  value and S's before `T`, and `commute_disc_rate`, which reads neither clock, keeps its
  value. The guard does not leave the tables unread: on an installment refund
  `is_active(t)` reads `stop_mth()`, whose search for `n_R` reads the payout schedule and
  so prices the premiums, so the age readers and `mort_rate_py` are read in cover or not,
  at keys the guard test bounds to the contract, and `IN_COVER_ONLY` holds `age` and
  `calendar_year` alone.
- *The acceleration.* `accel_payment_factor(t)` is 0.0 outside its blackout and where the
  lump sum was paid before the valuation date. The exercise month's lump sum reads the
  schedule and the certain floor by policy month inline, so no projection cell calls the
  factor, and T2 exempts it on a row valued after the exercise, where nothing reads it.
- *The reference rate on one path* (D7, as §7.9 carried it). A contract on the books at
  the valuation date discounts a commutation at
  `i_p + max(0, ref_rate_shift_init() + ref_rate_shift) + m_c`, the floor on the whole
  change since issue, and one issued later at `i_p + m_c`. A test reads one table holding
  point 15 in force at 240, its twin and the point issued 13 months on, at the Reference 0
  and 0.005, and with the column and the Reference of opposite signs: a column of -0.01 at
  0.005 discounts at 5.25%, and one of 0.01 at -0.005 at 5.75%, where a floor on each part
  would give 5.75% and 6.25%.
- *`Data` refuses, naming the point,* what S projects inconsistently or silently, each a
  recorded departure: a premium at or after the income start month in force; a broken
  adjustment pair, a new start month not after the exercise, or an exercise at or after
  `income_start_mth`; an acceleration or a commutation before `T`, or the two less than
  six months apart, the product's interlock [S4]; a point with no income bought and no
  positive premium due; a joint contract on the table basis; a `joint` flag other than
  True or False, or 1 or 0; a sex, or on a joint contract a `joint_sex`, other than M or
  F; a `survivor_pct`, `cola_rate`, `commute_frac` or `other_qlac_premium` that is not a
  number or is out of range; an `issue_age`, `joint_age`, `certain_period`, `frequency`,
  `issue_year` or `purchase_rate_dp` that is not whole or is below its least sensible
  value, each read by value; and in the companion, a premium before the valuation date and
  a row naming no point. The income start month and the option months are checked before
  every rule that reads them, and the checked columns are returned as the numbers checked.
- *`proj_len()` refuses* a point at or past the stop rule; a contract in force owing
  nothing, with one message for each of its three ways; and an acceleration on the books
  whose lump sum pulls forward instalments of a guarantee that a commutation before it
  reduced, which both models would pay unreduced. An acceleration that pulls forward only
  the life tail after the guarantee projects, and so does one paid before the valuation
  date.
- *The tables* (R5; §7.1, *Precised at M3*, item 9). DIA followed UL's form for its four
  tables: S's readers unchanged, an int count cell beside each, which each join asks
  first. Each count cell reads its table's keys by value and refuses, naming the file, the
  column and the lines, a key blank, text or not whole, a sex or payout form no join
  reads, a key on two rows and a gap in a sex's ages, then a value blank, text, infinite
  or outside its table's range. A negative improvement rate, a deterioration, projects as
  S projects it. The build had checked the values in place in S's readers; the fix stage
  moved the checks out, so that none of the four readers is rewritten, as R5 has it.
- *Text.* Ten bool decodes, the nine new cells and S's `is_qlac` rewritten as one, and the
  `joint` flag as `Data` checked it, carry every branch, so no projection cell compares
  the model point's text or calls a label accessor. The pricing and QLAC cells that passed
  policy months as `t` read the age at `T` as `age_at_entry(1) + T // 12`, and at `k` as
  `age_at_entry(1) + k // 12`, their sex from the model point's column and their form from
  the decodes (R1a).
- *The cap on mortality* (§5.1, step 6). `mort_rate_py` caps the annual rate as `DIA_US_S`
  does since §8.2 item 4's fix, `min(mort_ae_factor * q, 1.0)`, so the cap is no
  departure, and the build's "cap written rate first" is withdrawn. A test finds S's own
  product past 1 on S point 8 and variants 18 and 30 on the splice's inputs, asserts both
  models' annual and monthly rates `(float, 1.0)` there and the life's survival 0.0 after,
  compares every cell with S on the twin and on the row in force the month before, the
  capped months included, and reads a model with `mort_ae_factor` NaN, set before it
  computes anything, whose `mort_rate(0, 1)` is NaN.
- *Inputs on their clocks.* Expense inflation keeps S's annual steps, on `t`,
  `(1 + g)^(t // 12)`. Improvement is dated by the calendar on the policy clock (D7), so
  the splice does not neutralize it: point 16 restated at 240 reads S's
  `mort_rate(240 + t, life)` exactly.
- *The frame's end* (§7.1, *Precised at M3*, item 5). DIA's frame ends at the age horizon,
  or at the guarantee's end where it is later, with survivors left: the anchor's life in
  its last month is 6.13e-08. Survival, the one quantity its roll-forwards read at
  `t + 1`, is carried into `t = proj_len()`, and every other count, balance and flow is
  zero there, as is every rate read at a policy year or an age, and every flag is false,
  as the guard test asserts; the clocks and the valuation-clock inputs keep their values,
  and so does `commute_disc_rate`, which reads neither clock. The count, SPIA's chassis,
  is read at `t + 1` by no roll-forward and leaves the books at the stop rule (D5).
- *`result_pols` and `result_annual`.* `result_pols` puts `pols_if` and `pols_new_biz`
  first, then S's seven survival and payment-factor columns; T1 exempts it, and the module
  compares it with S's column by column. `result_annual` keeps S's policy-year key and
  drops the years before the valuation date's, as `Term_US_SEC`'s annual report does, its
  first row holding the rest of that policy year.
- *The product's fact* (§4, *Carried into Phase 1*).
  `EXTRA_POINT_ASSERTIONS["DIA_US_SEC"]` reads S's fact, that the income starts, on the
  valuation clock, `T` kept a policy month (R1a): the income at
  `max(T - duration_mth_init(), t_entry())` is positive and is the payout schedule's,
  `annual_income_payout()`.
- *No S cell is removed or renamed.* S's four docstring slips are corrected and its nine
  lines over 92 characters wrapped, in SEC only (*Carried, outside the SEC models*).
- *The splice.* Inflation is set to 0 in both models, the Baa yield to 6.25% and the A/E
  to 1.05 in both, and `ref_rate_shift` to 0.005 in S, where SEC's is 0, the change being
  in the restated rows' column, and future rows are compared with S read at 0. The
  mortality table and the improvement scale are set apart by age and sex in both copies,
  kept small so that no later row owes nothing, and the months are chosen on those edited
  inputs. Eighteen variants of S's points, each with its premium rows, are added to the
  copies of S's table and schedule. T2 and T3 compare to 1e-9 relative with no absolute
  floor, the four roll-forward residuals at the 1e-9 floor (§5.2, precised at M11). T2
  exempts `proj_len`, `payment_surv_mth`, the premium schedule's two readers,
  `result_annual` and, on a row valued after its acceleration, `accel_payment_factor`; T3
  compares a future row's premiums by month and its annual display too. Each S point is
  released after the last T2 case that compares a row of it, and the collector is frozen
  again after the last, which took the module's peak from 4.47 GB to 2.61 GB at the tests
  stage.
- *The committed rows and a residual that is not a number* (§7.1, *Precised at M3*,
  item 11). `test_every_committed_row_continues_its_s_point` compares each derived and
  future row of the committed table with its S point, frame by frame and cell by cell. The
  future row is compared with T3's exemptions, so its premiums by month and its annual
  display are compared too; `result_annual`'s `claims_death` differs from S's by at most
  3.7e-16 relative, from summation order.
  `test_a_residual_that_is_not_a_number_fails_its_check` reads the model with
  `mort_ae_factor`, a Reference, at NaN. It asserts that the survival check fails on every
  twin, and all four checks on the commuting point's twin, each on a residual NaN in some
  month and 0.0 in every other. `DIA_US_S`'s own `max(0.0, ...)` and `a > 0.0` lose the
  NaN in the payment factor, the annuity factor and the guarantee search, so the other
  three checks pass on most twins: the income check fails on twins 1, 2, 4, 7 and 15, the
  payment factor's on 5, 7 and 15 and the commutation's on 15 alone. Unlike UL's, DIA's
  flows are NaN too, `net_cf` on every row, so the checks are a second line. No formula is
  replaced, so the test runs compiled (§5.1, step 6, precised).
- *The rules test* has no `LOOK_AHEAD`: DIA admits no read beyond `t + 1`, the commutation
  residual reading back. It follows each precedent keyed by no month through its own
  precedents to the month-keyed calls it reads (`_months_read`), which found `G`'s base
  key reading the clock, at `duration_mth(t_entry())`, from a row issued 13 months on; it
  is now the static key, and no number changed (R2, precised).
- *T4* multiplies the count by 2.5 with `ref_rate_shift` switched on, on the four twins
  that carry every counted flow and on the derived and future rows, and asserts every
  counted cell (§5.2, precised at M11).
- *T5* reads each case with a model of its own, refused by the one rule under test and
  again through a projection; a sweep that dropped each of the 68 rules in turn showed
  each failing its own cases and no other (*Faults*, below).
- *The runner* keys each point as M14's `run_sec.py` does, freezes the collector once the
  table is read and again before the projections, releases and collects each point in both
  passes, and in `--block` asks every point for its frame first.
- *M14's carried items not yet taken.* Built on M11's tip, DIA's `_mismatches` passes
  `codes=codes(sec_proj)` from the build on, but its runner does not yet carry Term's
  `--cython`, `--build` and `_tool()`, nor its module the `create()`-copy test, and
  `proj_len()` does not yet refuse the four bounds *Carried into Phase 2* names; DIA's C
  step takes them up.

**Measured for K6 and F7.** Every time below was taken with other workflows sharing the
machine, the fix stages' and the re-review's at load averages of 2.8 to 3.9.
- *Time.* By default the module ran 251 passed and 90 skipped in 193.99 s and 196.63 s in
  its final state, peaking at 2.62 GB in one process; before the second fix's two tests it
  ran 249 passed and 90 skipped in 191.1 s and 193.3 s, and 246 passed in 205.3 s before
  the fix stage's last three cases. Over the full grid it ran 341 passed in 275.2 s at
  2.33 GB, and 339 passed in 280.8 s and 282.0 s before. So the default run takes 191 to
  205 s, about 10 to 40 s more than WholeLife's module, and the full grid about 15 to 25 s
  less. Most of it is fixed: the splice's fixture (26.4 s), `sec_read` (16.4 s), `s_model`
  (12.8 s), T4's scaling (12.8 s), the runner test (12.0 s) and the module's teardown
  (6.6 s); the second fix's two tests take 1.2 s each, so a cut would come from the
  fixtures. The SEC conventions, 31 passed and 2 skipped, took 29.2 s and 29.1 s at the
  fix stage and the re-review, and 42.5 s and 38.4 s at the review. On M11's tip with DIA
  added, the uslib suite ran 1,818 passed and 255 skipped in 15 min 50 s, peaking at
  3.88 GB in one process, and 1,816 passed in 16 min 25 s and 16 min 22 s before the
  second fix, at 3.88 GB and 3.84 GB. That peak is not DIA's: DIA's module alone peaks at
  2.62 GB, `Term_US_SEC`'s alone at 3.52 GB on M11's tip, M14's compile step included, and
  DIA's followed by Term's at the same 3.52 GB, so DIA adds nothing to it; a per-module
  watch of one suite run put the high-water mark at 2.64 GB after DIA's module and at
  3.61 GB in Term's. As landed, after M3 and §8.2 item 4's fix, the suite ran 2,258 passed
  and 365 skipped in 23 min 22 s (*Verified at landing*, below).
- *Depth.* A cold `net_cf(0)` runs 13 cells deep on the twins and on points 18 and 22, 12
  on points 19 to 21 and 23 to 25, 21 on the installment refund's twin, point 5, through
  its refund-period search, and on point 26, issued 13 months on, 10 fully cold and 8 once
  `Data`'s table is read, where `DIA_US_S`'s runs 251 on points 1 and 5 and 311 on
  point 13. A cold `net_cf` of the last month runs one cell a month back to `t_entry()`
  plus 7 to 9, and 12 in all on point 25's one-row frame: 728 on the 720-month twins, 726
  on point 5, 487 on point 19, 479 of them `cum_annuity_pp`, and 728 on point 26. At the
  longest cover, issue age 22 with the income from policy month 360, 1,176 months, it runs
  1,182 on an installment refund and 1,184 on a cash refund, both at the valuation date
  and issued 120 months on. Each figure counts the count cell a table's join asks first.
  An ascending sweep runs at most 16 deep, on point 5, a recursion limit of 15.
  `CALL_DEPTH` is 40, `CHAIN_OVERHEAD` 16 and `FIRST_MONTH_DEPTH` 32. In the modelx
  export, the cold call in the last month needs a recursion limit of 1,482 on the anchor's
  twin, 1,454 on point 5's, 1,000 on point 19, 1,482 on point 26 and 2,366 at the longest
  cover, and the ascending sweep 52 on the committed points and 62 on the longest cover's
  two rows.

**Faults.** Each fault went alone into its own copy of the library, and the tests aimed at
it ran through the gate.
- *Tests stage:* 94 faults and a control, at most two at a time: a fault in each of the
  eight opening columns, at every R1a site of the design and on each named risk. Every
  fault failed some test but F64, `Data` returning the raw columns, an equivalent mutant,
  since pandas reads every accepted input as the numbers checked. F60, `G` summed in
  reverse, passed the first sweep, and fails since a loop-order check on a COLA cash
  refund restated at policy month 265 was added. A sweep that dropped each of the 48
  refusals of the time showed each failing its own cases and no other, and each of the
  module's 43 test functions of the time failed under some fault.
- *Review (tests lens):* G07 and G08, the lump sum's floor and the acceleration factor's
  read from `surv_to_payout_init()`, which turn the lump sum NaN where `l_last(T)` is
  derived, passed the default module, the conventions and the full grid; so did G10,
  `phase`'s `PRE_ISSUE` dropped, and G11, the commutation residual's acceleration add-back
  with its sign flipped. G05, the payment factor reading `surv_to_payout()` in every
  month, a 240-month look-ahead through a cell keyed by no month, failed the depth test
  alone.
- *Fix stage:* 13 faults, all failing: G05 the core rules test and the depth test; G07 and
  G08 each T2 point25-d240 and T3 point25-k13; G10 the guard test; G11 T2 point35-d252 and
  the residual test; G12, survival based at 0, T3 point1-k1, the core rules test and the
  guard test; N01 and N02, a join that skips its count, 11 and 8 `TABLES` cases; N03, the
  guarantee rule a month short, 2 `REFUSED` cases; N04, the rule skipping the valuation
  month, 1; N05, the interlock at five months, 2 `MALFORMED` cases; N06, a weight of 0
  admitted, 2; and N07, `G`'s base reading the clock, the core rules test. A sweep that
  dropped each of the 68 rules, 37 in `model_point_table`, 8 in `premium_schedule_table`,
  18 in the four count cells and 5 in `proj_len()`, showed each failing its own cases and
  no case of another rule.
- *Re-review:* re-ran G05, G07 and G11, all failing, and found §7.1's item 11 half met: no
  committed future row was compared with S frame by frame, and no test showed a check
  failing on a residual that is not a number.
- *Second fix:* F01 to F04, each check rewritten as `not any(abs(r) > tol)`, which passes
  a NaN, fail the NaN-residual test, F01 on twin 1 and the others on twin 15, and F01 and
  F04, run against the whole default module, fail it alone, the other 250 tests passing:
  before this stage no test saw a check that passes a NaN. F05, `t_entry()` a month early
  on a contract issued later, fails the committed-rows test at row 26 alone.

**Carried into RILA (M10).** What DIA adds to what §7.9's *Record — M11* carries into RILA
with the payout chassis, and §7.10's *Record — M7* with the deferred one; RILA's record
says what it took.
- *Term-start inputs* take DIA's frozen-weight shape: a column only where the term began
  before the valuation month, blank otherwise and derived bit for bit, `Data` checking its
  presence both ways and its range, the term-start index level above 0, since `index_perf`
  divides by it. §7.10's *Record — M7* gives the cap and the term-start market state
  D6's value entering month 0 instead, on every row, as MYGA's `credit_rate_init` holds
  it: 0 on a point not yet in force, and on a row valued at a term start the expiring
  term's, unread. Each form's `Data` refuses a twin written in the other, so RILA's record
  says which it took. Term starts and ends, renewals and the maturity stay policy months,
  compared with `duration_mth(t)`.
- *Far-ahead pricing* goes in one explicit loop or a static cell keyed by policy month, as
  `lives_if_pm` and the payout schedule are, never a recursion on the valuation clock, and
  a schedule's recursion is based on a key the model point fixes, never a clock read (R2,
  precised).
- *A residual that sums ahead* is measured at its period's end, reading back, and asserted
  equal to S's on every row valued at or before the period's start, since at the floor a
  residual moved to the wrong month passes; on a row valued later, look-back stops at
  `t_entry()` (R1), and DIA's residual is asserted 0.0 in every month (R2, precised).
- *Tables and refusals.* S's readers stay unchanged, and each table a join reads gets an
  int count cell beside it, which the join asks first, as DIA's and UL's do; §7.10's
  *Record — M7* carries MYGA's checked copy instead, and §7.1's *Precised at M3*, item 9,
  admits either, so RILA's record says which it took. Every flag column is validated by
  value, True or False, or 1 or 0, and decoded from the checked value; and the option
  combinations the product's interlocks forbid are refused by name.
- *Tests.* Walk the rules test through each precedent keyed by no month to every
  month-keyed call it reads, and test the cap over both models. Write §7.1's item 11's two
  tests from the start: every committed derived and future row compared with its S point
  frame by frame, the future rows with T3's exemptions; and a residual that is not a
  number failing each check, sent through a Reference the residuals read, set before the
  model computes anything, so that it runs compiled, each check asserted only where its
  residual goes NaN, since S's own `max` and comparisons can lose one.
- *The count.* RILA's is a decrement chain, so its `pols_if` is `BEF_DECR` and needs no
  registry flag.

**Carried into every product still to come.** The first two were found writing §7.1's
item 11's tests at the second fix, the next two at the tests stage, and the last by the
design:
- The helper that compares a committed row with its S point takes the exemption set as a
  parameter: a future row compares more than a restated one, its whole schedule and its
  whole policy years.
- A NaN-residual test asserts that the residual is NaN in some month and 0.0, or within
  its tolerance, in every other, which shows the check failing on the NaN and not on a
  finite residual; where a Reference feeds the residuals, it sends the NaN through it, set
  before the model computes anything, so that the test runs compiled (§5.1, step 6,
  precised).
- The rows a module's product tests read are built in the splice's fixture while S is
  swept, and read once; each spliced S point is released after the last T2 case that
  compares a row of it, and the collector frozen again after the last, which took DIA's
  peak from 4.47 GB to 2.61 GB.
- A schedule summed by a loop has the loop's order asserted on a row whose instalments
  step: on level instalments a reversed loop gives the same float, and F60, `G` summed in
  reverse, passed every other test.
- An aggregate over a whole schedule becomes an opening-state column wherever the
  companion keeps only what is still due, as `guarantee_mths_pricing_init` carries `n_g`.

**Carried into Phase 2.**
- *Engine functions* (R14): S's float-parameter cells, `annuity_factor` and
  `pricing_disc_factor`, kept for S's tests and T1, which call them; Phase 2 inlines them.
- *Rounding* (R16): `purchase_rate`'s `round(pr, dp)` and `rop_factor`'s
  `int(round(deferral_yrs(k)))`, which Phase 2 precomputes in `Data`.
- *T1 and codes:* S's `claims(t, kind=None)` and `claims_ann(y, kind=None)` keys need a T1
  `arg_map` at stage `EC` (R12). `_mismatches`, the module's one call of
  `twin_mismatches`, passes `codes=codes(sec_proj)`, so the splice's comparisons take
  Phase 2's codes when they come.
- *Label accessors* that R17 and C5 do not admit as worded: `payout_form()`, derived from
  `income_form`, `payment_timing()`, which returns `timing`, and `sex(life)`; DIA's C step
  extends R17 and C5 for those three, or leaves them out of `"reporting"`.
- *Containers to remove:* `premium_by_mth`'s dict and `premium_pm`'s lookup in it, which
  become a dense `[idx, month]` array; `guarantee_mths_pricing`'s sum over the dict; the
  lists of `horizon_mths` and `qlac_flags`; and `phase`'s strings (R10).
- *`Data`:* the four count cells are R7's checking ints: Phase 2 sizes the ROP factor's
  array and the per-point payout factor from them, and int sex and form codes replace the
  string-keyed `.loc` joins.
- *Caches and bounds:* `t` 0..1,296, `k` 0..1,180, `y` 1..99 and `x` 22..119, as the
  spec's comment in `sec_support.py` derives them. Four inputs those sizes rest on are
  bounded by the product and refused by no cell at stage `E`: the issue age, 22 or more,
  the joint annuitant's age, the income start month, 13 to 360, and the certain period, 10
  to 30 years on PC. Phase 2 refuses each in `proj_len()` beside the cover check, or sizes
  the caches from the product's limits. The export's limits above size `sample_sec.py` and
  `run_sec.py --cython`.
- *Tests on the compiled model:* the NaN-residual test and the cap test's NaN case set a
  Reference before the model computes anything, so they run compiled unchanged (K7).

**Carried, outside the SEC models.**
- Fifteen S-side items for §8.2 item 4, found in `DIA_US_S`; the first is fixed in neither
  model, the rest in `DIA_US_SEC` only, refused there or corrected in its formulas or
  docstrings:
  - a joint cash refund below a 100% survivor percentage nets the unreduced schedule, so
    the refund after the first death is understated: points 8 and 9 ship it at two thirds,
    and §7.9's record carries the same item for `SPIA_US_S`;
  - a premium at or after the income start raises the instalments but not the refund base,
    `CP(T)`;
  - `commute_weight` assumes the commutation is in payout: one taken before `T` weighs
    `l_last(t_c)`, above the payment factor from `T` on in the guarantee, and the expected
    instalment goes negative;
  - an adjustment with one month blank, or a new start at or before the exercise, gives a
    start of -1 or one before the exercise;
  - an adjustment at or after the elected income start month pays nothing from that month
    to the exercise;
  - a point with no premium rows projects silently: point 1 copied under a new `point_id`
    totals -1,985.46 in `net_cf`, its expenses, against point 1's -277,363.94;
  - a joint point on the table basis is refused only when a premium is priced, naming no
    point;
  - the option and integer accessors take `int()` of the raw value, so 60.5 reads as 60
    and text raises Python's own message;
  - `bool()` of the `joint` column reads any text as True;
  - a blank `survivor_pct` or `cola_rate` is lost through a `max`;
  - an acceleration and a commutation inside each other's six months, which the product's
    interlock forbids: in the blackout the commuted value counts instalments the lump sum
    paid;
  - an acceleration after a commutation, inside its guarantee, pays the commuted cohort
    its pulled-forward instalments again (point 15 accelerating at 258: 7,805.70 of
    8,282.92), its check fails, and `check_commutation_value_resid`'s docstring calls the
    combination unreachable;
  - `check_lives_roll_fwd_resid` is the telescoping identity;
  - four docstring slips: `purchase_rate_dp` says None where it returns -1;
    `annuity_factor` nests a literal in bold; `liability_cf` has a stray space; and "`n_g`
    is two different quantities" goes on to describe three;
  - nine lines of `Projection` exceed 92 characters.
- *Tools*, for the next change to `tools/`:
  - `tools/gen_scaffolding.py` ignores an option it does not know, `--help` among them,
    and runs, writing the pages: at M12's fix stage `--help` rewrote uslib's doc tree,
    every file as it was;
  - doccheck's autodoc import writes `__pycache__` into the model folders of all six
    libraries, 183 directories at M12's docs stage; git ignores them, and
    `PYTHONDONTWRITEBYTECODE=1` in its Sphinx subprocess would stop it.

**Landing.** Rebased from 244360e (M11) onto e3e026e, after M3 and §8.2 item 4's fix.
`DIA_US_S` there caps its annual mortality with the bound second,
`min(mort_ae_factor * q, 1.0)`, which `DIA_US_SEC`'s `mort_rate_py` already wrote, so that
fix changed no formula of `DIA_US_SEC`. uslib's `index.md` took one conflict, the sentence
that lists the SEC models, which now names all six; `sec_support.py` took two, where DIA's
state extractors and spec follow MYGA's and UL's, all three kept; and `DIA_US_SEC`'s
`Projection` one, `mort_rate`, where the enhancement's, which reads `mort_rate_py`,
replaces the copy's. `INPUT_FILES`, regenerated with `gen_input_files.py --write`, came
out unchanged. `model-sec.md` now says the valuation-date base of `G` serves the refund
balance, its one other reader, where it named the commuted value too, which reads the
schedule instead; and `tools/gen_sec_points.py`'s docstring cites §5.1's step 10 for
`CLAUDE.md`'s name search, where it cited step 9, the number before the rates step was put
in as step 6.

**Verified at landing**, with two other workflows, FIA's and VUL's builds, sharing the
machine. The uslib suite, with modelx-cython installed and so the compile tests included,
gave 2,258 passed and 365 skipped in 1,402.73 s (23 min 22 s), its two warnings modelx's
renames of `Term_US_S` and `VUL_US_S` in the round-trip tests. DIA brings 251 passes and
90 skips in its module, 31 passes and 2 skips in its SEC conventions, and one pass in the
compiled convention that reads every SEC model. Over its full grid, DIA's module gave 341
passed in 272.44 s, and the `cython` selection 11 passed and none skipped under
`USLIB_REQUIRE_CYTHON=1`, in 118.99 s. doccheck built 497 pages with 0 warnings.
`gen_sec_points.py --check` found the files of the six SEC models current, and
`gen_sec_fingerprint.py Term_US_SEC --check` reproduced the fingerprint. md_lint reported
0, `gen_scaffolding.py --dry-run` 0 files in each of the six libraries, and
`gen_citation_links.py --dry-run` nothing on its 301 source tags. A case-insensitive
search of `model_point_table_sec.csv` and `premium_schedule_sec.csv` for every publisher,
product, form number, document code and host that `deferred_income_annuity/sources.md`
cites, each name's words matched also when joined by underscores, dots or hyphens or run
together, found none. These runs came before the landing's last edits, to two lines of
`model-sec.md` and to this plan, and before the rebase onto e3e026e, which changed two
lines of §8.2 item 4; none of them changed code or a test. On the tree as committed,
doccheck again built 497 pages with 0 warnings, md_lint reported 0 on uslib and on this
plan, `gen_citation_links.py --dry-run` nothing on its 301 source tags, and
`gen_scaffolding.py --dry-run` 0 files in each of the six libraries.

---

## 8. Risks and open questions

### 8.1 Risks

- **K1 — modelx-cython is at 0.1.0.**
  - Pin it in `requirements-cython.txt`.
  - C3 catches any regression in typing; the `cython` CI job catches compile failures on
    MSVC.
  - *M14:* `build_sec_cy.py` adds two directives mx2cy leaves at their defaults,
    `infer_types=True` and `cpow=True`, which C3 requires, and `-ffp-contract=off` to
    `CFLAGS` off Windows, which the toolchain test reads from the compile lines; and mx2cy
    0.1.0 types no uncached cell, which C5 refuses (R14). Move the modelx-cython pin with
    all of these checked.
- **K2 — Memory (F5).**
  - A compiled block run that keeps its ItemSpaces holds ~2.6 MB per point.
  - `run_sec.py --block` releases each one as it goes, and `model-sec.md` says why.
  - The benchmark records peak RSS beside time.
  - *M14:* the release is `gc.freeze()` once the table is read, `del` and a full
    `gc.collect()` per point in both passes and `gc.freeze()` again between them; a
    compiled Term ItemSpace is 429,896 bytes; `tools/bench_sec_cy.py` records 84 MB peak
    on 6,000 compiled points, flat over the loop.
- **K3 — Branch flips at knife edges.**
  - Floors such as `max(0, AV)`, depletion flags and NLG tests can turn a 1e-15 difference
    into a different branch.
  - The splice tolerance is relative, as C4's is off x86-64, and the splice months avoid
    exact thresholds.
  - A flip that does occur is investigated, never loosened away.
  - *M14:* C4 is exact on x86-64, so a one-ulp drift is seen before it can flip a branch.
    That needs the build's `-ffp-contract=off` as much as `cpow=True`: gcc and clang fuse
    a multiply and an add wherever `-march` gives the instruction, and a `-march=native`
    build without the flag gave `plt_mort_factor(10)` 2.15 against modelx's
    2.1500000000000004.
- **K4 — Future new business on market products.** Each future point needs its inputs
  re-based in T3; RILA and VA carry the most. D4's fallback exists for exactly this.
- **K5 — A wide in-force interface.**
  - VA adds about ten opening-state columns, RILA thirteen, and IUL a 12-slot ladder.
  - Each must come from an administration extract that may not carry it — a VA's highest
    quarterly value this contract year, a RILA's term-start volatility.
  - Ladders go in long companion tables keyed `(point_id, slot)`. Two or three funds stay
    as wide `_init_<i>` columns, as VUL's are today.
  - Each `model-sec.md` documents, column by column, what the field is and the instant it is
    measured at. Where an approximation is defensible, its consequence is stated, and it
    stays out of the model.
  - *M10:* RILA's thirteen are seven amounts, five term-start market values and the
    re-solved cap. Two of the amounts reach no report: `av_pp_init` opens month 0's
    investment return and `av_change`, which cancel in the Account Value's roll-forward,
    and `av_pp_prev_anniv_init` feeds the year's base and allowance outside anniversary
    months and `proj_len()`'s remainder rule; `Data`'s renewal and anniversary rules and
    T2 still hold both. The five term-start values are given only where the term under way
    began before the valuation month, and the cap only where that term began at a renewal
    under `nge_reset`; each is blank elsewhere (§7.8, *Record — M10*).
- **K6 — CI time.**
  - The matrix already takes up to 33 minutes against a 90-minute limit, and the SEC suites
    roughly double the projected volume.
  - Measure it on Term in Phase 0. If it threatens the limit, the splice sweeps move behind
    an opt-in marker before the timeout is raised.
  - *Phase 0:* T1 about doubles the sweep of the points it pairs; Term pays under a second
    (§4, *Record*). T2 is measured on Term at M1.
  - *M1:* T2 takes about 11 s on Term's 23 splices, fixture included, and Term's whole
    module 32 to 37 s; the uslib suite grew by about a minute (§7.1, *Record*). WholeLife's
    sweep is about ten times Term's, so M2 is the next measurement.
  - *M2:* WholeLife's module over its full splice grid, 105 T2 cases and 31 T3 cases,
    runs in 4 min 57 s, so by default it runs a core of 32 and 8 cases, which a test
    asserts reaches every branch, opening-state column, kind of valuation month and premium
    mode the full grid reaches. The other 73 and 23, and the rules test's scan of their
    rows, carry a `sec_full` marker and skip unless `USLIB_SEC_FULL=1`. The module then
    runs in 2 min 46 s to 3 min 01 s, 111 passed and 97 skipped, at a peak of 2.7 GB in
    one process, because each splice row is released once compared. The limit is not
    threatened yet, so the split is not this risk's remedy. It bounds the module's time on
    every leg but one: `ubuntu-latest` with Python 3.13 sets `USLIB_SEC_FULL=1`, so every
    CI run runs the full grid, for about two minutes more on that leg. The uslib suite
    went from 1,154 passed and 12 skipped in 5 min 54 s (M1) to 1,298 passed and 109
    skipped in 9 min 02 s to 9 min 18 s; the 144 new passes are the module's 111 and the
    SEC conventions' 33. These times were taken with other workflows sharing the machine.
    WholeLife added about 3 min 20 s to the suite. If each of the ten products still to
    come added as much, every leg would run about half an hour longer and the full-grid
    leg about 20 minutes more again, which on local times would bring the slowest leg near
    the 90-minute limit. So each record compares its module's cost with WholeLife's, and
    M13 measures the matrix.
  - *M14:* as landed, Term's module runs 99 modelx tests and 7 compile tests, and the
    `cython` selection 11 tests, Term's compile and the toolchain's among them. From the
    fix stage to the second, on Linux under load, the selection's 10 ran in 140 to 173 s,
    Term's compile in 53 to 67 s and C4 on its 55-point splice grid in 25 to 34 s; with
    the cap's compile test, the 11 ran in 144 to 201 s at the cap's stages and in 259 s at
    landing, beside the uslib suite and the three Phase 1 streams. The uslib suite with
    modelx-cython installed gave 1,217 passed and 12 skipped in 8 min 34 s on M14's tree
    before its rebase onto M2, and 1,364 passed and 109 skipped in 15 min 05 s as landed,
    WholeLife's module included.
  - *M11:* SPIA's module runs by default a core of 29 T2 and 11 T3 cases, which a test
    asserts reaches each listed branch and line coverage showed reaching every line the
    full grid reaches, in 3 min 11 s to 3 min 16 s (139 passed, 52 skipped). Its full
    grid, 62 and 29 cases, runs in 4 min 03 s to 4 min 25 s, at a peak of 2.72 GB in one
    process, and its SEC conventions take 44 s to 48 s. Most of its time is fixed, so the
    core saves only about a minute. By default it costs about 10 to 30 s more than
    WholeLife's module, and over the full grid about 30 to 55 s less. The uslib suite on
    M2's tip with SPIA added ran 1,468 passed and 163 skipped in 14 min 30 s to 14 min
    53 s, of which SPIA's share is about 4 minutes, and as landed, on M14's tip, 1,535
    passed and 163 skipped in 16 min 36 s. All times were taken with other workflows
    sharing the machine.
  - *M7:* MYGA's module holds 34 tests and 223 cases, six of them added at landing. Over
    its full grid, 72 T2 and 18 T3 cases, it ran 217 passed in 7 min 17 s at a peak of
    2.52 GB, and 207 passed in 7 min 14 s and 6 min 55 s before the second fix, so by
    default it runs a core of 17 and 7, which a test asserts reaches each category, kind
    of valuation month, opening-state column and named branch of the full grid. The other
    55 and 11, and the rules test's scan of their rows, carry `sec_full`. By default it
    ran 150 passed and 67 skipped in 4 min 31 s, at a peak of 2.33 GB in one process, and
    140 passed and 67 skipped in 3 min 58 s and 4 min 41 s before the second fix. Most of
    that is fixed: eight tests and fixtures take about 156 s together, and the 24 core
    cases took 55 s of one suite run, in which MYGA's module took 3 min 54 s of test time,
    WholeLife's 2 min 40 s, and MYGA's SEC conventions 37 s. By default it costs about 1
    to 2 minutes more than WholeLife's module, and over the full grid about 2 minutes
    more. The uslib suite on M2's tip with MYGA added ran 1,480 passed and 177 skipped in
    14 min 50 s, at a peak of 2.69 GB, and as landed, on M11's tip, 1,722 passed and 231
    skipped in 21 min 45 s. For C4, the full grid's 90 rows held 3,976,300 cached values
    over 34,718 months at the tests stage, against 1,067,350 on Term's 55 points. All
    times were taken with other workflows sharing the machine.
  - *M3:* UL's module runs by default a core of 20 T2 and 5 T3 cases, which a test asserts
    reaches every branch, opening-state column and kind of valuation month the full grid
    reaches, the corridor binding on either option, the lapse rate's cap and charges
    ceasing in cover among them, in 3 min 39 s and 3 min 50 s (159 passed, 41 skipped), at
    a peak of 2.45 GB in one process. Its full grid, 54 and 11 cases, runs in 5 min 30 s
    (200 passed) at 2.52 GB, and its SEC conventions take 17 s to 19 s. A splice or future
    case takes up to 4.5 s. By default the module costs about 40 s to 1 min more than
    WholeLife's, and over the full grid about 30 s more. The uslib suite on M2's tip with
    UL added ran 1,489 passed and 151 skipped in 13 min 54 s and 14 min 14 s, of which
    UL's share is about 4 minutes, and as landed, after M7 and Term's cap fix, 1,938
    passed and 273 skipped in 17 min 55 s, with no other workflow sharing the machine. The
    other times were taken with other workflows sharing the machine, and the module's, its
    full grid's and the suite's on M2's tip at a load average of 1.5 to 2.8.
  - *M12:* DIA's module runs by default a core of 36 T2 and 8 T3 cases, which a test
    asserts reaches each listed branch and line coverage showed executing all 660
    `Projection` lines the full grid executes, in 191 to 205 s (251 passed and 90 skipped
    in its final state), at a peak of 2.62 GB in one process. Its full grid, 112 and 21
    cases, runs in 272 to 282 s at 2.33 GB, and its SEC conventions take 29 to 43 s. Most
    of its time is fixed, so a cut would come from its fixtures. By default it costs about
    10 to 40 s more than WholeLife's module, and over the full grid about 15 to 25 s less.
    The uslib suite on M11's tip with DIA added ran 1,816 to 1,818 passed and 255 skipped
    in 15 min 50 s to 16 min 25 s, and as landed, after M3 and §8.2 item 4's fix, 2,258
    passed and 365 skipped in 23 min 22 s. The suite's peak, 3.6 to 3.9 GB in one process,
    is reached in `test_term_life_us_sec.py`, whose module peaks at 3.52 GB alone on M11's
    tip, M14's compile step included; DIA's module followed by Term's peaks at the same
    3.52 GB, so DIA adds nothing to it (measured at M12's re-review and again at its
    second fix). All times were taken with other workflows sharing the machine.
  - *M8:* FIA's module runs by default a core of 12 T2, 5 T3 and 5 switched-Reference
    cases, which a test asserts reaches each listed condition and line coverage showed
    running all 706 `Projection` lines the full grids run, in 317 to 330 s (231 passed and
    49 skipped as landed), at a peak of 3.15 GB in one process at the second fix, most of
    it two module fixtures held to the end. Its full grid, 44, 15 and 9 cases, runs in 452
    to 471 s, and its SEC conventions take 34 to 37 s. Most of its time is fixed: nine
    fixtures and whole-model tests take about three minutes, so a cut would come from
    them. By default it costs about 135 to 165 s more than WholeLife's module, and over
    the full grid about 155 to 175 s more. The uslib suite on M7's tip with FIA added ran
    1,990 passed and 281 skipped in 21 min 58 s to 22 min 48 s, at a peak of 3.86 GB in
    one process, and on the landing's tree, after Term's cap fix, M3, §8.2 item 4's fix
    and M12, and before its review added one case, 2,524 passed and 415 skipped in
    31 min 18 s. All times were taken with other workflows sharing the machine.
  - *M4:* VUL's module runs by default a core of 17 T2 and 5 T3 cases, which a test
    asserts reaches every option, class, schedule, issue age and kind of valuation month
    the full grid holds and 36 conditions on the splice's rows, in 424 to 432 s (240
    passed and 43 skipped at the second fix), at a peak of 3.39 GB in one process, in
    committed-model tests that read two more models beside two swept module fixtures. Its
    43 full-only cases run alone in 228 to 238 s at 2.72 GB, and its SEC conventions take
    19 to 21 s. That is about 2.4 times the three minutes this risk projects for each
    product from WholeLife's module, with the core already in place, and most of it is
    fixed: eleven fixtures and whole-model tests take about four minutes, so a cut would
    come from them, as the fix stage found, from the runner's subprocesses, the second
    half of the returns test or the extract's loop over the points, not from T2 or T3.
    M13, which measures the matrix, weighs it. By default the module costs about 240 to
    270 s more than WholeLife's. The uslib suite on ed73164 with VUL added ran 2,214 to
    2,216 passed and 317 skipped in 27 min 17 s to 27 min 57 s, at a peak of 3.71 GB in
    one process, and on the landing's tree, after d3a7be8, M12 and M8, and before its
    review added two cases, 2,798 passed and 459 skipped in 40 min 08 s. All times were
    taken with other workflows sharing the machine.
  - *M10:* RILA's module runs by default a core of 37 T2 and 6 T3 cases, which a test
    asserts reaches each listed property and line coverage showed running every
    `Projection` and `Data` line the full grid runs, in 287 to 383 s, 4.8 to 6.4 minutes
    (230 passed and 75 skipped at the fix stage), at a peak of 2.74 GB in one process. Its
    full grid, 101 and 16 cases, runs in 442 to 544 s, at 3.18 GB at the fix stage, and
    its SEC conventions take 34 to 36 s. That is about 1.6 to 2.1 times the three minutes
    this risk projects for each product from WholeLife's module, and past the design's
    five minutes in every run but the fastest, with the core already in place. Most of it
    is fixed: nine fixtures and whole-model tests take about 226 s together, where T2's 37
    core rows take 53 s. The design's remedy past five minutes, thinning the core of
    360-month rows that reach no branch another core row lacks, was not taken, since the
    core runs exactly the lines the full grid runs, so a cut would come from those rows or
    from the fixed costs. M13, which measures the matrix, weighs it. By default the module
    costs about 105 to 215 s more than WholeLife's, and over the full grid about 145 to
    245 s more. The uslib suite on e011a0c with RILA added ran 2,524 passed and 441
    skipped in 32 min 24 s to 34 min 01 s, at a peak of 3.72 GB in one process, and on the
    landing's tree, after M8 and M4, 3,063 passed and 535 skipped in 52 min 31 s. All
    times were taken with other workflows sharing the machine.
- **K7 — Tests that need modelx.** S tests that override formulas, reassign References and
  `clear_all`, or match `raise` source text, have no compiled equivalent. They stay in C1,
  and C4 compares what the cells return and raise.
  - *M14:* a compiled model clears no cache when a Reference is set: an ItemSpace takes the
    References when it is made and keeps its values until it is deleted, and the base Space
    and `Data` keep theirs for good; a compiled test pins it, and every Reference is set on
    a model just imported.
- **K8 — Upstream packaging.**
  - lifelib's CI will not install modelx-cython, so the compile tests must skip (D13).
  - No build output may reach the wheel or sdist: `MANIFEST.in` should prune `*_nomx*` as
    it prunes `_research/` (MERGE.md §2).
  - *M14:* `run_sec.py --cython` builds in place by default, leaving `<Model>_nomx/`,
    `<Model>_nomx_cy/`, `setup.py` and `build/` in the product directory; `.gitignore`
    covers them, but `MANIFEST.in` must prune `*_nomx*`, a `setup.py` beside a model and
    `build/` at the merge, or a `lifelib.create()` made from such a working tree copies
    them.
- **K9 — DIA's two survival curves.** Separating pricing from projection survival is the
  only Phase 1 change that restructures a model rather than extending it. It goes last, on
  the most mature harness.
  - *M12:* the streams put DIA second in the Payout stream, after SPIA (§5.3), not last.
    Its pricing reads a survival curve of its own, `lives_if_pm`, one loop from issue and
    S's recursion bit for bit, beside the projection's, which opens from the per-life
    columns; its cold `net_cf(0)` runs at most 21 cells deep on the committed points,
    where `DIA_US_S`'s runs 251 to 311 (§7.12, *Record — M12*).

### 8.2 Decisions

Items 1, 2, 3 and 5 were confirmed on 2026-11-01, as recommended, and item 4 on
2026-11-03.

1. **Future new business (D4).** Supported, as BasicTerm_SE does, with D4's per-product
   fallback. *Confirmed.*
2. **Economic inputs on the valuation clock (D7).** Expense inflation and mortality
   improvement run from the valuation date, so unit costs are in valuation-date dollars.
   New business is unaffected; S's existing in-force rows differ by design. *Confirmed.*
   Improvement is meant where it runs from the projection start; a scale dated by the
   calendar, as SPIA's is, stays on the policy clock (D7, precised at M11).
3. **Doc layout (D9).** Per-model autodoc folders for S and SEC alike, a one-time URL change
   before the merge. *Confirmed.*
4. **Small S fixes found on the way** — RILA's invalid escape, the `pols_if_at` stubs in UL
   and VUL that return `pols_if` for every timing, and the cap on an annual decrement rate
   built as a product of factors, `min(q, 1.0)` (§5.1, step 6), which `Term_US_S`,
   `UL_US_S`, `VUL_US_S`, `IUL_US_S` and `WholeLife_US_S` lacked, as did any of
   `MYGA_US_S`, `VA_US_S` and `RILA_US_S` whose factors can take a rate past 1.
   `SPIA_US_S`, `DIA_US_S`, `FIA_US_S` and `ULSG_US_S` capped with the bound first,
   `min(1.0, q)`, which reads a NaN as 1. Separate PRs on the S models? *Recommended: the
   escape, yes; the stubs are superseded in SEC and can stay; the cap, in each S model
   where it changes no shipped number, as on Term's points, with its bound second, while
   SEC caps whatever S does.*
   *Confirmed*, and done on 2026-11-03 in commits of their own. The first, which can go to
   `main` as a PR by itself, makes `RILA_US_S`'s Projection docstring a raw string, the
   same text at run time. The second caps the annual mortality of the ten S models whose
   rate is a product of factors, `min(q, 1.0)`: it adds the cap to `Term_US_S`,
   `WholeLife_US_S`, `UL_US_S`, `VUL_US_S`, `IUL_US_S` and `RILA_US_S`, and puts the bound
   second in `SPIA_US_S`'s two caps and in `DIA_US_S`'s, `FIA_US_S`'s and `ULSG_US_S`'s.
   `MYGA_US_S` and `VA_US_S` read the table rate with no factor and need none. On every
   shipped point of the ten, each value the model caches is the value it cached before, of
   the same kind, bit for bit: 4.29 million values, no rate above 1 and none NaN before.
   With it, `WholeLife_US_SEC` caps as `WholeLife_US_S` does, with a cap test on Term's
   form, at an A/E of 5.0, where the product passes 1 at attained age 97, and a test that a
   NaN stays NaN through the cap; `SPIA_US_SEC` puts its bounds second as `SPIA_US_S` does,
   with a NaN test of each cap; the cap tests of `Term_US_SEC` and `UL_US_SEC` compare
   every cell, the capped months included, where S turned complex before; and `UL_US_SEC`
   gains the NaN test Term's cap has. A third, after a review of the second, corrects the
   texts it left stale and holds the S models to it: `tests/test_mortality_caps.py` reads
   each of the ten, feeds its product a NaN and then a factor that takes it past 1, through
   its A/E factor, its class factor and its rating, each in turn where it has one, asserts
   the float NaN and then the float 1.0, and holds `SPIA_US_S`'s first cap where its second
   cannot bind. It reads each model where every factor of the product it does not feed
   differs from 1, and on each branch of the product: `Term_US_S` at `t = 0`, in its level
   term, and at `t = 120`, where M(1) is 3.5, `ULSG_US_S` at `t = 12`, where its improvement
   factor is 0.99, and `DIA_US_S` on its first point and on its one point on the
   generational basis. A review of it before it was pushed found that, reading each model
   once, at `t = 0` of its first point, it passed a cap that left outside a factor that it
   did not feed and that was 1, or not applied, where it read, the class factor, the PLT
   factor or the improvement of `ULSG_US_S` or `DIA_US_S`, and a cap missing from a branch
   it did not read, `Term_US_S`'s after its level term or `DIA_US_S`'s on the generational
   basis. Of 60 faults injected one at a time, each of the eleven caps removed, written with
   its bound first or bounded by the int 1, 23 caps each put on part of its product, a
   factor left outside, and four caps each put on one branch of it, it fails 59, where
   before that review it failed 50; the one it passes, `SPIA_US_S`'s first cap bounded by
   the int 1, changes no value, since the rating's float multiplies it before any rate is
   returned. Of the second and the third, only the S `Projection` modules can go to `main`
   as a PR by themselves, cherry-picked onto a branch from `main` with the other files left
   out: this plan, the SEC models and their tests and `model-sec.md` pages, and the new
   test, which reads the registry's `is_sec`, `point_keys` and `projection`, none of which
   `main` has. The fix is to mortality alone: the lapse rates' bounds keep S's order,
   `VA_US_S`'s and `IUL_US_S`'s at 1 among them (§5.1, step 6). The stubs stay,
   `ULSG_US_S`'s and `IUL_US_S`'s too (§7.3, *Record — M3*), and so do the other S-side
   items the records list, each fixed in its SEC model only where its record says so, and
   otherwise in neither, `test_term_life_us.py`'s race among them (§7.1, *Record — M1*). The
   records written before these fixes describe the models as they were then: `Term_US_S`,
   `UL_US_S`, `VUL_US_S` and `IUL_US_S` uncapped, and the caps of `SPIA_US_S`, `DIA_US_S`,
   `FIA_US_S`, `ULSG_US_S` and `SPIA_US_SEC` bound first.
5. **The `cython` CI job on Windows from the start (D13).** MSVC and the 1 MB main-thread
   stack are where a compiled model differs most. *Confirmed.*

---

## 9. Milestones

| # | Milestone | Content | Gate |
|---|---|---|---|
| M0 | Phase 0 — **done**, 2026-11-01 | Registry, conventions, scaffolding, `sec_support.py`, tools, CI job (§4) | every S model still green; Term's suite time measured (K6) |
| M1–M12 | Phase 1, one PR per product: M1, Term, and M2, WholeLife, **done**, 2026-11-01 (§7.1, §7.2); the other ten in §5.3's three streams, Life (M3–M6), Deferred annuity (M7–M9) and Payout (M11, M12, M10), of which M3, UL, M7, MYGA, and M11, SPIA, are **done**, 2026-11-02 (§7.3, §7.10, §7.9), and M12, DIA, M8, FIA, and M4, VUL, are **done**, 2026-11-03 (§7.12, §7.11, §7.6), and M10, RILA, the Payout stream's last, is **done**, 2026-11-04 (§7.8) | §5.1 recipe, T2–T6, `model-sec.md`, `run_sec.py` | T1–T6 and conventions green; doccheck zero; each product rebased onto the branch and the suite rerun before it lands |
| M13 | Phase 1 freeze | Fingerprints for every SEC point, Term's frozen at M14; `index.md`'s SEC conventions; M11's T2, T3 and T4 precisions taken into Term, WholeLife, MYGA and UL, and FIA's committed future row compared with its S point frame by frame, before the fingerprints are frozen (§5.4); M10's T5 precision taken into the eight products landed before RILA and its T4 precision into WholeLife, and RILA's first-year and first-term tolerances pinned from both sides and its first-term rule refused at month 1 (§5.4); and how CI runs the docstring parse tests, which skip where docutils is absent, settled across products (§7.8, *Record — M10*) | the whole matrix green under its timeout |
| M14 | Phase 2 for Term, brought forward to run beside Phase 1's streams (D2) — done on Linux, 2026-11-02; its Windows gate awaits the `cython` job's first run (§7.1, *Record — M14*) | Term's Phase 1 fingerprint frozen first; §6.1 recipe, `sample_sec.py`, `spec_sec.py` | C1–C5 green on Linux and Windows; C6 recorded |
| M15–M25 | Phase 2 for the other eleven, after M13, one PR per product, in §5.3's order | §6.1 recipe, `sample_sec.py`, `spec_sec.py` | C1–C5 green on Linux and Windows; C6 recorded |
| M26 | Close | The `cython` job made required; a benchmark table in `index.md` | — |
