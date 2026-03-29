# Litteratursøk — LOG650 G20 Rune Grødem
## Bakgrunn og metodeutvikling for ChatGPT-assistert litteratursøk

---

## 1. Hva dette dokumentet er

Dette dokumentet beskriver et pågående masteroppgave-lignende prosjekt (bacheloremne LOG650, Høgskolen i Molde, vår 2026). Formålet er å gi deg (ChatGPT) tilstrekkelig kontekst til å:

1. Vurdere relevansen og kvaliteten på de kildene vi allerede har identifisert
2. Finne **ytterligere relevante akademiske kilder** vi ikke har funnet
3. Særlig søke etter kilder som dekker hull vi har identifisert

---

## 2. Originalcase og problemstilling

### 2.1 Kontekst

110-sentralene er Norges nødmeldesentraler for brann og redning. Det finnes 12 sentraler i Norge. De mottar nødanrop (telefon 110), oppretter hendelser, utalarmeringen brannressurser og koordinerer innsats. Casen er **110 Sør-Vest** (dekker Rogaland og Haugaland, befolkning ca. 340 000), operert av Rogaland brann og redning IKS.

### 2.2 Original problemstilling

> *I hvilken grad samsvarer faktisk bemanning ved norske 110-sentraler med kapasitetsbehovet beregnet fra historiske hendelsesdata og køteoretiske modeller?*

### 2.3 Bakgrunn for problemstillingen

**Dimensjoneringsforskriften** (FOR-2023-01-06-23) gir kvantitative, etterprøvbare bemanningskrav for brannstasjoner basert på innbyggertall og responstid. For eksempel: en S1-stasjon (kasernert, storby) skal ha to biler på vakt, selv om begge sjelden er i bruk simultaneously — fordi konsekvensen av å mangle kapasitet ved samtidige hendelser er uakseptabel.

**Ingen tilsvarende nasjonal standard finnes for 110-operatører.** Bemanningsnivå fastsettes lokalt gjennom kvalitative risiko- og sårbarhetsanalyser (ROS). Minimum er nedfelt i brann- og redningsvesenforskriften (FOR-2021-09-15-2755) § 28–33: minst to operatører per vakt, hvorav én med vaktlederfunksjon. Utover dette er dimensjonering opp til hver sentral.

---

## 3. Faktisk bemanningsstruktur ved 110 Sør-Vest

Dette er kritisk for å forstå modellen:

| Skifttype | Total bemanning | Vaktleder (VL) | Operatører (c_total) | c_effektiv |
|---|---|---|---|---|
| Dag / Hverdag (07–19, man–fre) | 4 | 1 | 3 | **3** |
| Dag / Helg (07–19, lør–søn) | 3 | 1 | 2 | **2** |
| Natt / Hverdag (19–07, man–fre) | 3 | 1 | 2 | **2** |
| Natt / Helg (19–07, lør–søn) | 3 | 1 | 2 | **2** |

**Vaktleder (VL)-antagelsen:** VL besvarer normalt IKKE nødanrop. VL har en separat funksjon: overordnet situasjonsoversikt, prioritering av oppdrag, pressehåndtering, innkalling av ekstra ressurser og administrativt ansvar. Dette er nedfelt i sentralens interne prosedyre (se avsnitt 4). Derfor: c_effektiv = c_total − 1.

**De facto servicegrense:** Det 10. anropet i kø viderekoblet automatisk til nabosentral Agder. Ubesvart anrop etter 60 sekunder = registrert kapasitetsbrudd i henhold til brann- og redningsvesenforskriften § 21.

---

## 4. Operativ arbeidsmetodikk — prosedyren som styrer bemanningsbehovet

Dette er den viktigste enkeltstående faktoren i analysen. 110 Sør-Vest har en formell prosedyre for arbeidsmetodikk og utalarmering (Rogaland brann og redning IKS, versjon 4, 16.12.2024). Prosedyren definerer tre dynamiske roller som roterer mellom operatørene:

### Rolledefinisjon

