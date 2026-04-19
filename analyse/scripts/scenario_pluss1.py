"""
Scenarioanalyse: +1 operator per skift — V3-modell
===================================================
Sammenligner dagens bemanning (dag=3, natt/helg=2) med
+1 operator (dag=4, natt/helg=3) under V3 op-binder-semantikk.

Bruker samme klassifisering og bindingstider som konflikt_total_belastning.py.
Kun beredskapshendelser (D-pri1 + D-aba + skjulte) vurderes.

Output: figur + oppsummeringstabell
"""
import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PROJECT = pathlib.Path(r"C:\Users\runeg\OneDrive\Documents\Skole utdanning"
                       r"\Logistikk studie\LOG650 LOGISTIKK OG KI"
                       r"\G20-rune-individuell")
DATA_DIR = PROJECT / "004 data"
FIG_DIR = PROJECT / "analyse" / "figurer"

KVITTERING_MIN = 3.0
SKJULT_BIND_MIN = 1.0
DABA_FASE1_MIN = 3.0
DABA_FASE2_OFFSET_MIN = 1.5
DABA_P = 0.50  # hoved-scenario
DABA_Y = 6.0   # hoved-scenario
SEED_DABA = 20260419

plt.rcParams.update({"figure.dpi": 150, "font.size": 10})

# === LAST DATA ===
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

for c in ["Dato_og_Tid", "Ressurs_varslet", "Forste_ressurs_fremme"]:
    df[c] = pd.to_datetime(df[c], errors="coerce")

df["Time"] = pd.to_numeric(df["Time_paa_dognet"], errors="coerce").astype("Int64")
df["Skift"] = np.where(df["Time"].between(7, 18), "Dag", "Natt")
df["Ukedagsnr_int"] = pd.to_numeric(df["Ukedagsnr"], errors="coerce").astype("Int64")
df["Er_helg"] = df["Ukedagsnr_int"].isin([6, 7])

# === V3-KLASSIFISERING ===
def klassifiser(row):
    if pd.notna(row["Ressurs_varslet"]):
        oot = str(row["Opprinnelig_oppdragstype"]).strip() if pd.notna(row["Opprinnelig_oppdragstype"]) else ""
        kilde = str(row["Kilde"]).strip() if pd.notna(row["Kilde"]) else ""
        if oot.startswith("ABA") and kilde == "Alarm":
            return "D-aba"
        return "D-pri1"
    return "annet"

df["v3_kat"] = df.apply(klassifiser, axis=1)
print(f"D-pri1: {(df['v3_kat']=='D-pri1').sum():,}")
print(f"D-aba:  {(df['v3_kat']=='D-aba').sum():,}")

# === BINDINGSTID D-pri1 ===
d_pri1_mask = df["v3_kat"] == "D-pri1"
df.loc[d_pri1_mask, "bind_raa"] = (
    (df.loc[d_pri1_mask, "Forste_ressurs_fremme"] - df.loc[d_pri1_mask, "Dato_og_Tid"]).dt.total_seconds() / 60
)
df.loc[df["bind_raa"] < 0, "bind_raa"] = np.nan
df.loc[df["bind_raa"] > 180, "bind_raa"] = np.nan
median_bind = df.loc[d_pri1_mask & df["bind_raa"].notna(), "bind_raa"].median()
df.loc[d_pri1_mask & df["bind_raa"].isna(), "bind_raa"] = median_bind
df.loc[d_pri1_mask, "bind_D"] = df.loc[d_pri1_mask, "bind_raa"] + KVITTERING_MIN

# === SKJULTE ANROP ===
df["dato_id"] = df["110_ID"].str.extract(r"B\d+-(\d{6})-")[0]
df["seq_nr"] = df["110_ID"].str.extract(r"B\d+-\d{6}-(\d+)")[0].astype(float)

hidden_rows = []
for dato, group in df.groupby("dato_id"):
    seqs = set(group["seq_nr"].dropna().astype(int))
    if not seqs:
        continue
    max_s = max(seqs)
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
        hidden_rows.append({"Dato_og_Tid": est_tid})

print(f"Skjulte: {len(hidden_rows):,}")

# === BYGG EVENTS (beredskap, op-binder) ===
events_list = []

