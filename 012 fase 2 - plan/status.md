# Prosjektstatus — LOG650 G20 Rune Grødem

Statusdato: 2026-04-19

Denne statusen bygger på arbeidskopien per 2026-04-19, med prosjektstyringsplanen og WBS som referanse for avvik.

## Kort status

- Prosjektet er i fase 3 – gjennomføring. Hovedanalysen er fullført, og hoved-utkast nærmer seg.
- Primærmodellen (prosedyrbasert ankomstkonfliktmodell) er implementert, validert og dokumentert.
- Erlang-C-grunnlinjen er fullført og brukes som kontrastpunkt.
- Total belastningsmodell (variant B) og VL-validering av bindingstider er lagt til kap 6–7.
- **V3-klassifiseringsregelen er skjerpet 19.04:** L-aba krever nå Kilde=Alarm. ABA-oppdrag med Kilde=Samtale eller blank flyttes til L-hendelse. L-aba-bindingstid oppdatert fra 3 → 6 min (mean fra LABA-dybdeanalyse). Skript og figurer er regenerert; kap 5/6/7 må oppdateres med nye tall.
- Kap 2 (litteratur), kap 4 (case), kap 5 (metode), kap 6 (modell), kap 7 (analyse) og **kap 8 (diskusjon)** er ferdigskrevet — men kap 5/6/7 trenger mindre oppdatering etter 19.04-klassifiseringsendringen.
- Gjenstående rapportarbeid: kap 1 (innledning), kap 3 (teori), kap 9 (konklusjon), sammendrag/abstract, revisjon av kap 5/6/7, og sammenstilling.
- **Ny arbeidspakke siden v2.0:** nasjonal DSB-oversikt (508 228 oppdrag, alle 12 sentraler), LABA Sør-Vest dybdeanalyse (50 hendelser validert av lokal operatør), intern kalibrering av spørreskjema hos lokale operatører, og DSB-ønskeliste for BRIS-datauttrekk.
- Peer review planlagt fra 27. april (8 dager igjen). Rapportfrist 31. mai 2026.
- E-post sendt til DSB (bris-support) 5. april om vurdering av datadeling for peer review.

## Faktisk fremdrift

