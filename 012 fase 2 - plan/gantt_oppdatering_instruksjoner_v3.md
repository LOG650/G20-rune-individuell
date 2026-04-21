# Instruksjoner for oppdatering av Gantt-diagram i MS Project — v3

**Fil:** `Gantt_LOG650_G20_Rune_110.mpp` (eller importer fra `.xml`)
**Lokasjon:** `012 fase 2 - plan/`
**Dato for oppdatering:** 20. april 2026
**Status XML pr. nå:** Sist lagret 2026-04-06 (StatusDate satt til 2026-04-20 ved tekstedit, men oppgavefelter ikke oppdatert)
**Erstatter:** `gantt_oppdatering_instruksjoner.md` (v1, 06.04 — utført) og `gantt_oppdatering_instruksjoner_v2.md` (18.04 — delvis utført / ikke utført i Project)

---

## Kontekst

Gantt-diagrammet ble sist lagret i MS Project 06.04.2026 etter v1-oppdateringen. v2-instruksjonen (18.04) ble aldri utført i Project. Siden 06.04 har prosjektet:

1. **Fullført alle hovedkapitler** (kap 1–9) per 19.04.2026
2. **Utviklet V3-modellen** med op-binder-semantikk og D-pri1/D-aba-splitt
3. **Lagt til nye arbeidspakker** for nasjonal generalisering, LABA-dybdeanalyse, spørreskjemaer og DSB-ønskeliste
4. **Sendt LABA n=100** til utfylling 20.04 — venter svar
5. **Peer review-frist 27.04** — gjenstår: sammendrag, vedlegg, skjelett-synk

Denne v3-instruksjonen er **selvstendig**: én sammenhengende sekvens som bringer Project-filen fra dagens state opp til 20.04.2026.

---

## Steg 1: Sett statusdato

**Prosjekt → Prosjektinformasjon → Statusdato: 20.04.2026**

(Gjøres i Project i tillegg til at XML allerede er oppdatert.)

---

## Steg 2: Oppgaver som allerede er 100 % i XML — ingen endring

Disse er korrekt registrert som fullført fra v1-oppdateringen 06.04 og senere ad hoc-arbeid (ikke rør):

| UID | Oppgave | Status XML | Faktisk |
|---|---|---|---|
| 14 | L7 — Rapportskjelett + intro v1 | 100 % | Ferdig 16.03 |
| 15 | L8 — Datainnhenting | 100 % | Ferdig 17.03 |
| 16 | L8b — ROS/beredskapsanalyse | 100 % | Ferdig 17.03 |
| 33 | L8c — EDA | 100 % | Ferdig 24.03 |
| 18 | L9 — Parameterestimering | 100 % | Ferdig 27.03 |
| 20 | L10 — Kapasitetsmodellering (Erlang-C grunnlinje + prosedyrbasert) | 100 % | Ferdig 01.04 |
| 21 | L11 — Modellvalidering | 100 % | Ferdig 06.04 |
| 34 | L11b — Sensitivitets- og scenarioanalyse | 100 % | Ferdig 09.04 |
| 24 | L13 — Benchmarking | 100 % | Ferdig 16.04 |
| 17 | M3 — Rapportskjelett klar | 100 % | 16.03 |
| 19 | M4 — Data + EDA ferdig | 100 % | 24.03 |
| 23 | M5 — Kapasitetsmodell implementert og validert | 100 % | 09.04 |

**NB:** L11b og L13 har faktisk slutt etter v1-statusdato 06.04, fordi Project ble fortløpende redigert mellom 06.04 og dagens dato uten ny .mpp-lagring/XML-eksport. Dette er greit.

---

## Steg 3: Oppdater oppgaver som har endret status siden 06.04

