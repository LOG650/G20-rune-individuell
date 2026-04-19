# Instruksjoner for oppdatering av Gantt-diagram i MS Project — v2

**Fil:** `Gantt_LOG650_G20_Rune_110.mpp` (eller importer fra `.xml`)
**Lokasjon:** `012 fase 2 - plan/`
**Dato for oppdatering:** 18. april 2026
**Sist oppdatert i Project:** 13. mars 2026
**Erstatter:** `gantt_oppdatering_instruksjoner.md` (6. april — aldri utført)

---

## Bakgrunn

Gantt-diagrammet ble sist oppdatert 13. mars 2026 (fase 2 godkjent). Siden da er nesten hele fase 3 gjennomført, inkludert flere arbeidspakker som ikke var i den opprinnelige WBS. Den forrige instruksjonsfilen (6. april) ble aldri utført — denne v2 er **selvstendig og erstatter v1**, slik at én sammenhengende sekvens bringer Project-filen opp til dagens status (18.04.2026).

Siden 13.03 har prosjektet gjennomgått:
1. En faglig begrunnet modellendring (Erlang-C → prosedyrbasert primærmodell, Erlang-C beholdt som grunnlinje).
2. Utvidet analyse: total belastningsmodell (variant B), VL-validering av bindingstider, V3-kategorikonsistens.
3. **Nye arbeidspakker** for nasjonal generaliseringsambisjon: nasjonal DSB-oversikt (508 228 oppdrag, alle 12 sentraler), LABA-dybdeanalyse, reviderte spørreskjemaer og DSB-ønskeliste for BRIS-datauttrekk.

---

## Steg 1: Sett statusdato

**Prosjekt → Prosjektinformasjon → Statusdato: 18.04.2026**

---

## Steg 2: Fase 2 — rett 99 % → 100 %

Fase 2 ble godkjent 13. mars, men PercentComplete ble satt til 99 % i stedet for 100 %:

| UID | Oppgavenavn | Nå | Sett til | Faktisk ferdig |
|---|---|---|---|---|
| 5 | FASE 2 — Planlegging (sammenfatning) | 99 % | 100 % | 13.03.2026 |
| 10 | L5 — Godkjent prosjektstyringsplan | 99 % | 100 % | 13.03.2026 |
| 12 | M2 — Godkjent prosjektplan + Gantt | 99 % | 100 % | 13.03.2026 |

**Slik gjøres det:** Dobbeltklikk oppgaven → Generelt-fanen → % fullført → skriv 100.

---

## Steg 3: Fullførte leveranser i fase 3 — sett til 100 %

Alle disse er i dag fullført, men står på 0 % i Project:

| UID | Oppgavenavn | Sett til | Faktisk start | Faktisk ferdig |
|---|---|---|---|---|
| 14 | L7 — Rapportskjelett + introduksjon v1 | 100 % | 09.03.2026 | 09.03.2026 |
| 15 | L8 — Datainnhenting | 100 % | 13.03.2026 | 17.03.2026 |
| 16 | L8b — ROS/beredskapsanalyse-gjennomgang | 100 % | 13.03.2026 | 17.03.2026 |
| 33 | L8c — EDA | 100 % | 18.03.2026 | 25.03.2026 |
| 18 | L9 — Parameterestimering | 100 % | 25.03.2026 | 28.03.2026 |
| 20 | L10 — Kapasitetsmodellering (se Steg 6 for nytt navn) | 100 % | 30.03.2026 | 01.04.2026 |
| 21 | L11 — Modellvalidering (se Steg 6 for nytt navn) | 100 % | 02.04.2026 | 12.04.2026 |
| 34 | L11b — Sensitivitets- og scenarioanalyse (se Steg 6) | 100 % | 04.04.2026 | 13.04.2026 |
| 24 | L13 — Benchmarking | 100 % | 15.03.2026 | 02.04.2026 |

**Slik gjøres det for hver oppgave:**
1. Dobbeltklikk oppgaven → dialogboksen åpnes
2. Generelt-fanen: Sett «% fullført» til 100
3. Generelt-fanen: Sett «Faktisk start» til datoen i tabellen
4. Generelt-fanen: Sett «Faktisk ferdig» til datoen i tabellen
5. Klikk OK

**Merk:** L11 og L11b har fått senere faktisk slutt enn v1-instruksjonen tilsa, fordi total belastningsmodell (variant B) og VL-validering av bindingstider ble lagt til etter 6. april.

---

## Steg 4: Oppdater milepæler til 100 %

| UID | Milepælnavn | Sett til | Faktisk dato |
|---|---|---|---|
| 17 | M3 — Rapportskjelett + intro v1 klar | 100 % | 09.03.2026 |
| 19 | M4 — Data innhentet, validert og EDA ferdig | 100 % | 25.03.2026 |
| 23 | M5 — Kapasitetsmodell implementert og validert (se Steg 6 for nytt navn) | 100 % | 05.04.2026 |

