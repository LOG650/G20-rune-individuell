"""
Kapasitetsmodell for 110-sentraler
====================================
Prosedyrbasert ankomstkonfliktmodell med skjulte anrop.

Bruk:
    python kapasitetsmodell_110.py <BRIS-fil.xlsx> [--output <mappe>]

Programmet:
  1. Laster BRIS/LEO-datasett (Excel)
  2. Identifiserer beredskapsoppdrag (kategori D) og skjulte anrop (sekvensgap)
  3. Beregner bindingstider fra data (anrop -> forste ressurs fremme + kvittering)
  4. Kjorer ankomstkonfliktmodell for ulike bemanningsnivaer
  5. Produserer dimensjoneringskurve, figurer og oppsummeringstabeller

Modellen maler P(brudd pa driftsstandard ved ankomst): sannsynligheten for
at et anrop ankommer nar operatorkapasiteten allerede er bundet.

Akseptabelt serviceniva er en politisk/ledelsesmessig beslutning.
Modellen leverer det kvantitative grunnlaget for a ta et informert valg.

Forfatter: Rune Grodem, LOG650 G20, Hogskolen i Molde, 2026
"""
import argparse
import pathlib
import sys
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns


# ============================================================
# KONFIGURASJON
# ============================================================
KVITTERING_MIN = 3.0       # minutter etter forste ressurs fremme
SKJULT_BIND_MIN = 1.0      # bindingstid for sammenstilte anrop
MAX_BIND_MIN = 180.0        # maks rimelig bindingstid (3 timer)
SKIFT_DAG_START = 7         # dagskift starter kl 07
SKIFT_DAG_SLUTT = 18       # dagskift slutter kl 18 (19:00 = nattskift)

C_EFF_RANGE = range(2, 7)  # bemanningsnivaer a teste (2-6)


def _update_params(skjult_bind, kvittering):
    global SKJULT_BIND_MIN, KVITTERING_MIN
    SKJULT_BIND_MIN = skjult_bind
    KVITTERING_MIN = kvittering


