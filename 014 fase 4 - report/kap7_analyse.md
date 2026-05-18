# 7. Analyse

Dette kapitlet presenterer den analytiske prosessen som danner grunnlag for resultatene i kap 8. Det er strukturert i fire deler: 7.1 viser den metodiske utviklingen fra køteori til prosedyrebasert kapasitetsmodell (inkludert Erlang-C-grunnlinjen som baseline), 7.2 dokumenterer differansen mellom synlig oppdragsvolum og estimert faktisk anropsvolum via sekvensgap-metoden, 7.3 utleder kapasitetsnivåene fra den operative arbeidsmetodikken (RØD/GUL/GRØNN/VL), og 7.4 estimerer bindingstider per hendelseskategori basert på empirisk dataanalyse og operative kalibreringssamtaler.

Kapitlet svarer på RQ1 (avsnitt 7.1 og 7.2) og RQ2 (avsnitt 7.4). Resultatene som svarer på RQ3-RQ5 presenteres i kap 8.

## 7.1 Metodisk tilnærming: fra køteori til prosedyrebasert kapasitetsmodell

Den opprinnelige modellhypotesen i prosjektet var at Erlang-C (M/M/c) kunne brukes som hovedmodell for kapasitetsanalysen. Erlang-C estimerer sannsynligheten for at et innkommende anrop må vente, gitt ankomstrate (λ), gjennomsnittlig servicetid (μ⁻¹) og antall servere (c). Resultatene fra denne innledende analysen er presentert i Tabell 6.1 (kap 6.3.3) og inngår nå som **referansemodell** (baseline) som dokumenterer hvorfor klassisk køteori er utilstrekkelig for 110-konteksten, ikke som studiens hovedmodell. Den prosedyrebaserte ankomstkonfliktmodellen, formelt definert i kap 6.4 og kvantifisert i kap 8, er studiens **hovedmodell** og originale bidrag.

Erlang-C-analysen viste svært lav systemutnyttelse, med høyeste observerte verdi 5,9 % (Dag/Helg) for alle skifttyper, noe som isolert sett kunne tyde på at bemanningsnivået er komfortabelt (jf. Tabell 6.1). Resultatene er formelt korrekte gitt inputparametrene, men metodisk utilstrekkelige for 110-konteksten av tre grunner: modellen forutsetter at servere er *uavhengige* og *parallelle*, den behandler kapasitetsbinding utover samtaletid som null, og den baserer seg på en ankomstrate som undervurderer faktisk innkommende volum (se avsnitt 7.2). Samtaletiden brukt i Erlang-C er 3,44 min (vektet gjennomsnitt fra operative valideringssamtaler, avsnitt 5.2.4), vesentlig kortere enn den totale bindingstiden for D-pri1 (median 14,1 min inkl. akuttfase og kvittering) som brukes i primærmodellen.

Gjennomgang av den operative prosedyren (Rogaland brann og redning IKS, 2024) avslørte at forutsetningen om én uavhengig server per anrop ikke stemmer med faktisk arbeidsmetodikk.

---

## 7.2 Synlig oppdragsvolum versus faktisk anropsvolum

En viktig begrensning ved BRIS/LEO-data er at statistikken viser synlige oppdrag, ikke nødvendigvis alle innkommende anrop. Når flere personer ringer om samme hendelse, blir tilleggsanropene sammenstilt med det eksisterende oppdraget og forsvinner som egne observasjoner i årsrapport og eksportdata.

For 2025 viser datasettet 61 964 synlige oppdrag, mens sekvensnummerlogikken i LEO indikerer et estimert faktisk anropsvolum på minst 80 865 anrop.

**Tabell 7.1: Synlig versus faktisk anropsvolum, 110 Sør-Vest 2025**

| | Antall |
|---|---|
| Synlige oppdrag (BRIS/LEO) | 61 964 |
| Estimert faktisk anropsvolum | 80 865 |
| Skjulte/sammenstilte anrop | 18 901 |
| Korreksjonsfaktor | 1,305x |

