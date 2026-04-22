# 7. Analyse og resultater

## 7.1 Metodisk tilnærming: fra køteori til prosedyrbasert kapasitetsmodell

Den opprinnelige modellhypotesen i prosjektet var at Erlang-C (M/M/c) kunne brukes som hovedmodell for kapasitetsanalysen. Erlang-C estimerer sannsynligheten for at et innkommende anrop må vente, gitt ankomstrate (λ), gjennomsnittlig servicetid (μ⁻¹) og antall servere (c). Resultatene fra denne innledende analysen er presentert i Tabell 7.1 og inngår nå som **referansemodell** (baseline) som dokumenterer hvorfor klassisk køteori er utilstrekkelig for 110-konteksten — ikke som studiens hovedmodell. Den prosedyrbaserte ankomstkonfliktmodellen, utviklet i avsnitt 7.5 og formelt definert i kap 6.4, er studiens **hovedmodell** og originale bidrag.

Erlang-C-analysen viste svært lav systemutnyttelse, med høyeste observerte verdi 5,9 % (Dag/Helg) for alle skifttyper, noe som isolert sett kunne tyde på at bemanningsnivået er komfortabelt (se Tabell 7.1).

**Tabell 7.1: Erlang-C resultater — beredskapsoppdrag, 110 Sør-Vest 2025**

| Skifttype | λ (anrop/t) | c_eff | ρ = λ/(c·μ) | P(vente) | P(W > 30s) |
|---|---|---|---|---|---|
| Dag / Hverdag | 2,57 | 3 | 4,9 % | 0,05 % | 0,02 % |
| Dag / Helg | 2,06 | 2 | 5,9 % | 0,66 % | 0,38 % |
| Natt / Hverdag | 1,18 | 2 | 3,4 % | 0,22 % | 0,13 % |
| Natt / Helg | 1,30 | 2 | 3,7 % | 0,27 % | 0,15 % |

*Samtaletid (μ⁻¹): vektet gjennomsnitt 3,44 min basert på intervjudata (Anette, 2026). Merk: dette er samtaletiden brukt i Erlang-C, ikke den totale bindingstiden (median 13,0 min inkl. akuttfase og kvittering) som brukes i primærmodellen. λ inkluderer kun synlige beredskapsoppdrag fra BRIS/LEO — faktisk innkommende volum er høyere (se avsnitt 7.2). P(W > 30s): sannsynlighet for ventetid over 30 sekunder — terskelen for automatisk overføring til Agder ved ubesvart anrop (beredskapsanalyse J03 s. 25).*

Resultatene fra Erlang-C er formelt korrekte gitt inputparametrene, men metodisk utilstrekkelige for 110-konteksten. Årsaken er tredelt: modellen forutsetter at servere er *uavhengige* og *parallelle*, den behandler kapasitetsbinding utover samtaletid som null, og den baserer seg på en ankomstrate som undervurderer faktisk innkommende volum (se avsnitt 7.2). Gjennomgang av den operative prosedyren (Rogaland brann og redning IKS, 2024) avslørte at forutsetningen om én uavhengig server per anrop ikke stemmer med faktisk arbeidsmetodikk.

---

## 7.2 Synlig oppdragsvolum versus faktisk anropsvolum

En viktig begrensning ved BRIS/LEO-data er at statistikken viser synlige oppdrag, ikke nødvendigvis alle innkommende anrop. Når flere personer ringer om samme hendelse, blir tilleggsanropene sammenstilt med det eksisterende oppdraget og forsvinner som egne observasjoner i årsrapport og eksportdata.

For 2025 viser datasettet 61 964 synlige oppdrag, mens sekvensnummerlogikken i LEO indikerer et estimert faktisk anropsvolum på minst 80 865 anrop.

**Tabell 7.1b: Synlig versus faktisk anropsvolum — 110 Sør-Vest 2025**

| | Antall |
|---|---|
| Synlige oppdrag (BRIS/LEO) | 61 964 |
| Estimert faktisk anropsvolum | 80 865 |
| Skjulte/sammenstilte anrop | 18 901 |
| Korreksjonsfaktor | 1,305x |

Differansen på 18 901 anrop, tilsvarende 23,4 %, representerer ikke valgbare eller trivielle henvendelser, men faktiske innkommende anrop som beslaglegger operatørkapasitet. Korreksjonsfaktoren på 1,305x gjelder forholdet mellom synlige oppdrag og estimert totalt anropsvolum (ikke forholdet mellom kategori D og totale belastningsenheter i modellen). Faktoren varierer mellom måneder (størst i januar: 1,438x) og er generelt høyest ved dagtid på hverdager — nettopp der kapasitetspresset allerede er høyest.

Et ytterligere forbehold er at ikke alle tilleggsanrop faktisk blir sammenstilt med den aktive hendelsen de tilhører. Under høyt press og med flere operatører involvert hender det at anrop som operativt tilhører en pågående hendelse likevel lukkes som egne saker — med initiell hendelsestype som «service», «feilringing» eller «løst av 110» — i stedet for å bli tillagt det eksisterende oppdraget. Tilfeldig stikkprøvekontroll viser at anrop som kom inn som nødanrop kan bli lukket med slike kategorier. Disse anropene er i realiteten kritiske telefoner som må besvares, til forskjell fra faktiske servicehenvendelser som kan nedprioriteres. Konsekvensen er at estimatet på 18 901 sammenstilte anrop sannsynligvis er et underestimat av det faktiske antallet beredskapsrelaterte tilleggsanrop, noe som ytterligere forsterker modellens konservative karakter.

