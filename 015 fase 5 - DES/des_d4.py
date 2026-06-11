"""
D4 — NHPP-ankomstgenerator + burst (ring-flom)
==============================================
Til naa har DES vaert TRACE-drevet (faktiske 2025-tidsstempler). D4 gjoer den
FORDELINGS-drevet: vi estimerer en ikke-homogen Poisson-intensitet lambda(t)
fra Variant A og genererer nye, syntetiske "aar". Det gir to ting:

  1) En generativ kryss-sjekk: reproduserer syntetiske aar trace-resultatet?
     (Hvis ja, er den temporale strukturen godt fanget av lambda(t).)
  2) Burst-scenarioet (S4): ring-flom modelleres som korttids-klynger med
     eksponentielt avtagende intensitet (Gustavsson 2018), som NHPP alene
     ikke fanger fordi Poisson antar uavhengige ankomster.

Intensiteten er stykkevis konstant per (hverdag/helg x time-paa-doegnet).
Kategori trekkes fra den empiriske miksen i samme tidsbin. Service trekkes
som i D3 (D-pri1 bootstrap, oevrige lognormal). c_eff foelger turnus.

FORBEHOLD (jf. DES_oppsett R-DES-1): NHPP forutsetter at ankomstene er
tilnaermet Poisson. Dette er ikke formelt testet (R2/R3 i rapporten), saa
NHPP-aaret er en modell, ikke en validert prediksjon. Burst-caset er nettopp
det eksplisitte bruddet paa Poisson-antagelsen.
"""
import numpy as np
import pandas as pd

import des_data
import des_d2
import des_d3

BASE_SEED = 20260611
MIN_PER_DOEGN = 24 * 60

# Service-forventning per kategori (minutter) for lognormal-trekk i genererte aar
KAT_SERVICE_MEAN = {"D-aba-f1": des_data.DABA_FASE1_MIN, "skjult": des_data.SKJULT_BIND_MIN}
KAT_OPS = {"D-pri1": 2, "D-aba-f1": 1, "D-aba-f2": 1, "skjult": 1}


def estimer_intensitet(ev):
    """Estimer lambda[hverdag/helg][time] og kategorimiks per bin fra Variant A."""
    e = ev.copy()
    e["dato"] = e["Dato_og_Tid"].dt.date
    e["hverdag"] = ~e["Er_helg"]
    e["time"] = e["Dato_og_Tid"].dt.hour

    # antall distinkte datoer per type (for aa faa rate per time-forekomst)
    dager = e.groupby("hverdag")["dato"].nunique()

    lam = {}      # (hverdag, time) -> forventet antall ankomster den timen
    miks = {}     # (hverdag, time) -> {kat: andel}
    for (hv, t), grp in e.groupby(["hverdag", "time"]):
        lam[(hv, t)] = len(grp) / dager[hv]
        vc = grp["v3_kat"].value_counts(normalize=True)
        miks[(hv, t)] = vc.to_dict()
    return lam, miks, e


def _daba_f2_Y(scenario):
    return des_data.SCENARIOS[scenario]["daba_Y"]


def generer_aar(lam, miks, emp_pool, scenario, seed, cv=des_d3.CV_DEFAULT,
                burst=False, burst_pr_dag=0.0, burst_st=8, burst_B=des_data.BURST_B):
    """Generer ett syntetisk aar (52 uker) med NHPP-ankomster + valgfri burst.

    Returnerer event-DataFrame klar for des_d2.kjor_d2.
    """
    rng = np.random.default_rng(seed)
    Y = _daba_f2_Y(scenario)
    service_mean = dict(KAT_SERVICE_MEAN)
    service_mean["D-aba-f2"] = Y

    t0 = pd.Timestamp("2025-01-06")  # en mandag -> ren uke-syklus
    rows_t, rows_kat = [], []

    for dag in range(364):                       # 52 uker
        hverdag = (dag % 7) <= 4
        dag_start = t0 + pd.Timedelta(days=dag)
        for time in range(24):
            mu = lam.get((hverdag, time), 0.0)
            if mu <= 0:
                continue
            n = rng.poisson(mu)
            if n == 0:
                continue
            min_off = rng.uniform(0, 60, size=n) + time * 60
            kats = _trekk_kat(miks.get((hverdag, time), {}), n, rng)
            base = dag_start + pd.to_timedelta(min_off, unit="m")
            rows_t.extend(base)
            rows_kat.extend(kats)

        # burst: ring-flom-klynger paa toppen av NHPP
        if burst and rng.random() < burst_pr_dag:
            b_time = rng.integers(8, 22)          # dagtid-vektet burst-start
            b_start = dag_start + pd.Timedelta(hours=int(b_time)) + pd.Timedelta(minutes=float(rng.uniform(0, 60)))
            k = rng.poisson(burst_st)
            if k > 0:
                # eksponentielt avtagende intensitet -> korte mellomankomsttider
                dt = rng.exponential(1.0 / burst_B, size=k).cumsum()   # minutter
                b_kats = _trekk_kat(miks.get((hverdag, b_time), {}), k, rng)
                rows_t.extend(b_start + pd.to_timedelta(dt, unit="m"))
                rows_kat.extend(b_kats)

    ev = pd.DataFrame({"Dato_og_Tid": pd.to_datetime(rows_t), "v3_kat": rows_kat})
    ev = ev.sort_values("Dato_og_Tid", kind="mergesort").reset_index(drop=True)

    # ops, c_eff, service
    ev["ops_bundet"] = ev["v3_kat"].map(KAT_OPS).astype(int)
    ev["Time"] = ev["Dato_og_Tid"].dt.hour
    hverdag_m = ev["Dato_og_Tid"].dt.weekday <= 4
    dag_m = ev["Time"].between(7, 18)
    ev["c_eff"] = np.where(hverdag_m & dag_m, 3, 2)

    # service: D-pri1 bootstrap fra empirisk; oevrige lognormal om kategorimean
    bind = np.empty(len(ev))
    er_dp = (ev["v3_kat"] == "D-pri1").to_numpy()
    bind[er_dp] = rng.choice(emp_pool, size=int(er_dp.sum()), replace=True)
    for kat, m in service_mean.items():
        mask = (ev["v3_kat"] == kat).to_numpy()
        if mask.any():
            bind[mask] = des_d3._lognormal(m, cv, size=int(mask.sum()), rng=rng)
    ev["bind_min"] = np.maximum(bind, 0.01)
    return ev


