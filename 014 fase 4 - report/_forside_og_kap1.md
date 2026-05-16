---
title: "Kapasitetsstyring og bemanningsdimensjonering ved norske 110-sentraler"
subtitle: "En analyse av operatørkapasitet med prosedyrbasert ankomstkonfliktmodell"
author: "Rune Grødem · G20 Individuell"
date: "LOG650 Logistikk og kunstig intelligens · Høgskolen i Molde · Vår 2026 · Innlevert 31. mai 2026 · Veileder: Bård Inge Austigard Pettersen · Antall ord: ca. 19 700 (kap. 1 til 10, eksklusive tabeller, kode og litteraturliste)"
---

\newpage

## Obligatorisk egenerklæring

Den enkelte student er selv ansvarlig for å sette seg inn i hva som er lovlige hjelpemidler, retningslinjer for bruk av disse og regler om kildebruk. Erklæringen skal bevisstgjøre studentene på deres ansvar og hvilke konsekvenser fusk kan medføre. Manglende erklæring fritar ikke studentene fra sitt ansvar.

| # | Erklæring | Bekreftet |
|---|---|:---:|
| 1 | Jeg erklærer herved at min besvarelse er mitt eget arbeid, og at jeg ikke har brukt andre kilder eller har mottatt annen hjelp enn det som er nevnt i besvarelsen. | ☒ |
| 2 | Jeg erklærer videre at denne besvarelsen: ikke har vært brukt til annen eksamen ved annen avdeling/universitet/høgskole innenlands eller utenlands; ikke refererer til andres arbeid uten at det er oppgitt; ikke refererer til eget tidligere arbeid uten at det er oppgitt; har alle referansene oppgitt i litteraturlisten; ikke er en kopi, duplikat eller avskrift av andres arbeid eller besvarelse. | ☒ |
| 3 | Jeg er kjent med at brudd på ovennevnte er å betrakte som fusk og kan medføre annullering av eksamen og utestengelse fra universiteter og høgskoler i Norge, jf. Universitets- og høgskoleloven §§ 4-7 og 4-8 og Forskrift om eksamen §§ 14 og 15. | ☒ |
| 4 | Jeg er kjent med at alle innleverte oppgaver kan bli plagiatkontrollert i URKUND, se Retningslinjer for elektronisk innlevering og publisering av studiepoenggivende studentoppgaver. | ☒ |
| 5 | Jeg er kjent med at høgskolen vil behandle alle saker hvor det foreligger mistanke om fusk etter høgskolens retningslinjer for behandling av saker om fusk. | ☒ |
| 6 | Jeg har satt meg inn i regler og retningslinjer i bruk av kilder og referanser på biblioteket sine nettsider. | ☒ |

Bruk av generative KI-verktøy i prosjektet er dokumentert i Vedlegg D (KI-erklæring) i tråd med HiMolde sine retningslinjer.

## Personvern

**Personopplysningsloven.** Forskningsprosjekt som innebærer behandling av personopplysninger iht. Personopplysningsloven skal meldes til Sikt (tidligere NSD) for vurdering.

Har oppgaven vært vurdert av Sikt/NSD? ☐ ja  ☒ nei

Jeg erklærer at oppgaven ikke omfattes av Personopplysningsloven. ☒

*Begrunnelse:* Analysen bygger på aggregerte hendelsesdata fra LEO/BRIS hvor operatør-ID er strukturelt fraværende, og på operative valideringssamtaler som ikke inneholder personidentifiserbar informasjon. Se kap 5.7.

**Helseforskningsloven.** Har oppgaven vært til behandling hos REK? ☐ ja  ☒ nei

*Begrunnelse:* Prosjektet faller ikke inn under Helseforskningsloven. Det behandler ikke helseopplysninger eller pasientdata.

## Publiseringsavtale

| Felt | Verdi |
|---|---|
| Studiepoeng | 15 |
| Veileder | Bård Inge Austigard Pettersen |

