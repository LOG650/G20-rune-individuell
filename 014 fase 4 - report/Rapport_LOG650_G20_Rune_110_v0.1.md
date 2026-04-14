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

Denne rapporten analyserer i hvilken grad faktisk bemanning ved norske 110-sentraler samsvarer med kapasitetsbehovet beregnet fra historiske hendelsesdata og kapasitetsmodeller. En innledende Erlang-C-analyse (M/M/c) viste svært lav systemutnyttelse (ρ < 6 %) for alle skifttyper — et resultat som er formelt korrekt, men metodisk utilstrekkelig fordi modellen ikke fanger at sentralens operative prosedyre (makkerpar-drift) krever to operatører per hendelse. Primærmodellen er derfor en **prosedyrbasert ankomstkonfliktmodell** som måler sannsynligheten for at et beredskapsanrop ankommer i en tilstand der makkerpar-driftsstandarden ikke kan opprettholdes. Modellen er kalibrert mot LEO/BRIS-data fra 110 Sør-Vest (2025, 7 438 beredskapsanrop). Resultater benchmarkes mot alle norske 110-sentraler via DSBs årsrapporter.

**Nøkkelord:** 110-sentral, bemanningsdimensjonering, prosedyrbasert kapasitetsmodell, ankomstkonflikt, makkerpar, Erlang-C, køteori, kapasitetsanalyse, LEO, beredskap

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
- **RQ3:** I hvilken andel av beredskapsanropene ankommer anropet i en tilstand der sentralens operative driftsstandard (makkerpar) ikke kan opprettholdes — og hva er det strukturelle kapasitetsgapet mellom hverdag og helg?
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

> *[For 110 Sør-Vest: T_max = 30 sek (automatisk overføring til Agder ved ubesvart anrop — bekreftet beredskapsanalyse J03 s. 25), SL_target = [AVKLARES] — mulig 95% eller høyere.]*

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

**Note — servicetesting og sentral-spesifikk organisering:**

Innledende kontakt med Midt-Norge 110 (15. mars 2026) avdekker at sentrale har tre dedikerte servicemedarbeidere som håndterer ABA-servicetesting. Disse registreres ikke i LEO og fremkommer dermed ikke i BRIS-eksporten. I normalperioder (hverdager) belaster dermed T2-servicetesting ikke 110-operatørenes kapasitet ved denne sentralen. I helger, ved sykdom og overbelastning overtas funksjonen av ordinære 110-operatører.

Dette innebærer at «Service»-kategorien i BRIS-data ikke er direkte sammenlignbar på tvers av sentraler uten kjennskap til lokal organisering. Organiseringen ved 110 Sør-Vest, og øvrige sentraler, verifiseres gjennom planlagte intervjuer (avsnitt 5.2.3). Se møtenotat: `002 meetings/04 20260315 Midt-Norge 110 - telefonsamtale.md`

#### 4.2.3 Operative særtrekk og kapasitetsgrenser

| Særtrekk | Beskrivelse | Implikasjon for analyse |
|---|---|---|
| Overløp til Agder | 10. kø-anrop viderekoblet automatisk | De facto servicegrense — proxy for definert servicegrad |
| 30-sekunders-terskel | Ubesvarte anrop etter 30 sek → automatisk overføring til Agder (bekreftet beredskapsanalyse J03 s. 25). Ingen nasjonal svartidsfrist i forskriften. Merk: § 21 krever utalarmering innen 90 sek (dispatchkrav, ikke svartidskrav). | Operativ grense — brukes som terskel i Erlang-C sensitivitetsanalyse |
| Aktivt hendelsebilde | Pågående hendelser binder operatørkapasitet utover samtaletid | Økt effektiv håndteringstid; Erlang-C-forutsetning utfordres |
| Ring-flom (call surge) | Én hendelse utløser mange samtidige anrop | Brudd på Poisson-uavhengighet |

### 4.3 ROS- og beredskapsanalysegrunnlag

> *[Kort intro — detaljer i avsnitt 7.3 (RQ4). Referer til at 110 Sør-Vest har en beredskapsanalyse som formelt begrunner bemanningsnivået.]*

---

## 5. Metode og data

> **Kapittelet er ferdigskrevet i `kap5_metode_data.md`** — se den filen for fullstendig innhold.

---

## 6. Modell

> **Kapittelet er ferdigskrevet i `kap6_modell.md`** — se den filen for fullstendig innhold.
> Kortversjon av modellstrukturen er gjengitt nedenfor for oversiktens skyld.

### Modellutvikling — tre faser