| UID | Oppgavenavn (nytt eller uendret) | Sett til | Faktisk start | Faktisk ferdig | Kommentar |
|---|---|---|---|---|---|
| 22 | **Endre navn til:** L12 — Teorikapittel: kø-teori, Erlang-C, QED/square-root staffing, multiserver-jobs, op-binder-semantikk | 100 % | 13.03.2026 | 19.04.2026 | Skrevet samlet med kap 3 19.04. 153 linjer |
| 25 | L14 — Generaliseringsanalyse | 90 % | 17.04.2026 | (ikke ferdig) | Omtalt i kap 7.7 og 8.3, styrket av L8d/L14b. Endelig finpuss i sluttfase |
| 26 | L15 — Resultater og diskusjon | 100 % | 24.04.2026 (faktisk start: 04.04) | 19.04.2026 | Kap 7 og 8 ferdig 19.04 v2.0/v1.1. **Korriger faktisk start til 04.04** |
| 35 | L15a — Skrive kap 1 Innledning | 100 % | 19.04.2026 | 19.04.2026 | Skrevet samlet 19.04 |
| 36 | L15b — Skrive kap 3 Teori | 100 % | 19.04.2026 | 19.04.2026 | Skrevet samlet 19.04 — overlapper L12, behold begge for sporbarhet |
| 37 | L15c — Skrive kap 8 Diskusjon | 100 % | 14.04.2026 | 19.04.2026 | Ferdig v1.1 |
| 38 | L15d — Skrive kap 9 Konklusjon | 100 % | 19.04.2026 | 19.04.2026 | Skrevet samlet 19.04 |
| 39 | L15e — Sammenstille rapportutkast (sammendrag, vedlegg, skjelett-synk, referanseliste) | 30 % | 19.04.2026 | (pågår) | Gjenstår frem til 27.04 |

**Slik gjøres det for hver oppgave:**
1. Dobbeltklikk oppgaven → dialogboksen åpnes
2. Generelt-fanen: Sett «% fullført» til verdien i tabellen
3. Generelt-fanen: Sett «Faktisk start» og «Faktisk ferdig» til datoene i tabellen
4. For navneendringer: rediger «Navn»-feltet eller klikk navnet i Gantt-tabellen
5. Klikk OK

---

## Steg 4: Legg til nye arbeidspakker (etablert siden v1/v2)

**L-nummerering — viktig:** Status.md bruker L17, L18, L19, L20 for nye fase 3-leveranser. Men i Gantt eksisterer `L17 — Ferdigstilt rapport` (UID 30, fase 4) og `L18 — Muntlig eksamen` (UID 32, fase 4) fra opprinnelig WBS. **For å unngå nummerkonflikt i Gantt brukes alternative L-koder under fase 3, med kryssreferanse til status.md i Notater-feltet.**

Plasser oppgavene logisk (innrykk = OutlineLevel 3, under FASE 3-sammenfatningen UID 13):

| Nytt UID | Oppgavenavn i Gantt | Status.md-ref | Faktisk start | Faktisk ferdig | % | Forgjenger |
|---|---|---|---|---|---|---|
| 40 | L8d — Nasjonal DSB 2025-oversikt (508 228 oppdrag, alle 12 sentraler) | L8d | 15.04.2026 | 18.04.2026 | 100 % | L8c (UID 33) |
| 41 | L8e — Spørreskjemaer 110-sentraler (intern kalibrering) | L17 | 10.04.2026 | (pågår) | 70 % | L8 (UID 15) |
| 42 | L8f — DSB-ønskeliste BRIS-datauttrekk (22 datapunkter) | L18 | 17.04.2026 | 18.04.2026 | 100 % | L8 (UID 15) |
| 43 | L11c — V3-regelutvidelse: L-aba krever Kilde=Alarm | L19 | 18.04.2026 | 19.04.2026 | 100 % | L11 (UID 21) |
| 44 | L11d — V3 op-binder-semantikk + D-pri1/D-aba-splitt (2 ops vs serial) | L20 | 18.04.2026 | 19.04.2026 | 100 % | L11c (UID 43) |
| 45 | L13b — LABA Sør-Vest dybdeanalyse n=50 (utfylt) | L13b | 17.04.2026 | 19.04.2026 | 100 % | L13 (UID 24) |
| 46 | L13c — LABA Sør-Vest dybdeanalyse n=100 (sendt 20.04, venter) | L13c | 20.04.2026 | (pågår) | 30 % | L13b (UID 45) |
| 47 | L14b — Nasjonal 2025-analyse per sentral | L14b | 16.04.2026 | 18.04.2026 | 100 % | L14 (UID 25) |

