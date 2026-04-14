# 7. Analyse og resultater

## 7.1 Metodisk tilnærming: fra køteori til prosedyrbasert kapasitetsmodell

Prosjektet startet med Erlang-C (M/M/c) som primærmodell for kapasitetsanalyse. Erlang-C estimerer sannsynligheten for at et innkommende anrop må vente, gitt ankomstrate (λ), gjennomsnittlig servicetid (μ⁻¹) og antall servere (c). En innledende analyse med Erlang-C viste imidlertid svært lav systemutnyttelse (ρ < 10 %) for alle skifttyper, noe som isolert sett kunne tyde på at bemanningsnivået er komfortabelt (se Tabell 7.1).

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

2. **Kapasitetsanalysen er konservativ.** Ankomstkonfliktmodellen (avsnitt 7.5) er basert på synlige oppdrag med ressursvarsling. De sammenstilte tilleggsanropene opptar en operatør som ellers kunne vært ledig for neste hendelse, men er ikke modellert som egne belastningsenheter. Modellen gir dermed et minimumsanslag på faktisk operativ belastning.

3. **Skjult belastning påvirker dimensjonering direkte.** Sammenstilte tilleggsanrop påvirker ikke bare ankomstraten i køteoretisk forstand, men også den operative bindingen i den prosedyrbaserte modellen. Når flere innringere melder om samme hendelse, kan disse anropene oppta en operatør som ellers ville vært ledig for neste hendelse, eller forsterke belastningen i en allerede aktiv hendelse. For dimensjonering betyr dette at analyser basert på oppdragsteller alene kan undervurdere både arbeidsbelastning, samtidighetskonflikt og behovet for bufferkapasitet.

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

Bindingstid defineres som den perioden operatørene er aktivt bundet til en hendelse — fra anropets ankomsttidspunkt til operatørene er frigjort for neste hendelse. Bindingstidene er beregnet direkte fra BRIS-data for hendelser med ressursvarsling (kategori D, jf. avsnitt 6.2).

### 7.4.1 Avgrensning og datagrunnlag

Av 61 964 synlige hendelser i datasettet har 7 555 (12,2 %) registrert tidspunkt for ressursvarsling, noe som identifiserer dem som kategori D — beredskapsoppdrag med utrykningsbeslutning. Hovedanalysen avgrenser seg til disse hendelsene fordi de kan observeres robust gjennom ressursvarsling og tidspunkt for første ressurs fremme. Denne avgrensningen er valgt av hensyn til målepresisjon, ikke fordi andre hendelseskategorier er uviktige. Den kvantitative analysen prioriterer dermed robust observerbarhet fremfor fullstendighet.

Hendelser uten ressursvarsling er ikke nødvendigvis irrelevante for dimensjonering. En del av disse representerer reelle hendelser løst av 110 uten utrykning (kategori B), tidskritiske avklaringer som ABA (kategori C), og i tillegg kommer sammenstilte tilleggsanrop knyttet til eksisterende hendelser (avsnitt 7.2). Disse belaster operatørkapasitet, men lar seg ikke modellere like robust som kategori D med det foreliggende datasettet. De kvantitative hovedresultatene i denne studien beskriver dermed den best observerbare og mest tydelig beredskapsdimensjonerende delen av operatørbindingen. De utgjør ikke en fullstendig modellering av all operativ belastning i sentralen.

### 7.4.2 Beregning

Bindingstiden per hendelse er beregnet som:

> **Bindingstid = (Dato/tid anrop → Første ressurs fremme) + 3 minutter kvitteringsvindu**

De tre minuttene reflekterer vindusmelding som må kvitteres og logges av GUL-operatør etter at første ressurs er på plass. Av de 7 555 beredskapsoppdragene har 5 777 (76,5 %) registrert tidspunkt for første ressurs fremme. De resterende 1 778 (23,5 %) er tildelt median bindingstid fra de observerte verdiene.

### 7.4.3 Observert bindingstidsfordeling

**Tabell 7.3: Bindingstid per beredskapsoppdrag — 110 Sør-Vest 2025 (inkl. +3 min kvittering)**

