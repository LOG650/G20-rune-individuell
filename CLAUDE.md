# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# LOG650 – G20 Rune Grødem – Prosjektinstruksjoner for Claude

## Prosjektinfo
- **Student:** Rune Grødem, G20 Individuell
- **Emne:** LOG650 Logistikk og kunstig intelligens, Høgskolen i Molde, Vår 2026
- **Arbeidsform:** Individuelt
- **Fase nå:** Fase 3 – Gjennomføring (starter uke 12, 17. mars 2026)
- **Frist hoved-utkast:** Slutten av april 2026
- **Frist endelig rapport:** 31. mai 2026
- **Muntlig eksamen:** Tidlig juni 2026
- **Karakterkrav:** C-nivå på arbeidskrav, B-krav på rapport + muntlig

## Problemstilling
**I hvilken grad samsvarer faktisk bemanning ved norske 110-sentraler med kapasitetsbehovet
beregnet fra historiske hendelsesdata og køteoretiske modeller?**

## Dobbel ambisjon
1. **Casestudie (110 Sør-Vest):** Dokumentere om faktisk bemanning samsvarer med
   kapasitetsbehovet beregnet fra historiske LEO/BRIS-data og Erlang-C-modellen
2. **Generaliseringsambisjon:** Undersøke om strukturelle prediktorer (hendelsesvolum,
   innbyggertall, areal) kan danne grunnlag for en nasjonal, etterprøvbar
   dimensjoneringsmodell for 110-operatører — analogt med dimensjoneringsforskriften
   for brannvesenet

## Bakgrunn og motivasjon
Dimensjoneringsforskriften (FOR-2023-01-06-23) gir kvantitativ, etterprøvbar standard
for brannstasjoner basert på innbyggertall og responstid. **Ingen tilsvarende nasjonal
standard finnes for 110-operatører.** Bemanningsnivået fastsettes gjennom lokale
ROS- og beredskapsanalyser som er kvalitative og vanskelige å etterprøve kvantitativt
på tvers av sentraler. Prosjektets ambisjon er å bygge et kvantitativt referansepunkt
for 110-operatører analogt med dimensjoneringsforskriftens rolle for brannvesenet.

## Primærcase: 110 Sør-Vest
- **Skift:** Dag 07:00–19:00, Natt 19:00–07:00
- **Bemanning dag:** 3 operatører + Vaktleder (VL) = totalt 4. c_effektiv = 3
- **Bemanning natt/helg:** 2 operatører + Vaktleder = totalt 3. c_effektiv = 2
- **VL-antagelse:** Vaktleder besvarer normalt IKKE nødanrop → c_effektiv = c_total − 1
- **De facto servicegrense:** 10. anrop i kø → overføres til Agder; ubesvart etter 60 sek = brudd
- **Data tilgjengelig:** LEO/BRIS tilbake til 2020; felles LEO for alle sentraler fra høst 2024
- **ROS/beredskapsanalyse:** Tilgjengelig — forfatterens tilgang til dokumenter for 110 Sør-Vest

## Primærmodell: Erlang-C (M/M/c)
- **λ (ankomstrate):** Estimert per skiftperiode fra LEO/BRIS-data
- **μ⁻¹ (håndteringstid):** Estimert per hendelseskategori
- **c (servere):** Med VL-korreksjon (c_effektiv = c_total − 1)
- **Service level:** P(W > t) sammenlignet mot de facto grenser (10. anrop/60 sek)
- Tre analytiske dimensjoner: telefonhenvendelser (λ/Erlang-C), oppdrag (operativ aktivitet),
  samtidige aktive hendelser (kapasitetsbinding)

## Operative særtrekk (må hensyntas i modellen)
- **VL-rollen:** c_effektiv = c_total − 1
- **Aktivt hendelsebilde:** Pågående hendelser binder kapasitet utover samtaletid
- **Ring-flom (call surge):** Brudd på Poisson-uavhengighet — behandles som sensitivitetscase
- **Overløp til Agder:** 10. kø-anrop viderekoblet — de facto servicegrense
- **60-sekunders-regel:** Ubesvart anrop etter 60 sek = kapasitetsbrudd

