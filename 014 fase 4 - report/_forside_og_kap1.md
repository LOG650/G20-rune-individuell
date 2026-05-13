---
title: "Kapasitetsstyring og bemanningsdimensjonering ved norske 110-sentraler"
subtitle: "En analyse av operatørkapasitet med prosedyrbasert ankomstkonfliktmodell"
author: "Rune Grødem · G20 Individuell"
date: "LOG650 — Logistikk og kunstig intelligens · Høgskolen i Molde · Vår 2026 · Innlevert 31. mai 2026 · Veileder: [Veileder — fylles inn ved innlevering] · Antall ord: ca. 19 700 (kap. 1–9, eksklusive tabeller, kode og litteraturliste)"
abstract: |
  Norske 110-sentraler er kritisk beredskapsinfrastruktur som mottar nødmeldinger og koordinerer brann- og redningsinnsats. Bemanningsnivået fastsettes lokalt gjennom risiko- og beredskapsanalyser (ROS), men det finnes ingen nasjonal, kvantitativ standard for hvordan operativ belastning oversettes til konkret bemanning utover minimumskravet. Hovedanalysen i rapporten er en casestudie av 110 Sør-Vest; den nasjonale delen brukes som benchmarking og generaliseringsgrunnlag.

  Denne rapporten analyserer i hvilken grad faktisk bemanning ved 110 Sør-Vest (primærcase) samsvarer med kapasitetsbehovet beregnet fra historiske hendelsesdata. En innledende Erlang-C-analyse (M/M/c) viste svært lav systemutnyttelse (høyeste observerte verdi 5,9 %) for alle skifttyper — et resultat som er formelt korrekt, men metodisk utilstrekkelig fordi modellen ikke fanger at sentralens operative prosedyre (makkerpar-drift) krever to operatører parallelt per pri-1-hendelse. Studiens hovedmodell er derfor en **prosedyrbasert ankomstkonfliktmodell** med op-binder-semantikk, som måler sannsynligheten for at et beredskapsanrop ankommer i en tilstand der makkerpar-driftsstandarden ikke kan opprettholdes. Modellen skiller eksplisitt mellom D-pri1 (pri-1-utrykning, makkerpar) og D-aba (ABA-utrykning, serielt).

  Hovedfunnene for 110 Sør-Vest 2025 viser at **32,6 % av beredskapsanropene på natt/helg ankommer i svikt-tilstand** (variant A, beredskapsbelastning), stigende til 33,2 % ved inkludering av total operativ belastning (variant B). Over halvparten av beredskapsanropene på natt/helg ankommer i brudd eller svikt. En scenarioanalyse viser at én ekstra operatør på natt/helg reduserer sviktraten fra ca. 33 % til 16,7 %. Resultatene er benchmarket mot nasjonalt datagrunnlag (DSB BRIS 2025, 508 228 registrerte henvendelser i form av oppdrag, alle 12 sentraler — faktisk anropsvolum er høyere som følge av sammenstilling, jf. kap 6.2). L-aba-bindingstid er empirisk kalibrert via en to-trinns dybdeanalyse (n=100 i runde 2, mean 4,53 min). Studien fremstår som en av de første kvantitative kapasitetsanalysene av en norsk 110-sentral basert på historiske hendelsesdata, og foreslår en V3-klassifiseringsregel (D-pri1/D-aba/L-aba med Kilde=Alarm-krav) som forutsetning for sammenlignbar nasjonal benchmarking.

  **Nøkkelord:** 110-sentral · bemanningsdimensjonering · prosedyrbasert kapasitetsmodell · ankomstkonflikt · op-binder-semantikk · makkerpar · D-pri1 · D-aba · Erlang-C · køteori · LEO/BRIS · beredskap.
---

\newpage

## 1. Innledning

### 1.1 Bakgrunn og tema

Norske 110-sentraler er det primære kontaktpunktet for brann- og redningsnødmeldinger i Norge. De tolv sentralene opererer døgnet rundt og koordinerer utrykningsressurser over store geografiske områder. I 2025 håndterte de samlet 508 228 registrerte oppdrag (DSB, 2025). Tallet refererer til oppdrag i BRIS — faktisk anropsvolum er høyere fordi tilleggsanrop til samme hendelse rutinemessig sammenstilles i ett oppdrag (se kap 6.2).

Bemanningen av 110-operatører reguleres av brann- og redningsvesenforskriften. Forskriften pålegger minimum to operatører i vaktrommet. Fastsettelsen av bemanning utover dette overlates til lokale risiko- og beredskapsanalyser (ROS). Samme forskrift inneholder konkrete kvantitative krav til brann- og redningsvesenets organisering, beredskap, bemanning og innsatstid. En tilsvarende kvantitativ, nasjonal standard for 110-bemanning mangler.

