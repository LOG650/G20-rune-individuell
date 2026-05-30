---
title: "Kapasitetsstyring og bemanningsdimensjonering ved norske 110-sentraler"
subtitle: "En analyse av operatørkapasitet med prosedyrebasert ankomstkonfliktmodell"
author: "Rune Grødem · G20 Individuell"
date: "LOG650 Logistikk og kunstig intelligens · Høgskolen i Molde · Vår 2026 · Innlevert 31. mai 2026 · Veileder: Bård Inge Austigard Pettersen · Antall ord: ca. 30 400 (kap. 1 til 10, eksklusive tabeller, kode og litteraturliste; maskinell narrativtelling)"
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

Jeg gir herved Høgskolen i Molde en vederlagsfri rett til å gjøre oppgaven tilgjengelig for elektronisk publisering: ☐ ja  ☒ nei

Er oppgaven båndlagt (konfidensiell)? ☐ ja  ☒ nei

*Beredskapsanalyser, ROS-dokumenter og BRIS-uttrekk er behandlet som intern dokumentasjon. Rapporten presenterer kun aggregerte resultater og metodebeskrivelser som ikke kompromitterer beredskapsinformasjon.*

Dato: 31. mai 2026

\newpage

## Sammendrag

Norske 110-sentraler mottar nødmeldinger og koordinerer brann- og redningsinnsats. Bemanningen fastsettes lokalt gjennom risiko- og beredskapsanalyser (ROS), og det finnes ingen nasjonal, kvantitativ standard for hvordan operatørbelastning oversettes til konkret bemanning utover et minimumskrav på to operatører per skift. Denne rapporten er en casestudie av 110 Sør-Vest, supplert med nasjonal benchmarking mot de øvrige elleve sentralene.

Rapporten undersøker i hvilken grad faktisk bemanning ved 110 Sør-Vest samsvarer med kapasitetsbehovet beregnet fra historiske hendelsesdata. En klassisk køteoretisk analyse (Erlang-C) gir svært lav systemutnyttelse (under 6 %) for alle skift, og antyder at bemanningen er tilstrekkelig. Den fanger imidlertid ikke at sentralens prosedyre krever to operatører samtidig (makkerpar) for pri-1-hendelser som bygningsbrann og trafikkulykke. Rapporten utvikler derfor en prosedyrebasert kapasitetsmodell som måler hvor ofte et nytt beredskapsanrop ankommer i en tilstand der makkerpar-prinsippet ikke kan opprettholdes.

Hovedfunnet for 110 Sør-Vest 2025 er at om lag ett av fem beredskapsanrop på natt og helg ankommer i en slik svikt-tilstand (21,0 %, med 95 % bootstrap-konfidensintervall [20,1; 21,4]). Årsaken er at minimumsbemanningen på natt/helg er to operatører: én pågående pri-1-hendelse binder dermed hele kapasiteten. På dag hverdag er sviktraten 6,4 %. En scenarioanalyse viser at å heve minimumsbemanningen med én operatør på natt/helg reduserer sviktraten til 5,6 %, mens tilsvarende heving på dag reduserer sviktraten på dag fra 6,4 % til 3,5 %. Hovedtallet 21,0 % avhenger av antatt fordeling av de skjulte (sammenstilte) anropenes ankomsttidspunkt (sensitivitetsbånd 16,8 til 26,4 %). Den strukturelle natt/dag-asymmetrien i svikt er derimot robust: svikten på natt/helg er om lag tre ganger så høy som på dag (3,3×).

Studien er en av de første kvantitative kapasitetsanalysene av en norsk 110-sentral basert på historiske hendelsesdata. Rammeverket er prinsipielt overførbart til de øvrige sentralene gitt felles klassifiseringsregler.

**Nøkkelord:** 110-sentral · bemanningsdimensjonering · prosedyrebasert kapasitetsmodell · ankomstkonflikt · op-binder-semantikk · makkerpar · D-pri1 · D-aba · Erlang-C · køteori · LEO/BRIS · beredskap.

