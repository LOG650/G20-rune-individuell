# Prosjektstatus — LOG650 G20 Rune Grødem

Statusdato: 2026-05-15 (v2.8)

Denne statusen bygger på arbeidskopien per 2026-05-15, med prosjektstyringsplanen og WBS som referanse for avvik.

## Endringer fra v2.7 (2026-05-15)

**Bootstrap-CI for D-pri1-bindingstid (peer review-respons runde 2):** Ny ikke-parametrisk bootstrap-analyse (B = 1 000) propagerer statistisk usikkerhet i den observerte D-pri1-bindingstidsfordelingen og imputeringsusikkerhet for de 19 % manglende verdiene gjennom variant A-modellen. Resultat: **95 % CI for Svikt natt/helg = [32,1; 33,2] %** rundt punktestimat 32,8 %. Hovedfunnet er statistisk svært stabilt (CI-bredde 1,1 pp). MAR-sjekk avdekket at missingness klynger seg på Oppdragstype (CV 0,98), særlig "Avbrutt utrykning samtale" (73 % missing) — men avviket trekker estimatet i konservativ retning og endrer ikke konklusjonen.

Endringer i artefakter:
- `analyse/scripts/bootstrap_dpri1.py` — nytt skript med MAR-sjekk + bootstrap-loop
- `analyse/bootstrap_dpri1_resultater.csv` — CI per skift × niva
- `analyse/bootstrap_dpri1_mar_sjekk.csv` — missingness per Oppdragstype/Skift/Måned
- `analyse/figurer/bootstrap_dpri1_ci.png` — bootstrap-fordeling med punktestimat og CI
- `analyse/bootstrap_dpri1_run.log` — full kjøringslogg

Endringer i rapporten:
- Kap 3 v1.3 — intro-setning rammer Erlang-C som spesialtilfelle, ikke konkurrerende modell (avvæpner halmmann-kritikk fra peer review runde 2)
- Kap 5 v3.4 — bootstrap-CI lagt til som 6. reliabilitets-grep i 5.6.2; trussel 3 oppdatert; missingness korrigert til 19 % (var feilaktig 25 %)
- Kap 6 v3.5 — A2-status oppgradert til "Empirisk + statistisk validert"; D-pri1-imputasjon korrigert til 19 %; bootstrap-CI lenket fra Tabell 6.3 og A2-konsekvensvurdering
- Kap 7 v2.3 — nytt avsnitt 7.7.4 med Tabell 7.10b og bootstrap-figur
- Kap 9 v1.3 — skarp åpningssetning i 9.1 med direkte svar på problemstillingen før alle nyansene; bootstrap-CI inkludert i hovedsvar

## Endringer fra v2.6 (samme dag, senere)

**Kritisk feilretting:** Commit a7f24f5 (revisjon 2) hadde avkuttet hale i åtte rapportfiler — mid-setning eller mid-ord. Avkuttingen er nå restaurert:

- `_forside_og_kap1.md`: Forkortelseslisten 1.4.2 fullført (ROS, SSB, V3, VL), seksjonene 1.5 (Avgrensninger) og 1.6 (Rapportens struktur) restaurert.
- `kap2_litteratur.md`: Avsnitt 2.6 (kunnskapsgap Gap 1–5 + studiens posisjonering) restaurert.
- `kap3_teori.md`: Siste setning i 3.9 fullført + versjonsfooter.
- `kap4_casebeskrivelse.md`: Versjonsfooter lagt til.
- `kap5_metode_data.md`: Avsluttende ledd i 5.7 (etiske vurderinger, KI-bruk, oppsummering) restaurert.
- `kap6_modell.md`: Konsekvens-vurdering A2–A8 (P2.A i revisjon 2) skrevet i samme format som A1, samt samlet robusthetsvurdering.
- `kap7_analyse_resultater.md`: Avsnitt 7.10 (generaliserbarhet) og 7.11 (5 hovedfunn) restaurert + tre observasjoner under 7.9.3.
- `kap8_diskusjon.md`: Avsnitt 8.4.2 (modellmessige begrensninger), 8.4.3 (antakelser med konsekvenser) og 8.5 (videre forskning) restaurert.
- `kap9_konklusjon.md`: Avsluttende ledd i 9.5 restaurert + case-omfangs-presisering.

