# Prosjektstatus — LOG650 G20 Rune Grødem

Statusdato: 2026-04-20

Denne statusen bygger på arbeidskopien per 2026-04-20, med prosjektstyringsplanen og WBS som referanse for avvik.

## Kort status

- Prosjektet er i fase 3 – gjennomføring. **Alle hovedkapitler er ferdigskrevet** i første versjon.
- Primærmodellen (V3 prosedyrbasert ankomstkonfliktmodell med op-binder-semantikk) er implementert, validert og dokumentert. D-pri1 og D-aba splittet som egne undertyper basert på operativ prosedyre.
- Erlang-C-grunnlinjen er fullført og brukes som kontrastpunkt.
- Total belastningsmodell (variant B) og scenario +1 operatør er oppdatert med V3-semantikk.
- **V3-klassifisering implementert gjennomgående:** L-aba og D-aba krever Kilde=Alarm. D-pri1 binder 2 ops (makkerpar), D-aba binder 1 op serielt (Fase 1 + valgfri Fase 2).
- **Hovedresultat V3 (110 Sør-Vest 2025):** Natt/helg Svikt 32,6 % (variant A), 33,4 % (variant B hoved). +1 op halverer Svikt natt/helg til 16,7 %.
- **LABA-utvalg utvidet til n=100** (20.04) — sendt til utfylling hos lokal operatør for å få smalere CI på L-aba-bindingstid enn n=30 ga ([3,70; 8,56]).
- Gjenstående rapportarbeid: sammendrag/abstract (skrives sist), vedlegg (KI-erklæring, spørreskjemaer, DSB-ønskeliste, kode), synkronisering skjelett → kapittelfiler, referanseliste-finjustering.
- Peer review planlagt fra 27. april (7 dager igjen). Rapportfrist 31. mai 2026.
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
| L12 Teorikapittel | Uke 14–15 | **Ferdig 19.04** | Kap 3 skrevet v1.0, 153 linjer. Erlang-C, QED/square-root staffing, multiserver-jobs, op-binder-semantikk som formalt rammeverk |
| L13 Benchmarking | Uke 15 | Ferdig | Alle 12 sentraler, MOB 2022–2025, figurer generert |
| **L13b LABA Sør-Vest dybdeanalyse n=50 (NY)** | Uke 16 | Ferdig 19.04 | 50 hendelser utfylt. Mean 5,88 min (Kilde=Alarm-subset, n=30). Drev V3-regelutvidelse |
| **L13c LABA utvalg n=100 (NY)** | Uke 16 | **Sendt til utfylling 20.04** | Utvidet utvalg for smalere CI. Populasjon 3 430, utvalg 100 (2,9 %). Venter svar |
| L14 Generaliseringsanalyse | Uke 15–16 | Delvis | Omtalt i kap 7.7 og kap 8.3, styrket med nasjonal oversikt L8d |
| **L14b Nasjonal 2025-analyse per sentral (NY)** | Uke 16 | Ferdig 18.04 | `nasjonal_2025_analyse.py`, 3 figurer |
| L15 Resultater og diskusjon | Uke 16 | **Ferdig 19.04** | Kap 7 og kap 8 oppdatert med V3-tall. Alle variant A/B-tabeller og funn reformulert |
| L15b Kap 1 Innledning | Uke 16 | **Ferdig 19.04** | Bakgrunn, kunnskapsgap, problemstilling, avgrensninger, struktur — alle placeholders fjernet |
| L15c Kap 9 Konklusjon | Uke 16 | **Ferdig 19.04** | Svar på problemstilling + RQ1–RQ5, tre dimensjoneringsanbefalinger |
| **L17 Spørreskjemaer — intern kalibrering** | Uke 16 | Pågår | Skjema utviklet for alle 12 sentraler (`generer_skjema.py`). Sendt til et par lokale operatører for å kalibrere tider og verifisere spørsmål før utsendelse. **Ingen skjema sendt til eksterne sentraler ennå.** Utsendelse etter LABA n=100 er tilbake |
| **L18 DSB-ønskeliste BRIS-datauttrekk (NY)** | Uke 16 | Ferdig 18.04 | 22 prioriterte datapunkter |
| **L19 V3-regelutvidelse (Kilde=Alarm) (NY)** | Uke 16 | Ferdig 19.04 | Alle 5 skript oppdatert. 2 065 oppdrag flyttet L-aba → L-hendelse. Kap 5/6/7 oppdatert |
| **L20 V3 op-binder-semantikk + D-pri1/D-aba-splitt (NY)** | Uke 16 | Ferdig 19.04 | Refaktorert modell: D-pri1 (2 ops, makkerpar) og D-aba (Fase 1 + Fase 2, serial). Natt/helg Svikt 26 % → 33 %. Styrker dimensjoneringsargument |
| L16 Hoved-utkast + peer review | Slutten av april | **Nær komplett** | Alle hovedkapitler ferdig. Gjenstår: sammendrag, vedlegg, skjelett-synkronisering. Peer review 27. april |

