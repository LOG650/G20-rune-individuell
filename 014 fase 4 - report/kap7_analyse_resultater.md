# 7. Analyse og resultater

## 7.1 Metodisk tilnærming: fra køteori til prosedyrbasert kapasitetsmodell

Den opprinnelige modellhypotesen i prosjektet var at Erlang-C (M/M/c) kunne brukes som hovedmodell for kapasitetsanalysen. Erlang-C estimerer sannsynligheten for at et innkommende anrop må vente, gitt ankomstrate (λ), gjennomsnittlig servicetid (μ⁻¹) og antall servere (c). Resultatene fra denne innledende analysen er presentert i Tabell 7.1 og inngår nå som **referansemodell** (baseline) som dokumenterer hvorfor klassisk køteori er utilstrekkelig for 110-konteksten — ikke som studiens hovedmodell. Den prosedyrbaserte ankomstkonfliktmodellen, utviklet i avsnitt 7.5 og formelt definert i kap 6.4, er studiens **hovedmodell** og originale bidrag.

Erlang-C-analysen viste svært lav systemutnyttelse, med høyeste observerte verdi 5,9 % (Dag/Helg) for alle skifttyper, noe som isolert sett kunne tyde på at bemanningsnivået er komfortabelt (se Tabell 7.1).

Kapitlet svarer på forskningsspørsmålene slik: RQ1 behandles i avsnitt 7.1–7.2, RQ2 i 7.4, RQ3 i 7.5–7.7, RQ4 i 7.8 og RQ5 i 7.9–7.10. Avsnitt 7.11 samler hovedfunnene uten å innføre nye resultater.

**Tabell 7.1: Erlang-C resultater — beredskapsoppdrag, 110 Sør-Vest 2025**

| Skifttype | λ (anrop/t) | c_eff | ρ = λ/(c·μ) | P(vente) | P(W > 30s) |
|---|---|---|---|---|---|
| Dag / Hverdag | 2,57 | 3 | 4,9 % | 0,05 % | 0,02 % |
| Dag / Helg | 2,06 | 2 | 5,9 % | 0,66 % | 0,38 % |
| Natt / Hverdag | 1,18 | 2 | 3,4 % | 0,22 % | 0,13 % |
| Natt / Helg | 1,30 | 2 | 3,7 % | 0,27 % | 0,15 % |

*Samtaletid (μ⁻¹): vektet gjennomsnitt 3,44 min basert på operative valideringssamtaler (avsnitt 5.2.4). Merk: dette er samtaletiden brukt i Erlang-C, ikke den totale bindingstiden (median 13,0 min inkl. akuttfase og kvittering) som brukes i primærmodellen. λ inkluderer kun synlige beredskapsoppdrag fra BRIS/LEO — faktisk innkommende volum er høyere (se avsnitt 7.2). P(W > 30s): sannsynlighet for ventetid over 30 sekunder — terskelen for automatisk overføring til Agder ved ubesvart anrop (beredskapsanalyse J03 s. 25).*

Resultatene fra Erlang-C er formelt korrekte gitt inputparametrene, men metodisk utilstrekkelige for 110-konteksten. Årsaken er tredelt: modellen forutsetter at servere er *uavhengige* og *parallelle*, den behandler kapasitetsbinding utover samtaletid som null, og den baserer seg på en ankomstrate som undervurderer faktisk innkommende volum (se avsnitt 7.2). Gjennomgang av den operative prosedyren (Rogaland brann og redning IKS, 2024) avslørte at forutsetningen om én uavhengig server per anrop ikke stemmer med faktisk arbeidsmetodikk.

---

## 7.2 Synlig oppdragsvolum versus faktisk anropsvolum

En viktig begrensning ved BRIS/LEO-data er at statistikken viser synlige oppdrag, ikke nødvendigvis alle innkommende anrop. Når flere personer ringer om samme hendelse, blir tilleggsanropene sammenstilt med det eksisterende oppdraget og forsvinner som egne observasjoner i årsrapport og eksportdata.

For 2025 viser datasettet 61 964 synlige oppdrag, mens sekvensnummerlogikken i LEO indikerer et estimert faktisk anropsvolum på minst 80 865 anrop.

**Tabell 7.2: Synlig versus faktisk anropsvolum — 110 Sør-Vest 2025**

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

**Tabell 7.3: Kapasitetsnivåer — operativ tilpasningsmodell**

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

Av 61 964 synlige oppdrag i datasettet har 7 555 (12,2 %) registrert tidspunkt for ressursvarsling. Disse splittes i 4 499 D-pri1 (7,3 %) og 3 056 D-aba (4,9 %) basert på om `Opprinnelig_oppdragstype` starter med «ABA» og `Kilde` = «Alarm». Hovedanalysen (variant A) avgrenses til disse hendelsene pluss sammenstilte tilleggsanrop (avsnitt 7.2) fordi de kan observeres robust.

