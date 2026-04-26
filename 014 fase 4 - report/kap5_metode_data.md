# 5. Metode og data

## 5.1 Forskningsdesign

Prosjektet er gjennomført som en kvantitativ casestudie av 110 Sør-Vest, supplert med nasjonal benchmarking for å kontekstualisere casefunnene. Forskningsdesignet er retrospektivt og planleggingsrettet: analysen baseres på historiske hendelsesdata for å vurdere om faktisk bemanning samsvarer med observert belastning.

Casestudiedesignet er valgt fordi problemstillingen er tett knyttet til en spesifikk organisatorisk og operativ kontekst, der bemanning, arbeidsmetodikk og registreringspraksis må forstås samlet for å kunne modellere kapasitetsbinding. Forfatteren har operativ tilknytning til 110 Sør-Vest, noe som gir tilgang til prosedyredokumentasjon, beredskapsanalyse og operative informanter som er nødvendige for å konstruere og validere modellparametere. Modellrammeverket er utviklet for å være overførbart til andre sentraler gitt tilsvarende datatilgang (se avsnitt 6.1 og 7.7).

### Refleksivitet: insider-forskning og objektivitetstiltak

Forfatterens operative tilknytning til 110 Sør-Vest gir både privilegert tilgang og en risiko for systematisk bias — særlig ved tolkning av prosedyrer, vurdering av bemanningsstandarder og fortolkning av operatørers arbeidssituasjon. Studien adresserer dette gjennom fire konkrete grep:

1. **Objektive registerdata som primærgrunnlag.** Hovedfunnene springer ut av tidsstempler, ressursvarslinger og kategoriklassifisering i LEO/BRIS — registreringer som er gjort uavhengig av prosjektet og ikke gjenstand for forfatterens tolkning.
2. **Skript-basert, deterministisk analyseflyt.** All bearbeiding er implementert i versjonskontrollerte Python-skript med fast random seed (`SEED_DABA = 20260419`). Analyseflyten er dermed deterministisk gitt valgte parametre — gjentas analysen med samme inngangsdata og samme parametre, gir den identisk resultat. Flere sentrale parametre (D-aba Fase 2-sannsynlighet, L-aba-bindingstid, ikke-D bindingstider) bygger imidlertid på operativ kalibrering og delvis manuell validering og er ikke fri for skjønn (jf. antagelsestabellen i kap 6.7). Sensitivitetsanalysen i avsnitt 7.7 viser at hovedfunnet er robust over rimelige variasjoner i disse parametrene.
3. **Eksplisitt antagelsesdokumentasjon.** Alle modellantagelser er listet med kilde og status (kap 6.7, Tabell 5.5–5.6). Antagelser som hviler på operative samtaler er merket som sådanne — ikke fremstilt som direkte empiri.
4. **Triangulering mellom kilder.** Hvor antagelser bygger på samtaler, kontrolleres de mot prosedyredokumentasjon (Rogaland brann og redning IKS, 2024) og BRIS-tidsstempler. D-aba Fase 1 er for eksempel både prosedyrforankret (~90 sek call-out) og empirisk verifisert (median 74 sek).

Den primære risikoen som disse grepene ikke fullt eliminerer, er valg av modellramme — selve operasjonaliseringen av makkerpar som kapasitetsmetrikk reflekterer forfatterens forståelse av prosedyren og kunne blitt formulert annerledes av en utenforstående forsker. Denne begrensningen drøftes i kap 8.4.

Tre komplementære analysekomponenter benyttes:

**Tabell 5.1: Analysekomponenter**

| Analysekomponent | Primærvariabel | Funksjon |
|---|---|---|
| **Prosedyrbasert ankomstkonfliktmodell** (primær) — variant A: beredskap, variant B: total belastning | Antall aktive hendelser ved hvert anrops ankomsttidspunkt | Måle andel anrop der makkerpar-driftsstandarden ikke kan opprettholdes |
| Erlang-C (M/M/c) (grunnlinje) | λ, μ, c_eff | Tradisjonell køteoretisk referansemodell |
| Benchmarking (alle 12 sentraler) | Bemanning, oppdragsvolum, innbyggertall | Kontekstualisere casefunn mot nasjonal struktur |

Analyseenheten varierer mellom komponentene: i primærmodellen er analyseenheten det enkelte innkommende anropet ved dets ankomsttidspunkt. Variant A avgrenser til beredskapsoppdrag (kategori D — D-pri1 og D-aba) og sammenstilte tilleggsanrop; variant B utvider til alle åtte hendelseskategorier (D-pri1, D-aba, S, L-aba, L-hendelse, L-ukjent, F, V — se avsnitt 5.3.2 og 6.2). I Erlang-C er analyseenheten aggregerte ankomstrater per skifttype, og i benchmarkingen er det den enkelte 110-sentralen.

---

## 5.2 Datakilder

Analysen bygger på fem datakilder med ulik rolle og tilgangsstatus:

**Tabell 5.2: Oversikt over datakilder**

| Kilde | Type | Periode | Rolle i analysen | Tilgang |
|---|---|---|---|---|
| LEO/BRIS hendelsesdata | Registerdata | 2025 | Primærdata — ankomsttidspunkt, bindingstid, hendelsesklassifisering | Intern tilgang |
| DSB MOB-rapporter | Offentlig statistikk | 2022–2025 | Benchmarking — bemanning og volum alle 12 sentraler | Offentlig |
| Prosedyre- og analysedokumenter | Internprosedyre | Gjeldende | Modellparametere — rollestruktur, overløpsregler, VL-funksjon | Intern tilgang |
| Operative valideringssamtaler | Kvalitative data | Mars–april 2026 | Kalibrering og validering av modellforutsetninger | Egne samtaler |
| SSB befolkningsdata | Offentlig statistikk | 2026 | Generaliseringsanalyse — innbyggertall per dekningsområde | Offentlig |