**RØD funksjon** — den operatøren som besvarer nødtelefonen:
- Oppretter hendelse i LEO (operativt hendelsessystem)
- Gjennomfører intervju med innringer etter nasjonal trippelvarslingsprosedyre
- Logger essensiell informasjon løpende under samtalen
- Binder én operatør *fullt ut* under samtalefasen

**GUL funksjon** — den nærmeste ledige operatøren:
- Utalarmerer ressurser (brannbil, mannskaper) via ICCS-systemet
- Håndterer samband (nødnett) med mannskaper i felt
- Logger skadestedsfaktorer i LEO (problembeskrivelse, situasjonsrapporter)
- Følger hendelsen til den er lukket
- *Kan* håndtere flere gule hendelser parallelt i oppfølgingsfasen

**GRØNN funksjon** — ledig operatør:
- Klar for neste nødanrop
- Tar servicetelefoner og grå linjer i mellomtiden
- Prosedyren fastslår eksplisitt som målsetning: *«én operatør til enhver tid er ledig og kan ta nødtelefoner»*

**Vaktleder (VL):**
- Overordnet funksjon — oversikt, ledelse, prioritering
- Prosedyren fastslår eksplisitt: *«vaktleder skal som et utgangspunkt ikke besvare nødanrop»*

### Normal drift = makkerpar

Standard arbeidsform er at **to operatører samarbeider om én hendelse** (RØD + GUL). De utfyller hverandre: RØD fokuserer på innringer og informasjonsinnhenting, GUL handler umiddelbart på informasjonen og varsler ressurser. Prosedyren understreker at «tiden to operatører er involvert i samme hendelse gjøres så kort som mulig, for å raskt frigjøre kapasitet til neste hendelse».

### Kapasitetsdegrasjon ved simultane hendelser

Prosedyren erkjenner at ved høy aktivitet *må* operatørene håndtere hendelser alene — men dette beskrives eksplisitt som et nødmodus, ikke normalstandard. Sitert fra prosedyren: *«Normal arbeidsmetode vil være at to operatører samarbeider om en hendelse, men når det er mye aktivitet i sentralen, må en operatør allikevel kunne håndtere en hendelse alene.»*

**Det operative problemet beskrevet av operatørene selv:**

Med c_eff = 2 (natt/helg):
- Hendelse 1 ankommer: OP_A = RØD, OP_B = GUL → begge opptatt, null grønne
- Hendelse 2 ankommer: OP_B *må* bryte GUL-rollen og bli RØD på H2
  - OP_A (fremdeles på H1-samtalen) må nå *også* håndtere GUL på H1 alene
  - OP_B håndterer H2 alene (RØD + GUL)
  - **Begge operatørene jobber nå i solo-modus — makkerpar-prinsippet er brutt**
- Hendelse 3 ankommer: VL må bryte vaktlederfunksjon, eller anropet overføres til Agder

Med c_eff = 3 (dag/hverdag):
- Hendelse 1 ankommer: OP_A = RØD, OP_B = GUL, OP_C = GRØNN ✓
- Hendelse 2 ankommer: OP_C = RØD på H2, men ingen dedikert GUL for H2
  - OP_B forsøker å være GUL på begge (H1 og H2) — «etter beste evne»
  - OP_A avslutter samtalen og kan hjelpe som GUL
  - **Makkerpar-prinsippet er brutt for H2 — arbeid «etter beste evne»**
- Hendelse 3 ankommer: Alle tre opptatt — sviktmodus

---

## 5. Datagrunnlag

**Primærdata:** LEO/BRIS 2025, 110 Sør-Vest — 61 964 hendelsesrader, 44 kolonner.

**Nøkkelkolonner tilgjengelig:**
- `Dato anrop`, `Tid anrop` — presis tidsstempel for hvert anrop
- `Opprinnelig oppdragstype` — hendelseskategori (ABA, Brann i bygning, Trafikkulykke, etc.)
- `Oppdragstype` — utfall (Utrykning, Løst av 110, Unødig, etc.)
- `Overordnet oppdragstype` — skille mellom beredskapsoppdrag og T1-servicetelefoner