Hendelser uten ressursvarsling er ikke irrelevante for dimensjonering. L-hendelse, L-aba, S, F og V belaster operatørkapasitet, men lar seg ikke modellere like robust. Variant B (avsnitt 7.7) inkluderer disse med operative bindingstidsestimater.

### 7.4.2 D-pri1: makkerpar-binding

For D-pri1-hendelser binder makkerparet (RØD og GUL) to operatører parallelt gjennom hele akuttfasen. Bindingstiden beregnes per hendelse som:

> **Bindingstid = (Dato/tid anrop → Første ressurs fremme) + 3 minutter kvitteringsvindu**

De tre minuttene reflekterer vindusmelding som må kvitteres og logges av GUL-operatør etter at første ressurs er på plass. Av de 4 499 D-pri1-oppdragene har 3 357 registrert tidspunkt for første ressurs fremme. Resterende tildeles median bindingstid fra de observerte verdiene.

**Tabell 7.4: Bindingstid per D-pri1-oppdrag — 110 Sør-Vest 2025 (inkl. +3 min kvittering)**

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

**Tabell 7.5: Op-binder-profil per hendelseskategori (hoved-scenario)**

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

Figur 7.1 viser fordelingen av D-pri1-bindingstid og illustrerer det høyreskjeve mønsteret som ligger til grunn for valget av median (14,1 min) som hovedparameter. Den lange halen — P90 = 27,3 min — er det som driver Svikt-tilstander når en pri-1-hendelse strekker seg utover normaltid.

<div align="center">
  <img src="../analyse/figurer/bindingstid_beredskap_fordeling_v2.png" alt="Figur 7.1 Bindingstidsfordeling D-pri1" width="80%">
  <p align="center"><small><i>Fordeling av bindingstid per D-pri1-oppdrag (makkerpar-bundet). Median 14,1 min, høyreskjev fordeling.</i></small></p>
</div>

Dag- og nattskift viser tilnærmet lik D-pri1-bindingstid, noe som indikerer at bindingstiden primært drives av hendelsestype og geografi, ikke tidspunkt på døgnet.

---

## 7.5 Kapasitetsanalyse: variant A (beredskapsbelastning)

### Hva modellen måler i 7.5

Før resultatene presenteres er det viktig å være presis på *hva modellen kvantifiserer*. Erlang-C i Tabell 7.1 målte sannsynligheten for at et nytt anrop må stå i kø — en *ventetidsmetrikk*. Kapasitetsmodellen i 7.5–7.7 måler noe annet: sannsynligheten for at et nytt beredskapsanrop ankommer i en tilstand der den operative driftsstandarden (makkerpar) ikke kan opprettholdes. Det er en *prosedyrkonformitetsmetrikk*.

Forskjellen er substansiell. Erlang-C-ventetiden på 30 sek kan være 0 % selv når Svikt-andelen er 30 % — anropet kan besvares momentant av VL eller en operatør som forlater makker-rollen, men i begge tilfellene er den prosedyrekrevde driftsstandarden brutt. Modellen kvantifiserer altså *brudd på driftsstandarden ved ankomst*, ikke *brudd på tjenesteleveransen*.

De tre nivåene i Normal/Brudd/Svikt-klassifiseringen er definert i kap 6.4 og oppsummert her:

- **Normal** (ledige ≥ 2): Makkerpar er mulig for det nye anropet — full prosedyre kan følges.
- **Brudd på driftsstandard** (ledige = 1): Solo-håndtering er operativt mulig, men uten makker — redusert kvalitetssikring (jf. Antagelse A7 i Tabell 6.3 og diskusjonen i kap 8.2).
- **Svikt** (ledige ≤ 0): Ingen ledig operatør for makkerpar-binding. Anropet håndteres av VL, ved overflyt til Agder, eller ved at en operatør forlater pågående hendelse for å besvare det nye.

I alle tre tilfellene besvares anropet i praksis. Modellen sier ikke at tjenesten kollapser ved 32,6 % Svikt — den sier at driftsstandarden ikke kan opprettholdes for hvert tredje beredskapsanrop på natt/helg. Den operative kostnaden av å bryte standarden bæres i dag av operatørene gjennom kvalitetsreduksjon (kap 3.8 og 8.2).

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

**Tabell 7.6: Kapasitetsnivå — variant A (beredskapsbelastning)**