Hovedanalysen er kvantitativ og registerbasert. De kvalitative kildene (prosedyredokumenter og valideringssamtaler) har en støttende funksjon: de brukes til å forankre modellantakelser i operativ virkelighet, ikke som selvstendig empirisk grunnlag for hovedfunnene.

### 5.2.1 LEO/BRIS-data (primærdata)

Primærdatasettet er hendelsesdata fra 110 Sør-Vest eksportert fra LEO/BRIS-systemet. Uttrekket dekker hele kalenderåret 2025 (01.01.2025–31.12.2025) og inneholder 61 964 registrerte hendelser med 44 variabler per hendelse. Datasettet er eksportert som CSV med UTF-8-encoding (med BOM).

Fra høsten 2024 benytter alle tolv norske 110-sentraler det felles oppdragshåndteringssystemet LEO. Valget av 2025 som analyseår sikrer at hele perioden er dekket av det nye systemet, noe som gir bedre datakonsistens enn eldre perioder der systemovergangen kan ha påvirket registreringspraksis.

**Nøkkelvariabler benyttet i analysen:**

| Variabel | Kolonne i datasett | Bruk i analysen |
|---|---|---|
| Ankomsttidspunkt | `Dato anrop`, `Time på døgnet` | Grunnlag for ankomstrate (λ), tidsstempel per hendelse |
| Hendelsestype | `Oppdragstype`, `Opprinnelig oppdragstype`, `Kilde` | Klassifisering i åtte kategorier (D-pri1, D-aba, S, L-aba, L-hendelse, L-ukjent, F, V), se avsnitt 5.3.2 og 6.2 |
| Ressursvarsling | Tidspunkt for ressurs varslet | Identifisering av kategori D (utrykningshendelser) |
| Første ressurs fremme | Tidspunkt for første ressurs fremme | Bindingstidsberegning (akuttfasens varighet) |
| Oppdragsidentifikator | `110_ID` (f.eks. B06-250101-4) | Sekvensgapanalyse for estimering av sammenstilte anrop |
| Sentral | `110-sentral` | Filtrering til 110 Sør-Vest |

**Datakvalitet og strukturelle begrensninger:**

Datasettet har fullstendig dekning for ankomsttidspunkt gjennom hele analyseperioden. Følgende strukturelle begrensninger er identifisert:

**Tabell 5.3: Datakvalitet — strukturelle begrensninger**

| Felt | Dekningsgrad | Konsekvens for analysen |
|---|---|---|
| `Operatør-ID` | 0 % (100 % null) | Serverutnyttelse kan ikke observeres direkte på operatørnivå. Systemstrukturell begrensning bekreftet av DSB (mars 2026) |
| `Innsatsvarighet` | 76,4 % av kategori D (5 771 av 7 555) | Måler total varighet fra utrykning til siste ressurs ledig — kan vare i timer. **[Antagelse 5.1]** Variabelen er ikke benyttet som operatørbindingsmål fordi 110-operatørens binding antas avgrenset til akuttfasen (RØD + GUL), ikke hele innsatsperioden. Antagelsen er forankret i prosedyre og operative samtaler (avsnitt 5.2.4), men ikke direkte målt på operatørnivå (jf. manglende Operatør-ID over) |
| `Alarmbehandlingstid` | 99,0 % av kategori D (7 478 av 7 555) | Tilgjengelig for nesten alle utrykningshendelser |
| Første ressurs fremme | 76,5 % av kategori D (5 777 av 7 555) | Primært mål for bindingstid; resterende 23,5 % imputert med median |

Denne kildens viktigste begrensning er at den viser synlige oppdrag, ikke alle innkommende anrop. Tilleggsanrop som sammenstilles med eksisterende oppdrag forsvinner som egne observasjoner (se avsnitt 5.3.4).

### 5.2.2 DSB MOB-rapporter

Bemannings- og oppdragsdata for alle tolv norske 110-sentraler er hentet fra DSBs årlige rapportering gjennom MOB-systemet (Melding Om Brannvesen). Data foreligger for perioden 2022–2025 og inkluderer antall ansatte, bemanning per vakttype (dag/natt, hverdag/helg), antall operatørplasser og selvrapportert anropsvolum. Denne kilden brukes primært til benchmarking av casefunn mot nasjonal bemanningsstruktur. Denne kildens viktigste begrensning er at bemanningsnivået rapporteres som planlagt minimumsbemanning per vakttype, ikke som faktisk observert bemanning.

### 5.2.3 Prosedyre- og analysedokumenter

Tre interne dokumenter fra 110 Sør-Vest er sentrale for modellkonstruksjonen:

1. **Prosedyre for arbeidsmetodikk, utalarmering og loggføring** (Rogaland brann og redning IKS, 2024, versjon 4). Definerer rollestrukturen (RØD/GUL/GRØNN), makkerpar-prinsippet, VL-rollen og operativ arbeidsmetodikk.

2. **Beredskapsanalyse 110 Vest** (2022). Dokumenterer overløpsmekanismer, herunder 30-sekundersregelen for automatisk overføring til Agder og 10-anrops-køterskel.

3. **Risiko- og sårbarhetsanalyse (ROS) Bergen brannvesen** (2023). Dokumenterer det kvalitative grunnlaget for bemanningsdimensjonering.

Dokumentene er tilgjengelige gjennom forfatterens operative tilknytning til 110 Sør-Vest. Denne kilden brukes primært til å etablere modellparametere (c_eff, kapasitetsnivåer, overløpsregler). Denne kildens viktigste begrensning er at den beskriver prosedyrer og planer, ikke nødvendigvis faktisk etterlevelse i alle situasjoner.

### 5.2.4 Operative valideringssamtaler og LABA-dybdeanalyse

Modellforutsetninger og parameterestimater er validert gjennom tre komplementære kanaler: samtaler med operativt personell, en strukturert manuell dybdeanalyse av 50 L-aba-hendelser, og skriftlige spørreskjemaer til andre sentraler under kalibrering.

**Tabell 5.4: Gjennomførte valideringsaktiviteter**

