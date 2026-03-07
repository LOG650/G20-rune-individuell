# Prosjektstyringsplan
**LOG650 – Forskningsprosjekt: Logistikk og kunstig intelligens**

| | |
|---|---|
| **Prosjekt** | Kapasitetsstyring og bemanningsdimensjonering ved norske 110-sentraler |
| **Gruppe** | G20 – Rune Individuell |
| **Utarbeidet av** | Rune Grødem |
| **Autorisert av** | Emneansvarlig, LOG650 |
| **Dato** | 2026-03-07 |
| **Versjon** | 1.3 |

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

Dette dokumentet utgjør prosjektstyringsplanen for prosjektet **«Kapasitetsstyring og bemanningsdimensjonering ved norske 110-sentraler»**. Prosjektet gjennomføres i LOG650 som et prosjektorganisert forskningsarbeid, der hovedleveransen er en vitenskapelig rapport med tilhørende kvantitativ modell implementert i Python.

### 1.1 Bakgrunn og behov

Norske 110-sentraler mottar nødmeldinger og koordinerer brann- og redningsinnsats døgnet rundt. Minimumsbemanning er lovfestet til to operatører i vaktrommet, men dimensjonering utover dette fastsettes lokalt basert på risiko- og beredskapsanalyser (ROS). Det finnes ingen nasjonal, kvantitativ standard for hvordan operativ belastning skal oversettes til konkret bemanningsnivå.

Forfatteren har operativ erfaring fra 110 Sør-Vest og tilgang til hendelsesdata fra LEO/BRIS tilbake til 2020. Fra høsten 2024 benytter alle norske 110-sentraler det felles oppdragshåndteringssystemet LEO, noe som muliggjør sammenlignbare data på tvers av sentraler. Dette gir et unikt empirisk grunnlag for å analysere og sammenligne bemanningsbehov kvantitativt.

### 1.2 Problemstilling

I hvilken grad samsvarer faktisk bemanning ved norske 110-sentraler med kapasitetsbehovet beregnet fra historiske hendelsesdata og køteoretiske modeller?

Operativ belastning ved en 110-sentral kjennetegnes av stokastisk ankomst av hendelser med ulik håndteringstid og ressursbehov. En sentral modellantagelse er at Vaktleder (VL) normalt ikke besvarer nødanrop, noe som innebærer at effektiv operatørkapasitet er `c_effektiv = c_total − 1`. 110 Sør-Vest opererer med normalbesetning på 3 operatører + Vaktleder (totalt 4) på dagskift, og kan gå ned til 2 operatører + Vaktleder (totalt 3) på nattskift og i helger. Effektiv kapasitet er dermed `c_effektiv = 3` (dag) og `c_effektiv = 2` (natt/helg).

Prosjektet benytter primærcase **110 Sør-Vest** og benchmarker mot alle norske 110-sentraler via DSBs årsrapporter.

En viktig sekkundærdimensjon i prosjektet er en **kritisk gjennomgang av eksisterende ROS- og beredskapsanalyse** for 110 Sør-Vest. Dagens bemanningsnivå er formelt forankret i denne analysen. Prosjektet vil vurdere om analysen gir tilstrekkelig grunnlag for å begrunne faktisk bemanning, om dimensjonerende hendelser samsvarer med planlagt kapasitet, og om forutsetninger om systemer og rutiner er reelt til stede. Funn fra ROS-gjennomgangen sammenlignes eksplisitt med den kvantitative Erlang-C-vurderingen.

### 1.3 Mål

Prosjektmålet er å analysere bemanningssituasjonen ved norske 110-sentraler gjennom en køteoretisk modell basert på empiriske hendelsesdata, og å vurdere om en kvantitativ dimensjoneringsmodell for 110-operatorer kan etableres på samme faglige grunnlag som dimensjoneringsforskriften gir for brannstasjoner.

I dag finnes det ingen nasjonal, kvantitativ standard for bemanningsdimensjonering av 110-sentraler. Dimensjoneringsforskriften (FOR-2023-01-06-23) gir ferdige, etterprøvbare bemanningskrav for kasernert og deltidsbrannvesen basert på innbyggertall og responstid — en ferdig «ferdigtygget» analyse som gir liten rom for strategisk tilpasning. Tilsvarende standard mangler helt for 110-operatorer: bemanningsnivået fastsettes gjennom lokale ROS- og beredskapsanalyser som er kvalitative og vanskelige å etterprøve eller sammenligne kvantitativt på tvers av sentraler.