## Abstract

Norway's twelve fire and rescue dispatch centres (110-centres) receive emergency calls and coordinate fire and rescue response. Staffing levels are set locally through risk and emergency analyses (ROS), and Norway lacks a national, quantitative standard for translating operator workload into specific staffing levels beyond a regulatory minimum of two operators per shift. This report is a case study of 110 Sør-Vest, supplemented by national benchmarking against the remaining eleven centres.

The report investigates whether actual staffing at 110 Sør-Vest matches the capacity demand computed from historical incident data. A classical queueing-theory analysis (Erlang-C) yields very low server utilisation (below 6 %) across all shifts, suggesting that staffing is sufficient. However, this model does not capture the centre's procedural requirement of two operators working simultaneously (buddy-pair) for priority-1 incidents such as building fires and traffic accidents. The report therefore develops a procedure-based capacity model that measures how often a new emergency call arrives in a state where the buddy-pair principle cannot be maintained.

The main finding for 110 Sør-Vest 2025 is that roughly one in five emergency calls during nights and weekends arrives in such a failure state (21.0 %, with a 95 % bootstrap confidence interval of [20.1; 21.4]). The cause is that minimum staffing on nights and weekends is two operators: one ongoing priority-1 incident thus binds the entire capacity. On weekday day shifts, the failure rate is 6.4 %. A scenario analysis shows that adding one operator to night/weekend shifts reduces the failure rate to 5.6 %, while a corresponding increase on day shifts reduces the day failure rate from 6.4 % to 3.5 %. The headline figure of 21.0 % depends on the assumed distribution of the arrival times of the hidden (consolidated) calls (sensitivity band 16.8 to 26.4 %). The structural night/day asymmetry in failure is robust, however: the night/weekend failure rate is about three times the daytime rate (3.3×).

The study is one of the first quantitative capacity analyses of a Norwegian 110-centre based on historical incident data. The framework is in principle transferable to the other centres given common classification rules.

**Keywords:** emergency dispatch centre · staffing dimensioning · procedure-based capacity model · arrival conflict · op-binder semantics · buddy-pair operation · D-pri1 · D-aba · Erlang-C · queueing theory · LEO/BRIS · emergency preparedness.

\newpage

## 1. Innledning

### 1.1 Bakgrunn og tema

Norske 110-sentraler er det primære kontaktpunktet for brann- og redningsnødmeldinger i Norge. De tolv sentralene opererer døgnet rundt og koordinerer utrykningsressurser over store geografiske områder. I 2025 håndterte de samlet 508 228 registrerte oppdrag (DSB, 2025). Tallet refererer til oppdrag i BRIS, og faktisk anropsvolum er høyere fordi tilleggsanrop til samme hendelse rutinemessig sammenstilles i ett oppdrag (se kap 6.2).

Bemanningen av 110-operatører reguleres av brann- og redningsvesenforskriften. Forskriften pålegger minimum to operatører i vaktrommet. Fastsettelsen av bemanning utover dette overlates til lokale risiko- og beredskapsanalyser (ROS). Samme forskrift inneholder konkrete kvantitative krav til brann- og redningsvesenets organisering, beredskap, bemanning og innsatstid. En tilsvarende kvantitativ, nasjonal standard for 110-bemanning mangler.

Problemstillingen er ikke at 110-sentraler generelt er over- eller underbemannet. Den er at det ikke finnes et kvantitativt, etterprøvbart grunnlag for å avgjøre hva som er tilstrekkelig bemanning ved en gitt sentral. Konsekvensene drøftes i kap 9.

### 1.2 Tidligere forskning og kunnskapsgap

Klassisk køteori for telefonsystemer (Erlang, 1917; Gans et al., 2003) og kvalitetsdrevet bemanning (Halfin & Whitt, 1981; Garnett et al., 2002) er velprøvde rammeverk i kommersielle call-sentre. De er sjeldnere anvendt på nødmeldesentraler med makkerpar-prosedyre, aktivt hendelsebilde utover samtaletid og overløpsmekanismer.