| Dato | Aktør | Format | Primærtema |
|---|---|---|---|
| 15.03.2026 | Midt-Norge 110 | Telefon (uformell) | Bemanning, servicetesting-organisering |
| Mars–april 2026 | 110 Sør-Vest | Løpende operativ dialog | Makkerpar, bindingstider, VL-rolle, overløp, D-pri1/D-aba-dynamikk |
| 18.04.2026 | Lokal operatør 110 Sør-Vest | Strukturert utfylling (Excel) | LABA-dybdeanalyse: 50 hendelser med tidsstempler fra LEO |
| April 2026 | Lokale operatører 110 Sør-Vest | Intern kalibrering av spørreskjemautkast | Verifisering av tider og spørsmålsformuleringer før utsending |

Kanalene har avgrensede funksjoner: kalibrering av parametere og validering av operativ realisme i modellantakelsene. Konkret har samtalene og dybdeanalysen bidratt med:

- **Samtaletid for Erlang-C:** Vektet gjennomsnittlig samtaletid på 3,44 minutter (brukes kun i Erlang-C-grunnlinjen, ikke i primærmodellen)
- **VL-forutsetningen:** Bekreftelse av at vaktleder normalt ikke besvarer nødanrop direkte
- **Makkerpar-dynamikk for D-pri1 vs D-aba:** Operatørintervju bekreftet at ABA-utrykning ikke følger makkerpar-prosedyre — én operatør utfører kvittering, oppdragsopprettelse og call-out serielt i ~3 min. Dette er grunnlaget for å skille D-pri1 og D-aba som egne kategorier med ulik op-binder-profil (avsnitt 6.4.4–6.4.5)
- **D-aba Fase 2-parametre ($p$, $Y$):** Operatørestimerte verdier for andel D-aba med påfølgende nødtelefon og bindingstid for denne fasen; empirisk underkant-verifisert via sekvensgap-metoden
- **Bindingstid for L-aba:** Kvantitativt kalibrert via LABA-dybdeanalysen (se avsnitt 5.4)
- **Bindingstid for sammenstilte anrop:** Kvalitativt estimat på 1 minutt
- **Organisatoriske forskjeller:** Midt-Norge har dedikert servicepersonell utenfor LEO, noe som påvirker sammenlignbarheten av servicevolum mellom sentraler

**Skriftlige spørreskjemaer til alle tolv sentraler** er utviklet og er under intern kalibrering hos lokale operatører for å verifisere tidsantakelser og formuleringer før utsending. Utsendelse til eksterne sentraler skjer først når tidsgrunnlaget er bekreftet. Denne kildens viktigste begrensning er at den bygger på et begrenset antall samtaler og at operative vurderinger kan variere mellom informanter.

### 5.2.5 SSB befolkningsdata

Innbyggertall per sentrals dekningsområde er hentet fra SSB Statistikkbanken med referansedato 1. januar 2026. Denne kilden brukes primært til generaliseringsanalyse som strukturell prediktor for bemanningsbehov.

### 5.2.6 Datarensing og klargjøring

Følgende steg er gjennomført for å klargjøre primærdatasettet for analyse:

1. **Filtrering:** Datasettet er filtrert til 110 Sør-Vest og analyseperioden 01.01.2025–31.12.2025.
2. **Parsing av tidsvariabler:** `Dato anrop` er konvertert fra strengformat (`%d.%m.%Y`) til datetime-objekter. `Time på døgnet` er brukt til å konstruere fullstendige tidsstempler.
3. **Konstruksjon av skifttype:** Hvert anrop er klassifisert som dag (07:00–18:59) eller natt (19:00–06:59), og som hverdag (mandag–fredag) eller helg (lørdag–søndag), basert på tidsstempel. Dette gir fire skifttyper: dag/hverdag, dag/helg, natt/hverdag, natt/helg.
4. **Kontroll av sekvensnumre:** `110_ID`-feltets daglige sekvensnumre er ekstrahert og kontrollert for gap. Manglende sekvensnumre er registrert som estimerte sammenstilte anrop.
5. **Håndtering av manglende verdier:** For kategori D-hendelser uten registrert tidspunkt for første ressurs fremme (23,5 %) er median bindingstid fra observerte verdier brukt som imputeringsverdi. Øvrige manglende felt (operatør-ID, innsatsvarighet) er dokumentert som strukturelle begrensninger, ikke imputert.
6. **Håndtering av ekstreme verdier:** Bindingstider er kontrollert for negative verdier og urealistisk lange varigheter. Beregningene bygger på registrerte tidsstempler og er ikke manuelt justert.
7. **Encoding:** CSV-filen er lest med `encoding='utf-8-sig'` for å håndtere BOM-markør. Sentralnavn med encoding-avvik er normalisert via en oppslagstabell.

**Tilleggsbearbeiding for nasjonal benchmarking (kap 7.8 og 8.4.1):** Det nasjonale BRIS-datasettet for 2025 (508 228 oppdrag, alle 12 sentraler) er bearbeidet med samme V3-klassifiseringsregel som primærdatasettet (`Kilde = Alarm`-krav for L-aba og D-aba). Bearbeidingen er nødvendig fordi sentralnavn forekommer med ulike encoding-varianter (f.eks. `S?r-Vest 110`, `S\u00f8r-Vest 110`, `Sør-Vest 110`) og fordi `Opprinnelig oppdragstype` har ulik dekningsgrad mellom sentraler. To konkrete grep er gjort: (i) sentralnavn normaliseres via `SENTRALER_NORM`-oppslagstabellen i `analyse/scripts/benchmark_trend_analyse.py`; (ii) L-aba/D-aba-andelen rapporteres uten å justeres for ulik dekningsgrad — variasjonen mellom sentraler (0,0–7,5 %) tolkes derfor eksplisitt som indikasjon på heterogen registreringspraksis (jf. kap 8.4.1), ikke som direkte sammenlignbare nivåer. Den prosedyrbaserte ankomstkonfliktmodellen er per nå kjørt på 110 Sør-Vest alene; nasjonal modellanvendelse forutsetter klassifiseringsharmonisering (kap 9.4).