**P2-revisjoner i kap 5 utført:**
- 5.3.4: Sekvensgap-skjevhetsdrøfting strukturert i tre retninger (overestimering / underestimering / nettovurdering) med plausible størrelsesordener.
- 5.6.1: Validitetstrusler eksplisitt strukturert etter konstrukt-, intern- og ekstern validitet (5 nummererte trusler).
- 5.6.2: Insider-bias-kontroller listet eksplisitt som 5 grep + erkjent residuell risiko som ikke kan elimineres uten uavhengig replikasjon.

**Mindre språkrevisjoner:**
- Kap 1.2 og 1.3: To overlange setninger brutt opp.
- Kap 4.2.1 (skiftstruktur): Lang setning brutt opp.
- Kap 8.1 (Erlang-C-tolkning): Lang setning med to forskere brutt opp.
- Kap 4.1: Tabell 4.1 fikk eksplisitt intro-setning.

## Kort status

- Prosjektet er i fase 3 – gjennomføring. **Alle hovedkapitler er skrevet, og revisjon 2 etter peer review er gjennomført.**
- **Peer review mottatt 3. mai 2026 fra G21** (Elisabeth K. Orlien og Kaylee Floden). PDF arkivert som `013 fase 3 - review/Peer_review_G21_til_G20_mottatt_2026-05-03.pdf`. Detaljert gap-analyse: `013 fase 3 - review/peer_review_G21_mottatt_analyse.md`.
- **Revisjon 1 (delvis) ferdig 6. mai:** Formalia, kryssreferanser, tallavvik harmonisert, Penverne flyttet til kap 2, sekvensgap-forbehold inn i 5.3.4, √R-presisjon i 8.3.2, c_eff = c_total − 1 rammet inn i 9.5.
- **Revisjon 2 ferdig 13. mai (commit a7f24f5):** G21s tre hovedkritikker er adressert substansielt:
  - **P1.1 Scenariobånd** integrert i kap 7.5–7.7 og 7.11 (variant B-bånd 28–39 % ved sentrale tall, ikke kun i Tabell 7.10).
  - **P1.2 Generaliseringsnedtoning** i kap 7.9–7.10 og 9.1/9.5 (nasjonale anbefalinger reformulert som hypoteser/forutsetninger).
  - **P1.3 Balansert diskusjon** i kap 8.1–8.3 (nytt 8.2.3 med alternative tolkninger; Erlang-C-kritikk mindre kategorisk).
  - **P1.4 Språkrevisjon** i kap 3 og 5 + forkortelsesliste i kap 1.4.2 (gjenstår: kap 1/2/4/7/8/9, 110-sentral-standardisering, figur/tabell-integrering).
  - **P2.A** Konsekvens-vurdering for A1–A8 i Tabell 6.3 + tekstavsnitt.
  - **P2.B** Innledning kap 1.1–1.2 redusert ~30 %.
  - **P2.C** Litteraturkapittel mer analytisk (kap 2.2–2.5 med bro til metodevalg og per-kilde-begrensninger).
  - **P3.1** Kritisk kildevurdering pr. hovedkilde i kap 2.
  - **P3.2** Hva modellen faktisk måler tydeliggjort i kap 7.5-intro.
- Primærmodellen (V3 prosedyrbasert ankomstkonfliktmodell med op-binder-semantikk) er implementert, validert og dokumentert. D-pri1 og D-aba splittet som egne undertyper basert på operativ prosedyre.
- Erlang-C-grunnlinjen er fullført og brukes som kontrastpunkt.
- Total belastningsmodell (variant B) og scenario +1 operatør er oppdatert med V3-semantikk.
- **V3-klassifisering implementert gjennomgående:** L-aba og D-aba krever Kilde=Alarm. D-pri1 binder 2 ops (makkerpar), D-aba binder 1 op serielt (Fase 1 + valgfri Fase 2).
- **LABA n=100 ferdig utfylt 22.04** — Mean L-aba 4,53 min (CI [3,74; 5,43]). Hovedparameter L-aba satt til 4,5 min. Antagelse A5 oppgradert fra orienteringsanslag til empirisk kalibrert.
- **Hovedresultat V3 (110 Sør-Vest 2025) etter LABA n=100:** Natt/helg Svikt 32,6 % (variant A), **33,2 %** (variant B hoved; scenariobånd 28–39 % under variant B). +1 op halverer Svikt natt/helg til 16,7 % (under nåværende antagelsesgrunnlag).
- **PDF-pipeline (`verktoy/build_pdf.py`, Pandoc + XeLaTeX):** Samlet rapport-PDF rebygget etter revisjon 2 (808 930 bytes per a7f24f5).
- Gjenstående administrativt:
  - **Forsideveileder** står som placeholder — fylles inn ved innlevering.
  - **Taushetserklæring** og **publiseringsavtale** — sjekk innleveringskrav, ikke utfylt.
  - **Antall ord** og **endelig dato** i forsidedata oppdateres ved innlevering.
  - **KI-erklæring** v1.1 oppdatert med 28 nye loggføringer (commit a7f24f5).
  - **HiMolde KI-skjema** utfylt og arkivert i `005 report/`.