Prosjektet har således en dobbel ambisjon:
1. **Casestudie (110 Sør-Vest):** Dokumentere i hvilken grad faktisk bemanning samsvarer med kapasitetsbehovet beregnet fra historiske data og Erlang-C-modellen
2. **Generaliseringsambisjon:** Undersøke om strukturelle prediktorer (hendelsesvolum, innbyggertall, areal) kan danne grunnlag for en nasjonal, etterprøvbar dimensjoneringsmodell for 110-operatorer — analogt med dimensjoneringsforskriftens rolle for brannvesenet

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

> **Kilde:** Forelesning 11. februar 2026: *«vi har et C-krav på innlevert, altss det du leverer inn i løpet av milepælene, men vi har et B-krav når det gjelder rapport og muntlig»*.

---

## 2. Forretningscase

### 2.1 Bakgrunn

Norske 110-sentraler er kritisk beredskapsinfrastruktur. Alle 12 norske 110-sentraler (Finnmark, Troms, Nordland, Trøndelag, Møre og Romsdal, Vest, Sør-Vest, Agder, Sør-Øst, Oslo, Øst og Innlandet) er det primære kontaktpunktet for brann- og redningsnødmeldinger. Bemanningsdimensjonering er lovpålagt (Brann- og redningsvesenforskriften), men uten kvantitative nasjonale standarder er det opp til hver sentral å fastsette bemanning gjennom ROS-analyser av varierende kvalitet og metodisk robusthet.

Det finnes en tydelig kontrast til hvordan brannstasjonsbemanning dimensjoneres: dimensjoneringsforskriften (FOR-2023-01-06-23) gir ferdige, etterprøvbare krav til kasernert og deltidsbrannvesen basert på innbyggertall og responstid. Bemanningsnivået er kvantitativt forankret og kan etterprøves. En tilsvarende kvantitativ standard mangler helt for 110-operatorer.

Konsekvensene av feil dimensjonering er asymmetriske:
- **Underbemanning:** Forsinkede svar på nødanrop, økt kø, redusert operativ kapasitet ved samtidige hendelser — med potensielt livstruende konsekvenser
- **Overbemanning:** Unødvendige personalkostnader for kommunene som drifter sentralene

Et kvantitativt beslutningsgrunnlag basert på faktiske belastningsdata kan gi et mer etterprøvbart fundament for dimensjoneringsvedtak enn dagens erfaringsbaserte praksis. Det er grunn til å spørre om eksisterende ROS- og beredskapsanalyser faktisk begrunner valgt bemanning på en metodisk tilstrekkelig måte — herunder om dimensjonerende hendelser samsvarer med faktisk observert belastning, og om forutsetninger som legges til grunn for kapasitetsvurderingen er reelt oppfylt. En slik svakhet i eksisterende grunnlag forsterker behovet for en empirisk, kvantitativ tilnærming.

### 2.2 Vurderte alternativer

| Alternativ | Beskrivelse | Vurdering |
|---|---|---|
| **A0 – Status quo** | Videreфøring av ROS-basert dimensjonering uten kvantitativ modell | Forkastet — varierende kvalitet, ikke etterprøvbart |
| **A1 – Simuleringsbasert tilnærming** | Diskret-hendelses-simulering for kapasitetsanalyse | Ikke valgt som primærmetode |
| **A2 – Køteoretisk modell (Erlang-C) med empiriske data** | Fler-server kømodell kalibrert mot historiske hendelsesdata | **Valgt** |

Erlang-C (M/M/c) velges som utgangspunkt fordi modellen er veletablert for kapasitetsanalyse i fler-server call-center-systemer, er direkte tolkbar i dimensjoneringssammenheng, og gir klare implikasjoner for bemanningsanbefalinger per tidsperiode.

### 2.3 Forutsetninger

- LEO/BRIS-data fra 110 Sør-Vest er tilgjengelige for perioden 2020–2025
- Data fra høsten 2024 er sammenlignbare på tvers av sentraler (felles LEO)
- DSBs årsrapporter for 2025 inneholder tilstrekkelig informasjon om bemanning og anropsvolum
- SSB-befolkningsdata er offentlig tilgjengelig per dekningsområde
- Ekstraordinaere hendelser holdes utenfor modellens primære gyldighetsområde

### 2.4 Forventede gevinster

**Operative gevinster**
- Dokumentert sannsynlighet for å oppnå definert servicegrad gitt faktisk bemanning
- Kvantifisert kapasitetsrisiko ved redusert bemanning (nattskift/helg)
- Forståelse av ring-flom-belastning og kapasitetsbufferbehov

**Metodiske gevinster**
- Generaliserbar dimensjoneringsmodell for alle norske 110-sentraler
- Empirisk fundert alternativ til erfaringsbaserte ROS-prosesser