---

## 5.3 Databehandling og operasjonalisering

Dette avsnittet beskriver hvordan rådataene er transformert til analytiske variabler. Selve modellformuleringen presenteres i kapittel 6.

### 5.3.1 Analyseenheter: anrop, oppdrag og hendelse

Analysen opererer med tre distinkte enheter som må holdes adskilt:

- **Anrop:** En faktisk innkommende telefon eller varsling til sentralen. Hvert anrop binder en operatør.
- **Oppdrag:** En registrert sak i LEO/BRIS. Flere anrop kan sammenstilles i ett oppdrag.
- **Hendelse:** Den operative situasjonen sentralen håndterer. Én hendelse kan generere flere anrop fra ulike innringere.

I primærmodellen er analyseenheten det enkelte anropet ved dets ankomsttidspunkt, fordi det er anropet — ikke oppdraget — som binder operatørkapasitet. Skillet er sentralt fordi antall synlige oppdrag i datasettet undervurderer antall faktiske anrop (se avsnitt 5.3.4).

### 5.3.2 Klassifisering av hendelser

Hendelsene i datasettet er klassifisert i åtte kategorier basert på tre BRIS-felt: `Oppdragstype` (sluttklassifisering), `Opprinnelig oppdragstype` (initiell hendelsestype) og `Kilde` (Alarm/Samtale/blank — innringingskanal):

- **D-pri1** (Pri-1-utrykning): Hendelser med ressursvarsling som ikke er ABA-utløst. Byggingsbrann, trafikkulykke, farlig gods, etc. Krever makkerpar-prosedyre.
- **D-aba** (ABA-utløst utrykning): Hendelser med ressursvarsling der `Opprinnelig = "ABA"` og `Kilde = "Alarm"`. Ikke pri-1, håndteres serielt.
- **S** (Service): Overføringstester av brannalarmanlegg
- **L-aba** (ABA løst av 110): Automatisk brannalarm avklart uten utrykning — krever `Kilde = Alarm`
- **L-hendelse** (Reell hendelse løst av 110): Innringer melder reell situasjon, løst uten ressurs. Inkluderer ABA-oppdrag med `Kilde = Samtale` (publikumsmelding om brannalarm uten ABA-signal)
- **L-ukjent** (Løst av 110, uklassifisert): Henvendelser uten formell opprinnelig oppdragstype
- **F** (Feilringing): Feilringing, ikke-nødmelding, eCall feil
- **V** (Viderevarsling): Viderekobling til annen etat eller intern varsling

**Kilde = Alarm-kravet:** LABA-dybdeanalysen (avsnitt 5.4) viste at 24,5 % av oppdrag klassifisert med `Opprinnelig = ABA` faktisk ikke representerer automatisk brannalarm i operativ forstand — de inkluderer publikumsmeldinger om brannalarm, privat bygg uten 110-tilknytning, tester feilrevidert som oppdrag og duplikatoppdrag. Ved å kreve `Kilde = Alarm` for L-aba og D-aba skilles ekte ABA-signaler fra disse feilklassifiseringene. Oppdrag som tidligere ville vært L-aba men har `Kilde = Samtale` eller blank reklassifiseres til L-hendelse.

**D-pri1 vs D-aba-splitt:** Operatørintervju (avsnitt 5.2.4) og prosedyrereferanse (Rogaland brann og redning IKS, 2024) etablerer at pri-1-utrykning og ABA-utløst utrykning har fundamentalt ulik operativ dynamikk — makkerpar versus serial solo-håndtering. Denne splittingen er nødvendig for at kapasitetsmodellen skal reflektere korrekt op-binder-profil per hendelsestype (avsnitt 6.4).

Av 61 964 synlige hendelser i 2025 klassifiseres 4 499 (7,3 %) som D-pri1 og 3 056 (4,9 %) som D-aba. Primærmodellen (variant A) avgrenses til disse beredskapskategoriene pluss sammenstilte anrop. Den utvidede modellen (variant B) inkluderer alle åtte kategorier med empirisk kalibrerte eller operativt estimerte bindingstider. Fullstendig klassifiseringslogikk og operative beskrivelser er gitt i avsnitt 6.2.

### 5.3.3 Beregning av bindingstid

Bindingstid og antall operatører bundet per hendelse er differensiert per kategori fordi ulike hendelsestyper har ulik operativ dynamikk:

**D-pri1 (databasert, makkerpar-bundet):**

> **Bindingstid = (Første ressurs fremme − Dato/tid anrop) + 3 minutter kvitteringsvindu**
> **Ops bundet = 2 (makkerpar: RØD + GUL parallelt)**

Beregningen bygger på to registrerte tidsstempler: `Dato/tid anrop` og `Første ressurs fremme`. Kvitteringsvinduet på 3 minutter reflekterer at GUL-operatøren etter mottatt vindusmelding kvitterer og loggfører før kapasitet frigjøres. For de ~25 % av D-pri1-hendelsene som mangler tidspunkt for første ressurs fremme, er median bindingstid fra de observerte verdiene (14,1 minutter) brukt som imputeringsverdi.

**D-aba (operativ prosedyre + BRIS-verifisert):**

> **Fase 1 (alltid): 3 min × 1 operatør** — kvittering + oppdragsopprettelse + call-out
> **Fase 2 (med sannsynlighet p): Y min × 1 operatør** — nødtelefon + panel-veiledning, starter 90 sek etter Fase 1

Fase 1-varigheten er forankret i operativ prosedyre og verifisert empirisk: median tid fra anrop til ressurs varslet er 74 sek for D-aba (P75 = 80, P90 = 111) — konsistent med operativ beskrivelse av ~90 sek call-out. Med etterfølgende registrering estimeres Fase 1 til 3 min. Fase 2-parametrene ($p$, $Y$) varieres i tre scenarioer (lav/hoved/høy: $p = 0{,}30/0{,}50/0{,}70$; $Y = 3/6/10$ min), og hoved-scenarioet $p = 0{,}50$, $Y = 6$ min er grunnlaget i primæranalysen.