**Fullmakt til elektronisk publisering av oppgaven.** Forfatter har opphavsrett til oppgaven. Det betyr blant annet enerett til å gjøre verket tilgjengelig for allmennheten (Åndsverkloven § 2). Alle oppgaver som fyller kriteriene vil bli registrert og publisert i Brage HiM med forfatterens godkjennelse. Oppgaver som er unntatt offentlighet eller båndlagt vil ikke bli publisert.

Jeg gir herved Høgskolen i Molde en vederlagsfri rett til å gjøre oppgaven tilgjengelig for elektronisk publisering: ☐ ja  ☐ nei  *(fylles ut ved innlevering)*

Er oppgaven båndlagt (konfidensiell)? ☐ ja  ☒ nei

*Beredskapsanalyser, ROS-dokumenter og BRIS-uttrekk er behandlet som intern dokumentasjon. Rapporten presenterer kun aggregerte resultater og metodebeskrivelser som ikke kompromitterer beredskapsinformasjon.*

Dato: 31. mai 2026

\newpage

## Sammendrag

Norske 110-sentraler er kritisk beredskapsinfrastruktur som mottar nødmeldinger og koordinerer brann- og redningsinnsats. Bemanningsnivået fastsettes lokalt gjennom risiko- og beredskapsanalyser (ROS), men det finnes ingen nasjonal, kvantitativ standard for hvordan operativ belastning oversettes til konkret bemanning utover minimumskravet. Hovedanalysen i rapporten er en casestudie av 110 Sør-Vest; den nasjonale delen brukes som benchmarking og generaliseringsgrunnlag.

Denne rapporten analyserer i hvilken grad faktisk bemanning ved 110 Sør-Vest (primærcase) samsvarer med kapasitetsbehovet beregnet fra historiske hendelsesdata. En innledende Erlang-C-analyse (M/M/c) viste svært lav systemutnyttelse (høyeste observerte verdi 5,9 %) for alle skifttyper. Resultatet er formelt korrekt, men metodisk utilstrekkelig fordi modellen ikke fanger at sentralens operative prosedyre (makkerpar-drift) krever to operatører parallelt per pri-1-hendelse. Studiens hovedmodell er derfor en **prosedyrbasert ankomstkonfliktmodell** med op-binder-semantikk, som måler sannsynligheten for at et beredskapsanrop ankommer i en tilstand der makkerpar-driftsstandarden ikke kan opprettholdes. Modellen skiller eksplisitt mellom D-pri1 (pri-1-utrykning, makkerpar) og D-aba (ABA-utrykning, serielt).

Hovedfunnene for 110 Sør-Vest 2025 viser at **32,6 % av beredskapsanropene på natt/helg ankommer i svikt-tilstand** (variant A, beredskapsbelastning), stigende til 33,2 % ved inkludering av total operativ belastning (variant B). Statistisk usikkerhet i den observerte D-pri1-bindingstidsfordelingen er kvantifisert via ikke-parametrisk bootstrap (B = 1 000): 95 % CI [32,1; 33,2] %. Over halvparten av beredskapsanropene på natt/helg ankommer i brudd eller svikt. En scenarioanalyse viser at én ekstra operatør på natt/helg reduserer sviktraten fra ca. 33 % til 16,7 %. Resultatene er benchmarket mot nasjonalt datagrunnlag (DSB BRIS 2025, 508 228 registrerte henvendelser i form av oppdrag, alle 12 sentraler; faktisk anropsvolum er høyere som følge av sammenstilling, jf. kap 6.2). L-aba-bindingstid er empirisk kalibrert via en to-trinns dybdeanalyse (n=100 i runde 2, mean 4,53 min). Studien fremstår som en av de første kvantitative kapasitetsanalysene av en norsk 110-sentral basert på historiske hendelsesdata, og foreslår en V3-klassifiseringsregel (D-pri1/D-aba/L-aba med Kilde=Alarm-krav) som forutsetning for sammenlignbar nasjonal benchmarking.