Internasjonal forskning som dekker disse særtrekkene finnes. Chelst og Barlach (1981) og Harchol-Balter (2022) gir flerserver-rammeverk der jobber krever flere servere samtidig. Gustavsson (2018), L'Ecuyer et al. (2018) og Dwars (2013) har anvendt stokastiske modeller på nordiske og europeiske nødmeldesentraler. Van Buuren et al. (2017) viser at funksjonsdifferensiering kan forbedre kapasitet uten bemanningsøkning. Forskning på kognitiv belastning (Alzayed & Alsardi, 2025; Leonardsen et al., 2019) dokumenterer at operatørenes arbeidsmønster avviker vesentlig fra det klassiske kømodeller forutsetter.

Norsk forskning på 110-sentralenes kapasitet er derimot svært begrenset. Leonardsen et al. (2019) gir kvalitative funn om arbeidsforholdene ved norske nødmeldesentraler (EMCC/AMK). Samdal et al. (2021) analyserer dispatch-nøyaktighet i legebemannet prehospital akuttjeneste (HEMS/legebil). Etter litteratursøket i denne studien (kap 2) er det ikke funnet publiserte kvantitative kapasitetsanalyser av norske 110-sentraler basert på historiske hendelsesdata.

Kunnskapsgapet er dermed konkret: **det finnes ingen kjent kvantitativ, etterprøvbar analyse av 110-kapasitet som fanger makkerpar-bindingen, skiller ulike hendelsesdynamikker, og kan anvendes systematisk på tvers av sentralene i Norge.** Eksisterende ROS- og beredskapsanalyser er kvalitative og ikke sammenlignbare på tvers. Denne studien søker å bidra til å fylle dette gapet for én sentral, og å vurdere om rammeverket kan overføres til andre.

### 1.3 Problemstilling

**I hvilken grad samsvarer faktisk bemanning ved 110 Sør-Vest med kapasitetsbehovet beregnet fra historiske hendelsesdata og køteoretiske modeller, og hva indikerer funnene om overførbarhet til norske 110-sentraler?**

Spørsmålet undersøkes fordi fraværet av en kvantitativ dimensjoneringsstandard gjør dagens lokale bemanningsvurderinger vanskelige å etterprøve på tvers av sentraler.

Problemstillingen er todelt. Den krever (i) en operasjonalisering av begrepet *kapasitetsbehov* som er relevant for 110-driftens prosedyrekrav, og (ii) en empirisk vurdering av hvor godt faktisk bemanning matcher dette behovet. Erlang-C danner grunnlinjen, men viser seg utilstrekkelig i denne konteksten (jf. kap 6). Studien utvikler derfor en prosedyrebasert variant, den prosedyrebaserte ankomstkonfliktmodellen, som måler operativ kapasitet ved hvert beredskapsanrops ankomsttidspunkt.

Forskningsspørsmålene under operasjonaliserer problemstillingen. RQ1 og RQ2 etablerer det empiriske grunnlaget (ankomstrate og kapasitetsbinding). RQ3 måler kapasitetsgapet mot prosedyrestandarden. RQ4 sammenligner mot dagens kvalitative dimensjoneringsgrunnlag. RQ5 prøver overførbarheten til en nasjonal dimensjoneringslogikk.

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
- **Primærcase 110 Sør-Vest 2025.** Hovedmodellen er kjørt på denne ene sentralen. Den nasjonale delen (kap 8.5 og 8.6) er benchmarking og kontekst, ikke full prosedyrebasert modellering for de øvrige 11 sentralene.
- **Ordinære driftsforhold.** Ekstraordinære hendelser som langvarige storbranner og katastrofescenarier holdes utenfor modellens gyldighetsområde. De drøftes i diskusjonskapittelet som grenser for modellens anvendbarhet.
- **Ring-flom som kontekst.** Call surge belyses som operativ ekstrembelastning, men modelleres ikke som primærscenario.