| Persentil | Bindingstid (min) |
|---|---|
| P10 | 9,1 |
| P25 | 11,1 |
| **Median** | **13,0** |
| P75 | 15,4 |
| P90 | 21,6 |
| P95 | 29,2 |

Bindingstiden kan belyses gjennom to tidspunkter i BRIS-data. Tid fra anrop til ressurs varslet (median 1,2 minutter) måler hvor raskt GUL-operatøren får utalarmert ressurser — men dette er ikke det samme som at RØD-operatøren er frigjort. Både RØD og GUL er bundet parallelt gjennom hele akuttfasen:

- **0 – ~1 min:** RØD i samtale med innringer, GUL i medlytt og lokalisering
- **~1 – ~2 min:** GUL utalarmerer ressurser (ressurs varslet), RØD fortsetter samtalen
- **~2 – ~10 min:** RØD kan fortsatt være i telefon med innringer, GUL koordinerer samband og gir tidskritisk informasjon til mannskap underveis
- **~10 min:** Første ressurs fremme → vindusmelding
- **+3 min:** Kvittering og loggføring → GUL delvis frigjort

Både RØD og GUL er dermed bundet i hele perioden fra anrop til første ressurs er fremme. Bindingstiden på median 13,0 minutter representerer perioden der to operatører er opptatt med én hendelse. Etter at innringer legger på kan RØD frigjøres før GUL, men det eksakte tidspunktet varierer og er ikke registrert i BRIS.

![Figur 7.1a: Bindingstid per fase](../analyse/figurer/bindingstid_histogram.png)
*Figur 7.1a: Tidsintervaller i beredskapsoppdrag. Venstre: tid til utalarmering (median 1,2 min). Midten: utrykningstid (median 8,2 min). Høyre: total bindingstid (median 10,0 min, uten kvittering). Merk: RØD og GUL er bundet parallelt gjennom hele forløpet.*

**Tabell 7.3b: Bindingstid-fordeling (per 1000 beredskapsoppdrag)**

| Bindingstid | Antall | Andel | Kumulativ | Per 1000 |
|---|---|---|---|---|
| 0–5 min | 38 | 0,5 % | 0,5 % | 5 |
| 5–8 min | 331 | 4,4 % | 4,9 % | 44 |
| 8–10 min | 866 | 11,5 % | 16,3 % | 115 |
| **10–13 min** | **3 456** | **45,7 %** | **62,1 %** | **457** |
| 13–16 min | 1 194 | 15,8 % | 77,9 % | 158 |
| 16–20 min | 749 | 9,9 % | 87,8 % | 99 |
| 20–25 min | 378 | 5,0 % | 92,8 % | 50 |
| 25–30 min | 183 | 2,4 % | 95,2 % | 24 |
| 30–45 min | 211 | 2,8 % | 98,0 % | 28 |
| 45–60 min | 61 | 0,8 % | 98,8 % | 8 |
| 60+ min | 88 | 1,2 % | 100 % | 12 |

![Figur 7.1b: Bindingstid-fordeling](../analyse/figurer/bindingstid_beredskap_fordeling_v2.png)
*Figur 7.1b: Fordeling av operatørbindingstid per beredskapsoppdrag. Nesten halvparten (457/1000) binder operatørene i 10–13 minutter.*

Dag- og nattskift viser tilnærmet lik bindingstid (median 9,6 vs 10,4 min før kvitteringsvindu), noe som indikerer at bindingstiden primært drives av hendelsestype og geografi, ikke av tidspunkt på døgnet.

![Figur 7.1c: Bindingstid dag vs natt](../analyse/figurer/bindingstid_dag_natt.png)
*Figur 7.1c: Tidsintervaller (tid til utalarmering, utrykningstid, total bindingstid) fordelt på dag- og nattskift. RØD og GUL er bundet parallelt i alle tre faser. Forskjellene mellom dag og natt er marginale.*

---

## 7.5 Kapasitetsanalyse: korrigert modell med skjulte anrop

### Metode

