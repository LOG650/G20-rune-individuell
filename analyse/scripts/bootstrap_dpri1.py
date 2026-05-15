"""
Bootstrap-CI for Svikt-andelen i Variant A — D-pri1 bindingstid
================================================================
Adresserer peer review-kritikk runde 2: Sensitivitetsanalysen i kap 7.7
tester parameterspenn (lav/hoved/hoey) for D-aba/L-aba/m.fl., men ikke
statistisk usikkerhet i selve den observerte D-pri1-bindingstidsfordelingen
(n=4499 hendelser, ~25 % imputert med median for manglende
"Forste_ressurs_fremme"-tidsstempel).

Metode (per Beretta & Santaniello 2016 om multiple imputation + bootstrap):
  1. MAR-sjekk: rapporter missingness for "Forste_ressurs_fremme"
     stratifisert paa Oppdragstype/skift for aa vurdere MAR-antagelsen.
  2. Bootstrap-iterasjoner (B=1000):
       For hver iterasjon:
         - Trekk n_dpri1 bindingstider med erstatning fra de observerte
           (75 %) hendelsene. Dette gir én fresh draw per D-pri1-event.
         - Dette fanger bade sampling-variabilitet i den observerte
           empiriske fordelingen OG imputeringsusikkerhet for de ~25 %
           manglende.
         - Bygg variant A-events (D-pri1 + D-aba Fase 1+2 + skjulte).
         - Kjor sweep, beregn Normal/Brudd/Svikt-andel per skifttype.
  3. Beregn 95 % CI som [2.5; 97.5]-persentiler over de B iterasjonene.

D-aba Fase 2-sampling holdes deterministisk (samme SEED_DABA som
hovedscript) slik at bootstrap-CI isolerer D-pri1-usikkerheten.

Output:
  - bootstrap_dpri1_resultater.csv: punktestimat + CI per skift/niva
  - bootstrap_dpri1_mar_sjekk.csv: missingness per Oppdragstype
  - figurer/bootstrap_dpri1_ci.png: visualisert CI
"""
import pathlib
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# === KONFIGURASJON ===
PROJECT = pathlib.Path(r"C:\Users\runeg\OneDrive\Documents\Skole utdanning"
                       r"\Logistikk studie\LOG650 LOGISTIKK OG KI"
                       r"\G20-rune-individuell")
DATA_DIR = PROJECT / "004 data"
ANALYSE_DIR = PROJECT / "analyse"
FIG_DIR = ANALYSE_DIR / "figurer"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Modellparametre (matcher konflikt_total_belastning.py hoved-scenario)
KVITTERING_MIN = 3.0
SKJULT_BIND_MIN = 1.0
DABA_FASE1_MIN = 3.0
DABA_FASE2_OFFSET_MIN = 1.5
DABA_P_HOVED = 0.50
DABA_Y_HOVED = 6.0
SEED_DABA = 20260419        # matcher hovedscript
SEED_BOOTSTRAP = 20260515   # ny seed for bootstrap-trekk

N_BOOTSTRAP = 1000

sns.set_style("whitegrid")
plt.rcParams.update({"figure.dpi": 150, "font.size": 10})

# === 1. LAST DATA (samme datasett som hovedscript) ===
files = list(DATA_DIR.glob("110*TESTDATASETT.xlsx"))
if not files:
    raise FileNotFoundError("Fant ikke 110*TESTDATASETT.xlsx")
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