Problemstillingen er ikke at 110-sentraler generelt er over- eller underbemannet. Den er at det ikke finnes et kvantitativt, etterprøvbart grunnlag for å avgjøre hva som er tilstrekkelig bemanning ved en gitt sentral. Konsekvensene drøftes i kap 8.

### 1.2 Tidligere forskning og kunnskapsgap

Klassisk køteori for telefonsystemer (Erlang, 1917; Gans et al., 2003) og kvalitetsdrevet bemanning (Halfin & Whitt, 1981; Garnett et al., 2002) er velprøvde rammeverk i kommersielle call-sentre. De er sjeldnere anvendt på nødmeldesentraler med makkerpar-prosedyre, aktivt hendelsebilde utover samtaletid og overløpsmekanismer.

Internasjonal forskning som dekker disse særtrekkene finnes. Chelst og Barlach (1981) og Harchol-Balter (2022) gir flerserver-rammeverk der jobber krever flere servere samtidig. Gustavsson (2018), L'Ecuyer et al. (2018) og Dwars (2013) har anvendt stokastiske modeller på nordiske og europeiske nødmeldesentraler. Van Buuren et al. (2017) viser at funksjonsdifferensiering kan forbedre kapasitet uten bemanningsøkning. Forskning på kognitiv belastning (Al-Sarhani et al., 2025; Leonardsen et al., 2021) dokumenterer at operatørenes arbeidsmønster avviker vesentlig fra det klassiske kømodeller forutsetter.

Norsk forskning på 110-sentralenes kapasitet er derimot svært begrenset. Leonardsen et al. (2021) gir kvalitative funn fra AMK-sentraler. Samdal et al. (2021) analyserer dispatch-nøyaktighet for ambulanser. Etter litteratursøket i denne studien (kap 2) er det ikke funnet publiserte kvantitative kapasitetsanalyser av norske 110-sentraler basert på historiske hendelsesdata.

Kunnskapsgapet er dermed konkret: **det finnes ingen kjent kvantitativ, etterprøvbar analyse av 110-kapasitet som fanger makkerpar-bindingen, skiller ulike hendelsesdynamikker, og kan anvendes systematisk på tvers av sentralene i Norge.** Eksisterende ROS- og beredskapsanalyser er kvalitative og ikke sammenlignbare på tvers. Denne studien søker å bidra til å fylle dette gapet for én sentral, og å vurdere om rammeverket kan overføres til andre.

### 1.3 Problemstilling

**I hvilken grad samsvarer faktisk bemanning ved 110 Sør-Vest med kapasitetsbehovet beregnet fra historiske hendelsesdata og køteoretiske modeller, og hva indikerer funnene om overførbarhet til norske 110-sentraler?**

Spørsmålet undersøkes fordi fraværet av en kvantitativ dimensjoneringsstandard gjør dagens lokale bemanningsvurderinger vanskelige å etterprøve på tvers av sentraler.

Problemstillingen er todelt. Den krever (i) en operasjonalisering av begrepet *kapasitetsbehov* som er relevant for 110-driftens prosedyrekrav, og (ii) en empirisk vurdering av hvor godt faktisk bemanning matcher dette behovet. Erlang-C danner grunnlinjen, men viser seg utilstrekkelig i denne konteksten (jf. kap 6). Studien utvikler derfor en prosedyrbasert variant — den prosedyrbaserte ankomstkonfliktmodellen — som måler operativ kapasitet ved hvert beredskapsanrops ankomsttidspunkt.

Forskningsspørsmålene under operasjonaliserer problemstillingen. RQ1–RQ2 etablerer det empiriske grunnlaget (ankomstrate og kapasitetsbinding). RQ3 måler kapasitetsgapet mot prosedyrstandarden. RQ4 sammenligner mot dagens kvalitative dimensjoneringsgrunnlag. RQ5 prøver overførbarheten til en nasjonal dimensjoneringslogikk.