**L-aba (empirisk kalibrert, LABA-dybdeanalyse n = 100 Kilde=Alarm):**

> **Bindingstid = 4,5 min × 1 operatør (hoved)**

Bindingstiden for L-aba er kalibrert via en strukturert manuell dybdeanalyse i to runder (avsnitt 5.4). Hovedparameteren bygger på utvidet utvalg (n = 100, alle Kilde=Alarm) med mean 4,53 min og 95 % CI [3,74; 5,43] minutter. Forrige rapportversjon brukte n=30-anslaget (mean 5,88 min, CI [3,70; 8,56]) og er erstattet i denne versjonen.

**Øvrige kategorier (operativt estimert, sensitivitetsscenarioer):**

S: 1/2/4 min; L-hendelse: 3/5/8 min; L-ukjent: 1/3/5 min; F: 0,25/0,5/1 min; V: 0,5/1/2 min. Hovedscenario benyttes i primærresultatene; lavt og høyt i sensitivitetsanalyse (avsnitt 7.7).

**Sammenstilte tilleggsanrop:** 1 min × 1 operatør. **[Antagelse 5.2]** Forenklet estimat basert på operativ vurdering, ikke en direkte observasjon. Sensitivitetsanalysen i avsnitt 7.7 viser at hovedfunnet er robust over rimelige variasjoner.

### 5.3.4 Estimering av sammenstilte anrop

Når flere innringere melder om samme hendelse, sammenstilles tilleggsanropene med det eksisterende oppdraget i LEO/BRIS. Disse forsvinner da som egne observasjoner i datasettet. Metoden for å estimere antallet er basert på sekvensnummerlogikken i `110_ID`-feltet:

- Hvert synlige oppdrag tildeles et daglig sekvensnummer (f.eks. B06-250101-4, B06-250101-6).
- Manglende sekvensnumre i rekken (i dette tilfellet -5) tolkes som anrop som ble sammenstilt med et eksisterende oppdrag.
- Tidspunkt for sammenstilte anrop er interpolert fra nærmeste synlige oppdrags ankomsttidspunkt, da det eksakte tidspunktet ikke er registrert.

Metoden forutsetter at LEO tildeler sekvensnumre kronologisk og uten andre årsaker til gap. For 2025 er det gjennom denne metoden estimert 18 901 sammenstilte anrop (korreksjonsfaktor 1,305x). Et viktig forbehold er at metoden identifiserer at et anrop ble sammenstilt, men ikke hvilket oppdrag det ble knyttet til.

### 5.3.5 Konstruksjon av kapasitetsvariabler

Fra rådataene konstrueres følgende analytiske variabler for hvert beredskapsanrop:

1. **Aktiv op-binder ved ankomst** ($n_{\text{aktive}}$): Sum av `ops_bundet` for tidligere op-binder-events hvis bindingstid ennå ikke er utløpt ved det aktuelle anropets ankomsttidspunkt. D-pri1 bidrar med 2 op-binder per hendelse; øvrige kategorier med 1.
2. **Ledige operatører**: $c_{\text{eff}} - n_{\text{aktive}}$, der $c_{\text{eff}}$ er effektiv operatørkapasitet for gjeldende skifttype.
3. **Kapasitetsnivå**: Klassifisert som Normal (ledige $\geq$ 2), Brudd på driftsstandard (ledige = 1) eller Svikt (ledige $\leq$ 0).

Verdien av $c_{\text{eff}}$ er satt til 3 for dag/hverdag og 2 for øvrige skifttyper, basert på minimumsbemanning minus vaktleder (se avsnitt 4.2.1). Den matematiske formuleringen er gitt i avsnitt 6.4.7.

**Tabell 5.5: Observasjonsstatus for sentrale variabler**

| Variabel | Status | Grunnlag |
|---|---|---|
| Dato/tid anrop | Direkte observert | BRIS/LEO |
| Ressurs varslet | Direkte observert | BRIS/LEO |
| Første ressurs fremme | Direkte observert (~75 % av D-pri1) | BRIS/LEO |
| Bindingstid D-pri1 | Beregnet fra observerte tidsstempler; ~25 % imputert med median | BRIS/LEO + imputering |
| Bindingstid D-aba Fase 1 | Operativ prosedyre + BRIS-verifisert (median 74 sek call-out) | Prosedyre + BRIS |
| Bindingstid D-aba Fase 2 ($p$, $Y$) | Operatørinformert, empirisk underkant-verifisert | Samtaler + sekvensgap |
| Bindingstid L-aba | Empirisk kalibrert (mean 4,53 min, n=100, CI [3,74; 5,43]) | LABA-dybdeanalyse runde 2 |
| Bindingstider S, L-hendelse, L-ukjent, F, V | Operative estimater, tre sensitivitetsscenarioer | Samtaler + vaktleder-validering |
| Sammenstilte anrop (antall) | Estimert | Sekvensgapanalyse |
| Sammenstilte anrop (tidspunkt) | Interpolert | Nærmeste synlige oppdrag |
| Bindingstid sammenstilte anrop | Forenklet antakelse (1 min) | Operativ vurdering |
| c_eff | Operativt definert parameter | Prosedyre + valideringssamtaler |

---

## 5.4 LABA-dybdeanalyse — empirisk kalibrering av L-aba-bindingstid

For å kalibrere bindingstidsestimatet for L-aba er det gjennomført en strukturert dybdeanalyse i to runder ved 110 Sør-Vest 2025. Første runde omfattet 50 trukne hendelser (49 gyldige) og ga en innledende kalibrering med betydelig restusikkerhet. Andre runde utvidet utvalget til **100 hendelser (alle med gyldige tidsstempler, alle Kilde=Alarm)**, og er grunnlaget for den endelige modellparameteren. **Den standardiserte LABA-omtalen i rapporten er derfor: 100 trukne / 100 gyldige / Kilde=Alarm-subset (hovedparameter, n = 100).** Den første runden (n=49 totalt / n=30 Kilde=Alarm-subset, mean 5,88 min med CI [3,70; 8,56]) er metodisk dokumentert i `analyse/notat_V3_modellutvikling.md`.