| Skifttype | Normal | Brudd | Svikt | n |
|---|---:|---:|---:|---:|
| **Dag hverdag (c=3)** | 69,2 % | 15,9 % | 14,9 % | 15 944 |
| **Natt/helg (c=2)** | 46,9 % | 20,5 % | **32,6 %** | 12 016 |
| **Alle** | 59,6 % | 17,9 % | 22,5 % | 27 960 |

Tallene er punktestimater under hovedscenario-antagelsene i Tabell 7.8. Scenariospennet (variant B lav/hoved/høy, jf. Tabell 7.10) viser at Svikt-andelen på natt/helg holder seg innenfor ca. 30–38 % over hele parameterspennet — tallet 32,6 % skal derfor leses som et midtestimat med scenariobånd, ikke som en punktmåling.

Modellen avslører en markant asymmetri mellom dag og natt. På dag hverdag (c=3) er 69,2 % av beredskapsanrop i Normal og 14,9 % i Svikt. På natt/helg (c=2) er Normal-andelen under halvparten (46,9 %), og hvert tredje anrop ankommer i Svikt-tilstand (32,6 %, scenariobånd 30–38 %). Dette er en dobling av sviktraten fra dagskiftet — primært fordi c=2 gir null buffer når en pri-1-hendelse binder makkerparet.

**Hva tallet faktisk måler.** Svikt 32,6 % betyr at i 32,6 % av beredskapsanropene var det ingen ledig operatør for makkerpar-binding ved ankomsttidspunktet. Det betyr **ikke** at anropet ble ubesvart. Vaktleder (VL) kan tre inn, kvalitet reduseres ved solo-håndtering, eller anropet overføres til Agder etter 30-sek-regelen. Modellen måler brudd på driftsstandarden (makkerpar-tilgjengelighet), ikke brudd på tjenesteleveransen. Tolkningen av forskjellen mellom de to drøftes i kap 8.2.

### D-pri1 som primær svikt-driver

Den sterkeste enkeltdriveren for svikt er D-pri1-hendelser. På c=2 binder én aktiv D-pri1 hele operatørkapasiteten — begge ops er i makkerpar-rollen, og en ny beredskapsanrop i samme tidsvindu ankommer direkte i Svikt. D-aba derimot binder bare én op i Fase 1, slik at en D-aba-hendelse på natt/helg *tillater* en ny beredskapsanrop i parallell drift (Brudd, ikke Svikt).

Dette forklarer hvorfor Brudd-andelen er relativt lav (20,5 % på natt/helg) mens Svikt-andelen er høy: modellen differensierer strukturelt mellom lette og tunge beredskapsoppgaver, og pri-1-hendelser går direkte til Svikt-terskelen når c=2.

### Tolkning av svikt

«Svikt» i modellen betyr at ingen operatør er tilgjengelig for makkerpar-binding ved ankomst av neste beredskapsanrop. Operativt kan situasjonen likevel håndteres — vaktleder (VL) kan tre inn, anropet kan overføres til Agder ved ubesvart innen 30 sek, eller operatørene kan jobbe raskere med redusert kvalitet (jf. kap 8.2). Modellen måler brudd på operativ driftsstandard, ikke brudd på tjenesten.

Resultatene i variant A er et minimumsanslag fordi ikke-D-kategorier ikke er inkludert. Total belastning med alle kategorier analyseres i avsnitt 7.7.

### Alternative tolkninger og forbehold

Tallene i Tabell 7.6 forutsetter at modellen fanger den faktiske operative dynamikken. Tre alternative tolkninger bør vurderes før resultatene leses som dokumenterte funn:

1. **Registreringspraksis i BRIS:** Hvis sammenstilling av anrop er ufullstendig eller systematisk skjev (jf. avsnitt 5.3.4 og 7.2), kan både ankomstrate og bindingstid være feilestimert. Sekvensgap-metoden er validert lokalt, men ikke uavhengig revidert.
2. **VL-rollen i praksis:** Modellen forutsetter $c_{\text{eff}} = c_{\text{total}} - 1$. Hvis VL i praksis besvarer en større andel nødanrop enn antatt (særlig under press), er den reelle Svikt-andelen lavere enn modellen viser.
3. **Bindingstidsantagelser:** D-pri1-bindingstid er empirisk (median 14,1 min), men L-aba, S, F, V og L-hendelse hviler på operative anslag. Sensitivitetsspennet (Tabell 7.10) viser at hovedfunnet er robust, men forutsetter at båndet er bredt nok til å fange den reelle usikkerheten.

Disse forbeholdene reflekteres i scenariobåndene som følger hovedtallene.

---

## 7.6 Scenarioanalyse: effekt av +1 operatør per skift