def _trekk_kat(mix, n, rng):
    if not mix:
        return ["skjult"] * n
    kats = list(mix.keys())
    p = np.array([mix[k] for k in kats], dtype=float)
    p = p / p.sum()
    return list(rng.choice(kats, size=n, p=p))


def kjor_nhpp(df, scenario="hoved", nrep=200, burst=False, burst_pr_dag=0.0,
              cv=des_d3.CV_DEFAULT, verbose=True):
    """Generer nrep syntetiske aar og aggreger til CI (samme metrikker som D3)."""
    ev_a = des_data.build_events(df, scenario, include_only=des_data.VARIANT_A)
    lam, miks, _ = estimer_intensitet(ev_a)
    emp_pool = des_data.binding_distribution(df)

    rader = []
    for r in range(nrep):
        ev = generer_aar(lam, miks, emp_pool, scenario, seed=BASE_SEED + r,
                         cv=cv, burst=burst, burst_pr_dag=burst_pr_dag)
        res = des_d2.kjor_d2(ev, verbose=False)
        for skift, m in des_d3._metrikker(res).items():
            rader.append({"rep": r, "skift": skift, "n_anrop": len(ev), **m})
        if verbose and (r + 1) % 25 == 0:
            print(f"  ... {r + 1}/{nrep} syntetiske aar")

    long = pd.DataFrame(rader)
    maal = ["Normal", "Brudd", "Svikt", "overloep_pst", "vl_pst",
            "ventet_pst", "dpri1_makkerpar_pst"]
    agg = []
    for skift in ["Dag_hverdag", "Natt_helg"]:
        s = long[long["skift"] == skift]
        for m in maal:
            v = s[m].dropna()
            agg.append({"skift": skift, "maal": m, "mean": v.mean(),
                        "lo": v.quantile(0.025), "hi": v.quantile(0.975)})
    return long, pd.DataFrame(agg)


if __name__ == "__main__":
    import sys
    nrep = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    df = des_data.load_bris()

    # generativ kryss-sjekk (uten burst) + volum-kontroll
    ev_a = des_data.build_events(df, "hoved", include_only=des_data.VARIANT_A)
    lam, miks, _ = estimer_intensitet(ev_a)
    emp = des_data.binding_distribution(df)
    test = generer_aar(lam, miks, emp, "hoved", seed=1)
    print(f"Volumkontroll: syntetisk aar = {len(test)} anrop "
          f"(observert Variant A = {len(ev_a)})")

    print(f"\n[A] NHPP uten burst, {nrep} aar:")
    _, ci0 = kjor_nhpp(df, nrep=nrep, burst=False)
    for skift in ["Dag_hverdag", "Natt_helg"]:
        s = ci0[ci0["skift"] == skift].set_index("maal")
        sv, ov = s.loc["Svikt"], s.loc["overloep_pst"]
        print(f"  {skift:12s}: Svikt {sv['mean']:.1f}% [{sv['lo']:.1f};{sv['hi']:.1f}]  "
              f"overloep {ov['mean']:.2f}% [{ov['lo']:.2f};{ov['hi']:.2f}]")

    ci0.to_csv("d4_nhpp_ci.csv", index=False, encoding="utf-8")
    print("\nLagret: d4_nhpp_ci.csv")