- Rapportfrist 31. mai 2026 (**18 dager igjen**). Muntlig eksamen tidlig juni.

## Faktisk fremdrift

| Leveranse | Planlagt | Faktisk status | Kommentar |
|---|---|---|---|
| L7 Rapportskjelett + intro v1 | Uke 12 | Ferdig 09.03 | Skjelett v0.1, kapittelstruktur etablert |
| L8 Datainnhenting | Uke 12 | Ferdig mars 2026 | BRIS 2025, MOB 2022–2025, ROS/beredskapsanalyse inne |
| L8b ROS-gjennomgang | Uke 12–13 | Ferdig | Beredskapsanalyse og ROS gjennomgått, brukt i kap 4 og 6 |
| L8c EDA | Uke 12–13 | Ferdig | Døgnprofil, hendelsestyper, bindingstidsfordeling dokumentert |
| L8d Nasjonal DSB 2025-oversikt | Uke 15–16 | Ferdig 18.04 | 508 228 oppdrag, 12 sentraler, 7 figurer |
| L9 Parameterestimering | Uke 13 | Ferdig | λ per skifttype fra BRIS, μ fra operative samtaler (3,44 min) |
| L10 Kapasitetsmodellering (Erlang-C + prosedyrbasert) | Uke 14 | Ferdig | ρ < 6 % — beholdt som grunnlinje. Primærmodell prosedyrbasert |
| L11 Modellvalidering | Uke 14–15 | Ferdig | Bindingstid fra BRIS (median 13,0 min), VL-validering ferdig |
| L11b Sensitivitets- og scenarioanalyse | Uke 15 | Ferdig | +1 operatør, dimensjoneringskurve, variant A/B |
| L12 Teorikapittel | Uke 14–15 | Ferdig 19.04 | Kap 3 v1.1: Erlang-C, QED/square-root staffing, multiserver-jobs, op-binder-semantikk |
| L13 Benchmarking | Uke 15 | Ferdig | Alle 12 sentraler, MOB 2022–2025, figurer generert |
| L13b LABA Sør-Vest dybdeanalyse n=50 | Uke 16 | Ferdig 19.04 | 50 hendelser utfylt. Mean 5,88 min (n=30 Kilde=Alarm-subset). Drev V3-regelutvidelse |
| L13c LABA utvalg n=100 | Uke 16 | Ferdig 22.04 | Mean 4,53 min, CI [3,74; 5,43]. Hovedparameter justert 6 → 4,5 min |
| L14 Generaliseringsanalyse | Uke 15–16 | Ferdig | Omtalt i kap 7.9–7.10 og kap 8.3 (etter revisjon 2 reformulert som hypoteser) |
| L14b Nasjonal 2025-analyse per sentral | Uke 16 | Ferdig 18.04 | `nasjonal_2025_analyse.py`, 3 figurer + D-pri1/D-aba-splitt nasjonalt |
| L15 Resultater og diskusjon | Uke 16 | Ferdig 19.04 (rev 2: 13.05) | Kap 7 og 8 oppdatert med V3-tall. Revisjon 2 la til scenariobånd og balansert diskusjon |
| L15b Kap 1 Innledning | Uke 16 | Ferdig 19.04 (rev 2: 13.05) | Bakgrunn, kunnskapsgap, RQ1–RQ5, avgrensninger. Strammet ~30 % i revisjon 2. Forkortelsesliste 1.4.2 lagt til |
| L15c Kap 9 Konklusjon | Uke 16 | Ferdig 19.04 (rev 2: 13.05) | Svar på problemstilling + RQ1–RQ5. Nedtoning i 9.1/9.5 i revisjon 2 |
| L17 Spørreskjemaer — intern kalibrering | Uke 16 | Pågår | Skjema utviklet for alle 12 sentraler. Lokal kalibrering. Ingen skjema sendt eksternt — innenfor scope-vurdering for innlevering |
| L18 DSB-ønskeliste BRIS-datauttrekk | Uke 16 | Ferdig 18.04 | 22 prioriterte datapunkter |
| L19 V3-regelutvidelse (Kilde=Alarm) | Uke 16 | Ferdig 19.04 | Alle 5 skript oppdatert. 2 065 oppdrag flyttet L-aba → L-hendelse |
| L20 V3 op-binder-semantikk + D-pri1/D-aba-splitt | Uke 16 | Ferdig 19.04 | D-pri1 (2 ops, makkerpar), D-aba (Fase 1 + Fase 2, serial). Natt/helg Svikt 26 → 33 % |
| L16 Hoved-utkast + peer review | Slutten av april | Levert 27.04, peer review mottatt 03.05 | Innkommende peer review fra G21 gap-analysert (peer_review_G21_mottatt_analyse.md) |
| **L21 Revisjon 2 etter peer review (NY)** | Uke 19 | **Ferdig 13.05** | Commit a7f24f5: P1.1–P1.4, P2.A–P2.C, P3.1–P3.2. Admin: KI-erklæring v1.1, HiMolde-skjema utfylt, forsidedata, PDF rebygget |
| **L22 Bootstrap-CI for D-pri1 + skarpere 9.1 (NY)** | Uke 20 | **Ferdig 15.05** | Branch `bootstrap-dpri1-konfidensintervall`. 1000 iterasjoner, MAR-sjekk, ny 7.7.4, oppdatert 5.6.2 og 6.7. Kap 9.1 fikk direkte ettsetnings-svar på problemstillingen. Kap 3 fikk intro-setning som rammer Erlang-C som spesialtilfelle |

