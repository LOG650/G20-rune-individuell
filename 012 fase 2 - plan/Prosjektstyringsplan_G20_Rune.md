# Prosjektstyringsplan
**LOG650 – Forskningsprosjekt: Logistikk og kunstig intelligens**

| | |
|---|---|
| **Prosjekt** | Dimensjonering av røykdykkerbekledning under usikker etterspørsel |
| **Gruppe** | G20 – Rune Individuell |
| **Utarbeidet av** | Rune Grødem |
| **Autorisert av** | Emneansvarlig, LOG650 |
| **Dato** | 2026-02-25 |
| **Versjon** | 0.7 – utkast |

---

## Innhold

1. [Sammendrag](#1-sammendrag)
2. [Forretningscase](#2-forretningscase)
3. [Omfang](#3-omfang)
4. [Fremdrift](#4-fremdrift)
5. [Risiko](#5-risiko)
6. [Interessenter](#6-interessenter)
7. [Ressurser og roller](#7-ressurser-og-roller)
8. [Kommunikasjon og kvalitet](#8-kommunikasjon-og-kvalitet)

---

## 1. Sammendrag

Dette dokumentet utgjør prosjektstyringsplanen for prosjektet **«Dimensjonering av røykdykkerbekledning under usikker etterspørsel»**. Prosjektet gjennomføres i LOG650 som et prosjektorganisert forskningsarbeid, der hovedleveransen er en vitenskapelig rapport med tilhørende kvantitativ modell implementert i Python.

### 1.1 Bakgrunn og behov

Rogaland Brann og Redning IKS (RogBR) må sikre høy tilgjengelighet på kritisk røykdykkerbekledning. Dagens praksis er i stor grad basert på tommelfingerregler og lokal erfaring, og kan gi enten overbeholdning (unødvendig kapitalbinding) eller underbeholdning (operativ risiko). Prosjektet skal etablere et kvantitativt beslutningsgrunnlag ved å modellere samspillet mellom:

- Usikker, hendelsesdrevet etterspørsel
- Vaskekapasitet som mulig flaskehals
- Valgt lagerpolicy (personlig utstyr vs. pool vs. hybrid)

### 1.2 Problemstilling

Hvordan kan lagerstyring av røykdykkerbekledning ved Rogaland Brann og Redning IKS analyseres og dimensjoneres under usikker, hendelsesdrevet etterspørsel for å oppnå definert servicegrad til lavest mulig kapitalbinding?

Organisasjonen har flere kasernerte stasjoner (Stangeland, Schankeholen, Varmen, Kvernavik) med egne klespooler, samt deltidsstasjoner som i varierende grad benytter disse poolene. Dette skaper konkurrerende etterspørsel som øker kompleksiteten i dimensjoneringen.

Systemet er et **lukket system med fast populasjon** (recoverable items): draktene sirkulerer mellom tilstandene *tilgjengelig på stasjon*, *til vask / i ledetid* og *avskrevet/ødelagt*. Bestilling skjer kun ved avskrivning eller nye brukere — ikke ved ordinært forbruk. Dette gjør problemet strukturelt beslektet med militære reservedelsmodeller (Sherbrooke, 1968) snarere enn klassisk lagerstyring. Prosjektet plasseres innenfor området **lagerstyring under usikker etterspørsel (stokastisk inventory management)**, i tråd med kompendiets struktur: område → problemstilling → modell → metode.

### 1.3 Mål

Prosjektmålet er å analysere og dokumentere optimal dimensjonering av røykdykkerbekledning for RogBR gjennom en kvantitativ modell, slik at ønsket servicegrad kan oppnås til lavere eller lik totalkostnad enn dagens praksis — eller alternativt dokumentere tydelig trade-off mellom kostnad og tilgjengelighet.

Prosjektet vil analysere **optimal beholdning per stasjon/pool, sikkerhetslager og eventuelle allokeringsprinsipper mellom stasjoner**. Det skal avklares hvilken type servicegrad — *cycle service level* eller *fill rate* — som er mest hensiktsmessig i denne operative konteksten. Endelig servicegradnivå (minimum 99,x %) fastsettes i samarbeid med RogBR.

### 1.4 Arbeidsflyt

Prosjektet følger emnets faste struktur:

```
Problemstilling → Modell → Metode → Implementasjon → Analyse
```

Litteratursøk og rapportskriving startes tidlig og videreføres iterativt gjennom semesteret.

### 1.5 Godkjenningskrav

| Leveransetype | Krav for godkjent | Konsekvens ved ikke godkjent |
|---|---|---|
| Arbeidskrav (milepæler underveis) | C-nivå eller bedre | Iterere og relevere |
| Sluttrapport + muntlig eksamen | **B-krav** | Ikke bestått emne |

> **Kilde:** Forelesning 11. februar 2026: *«vi har et C-krav på innlevert, altså det du leverer inn i løpet av milepælene, men vi har et B-krav når det gjelder rapport og muntlig»*.

---

## 2. Forretningscase

### 2.1 Bakgrunn

Rogaland Brann og Redning IKS (RogBR) disponerer per i dag om lag 428 sett røykdykkerbekledning, med en anslått enhetskostnad på ca. 18 000 kroner per sett. Dette tilsvarer en samlet kapitalbinding på om lag **7,7 millioner kroner**. Dimensjoneringen av beholdningen er i stor grad basert på historisk praksis, lokale vurderinger og erfaringsbaserte tommelfingerregler.

Bekledningen er kritisk for operativ beredskap. For lav beholdning kan medføre redusert tilgjengelighet ved samtidige hendelser eller ved kapasitetsbegrensninger i vask. For høy beholdning medfører unødvendig kapitalbinding og økte lagerkostnader. Det foreligger derfor et tydelig behov for et mer strukturert, kvantitativt beslutningsgrunnlag.

### 2.2 Vurderte alternativer

| Alternativ | Beskrivelse | Vurdering |
|---|---|---|
| **A0 – Status quo** | Videreføring av dagens praksis uten systematisk modellering eller analyse | Forkastet — ingen dokumentert beslutningsstøtte |
| **A1 – Erfaringsbasert justering** | Manuell justering av beholdning basert på subjektiv vurdering og tidligere mangeltilfeller | Forkastet — ikke etterprøvbart, skalerer ikke |
| **A2 – Kvantitativ dimensjonering** | Utvikling av en kvantitativ modell som analyserer samspillet mellom usikker etterspørsel, vaskekapasitet og valgt servicegrad | **Valgt** |

Prosjektet gjennomfører og dokumenterer alternativ **A2**.

### 2.3 Forutsetninger

- BRIS-data og beholdningsdata fra RogBR er tilgjengelige i tilstrekkelig kvalitet
- Vaskekapasitet og gjennomsnittlig ledetid kan estimeres
- Servicegrad kan defineres i samarbeid med RogBR (minimum 99,x %)
- Ekstreme, katastrofepregede hendelser holdes utenfor modellens gyldighetsområde
- Prosjektet har som mål å gi beslutningsstøtte, ikke å implementere organisatoriske endringer direkte

### 2.4 Forventede gevinster

**Operative gevinster**
- Dokumentert sannsynlighet for å oppnå valgt servicegrad
- Redusert risiko for mangel på kritisk bekledning ved parallelle hendelser
- Bedre forståelse av vask som mulig flaskehals i systemet

**Økonomiske gevinster**
- Mulighet for reduksjon i kapitalbinding dersom dagens beholdning er overdimensjonert
- Alternativt: Dokumentert begrunnelse for at dagens nivå er nødvendig gitt ønsket servicegrad
- Synliggjøring av kost–service trade-off som beslutningsgrunnlag

**Strategiske gevinster**
- Overgang fra erfaringsbasert til analytisk beslutningsstøtte
- Metodisk rammeverk som kan overføres til annet kritisk verneutstyr
- Økt modenhet innen datadrevet logistikkstyring i organisasjonen

### 2.5 Kostnader

For RogBR påløper ingen direkte prosjektkostnader utover begrenset tidsbruk til datatilgang og intervju. Prosjektet gjennomføres som en del av LOG650 ved Høgskolen i Molde. Eventuelle fremtidige kostnader knyttet til implementering av anbefalt løsning vurderes separat av RogBR og inngår ikke i dette prosjektet.

### 2.6 Analyse og konklusjon

Gitt størrelsen på dagens kapitalbinding (ca. 7,7 mill. kr) og den operative kritikaliteten til røykdykkerbekledning, vurderes potensialet for gevinst som betydelig. Selv små prosentvise justeringer i beholdning kan gi merkbare økonomiske effekter, samtidig som en eksplisitt dokumentert servicegrad gir økt operativ trygghet.

Alternativ A2 – kvantitativ dimensjonering – gir et strukturert beslutningsgrunnlag som enten kan:
1. Dokumentere at dagens nivå er korrekt gitt ønsket servicegrad, eller
2. Identifisere en mer kostnadseffektiv dimensjonering uten å redusere operativ tilgjengelighet

På denne bakgrunn vurderes prosjektet som faglig og praktisk relevant for RogBR, og som et egnet forskningsprosjekt innen kvantitativ lagerstyring under usikkerhet.

---

## 3. Omfang

### 3.1 Krav

Prosjektet skal:

1. Dokumentere dagens prosessflyt og lagerpolicy (personlig/pool/hybrid) for røykdykkerbekledning i RogBR, inkludert relevante prioriteringsregler ved konkurrerende behov.
2. Etablere og beskrive datagrunnlaget (kilder, periode, variabler, datakvalitet, behandling av rådata), der bedriftsdata prioriteres.
3. Avklare og begrunne modellvalg fra pensum/kompendiet — METRIC (Sherbrooke 1968; Axsäter kap. 10.2) er identifisert som primærmodell — og beskrive modellens parametere, beslutningsvariabler, målsetting og begrensninger.
4. Implementere modellen i kode (Python) og utføre analyse med dokumentert validering og robusthetssjekk.
5. Skrive rapport fortløpende med tydelig skille mellom modell/metode og resultater/diskusjon, med korrekt og konsistent kildebruk (APA 7th norsk).

### 3.2 Avgrensninger

- Kun røykdykkerbekledning analyseres (ikke annet verneutstyr som hjelmer, hansker, støvler)
- Kun strategisk/taktisk planlegging — ikke operativ sanntidsstyring
- Avhengig av funn kan modellen forenkles til å analysere hovedpools (Stangeland, Schankeholen) med aggregert etterspørsel, fremfor full modellering av alle 15+ stasjoner
- Allokerings-policy mellom stasjoner forenkles til first-come-first-served hvis komplekse prioriteringsregler viser seg vanskelig å modellere
- Ekstreme situasjoner (flere samtidige storbranner, katastrofer) modelleres ikke
- RFID-analyse begrenses til scenariosammenligning uten egen datainnsamling
- Kostnader ved mangel kvantifiseres ikke direkte — håndteres gjennom service-level constraint

### 3.3 Bruk av kunstig intelligens (KI)

Prosjektet gjennomføres i LOG650 — Logistikk og kunstig intelligens. KI benyttes som analytisk verktøy, ikke som overfladisk pynt. Planlagt bruk:

- **Estimering av etterspørselsfordelinger** basert på BRIS-data (hendelsesfrekvens, sesongvariasjoner)
- **Simulering av lagerpolicyer** (Monte Carlo / diskret hendelses-simulering) for å beregne servicegrad og mangeltilfeller
- **Sensitivitetsanalyse** for å teste robusthet ved endringer i parametere (vaskekapasitet, etterspørselsvariasjon)
- **Strukturering av modellkode og validering** — Python-implementasjon med dokumenterte transformasjoner

### 3.4 Løsning og leveranser

Løsningen består av:

- **Casebeskrivelse** av RogBR (kontekst, prosessflyt, nøkkeltall og utfordring)
- **Datamodell og datagrunnlag** (BRIS-data 2021–2025, telleliste/beholdning, vaskekapasitet/ledetider og intervjudata for nettverk/pool-struktur)
- **Primær modell — METRIC** (Multi-Echelon Technique for Recoverable Item Control, Sherbrooke 1968; Axsäter kap. 10.2):
  - Sentrallager (Stangeland/vaskeri) løses eksakt med Poisson-kø; forsinkelse W₀ beregnes med Littles lov (M/D/∞)
  - Hver stasjon løses separat med effektiv ledetid L̃ᵢ = Lᵢ + W₀ og Poisson-etterspørsel λᵢ
  - Beslutningsvariabel: Sᵢ (order-up-to nivå per stasjon) som gir ønsket servicegrad
  - Validering gjennom Monte Carlo simulering for å kvantifisere approksimasjonsfeil
- **Implementasjon og analyse i Python**, inkludert validering, sensitivitetsanalyse og dokumentasjon av usikkerhet
- **Rapport** (hovedleveranse) med kode tilgjengelig på GitHub som vedlegg

### 3.5 Case-kartleggingsplan (L4)

Selve intervjuene gjennomføres i fase 3 (uke 11–12). Planlagte informanter:

| Informant | Rolle | Bidrag til prosjektet | Prioritet |
|---|---|---|---|
| Tom Meyer | Logistikkansvarlig, RogBR | Vaskekapasitet, beholdning per stasjon, kostnader, utskiftningsrate, ledetider | 1 — kritisk |
| Petter (etternavn ukjent) | Operativt ansvarlig klær/vask | Daglig styring av bekledning og vaskelinjer i praksis — identifisert av Tom Meyer 24.02 | 2 — kritisk |
| Bent (etternavn ukjent) | Operativt ansvarlig klær/vask | Daglig styring av bekledning og vaskelinjer i praksis — identifisert av Tom Meyer 24.02 | 2 — kritisk |
| Innsatsleder S01 | Kasernert stasjon (Stangeland/Schankeholen) | Pool-struktur, prioriteringsregler ved konkurrerende behov, mangeltilfeller observert operativt | 3 — viktig |
| Innkjøpsansvarlig | RogBR | Innkjøpspris, leveringstid fra leverandør, innkjøpsprosess ved avskrivning | 3 — viktig |
| 2–3 brannmenn (kasernert) | Operativt nivå | Validering: stemmer formell policy med faktisk praksis? Gap mellom teori og operativ hverdag | 4 — nyttig |

**Intervjuguide for Tom Meyer:** ferdigstilt, se `012 fase 2 - plan/Intervju_Tom_Meyer_Logistikk.tex`

**BRIS-datatilgang:** bekreftet — rådata tilgjengelig i `004 data/` (8 098 hendelser, 2021–2025)

**Øvrige informanter:** kortere semi-strukturert samtale (~15 min), fokus på å verifisere eller korrigere antakelser fra Tom Meyer-intervjuet og Thomas-rapporten.

---

### 3.6 Arbeidsnedbrytningsstruktur (WBS)

**Fase 1 — Initiering (fullført)**

| ID | Leveranse | Frist | Status |
|---|---|---|---|
| L0 | Godkjent proposal | 23. feb 2026 | ✅ Fullført |

**Fase 2 — Planlegging (frist 9. mars 2026)**

*Fase 2 er planlegging, ikke gjennomføring. Litteratursøk og case-kartlegging identifiseres og struktureres her — selve arbeidet gjennomføres i fase 3.*

| ID | Leveranse | Frist | Status |
|---|---|---|---|
| L1 | Avklart problemstilling + mål + avgrensninger (oppdatert fra proposal) | 28. feb | ✅ Fullført |
| L2 | Modellkandidat-liste fra pensum + beslutning om modelltilnærming → METRIC identifisert (Axsäter kap. 10.2, Sherbrooke 1968) | 28. feb | ✅ Fullført |
| L3 | Litteratursøk — **planlegging** (søkeord, databaser, avgrensning) | 5. mars | ✅ Fullført |
| L4 | Case-kartlegging — **planlegging** (kontaktpersoner, intervjuguide, tilgang BRIS) | 5. mars | ✅ Fullført |
| L5 | Dataplan — datakilder, variabler, kvalitet, rådatahåndtering | 5. mars | ⬜ |
| L6 | Godkjent prosjektplan (dette dokumentet) | **9. mars** | 🔄 Pågår |
| L7 | MS Project Gantt-diagram med referanseplan (baseline) | **9. mars** | ⬜ |

**Fase 3 — Gjennomføring (9. mars – slutten av april 2026)**

*Fase 3 er der planene fra fase 2 realiseres: intervjuer gjennomføres, litteratur søkes systematisk, modell implementeres og rapport skrives.*

| ID | Leveranse | Frist | Status |
|---|---|---|---|
| L8 | Introduksjon og problemstilling — rapportutkast v1 | Uke 12 | ⬜ |
| L9 | Datainnsamling + case-kartlegging — intervjuer (S01, logistikk), BRIS-eksport, prosessdokumentasjon | Uke 12 | ⬜ |
| L10 | Analyse av etterspørsel — distribusjon, sesongmønster, stasjonsnettverk | Uke 13 | ⬜ |
| L11 | Valg av modelltilnærming — METRIC valgt, formell begrunnelse og detaljering i rapport | Uke 13 | 🔄 Pågår |
| L12 | Litteratursøk gjennomføring + teorikapittel — stokastisk lagerstyring, evt. køteori | Uke 14 | ⬜ |
| L13 | Implementering i Python (KI-støttet) — modell og simulering | Uke 15 | ⬜ |
| L14 | Validering og sensitivitetsanalyse | Uke 16 | ⬜ |
| L15 | Resultater og diskusjon — rapportutkast | Uke 16 | ⬜ |
| L16 | Godkjent hovedutkast + peer review (skriftlig tilbakemelding til annen gruppe) | Slutten av april | ⬜ |

**Fase 4 — Avslutning**

| ID | Leveranse | Frist | Status |
|---|---|---|---|
| L17 | Ferdigstilt rapport (inkl. kode på GitHub) | 31. mai 2026 | ⬜ |
| L18 | Muntlig eksamen | Tidlig juni 2026 | ⬜ |

---

## 4. Fremdrift

### 4.1 Milepæler

| ID | Milepæl | Frist | Godkjenningskrav | Status |
|---|---|---|---|---|
| M1 | Godkjent proposal | 23. feb 2026 | C-nivå | ✅ Fullført |
| M2 | Rapportskjelett påbegynt + innledning v1 *(litteratursøk planlagt, ikke gjennomført)* | Innen 9. mars | C-nivå | ⬜ |
| M3 | Godkjent prosjektplan + Gantt med referanseplan | **9. mars 2026** | C-nivå | 🔄 Pågår |
| M4 | Godkjent hovedutkast + peer review gjennomført | Slutten av april 2026 | C-nivå | ⬜ |
| M5 | Ferdigstilt rapport innlevert + muntlig eksamen | Rapport: 31. mai / Muntlig: tidlig juni 2026 | **B-krav** | ⬜ |

> **Kilder:** Forelesning 12. jan og 11. feb 2026.

### 4.2 Avhengighetsdiagram

> ⬜ *Fylles inn basert på Gantt-diagrammet i MS Project*

### 4.3 Gantt-plan

Fremdriftsplanen etableres i MS Project og baseres på WBS-leveransene ovenfor. Planen inkluderer milepæler M1–M5 med frister og godkjenningskrav, aktiviteter med uke-presisjon, og kritisk sti som sikrer innlevering innen 31. mai.

**Referanseplan (baseline)** settes umiddelbart etter godkjenning av plan. Gantt oppdateres løpende gjennom fase 3 og re-innleveres ved fase 3-slutt med faktisk fremdrift plottet mot baseline, slik at avvik mellom plan og virkelighet er synlig for sensor.

> ⬜ *Gantt-diagram (.mpp) utarbeides i MS Project — se separat fil*

### 4.4 Kritisk linje

> ⬜ *Fylles inn etter at Gantt er etablert i MS Project*

---

## 5. Risiko

### 5.1 Prosess for risikostyring

Risikoregisteret gjennomgås ukentlig i forbindelse med statusnotatet. Risikoer overvåkes løpende og tiltak iverksettes proaktivt. Rune Grødem er eneste risikoeier og ansvarlig for alle tiltak.

### 5.2 Risikoregister

| ID | Risiko | Sannsynlighet | Konsekvens | Tiltak | Beredskap |
|---|---|---|---|---|---|
| R1 | Utilstrekkelig datakvalitet fra BRIS — manglende felter, korte tidsserier, feil i registrering | Middels | Høy | Etablere kontakt med logistikkansvarlig tidlig; be om råeksport og vurdere kvalitet før modellstart | Bruke Poisson-estimater fra litteratur som supplement; dokumentere begrensninger eksplisitt |
| R2 | Feil antagelser om etterspørselsuavhengighet mellom stasjoner | Middels | Høy | Kartlegge pool-struktur gjennom intervjuer med S01 | Forenkle til aggregert etterspørsel per pool; dokumentere forenklingen |
| R3 | Uklarhet i vaskekapasitet og ledetid | Middels | Middels | Innhente kapasitetsdata fra driftsavdelingen; bruke intervjuer som supplement | Bruke konservative estimater og sensitivitetsanalyse |
| R4 | Endringer i organisasjonsstruktur eller stasjonsoppsett under prosjektet | Lav | Middels | Avklare planlagte endringer tidlig; avgrense modellen mot disse | Spesifisere kartleggingstidspunkt som «snapshot» |
| R5 | Tidskollisjon med vaktarbeid på 110 Sør-Vest | Høy | Middels | Planlegge skriveøkter rundt vaktplan; bygge buffer inn i Gantt | Komprimere sensitivitetsanalysen; prioritere kjernemodell |
| R6 | Prokrastinering — skippertak mot innleveringsfrist | Middels | Høy | Ukentlige statusnotater og LLI-logg; tidlige delleveranser med egne frister | Akseptere enklere analyse fremfor å kompromittere rapportkvalitet |
| R7 | METRIC-approksimasjonsfeil — modellen antar uavhengige forsinkelser ved sentrallager, men common cause stockout (alle drakter til vask samtidig) rammer alle stasjoner samtidig | Middels | Middels | Kvantifisere feilen gjennom Monte Carlo simulering; sammenligne analytisk vs. simulert servicegrad | Dokumentere avviket som kjent begrensning i diskusjonskapittelet; vurdere VARI-METRIC som alternativ |

### 5.3 Ressursindikator (LLI)

Som erstatning for budsjett benyttes **Livsglede- og vilje-til-å-leve-indeks (LLI)** som styringsorientert mål på kognitiv belastning. Indeksen starter på 100 og loggføres i ukentlige statusnotater.

| Hendelse | LLI-endring |
|---|---|
| Systematisk litteratursøk uten relevante treff | −5 |
| Datavask/rydding med manglende felter | −8 |
| Omformulering av problemstilling etter veiledning | −10 |
| Modellvalg avklart og dokumentert | +5 |
| Kodepipeline kjører end-to-end med validering | +10 |

---

## 6. Interessenter

| Navn/Rolle | Organisasjon | Behov / Prioritering | Involvering |
|---|---|---|---|
| Rune Grødem | Student, G20 | Bestå emnet med god karakter | Prosjektleder, utfører alt arbeid |
| Emneansvarlig / veileder | Høgskolen i Molde | Vitenskapelig kvalitet, fremdrift | Godkjenning av plan og Gantt; veiledning underveis |
| Logistikkansvarlig, RogBR | Rogaland Brann og Redning IKS | Praktisk anvendbar dimensjoneringsanbefaling | Datakilder, intervju, validering av resultater |
| Innsatsleder S01, RogBR | Rogaland Brann og Redning IKS | Operativ beredskap ivaretas | Intervju om pool-struktur og prioriteringsregler |

---

## 7. Ressurser og roller

### 7.1 Prosjektteam

Prosjektet gjennomføres individuelt. Alle roller innehas av Rune Grødem.

| Rolle | Ansvar |
|---|---|
| Prosjektleder | Fremdrift, planoppfølging, Gantt-oppdatering, veilederkontakt |
| Faglig ansvarlig (modell) | Modellvalg, implementasjon i Python, validering |
| Forfatter | Rapportskriving, kildebruk (APA 7th), litteratursøk |
| Dataansvarlig | Datainnsamling, datavask, dokumentasjon av rådatabehandling |

### 7.2 Ressursbelastning

Tilgjengelig tid er begrenset av vaktarbeid ved 110 Sør-Vest. Planlegging tar hensyn til dette med buffer i Gantt-diagrammet. Minstekrav er én fokusøkt per uke, med økt intensitet i mars–april.

### 7.3 Kritiske ressurser

- **BRIS-data fra RogBR** — nødvendig for modellering; ingen erstatning uten forenklinger
- **Tilgang til MS Project** — bestilt via IT-avdelingen ved Høgskolen i Molde
- **Veileder** — tidlig forankring av modellvalg er kritisk for å unngå omstart i fase 3

---

## 8. Kommunikasjon og kvalitet

### 8.1 Kommunikasjonsplan

| Aktivitet | Frekvens | Format | Mottaker |
|---|---|---|---|
| Ukentlig statusnotat | Ukentlig | Kort skriftlig oppsummering — hva er gjort, neste steg, LLI | Eget arkiv / veileder ved behov |
| Veiledermøte | Ved behov / etter avtale | Teams eller oppmøte | Veileder |
| Oppdatering av Gantt (tracking) | Ukentlig | MS Project — avvik mot referanseplan registreres løpende | Re-innleveres ved fase 3-slutt |

### 8.2 Kvalitetsplan

1. **Tidlig rapportskriving** — introduksjon og problemstilling skrives i fase 2, videreføres iterativt
2. **Faglig forankring** — litteratursøk starter tidlig og kobles direkte til modellvalg
3. **Tydelig rapportstruktur** — skille mellom modell/metode og resultater/diskusjon fra første utkast
4. **Systematisk validering** — rimelighetssjekk og robusthetsanalyse av modellresultater
5. **Datahåndtering** — rådata lagres uendret, all behandling på kopier med dokumenterte transformasjoner
6. **Versjonskontroll** — kode versjonskontrolleres på GitHub og refereres som vedlegg i rapporten
7. **Kildebruk** — alle faglige påstander refereres etter APA 7th norsk

### 8.3 Peer review

Mot slutten av fase 3 gjennomføres gjensidig **skriftlig** fagfellevurdering med en annen gruppe, tilordnet av emneansvarlig. Peer review er obligatorisk del av arbeidskravet for M4. Ved konfidensielle data fra RogBR undertegnes taushetserklæring av begge grupper før utveksling.

---

*Sist oppdatert: 2026-02-25 | Versjon 0.7 | Neste gjennomgang: ved Gantt-godkjenning*