**Kritisk datakvalitetsproblem:**
- `Operatør-ID`: 0 % dekning — DSB bekrefter at operatøridentitet ikke registreres i BRIS av personvernhensyn
- `Alarmbehandlingstid`: ~12 % dekning (kun noen hendelseskategorier)
- `Innsatsvarighet`: ~9 % dekning (kun utrykningshendelser)

Dette betyr at vi **ikke kan observere bindingstid direkte fra data**. Bindingstid er innhentet gjennom strukturert ekspertintervju med erfaren operatør ved 110 Sør-Vest.

**Oppdragskategorier (2025, 110 Sør-Vest):**
- T1 / «110-oppdrag uten involvering av brannvesen» (servicetelefoner): **54 526 rader (88 %)**
- Beredskapsoppdrag (non-T1): **7 438 rader (12 %)**

---

## 6. Metodisk utvikling — hvordan analysen har dreid

### Fase 1: Erlang-C som primærmodell (opprinnelig plan)

Startet med standard M/M/c (Erlang-C) anvendt på innkommende beredskapsanrop per skifttype.

**Resultater Erlang-C:**

| Skifttype | λ (anrop/t) | c_eff | ρ | P(W > 60s) |
|---|---|---|---|---|
| Dag / Hverdag | 2,57 | 3 | 4,9 % | 0,02 % |
| Dag / Helg | 2,06 | 2 | 5,9 % | 0,38 % |
| Natt / Hverdag | 1,18 | 2 | 3,4 % | 0,13 % |
| Natt / Helg | 1,30 | 2 | 3,7 % | 0,15 % |

**Problem:** Systemutnyttelsen (ρ) er under 6 % i alle scenarier. Erlang-C sier kapasiteten er komfortabel. Men dette stemmer ikke med operatørenes erfaring og hendelsesmønsteret i data.

**Årsak til at Erlang-C er utilstrekkelig:** Modellen antar at én server (operatør) per anrop er tilstrekkelig. Men prosedyren definerer *to* operatører som standard for én hendelse (makkerpar). Erlang-C fanger ikke:
- Kapasitetstapet ved solo-drift
- At aktive hendelser binder operatørkapasitet *utover samtaletid* (GUL-fasen)
- At VL ikke bidrar til anropshåndtering

### Fase 2: Simultanitetetsanalyse (mellomsteg)

Analyserte antall aktive hendelser simultant per minutt (minutt-for-minutt tidsserieanalyse med Anettes bindingstider).

**Funn:** P(≥ 2 simultane) = 0,20 % av alle minutter ≈ 18 timer/år totalt. Konfliktraten virket lav fordi modellen ikke tok høyde for makkerpar-logikken.

### Fase 3: Prosedyrbasert ankomstkonfliktmodell (nåværende modell)

**Metodisk skifte:** Fra «kan noen svare?» til «kan anropet håndteres prosedyrkonformt?»

**Ny modell — ankomstkonfliktdeteksjon:**

For hvert beredskapsanrop som ankommer sentralen, beregnes antall *aktive* hendelser på ankomsttidspunktet (n_aktive). En hendelse er «aktiv» fra ankomsttidspunktet til estimert bindingstid er utløpt. Tre kapasitetsnivåer:

| Nivå | Definisjon | Terskel c=2 | Terskel c=3 |
|---|---|---|---|
| **Normal** | Makkerpar mulig, prosedyrkonform | n = 0 | n = 0 |
| **Brudd på arbeidsmetodikk** | Nytt anrop uten ledig makker. Operatørene jobber «etter beste evne». | n ≥ 1 | n ≥ 1 |
| **Svikt** | VL må bryte vaktlederfunksjon ELLER anrop til Agder | n ≥ 2 | n ≥ 3 |

**Viktig distinksjon:**
- c_eff = 3, n = 1: Det ER noen som kan svare (GRØNN-operatøren), men vedkommende får ingen dedikert makker fordi begge andre allerede er RØD+GUL på H1. Brudd på makkerpar-prinsippet.
- c_eff = 2, n = 1: Begge operatørene er RØD+GUL på H1. Det er *ingen* igjen til å ta H2 uten at noen bryter sin pågående rolle.