Dette har tre konsekvenser for analysen:

1. **Ankomstraten λ i Erlang-C er for lav.** En modell som bruker synlige oppdrag som grunnlag for λ vil systematisk undervurdere faktisk arbeidsbelastning. Selv en perfekt M/M/c-modell ville derfor vært basert på et ufullstendig inputgrunnlag.

2. **Sammenstilte anrop er modellert som egne belastningsenheter — men modellen er fortsatt konservativ.** I den prosedyrbaserte ankomstkonfliktmodellen (avsnitt 7.5, formell definisjon i kap 6.4.6) er de 18 901 estimerte sammenstilte anropene inkludert som egne op-binder-events med interpolert ankomsttidspunkt og bindingstid 1 minutt ($q = 1$, $d = 1$ min). De bidrar dermed til $n_{\text{aktive}}$ ved senere ankomster og kan utløse Brudd eller Svikt på samme måte som synlige oppdrag. Modellen er likevel konservativ av to grunner: (i) bindingstiden 1 min er et nedre estimat (faktisk varighet kan være lengre dersom innringer er stresset eller anropet håndteres som full hendelse), og (ii) sekvensgap-metoden fanger kun anrop som er sammenstilt med eksisterende oppdrag — beredskapsrelaterte anrop som er feilkategorisert og lukket som egne saker (f.eks. som «service» eller «feilringing» under høyt press) er fortsatt usynlige. Det reelle antallet beredskapsrelaterte tilleggsanrop er derfor sannsynligvis høyere enn 18 901.

3. **Skjult belastning påvirker dimensjonering direkte.** Sammenstilte tilleggsanrop påvirker ikke bare ankomstraten i køteoretisk forstand, men også den operative bindingen i den prosedyrbaserte modellen. Inkluderingen av skjulte anrop som egne op-binder-events (punkt 2) gjør at primærmodellen fanger denne effekten i variant A — men siden underestimatet av antall skjulte anrop fortsatt eksisterer, betyr det at modellens svikt- og brudd-andeler er nedre estimater. For dimensjonering tilsier dette at analyser basert utelukkende på oppdragsteller (uten skjult-anrop-korreksjon) systematisk vil undervurdere både arbeidsbelastning, samtidighetskonflikt og behovet for bufferkapasitet.

Skillet mellom synlig oppdragsvolum og faktisk anropsvolum viser at kapasitetsanalyse ikke kan ta utgangspunkt i registrerte saker alene. Det neste spørsmålet blir derfor ikke bare hvor mange oppdrag som finnes, men hvordan sentralens arbeidsmetodikk gjør at disse anropene binder operatører over tid.

---

## 7.3 Den operative arbeidsmetodikken som kapasitetsramme

Prosedyren definerer tre operative funksjoner som roterer dynamisk mellom operatørene:

- **Rød funksjon:** Operatøren som besvarer nødtelefonen, oppretter hendelse i LEO og gjennomfører intervju med innringer. Binder én operatør fullt ut i den aktive samtalefasen.
- **Gul funksjon:** Aktiveres samtidig med RØD — GUL-operatøren går umiddelbart i medlytt når RØD besvarer anropet, for å bygge situasjonsforståelse og avhjelpe med lokalisering. Etter den innledende medlyttfasen utalarmerer GUL ressurser, håndterer samband og gir tidskritisk informasjon til mannskap underveis, delvis fortsatt på medlytt. GUL forblir bundet frem til vindusmelding mottas om at første ressurs er fremme, pluss kvittering og loggføring (anslagsvis 3 minutter). Først etter dette er GUL delvis frigjort og kan håndtere flere gule hendelser parallelt i en mer sporadisk oppfølgingsfase.
- **Grønn funksjon:** Ledig — klar for neste nødanrop. Prosedyren definerer eksplisitt som målsetning at *«én operatør til enhver tid er ledig og kan ta nødtelefoner»*.
- **Vaktleder (VL):** Overordnet funksjon — oversikt, prioritering, pressehåndtering og innkalling. Prosedyren slår fast at *«vaktleder skal som et utgangspunkt ikke besvare nødanrop»*.

Den normale driftsformen er dermed et **makkerpar**: én rød og én gul operatør samarbeider om én hendelse, mens øvrige operatører er grønne og klare for neste anrop. Prosedyren definerer dette som normalstandarden, og understreker at *«tiden to operatører er involvert i samme hendelse gjøres så kort som mulig, for å raskt frigjøre kapasitet til neste hendelse»*.

### Kapasitetsnivåer utledet av prosedyren

Med utgangspunkt i prosedyrens rolledefinisjon etableres tre kapasitetsnivåer, som danner grunnlaget for den kvantitative analysen:

**Tabell 7.2: Kapasitetsnivåer — operativ tilpasningsmodell**

| Nivå | Definisjon | Betingelse | c_eff = 2 | c_eff = 3 |
|---|---|---|---|---|
| **Normal** | Makkerpar mulig for neste hendelse | ledige ≥ 2 | n_aktive = 0 | n_aktive ≤ 1 |
| **Brudd på driftsstandard** | Kun 1 ledig — solo-håndtering | ledige = 1 | n_aktive = 1 | n_aktive = 2 |
| **Svikt** | Ingen ledig operatør | ledige ≤ 0 | n_aktive ≥ 2 | n_aktive ≥ 3 |

*Ledige operatører = c_eff − n_aktive. Modellen speiler den operative virkeligheten: ved samtidskonflikter splittes makkerparet slik at operatørene fordeler seg. Med c_eff = 3 og 1 aktiv hendelse er det fortsatt 2 ledige (Normal) — den tredje operatøren kan ta neste hendelse med makkerpar. Brudd oppstår først når det kun er 1 ledig, og svikt når ingen er ledig.*

Tabellen bygger på en operativ tilpasningslogikk der makkerpar ikke nødvendigvis forblir fast låst til én hendelse gjennom hele akuttfasen. Ved c_eff = 3 og én aktiv hendelse er det fortsatt to tilgjengelige operatører, slik at neste hendelse i praksis kan tas med et nytt makkerpar. Brudd oppstår først når den neste hendelsen må håndteres med kun én ledig operatør, og svikt når ingen er ledige.

Den kritiske asymmetrien mellom c_eff = 2 og c_eff = 3 er at med c_eff = 2 er det kun étt steg fra normal drift til svikt: allerede ved andre samtidige hendelse er begge operatørene opptatt. Med c_eff = 3 finnes en buffersone der operatørene kan jobbe solo før svikt inntreffer.

---

## 7.4 Bindingstidsestimat

Bindingstid defineres som den perioden operatørene er aktivt bundet til en hendelse — fra ankomsttidspunkt til operatørene er frigjort for neste hendelse. Modellen skiller mellom to undertyper av utrykning med kvalitativt ulik operativ dynamikk: **D-pri1** (pri-1-hendelser som bygningsbrann, trafikkulykke, farlig gods — makkerpar-bundet) og **D-aba** (utrykning utløst av automatisk brannalarm — serielt solo-håndtert). Skillet er forankret i operativ prosedyre og operatørintervjuer ved 110 Sør-Vest, og beskrives metodisk i avsnitt 5.3.

### 7.4.1 Avgrensning og datagrunnlag

Av 61 964 synlige hendelser i datasettet har 7 555 (12,2 %) registrert tidspunkt for ressursvarsling. Disse splittes i 4 499 D-pri1 (7,3 %) og 3 056 D-aba (4,9 %) basert på om `Opprinnelig_oppdragstype` starter med «ABA» og `Kilde` = «Alarm». Hovedanalysen (variant A) avgrenses til disse hendelsene pluss sammenstilte tilleggsanrop (avsnitt 7.2) fordi de kan observeres robust.

Hendelser uten ressursvarsling er ikke irrelevante for dimensjonering. L-hendelse, L-aba, S, F og V belaster operatørkapasitet, men lar seg ikke modellere like robust. Variant B (avsnitt 7.7) inkluderer disse med operative bindingstidsestimater.

### 7.4.2 D-pri1: makkerpar-binding

For D-pri1-hendelser binder makkerparet (RØD og GUL) to operatører parallelt gjennom hele akuttfasen. Bindingstiden beregnes per hendelse som:

> **Bindingstid = (Dato/tid anrop → Første ressurs fremme) + 3 minutter kvitteringsvindu**

De tre minuttene reflekterer vindusmelding som må kvitteres og logges av GUL-operatør etter at første ressurs er på plass. Av de 4 499 D-pri1-oppdragene har 3 357 registrert tidspunkt for første ressurs fremme. Resterende tildeles median bindingstid fra de observerte verdiene.

**Tabell 7.3: Bindingstid per D-pri1-oppdrag — 110 Sør-Vest 2025 (inkl. +3 min kvittering)**

| Persentil | Bindingstid (min) |
|---|---|
| P25 | 11,2 |
| **Median** | **14,1** |
| Mean | 18,2 |
| P75 | 18,6 |
| P90 | 27,3 |

Både RØD og GUL er bundet parallelt gjennom hele akuttfasen:

- **0 – ~1 min:** RØD i samtale med innringer, GUL i medlytt og lokalisering
- **~1 – ~2 min:** GUL utalarmerer ressurser (ressurs varslet, median 83 sek for D-pri1), RØD fortsetter samtalen
- **~2 – ~11 min:** RØD i fortsatt innringerkontakt, GUL koordinerer samband og gir tidskritisk informasjon til mannskap underveis
- **~11 min:** Første ressurs fremme → vindusmelding
- **+3 min:** Kvittering og loggføring → GUL delvis frigjort

I den prosedyrebaserte modellen behandles D-pri1 som **to op-binder**: RØD og GUL aktiveres fra første sekund og forblir bundet i hele bindingstiden (median 14,1 min).