Scenarioet med én ekstra operatør per skift er en strukturtest av robusthet: hvilken effekt har en ekstra bufferressurs på sannsynligheten for brudd og svikt? Scenarioet øker c_eff fra 3 til 4 på dag hverdag og fra 2 til 3 på natt/helg.

**Tabell 7.7: Effekt av +1 operatør (variant A, beredskapsbelastning)**

| Skifttype | | Dagens bemanning | | +1 operatør | | |
|---|---|---|---|---|---|---|
| | Normal | Brudd | Svikt | Normal | Brudd | Svikt |
| **Dag hverdag** (3 → 4) | 69,2 % | 15,9 % | 14,9 % | **85,1 %** | **6,3 %** | **8,5 %** |
| **Natt/helg** (2 → 3) | 46,9 % | 20,3 % | 32,8 % | **67,2 %** | **16,1 %** | **16,7 %** |
| **Alle** | 59,6 % | 17,8 % | 22,5 % | **77,5 %** | **10,5 %** | **12,0 %** |

Figur 7.2 visualiserer skiftet i kapasitetsnivå når en ekstra operatør legges til på hvert skift. Hovedpoenget å se etter er **Normal-økningen på natt/helg** — søylen på venstre side går fra 47 % til 67 % — og den tilhørende reduksjonen i Svikt fra ca. 33 % til ca. 17 %. Effekten er strukturelt drevet av at c=3 endrer hva som skjer når én D-pri1 er aktiv (jf. neste tre punkter).

<div align="center">
  <img src="../analyse/figurer/scenario_pluss1_operator.png" alt="Scenario +1 operatør" width="95%">
  <p align="center"><small><i>Kapasitetsnivå ved dagens bemanning (3/2) vs +1 operatør (4/3). Solid søyle = dagens; halvgjennomsiktig med sort kant = +1 operatør.</i></small></p>
</div>

Tallene i Tabell 7.7 er punktestimater under hovedscenarioets antagelser, men retningen — at +1 op reduserer Svikt vesentlig — er robust gjennom hele parameterspennet i Tabell 7.10. Reduksjonens *størrelse* er derimot mer usikker enn punkttallet antyder: med D-aba Fase 2 trukket fra en annen stokastisk realisasjon enn primærmodellen er baseline for scenarioet 32,8 % (mot primærmodellens 32,6 %; differansen er innenfor stokastisk støy).

Tre observasjoner:

**1. Natt/helg: sviktraten halveres under hovedantagelsene.** Med +1 operatør øker Normal fra 46,9 % til 67,2 % (+20,3 pp), og Svikt reduseres fra ca. 33 % til 16,7 % (begge under hovedscenario). Den ekstra operatøren gir den buffersonen som c=2 mangler — med c=3 kan én D-pri1 håndteres samtidig som det fortsatt gir én ledig op, slik at pri-1-hendelser ikke lenger automatisk medfører Svikt. Halveringen er en modellprediksjon, ikke en validert effekt av faktisk bemanningsendring.

**2. Dag hverdag: Normal opp til 85 %.** Normal øker fra 69,2 % til 85,1 %. Svikt halveres fra 14,9 % til 8,5 %. Effekten er mindre markant enn på natt/helg fordi c=3 allerede gir buffer, men en fjerde operatør fjerner nesten all Svikt-risiko fra kombinasjonen av samtidig D-pri1 og lett bakgrunnsbelastning.

**3. Selv med +1 er sviktraten ikke null.** 12 % samlet svikt viser at kapasitetsproblemer ikke elimineres med én ekstra operatør — de reduseres vesentlig. Residualen skyldes perioder med to samtidige D-pri1-hendelser eller kombinasjoner av D-pri1 med mange bakgrunnshenvendelser.

Scenarioanalysen viser den strukturelle effekten av økt bufferkapasitet, men sier ikke alene hvordan en eventuell bemanningsøkning bør organiseres i praksis. Det er for eksempel ikke gitt at alle timer trenger samme økning, eller at effekten er lik med ulik kompetansesammensetning. Modellen sammenlignes heller ikke direkte mot en historisk bemanningsendring som kunne validert effekten empirisk. Resultatene bør derfor forstås som et analytisk beslutningsgrunnlag — en hypotetisk strukturtest under modellens antagelser — og ikke som en ferdig ressurs- eller turnusløsning.

---

### Oppsummering av modellantakelser

**Tabell 7.8: Modellantakelser og parametere**

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

**Tabell 7.9: Variant A (beredskap) vs Variant B (total) — hovedscenario**