## Rapportstatus

| Kapittel | Fil | Status | Kommentar |
|---|---|---|---|
| Forside + sammendrag | _forside_og_kap1.md | Ferdig v1.2 (13.05) | Forsidedata komplett (veileder placeholder). YAML-frontmatter med tittel, abstract 350 ord |
| 1 Innledning | _forside_og_kap1.md | Ferdig v1.2 (13.05) | Strammet ~30 % i revisjon 2. RQ1–RQ5, forkortelsesliste 1.4.2 lagt til, avgrensninger, struktur |
| 2 Litteratur | kap2_litteratur.md | Ferdig v1.3 (13.05) | Mer analytisk (revisjon 2): per-kilde-begrensninger, kritisk kildevurdering, bro til metodevalg |
| 3 Teori | kap3_teori.md | Ferdig v1.2 (13.05) | Op-binder-semantikk klargjort. Språkrevisjon (revisjon 2): kortere setninger |
| 4 Casebeskrivelse | kap4_casebeskrivelse.md | Ferdig v1.3 (21.04) | VL-forutsetning henviser til VL_validering_bindingstider.md. **Ikke språkrevidert** |
| 5 Metode og data | kap5_metode_data.md | Ferdig v3.3 (13.05) | LABA n=100-statistikk. Språkrevisjon i revisjon 2. Refleksivitet/insider-bias |
| 6 Modell | kap6_modell.md | Ferdig v3.4 (13.05) | Op-binder-semantikk, D-pri1/D-aba-splitt. Konsekvens-vurdering for A1–A8 i Tabell 6.3 (revisjon 2) |
| 7 Analyse og resultater | kap7_analyse_resultater.md | Ferdig v2.2 (13.05) | Scenariobånd integrert i 7.5–7.7 og 7.11 (revisjon 2). Hva modellen måler tydelig i 7.5-intro. RQ4 og RQ5 dekket |
| 8 Diskusjon | kap8_diskusjon.md | Ferdig v1.3 (13.05) | Balansert diskusjon i 8.1–8.3 (nytt 8.2.3, alternative tolkninger, Erlang-C mindre kategorisk) |
| 9 Konklusjon | kap9_konklusjon.md | Ferdig v1.2 (13.05) | Generaliseringsnedtoning i 9.1 og 9.5 (revisjon 2). Eksplisitt single-case-omfang |
| Referanser | _referanser_og_vedlegg.md | Ferdig v1.1 (13.05) | APA-referanser utvidet og verifisert mot LOG650Vault (Zeltyn & Mandelbaum 2005, McNamee 2024, Storesund m.fl. 2017) |
| Vedlegg A–G | _referanser_og_vedlegg.md | Ferdig v1.0 (22.04) | A: skript. B: Spørreskjema. C: DSB-ønskeliste. D: KI-erklæring. E: LABA. F: VL-validering. G: Prosjektdokumentasjon |
| Samlet rapport-PDF | Rapport_LOG650_G20_Rune_110_samlet.pdf | Bygget v1.2 (13.05) | 808 930 bytes etter revisjon 2. Genereres via `verktoy/build_pdf.py` |

