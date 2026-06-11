"""
D3 — Stokastisk service + replikasjoner -> konfidensintervall
=============================================================
Bygger paa den verifiserte D2-motoren (des_d2.kjor_d2). Trace-drevne
ankomster (faktiske 2025-tidsstempler) holdes faste, men SERVICE-tiden
trekkes stokastisk per replikasjon. Dermed fanges varians som den
deterministiske sweepen og D2-punktkjoeringen ikke viser, og vi faar
konfidensintervall paa alle utfallsmaal.

Service-modell per replikasjon r (seed = BASE_SEED + r):
  - D-pri1: bootstrap-resampling fra den EMPIRISKE bindingstidsfordelingen
    (samme fordeling som rapportens bootstrap, kap 8.3.4). Bevarer den
    hoeyreskjeve halen direkte uten parametrisk antagelse.
  - Oevrige kategorier (D-aba Fase 1/2, skjult): lognormal med forventning lik
    kategoriens bindingstid og variasjonskoeffisient CV (antagelse, jf.
    DES_oppsett R-DES-3). Lognormal bevarer forventningen, saa replikasjons-
    gjennomsnittet ligger ved D2-punktet; CI viser spredningen.
  - D-aba Fase 2-sammensetning (hvilke D-aba som faar oppfoelging) re-trekkes
    ogsaa per replikasjon (variabel daba_seed).

Utfallsmaal (per skifttype, med 95 % persentil-CI over replikasjoner):
  niva Normal/Brudd/Svikt, overloepsrate til Agder, VL-inntreden,
  D-pri1 makkerpar oppnaadd, andel som maatte vente i koe.
"""
import numpy as np
import pandas as pd

import des_data
import des_d2

BASE_SEED = 20260611
CV_DEFAULT = 0.6          # variasjonskoeffisient for ikke-D-pri1 service (antagelse)
NREP_DEFAULT = 400


def _lognormal(mean, cv, size, rng):
    """Lognormal-trekk med gitt forventning og variasjonskoeffisient."""
    mean = np.asarray(mean, dtype=float)
    sigma = np.sqrt(np.log(1.0 + cv * cv))
    mu = np.log(np.maximum(mean, 1e-9)) - 0.5 * sigma * sigma
    return rng.lognormal(mu, sigma, size=size)


def trekk_service(ev, emp_pool, cv, rng):
    """Returner ny bind_min-vektor med stokastisk trukket service per event."""
    kat = ev["v3_kat"].to_numpy()
    bind = ev["bind_min"].to_numpy(dtype=float).copy()
    er_dpri1 = kat == "D-pri1"
    n_dp = int(er_dpri1.sum())
    if n_dp:
        bind[er_dpri1] = rng.choice(emp_pool, size=n_dp, replace=True)  # bootstrap
    andre = ~er_dpri1
    if andre.any():
        bind[andre] = _lognormal(bind[andre], cv, size=int(andre.sum()), rng=rng)
    return np.maximum(bind, 0.01)


def _metrikker(res):
    """Hent ut alle utfallsmaal fra en D2-kjoering, per skifttype."""
    out = {}
    for skift in ["Dag_hverdag", "Natt_helg"]:
        d = res[res["skift"] == skift]
        tot = len(d)
        if tot == 0:
            continue
        dp = d[d["kat"] == "D-pri1"]
        out[skift] = {
            "Normal": (d["niva"] == "Normal").mean() * 100,
            "Brudd": (d["niva"] == "Brudd").mean() * 100,
            "Svikt": (d["niva"] == "Svikt").mean() * 100,
            "overloep_pst": (d["utfall"] == "overlop_agder").mean() * 100,
            "vl_pst": (d["utfall"] == "vl_solo").mean() * 100,
            "ventet_pst": (d["vent_min"] > 0).mean() * 100,
            "dpri1_makkerpar_pst": (dp["utfall"] == "makkerpar").mean() * 100 if len(dp) else np.nan,
        }
    return out


def kjor_replikasjoner(df, scenario="hoved", nrep=NREP_DEFAULT, cv=CV_DEFAULT,
                       include_only=None, kjor_fn=None, verbose=True):
    """Kjoer nrep replikasjoner med stokastisk service. Returnerer (df_long, oppsummering)."""
    include_only = des_data.VARIANT_A if include_only is None else include_only
    emp_pool = des_data.binding_distribution(df)
    kjor_fn = des_d2.kjor_d2 if kjor_fn is None else kjor_fn

    # Bygg event-grunnlaget EN gang (ankomster + D-aba Fase 2-sammensetning er faste);
    # kun service-tiden trekkes paa nytt per replikasjon. Det er service-variansen
    # som er den dominerende stokastiske kilden, jf. rapportens bootstrap (kap 8.3.4).
    ev_base = des_data.build_events(df, scenario, include_only=include_only)

    rader = []
    for r in range(nrep):
        rng = np.random.default_rng(BASE_SEED + r)
        ev = ev_base.copy()
        ev["bind_min"] = trekk_service(ev, emp_pool, cv, rng)
        res = kjor_fn(ev, verbose=False)
        for skift, m in _metrikker(res).items():
            rader.append({"rep": r, "skift": skift, **m})
        if verbose and (r + 1) % 50 == 0:
            print(f"  ... {r + 1}/{nrep} replikasjoner")

    long = pd.DataFrame(rader)
    maal = ["Normal", "Brudd", "Svikt", "overloep_pst", "vl_pst",
            "ventet_pst", "dpri1_makkerpar_pst"]
    agg = []
    for skift in ["Dag_hverdag", "Natt_helg"]:
        s = long[long["skift"] == skift]
        for m in maal:
            v = s[m].dropna()
            agg.append({"skift": skift, "maal": m,
                        "mean": v.mean(), "lo": v.quantile(0.025),
                        "hi": v.quantile(0.975), "sd": v.std()})
    oppsummering = pd.DataFrame(agg)
    return long, oppsummering


def _skriv(oppsummering, nrep, cv):
    print(f"\n=== D3: stokastisk service, {nrep} replikasjoner (CV={cv}) ===")
    print("Variant A (beredskap). 95 % persentil-CI over replikasjoner.\n")
    for skift in ["Dag_hverdag", "Natt_helg"]:
        print(f"  {skift}:")
        s = oppsummering[oppsummering["skift"] == skift].set_index("maal")
        for m in ["Normal", "Brudd", "Svikt", "overloep_pst", "vl_pst", "dpri1_makkerpar_pst"]:
            row = s.loc[m]
            print(f"    {m:22s} {row['mean']:5.1f} %   CI [{row['lo']:.1f}; {row['hi']:.1f}]")


if __name__ == "__main__":
    import sys
    nrep = int(sys.argv[1]) if len(sys.argv) > 1 else NREP_DEFAULT
    df = des_data.load_bris()
    long, oppsummering = kjor_replikasjoner(df, nrep=nrep)
    _skriv(oppsummering, nrep, CV_DEFAULT)
    oppsummering.to_csv("d3_ci_variant_a.csv", index=False, encoding="utf-8")
    long.to_csv("d3_replikasjoner_long.csv", index=False, encoding="utf-8")
    print("\nLagret: d3_ci_variant_a.csv, d3_replikasjoner_long.csv")
