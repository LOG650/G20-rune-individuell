# Prosjektstatus — LOG650 G20 Rune Grødem

Statusdato: 2026-04-22

Denne statusen bygger på arbeidskopien per 2026-04-22, med prosjektstyringsplanen og WBS som referanse for avvik.

## Kort status

- Prosjektet er i fase 3 – gjennomføring. **Alle hovedkapitler er ferdigskrevet** i første versjon.
- Primærmodellen (V3 prosedyrbasert ankomstkonfliktmodell med op-binder-semantikk) er implementert, validert og dokumentert. D-pri1 og D-aba splittet som egne undertyper basert på operativ prosedyre.
- Erlang-C-grunnlinjen er fullført og brukes som kontrastpunkt.
- Total belastningsmodell (variant B) og scenario +1 operatør er oppdatert med V3-semantikk.
- **V3-klassifisering implementert gjennomgående:** L-aba og D-aba krever Kilde=Alarm. D-pri1 binder 2 ops (makkerpar), D-aba binder 1 op serielt (Fase 1 + valgfri Fase 2).
- **LABA n=100 ferdig utfylt 22.04** — Mean L-aba-bindingstid justert fra 5,88 min (n=30, CI [3,70; 8,56]) til **4,53 min (n=100, CI [3,74; 5,43])**. Hovedparameter satt til 4,5 min. Antagelse A5 oppgradert fra orienteringsanslag til empirisk kalibrert. Modell re-kjørt; sensitivitetsscenarioer endret til 3/4,5/7 min.
- **Hovedresultat V3 (110 Sør-Vest 2025) etter LABA n=100:** Natt/helg Svikt 32,6 % (variant A), **33,2 %** (variant B hoved, marginal endring fra 33,4 %). +1 op halverer Svikt natt/helg til 16,7 %. Variant A er uendret (L-aba inngår ikke).
- **PDF-pipeline etablert** (`verktoy/build_pdf.py`, Pandoc + XeLaTeX): samlet rapport-PDF (74 sider, A4, forside, ToC, alle kapitler med 5 figurer, referanser, vedlegg), DSB-ønskeliste-PDF, og 12 interaktive AcroForm-spørreskjemaer.
- Spørreskjema regenerert med oppdatert L-aba-referanse (4,5 min, LABA n=100).
- Gjenstående rapportarbeid: vedlegg-finpuss (KI-erklæring, spørreskjemaer, DSB-ønskeliste, kode), referanseliste-finjustering.
- Peer review 27. april (5 dager igjen). Rapportfrist 31. mai 2026.
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
| Forside + sammendrag | _forside_og_kap1.md | **Ferdig v1.1 (22.04)** | YAML-frontmatter med tittel, undertittel, forfatter, dato, abstract (350 ord). Renderer via Pandoc titling som dedikert forside |
| 1 Innledning | _forside_og_kap1.md | **Ferdig v1.1 (22.04)** | Bakgrunn, kunnskapsgap, problemstilling, RQ1–RQ5, V3-nomenklaturtabell (1.4), avgrensninger med eksplisitt single-case-omfang, struktur |
| 2 Litteratur | kap2_litteratur.md | **Ferdig v1.2 (21.04)** | Gap 1–5 + studiens posisjonering (Gap 1/2/5). Originalitet myket («fremstår som en av de første»). Interdep. arbeidsgruppe 2009 + Harchol-Balter + Brill & Green |
| 3 Teori | kap3_teori.md | **Ferdig v1.1 (21.04)** | Op-binder-semantikk klargjort som forfatterens syntese av Chelst & Barlach + Harchol-Balter, med 110-konkret eksempel før Definisjon 3.1 |
| 4 Casebeskrivelse | kap4_casebeskrivelse.md | **Ferdig v1.3 (21.04)** | VL-forutsetning henviser til VL_validering_bindingstider.md. Figur 4.1 bildetekst presisert |
| 5 Metode og data | kap5_metode_data.md | **Ferdig v3.2 (22.04)** | V3-regel, refleksivitet/insider-bias-avsnitt, deterministisk analyseflyt myket, datavask for nasjonal benchmarking, **LABA n=100-statistikk** (mean 4,53 min, CI [3,74; 5,43]) |
| 6 Modell | kap6_modell.md | **Ferdig v3.3 (22.04)** | Op-binder-semantikk, D-pri1/D-aba-splitt, [Antagelse 6.1] under Tabell 6.2, ny seksjon 6.7 antagelsestabell A1–A8 (A5 oppgradert til empirisk kalibrert med n=100) |
| 7 Analyse og resultater | kap7_analyse_resultater.md | **Ferdig v2.1 (22.04)** | Erlang-C 5,9 % (referansemodell). V3-funn variant A 32,6 % / variant B **33,2 %** (oppdatert etter LABA n=100). Funn 4 explicit om scenario-baseline 32,8 (stokastisk støy). 4 figurer |
| 8 Diskusjon | kap8_diskusjon.md | **Ferdig v1.2 (22.04)** | RQ-oversikt, multiserver-job-konkretisering, driftsstandard vs lovpålagt minimum, L-ukjent som naturlig kategori, LABA n=100-omtale |
| 9 Konklusjon | kap9_konklusjon.md | **Ferdig v1.1 (22.04)** | Eksplisitt single-case-omfang, prosedyrkonformitet vs tjenesteleveranse, kø-effektivitet vs prosedyre-sikkerhet i 9.5, 9.4 strukturert i tre nivåer (case/forutsetninger/forskning) |
| Referanser | _referanser_og_vedlegg.md | **Ferdig v1.0 (22.04)** | 33 APA-referanser (foreløpig utvalg) — synkroniseres mot full Litteraturliste_LOG650 v3.0 ved endelig innlevering |
| Vedlegg A–G | _referanser_og_vedlegg.md | **Ferdig v1.0 (22.04)** | A: Python/skript + GitHub. B: Spørreskjema. C: DSB-ønskeliste. D: KI-erklæring. E: LABA-detaljer. F: VL-validering. G: Prosjektdokumentasjon |
| Samlet rapport-PDF | Rapport_LOG650_G20_Rune_110_samlet.pdf | **Bygget v1.1 (22.04)** | 74 sider, A4, forside, ToC, alle kapitler med 5 figurer, referanser, vedlegg. Genereres via `verktoy/build_pdf.py --rapport-full` |

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
| **LABA dybdeanalyse n=100 (NY)** | uttrekk_laba_sorvest.py | laba_sorvest_2025_dybdeanalyse_n100-ferdig utfylt.xlsx | **Ferdig 22.04**: mean 4,53 min, CI [3,74; 5,43], 78 % m/nødtelefon |
| **Spørreskjemageneratør (NY)** | generer_skjema.py, md_til_pdf.py | 12 md-skjemaer + 12 AcroForm-PDFer | Klare for utsendelse — venter på godkjenning av tider/innhold |
| **Sporbarhets-notat (NY)** | analyse/notat_V3_modellutvikling.md | — | Fullført 19.04 |
| **PDF-pipeline (NY)** | verktoy/build_pdf.py + dokument-header.tex | Pandoc + XeLaTeX | Etablert 21.04 — håndterer rapport, ønskelister, AcroForm-skjema |
| **Nasjonal D-pri1/D-aba-splitt (NY)** | nasjonal_2025_analyse.py (oppdatert) | benchmarkmatrise.csv regenerert | Ferdig 21.04: 4 472 D-pri1 + 3 055 D-aba nasjonalt |

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
4. **LABA to-trinns kalibrering (22.04):** Ikke planlagt opprinnelig. Runde 1 (n=49 / n=30 Kilde=Alarm) ga orienteringsanslag 5,88 min. Runde 2 (n=100, alle Kilde=Alarm) gir empirisk hovedparameter 4,53 min ([3,74; 5,43]). Reduserer L-aba-bindingstid fra 6 → 4,5 min; variant B Svikt natt/helg endret marginalt 33,4 → 33,2 %.
5. **Nye arbeidspakker:** L8d, L13b, L13c, L14b, L17, L18, L19, L20 + PDF-pipeline (build_pdf.py) er lagt til siden v2.0 som respons på empirisk validering, nasjonal generaliseringsambisjon, operativ innsikt og leveranseformat (PDF).
6. **Skjelett-fil ikke synkronisert (avvik avklart 22.04):** Ny pipeline bruker `_forside_og_kap1.md` + kapittelfilene + `_referanser_og_vedlegg.md` direkte. Skjelett-filen `Rapport_LOG650_G20_Rune_110_v0.1.md` er beholdt som arkiv og ikke lenger aktiv del av leveransen.

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
| LABA dybdeanalyse 100 hendelser (110 Sør-Vest 2025) | **Ferdig utfylt 22.04** — mean 4,53 min (CI [3,74; 5,43]), median 3,27 min, P90 9,48 min, 78 % m/nødtelefon. Hovedparameter L-aba justert 6 → 4,5 min |
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
| 22.04.2026 | Lokal operatør 110 Sør-Vest | LABA n=100 returnert | Ferdig utfylt utvalg returnert. Mean L-aba 4,53 min med strammere CI. Hovedparameter justert i modellen |

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