## Analyseartefakter

| Område | Skript | Figurer | Status |
|---|---|---|---|
| V3 Primærmodell + Variant B | konflikt_total_belastning.py | total_belastning_A_vs_B.png, total_belastning_sensitivitet.png | Fullført 19.04 |
| Bindingstidsanalyse | bindingstid_analyse.py | 4 figurer | Fullført |
| Benchmarking (2022–2025) | benchmark_trend_analyse.py | 3 figurer | Fullført |
| Scenarioanalyse (+1 op) V3 | scenario_pluss1.py | scenario_pluss1_operator.png | Fullført 19.04 |
| Kapasitetsfigurer | kapasitet_figurer.py | Diverse | Fullført |
| Nasjonal DSB 2025 | nasjonal_oversikt.py | nasjonal_oversikt_*.png (7 stk) | Fullført |
| Nasjonal 2025 per sentral | nasjonal_2025_analyse.py | nasjonal_2025_*.png (3 stk) | Fullført, D-pri1/D-aba-splitt nasjonalt 21.04 |
| LABA dybdeanalyse n=50 | uttrekk_laba_sorvest.py | laba_sorvest_2025_dybdeanalyse.xlsx | Fullført |
| LABA dybdeanalyse n=100 | uttrekk_laba_sorvest.py | laba_sorvest_2025_dybdeanalyse_n100-ferdig utfylt.xlsx | Ferdig 22.04: mean 4,53 min, CI [3,74; 5,43] |
| Spørreskjemageneratør | generer_skjema.py, md_til_pdf.py | 12 md-skjemaer + 12 AcroForm-PDFer | Klare — i intern kalibrering |
| Sporbarhets-notat | analyse/notat_V3_modellutvikling.md | — | Fullført 19.04 |
| PDF-pipeline | verktoy/build_pdf.py + dokument-header.tex | Pandoc + XeLaTeX | Etablert 21.04 (Python 3.10-syntaksfiks 13.05) |
| **Bootstrap-CI D-pri1 + MAR-sjekk** | bootstrap_dpri1.py | bootstrap_dpri1_ci.png | **Ferdig 15.05**: B=1000, 95 % CI Svikt natt/helg [32,1; 33,2] % |

## Milepæler

| ID | Milepæl | Planlagt | Faktisk | Vurdering |
|---|---|---|---|---|
| M1 | Godkjent proposal | 15. mars 2026 | Godkjent 7. mars | Ingen avvik |
| M2 | Godkjent prosjektplan | 15. mars 2026 | Godkjent 13. mars | Ingen avvik |
| M3 | Rapportskjelett klar | 22. mars 2026 | Ferdig 9. mars | Foran plan |
| M4 | Data innhentet og EDA ferdig | 29. mars 2026 | Ferdig mars 2026 | På plan |
| M5 | Kapasitetsmodell implementert og validert | 10. april 2026 | Ferdig 5. april | Foran plan |
| M6 | Hoved-utkast + peer review | Slutten av april / 27.04 | Levert 27.04, mottatt G21 03.05 | Ingen avvik |
| M6b | Revisjon 2 etter peer review (NY) | 13.–18. mai | **Ferdig 13.05** | Hovedrevisjon ferdig. Gjenstår språkrunde og admin |
| M7 | Endelig rapport + muntlig | 31. mai / juni | Planlagt | 18 dager igjen |

## Avvik mellom plan og faktisk

