"""
D0 — Delt datamodul for DES-utvidelsen
======================================
Gjenbruker klassifiseringen og op-binder-semantikken fra primaermodellen
(analyse/scripts/konflikt_total_belastning.py) slik at DES og sweep deler
NOEYAKTIG samme hendelsesgrunnlag. Dette er forutsetningen for at D1
(validerings-broen) kan sammenlignes meningsfullt.

Modulen produserer:
  load_bris()            -> raadata-DataFrame med v3-kategori
  build_events(...)      -> op-binder-event-tabell (t, d, q, kat, skift, helg, c_eff)
  binding_distribution() -> empirisk D-pri1-bindingstidsfordeling (for D3)

Ingen sideeffekter ved import; alt kjoeres via funksjoner.
"""
import pathlib
import numpy as np
import pandas as pd

# === KONFIGURASJON (speiler primaermodellen) ===
PROJECT = pathlib.Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT / "004 data"

KVITTERING_MIN = 3.0          # kvittering etter foerste ressurs fremme (D-pri1)
SKJULT_BIND_MIN = 1.0         # sammenstilte anrop
DABA_FASE1_MIN = 3.0          # kvittering + oppdragsopprettelse + call-out
DABA_FASE2_OFFSET_MIN = 1.5   # 90 sek foer evt. noedtelefon
SEED_DABA = 20260419          # reproduserbar fase-2-sampling
BURST_B = 4.0                 # decay-parameter for burst-fordeling av skjulte

# Bindingstider per scenario (identisk med konflikt_total_belastning.py)
SCENARIOS = {
    "lav":   {"S": 1, "L-aba": 3,   "L-hendelse": 3, "L-ukjent": 1, "F": 0.25, "V": 0.5,
              "daba_p": 0.30, "daba_Y": 3},
    "hoved": {"S": 2, "L-aba": 4.5, "L-hendelse": 5, "L-ukjent": 3, "F": 0.5,  "V": 1,
              "daba_p": 0.50, "daba_Y": 6},
    "hoey":  {"S": 4, "L-aba": 7,   "L-hendelse": 8, "L-ukjent": 5, "F": 1,    "V": 2,
              "daba_p": 0.70, "daba_Y": 10},
}

COLS = [
    "Oppdrag_ID", "110_ID", "Opprinnelig_oppdragstype", "Oppdragstype",
    "Overordnet_oppdragstype", "Kategori_oppdrag", "Adresseobjekt",
    "Postnr", "Poststed", "Kommunenavn", "Kommunenr", "Kommunenr_navn",
    "Fylke", "Ansvarlig_brannvesen", "110_sentral", "Kilde",
    "Time_paa_dognet", "Dato_anrop", "Tid_anrop", "Dato_og_Tid",
    "Ukedagsnr", "Ukedag", "Maanedsnr", "Maaned", "Anrop_aar",
    "Utvarslede_ressurser", "Antall_ressurser_paa_stedet",
    "Oppdrag_opprettet", "Ressurs_varslet", "Rykket_ut",
    "Forste_ressurs_fremme", "Siste_ressurs_ledig",
    "Alarmbehandlingstid", "Utrykningstid", "Responstid", "Forspenningstid",
]


def _klassifiser_kategori(row):
    """V3-regel (jf. konflikt_total_belastning.py:klassifiser_kategori_v2)."""
    if pd.notna(row["Ressurs_varslet"]):
        oot_d = str(row["Opprinnelig_oppdragstype"]).strip() if pd.notna(row["Opprinnelig_oppdragstype"]) else ""
        kilde_d = str(row["Kilde"]).strip() if pd.notna(row["Kilde"]) else ""
        if oot_d.startswith("ABA") and kilde_d == "Alarm":
            return "D-aba"
        return "D-pri1"

    ot = str(row["Oppdragstype"]).strip() if pd.notna(row["Oppdragstype"]) else ""
    oot = str(row["Opprinnelig_oppdragstype"]).strip() if pd.notna(row["Opprinnelig_oppdragstype"]) else ""
    kilde = str(row["Kilde"]).strip() if pd.notna(row["Kilde"]) else ""

    if ot == "Service":
        return "S"
    feilring_typer = {"Nødanrop feilring", "Ikke reell nødmelding",
                      "ECall feil bruk", "ECall teknisk/ukjent", "ECall veihjelp"}
    if ot in feilring_typer:
        return "F"
    if "viderevarslet" in ot.lower() or "viderekoble" in ot.lower():
        return "V"
    if "ppdrag" in ot and "110" in ot:
        if oot == "ABA" and kilde == "Alarm":
            return "L-aba"
        elif oot == "ABA":
            return "L-hendelse"
        elif oot and oot != "nan":
            return "L-hendelse"
        else:
            return "L-ukjent"
    return "L-ukjent"


