# PROSJEKTBESKRIVELSE (PROPOSAL)
**LOG650 – Forskningsprosjekt: Logistikk og kunstig intelligens**
Vår 2026

________________________________________________________________________________

**Gruppemedlemmer:**
Rune Grødem, G20 – Rune Individuell.

**Område:**
Kapasitetsstyring og bemanningsdimensjonering (Service Operations Management)

**Bedrift:**
Norske 110-sentraler (primærcase: 110 Sør-Vest)

---

## Problemstilling

I hvilken grad samsvarer faktisk bemanning ved norske 110-sentraler med kapasitetsbehovet beregnet fra historiske hendelsesdata og køteoretiske modeller?

Norske 110-sentraler mottar nødmeldinger og koordinerer brann- og redningsinnsats døgnet rundt. Minimumsbemanning er lovfestet til to operatører i vaktrommet, men dimensjonering utover dette fastsettes lokalt basert på risiko- og beredskapsanalyser. Det finnes ingen nasjonal, kvantitativ standard for hvordan operativ belastning skal oversettes til konkret bemanningsnivå.

Operativ belastning ved en 110-sentral kjennetegnes av stokastisk ankomst av hendelser med ulik håndteringstid og ressursbehov. En foreløpig typologi basert på etablert arbeidsmetodikk skiller mellom fire hendelseskategorier:

- **T1 — Ren telefonhenvendelse:** Oppdrag lukket uten initiell hendelsestype; kort håndteringstid for én operatør
- **T2 — Automatisk brannalarm (ABA):** Begrenset håndteringstid, normalt én operatør
- **T3 — Hendelse med utrykking:** Lengre håndteringstid med potensielt krav om flere simultane operatører
- **T4 — Hendelse vurdert og avsluttet uten utrykking:** Initiell hendelsestype lukket etter intervju og vurdering, uten ressursutsendelse

Typologien vil valideres mot data og justeres om nødvendig. En sentral modellantagelse er at vakthavende leder (VL) normalt ikke besvarer nødanrop, noe som innebærer at effektiv operatørkapasitet er `c_effektiv = c_total − 1`. Denne forutsetningen inngår eksplisitt i dimensjoneringsmodellen.

Prosjektet vil videre undersøke i hvilken grad kapasiteten påvirkes av det *aktive hendelsesbildet* — situasjoner der pågående hendelser i driftsfase binder operatørkapasitet og reduserer evnen til å håndtere nye anrop. Fenomenet *ring-flom* (call surge), der én hendelse utløser et stort antall samtidige anrop fra publikum, vil belyses som en operativ ekstrembelastning.

---

## Data

Prosjektet kombinerer tre typer empirisk grunnlag, noe som gir et særlig bredt fundament for analysen:

- **Operasjonelle data — hendelsesdata fra LEO/BRIS (primært 2025):** Fra 2025 benyttet alle norske 110-sentraler et felles oppdragshåndteringssystem (LEO), noe som muliggjør sammenlignbare hendelsesdata på tvers av sentraler. Eksport med tidsstempler og oppdragstype gir grunnlag for å analysere belastningsmønstre, ankomstrater og hendelsestypefordeling. Tilgjengelighet og detaljnivå kartlegges tidlig og avgjør hvilke analyser som er gjennomførbare.

- **Organisatoriske data — årsrapporter fra norske 110-sentraler (2025):** DSBs strukturerte årsrapporter inneholder bemanning per vakttype, antall operatørplasser og totalt anropsvolum for alle sentraler. Disse dataene er allerede innhentet og danner grunnlag for benchmarking.

- **Normative data — strukturerte intervjuer med operativt personell:** Håndteringstid per hendelseskategori og operative kapasitetsgrenser estimeres og valideres gjennom intervjuer med personell ved et utvalg norske 110-sentraler. Intervjuene dekker tidsbruk per hendelsestype, krav til antall operatører ved ulike situasjoner og erfaringer med kapasitetsutfordringer. Forfatterens egne operative erfaringer fra 110 Sør-Vest dokumenteres eksplisitt.