Differansen på 18 901 anrop, tilsvarende 23,4 %, representerer ikke valgbare eller trivielle henvendelser, men faktiske innkommende anrop som beslaglegger operatørkapasitet. Korreksjonsfaktoren på 1,305x gjelder forholdet mellom synlige oppdrag og estimert totalt anropsvolum (ikke forholdet mellom kategori D og totale belastningsenheter i modellen). Faktoren varierer mellom måneder (størst i januar: 1,438x) og er generelt høyest ved dagtid på hverdager, nettopp der kapasitetspresset allerede er høyest.

Et ytterligere forbehold er at ikke alle tilleggsanrop faktisk blir sammenstilt med den aktive hendelsen de tilhører. Under høyt press og med flere operatører involvert hender det at anrop som operativt tilhører en pågående hendelse likevel lukkes som egne saker, med initiell hendelsestype som «service», «feilringing» eller «løst av 110», i stedet for å bli tillagt det eksisterende oppdraget. Tilfeldig stikkprøvekontroll viser at anrop som kom inn som nødanrop kan bli lukket med slike kategorier. Disse anropene er i realiteten kritiske telefoner som må besvares, til forskjell fra faktiske servicehenvendelser som kan nedprioriteres. Konsekvensen er at estimatet på 18 901 sammenstilte anrop sannsynligvis er et underestimat av det faktiske antallet beredskapsrelaterte tilleggsanrop, noe som ytterligere forsterker modellens konservative karakter.

Dette har tre konsekvenser for analysen:

1. **Ankomstraten λ i Erlang-C er for lav.** En modell som bruker synlige oppdrag som grunnlag for λ vil systematisk undervurdere faktisk arbeidsbelastning. Selv en perfekt M/M/c-modell ville derfor vært basert på et ufullstendig inputgrunnlag.

2. **Sammenstilte anrop er modellert som egne belastningsenheter, men modellen er fortsatt konservativ.** I den prosedyrebaserte ankomstkonfliktmodellen (kvantifisert i avsnitt 8.1, formell definisjon i kap 6.4.6) er de 18 901 estimerte sammenstilte anropene inkludert som egne op-binder-events med interpolert ankomsttidspunkt og bindingstid 1 minutt (én operatør bundet i ett minutt). De bidrar dermed til antall aktive op-binder ved senere ankomster og kan utløse Brudd eller Svikt på samme måte som synlige oppdrag. Modellen er likevel konservativ av to grunner: (i) bindingstiden 1 min er et nedre estimat (faktisk varighet kan være lengre dersom innringer er stresset eller anropet håndteres som full hendelse), og (ii) sekvensgap-metoden fanger kun anrop som er sammenstilt med eksisterende oppdrag. Beredskapsrelaterte anrop som er feilkategorisert og lukket som egne saker (f.eks. som «service» eller «feilringing» under høyt press) er fortsatt usynlige. Det reelle antallet beredskapsrelaterte tilleggsanrop er derfor sannsynligvis høyere enn 18 901.

3. **Skjult belastning påvirker dimensjonering direkte.** Sammenstilte tilleggsanrop påvirker ikke bare ankomstraten i køteoretisk forstand, men også den operative bindingen i den prosedyrebaserte modellen. Inkluderingen av skjulte anrop som egne op-binder-events (punkt 2) gjør at primærmodellen fanger denne effekten i variant A, men siden underestimatet av antall skjulte anrop fortsatt eksisterer, betyr det at modellens svikt- og brudd-andeler er nedre estimater. For dimensjonering tilsier dette at analyser basert utelukkende på oppdragsteller (uten skjult-anrop-korreksjon) systematisk vil undervurdere både arbeidsbelastning, samtidighetskonflikt og behovet for bufferkapasitet.

Skillet mellom synlig oppdragsvolum og faktisk anropsvolum viser at kapasitetsanalyse ikke kan ta utgangspunkt i registrerte saker alene. Det neste spørsmålet blir derfor ikke bare hvor mange oppdrag som finnes, men hvordan sentralens arbeidsmetodikk gjør at disse anropene binder operatører over tid.

---

## 7.3 Den operative arbeidsmetodikken som kapasitetsramme

Prosedyren definerer tre operative funksjoner som roterer dynamisk mellom operatørene:

- **Rød funksjon:** Operatøren som besvarer nødtelefonen, oppretter hendelse i LEO og gjennomfører intervju med innringer. Binder én operatør fullt ut i den aktive samtalefasen.
- **Gul funksjon:** Aktiveres samtidig med RØD. GUL-operatøren går umiddelbart i medlytt når RØD besvarer anropet, for å bygge situasjonsforståelse og avhjelpe med lokalisering. Etter den innledende medlyttfasen utalarmerer GUL ressurser, håndterer samband og gir tidskritisk informasjon til mannskap underveis, delvis fortsatt på medlytt. GUL forblir bundet frem til vindusmelding mottas om at første ressurs er fremme, pluss kvittering og loggføring (anslagsvis 3 minutter). Først etter dette er GUL delvis frigjort og kan håndtere flere gule hendelser parallelt i en mer sporadisk oppfølgingsfase.
- **Grønn funksjon:** Ledig, klar for neste nødanrop. Prosedyren definerer eksplisitt som målsetning at *«én operatør til enhver tid er ledig og kan ta nødtelefoner»*.
- **Vaktleder (VL):** Overordnet funksjon med ansvar for oversikt, prioritering, pressehåndtering og innkalling. Prosedyren slår fast at *«vaktleder skal som et utgangspunkt ikke besvare nødanrop»*.

Den normale driftsformen er dermed et **makkerpar**: én rød og én gul operatør samarbeider om én hendelse, mens øvrige operatører er grønne og klare for neste anrop. Prosedyren definerer dette som normalstandarden, og understreker at *«tiden to operatører er involvert i samme hendelse gjøres så kort som mulig, for å raskt frigjøre kapasitet til neste hendelse»*.

### Kapasitetsnivåer utledet av prosedyren

Med utgangspunkt i prosedyrens rolledefinisjon etableres tre kapasitetsnivåer, som danner grunnlaget for den kvantitative analysen:

**Tabell 7.2: Kapasitetsnivåer i operativ tilpasningsmodell**

| Nivå | Definisjon | Betingelse | c_eff = 2 | c_eff = 3 |
|---|---|---|---|---|
| **Normal** | Makkerpar mulig for neste hendelse | ledige ≥ 2 | n_aktive = 0 | n_aktive ≤ 1 |
| **Brudd på driftsstandard** | Kun 1 ledig, solo-håndtering | ledige = 1 | n_aktive = 1 | n_aktive = 2 |
| **Svikt** | Ingen ledig operatør | ledige ≤ 0 | n_aktive ≥ 2 | n_aktive ≥ 3 |

*Ledige operatører = c_eff − n_aktive. Modellen speiler den operative virkeligheten: ved samtidskonflikter splittes makkerparet slik at operatørene fordeler seg. Med c_eff = 3 og 1 aktiv hendelse er det fortsatt 2 ledige (Normal), siden den tredje operatøren kan ta neste hendelse med makkerpar. Brudd oppstår først når det kun er 1 ledig, og svikt når ingen er ledig.*

Tabellen bygger på en operativ tilpasningslogikk der makkerpar ikke nødvendigvis forblir fast låst til én hendelse gjennom hele akuttfasen. Ved c_eff = 3 og én aktiv hendelse er det fortsatt to tilgjengelige operatører, slik at neste hendelse i praksis kan tas med et nytt makkerpar. Brudd oppstår først når den neste hendelsen må håndteres med kun én ledig operatør, og svikt når ingen er ledige.

Den kritiske asymmetrien mellom c_eff = 2 og c_eff = 3 er at med c_eff = 2 er det kun étt steg fra normal drift til svikt: allerede ved andre samtidige hendelse er begge operatørene opptatt. Med c_eff = 3 finnes en buffersone der operatørene kan jobbe solo før svikt inntreffer.

---

## 7.4 Bindingstidsestimat

Bindingstid defineres som den perioden operatørene er aktivt bundet til en hendelse, fra ankomsttidspunkt til operatørene er frigjort for neste hendelse. Modellen skiller mellom to undertyper av utrykning med kvalitativt ulik operativ dynamikk: **D-pri1** (pri-1-hendelser som bygningsbrann, trafikkulykke, farlig gods, makkerpar-bundet) og **D-aba** (utrykning utløst av automatisk brannalarm, serielt solo-håndtert). Skillet er forankret i operativ prosedyre og operatørintervjuer ved 110 Sør-Vest, og beskrives metodisk i avsnitt 5.3.

### 7.4.1 Avgrensning og datagrunnlag