# ============================================================
# DATALASTING OG KLARGJORING
# ============================================================
def last_bris_data(filsti):
    """Laster BRIS/LEO Excel-fil og returnerer klargjort DataFrame."""
    print(f"Laster {filsti.name}...")
    df = pd.read_excel(filsti, engine="openpyxl", skiprows=2)

    # Standardiser kolonnenavn (36 kolonner i BRIS-format)
    forventede = [
        "Oppdrag_ID", "110_ID", "Opprinnelig_oppdragstype", "Oppdragstype",
        "Overordnet_oppdragstype", "Kategori_oppdrag", "Adresseobjekt",
        "Postnr", "Poststed", "Kommunenavn", "Kommunenr", "Kommunenr_navn",
        "Fylke", "Ansvarlig_brannvesen", "110_sentral", "Kilde",
        "Time_paa_dognet", "Dato_anrop", "Tid_anrop", "Dato_og_Tid",
        "Ukedagsnr", "Ukedag", "Maanedsnr", "Maaned", "Anrop_aar",
        "Utvarslede_ressurser", "Antall_ressurser_paa_stedet",
        "Oppdrag_opprettet", "Ressurs_varslet", "Rykket_ut",
        "Forste_ressurs_fremme", "Siste_ressurs_ledig",
        "Alarmbehandlingstid", "Utrykningstid", "Responstid",
        "Forspenningstid",
    ]
    if len(df.columns) == len(forventede):
        df.columns = forventede
    else:
        print(f"  ADVARSEL: Forventet {len(forventede)} kolonner, fant {len(df.columns)}")
        print(f"  Forsok a bruke eksisterende kolonnenavn")

    # Parse datetimes
    for c in ["Dato_og_Tid", "Ressurs_varslet", "Forste_ressurs_fremme",
              "Siste_ressurs_ledig"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")

    # Time og skift
    df["Time"] = pd.to_numeric(df.get("Time_paa_dognet", pd.Series(dtype=float)),
                               errors="coerce").astype("Int64")
    df["Skift"] = np.where(df["Time"].between(SKIFT_DAG_START, SKIFT_DAG_SLUTT),
                           "Dag", "Natt")

    # Ukedag og helg
    df["Ukedagsnr_int"] = pd.to_numeric(df.get("Ukedagsnr", pd.Series(dtype=float)),
                                        errors="coerce").astype("Int64")
    df["Er_helg"] = df["Ukedagsnr_int"].isin([6, 7])

    # Sekvensnummer fra 110_ID
    if "110_ID" in df.columns:
        df["dato_id"] = df["110_ID"].str.extract(r"B\d+-(\d{6})-")[0]
        df["seq_nr"] = df["110_ID"].str.extract(r"B\d+-\d{6}-(\d+)")[0].astype(float)

    sentral = "ukjent"
    if "110_sentral" in df.columns:
        sentral = df["110_sentral"].dropna().mode()
        sentral = sentral.iloc[0] if len(sentral) > 0 else "ukjent"

    print(f"  Sentral: {sentral}")
    print(f"  Synlige oppdrag: {len(df)}")
    print(f"  Periode: {df['Dato_og_Tid'].min()} - {df['Dato_og_Tid'].max()}")

    return df, sentral


def identifiser_skjulte_anrop(df):
    """Identifiserer sammenstilte anrop via sekvensgap i 110_ID."""
    if "seq_nr" not in df.columns or "dato_id" not in df.columns:
        print("  ADVARSEL: Kan ikke identifisere skjulte anrop (mangler 110_ID)")
        return pd.DataFrame()

    hidden_rows = []
    for dato, group in df.groupby("dato_id"):
        seqs = set(group["seq_nr"].dropna().astype(int))
        if not seqs:
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
                "kilde": "skjult",
            })

    hdf = pd.DataFrame(hidden_rows)
    if len(hdf) > 0:
        hdf["Dato_og_Tid"] = pd.to_datetime(hdf["Dato_og_Tid"])
        hdf["Time"] = hdf["Dato_og_Tid"].dt.hour
        hdf["Skift"] = np.where(hdf["Time"].between(SKIFT_DAG_START, SKIFT_DAG_SLUTT),
                                "Dag", "Natt")
        hdf["Er_helg"] = hdf["Dato_og_Tid"].dt.dayofweek >= 5

    korreksjon = (len(df) + len(hdf)) / len(df) if len(df) > 0 else 1.0
    print(f"  Skjulte/sammenstilte anrop: {len(hdf)} (korreksjonsfaktor {korreksjon:.3f}x)")

    return hdf


def beregn_bindingstider(df):
    """Beregner bindingstid for kategori D-hendelser."""
    bered = df[df["Ressurs_varslet"].notna()].copy()

    bered["bind_raa"] = (
        (bered["Forste_ressurs_fremme"] - bered["Dato_og_Tid"]).dt.total_seconds() / 60
    )
    bered.loc[bered["bind_raa"] < 0, "bind_raa"] = np.nan
    bered.loc[bered["bind_raa"] > MAX_BIND_MIN, "bind_raa"] = np.nan

    has_fremme = bered["bind_raa"].notna()
    median_bind = bered.loc[has_fremme, "bind_raa"].median() if has_fremme.any() else 10.0
    bered.loc[~has_fremme, "bind_raa"] = median_bind
    bered["bind_min"] = bered["bind_raa"] + KVITTERING_MIN
    bered["kilde"] = "kategori_D"

    print(f"  Kategori D: {len(bered)} oppdrag")
    print(f"  Bindingstid median: {bered['bind_min'].median():.1f} min (inkl +{KVITTERING_MIN:.0f} min kvittering)")
    print(f"  Faktisk fremme-tid tilgjengelig: {has_fremme.sum()} ({has_fremme.mean()*100:.1f}%)")

    return bered


# ============================================================
# KAPASITETSMODELL
# ============================================================
def beregn_n_aktive(combined):
    """Beregner antall samtidige aktive hendelser ved hvert ankomsttidspunkt."""
    combined = combined.sort_values("Dato_og_Tid").reset_index(drop=True)
    combined["slutt_ts"] = combined["Dato_og_Tid"] + pd.to_timedelta(combined["bind_min"], unit="m")

    n = len(combined)
    ankomst = combined["Dato_og_Tid"].values
    slutt = combined["slutt_ts"].values

    n_aktive = np.zeros(n, dtype=int)
    active_set = []
    for i in range(n):
        t_i = ankomst[i]
        active_set = [s for s in active_set if s > t_i]
        n_aktive[i] = len(active_set)
        active_set.append(slutt[i])

    combined["n_aktive"] = n_aktive
    return combined


