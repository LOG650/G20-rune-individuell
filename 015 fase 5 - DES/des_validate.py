"""
D1 — Validering: SimPy-bro == primaermodellens sweep
====================================================
Kjorer (a) en referanse-sweep med NOEYAKTIG samme algoritme som
analyse/scripts/konflikt_total_belastning.py:kjor_sweep, og (b) SimPy-broen
i des_core.run_bridge, paa identisk event-grunnlag. Sammenligner rad-for-rad.

Suksesskriterium: 100 % identisk kapasitetsklassifisering for hver event,
og dermed identiske Normal/Brudd/Svikt-andeler. Da er DES-motoren en
verifisert utvidelse av primaermodellen, ikke en ny/ukontrollert modell.
"""
import numpy as np
import pandas as pd

import des_data
import des_core


def referanse_sweep(events):
    """Eksakt kopi av primaermodellens sweep (op-binder-semantikk)."""
    ev = events.sort_values("Dato_og_Tid", kind="mergesort").reset_index(drop=True)
    ev["slutt_ts"] = ev["Dato_og_Tid"] + pd.to_timedelta(ev["bind_min"], unit="m")

    n = len(ev)
    ankomst = ev["Dato_og_Tid"].values
    slutt = ev["slutt_ts"].values
    ops = ev["ops_bundet"].values.astype(int)
    c_eff_arr = ev["c_eff"].values

    n_aktive = np.zeros(n, dtype=int)
    active = []
    i = 0
    while i < n:
        t_i = ankomst[i]
        j = i
        while j < n and ankomst[j] == t_i:
            j += 1
        active = [(s, o) for s, o in active if s > t_i]
        base = sum(o for _, o in active)
        for k in range(i, j):
            n_aktive[k] = base
        for k in range(i, j):
            active.append((slutt[k], ops[k]))
        i = j

    ev["n_aktive"] = n_aktive
    ev["kapasitet"] = [des_core.klassifiser(c - na) for na, c in zip(n_aktive, c_eff_arr)]
    return ev


def sammenlign(label, events):
    ref = referanse_sweep(events)
    sim = des_core.run_bridge(events)
    # juster begge til samme rekkefoelge (sortert paa ankomst, stabilt)
    ref = ref.sort_values("Dato_og_Tid", kind="mergesort").reset_index(drop=True)
    sim = sim.sort_values("Dato_og_Tid", kind="mergesort").reset_index(drop=True)

    lik_kap = (ref["kapasitet"].values == sim["kapasitet"].values)
    lik_na = (ref["n_aktive"].values == sim["n_aktive"].values)
    n = len(ref)
    n_kap_avvik = int((~lik_kap).sum())
    n_na_avvik = int((~lik_na).sum())

    print(f"\n=== {label} (n={n}) ===")
    print(f"  n_aktive identisk : {n - n_na_avvik}/{n}  (avvik: {n_na_avvik})")
    print(f"  kapasitet identisk: {n - n_kap_avvik}/{n}  (avvik: {n_kap_avvik})")
    for ce, lab in [(None, "Alle"), (3, "Dag hverdag"), (2, "Natt/helg")]:
        fr, _ = des_core.fordeling(ref, ce)
        fs, _ = des_core.fordeling(sim, ce)
        match = "OK" if fr == fs else "AVVIK"
        print(f"  {lab:12s}: sweep N/B/S={fr['Normal']}/{fr['Brudd']}/{fr['Svikt']}  "
              f"sim={fs['Normal']}/{fs['Brudd']}/{fs['Svikt']}  [{match}]")
    return n_kap_avvik == 0


if __name__ == "__main__":
    df = des_data.load_bris()

    alle_ok = True
    # Variant A (primaermodellens hovedmetrikk)
    ev_a = des_data.build_events(df, "hoved", include_only=des_data.VARIANT_A)
    alle_ok &= sammenlign("Variant A (beredskap), hoved", ev_a)

    # Variant B (total belastning) — bredere test av motoren
    ev_b = des_data.build_events(df, "hoved", include_only=None)
    alle_ok &= sammenlign("Variant B (total), hoved", ev_b)

    print("\n" + "=" * 60)
    print("VALIDERINGSRESULTAT:", "BRO BEKREFTET (100% identisk)" if alle_ok
          else "AVVIK FUNNET — undersoek")
    print("=" * 60)
