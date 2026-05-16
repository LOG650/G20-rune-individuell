# 5. Metode og data

## 5.1 Forskningsdesign

Prosjektet er gjennomført som en kvantitativ casestudie av 110 Sør-Vest, supplert med nasjonal benchmarking for å kontekstualisere casefunnene. Forskningsdesignet er retrospektivt og planleggingsrettet: analysen baseres på historiske hendelsesdata for å vurdere om faktisk bemanning samsvarer med observert belastning.

Casestudiedesignet er valgt fordi problemstillingen er tett knyttet til en spesifikk organisatorisk og operativ kontekst. Bemanning, arbeidsmetodikk og registreringspraksis må forstås samlet for å kunne modellere kapasitetsbinding. Forfatteren har operativ tilknytning til 110 Sør-Vest. Det gir tilgang til prosedyredokumentasjon, beredskapsanalyse og operative informanter, alle nødvendige for å konstruere og validere modellparametere. Modellrammeverket er utviklet for å være overførbart til andre sentraler gitt tilsvarende datatilgang (se avsnitt 6.1 og 7.7).

### Refleksivitet: insider-forskning og objektivitetstiltak

Forfatterens operative tilknytning til 110 Sør-Vest gir både privilegert tilgang og en risiko for systematisk bias. Bias-risikoen er størst ved tolkning av prosedyrer, vurdering av bemanningsstandarder og fortolkning av operatørers arbeidssituasjon. Studien adresserer dette gjennom fire konkrete grep:

1. **Objektive registerdata som primærgrunnlag.** Hovedfunnene springer ut av tidsstempler, ressursvarslinger og kategoriklassifisering i LEO/BRIS. Disse registreringene er gjort uavhengig av prosjektet og er ikke gjenstand for forfatterens tolkning.
2. **Skript-basert, deterministisk analyseflyt.** All bearbeiding er implementert i versjonskontrollerte Python-skript med fast random seed (`SEED_DABA = 20260419`). Analyseflyten er deterministisk gitt valgte parametre. Gjentas analysen med samme inngangsdata og samme parametre, gir den identisk resultat. Flere sentrale parametre bygger imidlertid på operativ kalibrering og delvis manuell validering (D-aba Fase 2-sannsynlighet, L-aba-bindingstid, ikke-D bindingstider). Disse er ikke fri for skjønn, jf. antagelsestabellen i kap 6.7. Sensitivitetsanalysen i avsnitt 8.3 viser at hovedfunnet er robust over rimelige variasjoner i disse parametrene.
3. **Eksplisitt antagelsesdokumentasjon.** Alle modellantagelser er listet med kilde og status (kap 6.7, Tabell 6.3), og observasjonsstatus/analysegjennomføring er oppsummert i Tabell 5.5 og 5.6. Antagelser som hviler på operative samtaler er merket som sådanne, og er ikke fremstilt som direkte empiri.
4. **Triangulering mellom kilder.** Hvor antagelser bygger på samtaler, kontrolleres de mot prosedyredokumentasjon (Rogaland brann og redning IKS, 2024) og BRIS-tidsstempler. D-aba Fase 1 er for eksempel både prosedyrforankret (cirka 90 sek call-out) og empirisk verifisert (median 74 sek).

Den primære risikoen som disse grepene ikke fullt eliminerer, er valg av modellramme. Operasjonaliseringen av makkerpar som kapasitetsmetrikk reflekterer forfatterens forståelse av prosedyren. En utenforstående forsker kunne ha formulert metrikken annerledes. Denne begrensningen drøftes i kap 9.4.

Tre komplementære analysekomponenter benyttes:

**Tabell 5.1: Analysekomponenter**

| Analysekomponent | Primærvariabel | Funksjon |
|---|---|---|
| **Prosedyrbasert ankomstkonfliktmodell** (primær), variant A: beredskap, variant B: total belastning | Antall aktive hendelser ved hvert anrops ankomsttidspunkt | Måle andel anrop der makkerpar-driftsstandarden ikke kan opprettholdes |
| Erlang-C (M/M/c) (grunnlinje) | λ, μ, c_eff | Tradisjonell køteoretisk referansemodell |
| Benchmarking (alle 12 sentraler) | Bemanning, oppdragsvolum, innbyggertall | Kontekstualisere casefunn mot nasjonal struktur |

Analyseenheten varierer mellom komponentene. I primærmodellen er analyseenheten det enkelte innkommende anropet ved dets ankomsttidspunkt. Variant A avgrenser til beredskapsoppdrag (kategori D: D-pri1 og D-aba) og sammenstilte tilleggsanrop. Variant B utvider til alle åtte hendelseskategorier (D-pri1, D-aba, S, L-aba, L-hendelse, L-ukjent, F, V; se avsnitt 5.3.2 og 6.2). I Erlang-C er analyseenheten aggregerte ankomstrater per skifttype. I benchmarkingen er det den enkelte 110-sentralen.

---

## 5.2 Datakilder

Analysen bygger på fem datakilder med ulik rolle og tilgangsstatus:

**Tabell 5.2: Oversikt over datakilder**

| Kilde | Type | Periode | Rolle i analysen | Tilgang |
|---|---|---|---|---|
| LEO/BRIS hendelsesdata | Registerdata | 2025 | Primærdata: ankomsttidspunkt, bindingstid, hendelsesklassifisering | Intern tilgang |
| DSB MOB-rapporter | Offentlig statistikk | 2022 til 2025 | Benchmarking: bemanning og volum alle 12 sentraler | Offentlig |
| Prosedyre- og analysedokumenter | Internprosedyre | Gjeldende | Modellparametere: rollestruktur, overløpsregler, VL-funksjon | Intern tilgang |
| Operative valideringssamtaler | Kvalitative data | Mars til april 2026 | Kalibrering og validering av modellforutsetninger | Egne samtaler |
| SSB befolkningsdata | Offentlig statistikk | 2026 | Generaliseringsanalyse: innbyggertall per dekningsområde | Offentlig |

Hovedanalysen er kvantitativ og registerbasert. De kvalitative kildene (prosedyredokumenter og valideringssamtaler) har en støttende funksjon: de brukes til å forankre modellantakelser i operativ virkelighet, ikke som selvstendig empirisk grunnlag for hovedfunnene.