- **Befolkningsdata (SSB):** Innbyggertall per sentrals dekningsområde benyttes til å undersøke sammenhengen mellom befolkningsgrunnlag, hendelsesvolum og bemanningsbehov.

---

## Metode og modell

Prosjektet plasseres innenfor **kvantitativ kapasitetsanalyse** og benytter metoder fra **køteori og operasjonsanalyse**. Prosjektet vil anvende fler-server kømodeller, med **Erlang-C (M/M/c)** som utgangspunkt. Endelig modellvalg begrunnes etter eksplorativ datagjennomgang, og eventuelle utvidelser eller alternativer vurderes dersom dataene tilsier det.

Sentrale modellforutsetninger — herunder Poisson-fordelte ankomster, eksponentielle håndteringstider og hendelsesmessig uavhengighet — vil vurderes empirisk, og eventuelle avvik vil diskuteres eksplisitt.

Prosjektet gjennomføres i følgende steg:

1. **Eksplorativ dataanalyse:** Kartlegge belastningsmønstre, ankomstrater og hendelsestypefordeling. Valg av operativ enhet for modellering avgjøres etter datagjennomgang.
2. **Parameterestimering:** Estimere ankomstrate (λ) og gjennomsnittlig håndteringstid (μ) per tidsperiode, basert på kombinasjon av hendelsesdata og intervjuer.
3. **Modellering:** Beregne anbefalt bemanningsnivå per tidsperiode for definert servicegrad. Korreksjon for VL-rollen og eventuelle særtrekk ved T3-hendelser inngår i modellspesifikasjonen.
4. **Benchmarking:** Sammenligne modellanbefaling mot faktisk registrert bemanning på tvers av sentraler, og undersøke om enkeltstasjoner fremstår som systematisk over- eller underdimensjonerte. Analysere om befolkningsgrunnlag og hendelsesvolum kan forklare variasjonen i bemanningsnivå mellom sentraler.
5. **Generalisering (betinget av data):** Dersom datagrunnlaget tillater det, undersøkes om strukturelle prediktorer kan benyttes til å generalisere dimensjoneringsanbefalingen til sentraler uten detaljerte hendelsesdata.

---

## Målfunksjon

Prosjektet måler resultater langs to dimensjoner:

1. **Kapasitetsmessig samsvar:** I hvilken grad er faktisk bemanning tilstrekkelig til å håndtere observert belastning med akseptabel servicegrad?
2. **Generaliserbarhet:** Kan en dimensjoneringsmodell utvikles som er meningsfull på tvers av sentraler med ulik størrelse og belastning?

---

## Suksesskriterium

Prosjektet anses vellykket dersom det:

- Gjennomfører en empirisk belastningsanalyse basert på historiske hendelsesdata fra norske 110-sentraler
- Anvender og begrunner en køteoretisk modell for beregning av dimensjoneringsanbefaling
- Sammenligner modellanbefaling mot faktisk bemanning og diskuterer avvik
- Dokumenterer operative særtrekk som skiller 110-sentraler fra standard kømodell-forutsetninger, og vurderer modellens gyldighet i lys av dette

Omfanget av generaliseringsanalysen og benchmarkingen tilpasses tilgjengelige data.

---

## Avgrensninger

- Analysen avgrenses til **vaktromsbemanning** — ikke ressursdisponering i brannvesenet, taktisk hendelseshåndtering eller organisatoriske beslutninger
- Prosjektet er **retrospektivt og planleggingsrettet**, ikke et sanntidssystem
- **2025-data prioriteres** grunnet felles oppdragshåndteringssystem på tvers av sentraler, noe som sikrer sammenlignbarhet
- **Ekstraordinære hendelser** (langvarige storbranner, katastrofescenarier) holdes utenfor modellens primære gyldighetsområde og behandles i diskusjonskapittelet
- Endelig valg av modell, analyseenheter og analysedybde fastsettes etter eksplorativ datagjennomgang og begrunnes i rapporten

________________________________________________________________________________

*Dato: mars 2026*