For hvert innkommende anrop (beredskapsoppdrag kategori D + sammenstilte tilleggsanrop) beregnes antall samtidige aktive hendelser ved ankomsttidspunktet. En hendelse er «aktiv» i perioden fra anrop til bindingstiden er utløpt. Kapasitetsnivå klassifiseres basert på antall ledige operatører (se avsnitt 6.4.3).

Modellen speiler den operative virkeligheten: operatørene tilpasser seg alltid ved å splitte makkerparet når det trengs. Antall ledige = c_eff minus n_aktive.

De skjulte anropene kan ikke observeres direkte som egne oppdrag i BRIS/LEO. I modellen er de derfor plassert i tid ved å interpolere fra nærmeste synlige oppdrags ankomsttidspunkt. Dersom oppdrag B06-250101-4 og B06-250101-6 er synlige, legges det manglende sekvensnummeret (-5) inn med tidspunkt fra det foregående synlige oppdraget. Analysen fanger dermed den strukturelle effekten av at slike anrop beslaglegger kapasitet i perioder med eksisterende belastning, selv om det eksakte tidspunktet for hvert enkelt skjult anrop er et estimat.

Analysen gjennomføres i to varianter for å vise effekten av skjult anropsvolum:
- **Kun kategori D:** 7 555 beredskapsoppdrag med ressursvarsling (bindingstid: median 13,0 min)
- **Kategori D + skjulte anrop:** 7 555 + 18 901 = 26 456 belastningsenheter (der en belastningsenhet er et anrop eller hendelsesforløp som binder operatørkapasitet og derfor inngår i konfliktanalysen) (skjulte anrop: 1 min bindingstid)

### Antakelse om bindingstid for sammenstilte anrop

De sammenstilte tilleggsanropene er i modellen tildelt 1 minutts bindingstid. Dette er en forenklet og konservativ antakelse, valgt for å representere at slike anrop ofte er korte — operatøren kjenner allerede hendelsen, avklarer kort, informerer at ressurs er på vei og legger på — men likevel beslaglegger en operatør i et kritisk tidsvindu. Antakelsen må ikke forstås som en presis måling av faktisk samtaletid, men som en operativ proxy for kortvarig kapasitetsbinding. Dersom reell gjennomsnittlig bindingstid er høyere, vil modellen undervurdere effekten av skjulte anrop. Sensitiviteten for denne antakelsen er et område for videre analyse.

### Hovedresultater

**Tabell 7.4: Kapasitetsnivå — kun kategori D vs. med skjulte anrop**

| | **Kun kategori D** (n = 7 555) | | | **Med skjulte anrop** (n = 26 456) | | |
|---|---|---|---|---|---|---|
| Skifttype | Normal | Brudd | Svikt | Normal | Brudd | Svikt |
| **Dag hverdag (c=3)** | 86,9 % | 9,0 % | 4,2 % | 77,9 % | 12,0 % | 10,1 % |
| **Natt/helg (c=2)** | 62,8 % | 24,5 % | 12,7 % | 48,1 % | 28,4 % | 23,5 % |
| **Alle** | 73,8 % | 17,4 % | 8,8 % | 65,3 % | 19,0 % | 15,8 % |

![Figur 7.2: Effekt av skjulte anrop](../analyse/figurer/kapasitet_v4_med_skjulte.png)
*Figur 7.2: Kapasitetsnivå med og uten skjulte/sammenstilte anrop. Heltrukne søyler viser kun kategori D; halvgjennomsiktige søyler viser effekten av å inkludere 18 901 sammenstilte anrop. Effekten er størst på natt/helg der Normal faller fra 62,8 % til 48,1 %.*

### Effekten av skjulte anrop

De sammenstilte tilleggsanropene forsterker kapasitetspresset betydelig:

- **Normal faller med 8,5 prosentpoeng totalt** (73,8 % til 65,3 %)
- **Svikt nesten dobles** (8,8 % til 15,8 %)
- **Natt/helg rammes hardest:** Normal faller under halvparten (48,1 %), og nesten hvert 4. anrop medfører svikt (23,5 %)