## Rapportstatus

| Kapittel | Fil | Status | Kommentar |
|---|---|---|---|
| Sammendrag | rapport.md | Skall | Skrives sist når helheten er klar |
| 1 Innledning | rapport.md | **Ferdig v1.0 (19.04)** | Bakgrunn, kunnskapsgap, problemstilling, RQ1–RQ5, avgrensninger, struktur |
| 2 Litteratur | kap2_litteratur.md | Ferdig v1.1 (19.04) | 121 linjer + Harchol-Balter og Brill & Green som multiserver-jobs-referanser |
| 3 Teori | kap3_teori.md | **Ferdig v1.0 (19.04)** | 153 linjer. Erlang-C, QED/square-root staffing, multiserver-jobs, op-binder-semantikk som formalt rammeverk |
| 4 Casebeskrivelse | kap4_casebeskrivelse.md | Ferdig v1.2 (19.04) | 110 Sør-Vest + ABA-dynamikk-skille (pri-1 vs ABA-utrykning) |
| 5 Metode og data | kap5_metode_data.md | Ferdig v3.0 (19.04) | V3-regel (Kilde=Alarm), ny 5.4 LABA-dybdeanalyse, D-pri1/D-aba-splitt |
| 6 Modell | kap6_modell.md | Ferdig v3.1 (19.04) | Op-binder-semantikk, D-pri1 (2 ops) + D-aba (Fase 1 + Fase 2) som undertyper |
| 7 Analyse og resultater | kap7_analyse_resultater.md | Ferdig v2.0 (19.04) | Alle variant A/B-tall V3. Natt/helg Svikt 32,6/33,4 %. Fem funn reformulert |
| 8 Diskusjon | kap8_diskusjon.md | Ferdig v1.1 (19.04) | V3-tall, modell-vs-virkelighet beholdt/styrket, D-pri1 som primær svikt-driver |
| 9 Konklusjon | kap9_konklusjon.md | **Ferdig v1.0 (19.04)** | Svar på problemstilling + RQ1–RQ5, tre anbefalinger, avsluttende refleksjon |
| Referanser | rapport.md / Litteraturliste v3.0 | Pågår | Må synkroniseres mot kap 2/3 nye referanser (Harchol-Balter, Brill & Green m.fl.) |
| Vedlegg | — | **Ikke startet** | KI-erklæring, spørreskjemaer, DSB-ønskeliste, LABA-dybdeanalyse-detaljer, kode |
| Skjelett-synk | Rapport_LOG650_G20_Rune_110_v0.1.md | **Gjenstår** | Skjelett-fil må integreres med separate kapittelfiler (kap 2, 3, 4, 5, 6, 7, 8, 9) |

## Analyseartefakter

| Område | Skript | Figurer | Status |
|---|---|---|---|
| V3 Primærmodell + Variant B (op-binder-semantikk) | konflikt_total_belastning.py | total_belastning_A_vs_B.png, total_belastning_sensitivitet.png | Fullført 19.04 |
| Bindingstidsanalyse | bindingstid_analyse.py | 4 figurer | Fullført |
| Benchmarking (2022–2025) | benchmark_trend_analyse.py | 3 figurer | Fullført |
| Scenarioanalyse (+1 op) V3 | scenario_pluss1.py | scenario_pluss1_operator.png | Fullført 19.04 |
| Kapasitetsfigurer | kapasitet_figurer.py | Diverse | Fullført |
| **Nasjonal DSB 2025 (NY)** | nasjonal_oversikt.py | nasjonal_oversikt_*.png (7 stk) | Fullført |
| **Nasjonal 2025 per sentral (NY)** | nasjonal_2025_analyse.py | nasjonal_2025_*.png (3 stk) | Fullført |
| **LABA dybdeanalyse n=50 (NY)** | uttrekk_laba_sorvest.py | laba_sorvest_2025_dybdeanalyse.xlsx | Fullført (utfylt + analysert) |
| **LABA dybdeanalyse n=100 (NY)** | uttrekk_laba_sorvest.py (oppdatert) | laba_sorvest_2025_dybdeanalyse_n100.xlsx | **Sendt til utfylling 20.04** |
| **Spørreskjemageneratør (NY)** | generer_skjema.py, md_til_pdf.py | 11 md-skjemaer + 1 PDF så langt | I intern kalibrering |
| **Sporbarhets-notat (NY)** | analyse/notat_V3_modellutvikling.md | — | Fullført 19.04 |

