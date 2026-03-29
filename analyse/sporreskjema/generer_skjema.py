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

# Finn faktiske kolonnenavn fra data — bruker eksakt match mot kjente oppdragstyper
def finn_kolonne_eksakt(df, kandidater):
    """Finn kolonnenavn ved aa matche mot liste av kjente kandidatnavn (ascii-normalisert)."""
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
    'Unodige og falske utrykninger',
    'Unodige og falske utrykninger',
    'Un\u00f8dige og falske utrykninger',
])
KOL_UTEN_BV = finn_kolonne_eksakt(sample_df, [
    '110-oppdrag uten involvering av brannvesen',
])
KOL_ANDRE   = finn_kolonne_eksakt(sample_df, ['Andre typer oppdrag'])

# Fallback: iterer alle kolonnene og match paa starten av strengen
def finn_kolonne_prefix(df, prefix):
    prefix_ascii = prefix.lower().encode('ascii', 'ignore').decode()
    for col in df.columns:
        col_ascii = str(col).lower().encode('ascii', 'ignore').decode()
        if col_ascii.startswith(prefix_ascii):
            return col
    return None

if KOL_BRANN   is None: KOL_BRANN   = finn_kolonne_prefix(sample_df, 'brann')   or 'Brann'
if KOL_ULYKKE  is None: KOL_ULYKKE  = finn_kolonne_prefix(sample_df, 'ulykke')  or 'Ulykke'
if KOL_UNODIGE is None: KOL_UNODIGE = finn_kolonne_prefix(sample_df, 'un')       or 'Unodige'
if KOL_UTEN_BV is None: KOL_UTEN_BV = finn_kolonne_prefix(sample_df, '110-oppdrag uten') or '110-oppdrag'
if KOL_ANDRE   is None: KOL_ANDRE   = finn_kolonne_prefix(sample_df, 'andre typer') or 'Andre'

print(f"Kolonner funnet: Brann={KOL_BRANN}, Ulykke={KOL_ULYKKE}, Unodige={KOL_UNODIGE}")