- **RQ1:** Hva er ankomstraten (λ) til 110 Sør-Vest per skiftperiode, og hvilke belastningsmønstre fremgår av historiske LEO/BRIS-data?
- **RQ2:** Hva er gjennomsnittlig håndteringstid (μ⁻¹) per hendelseskategori, og i hvilken grad binder aktivt hendelsebilde operatørkapasitet utover samtaletid?
- **RQ3:** I hvilken andel av beredskapsanropene ved 110 Sør-Vest ankommer anropet i en tilstand der sentralens operative driftsstandard (makkerpar) ikke kan opprettholdes — og hva er det strukturelle kapasitetsgapet mellom hverdag og helg?
- **RQ4:** I hvilken grad gir eksisterende ROS- og beredskapsanalyse for 110 Sør-Vest et tilstrekkelig metodisk grunnlag for å begrunne faktisk bemanning?
- **RQ5:** Hvilke strukturelle forhold i nasjonalt DSB-grunnlag (hendelsesvolum, innbyggertall, areal og klassifiseringspraksis) kan inngå i en framtidig generaliserbar dimensjoneringsmodell på tvers av norske 110-sentraler?

### 1.4 Sentrale begreper og notasjon

Modellen og rapporten bygger på en spesifikk nomenklatur som introduseres formelt i kap 3 og 6, men brukes gjennomgående fra kap 4. Tabellene under gir minimumsdefinisjoner for leseren. Kategoritabellen i 1.4.1 dekker hendelseskategoriene og modellens kjernebegreper. Forkortelsestabellen i 1.4.2 dekker tekniske termer og systemnavn som brukes gjennom hele rapporten.

#### 1.4.1 Modellens kategorier og kjernebegreper

| Begrep | Kort definisjon |
|---|---|
| **D-pri1** | Pri-1-utrykning (bygningsbrann, trafikkulykke, farlig gods). Krever makkerpar — to operatører bundet parallelt under akuttfasen. |
| **D-aba** | ABA-utrykning (automatisk brannalarm). Håndteres serielt av én operatør; valgfri Fase 2 (nødtelefon/panel-veiledning) med sannsynlighet $p$. |
| **L-aba** | ABA-hendelse uten utrykning, men med Kilde=Alarm. Egen kategori for å skille reelle alarmhendelser fra øvrige korte oppdrag. |
| **L-hendelse / L-ukjent** | Korte oppdrag uten initiell hendelsestype eller uten registrert klassifisering. |
| **S / F / V** | Service (overføringstester), feilringing, viderevarsling. Bakgrunnsbelastning som ikke inngår i variant A, men i variant B. |
| **Op-binder** | Tidsavgrenset binding av $q \in \{1, 2\}$ operatører fra et tidspunkt $t$ i $d$ minutter. Hver hendelse ekspanderes til ett eller flere op-binder-events. |
| **Kilde=Alarm-krav** | V3-regel: L-aba og D-aba krever at oppdragets Kilde-felt er «Alarm» — sikrer at ABA-kategoriene ikke forurenses av telefonhenvendelser feilklassifisert som ABA. |
| **c_eff** | Effektiv operatørkapasitet $= c_{\text{total}} - 1$ (vaktleder besvarer normalt ikke nødanrop). |
| **Normal / Brudd / Svikt** | Kapasitetsnivåer ved ankomst av nytt beredskapsanrop. Normal = makkerpar mulig (ledige ≥ 2). Brudd = solo-håndtering mulig (ledige = 1). Svikt = ingen ledig operatør (ledige ≤ 0). |
| **Variant A / Variant B** | A: beredskapsbelastning (D-pri1, D-aba, skjulte anrop). B: total operativ belastning (alle kategorier inklusive S, L-aba, L-hendelse, L-ukjent, F, V). |
| **Scenariobånd (lav/hoved/høy)** | Tre parametersett som spenner usikkerheten i ikke-empiriske antagelser. Hovedscenario gir punktestimat; lav/høy gir bånd. Brukt for å indikere usikkerhet ved resultatene. |

#### 1.4.2 Forkortelser

