"""
D5 — Scenarioanalyse S0 til S5 paa den verifiserte DES-motoren
=============================================================
Hvert scenario kjoeres med stokastisk service (D3-rammeverk) eller som
syntetiske aar (D4/NHPP), med 95 % persentil-CI over replikasjoner.

  S0  Baseline (faktisk bemanning)             -> trace, Variant A
  S1  +1 operatoer natt/helg (c_eff 2->3)       -> cap_fn = 3 overalt
  S2  +1 operatoer dag hverdag (c_eff 3->4)      -> cap_fn dag=4
  S3  Funksjonsdifferensiering (S skilt ut)      -> Variant B med vs uten S
  S4  Burst / ring-flom                          -> NHPP med vs uten burst-klynger
  S5  Alternativ overloepsterskel                -> 60 sek / 15-i-koe

Alle resultater samles i d5_scenarioer_ci.csv (scenario x skift x maal).
"""
import pandas as pd

import des_data
import des_d2
import des_d3
import des_d4


def cap_alle3(ts):
    """S1: +1 paa natt/helg -> c_eff = 3 paa alle skift."""
    return 3


def cap_pluss1_dag(ts):
    """S2: +1 paa dag hverdag -> c_eff = 4 der, 2 ellers."""
    return 4 if (ts.weekday() <= 4 and 7 <= ts.hour <= 18) else 2


def _kjor_fn(**kw):
    def f(ev, verbose=False):
        return des_d2.kjor_d2(ev, verbose=False, **kw)
    return f


def _merk(ci, scenario, kilde):
    ci = ci.copy()
    ci["scenario"] = scenario
    ci["kilde"] = kilde
    return ci


VARIANT_B_UTEN_S = ["D-pri1", "D-aba", "L-aba", "L-hendelse", "L-ukjent", "F", "V", "skjult"]


def main(nrep_trace=120, nrep_b=120, nyear=60, burst_pr_dag=0.5):
    df = des_data.load_bris()
    alle = []

    trace_scen = [
        ("S0_baseline", {}),
        ("S1_pluss1_natthelg", dict(cap_fn=cap_alle3)),
        ("S2_pluss1_dag", dict(cap_fn=cap_pluss1_dag)),
        ("S5a_overlop_60s", dict(overloep_vent=1.0)),
        ("S5b_overlop_ko15", dict(koe_maks=15)),
    ]
    for navn, kw in trace_scen:
        print(f"[{navn}] {nrep_trace} replikasjoner ...", flush=True)
        _, ci = des_d3.kjor_replikasjoner(df, nrep=nrep_trace, kjor_fn=_kjor_fn(**kw), verbose=False)
        alle.append(_merk(ci, navn, "trace"))

    print(f"[S3] Variant B med/uten S, {nrep_b} replikasjoner ...", flush=True)
    _, ci_b = des_d3.kjor_replikasjoner(df, nrep=nrep_b, include_only=None, verbose=False)
    alle.append(_merk(ci_b, "S3_variantB_medS", "trace"))
    _, ci_bs = des_d3.kjor_replikasjoner(df, nrep=nrep_b, include_only=VARIANT_B_UTEN_S, verbose=False)
    alle.append(_merk(ci_bs, "S3_variantB_utenS", "trace"))

    print(f"[S4] NHPP {nyear} aar, baseline + burst ...", flush=True)
    _, ci_nh = des_d4.kjor_nhpp(df, nrep=nyear, burst=False, verbose=False)
    alle.append(_merk(ci_nh, "S4_nhpp_baseline", "nhpp"))
    _, ci_bu = des_d4.kjor_nhpp(df, nrep=nyear, burst=True, burst_pr_dag=burst_pr_dag, verbose=False)
    alle.append(_merk(ci_bu, "S4_nhpp_burst", "nhpp"))

    res = pd.concat(alle, ignore_index=True)
    res.to_csv("d5_scenarioer_ci.csv", index=False, encoding="utf-8")

    print("\n=== D5 oppsummering: natt/helg (Svikt og overloep) ===")
    for navn in res["scenario"].unique():
        s = res[(res["scenario"] == navn) & (res["skift"] == "Natt_helg")].set_index("maal")
        sv, ov = s.loc["Svikt"], s.loc["overloep_pst"]
        print(f"  {navn:22s} Svikt {sv['mean']:5.1f}% [{sv['lo']:4.1f};{sv['hi']:4.1f}]   "
              f"overloep {ov['mean']:5.2f}%")
    print("\nLagret: d5_scenarioer_ci.csv")


if __name__ == "__main__":
    main()
