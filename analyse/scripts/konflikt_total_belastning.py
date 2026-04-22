"""
V3: Total operativ belastning — utvidet ankomstkonfliktmodell
=============================================================
Oppdatert 2026-04-19: Op-binder-semantikk.

Tidligere modell telte hver hendelse som 1 makkerpar-slot. Dette ga feil
bilde for hendelser som ikke faktisk binder makkerparet (primaert ABA->D:
lav-pri utrykning der én operator haandterer serielt uten makkerpar-krav,
jf. operatør-intervju 2026-04-19).

Ny semantikk: Hver hendelse genererer en eller to op-binder-events med
(bindingstid, ops_bundet). Sweep akkumulerer summen av ops_bundet for
aktive events. Klassifisering:
  Normal:  ledige >= 2  (makkerpar mulig for ny hendelse)
  Brudd:   ledige == 1  (kun solo-haandtering mulig)
  Svikt:   ledige <= 0

Klassifisering basert paa Oppdragstype + Opprinnelig oppdragstype + Kilde:
  D-pri1     Utrykning ikke-ABA (byggningsbrann, trafikk, etc.)
             -> 2 ops bundet i full bindingstid (makkerpar, median 13 min)
  D-aba      Utrykning utloest av ABA (Opprinnelig = ABA, Kilde = Alarm)
             -> Fase 1: 1 op, 3 min (kvittering + oppdrag + call-out)
             -> Fase 2 (andel p): 1 op, Y min (noedtelefon + panel-veiledning)
             -> Fase 2-offset: 90 sek etter ankomst
  S          Service/overfoeringstest                        -> 1 op, 2 min
  L-aba      ABA loest av 110, Kilde=Alarm                   -> 1 op, 6 min
  L-hendelse Reell hendelse loest av 110 (inkl. ABA m/Samtale) -> 1 op, 5 min
  L-ukjent   Loest av 110, ukjent type                       -> 1 op, 3 min
  F          Feilringing / ikke-noedmelding / eCall feil     -> 1 op, 0.5 min
  V          Viderevarsling / viderekobling                  -> 1 op, 1 min
  skjult     Sammenstilte anrop (sekvensgap-metode)          -> 1 op, 1 min

Tre scenarioer for sensitivitetsanalyse (lav/hoved/hoey).
Eksisterende kode (konflikt_v4_korrigert.py) endres IKKE.
"""
import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# === KONFIGURASJON ===
PROJECT = pathlib.Path(r"C:\Users\runeg\OneDrive\Documents\Skole utdanning"
                       r"\Logistikk studie\LOG650 LOGISTIKK OG KI"
                       r"\G20-rune-individuell")
DATA_DIR = PROJECT / "004 data"
FIG_DIR = PROJECT / "analyse" / "figurer"
FIG_DIR.mkdir(parents=True, exist_ok=True)

KVITTERING_MIN = 3.0  # kvittering etter foerste ressurs fremme (D-pri1)
SKJULT_BIND_MIN = 1.0  # sammenstilte anrop

# D-aba-parametre (operatør-informert, 2026-04-19)
DABA_FASE1_MIN = 3.0          # kvittering + oppdragsopprettelse + call-out
DABA_FASE2_OFFSET_MIN = 1.5   # 90 sek foersinkelse foer evt. noedtelefon

SEED_DABA = 20260419  # reproduserbar fase-2-sampling

# Bindingstider og D-aba-parametre per scenario
# L-aba: hoved 4.5 min fra LABA-dybdeanalyse n=100 (mean 4.53, 95% CI [3.74; 5.43])
#        Erstatter tidligere n=30-anslag (mean 5.88, CI [3.70; 8.56])
# D-aba fase 2: p = andel D-aba med noedtelefon-oppfoelging; Y = bindingstid
# L-aba scenario-spenn (n=100): 3 min (CI-nedre) til 7 min (over CI-oevre)
SCENARIOS = {
    "lav":   {"S": 1, "L-aba": 3,   "L-hendelse": 3, "L-ukjent": 1, "F": 0.25, "V": 0.5,
              "daba_p": 0.30, "daba_Y": 3},
    "hoved": {"S": 2, "L-aba": 4.5, "L-hendelse": 5, "L-ukjent": 3, "F": 0.5,  "V": 1,
              "daba_p": 0.50, "daba_Y": 6},
    "hoey":  {"S": 4, "L-aba": 7,   "L-hendelse": 8, "L-ukjent": 5, "F": 1,    "V": 2,
              "daba_p": 0.70, "daba_Y": 10},
}