### 7.4.3 D-aba: serielt solo-håndtert med valgfri oppfølging

ABA-utrykninger er ikke pri-1-hendelser. Prosedyren krever ikke makkerpar fordi ABA ikke trippelvarsles, det gis ikke tidskritisk informasjon i BAPS, og operatøren som kvitterer alarmen er normalt den samme som oppretter oppdraget og utalarmerer ressurser (Rogaland brann og redning IKS, 2024). D-aba har derfor en vesentlig annen bindingsdynamikk enn D-pri1. Denne dynamikken modelleres i to faser:

**Fase 1 — oppdragsopprettelse og call-out (alltid)**
Én operatør kvitterer ABA-signalet, oppretter oppdrag i LEO og utalarmerer ressurser. Empirisk observeres median 74 sekunder fra anrop til ressurs varslet for D-aba (P75 = 80 sek, P90 = 111 sek) — konsistent med operativ beskrivelse av ca. 90 sekunder. Med etterfølgende registrering anslås Fase 1 til **3 minutter × 1 operatør**.

**Fase 2 — nødtelefon og panel-veiledning (valgfri)**
Etter call-out kommer ofte en nødtelefon fra stedet, typisk innen 90–120 sekunder. Denne besvares av vilkårlig ledig operatør og inneholder vanligvis intervju med innringer, veiledning til brannpanel, områdeavklaring, og eventuelt tilbakestilling av alarm. Fase 2 modelleres som **1 operatør bundet i Y minutter, med sannsynlighet p, ankommer 90 sekunder etter Fase 1**. Sensitivitetsscenarioer: lav (p = 0,30, Y = 3 min), hoved (p = 0,50, Y = 6 min), høy (p = 0,70, Y = 10 min).

Empirisk underkant-estimat for p fra sekvensgap-metoden (sammenstilte anrop innen 90 sek–Δ min etter D-aba): 8,7 % ved 3 min, 16,7 % ved 5 min, 28,8 % ved 10 min. Dette fanger kun nødtelefoner med eget 110-ID; de som logges inni hovedoppdraget er usynlige. Operatørens kvalitative beskrivelse tilsier at reell andel ligger betydelig høyere, noe som støtter hoved-scenario på 50 %.

### 7.4.4 L-aba: empirisk kalibrert via dybdeanalyse (n=100)

Bindingstid for L-aba (ABA løst av 110 uten utrykning) ble empirisk kalibrert gjennom to runder med dybdeanalyse av stratifiserte L-aba-hendelser fra 2025 (metode i avsnitt 5.4). Runde 1 (n=49 totalt / n=30 Kilde=Alarm-subset) ga et orienteringsanslag på mean 5,88 min med betydelig usikkerhet (CI [3,70; 8,56]). Runde 2 (n=100, alle Kilde=Alarm) gir den endelige modellparameteren: **mean 4,53 min, 95 % CI [3,74; 5,43], median 3,27 min, P90 = 9,48 min**. Standardavvik 4,37 min reflekterer at fordelingen forblir høyreskjev — drevet av langhalede tilfeller (industrivern-oppfølging, varmekamera-avklaring) — men terskelen for «høy bindingstid» er lavere enn antatt etter runde 1. Mean velges som hovedverdi.

Hovedscenario: **L-aba = 4,5 min × 1 operatør**. Sensitivitetsscenarioer: 3 min (CI-nedre), 7 min (over CI-øvre).

### 7.4.5 Oppsummering: op-binder per kategori

**Tabell 7.3b: Op-binder-profil per hendelseskategori (hoved-scenario)**

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

<div align="center">
  <img src="../analyse/figurer/bindingstid_beredskap_fordeling_v2.png" alt="Figur 7.1 Bindingstidsfordeling D-pri1" width="80%">
  <p align="center"><small><i>Figur 7.1: Fordeling av bindingstid per D-pri1-oppdrag (makkerpar-bundet). Median 14,1 min, høyreskjev fordeling.</i></small></p>
</div>

Dag- og nattskift viser tilnærmet lik D-pri1-bindingstid, noe som indikerer at bindingstiden primært drives av hendelsestype og geografi, ikke tidspunkt på døgnet.

---

## 7.5 Kapasitetsanalyse: variant A (beredskapsbelastning)

### Metode

For hvert beredskapsanrop måles hvor mange operatører som er bundet i pågående hendelser ved ankomsttidspunktet. Sweep-algoritmen akkumulerer *op-binder*, ikke bare antall aktive hendelser: D-pri1 bidrar med 2 op-binder gjennom bindingstiden, D-aba Fase 1 bidrar med 1 op-bind i 3 min, D-aba Fase 2 (med sannsynlighet p = 0,50) bidrar med 1 op-bind i 6 min, og skjulte anrop bidrar med 1 op-bind i 1 min. Kapasitetsnivå klassifiseres etter antall ledige operatører (avsnitt 6.4).