| Leveranse | Planlagt | Faktisk status | Kommentar |
|---|---|---|---|
| L7 Rapportskjelett + intro v1 | Uke 12 | Ferdig 09.03 | Skjelett v0.1, kapittelstruktur etablert |
| L8 Datainnhenting | Uke 12 | Ferdig mars 2026 | BRIS 2025, MOB 2022–2025, ROS/beredskapsanalyse inne |
| L8b ROS-gjennomgang | Uke 12–13 | Ferdig | Beredskapsanalyse og ROS gjennomgått, brukt i kap 4 og 6 |
| L8c EDA | Uke 12–13 | Ferdig | Døgnprofil, hendelsestyper, bindingstidsfordeling dokumentert |
| **L8d Nasjonal DSB 2025-oversikt (NY)** | Uke 15–16 | Ferdig 18.04 | 508 228 oppdrag, 12 sentraler, 7 figurer, volumavstemming, anomalier, størrelse-ranking |
| L9 Parameterestimering | Uke 13 | Ferdig | λ per skifttype fra BRIS, μ fra operative samtaler (3,44 min) |
| L10 Kapasitetsmodellering (Erlang-C + prosedyrbasert) | Uke 14 | Ferdig | ρ < 6 % alle skift — metodisk utilstrekkelig, beholdt som grunnlinje. Primærmodell prosedyrbasert |
| L11 Modellvalidering | Uke 14–15 | Ferdig | Bindingstid fra BRIS (median 13,0 min), VL-validering ferdig |
| L11b Sensitivitets- og scenarioanalyse | Uke 15 | Ferdig | +1 operatør, dimensjoneringskurve, total belastningsmodell variant A/B |
| L12 Teorikapittel | Uke 14–15 | **Ikke startet** | Skall finnes i rapport.md — må skrives innen peer review |
| L13 Benchmarking | Uke 15 | Ferdig | Alle 12 sentraler, MOB 2022–2025, figurer generert |
| **L13b LABA Sør-Vest dybdeanalyse (NY)** | Uke 16 | Ferdig 19.04 | Uttrekk-skript + xlsx-output. 50 hendelser utfylt av lokal operatør. Resultat: L-aba mean 6 min (dobbelt av tidligere antakelse), 24 % feilklassifisert — drev V3-regelutvidelse 19.04 |
| L14 Generaliseringsanalyse | Uke 15–16 | Delvis | Omtalt i kap 7.7, styrket med nasjonal oversikt L8d |
| **L14b Nasjonal 2025-analyse per sentral (NY)** | Uke 16 | Ferdig 18.04 | `nasjonal_2025_analyse.py`, 3 figurer |
| L15 Resultater og diskusjon | Uke 16 | **Ferdig 18.04** | Kap 7 ferdig, kap 8 v1.0 ferdig (lav-belastet paradoks, modell vs virkelighet, dimensjonering). Mindre talloppdatering nødvendig etter 19.04-klassifiseringsendring |
| **L17 Spørreskjemaer — intern kalibrering (REVIDERT)** | Uke 16 | Pågår | Skjema utviklet for alle 12 sentraler (`generer_skjema.py` +780 linjer). Sendt til et par lokale operatører for å kalibrere tider og verifisere spørsmål før utsendelse til andre sentraler. **Ingen skjema sendt til eksterne sentraler ennå.** Utsendelse avventer verifisert tidsgrunnlag fra lokal kalibrering og LABA-utfylling |
| **L18 DSB-ønskeliste BRIS-datauttrekk (NY)** | Uke 16 | Ferdig 18.04 | 22 prioriterte datapunkter, operatør-ID, samtalevarighet, ventetid m.m. |
| **L19 V3-regelutvidelse (Kilde=Alarm for L-aba) (NY)** | Uke 16 | Ferdig 19.04 | Alle 4 skript oppdatert. 2 065 oppdrag flyttet L-aba → L-hendelse. Variant B L-aba-bindingstid 3 → 6 min. Natt/helg Normal 52 % → 44 %, Svikt 22 % → 26 %. Kap 5/6/7 må oppdateres |
| L16 Hoved-utkast + peer review | Slutten av april | Pågår | Peer review fra 27. april |

## Rapportstatus

| Kapittel | Fil | Status | Kommentar |
|---|---|---|---|
| Sammendrag | rapport.md | Skall | Skrives sist |
| 1 Innledning | rapport.md | **Skall** | Problemstilling, RQ1–RQ5 og avgrensninger formulert — aktualisering og kunnskapsgap gjenstår |
| 2 Litteratur | kap2_litteratur.md | Ferdig v1.0 | Søkestrategi og 5 temaområder dokumentert (121 linjer) |
| 3 Teori | rapport.md | **Skall** | Køteori, Erlang-C, kapasitetsbegreper — ikke skrevet |
| 4 Casebeskrivelse | kap4_casebeskrivelse.md | Ferdig v1.1 | 110 Sør-Vest, bemanning, arbeidsmetodikk, operative særtrekk |
| 5 Metode og data | kap5_metode_data.md | **Oppdatering nødvendig** | V2.0 ferdig, men V3-regelen (Kilde=Alarm for L-aba) og LABA-dybdeanalyse (50 hendelser) må beskrives |
| 6 Modell | kap6_modell.md | **Oppdatering nødvendig** | V2.0 ferdig, men L-aba-bindingstid 3 → 6 min (empirisk kalibrert) må dokumenteres i 6.4 |
| 7 Analyse og resultater | kap7_analyse_resultater.md | **Oppdatering nødvendig** | V1.0 ferdig, men variant B-tall må oppdateres (natt/helg Normal 52 % → 44 %, Svikt 22 % → 26 %). Nasjonale tabeller L-aba/L-hendelse også |
| 8 Diskusjon | kap8_diskusjon.md | **Ferdig v1.0** | Lav-belastet paradoks, modell vs virkelighet, dimensjonering, begrensninger |
| 9 Konklusjon | rapport.md | **Skall** | Svar på problemstilling + RQ1–RQ5 — ikke skrevet |
| Referanser | rapport.md / Litteraturliste v3.0 | Pågår | md synkronisert mot xlsx (nr 52–64) |
| Vedlegg | — | Ikke startet | KI-erklæring, spørreskjemaer, DSB-ønskeliste, kode |

