# Prosjektstatus — LOG650 G20 Rune Grødem

Statusdato: 2026-04-06

Denne statusen bygger på arbeidskopien per 2026-04-06, med prosjektstyringsplanen og WBS som referanse for avvik.

## Kort status

- Prosjektet er i fase 3 – gjennomføring. Hovedanalysen er fullført.
- Primærmodellen (prosedyrbasert ankomstkonfliktmodell) er implementert, validert og dokumentert.
- Erlang-C-grunnlinjen er fullført og brukes som kontrastpunkt.
- Kap 2 (litteratur), kap 4 (case), kap 5 (metode), kap 6 (modell) og kap 7 (analyse) er ferdigskrevet.
- Gjenstående rapportarbeid: kap 1 (innledning), kap 3 (teori), kap 8 (diskusjon), kap 9 (konklusjon), sammendrag/abstract og sammenstilling.
- Peer review planlagt fra 27. april. Rapportfrist 31. mai 2026.
- E-post sendt til DSB (bris-support) 5. april om vurdering av datadeling for peer review.

## Faktisk fremdrift

| Leveranse | Planlagt | Faktisk status | Kommentar |
|---|---|---|---|
| L7 Rapportskjelett + intro v1 | Uke 12 | Ferdig 09.03 | Skjelett v0.1, kapittelstruktur etablert |
| L8 Datainnhenting | Uke 12 | Ferdig mars 2026 | BRIS 2025, MOB 2022–2025, ROS/beredskapsanalyse inne |
| L8b ROS-gjennomgang | Uke 12–13 | Ferdig | Beredskapsanalyse og ROS gjennomgått, brukt i kap 4 og 6 |
| L8c EDA | Uke 12–13 | Ferdig | Døgnprofil, hendelsestyper, bindingstidsfordeling dokumentert |
| L9 Parameterestimering | Uke 13 | Ferdig | λ per skifttype fra BRIS, μ fra operative samtaler (3,44 min) |
| L10 Erlang-C modellering | Uke 14 | Ferdig | ρ < 6 % alle skift — metodisk utilstrekkelig, beholdt som grunnlinje |
| L11 Modellvalidering | Uke 14–15 | Ferdig | Prosedyrbasert modell med bindingstid fra BRIS (median 13,0 min) |
| L11b Sensitivitetsanalyse | Uke 15 | Ferdig | Scenarioanalyse +1 operatør implementert |
| L12 Teorikapittel | Uke 14–15 | Ikke startet | Skall finnes i rapport.md |
| L13 Benchmarking | Uke 15 | Ferdig | Alle 12 sentraler, MOB 2022–2025, figurer generert |
| L14 Generaliseringsanalyse | Uke 15–16 | Delvis | Omtalt i kap 7.7, kan utvides |
| L15 Resultater og diskusjon | Uke 16 | Delvis | Kap 7 ferdig, kap 8 (diskusjon) ikke startet |
| L16 Hoved-utkast + peer review | Slutten av april | Pågår | Peer review fra 27. april |

## Rapportstatus

| Kapittel | Fil | Status | Kommentar |
|---|---|---|---|
| Sammendrag | rapport.md | Skall | Skrives sist |
| 1 Innledning | rapport.md | Skall | Problemstilling, RQ1–RQ5 og avgrensninger formulert |
| 2 Litteratur | kap2_litteratur.md | Ferdig v1.0 | Søkestrategi og 5 temaområder dokumentert (121 linjer) |
| 3 Teori | rapport.md | Skall | Køteori, Erlang-C, kapasitetsbegreper — ikke skrevet |
| 4 Casebeskrivelse | kap4_casebeskrivelse.md | Ferdig v1.1 | 110 Sør-Vest, bemanning, arbeidsmetodikk, operative særtrekk |
| 5 Metode og data | kap5_metode_data.md | Ferdig v2.0 | Forskningsdesign, datakilder, operasjonalisering, validitet |
| 6 Modell | kap6_modell.md | Ferdig v2.0 | Erlang-C grunnlinje + prosedyrbasert ankomstkonfliktmodell |
| 7 Analyse og resultater | kap7_analyse_resultater.md | Ferdig v1.0 | Erlang-C, bindingstid, kapasitetsanalyse, scenario +1, generaliserbarhet |
| 8 Diskusjon | rapport.md | Skall | Ikke skrevet |
| 9 Konklusjon | rapport.md | Skall | Ikke skrevet |
| Referanser | rapport.md | Skall | Ikke sammenstilt |
| Vedlegg | — | Ikke startet | KI-erklæring, intervjuguide, kode |