# === 2. KLASSIFISER (V3-regel — samme som hovedscript) ===
def klassifiser(row):
    if pd.notna(row["Ressurs_varslet"]):
        oot_d = str(row["Opprinnelig_oppdragstype"]).strip() if pd.notna(row["Opprinnelig_oppdragstype"]) else ""
        kilde_d = str(row["Kilde"]).strip() if pd.notna(row["Kilde"]) else ""
        if oot_d.startswith("ABA") and kilde_d == "Alarm":
            return "D-aba"
        return "D-pri1"
    ot = str(row["Oppdragstype"]).strip() if pd.notna(row["Oppdragstype"]) else ""
    oot = str(row["Opprinnelig_oppdragstype"]).strip() if pd.notna(row["Opprinnelig_oppdragstype"]) else ""
    kilde = str(row["Kilde"]).strip() if pd.notna(row["Kilde"]) else ""
    if ot == "Service":
        return "S"
    if ot in {"Nødanrop feilring", "Ikke reell nødmelding",
              "ECall feil bruk", "ECall teknisk/ukjent", "ECall veihjelp"}:
        return "F"
    if "viderevarslet" in ot.lower() or "viderekoble" in ot.lower():
        return "V"
    if "ppdrag" in ot and "110" in ot:
        if oot == "ABA" and kilde == "Alarm":
            return "L-aba"
        elif oot == "ABA":
            return "L-hendelse"
        elif oot and oot != "nan":
            return "L-hendelse"
        else:
            return "L-ukjent"
    return "L-ukjent"

df["v3_kat"] = df.apply(klassifiser, axis=1)
print("\n=== V3-fordeling ===")
for kat in ["D-pri1", "D-aba", "S", "L-aba", "L-hendelse", "L-ukjent", "F", "V"]:
    n = (df["v3_kat"] == kat).sum()
    print(f"  {kat:12s}: {n:>6} ({n/len(df)*100:>5.1f}%)")

# === 3. SKJULTE ANROP (sekvensgap) ===
df["dato_id"] = df["110_ID"].str.extract(r"B\d+-(\d{6})-")[0]
df["seq_nr"] = df["110_ID"].str.extract(r"B\d+-\d{6}-(\d+)")[0].astype(float)

hidden_rows = []
for dato, group in df.groupby("dato_id"):
    seqs = set(group["seq_nr"].dropna().astype(int))
    if not seqs:
        continue
    max_s = max(seqs)
    missing = sorted(set(range(1, max_s + 1)) - seqs)
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

print(f"\nSkjulte sammenstilte anrop: {len(hidden_rows)}")

# === 4. D-PRI1 BINDINGSTIDER (observert vs imputert) ===
d_pri1 = df[df["v3_kat"] == "D-pri1"].copy()
d_pri1["bind_raa"] = (
    (d_pri1["Forste_ressurs_fremme"] - d_pri1["Dato_og_Tid"]).dt.total_seconds() / 60
)
# Samme filtrering som hovedscript
d_pri1.loc[d_pri1["bind_raa"] < 0, "bind_raa"] = np.nan
d_pri1.loc[d_pri1["bind_raa"] > 180, "bind_raa"] = np.nan

n_total_dpri1 = len(d_pri1)
observed_mask = d_pri1["bind_raa"].notna()
n_observed = int(observed_mask.sum())
n_missing = int((~observed_mask).sum())
observed_bind = d_pri1.loc[observed_mask, "bind_raa"].values

print(f"\nD-pri1: n_total={n_total_dpri1}")
print(f"  observert Forste_ressurs_fremme: {n_observed} ({n_observed/n_total_dpri1*100:.1f}%)")
print(f"  manglende (imputeres):           {n_missing} ({n_missing/n_total_dpri1*100:.1f}%)")
print(f"  observert median: {np.median(observed_bind):.2f} min")
print(f"  observert mean:   {np.mean(observed_bind):.2f} min")
print(f"  observert P25/P75/P90: {np.percentile(observed_bind,[25,75,90])}")

# === 5. MAR-SJEKK ===
print("\n" + "=" * 70)
print("MAR-SJEKK: Missingness for 'Forste_ressurs_fremme' i D-pri1")
print("=" * 70)

d_pri1["mangler"] = ~observed_mask

mar_rows = []

# Per Oppdragstype
print("\nPer Oppdragstype (top 10 etter n):")
print(f"  {'Oppdragstype':<40} {'n':>6} {'mangler':>8} {'%':>6}")
print("  " + "-" * 64)
agg_ot = (d_pri1.groupby("Oppdragstype")
          .agg(n=("mangler", "size"), n_mangler=("mangler", "sum"))
          .sort_values("n", ascending=False))
