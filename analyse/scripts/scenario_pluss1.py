"""
Scenarioanalyse: +1 operator per skift
========================================
Sammenligner dagens bemanning (dag=3, natt/helg=2) med
+1 operator (dag=4, natt/helg=3) under begge driftsmoduser.

Output: Figur + oppsummeringstabell
"""
import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

PROJECT = pathlib.Path(r"C:\Users\runeg\OneDrive\Documents\Skole utdanning"
                       r"\Logistikk studie\LOG650 LOGISTIKK OG KI"
                       r"\G20-rune-individuell")
DATA_DIR = PROJECT / "004 data"
FIG_DIR = PROJECT / "analyse" / "figurer"

plt.rcParams.update({"figure.dpi": 150, "font.size": 10})

# === LAST DATA OG BEREGN n_aktive (identisk med v3) ===
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

bered = df[df["Ressurs_varslet"].notna()].copy()
bered["bind_raa"] = (bered["Forste_ressurs_fremme"] - bered["Dato_og_Tid"]).dt.total_seconds() / 60
bered.loc[bered["bind_raa"] < 0, "bind_raa"] = np.nan
bered.loc[bered["bind_raa"] > 180, "bind_raa"] = np.nan
median_bind = bered.loc[bered["bind_raa"].notna(), "bind_raa"].median()
bered.loc[bered["bind_raa"].isna(), "bind_raa"] = median_bind
bered["bind_min"] = bered["bind_raa"] + 3.0

work = bered.sort_values("Dato_og_Tid").reset_index(drop=True)
work["slutt_ts"] = work["Dato_og_Tid"] + pd.to_timedelta(work["bind_min"], unit="m")

n = len(work)
ankomst = work["Dato_og_Tid"].values
slutt = work["slutt_ts"].values
n_aktive = np.zeros(n, dtype=int)
active_set = []
for i in range(n):
    t_i = ankomst[i]
    active_set = [s for s in active_set if s > t_i]
    n_aktive[i] = len(active_set)
    active_set.append(slutt[i])

work["n_aktive"] = n_aktive
dag_hverdag = ((work["Skift"] == "Dag") & (~work["Er_helg"])).values

def klassifiser(n_a, c, ops):
    ledige = c - ops * n_a
    if ledige >= 2:
        return "Normal"
    elif ledige == 1:
        return "Degradert"
    else:
        return "Svikt"

# === SCENARIOER ===
scenarios = {
    "Dagens (3/2)": (3, 2),
    "+1 op (4/3)": (4, 3),
}
models = {
    "Prosedyre (2 op)": 2,
    "Beste evne (1 op)": 1,
}
subsets = {
    "Alle": np.ones(n, dtype=bool),
    "Dag hverdag": dag_hverdag,
    "Natt/helg": ~dag_hverdag,
}

# Beregn alle kombinasjoner
results = []
for sc_name, (c_dag, c_natt) in scenarios.items():
    c_eff = np.where(dag_hverdag, c_dag, c_natt)
    for mod_name, ops in models.items():
        kap = np.array([klassifiser(na, ce, ops) for na, ce in zip(n_aktive, c_eff)])
        for sub_name, mask in subsets.items():
            sk = kap[mask]
            ns = mask.sum()
            for niva in ["Normal", "Degradert", "Svikt"]:
                nv = (sk == niva).sum()
                results.append({
                    "Scenario": sc_name, "Modell": mod_name,
                    "Skifttype": sub_name, "Niva": niva,
                    "n": nv, "pct": nv / ns * 100,
                })

rdf = pd.DataFrame(results)

# === FIGUR: 2x3 sammenligning ===
fig, axes = plt.subplots(2, 3, figsize=(16, 9))
colors = {"Normal": "#4caf50", "Degradert": "#ff9800", "Svikt": "#d32f2f"}
order = ["Normal", "Degradert", "Svikt"]