**Strategiske gevinster**
- Overgang fra erfaringsbasert til analytisk beslutningsstøtte i beredskapsplanlegging
- Bedre forståelse av hvilke strukturelle prediktorer (innbyggertall, areal, hendelsesvolum) som forklarer bemanningsvariasjon
- Grunnlag for en nasjonal, etterprøvbar dimensjoneringsstandard for 110-operatorer — analogt med dimensjoneringsforskriften for brannvesenet
- Et objektivt, kvantitativt referansepunkt som kan supplere og sammenlignes med eksisterende ROS/beredskapsanalyser — og bidra til bedre etterprøvbarhet i dimensjoneringsvedtak

**Beredskapsperspektiv**

Et viktig premiss for tolkning av resultatene er at 110-sentraler er beredskapssystemer, ikke rene effektivitetssystemer. Lav kapasitetsutnyttelse i enkeltperioder er ikke nødvendigvis et tegn på overbemanning — i beredskapssystemer kan en viss uutnyttet kapasitet være nødvendig for å håndtere sjeldne, kritiske hendelser og samtidige belastningstopper. Dette perspektivet vil være sentralt i diskusjonskapittelet og påvirker hvordan modellresultatene oversættes til bemanningsanbefalinger.

### 2.5 Kostnader

For 110-sentralene påløper ingen direkte kostnader utover begrenset tidsbruk til intervjuer. Prosjektet gjennomføres som en del av LOG650 ved Høgskolen i Molde.

### 2.6 Analyse og konklusjon

Alternativ A2 — Erlang-C-modell med empiriske data — gir et strukturert, etterprøvbart beslutningsgrunnlag som kan dokumentere om faktisk bemanning er tilstrekkelig gitt observert belastning, identifisere perioder med kapasitetsunderskudd, og gi en generaliserbar modell på tvers av sentraler.

---

## 3. Omfang

### 3.1 Krav

Prosjektet skal:

1. Dokumentere operativ struktur, skiftorganisering og belastningsmonstre ved 110 Sør-Vest, inkludert hendelsestypologi og VL-rolleforutsetning.
2. Etablere og beskrive datagrunnlaget (LEO/BRIS-data, DSB-årsrapporter, SSB-data), inkludert periode, variabler, datakvalitet og rådatahandtering.
3. Avklare og begrunne modellvalg fra pensum — Erlang-C (M/M/c) er identifisert som primærmodell — og beskrive modellens parametere, beslutningsvariabler, målsetting og forutsetninger.
4. Implementere modellen i Python og utføre analyse med dokumentert validering og sensitivitetssjekk.
5. Skrive rapport fortløpende med tydelig skille mellom modell/metode og resultater/diskusjon, med korrekt kildebruk (APA 7th norsk).
6. Gjennomføre en kritisk analyse av eksisterende ROS- og beredskapsanalyse for 110 Sør-Vest: vurdere kvaliteten på dimensjoneringsgrunnlaget, samsvaret mellom antatte dimensjonerende hendelser og faktisk belastning, og i hvilken grad forutsetninger om systemer og rutiner er oppfylt i praksis.

### 3.2 Avgrensninger

- Analysen avgrenses til **vaktromsbemanning** — ikke ressursdisponering i brannvesenet
- Prosjektet er **retrospektivt og planleggingsrettet**, ikke et sanntidssystem
- **2024–2025-data prioriteres** for sammenlignbarhetsanalyse; eldre data benyttes for trendanalyse
- **Ekstraordinære hendelser** holdes utenfor modellens primære gyldighetsområde og behandles i diskusjonskapittelet
- **Ring-flom (call surge)** belyses som operativ ekstrembelastning, men modelleres ikke som primærscenario
- Endelig valg av modell og analysedybde fastsettes etter eksplorativ datagjennomgang og begrunnes i rapporten

### 3.3 Bruk av kunstig intelligens (KI)

Prosjektet gjennomføres i LOG650 — Logistikk og kunstig intelligens. KI benyttes som analytisk støtteverkøy. Planlagt bruk dokumenteres eksplisitt:

| KI-verkøy | Bruksområde |
|---|---|
| **Python (scipy, numpy, pandas)** | Implementasjon av Erlang-C-modell, parameterestimering, statistisk analyse av ankomstrater og håndteringstider |
| **Python (matplotlib, seaborn)** | Visualisering av belastningsmonstre, kapasitetsgap og benchmarking-resultater |
| **Claude (Anthropic)** | Litterätursøk, strukturering av analyse, skrivestotte, kodereview — all bruk dokumenteres i eget vedlegg |
| **GitHub Copilot / Claude Code** | Støtte ved Python-implementasjon — all generert kode valideres manuelt og dokumenteres |

