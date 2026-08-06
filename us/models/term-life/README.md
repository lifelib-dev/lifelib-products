# TermLifeUS — reference liability cash flow model

**Status:** Draft, 2026-08-06. Built from
[`us/products/term-life/technical-notes.md`](../../products/term-life/technical-notes.md);
the product it implements is specified in
[`product-spec.md`](../../products/term-life/product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual elements — the guaranteed premium schedule, the policy fee, expiry at
> attained age 95 — are sourced from a specimen policy. Every behavioural and expense
> assumption is a **[std]** standardization introduced for the reference implementation,
> because no public source carries them. Replace them with company data before drawing
> any conclusion from the numbers.

## Run it

```bash
python us/models/term-life/run.py
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("us/models/term-life/TermLifeUS")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a tidy `DataFrame` indexed by policy year `t` with one column per
cash flow line.

## Inputs

All inputs are CSVs inside the model folder, so every value is visible in a diff. There
are no pickled values — `_data/` contains only `iospecs.py`.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Model points. **Point 1 is the worked-example anchor cell** (M35 / StdNT / $100k / T10 / annual). Points 2 and 3 exercise the formula path and a different plan | anchor cell from the specimen [S6] |
| `premium_rates.csv` | Guaranteed premium schedule by policy year, with a `provenance` column marking each row | sourced anchors [S6]; intermediate ART years geometrically interpolated **[std]** |
| `mort_best_estimate.csv` | Best-estimate mortality by age, with a `provenance` column | ages 35–46 are the worked example's illustrative vector; ages 47+ are a geometric extension **[std]**, *not* a published table |
| `class_factors.csv` | Rate-class factors 0.80 / 0.90 / 1.00 / 1.75 | **[std]**, technical notes footnote A |
| `shock_lapse_table.csv` | Shock lapse by jump-ratio bucket | **[std]**, technical notes |

To swap in a licensed mortality basis, replace `mort_best_estimate.csv` with a
same-schema file — no formula changes.

## Cells → technical notes

| Cells | Implements | Notes section |
|---|---|---|
| `l`, `d_death`, `surv`, `c`, `x` | `l(t+1) = l(t)(1−q)(1−cv)(1−w)`, deaths → conversions → lapses | Decrement order and recursion |
| `q`, `q_base`, `class_factor`, `M_plt` | base × class factor × PLT deterioration | Assumption inputs (c); PLT mortality deterioration |
| `J`, `M1`, `M1_formula` | jump ratio and M(1) — see the fixture note below | PLT mortality deterioration |
| `w`, `shock_lapse` | level-period vector, anticipatory rise, shock at year *n*, PLT run-off | Policyholder behavior |
| `cv`, `conv_elig` | conversion while `t ≤ n` and attained age < 70 | Conversion |
| `AP`, `band` | guaranteed premium lookup, fee included | Assumption inputs (a) |
| `G`, `K`, `X_tax`, `E`, `DC`, `CV`, `NetCF` | the cash flow block | Cash flows |
| `max_t`, `phase`, `attained_age` | expiry at attained age 95; LEVEL / PLT / EXPIRED | Model scope and conventions |
| `expiry` | lives whose coverage ends at 95 — see below | model-side addition |
| `result_cf` | tidy output | — |

### One cells the notes do not define: `expiry`

The notes give the roll-forward as `l(t+1) = l(t)(1−q)(1−cv)(1−w)` and, separately, the
rule "l(t) = 0 for x+t−1 ≥ 95". Those two do not reconcile in the final policy year: the
survivors of year 60 do not lapse, die or convert — their coverage simply runs out — so
`l(t) − l(t+1)` exceeds `d + x + c` there and the roll-forward appears to lose lives with
no cause.

`expiry(t)` names that quantity (zero in every year but the last), which makes the
identity close exactly:

```
l(t) − l(t+1) = d_death(t) + x(t) + c(t) + expiry(t)      for every t
```

This is bookkeeping, not a new assumption — the value is fully determined by the notes'
own rules. It surfaced because the test asserting the identity failed at t = 60.

## Fixture note: M(1) is 3.50, not 3.4514

The technical notes give the rule `M(1) = min(8.0, 1 + 0.55·(J−1))`, which for the anchor
cell's `J = 5.4571` returns **3.4514** — but the worked-example table is computed with
**3.50**. The notes acknowledge this ("M(1) = 3.45 ≈ 3.50 (the worked example uses 3.50)").

Rather than pick one, the model ships both. `M1_formula()` computes the rule; the model
point carries an `m1_override` column, set to 3.50 on point 1 only, and `M1()` uses the
override when present and the formula otherwise. Point 2 is identical to point 1 except
that it leaves the override blank, so the divergence is exercised by a test rather than
buried. Neither value is "right" — the rule is a standardization and so is the pin.

## Standardizations used

Everything in this list is **[std]**: rate-class factors; the level-period lapse vector
(6%, 5%, 4%, 6% anticipatory) and the PLT run-off (30%, 15%, 10%); the shock-lapse
buckets; the M(1)/M(d) deterioration rule and the 3.50 pin; commission 80% / 5% / 2%;
premium tax 2%; maintenance $30 inflating at 2%; acquisition $300; the mortality
extension beyond age 46; and the interpolated ART premium years. Conversion is switched
**off** by default (`conv_rate = 0`) so the base run reproduces the worked example, which
sets it aside to keep one decrement narrative.

## Tests

`tests/test_term_life_us.py` asserts the full 12-row worked example to the cent, the
in-force column to six decimals, the decrement identity `l(t) − l(t+1) = d + x + c`,
expiry behaviour, the M(1) divergence, and a read → write → re-read round trip.

```bash
python -m pytest tests -q
```
