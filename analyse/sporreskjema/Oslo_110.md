# Sporreskjema -- Oslo 110
## Studie: Kapasitetsanalyse av norske 110-sentraler (LOG650, Hogskolen i Molde, 2026)

**Student:** Rune Grodem, G20 Individuell
**Formaal:** Masteroppgaven analyserer om faktisk bemanning ved norske 110-sentraler samsvarer med kapasitetsbehovet beregnet fra historiske hendelsesdata og koeteoretiske modeller.

> Svarene behandles konfidensielt og brukes kun i aggregert form i rapporten, med mindre Oslo 110 eksplisitt samtykker til navngiving.

---

## Del 1 -- Innrapporterte data fra DSB (2022-2025)

Tabellen er basert paa data dere selv har rapportert til DSB via MOB-systemet. Vi ber dere bekrefte, korrigere eller utdype disse tallene.

### 1.1 Bemanning (innrapportert)

| | 2022 | 2023 | 2024 | 2025 | Endring 22-25 |
|---|---|---|---|---|---|
| Ansatte heltid | 35 | 39 | 41 | 37 | +5.7% |
| Operatorer dag - hverdag | 5 | 5 | 5 | 5 | |
| Operatorer natt - hverdag | 4 | 4 | 4 | 4 | |
| Operatorer dag - helg | 4 | 4 | 4 | 4 | |
| Operatorer natt - helg | 4 | 4 | 4 | 4 | |

### 1.2 Oppdrag med utrykning (sammenlignbare tall 2022-2024)

> **Datakvalitetsmerknad:** Fra 2024 tok flere sentraler i bruk nytt operativsystem (LEO/OHV),
> og i 2025 registreres alle innkommende telefonsamtaler som egne hendelsesrader.
> Totalt oppdragsvolum er derfor IKKE sammenlignbart paa tvers av alle aar.
> Tabellen nedenfor viser kun oppdrag MED utrykning (Brann + Ulykke), som er
> konsistent registrert i alle aar uavhengig av system.

| | 2022 | 2023 | 2024 | 2025* | Endring 22-24 |
|---|---|---|---|---|---|
| Oppdrag - Brann | 2240 | 2249 | 1974 | 2067 | |
| Oppdrag - Ulykke | 1613 | 1669 | 1623 | 1531 | |
| **Sum med utrykning** | **3853** | **3918** | **3597** | **3598** | **-6.6%** |
| Unodige/falske utrykninger | 13135 | 13468 | 13621 | 11537 | |

*2025-tall er inkludert for orientering, men bor ikke brukes i trendsammenligning.

### 1.3 Mottatte 110-anrop (selvrapportert i MOB)

> Disse tallene er sentralenes egne innrapporteringer til DSB og er uavhengig av
> registreringssystemet. De kan brukes som supplerende indikator paa anropsvolum.

| | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Mottatte 110-anrop (MOB) | 25800 | 30735 | 29000 | 30000 |

---

## Del 2 -- Utdyping og korrigering

**Spm 1.** Er tallene i tabellene ovenfor korrekte? Hvis nei -- hva er riktige tall, og hva forklarer avviket?

> *Svar:*

**Spm 2.** Tabellen viser operatorantall som registrert minimum per vakttype. Er dette faktisk laveste planlagte bemanning, eller er det et normaltall? Hva er reelt operativt minimum ved lav bemanning (f.eks. sykdom, ferie)?

| Vakttype | Innrapportert | Faktisk minimum | Merknad |
|---|---|---|---|
| Dag - hverdag | 5 | | |
| Natt - hverdag | 4 | | |
| Dag - helg | 4 | | |
| Natt - helg/helligdag | 4 | | |

**Spm 3.** Besvarer vaktleder (VL) normalt innkommende nodanrop ved Oslo 110?

[ ] Ja, alltid   [ ] Ja, ved behov/hoy belastning   [ ] Nei, aldri   [ ] Ingen dedikert VL-rolle

**Spm 4.** Oppdrag med utrykning (Brann+Ulykke) endret seg med **-6.6%** fra 2022 til 2024, mens ansatte heltid endret seg med **+5.7%** fra 2022 til 2025. Kan dere si noe om hva som forklarer denne utviklingen?