## 12 norske 110-sentraler
Finnmark, Troms, Nordland, Trøndelag, Møre og Romsdal, Vest, Sør-Vest, Agder,
Sør-Øst, Oslo, Øst og Innlandet.

## Datakilder
| Kilde | Status |
|---|---|
| LEO/BRIS 110 Sør-Vest 2020–2025 | TILGJENGELIG |
| ROS- og beredskapsanalyse 110 Sør-Vest | TILGJENGELIG |
| DSB årsrapporter (alle sentraler) | OFFENTLIG |
| SSB befolkningsdata | OFFENTLIG |
| LEO-data tvers-sentraler (post-2024) | TILGJENGELIG |

## WBS — Fase 3 leveranser
```
L7  Rapportskjelett + intro v1                    (Uke 12)
L8  EDA — LEO/BRIS, belastningsmonstre per skift  (Uke 12–13)
L8b ROS/beredskapsanalyse-gjennomgang             (Uke 12–13)
L9  Parameterestimering (λ og μ per skiftperiode)   (Uke 13)
L10 Erlang-C modellering med VL-korreksjon        (Uke 14)
L11 Validering og sensitivitetsanalyse            (Uke 14–15)
L12 Teorikapittel                                 (Uke 14–15)
L13 Benchmarking (alle 12 sentraler via DSB)      (Uke 15)
L14 Generaliseringsanalyse                        (Uke 15–16)
L15 Resultater og diskusjon                       (Uke 16)
L16 Hoved-utkast + peer review                   (Slutten av april)
```

## Viktige filer
| Fil | Beskrivelse |
|---|---|
| `011 fase 1 - proposal/Proposal_LOG650_G20_Rune_110_v3.md` | Godkjent proposal v3 |
| `012 fase 2 - plan/Prosjektstyringsplan_G20_Rune_110.md` | Plan v1.8, innlevert 11. mars |
| `012 fase 2 - plan/Gantt_LOG650_G20_Rune_110.mpp` | Gantt med baseline (MS Project) |
| `012 fase 2 - plan/Gantt_LOG650_G20_Rune_110.xml` | Gantt XML-eksport (AI-lesbar) |
| `012 fase 2 - plan/Litteraturliste_LOG650_G20_Rune.xlsx` | 26 kilder, verifisert og fargekodet |
| `014 fase 4 - report/Rapport_LOG650_G20_Rune_110_v0.1.md` | Rapportskjelett v0.1 (markdown) |
| `KI_erklæring_LOG650_G20_Rune.md` | Løpende KI-brukslogg og erklæring |
| `004 data/` | Rådata (gitignored) — LEO/BRIS legges her i fase 3 |
| `OLD_forkastet/` | Gammelt prosjekt (røykdykkerbekledning/METRIC) — ikke bruk |

## Analyse — skript og notebooks

### Eksisterende skript
| Fil | Beskrivelse | Kjør med |
|---|---|---|
| `analyse/scripts/benchmark_trend_analyse.py` | Trendanalyse og benchmarking alle 12 110-sentraler 2022–2025. Laster MOB-filer + BRIS fullrapport, produserer 3 figurer i `figurer/` og `analyse/benchmark_tabell.csv` | `py "G20-rune-individuell/analyse/scripts/benchmark_trend_analyse.py"` |

### Datafilnavn i `004 data/` (eksisterende nedlastede filer)
```
# DSB MOB-filer (bemanningsdata alle sentraler)
20260315_174537_MOB_2022_110-sentral.xlsx
20260315_174530_MOB_2023_110-sentral.xlsx
20260315_174523_MOB_2024_110-sentral.xlsx
20260315_174514_MOB_2025_110-sentral.xlsx

# BRIS fullrapport (hendelsesdata 2025, alle sentraler)
20260315_174350_fullrapport.csv   — UTF-8 med BOM (encoding="utf-8-sig")
                                    Separator: auto (sep=None, engine="python")
                                    Hopp over 2 rader (skiprows=2), rad 1 er header

# Interndokumenter (110 Vest / Bergen brannvesen)
Beredskapsanalyse-110-Vest-30-04-2022.pdf
Beredskapsanalyse-Bergen-brannvesen-2023.pdf
Risiko-og-sarbarhetsanalyse-110-Vest.pdf
Risiko-og-sarbarhetsanalyse-Bergen-brannvesen-2023-.pdf
```