1. **Modellendring (fra v1.1):** Planen forutsatte Erlang-C som primærmodell. Analysen avdekket at Erlang-C er metodisk utilstrekkelig for 110-konteksten. Primærmodell er nå V3 prosedyrbasert ankomstkonfliktmodell med op-binder-semantikk. Erlang-C beholdes som grunnlinje.
2. **Sekvensgapmetode (fra v2.0):** Identifisering av sammenstilte anrop via sekvensgap i 110_ID var ikke planlagt. Gir 18 901 estimerte tilleggsanrop (korreksjonsfaktor 1,305×).
3. **D-pri1/D-aba-splitt (19.04):** Operativ innsikt avdekket at ABA-utrykning har fundamentalt annen dynamikk enn pri-1-hendelser. Modellen differensierer nå makkerpar-bundet D-pri1 (2 ops) fra serial D-aba (1 op + valgfri Fase 2).
4. **LABA to-trinns kalibrering (22.04):** Ikke planlagt opprinnelig. Runde 1 (n=49 / n=30 Kilde=Alarm) ga orienteringsanslag 5,88 min. Runde 2 (n=100, alle Kilde=Alarm) gir empirisk hovedparameter 4,53 min ([3,74; 5,43]).
5. **Nye arbeidspakker:** L8d, L13b, L13c, L14b, L17, L18, L19, L20, L21 + PDF-pipeline er lagt til siden v2.0 som respons på empirisk validering, nasjonal generaliseringsambisjon, operativ innsikt, leveranseformat (PDF) og peer review-revisjon.
6. **Skjelett-fil ikke synkronisert (avklart 22.04):** Ny pipeline bruker `_forside_og_kap1.md` + kapittelfilene + `_referanser_og_vedlegg.md` direkte. Skjelett-filen `Rapport_LOG650_G20_Rune_110_v0.1.md` er beholdt som arkiv.

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
| Spørreskjemaer til alle 12 sentraler | Utviklet — i intern kalibrering. Ingen sendt eksternt |
| LABA dybdeanalyse 50 hendelser (110 Sør-Vest 2025) | Utfylt — mean 5,88 min (n=30 Kilde=Alarm). Drev V3-regel |
| LABA dybdeanalyse 100 hendelser (110 Sør-Vest 2025) | Ferdig 22.04 — mean 4,53 min, CI [3,74; 5,43], median 3,27 min, P90 9,48 min |
| DSB-ønskeliste BRIS-datauttrekk | Ferdig — kan sendes til DSB |
| Datadelingsvurdering fra DSB | E-post sendt 5. april — avventer (ikke kritisk: peer review er gjennomført) |

## Intervju- og kontaktlogg

| Dato | Sentral/kontakt | Form | Tema |
|---|---|---|---|
| 15.03.2026 | Midt-Norge 110 | Telefon (uformell) | Bemanning, servicetesting-organisering |
| Mars–april 2026 | 110 Sør-Vest | Løpende operativ dialog | Makkerpar, bindingstider, VL-rolle |
| 13.03–25.03.2026 | Vidar Falkenberg, DSB | E-post | Datatilgang, henvendelsesdata, initiell hendelsestype |
| 05.04.2026 | bris-support@dsb.no | E-post | Datadelingsvurdering for peer review |
| April 2026 | Lokale operatører 110 Sør-Vest | Intern kalibrering | Spørreskjema-utforming, LABA-dybdeanalyse n=50, tidsestimat-validering |
| 20.04.2026 | Lokal operatør 110 Sør-Vest | LABA-dybdeanalyse utvidet | n=100-utvalg sendt til utfylling for smalere CI |
| 22.04.2026 | Lokal operatør 110 Sør-Vest | LABA n=100 returnert | Mean 4,53 min med strammere CI. Hovedparameter justert |
| 27.04.2026 | G21 (Orlien/Floden) | Sendt rapport til G21 | Utgående peer review-leveranse |
| 02.05.2026 | G21 (Odfjell-bunkring) | Levert peer review til G21 | Utgående: 4-siders peer review-rapport |
| 03.05.2026 | G21 (Orlien/Floden) | Mottatt peer review fra G21 | Innkommende: 4-siders vurdering. Hovedkritikk: usikkerhet, generalisering, språk |

## Risikoregister