| Skifttype | | Variant A (beredskap) | | | Variant B (total) | |
|---|---|---|---|---|---|---|
| | Normal | Brudd | Svikt | Normal | Brudd | Svikt |
| **Dag hverdag** (c=3) | 69,2 % | 15,9 % | 14,9 % | **59,5 %** | **19,0 %** | **21,6 %** |
| **Natt/helg** (c=2) | 46,9 % | 20,5 % | 32,6 % | **44,8 %** | **22,0 %** | **33,2 %** |
| **Alle** | 59,6 % | 17,9 % | 22,5 % | **53,9 %** | **20,1 %** | **25,9 %** |

Figur 7.3 sammenligner variant A (kun beredskap) med variant B (total belastning) for begge skifttyper. Det mest informative er **dag-søylene** — der utvidelsen til variant B trekker Normal-andelen ned fra 69 % til 59 % og dobler Svikt. Natt/helg-søylene endres lite, fordi bakgrunnsvolumet er begrenset om natten. Tolkningen er at dag- og natt-kapasiteten har ulik karakter: dagsproblemet er drevet av bakgrunnsbelastning, natt-problemet av beredskap alene.

<div align="center">
  <img src="../analyse/figurer/total_belastning_A_vs_B.png" alt="Variant A vs B" width="95%">
  <p align="center"><small><i>Variant A (beredskapsbelastning) vs Variant B (total operativ belastning), hovedscenario.</i></small></p>
</div>

Bakgrunnsbelastningen slår hardest på **dagtid**: Normal-andelen faller knapt 10 prosentpoeng (fra 69,2 % til 59,5 %) og svikt øker fra 14,9 % til 21,6 %. Dette er konsistent med at servicevolumet (22 542 overføringstester per år) er konsentrert på dagtid når servicevirksomhet pågår. Natt/helg påvirkes i mindre grad (Normal faller 2,1 pp, Svikt stiger 0,6 pp) fordi bakgrunnsvolumet er lavere — men utgangspunktet er allerede kritisk: Svikt-andelen på natt/helg er 33,2 % i variant B (scenariobånd 30–38 %), mot 32,6 % i variant A.

Funnet understreker at operatørene på dagtid ikke bare håndterer beredskap — de håndterer en kontinuerlig strøm av servicetester, avklaringer og feilringinger som binder kapasitet mellom beredskapsoppdragene. Med gjennomsnittlig ~10 bakgrunnshenvendelser per time på dagskift er operatørene sjelden reelt ledige selv i perioder uten beredskapsoppdrag.

### 7.7.3 Sensitivitetsanalyse: robusthet mot bindingstidsantakelser

Bindingstidene for ikke-D-kategorier og D-aba Fase 2-parametrene er operative estimater (D-aba Fase 2) og delvis empirisk kalibrerte (L-aba via dybdeanalyse). For å teste robustheten kjøres modellen med tre scenarioer (se avsnitt 6.5.3). Både (p, Y) for D-aba Fase 2 og bindingstider for L-aba/L-hendelse/L-ukjent/S/F/V varieres samtidig fra lav til høy. Analysen er derfor en samlet scenariosensitivitet, ikke en ceteris paribus-test av én parameter om gangen.

**Tabell 7.10: Sensitivitetsanalyse — variant B med tre scenarioer**

| Scenario | Dag hverdag (c=3) | | | Natt/helg (c=2) | | |
|---|---|---|---|---|---|---|
| | Normal | Brudd | Svikt | Normal | Brudd | Svikt |
| **A (beredskap)** | 69,2 % | 15,9 % | 14,9 % | 46,9 % | 20,5 % | 32,6 % |
| **B lav** | 68,8 % | 16,6 % | 14,6 % | 51,1 % | 18,8 % | 30,1 % |
| **B hoved** | 59,5 % | 19,0 % | 21,6 % | 44,8 % | 22,0 % | 33,2 % |
| **B høy** | 45,3 % | 21,0 % | 33,7 % | 38,1 % | 24,2 % | 37,7 % |

Figur 7.4 viser hvordan kapasitetsnivåene endrer seg når bindingstidsparametrene varieres fra lav til høy. Det avgjørende poenget er at natt/helg-søylen for Svikt **forblir over 30 % i alle tre scenarioer** — fra lav (30 %) til høy (38 %). Hovedfunnet om strukturell natt/helg-sårbarhet er dermed robust mot alle rimelige parameterantagelser. På dag hverdag er båndet bredere (15–34 %), noe som tilsier større usikkerhet for dagskonklusjonen.

<div align="center">
  <img src="../analyse/figurer/total_belastning_sensitivitet.png" alt="Sensitivitetsanalyse" width="90%">
  <p align="center"><small><i>Sensitivitetsanalyse — effekt av bindingstidsantakelser på kapasitetsnivå.</i></small></p>
</div>