**Bindingstidsestimater (kvalitativt innhentet, sensitivitetstestet):**

| Scenario | ABA / enkle | Brann, trafikk, redning |
|---|---|---|
| Optimistisk | 5 min | 10 min |
| Basis | 10 min | 15 min |
| Konservativ | 12 min | 20 min |

---

## 7. Nøkkelresultater fra nåværende modell (basis: 10/15 min)

**Tabell: Kapasitetsnivå ved ankomst av beredskapsanrop — 110 Sør-Vest 2025**

| Skifttype | Anrop | Normal | Brudd på AML | Svikt | c_eff |
|---|---|---|---|---|---|
| Dag / Hverdag | 3 382 | 79,4 % | 20,2 % | 0,35 % | 3 |
| Dag / Helg | 1 236 | 78,5 % | 17,1 % | 4,45 % | 2 |
| Natt / Hverdag | 1 934 | 86,5 % | 12,6 % | 0,98 % | 2 |
| Natt / Helg | 886 | 80,8 % | 14,6 % | 4,63 % | 2 |

**Det strukturelle gapet (det viktigste funnet):**

| | Hverdag dagskift | Helg dagskift |
|---|---|---|
| Beredskapsanrop per dag | 13,0 | 11,9 (91 % av hverdag) |
| c_eff | 3 | 2 |
| Sviktrate | 0,35 % | **4,45 % (12,7× høyere)** |
| Absolutt: svikt-hendelser/år | 12 | **55** |

- Beredskapsvolum er tilnærmet likt mellom hverdag og helg (dagskift)
- Helg natt har faktisk *høyere* volum enn hverdag natt (8,5 vs 7,4 anrop/dag)
- Likevel er bemanning lavere på helg
- Bemanningsreduksjonen er historisk begrunnet i lavere T1-servicetelefoner — ikke i lavere beredskapsbelastning

**Sensitivitet:** Alle tre bindingstidsscenarier gir samme strukturelle konklusjon. Rangeringen av skifttyper og helg/hverdag-gapet er robust.

**Effekt av c_eff = 3 på helg dagskift (hypotetisk):**
- Svikt reduseres fra 55 til 21 hendelser/år (−62 %)
- Bringer sviktraten ned fra 4,45 % til 1,70 % — tilnærmet hverdag-nivå

---

## 8. Hva vi egentlig måler — presist

Analysen måler **P(prosedyrbrudd ved ankomst)**: sannsynligheten for at et beredskapsanrop ankommer sentralen i en tilstand der makkerpar-prinsippet ikke kan opprettholdes.

Dette er *ikke* det samme som:
- P(ingen svarer) — noen svarer nesten alltid
- P(W > t) i klassisk Erlang-C forstand — det er sjelden kø i tradisjonell forstand
- P(kapasitetssystemet kollapser) — det kollapser sjelden totalt

Det er en prosedyrkonformitetsmetrikk forankret i operasjonell virkelighet: **i hvilken andel av beredskapsanropene er de operative forutsetningene for korrekt hendelseshåndtering til stede?**

**Analogien til dimensjoneringsforskriften for brannvesen:**
- S1-stasjon (stor by) har to biler selv om begge sjelden brukes simultant
- Dimensjonering skjer for *beredskapstopper*, ikke for gjennomsnittlig belastning
- Konsekvensen av utilstrekkelig kapasitet ved kritiske hendelser er uakseptabel
- Samme logikk: 110-bemanning bør dimensjoneres ut fra beredskapsbelastning, ikke ut fra servicetelefon-volum

---

## 9. Sentrale begreper for litteratursøk

For å hjelpe deg å finne relevante kilder, her er de viktigste fagbegrepene og konseptene i analysen:

**Operative begreper:**
- Public Safety Answering Point (PSAP) — norsk: nødmeldesentral
- Emergency Communications Center (ECC)
- 110-sentral / brann-dispatch / fire dispatch
- Call taker / dispatcher (to forskjellige roller i USA, kombinert i Norge)
- Workload, cognitive load, multitasking
- Simultaneous incidents / concurrent incidents
- Paired dispatcher workflow / team-based dispatch
- Work methodology / standard operating procedure (SOP)

