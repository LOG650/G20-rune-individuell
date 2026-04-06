# Instruksjoner for oppdatering av Gantt-diagram i MS Project

**Fil:** `Gantt_LOG650_G20_Rune_110.mpp` (eller importer fra `.xml`)
**Lokasjon:** `012 fase 2 - plan/`
**Dato for oppdatering:** 6. april 2026
**Sist oppdatert i Project:** 13. mars 2026

---

## Bakgrunn

Gantt-diagrammet ble sist oppdatert 13. mars 2026 (fase 2 godkjent). Siden da er mesteparten av fase 3 gjennomført, men dette er ikke registrert i Project-filen. Diagrammet må oppdateres slik at det gjenspeiler faktisk fremdrift per 6. april 2026.

Prosjektet har gjennomgått en faglig begrunnet modellendring: Erlang-C (M/M/c) ble degradert til grunnlinje, og en prosedyrbasert ankomstkonfliktmodell ble utviklet som primærmodell. Noen oppgavenavn bør justeres for å reflektere dette.

---

## Steg 1: Oppdater statusdato

Sett prosjektets statusdato til **06.04.2026**:
- Meny: Prosjekt → Prosjektinformasjon → Statusdato: 06.04.2026

---

## Steg 2: Rett 99 % → 100 % på fase 2-oppgaver

Disse ble godkjent 13. mars, men PercentComplete ble satt til 99 i stedet for 100:

| UID | Oppgavenavn | Nå | Sett til | Faktisk ferdig |
|---|---|---|---|---|
| 5 | FASE 2 — Planlegging (sammenfatning) | 99 % | 100 % | 13.03.2026 |
| 10 | L5 — Godkjent prosjektstyringsplan | 99 % | 100 % | 13.03.2026 |
| 12 | M2 — Godkjent prosjektplan + Gantt | 99 % | 100 % | 13.03.2026 |

**Slik gjøres det:** Dobbeltklikk oppgaven → Generelt-fanen → % fullført → skriv 100.

---

## Steg 3: Oppdater fullførte leveranser i fase 3

Alle disse står på 0 % og må settes til 100 %:

| UID | Oppgavenavn | Sett til | Faktisk start | Faktisk ferdig |
|---|---|---|---|---|
| 14 | L7 — Rapportskjelett + introduksjon v1 | 100 % | 09.03.2026 | 09.03.2026 |
| 15 | L8 — Datainnhenting | 100 % | 13.03.2026 | 17.03.2026 |
| 16 | L8b — ROS/beredskapsanalyse-gjennomgang | 100 % | 13.03.2026 | 17.03.2026 |
| 33 | L8c — EDA | 100 % | 18.03.2026 | 25.03.2026 |
| 18 | L9 — Parameterestimering | 100 % | 25.03.2026 | 28.03.2026 |
| 20 | L10 — Erlang-C modellering | 100 % | 30.03.2026 | 01.04.2026 |
| 21 | L11 — Modellvalidering | 100 % | 02.04.2026 | 04.04.2026 |
| 34 | L11b — Sensitivitetsanalyse | 100 % | 04.04.2026 | 05.04.2026 |
| 24 | L13 — Benchmarking | 100 % | 15.03.2026 | 02.04.2026 |

**Slik gjøres det for hver oppgave:**
1. Dobbeltklikk oppgaven for å åpne dialogboksen
2. Generelt-fanen: Sett «% fullført» til 100
3. Generelt-fanen: Sett «Faktisk start» til datoen i tabellen over
4. Generelt-fanen: Sett «Faktisk ferdig» til datoen i tabellen over
5. Klikk OK

**Alternativ hurtigmetode:** Marker alle oppgavene i tabellen → Fanen Oppgave → Oppdater som planlagt (eller skriv 100 direkte i %-kolonnen).

---

## Steg 4: Oppdater milepæler

| UID | Milepælnavn | Sett til | Faktisk dato |
|---|---|---|---|
| 17 | M3 — Rapportskjelett + intro v1 klar | 100 % | 09.03.2026 |
| 19 | M4 — Data innhentet, validert og EDA ferdig | 100 % | 25.03.2026 |
| 23 | M5 — Erlang-C modell implementert og validert | 100 % | 05.04.2026 |

Milepæler settes til 100 % og faktisk dato fylles inn. Gjøres likt som oppgaver (dobbeltklikk → % fullført → 100).

---

## Steg 5: Oppdater delvis fullførte oppgaver