sns.set_style("whitegrid")
plt.rcParams.update({"figure.dpi": 150, "font.size": 10})

# === 1. LAST DATA ===
files = list(DATA_DIR.glob("110*TESTDATASETT.xlsx"))
df = pd.read_excel(files[0], engine="openpyxl", skiprows=2)

cols = [
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
df.columns = cols

for c in ["Dato_og_Tid", "Ressurs_varslet", "Forste_ressurs_fremme", "Siste_ressurs_ledig"]:
    df[c] = pd.to_datetime(df[c], errors="coerce")

df["Time"] = pd.to_numeric(df["Time_paa_dognet"], errors="coerce").astype("Int64")
df["Skift"] = np.where(df["Time"].between(7, 18), "Dag", "Natt")
df["Ukedagsnr_int"] = pd.to_numeric(df["Ukedagsnr"], errors="coerce").astype("Int64")
df["Er_helg"] = df["Ukedagsnr_int"].isin([6, 7])

print(f"Totalt rader: {len(df)}")

# === 2. KLASSIFISER ALLE HENDELSER ===
def klassifiser_kategori(row):
    """Tildel V3-kategori basert paa Oppdragstype og Opprinnelig oppdragstype."""
    # D: har ressursvarsling
    if pd.notna(row["Ressurs_varslet"]):
        return "D"

    ot = str(row["Oppdragstype"]) if pd.notna(row["Oppdragstype"]) else ""
    oot = str(row["Opprinnelig_oppdragstype"]) if pd.notna(row["Opprinnelig_oppdragstype"]) else ""

    # S: Service
    if ot == "Service":
        return "S"

    # F: Feilringing og lignende
    if ot in ("Noedanrop feilring", "Ikke reell noedmelding",
              "ECall feil bruk", "ECall teknisk/ukjent", "ECall veihjelp"):
        return "F"

    # V: Viderevarsling / viderekobling
    if "viderevarslet" in ot.lower() or "viderekoble" in ot.lower():
        return "V"

    # L-varianter: Oppdrag loest av 110
    if ot == "Oppdrag loest av 110" or ot.startswith("Oppdrag l"):
        if oot == "ABA":
            return "L-aba"
        elif oot and oot != "nan":
            return "L-hendelse"
        else:
            return "L-ukjent"

    # Rest -> L-ukjent
    return "L-ukjent"

# Hent faktiske verdier for matching
print("\nUnike Oppdragstype-verdier (sjekker encoding):")
for v in sorted(df["Oppdragstype"].dropna().unique())[:10]:
    print(f"  '{v}'")

# Bruk faktiske strengverdier fra dataen
def klassifiser_kategori_v2(row):
    """V3-regel (oppdatert 2026-04-19):
    - D-aba: Ressurs_varslet finnes, Opprinnelig starter med 'ABA', Kilde=Alarm
    - D-pri1: Andre D-hendelser (byggningsbrann, trafikk, etc.)
    - L-aba krever Kilde=Alarm. ABA med Samtale/blank kilde -> L-hendelse."""
    # D-hendelser: har ressursvarsling
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

    if "ppdrag" in ot and "110" in ot:  # "Oppdrag løst av 110"
        if oot == "ABA" and kilde == "Alarm":
            return "L-aba"
        elif oot == "ABA":
            # ABA uten Kilde=Alarm (Samtale eller blank) -> L-hendelse
            return "L-hendelse"
        elif oot and oot != "nan":
            return "L-hendelse"
        else:
            return "L-ukjent"

    return "L-ukjent"

df["v3_kat"] = df.apply(klassifiser_kategori_v2, axis=1)

print("\n=== V3-kategorisering ===")
kat_counts = df["v3_kat"].value_counts()
for kat in ["D-pri1", "D-aba", "S", "L-aba", "L-hendelse", "L-ukjent", "F", "V"]:
    n = kat_counts.get(kat, 0)
    print(f"  {kat:12s}: {n:>6} ({n/len(df)*100:>5.1f}%)")
print(f"  {'TOTAL':12s}: {len(df):>6}")

# === 3. IDENTIFISER SKJULTE ANROP (fra v4) ===
df["dato_id"] = df["110_ID"].str.extract(r"B\d+-(\d{6})-")[0]
df["seq_nr"] = df["110_ID"].str.extract(r"B\d+-\d{6}-(\d+)")[0].astype(float)

hidden_rows = []
for dato, group in df.groupby("dato_id"):
    seqs = set(group["seq_nr"].dropna().astype(int))
    if len(seqs) == 0:
        continue
    max_s = int(max(seqs))
    missing = sorted(set(range(1, max_s + 1)) - seqs)
    if not missing:
        continue
    sorted_df = group.sort_values("seq_nr")
    for m in missing:
        before = sorted_df[sorted_df["seq_nr"] < m]
        after = sorted_df[sorted_df["seq_nr"] > m]
        if len(before) > 0 and pd.notna(before.iloc[-1]["Dato_og_Tid"]):
            est_tid = before.iloc[-1]["Dato_og_Tid"]
        elif len(after) > 0 and pd.notna(after.iloc[0]["Dato_og_Tid"]):
            est_tid = after.iloc[0]["Dato_og_Tid"]
        else:
            continue
        hidden_rows.append({
            "Dato_og_Tid": est_tid,
            "v3_kat": "skjult",
            "kilde": "skjult_sammenstilt",
        })

print(f"\nSkjulte/sammenstilte anrop: {len(hidden_rows)}")

# === 4. BEREGN BINDINGSTID FOR D-PRI1 (databasert) ===
# D-pri1 binder makkerparet i full bindingstid (Dato_og_Tid -> Forste_ressurs_fremme + kvittering).
# D-aba behandles separat i bygg_events (Fase 1 + valgfri Fase 2).
d_pri1_mask = df["v3_kat"] == "D-pri1"
df.loc[d_pri1_mask, "bind_raa"] = (
    (df.loc[d_pri1_mask, "Forste_ressurs_fremme"] - df.loc[d_pri1_mask, "Dato_og_Tid"]).dt.total_seconds() / 60
)
df.loc[df["bind_raa"] < 0, "bind_raa"] = np.nan
df.loc[df["bind_raa"] > 180, "bind_raa"] = np.nan
median_bind_d = df.loc[d_pri1_mask & df["bind_raa"].notna(), "bind_raa"].median()
df.loc[d_pri1_mask & df["bind_raa"].isna(), "bind_raa"] = median_bind_d
df.loc[d_pri1_mask, "bind_D"] = df.loc[d_pri1_mask, "bind_raa"] + KVITTERING_MIN

print(f"D-pri1 median bindingstid: {median_bind_d:.1f} min (+ {KVITTERING_MIN} kvittering)")

# === 5. SWEEP-FUNKSJON (op-binder-semantikk) ===
def kjor_sweep(events_df, label=""):
    """Ankomstkonflikt-sweep. Hver event har (bind_min, ops_bundet).
    n_aktive_ops akkumuleres ved hver ankomst som summen av ops_bundet
    for events med slutt_ts > t_i."""
    events = events_df.sort_values("Dato_og_Tid").reset_index(drop=True)
    events["slutt_ts"] = events["Dato_og_Tid"] + pd.to_timedelta(events["bind_min"], unit="m")

    n = len(events)
    ankomst = events["Dato_og_Tid"].values
    slutt = events["slutt_ts"].values
    ops = events["ops_bundet"].values.astype(int)
    c_eff_arr = events["c_eff"].values

    n_aktive_ops = np.zeros(n, dtype=int)
    active_set = []  # liste av (slutt_ts, ops_bundet)
    for i in range(n):
        t_i = ankomst[i]
        active_set = [(s, o) for s, o in active_set if s > t_i]
        n_aktive_ops[i] = sum(o for _, o in active_set)
        active_set.append((slutt[i], ops[i]))

    events["n_aktive"] = n_aktive_ops  # beholder navn for bakoverkompat, men betyr nå op-binder

    def klass(n_a, c):
        ledige = c - n_a
        if ledige >= 2:
            return "Normal"
        elif ledige == 1:
            return "Brudd"
        else:
            return "Svikt"

    events["kapasitet"] = [klass(na, ce) for na, ce in zip(n_aktive_ops, c_eff_arr)]
    return events


def _expand_d_aba(df_daba, p, Y):
    """Generer Fase 1 (alltid) + Fase 2 (med sannsynlighet p) events for D-aba.
    Returnerer DataFrame med kolonnene: Dato_og_Tid, v3_kat, Time, Skift,
    Er_helg, bind_min, ops_bundet."""
    rng = np.random.default_rng(SEED_DABA)
    fase2_flag = rng.random(len(df_daba)) < p

    # Fase 1: alltid, 1 op, DABA_FASE1_MIN
    f1 = df_daba[["Dato_og_Tid", "Time", "Skift", "Er_helg"]].copy()
    f1["v3_kat"] = "D-aba-f1"
    f1["bind_min"] = DABA_FASE1_MIN
    f1["ops_bundet"] = 1

    # Fase 2: andel p, 1 op, Y min, starter +90 sek
    f2_src = df_daba[fase2_flag].copy()
    f2 = f2_src[["Dato_og_Tid", "Time", "Skift", "Er_helg"]].copy()
    f2["Dato_og_Tid"] = f2["Dato_og_Tid"] + pd.to_timedelta(DABA_FASE2_OFFSET_MIN, unit="m")
    f2["v3_kat"] = "D-aba-f2"
    f2["bind_min"] = Y
    f2["ops_bundet"] = 1

    return pd.concat([f1, f2], ignore_index=True)


def bygg_events(scenario_name, include_only=None):
    """Bygg kombinert event-dataframe for et gitt scenario.
    include_only: liste av v3_kat som skal inkluderes (None = alle).
                  Eks: ['D-pri1','D-aba','skjult'] for Variant A."""
    scen = SCENARIOS[scenario_name]

    # Basisdata
    df_live = df[df["Dato_og_Tid"].notna()].copy()

    events_list = []

    # D-pri1: 2 op-binder (makkerpar) i full bindingstid
    d_pri1 = df_live[df_live["v3_kat"] == "D-pri1"]
    if len(d_pri1) > 0 and (include_only is None or "D-pri1" in include_only):
        e = d_pri1[["Dato_og_Tid", "Time", "Skift", "Er_helg"]].copy()
        e["v3_kat"] = "D-pri1"
        e["bind_min"] = df.loc[d_pri1.index, "bind_D"]
        e["ops_bundet"] = 2
        events_list.append(e)

    # D-aba: Fase 1 + valgfri Fase 2 (med sannsynlighet p, bindingstid Y)
    d_aba = df_live[df_live["v3_kat"] == "D-aba"]
    if len(d_aba) > 0 and (include_only is None or "D-aba" in include_only):
        events_list.append(_expand_d_aba(d_aba, scen["daba_p"], scen["daba_Y"]))

    # S, L-aba, L-hendelse, L-ukjent, F, V: 1 op per event
    for kat in ["S", "L-aba", "L-hendelse", "L-ukjent", "F", "V"]:
        if include_only is not None and kat not in include_only:
            continue
        sub = df_live[df_live["v3_kat"] == kat]
        if len(sub) == 0:
            continue
        e = sub[["Dato_og_Tid", "Time", "Skift", "Er_helg"]].copy()
        e["v3_kat"] = kat
        e["bind_min"] = scen[kat]
        e["ops_bundet"] = 1
        events_list.append(e)

    # Skjulte anrop: 1 op, 1 min
    if hidden_rows and (include_only is None or "skjult" in include_only):
        hdf = pd.DataFrame(hidden_rows)
        hdf["Dato_og_Tid"] = pd.to_datetime(hdf["Dato_og_Tid"])
        hdf["Time"] = hdf["Dato_og_Tid"].dt.hour
        hdf["Skift"] = np.where(hdf["Time"].between(7, 18), "Dag", "Natt")
        hdf["Er_helg"] = hdf["Dato_og_Tid"].dt.dayofweek >= 5
        hdf["v3_kat"] = "skjult"
        hdf["bind_min"] = SKJULT_BIND_MIN
        hdf["ops_bundet"] = 1
        events_list.append(hdf[["Dato_og_Tid", "v3_kat", "Time", "Skift", "Er_helg", "bind_min", "ops_bundet"]])

    combined = pd.concat(events_list, ignore_index=True)

    # c_eff
    dag_hverdag = (combined["Skift"] == "Dag") & (~combined["Er_helg"])
    combined["c_eff"] = np.where(dag_hverdag, 3, 2)

    return combined.sort_values("Dato_og_Tid").reset_index(drop=True)


# === 6. KJOER VARIANT A (kun beredskap: D-pri1 + D-aba + skjulte) og VARIANT B ===

# Variant A: beredskapsbelastning (D-pri1 + D-aba + skjulte) — bruker hoved-scenario for D-aba fase 2
print("\n" + "=" * 70)
print("VARIANT A: Beredskapsbelastning (D-pri1 + D-aba + skjulte)")
print("D-aba fase 2 bruker hoved-scenario (p=0.50, Y=6 min)")
print("=" * 70)

ev_a = bygg_events("hoved", include_only=["D-pri1", "D-aba", "skjult"])
result_a = kjor_sweep(ev_a, "Variant A")

order = ["Normal", "Brudd", "Svikt"]
def print_fordeling(label, data):
    total = len(data)
    parts = []
    for niva in order:
        nv = (data["kapasitet"] == niva).sum()
        parts.append(f"{niva}={nv/total*100:.1f}%")
    print(f"  {label:25s} (n={total:>6}): {', '.join(parts)}")

print_fordeling("Alle", result_a)
print_fordeling("Dag hverdag (c=3)", result_a[result_a["c_eff"] == 3])
print_fordeling("Natt/helg (c=2)", result_a[result_a["c_eff"] == 2])

# Variant B: alle hendelser, tre scenarioer
results_b = {}
for scen_name in ["lav", "hoved", "hoey"]:
    print(f"\n{'=' * 70}")
    print(f"VARIANT B ({scen_name}): Alle hendelser + skjulte")
    print(f"Bindingstider: {SCENARIOS[scen_name]}")
    print(f"{'=' * 70}")

    ev_b = bygg_events(scen_name)
    result_b = kjor_sweep(ev_b, f"Variant B ({scen_name})")
    results_b[scen_name] = result_b

    print_fordeling("Alle", result_b)
    print_fordeling("Dag hverdag (c=3)", result_b[result_b["c_eff"] == 3])
    print_fordeling("Natt/helg (c=2)", result_b[result_b["c_eff"] == 2])

# === 7. FIGURER ===

colors = {"Normal": "#4caf50", "Brudd": "#ff9800", "Svikt": "#d32f2f"}

# Figur 1: Variant A vs Variant B (hoved) — per skifttype
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for ax, (ce, label) in zip(axes, [(None, "Alle"), (3, "Dag hverdag (c=3)"), (2, "Natt/helg (c=2)")]):
    if ce is None:
        da = result_a
        db = results_b["hoved"]
    else:
        da = result_a[result_a["c_eff"] == ce]
        db = results_b["hoved"][results_b["hoved"]["c_eff"] == ce]

    x = np.arange(len(order))
    width = 0.35
    vals_a = [(da["kapasitet"] == k).mean() * 100 for k in order]
    vals_b = [(db["kapasitet"] == k).mean() * 100 for k in order]

    bars1 = ax.bar(x - width/2, vals_a, width, color=[colors[k] for k in order],
                   alpha=1.0, edgecolor="white", label="A: Kun beredskap")
    bars2 = ax.bar(x + width/2, vals_b, width, color=[colors[k] for k in order],
                   alpha=0.5, edgecolor="black", linewidth=1.2, label="B: Total belastning")

    for bars in [bars1, bars2]:
        for bar in bars:
            h = bar.get_height()
            if h > 0.3:
                ax.text(bar.get_x() + bar.get_width()/2, h + 0.3,
                        f"{h:.1f}%", ha="center", fontsize=7, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(order)
    ax.set_title(label, fontsize=11, fontweight="bold")
    ax.set_ylabel("Andel (%)")
    ax.set_ylim(0, max(max(vals_a), max(vals_b)) * 1.25)
    if ax == axes[0]:
        ax.legend(fontsize=8)

fig.suptitle(
    "Variant A (beredskapsbelastning) vs Variant B (total operativ belastning)\n"
    "110 Sor-Vest 2025 — hovedscenario",
    fontsize=12, fontweight="bold",
)
plt.tight_layout()
plt.savefig(FIG_DIR / "total_belastning_A_vs_B.png", bbox_inches="tight")
print(f"\nFigur 1: {FIG_DIR / 'total_belastning_A_vs_B.png'}")

# Figur 2: Sensitivitetsanalyse — tre scenarioer for natt/helg
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

for ax, (ce, label) in zip(axes, [(3, "Dag hverdag (c=3)"), (2, "Natt/helg (c=2)")]):
    da = result_a[result_a["c_eff"] == ce]

    x = np.arange(len(order))
    width = 0.18
    offsets = [-1.5, -0.5, 0.5, 1.5]
    labels_sc = ["A: Beredskap", "B: Lav", "B: Hoved", "B: Hoey"]
    datasets = [da, results_b["lav"][results_b["lav"]["c_eff"] == ce],
                results_b["hoved"][results_b["hoved"]["c_eff"] == ce],
                results_b["hoey"][results_b["hoey"]["c_eff"] == ce]]
    alphas = [1.0, 0.4, 0.7, 0.4]

    for j, (ds, lbl, alpha) in enumerate(zip(datasets, labels_sc, alphas)):
        vals = [(ds["kapasitet"] == k).mean() * 100 for k in order]
        bars = ax.bar(x + offsets[j] * width, vals, width,
                      color=[colors[k] for k in order], alpha=alpha,
                      edgecolor="black" if j > 0 else "white",
                      linewidth=0.8, label=lbl)
        for bar in bars:
            h = bar.get_height()
            if h > 1:
                ax.text(bar.get_x() + bar.get_width()/2, h + 0.3,
                        f"{h:.0f}", ha="center", fontsize=6)

    ax.set_xticks(x)
    ax.set_xticklabels(order)
    ax.set_title(label, fontsize=11, fontweight="bold")
    ax.set_ylabel("Andel (%)")
    ax.legend(fontsize=7, loc="upper right")

fig.suptitle(
    "Sensitivitetsanalyse: effekt av bindingstidsantakelser\n"
    "110 Sor-Vest 2025",
    fontsize=12, fontweight="bold",
)
plt.tight_layout()
plt.savefig(FIG_DIR / "total_belastning_sensitivitet.png", bbox_inches="tight")
print(f"Figur 2: {FIG_DIR / 'total_belastning_sensitivitet.png'}")

# === 8. EKSPORTER RESULTATER ===
summary = []
# Variant A
for ce, label in [(None, "Alle"), (3, "Dag hverdag"), (2, "Natt/helg")]:
    d = result_a if ce is None else result_a[result_a["c_eff"] == ce]
    summary.append({
        "Variant": "A (beredskap)", "Scenario": "-", "Skifttype": label,
        "n": len(d),
        "Normal_pct": round((d["kapasitet"] == "Normal").mean() * 100, 1),
        "Brudd_pct": round((d["kapasitet"] == "Brudd").mean() * 100, 1),
        "Svikt_pct": round((d["kapasitet"] == "Svikt").mean() * 100, 1),
    })
# Variant B
for scen_name in ["lav", "hoved", "hoey"]:
    rb = results_b[scen_name]
    for ce, label in [(None, "Alle"), (3, "Dag hverdag"), (2, "Natt/helg")]:
        d = rb if ce is None else rb[rb["c_eff"] == ce]
        summary.append({
            "Variant": "B (total)", "Scenario": scen_name, "Skifttype": label,
            "n": len(d),
            "Normal_pct": round((d["kapasitet"] == "Normal").mean() * 100, 1),
            "Brudd_pct": round((d["kapasitet"] == "Brudd").mean() * 100, 1),
            "Svikt_pct": round((d["kapasitet"] == "Svikt").mean() * 100, 1),
        })

out = pd.DataFrame(summary)
out.to_csv(PROJECT / "analyse" / "total_belastning_oppsummering.csv", index=False, encoding="utf-8")
print(f"\nOppsummering: {PROJECT / 'analyse' / 'total_belastning_oppsummering.csv'}")

# Kategorisering per hendelse (for eventuell videre analyse)
kat_export = df[["Oppdrag_ID", "110_ID", "Oppdragstype", "Opprinnelig_oppdragstype", "v3_kat"]].copy()
kat_export.to_csv(PROJECT / "analyse" / "total_belastning_kategorisering.csv", index=False, encoding="utf-8")
print(f"Kategorisering: {PROJECT / 'analyse' / 'total_belastning_kategorisering.csv'}")

print("\n=== FERDIG ===")