**Modelleringsbegreper:**
- Erlang-C / M/M/c queue
- Erlang-A / M/M/c+G (impatient customers)
- Arrival conflict / service availability
- Staffing level / capacity planning
- Service degradation / degraded mode
- Concurrent call handling
- Active incident binding (hendelse binder kapasitet etter anropsavslutning)

**Organisatoriske begreper:**
- Shift staffing / roster planning
- Weekday vs. weekend staffing differential
- Watch commander / supervisor role (analogt med VL)
- Reserve capacity / beredskapskapasitet

---

## 10. Litteratur vi allerede har funnet — be om vurdering og tillegg

Under følger kildene vi har identifisert. Vi ber deg:
1. **Vurdere hver kildes faktiske relevans** for vår spesifikke analyse
2. **Flagge eventuelle feil** (feil tittel, år, forfatter, DOI)
3. **Foreslå ytterligere litteratur** vi bør inkludere — særlig innen:
   - Prosedyrkonformitet og kapasitetsmodellering i operative systemer
   - Kognitiv belastning ved simultane hendelser i dispatch-kontekst
   - Team-basert servicesystem-modellering (to servere per kunde)
   - Nordisk nødmeldetjeneste-forskning
   - Bemanningsdimensjonering i sikkerhets-kritiske systemer generelt

### 10.1 Erlang-C og call center-kapasitetsmodellering

- Gans, N., Koole, G. & Mandelbaum, A. (2003). *Telephone Call Centers: Tutorial, Review, and Research Prospects.* Manufacturing & Service Operations Management, 5(2), 79–141. DOI: 10.1287/msom.5.2.79.16071

- Koole, G. & Mandelbaum, A. (2002). *Queueing Models of Call Centers: An Introduction.* Annals of Operations Research, 113(1–4), 41–59. DOI: 10.1023/A:1020949626017

- Aksin, Z., Armony, M. & Mehrotra, V. (2007). *The Modern Call Center: A Multi-Disciplinary Perspective on Operations Management Research.* Production and Operations Management, 16(6), 665–688. DOI: 10.1111/j.1937-5956.2007.tb00288.x

- Robbins, T. R. & Harrison, T. P. (u.å.). *Evaluating the Erlang C and Erlang A Models for Call Center Modeling.* Working paper, East Carolina University.

### 10.2 Tidsavhengig etterspørsel og skiftbasert bemanningsplanlegging

- Green, L. V., Kolesar, P. J. & Whitt, W. (2007). *Coping with Time-Varying Demand When Setting Staffing Requirements for a Service System.* Production and Operations Management, 16(1), 13–39. DOI: 10.1111/j.1937-5956.2007.tb00164.x

- Whitt, W. (1996). *Server Staffing to Meet Time-Varying Demand.* Management Science, 42(10), 1383–1394. DOI: 10.1287/mnsc.42.10.1383

- Stolletz, R. (2008). *Approximation of the Non-Stationary M(t)/M(t)/c(t)-Queue Using Stationary Queueing Models.* European Journal of Operational Research, 190(2), 478–493.

- Feldman, Z., Mandelbaum, A., Massey, W. & Whitt, W. (2008). *Staffing of Time-Varying Queues to Achieve Time-Stable Performance.* Management Science, 54(2), 324–338. DOI: 10.1287/mnsc.1070.0821

### 10.3 Erlang-A og frafall / 60-sekunders-regelen

- Garnett, O., Mandelbaum, A. & Reiman, M. (2002). *Designing a Call Center with Impatient Customers.* Manufacturing & Service Operations Management, 4(3), 208–227. DOI: 10.1287/msom.4.3.208.7753

- Mandelbaum, A. & Zeltyn, S. (2005). *Call Centers with Impatient Customers: Many-Server Asymptotics of the M/M/n+G Queue.* Queueing Systems, 51(3–4), 361–402. DOI: 10.1007/s11134-005-3699-8