**Nøkkelord:** 110-sentral · bemanningsdimensjonering · prosedyrbasert kapasitetsmodell · ankomstkonflikt · op-binder-semantikk · makkerpar · D-pri1 · D-aba · Erlang-C · køteori · LEO/BRIS · beredskap.

## Abstract

The twelve Norwegian fire and rescue dispatch centres (110-centres) constitute critical emergency infrastructure that receives emergency calls and coordinates fire and rescue response. Staffing levels are set locally through risk and emergency analyses (ROS), but Norway lacks a national, quantitative standard for translating operational load into specific staffing levels beyond a regulatory minimum of two operators. The main analysis in this report is a case study of 110 Sør-Vest; the national component is used for benchmarking and generalisation.

This report analyses the extent to which actual staffing at 110 Sør-Vest (primary case) matches the capacity demand computed from historical incident data. An initial Erlang-C (M/M/c) analysis yielded very low server utilisation (highest observed 5.9 %) across all shift types. The result is formally correct but methodologically inadequate, because the model does not capture that the centre's operational procedure (buddy-pair operation) requires two operators in parallel per priority-1 incident. The study's primary model is therefore a **procedure-based arrival conflict model** with op-binder semantics, which measures the probability that an emergency call arrives in a state where the buddy-pair operating standard cannot be maintained. The model explicitly distinguishes D-pri1 (priority-1 dispatches, buddy-pair) from D-aba (automatic fire alarm dispatches, serial single-operator).

Main findings for 110 Sør-Vest 2025 show that **32.6 % of emergency calls during nights and weekends arrive in a failure state** (variant A, emergency load), rising to 33.2 % when total operational load is included (variant B). Statistical uncertainty in the observed D-pri1 binding time distribution is quantified via non-parametric bootstrap (B = 1,000): 95 % CI [32.1; 33.2] %. More than half of all emergency calls during nights and weekends arrive in either breach or failure. A scenario analysis shows that adding one operator on night/weekend shifts reduces the failure rate from about 33 % to 16.7 %. Results are benchmarked against national data (DSB BRIS 2025, 508,228 registered dispatches across all 12 centres; actual call volume is higher due to merging of related calls, cf. ch. 6.2). The L-aba binding time has been empirically calibrated via a two-stage in-depth analysis (n=100 in round 2, mean 4.53 min). The study appears to be one of the first quantitative capacity analyses of a Norwegian 110-centre based on historical incident data, and proposes a V3 classification rule (D-pri1/D-aba/L-aba with a Kilde=Alarm requirement) as a prerequisite for comparable national benchmarking.

**Keywords:** emergency dispatch centre · staffing dimensioning · procedure-based capacity model · arrival conflict · op-binder semantics · buddy-pair operation · D-pri1 · D-aba · Erlang-C · queueing theory · LEO/BRIS · emergency preparedness.

\newpage

## 1. Innledning

### 1.1 Bakgrunn og tema

Norske 110-sentraler er det primære kontaktpunktet for brann- og redningsnødmeldinger i Norge. De tolv sentralene opererer døgnet rundt og koordinerer utrykningsressurser over store geografiske områder. I 2025 håndterte de samlet 508 228 registrerte oppdrag (DSB, 2025). Tallet refererer til oppdrag i BRIS, og faktisk anropsvolum er høyere fordi tilleggsanrop til samme hendelse rutinemessig sammenstilles i ett oppdrag (se kap 6.2).

Bemanningen av 110-operatører reguleres av brann- og redningsvesenforskriften. Forskriften pålegger minimum to operatører i vaktrommet. Fastsettelsen av bemanning utover dette overlates til lokale risiko- og beredskapsanalyser (ROS). Samme forskrift inneholder konkrete kvantitative krav til brann- og redningsvesenets organisering, beredskap, bemanning og innsatstid. En tilsvarende kvantitativ, nasjonal standard for 110-bemanning mangler.