def klassifiser_kapasitet(n_aktive_arr, c_eff_arr):
    """Klassifiserer kapasitetsniva basert pa ledige operatorer."""
    result = []
    for na, ce in zip(n_aktive_arr, c_eff_arr):
        ledige = ce - na
        if ledige >= 2:
            result.append("Normal")
        elif ledige == 1:
            result.append("Brudd")
        else:
            result.append("Svikt")
    return np.array(result)


def dimensjoneringskurve(combined, c_range=C_EFF_RANGE):
    """Beregner kapasitetsniva for ulike bemanningsnivaer."""
    dag_hverdag = ((combined["Skift"] == "Dag") & (~combined["Er_helg"])).values
    n_aktive = combined["n_aktive"].values
    n = len(combined)

    results = []
    for c_dag in c_range:
        for c_natt in c_range:
            if c_natt > c_dag:
                continue
            c_eff = np.where(dag_hverdag, c_dag, c_natt)
            kap = klassifiser_kapasitet(n_aktive, c_eff)

            for subset_name, mask in [("Alle", np.ones(n, bool)),
                                       ("Dag_hverdag", dag_hverdag),
                                       ("Natt_helg", ~dag_hverdag)]:
                s = kap[mask]
                t = len(s)
                results.append({
                    "c_dag": c_dag, "c_natt": c_natt,
                    "subset": subset_name, "n": t,
                    "Normal_pct": (s == "Normal").sum() / t * 100,
                    "Brudd_pct": (s == "Brudd").sum() / t * 100,
                    "Svikt_pct": (s == "Svikt").sum() / t * 100,
                })

    return pd.DataFrame(results)