### 5.2.1 LEO/BRIS-data (primærdata)

Primærdatasettet er hendelsesdata fra 110 Sør-Vest eksportert fra LEO/BRIS-systemet. Uttrekket dekker hele kalenderåret 2025 (01.01.2025 til 31.12.2025) og inneholder 61 964 registrerte oppdrag (synlige BRIS-rader) med 44 variabler per oppdrag. Faktisk antall innkommende anrop er høyere. Tilleggsanrop til samme hendelse sammenstilles med eksisterende oppdrag og forsvinner som egne observasjoner. Sekvensgapmetoden estimerer 18 901 sammenstilte anrop i tillegg (avsnitt 5.3.4). Datasettet er eksportert som CSV med UTF-8-encoding (med BOM).

Fra høsten 2024 benytter alle tolv norske 110-sentraler det felles oppdragshåndteringssystemet LEO. Valget av 2025 som analyseår sikrer at hele perioden er dekket av det nye systemet. Det gir bedre datakonsistens enn eldre perioder, der systemovergangen kan ha påvirket registreringspraksis.

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

**Tabell 5.3: Datakvalitet og strukturelle begrensninger**

| Felt | Dekningsgrad | Konsekvens for analysen |
|---|---|---|
| `Operatør-ID` | 0 % (100 % null) | Serverutnyttelse kan ikke observeres direkte på operatørnivå. Systemstrukturell begrensning bekreftet av DSB (mars 2026) |
| `Innsatsvarighet` | 76,4 % av kategori D (5 771 av 7 555) | Måler total varighet fra utrykning til siste ressurs ledig, og kan vare i timer. **[Metodeforbehold 5.1]** Variabelen er ikke benyttet som operatørbindingsmål fordi 110-operatørens binding antas avgrenset til akuttfasen (RØD + GUL), ikke hele innsatsperioden. Antagelsen er forankret i prosedyre og operative samtaler (avsnitt 5.2.4), men ikke direkte målt på operatørnivå (jf. manglende Operatør-ID over) |
| `Alarmbehandlingstid` | 99,0 % av kategori D (7 478 av 7 555) | Tilgjengelig for nesten alle utrykningshendelser |
| Første ressurs fremme | 76,5 % av kategori D (5 777 av 7 555) | Primært mål for bindingstid. Resterende 23,5 % er imputert med median |

Denne kildens viktigste begrensning er at den viser synlige oppdrag, ikke alle innkommende anrop. Tilleggsanrop som sammenstilles med eksisterende oppdrag forsvinner som egne observasjoner (se avsnitt 5.3.4).

### 5.2.2 DSB MOB-rapporter

Bemannings- og oppdragsdata for alle tolv norske 110-sentraler er hentet fra DSBs årlige rapportering gjennom MOB-systemet (Melding Om Brannvesen). Data foreligger for perioden 2022 til 2025. De inkluderer antall ansatte, rapportert bemanning per vakttype (dag/natt, hverdag/helg), antall operatørplasser og selvrapportert anropsvolum. Kilden brukes til deskriptiv benchmarking av casefunn mot nasjonal bemanningsstruktur. Den brukes ikke til å konkludere normativt om andre sentraler er riktig bemannet.

Kildens viktigste begrensning er at MOB viser rapportert plan-/minimumsnivå per vakttype, ikke faktisk observert bemanning på enkeltvakter. Svar fra enkelte sentraler viser også at MOB-tallet kan representere ulike lokale begreper: normalbemanning, minimumsbemanning eller bemanning inkludert vaktleder. For 110 Sør-Vest fastsettes $c_{\text{eff}}$ derfor fra lokale prosedyre- og beredskapsdokumenter. MOB-bemanning for øvrige sentraler brukes som en offentlig rapportert proxy i nasjonal oversikt. Der lokale avklaringer mangler, tolkes bemanningstallene med forbehold.

### 5.2.3 Prosedyre- og analysedokumenter

Tre interne dokumenter fra 110 Sør-Vest er sentrale for modellkonstruksjonen:

1. **Prosedyre for arbeidsmetodikk, utalarmering og loggføring** (Rogaland brann og redning IKS, 2024, versjon 4). Definerer rollestrukturen (RØD/GUL/GRØNN), makkerpar-prinsippet, VL-rollen og operativ arbeidsmetodikk.

2. **Beredskapsanalyse 110 Vest** (2022). Dokumenterer overløpsmekanismer, herunder 30-sekundersregelen for automatisk overføring til Agder og 10-anrops-køterskel.

3. **Risiko- og sårbarhetsanalyse (ROS) Bergen brannvesen** (2023). Dokumenterer det kvalitative grunnlaget for bemanningsdimensjonering.

Dokumentene er tilgjengelige gjennom forfatterens operative tilknytning til 110 Sør-Vest. Denne kilden brukes primært til å etablere modellparametere (c_eff, kapasitetsnivåer, overløpsregler). Denne kildens viktigste begrensning er at den beskriver prosedyrer og planer, ikke nødvendigvis faktisk etterlevelse i alle situasjoner.

### 5.2.4 Operative valideringssamtaler og LABA-dybdeanalyse

Modellforutsetninger og parameterestimater er validert gjennom tre komplementære kanaler: samtaler med operativt personell ved 110 Sør-Vest, en strukturert manuell dybdeanalyse av L-aba-hendelser, og en begrenset ekstern avklaringsrunde med andre sentraler. Den eksterne runden brukes til plausibilitetskontroll og forklaring av store dataavvik, ikke som nødvendig datagrunnlag for hovedanalysen.

**Tabell 5.4: Gjennomførte valideringsaktiviteter**

| Dato | Aktør | Format | Primærtema |
|---|---|---|---|
| 15.03.2026 | Midt-Norge 110 | Telefon (uformell) | Bemanning, servicetesting-organisering |
| Mars til april 2026 | 110 Sør-Vest | Løpende operativ dialog | Makkerpar, bindingstider, VL-rolle, overløp, D-pri1/D-aba-dynamikk |
| 18.04.2026 | Lokal operatør 110 Sør-Vest | Strukturert utfylling (Excel) | LABA-dybdeanalyse: 50 hendelser med tidsstempler fra LEO |
| 22.04.2026 | Lokal operatør 110 Sør-Vest | Utvidet strukturert utfylling (Excel) | LABA-dybdeanalyse runde 2: 100 Kilde=Alarm-hendelser |
| April 2026 | Lokale operatører 110 Sør-Vest | Intern kalibrering av spørreskjemautkast | Verifisering av tider og spørsmålsformuleringer før utsending |
| 23.04.2026 til 06.05.2026 | Fire andre 110-sentraler | E-post, PDF og telefonintervju | Begrenset ekstern plausibilitetskontroll: bemanning, VL-praksis, ABA/service og registreringsavvik |

