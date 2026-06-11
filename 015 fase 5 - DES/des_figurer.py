"""
Figurer for DES-utvidelsen (Fase 5)
===================================
Leser resultat-CSV-ene fra D3/D4/D5 og lager utskriftsvennlige figurer.
Stor, lesbar tekst; norsk desimalkomma; ingen em/en-dash i titler.
"""
import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

HER = pathlib.Path(__file__).resolve().parent
FIG = HER / "figurer"
FIG.mkdir(exist_ok=True)

sns.set_style("whitegrid")
plt.rcParams.update({"figure.dpi": 150, "font.size": 12})


def _komma(x):
    return f"{x:.1f}".replace(".", ",")


def fig_bro_vs_des():
    """Sweep (statisk) vs DES (dynamisk) Normal/Brudd/Svikt + overloep/VL, natt/helg + dag."""
    d3 = pd.read_csv(HER / "d3_ci_variant_a.csv")
    # rapportens sweep-tall (Variant A)
    sweep = {"Dag_hverdag": {"Normal": 78.6, "Brudd": 14.9, "Svikt": 6.4},
             "Natt_helg": {"Normal": 69.2, "Brudd": 9.8, "Svikt": 21.0}}

    fig, axes = plt.subplots(1, 2, figsize=(13, 6.2), sharey=True)
    nivaaer = ["Normal", "Brudd", "Svikt"]
    farger = {"sweep": "#7f8c8d", "des": "#2e86de"}
    for ax, skift in zip(axes, ["Dag_hverdag", "Natt_helg"]):
        s = d3[d3["skift"] == skift].set_index("maal")
        x = np.arange(len(nivaaer))
        sw = [sweep[skift][n] for n in nivaaer]
        de = [s.loc[n, "mean"] for n in nivaaer]
        lo = [s.loc[n, "mean"] - s.loc[n, "lo"] for n in nivaaer]
        hi = [s.loc[n, "hi"] - s.loc[n, "mean"] for n in nivaaer]
        ax.bar(x - 0.2, sw, 0.38, label="Sweep (rapporten)", color=farger["sweep"])
        ax.bar(x + 0.2, de, 0.38, yerr=[lo, hi], capsize=4, label="DES (dynamisk)", color=farger["des"])
        for xi, (a, b) in enumerate(zip(sw, de)):
            ax.text(xi - 0.2, a + 1, _komma(a), ha="center", fontsize=10)
            ax.text(xi + 0.2, b + 1, _komma(b), ha="center", fontsize=10, fontweight="bold")
        ax.set_title(skift.replace("_", " "), fontsize=14, fontweight="bold")
        ax.set_xticks(x); ax.set_xticklabels(nivaaer, fontsize=12)
        ax.set_ylim(0, 100)
    axes[0].set_ylabel("Andel av beredskapsanrop (%)", fontsize=13)
    axes[0].legend(fontsize=11, loc="upper right")
    fig.suptitle("Kapasitetsnivå ved ankomst: statisk sweep vs dynamisk DES\n"
                 "110 Sør-Vest 2025, Variant A (95 % CI over 400 replikasjoner)",
                 fontsize=15, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(FIG / "des_fig1_sweep_vs_des.png", bbox_inches="tight")
    plt.close(fig)


def fig_utfall():
    """Faktiske utfall natt/helg (det sweepen ikke viser): makkerpar/solo/VL/overloep."""
    res = pd.read_csv(HER / "d2_variant_a_resultat.csv")
    d = res[res["skift"] == "Natt_helg"]
    rekkef = ["makkerpar", "ordinaer", "solo", "ventet_servet", "vl_solo", "overlop_agder"]
    navn = {"makkerpar": "Makkerpar (D-pri1)", "ordinaer": "Ordinær (1 op)",
            "solo": "D-pri1 solo", "ventet_servet": "Ventet, servet",
            "vl_solo": "VL trer inn", "overlop_agder": "Overløp Agder"}
    vc = (d["utfall"].value_counts(normalize=True) * 100)
    verdier = [vc.get(k, 0) for k in rekkef]
    farger = ["#27ae60", "#2ecc71", "#f39c12", "#f1c40f", "#e67e22", "#c0392b"]
    fig, ax = plt.subplots(figsize=(11, 6))
    bars = ax.bar([navn[k] for k in rekkef], verdier, color=farger, edgecolor="#333")
    for b, v in zip(bars, verdier):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.5, _komma(v) + " %",
                ha="center", fontsize=11, fontweight="bold")
    ax.set_ylabel("Andel av beredskapsanrop natt/helg (%)", fontsize=13)
    ax.set_ylim(0, max(verdier) * 1.18)
    ax.set_title("Faktisk utfall natt/helg (DES) — det den statiske modellen ikke viser\n"
                 "110 Sør-Vest 2025, Variant A", fontsize=14, fontweight="bold")
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIG / "des_fig2_utfall_natthelg.png", bbox_inches="tight")
    plt.close(fig)