## Neste steg (5 dager til peer review 27.04)

### MÅ gjøres før peer review

1. **Endelig gjennomlesing av samlet rapport-PDF** (74 sider): sjekk at forside, ToC, alle kapitler, figurer, referanser og vedlegg ser riktig ut i bladbar PDF-format
2. **Synkronisere kap-2-tabell** med rapportstatus over (kapittel-versjoner)
3. **Oppdater Gantt** med L13c lukket (LABA n=100 ferdig 22.04) og PDF-pipeline-leveranser
4. **Levere til peer review 27. april** — last opp PDF + ev. tilleggsmateriale

### KAN gjøres før peer review (lavere prioritet)

5. **Send DSB-ønskeliste** til Vidar Falkenberg (DSB) — dokumentet er ferdig (PDF i `005 report/`)
6. **Send LABA n=100-resultater** til lokal operatør med takk + sluttrapport
7. **Send spørreskjema til 1–2 utvalgte sentraler** for å starte responsinnsamling (Midt-Norge naturlig kandidat — har bekreftet positiv kontakt). Responstid utenfor peer review-vinduet, men datagrunnlag inn mot endelig innlevering 31.05

### Mai 2026 — etter peer review

8. **Motta peer review-tilbakemelding** ca. 4.–10. mai
9. **Revisjon av rapport** basert på review (uke 19–20)
10. **Endelig referanseliste-finjustering** mot full Litteraturliste v3.0 (33 → 50+ kilder)
11. **D-pri1/D-aba-splittet** kunne med fordel også implementeres i nasjonal benchmarking-figurer for kap 7.8 (i dag bare D aggregert i nasjonale plots)
12. **Endelig innlevering** 31. mai 2026
13. **Forberede muntlig eksamen** tidlig juni