Dette bekrefter at de skjulte anropene — til tross for kort varighet (~1 min) — er det som vipper kapasiteten i perioder der presset allerede er høyt. En operatør som tar et sammenstilt anrop er utilgjengelig for neste hendelse i akkurat det kritiske vinduet.

De rapporterte andelene for normal, brudd og svikt beskriver et nedre estimat for kapasitetskonflikt i sentralen, fordi kategori B og C ikke er inkludert. Reell konfliktfrekvens kan være høyere. Begrensningene i datagrunnlaget trekker i hovedsak i én retning: mot undervurdering. Resultatene bør leses som et minimumsanslag på brudd- og sviktrisiko, ikke som et maksimumsanslag.

### Kapasitetsnivå per time

![Figur 7.3: Kapasitet per time](../analyse/figurer/kapasitet_v4_per_time.png)
*Figur 7.3: Kapasitetsnivå per time på døgnet (kategori D + skjulte anrop). Nattetimene (c=2) har gjennomgående høy svikt-andel (20-34 %). Skiftvekslingen kl. 19 (c=3 til c=2) er tydelig synlig. Dagskiftet (kl. 07-18) har markant bedre kapasitetsbilde takket være c=3.*

Tre tidsperioder skiller seg ut:
- **Kl. 03-04:** Over 30 % svikt — lavt volum, men når det treffer med c=2 er det sårbart
- **Kl. 19-20:** Skiftveksling fra c=3 til c=2 mens volumet fortsatt er høyt — 25 % svikt
- **Kl. 09-10:** Dagtidstoppen med ca. 1 900 hendelser per time — selv med c=3 er 10–11 % svikt

---

## 7.6 Scenarioanalyse: effekt av +1 operatør per skift

Scenarioet med én ekstra operatør per skift er en strukturtest av robusthet: hvilken effekt har en ekstra bufferressurs på sannsynligheten for brudd og svikt? Scenarioet øker c_eff fra 3 til 4 på dag hverdag og fra 2 til 3 på natt/helg.

**Tabell 7.5: Effekt av +1 operatør (kategori D + skjulte anrop)**

| Skifttype | | Dagens bemanning | | +1 operatør | | |
|---|---|---|---|---|---|---|
| | Normal | Brudd | Svikt | Normal | Brudd | Svikt |
| **Dag hverdag** (3 til 4) | 77,9 % | 12,0 % | 10,1 % | **89,9 %** | **4,8 %** | **5,3 %** |
| **Natt/helg** (2 til 3) | 48,1 % | 28,4 % | 23,5 % | **76,5 %** | **11,5 %** | **12,0 %** |
| **Alle** | 65,3 % | 19,0 % | 15,8 % | **84,2 %** | **7,6 %** | **8,2 %** |

![Figur 7.4: Dimensjoneringskurve](../005%20report/modelloutput/dimensjoneringskurve.png)
*Figur 7.4: Dimensjoneringskurve — andel normal/brudd/svikt som funksjon av bemanning (c_eff 2–6). Grenseverdien for akseptabelt servicenivå er en politisk/ledelsesmessig beslutning.*

Tre funn:

**1. Natt/helg: fra under halvparten til tre fjerdedeler Normal.** Med +1 operatør øker Normal fra 48,1 % til 76,5 % (+28,4 pp). Svikt halveres fra 23,5 % til 12,0 %. Den ekstra operatøren gir den buffersonen som c=2 mangler — operatørene kan jobbe solo før det går til svikt.

**2. Dag hverdag: solid forbedring.** Normal øker fra 77,9 % til 89,9 %. Svikt halveres fra 10,1 % til 5,3 %. Med c=4 kan to samtidige hendelser håndteres med makkerpar på den første og solo på den andre før svikt inntreffer.

**3. Selv med +1 er sviktraten ikke null.** 8,2 % samlet svikt viser at kapasitetsproblemer ikke elimineres med én ekstra operatør — de reduseres vesentlig. Dette skyldes perioder med tre eller flere samtidige hendelser, forsterket av skjulte anrop.