# ============================================================
# FIGURER
# ============================================================
def lag_figurer(combined, dim_df, sentral, output_dir):
    """Produserer alle figurer."""
    sns.set_style("whitegrid")
    plt.rcParams.update({"figure.dpi": 150, "font.size": 10})

    dag_hverdag = ((combined["Skift"] == "Dag") & (~combined["Er_helg"])).values
    n_aktive = combined["n_aktive"].values
    n = len(combined)

    # --- Figur 1: Dimensjoneringskurve ---
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))

    for ax, subset in zip(axes, ["Alle", "Dag_hverdag", "Natt_helg"]):
        sub = dim_df[(dim_df["subset"] == subset) & (dim_df["c_dag"] == dim_df["c_natt"])]
        sub = sub.sort_values("c_dag")
        ax.fill_between(sub["c_dag"], 0, sub["Svikt_pct"],
                        color="#d32f2f", alpha=0.3, label="Svikt")
        ax.fill_between(sub["c_dag"], sub["Svikt_pct"],
                        sub["Svikt_pct"] + sub["Brudd_pct"],
                        color="#ff9800", alpha=0.3, label="Brudd")
        ax.plot(sub["c_dag"], sub["Normal_pct"], "o-", color="#4caf50",
                lw=2.5, ms=8, label="Normal (%)")
        ax.plot(sub["c_dag"], sub["Svikt_pct"], "s--", color="#d32f2f",
                lw=2, ms=6, label="Svikt (%)")

        # Referanselinjer
        ax.axhline(80, color="gray", ls=":", alpha=0.5, label="80% ref.")
        ax.axhline(5, color="gray", ls=":", alpha=0.3)

        for _, r in sub.iterrows():
            ax.annotate(f"{r['Normal_pct']:.0f}%",
                       (r["c_dag"], r["Normal_pct"]),
                       textcoords="offset points", xytext=(0, 10),
                       ha="center", fontsize=8, fontweight="bold",
                       color="#2e7d32")
            ax.annotate(f"{r['Svikt_pct']:.0f}%",
                       (r["c_dag"], r["Svikt_pct"]),
                       textcoords="offset points", xytext=(0, -14),
                       ha="center", fontsize=8, color="#c62828")

        title_map = {"Alle": "Alle anrop", "Dag_hverdag": "Dag hverdag",
                     "Natt_helg": "Natt/helg"}
        ax.set_title(title_map[subset], fontsize=12, fontweight="bold")
        ax.set_xlabel("Antall operatorer (c_eff)")
        ax.set_ylabel("Andel (%)")
        ax.set_ylim(0, 105)
        ax.set_xticks(list(C_EFF_RANGE))
        if ax == axes[0]:
            ax.legend(fontsize=8, loc="center right")

    fig.suptitle(f"Dimensjoneringskurve - {sentral}\n"
                 f"Andel normal/brudd/svikt som funksjon av bemanning",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig.savefig(output_dir / "dimensjoneringskurve.png", bbox_inches="tight")
    print(f"  Figur: {output_dir / 'dimensjoneringskurve.png'}")

    # --- Figur 2: Kapasitet per time (dagens bemanning) ---
    # Bruk c_dag=3, c_natt=2 som default
    c_eff = np.where(dag_hverdag, 3, 2)
    kap = klassifiser_kapasitet(n_aktive, c_eff)

    fig, ax = plt.subplots(figsize=(13, 5.5))
    hourly = []
    for t in range(24):
        mask = combined["Time"].values == t
        s = kap[mask]
        if len(s) == 0:
            continue
        hourly.append({
            "Time": t, "n": len(s),
            "Normal": (s == "Normal").sum() / len(s) * 100,
            "Brudd": (s == "Brudd").sum() / len(s) * 100,
            "Svikt": (s == "Svikt").sum() / len(s) * 100,
        })
    hdf = pd.DataFrame(hourly)

    ax.bar(hdf["Time"], hdf["Normal"], color="#4caf50", alpha=0.8, label="Normal")
    ax.bar(hdf["Time"], hdf["Brudd"], bottom=hdf["Normal"],
           color="#ff9800", alpha=0.8, label="Brudd")
    ax.bar(hdf["Time"], hdf["Svikt"], bottom=hdf["Normal"] + hdf["Brudd"],
           color="#d32f2f", alpha=0.8, label="Svikt")

    ax2 = ax.twinx()
    ax2.plot(hdf["Time"], hdf["n"], "ko-", ms=4, lw=1.2, alpha=0.4)
    ax2.set_ylabel("Antall", color="gray")

    ax.axvspan(SKIFT_DAG_START, SKIFT_DAG_SLUTT + 0.99, alpha=0.05, color="blue")
    ax.set_xlabel("Time pa dognet")
    ax.set_ylabel("Andel (%)")
    ax.set_title(f"Kapasitetsniva per time - {sentral}\n"
                 f"Dagens bemanning (dag c=3, natt/helg c=2)",
                 fontsize=12, fontweight="bold")
    ax.legend(loc="lower left", fontsize=9)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.set_xlim(-0.5, 23.5)
    ax.set_ylim(0, 105)
    plt.tight_layout()
    fig.savefig(output_dir / "kapasitet_per_time.png", bbox_inches="tight")
    print(f"  Figur: {output_dir / 'kapasitet_per_time.png'}")

    # --- Figur 3: Bindingstid-histogram ---
    kat_d = combined[combined["kilde"] == "kategori_D"]
    fig, ax = plt.subplots(figsize=(10, 5))
    data = kat_d["bind_min"].dropna()
    ax.hist(data[data <= 60], bins=50, color="#1565c0", alpha=0.7, edgecolor="white")
    ax.axvline(data.median(), color="black", ls="--", lw=1.5,
               label=f"Median: {data.median():.1f} min")
    ax.axvline(data.quantile(0.9), color="black", ls=":", lw=1.5,
               label=f"P90: {data.quantile(0.9):.1f} min")
    ax.set_xlabel("Bindingstid (minutter)")
    ax.set_ylabel("Antall oppdrag")
    ax.set_title(f"Bindingstid kategori D - {sentral}", fontsize=12, fontweight="bold")
    ax.legend()
    plt.tight_layout()
    fig.savefig(output_dir / "bindingstid_fordeling.png", bbox_inches="tight")
    print(f"  Figur: {output_dir / 'bindingstid_fordeling.png'}")

    plt.close("all")


# ============================================================
# RAPPORT
# ============================================================
def skriv_rapport(combined, dim_df, sentral, output_dir):
    """Skriver oppsummeringsrapport til tekstfil."""
    dag_hverdag = ((combined["Skift"] == "Dag") & (~combined["Er_helg"])).values
    n_aktive = combined["n_aktive"].values
    n = len(combined)
    n_kat_d = (combined["kilde"] == "kategori_D").sum()
    n_skjult = (combined["kilde"] == "skjult").sum()

    lines = []
    lines.append(f"KAPASITETSANALYSE - {sentral}")
    lines.append(f"Generert: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"Datagrunnlag:")
    lines.append(f"  Kategori D (beredskapsoppdrag):  {n_kat_d:>6}")
    lines.append(f"  Skjulte/sammenstilte anrop:      {n_skjult:>6}")
    lines.append(f"  Totalt analyserte belastninger:   {n:>6}")
    lines.append(f"  Korreksjonsfaktor:               {(n_kat_d + n_skjult) / max(n_kat_d, 1):.3f}x")
    lines.append("")

    # Bindingstid
    kat_d = combined[combined["kilde"] == "kategori_D"]
    bt = kat_d["bind_min"]
    lines.append("Bindingstid kategori D (inkl kvittering):")
    for p, label in [(0.1, "P10"), (0.25, "P25"), (0.5, "Median"),
                     (0.75, "P75"), (0.9, "P90"), (0.95, "P95")]:
        lines.append(f"  {label:>6}: {bt.quantile(p):>6.1f} min")
    lines.append(f"  Skjulte anrop bindingstid: {SKJULT_BIND_MIN:.1f} min")
    lines.append("")

    # Dagens bemanning
    lines.append("DAGENS BEMANNING (dag c=3, natt/helg c=2):")
    lines.append("-" * 50)
    c_eff = np.where(dag_hverdag, 3, 2)
    kap = klassifiser_kapasitet(n_aktive, c_eff)
    for label, mask in [("Alle", np.ones(n, bool)),
                         ("Dag hverdag (c=3)", dag_hverdag),
                         ("Natt/helg (c=2)", ~dag_hverdag)]:
        s = kap[mask]
        t = len(s)
        lines.append(f"  {label:>22}: Normal={((s=='Normal').sum()/t*100):>5.1f}%  "
                     f"Brudd={((s=='Brudd').sum()/t*100):>5.1f}%  "
                     f"Svikt={((s=='Svikt').sum()/t*100):>5.1f}%  (n={t})")
    lines.append("")

    # Dimensjoneringskurve
    lines.append("DIMENSJONERINGSKURVE (c_dag = c_natt):")
    lines.append("-" * 70)
    lines.append(f"{'c_eff':>6} | {'Normal':>8} {'Brudd':>8} {'Svikt':>8} | "
                 f"{'Norm_dag':>9} {'Svikt_dag':>10} | {'Norm_natt':>10} {'Svikt_natt':>11}")
    lines.append("-" * 70)
    for c in C_EFF_RANGE:
        alle = dim_df[(dim_df["c_dag"] == c) & (dim_df["c_natt"] == c) & (dim_df["subset"] == "Alle")]
        dag = dim_df[(dim_df["c_dag"] == c) & (dim_df["c_natt"] == c) & (dim_df["subset"] == "Dag_hverdag")]
        natt = dim_df[(dim_df["c_dag"] == c) & (dim_df["c_natt"] == c) & (dim_df["subset"] == "Natt_helg")]
        if len(alle) > 0:
            a, d, nn = alle.iloc[0], dag.iloc[0], natt.iloc[0]
            lines.append(f"  {c:>4} | {a['Normal_pct']:>7.1f}% {a['Brudd_pct']:>7.1f}% "
                        f"{a['Svikt_pct']:>7.1f}% | {d['Normal_pct']:>8.1f}% "
                        f"{d['Svikt_pct']:>9.1f}% | {nn['Normal_pct']:>9.1f}% "
                        f"{nn['Svikt_pct']:>10.1f}%")
    lines.append("")

    # Realistiske kombinasjoner
    lines.append("REALISTISKE BEMANNINGSSCENARIOER:")
    lines.append("-" * 70)
    scenarios = [
        ("Dagens (3/2)", 3, 2),
        ("+1 alle (4/3)", 4, 3),
        ("+2 alle (5/4)", 5, 4),
        ("+1 natt (3/3)", 3, 3),
        ("+1 dag (4/2)", 4, 2),
    ]
    for name, cd, cn in scenarios:
        a = dim_df[(dim_df["c_dag"]==cd)&(dim_df["c_natt"]==cn)&(dim_df["subset"]=="Alle")]
        nn = dim_df[(dim_df["c_dag"]==cd)&(dim_df["c_natt"]==cn)&(dim_df["subset"]=="Natt_helg")]
        if len(a) > 0:
            lines.append(f"  {name:>20}: Normal={a.iloc[0]['Normal_pct']:>5.1f}%  "
                        f"Svikt={a.iloc[0]['Svikt_pct']:>5.1f}%  "
                        f"(natt: Normal={nn.iloc[0]['Normal_pct']:>5.1f}% "
                        f"Svikt={nn.iloc[0]['Svikt_pct']:>5.1f}%)")

    lines.append("")
    lines.append("MERK: Akseptabelt serviceniva er en politisk/ledelsesmessig beslutning.")
    lines.append("Modellen leverer det kvantitative grunnlaget for a ta et informert valg.")
    lines.append("Resultatene er et minimumsanslag - faktisk belastning er sannsynligvis hoyere.")

    rapport = "\n".join(lines)
    rapport_fil = output_dir / "kapasitetsrapport.txt"
    rapport_fil.write_text(rapport, encoding="utf-8")
    print(f"  Rapport: {rapport_fil}")
    print()
    print(rapport)


# ============================================================
# HOVEDPROGRAM
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="Kapasitetsmodell for 110-sentraler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("bris_fil", type=pathlib.Path,
                       help="Sti til BRIS/LEO Excel-fil (.xlsx)")
    parser.add_argument("--output", type=pathlib.Path, default=None,
                       help="Utdata-mappe (default: ./output)")
    parser.add_argument("--skjult-bind", type=float, default=SKJULT_BIND_MIN,
                       help=f"Bindingstid for sammenstilte anrop i minutter (default: {SKJULT_BIND_MIN})")
    parser.add_argument("--kvittering", type=float, default=KVITTERING_MIN,
                       help=f"Kvitteringstid etter forste ressurs fremme (default: {KVITTERING_MIN})")
    parser.add_argument("--c-dag", type=int, default=3,
                       help="Dagens c_eff dagskift hverdag (default: 3)")
    parser.add_argument("--c-natt", type=int, default=2,
                       help="Dagens c_eff nattskift/helg (default: 2)")

    args = parser.parse_args()

    # Oppdater modulniva-parametere
    _update_params(args.skjult_bind, args.kvittering)

    if not args.bris_fil.exists():
        print(f"FEIL: Finner ikke {args.bris_fil}")
        sys.exit(1)

    output_dir = args.output or pathlib.Path("./output")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("KAPASITETSMODELL FOR 110-SENTRALER")
    print("=" * 70)
    print()

    # 1. Last data
    df, sentral = last_bris_data(args.bris_fil)

    # 2. Identifiser skjulte anrop
    print()
    hidden_df = identifiser_skjulte_anrop(df)

    # 3. Beregn bindingstider
    print()
    bered = beregn_bindingstider(df)

    # 4. Kombiner
    bered_slim = bered[["Dato_og_Tid", "bind_min", "kilde", "Time", "Skift", "Er_helg"]].copy()
    if len(hidden_df) > 0:
        hidden_slim = hidden_df[["Dato_og_Tid", "bind_min", "kilde", "Time", "Skift", "Er_helg"]].copy()
        combined = pd.concat([bered_slim, hidden_slim], ignore_index=True)
    else:
        combined = bered_slim.copy()
    combined = combined.sort_values("Dato_og_Tid").reset_index(drop=True)

    # 5. Beregn n_aktive
    print(f"\nBeregner samtidige hendelser for {len(combined)} belastningsenheter...")
    combined = beregn_n_aktive(combined)

    # 6. Dimensjoneringskurve
    print("Beregner dimensjoneringskurve...")
    dim_df = dimensjoneringskurve(combined)
    dim_df.to_csv(output_dir / "dimensjoneringskurve.csv", index=False, encoding="utf-8")

    # 7. Figurer
    print("\nGenererer figurer...")
    lag_figurer(combined, dim_df, sentral, output_dir)

    # 8. Rapport
    print("\nGenererer rapport...")
    skriv_rapport(combined, dim_df, sentral, output_dir)

    print(f"\n{'='*70}")
    print(f"Ferdig. Resultater lagret i {output_dir}/")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
