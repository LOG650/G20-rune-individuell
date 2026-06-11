"""
D1 — SimPy DES-motor (bridge-modus) + kapasitetsklassifisering
==============================================================
Bridge-modus reproduserer primaermodellens sweep: hvert op-binder-event
klassifiseres Normal/Brudd/Svikt ved ankomst basert paa antall aktive
op-binder, sammenlignet med eventets c_eff. Ingen blokkering/koe ennaa
(det kommer i D2). SimPy fungerer som klokke; for aa garantere NOEYAKTIG
samme semantikk som sweepen (samtidige ankomster binder ikke hverandre)
behandles alle events med identisk tidsstempel som EN gruppe:
  1) utloep alle aktive binder med slutt <= t   (sweep: behold slutt > t)
  2) base = sum av aktive ops bundet
  3) alle gruppemedlemmer klassifiseres mot base
  4) alle gruppemedlemmer legger til sine binder

Dette gir et eksakt sammenligningsgrunnlag for valideringen i des_validate.py
og en struktur som D2 utvider med ekte SimPy-ressurser, koe og overloep.
"""
import numpy as np
import pandas as pd
import simpy


def klassifiser(ledige):
    """Normal: >=2 ledige (makkerpar mulig). Brudd: 1. Svikt: <=0."""
    if ledige >= 2:
        return "Normal"
    if ledige == 1:
        return "Brudd"
    return "Svikt"


def run_bridge(events, time_unit_min=1.0):
    """Kjoer DES i bridge-modus over en op-binder-event-tabell.

    events: DataFrame med Dato_og_Tid, bind_min, ops_bundet, c_eff (fra des_data).
    Returnerer kopi av events med kolonnene n_aktive og kapasitet.

    SimPy driver klokken i minutter fra foerste ankomst. Aktive binder spores
    i en liste; samtidige ankomster grupperes for eksakt sweep-semantikk.
    """
    ev = events.sort_values("Dato_og_Tid", kind="mergesort").reset_index(drop=True)
    # Tidsakse i heltalls-nanosekunder (identisk med pandas datetime64[ns]-semantikk),
    # slik at utloep-sammenligningen (slutt > ankomst) blir eksakt som referanse-sweepen.
    arr_ns = ev["Dato_og_Tid"].to_numpy().astype("datetime64[ns]").astype("int64")
    slutt_ts = ev["Dato_og_Tid"] + pd.to_timedelta(ev["bind_min"], unit="m")
    end_ns = slutt_ts.to_numpy().astype("datetime64[ns]").astype("int64")
    t0_ns = int(arr_ns[0])
    q = ev["ops_bundet"].to_numpy(dtype=int)
    c_eff = ev["c_eff"].to_numpy(dtype=int)
    n = len(ev)

    n_aktive = np.zeros(n, dtype=int)
    kapasitet = np.empty(n, dtype=object)

    env = simpy.Environment()  # klokke i minutter fra t0 (kun for tidssteg)
    active = []  # liste av (slutt_ns, ops)

    def feeder():
        i = 0
        while i < n:
            t_i = int(arr_ns[i])
            # advanser DES-klokken til neste ankomstgruppe (minutter fra t0)
            yield env.timeout((t_i - t0_ns) / 6e10 - env.now)
            # gruppe av samtidige ankomster (eksakt ns-likhet)
            j = i
            while j < n and int(arr_ns[j]) == t_i:
                j += 1
            # 1) utloep binder med slutt <= t_i (behold slutt > t_i) — heltalls-ns
            active[:] = [(s, o) for s, o in active if s > t_i]
            # 2) base
            base = sum(o for _, o in active)
            # 3) klassifiser hele gruppen mot base
            for k in range(i, j):
                n_aktive[k] = base
                kapasitet[k] = klassifiser(c_eff[k] - base)
            # 4) legg til gruppens binder
            for k in range(i, j):
                active.append((int(end_ns[k]), q[k]))
            i = j

    env.process(feeder())
    env.run()

    out = ev.copy()
    out["n_aktive"] = n_aktive
    out["kapasitet"] = kapasitet
    return out


def fordeling(df, c_eff=None):
    """Andel Normal/Brudd/Svikt (%) for hele df eller et c_eff-filter."""
    d = df if c_eff is None else df[df["c_eff"] == c_eff]
    total = len(d)
    return {niva: round((d["kapasitet"] == niva).mean() * 100, 1)
            for niva in ["Normal", "Brudd", "Svikt"]}, total


if __name__ == "__main__":
    import des_data
    df = des_data.load_bris()
    ev_a = des_data.build_events(df, "hoved", include_only=des_data.VARIANT_A)
    res = run_bridge(ev_a)
    print("SimPy bridge — Variant A (beredskap), hoved-scenario:")
    for ce, lab in [(None, "Alle"), (3, "Dag hverdag (c=3)"), (2, "Natt/helg (c=2)")]:
        f, tot = fordeling(res, ce)
        print(f"  {lab:20s} (n={tot:>6}): Normal={f['Normal']}%  "
              f"Brudd={f['Brudd']}%  Svikt={f['Svikt']}%")