def v(val):
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return '-'
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

    # Trend for sammenlignbare år: kun utrykning (Brann+Ulykke), 2022 vs 2024
    # 2025 utelates fra trend fordi nytt system (LEO/OHV) endrer hva som telles
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

    lines = []
    lines.append(f"# Sporreskjema -- {sentral}")
    lines.append("## Studie: Kapasitetsanalyse av norske 110-sentraler (LOG650, Hogskolen i Molde, 2026)")
    lines.append("")
    lines.append("**Student:** Rune Grodem, G20 Individuell")
    lines.append("**Formaal:** Masteroppgaven analyserer om faktisk bemanning ved norske 110-sentraler samsvarer med kapasitetsbehovet beregnet fra historiske hendelsesdata og koeteoretiske modeller.")
    lines.append("")
    lines.append(f"> Svarene behandles konfidensielt og brukes kun i aggregert form i rapporten, med mindre {sentral} eksplisitt samtykker til navngiving.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Del 1 -- Innrapporterte data fra DSB (2022-2025)")
    lines.append("")
    lines.append("Tabellen er basert paa data dere selv har rapportert til DSB via MOB-systemet. Vi ber dere bekrefte, korrigere eller utdype disse tallene.")
    lines.append("")
    lines.append("### 1.1 Bemanning (innrapportert)")
    lines.append("")
    lines.append("| | 2022 | 2023 | 2024 | 2025 | Endring 22-25 |")
    lines.append("|---|---|---|---|---|---|")
    lines.append(f"| Ansatte heltid | {v(mob_val(2022,'ansatte'))} | {v(mob_val(2023,'ansatte'))} | {v(mob_val(2024,'ansatte'))} | {v(mob_val(2025,'ansatte'))} | {ans_endr} |")
    lines.append(f"| Operatorer dag - hverdag | {v(mob_val(2022,'op_dag_hverd'))} | {v(mob_val(2023,'op_dag_hverd'))} | {v(mob_val(2024,'op_dag_hverd'))} | {v(mob_val(2025,'op_dag_hverd'))} | |")
    lines.append(f"| Operatorer natt - hverdag | {v(mob_val(2022,'op_natt_hverd'))} | {v(mob_val(2023,'op_natt_hverd'))} | {v(mob_val(2024,'op_natt_hverd'))} | {v(mob_val(2025,'op_natt_hverd'))} | |")
    lines.append(f"| Operatorer dag - helg | {v(mob_val(2022,'op_dag_helg'))} | {v(mob_val(2023,'op_dag_helg'))} | {v(mob_val(2024,'op_dag_helg'))} | {v(mob_val(2025,'op_dag_helg'))} | |")
    lines.append(f"| Operatorer natt - helg | {v(mob_val(2022,'op_natt_helg'))} | {v(mob_val(2023,'op_natt_helg'))} | {v(mob_val(2024,'op_natt_helg'))} | {v(mob_val(2025,'op_natt_helg'))} | |")
    lines.append("")
    lines.append("### 1.2 Oppdrag med utrykning (sammenlignbare tall 2022-2024)")
    lines.append("")
    lines.append("> **Datakvalitetsmerknad:** Fra 2024 tok flere sentraler i bruk nytt operativsystem (LEO/OHV),")
    lines.append("> og i 2025 registreres alle innkommende telefonsamtaler som egne hendelsesrader.")
    lines.append("> Totalt oppdragsvolum er derfor IKKE sammenlignbart paa tvers av alle aar.")
    lines.append("> Tabellen nedenfor viser kun oppdrag MED utrykning (Brann + Ulykke), som er")
    lines.append("> konsistent registrert i alle aar uavhengig av system.")
    lines.append("")
    lines.append("| | 2022 | 2023 | 2024 | 2025* | Endring 22-24 |")
    lines.append("|---|---|---|---|---|---|")
    lines.append(f"| Oppdrag - Brann | {v(full_val(2022,KOL_BRANN))} | {v(full_val(2023,KOL_BRANN))} | {v(full_val(2024,KOL_BRANN))} | {v(full_val(2025,KOL_BRANN))} | |")
    lines.append(f"| Oppdrag - Ulykke | {v(full_val(2022,KOL_ULYKKE))} | {v(full_val(2023,KOL_ULYKKE))} | {v(full_val(2024,KOL_ULYKKE))} | {v(full_val(2025,KOL_ULYKKE))} | |")
    lines.append(f"| **Sum med utrykning** | **{v(utr22)}** | **{v(utr23)}** | **{v(utr24)}** | **{v(utr25)}** | **{utr_endr_22_24}** |")
    lines.append(f"| Unodige/falske utrykninger | {v(full_val(2022,KOL_UNODIGE))} | {v(full_val(2023,KOL_UNODIGE))} | {v(full_val(2024,KOL_UNODIGE))} | {v(full_val(2025,KOL_UNODIGE))} | |")
    lines.append("")
    lines.append("*2025-tall er inkludert for orientering, men bor ikke brukes i trendsammenligning.")
    lines.append("")
    lines.append("### 1.3 Mottatte 110-anrop (selvrapportert i MOB)")
    lines.append("")
    lines.append("> Disse tallene er sentralenes egne innrapporteringer til DSB og er uavhengig av")
    lines.append("> registreringssystemet. De kan brukes som supplerende indikator paa anropsvolum.")
    lines.append("")
    lines.append("| | 2022 | 2023 | 2024 | 2025 |")
    lines.append("|---|---|---|---|---|")
    lines.append(f"| Mottatte 110-anrop (MOB) | {v(mob_val(2022,'anrop_110'))} | {v(mob_val(2023,'anrop_110'))} | {v(mob_val(2024,'anrop_110'))} | {v(mob_val(2025,'anrop_110'))} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Del 2 -- Utdyping og korrigering")
    lines.append("")
    lines.append("**Spm 1.** Er tallene i tabellene ovenfor korrekte? Hvis nei -- hva er riktige tall, og hva forklarer avviket?")
    lines.append("")
    lines.append("> *Svar:*")
    lines.append("")
    lines.append("**Spm 2.** Tabellen viser operatorantall som registrert minimum per vakttype. Er dette faktisk laveste planlagte bemanning, eller er det et normaltall? Hva er reelt operativt minimum ved lav bemanning (f.eks. sykdom, ferie)?")
    lines.append("")
    lines.append("| Vakttype | Innrapportert | Faktisk minimum | Merknad |")
    lines.append("|---|---|---|---|")
    lines.append(f"| Dag - hverdag | {od} | | |")
    lines.append(f"| Natt - hverdag | {on} | | |")
    lines.append(f"| Dag - helg | {oh} | | |")
    lines.append(f"| Natt - helg/helligdag | {onh} | | |")
    lines.append("")
    lines.append(f"**Spm 3.** Besvarer vaktleder (VL) normalt innkommende nodanrop ved {sentral}?")
    lines.append("")
    lines.append("[ ] Ja, alltid   [ ] Ja, ved behov/hoy belastning   [ ] Nei, aldri   [ ] Ingen dedikert VL-rolle")
    lines.append("")
    lines.append(f"**Spm 4.** Oppdrag med utrykning (Brann+Ulykke) endret seg med **{utr_endr_22_24}** fra 2022 til 2024, mens ansatte heltid endret seg med **{ans_endr}** fra 2022 til 2025. Kan dere si noe om hva som forklarer denne utviklingen?")
    lines.append("")
    lines.append("> *Svar:*")
    lines.append("")
    lines.append("**Spm 5.** Har det skjedd spesielle hendelser (storulykker, klimahendelser, nye oppgaver, organisasjonsendringer) som har hatt vesentlig pavirkning paa kapasitetssituasjonen i perioden 2022-2025?")
    lines.append("")
    lines.append("> *Svar:*")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Del 3 -- Handleringstider per hendelsestype")
    lines.append("")
    lines.append("Studien bruker en koeteoretisk modell (Erlang-C) for aa beregne kapasitetsbehov. Modellen krever")
    lines.append("gjennomsnittlig operatorbindingstid per hendelsestype -- den tiden en operator aktivt er bundet")
    lines.append("til aa handtere en hendelse (ikke total hendelsesvarighet, som kan vaere mye lengre).")
    lines.append("")
    lines.append("| Type | Beskrivelse | Typiske eksempler | Estimert bindingstid (min) |")
    lines.append("|---|---|---|---|")
    lines.append("| T1 | Ren telefonhenvendelse -- ingen utrykking, ingen oppdragslogg | Test av anlegg, generelle henvendelser, feilmeldinger | |")
    lines.append("| T2 | Automatisk brannalarm (ABA) -- begrenset handleringstid uavhengig av utfall | ABA kvittert som falsk alarm ELLER bekreftet og viderekoblet | |")
    lines.append("| T3 | Hendelse med utrykning -- lang operatorbinding, potensielt flere operatorer | Brann i bygg, trafikkulykke med skadde, hjertestans med ressursutalarmering | |")
    lines.append("| T4 | Melding vurdert og lukket uten utrykning -- lengre enn T1 men kortere enn T3 | Mulig brann avkreftet via intervju, oppdrag lost av 110 | |")
    lines.append("")
    lines.append(f"**Spm 6.** Stemmer denne inndelingen med operativ praksis ved {sentral}? Er det typer som mangler, overlapper eller bor slas sammen?")
    lines.append("")
    lines.append("> *Svar:*")
    lines.append("")
    lines.append("**Spm 7.** For T3-hendelser: Hva er typisk tidsrom fra anrop mottas til operator er ferdig med aktiv handtering (selv om oppdraget fortsatt er apent i systemet)? Er det vanlig at en T3-hendelse binder mer enn en operator samtidig?")
    lines.append("")
    lines.append("> *Svar:*")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Del 4 -- ROS- og beredskapsanalyse")
    lines.append("")
    lines.append("**Innrapportert status (fra MOB):**")
    lines.append(f"- ROS-analyse sist revidert: **{v(ros_aar)}**")
    lines.append(f"- Beredskapsanalyse utarbeidet: **{har_ber if har_ber else '-'}**, sist revidert: **{v(ber_aar)}**")
    lines.append("")
    lines.append("**Spm 8.** Bekrefter dere disse arstallene? Hvis nei -- hva er korrekte tall?")
    lines.append("")
    lines.append("> *Svar:*")
    lines.append("")
    lines.append("**Spm 9.** Naar er neste planlagte revisjon av ROS-/beredskapsanalysen?")
    lines.append("")
    lines.append("> *Svar:*")
    lines.append("")
    lines.append("**Spm 10.** Hvilke metoder/modeller bruker dere for aa dimensjonere bemanningsnivaa? Er det basert paa beredskapsanalysen, historiske data, avtaler, eller annet?")
    lines.append("")
    lines.append("> *Svar:*")
    lines.append("")
    lines.append("**Spm 11.** Mener dere at ROS- og beredskapsanalyser i sin navaerende form er tilstrekkelig som grunnlag for aa dimensjonere antall operatorer? Hva er eventuelt de viktigste manglene?")
    lines.append("")
    lines.append("> *Svar:*")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Del 5 -- Sammenfallende hendelser")
    lines.append("")
    lines.append("**Spm 12.** Opplever dere perioder der antall samtidige aktive hendelser overstiger operatorkapasiteten? Hvor hyppig skjer dette, og i hvilke situasjoner?")
    lines.append("")
    lines.append("> *Svar:*")
    lines.append("")
    lines.append("**Spm 13.** Hva skjer operativt naar kapasitetsgrensen naas?")
    lines.append("")
    lines.append("[ ] Vaktleder trer inn som operator   [ ] Overfort til nabosentral   [ ] Prioritering mellom hendelser   [ ] Annet: ___")
    lines.append("")
    lines.append("**Spm 14.** Er det et definert antall samtidige hendelser/anrop som utloster tiltak eller varsling (f.eks. bistand fra nabosentral)?")
    lines.append("")
    lines.append("> *Svar:*")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Del 6 -- Avsluttende kommentarer")
    lines.append("")
    lines.append(f"**Spm 15.** Er det andre forhold ved kapasitetssituasjonen ved {sentral} som dere mener er viktig aa forsta, og som ikke dekkes av sporsmalene ovenfor?")
    lines.append("")
    lines.append("> *Svar:*")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Takk for at dere tar dere tid til aa svare. Svarene kan returneres til [e-post] innen [frist].*")
    lines.append("*Sporsmal kan rettes til Rune Grodem, student LOG650, Hogskolen i Molde.*")

    filnavn = os.path.join(utmappe, f'{safe}.md')
    with open(filnavn, 'w', encoding='utf-8') as fout:
        fout.write('\n'.join(lines))
    print(f'Skrevet: {sentral}')

print('Ferdig.')
