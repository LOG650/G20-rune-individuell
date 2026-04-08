# V3-implementering — oppstartsbrief for ny Claude-sesjon

**Dato:** 2026-04-08
**Status:** Klar til oppstart
**Prosjekt:** LOG650 G20 Rune Grødem — Kapasitetsanalyse 110-sentraler

---

## Til ny Claude-sesjon: Hva du trenger å vite

Dette dokumentet er en **selvstendig oppstartsbrief** for å implementere V3 (kvantifisering av total operativ belastning) i prosjektet LOG650. Brukeren har allerede bygget en omfattende kapasitetsanalyse for 110 Sør-Vest, og V3 er en utvidelse som ble identifisert i forrige sesjon.

**Les først:** Repoets `CLAUDE.md` for prosjektregler, deretter `014 fase 4 - report/vurderinger_todo.md` (V1, V2, V3) for full kontekst på utvidelsesforslaget.

---

## 1. Prosjektkontekst (kort)

### Problemstilling
> *I hvilken grad samsvarer faktisk bemanning ved norske 110-sentraler med kapasitetsbehovet beregnet fra historiske hendelsesdata og køteoretiske modeller?*

### Case
**110 Sør-Vest** — én av tolv norske nødmeldesentraler for brann/redning. Dekker Rogaland og deler av Vestland/Agder, ca. 555 000 innbyggere.

### Bemanning
- **Dag/hverdag:** 4 operatører + vaktleder (VL). c_eff = 3 (VL besvarer normalt ikke nødanrop)
- **Natt/helg:** 3 operatører + VL. c_eff = 2

### Primærmodell (allerede ferdig)
**Prosedyrbasert ankomstkonfliktmodell** — for hvert beredskapsanrop klassifiseres kapasitetsnivå basert på antall aktive hendelser ved ankomsttidspunktet:
- **Normal:** ledige ≥ 2 (makkerpar mulig)
- **Brudd på driftsstandard:** ledige = 1 (solo-håndtering)
- **Svikt:** ledige ≤ 0 (VL/Agder må overta)

Modellen er agnostisk om hva belastningen er — den teller kun "(start, varighet)" per belastningsenhet.

---

## 2. Hva er gjort og hva gjenstår

### Ferdige rapportkapitler
| Kapittel | Fil | Versjon | Status |
|---|---|---|---|
| 2 Litteratur | `kap2_litteratur.md` | v1.0 | Ferdig |
| 4 Casebeskrivelse | `kap4_casebeskrivelse.md` | v1.1 | Ferdig |
| 5 Metode og data | `kap5_metode_data.md` | v2.0 | Ferdig |
| 6 Modell | `kap6_modell.md` | v2.0 | Ferdig |
| 7 Analyse og resultater | `kap7_analyse_resultater.md` | v1.0 | Ferdig |

### Gjenstående
- Kap 1 Innledning (skall i `Rapport_LOG650_G20_Rune_110_v0.1.md`)
- Kap 3 Teori (skall)
- Kap 8 Diskusjon (skall)
- Kap 9 Konklusjon (skall)
- Sammendrag + abstract

### Viktige frister
- **27. april 2026:** Peer review starter
- **31. mai 2026:** Endelig rapport
- **Juni 2026:** Muntlig eksamen

---

## 3. V3 — kvantifisering av total operativ belastning

### Motivasjon
Eksisterende primærmodell måler kun **kategori D (utrykningshendelser)** = 7 555 av 61 964 hendelser. De resterende 54 409 (kategori A/B/C — service, henvendelser uten utrykning, ABA) bidrar til reell operativ belastning, men er ikke kvantifisert.

Dette skaper et metodisk problem: prosjektet skal nettopp **erstatte kvalitative ROS-vurderinger med kvantitativ modell**. Hvis bakgrunnsbelastningen kun behandles kvalitativt, faller vi tilbake i akkurat den fellen vi forsøker å unngå.

### Hva V3 gjør
Bruker **samme prosedyrbaserte ankomstkonfliktmodell** på hele anropsvolumet (alle 61 964 hendelser), ikke bare kategori D. Resultatet presenteres **parallelt** med eksisterende beredskapsmodell:

| Modellvariant | Belastningsenheter | Spørsmål den besvarer |
|---|---|---|
| **A (eksisterende, primær)** | Kategori D + sammenstilte anrop (26 456) | Kan vi opprettholde driftsstandard for nødanrop? |
| **B (V3, ny)** | Alle kategorier (≥61 964) | Hvor opptatt er operatørene faktisk gjennom skiftet? |