## Milepæler

| ID | Milepæl | Planlagt | Faktisk | Vurdering |
|---|---|---|---|---|
| M1 | Godkjent proposal | 15. mars 2026 | Godkjent 7. mars | Ingen avvik |
| M2 | Godkjent prosjektplan | 15. mars 2026 | Godkjent 13. mars | Ingen avvik |
| M3 | Rapportskjelett klar | 22. mars 2026 | Ferdig 9. mars | Foran plan |
| M4 | Data innhentet og EDA ferdig | 29. mars 2026 | Ferdig mars 2026 | På plan |
| M5 | Kapasitetsmodell implementert og validert | 10. april 2026 | Ferdig 5. april | Foran plan |
| M6 | Hoved-utkast + peer review | Slutten av april / 27.04 | **Nær komplett 19.04** | Alle hovedkapitler ferdig. Gjenstår: sammendrag, vedlegg, skjelett-synk. 7 dager igjen |
| M7 | Endelig rapport + muntlig | 31. mai / juni | Planlagt | Ingen endring |

## Avvik mellom plan og faktisk

1. **Modellendring (fra v1.1):** Planen forutsatte Erlang-C som primærmodell. Analysen avdekket at Erlang-C er metodisk utilstrekkelig for 110-konteksten. Primærmodell er nå V3 prosedyrbasert ankomstkonfliktmodell med op-binder-semantikk. Erlang-C beholdes som grunnlinje.
2. **Sekvensgapmetode (fra v2.0):** Identifisering av sammenstilte anrop via sekvensgap i 110_ID var ikke planlagt. Gir 18 901 estimerte tilleggsanrop (korreksjonsfaktor 1,305×).
3. **D-pri1/D-aba-splitt (19.04):** Operativ innsikt avdekket at ABA-utrykning har fundamentalt annen dynamikk enn pri-1-hendelser. Modellen differensierer nå makkerpar-bundet D-pri1 (2 ops) fra serial D-aba (1 op + valgfri Fase 2). Dette er en metodisk forbedring som styrker dimensjoneringsargumentet.
4. **Nye arbeidspakker:** L8d, L13b, L13c, L14b, L17, L18, L19, L20 er lagt til siden v2.0 som respons på empirisk validering, nasjonal generaliseringsambisjon og operativ innsikt.
5. **Kap 1, 3 og 9 skrevet 19.04.** Tidligere flagget som kritisk sti mot M6. Nå ferdig.
6. **Rapportskjelett må synkroniseres med separate kapittelfiler.** Skjelett-filen (`Rapport_LOG650_G20_Rune_110_v0.1.md`) har fortsatt kap 2-9 som eget innhold — må erstattes med referanser til separate filer eller inline-integreres.

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
| LABA dybdeanalyse 50 hendelser (110 Sør-Vest 2025) | Utfylt av lokal operatør — mean bindingstid 5,88 min (Kilde=Alarm-subset, n=30), 24 % feilklassifisert. Driver V3-regel 19.04 |
| LABA dybdeanalyse 100 hendelser (110 Sør-Vest 2025) | **Sendt til utfylling 20.04** — utvidet utvalg for smalere CI. Populasjon 3 430, utvalg 100 (2,9 %) |
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
| 20.04.2026 | Lokal operatør 110 Sør-Vest | LABA-dybdeanalyse utvidet | n=100-utvalg sendt til utfylling for smalere CI på L-aba-bindingstid |

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
| R8 | Prokrastinering mot frist | **Redusert** | Alle hovedkapitler skrevet 19.04. Gjenstår sammendrag, vedlegg, skjelett-synk — 7 dager igjen |
| R9 | Sensitive funn fra ROS-gjennomgang | Håndtert | Framing-retningslinje etablert: supplere, ikke angripe |
| R10 | Datadeling for peer review uavklart | Åpen | E-post sendt til DSB 5. april. Avventer svar |
| R11 | **Skjema til andre sentraler ikke sendt** | Åpen | Venter på verifisert tidsgrunnlag fra lokal kalibrering. Responstid fra eksterne sentraler vil uansett ikke rekke peer review 27.04 — benchmark-data fra DSB (L8d/L14b) dekker nasjonal del for peer review |
| R12 | **L-aba-klassifisering nasjonalt heterogen (NY)** | Åpen | Sør-Øst og Oslo har ≈0 % L-aba — trolig ulik registreringspraksis. Må adresseres i kap 8.3 som begrensning ved nasjonal benchmarking |