Erlang-C er en analytisk formel, ikke en ML-modell. KI i dette prosjektet handler primært om bruk av KI-verktøy som støtte i en kvantitativ analyseprosess — i tråd med emnets tilnærming til KI som beslutningsstøtteverkøy.

### 3.4 Løsning og leveranser

Løsningen består av:

- **Casebeskrivelse** av 110 Sør-Vest (kontekst, skiftstruktur, hendelsestypologi, VL-rolle, nøkkeltall)
- **Datamodell og datagrunnlag** (LEO/BRIS-data 2020–2025, DSB-årsrapporter, SSB-befolkningsdata, intervjudata)
- **Primærmodell — Erlang-C (M/M/c)**:
  - Ankomstrate (λ) estimert per skiftperiode fra LEO/BRIS-data
  - Gjennomsnittlig håndteringstid (μ⁻¹) estimert per hendelseskategori
  - Antall servere (c) med VL-korreksjon (`c_effektiv = c_total − 1`)
  - Beregnet servicegrad sammenlignet mot de facto grenser (10. anrop → Agder, 60 sek uten svar)
  - Anbefalt bemanning per skiftperiode for definert servicegrad
- **ROS- og beredskapsanalyse-gjennomgang** — kritisk vurdering av eksisterende dimensjoneringsgrunnlag ved 110 Sør-Vest:
  - Identifikasjon av dimensjonerende hendelser som analyäsen legger til grunn
  - Vurdering av om disse samsvarer med faktisk observert hendelsesbelastning fra LEO/BRIS
  - Gjennomgang av forutsetninger om systemer og rutiner — er disse reelt operasjonalisert?
  - Konklusjon om analysens evne til å begrunne valgt bemanningsnivå
- **Benchmarking** mot alle norske 110-sentraler via DSB-årsrapporter
- **Generaliseringsanalyse** — nykkelanalyse: om hendelsesvolum, innbyggertall og areal kan predikere bemanningsbehov på tvers av sentraler med tilstrekkelig presisjon til å danne grunnlag for en nasjonal dimensjoneringsstandard. Denne analysen er det metodiske kjernen i prosjektets nasjonale ambisjoner; omfang tilpasses tilgjengelige data.
- **Implementasjon og analyse i Python** med validering og sensitivitetsanalyse
- **Rapport** med kode tilgjengelig på GitHub

### 3.5 Operative særtrekk og modellforutsetninger

Følgende operative særtrekk ved 110-sentraler skiller dem fra et standard M/M/c-køsystem og vil vurderes eksplisitt i rapporten:

| Særtrekk | Beskrivelse | Modellimplikasjon |
|---|---|---|
| **VL-rollen** | Vaktleder besvarer normalt ikke nødanrop | `c_effektiv = c_total − 1` — eksplisitt korreksjon i modellen |
| **Aktivt hendelsebilde** | Pågående hendelser binder operatørkapasitet utover samtaletid | Økt effektiv håndteringstid; Erlang-C-forutsetning utfordres |
| **Ring-flom (call surge)** | Én hendelse utløser mange samtidige anrop | Brudd på Poisson-uavhengighet; behandles som sensitivitetscase |
| **Overløp til Agder** | 10. kø-anrop viderekoblet | De facto servicegrense — proxy for definert servicegrad |
| **60-sekunders-regel** | Ubesvarte anrop etter 60 sek = kapasitetsbrudd | Proxy for maksimal akseptabel ventetid W |

**Analytiske dimensjoner av operativ belastning**

Operativ belastning ved en 110-sentral kan ikke reduseres til én enkelt variabel. Prosjektet analyserer belastning langs tre komplementære dimensjoner:

| Analysekomponent | Primærvariabel | Funksjon i analysen |
|---|---|---|
| **Kømodell** | Innkommende telefonhenvendelser (λ) | Erlang-C-input; estimerer nødvendig operatørkapasitet |
| **Operativ belastningsanalyse** | Antall oppdrag/hendelser | Forstå faktisk operativ aktivitet og ressursdisponering |
| **Kapasitetsbinding** | Samtidige aktive hendelser | Forklare operatørbinding utover samtaletid |

Primæranalysen bruker telefonhenvendelser som Erlang-C-input (λ). De to øvrige dimensjonene benyttes til å kontekstualisere resultater og belyse avvik mellom telefonbelastning og faktisk operatørbinding — særlig relevant for å forstå effekten av aktivt hendelsebilde (jf. tabell over).

