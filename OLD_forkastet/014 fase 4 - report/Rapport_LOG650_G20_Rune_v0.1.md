# Dimensjonering av røykdykkerbekledning under usikker etterspørsel

**En kvantitativ analyse av lagerstyring ved Rogaland Brann og Redning IKS**

---

| | |
|---|---|
| **Tittel (norsk)** | Dimensjonering av røykdykkerbekledning under usikker etterspørsel |
| **Tittel (engelsk)** | Dimensioning of firefighter protective clothing under uncertain demand |
| **Forfatter** | Rune Grødem |
| **Emne** | LOG650 – Logistikk og kunstig intelligens |
| **Institusjon** | Høgskolen i Molde — Avdeling for logistikk |
| **Innleveringsdato** | 31. mai 2026 |
| **Molde** | 31. mai 2026 |
| **Totalt antall sider inkl. forside** | [PLACEHOLDER] |

---

## Obligatorisk egenerklæring / gruppeerklæring

Den enkelte student er selv ansvarlig for å sette seg inn i hva som er lovlige hjelpemidler, retningslinjer for bruk av disse og regler om kildebruk. Erklæringen skal bevisstgjøre studentene på deres ansvar og hvilke konsekvenser fusk kan medføre. Manglende erklæring fritar ikke studentene fra sitt ansvar.

> **Erklæring:** Jeg erklærer herved at jeg har gjennomgått retningslinjer for kildebruk og bruk av kunstig intelligens i denne rapporten. Rapporten er mitt eget arbeid, og alle kilder er korrekt sitert i henhold til APA 7th (norsk).
>
> *Rune Grødem, Molde, 31. mai 2026*

---

## Personvern

**Personopplysningsloven**

Har oppgaven vært vurdert av NSD? **Nei**

Jeg erklærer at oppgaven ikke er underlagt Personopplysningsloven. Oppgaven benytter anonymiserte hendelsesdata fra BRIS-registeret (Brann- og redningsvesenet Informasjonssystem), uten kobling til enkeltpersoner. Intervjudata fra ansatte i Rogaland Brann og Redning IKS behandles i aggregert, ikke-identifiserbar form og omhandler organisatoriske prosesser, ikke personopplysninger.

**Helseforskningsloven**

Har oppgaven vært til behandling hos REK? **Nei** — prosjektet faller ikke inn under helseforskningsloven.

---

## Publiseringsavtale

| | |
|---|---|
| **Studiepoeng** | 15 |
| **Veileder** | [PLACEHOLDER] |

Fullmakt til elektronisk publisering av oppgaven: **Ja** — med forbehold om at konfidensielle data fra Rogaland Brann og Redning IKS ikke offentliggjøres. Rapporten publiseres uten vedlegg som inneholder rådata.

Er oppgaven båndlagt (konfidensiell)? **Nei** *(rådata er unntatt, men selve rapporten er åpen)*

---

## Sammendrag

> **[PLACEHOLDER — skrives etter at analyse og resultater er fullført i fase 3/4]**
>
> Sammendraget skal inneholde: bakgrunn og problemstilling, metode, hovefunn (kvantitative), konklusjon og praktisk implikasjon. Lengde: 150–250 ord.

---

## Abstract

> **[PLACEHOLDER — engelsk sammendrag, skrives parallelt med norsk sammendrag]**
>
> The abstract should cover: research problem, method (METRIC model), key findings, and practical implications. Length: 150–250 words.

---

## Innhold