### Eksplisitt nedprioritert (ikke nødvendig før innlevering)

- **D-aba Fase 2 empirisk validering** — vurdert 22.04, prioritert til DSB-datatilgang fremfor ad hoc-skript på dagens BRIS-eksport (ufullstendig data gir kun underkant-estimat). Lagt til som styrkelse av punkt 3 i DSB-ønskelisten.
- **Skjelett-fil-synk** — ikke aktuelt lenger; ny pipeline bygger fra `_forside_og_kap1.md` + kapittelfiler + `_referanser_og_vedlegg.md`. Skjelett-filen `Rapport_LOG650_G20_Rune_110_v0.1.md` beholdes som arkiv.

## Versjonshistorikk

| Versjon | Dato | Endring |
|---|---|---|
| 1.0 | 2026-03-13 | Opprettet ved godkjenning av fase 2 |
| 1.1 | 2026-03-17 | Datagrunnlag oppdatert, litteraturliste ferdig, intervjulogg opprettet |
| 2.0 | 2026-04-06 | Full oppdatering: primærmodell ferdig, kap 2/4/5/6/7 ferdigskrevet, risikoregister oppdatert, analyseartefakter dokumentert, DSB-henvendelse om datadeling |
| 2.1 | 2026-04-18 | Kap 8 ferdig, total belastningsmodell, VL-validering, V3-kategorikonsistens, litteraturliste v3.0. Nye arbeidspakker L8d/L13b/L14b/L17/L18 lagt til. R11 (skjemarespons) ny risiko. Neste steg omprioritert mot peer review 27.04 |
| 2.2 | 2026-04-19 | LABA-dybdeanalyse (50 hendelser) utfylt av lokal operatør. V3-regel skjerpet: L-aba krever Kilde=Alarm. 2 065 oppdrag flyttet L-aba → L-hendelse. L-aba-bindingstid 3 → 6 min. Variant B natt/helg Normal 52 % → 44 %, Svikt 22 % → 26 %. L17 presisert: kun intern kalibrering, ingen eksterne sendinger ennå. R12 (heterogen nasjonal L-aba-klassifisering) ny risiko. L19 ny leveranse (V3-regelutvidelse). Kap 5/6/7 flagget for oppdatering |
| 2.3 | 2026-04-20 | V3 op-binder-semantikk og D-pri1/D-aba-splitt implementert (L20). Alle hovedkapitler ferdig: kap 1, 3, 9 skrevet; kap 2, 4, 5, 6, 7, 8 oppdatert til V3. Scenario +1 op halverer Svikt natt/helg (33 → 17 %). LABA n=100-utvalg (L13c) sendt til utfylling. Rapport-status: kun sammendrag, vedlegg og skjelett-synk gjenstår før peer review. R8 (prokrastinering) nedgradert fra kritisk til redusert |
| 2.4 | 2026-04-22 | **LABA n=100 ferdig utfylt** (L13c lukket). Hovedparameter L-aba: 6 min → **4,5 min** (mean 4,53 min, CI [3,74; 5,43]). Antagelse A5 oppgradert til empirisk kalibrert. Modell re-kjørt: variant B natt/helg Svikt 33,4 → 33,2 % (variant A uendret 32,6 %). Kap 5.4, 6.4.5, 6.7, 7.4.4, 7.7, 8.4.3 og 9 oppdatert. Spørreskjema regenerert med 4,5 min som Sør-Vest-referanse. **PDF-pipeline etablert** (`verktoy/build_pdf.py`, Pandoc + XeLaTeX): samlet rapport-PDF (74 sider med forside, ToC, 5 figurer), DSB-ønskeliste-PDF, 12 AcroForm-skjemaer. _forside_og_kap1.md og _referanser_og_vedlegg.md skapt for ren samlet bygging |