| Forkortelse | Forklaring |
|---|---|
| **ABA** | Automatisk brannalarm — alarm utløst av røyk-/varmedetektor i bygg, mottatt elektronisk hos 110. |
| **AMK** | Akuttmedisinsk kommunikasjonssentral — helsesektorens 113-sentral (analog til 110 for brann). |
| **BRIS** | Brannvesenets innrapporteringsløsning — DSBs nasjonale registrerings- og statistikksystem for hendelser. |
| **DSB** | Direktoratet for samfunnssikkerhet og beredskap — fagdirektorat for brann- og redningsvesenet i Norge. |
| **EMS** | Emergency Medical Services — internasjonal terminologi for prehospitalt helsevesen (analog til norsk AMK). |
| **GUL** | Operativ funksjon: medlytt og utalarmering. Bundet parallelt med RØD under akuttfasen. |
| **GRØNN** | Operativ funksjon: ledig, klar for neste nødanrop. |
| **ISM** | Integrated Status Monitoring (eller tilsvarende alarmmottakssystem) — brukes ved enkelte sentraler i stedet for konvensjonell ABA-rute. |
| **LABA** | Logging og analyse av alarm- og bindingsdata — intern dybdeanalyse av L-aba-hendelser (kap 5.4). |
| **LEO** | Felles oppdragshåndteringssystem for 110-sentralene fra høst 2024. |
| **M/M/c** | Standard køteoretisk modell: Markov-ankomst, Markov-service, c parallelle servere (Erlang-C). |
| **MOB** | Melding Om Brannvesen — DSBs årlige rapportering av bemanning og struktur fra hver sentral. |
| **MSJ** | Multiserver-Job — køteoretisk rammeverk der hver jobb krever flere servere samtidig (Harchol-Balter, 2022). |
| **NENA** | National Emergency Number Association (USA) — standardiseringsorganisasjon for 9-1-1-sentraler. |
| **PSAP** | Public Safety Answering Point — amerikansk betegnelse for 110-, 112- eller 911-mottakssentral. |
| **QED-regime** | Quality-and-Efficiency-Driven regime — Halfin-Whitt-asymptotikk for store servicesystemer der både kvalitet og effektivitet kan oppnås. |
| **RØD** | Operativ funksjon: besvarer nødanropet og gjennomfører intervju. Hovedansvarlig under akuttfasen. |
| **ROS** | Risiko- og sårbarhetsanalyse — kvalitativ analyse som ligger til grunn for lokal bemanningsfastsettelse utover forskriftens minimum. |
| **SSB** | Statistisk sentralbyrå — nasjonal kilde for befolknings- og strukturdata brukt i benchmarking. |
| **V3** | Tredje generasjon klassifiseringsregel utviklet i denne studien. Definerer D-pri1, D-aba og L-aba med Kilde=Alarm-krav (kap 5.3.2). |
| **VL** | Vaktleder — operativ leder per vakt. Besvarer som hovedregel ikke nødanrop, derav $c_{\text{eff}} = c_{\text{total}} - 1$. |

### 1.5 Avgrensninger

Prosjektet avgrenses til følgende områder:

- **Vaktromsbemanning ved 110-sentral.** Ressursdisponering i brannvesenet, taktisk hendelseshåndtering og organisatoriske beslutninger utover sentralen ligger utenfor scope.
- **Retrospektiv og planleggingsrettet analyse.** Modellen er et beslutningsverktøy for kapasitetsvurdering, ikke et sanntidssystem for operativ styring.
- **Primærcase 110 Sør-Vest 2025.** Hovedmodellen er kjørt på denne ene sentralen. Den nasjonale delen (kap 7.9 og 8.4.1) er benchmarking og kontekst — ikke full prosedyrbasert modellering for de øvrige 11 sentralene.
- **Ordinære driftsforhold.** Ekstraordinære hendelser som langvarige storbranner og katastrofescenarier holdes utenfor modellens gyldighetsområde. De drøftes i diskusjonskapittelet som grenser for modellens anvendbarhet.
- **Ring-flom som kontekst.** Call surge belyses som operativ ekstrembelastning, men modelleres ikke som primærscenario.

Disse avgrensningene er valgt fordi de definerer det området hvor data, prosedyrekunnskap og analytisk rammeverk er konsistent nok til å gi etterprøvbare resultater. Begrunnelsen er ikke tidsmangel, men metodisk avgrensning.

### 1.6 Rapportens struktur

Rapporten består av ni kapitler.

**Kapittel 2** gjennomgår relevant litteratur strukturert etter fem tematiske områder: klassisk køteori, nødmeldesentraler, team-basert kapasitet og prosedyrkonformitet, nordisk nødmeldeforskning, og dimensjoneringsregulering.

**Kapittel 3** etablerer det teoretiske rammeverket. Erlang-C presenteres som grunnlinje, QED-regimet som regimekarakteristikk, og multiserver-jobs som rammeverk for op-binder-semantikk.

**Kapittel 4** beskriver 110 Sør-Vest som case. Bemanning, arbeidsmetodikk og operative særtrekk dokumenteres.

**Kapittel 5** presenterer metode og data, inkludert V3-klassifiseringsregelen og LABA-dybdeanalysen.

**Kapittel 6** utvikler kapasitetsmodellen gjennom tre faser: Erlang-C, simultanitetsanalyse og prosedyrbasert ankomstkonfliktmodell.

**Kapittel 7** presenterer analyseresultater for 110 Sør-Vest 2025. Scenario +1 operatør og variant A/B inngår.

**Kapittel 8** diskuterer funnene mot problemstilling, teori og begrensninger.

**Kapittel 9** besvarer problemstillingen og gir anbefalinger for dimensjonering og videre forskning.