Problemstillingen er ikke at 110-sentraler generelt er over- eller underbemannet. Den er at det ikke finnes et kvantitativt, etterprøvbart grunnlag for å avgjøre hva som er tilstrekkelig bemanning ved en gitt sentral. Konsekvensene drøftes i kap 9.

### 1.2 Tidligere forskning og kunnskapsgap

Klassisk køteori for telefonsystemer (Erlang, 1917; Gans et al., 2003) og kvalitetsdrevet bemanning (Halfin & Whitt, 1981; Garnett et al., 2002) er velprøvde rammeverk i kommersielle call-sentre. De er sjeldnere anvendt på nødmeldesentraler med makkerpar-prosedyre, aktivt hendelsebilde utover samtaletid og overløpsmekanismer.

Internasjonal forskning som dekker disse særtrekkene finnes. Chelst og Barlach (1981) og Harchol-Balter (2022) gir flerserver-rammeverk der jobber krever flere servere samtidig. Gustavsson (2018), L'Ecuyer et al. (2018) og Dwars (2013) har anvendt stokastiske modeller på nordiske og europeiske nødmeldesentraler. Van Buuren et al. (2017) viser at funksjonsdifferensiering kan forbedre kapasitet uten bemanningsøkning. Forskning på kognitiv belastning (Al-Sarhani et al., 2025; Leonardsen et al., 2021) dokumenterer at operatørenes arbeidsmønster avviker vesentlig fra det klassiske kømodeller forutsetter.

Norsk forskning på 110-sentralenes kapasitet er derimot svært begrenset. Leonardsen et al. (2021) gir kvalitative funn fra AMK-sentraler. Samdal et al. (2021) analyserer dispatch-nøyaktighet for ambulanser. Etter litteratursøket i denne studien (kap 2) er det ikke funnet publiserte kvantitative kapasitetsanalyser av norske 110-sentraler basert på historiske hendelsesdata.

Kunnskapsgapet er dermed konkret: **det finnes ingen kjent kvantitativ, etterprøvbar analyse av 110-kapasitet som fanger makkerpar-bindingen, skiller ulike hendelsesdynamikker, og kan anvendes systematisk på tvers av sentralene i Norge.** Eksisterende ROS- og beredskapsanalyser er kvalitative og ikke sammenlignbare på tvers. Denne studien søker å bidra til å fylle dette gapet for én sentral, og å vurdere om rammeverket kan overføres til andre.

### 1.3 Problemstilling

**I hvilken grad samsvarer faktisk bemanning ved 110 Sør-Vest med kapasitetsbehovet beregnet fra historiske hendelsesdata og køteoretiske modeller, og hva indikerer funnene om overførbarhet til norske 110-sentraler?**

Spørsmålet undersøkes fordi fraværet av en kvantitativ dimensjoneringsstandard gjør dagens lokale bemanningsvurderinger vanskelige å etterprøve på tvers av sentraler.

Problemstillingen er todelt. Den krever (i) en operasjonalisering av begrepet *kapasitetsbehov* som er relevant for 110-driftens prosedyrekrav, og (ii) en empirisk vurdering av hvor godt faktisk bemanning matcher dette behovet. Erlang-C danner grunnlinjen, men viser seg utilstrekkelig i denne konteksten (jf. kap 6). Studien utvikler derfor en prosedyrbasert variant, den prosedyrbaserte ankomstkonfliktmodellen, som måler operativ kapasitet ved hvert beredskapsanrops ankomsttidspunkt.

Forskningsspørsmålene under operasjonaliserer problemstillingen. RQ1 og RQ2 etablerer det empiriske grunnlaget (ankomstrate og kapasitetsbinding). RQ3 måler kapasitetsgapet mot prosedyrstandarden. RQ4 sammenligner mot dagens kvalitative dimensjoneringsgrunnlag. RQ5 prøver overførbarheten til en nasjonal dimensjoneringslogikk.