| UID | Oppgavenavn | Sett til | Kommentar |
|---|---|---|---|
| 22 | L12 — Teorikapittel | 0 % | Ikke startet — beholdes som er |
| 25 | L14 — Generaliseringsanalyse | 75 % | Omtalt i kap 7.7, men kan utvides |
| 26 | L15 — Resultater og diskusjon | 50 % | Kap 7 (resultater) ferdig, kap 8 (diskusjon) ikke startet |

---

## Steg 6: Navneendringer

Endre navn på følgende oppgaver for å gjenspeile at primærmodellen er prosedyrbasert, ikke Erlang-C:

| UID | Gammelt navn | Nytt navn |
|---|---|---|
| 20 | L10 — Erlang-C modellering: bemanningsanbefaling per skiftperiode med VL-korreksjon | L10 — Kapasitetsmodellering: Erlang-C grunnlinje + prosedyrbasert ankomstkonfliktmodell |
| 21 | L11 — Modellvalidering: kontrollere at Erlang-C-resultatene gjenspeiler målt belastning... | L11 — Modellvalidering: bindingstidsanalyse fra BRIS, kapasitetsnivåklassifisering |
| 34 | L11b — Sensitivitetsanalyse: effekt av endringer i ankomstrate... | L11b — Sensitivitets- og scenarioanalyse: +1 operatør, dimensjoneringskurve |
| 23 | M5 — Erlang-C modell implementert og validert | M5 — Kapasitetsmodell implementert og validert |

**Slik gjøres det:** Klikk direkte på oppgavenavnet i Gantt-tabellen og rediger teksten. Eller dobbeltklikk → Generelt → Navn.

---

## Steg 7 (valgfritt): Legg til nye oppgaver for gjenstående rapportarbeid

Prosjektet har identifisert at følgende kapitler gjenstår. Disse kan legges inn som nye oppgaver under Fase 3, etter L15:

| Nytt navn | Planlagt start | Planlagt ferdig | Avhenger av |
|---|---|---|---|
| L15a — Skrive kap 1 Innledning | 07.04.2026 | 11.04.2026 | — |
| L15b — Skrive kap 3 Teori | 07.04.2026 | 14.04.2026 | — |
| L15c — Skrive kap 8 Diskusjon | 14.04.2026 | 21.04.2026 | L15 |
| L15d — Skrive kap 9 Konklusjon | 21.04.2026 | 23.04.2026 | L15c |
| L15e — Sammenstille rapportutkast | 23.04.2026 | 27.04.2026 | L15a, L15b, L15d |

**Slik legges nye oppgaver til:**
1. Klikk på raden under L15 i Gantt-tabellen
2. Meny: Sett inn → Ny oppgave (eller trykk Insert-tasten)
3. Skriv inn navn, start- og sluttdato
4. Sett innrykk (indent) til samme nivå som øvrige L-oppgaver under Fase 3 (bruk pil-høyre-knappen i verktøylinjen for å rykke inn)
5. For avhengigheter: Dobbeltklikk oppgaven → Forgjengere → legg inn UID for avhengig oppgave

**Merk:** Disse nye oppgavene vil ikke ha baseline-verdier (siden de ikke fantes i den opprinnelige planen). Det er greit — de representerer en oppdatert plan basert på faktisk prosjektutvikling.

---

## Steg 8: Oppdater sammenfatningsoppgaven for fase 3

Etter at alle underoppgaver er oppdatert, bør sammenfatningen for FASE 3 (UID 13) automatisk oppdateres av Project til å vise riktig samlet %. Verifiser at den viser ca. 70–80 % (de fleste leveranser er fullført).

Dersom den ikke oppdateres automatisk: Meny → Prosjekt → Oppdater prosjekt → velg «Oppdater arbeid som fullført til:» → 06.04.2026.

---

## Steg 9: Lagre som både .mpp og .xml

1. Lagre som `Gantt_LOG650_G20_Rune_110.mpp` (Project-format)
2. Lagre som `Gantt_LOG650_G20_Rune_110.xml` (XML-eksport for versjonskontroll)
   - Fil → Lagre som → velg «XML-format (*.xml)»

Begge filene skal ligge i `012 fase 2 - plan/`.

---

## Oppsummering av endringer

| Type | Antall | Detalj |
|---|---|---|
| 99 % → 100 % | 3 oppgaver | Fase 2-oppgaver som var nesten lukket |
| 0 % → 100 % | 9 oppgaver | Fullførte fase 3-leveranser |
| 0 % → 100 % | 3 milepæler | M3, M4, M5 oppnådd |
| Delvis oppdatering | 2 oppgaver | L14 (75 %), L15 (50 %) |
| Navneendring | 4 oppgaver | Erlang-C → kapasitetsmodell/prosedyrbasert |
| Nye oppgaver (valgfritt) | 5 oppgaver | Gjenstående kapittelskriving |
