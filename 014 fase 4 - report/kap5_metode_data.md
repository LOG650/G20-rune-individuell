# 5. Metode og data

## 5.1 Forskningsdesign

Prosjektet er gjennomført som en kvantitativ casestudie av 110 Sør-Vest, supplert med nasjonal benchmarking for å kontekstualisere casefunnene. Forskningsdesignet er retrospektivt og planleggingsrettet: analysen baseres på historiske hendelsesdata for å vurdere om faktisk bemanning samsvarer med observert belastning.

Casestudiedesignet er valgt fordi problemstillingen er tett knyttet til en spesifikk organisatorisk og operativ kontekst, der bemanning, arbeidsmetodikk og registreringspraksis må forstås samlet for å kunne modellere kapasitetsbinding. Forfatteren har operativ tilknytning til 110 Sør-Vest, noe som gir tilgang til prosedyredokumentasjon, beredskapsanalyse og operative informanter som er nødvendige for å konstruere og validere modellparametere. Modellrammeverket er utviklet for å være overførbart til andre sentraler gitt tilsvarende datatilgang (se avsnitt 6.1 og 7.7).

Tre komplementære analysekomponenter benyttes:

**Tabell 5.1: Analysekomponenter**

| Analysekomponent | Primærvariabel | Funksjon |
|---|---|---|
| **Prosedyrbasert ankomstkonfliktmodell** (primær) — variant A: beredskap, variant B: total belastning | Antall aktive hendelser ved hvert anrops ankomsttidspunkt | Måle andel anrop der makkerpar-driftsstandarden ikke kan opprettholdes |
| Erlang-C (M/M/c) (grunnlinje) | λ, μ, c_eff | Tradisjonell køteoretisk referansemodell |
| Benchmarking (alle 12 sentraler) | Bemanning, oppdragsvolum, innbyggertall | Kontekstualisere casefunn mot nasjonal struktur |

Analyseenheten varierer mellom komponentene: i primærmodellen er analyseenheten det enkelte innkommende anropet ved dets ankomsttidspunkt. Variant A avgrenser til beredskapsoppdrag (kategori D) og sammenstilte tilleggsanrop; variant B utvider til alle syv hendelseskategorier (se avsnitt 6.2). I Erlang-C er analyseenheten aggregerte ankomstrater per skifttype, og i benchmarkingen er det den enkelte 110-sentralen.

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
| Hendelsestype | `Oppdragstype`, `Opprinnelig oppdragstype`, `Kilde` | Klassifisering i syv kategorier (D, S, L-aba, L-hendelse, L-ukjent, F, V), se avsnitt 6.2 |
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
| `Innsatsvarighet` | 76,4 % av kategori D (5 771 av 7 555) | Måler total varighet fra utrykning til siste ressurs ledig — kan vare i timer. Ikke relevant som operatørbindingsmål fordi 110-operatørens binding er avgrenset til akuttfasen, ikke hele innsatsperioden |
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

### 5.2.4 Operative valideringssamtaler

Modellforutsetninger og parameterestimater er validert gjennom samtaler med operativt personell ved 110-sentraler. Samtalene ble gjennomført i perioden mars–april 2026 med en strukturert intervjuguide (se Vedlegg B) som dekker bemanning og rollefordeling, bindingstider per hendelsestype, kapasitetsgrenser og overløpspraksis, samt dimensjoneringsgrunnlag.

**Tabell 5.4: Gjennomførte valideringssamtaler**

| Dato | Sentral | Format | Primærtema |
|---|---|---|---|
| 15.03.2026 | Midt-Norge 110 | Telefon (uformell) | Bemanning, servicetesting-organisering |
| Mars–april 2026 | 110 Sør-Vest | Løpende operativ dialog | Makkerpar, bindingstider, VL-rolle, overløp |

Samtalene er ikke et selvstendig kvalitativt delstudie, men har en avgrenset funksjon: kalibrering av parametere og validering av operativ realisme i modellantakelsene. Konkret har samtalene bidratt med:

- **Samtaletid for Erlang-C:** Vektet gjennomsnittlig samtaletid på 3,44 minutter (brukes kun i Erlang-C-grunnlinjen, ikke i primærmodellen)
- **VL-forutsetningen:** Bekreftelse av at vaktleder normalt ikke besvarer nødanrop direkte
- **Bindingstid for sammenstilte anrop:** Kvalitativt estimat på 1 minutt
- **Organisatoriske forskjeller:** Midt-Norge har dedikert servicepersonell utenfor LEO, noe som påvirker sammenlignbarheten av servicevolum mellom sentraler

I tillegg er det utarbeidet skriftlige spørreskjemaer til alle tolv sentraler med sentralspesifikke data fra MOB-rapportene for verifisering. Denne kildens viktigste begrensning er at den bygger på et begrenset antall samtaler og at operative vurderinger kan variere mellom informanter.

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