**Slik legges nye oppgaver til:**
1. Klikk på raden der oppgaven skal settes inn (f.eks. under L8c for L8d)
2. Meny: Sett inn → Ny oppgave (eller Insert-tasten)
3. Skriv navn i tabellen
4. Sett innrykk til OutlineLevel 3 (samme som øvrige L-oppgaver under FASE 3)
5. Dobbeltklikk → Generelt → fyll inn Faktisk start, Faktisk ferdig, % fullført
6. Forgjenger-fanen: legg inn UID fra tabellen
7. **Notater-feltet:** Skriv `Status.md-ref: L17` (eller tilsvarende) for sporbarhet

**Merk:** Disse oppgavene har ingen baseline (ikke i opprinnelig plan). Project vil vise «Baseline ikke satt» — det er greit; de representerer oppdatert plan basert på faktisk prosjektutvikling.

---

## Steg 5: Etterlatenskaper fra v2-instruksjonen

v2-instruksjonen (18.04) ble ikke utført i Project. Den foreslo å legge til UID 35–44 som tildels overlapper med UID 35–39 som allerede finnes i XML (L15a–L15e som kapittelskriving) og UID 40–44 som ikke finnes.

**Forhold deg til v3 (denne fila), ikke v2.** v3 forutsetter at L15a–L15e (UID 35–39) allerede eksisterer i Project og bare skal oppdateres til 100 % per Steg 3. Nye L8d/L8e/L8f/L11c/L11d/L13b/L13c/L14b legges som UID 40–47.

---

## Steg 6: Oppdater FASE 3-sammenfatningen (UID 13)

Etter Steg 2–4 bør FASE 3-sammenfatningen automatisk vise ca. **92–95 %** (alt unntatt L8e, L13c, L15e og deler av L14 fullført).

Hvis ikke automatisk: **Prosjekt → Oppdater prosjekt → «Oppdater arbeid som fullført til:» → 20.04.2026**

---

## Steg 7: Risikoregister — oppdateringer

| ID | Risiko | Status etter 20.04 | Notat |
|---|---|---|---|
| R8 | Prokrastinering mot frist | **Redusert** | Alle hovedkapitler ferdig 19.04 |
| R10 | Datadeling for peer review uavklart | Åpen | Avventer DSB-svar |
| R11 | Skjema til andre sentraler ikke sendt | Åpen | Venter på LABA n=100 før utsendelse |
| R12 | **Heterogen nasjonal L-aba-klassifisering (NY)** | Åpen | Sør-Øst og Oslo har ≈0 % L-aba — adresseres i kap 8.3 |

Hvis Gantt-filen har risikoregister som oppgaver/notater: legg til R12.

---

## Steg 8: Lagre som både .mpp og .xml

1. **Fil → Lagre** → `Gantt_LOG650_G20_Rune_110.mpp`
2. **Fil → Lagre som → XML-format (*.xml)** → `Gantt_LOG650_G20_Rune_110.xml`

Begge filene i `012 fase 2 - plan/`.

---

## Oppsummering av endringer i v3

| Type | Antall | Detalj |
|---|---|---|
| Statusdato | 1 | 06.04 → 20.04 (XML allerede oppdatert) |
| 0 % → 100 % | 6 oppgaver | L12, L15a, L15b, L15c, L15d (UID 22, 35–38) |
| 0 % → 30 % | 1 oppgave | L15e sammenstille (UID 39) |
| 50 % → 100 % | 1 oppgave | L15 (UID 26) |
| 75 % → 90 % | 1 oppgave | L14 (UID 25) |
| Navneendring | 1 oppgave | L12 (UID 22) — utvidet teori-omtale |
| **Nye oppgaver** | **8 oppgaver (UID 40–47)** | L8d, L8e, L8f, L11c, L11d, L13b, L13c, L14b |
| Risikoregister | 1 ny | R12 — heterogen L-aba-klassifisering |