- **RQ1:** Hva er ankomstraten (λ) til 110 Sør-Vest per skiftperiode, og hvilke belastningsmønstre fremgår av historiske LEO/BRIS-data?
- **RQ2:** Hva er gjennomsnittlig håndteringstid (μ⁻¹) per hendelseskategori, og i hvilken grad binder aktivt hendelsebilde operatørkapasitet utover samtaletid?
- **RQ3:** I hvilken andel av beredskapsanropene ved 110 Sør-Vest ankommer anropet i en tilstand der sentralens operative driftsstandard (makkerpar) ikke kan opprettholdes, og hva er det strukturelle kapasitetsgapet mellom hverdag og helg?
- **RQ4:** I hvilken grad gir eksisterende ROS- og beredskapsanalyse for 110 Sør-Vest et tilstrekkelig metodisk grunnlag for å begrunne faktisk bemanning?
- **RQ5:** Hvilke strukturelle forhold i nasjonalt DSB-grunnlag (hendelsesvolum, innbyggertall, areal og klassifiseringspraksis) kan inngå i en framtidig generaliserbar dimensjoneringsmodell på tvers av norske 110-sentraler?

### 1.4 Sentrale begreper og notasjon

Modellen og rapporten bygger på en spesifikk nomenklatur som introduseres formelt i kap 3 og 6, men brukes gjennomgående fra kap 4. Tabellene under gir minimumsdefinisjoner for leseren. Kategoritabellen i 1.4.1 dekker hendelseskategoriene og modellens kjernebegreper. Forkortelsestabellen i 1.4.2 dekker tekniske termer og systemnavn som brukes gjennom hele rapporten.

#### 1.4.1 Modellens kategorier og kjernebegreper

| Begrep | Kort definisjon |
|---|---|
| **D-pri1** | Pri-1-utrykning (bygningsbrann, trafikkulykke, farlig gods). Krever makkerpar: to operatører bundet parallelt under akuttfasen. |
| **D-aba** | ABA-utrykning (automatisk brannalarm). Håndteres serielt av én operatør; valgfri Fase 2 (nødtelefon/panel-veiledning) med sannsynlighet $p$. |
| **L-aba** | ABA-hendelse uten utrykning, men med Kilde=Alarm. Egen kategori for å skille reelle alarmhendelser fra øvrige korte oppdrag. |
| **L-hendelse / L-ukjent** | Korte oppdrag uten initiell hendelsestype eller uten registrert klassifisering. |
| **S / F / V** | Service (overføringstester), feilringing, viderevarsling. Bakgrunnsbelastning som ikke inngår i variant A, men i variant B. |
| **Op-binder** | Tidsavgrenset binding av $q \in \{1, 2\}$ operatører fra et tidspunkt $t$ i $d$ minutter. Hver hendelse ekspanderes til ett eller flere op-binder-events. |
| **Kilde=Alarm-krav** | V3-regel: L-aba og D-aba krever at oppdragets Kilde-felt er «Alarm». Dette sikrer at ABA-kategoriene ikke forurenses av telefonhenvendelser feilklassifisert som ABA. |
| **c_eff** | Effektiv operatørkapasitet $= c_{\text{total}} - 1$ (vaktleder besvarer normalt ikke nødanrop). |
| **Normal / Brudd / Svikt** | Kapasitetsnivåer ved ankomst av nytt beredskapsanrop. Normal = makkerpar mulig (ledige ≥ 2). Brudd = solo-håndtering mulig (ledige = 1). Svikt = ingen ledig operatør (ledige ≤ 0). |
| **Variant A / Variant B** | A: beredskapsbelastning (D-pri1, D-aba, skjulte anrop). B: total operativ belastning (alle kategorier inklusive S, L-aba, L-hendelse, L-ukjent, F, V). |
| **Scenariobånd (lav/hoved/høy)** | Tre parametersett som spenner usikkerheten i ikke-empiriske antagelser. Hovedscenario gir punktestimat; lav/høy gir bånd. Brukt for å indikere usikkerhet ved resultatene. |

#### 1.4.2 Forkortelser