Skjulte anrop plasseres i tid via sekvensgap-metoden. Dersom oppdrag B06-250101-4 og B06-250101-6 er synlige, tildeles det manglende sekvensnummeret -5 tidspunkt fra nærmeste synlige oppdrag. Analysen fanger dermed den strukturelle effekten selv om eksakt ankomsttid for hvert skjult anrop er estimert.

Variant A omfatter:
- **D-pri1:** 4 499 oppdrag × 2 op-binder × median 14,1 min
- **D-aba Fase 1:** 3 056 × 1 op × 3 min (alltid)
- **D-aba Fase 2:** ~1 528 × 1 op × 6 min (sannsynlighet p = 0,50, offset + 1,5 min)
- **Skjulte anrop:** 18 901 × 1 op × 1 min

Totalt inngår 27 960 op-binder-events i sweep-en.

De sammenstilte tilleggsanropene er tildelt 1 minutts bindingstid — en konservativ antakelse som representerer at slike anrop er korte (operatøren kjenner allerede hendelsen), men likevel beslaglegger én operatør i et kritisk tidsvindu. Dersom reell gjennomsnittlig bindingstid er høyere, vil modellen undervurdere effekten.

### Hovedresultater

**Tabell 7.4: Kapasitetsnivå — variant A (beredskapsbelastning)**

| Skifttype | Normal | Brudd | Svikt | n |
|---|---:|---:|---:|---:|
| **Dag hverdag (c=3)** | 69,2 % | 15,9 % | 14,9 % | 15 944 |
| **Natt/helg (c=2)** | 46,9 % | 20,5 % | **32,6 %** | 12 016 |
| **Alle** | 59,6 % | 17,9 % | 22,5 % | 27 960 |

Modellen avslører en markant asymmetri mellom dag og natt. På dag hverdag (c=3) er 69,2 % av beredskapsanrop i Normal og 14,9 % i Svikt. På natt/helg (c=2) er Normal-andelen under halvparten (46,9 %), og hvert tredje anrop ankommer i Svikt-tilstand (32,6 %). Dette er en dobling av sviktraten fra dagskiftet — primært fordi c=2 gir null buffer når en pri-1-hendelse binder makkerparet.

### D-pri1 som primær svikt-driver

Den sterkeste enkeltdriveren for svikt er D-pri1-hendelser. På c=2 binder én aktiv D-pri1 hele operatørkapasiteten — begge ops er i makkerpar-rollen, og en ny beredskapsanrop i samme tidsvindu ankommer direkte i Svikt. D-aba derimot binder bare én op i Fase 1, slik at en D-aba-hendelse på natt/helg *tillater* en ny beredskapsanrop i parallell drift (Brudd, ikke Svikt).

Dette forklarer hvorfor Brudd-andelen er relativt lav (20,5 % på natt/helg) mens Svikt-andelen er høy: modellen differensierer strukturelt mellom lette og tunge beredskapsoppgaver, og pri-1-hendelser går direkte til Svikt-terskelen når c=2.

### Tolkning av svikt

«Svikt» i modellen betyr at ingen operatør er tilgjengelig ved ankomst av neste beredskapsanrop. Operativt kan situasjonen likevel håndteres — vaktleder (VL) kan tre inn, anropet kan overføres til Agder ved ubesvart innen 30 sek, eller operatørene kan jobbe raskere med redusert kvalitet (jf. kap 8.2). Modellen måler brudd på operativ driftsstandard, ikke brudd på tjenesten.

Resultatene i variant A er et minimumsanslag fordi ikke-D-kategorier ikke er inkludert. Total belastning med alle kategorier analyseres i avsnitt 7.7.

---

## 7.6 Scenarioanalyse: effekt av +1 operatør per skift

Scenarioet med én ekstra operatør per skift er en strukturtest av robusthet: hvilken effekt har en ekstra bufferressurs på sannsynligheten for brudd og svikt? Scenarioet øker c_eff fra 3 til 4 på dag hverdag og fra 2 til 3 på natt/helg.

**Tabell 7.5: Effekt av +1 operatør (variant A, beredskapsbelastning)**

| Skifttype | | Dagens bemanning | | +1 operatør | | |
|---|---|---|---|---|---|---|
| | Normal | Brudd | Svikt | Normal | Brudd | Svikt |
| **Dag hverdag** (3 → 4) | 69,2 % | 15,9 % | 14,9 % | **85,1 %** | **6,3 %** | **8,5 %** |
| **Natt/helg** (2 → 3) | 46,9 % | 20,3 % | 32,8 % | **67,2 %** | **16,1 %** | **16,7 %** |
| **Alle** | 59,6 % | 17,8 % | 22,5 % | **77,5 %** | **10,5 %** | **12,0 %** |

<div align="center">
  <img src="../analyse/figurer/scenario_pluss1_operator.png" alt="Scenario +1 operatør" width="95%">
  <p align="center"><small><i>Figur 7.4: Kapasitetsnivå ved dagens bemanning (3/2) vs +1 operatør (4/3). Solid søyle = dagens; halvgjennomsiktig med sort kant = +1 operatør.</i></small></p>
</div>

Tre funn:

**1. Natt/helg: sviktraten halveres.** Med +1 operatør øker Normal fra 46,9 % til 67,2 % (+20,3 pp). Svikt halveres fra 32,8 % til 16,7 %. Den ekstra operatøren gir den buffersonen som c=2 mangler — med c=3 kan én D-pri1 håndteres samtidig som c=2 fortsatt gir én ledig op, slik at pri-1-hendelser ikke lenger automatisk medfører Svikt.

**2. Dag hverdag: Normal opp til 85 %.** Normal øker fra 69,2 % til 85,1 %. Svikt halveres fra 14,9 % til 8,5 %. Effekten er mindre dramatisk enn på natt/helg fordi c=3 allerede gir buffer, men en fjerde operatør fjerner nesten all Svikt-risiko fra kombinasjonen av samtidig D-pri1 og lett bakgrunnsbelastning.

**3. Selv med +1 er sviktraten ikke null.** 12 % samlet svikt viser at kapasitetsproblemer ikke elimineres med én ekstra operatør — de reduseres vesentlig. Residualen skyldes perioder med to samtidige D-pri1-hendelser eller kombinasjoner av D-pri1 med mange bakgrunnshenvendelser.

Scenarioanalysen viser den strukturelle effekten av økt bufferkapasitet, men sier ikke alene hvordan en eventuell bemanningsøkning bør organiseres i praksis. Det er for eksempel ikke gitt at alle timer trenger samme økning, eller at effekten er lik med ulik kompetansesammensetning. Resultatene bør derfor forstås som et analytisk beslutningsgrunnlag, ikke som en ferdig ressurs- eller turnusløsning.

---

### Oppsummering av modellantakelser

**Tabell 7.6: Modellantakelser og parametere**

| Parameter | Verdi | Kilde |
|---|---|---|
| Bindingstid D-pri1 | Observert fra BRIS + 3 min kvittering | Median 14,1 min |
| Op-binder D-pri1 | 2 (makkerpar) | Operativ prosedyre |
| Bindingstid D-aba Fase 1 | 3 min | Operativ prosedyre + BRIS (median 74 sek call-out) |
| Bindingstid D-aba Fase 2 | 6 min (hoved) | Operatørinformert, sensitivitet 3/6/10 min |
| Sannsynlighet D-aba Fase 2 (p) | 0,50 (hoved) | Operatørestimert, sensitivitet 0,30/0,50/0,70 |
| Bindingstid L-aba | 4,5 min | LABA-dybdeanalyse n=100 mean (Kilde=Alarm-subset) |
| Bindingstid skjulte anrop | 1 min | Operativ vurdering |
| Kapasitetsnivå: Normal | ledige ≥ 2 | Makkerpar mulig |
| Kapasitetsnivå: Brudd | ledige = 1 | Solo-håndtering |
| Kapasitetsnivå: Svikt | ledige ≤ 0 | VL/Agder |
| c_eff dag hverdag | 3 (4 tot. − 1 VL) | Prosedyre |
| c_eff natt/helg | 2 (3 tot. − 1 VL) | Prosedyre |
| Skjulte anrop identifisert via | Sekvensgap i 110_ID | 18 901 stk |

---

## 7.7 Total operativ belastning (variant B)

### 7.7.1 Bakgrunn

Primærmodellen (variant A) kvantifiserer kapasitetsnivå basert på beredskapsoppdrag (D-pri1, D-aba) og sammenstilte anrop. Dette gir et presist bilde av beredskapskapasiteten, men dekker kun 27 960 av estimert 80 865 anrop. Variant B utvider analysen til å inkludere alle hendelseskategorier (se avsnitt 6.5) for å kvantifisere den samlede operative belastningen.

### 7.7.2 Resultater: beredskapsbelastning versus total belastning

**Tabell 7.7: Variant A (beredskap) vs Variant B (total) — hovedscenario**

| Skifttype | | Variant A (beredskap) | | | Variant B (total) | |
|---|---|---|---|---|---|---|
| | Normal | Brudd | Svikt | Normal | Brudd | Svikt |
| **Dag hverdag** (c=3) | 69,2 % | 15,9 % | 14,9 % | **59,5 %** | **19,0 %** | **21,6 %** |
| **Natt/helg** (c=2) | 46,9 % | 20,5 % | 32,6 % | **44,8 %** | **22,0 %** | **33,2 %** |
| **Alle** | 59,6 % | 17,9 % | 22,5 % | **53,9 %** | **20,1 %** | **25,9 %** |

<div align="center">
  <img src="../analyse/figurer/total_belastning_A_vs_B.png" alt="Variant A vs B" width="95%">
  <p align="center"><small><i>Figur 7.5: Variant A (beredskapsbelastning) vs Variant B (total operativ belastning), hovedscenario.</i></small></p>
</div>

Bakgrunnsbelastningen slår hardest på **dagtid**: Normal-andelen faller knapt 10 prosentpoeng (fra 69,2 % til 59,5 %) og svikt øker fra 14,9 % til 21,6 %. Dette er konsistent med at servicevolumet (22 542 overføringstester per år) er konsentrert på dagtid når servicevirksomhet pågår. Natt/helg påvirkes i mindre grad (Normal faller 2,1 pp, Svikt stiger 0,6 pp) fordi bakgrunnsvolumet er lavere — men utgangspunktet er allerede kritisk: Svikt-andelen på natt/helg er 33,2 % i variant B (mot 32,6 % i variant A).