---

## Mapping mellom status.md og Gantt L-koder

For å unngå L-nummerkonflikt mellom fase 3-arbeidspakker og fase 4-leveranser i Gantt:

| Status.md-kode | Gantt-kode | Innhold | Begrunnelse for mapping |
|---|---|---|---|
| L17 | **L8e** | Spørreskjemaer kalibrering | Gantt L17 = Ferdigstilt rapport (fase 4) |
| L18 | **L8f** | DSB-ønskeliste BRIS | Gantt L18 = Muntlig eksamen (fase 4) |
| L19 | **L11c** | V3-regelutvidelse Kilde=Alarm | Logisk under L11 modellvalidering |
| L20 | **L11d** | V3 op-binder + D-pri1/D-aba | Logisk under L11 modellvalidering |
| L8d | L8d | Nasjonal DSB 2025-oversikt | Ingen konflikt |
| L13b | L13b | LABA n=50 dybdeanalyse | Ingen konflikt |
| L13c | L13c | LABA n=100 dybdeanalyse | Ingen konflikt |
| L14b | L14b | Nasjonal per-sentral | Ingen konflikt |

Notater-feltet i Project bør inneholde kryssreferansen, f.eks. for L8e: `Status.md-ref: L17. Spørreskjema sendt til intern kalibrering — utsendelse til 11 andre sentraler etter LABA n=100 er tilbake.`

---

## Kvalitetssjekk etter oppdatering

- [ ] Statusdato i Project er 20.04.2026
- [ ] L12 (UID 22) står på 100 %, navn oppdatert
- [ ] L15 (UID 26) står på 100 %, faktisk start korrigert til 04.04
- [ ] L15a–L15d (UID 35–38) står på 100 %
- [ ] L15e (UID 39) står på 30 %
- [ ] L14 (UID 25) står på 90 %
- [ ] Åtte nye oppgaver (UID 40–47) er lagt til med riktig innrykk under FASE 3
- [ ] Forgjenger-lenker er satt på alle nye oppgaver
- [ ] Notater-feltet inneholder Status.md-ref for L8e/L8f/L11c/L11d
- [ ] FASE 3-sammenfatning (UID 13) viser 92–95 %
- [ ] Lagret som både .mpp og .xml

---

## For Claude Cowork eller annen AI-agent

Hvis denne instruksjonen kjøres av en AI-agent som kan åpne MS Project (Claude Cowork) eller redigere XML programmatisk:

**Foretrukket rekkefølge:**
1. Steg 1 (statusdato) — alltid først
2. Steg 3 (oppdater eksisterende) — før nye legges til
3. Steg 4 (nye oppgaver) — én og én, verifiser UID-tildeling
4. Steg 5 (skip — bare orientering)
5. Steg 6 (rollup-verifisering)
6. Steg 7 (risiko)
7. Steg 8 (lagring)

**Ved usikkerhet om UID:** søk på oppgavenavnet, ikke stol på UID alene. Gantt-strukturen kan ha drevet siden siste XML-eksport.

**Ved konflikt mellom denne instruksjonen og status.md:** status.md (`012 fase 2 - plan/status.md`) er sannhetskilden for fremdrift. Denne instruksjonen er en operasjonalisering for Project-filen.

**Hvis du må endre v3 underveis:** dokumenter avviket i `versjonshistorikk` nederst i denne fila og oppdater status.md tilsvarende.

---

## Versjonshistorikk

| Versjon | Dato | Endring |
|---|---|---|
| v1 | 06.04.2026 | Første oppdateringsinstruksjon — utført i Project samme dag |
| v2 | 18.04.2026 | Utvidet med nye arbeidspakker — IKKE utført i Project |
| v3 | 20.04.2026 | Selvstendig instruksjon basert på faktisk Gantt-state og status.md v2.3. Erstatter v1 og v2 |
