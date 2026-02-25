# LOG650 - Forskningsprosjekt: Logistikk og KI

## Prosjektinfo
- **Student:** Rune Grødem (G20)
- **Emne:** LOG650, Høgskolen i Molde
- **Arbeidsform:** Individuelt
- **Frist fase 3 (hovedutkast):** 1. mai 2026
- **Frist endelig rapport:** 31. mai 2026

## Problemstilling
**Hvordan kan røykdykkerbekledning i norske brannvesen dimensjoneres optimalt når samspillet mellom usikker etterspørsel, vaskekapasitet som flaskehals, og valg av lagerpolicy er kritisk for operativ tilgjengelighet?**

## Forskningsspørsmål
- **RQ1 (kjerne):** Etterspørselsmodellering basert på BRIS-data
- **RQ2 (kjerne):** Vaskekapasitet som flaskehals (køteori)
- **RQ3 (kjerne):** Lagerpolicy-sammenligning (personlig vs. pool vs. hybrid)
- **RQ4 (sekundær):** RFID-effekt på dimensjonering
- **RQ5 (sekundær):** Generalisering til andre brannvesen

## Case
Rogaland Brann og Redning IKS (RogBR) med tre lokasjoner:
- Stangeland (hovedstasjon, vaskelinje, sentrallager)
- Schankeholen (vaskelinje, klespool)
- Innsatskonteiner (mobil beredskap)

## Kontaktpersoner RogBR
- Brannsjef Razums Viggen
- Logistikkansvarlig Tom Meyer
- Student arbeider i 110 Sør-Vest

## Teori
- **Primær:** METRIC (Sherbrooke 1968; Axsäter kap. 10.2) — multi-echelon recoverable item control
- **Støtte:** Stokastisk lagerstyring (Silver, Pyke & Peterson; Zipkin; Axsäter), Køteori M/D/∞ (Littles lov)
- **Rammeverk:** Risk-pooling, Theory of Constraints

## Nøkkeltall fra 2024-rapporten (Tom Meyer)
- 428 sett brannbekledning totalt (hel+deltid)
- Pool Stangeland: 65 sett, Pool Schankeholen: 49 sett
- Pris per sett: ca. 18 000 kr
- Utskiftningsrate: 17,5% (ca. 75 sett/år)
- Dimensjonering Stangeland: 22 sett (3 branner × 6 røykdykkere + 4 tillegg)
- Dimensjonering Schankeholen: 6 sett (2 branner × 6 røykdykkere, men bare 6 pga overlap)
- Innsatskonteiner: 6 røykdykkere (2 biler × 3 RD)

## Datagrunnlag

### BRIS-data (Datagrunnlag/20260210_203820_fullrapport_brannvesen.xlsx)
- **Omfang:** 8 098 hendelser, 580 kolonner
- **Nøkkelkolonner for analyse:**
  - Kol 0: Oppdrag ID
  - Kol 3: Oppdragstype (Brann, Ulykke, etc.)
  - Kol 4: Overordnet oppdragstype
  - Kol 9: Kommunenavn
  - Kol 14: Ansvarlig brannvesen
  - Kol 25: Time på døgnet
  - Kol 26: Dato anrop
  - Kol 28-33: Ukedag, ukenr, måned, år
  - Kol 36: Antall ressurser på oppdragsstedet
  - Kol 46: Utrykningstid
  - Kol 47: Responstid
  - Kol 49: Innsatsvarighet
  - **Kol 56: Innvendig røykdykkerinnsats (JA/NEI) - NØKKELKOLONNE for RQ1**
  - Kol 57: Kjemikaliedykkerinnsats
  - Kol 120: Type brann

## Mappestruktur
```
LOG650 LOGISTIKK OG KI/
├── CLAUDE.md                    # Denne filen
├── 01_proposal/                 # Fase 1: Godkjent proposal
├── 02_prosjektplan/             # Fase 2: Kravspesifikasjon, WBS, Gantt
├── 03_rapport/                  # Fase 3+4: Selve forskningsrapporten
├── Datagrunnlag/                # Rådatasett (BRIS-uttrekk)
├── analyse/
│   ├── notebooks/               # Jupyter notebooks for EDA og analyse
│   └── scripts/                 # Python-scripts for modellering
├── figurer/                     # Genererte figurer og visualiseringer
├── litteratur/                  # Kildenotater og referanser
├── peer_review/                 # Peer-review dokumenter
├── LOG650_Prosjektproposal_FINAL.docx
├── Vernebekledning 2024.docx    # Tom Meyers 2024-rapport
├── Oppdrag logistikk.docx       # Originaloppdraget fra avdelingsleder
└── [diverse maler og PDF-er]
```

## Teknisk stack
- Python (pandas, numpy, scipy, statsmodels, scikit-learn)
- Jupyter notebooks for analyse
- APA 7th referansestil (norsk)
- Rapport i Word (.docx) basert på NTNU-mal eller LOG650-mal

## Primær modell — METRIC
RogBR er et **lukket system med fast populasjon** (recoverable items), ikke et klassisk lagerproblem. Draktene sirkulerer mellom tilstandene: tilgjengelig → til vask → tilbake. Bestilling skjer kun ved avskrivning eller nye brukere.

**METRIC** (Multi-Echelon Technique for Recoverable Item Control, Sherbrooke 1968) er identifisert som primær modell:
- Sentrallager (Stangeland/vaskeri) løses eksakt med Poisson-kø
- Forsinkelse W₀ beregnes med Littles lov (M/D/∞)
- Hver stasjon løses separat med effektiv ledetid L̃ᵢ = Lᵢ + W₀
- Sᵢ (order-up-to nivå per stasjon) er beslutningsvariabelen

**Kjent begrensning:** METRIC antar uavhengige forsinkelser — common cause stockout adresseres i diskusjonskapittel + valideres med Monte Carlo simulering.

## Viktige retningslinjer
- Rapport 80-100 sider (ekskl. vedlegg)
- 60% tid på RQ1-RQ3, 20% på RQ4-RQ5, 20% validering/skriving
- KI brukes som analyseverktøy, ikke som forskningsbidrag
- Service-level constraint: SL ≥ 99%
- Modellen skal være parametriserbar for andre brannvesen