### Kjente BRIS-datastruktur (2025 fullrapport)
- **Nøkkelkolonner:** `Dato anrop` (format `%d.%m.%Y`), `Time på døgnet`, `110-sentral`, `Oppdrag ID`, `Kilde` (verdier: `Alarm` / `Samtale`)
- **110 Sør-Vest 2025:** 61 964 hendelsesrader, 44 kolonner
- **Kritiske datakvalitetsgrenser:**
  - `Operatør-ID`: 0 % dekning (100 % null) — systemstrukturell begrensning bekreftet av DSB
  - `Innsatsvarighet`: ~9 % dekning (kun utrykningshendelser T2/T3)
  - `Alarmbehandlingstid`: ~12 % dekning
  - T1-anrop (88 % av volum, "110-oppdrag uten involvering av brannvesen"): ingen tidsregistrering i BRIS — håndteringstid hentes fra intervjuer

### Sentralnavn-normalisering
Sentralnavn i BRIS/MOB kan ha encoding-feil (f.eks. `S?r-Vest 110`, `S\u00f8r-Vest 110`). Bruk `SENTRALER_NORM`-ordboken i `benchmark_trend_analyse.py` som referanse ved ny kode.

### Notebooks
`analyse/notebooks/` er tom — EDA-notebooks skal opprettes her i fase 3.

## Tekniske retningslinjer
- **Rapport skrives i Markdown, IKKE Word** — foreleseren var eksplisitt på dette (9. mars 2026).
  Én fil per kapittel, lenket inn i hoved-`rapport.md`. Se `014 fase 4 - report/`.
- **`005 report/`** — mappe for ferdig rapport-output (f.eks. eksporterte tabeller og figurer til rapport). Ikke forveksle med `014 fase 4 - report/` som er selve rapportskriptet.
- **Filskriving:** Edit/Write-tool kan feile med EEXIST på noen mapper —
  bruk Python-skript i `C:\Users\runeg\AppData\Local\Temp\` og kjør med `py "C:/path/script.py"`
- **Encoding:** Alltid `encoding='utf-8'` i Python-filoperasjoner
- **Bash Unicode:** Unngå heredoc med Unicode — bruk .py-skriptfiler
- **Python-stack:** pandas, numpy, scipy, matplotlib, seaborn, openpyxl
- **Versjonskontroll:** Git (GitHub: LOG650/G20-rune-individuell)
- **Referansestil:** APA 7th norsk (se `000 templates/Referansestiler/`)
- **Rådata:** Lagres i `004 data/` — aldri modifisert direkte; all behandling i Jupyter notebooks
- **KI-brukslogg:** Oppdater `KI_erklæring_LOG650_G20_Rune.md` etter hver session

## Risikofaktorer å huske
- **R2/R3:** Poisson-antagelse må testes eksplisitt på LEO/BRIS-data
- **R6:** ~~Tvers-sentraldata (LEO post-2024) — avklar tilgang~~ LUKKET: tilgang bekreftet 10. mars 2026
- **R7:** Tidskollisjon med vaktarbeid ved 110 Sør-Vest — buffer i Gantt
- **R9:** ROS-gjennomgang må formuleres som metodisk vurdering, ikke personkritikk

## Framing-retningslinje (VIKTIG)
ROS/beredskapsanalyser er **kvalitative og vanskelige å etterprøve kvantitativt** på
tvers av sentraler — IKKE at de er strategisk manipulert eller bestillingsverk.
Prosjektet *supplerer og sammenligner* med eksisterende analyser, det *angriper* dem ikke.
