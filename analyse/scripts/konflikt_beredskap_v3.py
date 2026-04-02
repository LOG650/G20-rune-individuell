"""
Ankomstkonfliktmodell v3 - to driftsmoduser
=============================================
Sammenligner kapasitetsniva under to forutsetninger:

  Modell A - PROSEDYRE (makkerpar): Hver hendelse binder 2 operatorer
    Slik det SKAL gjores iht. driftsstandard.

  Modell B - BESTE EVNE (solo): Hver hendelse binder 1 operator
    Slik det FAKTISK gjores nar kapasiteten presses.

Klassifisering:
  Normal:     Nok ledige operatorer til makkerpar pa NESTE hendelse (>=2 ledige)
  Degradert:  Kun 1 ledig operator - solo-handtering
  Svikt:      Ingen ledig operator - VL ma overta eller overlop

Bindingstid = (anrop -> forste ressurs fremme) + 3 min kvittering
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

KVITTERING_MIN = 3.0

sns.set_style("whitegrid")
plt.rcParams.update({"figure.dpi": 150, "font.size": 10})

# === 1. LAST OG KLARGJOR ===
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

dt_cols = [
    "Dato_og_Tid", "Oppdrag_opprettet", "Ressurs_varslet",
    "Rykket_ut", "Forste_ressurs_fremme", "Siste_ressurs_ledig",
]
for c in dt_cols:
    df[c] = pd.to_datetime(df[c], errors="coerce")

df["Time"] = pd.to_numeric(df["Time_paa_dognet"], errors="coerce").astype("Int64")
df["Skift"] = np.where(df["Time"].between(7, 18), "Dag", "Natt")
df["Ukedagsnr_int"] = pd.to_numeric(df["Ukedagsnr"], errors="coerce").astype("Int64")
df["Er_helg"] = df["Ukedagsnr_int"].isin([6, 7])
df["c_eff"] = np.where((df["Skift"] == "Dag") & (~df["Er_helg"]), 3, 2)

# === 2. FILTRER TIL BEREDSKAPSOPPDRAG ===
bered = df[df["Ressurs_varslet"].notna()].copy()

# Bindingstid
bered["bind_raa"] = (
    (bered["Forste_ressurs_fremme"] - bered["Dato_og_Tid"]).dt.total_seconds() / 60
)
bered.loc[bered["bind_raa"] < 0, "bind_raa"] = np.nan
bered.loc[bered["bind_raa"] > 180, "bind_raa"] = np.nan

has_fremme = bered["bind_raa"].notna()
median_bind = bered.loc[has_fremme, "bind_raa"].median()
bered.loc[~has_fremme, "bind_raa"] = median_bind
bered["bind_min"] = bered["bind_raa"] + KVITTERING_MIN

print(f"Beredskapsoppdrag: {len(bered)}")
print(f"Median bindingstid (inkl +3 min): {bered['bind_min'].median():.1f} min")
print()

# === 3. ANKOMSTKONFLIKTMODELL ===
work = bered.sort_values("Dato_og_Tid").reset_index(drop=True)
work["ankomst_ts"] = work["Dato_og_Tid"]
work["slutt_ts"] = work["Dato_og_Tid"] + pd.to_timedelta(work["bind_min"], unit="m")

n = len(work)
ankomst = work["ankomst_ts"].values
slutt = work["slutt_ts"].values

# Tell samtidige aktive hendelser
n_aktive = np.zeros(n, dtype=int)
active_set = []
for i in range(n):
    t_i = ankomst[i]
    active_set = [s for s in active_set if s > t_i]
    n_aktive[i] = len(active_set)
    active_set.append(slutt[i])

work["n_aktive"] = n_aktive
c_eff_arr = work["c_eff"].values

# === MODELL A: PROSEDYRE (2 operatorer per hendelse) ===
# Ledige operatorer = c_eff - 2 * n_aktive
# Normal:    ledige >= 2  (kan sette makkerpar pa neste)
# Degradert: ledige = 1   (kun solo mulig)
# Svikt:     ledige <= 0  (ingen ledig)

def klassifiser_prosedyre(n_a, c):
    ledige = c - 2 * n_a
    if ledige >= 2:
        return "Normal"
    elif ledige == 1:
        return "Degradert"
    else:
        return "Svikt"

work["kap_prosedyre"] = [
    klassifiser_prosedyre(na, ce) for na, ce in zip(n_aktive, c_eff_arr)
]

# === MODELL B: BESTE EVNE (1 operator per hendelse) ===
# Ledige operatorer = c_eff - 1 * n_aktive
# Normal:    ledige >= 2  (kan sette makkerpar pa neste)
# Degradert: ledige = 1   (kun solo mulig)
# Svikt:     ledige <= 0  (ingen ledig)

def klassifiser_beste_evne(n_a, c):
    ledige = c - n_a
    if ledige >= 2:
        return "Normal"
    elif ledige == 1:
        return "Degradert"
    else:
        return "Svikt"

work["kap_beste_evne"] = [
    klassifiser_beste_evne(na, ce) for na, ce in zip(n_aktive, c_eff_arr)
]

# === 4. RESULTATER ===
order = ["Normal", "Degradert", "Svikt"]

def print_fordeling(label, series, total):
    print(f"\n{label}:")
    for niva in order:
        n_val = (series == niva).sum()
        print(f"  {niva:>10}: {n_val:>5} ({n_val/total*100:.1f}%)")

print("=" * 65)
print("SAMMENLIGNING: Prosedyre (2 op) vs. Beste evne (1 op)")
print("=" * 65)

# Alle
print_fordeling("MODELL A - PROSEDYRE (2 op/hendelse) - Alle",
                work["kap_prosedyre"], len(work))
print_fordeling("MODELL B - BESTE EVNE (1 op/hendelse) - Alle",
                work["kap_beste_evne"], len(work))

# Per bemanningsniva
for ce, label in [(3, "Dag hverdag (c_eff=3)"), (2, "Natt/helg (c_eff=2)")]:
    s = work[work["c_eff"] == ce]
    print(f"\n--- {label} (n={len(s)}) ---")
    print_fordeling(f"  Prosedyre (2 op)", s["kap_prosedyre"], len(s))
    print_fordeling(f"  Beste evne (1 op)", s["kap_beste_evne"], len(s))

# Sammenligning per time
print(f"\n{'':=<80}")
print("PER TIME - Prosedyre vs Beste evne (% ikke-Normal)")
print(f"{'':=<80}")
print(f"{'Kl':>4}  {'n':>5}  {'--- Prosedyre ---':>20}  {'--- Beste evne ---':>20}")
print(f"{'':>4}  {'':>5}  {'Deg':>7} {'Svikt':>7} {'Tot':>6}  {'Deg':>7} {'Svikt':>7} {'Tot':>6}")
print("-" * 70)

hourly_results = []
for t in range(24):
    s = work[work["Time"] == t]
    if len(s) == 0:
        continue
    p_deg = (s["kap_prosedyre"] == "Degradert").mean() * 100
    p_svikt = (s["kap_prosedyre"] == "Svikt").mean() * 100
    b_deg = (s["kap_beste_evne"] == "Degradert").mean() * 100
    b_svikt = (s["kap_beste_evne"] == "Svikt").mean() * 100
    print(f"  {t:>2}  {len(s):>5}  {p_deg:>6.1f}% {p_svikt:>6.1f}% {p_deg+p_svikt:>5.1f}%"
          f"  {b_deg:>6.1f}% {b_svikt:>6.1f}% {b_deg+b_svikt:>5.1f}%")
    hourly_results.append({
        "Time": t, "n": len(s),
        "P_normal": (s["kap_prosedyre"] == "Normal").mean() * 100,
        "P_deg": p_deg, "P_svikt": p_svikt,
        "B_normal": (s["kap_beste_evne"] == "Normal").mean() * 100,
        "B_deg": b_deg, "B_svikt": b_svikt,
    })

hdf = pd.DataFrame(hourly_results)

# === 5. FIGURER ===

# Figur A: Sammenligning prosedyre vs beste evne - stolpediagram
fig, axes = plt.subplots(2, 3, figsize=(15, 9))
colors = {"Normal": "#4caf50", "Degradert": "#ff9800", "Svikt": "#d32f2f"}

datasets = [
    ("Alle (n={})".format(len(work)), work),
    ("Dag hverdag c=3\n(n={})".format(len(work[work["c_eff"]==3])),
     work[work["c_eff"] == 3]),
    ("Natt/helg c=2\n(n={})".format(len(work[work["c_eff"]==2])),
     work[work["c_eff"] == 2]),
]

for col_idx, (title, data) in enumerate(datasets):
    for row_idx, (model_col, model_name) in enumerate([
        ("kap_prosedyre", "Prosedyre (2 op)"),
        ("kap_beste_evne", "Beste evne (1 op)"),
    ]):
        ax = axes[row_idx, col_idx]
        kd = data[model_col].value_counts()
        vals = [kd.get(k, 0) for k in order]
        total_d = sum(vals)
        pcts = [v / total_d * 100 if total_d > 0 else 0 for v in vals]
        bars = ax.bar(order, pcts, color=[colors[k] for k in order], edgecolor="white")
        for bar, pct, val in zip(bars, pcts, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
                    f"{pct:.1f}%\n(n={val})", ha="center", fontsize=8, fontweight="bold")
        if row_idx == 0:
            ax.set_title(title, fontsize=10, fontweight="bold")
        if col_idx == 0:
            ax.set_ylabel(f"{model_name}\nAndel (%)", fontsize=10, fontweight="bold")
        ax.set_ylim(0, max(pcts) * 1.3 if max(pcts) > 0 else 100)

fig.suptitle(
    "Kapasitetsniva: Prosedyre (2 op/hendelse) vs. Beste evne (1 op/hendelse)\n"
    "110 Sor-Vest 2025 - kun beredskapsoppdrag, bindingstid inkl +3 min kvittering",
    fontsize=13, fontweight="bold",
)
plt.tight_layout()
plt.savefig(FIG_DIR / "kapasitet_prosedyre_vs_beste_evne.png", bbox_inches="tight")
print(f"\nFigur A: {FIG_DIR / 'kapasitet_prosedyre_vs_beste_evne.png'}")

# Figur B: Stacked per time - begge modeller
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 9), sharex=True)

for ax, prefix, model_name in [
    (ax1, "P_", "PROSEDYRE (2 operatorer per hendelse)"),
    (ax2, "B_", "BESTE EVNE (1 operator per hendelse)"),
]:
    ax.bar(hdf["Time"], hdf[f"{prefix}normal"], color="#4caf50", alpha=0.8,
           label="Normal (makkerpar)")
    ax.bar(hdf["Time"], hdf[f"{prefix}deg"],
           bottom=hdf[f"{prefix}normal"],
           color="#ff9800", alpha=0.8, label="Degradert (solo)")
    ax.bar(hdf["Time"], hdf[f"{prefix}svikt"],
           bottom=hdf[f"{prefix}normal"] + hdf[f"{prefix}deg"],
           color="#d32f2f", alpha=0.8, label="Svikt (ingen ledig)")

    ax3 = ax.twinx()
    ax3.plot(hdf["Time"], hdf["n"], "ko-", ms=4, lw=1, alpha=0.3)
    ax3.set_ylabel("Antall", color="gray", fontsize=8)

    ax.axvspan(7, 18.99, alpha=0.05, color="blue")
    ax.set_ylabel("Andel (%)")
    ax.set_title(model_name, fontsize=11, fontweight="bold")
    ax.legend(loc="lower left", fontsize=8)
    ax.set_ylim(0, 105)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

ax2.set_xlabel("Time pa dognet")
ax1.set_xlim(-0.5, 23.5)

fig.suptitle(
    "Kapasitetsniva per time - to driftsmoduser\n110 Sor-Vest 2025",
    fontsize=13, fontweight="bold",
)
plt.tight_layout()
plt.savefig(FIG_DIR / "kapasitet_per_time_to_modeller.png", bbox_inches="tight")
print(f"Figur B: {FIG_DIR / 'kapasitet_per_time_to_modeller.png'}")

# Figur C: Differanse-figur (gap mellom prosedyre og beste evne)
fig, ax = plt.subplots(figsize=(13, 5))
hdf["gap_deg"] = hdf["P_deg"] - hdf["B_deg"]
hdf["gap_svikt"] = hdf["P_svikt"] - hdf["B_svikt"]
hdf["gap_total"] = (hdf["P_deg"] + hdf["P_svikt"]) - (hdf["B_deg"] + hdf["B_svikt"])

ax.bar(hdf["Time"], hdf["gap_total"], color="#7b1fa2", alpha=0.7,
       label="Ekstra ikke-Normal ved prosedyre vs. beste evne")
ax.plot(hdf["Time"], hdf["P_deg"] + hdf["P_svikt"], "s-", color="#d32f2f",
        lw=2, label="Prosedyre: total ikke-Normal %")
ax.plot(hdf["Time"], hdf["B_deg"] + hdf["B_svikt"], "o-", color="#1565c0",
        lw=2, label="Beste evne: total ikke-Normal %")

ax.axvspan(7, 18.99, alpha=0.05, color="orange")
ax.set_xlabel("Time pa dognet")
ax.set_ylabel("Andel (%)")
ax.set_title(
    "Gapet mellom prosedyre og virkelighet\n"
    "Hvor mye driften tilpasses for a holde tjenesten gaende",
    fontsize=12, fontweight="bold",
)
ax.legend(fontsize=9)
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.set_xlim(-0.5, 23.5)
plt.tight_layout()
plt.savefig(FIG_DIR / "kapasitet_gap_prosedyre_virkelighet.png", bbox_inches="tight")
print(f"Figur C: {FIG_DIR / 'kapasitet_gap_prosedyre_virkelighet.png'}")

# === 6. EKSPORTER ===
result = work[["Oppdrag_ID", "Dato_og_Tid", "Time", "Skift", "Er_helg", "c_eff",
               "bind_min", "n_aktive", "kap_prosedyre", "kap_beste_evne",
               "Overordnet_oppdragstype"]].copy()
result.to_csv(PROJECT / "analyse" / "konflikt_to_modeller_v3.csv",
              index=False, encoding="utf-8")

# Oppsummeringstabell
rows = []
for label, data in [("Alle", work),
                     ("Dag hverdag (c=3)", work[work["c_eff"]==3]),
                     ("Natt/helg (c=2)", work[work["c_eff"]==2])]:
    n_t = len(data)
    rows.append({
        "Skifttype": label, "n": n_t,
        "Prosedyre_Normal": round((data["kap_prosedyre"]=="Normal").mean()*100, 1),
        "Prosedyre_Degradert": round((data["kap_prosedyre"]=="Degradert").mean()*100, 1),
        "Prosedyre_Svikt": round((data["kap_prosedyre"]=="Svikt").mean()*100, 1),
        "BesteEvne_Normal": round((data["kap_beste_evne"]=="Normal").mean()*100, 1),
        "BesteEvne_Degradert": round((data["kap_beste_evne"]=="Degradert").mean()*100, 1),
        "BesteEvne_Svikt": round((data["kap_beste_evne"]=="Svikt").mean()*100, 1),
    })
pd.DataFrame(rows).to_csv(
    PROJECT / "analyse" / "kapasitet_oppsummering_v3.csv",
    index=False, encoding="utf-8",
)
print(f"\nOppsummering: {PROJECT / 'analyse' / 'kapasitet_oppsummering_v3.csv'}")
print("\n=== FERDIG ===")