| ID | Risiko | Status | Vurdering |
|---|---|---|---|
| R1 | BRIS-datakvalitet utilstrekkelig | Håndtert | Datakvalitet dokumentert i kap 5. Operatør-ID strukturelt fraværende — håndtert |
| R2 | Erlang-C-forutsetninger brytes | Håndtert | Erlang-C degradert til grunnlinje. Primærmodell prosedyrbasert |
| R3 | Ring-flom forstyrrer Poisson | Delvis håndtert | Sekvensgapmetoden fanger sammenstilte anrop |
| R4 | VL-antagelse holder ikke | Lukket | Bekreftet gjennom prosedyre og VL-validering |
| R5 | Benchmarking vanskelig pga. heterogen bemanning | Håndtert | MOB-data, L8d/L14b styrker nasjonal dokumentasjon |
| R6 | Tilgang til tvers-sentraldata | Lukket 10.03 | LEO felles fra høst 2024, tilgang bekreftet |
| R7 | Tidskollisjon med vaktarbeid | Åpen | Buffer i Gantt — håndterbart |
| R8 | Prokrastinering mot frist | Sterkt redusert | Alle hovedkapitler ferdig og revisjon 2 gjennomført 13.05. Gjenstår: språkrunde + admin. 18 dager til innlevering |
| R9 | Sensitive funn fra ROS-gjennomgang | Håndtert | Framing-retningslinje etablert: supplere, ikke angripe |
| R10 | Datadeling for peer review uavklart | Lukket (irrelevant) | Peer review gjennomført uten datadeling fra DSB |
| R11 | Skjema til andre sentraler ikke sendt | Lukket (utenfor scope) | Innenfor scope for innlevering — nasjonal del dekkes av DSB-data |
| R12 | L-aba-klassifisering nasjonalt heterogen | Håndtert | Adressert i kap 8.3 som begrensning ved nasjonal benchmarking |
| R13 | Generaliseringstone for sterk | Håndtert (rev 2 13.05) | Kap 7.9–7.10 og 9.1/9.5 reformulert som hypoteser/forutsetninger |
| R14 | Usikkerhet ikke integrert i resultater | Håndtert (rev 2 13.05 + bootstrap 15.05) | Scenariobånd 28–39 % integrert i kap 7.5–7.7 og 7.11. Bootstrap-CI for Svikt natt/helg [32,1; 33,2] % i 7.7.4 |
| R15 | Språklig kompleksitet | Stort sett håndtert | Kap 1, 2, 3, 5 språkrevidert + forkortelsesliste 1.4.2. Kap 4, 7, 8 har punktrevisjoner. Gjenstår: full setning-for-setning-gjennomgang av kap 4, 7, 8, 9 — naturlig del av brukerens final-read |
| **R16** | **Adminstrative skjema ikke utfylt (NY)** | Åpen | Taushetserklæring og publiseringsavtale: status uavklart. Veileder, antall ord, endelig dato i forside må fylles inn ved innlevering |

## Neste steg (18 dager til innlevering 31. mai)

### Gjenstående fra peer review-revisjonen

1. **Full språkrunde på resterende kapitler** (kap 4, 7, 8, 9): Kap 1, 2, 3, 5 er revidert. Kap 4, 7, 8 har fått punktrevisjoner på de lengste setningene, men ikke en fullstendig setning-for-setning-gjennomgang. Mål: gjennomsnittlig setningslengde under 25 ord, korte sammensatte setninger. [G21-punkt 7.A]
2. **Figur/tabell-integrering, finsjekk**: Kap 4 Tabell 4.1 har fått intro. Kap 7 og 8 er allerede stort sett tilfredsstillende. En finsjekk av om alle figurer/tabeller har eksplisitte intro-setninger som forklarer *hva leseren skal se* kan gjøres som del av brukerens gjennomlesning. [G21-punkt 7.D]

### Administrativt

7. **Veileder fylles inn** i forsidedata (placeholder per 13.05).
8. **Taushetserklæring**: avklar krav, fyll ut HiMolde-mal hvis nødvendig.
9. **Publiseringsavtale**: avklar krav.
10. **Antall ord og endelig dato** oppdateres i forsidedata ved innlevering.

### Sluttproduksjon

11. **Korrekturlesing** av hele rapporten etter språkrunden.
12. **Final PDF-rebuild** via `verktoy/build_pdf.py` etter siste tekstendringer.
13. **Innlevering 31. mai** + forberedelse til muntlig eksamen tidlig juni.

### Valgfritt (fra selvevaluering 1. mai, ikke G21-prioritert)

- Konsolidering av overlapp mellom kap 4.2.2 / 6.4.4 / 7.4.2 (makkerpar-tidslinjen)
- Konsolidering av klassifisering mellom 5.3.2 / 6.2 / 7.4.1
- Egen underseksjon 8.3.6 «To ulike kapasitetsproblem»
- Variant A oppsplittet per skifttype