## Neste steg (prioritert mot peer review 27.04)

1. **Ventende (når LABA n=100 er tilbake):**
   - Statistikk på n=100 (mean/median/P90, bootstrap CI) og sammenligning mot n=30-subset
   - Oppdater L-aba-bindingstid i modellen dersom ny mean avviker fra 6 min
   - Gjennomgang av alle bindingstider gjennomgående i rapporten (kap 5.5, 6.4, 7.4, 7.6) for konsistens
   - Oppdater spørreskjema til sentralene basert på verifiserte verdier
2. **Denne uken (uke 16, 20.–25.04):**
   - Sammenstille rapportutkast: synkronisere skjelettfil med separate kapittelfiler
   - Skrive sammendrag/abstract basert på ferdig innhold
   - Skrive vedlegg: LABA-dybdeanalyse-detaljer, KI-erklæring, spørreskjema-eksempel, DSB-ønskeliste, kodeoversikt
   - Finjustere referanseliste (legg til Harchol-Balter, Brill & Green og øvrige nye refs fra kap 2/3)
3. **Uke 17 (26.–27.04):**
   - Endelig gjennomgang av hoved-utkast
   - Levere til peer review 27. april
4. **Mai:** Revisjon basert på peer review + endelig innlevering 31. mai
5. **Før peer review dersom tid:** Send DSB-ønskeliste til Vidar Falkenberg. Skjema til eksterne sentraler utsettes til etter hoved-utkast.

## Versjonshistorikk

| Versjon | Dato | Endring |
|---|---|---|
| 1.0 | 2026-03-13 | Opprettet ved godkjenning av fase 2 |
| 1.1 | 2026-03-17 | Datagrunnlag oppdatert, litteraturliste ferdig, intervjulogg opprettet |
| 2.0 | 2026-04-06 | Full oppdatering: primærmodell ferdig, kap 2/4/5/6/7 ferdigskrevet, risikoregister oppdatert, analyseartefakter dokumentert, DSB-henvendelse om datadeling |
| 2.1 | 2026-04-18 | Kap 8 ferdig, total belastningsmodell, VL-validering, V3-kategorikonsistens, litteraturliste v3.0. Nye arbeidspakker L8d/L13b/L14b/L17/L18 lagt til. R11 (skjemarespons) ny risiko. Neste steg omprioritert mot peer review 27.04 |
| 2.2 | 2026-04-19 | LABA-dybdeanalyse (50 hendelser) utfylt av lokal operatør. V3-regel skjerpet: L-aba krever Kilde=Alarm. 2 065 oppdrag flyttet L-aba → L-hendelse. L-aba-bindingstid 3 → 6 min. Variant B natt/helg Normal 52 % → 44 %, Svikt 22 % → 26 %. L17 presisert: kun intern kalibrering, ingen eksterne sendinger ennå. R12 (heterogen nasjonal L-aba-klassifisering) ny risiko. L19 ny leveranse (V3-regelutvidelse). Kap 5/6/7 flagget for oppdatering |
| 2.3 | 2026-04-20 | V3 op-binder-semantikk og D-pri1/D-aba-splitt implementert (L20). Alle hovedkapitler ferdig: kap 1, 3, 9 skrevet; kap 2, 4, 5, 6, 7, 8 oppdatert til V3. Scenario +1 op halverer Svikt natt/helg (33 → 17 %). LABA n=100-utvalg (L13c) sendt til utfylling. Rapport-status: kun sammendrag, vedlegg og skjelett-synk gjenstår før peer review. R8 (prokrastinering) nedgradert fra kritisk til redusert |