1. [Innledning](#1-innledning)
   - 1.1 [Bakgrunn og tema](#11-bakgrunn-og-tema)
   - 1.2 [Aktualisering — regulatorisk kontekst](#12-aktualisering--regulatorisk-kontekst)
   - 1.3 [Tidligere litteratur](#13-tidligere-litteratur)
   - 1.4 [Problemstilling](#14-problemstilling)
   - 1.5 [Avgrensninger](#15-avgrensninger)
   - 1.6 [Antagelser](#16-antagelser)
2. [Litteratur](#2-litteratur)
3. [Teori](#3-teori)
4. [Casebeskrivelse](#4-casebeskrivelse)
5. [Metode og data](#5-metode-og-data)
   - 5.1 [Metode](#51-metode)
   - 5.2 [Data](#52-data)
6. [Modellering](#6-modellering)
7. [Analyse](#7-analyse)
8. [Resultat](#8-resultat)
9. [Diskusjon](#9-diskusjon)
10. [Konklusjon](#10-konklusjon)
11. [Bibliografi](#11-bibliografi)
12. [Vedlegg](#12-vedlegg)

---

## 1. Innledning

### 1.1 Bakgrunn og tema

Personlig verneutstyr (PVU) utgjør en kritisk ressurs i brannvesenets beredskapsevne. For røykdykkere — mannskaper som opererer i giftige eller oksygenfattige miljøer — er bekledningen ikke bare arbeidsantrekk, men livreddende utstyr med strenge funksjonskrav. Rogaland Brann og Redning IKS (RogBR) forvalter per i dag om lag 428 sett røykdykkerbekledning fordelt mellom heltids- og deltidsstyrker, til en samlet bokført verdi av om lag 7,7 millioner kroner (RogBR intern dokumentasjon, 2025). Å dimensjonere denne beholdningen riktig — verken for stort til å binde unødvendig kapital, eller for lite til å svekke innsatsevnen — er en logistikkfaglig utfordring som denne rapporten adresserer.

Temaet er lagerstyring under usikker etterspørsel, anvendt på en sikkerhetskritisk kontekst. Etterspørselen etter rent, funksjonsdyktig bekledning oppstår ikke jevnt over tid, men er hendelsesdrevet: den utløses av brannalarmer og røykdykkerinnsatser som er stokastiske i både frekvens og størrelse. Etter hver innsats må bekledningen gjennom en vaskesyklus — estimert turnaround 24–36 timer fra innsats til tilbake i pool — før den igjen er tilgjengelig (T. Meyer, personlig kommunikasjon, 24. februar 2026). Vaskekapasiteten er begrenset; maskinen tar fire sett per runde, noe som introduserer en potensiell flaskehals mellom etterspørsel og tilgjengelighet. Summen av disse forholdene gjør dimensjoneringen ikke-triviell og rettferdiggjør en analytisk tilnærming basert på lagerteori og køteori.

### 1.2 Aktualisering — regulatorisk kontekst

Frem til 2022 ga norsk særlovgivning relativt detaljerte krav til brannvesenets verneutstyr. Forskrift av 18. januar 2022 nr. 65 (FOR-2022-01-18-65) endret dette ved å fjerne de detaljerte PPE-kravene og i stedet overføre dimensjoneringsansvaret til det alminnelige regelverket i arbeidsmiljøloven (DSB, 2022). Konsekvensen er at den enkelte brannkommune og det interkommunale selskapet nå selv må gjennomføre risiko- og sårbarhetsanalyse (ROS-analyse) og beredskapsanalyse som det lovpålagte grunnlaget for ressursdimensjonering. For RogBR betyr dette at spørsmålet «hvor mange sett bekledning trenger vi?» ikke lenger kan besvares ved å slå opp i en tabell, men krever en systematisk, dokumenterbar metodikk.

Denne rapporten er motivert nettopp av dette regulatoriske skiftet: det er behov for analytiske verktøy som kan understøtte beredskapsanalysen med kvantitativt grunnlag for lagerdimensjonering.

### 1.3 Tidligere litteratur

Lagerstyring av reservedeler og kritisk utstyr med sporadisk, hendelsesdrevet etterspørsel er et veletablert forskningsfelt innen operasjonsanalyse. Det sentrale rammeverket for flerstegs reservedelslagre er METRIC-modellen (*Multi-Echelon Technique for Recoverable Item Control*), opprinnelig utviklet av Sherbrooke (1968) for det amerikanske flyvåpenets logistikksystem. METRIC modellerer etterspørsel som en Poisson-prosess og beregner optimale lagernivåer på tvers av et hierarki av lagerpunkter, slik at en gitt systemtilgjengelighet oppnås til lavest mulig kostnad (Sherbrooke, 1968). Modellen er siden videreutviklet — blant annet til MOD-METRIC (Muckstadt, 1973), VARI-METRIC (Sherbrooke, 1986) og Approximate METRIC — for å håndtere variabel etterspørsel, multiple innsatspunkter og endogen reparasjonskapasitet. Axsäter (2015, kap. 10.2) gir en tilgjengelig fremstilling av METRIC-familien og dens anvendelse på flerstegs lagersystemer med reparerbare enheter. Guide og Srivastava (1997) gir en bred oversikt over feltet for reparerbare lagersystemer, mens Basten og van Houtum (2014) diskuterer systemorienterte servicekrav — en tilnærming som er direkte relevant for beredskapslogistikk der «systemet må fungere» er det operative kravet.

Den strukturelle analogien til RogBRs situasjon er tydelig: bekledning sendes «til reparasjon» (vask), etterspørselen er stokastisk og operasjonsdrevet, og systemet opererer med et implisitt servicegradkrav. Denne analogien er et sentralt metodisk grep i rapporten.

> **[PLACEHOLDER: Legg til funn fra systematisk litteratursøk (fase 3) om eventuell tidligere forskning på lagerstyring av brannvesen-PVU, norsk eller internasjonal. Dersom ingen treff: dokumenter dette som en identifisert forskningsgap.]**

### 1.4 Problemstilling

På bakgrunn av ovenstående er rapportens overordnede problemstilling:

> *Hvordan kan lagerstyring av røykdykkerbekledning ved Rogaland Brann og Redning IKS analyseres og dimensjoneres under usikker, hendelsesdrevet etterspørsel for å oppnå definert servicegrad til lavest mulig kapitalbinding?*

Problemstillingen operasjonaliseres gjennom fem forskningsspørsmål. De tre første er kjernen i prosjektet:

- **RQ1:** Hvordan kan etterspørselen etter rent røykdykkerutstyr modelleres på grunnlag av historiske BRIS-data, og hva kjennetegner etterspørselsmønsteret per stasjon?
- **RQ2:** I hvilken grad utgjør vaskekapasiteten en flaskehals, og hvordan kan denne modelleres med køteori for å bestemme forventet forsinkelse W₀?
- **RQ3:** Hvilken lagerpolicy — personlig tildeling, felles pool eller hybrid — gir best balanse mellom servicegrad og kapitalbinding gitt observert etterspørsel?

To sekundære spørsmål belyser utvidelsespotensialet:

- **RQ4:** Hvilken effekt vil innføring av RFID-sporbarhet ha på dimensjoneringsbehovet og styringsmulighetene?
- **RQ5:** I hvilken grad kan metodikken generaliseres til andre norske brannvesen med tilsvarende struktur?

### 1.5 Avgrensninger

For å holde prosjektet gjennomførbart er følgende avgrensninger lagt til grunn:

**Utstyrsavgrensning.** Rapporten behandler utelukkende røykdykkerbekledning (jakke og bukse). Øvrig PVU som hjelmer, hansker og støvler holdes utenfor, da disse har vesentlig annerledes vaskesyklus og dimensjoneringslogikk.

**Planleggingsnivå.** Analysen opererer på strategisk og taktisk planleggingsnivå — fastsettelse av samlet beholdningsstørrelse og poolstruktur. Operativ sanntidsstyring er ikke en del av modellen.

**Geografisk og organisatorisk avgrensning.** Modellen analyserer primært de to poolene ved Stangeland og Schankeholen, der etterspørselen aggregeres per pool. Full modellering av alle stasjoner gjøres avhengig av datatilgjengelighet.

**Allokeringspolicy.** For modellens formål forenkles allokeringen til «first-come-first-served»; mer komplekse prioriteringsregler er ikke inkludert i grunnmodellen.

**Ekstreme hendelser.** Masseulykker og ekstraordinære hendelser som krever ressurser utover normal beredskapskapasitet holdes utenfor modellens gyldighetsområde.

**RFID (RQ4).** Analysen av RFID-teknologi begrenses til scenariosammenligning og inkluderer ikke implementeringskostnader eller teknisk spesifisering.

**Kostnader ved mangel.** Konsekvenser av bekledningsunderskudd kvantifiseres ikke monetært; servicegrad brukes som surrogatmål for beredskapsevne.

### 1.6 Antagelser

Følgende antagelser legges til grunn for analysen:

- BRIS-data og beholdningsdata fra RogBR er tilgjengelige i tilstrekkelig kvalitet til å estimere etterspørselsparametere
- Vaskekapasitet og gjennomsnittlig ledetid kan estimeres fra operasjonelle data og intervjuer
- Servicegrad kan defineres i samarbeid med RogBR, med et minimum på 99 %
- Drakter er funksjonelt identiske — ingen differensiering av størrelse eller merke i modellen
- Systemet er i stasjonær tilstand (steady-state) — ingen strukturelle endringer i stasjonsnettverk i analyseperioden

---

## 2. Litteratur

> *Litteraturkapittelet diskuterer de viktigste bidragene fra de siste 5–10 årene innen temaet, plasserer oppgaven i feltet, og viser hvorfor METRIC er valgt som primærmodell. Her skal det trekkes tråder til problemstillingen og beskrives hvor rapporten posisjonerer seg.*

> **[PLACEHOLDER — skrives i fase 3 etter systematisk litteratursøk]**
>
> **Litteratursøket skal dekke:**
> - METRIC-familien og recoverable item inventory (Sherbrooke 1968, Graves 1985, Sherbrooke 2004, Axsäter 2015)
> - Compound Poisson-etterspørsel og parameterestimering fra begrenset data (Prak et al. 2021, Turrini & Meissner 2019)
> - To-echelon modeller med lateral transshipments (Lee 1987, Drent & Arts 2021)
> - System-orienterte servicekrav og beredskapslogistikk (Basten & van Houtum 2014)
> - Eventuell PPE-logistikk-litteratur (brannvesen, ambulanse, militær)
> - Gap-identifikasjon: oppgavens bidrag til feltet

---

## 3. Teori

> *Teorikapittelet presenterer det teoretiske fundamentet for modellen. Det skal beskrive grunnlaget for studiet og danne utgangspunktet for metodevalg. Skrives i fase 3 etter at litteratursøk er gjennomført.*

### 3.1 Stokastisk lagerstyring og recoverable items

> **[PLACEHOLDER — skrives fase 3]**
>
> **Innhold:** Klassisk lagerteori (Axsäter 2015, Silver et al.) → recoverable item-paradigme: lukket kretsløp, fixed population. Systemets tilstandsrom: tilgjengelig / i pipeline (vask) / avskrevet. Forutsetninger for steady-state-analyse.

### 3.2 Base-stock policy og (S−1, S)-logikk

> **[PLACEHOLDER — skrives fase 3]**
>
> **Innhold:** One-for-one replenishment som optimal policy under Poisson-etterspørsel (Hadley & Whitin 1963). Base-stock-nivå Sᵢ som beslutningsvariabel. EBO-beregning (Expected Backorders). Servicegradfunksjoner: cycle service level vs. fill rate — valg av CSL som primær metric i beredskapssammenheng (Axsäter 2015, kap. 3).

### 3.3 METRIC — Multi-Echelon Technique for Recoverable Item Control

> **[PLACEHOLDER — skrives fase 3]**
>
> **Innhold:**
> - Originalartikel Sherbrooke (1968): pipeline-logikk, etterspørsel som Poisson-prosess, to-nivå struktur
> - Graves (1985): eksakt steady-state-løsning med one-for-one og compound Poisson
> - VARI-METRIC (Sherbrooke 1986): forbedrede approksimasjoner
> - Applikasjon på RogBR: sentrallager = Stangeland/vaskeri, baser = stasjonene
> - Beslutningsvariabel Sᵢ og servicegradkravet

### 3.4 Køteori og vaskekapasitet som flaskehals

> **[PLACEHOLDER — skrives fase 3]**
>
> **Innhold:** M/D/c-kø for vaskelinjen. Littles lov: L = λW. Beregning av W₀ (gjennomsnittlig ventetid på vask). Effektiv ledetid L̃ᵢ = Lᵢ + W₀. Flaskehalsbetingelse: når kapasitetsutnyttelse ρ → 1 divergerer W₀.

### 3.5 Compound Poisson-etterspørsel

> **[PLACEHOLDER — skrives fase 3]**
>
> **Innhold:** Motivasjon: ett oppdrag kan utløse bruk av k sett (k = antall røykdykkere i innsats). Compound Poisson (λ, G_k) som modell (Graves 1985). Estimering fra BRIS-data (Prak et al. 2021, Turrini & Meissner 2019).

---

## 4. Casebeskrivelse

### 4.1 Organisasjon og kontekst

Rogaland Brann og Redning IKS (RogBR) er et interkommunalt selskap som ivaretar brann- og redningstjenesten for Stavanger-regionen i Rogaland fylke. Selskapet opererer med kasernert heltidsstyrke ved sine to hovedstasjoner og dekker i tillegg et nettverk av deltidsstasjoner i regionen.

> **[PLACEHOLDER: Antall eierkommuner, totalt antall ansatte, organisasjonskart — innhentes fra Tom Meyer / RogBR]**

Røykdykkerinnsats er blant de mest ressurskrevende operasjonene brannvesenet utfører: det krever spesialtrent personell med godkjent verneutstyr, og utgjør dermed den mest krevende kategorien av innsatser sett fra et utstyrsperspektiv. Bekledningen er livreddende og underlagt krav til funksjonsdyktighet (renhet, integritet) som nødvendiggjør vask etter hver innsats.

### 4.2 Stasjonsnettverk og poolstruktur

RogBR opererer med en poolbasert struktur for røykdykkerbekledning, der de to kasernerte stasjonene utgjør knutepunktene:

| Lokasjon | Type | Pool-beholdning | Vaskelinje |
|---|---|---|---|
| **Stangeland** | Hovedstasjon, sentrallager | 65 sett | Ja — kapasitet 4 sett/runde |
| **Schankeholen** | Kasernert stasjon | 49 sett | Ja — kapasitet 4 sett/runde |
| **Innsatskonteiner** | Mobil beredskap | 6 sett | Nei — til Stangeland/Schankeholen |
| **Varmen** | [PLACEHOLDER type] | [PLACEHOLDER] | [PLACEHOLDER] |
| **Kvernavik** | [PLACEHOLDER type] | [PLACEHOLDER] | [PLACEHOLDER] |
| **Øvrige deltidsstasjoner** | Deltid | [PLACEHOLDER] | Nei |

*Kilde: RogBR intern dokumentasjon (2025); T. Meyer, personlig kommunikasjon, 24. februar 2026*

Stangeland fungerer som sentrallager (depot) og betjener i tillegg deltidsstasjoner som ikke har egen vaskelinje. Den samlede beholdningen utgjør om lag 428 sett fordelt mellom hel- og deltidsstyrker.

> **[PLACEHOLDER: Fullt stasjonskart med stasjonsnummer, type og tilknytning til pool — innhentes fra Petter Nielsen (ansvarlig for røykdykkere) og Geir Nilsen (ansvarlig inventar/bygg)]**

### 4.3 Bekledningssystemet

Røykdykkerbekledningen som analyseres i denne rapporten består av jakke og bukse. Settet er teknisk verneutstyr som tilfredsstiller kravene i EN 469 (europeisk standard for brannbekledning).

> **[PLACEHOLDER: Teknisk spesifikasjon, merkevare/leverandør, levetid — innhentes fra Bent Høgemark (innkjøpsansvarlig)]**

Systemet er et **lukket kretsløp med fast populasjon** (*recoverable items*): draktene sirkulerer mellom tilstandene *tilgjengelig på stasjon*, *i bruk eller til vask* og *avskrevet*. Nye enheter tilføres kun ved avskrivning eller ved nye brukere — ikke ved ordinært forbruk. Utskiftningsraten er estimert til 17,5 % per år, tilsvarende om lag 75 sett per år (RogBR intern dokumentasjon, 2025). Dette systemet skiller seg fundamentalt fra klassisk bestillingslager: det er ikke snakk om å «fylle opp» fra en ekstern leverandør ved bruk, men om å dimensjonere et sirkulerende lager slik at et minimum antall sett alltid er tilgjengelig på riktig sted.

### 4.4 Prosessflyt: vask og retur

Etter røykdykkerinnsats pakkes bekledningen i plastikksekker på skadestedet. Deretter følger en standardisert prosessflyt:

1. **Innlevering og transport** — Bekledningen transporteres til nærmeste vaskelinje (Stangeland eller Schankeholen)
2. **Vask** — Maskinvask; kapasitet er **4 sett per vaskerunde**
3. **Tørking** — Bekledningen henges i tørkerom; estimert tørketid ca. ett døgn
4. **Retur til pool** — Bekledningen legges tilbake i klespool og er igjen tilgjengelig

**Estimert total turnaround: 24–36 timer** fra innlevert til klart for ny innsats (T. Meyer, personlig kommunikasjon, 24. februar 2026). Denne ledetiden (W₀ i METRIC-modellen) er den sentrale parameteren for å beregne forventet pipeline-lager og dimensjoneringsbehovet.

**Dekontaminering:** RogBR utøver ikke ozonbehandling. Selskapet har imidlertid signert avtale om CO₂-dekontaminering for oppdrag med kjemikalieeksponering. CO₂-behandling kan ha lengre prosessid enn ordinær vask og vil undersøkes nærmere i fase 3.

> **[PLACEHOLDER: Detaljer om CO₂-vaskekapasitet og prosessid — avklares med Petter Nielsen]**

### 4.5 Beholdningsstatus og dimensjoneringspraksis i dag

RogBRs nåværende dimensjonering er basert på en tommelfingerregel som beregner behov med utgangspunkt i simultane hendelser:

| Stasjon | Beregningsgrunnlag | Resulterende dimensjonering |
|---|---|---|
| Stangeland | 3 samtidige branner × 6 røykdykkere + 4 i reserve | 22 sett per innsats |
| Schankeholen | 2 samtidige branner × 6 røykdykkere, begrenset av ressursoverlapp | 6 sett per innsats |

Samlet beholdning er om lag 428 sett, med en enhetskostnad på ca. 18 000 kr, tilsvarende en kapitalbinding på om lag **7,7 millioner kroner**.

Beholdningsoversikten per stasjon er i dag basert på en telleliste, men denne er ifølge logistikkansvarlig ikke pålitelig i praksis:

> *«Vi har pr i dag en dårlig rutine på det. Vi skal i utgangspunktet forholde oss til en telleliste, men denne fungerer ikke i praksis.»* — Tom Meyer, logistikkansvarlig RogBR, 24. februar 2026

Faktisk antall sett per stasjon vil verifiseres gjennom feltarbeid i fase 3, enten via manuell opptelling eller via RFID-data dersom tilgjengelig.

### 4.6 Rettslig rammeverk og dimensjoneringsansvar

Frem til 2022 spesifiserte den nasjonale brannvernforskriften detaljerte krav til brannvesenets verneutstyr. Etter vedtagelsen av FOR-2022-01-18-65 ble dimensjoneringsansvaret overført til arbeidsmiljøloven, noe som innebærer at RogBR nå selv — gjennom sin ROS- og beredskapsanalyse — er forpliktet til å dokumentere dimensjonerende hendelser og nødvendig utstyrsbehov (DSB, 2022).

RogBR har en eksisterende ROS- og beredskapsanalyse som angir dimensjonerende hendelser organisasjonen skal være forberedt på. Denne rapporten vil sammenligne modellens dimensjoneringsanbefaling med analysens normative krav, og vurdere om det er samsvar mellom historisk BRIS-etterspørsel og de dimensjonerende scenarioene i beredskapsanalysen.

> **[PLACEHOLDER: ROS- og beredskapsanalysen anskaffes i fase 3 fra Geir Nilsen / Tom Meyer]**

---

## 5. Metode og data

### 5.1 Metode

**Forskningsdesign**

Rapporten benytter et **kvantitativt case-studie-design**. Case-studiet er valgt fordi problemstillingen er avgrenset til én konkret organisasjon (RogBR), og fordi tilgangen til rike, detaljerte data fra BRIS-registeret muliggjør et dybdestudie som ikke lar seg gjennomføre med en ren surveybasert tilnærming.

> **[PLACEHOLDER — beskriv forskningsparadigme (positivistisk/pragmatisk), argumenter for case-metode mot alternativene]**

**Innsamlingsmetode**

Data innhentes gjennom to primære kanaler:

1. **Kvantitative registerdata** — BRIS-registeret (8 098 hendelser, 2021–2025) for etterspørselsmodellering
2. **Semi-strukturerte intervjuer** — nøkkelinformanter i RogBR for å kartlegge organisatorisk kontekst, vaskekapasitet, pool-struktur og validere antagelser

**Analysemetode**

Analysen kombinerer:
- Statistisk etterspørselsmodellering (fordelingstilpasning, Poisson-test)
- Analytisk modellering (METRIC, køteori)
- Monte Carlo simulering (validering av approksimasjonsfeil)
- Scenarioanalyse (sensitivitetsanalyse og RFID-effekt)

**Bruk av kunstig intelligens**

KI benyttes som analytisk verktøy i dette prosjektet, ikke som selvstendig forskningsbidrag. Konkret bruk inkluderer: parameterestimering fra BRIS-data, Monte Carlo-simulering og strukturering av Python-implementasjonen. KI-assisterte steg er dokumentert med revisjonsspor i Jupyter notebooks.

### 5.2 Data

**BRIS-data (primær kvantitativ datakilde)**

| Parameter | Verdi |
|---|---|
| Kilde | Direktoratet for samfunnssikkerhet og beredskap (DSB) via RogBR |
| Tidsperiode | 2021–2025 (5 år) |
| Antall observasjoner (rådata) | 8 098 hendelser |
| Antall kolonner | 580 |
| Nøkkelkolonne for analyse | Kol. 56: Innvendig røykdykkerinnsats (JA/NEI) |
| Antall observasjoner etter rensing | [PLACEHOLDER — etter datarensing i fase 3] |

Rådata lagres uendret i `004 data/`. All behandling skjer på kopier med dokumenterte transformasjoner i Jupyter notebooks.

**Intervjudata**

| Informant | Rolle | Bidrag | Tidspunkt |
|---|---|---|---|
| Tom Meyer | Logistikkansvarlig | Vaskekapasitet, ledetider, kostnader, overordnet dataoversikt | E-post 24.02.2026; intervju fase 3 |
| Petter Nielsen | Ansvarlig for røykdykkere | Pool-struktur, prioriteringsregler, operativ praksis | Intervju fase 3 |
| Bent Høgemark | Innkjøpsansvarlig | Innkjøpspris, leveringstid, kassering | Intervju fase 3 |
| Geir Nilsen | Ansvarlig inventar/bygg | Lageroversikt, stasjonskartlegging, ROS-analyse | Intervju fase 3 |
| Innsatsleder S01 | Kasernert stasjon | Validering: mangeltilfeller, faktisk praksis | Intervju fase 3 |
| 2–3 brannmenn | Operativt nivå | Validering: stemmer formell policy med faktisk praksis? | Fase 3 |

**Øvrige datakilder**

> **[PLACEHOLDER — ROS- og beredskapsanalyse fra RogBR (Geir Nilsen); RFID-vaskedata (Petter Nielsen/Bent Høgemark — status uavklart)]**

---

## 6. Modellering

### 6.1 Systemrepresentasjon

RogBRs bekledningssystem modelleres som et **to-nivå recoverable item-system** i tråd med METRIC-rammeverket (Sherbrooke, 1968; Axsäter, 2015, kap. 10.2):

- **Nivå 1 — Depot (sentrallager):** Stangeland/vaskelinje. Mottar brukte drakter fra alle stasjoner; utfører vask og returnerer til poolene.
- **Nivå 2 — Baser:** De individuelle stasjonene/poolene (Stangeland, Schankeholen, innsatskonteiner, [PLACEHOLDER: øvrige stasjoner]).

**Beslutningsvariabel:** Sᵢ — order-up-to-nivå (pool-størrelse) per stasjon i, som velges for å tilfredsstille servicegradkravet SL ≥ 99 %.

### 6.2 Etterspørselsmodell

Etterspørselen ved stasjon i modelleres som en Poisson-prosess med rate **λᵢ** hendelser per tidsenhet (dag/uke). Parameteren estimeres fra BRIS-data, kolonne 56 (innvendig røykdykkerinnsats), for perioden 2021–2025.

Muligheten for **compound Poisson-etterspørsel** (batch-etterspørsel) undersøkes: ett brannoppdrag utløser bruk av k sett, der k varierer med type og omfang av innsatsen. Dersom compound Poisson er en bedre tilpasning til dataene enn enkel Poisson, benyttes Graves (1985) sitt rammeverk for eksakt compound Poisson-behandling i METRIC.

> **[PLACEHOLDER: Faktisk estimert λᵢ per stasjon og empirisk fordeling av batch-størrelse k — resulterer fra dataanalysen i fase 3]**

### 6.3 Depotmodell og flaskehalsvurdering (W₀)

Depotet modelleres som en **M/D/c-kø** (Poisson-ankomster, deterministisk betjeningstid, c maskiner), der:

| Parameter | Verdi | Kilde |
|---|---|---|
| Ankomstrate λ_total | [PLACEHOLDER] drakter/dag | Estimert fra BRIS-data |
| Betjeningstid per sett | ca. 1 døgn (vask + tørk) | T. Meyer, 24.02.2026 |
| Kapasitet c | 4 sett per vaskerunde | T. Meyer, 24.02.2026 |
| Antall maskiner | [PLACEHOLDER] | Petter Nielsen (fase 3) |

Gjennomsnittlig ventetid **W₀** (forventet tilleggsforsinkelse pga. vaskekapasitetsgrensen) beregnes med Littles lov:

```
L = λ · W  →  W₀ = L₀ / λ
```

W₀ inngår som tilleggsforsinkelse i effektiv ledetid for hver stasjon: **L̃ᵢ = Lᵢ + W₀**.

### 6.4 METRIC-modellen — parameterisering

For hver stasjon i med base-stock-nivå Sᵢ beregnes forventet antall drakter «i pipeline» (EBOᵢ, Expected Backorders) basert på Poisson-fordelingen med parameter (λᵢ · L̃ᵢ):

> **[PLACEHOLDER: EBO-formel, distribusjonsfunksjoner og servicegrad-uttrykk — inkluderes ved implementasjonen i fase 3, ref. Axsäter 2015 kap. 10.2, Sherbrooke 1968]**

Optimal Sᵢ velges som det minste heltall som tilfredsstiller:

```
SL(Sᵢ) = P(etterspørsel ≤ Sᵢ i ledetid L̃ᵢ) ≥ 0,99
```

**Total kapitalbinding** tilhørende en konfigurasjon {S₁, S₂, ..., Sₙ}:

```
K = Σ Sᵢ · c_enhet = Σ Sᵢ · 18 000 kr
```

### 6.5 Validering

Monte Carlo-simulering benyttes for å validere den analytiske METRIC-approksimasjonen. Simuleringen modellerer individuelle drakters tilstandsoverganger (tilgjengelig → i vask → tilgjengelig) over en tilstrekkelig lang tidshorisont.

- Antall replikasjoner: [PLACEHOLDER: N = X, fastsettes ved implementasjon]
- Målevariabler: observert servicegrad per stasjon vs. analytisk prediksjon
- Akseptkriterium: avvik ≤ 0,5 prosentpoeng

---

## 7. Analyse

> **[PLACEHOLDER — gjennomføres i fase 3]**
>
> **Planlagt innhold:**
> - 7.1 Eksplorativ analyse av BRIS-data: etterspørselsrate λᵢ per stasjon, sesongmønster, fordelingstilpasning
> - 7.2 Vaskekapasitetsanalyse: beregning av W₀ under ulike kapasitetsscenarioer
> - 7.3 METRIC-kjøring: beregning av optimale Sᵢ for valgt servicegradkrav
> - 7.4 Policy-sammenligning: personlig vs. pool vs. hybrid (RQ3)
> - 7.5 Sensitivitetsanalyse: robusthet ved endringer i λ, W₀ og servicegradkrav
> - 7.6 RFID-scenario (RQ4): sammenligning med og uten forbedret informasjon

---

## 8. Resultat

> **[PLACEHOLDER — presenteres i fase 3/4]**
>
> **Planlagt innhold:**
> - Tabell: optimalt beholdningsnivå Sᵢ per stasjon for SL = 99 %
> - Sammenligningstabell: nåsituasjon (428 sett) vs. modellanbefaling
> - Figur: servicegrad som funksjon av total beholdning (kost–service-kurve)
> - Tabell: policy-sammenligning (pool vs. personlig vs. hybrid)
> - Figur: sensitivitetsanalyse — nøkkelparametere
> - Monte Carlo-validering: analytisk vs. simulert servicegrad

---

## 9. Diskusjon

> **[PLACEHOLDER — skrives i fase 3/4 etter resultater]**

### 9.1 Tolkning av resultater

> **[PLACEHOLDER]**
>
> Diskuter: Er resultatet som forventet? Stemmer modellens anbefaling med RogBRs intuitive vurderinger? Hva forklarer eventuelle avvik?

### 9.2 Validering mot beredskapsanalyse

> **[PLACEHOLDER]**
>
> Sammenlign modellens dimensjoneringsanbefaling med RogBRs normative beredskapsanalyse (ROS). Dekker METRIC-modellen dimensjonerende scenario? Er det samsvar mellom historisk BRIS-etterspørsel og analysens forutsetninger?

### 9.3 Begrensninger

**Kjente modellantagelser og begrensninger:**

- METRIC antar uavhengige forsinkelser mellom stasjoner. I praksis kan «common cause stockout» oppstå: hvis alle drakter er til vask samtidig, rammes alle stasjoner parallelt. Denne korrelasjonen adresseres gjennom Monte Carlo-simulering og dokumenteres som kjent begrensning.
- Poisson-etterspørsel antar at hendelser er uavhengige og stasjonære. Eventuelle sesong- og ukedagsmønster i BRIS-data vil undersøkes og dokumenteres.
- Tellelisten er upålitelig — faktisk beholdning per stasjon er ikke bekreftet og kan avvike fra 428 sett.

> **[PLACEHOLDER: Ytterligere begrensninger identifisert under gjennomføringen]**

### 9.4 Generalisering (RQ5)

> **[PLACEHOLDER]**
>
> Diskuter forutsetninger for at metodikken kan overføres til andre norske brannvesen. Hvilke parametere er lokale (λᵢ, W₀) vs. generiske (modellstruktur)?

### 9.5 Praktisk implikasjon for RogBR

> **[PLACEHOLDER]**
>
> Hva bør RogBR gjøre på bakgrunn av funnene? Konkrete handlingsanbefalinger.

---

## 10. Konklusjon

> **[PLACEHOLDER — skrives i fase 4]**
>
> **Struktur:**
> - Gjenta problemstillingen
> - Oppsummer de viktigste funnene (én setning per RQ)
> - Konkluder i lys av problemstillingen
> - Fremhev praktisk implikasjon
> - Pek på åpne spørsmål for videre forskning

---

## 11. Bibliografi

Axsäter, S. (2015). *Inventory control* (3. utg.). Springer. https://doi.org/10.1007/978-3-319-15729-0

Basten, R. J. I., & van Houtum, G. J. (2014). System-oriented inventory models for spare parts. *Surveys in Operations Research and Management Science, 19*(1), 34–55. https://doi.org/10.1016/j.sorms.2014.05.002

Direktoratet for samfunnssikkerhet og beredskap. (2022). *Brann- og redningsvesenforskriften* (FOR-2022-01-18-65). Lovdata. https://lovdata.no/dokument/SF/forskrift/2022-01-18-65

Direktoratet for samfunnssikkerhet og beredskap. (2022). *Veiledning til brann- og redningsvesenforskriften*. DSB. https://www.dsb.no

Drent, M., & Arts, J. (2021). Expediting in two-echelon spare parts inventory systems. *Manufacturing & Service Operations Management, 24*(2), 1000–1019. https://doi.org/10.1287/msom.2020.0888

Graves, S. C. (1985). A multi-echelon inventory model for a repairable item with one-for-one replenishment. *Management Science, 31*(10), 1247–1256. https://doi.org/10.1287/mnsc.31.10.1247

Guide, V. D. R., Jr., & Srivastava, R. (1997). Repairable inventory theory: Models and applications. *European Journal of Operational Research, 102*(1), 1–20. https://doi.org/10.1016/S0377-2217(97)00155-0

Hadley, G., & Whitin, T. M. (1963). The (S−1, S) inventory policy under compound Poisson demand. *Management Science, 9*(3), 391–396. https://doi.org/10.1287/mnsc.9.3.391

Hillestad, R. (1982). *Dyna-METRIC: Dynamic multi-echelon technique for recoverable item control* (RAND Report R-2785-AF). RAND Corporation.

Hu, Q., Boylan, J. E., Chen, H., & Labib, A. (2018). OR in spare parts management: A review. *European Journal of Operational Research, 266*(2), 395–414. https://doi.org/10.1016/j.ejor.2017.07.058

Lee, H. L. (1987). A multi-echelon inventory model for repairable items with emergency lateral transshipments. *Management Science, 33*(10), 1302–1316. https://doi.org/10.1287/mnsc.33.10.1302

Lesniak, Z. C., Smith, D. L., & Notarianni, K. A. (2020). The effect of personal protective equipment on firefighter occupational performance. *Journal of Occupational and Environmental Hygiene, 17*(1), 1–9. https://doi.org/10.1080/15459624.2019.1692684

Muckstadt, J. A. (1973). A model for a multi-item, multi-echelon, multi-indenture inventory system. *Management Science, 20*(4), 472–481. https://doi.org/10.1287/mnsc.20.4.472

Prak, D., Teunter, R., Syntetos, A., & van Houtum, G. J. (2021). Robust compound Poisson parameter estimation for inventory control. *Omega, 104*, 102481. https://doi.org/10.1016/j.omega.2021.102481

Sherbrooke, C. C. (1968). METRIC: A multi-echelon technique for recoverable item control. *Operations Research, 16*(1), 122–141. https://doi.org/10.1287/opre.16.1.122

Sherbrooke, C. C. (1986). VARI-METRIC: Improved approximations for multi-indenture, multi-echelon availability models. *Operations Research, 34*(2), 311–319. https://doi.org/10.1287/opre.34.2.311

Sherbrooke, C. C. (2004). *Optimal inventory modeling of systems: Multi-echelon techniques* (2. utg.). Springer. https://doi.org/10.1007/b109856

Srivathsan, S., & Viswanathan, S. (2017). Queueing-based models for a multi-echelon repairable item inventory system. *Computers & Operations Research, 79*, 350–362. https://doi.org/10.1016/j.cor.2016.07.011

Teunter, R. H., Syntetos, A. A., & Babai, M. Z. (2011). Intermittent demand: Linking forecasting to inventory obsolescence. *European Journal of Operational Research, 214*(3), 606–615. https://doi.org/10.1016/j.ejor.2011.05.018

Topan, E., Eruguz, A. S., Ma, W., van der Heijden, M. C., & Dekker, R. (2019). A review of operational spare parts service logistics in service control towers. *European Journal of Operational Research, 276*(3), 1–17. https://doi.org/10.1016/j.ejor.2019.03.026

Turrini, L., & Meissner, J. (2019). Spare parts inventory management: New evidence from distribution fitting. *European Journal of Operational Research, 273*(1), 118–130. https://doi.org/10.1016/j.ejor.2018.07.017

van Houtum, G.-J., & Kranenburg, B. (2015). *Spare parts inventory control under system availability constraints*. Springer. https://doi.org/10.1007/978-1-4615-4195-8

---

## 12. Vedlegg

### Vedlegg A — Python-kode

> **[PLACEHOLDER: Kode legges på GitHub og refereres her. Inkluderer: BRIS-rensing, etterspørselsestimering, METRIC-implementasjon, Monte Carlo-simulering, sensitivitetsanalyse]**

### Vedlegg B — Intervjuguide: Tom Meyer (logistikkansvarlig)

> Fullstendig intervjuguide, se `012 fase 2 - plan/Intervju_Tom_Meyer_Logistikk.tex`

### Vedlegg C — Intervjuguider: Petter Nielsen, Bent Høgemark, Geir Nilsen

> **[PLACEHOLDER: Semi-strukturerte intervjuguider — utarbeides i fase 3]**

### Vedlegg D — BRIS-databehandling

> **[PLACEHOLDER: Dokumentasjon av datarensingsprosess — antall inkluderte og ekskluderte observasjoner, kolonnebeskrivelse, Jupyter notebook]**

### Vedlegg E — Sensitivitetsanalyse (utvidet tabeller)

> **[PLACEHOLDER: Tabeller for alle sensitivitetsscenarioer]**

---

*Rapport v0.1 — Opprettet: 2026-02-27 | Neste gjennomgang: etter intervjuer i fase 3 (uke 11–12)*

*Seksjoner med `[PLACEHOLDER]` er planlagt innhold som realiseres i fase 3–4.*