Kanalene har avgrensede funksjoner: kalibrering av parametere og validering av operativ realisme i modellantakelsene. Konkret har samtalene og dybdeanalysen bidratt med:

Valideringssamtalene er dokumentert på dato, rolle/funksjon og tema, uten navn eller personidentifiserende detaljer, og brukes kun som grunnlag for parameterkalibrering og operativ plausibilitetskontroll.

- **Samtaletid for Erlang-C:** Vektet gjennomsnittlig samtaletid på 3,44 minutter (brukes kun i Erlang-C-grunnlinjen, ikke i primærmodellen)
- **VL-forutsetningen:** Bekreftelse av at vaktleder normalt ikke besvarer nødanrop direkte
- **Makkerpar-dynamikk for D-pri1 vs D-aba:** Operatørintervju bekreftet at ABA-utrykning ikke følger makkerpar-prosedyre. Én operatør utfører kvittering, oppdragsopprettelse og call-out serielt i cirka 3 min. Dette er grunnlaget for å skille D-pri1 og D-aba som egne kategorier med ulik op-binder-profil (avsnitt 6.4.4 til 6.4.5)
- **D-aba Fase 2-parametre ($p$, $Y$):** Operatørestimerte verdier for andel D-aba med påfølgende nødtelefon og bindingstid for denne fasen; empirisk underkant-verifisert via sekvensgap-metoden
- **Bindingstid for L-aba:** Kvantitativt kalibrert via LABA-dybdeanalysen (se avsnitt 5.4)
- **Bindingstid for sammenstilte anrop:** Kvalitativt estimat på 1 minutt
- **Organisatoriske forskjeller:** Midt-Norge har dedikert servicepersonell utenfor LEO, noe som påvirker sammenlignbarheten av servicevolum mellom sentraler

**Avklaringer med andre sentraler** ble forsøkt innhentet for å forstå registreringspraksis og store avvik i DSB/MOB-tallene. Per 06.05.2026 foreligger dokumenterte svar fra Innlandet, Finnmark, Midt-Norge og Vest 110. Svarene viser at slike avklaringer er nyttige for å forklare avvik, for eksempel bålmeldinger som L-ukjent, direkte ABA-utalarmering og dedikert servicepersonell. Avklaringene er likevel ikke en forutsetning for hovedanalysens troverdighet. Hovedanalysen bygger på registerdata og lokal prosedyrevalidering ved 110 Sør-Vest. For de øvrige sentralene brukes LEO/BRIS- og MOB-tall som sekundærdata med eksplisitte forbehold. Manglende svar begrenser bare hvor sikkert lokale avvik kan forklares.

### 5.2.5 SSB befolkningsdata

Innbyggertall per sentrals dekningsområde er hentet fra SSB Statistikkbanken med referansedato 1. januar 2026. Denne kilden brukes primært til generaliseringsanalyse som strukturell prediktor for bemanningsbehov.

### 5.2.6 Datarensing og klargjøring

Følgende steg er gjennomført for å klargjøre primærdatasettet for analyse:

1. **Filtrering:** Datasettet er filtrert til 110 Sør-Vest og analyseperioden 01.01.2025 til 31.12.2025.
2. **Parsing av tidsvariabler:** `Dato anrop` er konvertert fra strengformat (`%d.%m.%Y`) til datetime-objekter. `Time på døgnet` er brukt til å konstruere fullstendige tidsstempler.
3. **Konstruksjon av skifttype:** Hvert anrop er klassifisert som dag (07:00 til 18:59) eller natt (19:00 til 06:59), og som hverdag (mandag til fredag) eller helg (lørdag til søndag), basert på tidsstempel. Dette gir fire skifttyper: dag/hverdag, dag/helg, natt/hverdag, natt/helg.
4. **Kontroll av sekvensnumre:** `110_ID`-feltets daglige sekvensnumre er ekstrahert og kontrollert for gap. Manglende sekvensnumre er registrert som estimerte sammenstilte anrop.
5. **Håndtering av manglende verdier:** For kategori D-hendelser uten registrert tidspunkt for første ressurs fremme (23,5 %) er median bindingstid fra observerte verdier brukt som imputeringsverdi. Øvrige manglende felt (operatør-ID, innsatsvarighet) er dokumentert som strukturelle begrensninger, ikke imputert.
6. **Håndtering av ekstreme verdier:** Bindingstider er kontrollert for negative verdier og urealistisk lange varigheter. Beregningene bygger på registrerte tidsstempler og er ikke manuelt justert.
7. **Encoding:** CSV-filen er lest med `encoding='utf-8-sig'` for å håndtere BOM-markør. Sentralnavn med encoding-avvik er normalisert via en oppslagstabell.

**Tilleggsbearbeiding for nasjonal benchmarking (kap 8.5 og 8.4.1):** Det nasjonale BRIS-datasettet for 2025 dekker alle 12 sentraler (508 228 registrerte oppdrag, proxy for henvendelser, med kjent undertelling pga. sammenstilling, jf. avsnitt 5.3.1 og 5.3.4). Datasettet er bearbeidet med samme V3-klassifiseringsregel som primærdatasettet (`Kilde = Alarm`-krav for L-aba og D-aba). Bearbeidingen er nødvendig av to grunner. Sentralnavn forekommer med ulike encoding-varianter (f.eks. `S?r-Vest 110`, `S\u00f8r-Vest 110`, `Sør-Vest 110`) I tillegg har `Opprinnelig oppdragstype` ulik dekningsgrad mellom sentraler. To konkrete grep er gjort: sentralnavn normaliseres via `SENTRALER_NORM`-oppslagstabellen i `analyse/scripts/benchmark_trend_analyse.py`. L-aba/D-aba-andelen rapporteres uten justering for ulik dekningsgrad. Variasjonen mellom sentraler (0,0 til 7,5 %) tolkes derfor eksplisitt som indikasjon på heterogen registreringspraksis (jf. kap 9.4.1), ikke som direkte sammenlignbare nivåer. Lokale svar brukes bare til å forklare avvik der de foreligger. Registertallene endres ikke uten dokumentert grunnlag. Den prosedyrbaserte ankomstkonfliktmodellen er per nå kjørt på 110 Sør-Vest alene. Nasjonal modellanvendelse forutsetter klassifiseringsharmonisering (kap 10.4).

