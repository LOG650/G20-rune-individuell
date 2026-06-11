"""
D2 — Full DES-dynamikk: tidsvarierende turnus, koe, overloep, VL
=================================================================
Bygger paa den verifiserte motoren (D1). Legger til det sweepen IKKE kan:

1) TIDSVARIERENDE KAPASITET. Operatoerpoolen foelger turnus: c_eff = 3 paa
   dag/hverdag (man-fre 07-19), ellers 2. En binding startet paa dagskift
   baeres inn i nattskiftet — fanger overgangssonen kl. 19:00 (RQ1).

2) EKTE RESSURSER, IKKE TELLING. En D-pri1 oensker makkerpar (q=2). Men i
   Brudd/Svikt finnes ikke 2 ledige operatoerer — da haandteres hendelsen
   MEKANISK SOLO (binder 1). DES gjoer dermed solo-driften eksplisitt, ikke
   bare klassifisert. (Sweepen bandt alltid q=2; her bindes det som faktisk
   finnes.)

3) KOE + OVERLOEP. Anrop uten ledig operatoer venter. Ved >30 sek ELLER 10.
   anrop i koe -> overloep til Agder (de facto servicegrense, beredskaps-
   analyse s. 25). Gir overloepsrate — nytt utfallsmaal.

4) VL BETINGET INNTREDEN (besluttet: kun ved Svikt). Naar et beredskapsanrop
   ankommer til 0 ledige operatoerer, traer VL inn og haandterer det (solo),
   forutsatt at VL er ledig. Ellers koe/overloep.

KOEDISIPLIN (besluttet): prioritet D-pri1 > D-aba > skjult, FIFO innen prioritet.

Klassifisering (Normal/Brudd/Svikt) registreres ved ankomst som i rapporten,
slik at fordelingen er sammenlignbar med sweepen. I tillegg registreres
FAKTISK utfall (makkerpar / solo / VL / overloep) og koeventetid.

Service-tid er deterministisk her (fra data); stokastikk kommer i D3.
"""
import numpy as np
import pandas as pd
import simpy

import des_data

# Prioritet per kategori (lavere tall = hoeyere prioritet)
PRIO = {"D-pri1": 0, "D-aba-f1": 1, "D-aba-f2": 1, "D-aba": 1, "skjult": 2}
OVERLOEP_VENT_MIN = 0.5   # 30 sek
KOE_MAKS = 10             # 10. anrop i koe -> overloep


def shift_ceff(ts):
    """c_eff fra turnus: 3 paa man-fre 07-19, ellers 2."""
    hverdag = ts.weekday() <= 4          # 0=man ... 4=fre
    dag = 7 <= ts.hour <= 18
    return 3 if (hverdag and dag) else 2


def shift_label(ts):
    """Skifttype fra KLOKKA (uavhengig av bemanning): Dag_hverdag vs Natt_helg.
    Brukes til rapportering slik at scenarioer som endrer kapasitet (S1/S2)
    ikke flytter anrop mellom skiftkategoriene."""
    hverdag = ts.weekday() <= 4
    dag = 7 <= ts.hour <= 18
    return "Dag_hverdag" if (hverdag and dag) else "Natt_helg"


def _capacity_changes(t_min_index, t0, cap_fn=shift_ceff):
    """Precompute (tid_min, ny_cap) ved hver turnusendring over datasettets spenn."""
    start = t0.floor("h")
    slutt = t0 + pd.to_timedelta(t_min_index.max(), unit="m") + pd.Timedelta(hours=1)
    timer = pd.date_range(start, slutt, freq="h")
    caps = [cap_fn(t) for t in timer]
    changes = []
    forrige = None
    for t, c in zip(timer, caps):
        if c != forrige:
            changes.append(((t - t0).total_seconds() / 60.0, c))
            forrige = c
    return changes