for ot, r in agg_ot.head(10).iterrows():
    pct = r["n_mangler"] / r["n"] * 100
    print(f"  {str(ot)[:40]:<40} {int(r['n']):>6} {int(r['n_mangler']):>8} {pct:>5.1f}%")
    mar_rows.append({"stratum": "Oppdragstype", "verdi": str(ot),
                     "n": int(r["n"]), "n_mangler": int(r["n_mangler"]),
                     "pct_mangler": round(pct, 1)})

# Per Skift
print("\nPer Skift:")
print(f"  {'Skift':<10} {'n':>6} {'mangler':>8} {'%':>6}")
print("  " + "-" * 32)
agg_skift = (d_pri1.groupby("Skift")
             .agg(n=("mangler", "size"), n_mangler=("mangler", "sum")))
for s, r in agg_skift.iterrows():
    pct = r["n_mangler"] / r["n"] * 100
    print(f"  {s:<10} {int(r['n']):>6} {int(r['n_mangler']):>8} {pct:>5.1f}%")
    mar_rows.append({"stratum": "Skift", "verdi": str(s),
                     "n": int(r["n"]), "n_mangler": int(r["n_mangler"]),
                     "pct_mangler": round(pct, 1)})

# Per Skifttype (Dag/hverdag, Dag/helg, Natt/hverdag, Natt/helg)
d_pri1["skifttype"] = (
    d_pri1["Skift"].astype(str)
    + "/"
    + np.where(d_pri1["Er_helg"], "helg", "hverdag")
)
print("\nPer Skifttype:")
print(f"  {'Skifttype':<15} {'n':>6} {'mangler':>8} {'%':>6}")
print("  " + "-" * 37)
agg_st = (d_pri1.groupby("skifttype")
          .agg(n=("mangler", "size"), n_mangler=("mangler", "sum")))
for s, r in agg_st.iterrows():
    pct = r["n_mangler"] / r["n"] * 100
    print(f"  {s:<15} {int(r['n']):>6} {int(r['n_mangler']):>8} {pct:>5.1f}%")
    mar_rows.append({"stratum": "Skifttype", "verdi": str(s),
                     "n": int(r["n"]), "n_mangler": int(r["n_mangler"]),
                     "pct_mangler": round(pct, 1)})

# Per Maaned
print("\nPer Maaned:")
agg_m = (d_pri1.groupby("Maanedsnr")
         .agg(n=("mangler", "size"), n_mangler=("mangler", "sum")))
print(f"  {'Maaned':<8} {'n':>6} {'mangler':>8} {'%':>6}")
print("  " + "-" * 30)
for m, r in agg_m.iterrows():
    pct = r["n_mangler"] / r["n"] * 100
    print(f"  {str(m):<8} {int(r['n']):>6} {int(r['n_mangler']):>8} {pct:>5.1f}%")
    mar_rows.append({"stratum": "Maanedsnr", "verdi": str(m),
                     "n": int(r["n"]), "n_mangler": int(r["n_mangler"]),
                     "pct_mangler": round(pct, 1)})

mar_df = pd.DataFrame(mar_rows)
mar_df.to_csv(ANALYSE_DIR / "bootstrap_dpri1_mar_sjekk.csv",
              index=False, encoding="utf-8")
print(f"\nMAR-rapport lagret: {ANALYSE_DIR / 'bootstrap_dpri1_mar_sjekk.csv'}")

# Vurdering: koeffisientvariasjon i missing-rate paa tvers av Oppdragstype
ot_pcts = [r["n_mangler"] / r["n"] * 100 for _, r in agg_ot.iterrows() if r["n"] >= 30]
if ot_pcts:
    cv = np.std(ot_pcts) / np.mean(ot_pcts) if np.mean(ot_pcts) > 0 else float('nan')
    print(f"\nMissingness CV paa tvers av Oppdragstype (n>=30): {cv:.2f}")
    print("  CV < 0.30 -> rimelig uniform (MAR plausibel for pooled re-imputation)")
    print("  CV > 0.50 -> klyngestruktur, vurder stratifisert imputering")