## Analyseartefakter

| Område | Skript | Figurer | Status |
|---|---|---|---|
| Primærmodell (ankomstkonflikt) | konflikt_v4_korrigert.py | kapasitet_v4_med_skjulte.png, kapasitet_v4_per_time.png | Fullført |
| Bindingstidsanalyse | bindingstid_analyse.py | bindingstid_histogram.png, bindingstid_beredskap_fordeling_v2.png, bindingstid_dag_natt.png, bindingstid_per_time.png | Fullført |
| Benchmarking | benchmark_trend_analyse.py | 3 figurer i analyse/figurer/ | Fullført |
| Scenarioanalyse (+1 op) | scenario_pluss1.py | dimensjoneringskurve.png | Fullført |
| Kapasitetsfigurer | kapasitet_figurer.py | Diverse | Fullført |

## Milepæler

| ID | Milepæl | Planlagt | Faktisk | Vurdering |
|---|---|---|---|---|
| M1 | Godkjent proposal | 15. mars 2026 | Godkjent 7. mars | Ingen avvik |
| M2 | Godkjent prosjektplan | 15. mars 2026 | Godkjent 13. mars | Ingen avvik |
| M3 | Rapportskjelett klar | 22. mars 2026 | Ferdig 9. mars | Foran plan |
| M4 | Data innhentet og EDA ferdig | 29. mars 2026 | Ferdig mars 2026 | På plan |
| M5 | Modell implementert og validert | 10. april 2026 | Ferdig april 2026 | På plan — primærmodell erstatter Erlang-C som primærmodell |
| M6 | Hoved-utkast + peer review | Slutten av april | Pågår | Kap 1, 3, 8, 9 gjenstår |
| M7 | Endelig rapport + muntlig | 31. mai / juni | Planlagt | Ingen endring |

## Avvik mellom plan og faktisk

1. **Modellendring:** Planen forutsatte Erlang-C som primærmodell. Analysen avdekket at Erlang-C er metodisk utilstrekkelig for 110-konteksten (ρ < 6 % men makkerpar-binding ikke fanget). Primærmodell er nå den prosedyrbaserte ankomstkonfliktmodellen. Erlang-C beholdes som grunnlinje. Dette er en faglig begrunnet endring, ikke et avvik fra tidsplan.
2. **Sekvensgapmetode:** Identifisering av sammenstilte anrop via sekvensgap i 110_ID var ikke planlagt, men ble utviklet som respons på databegrensninger. Gir 18 901 estimerte tilleggsanrop (korreksjonsfaktor 1,305x).
3. **Teorikapittel (L12) ikke startet.** Planlagt uke 14–15, nå i uke 15. Moderat forsinkelse — innholdet er implisitt i kap 6, men må skrives eksplisitt.

## Datagrunnlag

| Kilde | Status |
|---|---|
| BRIS fullrapport 110 Sør-Vest 2025 (61 964 hendelser) | Inne — analysert |
| BRIS fullrapport nasjonal 2025 (alle sentraler) | Inne — brukt i benchmarking |
| DSB MOB-rapporter 2022–2025 | Inne — brukt i benchmarking |
| ROS/beredskapsanalyse 110 Sør-Vest | Inne — brukt i kap 4 og 6 |
| SSB befolkningsdata (1. jan 2026) | Inne — brukt i generaliseringsanalyse |
| BRIS fullrapport nasjonal med initiell hendelsestype | Forespurt fra DSB (Vidar Falkenberg) |
| Henvendelsesdata fra LEO (inquiries-array) | Forespurt fra DSB — ikke nødvendig for analyse |
| Spørreskjemaer til alle 12 sentraler | Sendt ut — avventer svar |
| Datadelingsvurdering fra DSB | E-post sendt til bris-support 5. april 2026 |