Hendelsene i datasettet er klassifisert i syv kategorier basert på to BRIS-felt: `Oppdragstype` (sluttklassifisering) og `Opprinnelig oppdragstype` (initiell hendelsestype):

- **D** (Utrykning): Hendelser med ressursvarsling — identifisert ved at `Ressurs varslet` har verdi
- **S** (Service): Overføringstester av brannalarmanlegg
- **L-aba** (ABA løst av 110): Automatisk brannalarm avklart uten utrykning
- **L-hendelse** (Reell hendelse løst av 110): Innringer melder reell situasjon, løst uten ressurs
- **L-ukjent** (Løst av 110, uklassifisert): Henvendelser uten formell opprinnelig oppdragstype
- **F** (Feilringing): Feilringing, ikke-nødmelding, eCall feil
- **V** (Viderevarsling): Viderekobling til annen etat eller intern varsling

Av 61 964 synlige hendelser er 7 555 (12,2 %) klassifisert som kategori D. Primærmodellen (variant A) avgrenses til kategori D fordi det er den eneste kategorien der tidsstempler for hele akuttfasen kan observeres i registerdataene. Den utvidede modellen (variant B) inkluderer alle syv kategorier med operative bindingstidsestimater. Fullstendig klassifiseringslogikk og operative beskrivelser er gitt i avsnitt 6.2.

### 5.3.3 Beregning av bindingstid

Bindingstid per beredskapsoppdrag (kategori D) er beregnet fra BRIS-data som:

> **Bindingstid = (Første ressurs fremme − Dato/tid anrop) + 3 minutter kvitteringsvindu**

Beregningen bygger på to registrerte tidsstempler i datasettet: `Dato/tid anrop` og `Første ressurs fremme`. Kvitteringsvinduet på 3 minutter er lagt til basert på operativ vurdering av at GUL-operatøren etter mottatt vindusmelding kvitterer og loggfører før kapasitet frigjøres.

For de 23,5 % av kategori D-hendelsene som mangler tidspunkt for første ressurs fremme, er median bindingstid fra de observerte verdiene (13,0 minutter) brukt som imputeringsverdi.

For sammenstilte tilleggsanrop er bindingstiden satt til 1 minutt. Dette er et forenklet estimat basert på operativ vurdering, ikke en direkte observasjon (se avsnitt 5.2.4).

### 5.3.4 Estimering av sammenstilte anrop

Når flere innringere melder om samme hendelse, sammenstilles tilleggsanropene med det eksisterende oppdraget i LEO/BRIS. Disse forsvinner da som egne observasjoner i datasettet. Metoden for å estimere antallet er basert på sekvensnummerlogikken i `110_ID`-feltet:

- Hvert synlige oppdrag tildeles et daglig sekvensnummer (f.eks. B06-250101-4, B06-250101-6).
- Manglende sekvensnumre i rekken (i dette tilfellet -5) tolkes som anrop som ble sammenstilt med et eksisterende oppdrag.
- Tidspunkt for sammenstilte anrop er interpolert fra nærmeste synlige oppdrags ankomsttidspunkt, da det eksakte tidspunktet ikke er registrert.

Metoden forutsetter at LEO tildeler sekvensnumre kronologisk og uten andre årsaker til gap. For 2025 er det gjennom denne metoden estimert 18 901 sammenstilte anrop (korreksjonsfaktor 1,305x). Et viktig forbehold er at metoden identifiserer at et anrop ble sammenstilt, men ikke hvilket oppdrag det ble knyttet til.

### 5.3.5 Konstruksjon av kapasitetsvariabler

Fra rådataene konstrueres følgende analytiske variabler for hvert innkommende anrop:

1. **Aktive hendelser ved ankomst** ($n_{\text{aktive}}$): Antall tidligere anrop hvis bindingstid ennå ikke er utløpt ved det aktuelle anropets ankomsttidspunkt.
2. **Ledige operatører**: $c_{\text{eff}} - n_{\text{aktive}}$, der $c_{\text{eff}}$ er effektiv operatørkapasitet for gjeldende skifttype.
3. **Kapasitetsnivå**: Klassifisert som Normal (ledige $\geq$ 2), Brudd på driftsstandard (ledige = 1) eller Svikt (ledige $\leq$ 0).

Verdien av $c_{\text{eff}}$ er satt til 3 for dag/hverdag og 2 for øvrige skifttyper, basert på minimumsbemanning minus vaktleder (se avsnitt 4.2.1). Den matematiske formuleringen er gitt i avsnitt 6.4.5.

**Tabell 5.5: Observasjonsstatus for sentrale variabler**