Analysen har to formål: (1) empirisk måling av faktisk operatørbindingstid for automatiske brannalarmer løst uten utrykning, og (2) vurdering av klassifiseringsnøyaktigheten i BRIS L-aba-kategorien.

### 5.4.1 Utvalgsdesign

Populasjonen består av 3 430 L-aba-hendelser for 110 Sør-Vest 2025 (etter V3-klassifisering med Kilde=Alarm-krav). Utvalget for runde 2 er stratifisert på måned for å sikre jevn dekning over året:

- 8 hendelser per måned × 8 måneder + 9 hendelser per måned × 4 måneder = 100 hendelser
- Tilfeldig utvalg innen hver måned med fast seed (`SEED = 20260418`) for reproduserbarhet
- Utvalgsandel: 2,9 %

### 5.4.2 Gjennomføring

For hver hendelse i utvalget åpnet en operatør ved 110 Sør-Vest LEO-loggen og registrerte fire tidsstempler:

- `T_alarm_inn` — når ABA-signalet ble mottatt i LEO
- `T_nødtelefon_inn` — når eventuell nødtelefon fra stedet ble besvart
- `T_avklart` — når operatør bekreftet ufarlig årsak
- `T_operatør_frigjort` — når oppdraget ble lukket

Bindingstid beregnes automatisk som $T_{\text{operatør\_frigjort}} - T_{\text{alarm\_inn}}$. Kommentarfelt ble brukt til observasjoner om klassifiseringsavvik, datakvalitet og operative særtrekk. Av de 100 hendelsene var 78 registrert med påfølgende nødtelefon fra stedet (subgruppe-mean 4,41 min, median 3,30 min) og 22 uten (subgruppe-mean 4,95 min, median 2,59 min).

### 5.4.3 Resultater

**Kilde = Alarm-subset, n = 100 (modellparameter):**

| Metrikk | Verdi |
|---|---:|
| Mean bindingstid | **4,53 min** |
| Median | 3,27 min |
| Standardavvik | 4,37 min |
| Min | 0,57 min |
| P25 | 1,80 min |
| P75 | 5,18 min |
| P90 | 9,48 min |
| P95 | 13,58 min |
| Max | 25,23 min |
| **95 % CI mean (bootstrap, 10 000 resampling)** | **[3,74; 5,43]** |

**Sammenligning runde 1 (n=30) → runde 2 (n=100):**

| Metrikk | Runde 1 (n=30) | Runde 2 (n=100) | Endring |
|---|---|---|---|
| Mean | 5,88 min | 4,53 min | −1,35 min (−23 %) |
| Median | 2,87 min | 3,27 min | +0,40 min |
| P90 | 11,51 min | 9,48 min | −2,03 min |
| 95 % CI-bredde | 4,86 min | 1,69 min | redusert til 35 % |

Mean fra runde 2 er **utenfor** 95 % CI fra runde 1 (5,88 lå innenfor [3,70; 8,56], men 4,53 ligger nærmere CI-nedre). Standardavvik (4,37 min) reflekterer at fordelingen forblir høyreskjev — drevet av langhalede tilfeller (industrivern-oppfølging, varmekamera-avklaring), men terskelen for «høy bindingstid» er lavere enn antatt i runde 1.

### 5.4.4 Klassifiseringsobservasjoner

Operatørens kommentarer (begge runder) avdekket at en betydelig andel L-aba-oppdrag ikke representerer automatisk brannalarm i operativ forstand. I runde 1 (n=49) var dette 12 av 49 (24,5 %), fordelt på følgende kategorier:

| Kategori | N (av 49) |
|---|---:|
| «Privat brannalarm uten tilknytting til 110» (ikke ISM-kunde) | 4 |
| «Kun nødanrop, ikke alarm i ISM» (publikumsmelding, ikke ABA-signal) | 3 |
| «Test av anlegg / øvelse feilrevidert» (burde vært kategori S) | 3 |
| «Innbruddsalarm ikke innlagt i ISM» (feilkategorisert) | 1 |
| «Ikke i henhold til prosedyre» | 1 |

Disse hendelsene har det til felles at `Kilde = Samtale` eller blank, mens ekte ABA-signal har `Kilde = Alarm`. Observasjonen motiverte V3-klassifiseringsregelen som krever `Kilde = Alarm` for L-aba og D-aba (avsnitt 5.3.2 og 6.2). Runde 2 (n=100, alle Kilde=Alarm) bekrefter at klassifiseringsregelen virker som tilsiktet — alle 100 trukne hendelser er ekte ABA-signaler i operativ forstand.

### 5.4.5 Valgte parametre og sensitivitet

Basert på n=100-resultatet velges mean **4,53 min ≈ 4,5 min** som hovedverdi. Median ville undervurdere eksponeringen fordi fordelingen er høyreskjev. Sensitivitetsscenarioer i variant B er justert tilsvarende: lav (3 min, CI-nedre), hoved (4,5 min, empirisk mean), høy (7 min, over CI-øvre). Tidligere scenarioer (3/6/9 min basert på n=30) er erstattet.

### 5.4.6 Begrensninger

- **Utvalgsstørrelse:** n = 100 gir 95 % CI ±0,85 min for mean — substansielt strammere enn n=30-runden (±2,4 min). Restusikkerheten er lav nok til at parameteren kan brukes som empirisk kalibrert hovedverdi, ikke kun orienteringsanslag.
- **Enkelt-operatør-perspektiv:** Utfyllingen er gjort av én operatør. Flere operatører ville kunne vurdere klassifiseringstvil ulikt — men siden runde 2 kun trekker fra Kilde=Alarm-subsettet er rommet for klassifiseringstvil betydelig redusert.
- **Tre ekstreme verdier (>15 min):** Av 100 hendelser har 3 bindingstid over 15 min. To har eksplisitt forklarende kommentar (én «feilrevidert», én «nødanrop ikke lagt til, baserer tid på første logglinje») og kunne potensielt utelates. Mean uten disse 3: ca. 4,1 min. Tallet 4,5 min beholdes som hovedparameter for konservatisme.
- **Datakvalitetsobservasjon ikke reell feilmelding:** Analysen avdekket uventet variasjon i loggkvalitet. Enkelte hendelser har mangelfulle eller fraværende tidsstempler i LEO. Dette er rapportert tilbake til 110 Sør-Vest som empirisk datakvalitetsinput.