---

## 5.3 Databehandling og operasjonalisering

Dette avsnittet beskriver hvordan rådataene er transformert til analytiske variabler. Selve modellformuleringen presenteres i kapittel 6.

### 5.3.1 Analyseenheter: anrop, oppdrag og hendelse

Analysen opererer med tre distinkte enheter som må holdes adskilt:

- **Anrop:** En faktisk innkommende telefon eller varsling til sentralen. Hvert anrop binder en operatør.
- **Oppdrag:** En registrert sak i LEO/BRIS. Flere anrop kan sammenstilles i ett oppdrag.
- **Hendelse:** Den operative situasjonen sentralen håndterer. Én hendelse kan generere flere anrop fra ulike innringere.

I primærmodellen er analyseenheten det enkelte anropet ved dets ankomsttidspunkt, fordi det er anropet, ikke oppdraget, som binder operatørkapasitet. Skillet er sentralt fordi antall synlige oppdrag i datasettet undervurderer antall faktiske anrop (se avsnitt 5.3.4).

### 5.3.2 Klassifisering av hendelser

Hendelsene i datasettet er klassifisert i åtte kategorier basert på tre BRIS-felt: `Oppdragstype` (sluttklassifisering), `Opprinnelig oppdragstype` (initiell hendelsestype) og `Kilde` (Alarm/Samtale/blank, dvs. innringingskanal):

- **D-pri1** (Pri-1-utrykning): Hendelser med ressursvarsling som ikke er ABA-utløst. Byggingsbrann, trafikkulykke, farlig gods, etc. Krever makkerpar-prosedyre.
- **D-aba** (ABA-utløst utrykning): Hendelser med ressursvarsling der `Opprinnelig = "ABA"` og `Kilde = "Alarm"`. Ikke pri-1, håndteres serielt.
- **S** (Service): Overføringstester av brannalarmanlegg
- **L-aba** (ABA løst av 110): Automatisk brannalarm avklart uten utrykning. Krever `Kilde = Alarm`
- **L-hendelse** (Reell hendelse løst av 110): Innringer melder reell situasjon, løst uten ressurs. Inkluderer ABA-oppdrag med `Kilde = Samtale` (publikumsmelding om brannalarm uten ABA-signal)
- **L-ukjent** (Løst av 110, uklassifisert): Henvendelser uten formell opprinnelig oppdragstype
- **F** (Feilringing): Feilringing, ikke-nødmelding, eCall feil
- **V** (Viderevarsling): Viderekobling til annen etat eller intern varsling

**Kilde = Alarm-kravet:** LABA-dybdeanalysen (avsnitt 5.4) viste at 24,5 % av oppdrag klassifisert med `Opprinnelig = ABA` faktisk ikke representerer automatisk brannalarm i operativ forstand. Disse inkluderer publikumsmeldinger om brannalarm, privat bygg uten 110-tilknytning, tester feilrevidert som oppdrag og duplikatoppdrag. Ved å kreve `Kilde = Alarm` for L-aba og D-aba skilles ekte ABA-signaler fra disse feilklassifiseringene. Oppdrag som tidligere ville vært L-aba, men har `Kilde = Samtale` eller blank, reklassifiseres til L-hendelse.

**D-pri1 vs D-aba-splitt:** Operatørintervju (avsnitt 5.2.4) og prosedyrereferanse (Rogaland brann og redning IKS, 2024) etablerer at pri-1-utrykning og ABA-utløst utrykning har fundamentalt ulik operativ dynamikk. Pri-1 krever makkerpar, mens ABA håndteres serielt og solo. Splittingen er nødvendig for at kapasitetsmodellen skal reflektere korrekt op-binder-profil per hendelsestype (avsnitt 6.4).

Av 61 964 synlige oppdrag i 2025 klassifiseres 4 499 (7,3 %) som D-pri1 og 3 056 (4,9 %) som D-aba. Primærmodellen (variant A) avgrenses til disse beredskapskategoriene pluss sammenstilte anrop. Den utvidede modellen (variant B) inkluderer alle åtte kategorier. Bindingstider er empirisk kalibrert eller operativt estimert. Fullstendig klassifiseringslogikk og operative beskrivelser er gitt i avsnitt 6.2.

### 5.3.3 Beregning av bindingstid

Bindingstid og antall operatører bundet per hendelse er differensiert per kategori fordi ulike hendelsestyper har ulik operativ dynamikk:

**D-pri1 (databasert, makkerpar-bundet):**

> **Bindingstid = (Første ressurs fremme $-$ Dato/tid anrop) + 3 minutter kvitteringsvindu**
> **Ops bundet = 2 (makkerpar: RØD + GUL parallelt)**

Beregningen bygger på to registrerte tidsstempler: `Dato/tid anrop` og `Første ressurs fremme`. Kvitteringsvinduet på 3 minutter reflekterer at GUL-operatøren etter mottatt vindusmelding kvitterer og loggfører før kapasitet frigjøres. For de ~25 % av D-pri1-hendelsene som mangler tidspunkt for første ressurs fremme, er median bindingstid fra de observerte verdiene (14,1 minutter) brukt som imputeringsverdi.

**D-aba (operativ prosedyre + BRIS-verifisert):**

> **Fase 1 (alltid): 3 min × 1 operatør** (kvittering + oppdragsopprettelse + call-out)
> **Fase 2 (med sannsynlighet p): Y min × 1 operatør** (nødtelefon + panel-veiledning, starter 90 sek etter Fase 1)