def load_bris():
    """Last BRIS-testdatasett, klassifiser kategori og beregn D-pri1 bindingstid."""
    files = list(DATA_DIR.glob("110*TESTDATASETT.xlsx"))
    if not files:
        raise FileNotFoundError(f"Fant ingen 110*TESTDATASETT.xlsx i {DATA_DIR}")
    df = pd.read_excel(files[0], engine="openpyxl", skiprows=2)
    df.columns = COLS

    for c in ["Dato_og_Tid", "Ressurs_varslet", "Forste_ressurs_fremme", "Siste_ressurs_ledig"]:
        df[c] = pd.to_datetime(df[c], errors="coerce")

    df["Time"] = pd.to_numeric(df["Time_paa_dognet"], errors="coerce").astype("Int64")
    df["Skift"] = np.where(df["Time"].between(7, 18), "Dag", "Natt")
    df["Ukedagsnr_int"] = pd.to_numeric(df["Ukedagsnr"], errors="coerce").astype("Int64")
    df["Er_helg"] = df["Ukedagsnr_int"].isin([6, 7])
    df["v3_kat"] = df.apply(_klassifiser_kategori, axis=1)

    # D-pri1 bindingstid (databasert): anrop -> foerste ressurs fremme + kvittering
    m = df["v3_kat"] == "D-pri1"
    raa = (df.loc[m, "Forste_ressurs_fremme"] - df.loc[m, "Dato_og_Tid"]).dt.total_seconds() / 60
    raa = raa.where((raa >= 0) & (raa <= 180))           # avvis negative/>180 min
    median_bind = raa.median()
    df.loc[m, "bind_raa"] = raa.fillna(median_bind)
    df.loc[m, "bind_D"] = df.loc[m, "bind_raa"] + KVITTERING_MIN
    df.attrs["dpri1_median_bind"] = float(median_bind)
    return df


def _build_hidden_rows(df, mode="uniform"):
    """Estimer sammenstilte (skjulte) anrop fra sekvensgap i 110_ID.
    Antallet er identisk uansett mode; kun tidspunkt i gapet varierer."""
    df = df.copy()
    df["dato_id"] = df["110_ID"].str.extract(r"B\d+-(\d{6})-")[0]
    df["seq_nr"] = df["110_ID"].str.extract(r"B\d+-\d{6}-(\d+)")[0].astype(float)

    rows = []
    for _, group in df.groupby("dato_id"):
        seqs = set(group["seq_nr"].dropna().astype(int))
        if not seqs:
            continue
        max_s = int(max(seqs))
        missing = sorted(set(range(1, max_s + 1)) - seqs)
        if not missing:
            continue
        sdf = group.sort_values("seq_nr")
        for m in missing:
            before = sdf[(sdf["seq_nr"] < m) & sdf["Dato_og_Tid"].notna()]
            after = sdf[(sdf["seq_nr"] > m) & sdf["Dato_og_Tid"].notna()]
            hb, ha = len(before) > 0, len(after) > 0
            if hb and ha:
                s0 = before.iloc[-1]["seq_nr"]; t0 = before.iloc[-1]["Dato_og_Tid"]
                s1 = after.iloc[0]["seq_nr"];  t1 = after.iloc[0]["Dato_og_Tid"]
                if t1 > t0 and s1 > s0:
                    u = (m - s0) / (s1 - s0)
                    if mode == "collapse":
                        frac = 0.0
                    elif mode == "burst":
                        frac = -np.log(1 - u * (1 - np.exp(-BURST_B))) / BURST_B
                    else:
                        frac = u
                    est = t0 + (t1 - t0) * frac
                else:
                    est = t0
            elif hb:
                est = before.iloc[-1]["Dato_og_Tid"]
            elif ha:
                est = after.iloc[0]["Dato_og_Tid"]
            else:
                continue
            rows.append({"Dato_og_Tid": est, "v3_kat": "skjult"})
    return rows


def _expand_d_aba(df_daba, p, Y, seed=SEED_DABA):
    """Fase 1 (alltid) + Fase 2 (sannsynlighet p, +90 sek) for D-aba."""
    rng = np.random.default_rng(seed)
    fase2 = rng.random(len(df_daba)) < p

    f1 = df_daba[["Dato_og_Tid", "Time", "Skift", "Er_helg"]].copy()
    f1["v3_kat"] = "D-aba-f1"; f1["bind_min"] = DABA_FASE1_MIN; f1["ops_bundet"] = 1

    f2 = df_daba[fase2][["Dato_og_Tid", "Time", "Skift", "Er_helg"]].copy()
    f2["Dato_og_Tid"] = f2["Dato_og_Tid"] + pd.to_timedelta(DABA_FASE2_OFFSET_MIN, unit="m")
    f2["v3_kat"] = "D-aba-f2"; f2["bind_min"] = Y; f2["ops_bundet"] = 1
    return pd.concat([f1, f2], ignore_index=True)


