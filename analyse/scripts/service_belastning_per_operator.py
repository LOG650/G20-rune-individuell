# -*- coding: utf-8 -*-
"""
=====================================================================
  DIVERSE ANALYSER: Service-belastning per 110-sentral, volum + per operatør
=====================================================================
  Én figur som viser to ting samtidig for alle 12 sentraler (ukedager 2025):
    - Hele søylens lengde = antall service-anrop per ukedag i 07-19 (volum).
    - Søylen er delt i like blokker, én per effektiv dagoperatør.
      Bredden på én blokk = belastning per operatør (samme x-akse).

  Datakilder:
    - BRIS 2025 alle sentraler: 004 data/2025_fullrapport_110_alle_sentraler_fra_dsb.xlsx
      (Oppdragstype == "Service", ukedager = Ukedagsnr 1-5, time = "Time på døgnet")
    - Dagbemanning hverdager: DSB årsrapport 2025 (MOB). Se DAG-ordboken.

  Antagelse (jf. primærcasen): hver sentral har én vaktleder som normalt
  IKKE besvarer service -> c_eff = dagoperatører - 1.

  Utdata: diverse analyser/service_belastning_per_operator.png
=====================================================================
"""
import pathlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch

PROJECT = pathlib.Path(r"C:\Users\runeg\OneDrive\Documents\Skole utdanning"
                       r"\Logistikk studie\LOG650 LOGISTIKK OG KI\G20-rune-individuell")
DATA_DIR = PROJECT / "004 data"
OUT_DIR = PROJECT / "diverse analyser"
SRC = DATA_DIR / "2025_fullrapport_110_alle_sentraler_fra_dsb.xlsx"
FIG_PATH = OUT_DIR / "service_belastning_per_operator.png"

# Dagbemanning hverdager (totalt inkl. vaktleder) fra DSB årsrapport 2025 (MOB).
DAG = {"Sør-Vest": 4, "Vest": 4, "Sør-Øst": 6, "Møre og Romsdal": 4,
       "Nordland": 3, "Innlandet": 4, "Midt-Norge": 4, "Øst": 6,
       "Agder": 4, "Oslo": 5, "Tromsø": 2, "Finnmark": 3}

# === 1. LAST + FILTRER ========================================================
df = pd.read_excel(SRC, engine="openpyxl", header=0)
df.columns = [str(c).strip() for c in df.columns]
df["ot"] = df["Oppdragstype"].astype(str).str.strip()
df["kort"] = df["110-sentral"].astype(str).str.strip().str.replace(" 110", "", regex=False)
df["ukedag"] = pd.to_numeric(df["Ukedagsnr"], errors="coerce")
df["hour"] = pd.to_numeric(df["Time på døgnet"], errors="coerce")
df["dato"] = pd.to_datetime(df["Dato anrop"], errors="coerce")

wd = df["ukedag"].between(1, 5)
ndays = df[wd]["dato"].dt.date.nunique()                      # operasjonsdager (ukedager)
sv = df[(df["ot"] == "Service") & wd & df["hour"].between(7, 18)]   # 07-19

# === 2. VOLUM OG BELASTNING PER SENTRAL =======================================
rows = []
for kort, dag in DAG.items():
    tot = (sv["kort"] == kort).sum() / ndays          # service/ukedag i 07-19
    ceff = max(dag - 1, 1)                             # VL svarer normalt ikke service
    rows.append(dict(sentral=kort, tot=tot, dag=dag, ceff=ceff, per=tot / ceff))
t = pd.DataFrame(rows).set_index("sentral").sort_values("per")   # størst øverst

# === 3. FIGUR =================================================================
plt.rcParams.update({"font.family": "DejaVu Sans"})
RED = ["#c62828", "#e35858"]
GREY = ["#7d8794", "#9aa3b0"]
H = 0.62

fig, ax = plt.subplots(figsize=(12.5, 7.4))
for i, (kort, r) in enumerate(t.iterrows()):
    is_sv = (kort == "Sør-Vest")
    pal = RED if is_sv else GREY
    for k in range(int(r.ceff)):
        ax.add_patch(Rectangle((k * r.per, i - H / 2), r.per, H,
                     facecolor=pal[k % 2], edgecolor="white", linewidth=1.8, zorder=3))
    ax.text(r.tot + 1.2, i, f"{r.per:.1f}".replace(".", ",") + " /operatør",
            va="center", ha="left", fontsize=10, fontweight="bold",
            color=("#c62828" if is_sv else "#333"))
    ax.text(r.tot + 1.2, i - 0.30, f"{r.tot:.0f}/dag · {int(r.ceff)} operatører",
            va="center", ha="left", fontsize=8, color="#777")

# bracket på Sør-Vest sin første blokk = én operatørs andel
sv_i = list(t.index).index("Sør-Vest")
svr = t.loc["Sør-Vest"]
ax.annotate("", xy=(0, sv_i + H / 2 + 0.18), xytext=(svr.per, sv_i + H / 2 + 0.18),
            arrowprops=dict(arrowstyle="<->", color="#c62828", lw=1.4))
ax.text(svr.per / 2, sv_i + H / 2 + 0.42, "én operatørs andel", ha="center",
        fontsize=8.5, color="#c62828", style="italic")

ax.set_yticks(range(len(t)))
ax.set_yticklabels(t.index, fontsize=10.5)
ax.set_ylim(-0.7, len(t) - 0.3)
ax.set_xlim(0, t["tot"].max() * 1.30)
ax.set_xlabel("Service-anrop per ukedag i 07–19  "
              "(hele søylen = volum · bredden på én blokk = anrop per operatør)", fontsize=10)
ax.set_title("110-sentralenes servicebelastning i én figur: volum og per operatør\n"
             "Søylelengde = service per dag · hver blokk = én operatørs andel "
             "(dagoperatører minus vaktleder)", fontweight="bold", fontsize=12.5, pad=14)
ax.grid(axis="x", color="#e6e6e6", zorder=0)
ax.set_axisbelow(True)
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.legend(handles=[Patch(facecolor=RED[0], label="Sør-Vest"),
                   Patch(facecolor=GREY[0], label="Øvrige sentraler"),
                   Patch(facecolor="white", edgecolor="#bbb", label="Hver blokk = 1 effektiv operatør")],
          loc="lower right", fontsize=9, frameon=True)
fig.text(0.012, 0.012,
         "Kilde: BRIS 2025 (Oppdragstype = Service, ukedager) + DSB årsrapport 2025 (dagbemanning hverdager). "
         "Antagelse: hver sentral har én vaktleder som normalt ikke besvarer service (c_eff = dagoperatører − 1).",
         fontsize=7.3, color="#888")
plt.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig(FIG_PATH, dpi=150)
plt.close(fig)

print(f"Lagret figur: {FIG_PATH}")
print(f"Grunnlag: {len(sv)} serviceanrop (07-19, ukedager), {ndays} ukedager.")
print(t.assign(tot=t["tot"].round(1), per=t["per"].round(1)).to_string())