Fase 1-varigheten er forankret i operativ prosedyre og verifisert empirisk. Median tid fra anrop til ressurs varslet er 74 sek for D-aba (P75 = 80, P90 = 111). Dette er konsistent med operativ beskrivelse av cirka 90 sek call-out. Med etterfølgende registrering estimeres Fase 1 til 3 min. Fase 2-parametrene ($p$, $Y$) varieres i tre scenarioer (lav/hoved/høy: $p = 0{,}30/0{,}50/0{,}70$; $Y = 3/6/10$ min). Hovedscenarioet $p = 0{,}50$, $Y = 6$ min er grunnlaget i primæranalysen.

**L-aba (empirisk kalibrert, LABA-dybdeanalyse n = 100 Kilde=Alarm):**

> **Bindingstid = 4,5 min × 1 operatør (hoved)**

Bindingstiden for L-aba er kalibrert via en strukturert manuell dybdeanalyse i to runder (avsnitt 5.4). Hovedparameteren bygger på utvidet utvalg (n = 100, alle Kilde=Alarm). Mean er 4,53 min med 95 % CI [3,74; 5,43] minutter. Forrige rapportversjon brukte n=30-anslaget (mean 5,88 min, CI [3,70; 8,56]). Det er erstattet i denne versjonen.

**Øvrige kategorier (operativt estimert, sensitivitetsscenarioer):**

S: 1/2/4 min; L-hendelse: 3/5/8 min; L-ukjent: 1/3/5 min; F: 0,25/0,5/1 min; V: 0,5/1/2 min. Hovedscenario benyttes i primærresultatene, mens lavt og høyt brukes i sensitivitetsanalyse (avsnitt 8.3).

**Sammenstilte tilleggsanrop:** 1 min × 1 operatør. **[Metodeforbehold 5.2]** Forenklet estimat basert på operativ vurdering, ikke en direkte observasjon. Sensitivitetsanalysen i avsnitt 8.3 viser at hovedfunnet er robust over rimelige variasjoner.

### 5.3.4 Estimering av sammenstilte anrop

Når flere innringere melder om samme hendelse, sammenstilles tilleggsanropene med det eksisterende oppdraget i LEO/BRIS. Disse forsvinner da som egne observasjoner i datasettet. Metoden for å estimere antallet er basert på sekvensnummerlogikken i `110_ID`-feltet:

- Hvert synlige oppdrag tildeles et daglig sekvensnummer (f.eks. B06-250101-4, B06-250101-6).
- Manglende sekvensnumre i rekken (i dette tilfellet -5) tolkes som anrop som ble sammenstilt med et eksisterende oppdrag.
- Tidspunkt for sammenstilte anrop er interpolert fra nærmeste synlige oppdrags ankomsttidspunkt, da det eksakte tidspunktet ikke er registrert.

Metoden forutsetter at LEO tildeler sekvensnumre kronologisk. Gap kan i prinsippet også reflektere overflyt til nabosentral eller avbrutte anrop, ikke bare sammenstilte anrop. For Sør-Vest er sekvensgapene validert operativt som overveiende sammenstillinger (jf. avsnitt 7.2). For 2025 er det estimert 18 901 sammenstilte anrop (korreksjonsfaktor 1,305x). Metoden identifiserer at et anrop mangler som synlig oppdrag, men ikke hvilket oppdrag det ble knyttet til.

**Retning og størrelsesorden på skjevheten.** Sekvensgap-metoden kan i prinsippet feilklassifisere tre typer hendelser som sammenstilte anrop, og disse drar i hver sin retning.

*Mulig overestimering:* Hvis et sekvensgap reflekterer (a) automatisk overflyt til Agder ved 10. kø-anrop, (b) automatisk overflyt etter 30 sekunder ubesvart, eller (c) avbrutt anrop som aldri ble registrert som oppdrag, har anropet ikke bundet en operatør ved 110 Sør-Vest. Modellen overestimerer da $n_{\text{aktive}}$ og dermed variant A-Svikt-andelen. *Plausibel øvre grense:* 10-anrops-overflyten forutsetter ti samtidige kø-anrop, som ved observert systemutnyttelse $\rho < 6$ % (kap 7.1) er en svært sjelden tilstand. 30-sekunders-overflyten kan inntreffe i Svikt-tilstander der alle operatører er bundet. Siden modellen klassifiserer 32,6 % av natt/helg-anropene som Svikt (variant A), gir dette en realistisk øvre andel av sekvensgap som *kunne* være 30-sek-overflyt. Den faktiske andelen er sannsynligvis lavere fordi VL ofte tar anropet før 30-sekunders-grensen utløses (jf. avsnitt 4.2.1).

*Mulig underestimering:* Hvis beredskapsrelaterte anrop blir feilkategorisert som «service», «feilringing» eller «løst av 110» og lukket som egne oppdrag (slik LABA-dybdeanalysen indikerer for L-aba, avsnitt 5.4.4 og kap 7.2), er det reelle antallet skjulte beredskapsanrop høyere enn 18 901. Modellen underestimerer da samlet operativ binding.

*Netto vurdering for 110 Sør-Vest:* Operativ validering av sekvensgapene mot kjent driftspraksis (kap 7.2) støtter at de overveiende reflekterer sammenstilte anrop, ikke overflyt. De to skjevhetene drar i hver sin retning, og nettoeffekten er vurdert som liten på variant A-Svikt-andelen, dvs. innenfor scenariobåndet i Tabell 8.5 (28 til 39 % under variant B). Skjevheten er likevel ikke nøyaktig kvantifisert. For sentraler med vesentlig høyere skjult-rate (Finnmark 65 %, Agder 54 %) bør sekvensgap-tolkningen valideres lokalt før modellen anvendes nasjonalt. For disse er skjevhetspotensialet større.

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

## 5.4 LABA-dybdeanalyse: empirisk kalibrering av L-aba-bindingstid

For å kalibrere bindingstidsestimatet for L-aba er det gjennomført en strukturert dybdeanalyse i to runder ved 110 Sør-Vest 2025. Første runde omfattet 50 trukne hendelser (49 gyldige) og ga en innledende kalibrering med betydelig restusikkerhet. Andre runde utvidet utvalget til **100 hendelser (alle med gyldige tidsstempler, alle Kilde=Alarm)**, og er grunnlaget for den endelige modellparameteren. **Den standardiserte LABA-omtalen i rapporten er derfor: 100 trukne / 100 gyldige / Kilde=Alarm-subset (hovedparameter, n = 100).** Den første runden (n=49 totalt / n=30 Kilde=Alarm-subset, mean 5,88 min med CI [3,70; 8,56]) er metodisk dokumentert i `analyse/notat_V3_modellutvikling.md`.