Tre observasjoner:

**1. Selv lavt scenario viser merkbar bakgrunnseffekt.** Med minimale bindingstider (Service 1 min, L-aba 3 min, feilringing 15 sek, D-aba Fase 2 kun for 30 % med Y = 3 min) er dag-hverdag-resultatet nesten uendret fra variant A (Normal 68,8 vs 69,2 %). På natt/helg gir lav-scenarioet faktisk litt bedre Normal (51 %) enn variant A (47 %) — D-aba Fase 2 slås mindre til når p = 0,30. Dette bekrefter at variant A-resultatet ikke er avhengig av optimistiske antakelser.

**2. Hovedscenario gir vesentlig kapasitetsforverring på dagtid.** Normal faller til 59,5 % og svikt øker til 21,6 %. Dagskiftet, som i variant A framstår som komfortabelt (69 % Normal), blir klart mer presset når hele arbeidsvolumet inkluderes.

**3. Høyt scenario illustrerer bristepunktet.** Med bindingstider i øvre sjikt (Service 4 min, L-aba 9 min, D-aba Fase 2 p = 0,70 og Y = 10 min) faller Normal under 50 % på dag — operatørene er oftere i Brudd eller Svikt enn i normal drift. For natt/helg når Svikt 38 %. Dette representerer dager med tungt servicevolum, uerfarne operatører, eller stor andel ABA-hendelser med oppfølgende nødtelefon.

**Konklusjon:** Hovedfunnet — at natt/helg har 30–38 % Svikt uavhengig av bindingstidsantakelser — er robust over hele spennet. Dimensjoneringsproblemet på natt/helg kan ikke forklares bort gjennom alternative parametervalg.

---

## 7.8 ROS- og beredskapsanalyse som dimensjoneringsgrunnlag (RQ4)

For å besvare RQ4 er beredskapsanalysen for 110 Sør-Vest (Beredskapsanalyse 110 Vest, 2022) og tilhørende ROS-dokument (Risiko- og sårbarhetsanalyse 110 Vest) gjennomgått systematisk. Analysen er rent observerende — vurderingen mot funnene fra primærmodellen drøftes i kap 8.3.4.

**Tabell 7.11: Hva ROS-/beredskapsanalysen for 110 Sør-Vest dokumenterer kvantitativt**

| Element | Dokumentert i ROS/beredskapsanalyse | Form |
|---|---|---|
| Minimumsbemanning per skift | 2 operatører (ekskl. VL) | Forskriftsfestet (FOR-2021-09-15-2755) |
| Faktisk bemanning dag/natt | Dag: 3 + VL; natt/helg: 2 + VL | Numerisk angitt i beredskapsanalysen |
| Overløpsmekanisme til Agder | 30-sek-regel + 10. kø-anrop | Operativ regel, J03 s. 25 |
| Servicegrad (kvantifisert mål) | Ikke spesifisert | Ingen tallfestet servicenivåterskel |
| Andel anrop besvart innen X sek | Ikke spesifisert | Ingen mål satt |
| Andel hendelser med makkerpar | Ikke spesifisert | Ikke uttrykt som målbar metrikk |
| Modellbasert kapasitetsestimat | Ikke gjennomført | ROS bygger på kvalitativ vurdering |
| Sammenligningsgrunnlag andre sentraler | Ikke inkludert | Sentral-spesifikk analyse |

**Observasjon:** ROS-/beredskapsanalysen dokumenterer minimumskrav, faktisk bemanning og overløpsmekanismer, men inneholder ingen kvantitative servicenivåmål eller andre etterprøvbare terskler som kan måles direkte mot observerte hendelsesdata. Analysens grunnlag er kvalitative vurderinger av risiko og operativ erfaring. Interdepartemental arbeidsgruppe (2009) bemerket eksplisitt at det «ikke finnes vitenskapelig grunnlag for de valgte terskelverdiene» for svartid på nasjonalt nivå — en observasjon som er konsistent med funnet at lokal ROS heller ikke etablerer slike terskler. Meld. St. 16 (2023–2024) viderefører den kvalitative tilnærmingen uten å introdusere en nasjonal kvantitativ standard.

For sammenligning viser brann- og redningsvesenforskriften (FOR-2021-09-15-2755) at kvantitative og etterprøvbare krav er mulig på brann- og redningssiden gjennom krav til organisering, beredskap, bemanning og innsatstid. En tilsvarende operatørstandard for 110-sentralene mangler. Den analytiske tolkningen av dette gapet, og hvilke implikasjoner det har for dimensjoneringspraksis, drøftes i kap 8.3.4.

---

## 7.9 Nasjonal benchmarking — DSB 2025-data (RQ5)

