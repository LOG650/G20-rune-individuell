"""
Generer spørreskjema per 110-sentral basert på MOB- og BRIS-data.

Skjemaet brukes for å verifisere DSB-rapporterte tall og innhente operative
parametre nødvendige for benchmark av kapasitetsbelastning (normal / degradert /
svikt) på tvers av alle 12 norske 110-sentraler.

Output: én Markdown-fil per sentral i denne mappen.
"""
import pandas as pd
import warnings, os, re
warnings.filterwarnings('ignore')

utmappe = os.path.dirname(os.path.abspath(__file__))
datamappe = os.path.join(os.path.dirname(os.path.dirname(utmappe)), '004 data')

def les_mob(fil, aar):
    xl = pd.read_excel(fil, sheet_name=0, header=None)
    headers = xl.iloc[3].tolist()
    data = xl.iloc[4:].copy()
    data.columns = headers
    data = data[data.iloc[:,0].notna()].copy()
    def hent(sok):
        for c in data.columns:
            if sok.lower() in str(c).lower():
                return data[c].values
        return [None]*len(data)
    return pd.DataFrame({
        'sentral': data.iloc[:,0].values,
        'ansatte': hent('heltid'),
        'op_dag_hverd': hent('dag - hverdager'),
        'op_natt_hverd': hent('natt - hverdager'),
        'op_dag_helg': hent('dag - helg'),
        'op_natt_helg': hent('natt - helg'),
        'ros_aar': hent('ROS-analysen sist'),
        'beredskap_aar': hent('beredskapsanalysen sist'),
        'har_beredskap': hent('utarbeidet beredskapsanalyse'),
        'anrop_110': hent('mottatte 110-anrop'),
        'aar': aar,
    })

mob_filer = {
    2022: '20260315_174537_MOB_2022_110-sentral.xlsx',
    2023: '20260315_174530_MOB_2023_110-sentral.xlsx',
    2024: '20260315_174523_MOB_2024_110-sentral.xlsx',
    2025: '20260315_174514_MOB_2025_110-sentral.xlsx',
}
mob_alle = pd.concat(
    [les_mob(os.path.join(datamappe, f), a) for a, f in mob_filer.items()],
    ignore_index=True
)
mob_alle = mob_alle[mob_alle['sentral'] != 'Sum'].copy()

full_filer = {
    2022: 'Fullrapport2022_110-sentral.csv',
    2023: 'Fullrapport2023_110-sentral.csv',
    2024: 'Fullrapport2024_110-sentral.csv',
    2025: 'fullrapport2025.csv',
}
full_alle = []
for aar, fn in full_filer.items():
    df = pd.read_csv(os.path.join(datamappe, fn), sep=';', skiprows=3,
                     encoding='utf-8-sig', low_memory=False)
    grp = df.groupby(['110-sentral','Overordnet oppdragstype']).size().unstack(fill_value=0)
    grp['totalt'] = grp.sum(axis=1)
    grp['aar'] = aar
    full_alle.append(grp.reset_index().rename(columns={'110-sentral':'sentral'}))
full_df = pd.concat(full_alle, ignore_index=True)

def finn_kolonne_eksakt(df, kandidater):
    for col in df.columns:
        col_ascii = str(col).lower().encode('ascii', 'ignore').decode().strip()
        for k in kandidater:
            if col_ascii == k.lower().encode('ascii', 'ignore').decode().strip():
                return col
    return None

sample_df = full_df[full_df['aar'] == 2022]
KOL_BRANN   = finn_kolonne_eksakt(sample_df, ['Brann'])
KOL_ULYKKE  = finn_kolonne_eksakt(sample_df, ['Ulykke'])
KOL_UNODIGE = finn_kolonne_eksakt(sample_df, [
    'Unødige og falske utrykninger',
    'Unodige og falske utrykninger',
])

def finn_kolonne_prefix(df, prefix):
    prefix_ascii = prefix.lower().encode('ascii', 'ignore').decode()
    for col in df.columns:
        col_ascii = str(col).lower().encode('ascii', 'ignore').decode()
        if col_ascii.startswith(prefix_ascii):
            return col
    return None

if KOL_BRANN   is None: KOL_BRANN   = finn_kolonne_prefix(sample_df, 'brann')   or 'Brann'
if KOL_ULYKKE  is None: KOL_ULYKKE  = finn_kolonne_prefix(sample_df, 'ulykke')  or 'Ulykke'
if KOL_UNODIGE is None: KOL_UNODIGE = finn_kolonne_prefix(sample_df, 'un')      or 'Unodige'

print(f"Kolonner funnet: Brann={KOL_BRANN}, Ulykke={KOL_ULYKKE}, Unodige={KOL_UNODIGE}")

# === Nasjonal DSB 2025-data (for sentralspesifikke avklaringer) ===
NASJONAL_DIR = os.path.join(os.path.dirname(utmappe), 'nasjonal_2025')
try:
    bench = pd.read_csv(os.path.join(NASJONAL_DIR, 'benchmarkmatrise.csv'), encoding='utf-8-sig')
    tid = pd.read_csv(os.path.join(NASJONAL_DIR, 'tidsdata_kategori_D.csv'), encoding='utf-8-sig')
    vol = pd.read_csv(os.path.join(NASJONAL_DIR, 'volumavstemming.csv'), encoding='utf-8-sig')
    print(f"Nasjonal DSB 2025-data lastet ({len(bench)} sentraler)")
except Exception as e:
    print(f"ADVARSEL: Nasjonal DSB 2025-data ikke lastet: {e}")
    bench = tid = vol = None

def _stats(series):
    s = series.dropna()
    return {
        'min': float(s.min()), 'max': float(s.max()),
        'median': float(s.median()),
        'q20': float(s.quantile(0.20)),
        'q80': float(s.quantile(0.80)),
    }

NASJONAL_STATS = {}
if bench is not None:
    for kat in ['D_pct', 'D-pri1_pct', 'D-aba_pct', 'L-aba_pct', 'L-hendelse_pct', 'L-ukjent_pct', 'F_pct', 'V_pct']:
        if kat in bench.columns:
            NASJONAL_STATS[kat] = _stats(bench[kat])
    for kol in ['alarmbeh_median_min', 'alarmbeh_p90_min']:
        NASJONAL_STATS[kol] = _stats(tid[kol])
    NASJONAL_STATS['DSB_vs_MOB_pct'] = _stats(vol['DSB_vs_MOB_pct'])


def flagg(verdi, stats):
    """Returner 'HØY'/'LAV'/'NORMAL' basert på 20/80-percentil (bottom-3 / top-3 av 12)."""
    if verdi >= stats['q80']: return 'HØY'
    if verdi <= stats['q20']: return 'LAV'
    return 'NORMAL'