## Analyseartefakter

| Område | Skript | Figurer | Status |
|---|---|---|---|
| Primærmodell (ankomstkonflikt) | konflikt_v4_korrigert.py | kapasitet_v4_med_skjulte.png, kapasitet_v4_per_time.png | Fullført |
| Total belastningsmodell (variant B) | konflikt_total_belastning.py | total_belastning_A_vs_B.png, total_belastning_sensitivitet.png | Fullført |
| Bindingstidsanalyse | bindingstid_analyse.py | 4 figurer | Fullført |
| Benchmarking | benchmark_trend_analyse.py | 3 figurer | Fullført |
| Scenarioanalyse (+1 op) | scenario_pluss1.py | dimensjoneringskurve.png | Fullført |
| Kapasitetsfigurer | kapasitet_figurer.py | Diverse | Fullført |
| **Nasjonal DSB 2025 (NY)** | nasjonal_oversikt.py | nasjonal_oversikt_*.png (7 stk) | Fullført |
| **Nasjonal 2025 per sentral (NY)** | nasjonal_2025_analyse.py | nasjonal_2025_*.png (3 stk) | Fullført |
| **LABA Sør-Vest dybdeuttrekk (NY)** | uttrekk_laba_sorvest.py | laba_sorvest_2025_dybdeanalyse.xlsx | Fullført |
| **Spørreskjemageneratør (NY)** | generer_skjema.py, md_til_pdf.py | 11 md-skjemaer + 1 PDF så langt | Pågår |

## Milepæler

| ID | Milepæl | Planlagt | Faktisk | Vurdering |
|---|---|---|---|---|
| M1 | Godkjent proposal | 15. mars 2026 | Godkjent 7. mars | Ingen avvik |
| M2 | Godkjent prosjektplan | 15. mars 2026 | Godkjent 13. mars | Ingen avvik |
| M3 | Rapportskjelett klar | 22. mars 2026 | Ferdig 9. mars | Foran plan |
| M4 | Data innhentet og EDA ferdig | 29. mars 2026 | Ferdig mars 2026 | På plan |
| M5 | Kapasitetsmodell implementert og validert | 10. april 2026 | Ferdig 5. april | Foran plan |
| M6 | Hoved-utkast + peer review | Slutten av april / 27.04 | Pågår | Kap 1, 3, 9 gjenstår — 9 dager igjen |
| M7 | Endelig rapport + muntlig | 31. mai / juni | Planlagt | Ingen endring |

## Avvik mellom plan og faktisk

1. **Modellendring (fra v1.1):** Planen forutsatte Erlang-C som primærmodell. Analysen avdekket at Erlang-C er metodisk utilstrekkelig for 110-konteksten. Primærmodell er nå den prosedyrbaserte ankomstkonfliktmodellen. Erlang-C beholdes som grunnlinje.
2. **Sekvensgapmetode (fra v2.0):** Identifisering av sammenstilte anrop via sekvensgap i 110_ID var ikke planlagt. Gir 18 901 estimerte tilleggsanrop (korreksjonsfaktor 1,305×).
3. **Nye arbeidspakker (NYTT):** L8d, L13b, L14b, L17, L18 er lagt til siden v2.0 som respons på nasjonal generaliseringsambisjon og DSB-dialog. L8d/L14b/L18 styrker kap 7.7 og kap 8.3 direkte; L17 styrker datainnsamling for peer review; L13b gir dypere casebelegg.
4. **Teorikapittel (L12) fortsatt ikke startet.** Planlagt uke 14–15, nå uke 16. Moderat forsinkelse — innholdet er implisitt i kap 6, men må skrives eksplisitt. **Kritisk sti mot M6.**
5. **Kap 1 Innledning ikke startet.** Skall eksisterer, aktualisering/kunnskapsgap gjenstår. **Kritisk sti mot M6.**