For å belyse RQ5 er DSBs samlede 2025-datasett (508 228 registrerte oppdrag — proxy for henvendelser, med kjent undertelling pga. sammenstilling, jf. kap 6.2 — alle 12 sentraler) klassifisert etter V3-regelen (avsnitt 5.3.2) og sammenlignet på sentralnivå. Avsnittet er rent beskrivende kontekstualisering — primærmodellen er ikke kjørt på data fra andre sentraler enn Sør-Vest. De normative implikasjonene drøftes som åpne forskningsspørsmål i kap 8.3.4 og 9.3, ikke som konklusjoner fra denne studien.

Med *benchmarking* menes her en strukturert sammenstilling av register- og årsrapportdata, ikke en evaluering av om de andre sentralene er korrekt bemannet, og heller ikke en validering av modellen mot andre datasett. DSB/LEO/BRIS- og MOB-tallene kan brukes som sekundærdata selv om ikke alle sentralene har besvart avklaringsspørsmål. Manglende svar gjør først og fremst at enkelte avvik må stå som datakvalitets- eller registreringsforbehold. Der slike avvik kan påvirke tolkningen vesentlig, omtales de som forbehold heller enn som lokale feil.

Tabellene i avsnitt 7.9 bruker det nasjonale DSB-uttrekket for sammenlignbarhet mellom sentraler. For Sør-Vest gir dette 61 934 registrerte oppdrag og 7 527 D-hendelser. Hovedanalysen for casen bruker den lokale Sør-Vest-eksporten med 61 964 registrerte oppdrag og 7 555 D-hendelser. Differansen er liten (30 oppdrag / 28 D-hendelser), men tallgrunnlagene holdes adskilt: lokal eksport brukes i primærmodellen, nasjonalt uttrekk brukes i benchmarking.

### 7.9.1 Volum og arbeidsmengde

**Tabell 7.12: Volum og operatørbelastning per sentral, DSB 2025**

| Sentral | Totalvolum | Beredskap (D) | D-andel | c_eff dag (MOB) | Oppdrag/c_eff (MOB) | Arbmengde (timer/dag) |
|---|---:|---:|---:|---:|---:|---:|
| Oslo | 71 421 | 17 811 | 24,9 % | 4 | 17 855 | 19,4 |
| Sør-Øst | 68 654 | 14 174 | 20,6 % | 5 | 13 731 | 16,4 |
| Sør-Vest | 61 934 | 7 527 | 12,2 % | 3 | 20 645 | 11,5 |
| Øst | 58 138 | 12 478 | 21,5 % | 5 | 11 628 | 13,9 |
| Vest | 50 778 | 8 041 | 15,8 % | 3 | 16 926 | 10,5 |
| Innlandet | 44 001 | 6 600 | 15,0 % | 3 | 14 667 | 8,9 |
| Midt-Norge | 41 374 | 8 043 | 19,4 % | 3 | 13 791 | 9,3 |
| Nordland | 29 577 | 2 749 | 9,3 % | 2 | 14 789 | 4,9 |
| Møre og Romsdal | 29 384 | 3 492 | 11,9 % | 3 | 9 795 | 5,1 |
| Agder | 26 238 | 6 409 | 24,4 % | 3 | 8 746 | 6,6 |
| Tromsø | 19 327 | 3 927 | 20,3 % | 1 | 19 327 | 4,7 |
| Finnmark | 7 402 | 1 281 | 17,3 % | 2 | 3 701 | 1,6 |

*Kilde: `analyse/nasjonal_2025/storrelse_ranking.csv` og `benchmarkmatrise.csv`. c_eff dag (MOB) = rapportert c_total dag − 1 (VL-korreksjon). For andre sentraler enn Sør-Vest er dette en sammenligningsproxy, ikke lokalt validert faktisk bemanning. Arbmengde = volum × kategori-spesifikk bindingstid summert over et år.*

Totalvolumet varierer 9,6× mellom Finnmark (7 402) og Oslo (71 421). Basert på rapportert MOB-bemanning ligger Sør-Vest (20 645) høyt på oppdrag per effektiv operatør foran Tromsø (19 327) og Oslo (17 855), mens Finnmark (3 701) ligger lavest. Dette er et strukturelt benchmarksignal, ikke en konklusjon om faktisk vaktbelastning ved hver enkelt sentral. Arbeidsmengde per dag spenner fra 1,6 timer (Finnmark) til 19,4 timer (Oslo).

### 7.9.2 Kategorifordeling og klassifiseringspraksis

**Tabell 7.13: Andel av totalvolum per V3-kategori, DSB 2025**

