"""
V3: Total operativ belastning — utvidet ankomstkonfliktmodell
=============================================================
Bruker SAMME sweep-algoritme som konflikt_v4_korrigert.py,
men inkluderer ALLE hendelser (61 964), ikke bare kategori D.

Klassifisering basert paa Oppdragstype + Opprinnelig oppdragstype:
  D         Utrykningshendelse (Ressurs_varslet finnes)   -> databasert
  S         Service/overfoeingstest                        -> 2 min
  L-aba     ABA loest av 110                               -> 3 min
  L-hendelse Reell hendelse loest av 110                   -> 5 min
  L-ukjent  Loest av 110, ukjent type                      -> 3 min
  F         Feilringing / ikke-noedmelding / eCall feil     -> 0.5 min
  V         Viderevarsling / viderekobling                  -> 1 min

Kjoerer tre scenarioer (lav/hoved/hoey) for sensitivitetsanalyse.
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

KVITTERING_MIN = 3.0  # kvittering etter foerste ressurs fremme (kat D)
SKJULT_BIND_MIN = 1.0  # sammenstilte anrop

# Bindingstider per scenario (minutter)
SCENARIOS = {
    "lav": {"S": 1, "L-aba": 2, "L-hendelse": 3, "L-ukjent": 1, "F": 0.25, "V": 0.5},
    "hoved": {"S": 2, "L-aba": 3, "L-hendelse": 5, "L-ukjent": 3, "F": 0.5, "V": 1},
    "hoey": {"S": 4, "L-aba": 5, "L-hendelse": 8, "L-ukjent": 5, "F": 1, "V": 2},
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
    if pd.notna(row["Ressurs_varslet"]):
        return "D"

    ot = str(row["Oppdragstype"]).strip() if pd.notna(row["Oppdragstype"]) else ""
    oot = str(row["Opprinnelig_oppdragstype"]).strip() if pd.notna(row["Opprinnelig_oppdragstype"]) else ""

    if ot == "Service":
        return "S"

    feilring_typer = {"Nødanrop feilring", "Ikke reell nødmelding",
                      "ECall feil bruk", "ECall teknisk/ukjent", "ECall veihjelp"}
    if ot in feilring_typer:
        return "F"

    if "viderevarslet" in ot.lower() or "viderekoble" in ot.lower():
        return "V"

    if "ppdrag" in ot and "110" in ot:  # "Oppdrag løst av 110"
        if oot == "ABA":
            return "L-aba"
        elif oot and oot != "nan":
            return "L-hendelse"
        else:
            return "L-ukjent"

    return "L-ukjent"

df["v3_kat"] = df.apply(klassifiser_kategori_v2, axis=1)

print("\n=== V3-kategorisering ===")
kat_counts = df["v3_kat"].value_counts()
for kat in ["D", "S", "L-aba", "L-hendelse", "L-ukjent", "F", "V"]:
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

# === 4. BEREGN BINDINGSTID FOR KATEGORI D (databasert) ===
d_mask = df["v3_kat"] == "D"
df.loc[d_mask, "bind_raa"] = (
    (df.loc[d_mask, "Forste_ressurs_fremme"] - df.loc[d_mask, "Dato_og_Tid"]).dt.total_seconds() / 60
)
df.loc[df["bind_raa"] < 0, "bind_raa"] = np.nan
df.loc[df["bind_raa"] > 180, "bind_raa"] = np.nan
median_bind_d = df.loc[d_mask & df["bind_raa"].notna(), "bind_raa"].median()
df.loc[d_mask & df["bind_raa"].isna(), "bind_raa"] = median_bind_d
df.loc[d_mask, "bind_D"] = df.loc[d_mask, "bind_raa"] + KVITTERING_MIN

print(f"Kategori D median bindingstid: {median_bind_d:.1f} min (+ {KVITTERING_MIN} kvittering)")

# === 5. SWEEP-FUNKSJON ===
def kjor_sweep(events_df, label=""):
    """Kjoer ankomstkonflikt-sweep paa sortert events_df med kolonnene
    Dato_og_Tid, bind_min, c_eff. Returnerer events_df med n_aktive og kapasitet."""
    events = events_df.sort_values("Dato_og_Tid").reset_index(drop=True)
    events["slutt_ts"] = events["Dato_og_Tid"] + pd.to_timedelta(events["bind_min"], unit="m")

    n = len(events)
    ankomst = events["Dato_og_Tid"].values
    slutt = events["slutt_ts"].values
    c_eff_arr = events["c_eff"].values

    n_aktive = np.zeros(n, dtype=int)
    active_set = []
    for i in range(n):
        t_i = ankomst[i]
        active_set = [s for s in active_set if s > t_i]
        n_aktive[i] = len(active_set)
        active_set.append(slutt[i])

    events["n_aktive"] = n_aktive

    def klass(n_a, c):
        ledige = c - n_a
        if ledige >= 2:
            return "Normal"
        elif ledige == 1:
            return "Brudd"
        else:
            return "Svikt"

    events["kapasitet"] = [klass(na, ce) for na, ce in zip(n_aktive, c_eff_arr)]
    return events


def bygg_events(scenario_name):
    """Bygg kombinert event-dataframe for et gitt scenario."""
    scen = SCENARIOS[scenario_name]

    # Alle synlige hendelser
    ev = df[["Dato_og_Tid", "v3_kat", "Time", "Skift", "Er_helg"]].copy()
    ev = ev[ev["Dato_og_Tid"].notna()].copy()

    # Sett bindingstid
    ev["bind_min"] = 0.0
    for kat, bind in scen.items():
        ev.loc[ev["v3_kat"] == kat, "bind_min"] = bind
    # D: databasert
    ev.loc[ev["v3_kat"] == "D", "bind_min"] = df.loc[ev[ev["v3_kat"] == "D"].index, "bind_D"]

    # Skjulte anrop
    if hidden_rows:
        hdf = pd.DataFrame(hidden_rows)
        hdf["Dato_og_Tid"] = pd.to_datetime(hdf["Dato_og_Tid"])
        hdf["Time"] = hdf["Dato_og_Tid"].dt.hour
        hdf["Skift"] = np.where(hdf["Time"].between(7, 18), "Dag", "Natt")
        hdf["Er_helg"] = hdf["Dato_og_Tid"].dt.dayofweek >= 5
        hdf["bind_min"] = SKJULT_BIND_MIN
        combined = pd.concat([ev, hdf[["Dato_og_Tid", "v3_kat", "Time", "Skift", "Er_helg", "bind_min"]]])
    else:
        combined = ev

    # c_eff
    dag_hverdag = (combined["Skift"] == "Dag") & (~combined["Er_helg"])
    combined["c_eff"] = np.where(dag_hverdag, 3, 2)

    return combined.sort_values("Dato_og_Tid").reset_index(drop=True)


# === 6. KJOER VARIANT A (kun D + skjulte) og VARIANT B (alle, tre scenarioer) ===

# Variant A: reproduser eksisterende modell
print("\n" + "=" * 70)
print("VARIANT A: Kun kategori D + skjulte anrop (eksisterende modell)")
print("=" * 70)

ev_a = df[df["v3_kat"] == "D"][["Dato_og_Tid", "v3_kat", "Time", "Skift", "Er_helg"]].copy()
ev_a = ev_a[ev_a["Dato_og_Tid"].notna()].copy()
ev_a["bind_min"] = df.loc[ev_a.index, "bind_D"]

if hidden_rows:
    hdf = pd.DataFrame(hidden_rows)
    hdf["Dato_og_Tid"] = pd.to_datetime(hdf["Dato_og_Tid"])
    hdf["Time"] = hdf["Dato_og_Tid"].dt.hour
    hdf["Skift"] = np.where(hdf["Time"].between(7, 18), "Dag", "Natt")
    hdf["Er_helg"] = hdf["Dato_og_Tid"].dt.dayofweek >= 5
    hdf["bind_min"] = SKJULT_BIND_MIN
    hdf["v3_kat"] = "skjult"
    ev_a = pd.concat([ev_a, hdf[["Dato_og_Tid", "v3_kat", "Time", "Skift", "Er_helg", "bind_min"]]])

dag_hv_a = (ev_a["Skift"] == "Dag") & (~ev_a["Er_helg"])
ev_a["c_eff"] = np.where(dag_hv_a, 3, 2)
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