## Datagrunnlag

| Kilde | Status |
|---|---|
| BRIS fullrapport 110 Sør-Vest 2025 (61 964 hendelser) | Inne — analysert |
| BRIS fullrapport nasjonal 2025 (508 228 oppdrag alle sentraler) | Inne — analysert (L8d/L14b) |
| DSB MOB-rapporter 2022–2025 | Inne — brukt i benchmarking |
| ROS/beredskapsanalyse 110 Sør-Vest | Inne — brukt i kap 4 og 6 |
| SSB befolkningsdata (1. jan 2026) | Inne — brukt i generaliseringsanalyse |
| BRIS fullrapport nasjonal med initiell hendelsestype | Forespurt fra DSB (Vidar Falkenberg) |
| Henvendelsesdata fra LEO (inquiries-array) | Forespurt fra DSB — ikke nødvendig for analyse |
| Spørreskjemaer til alle 12 sentraler | Utviklet (md + PDF-infrastruktur) — i intern kalibrering hos lokale operatører. Ingen sendt til eksterne sentraler ennå |
| LABA dybdeanalyse 50 hendelser (110 Sør-Vest 2025) | Utfylt av lokal operatør — mean bindingstid 6 min, 24 % feilklassifisert. Driver V3-regel 19.04 |
| DSB-ønskeliste BRIS-datauttrekk | Ferdig — kan sendes til DSB |
| Datadelingsvurdering fra DSB | E-post sendt til bris-support 5. april 2026 — avventer svar |

## Intervju- og kontaktlogg

| Dato | Sentral/kontakt | Form | Tema |
|---|---|---|---|
| 15.03.2026 | Midt-Norge 110 | Telefon (uformell) | Bemanning, servicetesting-organisering |
| Mars–april 2026 | 110 Sør-Vest | Løpende operativ dialog | Makkerpar, bindingstider, VL-rolle |
| 13.03–25.03.2026 | Vidar Falkenberg, DSB | E-post | Datatilgang, henvendelsesdata, initiell hendelsestype |
| 05.04.2026 | bris-support@dsb.no | E-post | Datadelingsvurdering for peer review |
| April 2026 | Lokale operatører 110 Sør-Vest | Intern kalibrering | Spørreskjema-utforming, LABA-dybdeanalyse (50 hendelser utfylt), tidsestimat-validering før utsendelse til andre sentraler |

## Risikoregister

