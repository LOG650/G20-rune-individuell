"""
Figur 7.1: Fordeling av operatorbindingstid per beredskapsoppdrag
=================================================================
Reproduserer 'bindingstid_beredskap_fordeling_v2.png' med stoerre,
lesbar tekst (utskriftsvennlig). Datametoden er identisk med
konflikt_total_belastning.py sin D-pri1/D-aba-klassifisering:

  Beredskapsoppdrag (D) = D-pri1 (ikke-ABA utrykning) + D-aba (ABA-utrykning,
  Kilde=Alarm). Bindingstid = (Forste_ressurs_fremme - Dato_og_Tid), klippet
  til [0, 180] min, manglende imputert med global median over D, pluss 3 min
  kvitteringsvindu. n = 7 555.

Skriver bare figuren; ingen CSV/tallgrunnlag roeres.
"""
import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# === KONFIGURASJON (speiler konflikt_total_belastning.py) ===
PROJECT = pathlib.Path(r"C:\Users\runeg\OneDrive\Documents\Skole utdanning"
                       r"\Logistikk studie\LOG650 LOGISTIKK OG KI"
                       r"\G20-rune-individuell")
DATA_DIR = PROJECT / "004 data"
FIG_DIR = PROJECT / "analyse" / "figurer"
FIG_DIR.mkdir(parents=True, exist_ok=True)

KVITTERING_MIN = 3.0  # kvitteringsvindu etter forste ressurs fremme

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


def klassifiser(row):
    """D-aba: ressursvarslet + Opprinnelig starter med 'ABA' + Kilde=Alarm.
    D-pri1: ovrige utrykninger. Identisk med konflikt_total_belastning.py."""
    if pd.notna(row["Ressurs_varslet"]):
        oot = str(row["Opprinnelig_oppdragstype"]).strip() if pd.notna(row["Opprinnelig_oppdragstype"]) else ""
        kilde = str(row["Kilde"]).strip() if pd.notna(row["Kilde"]) else ""
        if oot.startswith("ABA") and kilde == "Alarm":
            return "D-aba"
        return "D-pri1"
    return "annet"


def last_data():
    files = list(DATA_DIR.glob("110*TESTDATASETT.xlsx"))
    df = pd.read_excel(files[0], engine="openpyxl", skiprows=2)
    df.columns = COLS
    for c in ["Dato_og_Tid", "Ressurs_varslet", "Forste_ressurs_fremme"]:
        df[c] = pd.to_datetime(df[c], errors="coerce")
    df["v3_kat"] = df.apply(klassifiser, axis=1)
    return df


def beregn_bindingstid(df):
    D = df[df["v3_kat"].isin(["D-pri1", "D-aba"])].copy()
    raw = (D["Forste_ressurs_fremme"] - D["Dato_og_Tid"]).dt.total_seconds() / 60
    raw = raw.where((raw >= 0) & (raw <= 180), np.nan)   # klipp avvisende verdier
    raw = raw.fillna(raw.median())                        # median-imputering over D
    D["bind"] = raw + KVITTERING_MIN
    return D


# === FIGUR ===
BINS = [0, 5, 8, 10, 13, 16, 20, 25, 30, 45, 60, np.inf]
LABELS = ["0-5", "5-8", "8-10", "10-13", "13-16", "16-20",
          "20-25", "25-30", "30-45", "45-60", "60+"]


def lag_figur(D):
    n = len(D)
    cut = pd.cut(D["bind"], bins=BINS, labels=LABELS, right=False)
    antall = cut.value_counts().reindex(LABELS).astype(int)
    pct = antall / n * 100

    sns.set_style("whitegrid")
    farger = plt.cm.RdYlGn_r(np.linspace(0.08, 0.92, len(LABELS)))

    fig, ax = plt.subplots(figsize=(12.5, 7.2))
    x = np.arange(len(LABELS))
    bars = ax.bar(x, antall.values, color=farger, edgecolor="#333333", linewidth=0.8, width=0.82)

    # Verdietiketter: antall + prosent (norsk komma), godt over soylen
    topp = antall.max()
    for xi, (a, p) in enumerate(zip(antall.values, pct.values)):
        ax.text(xi, a + topp * 0.012,
                f"{a:,}".replace(",", " ") + f"\n{p:.1f} %".replace(".", ","),
                ha="center", va="bottom", fontsize=12, fontweight="bold",
                color="#222222", linespacing=1.15)

    ax.set_ylim(0, topp * 1.18)   # headroom slik at etikettene ikke overlapper toppen
    ax.set_xticks(x)
    ax.set_xticklabels(LABELS, fontsize=13)
    ax.set_xlabel("Bindingstid (minutter), inkludert 3 min kvitteringsvindu", fontsize=15, labelpad=10)
    ax.set_ylabel("Antall beredskapsoppdrag", fontsize=15, labelpad=10)
    ax.tick_params(axis="y", labelsize=12.5)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{int(v):,}".replace(",", " ")))

    ax.set_title(
        "Fordeling av operatørbindingstid per beredskapsoppdrag\n"
        f"110 Sør-Vest 2025 (n = {n:,}".replace(",", " ") + ", D-pri1 og D-aba)",
        fontsize=17, fontweight="bold", pad=16,
    )

    fig.tight_layout()
    ut = FIG_DIR / "bindingstid_beredskap_fordeling_v2.png"
    fig.savefig(ut, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return n, antall, pct, ut


if __name__ == "__main__":
    df = last_data()
    D = beregn_bindingstid(df)
    n, antall, pct, ut = lag_figur(D)
    # D-pri1-statistikk rapporteres paa D-pri1s EGNE observerte verdier
    # (ikke global imputering), slik at tallene samsvarer med rapportens
    # D-pri1-parameter (median ca. 14 min inkl. kvittering).
    dp = df[df["v3_kat"] == "D-pri1"]
    dp_raw = (dp["Forste_ressurs_fremme"] - dp["Dato_og_Tid"]).dt.total_seconds() / 60
    dp_obs = dp_raw.where((dp_raw >= 0) & (dp_raw <= 180), np.nan).dropna()
    print(f"n (D-pri1 + D-aba) = {n}")
    print(f"D-pri1 (observert, n={len(dp_obs)}): median bind (+3 min) = {dp_obs.median() + KVITTERING_MIN:.1f}, "
          f"P90 = {dp_obs.quantile(0.9) + KVITTERING_MIN:.1f}")
    print("Bin / antall / pct:")
    for l in LABELS:
        print(f"  {l:7s} {int(antall[l]):5d}  {pct[l]:5.1f} %")
    print(f"Lagret: {ut}")