| Variabel | Status | Grunnlag |
|---|---|---|
| Dato/tid anrop | Direkte observert | BRIS/LEO |
| Ressurs varslet | Direkte observert | BRIS/LEO |
| Første ressurs fremme | Direkte observert (76,5 % av kat. D) | BRIS/LEO |
| Bindingstid kategori D | Beregnet fra observerte tidsstempler; 23,5 % imputert med median | BRIS/LEO + imputering |
| Sammenstilte anrop (antall) | Estimert | Sekvensgapanalyse |
| Sammenstilte anrop (tidspunkt) | Interpolert | Nærmeste synlige oppdrag |
| Bindingstid sammenstilte anrop | Forenklet antakelse (1 min) | Operativ vurdering |
| c_eff | Operativt definert parameter | Prosedyre + valideringssamtaler |

---

## 5.4 Analysegjennomføring

Analysen er gjennomført i følgende steg:

**Tabell 5.6: Analysesteg**

| Steg | Beskrivelse | Datakilde | Type |
|---|---|---|---|
| 1 | Filtrering av primærdatasettet til 110 Sør-Vest, 2025 | BRIS/LEO | Direkte |
| 2 | Identifisering av hendelser med ressursvarsling (kategori D): 7 555 hendelser | BRIS/LEO | Direkte |
| 3 | Beregning av bindingstid for observerte kategori D-hendelser (5 777 stk) | BRIS/LEO | Beregnet |
| 4 | Imputering av bindingstid for resterende kategori D (1 778 stk) med median | Steg 3 | Imputert |
| 5 | Estimering av sammenstilte anrop gjennom sekvensgap i 110_ID: 18 901 anrop | BRIS/LEO | Estimert |
| 6 | Tildeling av bindingstid (1 min) og interpolert tidspunkt til sammenstilte anrop | Operativ vurdering | Antakelse |
| 7 | Beregning av aktive hendelser ved hvert ankomsttidspunkt (sweep-algoritme) | Steg 1–6 | Beregnet |
| 8 | Klassifisering av kapasitetsnivå (Normal / Brudd / Svikt) per anrop | Steg 7 + c_eff | Beregnet |
| 9 | Beregning av Erlang-C (M/M/c) som referansemodell | BRIS/LEO + samtaler | Beregnet |
| 10 | Scenarioanalyse: +1 operatør per skifttype | Steg 7–8 med endret c_eff | Modellbasert |
| 11 | Benchmarking mot alle 12 sentraler via DSB MOB-data | DSB MOB + SSB | Direkte |

Steg 1–6 representerer databehandling og operasjonalisering. Steg 7–8 er primæranalysen. Steg 9–11 er supplerende analyser. Steg som er markert som «direkte» bygger på observerte registerdata, mens «estimert», «imputert» og «antakelse» innebærer metodiske valg som må tas med i tolkningen av resultatene.

---

## 5.5 Validitet, reliabilitet og begrensninger

### 5.5.1 Målevaliditet

Analysens sentrale metrikk — kapasitetsnivå ved ankomst — bygger på observerte tidsstempler for kategori D-hendelser, som kan identifiseres robust gjennom ressursvarsling. Følgende forhold begrenser målevaliditeten:

- **Ikke-D-kategorier har estimerte, ikke observerte bindingstider.** Kategoriene S, L-aba, L-hendelse, L-ukjent, F og V binder operatørkapasitet, men BRIS registrerer ikke håndteringstid for disse. Primærmodellen (variant A) avgrenses til kategori D; den utvidede modellen (variant B) inkluderer alle kategorier med operative bindingstidsestimater validert av vaktleder. Sensitivitetsanalysen (avsnitt 7.7) viser at hovedfunnet er robust over hele spennet av rimelige antakelser.
- **Sammenstilte anrop estimeres indirekte.** Sekvensgapmetoden gir et estimat på antall, men det eksakte tidspunktet og varigheten for hvert enkelt anrop er ikke observert.
- **Bindingstid for sammenstilte anrop er en forenklet antakelse.** Estimatet på 1 minutt er basert på operativ vurdering, ikke direkte måling. Dersom reell gjennomsnittlig bindingstid er høyere, vil analysen undervurdere effekten.
- **Imputering med median.** De 23,5 % av kategori D-hendelsene med imputert bindingstid kan avvike fra faktisk varighet, særlig for tyngre hendelser.

Begrensningene trekker i hovedsak i én retning: mot at analysen gir et konservativt estimat av faktisk kapasitetsbelastning.

### 5.5.2 Reliabilitet og reproduserbarhet

Analysen bygger primært på registerdata fra et nasjonalt system (LEO/BRIS), noe som gir høy sporbarhet og konsistens. Sekvensgapmetoden for sammenstilte anrop er systematisk og kan gjentas av andre med tilgang til samme datasett. Alle analysesteg er implementert i skriptbasert arbeidsflyt (se avsnitt 5.7), noe som muliggjør konsistent reproduksjon.