Av 61 964 synlige oppdrag i datasettet har 7 555 (12,2 %) registrert tidspunkt for ressursvarsling. Disse splittes i 4 499 D-pri1 (7,3 %) og 3 056 D-aba (4,9 %) basert på om `Opprinnelig_oppdragstype` starter med «ABA» og `Kilde` = «Alarm». Hovedanalysen (variant A) avgrenses til disse hendelsene pluss sammenstilte tilleggsanrop (avsnitt 7.2) fordi de kan observeres robust.

Hendelser uten ressursvarsling er ikke irrelevante for dimensjonering. L-hendelse, L-aba, S, F og V belaster operatørkapasitet, men lar seg ikke modellere like robust. Variant B (avsnitt 8.3) inkluderer disse med operative bindingstidsestimater.

### 7.4.2 D-pri1: makkerpar-binding

For D-pri1-hendelser binder makkerparet (RØD og GUL) to operatører parallelt gjennom hele akuttfasen. Bindingstiden beregnes per hendelse som:

> **Bindingstid = (Dato/tid anrop → Første ressurs fremme) + 3 minutter kvitteringsvindu**

De tre minuttene reflekterer vindusmelding som må kvitteres og logges av GUL-operatør etter at første ressurs er på plass. Av de 4 499 D-pri1-oppdragene har 3 645 (81 %) gyldig tidspunkt for første ressurs fremme. Resterende 854 (19 %) tildeles median bindingstid fra de observerte verdiene.

**Tabell 7.3: Bindingstid per D-pri1-oppdrag, 110 Sør-Vest 2025 (inkl. +3 min kvittering)**

| Persentil | Bindingstid (min) |
|---|---|
| P25 | 11,2 |
| **Median** | **14,1** |
| Mean | 18,2 |
| P75 | 18,6 |
| P90 | 27,3 |

Både RØD og GUL er bundet parallelt gjennom hele akuttfasen:

- **0 til ~1 min:** RØD i samtale med innringer, GUL i medlytt og lokalisering
- **~1 til ~2 min:** GUL utalarmerer ressurser (ressurs varslet, median 83 sek for D-pri1), RØD fortsetter samtalen
- **~2 til ~11 min:** RØD i fortsatt innringerkontakt, GUL koordinerer samband og gir tidskritisk informasjon til mannskap underveis
- **~11 min:** Første ressurs fremme → vindusmelding
- **+3 min:** Kvittering og loggføring → GUL delvis frigjort

I den prosedyrebaserte modellen behandles D-pri1 som **to op-binder**: RØD og GUL aktiveres fra første sekund og forblir bundet i hele bindingstiden (median 14,1 min).

### 7.4.3 D-aba: serielt solo-håndtert med valgfri oppfølging

ABA-utrykninger er ikke pri-1-hendelser. Prosedyren krever ikke makkerpar fordi ABA ikke trippelvarsles, det gis ikke tidskritisk informasjon i BAPS, og operatøren som kvitterer alarmen er normalt den samme som oppretter oppdraget og utalarmerer ressurser (Rogaland brann og redning IKS, 2024). D-aba har derfor en vesentlig annen bindingsdynamikk enn D-pri1. Denne dynamikken modelleres i to faser:

**Fase 1: oppdragsopprettelse og call-out (alltid)**
Én operatør kvitterer ABA-signalet, oppretter oppdrag i LEO og utalarmerer ressurser. Empirisk observeres median 74 sekunder fra anrop til ressurs varslet for D-aba (P75 = 80 sek, P90 = 111 sek), konsistent med operativ beskrivelse av ca. 90 sekunder. Med etterfølgende registrering anslås Fase 1 til **3 minutter × 1 operatør**.

**Fase 2: nødtelefon og panel-veiledning (valgfri)**
Etter call-out kommer ofte en nødtelefon fra stedet, typisk innen 90 til 120 sekunder. Denne besvares av vilkårlig ledig operatør og inneholder vanligvis intervju med innringer, veiledning til brannpanel, områdeavklaring, og eventuelt tilbakestilling av alarm. Fase 2 modelleres som **1 operatør bundet i Y minutter, med sannsynlighet p, ankommer 90 sekunder etter Fase 1**. Sensitivitetsscenarioer: lav (p = 0,30, Y = 3 min), hoved (p = 0,50, Y = 6 min), høy (p = 0,70, Y = 10 min).