for row, (mod_name, ops) in enumerate(models.items()):
    for col, (sub_name, _) in enumerate(subsets.items()):
        ax = axes[row, col]
        x = np.arange(len(order))
        width = 0.35

        for i, (sc_name, _) in enumerate(scenarios.items()):
            vals = []
            for niva in order:
                r = rdf[(rdf["Scenario"] == sc_name) & (rdf["Modell"] == mod_name) &
                        (rdf["Skifttype"] == sub_name) & (rdf["Niva"] == niva)]
                vals.append(r["pct"].values[0] if len(r) > 0 else 0)

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
                            f"{val:.1f}%", ha="center", fontsize=7,
                            fontweight="bold")

        ax.set_xticks(x)
        ax.set_xticklabels(order)
        if row == 0:
            ax.set_title(sub_name, fontsize=11, fontweight="bold")
        if col == 0:
            ax.set_ylabel(f"{mod_name}\nAndel (%)", fontsize=10, fontweight="bold")
        max_val = rdf[(rdf["Modell"] == mod_name) & (rdf["Skifttype"] == sub_name)]["pct"].max()
        ax.set_ylim(0, max(max_val * 1.25, 5))
        if col == 0 and row == 0:
            ax.legend(fontsize=9, loc="upper right")

fig.suptitle(
    "Effekt av +1 operator per skift\n"
    "Solid = dagens bemanning (3/2), halv-gjennomsiktig med sort kant = +1 (4/3)",
    fontsize=13, fontweight="bold",
)
plt.tight_layout()
plt.savefig(FIG_DIR / "scenario_pluss1_operator.png", bbox_inches="tight")
print(f"Figur: {FIG_DIR / 'scenario_pluss1_operator.png'}")

# === OPPSUMMERINGSTABELL ===
summary_rows = []
for sub_name in ["Alle", "Dag hverdag", "Natt/helg"]:
    for mod_name in models:
        row = {"Skifttype": sub_name, "Modell": mod_name}
        for sc_name in scenarios:
            for niva in order:
                r = rdf[(rdf["Scenario"] == sc_name) & (rdf["Modell"] == mod_name) &
                        (rdf["Skifttype"] == sub_name) & (rdf["Niva"] == niva)]
                key = f"{sc_name}_{niva}"
                row[key] = round(r["pct"].values[0], 1) if len(r) > 0 else 0
        summary_rows.append(row)

sdf = pd.DataFrame(summary_rows)
sdf.to_csv(PROJECT / "analyse" / "scenario_pluss1_tabell.csv", index=False, encoding="utf-8")
print(f"Tabell: {PROJECT / 'analyse' / 'scenario_pluss1_tabell.csv'}")

# Print for rapport
print("\nSammendrag for rapport:")
for mod_name in models:
    print(f"\n{mod_name}:")
    print(f"{'':>15} | {'Dagens (3/2)':>30} | {'+1 op (4/3)':>30}")
    print(f"{'':>15} | {'Norm':>8} {'Deg':>8} {'Svikt':>8} | {'Norm':>8} {'Deg':>8} {'Svikt':>8}")
    print("-" * 85)
    for sub_name in subsets:
        r_now = {nv: rdf[(rdf["Scenario"]=="Dagens (3/2)") & (rdf["Modell"]==mod_name) &
                         (rdf["Skifttype"]==sub_name) & (rdf["Niva"]==nv)]["pct"].values[0]
                 for nv in order}
        r_new = {nv: rdf[(rdf["Scenario"]=="+1 op (4/3)") & (rdf["Modell"]==mod_name) &
                         (rdf["Skifttype"]==sub_name) & (rdf["Niva"]==nv)]["pct"].values[0]
                 for nv in order}
        print(f"{sub_name:>15} | {r_now['Normal']:>7.1f}% {r_now['Degradert']:>7.1f}% {r_now['Svikt']:>7.1f}%"
              f" | {r_new['Normal']:>7.1f}% {r_new['Degradert']:>7.1f}% {r_new['Svikt']:>7.1f}%")

print("\n=== FERDIG ===")
