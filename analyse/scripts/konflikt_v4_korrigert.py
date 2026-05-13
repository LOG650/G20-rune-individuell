"""
Ankomstkonfliktmodell v4 - korrigert operativ logikk + skjulte anrop
=====================================================================
Endringer fra v3:
  1. Korrigert kapasitetsklassifisering:
     - Operatorene tilpasser seg ALLTID - makkerpar splittes ved behov
     - Normal: nok ledige til makkerpar pa neste (>=2 ledige)
     - Brudd pa driftsstandard: kun 1 ledig, solo-handtering
     - Svikt: 0 ledige, VL/Agder
     - Hver aktiv hendelse binder 1 operator (operativ virkelighet)

  2. Skjulte/sammenstilte anrop inkludert:
     - Identifisert via sekvensgap i 110_ID
     - Bindingstid 1 min (kort avklaring, innringer informeres)
     - Tidspunkt interpolert fra naermeste synlige oppdrag

Output: Figurer + statistikk for rapport
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
SKJULT_BIND_MIN = 1.0  # sammenstilt anrop: kort avklaring

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

# === 2. IDENTIFISER SKJULTE ANROP VIA SEKVENSGAP ===
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
            "bind_min": SKJULT_BIND_MIN,
            "kilde": "skjult_sammenstilt",
        })

print(f"Synlige oppdrag: {len(df)}")
print(f"Skjulte/sammenstilte anrop (sekvensgap): {len(hidden_rows)}")

# === 3. BYGG BEREDSKAPS-DATASET (kategori D) ===
bered = df[df["Ressurs_varslet"].notna()].copy()

# Bindingstid for kategori D
bered["bind_raa"] = (
    (bered["Forste_ressurs_fremme"] - bered["Dato_og_Tid"]).dt.total_seconds() / 60
)
bered.loc[bered["bind_raa"] < 0, "bind_raa"] = np.nan
bered.loc[bered["bind_raa"] > 180, "bind_raa"] = np.nan
has_fremme = bered["bind_raa"].notna()
median_bind = bered.loc[has_fremme, "bind_raa"].median()
bered.loc[~has_fremme, "bind_raa"] = median_bind
bered["bind_min"] = bered["bind_raa"] + KVITTERING_MIN
bered["kilde"] = "kategori_D"

print(f"Kategori D (beredskapsoppdrag): {len(bered)}")

# === 4. KOMBINER: kategori D + skjulte anrop ===
hidden_df = pd.DataFrame(hidden_rows)
hidden_df["Dato_og_Tid"] = pd.to_datetime(hidden_df["Dato_og_Tid"])

# For skjulte: beregn skift og c_eff
hidden_df["Time"] = hidden_df["Dato_og_Tid"].dt.hour
hidden_df["Skift"] = np.where(hidden_df["Time"].between(7, 18), "Dag", "Natt")
ukedager = hidden_df["Dato_og_Tid"].dt.dayofweek  # 0=man, 6=son
hidden_df["Er_helg"] = ukedager >= 5

# Kategori D: beregn same felter
bered_slim = bered[["Dato_og_Tid", "bind_min", "kilde", "Time", "Skift", "Er_helg"]].copy()

# Kombiner
combined = pd.concat([bered_slim, hidden_df[["Dato_og_Tid", "bind_min", "kilde", "Time", "Skift", "Er_helg"]]], ignore_index=True)
combined = combined.sort_values("Dato_og_Tid").reset_index(drop=True)

# c_eff
dag_hverdag = (combined["Skift"] == "Dag") & (~combined["Er_helg"])
combined["c_eff"] = np.where(dag_hverdag, 3, 2)

print(f"Kombinert datasett: {len(combined)} ({len(bered)} kat.D + {len(hidden_df)} skjulte)")
print()

# === 5. ANKOMSTKONFLIKTMODELL - KORRIGERT LOGIKK ===
# Operativ virkelighet: en hendelse binder normalt 2 operatorer (ROD+GUL),
# men ved samtidskonflikter splittes makkerparet. Modellen teller antall
# aktive hendelser mot c_eff for a avgjore kapasitetsniva for neste anrop.
# Normal: ledige >= 2 (makkerpar mulig for neste)
# Brudd:  ledige = 1  (solo)
# Svikt:  ledige = 0  (ingen ledig)
# ledige = c_eff - n_aktive

combined["slutt_ts"] = combined["Dato_og_Tid"] + pd.to_timedelta(combined["bind_min"], unit="m")
n = len(combined)
ankomst = combined["Dato_og_Tid"].values
slutt = combined["slutt_ts"].values
c_eff_arr = combined["c_eff"].values

n_aktive = np.zeros(n, dtype=int)
active_set = []
for i in range(n):
    t_i = ankomst[i]
    active_set = [s for s in active_set if s > t_i]
    n_aktive[i] = len(active_set)
    active_set.append(slutt[i])

combined["n_aktive"] = n_aktive

def klassifiser(n_a, c):
    ledige = c - n_a
    if ledige >= 2:
        return "Normal"
    elif ledige == 1:
        return "Brudd"
    else:
        return "Svikt"

combined["kapasitet"] = [klassifiser(na, ce) for na, ce in zip(n_aktive, c_eff_arr)]

# === 6. RESULTATER ===
order = ["Normal", "Brudd", "Svikt"]

def fordeling(label, data):
    total = len(data)
    print(f"\n{label} (n={total}):")
    for niva in order:
        nv = (data["kapasitet"] == niva).sum()
        print(f"  {niva:>10}: {nv:>6} ({nv/total*100:.1f}%)")

print("=" * 70)
print("KORRIGERT MODELL: operativ tilpasning + skjulte anrop")
print("=" * 70)

# Bare kategori D
kat_d = combined[combined["kilde"] == "kategori_D"]
fordeling("Kun kategori D (uten skjulte)", kat_d)

# Alt kombinert
fordeling("Kategori D + skjulte anrop", combined)

# Per bemanningsniva
for ce, label in [(3, "Dag hverdag (c=3)"), (2, "Natt/helg (c=2)")]:
    print(f"\n--- {label} ---")
    d_only = kat_d[kat_d["c_eff"] == ce]
    all_c = combined[combined["c_eff"] == ce]
    print(f"  Kun kat.D (n={len(d_only)}):", end="")
    for niva in order:
        nv = (d_only["kapasitet"] == niva).sum()
        print(f"  {niva}={nv/len(d_only)*100:.1f}%", end="")
    print()
    print(f"  +skjulte  (n={len(all_c)}):", end="")
    for niva in order:
        nv = (all_c["kapasitet"] == niva).sum()
        print(f"  {niva}={nv/len(all_c)*100:.1f}%", end="")
    print()

# Per time
print(f"\n{'Kl':>4} {'n_totalt':>9} {'Normal':>8} {'Brudd':>8} {'Svikt':>7}")
print("-" * 40)
for t in range(24):
    s = combined[combined["Time"] == t]
    if len(s) == 0:
        continue
    n_n = (s["kapasitet"] == "Normal").mean() * 100
    n_b = (s["kapasitet"] == "Brudd").mean() * 100
    n_s = (s["kapasitet"] == "Svikt").mean() * 100
    print(f"  {t:>2}   {len(s):>7}  {n_n:>6.1f}%  {n_b:>6.1f}%  {n_s:>5.1f}%")

# === 7. +1 SCENARIO ===
print(f"\n{'='*70}")
print("SCENARIO: +1 operator (dag 3->4, natt/helg 2->3)")
print(f"{'='*70}")

c_new = np.where(dag_hverdag, 4, 3)
kap_new = [klassifiser(na, ce) for na, ce in zip(n_aktive, c_new)]
combined["kap_pluss1"] = kap_new

for label, data in [("Alle", combined),
                     ("Dag hverdag", combined[combined["c_eff"]==3]),
                     ("Natt/helg", combined[combined["c_eff"]==2])]:
    print(f"\n{label} (n={len(data)}):")
    for niva in order:
        nv_now = (data["kapasitet"] == niva).sum()
        nv_new = (data["kap_pluss1"] == niva).sum()
        print(f"  {niva:>10}: {nv_now/len(data)*100:.1f}% -> {nv_new/len(data)*100:.1f}%")

# === 8. FIGURER ===

# Figur A: Sammenligning kat.D alene vs kat.D + skjulte
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
colors = {"Normal": "#4caf50", "Brudd": "#ff9800", "Svikt": "#d32f2f"}

for ax, (ce, label) in zip(axes, [(None, "Alle"), (3, "Dag hverdag (c=3)"), (2, "Natt/helg (c=2)")]):
    if ce is None:
        d_only = kat_d
        d_all = combined
    else:
        d_only = kat_d[kat_d["c_eff"] == ce]
        d_all = combined[combined["c_eff"] == ce]

    x = np.arange(len(order))
    width = 0.35
    vals_d = [(d_only["kapasitet"] == k).mean() * 100 for k in order]
    vals_a = [(d_all["kapasitet"] == k).mean() * 100 for k in order]

    bars1 = ax.bar(x - width/2, vals_d, width, color=[colors[k] for k in order],
                   alpha=1.0, edgecolor="white", label="Kun kat. D")
    bars2 = ax.bar(x + width/2, vals_a, width, color=[colors[k] for k in order],
                   alpha=0.5, edgecolor="black", linewidth=1.2, label="Kat. D + skjulte")

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
    ax.set_ylim(0, max(max(vals_d), max(vals_a)) * 1.25)
    if ax == axes[0]:
        ax.legend(fontsize=8)

fig.suptitle(
    "Effekt av skjulte/sammenstilte anrop pa kapasitetsniva\n"
    "Korrigert modell: operatorer tilpasser seg (1 op/hendelse, makkerpar splittes)",
    fontsize=12, fontweight="bold",
)
plt.tight_layout()
plt.savefig(FIG_DIR / "kapasitet_v4_med_skjulte.png", bbox_inches="tight")
print(f"\nFigur A: {FIG_DIR / 'kapasitet_v4_med_skjulte.png'}")

# Figur B: Per time - stacked bar
fig, ax = plt.subplots(figsize=(13, 5.5))

hourly_data = []
for t in range(24):
    s = combined[combined["Time"] == t]
    if len(s) == 0:
        continue
    hourly_data.append({
        "Time": t, "n": len(s),
        "Normal": (s["kapasitet"] == "Normal").mean() * 100,
        "Brudd": (s["kapasitet"] == "Brudd").mean() * 100,
        "Svikt": (s["kapasitet"] == "Svikt").mean() * 100,
    })
hdf = pd.DataFrame(hourly_data)

ax.bar(hdf["Time"], hdf["Normal"], color="#4caf50", alpha=0.8, label="Normal (makkerpar mulig)")
ax.bar(hdf["Time"], hdf["Brudd"], bottom=hdf["Normal"],
       color="#ff9800", alpha=0.8, label="Brudd (solo-drift)")
ax.bar(hdf["Time"], hdf["Svikt"], bottom=hdf["Normal"] + hdf["Brudd"],
       color="#d32f2f", alpha=0.8, label="Svikt (ingen ledig)")

ax2 = ax.twinx()
ax2.plot(hdf["Time"], hdf["n"], "ko-", ms=4, lw=1.2, alpha=0.4, label="Antall hendelser")
ax2.set_ylabel("Antall (kat.D + skjulte)", color="gray")

ax.axvspan(7, 18.99, alpha=0.05, color="blue")
ax.set_xlabel("Time pa dognet")
ax.set_ylabel("Andel (%)")
ax.set_title(
    "Kapasitetsniva per time - korrigert modell med skjulte anrop\n"
    "110 Sor-Vest 2025",
    fontsize=12, fontweight="bold",
)
ax.legend(loc="lower left", fontsize=9)
ax2.legend(loc="upper right", fontsize=9)
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.set_xlim(-0.5, 23.5)
ax.set_ylim(0, 105)
plt.tight_layout()
plt.savefig(FIG_DIR / "kapasitet_v4_per_time.png", bbox_inches="tight")
print(f"Figur B: {FIG_DIR / 'kapasitet_v4_per_time.png'}")

# === 9. EKSPORTER ===
summary_rows = []
for label, data in [("Alle", combined),
                     ("Dag hverdag (c=3)", combined[combined["c_eff"]==3]),
                     ("Natt/helg (c=2)", combined[combined["c_eff"]==2])]:
    n_t = len(data)
    summary_rows.append({
        "Skifttype": label, "n": n_t,
        "n_katD": (data["kilde"] == "kategori_D").sum(),
        "n_skjulte": (data["kilde"] == "skjult_sammenstilt").sum(),
        "Normal_pct": round((data["kapasitet"] == "Normal").mean() * 100, 1),
        "Brudd_pct": round((data["kapasitet"] == "Brudd").mean() * 100, 1),
        "Svikt_pct": round((data["kapasitet"] == "Svikt").mean() * 100, 1),
    })
pd.DataFrame(summary_rows).to_csv(
    PROJECT / "analyse" / "kapasitet_v4_oppsummering.csv",
    index=False, encoding="utf-8",
)
print(f"\nOppsummering: {PROJECT / 'analyse' / 'kapasitet_v4_oppsummering.csv'}")
print("\n=== FERDIG ===")