## Intervju- og kontaktlogg

| Dato | Sentral/kontakt | Form | Tema |
|---|---|---|---|
| 15.03.2026 | Midt-Norge 110 | Telefon (uformell) | Bemanning, servicetesting-organisering |
| Mars–april 2026 | 110 Sør-Vest | Løpende operativ dialog | Makkerpar, bindingstider, VL-rolle |
| 13.03–25.03.2026 | Vidar Falkenberg, DSB | E-post | Datatilgang, henvendelsesdata, initiell hendelsestype |
| 05.04.2026 | bris-support@dsb.no | E-post | Datadelingsvurdering for peer review |

## Risikoregister

| ID | Risiko | Status | Vurdering |
|---|---|---|---|
| R1 | BRIS-datakvalitet utilstrekkelig | Håndtert | Datakvalitet dokumentert i kap 5. Operatør-ID strukturelt fraværende — håndtert gjennom indirekte estimering |
| R2 | Erlang-C-forutsetninger brytes | Håndtert | Erlang-C degradert til grunnlinje. Primærmodell er prosedyrbasert og ikke avhengig av Poisson-antagelsen |
| R3 | Ring-flom forstyrrer Poisson | Delvis håndtert | Sekvensgapmetoden fanger sammenstilte anrop. Inquiry-data fra DSB kan styrke videre |
| R4 | VL-antagelse holder ikke | Lukket | Bekreftet gjennom prosedyre og operative samtaler |
| R5 | Benchmarking vanskelig pga. heterogen bemanning | Håndtert | Benchmarking gjennomført med MOB-data. Organisatoriske forskjeller (Midt-Norge servicepersonell) dokumentert |
| R6 | Tilgang til tvers-sentraldata | Lukket 10.03 | LEO felles fra høst 2024, tilgang bekreftet |
| R7 | Tidskollisjon med vaktarbeid | Åpen | Buffer i Gantt — foreløpig håndterbart |
| R8 | Prokrastinering mot frist | Åpen | Kap 1, 3, 8, 9 må skrives innen peer review 27. april |
| R9 | Sensitive funn fra ROS-gjennomgang | Håndtert | Framing-retningslinje etablert: supplere, ikke angripe |
| R10 | Datadeling for peer review uavklart | Ny | E-post sendt til DSB 5. april. Avventer svar |

## Neste steg

1. **Uke 15 (nå):** Skrive kap 3 (teori) — køteori, Erlang-C-rammeverk, kapasitetsbegreper
2. **Uke 15–16:** Skrive kap 8 (diskusjon) — funn mot problemstilling, begrensninger, implikasjoner
3. **Uke 16:** Skrive kap 9 (konklusjon) — svar på problemstilling
4. **Uke 16:** Ferdigstille kap 1 (innledning) — aktualisering, kunnskapsgap, rapportstruktur
5. **Uke 16–17:** Sammenstille rapportutkast — sammendrag, abstract, referanser, vedlegg
6. **27. april:** Peer review starter
7. **Mai:** Revisjon basert på peer review + endelig innlevering 31. mai

## Versjonshistorikk

| Versjon | Dato | Endring |
|---|---|---|
| 1.0 | 2026-03-13 | Opprettet ved godkjenning av fase 2 |
| 1.1 | 2026-03-17 | Datagrunnlag oppdatert, litteraturliste ferdig, intervjulogg opprettet |
| 2.0 | 2026-04-06 | Full oppdatering: primærmodell ferdig, kap 2/4/5/6/7 ferdigskrevet, risikoregister oppdatert, analyseartefakter dokumentert, DSB-henvendelse om datadeling |