# Kategorier som inngaar i Variant A (beredskap)
VARIANT_A = ["D-pri1", "D-aba", "skjult"]


def build_events(df, scenario_name="hoved", include_only=None, hidden_mode="uniform",
                 daba_seed=SEED_DABA):
    """Bygg op-binder-event-tabell (identisk semantikk med primaermodellen).

    Returnerer DataFrame sortert etter ankomst med kolonner:
      Dato_og_Tid, v3_kat, Time, Skift, Er_helg, bind_min, ops_bundet, c_eff
    include_only=None -> Variant B (alle). Bruk VARIANT_A for primaermodellens variant A.
    """
    scen = SCENARIOS[scenario_name]
    live = df[df["Dato_og_Tid"].notna()].copy()
    parts = []

    d1 = live[live["v3_kat"] == "D-pri1"]
    if len(d1) and (include_only is None or "D-pri1" in include_only):
        e = d1[["Dato_og_Tid", "Time", "Skift", "Er_helg"]].copy()
        e["v3_kat"] = "D-pri1"; e["bind_min"] = df.loc[d1.index, "bind_D"]; e["ops_bundet"] = 2
        parts.append(e)

    da = live[live["v3_kat"] == "D-aba"]
    if len(da) and (include_only is None or "D-aba" in include_only):
        parts.append(_expand_d_aba(da, scen["daba_p"], scen["daba_Y"], daba_seed))

    for kat in ["S", "L-aba", "L-hendelse", "L-ukjent", "F", "V"]:
        if include_only is not None and kat not in include_only:
            continue
        sub = live[live["v3_kat"] == kat]
        if not len(sub):
            continue
        e = sub[["Dato_og_Tid", "Time", "Skift", "Er_helg"]].copy()
        e["v3_kat"] = kat; e["bind_min"] = scen[kat]; e["ops_bundet"] = 1
        parts.append(e)

    if include_only is None or "skjult" in include_only:
        hidden = _build_hidden_rows(df, hidden_mode)
        if hidden:
            h = pd.DataFrame(hidden)
            h["Dato_og_Tid"] = pd.to_datetime(h["Dato_og_Tid"])
            h["Time"] = h["Dato_og_Tid"].dt.hour
            h["Skift"] = np.where(h["Time"].between(7, 18), "Dag", "Natt")
            h["Er_helg"] = h["Dato_og_Tid"].dt.dayofweek >= 5
            h["v3_kat"] = "skjult"; h["bind_min"] = SKJULT_BIND_MIN; h["ops_bundet"] = 1
            parts.append(h[["Dato_og_Tid", "v3_kat", "Time", "Skift", "Er_helg", "bind_min", "ops_bundet"]])

    ev = pd.concat(parts, ignore_index=True)
    dag_hverdag = (ev["Skift"] == "Dag") & (~ev["Er_helg"])
    ev["c_eff"] = np.where(dag_hverdag, 3, 2)
    return ev.sort_values("Dato_og_Tid", kind="mergesort").reset_index(drop=True)


def binding_distribution(df):
    """Empirisk D-pri1-bindingstidsfordeling (inkl. kvittering), for D3-stokastikk."""
    m = df["v3_kat"] == "D-pri1"
    return df.loc[m, "bind_D"].dropna().to_numpy()


if __name__ == "__main__":
    df = load_bris()
    print(f"Totalt rader: {len(df)}")
    print(f"D-pri1 median bindingstid: {df.attrs['dpri1_median_bind']:.1f} min "
          f"(+ {KVITTERING_MIN} kvittering)")
    print("\n=== V3-kategorisering (forventet jf. rapport kap 6.2) ===")
    forventet = {"D-pri1": 4499, "D-aba": 3056, "S": 22542, "L-aba": 3430,
                 "L-hendelse": 4298, "L-ukjent": 16768, "F": 6824, "V": 547}
    kc = df["v3_kat"].value_counts()
    ok = True
    for kat, exp in forventet.items():
        got = int(kc.get(kat, 0))
        flag = "OK" if got == exp else f"AVVIK (forventet {exp})"
        if got != exp:
            ok = False
        print(f"  {kat:12s}: {got:>6}  {flag}")
    print(f"  {'TOTAL':12s}: {len(df):>6}")

    ev_a = build_events(df, "hoved", include_only=VARIANT_A)
    print(f"\nVariant A op-binder-events: {len(ev_a)} "
          f"(forventet ~27 960 jf. kap 6.5.1)")
    print(f"Skjulte anrop: {(ev_a['v3_kat'] == 'skjult').sum()} (forventet 18 901)")
    print("\nKategoritall matcher rapporten:" , "JA" if ok else "NEI - undersoek")