Analysen har to formål: (1) empirisk måling av faktisk operatørbindingstid for automatiske brannalarmer løst uten utrykning, og (2) vurdering av klassifiseringsnøyaktigheten i BRIS L-aba-kategorien.

### 5.4.1 Utvalgsdesign

Populasjonen består av 3 430 L-aba-hendelser for 110 Sør-Vest 2025 (etter V3-klassifisering med Kilde=Alarm-krav). Utvalget for runde 2 er stratifisert på måned for å sikre jevn dekning over året:

- 8 hendelser per måned × 8 måneder + 9 hendelser per måned × 4 måneder = 100 hendelser
- Tilfeldig utvalg innen hver måned med fast seed (`SEED = 20260418`) for reproduserbarhet
- Utvalgsandel: 2,9 %

### 5.4.2 Gjennomføring

For hver hendelse i utvalget åpnet en operatør ved 110 Sør-Vest LEO-loggen og registrerte fire tidsstempler:

- `T_alarm_inn`: når ABA-signalet ble mottatt i LEO
- `T_nødtelefon_inn`: når eventuell nødtelefon fra stedet ble besvart
- `T_avklart`: når operatør bekreftet ufarlig årsak
- `T_operatør_frigjort`: når oppdraget ble lukket

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

Mean fra runde 2 er **utenfor** 95 % CI fra runde 1 (5,88 lå innenfor [3,70; 8,56], men 4,53 ligger nærmere CI-nedre). Standardavvik (4,37 min) reflekterer at fordelingen forblir høyreskjev, drevet av langhalede tilfeller (industrivern-oppfølging, varmekamera-avklaring), men terskelen for «høy bindingstid» er lavere enn antatt i runde 1.

### 5.4.4 Klassifiseringsobservasjoner

Operatørens kommentarer (begge runder) avdekket at en betydelig andel L-aba-oppdrag ikke representerer automatisk brannalarm i operativ forstand. I runde 1 (n=49) var dette 12 av 49 (24,5 %), fordelt på følgende kategorier:

| Kategori | N (av 49) |
|---|---:|
| «Privat brannalarm uten tilknytting til 110» (ikke ISM-kunde) | 4 |
| «Kun nødanrop, ikke alarm i ISM» (publikumsmelding, ikke ABA-signal) | 3 |
| «Test av anlegg / øvelse feilrevidert» (burde vært kategori S) | 3 |
| «Innbruddsalarm ikke innlagt i ISM» (feilkategorisert) | 1 |
| «Ikke i henhold til prosedyre» | 1 |

Disse hendelsene har det til felles at `Kilde = Samtale` eller blank, mens ekte ABA-signal har `Kilde = Alarm`. Observasjonen motiverte V3-klassifiseringsregelen som krever `Kilde = Alarm` for L-aba og D-aba (avsnitt 5.3.2 og 6.2). Runde 2 (n=100, alle Kilde=Alarm) bekrefter at klassifiseringsregelen virker som tilsiktet, ved at alle 100 trukne hendelser er ekte ABA-signaler i operativ forstand.

### 5.4.5 Valgte parametre og sensitivitet

Basert på n=100-resultatet velges mean **4,53 min ≈ 4,5 min** som hovedverdi. Median ville undervurdere eksponeringen fordi fordelingen er høyreskjev. Sensitivitetsscenarioer i variant B er justert tilsvarende: lav (3 min, CI-nedre), hoved (4,5 min, empirisk mean), høy (7 min, over CI-øvre). Tidligere scenarioer (3/6/9 min basert på n=30) er erstattet.

### 5.4.6 Begrensninger

- **Utvalgsstørrelse:** n = 100 gir 95 % CI ±0,85 min for mean, substansielt strammere enn n=30-runden (±2,4 min). Restusikkerheten er lav nok til at parameteren kan brukes som empirisk kalibrert hovedverdi, ikke kun orienteringsanslag.
- **Enkelt-operatør-perspektiv:** Utfyllingen er gjort av én operatør. Flere operatører ville kunne vurdere klassifiseringstvil ulikt, men siden runde 2 kun trekker fra Kilde=Alarm-subsettet er rommet for klassifiseringstvil betydelig redusert.
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
| 8 | Ekspansjon av hver hendelse til op-binder-events med (bindingstid, ops_bundet) | Steg 2-7 | Beregnet |
| 9 | Sweep-algoritme: beregn $n_{\text{aktive}}$ ved hvert ankomsttidspunkt | Steg 8 | Beregnet |
| 10 | Klassifisering av kapasitetsnivå (Normal / Brudd / Svikt) per beredskapsanrop | Steg 9 + c_eff | Beregnet |
| 11 | Beregning av Erlang-C (M/M/c) som referansemodell | BRIS/LEO + samtaler | Beregnet |
| 12 | Scenarioanalyse: +1 operatør per skifttype | Steg 9-10 med endret c_eff | Modellbasert |
| 13 | Benchmarking mot alle 12 sentraler via DSB MOB-data og DSB 2025-fullrapport | DSB MOB + DSB 2025 + SSB | Direkte |

Steg 1 til 8 representerer databehandling og operasjonalisering. Steg 9 til 10 er primæranalysen. Steg 11 til 13 er supplerende analyser. Steg som er markert som «direkte» bygger på observerte registerdata, mens «estimert», «imputert», «empirisk» og «modellbasert» innebærer metodiske valg som må tas med i tolkningen av resultatene.

---

## 5.6 Validitet, reliabilitet og begrensninger

### 5.6.1 Validitet

Analysens sentrale metrikk er kapasitetsnivå ved ankomst. Den bygger på to ulike datakilder. D-pri1-hendelser identifiseres robust gjennom ressursvarsling. L-aba-bindingstider er empirisk kalibrert via LABA-dybdeanalyse (avsnitt 5.4). Validitetstruslene struktureres etter konstrukt-, intern- og ekstern validitet.