# === 6. PRE-BUILD STATISKE EVENTS (D-aba, skjulte) ===
# Disse endres ikke mellom bootstrap-iterasjoner.

def expand_d_aba_static(df_daba, p, Y, seed):
    """D-aba: Fase 1 alltid + Fase 2 med sannsynlighet p. Deterministisk via seed."""
    rng = np.random.default_rng(seed)
    fase2_flag = rng.random(len(df_daba)) < p
    f1 = df_daba[["Dato_og_Tid", "Time", "Skift", "Er_helg"]].copy()
    f1["bind_min"] = DABA_FASE1_MIN
    f1["ops_bundet"] = 1
    f2_src = df_daba[fase2_flag].copy()
    f2 = f2_src[["Dato_og_Tid", "Time", "Skift", "Er_helg"]].copy()
    f2["Dato_og_Tid"] = f2["Dato_og_Tid"] + pd.to_timedelta(DABA_FASE2_OFFSET_MIN, unit="m")
    f2["bind_min"] = Y
    f2["ops_bundet"] = 1
    return pd.concat([f1, f2], ignore_index=True)

# D-aba events (statisk)
d_aba_df = df[(df["v3_kat"] == "D-aba") & df["Dato_og_Tid"].notna()].copy()
daba_events = expand_d_aba_static(d_aba_df, DABA_P_HOVED, DABA_Y_HOVED, SEED_DABA)
print(f"\nD-aba events (Fase 1 + Fase 2): {len(daba_events)}")

# Skjulte events (statisk)
hdf = pd.DataFrame(hidden_rows)
hdf["Dato_og_Tid"] = pd.to_datetime(hdf["Dato_og_Tid"])
hdf["Time"] = hdf["Dato_og_Tid"].dt.hour
hdf["Skift"] = np.where(hdf["Time"].between(7, 18), "Dag", "Natt")
hdf["Er_helg"] = hdf["Dato_og_Tid"].dt.dayofweek >= 5
hdf["bind_min"] = SKJULT_BIND_MIN
hdf["ops_bundet"] = 1
hidden_events = hdf[["Dato_og_Tid", "Time", "Skift", "Er_helg", "bind_min", "ops_bundet"]]
print(f"Skjulte events: {len(hidden_events)}")

# D-pri1: timestamps faste, bindingstider varierer
d_pri1_meta = d_pri1[["Dato_og_Tid", "Time", "Skift", "Er_helg"]].copy()
d_pri1_meta["ops_bundet"] = 2
d_pri1_meta = d_pri1_meta.reset_index(drop=True)
print(f"D-pri1 meta-events (timestamps faste): {len(d_pri1_meta)}")

# === 7. SWEEP-FUNKSJON ===
def sweep_kapasitet(events_df):
    """Op-binder-sweep. Returnerer events med 'kapasitet'-kolonne."""
    events = events_df.sort_values("Dato_og_Tid").reset_index(drop=True)
    events["slutt_ts"] = events["Dato_og_Tid"] + pd.to_timedelta(events["bind_min"], unit="m")
    n = len(events)
    ankomst = events["Dato_og_Tid"].values
    slutt = events["slutt_ts"].values
    ops = events["ops_bundet"].values.astype(int)
    c_eff_arr = events["c_eff"].values

    n_aktive_ops = np.zeros(n, dtype=int)
    active = []  # (slutt_ts, ops)
    for i in range(n):
        t_i = ankomst[i]
        active = [(s, o) for s, o in active if s > t_i]
        n_aktive_ops[i] = sum(o for _, o in active)
        active.append((slutt[i], ops[i]))

    ledige = c_eff_arr - n_aktive_ops
    kap = np.where(ledige >= 2, "Normal", np.where(ledige == 1, "Brudd", "Svikt"))
    events["kapasitet"] = kap
    return events