class Pool:
    """Operatoerpool med tidsvarierende kapasitet, prioritetskoe og VL-reserve."""

    def __init__(self, env, koe_maks=KOE_MAKS, overloep_vent=OVERLOEP_VENT_MIN):
        self.env = env
        self.koe_maks = koe_maks
        self.overloep_vent = overloep_vent
        self.cap = 2          # gjeldende c_eff (oppdateres av shift-prosess)
        self.busy = 0         # ordinaere operatoerer bundet av aktive hendelser
        self.vl_busy = False  # VL bundet?
        self.waiters = []     # [(prio, seq, simpy.Event, q)] beredskap i koe
        self._seq = 0
        # statistikk
        self.stats = []       # per anrop: dict med niva, utfall, vent_min, skift-info

    def free(self):
        return max(0, self.cap - self.busy)

    def set_cap(self, c):
        oekte = c > self.cap
        self.cap = c
        if oekte:
            self._dispatch()  # mer kapasitet -> sjekk koe

    def _dispatch(self):
        """Tildel ledige operatoerer til ventende anrop i prioritetsrekkefoelge."""
        self.waiters.sort(key=lambda w: (w[0], w[1]))
        i = 0
        while i < len(self.waiters) and self.free() >= 1:
            prio, seq, ev, q = self.waiters.pop(i)
            self.busy += 1            # solo-tildeling fra koe (1 op)
            if not ev.triggered:
                ev.succeed(value="servet_solo")
        # (q=2 oenske kan ikke garanteres fra koe; solo er den realistiske utfallet)

    def release_regular(self, k=1):
        self.busy -= k
        self._dispatch()

    def release_vl(self):
        self.vl_busy = False
        self._dispatch()


def _shift_proc(env, pool, changes):
    for t_min, c in changes:
        if t_min > env.now:
            yield env.timeout(t_min - env.now)
        pool.set_cap(c)


def _call_proc(env, pool, t_arr, dur, q, kat, skift):
    if t_arr > env.now:
        yield env.timeout(t_arr - env.now)

    free = pool.free()
    niva = "Normal" if free >= 2 else ("Brudd" if free == 1 else "Svikt")
    ce = pool.cap
    rec = {"kat": kat, "niva": niva, "c_eff": ce, "skift": skift,
           "utfall": None, "vent_min": 0.0, "q_oensket": q, "q_bundet": 0}

    if free >= q:
        # nok ledige -> bind oensket antall (makkerpar for D-pri1)
        pool.busy += q
        rec["utfall"] = "makkerpar" if q == 2 else "ordinaer"
        rec["q_bundet"] = q
        yield env.timeout(dur)
        pool.release_regular(q)

    elif free >= 1:
        # Brudd: kun 1 ledig -> solo-haandtering (binder 1, ikke q)
        pool.busy += 1
        rec["utfall"] = "solo" if q == 2 else "ordinaer"
        rec["q_bundet"] = 1
        yield env.timeout(dur)
        pool.release_regular(1)

    else:
        # Svikt: 0 ledige ordinaere
        if not pool.vl_busy:
            # VL trer inn (besluttet: kun ved Svikt) — haandterer solo
            pool.vl_busy = True
            rec["utfall"] = "vl_solo"
            rec["q_bundet"] = 0  # VL, ikke ordinaer op
            yield env.timeout(dur)
            pool.release_vl()
        else:
            # VL opptatt -> koe, vent inntil 30 sek / sjekk 10-i-koe
            if len(pool.waiters) >= pool.koe_maks:
                rec["utfall"] = "overlop_agder"
                rec["vent_min"] = 0.0
            else:
                grant = env.event()
                pool._seq += 1
                entry = (PRIO.get(kat, 3), pool._seq, grant, q)
                pool.waiters.append(entry)
                t_inn = env.now
                res = yield grant | env.timeout(pool.overloep_vent)
                rec["vent_min"] = env.now - t_inn
                if grant in res:
                    # fikk operatoer innen 30 sek (solo fra koe)
                    rec["utfall"] = "ventet_servet"
                    rec["q_bundet"] = 1
                    yield env.timeout(dur)
                    pool.release_regular(1)
                else:
                    # 30 sek utloept -> overloep til Agder
                    if entry in pool.waiters:
                        pool.waiters.remove(entry)
                    rec["utfall"] = "overlop_agder"

    pool.stats.append(rec)