Valideringssamtalene er vanskeligere å reprodusere eksakt, men brukes kun til å kalibrere parametere som er eksplisitt dokumentert (Tabell 5.5). En annen forsker med tilgang til samme data og prosedyredokumenter vil kunne gjenta analysen med de dokumenterte parameterverdiene.

### 5.5.3 Avgrensninger

- **Én hovedcase.** Primæranalysen er begrenset til 110 Sør-Vest. Overførbarhet til andre sentraler er plausibel, men ikke empirisk testet.
- **Analyseår 2025.** Datagrunnlaget dekker ett kalenderår. Sesongvariasjoner fanges, men årlige svingninger og langtidstrender er ikke adressert.
- **Fokus på kategori D.** Andre hendelseskategorier som binder operatørkapasitet er ikke modellert som egne belastningsenheter.
- **Operatør-ID er strukturelt fraværende.** Individuell serverbelastning kan ikke observeres direkte. Denne begrensningen gjelder for alle norske 110-sentraler.
- **Benchmarkingdata er planlagt minimum.** MOB-dataene viser planlagt minimumsbemanning, ikke faktisk observert bemanning på enkeltvakter.
- **Poisson-forutsetning ikke formelt testet.** Erlang-C-grunnlinjen forutsetter Poisson-ankomster; dette er ikke empirisk validert. Primærmodellen er imidlertid ikke avhengig av denne antagelsen.

---

## 5.6 Etiske vurderinger og rolleforståelse

Prosjektet benytter anonymiserte registerdata der ingen personopplysninger er tilgjengelige — operatør-ID er strukturelt fraværende i BRIS-eksporter. Valideringssamtaler er gjennomført som operative fagsamtaler, ikke som formelle forskningsintervjuer, og inneholder ikke personidentifiserbar informasjon. Studien er ikke vurdert å kreve godkjenning fra Sikt (tidligere NSD), da den ikke behandler personopplysninger.

Forfatterens operative tilknytning til 110 Sør-Vest gir tilgang til dokumenter og operativ kontekst, men innebærer også nærhet til caset som kan påvirke tolkninger. Denne dobbeltposisjonen er håndtert gjennom:

- **Registerbasert hovedanalyse:** Hovedfunnene bygger på kvantitative data fra registersystemer, ikke subjektive vurderinger.
- **Eksplisitt dokumentasjon:** Alle modellforutsetninger og parametere er dokumentert slik at analysen er etterprøvbar (Tabell 5.5 og 5.6).
- **Tydelig skille mellom observert og antatt:** Tabell 5.5 angir eksplisitt hvilke variabler som er direkte observert, beregnet, estimert eller antatt.
- **Nasjonal benchmarking som korrektiv:** Casefunnene kontekstualiseres mot data fra alle tolv sentraler for å motvirke at lokale særtrekk overtolkes.

---

## 5.7 Implementasjon og verktøy

Alle analyser er implementert i Python med skriptbasert arbeidsflyt. Sentrale biblioteker er `pandas` og `numpy` for databehandling, `scipy` for statistiske beregninger og Erlang-C-formelen, `matplotlib` og `seaborn` for visualisering, og `openpyxl` for lesing av Excel-filer. Alle figurer og tabeller i rapporten er generert fra samme analysegrunnlag.

Kildekode og analyseskript er versjonskontrollert på GitHub. Sentrale skript:

| Skript | Funksjon |
|---|---|
| `analyse/scripts/konflikt_v4_korrigert.py` | Primærmodell med sammenstilte anrop |
| `analyse/scripts/bindingstid_analyse.py` | Bindingstidsberegning og fordeling |
| `analyse/scripts/benchmark_trend_analyse.py` | Benchmarking alle 12 sentraler |
| `analyse/scripts/scenario_pluss1.py` | Scenarioanalyse (+1 operatør) |

Generative KI-verktøy (Claude, GitHub Copilot) er benyttet som støtteverktøy for koding, litteratursøk og rapportskriving. All bruk er dokumentert med dato, kontekst og hva som ble produsert (se Vedlegg D). Alle analytiske beslutninger, tolkninger og konklusjoner er forfatterens egne.

---

Samlet gir datagrunnlaget et godt grunnlag for å modellere den best observerbare og mest beredskapsdimensjonerende delen av operatørbindingen, samtidig som enkelte belastningselementer må estimeres eller behandles som konservative antakelser. På dette grunnlaget utvikles i neste kapittel modellrammeverket for kapasitetsanalysen.

---

*Kap 5 — Versjon 2.0 | Sist oppdatert: 2026-04-05*