### Bindingstidsestimater (operativt utgangspunkt — må valideres)
| Kategori | Beskrivelse | Bindingstid |
|---|---|---|
| A1 | ABA-test (anlegg i service-modus) | 2–5 min |
| A2 | Generell henvendelse / feilringing | 30 sek – 1 min |
| A3 | Administrativ henvendelse | 1–3 min |
| B | Reell hendelse uten utrykning | 5–10 min |
| C | Tidskritisk avklaring (ABA reell) | 3–8 min |
| D | Utrykningshendelse | Median 13 min (databasert) |

**MERK:** Disse må valideres med brukeren (operativ erfaring) før kjøring.

---

## 4. Implementeringsplan med sjekkpunkter

Brukeren har eksplisitt sagt at vi skal kunne **forkaste V3 hvis det går galt**. Derfor: 5 sjekkpunkter med go/no-go mellom hvert.

| Sjekkpunkt | Innhold | Tid | Beslutning |
|---|---|---|---|
| **C1** | Klassifisere alle 61 964 hendelser i A/B/C/D. Verifisere fordeling. | ~1 t | Go hvis fordeling ser fornuftig ut og bruker gjenkjenner volumforhold |
| **C2** | Definere bindingstidsestimater per kategori. Diskutere med bruker. | ~30 min | Go når bruker har validert mot operativ erfaring |
| **C3** | Kjøre utvidet modell. Generere kapasitetsnivå-fordeling. | ~1 t | Go hvis resultatene gir fornuftige tall |
| **C4** | Sammenligne med eksisterende beredskapsmodell. Lage figur. | ~1 t | Go hvis funnene styrker, ikke fortrenger, kjernebudskapet |
| **C5** | Skrive nytt avsnitt 7.x og oppdatere kap 6.4. | ~2 t | Ferdig — eller forkast hvis kap 7 blir uleselig |

**Viktig regel:** Vis brukeren resultatet ved hvert sjekkpunkt før du går videre.

**Forkastings-strategi:** Eksisterende kode endres ikke. Lag et nytt skript `analyse/scripts/konflikt_total_belastning.py` som kan slettes uten konsekvens. Eksisterende `konflikt_v4_korrigert.py` står urørt.

---

## 5. Sentrale filer

### Eksisterende analyse
| Fil | Beskrivelse |
|---|---|
| `analyse/scripts/konflikt_v4_korrigert.py` | Primærmodell — IKKE endre, kun referanse |
| `analyse/scripts/bindingstid_analyse.py` | Bindingstidsberegning fra BRIS |
| `analyse/scripts/benchmark_trend_analyse.py` | Benchmarking 12 sentraler |
| `analyse/scripts/scenario_pluss1.py` | Scenarioanalyse +1 operatør |

### Datakilder
| Fil | Innhold |
|---|---|
| `004 data/20260315_174350_fullrapport.csv` | BRIS 2025, alle sentraler. **NB:** UTF-8 med BOM (`encoding='utf-8-sig'`), separator auto-deteksjon, `skiprows=2`. **Filteres til 110 Sør-Vest** |
| `004 data/20260315_174537_MOB_2022_110-sentral.xlsx` | DSB MOB 2022 |
| `004 data/20260315_174530_MOB_2023_110-sentral.xlsx` | DSB MOB 2023 |
| `004 data/20260315_174523_MOB_2024_110-sentral.xlsx` | DSB MOB 2024 |
| `004 data/20260315_174514_MOB_2025_110-sentral.xlsx` | DSB MOB 2025 |

### BRIS-datastruktur (kjent)
- **110 Sør-Vest 2025:** 61 964 hendelsesrader, 44 kolonner
- **Av disse:** 7 555 (12,2 %) er kategori D (utrykningshendelser)
- **Nøkkelkolonner:** `Dato anrop` (`%d.%m.%Y`), `Time på døgnet`, `110-sentral`, `Oppdrag ID`, `Kilde` (Alarm/Samtale), `110_ID` (sekvensnummerformat: `B06-250101-4`)
- **Operatør-ID:** 0 % dekning (strukturell begrensning)
- **Innsatsvarighet:** 76,4 % dekning av kat. D — IKKE bruk som binding (måler hele oppdrag, ikke akuttfase)
- **Første ressurs fremme:** 76,5 % av kat. D — primært bindingstidsmål

### Rapportfiler
| Fil | Beskrivelse |
|---|---|
| `014 fase 4 - report/Rapport_LOG650_G20_Rune_110_v0.1.md` | Rapportskjelett |
| `014 fase 4 - report/kap6_modell.md` | Modell v2.0 (les avsnitt 6.4 om primærmodellen) |
| `014 fase 4 - report/kap7_analyse_resultater.md` | Analyse v1.0 (les avsnitt 7.5 om kapasitetsanalysen) |
| `014 fase 4 - report/vurderinger_todo.md` | **LES DENNE FØRST** — V1, V2, V3 fullt dokumentert |
| `014 fase 4 - report/V3_oppstart_brief.md` | **DENNE FILEN** |