Fullstendig metodebeskrivelse, resultattabeller og kommentarlogg er gitt i `analyse/notat_V3_modellutvikling.md` og det utfylte datasettet `analyse/uttrekk/Kopi av laba_sorvest_2025_dybdeanalyse_n100-ferdig utfylt.xlsx`.

---

## 5.5 Analysegjennomføring

Analysen er gjennomført i følgende steg:

**Tabell 5.6: Analysesteg**

| Steg | Beskrivelse | Datakilde | Type |
|---|---|---|---|
| 1 | Filtrering av primærdatasettet til 110 Sør-Vest, 2025 | BRIS/LEO | Direkte |
| 2 | V3-klassifisering av alle hendelser i 8 kategorier (D-pri1, D-aba, S, L-aba, L-hendelse, L-ukjent, F, V) | BRIS/LEO (Oppdragstype, Opprinnelig, Kilde) | Beregnet |
| 3 | Beregning av bindingstid for observerte D-pri1 (median 14,1 min) | BRIS/LEO | Beregnet |
| 4 | Imputering av bindingstid for D-pri1 uten fremme-tidspunkt med median | Steg 3 | Imputert |
| 5 | Ekspansjon av D-aba til Fase 1 (alltid) + Fase 2 (med sannsynlighet $p$) | Operativ prosedyre + scenarioer | Modellbasert |
| 6 | Empirisk kalibrering av L-aba-bindingstid til 4,5 min | LABA-dybdeanalyse n=100 (avsnitt 5.4) | Empirisk |
| 7 | Estimering av sammenstilte anrop gjennom sekvensgap i 110_ID: 18 901 anrop | BRIS/LEO | Estimert |
| 8 | Ekspansjon av hver hendelse til op-binder-events med (bindingstid, ops_bundet) | Steg 2–7 | Beregnet |
| 9 | Sweep-algoritme: beregn $n_{\text{aktive}}$ ved hvert ankomsttidspunkt | Steg 8 | Beregnet |
| 10 | Klassifisering av kapasitetsnivå (Normal / Brudd / Svikt) per beredskapsanrop | Steg 9 + c_eff | Beregnet |
| 11 | Beregning av Erlang-C (M/M/c) som referansemodell | BRIS/LEO + samtaler | Beregnet |
| 12 | Scenarioanalyse: +1 operatør per skifttype | Steg 9–10 med endret c_eff | Modellbasert |
| 13 | Benchmarking mot alle 12 sentraler via DSB MOB-data og DSB 2025-fullrapport | DSB MOB + DSB 2025 + SSB | Direkte |

Steg 1–8 representerer databehandling og operasjonalisering. Steg 9–10 er primæranalysen. Steg 11–13 er supplerende analyser. Steg som er markert som «direkte» bygger på observerte registerdata, mens «estimert», «imputert», «empirisk» og «modellbasert» innebærer metodiske valg som må tas med i tolkningen av resultatene.

---

## 5.6 Validitet, reliabilitet og begrensninger

### 5.6.1 Målevaliditet

Analysens sentrale metrikk — kapasitetsnivå ved ankomst — bygger på observerte tidsstempler for D-pri1-hendelser (som kan identifiseres robust gjennom ressursvarsling) og på empirisk kalibrerte bindingstider for L-aba (LABA-dybdeanalyse, avsnitt 5.4). Følgende forhold begrenser målevaliditeten:

- **Ikke alle bindingstider er empirisk målt.** D-pri1 og L-aba bygger på direkte observasjon (databasert respektive LABA-dybdeanalyse). D-aba Fase 1 er forankret i operativ prosedyre og empirisk verifisert (median 74 sek call-out). D-aba Fase 2 og øvrige kategorier (S, L-hendelse, L-ukjent, F, V) er operative estimater validert av vaktleder. Sensitivitetsanalysen (avsnitt 7.7) viser at hovedfunnet er robust over hele spennet av rimelige antakelser.
- **Sammenstilte anrop estimeres indirekte.** Sekvensgapmetoden gir et estimat på antall, men det eksakte tidspunktet og varigheten for hvert enkelt anrop er ikke observert.
- **D-aba Fase 2-sannsynligheten $p$ er delvis empirisk underbygd.** Sekvensgap-metoden gir underkant-estimat (17–37 % avhengig av tidsvindu) fordi nødtelefoner logget inni hovedoppdraget er usynlige. Hovedscenario $p = 0{,}50$ reflekterer operatørens kvalitative vurdering.
- **Imputering med median.** De ~25 % av D-pri1-hendelsene med imputert bindingstid kan avvike fra faktisk varighet, særlig for tyngre hendelser.
- **LABA-dybdeanalysen har fortsatt begrenset utvalgsstørrelse, men er styrket i runde 2 (n = 100 for Kilde=Alarm).** 95 % CI for mean er [3,74; 5,43], som gjør L-aba-parameteren langt bedre kalibrert enn runde 1 (n = 30), men fortsatt avgrenset til 110 Sør-Vest 2025.

Begrensningene trekker i hovedsak i én retning: mot at analysen gir et konservativt estimat av faktisk kapasitetsbelastning.

### 5.6.2 Reliabilitet og reproduserbarhet

Analysen bygger primært på registerdata fra et nasjonalt system (LEO/BRIS), noe som gir høy sporbarhet og konsistens. Sekvensgapmetoden for sammenstilte anrop og D-aba Fase 2-stokastikken er systematiske og bruker fast random seed (`SEED_DABA = 20260419`) for reproduserbarhet. Alle analysesteg er implementert i skriptbasert arbeidsflyt (se avsnitt 5.8), noe som muliggjør konsistent reproduksjon.