def fig_scenarioer():
    """Natt/helg Svikt + overloep per scenario, med CI."""
    d5 = pd.read_csv(HER / "d5_scenarioer_ci.csv")
    rekkef = ["S0_baseline", "S1_pluss1_natthelg", "S2_pluss1_dag",
              "S5a_overlop_60s", "S5b_overlop_ko15", "S4_nhpp_baseline", "S4_nhpp_burst"]
    etikett = {"S0_baseline": "S0 baseline", "S1_pluss1_natthelg": "S1 +1 natt/helg",
               "S2_pluss1_dag": "S2 +1 dag", "S5a_overlop_60s": "S5a 60s-terskel",
               "S5b_overlop_ko15": "S5b 15-i-kø", "S4_nhpp_baseline": "S4 NHPP",
               "S4_nhpp_burst": "S4 NHPP+burst"}
    rekkef = [s for s in rekkef if s in d5["scenario"].unique()]

    fig, ax = plt.subplots(figsize=(12, 6.5))
    x = np.arange(len(rekkef))
    sv = d5[(d5["skift"] == "Natt_helg") & (d5["maal"] == "Svikt")].set_index("scenario")
    means = [sv.loc[s, "mean"] for s in rekkef]
    lo = [sv.loc[s, "mean"] - sv.loc[s, "lo"] for s in rekkef]
    hi = [sv.loc[s, "hi"] - sv.loc[s, "mean"] for s in rekkef]
    cols = ["#2e86de" if s.startswith(("S0", "S1", "S2", "S5")) else "#8e44ad" for s in rekkef]
    bars = ax.bar(x, means, 0.6, yerr=[lo, hi], capsize=4, color=cols, edgecolor="#333")
    for b, v in zip(bars, means):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.3, _komma(v) + " %",
                ha="center", fontsize=11, fontweight="bold")
    ax.axhline(21.0, ls="--", color="#c0392b", lw=1.2)
    ax.text(len(rekkef) - 0.5, 21.4, "Sweep 21,0 %", color="#c0392b", ha="right", fontsize=10)
    ax.set_xticks(x); ax.set_xticklabels([etikett[s] for s in rekkef], rotation=20, ha="right", fontsize=11)
    ax.set_ylabel("Svikt natt/helg (%)", fontsize=13)
    ax.set_ylim(0, max(means) * 1.25)
    ax.set_title("DES-scenarioanalyse: Svikt natt/helg med 95 % CI\n"
                 "Blå = trace-drevet (Variant A), lilla = NHPP-generert", fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(FIG / "des_fig3_scenarioer.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    laget = []
    if (HER / "d3_ci_variant_a.csv").exists():
        fig_bro_vs_des(); laget.append("des_fig1_sweep_vs_des.png")
    if (HER / "d2_variant_a_resultat.csv").exists():
        fig_utfall(); laget.append("des_fig2_utfall_natthelg.png")
    if (HER / "d5_scenarioer_ci.csv").exists():
        fig_scenarioer(); laget.append("des_fig3_scenarioer.png")
    print("Figurer laget:", ", ".join(laget) if laget else "ingen (mangler resultat-CSV)")