Scenarioanalysen viser den strukturelle effekten av økt bufferkapasitet, men sier ikke alene hvordan en eventuell bemanningsøkning bør organiseres i praksis. Det er for eksempel ikke gitt at alle timer trenger samme økning, eller at effekten er lik med ulik kompetansesammensetning. Resultatene bør derfor forstås som et analytisk beslutningsgrunnlag, ikke som en ferdig ressurs- eller turnusløsning.

---

### Oppsummering av modellantakelser

**Tabell 7.6: Modellantakelser og parametere**

| Parameter | Verdi | Kilde |
|---|---|---|
| Bindingstid kategori D | Observert fra BRIS + 3 min kvittering | Median 13,0 min |
| Bindingstid skjulte anrop | 1 min (kvalitativt estimat) | Operativ vurdering |
| Kapasitetsnivå: Normal | ledige ≥ 2 | Makkerpar mulig |
| Kapasitetsnivå: Brudd | ledige = 1 | Solo-håndtering |
| Kapasitetsnivå: Svikt | ledige ≤ 0 | VL/Agder |
| c_eff dag hverdag | 3 (4 tot. − 1 VL) | Prosedyre |
| c_eff natt/helg | 2 (3 tot. − 1 VL) | Prosedyre |
| Skjulte anrop identifisert via | Sekvensgap i 110_ID | 18 901 stk |
| Imputering manglende fremme-tid | Median bindingstid | 23,5 % av kat. D |

---

## 7.7 Total operativ belastning (variant B)

### 7.7.1 Bakgrunn

Primærmodellen (variant A) kvantifiserer kapasitetsnivå basert på beredskapsoppdrag (kategori D) og sammenstilte anrop. Dette gir et presist bilde av beredskapskapasiteten, men dekker kun 26 456 av estimert 80 865 anrop. Variant B utvider analysen til å inkludere alle hendelseskategorier (se avsnitt 6.5) for å kvantifisere den samlede operative belastningen.

### 7.7.2 Resultater: beredskapsbelastning versus total belastning

**Tabell 7.7: Variant A (beredskap) vs Variant B (total) — hovedscenario**

| Skifttype | | Variant A (beredskap) | | | Variant B (total) | |
|---|---|---|---|---|---|---|
| | Normal | Brudd | Svikt | Normal | Brudd | Svikt |
| **Dag hverdag** (c=3) | 77,9 % | 12,0 % | 10,1 % | **64,8 %** | **18,6 %** | **16,5 %** |
| **Natt/helg** (c=2) | 48,1 % | 28,4 % | 23,5 % | **45,0 %** | **29,6 %** | **25,4 %** |
| **Alle** | 65,3 % | 19,0 % | 15,8 % | **58,1 %** | **22,4 %** | **19,6 %** |

<div align="center">
  <img src="../analyse/figurer/total_belastning_A_vs_B.png" alt="Variant A vs B" width="95%">
  <p align="center"><small><i>Figur 7.5: Variant A (beredskapsbelastning) vs Variant B (total operativ belastning), hovedscenario.</i></small></p>
</div>

Bakgrunnsbelastningen slår hardest på **dagtid**: Normal-andelen faller 13 prosentpoeng (fra 77,9 % til 64,8 %) og svikt øker fra 10,1 % til 16,5 %. Dette er konsistent med at servicevolumet (22 542 overføringstester per år) er konsentrert på dagtid når servicevirksomhet pågår. Natt/helg påvirkes i mindre grad (Normal faller 3 pp) fordi bakgrunnsvolumet er lavere.

Funnet understreker at operatørene på dagtid ikke bare håndterer beredskap — de håndterer en kontinuerlig strøm av servicetester, avklaringer og feilringinger som binder kapasitet mellom beredskapsoppdragene. Med gjennomsnittlig ~10 bakgrunnshenvendelser per time på dagskift er operatørene sjelden reelt ledige selv i perioder uten beredskapsoppdrag.

### 7.7.3 Sensitivitetsanalyse: robusthet mot bindingstidsantakelser