Funnet understreker at operatørene på dagtid ikke bare håndterer beredskap — de håndterer en kontinuerlig strøm av servicetester, avklaringer og feilringinger som binder kapasitet mellom beredskapsoppdragene. Med gjennomsnittlig ~10 bakgrunnshenvendelser per time på dagskift er operatørene sjelden reelt ledige selv i perioder uten beredskapsoppdrag.

### 7.7.3 Sensitivitetsanalyse: robusthet mot bindingstidsantakelser

Bindingstidene for ikke-D-kategorier og D-aba Fase 2-parametrene er operative estimater (D-aba Fase 2) og delvis empirisk kalibrerte (L-aba via dybdeanalyse). For å teste robustheten kjøres modellen med tre scenarioer (se avsnitt 6.5.3). Både (p, Y) for D-aba Fase 2 og bindingstider for L-aba/L-hendelse/L-ukjent/S/F/V varieres samtidig fra lav til høy.

**Tabell 7.8: Sensitivitetsanalyse — variant B med tre scenarioer**

| Scenario | Dag hverdag (c=3) | | | Natt/helg (c=2) | | |
|---|---|---|---|---|---|---|
| | Normal | Brudd | Svikt | Normal | Brudd | Svikt |
| **A (beredskap)** | 69,2 % | 15,9 % | 14,9 % | 46,9 % | 20,5 % | 32,6 % |
| **B lav** | 68,8 % | 16,6 % | 14,6 % | 51,1 % | 18,8 % | 30,1 % |
| **B hoved** | 59,5 % | 19,0 % | 21,6 % | 44,8 % | 22,0 % | 33,2 % |
| **B høy** | 45,3 % | 21,0 % | 33,7 % | 38,1 % | 24,2 % | 37,7 % |

<div align="center">
  <img src="../analyse/figurer/total_belastning_sensitivitet.png" alt="Sensitivitetsanalyse" width="90%">
  <p align="center"><small><i>Figur 7.6: Sensitivitetsanalyse — effekt av bindingstidsantakelser på kapasitetsnivå.</i></small></p>
</div>

Tre observasjoner:

**1. Selv lavt scenario viser merkbar bakgrunnseffekt.** Med minimale bindingstider (Service 1 min, L-aba 3 min, feilringing 15 sek, D-aba Fase 2 kun for 30 % med Y = 3 min) er dag-hverdag-resultatet nesten uendret fra variant A (Normal 68,8 vs 69,2 %). På natt/helg gir lav-scenarioet faktisk litt bedre Normal (51 %) enn variant A (47 %) — D-aba Fase 2 slås mindre til når p = 0,30. Dette bekrefter at variant A-resultatet ikke er avhengig av optimistiske antakelser.

**2. Hovedscenario gir vesentlig kapasitetsforverring på dagtid.** Normal faller til 59,5 % og svikt øker til 21,6 %. Dagskiftet, som i variant A framstår som komfortabelt (69 % Normal), blir klart mer presset når hele arbeidsvolumet inkluderes.

**3. Høyt scenario illustrerer bristepunktet.** Med bindingstider i øvre sjikt (Service 4 min, L-aba 9 min, D-aba Fase 2 p = 0,70 og Y = 10 min) faller Normal under 50 % på dag — operatørene er oftere i Brudd eller Svikt enn i normal drift. For natt/helg når Svikt 38 %. Dette representerer dager med tungt servicevolum, uerfarne operatører, eller stor andel ABA-hendelser med oppfølgende nødtelefon.

**Konklusjon:** Hovedfunnet — at natt/helg har 30–38 % Svikt uavhengig av bindingstidsantakelser — er robust over hele spennet. Dimensjoneringsproblemet på natt/helg kan ikke forklares bort gjennom alternative parametervalg.

---

## 7.8 Generaliserbarhet

Den konkrete analysen er gjennomført på data fra 110 Sør-Vest, men modellrammeverket er utviklet for å kunne anvendes sentralsvis på alle norske 110-sentraler. Det sentrale er ikke de eksakte prosentverdiene i denne studien, men metoden for å identifisere hvor ofte en ny hendelse ankommer i en tilstand der tilgjengelig operatørkapasitet allerede er bundet.

Andre sentraler kan bruke samme analyseopplegg dersom de har tilgang til:
- Ankomsttidspunkt for hendelser
- Tidspunkt for ressursvarsling (identifiserer kategori D)
- En proxy for akuttfasens varighet (første ressurs fremme eller tilsvarende)
- Eventuelt indikatorer på sammenstilte tilleggsanrop for korreksjon av ankomstrate

Forutsatt felles klassifiseringsregler (V3-regelen, jf. avsnitt 5.3.2) og tilstrekkelig datatilgang er metoden teknisk overførbar til alle 12 sentraler. De normative implikasjonene — om dette bør utgjøre grunnlag for en nasjonal dimensjoneringsstandard — drøftes i kap 8.3 og 9.3.

---

## 7.9 Sammenstilling og tolkning