def avklaring_aba(pct, n, flagg_navn, stats, sentral=''):
    label = f" ved {sentral}" if sentral else ""
    if flagg_navn == 'LAV':
        return (
            f"**[SENTRALSPESIFIKT AVVIK{label}]** ABA løst uten utrykning registrert som usedvanlig lav ({pct:.1f}%, {n} oppdrag). "
            f"Nasjonalt: median {stats['median']:.1f}%, spenn {stats['min']:.1f}–{stats['max']:.1f}%. "
            f"Andre sentraler har rutinemessig 3–9 %. **Dette avviker betydelig fra forventet mønster og må forklares lokalt** — uten avklaring kan vi ikke benchmarke dere mot øvrige sentraler.\n\n"
            f"> *Avklaring:* Hvordan registreres automatiske brannalarmer som avklares uten utrykning (matlaging, damp, service utenom prosedyre){label}? "
            f"Velger dere en annen verdi for «Opprinnelig oppdragstype» enn 'ABA' ved slik avklaring, "
            f"eller utløser ABA rutinemessig utrykning hos dere uavhengig av avklaring innen 90 sek? "
            f"Kan dere beskrive registreringspraksis og ev. lokal prosedyre som skiller dere fra Sør-Vest-modellen?"
        )
    if flagg_navn == 'HØY':
        return (
            f"**[SENTRALSPESIFIKT AVVIK{label}]** ABA løst uten utrykning er høy ({pct:.1f}%, {n} oppdrag). "
            f"Nasjonalt: median {stats['median']:.1f}%, spenn {stats['min']:.1f}–{stats['max']:.1f}%. **Dette avviker fra forventet mønster og må forklares lokalt.**\n\n"
            f"> *Avklaring:* Er terskelen for å lukke ABA uten utrykning annerledes hos dere — "
            f"lengre venteperiode før utkalling, mer kontakt med objektet, eller annen prosedyre?"
        )
    return None


def avklaring_utr(pct, stats, sentral=''):
    label = f" ved {sentral}" if sentral else ""
    if pct >= stats['q80']:
        return (
            f"**[SENTRALSPESIFIKT AVVIK{label}]** Utrykningsrate (D-andel) er høy ({pct:.1f}%). Nasjonal median: {stats['median']:.1f}%, spenn {stats['min']:.1f}–{stats['max']:.1f}%. **Dere ligger blant de øverste 3 av 12 sentraler — avviker fra forventet mønster og må forklares lokalt.**\n\n"
            f"> *Avklaring:* Registreres færre oppdrag som «avklart uten utrykning» hos dere, eller har dere praksis "
            f"der utrykning aktiveres raskere (f.eks. på ABA uten ventetid, eller ved lav terskel for bekreftelse)?"
        )
    if pct <= stats['q20']:
        return (
            f"**[SENTRALSPESIFIKT AVVIK{label}]** Utrykningsrate (D-andel) er lav ({pct:.1f}%). Nasjonal median: {stats['median']:.1f}%, spenn {stats['min']:.1f}–{stats['max']:.1f}%. **Dere ligger blant de nederste 3 av 12 sentraler — avviker fra forventet mønster og må forklares lokalt.**\n\n"
            f"> *Avklaring:* Filtreres flere henvendelser ut som «løst av 110» før utrykning aktiveres, eller har dere "
            f"lokale samarbeidsformer (politi/AMK/brann) som håndterer en del hendelser før utalarmering?"
        )
    return None


def avklaring_ukjent(pct, stats, sentral=''):
    label = f" ved {sentral}" if sentral else ""
    if pct >= stats['q80']:
        return (
            f"**[SENTRALSPESIFIKT AVVIK{label}]** L-ukjent-andel er høy ({pct:.1f}%). Nasjonal median: {stats['median']:.1f}%, spenn {stats['min']:.1f}–{stats['max']:.1f}%. **Dere ligger blant de øverste 3 av 12 sentraler — store mengder oppdrag er registrert som «Oppdrag løst av 110» uten at «Opprinnelig oppdragstype» er satt. Dette må forklares lokalt før vi kan tolke L-ukjent som sammenlignbar kategori.**\n\n"
            f"> *Avklaring:* Hva er typisk innhold i disse oppdragene — korte avklaringer og spørsmål "
            f"(bål-henvendelser, telefonhjelp), eller er det også reelle hendelser som ikke klassifiseres? "
            f"Er det en lokal rutine å lukke enkelte henvendelsestyper uten opprinnelig type?"
        )
    if pct <= stats['q20']:
        return (
            f"**[SENTRALSPESIFIKT AVVIK{label}]** L-ukjent-andel er lav ({pct:.1f}%). Nasjonal median: {stats['median']:.1f}%, spenn {stats['min']:.1f}–{stats['max']:.1f}%. **Dere setter «Opprinnelig oppdragstype» oftere enn andre sentraler ved lukking — avviker fra forventet mønster og må forklares lokalt.**\n\n"
            f"> *Avklaring:* Er det en lokal praksis å alltid klassifisere hendelser før lukking, eller "
            f"reflekterer det at dere håndterer færre uklassifiserte henvendelser?"
        )
    return None


def avklaring_l_hendelse(pct, stats, sentral=''):
    label = f" ved {sentral}" if sentral else ""
    if pct >= stats['q80']:
        return (
            f"**[SENTRALSPESIFIKT AVVIK{label}]** L-hendelse-andel er høy ({pct:.1f}%). Nasjonal median: {stats['median']:.1f}%, spenn {stats['min']:.1f}–{stats['max']:.1f}%. **Dere ligger blant de øverste 3 av 12 sentraler — avviker fra forventet mønster og må forklares lokalt.**\n\n"
            f"> *Avklaring:* Er det en lokal praksis at alle reelle hendelser får en opprinnelig oppdragstype før lukking? "
            f"Hva er typisk innhold — veiledningssamtaler, varsling fra publikum uten behov for utrykning, eller noe annet?"
        )
    if pct <= stats['q20']:
        return (
            f"**[SENTRALSPESIFIKT AVVIK{label}]** L-hendelse-andel er lav ({pct:.1f}%). Nasjonal median: {stats['median']:.1f}%, spenn {stats['min']:.1f}–{stats['max']:.1f}%. **Dere ligger blant de nederste 3 av 12 sentraler — avviker fra forventet mønster og må forklares lokalt.**\n\n"
            f"> *Avklaring:* Registreres disse under andre kategorier (L-ukjent, V), eller rykker dere ut oftere på "
            f"hendelser som andre sentraler avklarer telefonisk?"
        )
    return None


def avklaring_feilring(pct, stats, sentral=''):
    label = f" ved {sentral}" if sentral else ""
    if pct >= stats['q80']:
        return (
            f"**[SENTRALSPESIFIKT AVVIK{label}]** Feilring-andel er høy ({pct:.1f}%). Nasjonal median: {stats['median']:.1f}%, spenn {stats['min']:.1f}–{stats['max']:.1f}%. **Dere ligger blant de øverste 3 av 12 sentraler — avviker fra forventet mønster og må forklares lokalt.**\n\n"
            f"> *Avklaring:* Er det reelt flere feilringinger hos dere (f.eks. fra samlokalisering med 112/113), "
            f"eller klassifiseres flere henvendelser som «feilring» enn andre sentraler ville gjort?"
        )
    if pct <= stats['q20']:
        return (
            f"**[SENTRALSPESIFIKT AVVIK{label}]** Feilring-andel er lav ({pct:.1f}%). Nasjonal median: {stats['median']:.1f}%, spenn {stats['min']:.1f}–{stats['max']:.1f}%. **Dere ligger blant de nederste 3 av 12 sentraler — avviker fra forventet mønster og må forklares lokalt.**\n\n"
            f"> *Avklaring:* Registreres feilringinger under annen kategori (f.eks. L-ukjent eller V), "
            f"eller er feilringinger faktisk sjeldnere i deres distrikt?"
        )
    return None