Bindingstidene for ikke-D-kategorier er operative estimater, ikke målinger. For å teste robustheten kjøres modellen med tre scenarioer (se avsnitt 6.5.3).

**Tabell 7.8: Sensitivitetsanalyse — variant B med tre bindingstidsscenarioer**

| Scenario | Dag hverdag (c=3) | | | Natt/helg (c=2) | | |
|---|---|---|---|---|---|---|
| | Normal | Brudd | Svikt | Normal | Brudd | Svikt |
| **A (beredskap)** | 77,9 % | 12,0 % | 10,1 % | 48,1 % | 28,4 % | 23,5 % |
| **B lav** | 75,3 % | 14,4 % | 10,3 % | 49,8 % | 28,6 % | 21,6 % |
| **B hoved** | 64,8 % | 18,6 % | 16,5 % | 45,0 % | 29,6 % | 25,4 % |
| **B høy** | 50,5 % | 21,8 % | 27,7 % | 40,2 % | 29,9 % | 30,0 % |

<div align="center">
  <img src="../analyse/figurer/total_belastning_sensitivitet.png" alt="Sensitivitetsanalyse" width="90%">
  <p align="center"><small><i>Figur 7.6: Sensitivitetsanalyse — effekt av bindingstidsantakelser på kapasitetsnivå.</i></small></p>
</div>

Tre observasjoner:

**1. Selv lavt scenario viser merkbar effekt.** Med minimale bindingstider (Service 1 min, feilringing 15 sek) faller Normal-andelen på dag fra 77,9 % til 75,3 %. Effekten er moderat men målbar, og bekrefter at bakgrunnsbelastningen ikke er triviell selv under de mest konservative antakelsene.

**2. Hovedscenario gir vesentlig kapasitetsforverring på dagtid.** Normal faller til 64,8 % og svikt øker til 16,5 %. Dagskiftet, som i variant A fremstår som komfortabelt (78 % Normal), viser seg å være vesentlig mer presset når hele arbeidsvolumet inkluderes.

**3. Høyt scenario illustrerer bristepunktet.** Med bindingstider i øvre sjikt (Service 4 min, L-ukjent 5 min) faller Normal under 50 % på dag — operatørene er oftere i degradert eller svikt enn i normal drift. For natt/helg er svikt-andelen 30 %. Dette scenarioet representerer dager med tungt servicevolum eller uerfarne operatører som bruker lengre tid per hendelse.

**Konklusjon:** Hovedfunnet — at bakgrunnsbelastning forverrer kapasitetsbildet merkbart, spesielt på dagtid — er robust over hele spennet av rimelige bindingstidsantakelser.

---

## 7.8 Generaliserbarhet

Den konkrete analysen er gjennomført på data fra 110 Sør-Vest, men modellrammeverket er utviklet for å kunne anvendes sentralsvis på alle norske 110-sentraler. Det sentrale er ikke de eksakte prosentverdiene i denne studien, men metoden for å identifisere hvor ofte en ny hendelse ankommer i en tilstand der tilgjengelig operatørkapasitet allerede er bundet.

Andre sentraler kan bruke samme analyseopplegg dersom de har tilgang til:
- Ankomsttidspunkt for hendelser
- Tidspunkt for ressursvarsling (identifiserer kategori D)
- En proxy for akuttfasens varighet (første ressurs fremme eller tilsvarende)
- Eventuelt indikatorer på sammenstilte tilleggsanrop for korreksjon av ankomstrate

Modellen kan dermed danne grunnlag for en nasjonal, etterprøvbar dimensjoneringsstandard for 110-operatører — analogt med dimensjoneringsforskriftens rolle for brannstasjoner, men basert på operatørbinding fremfor responstid.

---

## 7.9 Sammenstilling og tolkning

Analysen dokumenterer fem hovedfunn:

**Funn 1: Erlang-C alene er utilstrekkelig for 110-dimensjonering.**
Den tradisjonelle køteoretiske modellen gir svært lav systemutnyttelse (ρ < 10 %) og P(W > 30s) < 0,5 % for alle skifttyper. Modellen behandler operatører som uavhengige servere, fanger ikke kapasitetstapet ved makkerpar-kravet, og baserer seg på en ankomstrate fra synlige oppdrag som undervurderer faktisk innkommende volum med anslagsvis 23 %.

**Funn 2: Faktisk bindingstid er lengre enn samtaletid — og databasert.**
Bindingstiden (anrop → første ressurs fremme + 3 min kvittering) har median 13,0 minutter basert på 7 555 beredskapsoppdrag. Nesten halvparten (45,7 %) av oppdragene binder operatørene i 10–13 minutter, mens 12,2 % tar over 20 minutter. Tiden til utalarmering (median 1,2 min) viser at GUL handler raskt, men både RØD og GUL er bundet parallelt gjennom hele akuttfasen.

**Funn 3: Skjulte anrop forsterker kapasitetsproblemet vesentlig.**
Med den korrigerte modellen (operativ tilpasning + skjulte anrop) er 15,8 % av alle anrop i svikt og 19,0 % i brudd på driftsstandard. Uten de skjulte anropene er svikt 8,8 % — differansen på 7 prosentpoeng viser at de sammenstilte tilleggsanropene, til tross for kort varighet (~1 min), er det som vipper kapasiteten i perioder der presset allerede er høyt. På natt/helg (c=2) er under halvparten av anropene i normal drift (48,1 %), og nesten hvert 4. anrop medfører svikt (23,5 %). Disse tallene er fortsatt et minimumsanslag fordi kategori B og C ikke er inkludert.

**Funn 4: +1 operatør per skift har størst effekt på natt/helg.**
Én ekstra operatør (c_eff 2→3 natt/helg, 3→4 dag) øker Normal fra 48,1 % til 76,5 % på natt/helg (+28,4 pp) og reduserer svikt fra 23,5 % til 12,0 %. På dag hverdag øker Normal fra 77,9 % til 89,9 %. Den ekstra operatøren gir den buffersonen som c=2 mangler — operatørene kan jobbe solo før det går til svikt. Analysen indikerer at bemanningsstrukturen er en mer direkte driver for observerte kapasitetsforskjeller enn samlet synlig oppdragsvolum alene.

**Funn 5: Total operativ belastning forverrer kapasitetsbildet merkbart, spesielt på dagtid.**
Når alle hendelseskategorier inkluderes (variant B), faller Normal-andelen på dag hverdag fra 77,9 % til 64,8 % (−13 pp) og svikt øker fra 10,1 % til 16,5 %. Effekten skyldes primært servicevolumet (22 542 overføringstester) som er konsentrert på dagtid. Sensitivitetsanalysen viser at denne forverringen er robust: selv med minimale bindingstidsantakelser faller Normal til 75,3 %. Funnet understreker at beredskapskapasiteten ikke kan vurderes isolert fra den samlede arbeidsbyrden.

Funnene har direkte parallell til dimensjoneringslogikken i brannstasjonsforskriften: S1-stasjoner (kasernerte brannstasjoner med størst beredskapsansvar) dimensjoneres med to kjøretøy ikke fordi begge alltid er i bruk, men fordi konsekvensen av utilstrekkelig kapasitet ved simultane hendelser er uakseptabel. Det samme prinsippet — dimensjonering for beredskapstopper, ikke for gjennomsnittsbelastning — bør ligge til grunn for 110-operatørkapasitet.

---

*Skript for analyser og figurer: `analyse/scripts/konflikt_v4_korrigert.py` (variant A), `analyse/scripts/konflikt_total_belastning.py` (variant B), `analyse/kapasitetsmodell_110.py`, `analyse/scripts/bindingstid_analyse.py`*
*Data: `004 data/110 SØR VEST TESTDATASETT.xlsx` (BRIS 2025, 61 964 synlige oppdrag, 7 555 beredskapsoppdrag kategori D)*
*Prosedyreferanse: Rogaland brann og redning IKS (2024). Prosedyre arbeidsmetodikk, utalarmering og loggføring, versjon 4, 16.12.2024.*