| Forkortelse | Forklaring |
|---|---|
| **ABA** | Automatisk brannalarm: alarm utløst av røyk-/varmedetektor i bygg, mottatt elektronisk hos 110. |
| **AMK** | Akuttmedisinsk kommunikasjonssentral: helsesektorens 113-sentral (analog til 110 for brann). |
| **BRIS** | Brannvesenets innrapporteringsløsning: DSBs nasjonale registrerings- og statistikksystem for hendelser. |
| **DSB** | Direktoratet for samfunnssikkerhet og beredskap: fagdirektorat for brann- og redningsvesenet i Norge. |
| **EMS** | Emergency Medical Services: internasjonal terminologi for prehospitalt helsevesen (analog til norsk AMK). |
| **GUL** | Operativ funksjon: medlytt og utalarmering. Bundet parallelt med RØD under akuttfasen. |
| **GRØNN** | Operativ funksjon: ledig, klar for neste nødanrop. |
| **ISM** | Integrated Status Monitoring (eller tilsvarende alarmmottakssystem), brukes ved enkelte sentraler i stedet for konvensjonell ABA-rute. |
| **LABA** | Logging og analyse av alarm- og bindingsdata: intern dybdeanalyse av L-aba-hendelser (kap 5.4). |
| **LEO** | Felles oppdragshåndteringssystem for 110-sentralene fra høst 2024. |
| **M/M/c** | Standard køteoretisk modell: Markov-ankomst, Markov-service, c parallelle servere (Erlang-C). |
| **MOB** | Melding Om Brannvesen: DSBs årlige rapportering av bemanning og struktur fra hver sentral. |
| **MSJ** | Multiserver-Job: køteoretisk rammeverk der hver jobb krever flere servere samtidig (Harchol-Balter, 2022). |
| **NENA** | National Emergency Number Association (USA): standardiseringsorganisasjon for 9-1-1-sentraler. |
| **PSAP** | Public Safety Answering Point: amerikansk betegnelse for 110-, 112- eller 911-mottakssentral. |
| **QED-regime** | Quality-and-Efficiency-Driven regime: Halfin-Whitt-asymptotikk for store servicesystemer der både kvalitet og effektivitet kan oppnås. |
| **RØD** | Operativ funksjon: besvarer nødanropet og gjennomfører intervju. Hovedansvarlig under akuttfasen. |
| **ROS** | Risiko- og sårbarhetsanalyse: kvalitativ analyse som ligger til grunn for lokal bemanningsfastsettelse utover forskriftens minimum. |
| **SSB** | Statistisk sentralbyrå: nasjonal kilde for befolknings- og strukturdata brukt i benchmarking. |
| **V3** | Tredje generasjon klassifiseringsregel utviklet i denne studien. Definerer D-pri1, D-aba og L-aba med Kilde=Alarm-krav (kap 5.3.2). |
| **VL** | Vaktleder: operativ leder per vakt. Besvarer som hovedregel ikke nødanrop, derav $c_{\text{eff}} = c_{\text{total}} - 1$. |

### 1.5 Avgrensninger

Prosjektet avgrenses til følgende områder:

- **Vaktromsbemanning ved 110-sentral.** Ressursdisponering i brannvesenet, taktisk hendelseshåndtering og organisatoriske beslutninger utover sentralen ligger utenfor scope.
- **Retrospektiv og planleggingsrettet analyse.** Modellen er et beslutningsverktøy for kapasitetsvurdering, ikke et sanntidssystem for operativ styring.
- **Primærcase 110 Sør-Vest 2025.** Hovedmodellen er kjørt på denne ene sentralen. Den nasjonale delen (kap 8.5 og 8.4.1) er benchmarking og kontekst, ikke full prosedyrbasert modellering for de øvrige 11 sentralene.
- **Ordinære driftsforhold.** Ekstraordinære hendelser som langvarige storbranner og katastrofescenarier holdes utenfor modellens gyldighetsområde. De drøftes i diskusjonskapittelet som grenser for modellens anvendbarhet.
- **Ring-flom som kontekst.** Call surge belyses som operativ ekstrembelastning, men modelleres ikke som primærscenario.