Disse avgrensningene er valgt fordi de definerer det området hvor data, prosedyrekunnskap og analytisk rammeverk er konsistent nok til å gi etterprøvbare resultater. Begrunnelsen er ikke tidsmangel, men metodisk avgrensning.

### 1.6 Antagelser

Modellen hviler på et lite sett eksplisitte antagelser som er listet, kategorisert og konsekvensvurdert i Tabell 6.3 i kap 6.7. Antagelsene er forankret i prosedyredokumentasjon (Rogaland brann og redning IKS, 2024), BRIS-tidsstempler eller operative valideringssamtaler, og er merket etter type: empirisk, empirisk + statistisk validert, forankret antagelse, forenklet antagelse, eller operativt estimat med sensitivitetsspenn.

De viktigste antagelsene for hovedfunnet er:

- **A1.** Effektiv operatørkapasitet $c_{\text{eff}} = c_{\text{total}} - 1$, fordi vaktleder normalt ikke besvarer nødanrop. Konsekvens hvis brutt: Svikt-andelen overestimert.
- **A2.** D-pri1 binder makkerpar parallelt gjennom hele akuttfasen ($q = 2$). Empirisk grunnlag i BRIS-tidsstempler for bindingstiden; selve makkerpar-bindingen ($q = 2$) er prosedyreforankret, mens bindingstidsfordelingen er bootstrap-kvantifisert (avsnitt 8.3.4 i kap 8).
- **A5.** L-aba bindingstid = 4,5 min (empirisk kalibrert via LABA-dybdeanalysen, n=100, mean 4,53, 95 % CI [3,74; 5,43]).
- **A6.** Sammenstilte tilleggsanrop binder 1 min. Største restusikkerhet av de antatte parametrene. Trekker mot konservativt estimat.

Antagelsene drøftes systematisk i kap 6.7 med konsekvens hvis de svikter, og resultatkapitlets sensitivitets- og bootstrap-analyser tester robusthet mot variasjon i parameterverdier (kap 8.3.3 og 8.3.4). Ekstraordinære hendelser (storbranner, katastrofescenarier) holdes utenfor modellens gyldighetsområde (jf. avgrensning i 1.5).

### 1.7 Rapportens struktur

Rapporten består av ti fagkapitler, i tillegg til bibliografi og vedlegg.

**Kapittel 2** gjennomgår relevant litteratur strukturert etter fem tematiske områder: klassisk køteori, nødmeldesentraler, team-basert kapasitet og prosedyreetterlevelse, nordisk nødmeldeforskning, og dimensjoneringsregulering.

**Kapittel 3** etablerer det teoretiske rammeverket. Erlang-C presenteres som grunnlinje, QED-regimet som regimekarakteristikk, og multiserver-jobs som rammeverk for op-binder-semantikk.

**Kapittel 4** beskriver 110 Sør-Vest som case. Bemanning, arbeidsmetodikk og operative særtrekk dokumenteres.

**Kapittel 5** presenterer metode og data, inkludert V3-klassifiseringsregelen og LABA-dybdeanalysen.

**Kapittel 6** utvikler kapasitetsmodellen gjennom tre faser: Erlang-C, simultanitetsanalyse og prosedyrebasert ankomstkonfliktmodell.

**Kapittel 7** presenterer analysen: metodisk tilnærming, datagrunnlag for synlige og sammenstilte anrop, operativ arbeidsmetodikk som kapasitetsramme, og bindingstidsestimater per kategori.

**Kapittel 8** presenterer resultatene for 110 Sør-Vest 2025: Erlang-C-grunnlinje, prosedyrebasert ankomstkonfliktmodell (variant A), scenario +1 operatør, total operativ belastning (variant B) med sensitivitets- og bootstrap-analyse, ROS-grunnlaget (RQ4), og nasjonal benchmarking (RQ5).

**Kapittel 9** diskuterer funnene mot problemstilling, teori og begrensninger.

**Kapittel 10** besvarer problemstillingen og gir anbefalinger for dimensjonering og videre forskning.