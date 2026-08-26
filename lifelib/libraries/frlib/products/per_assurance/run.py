"""Run the PER_FR_A reference model and print its state and cash flow statements.

    python products/per_assurance/run.py            # the notes' worked example
    python products/per_assurance/run.py 6          # the annuity that is not commuted
    python products/per_assurance/run.py 10         # the cell whose death floor bites

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "PER_FR_A")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
n = proj.proj_len()
print("model point {}: {} - {} {}, horizon {} ({} plan years), {} / {}".format(
    point_id, proj.policy_id(), proj.sex(), proj.age_init(),
    proj.retirement_age(), n, proj.compartment(), proj.allocation_profile()))
print("versement {:,.2f} p.a. gross, {:,.2f} net of the {:.2%} loading; "
      "carried in: euro {:,.2f}  UC {:,.2f}  floor {:,.2f}".format(
          proj.premium_init(), proj.prem_to_av_pp(1),
          model.Projection.load_rate, proj.av_euro_init(), proj.av_uc_init(),
          proj.death_floor_init()))
print("euro {:.2%} gross less {:.2%} charge; UC {:.2%} gross less {:.2%} charge; "
      "arbitrage {:.2%} of the amount switched".format(
          model.Projection.return_euro, model.Projection.charge_euro,
          model.Projection.return_uc, model.Projection.charge_uc,
          model.Projection.arb_rate))
print("exit: {} with annuity share {:.0%}; mortality basis {}; "
      "death floor {} to age {}".format(
          proj.exit_form(), proj.annuity_share(), proj.mort_basis(),
          "on" if proj.death_floor_flag() else "off",
          model.Projection.floor_cease_age))
print()

print("Glide path and supports (per policy; pols_if_eoy is the notes' l(t)):")
state = proj.result_state()
print(state.head(4).round(
    {c: (4 if c == "alloc_euro" else 6 if c == "pols_if_eoy" else 2)
     for c in state.columns}).to_string())
print("...")
print(state.tail(2).round(
    {c: (4 if c == "alloc_euro" else 6 if c == "pols_if_eoy" else 2)
     for c in state.columns}).to_string())
print()

print("Settlement at the horizon (per policy):")
settle = proj.result_settlement()
for label in settle.index:
    print("  {:24s} {:>14,.4f}".format(label, settle[label]))
print("  commutation test: {:,.2f} a month against {:,.2f} -> {}".format(
    settle["rente_net_mth"], model.Projection.commute_threshold_mth,
    "commute" if proj.is_commuted() else "pay the rente"))
print()

print("Cash flows (pols_if is the count each row OPENS with, and its own weight):")
cf = proj.result_cf()
print(cf.head(3).round(
    {c: (6 if c == "pols_if" else 2) for c in cf.columns}).to_string())
print("...")
print(cf.tail(1).round(
    {c: (6 if c == "pols_if" else 2) for c in cf.columns}).to_string())
print()
print("undiscounted totals: claims {:,.2f}  annuity conversion {:,.2f}  "
      "expenses {:,.2f}  versements {:,.2f}  net_cf {:,.2f}".format(
          cf[["claims_death", "claims_early_release", "claims_transfer",
              "claims_maturity"]].sum().sum(),
          cf["annuity_conversion"].sum(), cf["expenses"].sum(),
          cf["premiums"].sum(), cf["net_cf"].sum()))
print()
print("Checks: policies {}  account value {}  floor identity {}  "
      "euro share minimum {}".format(
          proj.check_pols_roll_fwd(), proj.check_av_roll_fwd(),
          proj.check_floor_identity(), proj.check_euro_share_min()))
print("        glide path closes {}  commutation identity {}  horizon {}".format(
    proj.check_glide_path_closes(), proj.check_commutation_identity(),
    proj.check_horizon()))

model.close()