| ID | Risiko | Status | Vurdering |
|---|---|---|---|
| R1 | BRIS-datakvalitet utilstrekkelig | Håndtert | Datakvalitet dokumentert i kap 5. Operatør-ID strukturelt fraværende — håndtert gjennom indirekte estimering |
| R2 | Erlang-C-forutsetninger brytes | Håndtert | Erlang-C degradert til grunnlinje. Primærmodell er prosedyrbasert og ikke avhengig av Poisson-antagelsen |
| R3 | Ring-flom forstyrrer Poisson | Delvis håndtert | Sekvensgapmetoden fanger sammenstilte anrop. Inquiry-data fra DSB kan styrke videre |
| R4 | VL-antagelse holder ikke | Lukket | Bekreftet gjennom prosedyre, operative samtaler og VL-validering bindingstider |
| R5 | Benchmarking vanskelig pga. heterogen bemanning | Håndtert | Benchmarking gjennomført med MOB-data. L8d/L14b styrker nasjonal dokumentasjon |
| R6 | Tilgang til tvers-sentraldata | Lukket 10.03 | LEO felles fra høst 2024, tilgang bekreftet |
| R7 | Tidskollisjon med vaktarbeid | Åpen | Buffer i Gantt — foreløpig håndterbart |
| R8 | Prokrastinering mot frist | **Åpen — kritisk** | Kap 1, 3, 9 må skrives + kap 5/6/7 oppdateres innen peer review 27. april — 8 dager igjen |
| R9 | Sensitive funn fra ROS-gjennomgang | Håndtert | Framing-retningslinje etablert: supplere, ikke angripe |
| R10 | Datadeling for peer review uavklart | Åpen | E-post sendt til DSB 5. april. Avventer svar |
| R11 | **Skjema til andre sentraler ikke sendt** | Åpen | Venter på verifisert tidsgrunnlag fra lokal kalibrering. Responstid fra eksterne sentraler vil uansett ikke rekke peer review 27.04 — benchmark-data fra DSB (L8d/L14b) dekker nasjonal del for peer review |
| R12 | **L-aba-klassifisering nasjonalt heterogen (NY)** | Åpen | Sør-Øst og Oslo har ≈0 % L-aba — trolig ulik registreringspraksis. Må adresseres i kap 8.3 som begrensning ved nasjonal benchmarking |

## Neste steg (prioritert mot peer review 27.04)

1. **Denne uken (uke 16, 19.–25.04):**
   - Oppdater kap 5/6/7 med 19.04-klassifiseringsregel (Kilde=Alarm for L-aba) og ny L-aba-bindingstid (6 min)
   - Skrive kap 3 (teori) — køteori, Erlang-C-rammeverk, kapasitetsbegreper, multiserver-jobs (Chelst & Barlach, Harchol-Balter)
   - Skrive kap 1 (innledning) — aktualisering, kunnskapsgap, rapportstruktur
   - Skrive kap 9 (konklusjon) — svar på problemstilling + RQ1–RQ5
   - Skrive vedlegg: LABA-dybdeanalyse (50 hendelser, metode, funn)
2. **Uke 17 (26.–27.04):**
   - Sammenstille rapportutkast — sammendrag, abstract, referanser, vedlegg
   - Levere hoved-utkast til peer review 27. april
3. **Mai:** Revisjon basert på peer review + endelig innlevering 31. mai
4. **Før peer review dersom tid:** Send DSB-ønskeliste til Vidar Falkenberg. Skjema til eksterne sentraler utsettes til etter hoved-utkast — kalibreres ferdig først.

## Versjonshistorikk

| Versjon | Dato | Endring |
|---|---|---|
| 1.0 | 2026-03-13 | Opprettet ved godkjenning av fase 2 |
| 1.1 | 2026-03-17 | Datagrunnlag oppdatert, litteraturliste ferdig, intervjulogg opprettet |
| 2.0 | 2026-04-06 | Full oppdatering: primærmodell ferdig, kap 2/4/5/6/7 ferdigskrevet, risikoregister oppdatert, analyseartefakter dokumentert, DSB-henvendelse om datadeling |
| 2.1 | 2026-04-18 | Kap 8 ferdig, total belastningsmodell, VL-validering, V3-kategorikonsistens, litteraturliste v3.0. Nye arbeidspakker L8d/L13b/L14b/L17/L18 lagt til. R11 (skjemarespons) ny risiko. Neste steg omprioritert mot peer review 27.04 |
| 2.2 | 2026-04-19 | LABA-dybdeanalyse (50 hendelser) utfylt av lokal operatør. V3-regel skjerpet: L-aba krever Kilde=Alarm. 2 065 oppdrag flyttet L-aba → L-hendelse. L-aba-bindingstid 3 → 6 min. Variant B natt/helg Normal 52 % → 44 %, Svikt 22 % → 26 %. L17 presisert: kun intern kalibrering, ingen eksterne sendinger ennå. R12 (heterogen nasjonal L-aba-klassifisering) ny risiko. L19 ny leveranse (V3-regelutvidelse). Kap 5/6/7 flagget for oppdatering |