def avklaring_v(pct, stats, sentral=''):
    label = f" ved {sentral}" if sentral else ""
    if pct >= stats['q80']:
        return (
            f"**[SENTRALSPESIFIKT AVVIK{label}]** Viderekoble-andel er høy ({pct:.1f}%). Nasjonal median: {stats['median']:.1f}%, spenn {stats['min']:.1f}–{stats['max']:.1f}%. **Dere ligger blant de øverste 3 av 12 sentraler — avviker fra forventet mønster og må forklares lokalt.**\n\n"
            f"> *Avklaring:* Hvilke typer henvendelser viderekobles? Er det mye 112/113-feilringinger, "
            f"eller har dere eksplisitt samarbeid med nabosentraler/andre etater som øker viderekobling?"
        )
    return None


def avklaring_dsb_mob(ratio, mob, dsb, stats, sentral=''):
    label = f" ved {sentral}" if sentral else ""
    felles_avklaring = (
        f"**Hva teller dere egentlig i MOB-feltet «Mottatte 110-anrop»?** "
        f"MOB-skjemaet gir ikke en entydig definisjon, og variasjonen mellom sentraler kan skyldes dette. "
        f"Vi ber om å få bekreftet konkret hva deres tall inkluderer: "
        f"(a) kun besvarte telefonanrop på 110-nødlinjen, "
        f"(b) alle telefonanrop inkludert overførte, viderekoblede og avbrutte, "
        f"(c) også automatiske ABA-signaler som kommer inn uten samtale, "
        f"(d) også servicetelefon, eller "
        f"(e) alle henvendelser uavhengig av kanal. "
        f"Dette er en nøkkelavklaring for om MOB-anroptallet kan brukes som felles mål på tvers av sentraler."
    )
    if ratio >= stats['q80']:
        return (
            f"**[SENTRALSPESIFIKT AVVIK{label}]** Forhold DSB/MOB er høyt ({ratio:.1f}×). Nasjonal median: {stats['median']:.1f}×. "
            f"MOB-selvrapport: {mob:,} mottatte anrop. DSB-oppdrag: {dsb:,}. **Dere ligger blant de øverste 3 av 12 sentraler i differanse — krever forklaring for at MOB- og DSB-tall skal kunne brukes konsistent.**\n\n"
            f"> *Avklaring:* {felles_avklaring}"
        )
    if ratio <= stats['q20']:
        return (
            f"**[SENTRALSPESIFIKT AVVIK{label}]** Forhold DSB/MOB er lavt ({ratio:.1f}×). Nasjonal median: {stats['median']:.1f}×. "
            f"MOB-selvrapport: {mob:,} mottatte anrop. DSB-oppdrag: {dsb:,}. **Dere ligger blant de nederste 3 av 12 sentraler i differanse — krever forklaring for at MOB- og DSB-tall skal kunne brukes konsistent.**\n\n"
            f"> *Avklaring:* {felles_avklaring}"
        )
    return None


def avklaring_tid(tid_row, stats_med, stats_p90, sentral=''):
    label = f" ved {sentral}" if sentral else ""
    ab_med = tid_row.get('alarmbeh_median_min')
    ab_p90 = tid_row.get('alarmbeh_p90_min')
    deler = []
    if pd.notna(ab_med) and ab_med >= stats_med['q80']:
        deler.append(
            f"Median alarmbehandlingstid på D-oppdrag er **{ab_med:.2f} min** (nasj. median {stats_med['median']:.2f} min)."
        )
    if pd.notna(ab_p90) and ab_p90 >= stats_p90['q80']:
        deler.append(
            f"p90 alarmbehandlingstid er **{ab_p90:.1f} min** (nasj. median {stats_p90['median']:.1f} min) — altså 10 % av D-oppdrag bruker mer enn dette før utalarmering."
        )
    if not deler:
        return None
    return (
        f"**[SENTRALSPESIFIKT AVVIK{label}]** Alarmbehandlingstid avviker fra nasjonalt snitt. " + " ".join(deler) + " **Dere ligger blant de øverste 3 av 12 sentraler — krever lokal forklaring.**\n\n"
        "> *Avklaring:* Kan forskjellen forklares av geografiske forhold (lengre verifikasjon/kjentmenn), "
        "volum per operatør, eller registreringspraksis (f.eks. hvordan tidspunkt for «ressurs varslet» settes)?"
    )