### 3.6 Arbeidsnedbrytningsstruktur (WBS)

**Fase 1 — Initiering (fullført)**

| ID | Leveranse | Frist | Status |
|---|---|---|---|
| L0 | Godkjent proposal | 7. mars 2026 | Innlevert — avventer formell godkjenning |

**Fase 2 — Planlegging (frist 15. mars 2026)**

*Fase 2 er planlegging, ikke gjennomføring. Litterätursøk og datainnhenting planlegges her — selve arbeidet gjennomføres i fase 3.*

| ID | Leveranse | Frist | Status |
|---|---|---|---|
| L1 | Avklart problemstilling + mål + avgrensninger | 7. mars | Fullført |
| L2 | Modellvalg — Erlang-C (M/M/c) identifisert og begrunnet | 7. mars | Fullført |
| L3 | Litterätursøk — planlegging (søkeord, databaser, avgrensning) | 10. mars | På gang |
| L4 | Dataplan — datakilder, variabler, kvalitet, tilgangsstatus | 10. mars | På gang |
| L5 | Godkjent prosjektstyringsplan (dette dokumentet) | **15. mars** | På gang |
| L6 | MS Project Gantt-diagram med referanseplan (baseline) | **15. mars** | Ikke startet |

**Fase 3 — Gjennomføring (17. mars – slutten av april 2026)**

*Fase 3 er der planene fra fase 2 realiseres: data analyseres, modell implementeres og rapport skrives.*

| ID | Leveranse | Frist | Status |
|---|---|---|---|
| L7 | Rapportskjelett + introduksjon og problemstilling v1 | Uke 12 | Ikke startet |
| L8 | Datainnhenting + EDA — LEO/BRIS, belastningsmonstre per skift, hendelsestypefordeling | Uke 12–13 | Ikke startet |
| L8b | ROS- og beredskapsanalyse-gjennomgang — dokumentanalyse av dimensjoneringsgrunnlag, sammenligning med LEO/BRIS-data, vurdering av forutsetninger | Uke 12–13 | Ikke startet |
| L9 | Parameterestimering — ankomstrate (λ) og håndteringstid (μ) per skiftperiode og hendelseskategori | Uke 13 | Ikke startet |
| L10 | Erlang-C modellering — bemanningsanbefaling per skiftperiode med VL-korreksjon | Uke 14 | Ikke startet |
| L11 | Validering og sensitivitetsanalyse — Poisson-test, robusthet ved parameterendringer | Uke 14–15 | Ikke startet |
| L12 | Teorikapittel — køteori, Erlang-C, kapasitetsstyring i beredskapsoperative systemer | Uke 14–15 | Ikke startet |
| L13 | Benchmarking — sammenligning modellanbefaling vs. faktisk bemanning, alle norske 110-sentraler | Uke 15 | Ikke startet |
| L14 | Generaliseringsanalyse — prediksjon av bemanningsbehov fra strukturelle variabler (innb., areal, volum) | Uke 15–16 | Ikke startet |
| L15 | Resultater og diskusjon — rapportutkast inkl. operative særtrekk og modellbegrensninger | Uke 16 | Ikke startet |
| L16 | Godkjent hoved-utkast + peer review (skriftlig tilbakemelding til annen gruppe) | Slutten av april | Ikke startet |

**Fase 4 — Avslutning**

| ID | Leveranse | Frist | Status |
|---|---|---|---|
| L17 | Ferdigstilt rapport (inkl. kode på GitHub) | 31. mai 2026 | Ikke startet |
| L18 | Muntlig eksamen | Tidlig juni 2026 | Ikke startet |

---

### 3.7 Dataplan (L4)

Alle rådata lagres uendret i `004 data/`. All behandling skjer på kopier med dokumenterte transformasjoner i Python-kode. Rådata er gitignored og deles ikke via GitHub.