### 10.4 Nødmeldesentraler og dispatch — forskning og praksis

- Gardett, I. & Clawson, J. J. (2013). *Past, Present, and Future of Emergency Dispatch Research: A Systematic Literature Review.* Annals of Emergency Dispatch & Response, 1(2).

- Mukhopadhyay, A. et al. (2022). *A Review of Incident Prediction, Resource Allocation, and Dispatch Models for Emergency Management.* Accident Analysis & Prevention, 165, artikkel 106501. DOI: 10.1016/j.aap.2021.106501

- Ohio Auditor of State (2025). *Washington County 911 Dispatch Feasibility Study.* Ohio Auditor Performance Audit.

- APCO International (2005). *Staffing and Retention in Public Safety Communication Centers — Project RETAINS Effective Practices Guide.*

- NENA (2003). *PSAP Staffing Guidelines Report and Staffing Worksheet.* NENA-REF-001-2003.

### 10.5 Team-basert service og VL-rollen

- Jouini, O., Dallery, Y. & Nait-Abdallah, R. (2008). *Analysis of the Impact of Team-Based Organizations in Call Center Management.* Management Science, 54(2), 400–414. DOI: 10.1287/mnsc.1070.0792

- Kim, C., Lee, M., Dudin, A. & Klimenok, V. (2008). *Multi-Server Queueing Systems with Cooperation of the Servers.* Annals of Operations Research, 162(1), 57–68. DOI: 10.1007/s10479-008-0319-0

### 10.6 Kognitiv belastning og simultane hendelser

- Al-Sarhani, M. et al. (2025). *Dispatch under Pressure: An Investigation into the Cognitive Load of Kuwait's Emergency Responders.* International Journal of Disaster Risk Reduction. DOI: 10.1016/j.ijdrr.2025...

- Simplesense / Draper Laboratory (2020). *Quantifying Cognitive Load of Emergency Dispatchers.* Annals of Emergency Dispatch & Response.

- Simplesense (2023/2024). *Cognitive Workload for Dispatchers Remains at Dangerous Levels.* Industry report.

### 10.7 Nordisk og norsk nødmeldeforskning

- Zakariassen, E. et al. (2019). *Exploring Individual and Work Organizational Peculiarities of Working in Emergency Medical Communication Centers in Norway — A Qualitative Study.* BMC Health Services Research, 19, artikkel 553. DOI: 10.1186/s12913-019-4370-0

- Ellensen, E. N. et al. (2022/2023). *Swedish Emergency Medical Dispatch Centres' Ability to Answer Emergency Medical Calls.* Resuscitation, 189, artikkel 109875. DOI: 10.1016/j.resuscitation.2023.109875

- McNamee, M. et al. (2023). *FIRE21 — Final Report: Nordic Fire and Rescue Services, Problem-Solving in the 21st Century.* Lund University / NordForsk.

- Rehn, M. et al. (2021). *Dispatch Accuracy of Physician-Staffed Emergency Medical Services in Trauma Care in South-East Norway.* Scandinavian Journal of Trauma, Resuscitation and Emergency Medicine, 29, artikkel 163. DOI: 10.1186/s13049-021-00982-3

### 10.8 Operative nødtjeneste-modeller (hypercube, multi-enhet)

- Larson, R. C. (1974). *A Hypercube Queuing Model for Facility Location and Redistricting in Urban Emergency Services.* Computers & Operations Research, 1(1), 67–95.

- Chelst, K. R. & Barlach, Z. (1981). *Multiple Unit Dispatches in Emergency Services: Models to Estimate System Performance.* Management Science, 27(12), 1390–1409. DOI: 10.1287/mnsc.27.12.1390

### 10.9 Norsk regulering

- Direktoratet for samfunnssikkerhet og beredskap — DSB (2021). *Forskrift om organisering, bemanning og utrustning av brann- og redningsvesen og nødmeldesentralene (brann- og redningsvesenforskriften).* FOR-2021-09-15-2755. Ikrafttredelse 1. mars 2022.