def sentralspesifikke_avklaringer(sentral_mob, start_spm=26):
    """Bygg markdown-linjer for Del 7 for en gitt sentral. start_spm = første spørsmålsnummer."""
    if bench is None:
        return []

    # MOB-navn: "Agder 110" → benchmarkmatrise: "Agder"
    navn_kort = sentral_mob.replace(' 110', '').strip()
    br = bench[bench['sentral'] == navn_kort]
    if br.empty:
        return []
    br = br.iloc[0]
    tr = tid[tid['sentral'] == navn_kort].iloc[0] if len(tid[tid['sentral'] == navn_kort]) else None
    vr = vol[vol['sentral'] == navn_kort].iloc[0] if len(vol[vol['sentral'] == navn_kort]) else None

    total_n = int(br['Totalt'])
    mob_n = int(vr['MOB_selvrapport']) if vr is not None and pd.notna(vr['MOB_selvrapport']) else 0
    dsb_mob_ratio = float(vr['DSB_vs_MOB_pct']) / 100 + 1 if vr is not None and pd.notna(vr['DSB_vs_MOB_pct']) else None
    # DSB_vs_MOB_pct is (DSB-MOB)/MOB*100. ratio = DSB/MOB = DSB_vs_MOB/100 + 1
    # But stored as %, so ratio_times = 1 + pct/100
    # For the stats dict we stored pct, so convert sentral value similarly
    sentral_dsb_mob_pct = float(vr['DSB_vs_MOB_pct']) if vr is not None and pd.notna(vr['DSB_vs_MOB_pct']) else None

    L = []
    L.append("---")
    L.append("")
    L.append(f"## Del 7 — Sentralspesifikke avklaringer for {sentral_mob} (DSB 2025-data)")
    L.append("")
    L.append(
        f"> **Hvorfor dette avsnittet er spesifikt for {sentral_mob}:** "
        f"DSB har i 2026 levert et fullstendig hendelsesdatasett for alle 12 sentraler (2025). "
        f"Jeg har klassifisert alle oppdrag etter V3-logikken (D-pri1 / D-aba / S / L-aba / L-hendelse / L-ukjent / F / V) "
        f"basert på kolonnene «Oppdragstype», «Opprinnelig oppdragstype», «Kilde» og «Ressurs varslet». "
        f"D er splittet i D-pri1 (pri-1-utrykning, krever makkerpar) og D-aba (ABA-utrykning med Kilde=Alarm, håndteres serielt). "
        f"Sammenligningen avdekker at **{sentral_mob} avviker betydelig fra nasjonalt snitt på enkelte kategorier** — "
        f"spørsmålene under er generert kun for dere, basert på hvor deres tall ligger i topp-3 (↑ HØY) eller bunn-3 (↓ LAV) av de 12 sentralene. "
        f"**Vi kan ikke benchmarke dere mot andre sentraler uten å forstå om disse avvikene skyldes registreringspraksis, lokal organisering eller reell operativ forskjell.**"
    )
    L.append("")
    L.append(
        f"Under vises **{sentral_mob}s tall i nasjonal sammenheng**. Avvikene er flagget med ↑ HØY eller ↓ LAV. "
        f"For hver flagget kategori følger et spesifikt oppfølgingsspørsmål merket **[SENTRALSPESIFIKT AVVIK ved {sentral_mob}]**."
    )
    L.append("")
    L.append("### 7.1 Deres sentral i nasjonal sammenheng (DSB 2025)")
    L.append("")
    L.append(f"Totalvolum DSB 2025: **{total_n:,}** oppdrag. MOB-selvrapport: **{mob_n:,}** mottatte anrop. Forhold DSB/MOB: **{total_n/mob_n:.1f}×**." if mob_n else
             f"Totalvolum DSB 2025: **{total_n:,}** oppdrag.")
    L.append("")
    L.append("| Kategori | Deres andel | Antall | Nasj. median | Nasj. spenn | Avvik |")
    L.append("|---|---:|---:|---:|---:|---|")
    kat_labels = {
        'D-pri1': 'D-pri1 — pri-1-utrykning (makkerpar)',
        'D-aba': 'D-aba — ABA-utrykning (serielt)',
        'L-aba': 'L-aba — ABA løst av 110 uten utrykning',
        'L-hendelse': 'L-hendelse — reell hendelse løst av 110',
        'L-ukjent': 'L-ukjent — lukket uten opprinnelig type',
        'F': 'F — feilringing',
        'V': 'V — viderekobling',
    }
    for k, label in kat_labels.items():
        pct = float(br[f'{k}_pct'])
        n = int(br[k])
        stats = NASJONAL_STATS[f'{k}_pct']
        fl = flagg(pct, stats)
        fl_visning = {'HØY': '↑ HØY', 'LAV': '↓ LAV', 'NORMAL': '–'}[fl]
        L.append(
            f"| {label} | {pct:.1f}% | {n:,} | {stats['median']:.1f}% | "
            f"{stats['min']:.1f}–{stats['max']:.1f}% | {fl_visning} |"
        )
    L.append("")

    # Lag avklaringer
    avklaringer = []
    # ABA
    aba_pct = float(br['L-aba_pct'])
    aba_n = int(br['L-aba'])
    aba_fl = flagg(aba_pct, NASJONAL_STATS['L-aba_pct'])
    if aba_fl != 'NORMAL':
        t = avklaring_aba(aba_pct, aba_n, aba_fl, NASJONAL_STATS['L-aba_pct'], sentral_mob)
        if t: avklaringer.append(t)

    # D (aggregert utrykningsrate) — beholdes som overordnet flagg
    d_pct = float(br['D_pct'])
    t = avklaring_utr(d_pct, NASJONAL_STATS['D_pct'], sentral_mob)
    if t: avklaringer.append(t)

    # D-pri1 / D-aba — splittsjekk
    if 'D-pri1_pct' in br.index and 'D-pri1_pct' in NASJONAL_STATS:
        dpri_pct = float(br['D-pri1_pct'])
        dpri_fl = flagg(dpri_pct, NASJONAL_STATS['D-pri1_pct'])
        if dpri_fl != 'NORMAL':
            label = f" ved {sentral_mob}"
            retning = "høy" if dpri_fl == 'HØY' else "lav"
            posisjon = "øverste" if dpri_fl == 'HØY' else "nederste"
            tekst = (
                f"**[SENTRALSPESIFIKT AVVIK{label}]** D-pri1-andel (pri-1-utrykninger som krever makkerpar) er {retning} ({dpri_pct:.1f}%). "
                f"Nasjonal median: {NASJONAL_STATS['D-pri1_pct']['median']:.1f}%, spenn {NASJONAL_STATS['D-pri1_pct']['min']:.1f}–{NASJONAL_STATS['D-pri1_pct']['max']:.1f}%. "
                f"**Dere ligger blant de {posisjon} 3 av 12 sentraler.**\n\n"
                f"> *Avklaring:* Skyldes dette ulik registreringspraksis (f.eks. om Opprinnelig oppdragstype settes til ABA på utrykninger som ikke er ren ABA), reell forskjell i pri-1-volum, eller lokal terskel for å klassifisere oppdrag som pri-1 vs ABA-utrykning?"
            )
            avklaringer.append(tekst)
    if 'D-aba_pct' in br.index and 'D-aba_pct' in NASJONAL_STATS:
        daba_pct = float(br['D-aba_pct'])
        daba_fl = flagg(daba_pct, NASJONAL_STATS['D-aba_pct'])
        if daba_fl != 'NORMAL':
            label = f" ved {sentral_mob}"
            retning = "høy" if daba_fl == 'HØY' else "lav"
            posisjon = "øverste" if daba_fl == 'HØY' else "nederste"
            tekst = (
                f"**[SENTRALSPESIFIKT AVVIK{label}]** D-aba-andel (ABA-utrykninger registrert med Kilde=Alarm) er {retning} ({daba_pct:.1f}%). "
                f"Nasjonal median: {NASJONAL_STATS['D-aba_pct']['median']:.1f}%, spenn {NASJONAL_STATS['D-aba_pct']['min']:.1f}–{NASJONAL_STATS['D-aba_pct']['max']:.1f}%. "
                f"**Dere ligger blant de {posisjon} 3 av 12 sentraler.**\n\n"
                f"> *Avklaring:* Reflekterer dette objekttetthet (mange ABA-objekter), terskel for utrykning på ABA, eller registreringspraksis (settes Kilde=Alarm konsistent for ABA-signaler hos dere)?"
            )
            avklaringer.append(tekst)

    # L-hendelse
    lh_pct = float(br['L-hendelse_pct'])
    t = avklaring_l_hendelse(lh_pct, NASJONAL_STATS['L-hendelse_pct'], sentral_mob)
    if t: avklaringer.append(t)

    # L-ukjent
    u_pct = float(br['L-ukjent_pct'])
    t = avklaring_ukjent(u_pct, NASJONAL_STATS['L-ukjent_pct'], sentral_mob)
    if t: avklaringer.append(t)

    # F
    f_pct = float(br['F_pct'])
    t = avklaring_feilring(f_pct, NASJONAL_STATS['F_pct'], sentral_mob)
    if t: avklaringer.append(t)

    # V
    v_pct = float(br['V_pct'])
    t = avklaring_v(v_pct, NASJONAL_STATS['V_pct'], sentral_mob)
    if t: avklaringer.append(t)

    # DSB/MOB ratio
    if sentral_dsb_mob_pct is not None:
        t = avklaring_dsb_mob(
            1 + sentral_dsb_mob_pct / 100, mob_n, total_n,
            {'median': 1 + NASJONAL_STATS['DSB_vs_MOB_pct']['median']/100,
             'q20': 1 + NASJONAL_STATS['DSB_vs_MOB_pct']['q20']/100,
             'q80': 1 + NASJONAL_STATS['DSB_vs_MOB_pct']['q80']/100},
            sentral_mob
        )
        if t: avklaringer.append(t)

    # Tid
    if tr is not None:
        t = avklaring_tid(tr, NASJONAL_STATS['alarmbeh_median_min'], NASJONAL_STATS['alarmbeh_p90_min'], sentral_mob)
        if t: avklaringer.append(t)

    L.append(f"### 7.2 Oppfølgingsspørsmål — sentralspesifikke avvik for {sentral_mob}")
    L.append("")
    if not avklaringer:
        L.append(
            f"**{sentral_mob} ligger innenfor nasjonalt normalt spenn (mellom 20- og 80-percentil av 12 sentraler) på alle kategorier.** "
            "Vi ber likevel om bekreftelse på tallene i 7.1 og korte kommentarer på om noe av dette virker overraskende."
        )
        L.append("")
        L.append("> *Svar:*")
        L.append("")
    else:
        for i, txt in enumerate(avklaringer, start=start_spm):
            L.append(f"**Spm {i}.** {txt}")
            L.append("")
            L.append("> *Svar:*")
            L.append("")

    return L