# === 8. PUNKTESTIMAT (deterministisk imputering — som i hovedscript) ===
# For aa verifisere at vi reproduserer hovedscriptets tall
median_obs = np.median(observed_bind)
d_pri1_punkt = d_pri1_meta.copy()
bind_punkt = np.full(len(d_pri1_punkt), np.nan)
bind_punkt[observed_mask.values] = observed_bind
bind_punkt[~observed_mask.values] = median_obs
d_pri1_punkt["bind_min"] = bind_punkt + KVITTERING_MIN

# Bygg variant A
ev_punkt = pd.concat([d_pri1_punkt, daba_events, hidden_events], ignore_index=True)
dag_hverdag_p = (ev_punkt["Skift"] == "Dag") & (~ev_punkt["Er_helg"])
ev_punkt["c_eff"] = np.where(dag_hverdag_p, 3, 2)
res_punkt = sweep_kapasitet(ev_punkt)

print("\n" + "=" * 70)
print("PUNKTESTIMAT (median-imputert, samme som hovedscript)")
print("=" * 70)
for ce, label in [(None, "Alle"), (3, "Dag hverdag (c=3)"), (2, "Natt/helg (c=2)")]:
    d = res_punkt if ce is None else res_punkt[res_punkt["c_eff"] == ce]
    n = len(d)
    n_norm = (d["kapasitet"] == "Normal").mean() * 100
    n_brud = (d["kapasitet"] == "Brudd").mean() * 100
    n_sv = (d["kapasitet"] == "Svikt").mean() * 100
    print(f"  {label:<25} n={n:>6}: Normal={n_norm:5.1f}% Brudd={n_brud:5.1f}% Svikt={n_sv:5.1f}%")

# === 9. BOOTSTRAP-LOOP ===
print("\n" + "=" * 70)
print(f"BOOTSTRAP: {N_BOOTSTRAP} iterasjoner (hver D-pri1 bindingstid trekkes")
print(f"med erstatning fra n={n_observed} observerte verdier)")
print("=" * 70)

rng_boot = np.random.default_rng(SEED_BOOTSTRAP)
n_dpri1 = len(d_pri1_meta)

# Pre-allokering av resultater
metrics = []
t_start = time.time()

for b in range(N_BOOTSTRAP):
    # Trekk n_dpri1 bindingstider med erstatning fra observerte
    bind_boot = rng_boot.choice(observed_bind, size=n_dpri1, replace=True)

    # Bygg D-pri1 events for denne iterasjonen
    d_b = d_pri1_meta.copy()
    d_b["bind_min"] = bind_boot + KVITTERING_MIN

    # Variant A
    ev_b = pd.concat([d_b, daba_events, hidden_events], ignore_index=True)
    dag_hverdag_b = (ev_b["Skift"] == "Dag") & (~ev_b["Er_helg"])
    ev_b["c_eff"] = np.where(dag_hverdag_b, 3, 2)
    res_b = sweep_kapasitet(ev_b)

    # Lagre andeler per skifttype
    for ce, label in [(None, "Alle"), (3, "Dag hverdag"), (2, "Natt/helg")]:
        d = res_b if ce is None else res_b[res_b["c_eff"] == ce]
        for niva in ["Normal", "Brudd", "Svikt"]:
            metrics.append({
                "iter": b,
                "skift": label,
                "niva": niva,
                "andel": (d["kapasitet"] == niva).mean() * 100,
                "n": len(d),
            })

    if (b + 1) % 100 == 0:
        elapsed = time.time() - t_start
        eta = elapsed / (b + 1) * (N_BOOTSTRAP - b - 1)
        print(f"  iter {b+1:>4}/{N_BOOTSTRAP} ({elapsed:.0f}s elapsed, ~{eta:.0f}s gjenstaar)")

t_total = time.time() - t_start
print(f"\nBootstrap ferdig: {t_total:.1f}s ({t_total/N_BOOTSTRAP*1000:.0f}ms/iter)")

boot_df = pd.DataFrame(metrics)