| Datakilde | Innhold | Tilgjengelighet | Primært bruk |
|---|---|---|---|
| **LEO/BRIS-data 2020–2025 (110 Sør-Vest)** | Hendelsestidsstempler, oppdragstype, varighet, ressursutsendelse | Tilgjengelig | EDA: ankomstrater, skiftbelastning, hendelsestypefordeling; parameterestimering |
| **LEO-data fra høst 2024 (alle sentraler)** | Sammenlignbare hendelsesdata — felles LEO-format | Avklares | Benchmarking og generaliseringsanalyse |
| **DSB årsrapporter 2025** | Bemanning per vakttype, antall operatørplasser, totalt anropsvolum | Offentlig | Benchmarking: modellanbefaling vs. faktisk bemanning |
| **SSB befolkningsdata** | Innbyggertall per sentrals dekningsområde | Offentlig | Predikatoranalyse |
| **ROS- og beredskapsanalyse (110 Sør-Vest)** | Dimensjonerende hendelser, forutsetninger om systemer/rutiner, bemanningsbegrunnelse | Tilgjengelig — forfatteren har tilgang til dokumentene | Kritisk dokumentanalyse: sammenligning med empirisk belastning og kvalitetsvurdering av dimensjoneringsgrunnlag |
| **Strukturerte intervjuer — operativt personell** | Håndteringstid per hendelseskategori, VL-praksis, operative særtrekk | Planlegges uke 12–13 | Parametervalidering; dokumentasjon av særtrekk |
| **Forfatterens egne erfaringer (110 Sør-Vest)** | Operativ praksis, VL-rolle, ring-flom, aktivt hendelsebilde | Tilgjengelig — dokumenteres eksplisitt | Kontekstualisering; validering av modellantagelser |

**Datakvalitetsvurdering og fallback:**
- Dersom LEO-data på tvers av sentraler ikke er tilgjengelig: benchmarking baseres utelukkende på DSB-årsrapporter. Dokumenteres som begrensning.
- Dersom håndteringstid per kategori ikke lar seg estimere fra data: benytt intervjudata som primærkilde. Dokumenteres.
- Dersom Poisson-antagelse forkastes empirisk: vurder alternativ fordeling og begrunn i rapport.

**Rådatahandtering:**
- Rådata lagres i `004 data/` — aldri modifisert direkte
- Alle transformasjoner dokumenteres i Jupyter notebooks med revisjonsspor

---

## 4. Fremdrift

### 4.1 Milepæler

| ID | Milepæl | Frist | Godkjenningskrav | Status |
|---|---|---|---|---|
| M1 | Godkjent proposal | 15. mars 2026 | C-nivå | Innlevert 7. mars — avventer godkjenning |
| M2 | Godkjent prosjektplan + Gantt med referanseplan | **15. mars 2026** | C-nivå | På gang |
| M3 | Rapportskjelett + introduksjon v1 klar | 22. mars 2026 | Intern | Ikke startet |
| M4 | Data innhentet, validert og EDA ferdig | 29. mars 2026 | Intern | Ikke startet |
| M5 | Erlang-C modell implementert og validert | 10. april 2026 | Intern | Ikke startet |
| M6 | Godkjent hoved-utkast + peer review gjennomført | Slutten av april 2026 | C-nivå | Ikke startet |
| M7 | Ferdigstilt rapport innlevert + muntlig eksamen | Rapport: 31. mai / Muntlig: tidlig juni 2026 | **B-krav** | Ikke startet |

> **Kilder:** Forelesning 12. jan og 11. feb 2026.

### 4.2 Avhengighetsdiagram

Kritiske avhengigheter mellom leveranser:

```
L0 (Proposal) → [M1 godkjent]
                      |
              L5 (Plan) + L6 (Gantt) → [M2 godkjent]
                      |
              L7 (Rapportskjelett) ————————→ L12 (Teorikapittel)
              L8 (EDA) → L9 (Param.) → L10 (Erlang-C modell)
                                                  |
                                       L11 (Validering) → L13 (Benchmarking)
                                                                |
                                                    L14 (Generaliseringsanalyse)
                                                                |
                                              L15 (Resultater) → L16 [M6]
                                                                      |
                                                             L17 [M7] + L18
```

**Kritisk sti:** L8 → L9 → L10 → L11 → L13 → L14 → L15 → L16 → L17

### 4.3 Gantt-plan (oversikt)

| Aktivitet | Uke 11 (7–15.3) | Uke 12 (16–22.3) | Uke 13 (23–29.3) | Uke 14 (30.3–5.4) | Uke 15 (6–12.4) | Uke 16 (13–19.4) | Uke 17–18 (20.4–3.5) | Uke 19–22 (4–31.5) |
|---|---|---|---|---|---|---|---|---|
| **L5 Prosjektplan** | ███ | | | | | | | |
| **L6 Gantt (MS Project)** | ███ | | | | | | | |
| **[M2] Plan godkjent** | (M) | | | | | | | |
| **L7 Rapportskjelett + intro v1** | | ███ | | | | | | |
| **L8 Datainnhenting + EDA** | | ███ | ███ | | | | | |
| **L9 Parameterestimering** | | | ███ | | | | | |
| **L10 Erlang-C modellering** | | | | ███ | | | | |
| **L11 Validering og sensitivitet** | | | | ███ | ███ | | | |
| **L12 Teorikapittel** | | | | ███ | ███ | | | |
| **L13 Benchmarking** | | | | | ███ | | | |
| **L14 Generaliseringsanalyse** | | | | | ███ | | | |
| **L15 Resultater + diskusjon** | | | | | | ███ | | |
| **L16 Hoved-utkast + peer review** | | | | | | | ███ | |
| **[M6] Godkjent utkast** | | | | | | | (M) | |
| **L17 Sluttrapport** | | | | | | | | ███ |
| **[M7] Innlevering** | | | | | | | | (M) |