# D-pri1: 2 ops, databasert bindingstid
d_pri1 = df[df["v3_kat"] == "D-pri1"].copy()
d_pri1 = d_pri1[d_pri1["Dato_og_Tid"].notna()]
e = d_pri1[["Dato_og_Tid", "Skift", "Er_helg"]].copy()
e["v3_kat"] = "D-pri1"
e["bind_min"] = df.loc[d_pri1.index, "bind_D"]
e["ops_bundet"] = 2
events_list.append(e)

# D-aba: Fase 1 + valgfri Fase 2
d_aba = df[df["v3_kat"] == "D-aba"].copy()
d_aba = d_aba[d_aba["Dato_og_Tid"].notna()]
rng = np.random.default_rng(SEED_DABA)
fase2_flag = rng.random(len(d_aba)) < DABA_P

f1 = d_aba[["Dato_og_Tid", "Skift", "Er_helg"]].copy()
f1["v3_kat"] = "D-aba-f1"
f1["bind_min"] = DABA_FASE1_MIN
f1["ops_bundet"] = 1
events_list.append(f1)

f2_src = d_aba[fase2_flag]
f2 = f2_src[["Dato_og_Tid", "Skift", "Er_helg"]].copy()
f2["Dato_og_Tid"] = f2["Dato_og_Tid"] + pd.to_timedelta(DABA_FASE2_OFFSET_MIN, unit="m")
f2["v3_kat"] = "D-aba-f2"
f2["bind_min"] = DABA_Y
f2["ops_bundet"] = 1
events_list.append(f2)

# Skjulte
if hidden_rows:
    hdf = pd.DataFrame(hidden_rows)
    hdf["Dato_og_Tid"] = pd.to_datetime(hdf["Dato_og_Tid"])
    hdf["Skift"] = np.where(hdf["Dato_og_Tid"].dt.hour.between(7, 18), "Dag", "Natt")
    hdf["Er_helg"] = hdf["Dato_og_Tid"].dt.dayofweek >= 5
    hdf["v3_kat"] = "skjult"
    hdf["bind_min"] = SKJULT_BIND_MIN
    hdf["ops_bundet"] = 1
    events_list.append(hdf[["Dato_og_Tid", "Skift", "Er_helg", "v3_kat", "bind_min", "ops_bundet"]])

events = pd.concat(events_list, ignore_index=True)
events = events.sort_values("Dato_og_Tid").reset_index(drop=True)
events["slutt_ts"] = events["Dato_og_Tid"] + pd.to_timedelta(events["bind_min"], unit="m")

print(f"Totale events: {len(events):,}")

# === SWEEP ===
n = len(events)
ankomst = events["Dato_og_Tid"].values
slutt = events["slutt_ts"].values
ops = events["ops_bundet"].values.astype(int)

n_aktive_ops = np.zeros(n, dtype=int)
active_set = []
for i in range(n):
    t_i = ankomst[i]
    active_set = [(s, o) for s, o in active_set if s > t_i]
    n_aktive_ops[i] = sum(o for _, o in active_set)
    active_set.append((slutt[i], ops[i]))

events["n_aktive_ops"] = n_aktive_ops
dag_hverdag = ((events["Skift"] == "Dag") & (~events["Er_helg"])).values

# === SCENARIOER ===
def klassifiser_kap(n_a, c):
    ledige = c - n_a
    if ledige >= 2:
        return "Normal"
    elif ledige == 1:
        return "Brudd"
    else:
        return "Svikt"

scenarios = {
    "Dagens (3/2)": (3, 2),
    "+1 op (4/3)": (4, 3),
}
subsets = {
    "Alle": np.ones(n, dtype=bool),
    "Dag hverdag": dag_hverdag,
    "Natt/helg": ~dag_hverdag,
}

results = []
for sc_name, (c_dag, c_natt) in scenarios.items():
    c_eff = np.where(dag_hverdag, c_dag, c_natt)
    kap = np.array([klassifiser_kap(na, ce) for na, ce in zip(n_aktive_ops, c_eff)])
    for sub_name, mask in subsets.items():
        sk = kap[mask]
        ns = mask.sum()
        for niva in ["Normal", "Brudd", "Svikt"]:
            nv = (sk == niva).sum()
            results.append({
                "Scenario": sc_name, "Skifttype": sub_name, "Niva": niva,
                "n": nv, "pct": nv / ns * 100,
            })