Empirisk underkant-estimat for p fra sekvensgap-metoden (sammenstilte anrop innen 90 sek til Δ min etter D-aba): 8,7 % ved 3 min, 16,7 % ved 5 min, 28,8 % ved 10 min. Dette fanger kun nødtelefoner med eget 110-ID; de som logges inni hovedoppdraget er usynlige. Operatørens kvalitative beskrivelse tilsier at reell andel ligger betydelig høyere, noe som støtter hoved-scenario på 50 %.

### 7.4.4 L-aba: empirisk kalibrert via dybdeanalyse (n=100)

Bindingstid for L-aba (ABA løst av 110 uten utrykning) ble empirisk kalibrert gjennom to runder med dybdeanalyse av stratifiserte L-aba-hendelser fra 2025 (metode i avsnitt 5.4). Runde 1 (n=49 totalt / n=30 Kilde=Alarm-subset) ga et orienteringsanslag på mean 5,88 min med betydelig usikkerhet (CI [3,70; 8,56]). Runde 2 (n=100, alle Kilde=Alarm) gir den endelige modellparameteren: **mean 4,53 min, 95 % CI [3,74; 5,43], median 3,27 min, P90 = 9,48 min**. Standardavvik 4,37 min reflekterer at fordelingen forblir høyreskjev, drevet av langhalede tilfeller (industrivern-oppfølging, varmekamera-avklaring), men terskelen for «høy bindingstid» er lavere enn antatt etter runde 1. Mean velges som hovedverdi.

Hovedscenario: **L-aba = 4,5 min × 1 operatør**. Sensitivitetsscenarioer: 3 min (CI-nedre), 7 min (over CI-øvre).

### 7.4.5 Oppsummering: op-binder per kategori

**Tabell 7.4: Op-binder-profil per hendelseskategori (hoved-scenario)**

| Kategori | N 2025 | Ops bundet | Bindingstid (min) | Kilde |
|---|---:|---:|---:|---|
| **D-pri1** | 4 499 | 2 | Median 14,1 (databasert) | BRIS |
| **D-aba Fase 1** | 3 056 | 1 | 3 (alltid) | Operativ prosedyre + BRIS |
| **D-aba Fase 2** | ~1 528 | 1 | 6 (p = 0,50) | Operatørinformert, LABA-dybdeanalyse |
| **S** (service) | 22 542 | 1 | 2 | Operativ estimat |
| **L-aba** | 3 430 | 1 | 4,5 | LABA-dybdeanalyse n=100 (mean 4,53) |
| **L-hendelse** | 4 298 | 1 | 5 | Operativ estimat |
| **L-ukjent** | 16 768 | 1 | 3 | Operativ estimat |
| **F** (feilring) | 6 824 | 1 | 0,5 | Operativ estimat |
| **V** (viderevarsling) | 547 | 1 | 1 | Operativ estimat |
| **Skjulte** | 18 901 | 1 | 1 | Sekvensgap-metode |

Figur 7.1 viser fordelingen av D-pri1-bindingstid og illustrerer det høyreskjeve mønsteret som ligger til grunn for valget av median (14,1 min) som hovedparameter for D-pri1 i primærmodellen. Den lange halen (P90 = 27,3 min) er det som driver Svikt-tilstander når en pri-1-hendelse strekker seg utover normaltid.

<div align="center">
  <img src="../analyse/figurer/bindingstid_beredskap_fordeling_v2.png" alt="Figur 7.1 Bindingstidsfordeling D-pri1" width="80%">
  <p align="center"><small><i>Figur 7.1: Fordeling av bindingstid per D-pri1-oppdrag (makkerpar-bundet). Median 14,1 min, høyreskjev fordeling.</i></small></p>
</div>

Dag- og nattskift viser tilnærmet lik D-pri1-bindingstid, noe som indikerer at bindingstiden primært drives av hendelsestype og geografi, ikke tidspunkt på døgnet.

---

Analysen i 7.1-7.4 etablerer den metodiske rammen og parametergrunnlaget for kapasitetsmodellen. Variant A og B, scenarioanalyse, sensitivitetsanalyse og bootstrap-CI presenteres som resultater i kap 8. Tolkningen av resultatene mot teori og praktiske implikasjoner skjer i kap 9.

---