Valideringssamtalene er vanskeligere å reprodusere eksakt, men brukes kun til å kalibrere parametere som er eksplisitt dokumentert (Tabell 5.5). En annen forsker med tilgang til samme data, prosedyredokumenter og `notat_V3_modellutvikling.md` vil kunne gjenta analysen med de dokumenterte parameterverdiene.

### 5.6.3 Avgrensninger

- **Én hovedcase.** Primæranalysen er begrenset til 110 Sør-Vest. Overførbarhet til andre sentraler er plausibel, men ikke empirisk testet.
- **Analyseår 2025.** Datagrunnlaget dekker ett kalenderår. Sesongvariasjoner fanges, men årlige svingninger og langtidstrender er ikke adressert.
- **Begrenset dekning av ikke-D-kategorier i variant A.** Øvrige kategorier inkluderes i variant B; hovedfunnet for variant A er en avgrenset beredskapsmetrikk, ikke total operatørbelastning.
- **Operatør-ID er strukturelt fraværende.** Individuell serverbelastning kan ikke observeres direkte. Denne begrensningen gjelder for alle norske 110-sentraler.
- **Benchmarkingdata er planlagt minimum.** MOB-dataene viser planlagt minimumsbemanning, ikke faktisk observert bemanning på enkeltvakter.
- **Poisson-forutsetning ikke formelt testet.** Erlang-C-grunnlinjen forutsetter Poisson-ankomster; dette er ikke empirisk validert. Primærmodellen er imidlertid ikke avhengig av denne antagelsen.

---

## 5.7 Etiske vurderinger og rolleforståelse

Prosjektet benytter anonymiserte registerdata der ingen personopplysninger er tilgjengelige — operatør-ID er strukturelt fraværende i BRIS-eksporter. Valideringssamtaler er gjennomført som operative fagsamtaler, ikke som formelle forskningsintervjuer, og inneholder ikke personidentifiserbar informasjon. Studien er ikke vurdert å kreve godkjenning fra Sikt (tidligere NSD), da den ikke behandler personopplysninger.

Forfatterens operative tilknytning til 110 Sør-Vest gir tilgang til dokumenter og operativ kontekst, men innebærer også nærhet til caset som kan påvirke tolkninger. Denne dobbeltposisjonen er håndtert gjennom:

- **Registerbasert hovedanalyse:** Hovedfunnene bygger på kvantitative data fra registersystemer, ikke subjektive vurderinger.
- **Eksplisitt dokumentasjon:** Alle modellforutsetninger og parametere er dokumentert slik at analysen er etterprøvbar (Tabell 5.5 og 5.6).
- **Tydelig skille mellom observert og antatt:** Tabell 5.5 angir eksplisitt hvilke variabler som er direkte observert, beregnet, estimert eller antatt.
- **Nasjonal benchmarking som korrektiv:** Casefunnene kontekstualiseres mot data fra alle tolv sentraler for å motvirke at lokale særtrekk overtolkes.

---

## 5.8 Implementasjon og verktøy

Alle analyser er implementert i Python med skriptbasert arbeidsflyt. Sentrale biblioteker er `pandas` og `numpy` for databehandling, `scipy` for statistiske beregninger og Erlang-C-formelen, `matplotlib` og `seaborn` for visualisering, og `openpyxl` for lesing av Excel-filer. Alle figurer og tabeller i rapporten er generert fra samme analysegrunnlag.

Kildekode og analyseskript er versjonskontrollert på GitHub. Sentrale skript:

| Skript | Funksjon |
|---|---|
| `analyse/scripts/konflikt_total_belastning.py` | Primærmodell (variant A og B) med op-binder-semantikk |
| `analyse/scripts/scenario_pluss1.py` | Scenarioanalyse (+1 operatør) |
| `analyse/scripts/bindingstid_analyse.py` | Bindingstidsberegning og fordeling |
| `analyse/scripts/benchmark_trend_analyse.py` | Benchmarking alle 12 sentraler (MOB 2022–2025) |
| `analyse/scripts/nasjonal_oversikt.py` | Nasjonal DSB 2025-analyse (alle 12 sentraler) |
| `analyse/scripts/nasjonal_2025_analyse.py` | Nasjonal per sentral-analyse (kategorier, tidsdata) |
| `analyse/scripts/uttrekk_laba_sorvest.py` | Stratifisert utvalgsgenerering for LABA-dybdeanalyse |

Parameterkalibrering og modellutvikling er dokumentert i `analyse/notat_V3_modellutvikling.md` som inkluderer endringslogg, beslutningsrasjonale og fullstendig modellspesifikasjon.

Generative KI-verktøy (Claude Code av Anthropic og ChatGPT av OpenAI) er benyttet som støtteverktøy for koding, litteratursøk og rapportskriving. All bruk er dokumentert med dato, kontekst og hva som ble produsert (se Vedlegg D / `KI_erklæring_LOG650_G20_Rune.md`). Alle analytiske beslutninger, tolkninger og konklusjoner er forfatterens egne. Den deterministiske, skript-baserte analyseflyten beskrevet over (refleksivitetsavsnittet i 5.1) sikrer at KI-verktøyenes rolle er begrenset til kode- og tekststøtte — ikke til generering av modellresultater eller tolkninger.

---

Samlet gir datagrunnlaget et godt grunnlag for å modellere den best observerbare og mest beredskapsdimensjonerende delen av operatørbindingen, samtidig som enkelte belastningselementer må estimeres eller empirisk kalibreres. På dette grunnlaget utvikles i neste kapittel modellrammeverket for kapasitetsanalysen.

---

*Kap 5 — Versjon 3.0 | Sist oppdatert: 2026-04-19 (V3 op-binder-semantikk, LABA-dybdeanalyse, D-pri1/D-aba-splitt)*
