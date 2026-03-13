# Kapasitetsstyring og bemanningsdimensjonering ved norske 110-sentraler
## En køteoretisk analyse av operatørkapasitet basert på historiske hendelsesdata

---

**Emne:** LOG650 – Logistikk og kunstig intelligens
**Høgskolen i Molde, Vår 2026**
**Student:** Rune Grødem, G20 Individuell
**Veileder:** [NAVN]
**Dato:** [DATO]
**Versjon:** 0.1 – Skall

---

## Sammendrag

> *[Utkast — skrives endelig sist, etter at alle resultater foreligger. Erstat dette avsnittet med ferdig sammendrag (ca. 200–300 ord).]*

Norske 110-sentraler er kritisk beredskapsinfrastruktur som mottar nødmeldinger og koordinerer brann- og redningsinnsats. Bemanningsnivået fastsettes lokalt gjennom risiko- og beredskapsanalyser (ROS), men det finnes ingen nasjonal, kvantitativ standard for hvordan operativ belastning oversettes til konkret bemanning.

Denne rapporten analyserer i hvilken grad faktisk bemanning ved norske 110-sentraler samsvarer med kapasitetsbehovet beregnet fra historiske hendelsesdata og køteoretiske modeller. Erlang-C-modellen (M/M/c) benyttes som primærmodell, kalibrert mot LEO/BRIS-data fra 110 Sør-Vest for perioden [PERIODE]. Resultater benchmarkes mot alle norske 110-sentraler via DSBs årsrapporter.

**Nøkkelord:** 110-sentral, bemanningsdimensjonering, Erlang-C, M/M/c, køteori, kapasitetsanalyse, LEO, beredskap

---

## Innholdsfortegnelse