**Trussel 1 [konstruktvaliditet]: målet er en prosedyrkonformitetsmetrikk, ikke et tjenestekvalitetsmål.** Modellen måler andel beredskapsanrop der makkerpar-kravet ikke kan opprettholdes ved ankomst. Det er ikke det samme som andel anrop der tjenesten leveres med redusert kvalitet, eller andel der innringer opplever forsinkelse. Konstruktvaliditeten begrenses derfor til det modellen eksplisitt måler. Diskusjonen i kap 9.2 og 8.2.3 problematiserer dette skillet eksplisitt.

**Trussel 2 [intern validitet]: målefeil i bindingstider.** Ikke alle bindingstider er empirisk målt:

- D-pri1 og L-aba bygger på direkte observasjon (databasert respektive LABA-dybdeanalyse).
- D-aba Fase 1 er forankret i operativ prosedyre og empirisk verifisert (median 74 sek call-out).
- D-aba Fase 2 og øvrige kategorier (S, L-hendelse, L-ukjent, F, V) er operative estimater validert av vaktleder, ikke direkte observert.

Sensitivitetsanalysen (avsnitt 8.3) viser at hovedfunnet er robust over hele spennet av rimelige antakelser. Det er likevel mulig at parametrene systematisk underestimerer bindingstid for noen kategorier (særlig under press), noe som ville gjøre Svikt-andelen høyere enn rapportert.

**Trussel 3 [intern validitet]: indirekte estimerte tilleggsanrop.** Sammenstilte anrop estimeres via sekvensgapmetoden (avsnitt 5.3.4). Antallet er estimert. Tidspunkt og varighet er ikke observert direkte. Hovedscenario $p = 0{,}50$ for D-aba Fase 2 reflekterer operatørens kvalitative vurdering, ikke direkte måling. Sekvensgap-metoden gir underkant-estimat (17 til 37 % avhengig av tidsvindu) fordi nødtelefoner logget inni hovedoppdraget er usynlige. Imputering med median for de cirka 19 % av D-pri1-hendelsene uten registrert fremme-tidspunkt kan systematisk feilrepresentere enkelte hendelser, men er nå statistisk validert via bootstrap (avsnitt 8.3.4): bidraget til total usikkerhet i Svikt-andelen er ±0,5 pp.

**Trussel 4 [intern validitet]: bekreftelseskontroll på modellrammeverket.** Modellrammen er utviklet av forfatteren basert på operativ prosedyreforståelse. En alternativ analytiker uten samme operative tilknytning kunne formulert kapasitetsmetrikken annerledes (jf. tre konkrete eksempler i 5.6.2). Konsekvensen er ikke at hovedfunnet er feil, men at den isolerte Svikt-prosenten ikke kan tolkes uavhengig av valgte definisjoner. Sensitivitetsanalysen (avsnitt 8.3) tester parameterrobusthet, ikke definisjonsrobusthet, og sistnevnte er drøftet kvalitativt i kap 9.2.3.

**Trussel 5 [ekstern validitet]: overførbarhet til andre sentraler.** LABA-dybdeanalysen er empirisk grunnlag for L-aba-parameteren, men gjelder kun 110 Sør-Vest 2025. 95 % CI [3,74; 5,43] for mean er strammere enn runde 1 (n = 30), men kan ikke uten videre overføres til andre sentraler. Nasjonal benchmarking i kap 8.5 viser dessuten store sentralforskjeller i L-aba-rate (0 til 7,5 %), trolig drevet av ulik registreringspraksis. Modellrammeverket er prinsipielt overførbart, men parameterverdiene må kalibreres lokalt.

Samlet trekker truslene i ulike retninger. Trussel 2 og 3 trekker i hovedsak mot konservativt estimat (undervurdering av faktisk belastning). Trussel 1, 4 og 5 er definisjons- og kontekstavhengige, og begrenser hva tallene *betyr* og hvor de gjelder, ikke nødvendigvis hvor store de er.

### 5.6.2 Reliabilitet og reproduserbarhet

Analysen bygger primært på registerdata fra et nasjonalt system (LEO/BRIS). Det gir høy sporbarhet og konsistens. Sekvensgapmetoden for sammenstilte anrop og D-aba Fase 2-stokastikken er systematiske og bruker fast random seed (`SEED_DABA = 20260419`) for reproduserbarhet. Alle analysesteg er implementert i skriptbasert arbeidsflyt (se avsnitt 5.8). Det muliggjør konsistent reproduksjon.

Variant A er i hovedsak deterministisk, ved at usikkerheten ligger i parameterantagelser, ikke i stokastisk simulering. Random seed er kun relevant for D-aba Fase 2-stokastikken i variant B, der hver D-aba-hendelse trekker uniformt mot Fase 2-sannsynligheten $p$. Identisk seed gir identisk realisasjon. En annen seed kan gi en marginalt ulik Svikt-andel, typisk innenfor ±0,3 prosentpoeng for natt/helg, jf. observert differanse mellom primærmodellens 32,6 % og scenarioets baseline 32,8 % (avsnitt 8.2).

Valideringssamtalene er vanskeligere å reprodusere eksakt. De brukes kun til å kalibrere parametere som er eksplisitt dokumentert (Tabell 5.5). En annen forsker med tilgang til samme data, prosedyredokumenter og `notat_V3_modellutvikling.md` vil kunne gjenta analysen med de dokumenterte parameterverdiene.

**Insider-perspektivets påvirkning på reliabilitet: kontrollmekanismer.** Refleksivitetsavsnittet i 5.1 lister fire kontrollmekanismer, og 5.6.1 listet tre validitetstrusler. Reliabilitet, i betydningen «om en annen analytiker ville få samme resultat», er kontrollert gjennom fem grep:

1. **Objektive registerdata som primærgrunnlag** (jf. 5.1, grep 1). Hovedfunnene springer ut av tidsstempler og kategoriklassifisering i LEO/BRIS, uavhengig av forfatterens tolkning.
2. **Deterministisk skriptbasert analyseflyt** (jf. 5.1, grep 2). Identisk seed og parametere gir identisk resultat; alle skript er versjonskontrollert.
3. **Triangulering mellom kilder** (jf. 5.1, grep 4). Operatørbaserte parametere kontrolleres mot prosedyredokumentasjon og BRIS-tidsstempler. Eksempel: D-aba Fase 1 er prosedyreforankret (cirka 90 sek call-out) og empirisk verifisert (median 74 sek). LABA-tider er kontrollert mot interpolert call-handling-tid i BRIS.
4. **Eksplisitt antagelsesdokumentasjon** (jf. 5.1, grep 3). Alle valgte parametere er listet i Tabell 5.5, 5.6 og Tabell 6.3 med kilde- og kalibreringsstatus. Andre forskere kan reprodusere analysen med dokumenterte parameterverdier eller systematisk variere dem.
5. **Sensitivitetsanalyse over rimelige parameterspenn** (avsnitt 8.3, Tabell 8.5). Robusthet testes på tvers av tre scenarioer; resultatet er at hovedfunnet ikke avhenger av spesifikk parametersetting.
6. **Statistisk usikkerhetskvantifisering via bootstrap** (avsnitt 8.3.4, Tabell 8.6). Variant A er reberegnet med 1 000 bootstrap-iterasjoner der D-pri1-bindingstider trekkes med erstatning fra de observerte verdiene, slik at både sampling-variabilitet i den empiriske fordelingen og imputeringsusikkerhet for de 19 % manglende verdiene propageres til Svikt-andelen. Resultatet er en 95 % CI på [32,1; 33,2] % for Svikt natt/helg; punktestimat 32,8 % ligger sentralt i CI-en. MAR-antagelsen er ikke strengt oppfylt, men avviket trekker estimatet i konservativ retning, jf. drøfting i 7.7.4.

Det disse grepene **ikke** kontrollerer er valg av modellramme. Operasjonaliseringen av makkerpar som kapasitetsmetrikk reflekterer forfatterens forståelse av prosedyren. En utenforstående forsker uten operativ tilknytning kunne formulert metrikken annerledes. Tre konkrete eksempler på alternative valg: (i) å definere bindingstid som «første ressurs fremme» uten +3 min kvitteringsvindu, (ii) å klassifisere D-aba som makkerpar-bundet i Fase 2 fremfor seriell solo-håndtering, (iii) å bruke `Innsatsvarighet` som operatørbindingsmål fremfor akuttfase-proxy. Hvert alternativ ville gitt et annet Svikt-tall.

Innenfor rammen av nåværende prosjekt er det ikke gjennomført uavhengig replikasjon eller blind tolkning fra en utenforstående analytiker; dette ville krevd egen forskningsetisk vurdering og er foreslått som videre forskning (kap 10.4). Den residuelle insider-bias-risikoen er dermed eksplisitt erkjent som en grense for hvor uavhengig replikasjon kan være, ikke som et eliminert problem.

### 5.6.3 Avgrensninger

- **Én hovedcase.** Primæranalysen er begrenset til 110 Sør-Vest. Overførbarhet til andre sentraler er plausibel, men ikke empirisk testet.
- **Analyseår 2025.** Datagrunnlaget dekker ett kalenderår. Sesongvariasjoner fanges, men årlige svingninger og langtidstrender er ikke adressert.
- **Begrenset dekning av ikke-D-kategorier i variant A.** Øvrige kategorier inkluderes i variant B; hovedfunnet for variant A er en avgrenset beredskapsmetrikk, ikke total operatørbelastning.
- **Operatør-ID er strukturelt fraværende.** Individuell serverbelastning kan ikke observeres direkte. Denne begrensningen gjelder for alle norske 110-sentraler.
- **MOB-bemanning er rapportert nivå, ikke faktisk vaktdata.** MOB-dataene viser bemanning rapportert per vakttype, men ikke faktisk observert bemanning på enkeltvakter. Lokale svar viser at tallet kan tolkes ulikt mellom sentraler, særlig om det representerer normalbemanning, minimumsbemanning og/eller inkluderer vaktleder.
- **Manglende sentralavklaringer.** Det foreligger ikke svar fra alle øvrige 110-sentraler. Dette svekker ikke hovedanalysen av 110 Sør-Vest, men begrenser hvor presist avvik i nasjonal benchmarking kan forklares. Derfor trekkes det ikke normative konklusjoner om bemanningsriktighet for andre enkelt-sentraler.
- **Poisson-forutsetning ikke formelt testet.** Erlang-C-grunnlinjen forutsetter Poisson-ankomster; dette er ikke empirisk validert. Primærmodellen er imidlertid ikke avhengig av denne antagelsen.

---

## 5.7 Etiske vurderinger og rolleforståelse

Prosjektet benytter anonymiserte registerdata der ingen personopplysninger er tilgjengelige, og operatør-ID er strukturelt fraværende i BRIS-eksporter. Valideringssamtaler er gjennomført som operative fagsamtaler, ikke som formelle forskningsintervjuer, og inneholder ikke personidentifiserbar informasjon. Studien er ikke vurdert å kreve godkjenning fra Sikt (tidligere NSD), da den ikke behandler personopplysninger. Rådata og interne prosedyre- og beredskapsdokumenter publiseres ikke; rapporten presenterer kun aggregerte resultater, metodiske beskrivelser og kildehenvisninger på et nivå som ivaretar intern konfidensialitet.

Forfatterens operative tilknytning til 110 Sør-Vest er gjort eksplisitt og adressert metodisk gjennom refleksivitetsavsnittet i 5.1 og kontrollmekanismene i 5.6.2. Generative KI-verktøy (Claude Code av Anthropic og ChatGPT av OpenAI) er benyttet som støtteverktøy for koding, litteratursøk og rapportskriving. All bruk er dokumentert med dato, kontekst og hva som ble produsert (se Vedlegg D / `KI_erklæring_LOG650_G20_Rune.md`). Alle analytiske beslutninger, tolkninger og konklusjoner er forfatterens egne. Den deterministiske, skriptbaserte analyseflyten beskrevet over sikrer at KI-verktøyenes rolle er begrenset til kode- og tekststøtte, ikke til generering av modellresultater eller tolkninger.

---

Samlet gir datagrunnlaget et godt grunnlag for å modellere den best observerbare og mest beredskapsdimensjonerende delen av operatørbindingen. Enkelte belastningselementer må estimeres eller empirisk kalibreres. På dette grunnlaget utvikles i neste kapittel modellrammeverket for kapasitetsanalysen.

---

*Kap 5, Versjon 3.4 | Sist oppdatert: 2026-05-15 (bootstrap-CI som 6. reliabilitets-grep i 5.6.2; trussel 3 oppdatert med bootstrap-validering og korrigert til 19 % missingness)*