# === 10. CI-BEREGNING ===
print("\n" + "=" * 70)
print("BOOTSTRAP-CI (95 %, persentilmetode)")
print("=" * 70)

ci_rows = []
for skift in ["Alle", "Dag hverdag", "Natt/helg"]:
    print(f"\n--- {skift} ---")
    for niva in ["Normal", "Brudd", "Svikt"]:
        sub = boot_df[(boot_df["skift"] == skift) & (boot_df["niva"] == niva)]["andel"]
        mean = sub.mean()
        ci_lo, ci_hi = np.percentile(sub, [2.5, 97.5])
        # Punktestimat fra median-imputert
        d_punkt = res_punkt if skift == "Alle" else (
            res_punkt[res_punkt["c_eff"] == (3 if skift == "Dag hverdag" else 2)]
        )
        punkt = (d_punkt["kapasitet"] == niva).mean() * 100
        print(f"  {niva:<8}: punkt={punkt:5.2f}%  bootstrap mean={mean:5.2f}%  "
              f"95%CI=[{ci_lo:5.2f}; {ci_hi:5.2f}]  bredde={ci_hi-ci_lo:4.2f}pp")
        ci_rows.append({
            "Skifttype": skift,
            "Niva": niva,
            "Punktestimat_pct": round(punkt, 2),
            "Bootstrap_mean_pct": round(mean, 2),
            "CI_lav_pct": round(ci_lo, 2),
            "CI_hoy_pct": round(ci_hi, 2),
            "CI_bredde_pp": round(ci_hi - ci_lo, 2),
            "n_iterasjoner": N_BOOTSTRAP,
        })

ci_df = pd.DataFrame(ci_rows)
ci_df.to_csv(ANALYSE_DIR / "bootstrap_dpri1_resultater.csv",
             index=False, encoding="utf-8")
print(f"\nCI-resultater lagret: {ANALYSE_DIR / 'bootstrap_dpri1_resultater.csv'}")

# === 11. FIGUR ===
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
colors = {"Normal": "#4caf50", "Brudd": "#ff9800", "Svikt": "#d32f2f"}
order = ["Normal", "Brudd", "Svikt"]

for ax, skift in zip(axes, ["Alle", "Dag hverdag", "Natt/helg"]):
    for i, niva in enumerate(order):
        sub = boot_df[(boot_df["skift"] == skift) & (boot_df["niva"] == niva)]["andel"]
        # Histogram
        ax.hist(sub, bins=30, color=colors[niva], alpha=0.5, label=niva,
                edgecolor="black", linewidth=0.3)
        # Marker punktestimat
        d_punkt = res_punkt if skift == "Alle" else (
            res_punkt[res_punkt["c_eff"] == (3 if skift == "Dag hverdag" else 2)]
        )
        punkt = (d_punkt["kapasitet"] == niva).mean() * 100
        ax.axvline(punkt, color=colors[niva], linestyle="--", linewidth=1.5)
        # CI-grenser
        ci_lo, ci_hi = np.percentile(sub, [2.5, 97.5])
        ax.axvline(ci_lo, color=colors[niva], linestyle=":", alpha=0.6)
        ax.axvline(ci_hi, color=colors[niva], linestyle=":", alpha=0.6)

    ax.set_title(skift, fontsize=11, fontweight="bold")
    ax.set_xlabel("Andel (%)")
    ax.set_ylabel("Antall iterasjoner")
    ax.legend(fontsize=8, loc="upper right")

fig.suptitle(
    f"Bootstrap-fordeling av kapasitetsniva (B={N_BOOTSTRAP})\n"
    "D-pri1 bindingstid trukket med erstatning fra observerte (n=" + str(n_observed) + ")",
    fontsize=12, fontweight="bold",
)
plt.tight_layout()
plt.savefig(FIG_DIR / "bootstrap_dpri1_ci.png", bbox_inches="tight")
print(f"Figur: {FIG_DIR / 'bootstrap_dpri1_ci.png'}")

print("\n=== FERDIG ===")