> *Svar:*

**Spm 5.** Har det skjedd spesielle hendelser (storulykker, klimahendelser, nye oppgaver, organisasjonsendringer) som har hatt vesentlig pavirkning paa kapasitetssituasjonen i perioden 2022-2025?

> *Svar:*

---

## Del 3 -- Handleringstider per hendelsestype

Studien bruker en koeteoretisk modell (Erlang-C) for aa beregne kapasitetsbehov. Modellen krever
gjennomsnittlig operatorbindingstid per hendelsestype -- den tiden en operator aktivt er bundet
til aa handtere en hendelse (ikke total hendelsesvarighet, som kan vaere mye lengre).

| Type | Beskrivelse | Typiske eksempler | Estimert bindingstid (min) |
|---|---|---|---|
| T1 | Ren telefonhenvendelse -- ingen utrykking, ingen oppdragslogg | Test av anlegg, generelle henvendelser, feilmeldinger | |
| T2 | Automatisk brannalarm (ABA) -- begrenset handleringstid uavhengig av utfall | ABA kvittert som falsk alarm ELLER bekreftet og viderekoblet | |
| T3 | Hendelse med utrykning -- lang operatorbinding, potensielt flere operatorer | Brann i bygg, trafikkulykke med skadde, hjertestans med ressursutalarmering | |
| T4 | Melding vurdert og lukket uten utrykning -- lengre enn T1 men kortere enn T3 | Mulig brann avkreftet via intervju, oppdrag lost av 110 | |

**Spm 6.** Stemmer denne inndelingen med operativ praksis ved Oslo 110? Er det typer som mangler, overlapper eller bor slas sammen?

> *Svar:*

**Spm 7.** For T3-hendelser: Hva er typisk tidsrom fra anrop mottas til operator er ferdig med aktiv handtering (selv om oppdraget fortsatt er apent i systemet)? Er det vanlig at en T3-hendelse binder mer enn en operator samtidig?

> *Svar:*

---

## Del 4 -- ROS- og beredskapsanalyse

**Innrapportert status (fra MOB):**
- ROS-analyse sist revidert: **2023**
- Beredskapsanalyse utarbeidet: **Ja**, sist revidert: **2023**

**Spm 8.** Bekrefter dere disse arstallene? Hvis nei -- hva er korrekte tall?

> *Svar:*

**Spm 9.** Naar er neste planlagte revisjon av ROS-/beredskapsanalysen?

> *Svar:*

**Spm 10.** Hvilke metoder/modeller bruker dere for aa dimensjonere bemanningsnivaa? Er det basert paa beredskapsanalysen, historiske data, avtaler, eller annet?

> *Svar:*

**Spm 11.** Mener dere at ROS- og beredskapsanalyser i sin navaerende form er tilstrekkelig som grunnlag for aa dimensjonere antall operatorer? Hva er eventuelt de viktigste manglene?

> *Svar:*

---

## Del 5 -- Sammenfallende hendelser

**Spm 12.** Opplever dere perioder der antall samtidige aktive hendelser overstiger operatorkapasiteten? Hvor hyppig skjer dette, og i hvilke situasjoner?

> *Svar:*

**Spm 13.** Hva skjer operativt naar kapasitetsgrensen naas?

[ ] Vaktleder trer inn som operator   [ ] Overfort til nabosentral   [ ] Prioritering mellom hendelser   [ ] Annet: ___

**Spm 14.** Er det et definert antall samtidige hendelser/anrop som utloster tiltak eller varsling (f.eks. bistand fra nabosentral)?

> *Svar:*

---

## Del 6 -- Avsluttende kommentarer

**Spm 15.** Er det andre forhold ved kapasitetssituasjonen ved Oslo 110 som dere mener er viktig aa forsta, og som ikke dekkes av sporsmalene ovenfor?

> *Svar:*

---

*Takk for at dere tar dere tid til aa svare. Svarene kan returneres til [e-post] innen [frist].*
*Sporsmal kan rettes til Rune Grodem, student LOG650, Hogskolen i Molde.*