*(M) = milepæl. Detaljert Gantt med aktivitetsnivå og baseline etableres i MS Project — se separat fil.*

**Kapasitetsbudsjett:** 20 timer/uke. Fase 3–4 (uke 12–22, 11 uker): ca. 220 timer tilgjengelig. Buffer innbakt ved at interne milepæler (M3–M5) settes 1–2 uker før kritiske rapportfrister.

### 4.4 Kritisk linje

Kritisk sti: **Datainnhenting/EDA (L8) → Parameterestimering (L9) → Erlang-C modell (L10) → Validering (L11) → Benchmarking (L13) → Resultater (L15) → Sluttrapport (L17)**

Forsinkelse i L8 forplanter seg direkte til alle nedstrømsaktiviteter. Tiltak: prioriter datagjennomgang som første aktivitet i fase 3, senest uke 12.

---

## 5. Risiko

### 5.1 Prosess for risikostyring

Risikoregisteret gjennomgås ukentlig i forbindelse med statusnotatet. Rune Grødem er eneste risikoeier og ansvarlig for alle tiltak.

### 5.2 Risikoregister

| ID | Risiko | Sannsynlighet | Konsekvens | Tiltak | Beredskap |
|---|---|---|---|---|---|
| R1 | LEO/BRIS-datakvalitet utilstrekkelig — manglende felter, feil i registrering | Middels | Høy | Eksplorativ dataanalyse tidlig (uke 12); kartlegg felt og dekningsperiode | DSB-årsrapporter som supplement; dokumenter begrensninger |
| R2 | Erlang-C-forutsetninger brytes empirisk — ikke-Poisson-ankomster | Middels | Middels | Test distribusjon eksplisitt; vurder negativ binomial | Dokumenter avvik og diskuter implikasjonene; bruk simulering som sensitivitetssjekk |
| R3 | Ring-flom (call surge) forstyrrer Poisson-antagelse | Middels | Middels | Identifiser og analyser call-surge-hendelser separat i EDA | Filtrer fra primæranalyse; behandle som eget underkapittel |
| R4 | VL-antagelse holder ikke i praksis | Middels | Lav | Valider via intervjuer med operativt personell | Variabel VL-korreksjonsfaktor; sensitivitetsanalyse på c_effektiv |
| R5 | Benchmarking vanskelig pga. heterogen bemanning og hendelsesvolum | Høy | Middels | Standardiser mot per-innbygger- og per-hendelse-nøkkeltall | Begrens til sammenlignbare størrelsesklasser |
| R6 | Tilgang til tvers-sentraldata (LEO post-2024) avklares ikke | Middels | Middels | Avklar datatilgang tidlig i fase 3 (uke 12) | Fall tilbake på DSB-årsrapporter; omfang reduseres og dokumenteres |
| R7 | Tidskollisjon med vaktarbeid ved 110 Sør-Vest | Høy | Middels | Planlegg skriveokter rundt vaktplan; buffer i Gantt | Komprimere generaliseringsanalysen; prioritere kjernemodell |
| R8 | Prokrastinering — skippertak mot innleveringsfrist | Middels | Høy | Ukentlige statusnotater og LLI-logg; tidlige interne delleveransfrister | Akseptere enklere analyse fremfor å kompromittere rapportkvalitet |
| R9 | Sensitive funn fra ROS-gjennomgang — konklusjoner om svak analysekvalitet kan oppfattes som kritikk av kollegaer eller organisasjon | Middels | Middels | Formuler funn som metodisk vurdering, ikke personkritikk; forankre i faglige standarder | Begrens deling av utkast med berørte parter under arbeidet; anonymiser der relevant |

### 5.3 Ressursindikator (LLI)

Som erstatning for budsjett benyttes **Livsglede- og vilje-til-å-leve-indeks (LLI)** som styringsorientert mål på kognitiv belastning. Indeksen starter på 100 og loggføres i ukentlige statusnotater.