1. [Innledning](#1-innledning)
2. [Litteratur](#2-litteratur)
3. [Teori](#3-teori)
4. [Casebeskrivelse — 110 Sør-Vest](#4-casebeskrivelse)
5. [Metode og data](#5-metode-og-data)
6. [Modell](#6-modell)
7. [Analyse og resultater](#7-analyse-og-resultater)
8. [Diskusjon](#8-diskusjon)
9. [Konklusjon](#9-konklusjon)
10. [Referanser](#10-referanser)
11. [Vedlegg](#11-vedlegg)

---

## 1. Innledning

> *[1–3 sider. Led leseren fra generelt tema → kjent kunnskap → kunnskapsgap → vår problemstilling. Skap nysgjerrighet — ikke avsløre resultatet.]*

### 1.1 Bakgrunn og tema

Norske 110-sentraler er det primære kontaktpunktet for brann- og redningsnødmeldinger i Norge. De tolv sentralene [LISTE SENTRALER] opererer døgnet rundt og koordinerer utrykningsressurser over store geografiske områder.

Bemanningsdimensjonering av 110-operatorer reguleres av brann- og redningsvesenforskriften, som pålegger minimum to operatører i vaktrommet, men overlater fastsettelse av bemanning utover dette til lokale risiko- og beredskapsanalyser. I kontrast gir dimensjoneringsforskriften (FOR-2023-01-06-23) ferdige, etterprøvbare bemanningskrav for kasernert og deltidsbrannvesen basert på innbyggertall og responstid. En tilsvarende kvantitativ standard mangler for 110-operatorer.

> *[Aktualisér temaet: hva skjer dersom 110 er underdimensjonert? Hva koster overbemanning? Kort om beredskapslogikk — kapasitetsbuffer er ikke sløsing.]*

### 1.2 Tidligere forskning og kunnskapsgap

> *[SKRIVES ETTER LITTERATURSØK — ca. ½–1 side. Hva finnes av forskning på 110-dimensjonering, call-center-kapasitet og Erlang-C i beredskapsoperative systemer? Hva mangler?]*

Erlang-C-modellen er veletablert innen kapasitetsplanlegging for fler-server telefonisystemer og call-center-miljøer (Erlang 1917; Gans et al. 2003; [YTTERLIGERE REF]). Modellen er imidlertid sjelden anvendt på nødmeldesentraler med de særtrekkene som kjennetegner 110-operasjoner — herunder aktivt hendelsebilde, ring-flom og VL-rollen.

> *[Identifiser kunnskapsgapet eksplisitt: «ingen studier har kvantitativt analysert…»]*

### 1.3 Problemstilling

**I hvilken grad samsvarer faktisk bemanning ved norske 110-sentraler med kapasitetsbehovet beregnet fra historiske hendelsesdata og køteoretiske modeller?**

Problemstillingen adresseres gjennom følgende forskningsspørsmål:

- **RQ1:** Hva er ankomstraten (λ) til 110 Sør-Vest per skiftperiode, og hvilke belastningsmønstre fremgår av historiske LEO/BRIS-data?
- **RQ2:** Hva er gjennomsnittlig håndteringstid (μ⁻¹) per hendelseskategori, og i hvilken grad binder aktivt hendelsebilde operatørkapasitet utover samtaletid?
- **RQ3:** Hvilken bemanningsanbefaling gir Erlang-C-modellen per skiftperiode ved definert servicegrad, og hvordan samsvarer dette med faktisk bemanning?
- **RQ4:** I hvilken grad gir eksisterende ROS- og beredskapsanalyse for 110 Sør-Vest et tilstrekkelig metodisk grunnlag for å begrunne faktisk bemanning?
- **RQ5:** Kan strukturelle prediktorer (hendelsesvolum, innbyggertall, areal) danne grunnlag for en generaliserbar dimensjoneringsmodell på tvers av norske 110-sentraler?

### 1.4 Avgrensninger

Prosjektet avgrenses til følgende:

- **Vaktromsbemanning** — ikke ressursdisponering i brannvesenet, taktisk hendelseshåndtering eller organisatoriske beslutninger
- **Retrospektivt og planleggingsrettet** — ikke et sanntidssystem for kapasitetsstyring
- **2024–2025-data prioriteres** for benchmarking og sammenlignbarhetsanalyse; eldre data (2020–2023) benyttes for trendanalyse
- **Ekstraordinære hendelser** (langvarige storbranner, katastrofescenarier) holdes utenfor modellens primære gyldighetsområde og behandles i diskusjonskapittelet
- **Ring-flom (call surge)** belyses som operativ ekstrembelastning, men modelleres ikke som primærscenario

### 1.5 Rapportens struktur

> *[Kort veiviser — 1 avsnitt. «Kapittel 2 presenterer… Kapittel 3 gir det teoretiske grunnlaget…»]*

---

## 2. Litteratur

> *[1–2 sider. Systematisk litteratursøk: søkeord, databaser, inklusjons-/eksklusjonskriterier, antall treff. Kan presenteres som tabell eller flytskjema (PRISMA-lignende). Oppsummer hva litteraturen sier og hva som mangler.]*

### 2.1 Søkestrategi

> *[SKRIVES ETTER LITTERATURSØK — databaser (Scopus, Web of Science, Google Scholar), søkeord (Erlang-C, emergency dispatch, staffing, queuing theory, call center capacity, 110-sentraler), tidsavgrensning, språk, inklusjonskriterier.]*

**Søkeord benyttet:**
`Erlang-C`, `M/M/c queue`, `emergency dispatch staffing`, `public safety answering point`, `PSAP capacity`, `call center dimensioning`, `queue theory emergency services`, `nødmeldesentral`, `110-sentral bemanning`

| Database | Søkeord | Treff | Inkludert |
|---|---|---|---|
| [FYLLE INN] | | | |

### 2.2 Funn fra litteraturen

> *[SKRIVES ETTER LITTERATURSØK — gruppert etter tema: (a) Erlang-C og call-center-kapasitet, (b) beredskapsoperative systemer og dimensjonering, (c) norske 110-sentraler og beredskapsplanlegging.]*

---

## 3. Teori

> *[4–6 sider. Presentér det teoretiske rammeverket som modellen hviler på. Definér begreper. Jf. mal: teoridelen danner grunnlaget for videre metodevalg.]*

### 3.1 Køteori — grunnbegreper

Køteori er den matematiske studien av systemer der etterspørsel etter en ressurs overstiger øyeblikkelig tilgjengelig kapasitet (Gross et al. 2008). Et køsystem beskrives ved Kendalls notasjon A/B/c/K/N/D, der:

- **A** = ankomstprosess (M = Markovsk/Poisson)
- **B** = servicetidfordeling (M = eksponentiell, D = deterministisk, G = generell)
- **c** = antall servere (operatører)
- **K** = systemkapasitet (købegrensning); ∞ dersom ubegrenset
- **N** = populasjonsstørrelse; ∞ dersom ubegrenset
- **D** = betjeningsrekkefølge (FCFS = First Come, First Served)

#### 3.1.1 Poissonprosessen

Hendelsesankomster modelleres som en Poisson-prosess med rate λ når ankomstene er:

1. **Uavhengige** — ankomst av én hendelse påvirker ikke sannsynligheten for neste
2. **Stasjonære** — rate λ er konstant innenfor analyseperioden
3. **Enkeltankomster** — maks én ankomst per infinitesimalt tidsintervall

Ankomstintervallene er da eksponentielt fordelt med tetthetsfunksjon:

```
f(t) = λ · exp(−λt),   t ≥ 0
```

> *[Beskriv empirisk test av Poisson-antagelsen — Kolmogorov-Smirnov, χ²-test, overdispersjon.]*

#### 3.1.2 Eksponentiell servicetid

Servicetiden (håndteringstid) antas eksponentielt fordelt med rate μ, slik at gjennomsnittlig servicetid er 1/μ. Eksponentialfordelingen har en minnetapsegenskapen (memoryless property), som forenkler analysen vesentlig.

> *[Diskutér om eksponentiell servicetid er rimelig for 110 — ulik håndteringstid per kategori T1–T4.]*

### 3.2 M/M/c — Erlang-C-modellen

M/M/c-modellen (Erlang-C) er et køsystem med:
- Poissonfordelte ankomster (rate λ)
- Eksponentielle servicetider (rate μ per server)
- c parallelle servere
- Ubegrenset kø (ingen kunder forlater systemet uten å bli betjent)

#### 3.2.1 Trafikkintensitet

Systembelastningen (trafikkintensitet) er:

```
ρ = λ / (c · μ)
```

For stabilt system kreves ρ < 1, dvs. λ < c · μ.

Total tilbudt trafikk (Erlang):

```
A = λ / μ
```

#### 3.2.2 Erlang-C-formelen

Sannsynligheten for at en innkommende henvendelse må vente i kø (køsannsynlighet):

```
C(c, A) = [A^c / (c! · (1 − ρ))] / [Σ_{k=0}^{c-1} A^k/k! + A^c / (c! · (1 − ρ))]
```

#### 3.2.3 Prestasjonsmål

Fra Erlang-C-formelen utledes sentrale prestasjonsmål:

| Mål | Formel | Tolkning |
|---|---|---|
| Gjennomsnittlig ventetid i kø | W_q = C(c,A) / (c·μ − λ) | Forventet ventetid for en henvendelse som må vente |
| Gjennomsnittlig antall i kø | L_q = λ · W_q | Littles lov |
| Sannsynlighet for ventetid > t | P(W > t) = C(c,A) · exp(−(c·μ−λ)·t) | Servicegradmål |
| Anbefalt c for servicegrad SL | Min c s.t. P(W > T) ≤ 1 − SL | Beslutningsvariabel |

#### 3.2.4 Servicegrad og dimensjoneringsanbefaling

Anbefalt bemanningsnivå c* er det laveste c som oppfyller:

```
P(W > T_max) ≤ 1 − SL_target
```

der T_max er maksimal akseptabel ventetid og SL_target er ønsket servicegrad.

> *[For 110 Sør-Vest: T_max ≈ 60 sek (lovkrav / 60-sekunders-regel), SL_target = [AVKLARES] — mulig 95% eller høyere.]*

### 3.3 Kapasitetsstyring i beredskapsoperative systemer

> *[SKRIVES ETTER LITTERATURSØK — skille mellom effektivitetsorienterte systemer (minimér kø) og beredskapsorienterte systemer (garantér respons i kritiske situasjoner). Lav kapasitetsutnyttelse er ikke sløsing i beredskapssystemer — buffer for samtidige hendelser og ring-flom.]*

#### 3.3.1 Beredskapsbuffer og ekstrembelastning

> *[Teorifundament for kapasitetsbuffer. Ring-flom som brudd på Poisson-uavhengighet.]*

### 3.4 KI som analyseverktøy

LOG650 er et emne i logistikk og kunstig intelligens, og prosjektet benytter KI-verktøy i analyse og rapportutforming. Implementasjonen av Erlang-C-modellen er gjennomført i Python (se avsnitt 5.4), mens bruk av generative KI-verktøy (Claude, GitHub Copilot) er dokumentert i Vedlegg D i henhold til kravene for LOG650.

---

## 4. Casebeskrivelse

> *[2–3 sider. Beskriv 110 Sør-Vest: kontekst, struktur, operative særtrekk. Kun det som er nødvendig for å forstå problemet — ikke mer. Rød tråd til problemstillingen.]*

### 4.1 Norske 110-sentraler — oversikt

Norge har tolv 110-sentraler som dekker hele landets befolkning. Fra høsten 2024 benytter alle sentraler felles oppdragshåndteringssystem (LEO), noe som for første gang muliggjør sammenlignbare hendelsesdata på tvers av sentraler.

> *[Tabell: alle 12 sentraler med dekningsområde, innbyggertall, hendelsesvolum (fra DSB-årsrapport 2025).]*

### 4.2 110 Sør-Vest — primærcase

110 Sør-Vest dekker [DEKNINGSOMRÅDE] med [INNBYGGERTALL] innbyggere og koordinerer brann- og redningsinnsats for [ANTALL] kommuner.

#### 4.2.1 Skiftstruktur og bemanningsnivå

> *[Beskriv faktisk bemanningsnivå basert på tilgjengelig dokumentasjon:]*

| Skifttype | c_total | c_effektiv (VL-korreksjon) |
|---|---|---|
| Dagskift (hverdager) | 4 (3 op. + VL) | 3 |
| Nattskift / helg | 3 (2 op. + VL) | 2 |

**VL-rollen:** Vakthavende leder (VL) besvarer normalt ikke nødanrop direkte, men koordinerer ressurser og ivaretar ledelsesansvar. Dette medfører at effektiv operatørkapasitet er `c_effektiv = c_total − 1`. Denne forutsetningen valideres gjennom intervjuer med operativt personell (jf. avsnitt 5.2.3).

#### 4.2.2 Hendelsestypologi

Basert på operativ arbeidsmetodikk ved 110 Sør-Vest skilles mellom fire hendelseskategorier:

| Type | Beskrivelse | Forventet håndteringstid | Operatørbelastning |
|---|---|---|---|
| T1 | Ren telefonhenvendelse — lukket uten initiell hendelsestype | Kort | Én operatør, samtaletid |
| T2 | Automatisk brannalarm (ABA) | Middels | Én operatør, begrenset oppfølging |
| T3 | Hendelse med utrykking | Lang | Potensielt krav om simultane operatører |
| T4 | Hendelse vurdert og avsluttet uten utrykking | Variabel | Én operatør |

> *[Typologien valideres mot data i avsnitt 5.2 — beskriv eventuelt justeringer her.]*

#### 4.2.3 Operative særtrekk og kapasitetsgrenser

| Særtrekk | Beskrivelse | Implikasjon for analyse |
|---|---|---|
| Overløp til Agder | 10. kø-anrop viderekoblet automatisk | De facto servicegrense — proxy for definert servicegrad |
| 60-sekunders-regel | Ubesvarte anrop etter 60 sek = kapasitetsbrudd | Proxy for T_max i Erlang-C |
| Aktivt hendelsebilde | Pågående hendelser binder operatørkapasitet utover samtaletid | Økt effektiv håndteringstid; Erlang-C-forutsetning utfordres |
| Ring-flom (call surge) | Én hendelse utløser mange samtidige anrop | Brudd på Poisson-uavhengighet |

### 4.3 ROS- og beredskapsanalysegrunnlag

> *[Kort intro — detaljer i avsnitt 7.3 (RQ4). Referer til at 110 Sør-Vest har en beredskapsanalyse som formelt begrunner bemanningsnivået.]*

---

## 5. Metode og data

> *[3–4 sider. Metodevalg og datagrunnlag. Beskriv hva som er gjort — ikke resultatene.]*

### 5.1 Forskningsdesign

Prosjektet gjennomføres som en **kvantitativ casestudie** av 110 Sør-Vest med benchmarking mot alle norske 110-sentraler. Forskningsdesignet er **retrospektivt og planleggingsrettet** — analysen baseres på historiske hendelsesdata for å vurdere om faktisk bemanning er tilstrekkelig gitt observert belastning.

Tre komplementære analysekomponenter benyttes:

| Analysekomponent | Primærvariabel | Funksjon |
|---|---|---|
| Kømodell (Erlang-C) | Innkommende telefonhenvendelser (λ) | Beregne nødvendig operatørkapasitet |
| Operativ belastningsanalyse | Antall oppdrag/hendelser | Kartlegge faktisk operativ aktivitet |
| Kapasitetsbinding | Samtidige aktive hendelser | Forstå operatørbinding utover samtaletid |

### 5.2 Data

#### 5.2.1 LEO/BRIS-data (primærdata)

**Kilde:** Hendelsesdata fra 110 Sør-Vest, eksportert fra LEO/BRIS-systemet
**Periode:** [AVKLAR — 2020–2025, primært 2024–2025]
**Omfang:** [ANTALL HENDELSER] hendelser, [ANTALL KOLONNER] kolonner

Nøkkelvariabler benyttet i analysen:

| Variabel | Kolonne | Beskrivelse |
|---|---|---|
| Hendelsestidspunkt | [KOL] | Anropstidspunkt — grunnlag for λ-estimering |
| Oppdragstype | [KOL] | Grunnlag for hendelsestypologi T1–T4 |
| Varighet / innsatsvarighet | [KOL] | Grunnlag for μ-estimering |
| Ressursutsendelse | [KOL] | Skille T3 fra T1/T4 |
| [YTTERLIGERE VARIABLER] | | |

**Datakvalitetsvurdering:**

> *[SKRIVES ETTER EDA — manglende verdier, feilkoding, dekningsgrad per periode. Dokumentér transformasjoner her.]*

#### 5.2.2 DSB årsrapporter 2025

**Kilde:** Direktoratet for samfunnssikkerhet og beredskap
**Innhold:** Bemanning per vakttype, antall operatørplasser, totalt anropsvolum for alle norske 110-sentraler
**Bruk:** Benchmarking — sammenligning av modellanbefaling mot faktisk registrert bemanning

#### 5.2.3 Strukturerte intervjuer

**Formål:** Estimere og validere håndteringstid per hendelseskategori; validere VL-forutsetningen
**Utvalg:** [ANTALL] intervjuobjekter ved 110 Sør-Vest — [ROLLE/FUNKSJON]
**Gjennomføring:** [DATO/PERIODE], strukturert intervjuguide (se Vedlegg X)

> *[Oppgi: Varighet, format (telefon/oppmøte/Teams), transkripsjonsmetode, anonymisering.]*

#### 5.2.4 SSB befolkningsdata

Innbyggertall per sentrals dekningsområde benyttes i generaliseringsanalysen (RQ5). Data hentet fra SSB Statistikkbanken, referansedato [DATO].

#### 5.2.5 ROS- og beredskapsanalyse (110 Sør-Vest)

Internt planleggingsdokument — tilgjengelig via forfatterens operative tilknytning til 110 Sør-Vest. Benyttes til kritisk dokumentanalyse (RQ4).

### 5.3 Empirisk validering av modellforutsetninger

Før Erlang-C-modellen kan tas i bruk, valideres nøkkelforutsetningene empirisk mot dataene:

| Forutsetning | Test | Forventet resultat |
|---|---|---|
| Poisson-ankomster | Kolmogorov-Smirnov-test mot eksponentialfordeling; overdispersjonstest | Diskuteres i avsnitt 7.1 |
| Stasjonær ankomstrate | Segmentér data per tidsperiode (skift/time/ukedag) | Periode-spesifikke λ-estimater |
| Eksponentielle servicetider | Histogram og K-S-test av håndteringstider per kategori | Diskuteres i avsnitt 7.2 |
| Uavhengige ankomster | Identifisér call surge-hendelser; ACF-analyse | Diskuteres i avsnitt 8 |


### 5.4 KI-verktøy og Python-implementasjon

Erlang-C-modellen er implementert i Python ved bruk av bibliotekene `scipy`, `numpy`, `pandas`, `matplotlib` og `seaborn`. Kildekode og Jupyter notebooks er versjonskontrollert på GitHub (se Vedlegg A).

Generative KI-verktøy (Claude Sonnet 4.6, GitHub Copilot) er benyttet som støtteverktøy for koding, litteratursøk og rapportskriving. All bruk er dokumentert med dato, kontekst og hva som ble produsert (se Vedlegg D — Dokumentasjon av KI-bruk). Alle analytiske beslutninger, tolkninger og konklusjoner er forfatterens egne.

---

## 6. Modell

> *[2–3 sider. Presentér den matematiske modellen. Én-til-én sammenheng med problemstillingen. Presist — bruk symboler gjennomgående. Jf. forelesning: «modellen er det viktigste kapittelet — det er her du skaper noe nytt».]*

### 6.1 Modellbeskrivelse

110 Sør-Vest modelleres som et M/M/c-køsystem med følgende parametere:

**Parametre (input — gitt fra data):**

| Symbol | Beskrivelse | Kilde |
|---|---|---|
| λ | Ankomstrate innkommende henvendelser [anrop/time] | LEO/BRIS-data |
| μ | Servicerate per operatør [anrop/time] = 1/E[håndteringstid] | LEO/BRIS + intervjuer |
| c_effektiv | Antall effektive servere = c_total − 1 | Bemanningsdata + VL-validering |
| T_max | Maksimal akseptabel ventetid [sek] | 60 sek (operativ grense) |
| SL_target | Ønsket servicegrad: P(W ≤ T_max) ≥ SL_target | [AVKLARES — foreslår 95%] |

**Variabel (beslutning):**

| Symbol | Beskrivelse |
|---|---|
| c* | Anbefalt antall effektive operatører per skiftperiode |

**Målfunksjon:**

Finn laveste c* slik at:

```
P(W > T_max) ≤ 1 − SL_target
```

Tilsvarende: finn c* = min{c : C(c, A) · exp(−(c·μ − λ)·T_max) ≤ 1 − SL_target}

der A = λ/μ er total tilbudt trafikk og C(c, A) er Erlang-C-formelen (avsnitt 3.2.2).

**Krav (constraints):**

- ρ = λ/(c·μ) < 1 (stabilitetskrav — systemet kan ikke motta mer enn det leverer)
- c_total ≥ 2 (lovpålagt minimum: to personer i vaktrommet, inkl. VL); tilsvarende c_effektiv ≥ 1 etter VL-korreksjonen

### 6.2 VL-korreksjon

Modellen opererer eksplisitt med `c_effektiv = c_total − 1` som default, basert på at VL normalt ikke besvarer nødanrop. Sensitivitetsanalyse (avsnitt 7.4) evaluerer modellens robusthet dersom VL-antagelsen ikke holder i praksis.

### 6.3 Periode-segmentert analyse

110 Sør-Vest opererer med to operative skift: dag (07:00–19:00) og natt (19:00–07:00). Ankomstraten λ varierer imidlertid innen og mellom skiftene. EDA (avsnitt 7.1) vil avgjøre om to perioder er tilstrekkelig for analysen, eller om finer segmentering (f.eks. dag/kveld/natt) gir bedre modellpresisjon.

| Periode | Tentativt tidsrom | Tilsvarende skift |
|---|---|---|
| Dag | 07:00–19:00 | Dagskift |
| Natt | 19:00–07:00 | Nattskift |
| *[Evt. underperioder]* | *[Fastsettes etter EDA]* | — |

> *[Endelig segmentering fastsettes etter EDA — belastningsmønstre per time og ukedag avgjør granulariteten.]*

### 6.4 Implementasjon

Modellen er implementert i Python. Erlang-C beregnes via:

```python
# scipy.special.factorial for stabilt beregning av store fakulteter
# Iterativ løsning for c* gitt SL_target og T_max
# Se Vedlegg X — Python-kode og Jupyter notebook
```

Kildekode er tilgjengelig på GitHub: [LENKE]

---

## 7. Analyse og resultater

> *[Hoveddelen — 10–15 sider. Presenter resultater kaldt og objektivt. Ingen tolkning her — det kommer i diskusjonen. Tabeller og figurer med forklarende tekst.]*

### 7.1 RQ1 — Eksplorativ dataanalyse og ankomstrater

> *[SKRIVES ETTER EDA]*

#### 7.1.1 Datakvalitet og dekningsgrad

> *[Beskriv rådata: manglende verdier, periode, volum. Transformasjoner dokumentert.]*

#### 7.1.2 Belastningsmønstre

> *[Figur: anropsvolum per time på døgnet, per ukedag, per måned. Identifiser toppbelastning.]*

#### 7.1.3 Hendelsestypefordeling

> *[Tabell: andel T1/T2/T3/T4 av totalt volum. Validering av typologi mot data.]*

#### 7.1.4 Estimerte ankomstrater per periode

| Periode | λ [anrop/time] | 95% KI | n (observasjoner) |
|---|---|---|---|
| Dag | [VERDI] | [KI] | [n] |
| Kveld | [VERDI] | [KI] | [n] |
| Natt | [VERDI] | [KI] | [n] |

#### 7.1.5 Test av Poisson-forutsetning

> *[K-S-test resultater. Overdispersjon? Konklusjon: holder forutsetningen, eller bør alternativ fordeling vurderes?]*

### 7.2 RQ2 — Håndteringstid og kapasitetsbinding

> *[SKRIVES ETTER DATA/INTERVJUER]*

#### 7.2.1 Estimerte håndteringstider

| Hendelsestype | Gjsn. håndteringstid [min] | Std.avvik | Kilde |
|---|---|---|---|
| T1 | [VERDI] | | LEO/BRIS |
| T2 | [VERDI] | | LEO/BRIS |
| T3 | [VERDI] | | LEO/BRIS + intervju |
| T4 | [VERDI] | | LEO/BRIS |
| **Vektet gjennomsnitt** | **[VERDI]** | | |

#### 7.2.2 Aktivt hendelsebilde — kapasitetsbinding utover samtaletid

> *[Analyse av simultane aktive hendelser. Figur: distribusjon av antall simultane T3-hendelser. Implikasjon for effektiv håndteringstid.]*

### 7.3 RQ3 — Erlang-C-dimensjonering

> *[Kjerneresultat.]*

#### 7.3.1 Bemanningsanbefaling per skiftperiode

| Periode | λ | μ | A | c_faktisk | c* (SL=[X]%) | Kapasitetsgap |
|---|---|---|---|---|---|---|
| Dag | | | | 3 | [VERDI] | [+/−] |
| Kveld | | | | [VERDI] | [VERDI] | [+/−] |
| Natt | | | | 2 | [VERDI] | [+/−] |

> *[Figur: Erlang-C servicegrad som funksjon av c for hver periode. Marker faktisk c og c*.]*

#### 7.3.2 Beregnet servicegrad ved faktisk bemanning

| Periode | c_faktisk | P(W ≤ 60 sek) | E[W_q] [sek] | Vurdering |
|---|---|---|---|---|
| Dag | 3 | [VERDI]% | [VERDI] | [Over/Under SL-grense] |
| Natt | 2 | [VERDI]% | [VERDI] | [Over/Under SL-grense] |

### 7.4 Sensitivitetsanalyse

> *[SKRIVES ETTER MODELLERING]*

#### 7.4.1 VL-korreksjon

> *[Hva skjer med c* dersom VL i realiteten besvarer henvendelser 20% av tiden?]*

#### 7.4.2 Variasjon i ankomstrate

> *[Hva er c* ved ±20% variasjon i λ — robust modell?]*

#### 7.4.3 Servicegrad-target

> *[c* ved SL = 90%, 95%, 99%.]*

### 7.5 RQ4 — Gjennomgang av eksisterende ROS- og beredskapsanalyse

> *[SKRIVES ETTER DOKUMENTANALYSE]*

#### 7.5.1 Dimensjonerende hendelser i analysen

> *[Hva legger eksisterende ROS-analyse til grunn? Samsvarer dette med observert belastning?]*

#### 7.5.2 Sammenligning med empirisk belastning

> *[Tabell: ROS-forutsetning vs. observert fra LEO/BRIS.]*

#### 7.5.3 Vurdering av forutsetninger og metodisk grunnlag

> *[Er systemforutsetninger (f.eks. overløpssystem til Agder) reelt operasjonalisert? Formulér som metodisk vurdering — ikke personkritikk.]*

### 7.6 RQ5 — Benchmarking og generaliseringsanalyse

> *[SKRIVES ETTER BENCHMARKING]*

#### 7.6.1 Benchmarking — modellanbefaling vs. faktisk bemanning

> *[Tabell: alle 12 norske 110-sentraler. Kolonner: sentral, innbyggertall, hendelsesvolum (DSB), faktisk bemanning (DSB), modellestimert c* (der data tillater). Identifiser systematisk over-/underdimensjonering.]*

#### 7.6.2 Generaliseringsanalyse

> *[Kan hendelsesvolum, innbyggertall og areal predikere bemanningsbehov? Regresjonsresultater.]*

---

## 8. Diskusjon

> *[3–4 sider. Diskutér hva resultatene betyr. Koble til problemstillingen og forskningslitteraturen. Metodediskusjon. Generaliserbarhet. Begrensninger.]*

### 8.1 Diskusjon av hovedfunn

> *[RQ1–RQ5 diskuteres her. Var resultatene som forventet? Uventede funn? Samsvar med litteraturen?]*

**RQ1 — Belastningsmønstre:**
> *[Diskusjonstekst]*

**RQ2 — Håndteringstid og aktivt hendelsebilde:**
> *[Diskutér i hvilken grad aktivt hendelsebilde utfordrer M/M/c-forutsetningene.]*

**RQ3 — Erlang-C-dimensjonering:**
> *[Er 110 Sør-Vest dimensjonert tilstrekkelig? Diskutér kapasitetsgap opp mot beredskapsperspektivet — lav utnyttelse er ikke nødvendigvis sløsing.]*

**RQ4 — ROS-gjennomgang:**
> *[Metodisk vurdering av eksisterende dimensjoneringsgrunnlag. Bidrar den kvantitative analysen med noe ROS-analysen mangler?]*

**RQ5 — Generaliserbarhet:**
> *[Kan modellen anbefales som nasjonal dimensjoneringsstandard? Hvilke forutsetninger må oppfylles?]*

> *[NOTE TIL FORFATTER — fange opp ved skriving: Diskutér asymmetrien mellom å produsere et kvantitativt grunnlag og å få det implementert. Analogien til dimensjoneringsforskriften er sentral her: for brannvesen sier forskriften at dersom innbyggertallet er under en terskel, skal det være deltid med vakt. Selv om en beredskapsanalyse peker på behov for kasernert styrke, er dette svært vanskelig å få gjennomslag for hos kommunene — kostnadene er store og forskriften gir rom for å si nei. Tilsvarende dynamikk gjelder for 110: en Erlang-C-modell som viser at c* > c_faktisk (dvs. underbemanning) er et faglig solid funn, men kommunene som finansierer sentralene kan avvise det med henvisning til egen ROS-analyse eller budsjettrammer. En nasjonal standard som likestiller den kvantitative dimensjoneringsmodellen med dimensjoneringsforskriftens rolle for brannvesen, ville endre denne maktsituasjonen — men å anbefale en slik standard overfor DSB er en politisk, ikke bare faglig, handling. Diskutér om prosjektets funn bidrar til å bygge en slik evidensbase, og hva som eventuelt gjenstår for at den skal kunne brukes normativt.]*

### 8.2 Metodediskusjon

#### 8.2.1 Erlang-C — forutsetninger og brudd

> *[Kritisk gjennomgang: Poisson-ankomster (ring-flom), eksponentielle servicetider (heterogen T1–T4), stasjonær rate (daglig/ukentlig variasjon), uavhengige ankomster. Hva betyr bruddene for resultatenes pålitelighet?]*

#### 8.2.2 Datakvalitet og målefeil

> *[LEO/BRIS-registeringspraksis — er håndteringstid nøyaktig registrert? Konfunderende faktorer.]*

#### 8.2.3 Generaliserbarhet

> *[Kan funn fra 110 Sør-Vest generaliseres til andre sentraler? Hvilke sentraler er sammenlignbare?]*

### 8.3 Beredskapsperspektiv

> *[Beredskapssystemer skiller seg fra effektivitetssystemer. Lav kapasitetsutnyttelse som nødvendig buffer. Implikasjoner for tolkning av c*-anbefalinger.]*

### 8.4 Implikasjoner for praksis

> *[Hva bør 110 Sør-Vest, DSB og norske 110-sentraler gjøre basert på disse funnene? Er empirisk kvantitativ dimensjonering bedre enn ROS-basert praksis?]*

> *[NOTE TIL FORFATTER — fange opp ved skriving: Diskutér gapet mellom å produsere kvantitativ kunnskap og å omsette den til endring. Pek på følgende spenning: En modell som viser underbemanning (c* > c_faktisk) stiller krav om økte kostnader overfor kommunene — det er en hard selgeroppgave. Modellen er ikke nøytral: den kan brukes til å argumentere for mer bemanning, men den kan like gjerne brukes av kommuner til å begrunne kutt dersom modellen viser c* < c_faktisk. Strukturen minner om utfordringen brannvesenet møter med dimensjoneringsforskriften: forskriften setter en terskel (innbyggertall → bemanningstype), og selv om en faglig analyse viser at kasernert styrke er nødvendig, er det ekstremt vanskelig å gjennomføre fordi deltid med vakt er forskriftens standard og kostnadene ved avvik er enorme. For 110-sentraler mangler en tilsvarende regulatorisk standard helt — noe som paradoksalt gir kommunene mer handlingsrom til å ignorere faglige anbefalinger. Drøft hvilken posisjon DSB bør ha i dette: bør en kvantitativ dimensjoneringsmodell som denne forankres som nasjonalt normativt instrument på linje med dimensjoneringsforskriften? Hva er forutsetningene? Hva er risikoen?]*

---

## 9. Konklusjon

> *[1–2 sider. Oppsummer svar på problemstillingen. Gjenta ikke resultater i detalj — pek på de viktigste funnene og implikasjonene. Avslutt med videre forskning.]*

### 9.1 Hovedkonklusjon

> *[Svar direkte på problemstillingen: «I hvilken grad samsvarer faktisk bemanning ved norske 110-sentraler med kapasitetsbehovet beregnet fra historiske hendelsesdata og køteoretiske modeller?»]*

### 9.2 Oppsummering av forskningsspørsmål

| Forskningsspørsmål | Hovedfunn |
|---|---|
| RQ1 — Belastningsmønstre | [OPPSUMMERING] |
| RQ2 — Håndteringstid | [OPPSUMMERING] |
| RQ3 — Erlang-C-dimensjonering | [OPPSUMMERING] |
| RQ4 — ROS-gjennomgang | [OPPSUMMERING] |
| RQ5 — Generaliserbarhet | [OPPSUMMERING] |

### 9.3 Videre forskning

> *[Hva gjenstår? Hva bør neste studie gjøre? Mulige utvidelser av modellen (M/M/c/K, M/G/c, simulering).]*

---

## 10. Referanser

> *[APA 7th norsk. Sortert alfabetisk. Primærkilder prioritert.]*

> *[Eksempel på forventet referanseliste — suppleres med faktisk litteratur etter søk:]*

Brann- og redningsvesenforskriften. (2002). *Forskrift om organisering og dimensjonering av brannvesen* (FOR-2002-06-26-729). Justis- og beredskapsdepartementet. https://lovdata.no/dokument/SF/forskrift/2002-06-26-729

Dimensjoneringsforskriften. (2023). *Forskrift om dimensjonering, utrusting og bemanning av brannvesen* (FOR-2023-01-06-23). Justis- og beredskapsdepartementet.

DSB. (2025). *Årsrapport 110-sentralene 2025*. Direktoratet for samfunnssikkerhet og beredskap.

Erlang, A. K. (1917). Solution of some problems in the theory of probabilities of significance in automatic telephone exchanges. *The Post Office Electrical Engineers' Journal*, *10*(189–197).

Gans, N., Koole, G., & Mandelbaum, A. (2003). Telephone call centers: Tutorial, review, and research prospects. *Manufacturing & Service Operations Management*, *5*(2), 79–141.

Gross, D., Shortle, J. F., Thompson, J. M., & Harris, C. M. (2008). *Fundamentals of queueing theory* (4. utg.). Wiley.

Jagerman, D. L. (1974). Some properties of the Erlang loss function. *The Bell System Technical Journal*, *53*(3), 525–551.

[TILLEGG ETTER LITTERATURSØK]

---

## 11. Vedlegg

### Vedlegg A — Python-implementasjon av Erlang-C

> *[Link til GitHub-repo eller innsatt kode. Beskriv notebook-struktur.]*

### Vedlegg B — Intervjuguide

> *[Strukturert intervjuguide benyttet ved datainnsamling.]*

### Vedlegg C — Dataoversikt og rådatabeskrivelse

> *[Variabelliste, periode, datakvalitetslogg.]*

### Vedlegg D — Dokumentasjon av KI-bruk

Fullstendig brukslogg, rapporttekst og administrativ erklæring finnes i det løpende dokumentet:

**`KI_erklæring_LOG650_G20_Rune.md`** (prosjektrot)

Dokumentet inneholder:
- Del 1: «Bruk av kunstig intelligens» — rapporttekst (kopieres til rapport ved levering)
- Del 2: Løpende brukslogg med dato, verktøy, formål og hva som ble tatt inn
- Del 3: Administrativ erklæring (signeres ved innlevering)
- Del 4: Personvern og konfidensialitet

Det offisielle HiMolde-skjemaet «Erklæring om bruk av kunstig intelligens» (Word) leveres som separat administrativt vedlegg ved innlevering av sluttrapport.

### Vedlegg E — Sensitivitetsanalyse (utvidet)

> *[Tabeller og figurer som ikke fikk plass i hoveddelen.]*

---

*Versjon 0.2 — Skall (revidert) | Sist oppdatert: 2026-03-09*
*Neste steg: Fase 3 — start med L7 (rapportskjelett + intro v1) og L8 (EDA)*