Prosjektet gjennomgikk en metodisk utvikling fra Erlang-C til prosedyrbasert modell:

| Fase | Modell | Konklusjon |
|---|---|---|
| 1 | Erlang-C (M/M/c) | ρ < 6 % — formelt korrekt, metodisk utilstrekkelig |
| 2 | Simultanitetsanalyse | Lav konfliktrate — makkerpar-logikk ikke fanget |
| **3** | **Prosedyrbasert ankomstkonfliktmodell** | **Primærmodell — strukturelt helg/hverdag-gap** |

### Primærmodell: Prosedyrbasert ankomstkonfliktmodell

For hvert beredskapsanrop i klassifiseres kapasitetsnivå basert på antall aktive hendelser n_aktive ved ankomsttidspunktet t_i:

| Nivå | c_eff = 2 | c_eff = 3 |
|---|---|---|
| **Normal** — makkerpar mulig | n_aktive = 0 | n_aktive = 0 |
| **Brudd** — ingen ledig makker | n_aktive ≥ 1 | n_aktive ≥ 1 |
| **Svikt** — VL/Agder må overta | n_aktive ≥ 2 | n_aktive ≥ 3 |

En hendelse er «aktiv» fra ankomsttidspunktet til estimert bindingstid er utløpt (RØD-fase + GUL-fase). Bindingstider er estimert via ekspertintervju og sensitivitetstestet (se `kap6_modell.md` avsnitt 6.3.4).

### Erlang-C beholdes som grunnlinje

Erlang-C (M/M/c) presenteres som Fase 1 / sammenligningsgrunnlag i avsnitt 7.1. Den viser hvorfor klassisk køteori er utilstrekkelig for 110-konteksten, og danner det metodiske argumentet for primærmodellen.

> *Se `kap6_modell.md` for: fullstendig matematisk formulering, bindingstidstabell, pseudokode og implementasjonsdetaljer.*

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

### 7.3 RQ3 — Prosedyrbasert kapasitetsanalyse

> *Ferdigskrevet i `kap7_analyse_resultater.md` avsnitt 7.4–7.6. Nøkkelresultater:*

**Tabell: Kapasitetsnivå ved ankomst — basis (ABA=10 min, Tyngre=15 min)**

| Skifttype | Anrop | Normal | Brudd på AML | Svikt | c_eff |
|---|---|---|---|---|---|
| Dag / Hverdag | 3 382 | 79,4 % | 20,2 % | 0,4 % | 3 |
| Dag / Helg | 1 236 | 78,5 % | 17,1 % | **4,5 %** | 2 |
| Natt / Hverdag | 1 934 | 86,5 % | 12,6 % | 1,0 % | 2 |
| Natt / Helg | 886 | 80,8 % | 14,6 % | **4,6 %** | 2 |

**Strukturelt funn:** Helg dagskift har 12,7× høyere sviktrate enn hverdag dagskift (4,5 % mot 0,4 %), til tross for tilnærmet likt beredskapsvolum. Funnet er robust på tvers av alle tre bindingstidsscenarier.

> *Erlang-C-grunnlinjen (Fase 1) finnes i `kap7_analyse_resultater.md` Tabell 7.1.*

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

> **Se [kap8_diskusjon.md](kap8_diskusjon.md) — v1.0**
>
> Strukturert rundt fire tema:
> - 8.1 Hvorfor Erlang-C er utilstrekkelig — det lav-belastede paradokset, makkerpar som flereenhets-betjening, bindingstid som kapasitetsbegrep
> - 8.2 Modellprediksjoner versus opplevd virkelighet — gapet mellom modell og erfaring, kvalitetsreduksjon som usynlig buffer
> - 8.3 Implikasjoner for dimensjonering — svar på problemstillingen, dag/natt-asymmetri, bakgrunnsbelastning, kvantitativ standard, overløpsarkitektur
> - 8.4 Begrensninger — data, modell, antakelser
> - 8.5 Videre forskning — tverrsentralvalidering, tidsvariabel analyse, DES

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
| RQ3 — Prosedyrbasert kapasitetsanalyse | Helg dagskift: sviktrate 4,5 % (12,7× hverdag). Funnet robust på tvers av alle bindingstidsscenarier. |
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

### Vedlegg A — Python-implementasjon

> *[Link til GitHub-repo. To hoveddeler: (1) Erlang-C grunnlinje (scipy), (2) prosedyrbasert ankomstkonfliktmodell med heap-algoritme (`analyse/scripts/kapasitet_figurer.py`). Beskriv notebook-struktur.]*

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