def v(val):
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return '—'
    try:
        return str(int(float(val)))
    except:
        return str(val)

def endring(a, b):
    try:
        a, b = float(a), float(b)
        if pd.isna(a) or pd.isna(b):
            return ''
        pct = round((b - a) / a * 100, 1)
        sign = '+' if pct >= 0 else ''
        return f'{sign}{pct}%'
    except:
        return ''

sentraler = sorted([s for s in mob_alle['sentral'].unique() if s != 'Sum'])

for sentral in sentraler:
    m = mob_alle[mob_alle['sentral'] == sentral].sort_values('aar')
    f_data = full_df[full_df['sentral'] == sentral].sort_values('aar')

    def mob_val(aar, kol):
        r = m[m['aar'] == aar]
        return None if r.empty else r.iloc[0][kol]

    def full_val(aar, kol):
        r = f_data[f_data['aar'] == aar]
        if r.empty or kol not in r.columns:
            return None
        val = r.iloc[0][kol]
        return None if (isinstance(val, float) and pd.isna(val)) else val

    def utrykn(aar):
        b = full_val(aar, KOL_BRANN) or 0
        u = full_val(aar, KOL_ULYKKE) or 0
        try:
            return int(float(b)) + int(float(u))
        except:
            return None

    safe = re.sub(r'[^\w]', '_', sentral)
    ans_endr = endring(mob_val(2022, 'ansatte'), mob_val(2025, 'ansatte'))

    utr22 = utrykn(2022)
    utr23 = utrykn(2023)
    utr24 = utrykn(2024)
    utr25 = utrykn(2025)
    utr_endr_22_24 = endring(utr22, utr24)

    ros_aar = mob_val(2025, 'ros_aar') or mob_val(2024, 'ros_aar')
    ber_aar = mob_val(2025, 'beredskap_aar') or mob_val(2024, 'beredskap_aar')
    har_ber = mob_val(2025, 'har_beredskap') or mob_val(2024, 'har_beredskap')

    od  = v(mob_val(2025, 'op_dag_hverd'))
    on  = v(mob_val(2025, 'op_natt_hverd'))
    oh  = v(mob_val(2025, 'op_dag_helg'))
    onh = v(mob_val(2025, 'op_natt_helg'))

    L = []
    L.append(f"# Spørreskjema — {sentral}")
    L.append("## Validering av kapasitetsdata for nasjonal benchmarkstudie")
    L.append("### LOG650, Høgskolen i Molde, vår 2026")
    L.append("")
    L.append("**Student:** Rune Grødem")
    L.append("**Kontakt:** rune.grodem@rogbr.no")
    L.append("**Innlevering:** hovedutkast slutten av april 2026, endelig rapport 31. mai 2026")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Om studien")
    L.append("")
    L.append("Brannvesenet har en nasjonal dimensjoneringsforskrift (FOR-2023-01-06-23) som setter")
    L.append("kvantitative, etterprøvbare krav til antall brannmannskap basert på innbyggertall og")
    L.append("responstid. **Ingen tilsvarende standard finnes for 110-operatører.** Bemanningsnivået")
    L.append("fastsettes lokalt gjennom ROS- og beredskapsanalyser som er kvalitative og vanskelige å")
    L.append("etterprøve på tvers av sentraler.")
    L.append("")
    L.append("Forskningsprosjektet undersøker problemstillingen:")
    L.append("")
    L.append("> *I hvilken grad samsvarer faktisk bemanning ved norske 110-sentraler med kapasitetsbehovet")
    L.append("> beregnet fra historiske hendelsesdata og køteoretiske/prosedyrbaserte modeller?*")
    L.append("")
    L.append("Målet er å bygge et **kvantitativt referansepunkt** for 110-bemanning — ikke for å kritisere")
    L.append("lokale valg, men for å komplettere ROS-analyser med tallbaserte målepunkter som kan")
    L.append("sammenlignes på tvers av alle 12 sentraler.")
    L.append("")
    L.append("- **Primærcase:** 110 Sør-Vest, der jeg har detaljerte LEO/BRIS-data og intern beredskapsanalyse")
    L.append("- **Benchmarkgrunnlag:** alle 12 sentraler via DSB-årsrapporter (MOB) og BRIS-fullrapporter")
    L.append("- **Modell:** prosedyrbasert ankomstkonfliktmodell som måler andel beredskapsanrop som")
    L.append("  håndteres i normal-, degradert- (solo) eller sviktnivå")
    L.append("")
    L.append(f"**Hvorfor jeg kontakter {sentral}:** for å kunne benchmarke kapasitetsbelastning må jeg")
    L.append("verifisere at DSB-tallene gjenspeiler operativ virkelighet, og forstå lokale særtrekk ved")
    L.append("bemanning, vaktordning og arbeidsmetodikk.")
    L.append("")
    L.append(f"> Svarene behandles konfidensielt. {sentral} navngis kun med eksplisitt samtykke.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Del 1 — Verifisering av DSB-rapporterte data (2022–2025)")
    L.append("")
    L.append("Tabellene under er hentet fra det dere selv har rapportert til DSB via MOB-systemet. Jeg")
    L.append("ber dere bekrefte, korrigere eller utdype disse tallene.")
    L.append("")
    L.append("### 1.1 Bemanning (MOB-rapportert)")
    L.append("")
    L.append("> **Merknad:** MOB-tallene under er ett enkelt tall per skift-type per år, og skiller ikke mellom **normal bemanning** (planlagt nivå når alle stiller) og **minimumsbemanning** (det laveste nivået sentralen kan operere på, f.eks. ved sykdom eller fravær). Skillet er sentralt for kapasitetsanalysen og presiseres i Spm 4 (tabell 1.1b).")
    L.append("")
    L.append("**Tabell 1.1a — MOB-rapportert bemanning per år:**")
    L.append("")
    L.append("| Kategori | 2022 | 2023 | 2024 | 2025 | Endring 22–25 |")
    L.append("|---|---|---|---|---|---|")
    L.append(f"| Ansatte heltid | {v(mob_val(2022,'ansatte'))} | {v(mob_val(2023,'ansatte'))} | {v(mob_val(2024,'ansatte'))} | {v(mob_val(2025,'ansatte'))} | {ans_endr} |")
    L.append(f"| Operatører dag — hverdag | {v(mob_val(2022,'op_dag_hverd'))} | {v(mob_val(2023,'op_dag_hverd'))} | {v(mob_val(2024,'op_dag_hverd'))} | {v(mob_val(2025,'op_dag_hverd'))} | |")
    L.append(f"| Operatører natt — hverdag | {v(mob_val(2022,'op_natt_hverd'))} | {v(mob_val(2023,'op_natt_hverd'))} | {v(mob_val(2024,'op_natt_hverd'))} | {v(mob_val(2025,'op_natt_hverd'))} | |")
    L.append(f"| Operatører dag — helg | {v(mob_val(2022,'op_dag_helg'))} | {v(mob_val(2023,'op_dag_helg'))} | {v(mob_val(2024,'op_dag_helg'))} | {v(mob_val(2025,'op_dag_helg'))} | |")
    L.append(f"| Operatører natt — helg | {v(mob_val(2022,'op_natt_helg'))} | {v(mob_val(2023,'op_natt_helg'))} | {v(mob_val(2024,'op_natt_helg'))} | {v(mob_val(2025,'op_natt_helg'))} | |")
    L.append("")
    L.append("Tallene over er det dere har rapportert til DSB. Tabell 1.1b under ber om presisering av hva som er *normalt planlagt* versus *minimum* — dette skillet kan ikke utledes fra MOB.")
    L.append("")
    L.append("### 1.2 Oppdrag med utrykning (sammenlignbare tall 2022–2024)")
    L.append("")
    L.append("> **Datakvalitetsmerknad:** Flere sentraler tok i bruk nytt operativsystem (LEO/OHV) fra")
    L.append("> 2024, og fra 2025 registreres alle innkommende telefonsamtaler som egne hendelsesrader.")
    L.append("> Totalt oppdragsvolum er derfor **ikke** sammenlignbart på tvers av alle år. Tabellen")
    L.append("> nedenfor viser kun oppdrag MED utrykning (Brann + Ulykke), som er konsistent registrert")
    L.append("> alle år uavhengig av system.")
    L.append("")
    L.append("| Kategori | 2022 | 2023 | 2024 | 2025* | Endring 22–24 |")
    L.append("|---|---|---|---|---|---|")
    L.append(f"| Oppdrag — Brann | {v(full_val(2022,KOL_BRANN))} | {v(full_val(2023,KOL_BRANN))} | {v(full_val(2024,KOL_BRANN))} | {v(full_val(2025,KOL_BRANN))} | |")
    L.append(f"| Oppdrag — Ulykke | {v(full_val(2022,KOL_ULYKKE))} | {v(full_val(2023,KOL_ULYKKE))} | {v(full_val(2024,KOL_ULYKKE))} | {v(full_val(2025,KOL_ULYKKE))} | |")
    L.append(f"| **Sum med utrykning** | **{v(utr22)}** | **{v(utr23)}** | **{v(utr24)}** | **{v(utr25)}** | **{utr_endr_22_24}** |")
    L.append(f"| Unødige/falske utrykninger | {v(full_val(2022,KOL_UNODIGE))} | {v(full_val(2023,KOL_UNODIGE))} | {v(full_val(2024,KOL_UNODIGE))} | {v(full_val(2025,KOL_UNODIGE))} | |")
    L.append("")
    L.append("*2025-tall vises for orientering, men bør ikke brukes i trendsammenligning på grunn av systembytte.")
    L.append("")
    L.append("### 1.3 Mottatte 110-anrop (MOB, selvrapportert)")
    L.append("")
    L.append("> Sentralenes egne innrapporteringer, uavhengig av registreringssystem.")
    L.append("")
    L.append("| | 2022 | 2023 | 2024 | 2025 |")
    L.append("|---|---|---|---|---|")
    L.append(f"| Mottatte 110-anrop (MOB) | {v(mob_val(2022,'anrop_110'))} | {v(mob_val(2023,'anrop_110'))} | {v(mob_val(2024,'anrop_110'))} | {v(mob_val(2025,'anrop_110'))} |")
    L.append("")
    L.append("**Spm 1.** Er tallene i 1.1–1.3 korrekte? Hvis nei — hva er riktige tall, og hva forklarer avviket?")
    L.append("")
    L.append("> *Svar:*")
    L.append("")
    L.append("**Spm 1b.** Hva inkluderer MOB-feltet «Mottatte 110-anrop» *konkret* hos dere? (Velg alle som gjelder — **flere svar kan brukes**)")
    L.append("")
    L.append("- [ ] Kun besvarte telefonanrop på 110-nødlinjen")
    L.append("- [ ] Alle telefonanrop inkludert overførte, viderekoblede og avbrutte")
    L.append("- [ ] Automatiske ABA-signaler som kommer inn uten samtale")
    L.append("- [ ] Servicetelefon / teknisk support")
    L.append("- [ ] Alle henvendelser uavhengig av kanal")
    L.append("- [ ] Annet: ___")
    L.append("")
    L.append("> *Kommentar (eksakt definisjon dere bruker):* MOB-skjemaet gir ikke en entydig definisjon, og variasjonen mellom sentraler i forholdet mellom MOB-anrop og DSB-oppdrag kan skyldes ulik tolkning. En presis avklaring her er nøkkel for nasjonal sammenligning.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Del 2 — Vaktordning og bemanningsstruktur")
    L.append("")
    L.append("**Kontekst (110 Sør-Vest):** Todelt skift med dag 07–19 og natt 19–07. Sentralen har")
    L.append("**6 vaktlag à 3 operatører + 1 vaktleder**. Normalbemanning er **3 operatører + VL = 4")
    L.append("personer på alle vakter** (også natt og helg). Sentralen kan på natt og helg gå ned til")
    L.append("**minimumsbemanning 2 operatører + VL = 3 personer**, og det er ikke planlagt å fylle opp")
    L.append("med vikarer ved fravær på disse skiftene. **Mer enn 50 % av vaktene på natt/helg")
    L.append("gjennomføres derfor på minimumsbemanning** (2+1 i stedet for 3+1). Sentralen tillater at")
    L.append("den 3. personen på natt/helg kan være vikar. Vi vet at noen sentraler kjører dagturnus i")
    L.append("stedet for todelt skift, og at faktisk bemanning kan avvike fra MOB-rapporten.")
    L.append("")
    L.append(f"**Spm 2.** Hvilken vaktordning kjører {sentral}?")
    L.append("")
    L.append("- [ ] Todelt skift (dag ca. 07–19, natt ca. 19–07)")
    L.append("- [ ] Dagturnus med separat natt (f.eks. 08–16 dag + egen natt)")
    L.append("- [ ] Annen ordning (beskriv under)")
    L.append("")
    L.append("> *Beskrivelse:*")
    L.append("")
    L.append("**Spm 3.** Avviker helgeordningen fra hverdager? På hvilken måte?")
    L.append("")
    L.append("> *Svar:*")
    L.append("")
    L.append("**Spm 4. — Tabell 1.1b: Normalbemanning vs. minimumsbemanning per skifttype.**")
    L.append("")
    L.append("MOB-tallet under er det dere rapporterte til DSB for 2025. **Vi ber dere fylle ut hva som er normalbemanning (planlagt nivå når alle stiller) og minimumsbemanning (det laveste nivået sentralen faktisk kan operere på).** Skillet er sentralt for kapasitetsanalysen — fyll inn antall operatører + VL der det er relevant. Hvis MOB-tallet ikke samsvarer med normal eller minimum, forklar gjerne i kommentarfeltet under.")
    L.append("")
    L.append("| Vakttype | MOB-tall (2025) | Normalbemanning (op + VL) | Minimumsbemanning (op + VL) | Maks ved topp |")
    L.append("|---|---|---|---|---|")
    L.append(f"| Dag — hverdag | {od} | | | |")
    L.append(f"| Natt — hverdag | {on} | | | |")
    L.append(f"| Dag — helg | {oh} | | | |")
    L.append(f"| Natt — helg/helligdag | {onh} | | | |")
    L.append("")
    L.append("> *Kommentar:* Andel av vaktene som gjennomføres på minimumsbemanning (anslag, %)?")
    L.append("")
    L.append("**Spm 5.** Hvordan dekkes vakter ved sykdom eller annet fravær? (**Flere svar kan velges**)")
    L.append("")
    L.append("- [ ] Tilkall fra vikarliste / ekstrahjelper")
    L.append("- [ ] Beredskapsvakt (hjemmevakt)")
    L.append("- [ ] Kolleger som tar over / forlenger egen vakt")
    L.append("- [ ] Driftes med redusert bemanning")
    L.append("- [ ] Annet: ___")
    L.append("")
    L.append("**Spm 6.** Anslagsvis hvor stor andel av vaktene dekkes av vikarer/ekstrahjelper sammenlignet med fast ansatte?")
    L.append("")
    L.append("> *Svar:*")
    L.append("")
    L.append("**Spm 7.** Er vaktlag ofte satt opp med planlagt overkapasitet (f.eks. planlagt 5, definert minimum 4)? Anslag for typisk overkapasitet per vakttype?")
    L.append("")
    L.append("> *Svar:*")
    L.append("")
    L.append(f"**Spm 8.** Besvarer vaktleder (VL) normalt innkommende nødanrop ved {sentral}?")
    L.append("")
    L.append("- [ ] Ja, alltid")
    L.append("- [ ] Ja, ved behov / høy belastning")
    L.append("- [ ] Nei, aldri")
    L.append("- [ ] Ingen dedikert VL-rolle")
    L.append("")
    L.append("> *Utdyping:*")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Del 3 — Arbeidsmetodikk: makkerpar vs solo-drift")
    L.append("")
    L.append("**Kontekst (110 Sør-Vest):**")
    L.append("Prosedyrestandarden krever at hver beredskapshendelse håndteres av to operatører")
    L.append("(«makkerpar»): én på samtale med innringer, én som håndterer ressursutkalling, loggføring")
    L.append("og oppfølging. I praksis går drift ofte over i **solo-håndtering** når flere hendelser")
    L.append("inntreffer samtidig — alternativet er å la neste innringer vente. Kvaliteten synker, men")
    L.append("blir «godt nok». Modellen vår forsøker å kvantifisere hvor ofte dette skjer.")
    L.append("")
    L.append(f"**Spm 9.** Hvordan beskriver dere prosedyrestandarden ved {sentral}?")
    L.append("")
    L.append("- [ ] Makkerpar er standard, solo-drift kun ved samtidige hendelser eller press")
    L.append("- [ ] Solo-drift er utgangspunktet; makkerpar aktiveres kun ved store hendelser")
    L.append("- [ ] Annen modell (beskriv)")
    L.append("")
    L.append("> *Beskrivelse:*")
    L.append("")
    L.append("**Spm 10.** Omtrentlig: hvor ofte må operatør jobbe solo på beredskapshendelser ved vanlig bemanning? (daglig, ukentlig, sjelden)")
    L.append("")
    L.append("> *Svar:*")
    L.append("")
    L.append("**Spm 11.** Har dere en intern norm/grense for hvor lenge et anrop kan vente før overføring til nabosentral? (Sør-Vest: 30 sek ubesvart → automatisk overføring til Agder; 10. anrop i kø overføres også.)")
    L.append("")
    L.append("> *Svar:*")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Del 4 — Hendelseskategorier og operatørbindingstider")
    L.append("")
    L.append("Studien bruker en **prosedyrebasert ankomstkonfliktmodell** der hver ny beredskapshendelse")
    L.append("måles mot kapasitetstilstanden (normal / degradert / svikt) på ankomsttidspunktet. Dette")
    L.append("krever at vi vet hvor lenge en operatør er **aktivt bundet** av en hendelse — ikke total")
    L.append("varighet i systemet, men fra anrop mottas til operatør er ferdig med oppfølging.")
    L.append("")
    L.append("BRIS gir tidsdata for beredskapshendelser med utrykning, men mangler tidsdata for alle")
    L.append("andre henvendelsestyper. Derfor trenger vi operative estimater. Kategoriseringen nedenfor")
    L.append("er utledet fra BRIS 2025 ved 110 Sør-Vest. Referansetallene er Sør-Vests estimater og er")
    L.append("oppgitt som utgangspunkt for diskusjon.")
    L.append("")
    L.append("| Kategori | Hva det er i praksis | Sør-Vest ref (min) | Ops bundet | Deres estimat (min) |")
    L.append("|---|---|---|---|---|")
    L.append("| **D-pri1 — Pri-1-utrykning (makkerpar)** | Bygningsbrann, trafikkulykke, farlig gods og andre pri-1-hendelser. Krever to operatører bundet parallelt fra første sekund (RØD = innringer-samtale, GUL = ressursvarsling/samband) gjennom hele akuttfasen | 14 (median) | 2 | |")
    L.append("| **D-aba — ABA-utrykning (serielt)** | Automatisk brannalarm som leder til utrykning fordi avklaring ikke kom innen 90 sek. Ikke pri-1 — én operatør kvitterer alarm, oppretter oppdrag og utalarmerer ressurser serielt | ca. 3 min (lengre dersom nødtelefon kommer fra stedet etterpå) | 1 | |")
    L.append("| **S — Service/overføringstest** | Servicetekniker tester brannalarmanlegg; operatør verifiserer signal og kvitterer ut | 2 | 1 | |")
    L.append("| **L-aba — ABA løst av 110 uten utrykning** | Automatisk brannalarm der nødtelefon innen 90 sek bekrefter ufarlig årsak (f.eks. matlaging) — lukkes uten utrykning. Krever Kilde=Alarm i registreringen | 4,5 (LABA n=100) | 1 | |")
    L.append("| **L-hendelse — Reell hendelse løst av 110** | Innringer melder noe reelt; operatør gir råd eller avklarer uten å sende ressurs. Inkluderer ABA-oppdrag med Kilde=Samtale (publikumsmelding om alarm uten ABA-signal) | 5 | 1 | |")
    L.append("| **L-ukjent — Løst av 110 uten initiell hendelsestype** | Oppdrag lukket som «Løst av 110» der feltet «Opprinnelig oppdragstype» ikke er satt — typisk bål-spørsmål, service lukket feil, korte avklaringer og andre henvendelser uten formell klassifisering før lukking | 3 | 1 | |")
    L.append("| **F — Feilringing** | Feilringing, «ønsket 112/113», eCall feil bruk | 0,5 | 1 | |")
    L.append("| **V — Viderevarsling** | Viderekobling til annen etat eller intern varsling | 1 | 1 | |")
    L.append("")
    L.append(f"**Spm 12.** Er kategoriseringen gjenkjennbar ved {sentral}? Mangler det en type, eller er noe slått sammen som burde vært skilt?")
    L.append("")
    L.append("> *Svar:*")
    L.append("")
    L.append("**Spm 13.** Er Sør-Vests bindingstidsestimater rimelige sammenlignet med deres operative praksis? Hvilke kategorier avviker mest, og hvorfor?")
    L.append("")
    L.append("> *Svar:*")
    L.append("")
    L.append("**Spm 14.** For beredskapshendelser (D): er det vanlig at én hendelse binder to eller flere operatører samtidig (makkerpar-håndtering)? Hvor lenge holder den parallelle bindingen?")
    L.append("")
    L.append("> *Svar:*")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Del 5 — ROS- og beredskapsanalyse")
    L.append("")
    L.append("**Innrapportert status (fra MOB):**")
    L.append(f"- ROS-analyse sist revidert: **{v(ros_aar)}**")
    L.append(f"- Beredskapsanalyse utarbeidet: **{har_ber if har_ber else '—'}**, sist revidert: **{v(ber_aar)}**")
    L.append("")
    L.append("**Spm 15.** Bekrefter dere årstallene ovenfor? Hvis nei — hva er korrekt?")
    L.append("")
    L.append("> *Svar:*")
    L.append("")
    L.append("**Spm 16.** Har dere selv god kjennskap til analysen? Brukes den aktivt i driftsplanlegging, eller er den et formelt dokument som revideres periodisk?")
    L.append("")
    L.append("> *Svar:*")
    L.append("")
    L.append("**Spm 17.** Når er neste planlagte revisjon?")
    L.append("")
    L.append("> *Svar:*")
    L.append("")
    L.append("**Spm 18.** Hvilke metoder/data bruker dere for å dimensjonere bemanningsnivå? (Beredskapsanalyse, historiske hendelsesdata, avtaler med eier, faglig skjønn, annet?)")
    L.append("")
    L.append("> *Svar:*")
    L.append("")
    L.append("**Spm 19.** Er ROS-/beredskapsanalysen i nåværende form tilstrekkelig som grunnlag for å dimensjonere antall operatører? Hva mangler eventuelt?")
    L.append("")
    L.append("> *Svar:*")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Del 6 — Operativ belastning og opplevd bemanning")
    L.append("")
    L.append("**Spm 20.** Hvor ofte opplever dere perioder der antall aktive hendelser overstiger ledig operatørkapasitet? (Daglig, ukentlig, sjelden?)")
    L.append("")
    L.append("> *Svar:*")
    L.append("")
    L.append("**Spm 21.** Hva skjer operativt når kapasitetsgrensen nås?")
    L.append("")
    L.append("- [ ] Vaktleder trer inn som operatør")
    L.append("- [ ] Overført til nabosentral")
    L.append("- [ ] Prioritering mellom hendelser")
    L.append("- [ ] Redusert kvalitet på håndtering (f.eks. solo-drift, kortere intervju)")
    L.append("- [ ] Annet: ___")
    L.append("")
    L.append("**Spm 22.** Er det et definert antall samtidige hendelser/anrop som utløser tiltak eller varsling (f.eks. bistand fra nabosentral)?")
    L.append("")
    L.append("> *Svar:*")
    L.append("")
    L.append("**Spm 23.** Hvordan oppleves dagens bemanning fra et operativt perspektiv?")
    L.append("")
    L.append("- [ ] Overdimensjonert")
    L.append("- [ ] Passe")
    L.append("- [ ] Knapt nok")
    L.append("- [ ] Underdimensjonert")
    L.append("")
    L.append("> *Utdyping (gjerne med eksempler på når det merkes):*")
    L.append("")
    # Sentralspesifikke avklaringer (Del 7) — basert på DSB 2025-avvik
    n_del1_6 = sum(1 for line in L if line.startswith('**Spm '))
    del7 = sentralspesifikke_avklaringer(sentral, start_spm=n_del1_6 + 1)
    L.extend(del7)
    n_del7 = sum(1 for line in del7 if line.startswith('**Spm '))
    neste_spm = n_del1_6 + n_del7 + 1

    L.append("---")
    L.append("")
    L.append("## Del 8 — Avsluttende kommentarer")
    L.append("")
    L.append(f"**Spm {neste_spm}.** Har det skjedd spesielle hendelser (storulykker, klimahendelser, nye oppgaver, organisasjonsendringer) i perioden 2022–2025 som har hatt vesentlig påvirkning på kapasitetssituasjonen?")
    L.append("")
    L.append("> *Svar:*")
    L.append("")
    L.append(f"**Spm {neste_spm + 1}.** Er det andre forhold ved kapasitetssituasjonen ved {sentral} som er viktig å forstå, og som ikke dekkes av spørsmålene ovenfor?")
    L.append("")
    L.append("> *Svar:*")
    L.append("")
    L.append("---")
    L.append("")
    L.append("*Takk for at dere tar dere tid til å svare. Svarene kan returneres til rune.grodem@rogbr.no.*")
    L.append("*Spørsmål kan rettes til Rune Grødem, student LOG650 Forskningsprosjekt, Høgskolen i Molde.*")

    filnavn = os.path.join(utmappe, f'{safe}.md')
    with open(filnavn, 'w', encoding='utf-8') as fout:
        fout.write('\n'.join(L))
    print(f'Skrevet: {sentral} -> {os.path.basename(filnavn)}')

print('Ferdig.')