Disse avgrensningene er valgt fordi de definerer det området hvor data, prosedyrekunnskap og analytisk rammeverk er konsistent nok til å gi etterprøvbare resultater. Begrunnelsen er ikke tidsmangel, men metodisk avgrensning.

### 1.6 Antagelser

Modellen hviler på et lite sett eksplisitte antagelser som er listet, kategorisert og konsekvensvurdert i Tabell 6.3 i kap 6.7. Antagelsene er forankret i prosedyredokumentasjon (Rogaland brann og redning IKS, 2024), BRIS-tidsstempler eller operative valideringssamtaler, og er merket etter type: empirisk, empirisk + statistisk validert, forankret antagelse, forenklet antagelse, eller operativt estimat med sensitivitetsspenn.

De viktigste antagelsene for hovedfunnet er:

- **A1.** Effektiv operatørkapasitet $c_{\text{eff}} = c_{\text{total}} - 1$, fordi vaktleder normalt ikke besvarer nødanrop. Konsekvens hvis brutt: Svikt-andelen overestimert.
- **A2.** D-pri1 binder makkerpar parallelt gjennom hele akuttfasen ($q = 2$). Empirisk grunnlag i BRIS-tidsstempler, statistisk validert via bootstrap-CI (avsnitt 8.3.4 i kap 8).
- **A5.** L-aba bindingstid = 4,5 min (empirisk kalibrert via LABA-dybdeanalysen, n=100, mean 4,53, 95 % CI [3,74; 5,43]).
- **A6.** Sammenstilte tilleggsanrop binder 1 min. Største restusikkerhet av de antatte parametrene. Trekker mot konservativt estimat.

Antagelsene drøftes systematisk i kap 6.7 med konsekvens hvis de svikter, og resultatkapitlets sensitivitets- og bootstrap-analyser tester robusthet mot variasjon i parameterverdier (kap 8.3.3 og 8.3.4). Ekstraordinære hendelser (storbranner, katastrofescenarier) holdes utenfor modellens gyldighetsområde (jf. avgrensning i 1.5).

### 1.7 Rapportens struktur

Rapporten består av ti kapitler.

**Kapittel 2** gjennomgår relevant litteratur strukturert etter fem tematiske områder: klassisk køteori, nødmeldesentraler, team-basert kapasitet og prosedyrkonformitet, nordisk nødmeldeforskning, og dimensjoneringsregulering.

**Kapittel 3** etablerer det teoretiske rammeverket. Erlang-C presenteres som grunnlinje, QED-regimet som regimekarakteristikk, og multiserver-jobs som rammeverk for op-binder-semantikk.

**Kapittel 4** beskriver 110 Sør-Vest som case. Bemanning, arbeidsmetodikk og operative særtrekk dokumenteres.

**Kapittel 5** presenterer metode og data, inkludert V3-klassifiseringsregelen og LABA-dybdeanalysen.

**Kapittel 6** utvikler kapasitetsmodellen gjennom tre faser: Erlang-C, simultanitetsanalyse og prosedyrbasert ankomstkonfliktmodell.

**Kapittel 7** presenterer analysen: metodisk tilnærming, datagrunnlag for synlige og sammenstilte anrop, operativ arbeidsmetodikk som kapasitetsramme, og bindingstidsestimater per kategori.

**Kapittel 8** presenterer resultatene for 110 Sør-Vest 2025: Erlang-C-grunnlinje, prosedyrbasert ankomstkonfliktmodell (variant A), scenario +1 operatør, total operativ belastning (variant B) med sensitivitets- og bootstrap-analyse, ROS-grunnlaget (RQ4), og nasjonal benchmarking (RQ5).

**Kapittel 9** diskuterer funnene mot problemstilling, teori og begrensninger.

**Kapittel 10** besvarer problemstillingen og gir anbefalinger for dimensjonering og videre forskning.