rdf = pd.DataFrame(results)

# === FIGUR ===
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
colors = {"Normal": "#4caf50", "Brudd": "#ff9800", "Svikt": "#d32f2f"}
order = ["Normal", "Brudd", "Svikt"]

for col, sub_name in enumerate(subsets):
    ax = axes[col]
    x = np.arange(len(order))
    width = 0.35

    for i, sc_name in enumerate(scenarios):
        vals = [rdf[(rdf["Scenario"] == sc_name) & (rdf["Skifttype"] == sub_name) &
                    (rdf["Niva"] == niva)]["pct"].values[0] for niva in order]
        offset = (i - 0.5) * width
        bar_colors = [colors[k] for k in order]
        alpha = 1.0 if i == 0 else 0.5
        edgecolor = "black" if i == 1 else "white"
        bars = ax.bar(x + offset, vals, width, alpha=alpha,
                     color=bar_colors, edgecolor=edgecolor, linewidth=1.2,
                     label=sc_name if col == 0 else "")
        for bar, val in zip(bars, vals):
            if val > 0.3:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.5,
                        f"{val:.1f}%", ha="center", fontsize=8, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(order)
    ax.set_title(sub_name, fontsize=11, fontweight="bold")
    ax.set_ylabel("Andel (%)")
    ax.set_ylim(0, 100)
    if col == 0:
        ax.legend(fontsize=9, loc="upper right")

fig.suptitle(
    "Effekt av +1 operator per skift (V3-modell, op-binder-semantikk)\n"
    "Solid = dagens bemanning (3/2), halv-gjennomsiktig med sort kant = +1 (4/3)",
    fontsize=13, fontweight="bold",
)
plt.tight_layout()
plt.savefig(FIG_DIR / "scenario_pluss1_operator.png", bbox_inches="tight")
print(f"Figur: {FIG_DIR / 'scenario_pluss1_operator.png'}")

# === OPPSUMMERING ===
summary_rows = []
for sub_name in ["Alle", "Dag hverdag", "Natt/helg"]:
    row = {"Skifttype": sub_name}
    for sc_name in scenarios:
        for niva in order:
            r = rdf[(rdf["Scenario"] == sc_name) & (rdf["Skifttype"] == sub_name) &
                    (rdf["Niva"] == niva)]
            key = f"{sc_name}_{niva}"
            row[key] = round(r["pct"].values[0], 1) if len(r) > 0 else 0
    summary_rows.append(row)

sdf = pd.DataFrame(summary_rows)
sdf.to_csv(PROJECT / "analyse" / "scenario_pluss1_tabell.csv", index=False, encoding="utf-8")
print(f"Tabell: {PROJECT / 'analyse' / 'scenario_pluss1_tabell.csv'}")

# Print for rapport
print("\nSammendrag for rapport (V3-modell):")
print(f"{'':>15} | {'Dagens (3/2)':>30} | {'+1 op (4/3)':>30}")
print(f"{'':>15} | {'Norm':>8} {'Brudd':>8} {'Svikt':>8} | {'Norm':>8} {'Brudd':>8} {'Svikt':>8}")
print("-" * 88)
for sub_name in subsets:
    r_now = {nv: rdf[(rdf["Scenario"]=="Dagens (3/2)") &
                     (rdf["Skifttype"]==sub_name) & (rdf["Niva"]==nv)]["pct"].values[0]
             for nv in order}
    r_new = {nv: rdf[(rdf["Scenario"]=="+1 op (4/3)") &
                     (rdf["Skifttype"]==sub_name) & (rdf["Niva"]==nv)]["pct"].values[0]
             for nv in order}
    print(f"{sub_name:>15} | {r_now['Normal']:>7.1f}% {r_now['Brudd']:>7.1f}% {r_now['Svikt']:>7.1f}%"
          f" | {r_new['Normal']:>7.1f}% {r_new['Brudd']:>7.1f}% {r_new['Svikt']:>7.1f}%")

print("\n=== FERDIG ===")
