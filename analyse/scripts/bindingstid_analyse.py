"""
Bindingstid-analyse: 110 Sor-Vest testdatasett
================================================
Estimerer hvor lenge operatorer er bundet per oppdrag,
basert pa tidsregistreringer i BRIS-data.

Faser:
  ROD-fase:  Anrop -> Ressurs varslet  (akutt samtale + varsling)
  GUL-fase:  Ressurs varslet -> Forste ressurs fremme (oppfolging)
  Total:     Anrop -> Forste ressurs fremme (begge operatorer bundet)

Output: Figurer i analyse/figurer/ + statistikk-tabell
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

sns.set_style("whitegrid")
plt.rcParams.update({"figure.dpi": 150, "font.size": 10})

# === 1. LAST DATA ===
files = list(DATA_DIR.glob("110*TESTDATASETT.xlsx"))
if not files:
    raise FileNotFoundError("Fant ikke testdatasett i 004 data/")

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

# Parse datetimes
dt_cols = [
    "Dato_og_Tid", "Oppdrag_opprettet", "Ressurs_varslet",
    "Rykket_ut", "Forste_ressurs_fremme", "Siste_ressurs_ledig",
]
for c in dt_cols:
    df[c] = pd.to_datetime(df[c], errors="coerce")

# Time som int
df["Time"] = pd.to_numeric(df["Time_paa_dognet"], errors="coerce").astype("Int64")

# Skifttype: Dag 07-19, Natt 19-07
df["Skift"] = np.where(df["Time"].between(7, 18), "Dag (07-19)", "Natt (19-07)")

# Ukedag (1=mandag ... 7=sondag)
df["Ukedagsnr_int"] = pd.to_numeric(df["Ukedagsnr"], errors="coerce").astype("Int64")
df["Er_helg"] = df["Ukedagsnr_int"].isin([6, 7])

print(f"Totalt: {len(df)} hendelser")
print(f"Skiftfordeling:\n{df['Skift'].value_counts().to_string()}")
print()

# === 2. BEREGN BINDINGSTIDER ===
utr = df[df["Ressurs_varslet"].notna()].copy()
print(f"Hendelser med Ressurs varslet: {len(utr)} ({len(utr)/len(df)*100:.1f}%)")

# ROD-fase: Anrop -> Ressurs varslet
utr["ROD_min"] = (utr["Ressurs_varslet"] - utr["Dato_og_Tid"]).dt.total_seconds() / 60

# GUL-fase: Ressurs varslet -> Forste ressurs fremme
utr["GUL_min"] = (utr["Forste_ressurs_fremme"] - utr["Ressurs_varslet"]).dt.total_seconds() / 60

# Total binding: Anrop -> Forste ressurs fremme
utr["Total_bind_min"] = (utr["Forste_ressurs_fremme"] - utr["Dato_og_Tid"]).dt.total_seconds() / 60

# Full syklus: Anrop -> Siste ressurs ledig
utr["Full_syklus_min"] = (utr["Siste_ressurs_ledig"] - utr["Dato_og_Tid"]).dt.total_seconds() / 60

# Filtrer ut datafeil (negative verdier, ekstreme outliers)
for c in ["ROD_min", "GUL_min", "Total_bind_min", "Full_syklus_min"]:
    utr.loc[utr[c] < 0, c] = np.nan
    utr.loc[utr[c] > 180, c] = np.nan  # >3 timer = sannsynlig datafeil

print(f"Gyldige ROD: {utr['ROD_min'].notna().sum()}")
print(f"Gyldige GUL: {utr['GUL_min'].notna().sum()}")
print(f"Gyldige Total: {utr['Total_bind_min'].notna().sum()}")
print(f"Gyldige Full syklus: {utr['Full_syklus_min'].notna().sum()}")
print()

# === 3. STATISTIKK-TABELL ===
def stats_row(series, label):
    s = series.dropna()
    return {
        "Fase": label,
        "n": len(s),
        "Gjennomsnitt": round(s.mean(), 1),
        "Median": round(s.median(), 1),
        "P10": round(s.quantile(0.10), 1),
        "P25": round(s.quantile(0.25), 1),
        "P75": round(s.quantile(0.75), 1),
        "P90": round(s.quantile(0.90), 1),
        "P95": round(s.quantile(0.95), 1),
    }

stats = pd.DataFrame([
    stats_row(utr["ROD_min"], "ROD (anrop til varslet)"),
    stats_row(utr["GUL_min"], "GUL (varslet til fremme)"),
    stats_row(utr["Total_bind_min"], "Total (anrop til fremme)"),
    stats_row(utr["Full_syklus_min"], "Full syklus (anrop til ledig)"),
])
print("=== BINDINGSTID-STATISTIKK (minutter) ===")
print(stats.to_string(index=False))
print()

# Per skift
print("=== PER SKIFTTYPE ===")
for skift in ["Dag (07-19)", "Natt (19-07)"]:
    s = utr[utr["Skift"] == skift]
    print(f"\n--- {skift} ---")
    stats_skift = pd.DataFrame([
        stats_row(s["ROD_min"], "ROD"),
        stats_row(s["GUL_min"], "GUL"),
        stats_row(s["Total_bind_min"], "Total"),
    ])
    print(stats_skift.to_string(index=False))

# Per oppdragstype
print("\n=== PER OVERORDNET OPPDRAGSTYPE (Total bindingstid) ===")
for ot, g in utr.groupby("Overordnet_oppdragstype"):
    s = g["Total_bind_min"].dropna()
    if len(s) > 10:
        print(f"  {ot}: n={len(s)}, median={s.median():.1f}, P90={s.quantile(.9):.1f} min")

# === 4. FIGUR 1: Histogram bindingstider ===
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

plot_specs = [
    ("ROD_min", "ROD-fase\n(anrop til ressurs varslet)", "#d32f2f"),
    ("GUL_min", "GUL-fase\n(varslet til forste fremme)", "#ff9800"),
    ("Total_bind_min", "Total bindingstid\n(anrop til forste fremme)", "#1565c0"),
]

for ax, (col, title, color) in zip(axes, plot_specs):
    data = utr[col].dropna()
    xlim = min(data.quantile(0.99) * 1.2, 60)
    ax.hist(data[data <= xlim], bins=50, color=color, alpha=0.7, edgecolor="white")
    ax.axvline(data.median(), color="black", ls="--", lw=1.5,
               label=f"Median: {data.median():.1f} min")
    ax.axvline(data.quantile(0.9), color="black", ls=":", lw=1.5,
               label=f"P90: {data.quantile(0.9):.1f} min")
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_xlabel("Minutter")
    ax.set_ylabel("Antall oppdrag")
    ax.legend(fontsize=8)
    ax.set_xlim(0, xlim)

fig.suptitle("Bindingstid per fase - 110 Sor-Vest 2025 (oppdrag med utrykningsressurser)",
             fontsize=12, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(FIG_DIR / "bindingstid_histogram.png", bbox_inches="tight")
print(f"\nFigur 1 lagret: {FIG_DIR / 'bindingstid_histogram.png'}")

# === 5. FIGUR 2: Boxplot per skifttype ===
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

box_specs = [
    ("ROD_min", "ROD-fase"),
    ("GUL_min", "GUL-fase"),
    ("Total_bind_min", "Total bindingstid"),
]

for ax, (col, title) in zip(axes, box_specs):
    cutoff = utr[col].quantile(0.95)
    data = utr[utr[col].notna() & (utr[col] <= cutoff)]
    sns.boxplot(data=data, x="Skift", y=col, ax=ax, palette=["#ffa726", "#42a5f5"])
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_ylabel("Minutter")
    ax.set_xlabel("")

fig.suptitle("Bindingstid dag vs. natt - 110 Sor-Vest 2025",
             fontsize=12, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(FIG_DIR / "bindingstid_dag_natt.png", bbox_inches="tight")
print(f"Figur 2 lagret: {FIG_DIR / 'bindingstid_dag_natt.png'}")

# === 6. FIGUR 3: Boxplot per oppdragstype ===
fig, ax = plt.subplots(figsize=(10, 5))
data_plot = utr[utr["Total_bind_min"].notna() & (utr["Total_bind_min"] <= 60)].copy()
type_map = {
    "110-oppdrag uten involvering av brannvesen": "T1 (uten brannvesen)",
    "Brann": "Brann",
    "Ulykke": "Ulykke",
    "Andre typer oppdrag": "Andre",
}
data_plot["Type_kort"] = data_plot["Overordnet_oppdragstype"].map(
    lambda x: type_map.get(x, x))
order = ["Brann", "Ulykke", "Andre", "T1 (uten brannvesen)"]
order = [o for o in order if o in data_plot["Type_kort"].values]
sns.boxplot(data=data_plot, x="Type_kort", y="Total_bind_min", order=order,
            ax=ax, palette="Set2")
ax.set_title("Total bindingstid per oppdragstype - 110 Sor-Vest 2025",
             fontsize=12, fontweight="bold")
ax.set_ylabel("Minutter (anrop til forste ressurs fremme)")
ax.set_xlabel("")
plt.tight_layout()
plt.savefig(FIG_DIR / "bindingstid_per_type.png", bbox_inches="tight")
print(f"Figur 3 lagret: {FIG_DIR / 'bindingstid_per_type.png'}")

# === 7. FIGUR 4: Tidsprofil per time ===
fig, ax = plt.subplots(figsize=(10, 4.5))
hourly = utr.groupby("Time")["Total_bind_min"].agg(["median", "mean", "count"]).dropna()
ax2 = ax.twinx()
ax2.bar(hourly.index, hourly["count"], alpha=0.15, color="gray", label="Antall oppdrag")
ax.plot(hourly.index, hourly["median"], "o-", color="#1565c0", lw=2,
        label="Median bindingstid")
ax.plot(hourly.index, hourly["mean"], "s--", color="#d32f2f", lw=1.5,
        label="Gjennomsnitt bindingstid")
ax.axvspan(7, 18.99, alpha=0.08, color="orange", label="Dagskift")
ax.set_xlabel("Time pa dognet")
ax.set_ylabel("Bindingstid (minutter)")
ax2.set_ylabel("Antall oppdrag", color="gray")
ax.set_title("Bindingstid og volum per time - 110 Sor-Vest 2025",
             fontsize=12, fontweight="bold")
ax.legend(loc="upper left", fontsize=8)
ax2.legend(loc="upper right", fontsize=8)
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.set_xlim(-0.5, 23.5)
plt.tight_layout()
plt.savefig(FIG_DIR / "bindingstid_per_time.png", bbox_inches="tight")
print(f"Figur 4 lagret: {FIG_DIR / 'bindingstid_per_time.png'}")

# === 8. EKSPORTER STATISTIKK ===
stats.to_csv(PROJECT / "analyse" / "bindingstid_statistikk.csv", index=False, encoding="utf-8")
print(f"\nStatistikk-tabell lagret: {PROJECT / 'analyse' / 'bindingstid_statistikk.csv'}")

print("\n=== FERDIG ===")