def kjor_d2(events, verbose=True, cap_fn=shift_ceff,
            koe_maks=KOE_MAKS, overloep_vent=OVERLOEP_VENT_MIN):
    """Kjoer full D2-DES over en variant-A event-tabell (beredskap).

    cap_fn(ts)->int overstyrer turnus (scenarioer S1/S2). koe_maks/overloep_vent
    overstyrer overloepsterskelen (S5). Defaults gir baseline (S0).
    """
    ev = events.sort_values("Dato_og_Tid", kind="mergesort").reset_index(drop=True)
    t0 = ev["Dato_og_Tid"].iloc[0]
    t_min = (ev["Dato_og_Tid"] - t0).dt.total_seconds().to_numpy() / 60.0
    dur = ev["bind_min"].to_numpy(dtype=float)
    q = ev["ops_bundet"].to_numpy(dtype=int)
    kat = ev["v3_kat"].to_numpy()
    skift_arr = ev["Dato_og_Tid"].map(shift_label).to_numpy()

    env = simpy.Environment()
    pool = Pool(env, koe_maks=koe_maks, overloep_vent=overloep_vent)
    pool.cap = cap_fn(t0)

    changes = _capacity_changes(pd.Series(t_min), t0, cap_fn)
    env.process(_shift_proc(env, pool, changes))
    for i in range(len(ev)):
        env.process(_call_proc(env, pool, float(t_min[i]), float(dur[i]),
                               int(q[i]), str(kat[i]), str(skift_arr[i])))
    env.run()

    res = pd.DataFrame(pool.stats)
    if verbose:
        _rapport(res)
    return res


def _rapport(res):
    n = len(res)
    print(f"\n=== D2 full DES — Variant A (beredskap), {n} anrop ===")
    print("\nKapasitetsniva ved ankomst (sammenlignbar med sweep):")
    for skift in ["Dag_hverdag", "Natt_helg", "ALLE"]:
        d = res if skift == "ALLE" else res[res["skift"] == skift]
        tot = len(d)
        nm = (d["niva"] == "Normal").mean() * 100
        br = (d["niva"] == "Brudd").mean() * 100
        sv = (d["niva"] == "Svikt").mean() * 100
        print(f"  {skift:12s} (n={tot:>6}): Normal={nm:.1f}%  Brudd={br:.1f}%  Svikt={sv:.1f}%")

    print("\nFaktisk utfall (NYTT — det sweepen ikke viser):")
    for skift in ["Dag_hverdag", "Natt_helg", "ALLE"]:
        d = res if skift == "ALLE" else res[res["skift"] == skift]
        tot = len(d)
        vc = d["utfall"].value_counts()
        ov = vc.get("overlop_agder", 0)
        vl = vc.get("vl_solo", 0)
        solo = vc.get("solo", 0) + vc.get("ventet_servet", 0)
        print(f"  {skift:12s}: overloep Agder={ov} ({ov/tot*100:.2f}%)  "
              f"VL-inntreden={vl} ({vl/tot*100:.2f}%)  "
              f"D-pri1-solo={solo}")

    # D-pri1 spesifikt: hvor ofte mister den makkerpar?
    dp = res[res["kat"] == "D-pri1"]
    if len(dp):
        mk = (dp["utfall"] == "makkerpar").mean() * 100
        print(f"\nD-pri1 (n={len(dp)}): makkerpar oppnaadd {mk:.1f}%, "
              f"solo/VL/overloep {100-mk:.1f}%")
    vent = res[res["vent_min"] > 0]["vent_min"]
    if len(vent):
        print(f"Anrop som ventet i koe: {len(vent)} (median {vent.median()*60:.0f} sek)")


if __name__ == "__main__":
    df = des_data.load_bris()
    ev_a = des_data.build_events(df, "hoved", include_only=des_data.VARIANT_A)
    res = kjor_d2(ev_a)
    res.to_csv("d2_variant_a_resultat.csv", index=False, encoding="utf-8")
    print("\nLagret: d2_variant_a_resultat.csv")