---

## 6. Konkret oppstartsoppgave

Når brukeren ber deg starte V3, gjør følgende i rekkefølge:

1. **Les `vurderinger_todo.md`** — full kontekst på V1 (sammenstilte anrop dobbeltbinding), V2 (kategori A bakgrunnsstress), og V3 (denne oppgaven)
2. **Les `analyse/scripts/konflikt_v4_korrigert.py`** — forstå eksisterende sweep-algoritme
3. **Kjør utforskning av BRIS-data:** Hvilke initielle hendelsestyper finnes? Hvor mange per type? Hvordan kan vi best klassifisere A/B/C/D?
4. **Foreslå klassifiseringslogikk** for brukerens godkjenning (C1)
5. **Vent på bruker-OK** før du går videre til C2

---

## 7. Risiko og nedfallsplan

### Hovedrisiko
At den utvidede modellen blir så dominerende at den fortrenger kjernebudskapet om makkerpar/beredskap. Variant A skal forbli primærmodell.

### Nedfallsplan
1. Eksisterende kode og dokumenter er IKKE endret
2. Nye filer ligger separat:
   - `analyse/scripts/konflikt_total_belastning.py` (nytt skript)
   - Eventuelle nye figurer i `analyse/figurer/` med prefiks `total_`
3. Kan slettes med ett `git rm` hvis vi forkaster

### Hvis du møter problemer
- Stopp og spør brukeren før du fortsetter
- Aldri implementer "litt til" uten godkjenning
- Vis output ved hvert sjekkpunkt

---

## 8. Aktive vurderinger som påvirker V3

Fra `vurderinger_todo.md`:

**V1 (sammenstilte anrop dobbeltbinding):** Hvert sammenstilt anrop binder en operatør utover foreldreoppdraget. Hvis foreldre er kategori B/C, mangler modellen 1 operator-binding. Anbefaling: Dokumentere som ekstra konservatisme i kap 6.4.8.

**V2 (kategori A bakgrunnsstress):** Bakgrunnsbelastning fra A-volum bygger over 12-timersskift. 110 Sør-Vest håndterer mer enn andre sentraler (Midt-Norge har dedikert servicepersonell). Avhenger delvis av V3 (kvantifisering).

**V3 (denne):** Kvantifisere total belastning som komplement til beredskapsmodell.

---

## 9. Litteraturstøtte for V3

Tre nye kilder lastet ned i `003 references/` (verifisert mot PDF-er 2026-04-08):

| Nr | Kilde | Hvorfor relevant for V3 |
|---|---|---|
| **35** | Harchol-Balter (2022) — multiserver job queueing | Matematisk formalisering av jobber som krever flere servere parallelt |
| **47** | Jouini, Dallery & Nait-Abdallah (2008) — team-based organizations | Eneste tidligere studie som modellerer team-basert kapasitet i call center |
| **48** | Kim, Lee, Dudin & Klimenok (2008) — cooperation of servers | Kø-modeller med samarbeidende servere |
| **37** | APCO/CSSR (2019) — Call Handling and Incident Processing | Empirisk støtte for at bemanning + duplikatanrop forsinker (N=772 PSAP) |

Disse kan refereres når kap 6 og 7 utvides for V3.

---

## 10. Tekniske retningslinjer (fra CLAUDE.md)

- **Encoding:** Alltid `encoding='utf-8'` i Python. BRIS CSV: `encoding='utf-8-sig'` (BOM)
- **Python-stack:** pandas, numpy, scipy, matplotlib, seaborn, openpyxl
- **Figurer:** Lagres i `analyse/figurer/` med beskrivende navn
- **Inline matematikk:** `$...$`, ikke `\(...\)`
- **Kapittelskille (KRITISK):** Hold metode (kap 5), modell (kap 6), resultater (kap 7) og diskusjon (kap 8) tydelig adskilt
- **Antagelser:** Skriv eksplisitt som antagelser med konsekvenser, aldri som verifiserte fakta
- **Commit:** Commit hyppig med meningsfulle meldinger. Bruk `Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>`

---

## 11. Forrige sesjons nøkkelinnsikter

1. **Erlang-C er degradert til grunnlinje** — primærmodellen er prosedyrbasert ankomstkonfliktmodell
2. **Sekvensgapmetode** identifiserer 18 901 sammenstilte anrop (korreksjonsfaktor 1,305x)
3. **Bindingstid for kategori D er median 13 min** (anrop til første ressurs fremme + 3 min kvittering)
4. **Modellen viser 23,5 % svikt på natt/helg** — kjernebudskapet
5. **Vaultens 50 kilder er verifisert mot PDF** 2026-04-08 — ingen feilsiteringer

---

*Brief opprettet: 2026-04-08 | Klar for V3-implementering*