| Sentral | D-pri1 | D-aba | S | L-aba | L-hendelse | L-ukjent | F | V |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Agder | 10,3 % | 14,1 % | 30,9 % | 3,8 % | 7,6 % | 13,8 % | 18,5 % | 1,0 % |
| Finnmark | 14,0 % | 3,3 % | 31,4 % | 5,3 % | 8,1 % | 28,1 % | 8,6 % | 1,2 % |
| Innlandet | 10,2 % | 4,8 % | 21,2 % | 5,2 % | 3,4 % | 39,6 % | 13,0 % | 2,6 % |
| Midt-Norge | 9,7 % | 9,7 % | 22,4 % | 0,6 % | 3,8 % | 35,9 % | 17,2 % | 0,7 % |
| Møre og Romsdal | 9,7 % | 2,2 % | 47,1 % | 3,8 % | 3,3 % | 18,8 % | 13,8 % | 1,3 % |
| Nordland | 7,0 % | 2,3 % | 38,0 % | 7,5 % | 4,5 % | 30,1 % | 9,1 % | 1,5 % |
| Oslo | 24,9 % | 0,0 % | 9,3 % | 0,0 % | 9,3 % | 40,4 % | 14,5 % | 1,5 % |
| Sør-Vest | 7,2 % | 4,9 % | 36,4 % | 5,5 % | 6,9 % | 27,1 % | 11,0 % | 0,9 % |
| Sør-Øst | 20,6 % | 0,0 % | 22,9 % | 0,0 % | 10,2 % | 28,7 % | 15,8 % | 1,6 % |
| Tromsø | 9,8 % | 10,5 % | 18,3 % | 6,1 % | 8,4 % | 35,9 % | 10,4 % | 0,6 % |
| Vest | 11,4 % | 4,4 % | 38,1 % | 0,6 % | 9,9 % | 20,6 % | 13,9 % | 1,1 % |
| Øst | 11,8 % | 9,6 % | 13,5 % | 2,3 % | 5,8 % | 34,8 % | 20,6 % | 1,5 % |

*Kilde: `analyse/nasjonal_2025/benchmarkmatrise.csv`. V3-klassifisering med Kilde=Alarm-krav for D-aba og L-aba.*

Tre observasjoner:

**1. L-aba-andel varierer 0,0 %–7,5 %** — Sør-Øst og Oslo har tilnærmet null L-aba (3 oppdrag samlet), mens Nordland topper med 7,5 %. Dette er konsistent med ulik registreringspraksis: ABA-oppdrag uten utrykning kan klassifiseres under L-hendelse, L-ukjent eller F i sentraler uten L-aba-bruk.

**2. D-pri1-andel varierer 7,0 %–24,9 %** — Oslo (24,9 %) og Sør-Øst (20,6 %) ligger 2–3× høyere enn Sør-Vest (7,2 %) og Nordland (7,0 %). Mønsteret er konsistent med at noen sentraler varsler tidlig, mens andre avklarer på telefon først.

**3. L-ukjent er gjennomgående høy (13,8 %–40,4 %)** — feltet `Opprinnelig oppdragstype` lukkes ofte uten utfylling. Dette gir høy datausikkerhet for kategorifordelingen og er en strukturell begrensning på tvers av alle sentraler.

### 7.9.3 Skjulte 110-ID-sekvenser

**Tabell 7.14: Andel skjulte sekvensnumre i 110-ID per sentral, DSB 2025**

| Sentral | Registrerte oppdrag | Skjulte sekvensnr | Estimert totalt | Skjult-rate |
|---|---:|---:|---:|---:|
| Finnmark | 7 402 | 13 780 | 21 182 | 65,1 % |
| Agder | 26 238 | 31 339 | 57 577 | 54,4 % |
| Øst | 58 138 | 47 577 | 105 715 | 45,0 % |
| Tromsø | 19 327 | 13 447 | 32 774 | 41,0 % |
| Innlandet | 44 001 | 28 761 | 72 762 | 39,5 % |
| Sør-Øst | 68 652 | 35 323 | 103 975 | 34,0 % |
| Nordland | 29 577 | 12 837 | 42 414 | 30,3 % |
| Vest | 50 778 | 20 723 | 71 501 | 29,0 % |
| Møre og Romsdal | 29 384 | 10 791 | 40 175 | 26,9 % |
| Oslo | 71 421 | 26 140 | 97 561 | 26,8 % |
| Sør-Vest | 61 934 | 18 930 | 80 864 | 23,4 % |
| Midt-Norge | 41 374 | 12 223 | 53 597 | 22,8 % |

*Skjulte sekvensnumre dekker tre fenomener: (i) sammenstilte anrop, (ii) overføringer til nabosentral via