---

## Steg 5: Kap 8 diskusjon — L15 delvis ferdig

Kap 8 (diskusjon) ble ferdigstilt 18.04.2026. Kap 7 (resultater) var ferdig 04.04.2026.

| UID | Oppgavenavn | Sett til | Kommentar |
|---|---|---|---|
| 22 | L12 — Teorikapittel | 0 % | **Ikke startet — kritisk sti mot peer review 27.04** |
| 25 | L14 — Generaliseringsanalyse | 90 % | Omtalt i kap 7.7, styrket av nye L8d/L14b |
| 26 | L15 — Resultater og diskusjon | **75 %** | Kap 7 ferdig 04.04, kap 8 ferdig 18.04. Gjenstår: revisjon etter peer review |

---

## Steg 6: Navneendringer

Endre navn på følgende oppgaver for å gjenspeile at primærmodellen er prosedyrbasert, ikke Erlang-C:

| UID | Gammelt navn | Nytt navn |
|---|---|---|
| 20 | L10 — Erlang-C modellering: bemanningsanbefaling per skiftperiode med VL-korreksjon | L10 — Kapasitetsmodellering: Erlang-C grunnlinje + prosedyrbasert ankomstkonfliktmodell |
| 21 | L11 — Modellvalidering: kontrollere at Erlang-C-resultatene gjenspeiler målt belastning... | L11 — Modellvalidering: bindingstidsanalyse fra BRIS, VL-validering, kapasitetsnivåklassifisering |
| 34 | L11b — Sensitivitetsanalyse: effekt av endringer i ankomstrate... | L11b — Sensitivitets- og scenarioanalyse: +1 operatør, dimensjoneringskurve, total belastningsmodell variant A/B |
| 23 | M5 — Erlang-C modell implementert og validert | M5 — Kapasitetsmodell implementert og validert |

**Slik gjøres det:** Klikk direkte på oppgavenavnet i Gantt-tabellen og rediger teksten. Eller dobbeltklikk → Generelt → Navn.

---

## Steg 7: Legg til NYE arbeidspakker (ikke i opprinnelig WBS)

Fem nye leveranser er etablert siden v1-instruksjonen og skal inn i fase 3 under FASE 3-sammenfatningen (UID 13). Plasser dem logisk etter eksisterende leveranser (f.eks. L8d etter L8c, L13b etter L13, osv.).

| Nytt UID | Nytt navn | Faktisk start | Faktisk ferdig | % | Forgjenger |
|---|---|---|---|---|---|
| 35 | L8d — Nasjonal DSB 2025-oversikt (alle 12 sentraler, 508 228 oppdrag) | 15.04.2026 | 18.04.2026 | 100 % | L8c (UID 33) |
| 36 | L13b — LABA Sør-Vest 2025 dybdeanalyse | 17.04.2026 | 18.04.2026 | 100 % | L13 (UID 24) |
| 37 | L14b — Nasjonal 2025-analyse per sentral | 16.04.2026 | 18.04.2026 | 100 % | L14 (UID 25) |
| 38 | L17 — Spørreskjemaer til alle 11 andre sentraler (revidert + PDF-eksport) | 10.04.2026 | — | 70 % | L8 (UID 15) |
| 39 | L18 — DSB-ønskeliste BRIS-datauttrekk (22 prioriterte datapunkter) | 17.04.2026 | 18.04.2026 | 100 % | L8 (UID 15) |

**Slik legges nye oppgaver til:**
1. Klikk på raden der den nye oppgaven skal settes inn (f.eks. under L8c)
2. Meny: Sett inn → Ny oppgave (eller trykk Insert-tasten)
3. Skriv inn navn i tabellen
4. Sett innrykk (Indent, pil-høyre-knappen) til samme nivå som øvrige L-oppgaver under Fase 3
5. Dobbeltklikk → Generelt → fyll inn Faktisk start, Faktisk ferdig, % fullført
6. For forgjengere: Fanen Forgjengere → legg inn UID fra tabellen

**Merk:** Disse oppgavene vil ikke ha baseline-verdier (finnes ikke i opprinnelig plan). Det er greit — de representerer en oppdatert plan basert på faktisk prosjektutvikling. Noter i oppgavens «Notater»-felt at oppgaven er lagt til 18.04.2026 som respons på nasjonal generaliseringsambisjon og DSB-dialog.

---

## Steg 8: Legg til gjenstående kapittelskriving som nye oppgaver

Disse var foreslått i v1-instruksjonen men ble ikke lagt inn. Plan nå justert mot peer review 27.04:

| Nytt UID | Nytt navn | Planlagt start | Planlagt ferdig | Forgjenger |
|---|---|---|---|---|
| 40 | L15a — Skrive kap 1 Innledning | 19.04.2026 | 23.04.2026 | — |
| 41 | L15b — Skrive kap 3 Teori (L12-erstatning) | 19.04.2026 | 24.04.2026 | — |
| 42 | L15c — Kap 8 Diskusjon v1.0 (FERDIG) | 14.04.2026 | 18.04.2026 | L15 (UID 26) |
| 43 | L15d — Skrive kap 9 Konklusjon | 24.04.2026 | 25.04.2026 | L15a (40), L15b (41), L15c (42) |
| 44 | L15e — Sammenstille rapportutkast (sammendrag, abstract, referanser, vedlegg) | 25.04.2026 | 27.04.2026 | L15d (43) |

**Viktig:** Sett **L15c (UID 42) til 100 % fullført** med Faktisk start 14.04.2026 og Faktisk ferdig 18.04.2026.

L15a og L15b kjøres parallelt (ingen avhengighet mellom dem), men begge må være ferdig før L15d kan starte.

---

## Steg 9: Oppdater sammenfatningsoppgaver

Etter at alle underoppgaver er oppdatert, bør FASE 3-sammenfatningen (UID 13) automatisk vise ca. 85–90 % (de fleste leveranser er fullført, kun L12/L15a/L15b/L15d/L15e gjenstår).

Dersom sammenfatningen ikke oppdateres automatisk:
- **Meny → Prosjekt → Oppdater prosjekt → velg «Oppdater arbeid som fullført til:» → 18.04.2026**

---

## Steg 10: Risikoregister — ny risiko R11

Dersom Gantt-filen har et risikoregister-område (eller hvis risiko følges som oppgaver), legg til:

| ID | Risiko | Status |
|---|---|---|
| R11 | Svar fra andre sentraler på spørreskjema — responstid usikker i 9-dagers vindu før peer review | Åpen |

---

## Steg 11: Lagre som både .mpp og .xml

1. **Fil → Lagre** (Project-format): `Gantt_LOG650_G20_Rune_110.mpp`
2. **Fil → Lagre som → XML-format (*.xml)**: `Gantt_LOG650_G20_Rune_110.xml`

Begge filene skal ligge i `012 fase 2 - plan/`.

---

## Oppsummering av endringer i v2

| Type | Antall | Detalj |
|---|---|---|
| 99 % → 100 % | 3 oppgaver | Fase 2-oppgaver som var nesten lukket |
| 0 % → 100 % | 9 oppgaver | Fullførte fase 3-leveranser |
| 0 % → 100 % | 3 milepæler | M3, M4, M5 oppnådd |
| Delvis oppdatering | 3 oppgaver | L12 (0 %), L14 (90 %), L15 (75 %) |
| Navneendring | 4 oppgaver | Erlang-C → kapasitetsmodell/prosedyrbasert |
| **Nye oppgaver — nye arbeidspakker** | **5 oppgaver (UID 35–39)** | L8d, L13b, L14b, L17, L18 |
| **Nye oppgaver — kapittelskriving** | **5 oppgaver (UID 40–44)** | L15a–L15e. L15c allerede ferdig (kap 8) |
| Ny risiko | 1 | R11 — skjemarespons |

---

## Kvalitetssjekk etter oppdatering

Før du lagrer, sjekk:

- [ ] Statusdato er 18.04.2026
- [ ] Alle 9 fullførte L-oppgaver står på 100 % med faktiske datoer
- [ ] M3, M4, M5 står på 100 %
- [ ] De 5 nye arbeidspakkene (UID 35–39) er lagt til med riktig innrykk under FASE 3
- [ ] De 5 nye kapittel-oppgavene (UID 40–44) er lagt til med avhengigheter
- [ ] L15c (kap 8) står på 100 %, ferdig 18.04.2026
- [ ] FASE 3-sammenfatning (UID 13) viser ca. 85–90 %
- [ ] Lagret som både .mpp og .xml

---

## For Claude Cowork

Claude Cowork kan åpne `Gantt_LOG650_G20_Rune_110.mpp` direkte i MS Project og følge stegene 1–11 sekvensielt. Nøkkelinformasjon som trengs fra denne filen:

- Alle eksisterende UID-er (1–34) og deres forventede navn/datoer i steg 2–6
- Nye UID-er 35–44 i steg 7–8 med faktiske datoer og avhengigheter
- Navneendringer i steg 6 (full ny tekst)
- Lagringsformater i steg 11

Ved tvil om et UID ikke finnes eller har et annet navn: søk på oppgavenavnet i Gantt-tabellen i stedet for å stole på UID alene. Strukturen i planen kan ha driftet siden .xml-eksporten 6. april.