| Hendelse | LLI-endring |
|---|---|
| Datavask og manglende felter i LEO/BRIS | −8 |
| Poisson-forutsetning empirisk forkastet | −10 |
| Vaktplankollisjon kaster bort en planlagt økt | −5 |
| Erlang-C gir tolkbare og meningsfulle resultater | +10 |
| Benchmarking viser tydelig mønster på tvers av sentraler | +8 |
| Rapportkapittel ferdigstilt og vurdert som B-nivå | +10 |

---

## 6. Interessenter

| Navn/Rolle | Organisasjon | Behov / Prioritering | Involvering |
|---|---|---|---|
| Rune Grødem | Student, G20 — 110 Sør-Vest | Bestå emnet med god karakter; produsere analyse relevant for arbeidsgiver | Prosjektleder, utfører alt arbeid |
| Emneansvarlig / veileder | Høgskolen i Molde | Vitenskapelig kvalitet, fremdrift, metodisk ryddighet | Godkjenning av plan og Gantt; veiledning underveis |
| Operativt personell (110 Sør-Vest) | 110 Sør-Vest | Velfunderte bemanningsbeslutninger | Intervju om håndteringstider, kapasitetsgrenser og operative særtrekk |
| DSB / sentralledere | Direktoratet for samfunnssikkerhet og beredskap | Etterprøvbart grunnlag for dimensjoneringsvedtak | Ikke direkte involvert — kan motta rapport |

---

## 7. Ressurser og roller

### 7.1 Prosjektteam

Prosjektet gjennomføres individuelt. Alle roller innehas av Rune Grødem.

| Rolle | Ansvar |
|---|---|
| Prosjektleder | Fremdrift, planoppfølging, Gantt-oppdatering, veilederkontakt |
| Faglig ansvarlig (modell) | Modellvalg, implementasjon i Python, validering og sensitivitetsanalyse |
| Forfatter | Rapportskriving, kildebruk (APA 7th norsk), litterätursøk |
| Dataansvarlig | Datainnsamling, datavask, dokumentasjon av rådatabehandling |
| Feltforsker | Strukturerte intervjuer med operativt personell |

### 7.2 Ressursbelastning

Tilgjengelig tid er 20 timer per uke, begrenset av vaktarbeid ved 110 Sør-Vest. Planlegging tar hensyn til dette med interne buffere i Gantt-diagrammet. Fase 3 (17. mars – 30. april) utgjør hoveddelen av analysearbeidet: ca. 140 timer over 7 uker.

### 7.3 Kritiske ressurser

- **LEO/BRIS-data fra 110 Sør-Vest** — nødvendig for parameterestimering; foreligger, men kvalitet verifiseres i fase 3
- **DSB årsrapporter 2025** — kritisk for benchmarking; offentlig tilgjengelige
- **Tilgang til MS Project** — tilgjengelig via Høgskolen i Molde
- **Veileder** — tidlig avklaring av modellvalg er kritisk for å unngå omstart i fase 3

---

## 8. Kommunikasjon og kvalitet

### 8.1 Kommunikasjonsplan

| Aktivitet | Frekvens | Format | Mottaker |
|---|---|---|---|
| Ukentlig statusnotat | Ukentlig | Kort skriftlig oppsummering — hva er gjort, neste steg, LLI | Eget arkiv / veileder ved behov |
| Veiledermøte | Ved behov / etter avtale | Teams eller oppmøte | Veileder |
| Oppdatering av Gantt (tracking) | Ukentlig | MS Project — avvik mot referanseplan registreres løpende | Re-innleveres ved fase 3-slutt |

### 8.2 Kvalitetsplan

1. **Tidlig rapportskriving** — introduksjon og problemstilling skrives i fase 2/tidlig fase 3, videreføres iterativt
2. **Faglig forankring** — litterätursøk starter tidlig og kobles til modellvalg og metodebegrunnelse
3. **Tydelig rapportstruktur** — skille mellom modell/metode og resultater/diskusjon fra første utkast
4. **Empirisk validering** — Erlang-C-forutsetninger testes eksplisitt; avvik diskuteres åpent
5. **Datahandtering** — rådata lagres uendret, all behandling på kopier med dokumenterte transformasjoner i Jupyter notebooks
6. **Versjonskontroll** — kode versjonskontrolleres på GitHub og refereres som vedlegg i rapporten
7. **Kildebruk** — alle faglige påstander refereres etter APA 7th norsk; primærkilder prioriteres

### 8.3 Peer review

Mot slutten av fase 3 gjennomføres gjensidig **skriftlig** fagfellevurdering med en annen gruppe, tilordnet av emneansvarlig. Peer review er obligatorisk del av arbeidskravet for M6.

---

*Sist oppdatert: 2026-03-07 | Versjon 1.4 | Neste gjennomgang: ved Gantt-godkjenning*