Analysen dokumenterer fem hovedfunn:

**Funn 1: Erlang-C alene er utilstrekkelig for 110-dimensjonering.**
Den tradisjonelle køteoretiske modellen gir svært lav systemutnyttelse (høyeste observerte verdi 5,9 %) og P(W > 30s) < 0,5 % for alle skifttyper. Modellen behandler operatører som uavhengige servere, fanger ikke kapasitetstapet ved makkerpar-kravet for pri-1-hendelser, differensierer ikke mellom ulike hendelsesdynamikker, og baserer seg på en ankomstrate fra synlige oppdrag som undervurderer faktisk innkommende volum med anslagsvis 23 %.

**Funn 2: D-pri1 og D-aba har fundamentalt ulik operativ dynamikk.**
Pri-1-hendelser (bygningsbrann, trafikkulykke, farlig gods) binder makkerparet (RØD og GUL) parallelt i median 14,1 min. ABA-utrykninger er ikke pri-1 og håndteres serielt av én operatør i 3 min (oppdragsopprettelse + call-out), med valgfri oppfølgingsfase for nødtelefon og panel-veiledning. For 110 Sør-Vest 2025 utgjør D-pri1 59 % (4 499) og D-aba 41 % (3 056) av utrykningshendelsene. Differensieringen er avgjørende for korrekt kapasitetsmodellering — uten den ville modellen antatt at en ABA-utrykning binder makkerparet tilsvarende en bygningsbrann, noe som er operativt feil.

**Funn 3: Natt/helg er strukturelt sårbar — Svikt ved hvert tredje beredskapsanrop.**
På natt/helg (c=2) er 32,6 % av beredskapsanropene i Svikt-tilstand og kun 46,9 % i Normal. Svikt-raten skyldes primært at én aktiv D-pri1-hendelse binder hele makkerparet, slik at en ny beredskapsanrop i samme tidsvindu ankommer uten ledig op. D-aba bidrar relativt mindre til Svikt fordi serial-håndteringen etterlater 1 op ledig. Resultatene er robust på tvers av D-aba-parameterscenarioer (Svikt 30–38 % i sensitivitetsspennet).

**Funn 4: +1 operatør per skift halverer sviktraten på natt/helg.**
Én ekstra operatør (c_eff 2→3 natt/helg, 3→4 dag) øker Normal fra 46,9 % til 67,2 % på natt/helg (+20,3 pp) og reduserer Svikt fra 32,8 % til 16,7 % (jf. Tabell 7.5 — scenarioets baseline 32,8 % skyldes annen tilfeldig D-aba Fase 2-realisasjon enn primærmodellens 32,6 %; differansen er innenfor stokastisk støy). På dag hverdag øker Normal fra 69,2 % til 85,1 %. Den strukturelle forbedringen er størst på natt/helg fordi c=3 endrer kapasitetsdynamikken kvalitativt: D-pri1 binder fortsatt 2 ops men etterlater 1 ledig op, slik at pri-1-hendelser ikke lenger automatisk medfører Svikt. Analysen indikerer at bemanningsstrukturen er en mer direkte driver for kapasitetsbildet enn samlet synlig oppdragsvolum alene.

**Funn 5: Total operativ belastning forverrer dagkapasiteten merkbart.**
Når alle hendelseskategorier inkluderes (variant B), faller Normal-andelen på dag hverdag fra 69,2 % til 59,5 % (−9,7 pp) og Svikt øker fra 14,9 % til 21,6 %. Effekten skyldes primært servicevolumet (22 542 overføringstester) konsentrert på dagtid. Natt/helg påvirkes i mindre grad fordi bakgrunnsvolumet er lavere. Sensitivitetsanalysen viser at denne forverringen er robust: selv med minimale bindingstidsantakelser (variant B lav) er natt/helg Svikt 30,1 %. Funnet understreker at beredskapskapasiteten ikke kan vurderes isolert fra den samlede arbeidsbyrden.

Sammenstillingen over presenterer fem hovedfunn som rene resultater. Tolkningen av funnene mot dimensjoneringspraksis, parallellen til dimensjoneringsforskriften for brannvesen, og de praktiske implikasjonene drøftes i kap 8 (særlig 8.3) og kap 9.

---

*Skript for analyser og figurer: `analyse/scripts/konflikt_total_belastning.py` (variant A og B), `analyse/scripts/scenario_pluss1.py` (scenario +1 op), `analyse/scripts/bindingstid_analyse.py`, `analyse/scripts/uttrekk_laba_sorvest.py` (LABA-dybdeanalyse).*
*Metodedokumentasjon: `analyse/notat_V3_modellutvikling.md` (parameterkalibrering, beslutningslogikk).*
*Data: `004 data/110 SØR VEST TESTDATASETT.xlsx` (BRIS 2025, 61 964 synlige oppdrag, 7 555 beredskapsoppdrag fordelt på 4 499 D-pri1 og 3 056 D-aba).*
*Prosedyreferanse: Rogaland brann og redning IKS (2024). Prosedyre arbeidsmetodikk, utalarmering og loggføring, versjon 4, 16.12.2024.*