- Direktoratet for samfunnssikkerhet og beredskap — DSB (2023). *Forskrift om organisering og dimensjonering av brannvesen (dimensjoneringsforskriften).* FOR-2023-01-06-23.

---

## 11. Spesifikke litteraturgap vi ber deg søke etter

Vi har identifisert følgende gap som vi *ikke* finner dekning på i eksisterende litteratur:

### Gap 1: Prosedyrkonformitet som kapasitetsmetrikk
Vi måler ikke bare «kan noen svare?» men «kan anropet håndteres etter prosedyre?» — dvs. med makkerpar. Finnes det litteratur på:
- Prosedyrkonformitet som kapasitetsmål i operative systemer?
- «Degraded mode operations» i sikkerhets-kritiske servicetjenester?
- SOP compliance under høy belastning?

### Gap 2: To-server-per-kunde servicekrav (makkerpar)
Standard Erlang-C antar én server per kunde. Vi har et system der *to* servere normalt betjener én kunde simultant. Finnes det:
- Kømodeller der minimumskravet er k servere per kunde (k>1)?
- Modeller for «cooperative service» der to agenter jobber parallelt på én oppgave?
- «Dual-dispatch» modeller i nødtjenestekontekst?

### Gap 3: Kapasitetsbinding utover samtaletid (GUL-fasen)
Etter at samtalen er avsluttet (RØD-fasen over), er operatøren fremdeles bundet i GUL-funksjon: utalarmering, samband, logging. Dette er ikke samtaletid, men det er ikke ledig kapasitet heller. Finnes det:
- Modeller for «post-call work» / «after-call work» i nødmeldesammenheng?
- Modeller der server-binding deles i to faser (aktiv fase + etterarbeid)?
- Dokumentasjon av at «service time» i brann-dispatch inkluderer koordineringsarbeid etter telefonsamtalen?

### Gap 4: Bemanningsdifferensiering hverdag/helg uten empirisk beredskapsgrunnlag
Vi dokumenterer at helgebemanning er lavere enn hverdagsbemanning til tross for at beredskapsvolum er tilnærmet identisk. Finnes det:
- Studier som kritiserer servicetelefon-volumbasert bemanningsdimensjonering i nødetaten?
- Forskning på uintenderte konsekvenser av bemanningsreduksjon på lavtrafikk-perioder i beredskapsorganisasjoner?
- Analogier fra andre sektorer (f.eks. sykehus, lufttrafikkkontroll) der «stille perioder» faktisk er høyrisikoperioder?

### Gap 5: Nordisk / skandinavisk 110-forskning
Vi finner nesten ingen studier på norske eller nordiske 110-brann-sentraler spesifikt. Be om grundig søk på:
- DSBs egne analyser og rapporter om 110-kapasitet
- KOKOMs (Nasjonalt kompetansesenter for helsetjenestens kommunikasjonsberedskap) rapporter om nødmeldetjeneste
- Norsk senter for forskningsdata (NSD) / norske masteroppgaver om 110 eller AMK-dimensjonering
- Svenske og danske tilsvarende studier (SOS Alarm, AMK-tilsvarende)

---

## 12. Oppsummering — hva vi trenger fra deg

1. **Vurder** kildene i avsnitt 10 — er de relevante og korrekte?
2. **Finn ytterligere litteratur** som dekker gap 1–5 i avsnitt 11
3. **Prioriter** funnene etter relevans for vår spesifikke ankomstkonflikt-modell
4. **Merk** spesielt om du finner noe om:
   - Team-basert / makkerpar-dispatch som standard operasjonsprosedyre
   - Bemanningsdimensjonering for *beredskap* (worst-case) vs. gjennomsnittlig belastning
   - «Degraded mode» i nødmeldesentraler under høy belastning
   - Kvantitative mål på prosedyrkonformitet i sikkerhets-kritiske operasjoner

Bruk gjerne Google Scholar, Scopus, PubMed, ResearchGate og andre akademiske databaser. Rapporter fra DSB, KOKOM, Riksrevisjonen og Direktoratet for e-helse er også relevante.
