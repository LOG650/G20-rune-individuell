# Prosjektstatus — LOG650 G20 Rune Grødem
**Oppdatert:** 2026-03-17
**Prosjekt:** Kapasitetsstyring og bemanningsdimensjonering ved norske 110-sentraler

---

## Milepæler

| ID | Milepæl | Frist | Status |
|---|---|---|---|
| M1 | Godkjent proposal | 15. mars 2026 | GODKJENT |
| M2 | Godkjent prosjektplan + Gantt med referanseplan | 15. mars 2026 | GODKJENT 13. mars 2026 |
| M3 | Rapportskjelett + introduksjon v1 klar | 22. mars 2026 | FULLFORT (L7 fullfort, v0.2, 09.03) |
| M4 | Data innhentet, validert og EDA ferdig | 29. mars 2026 | Ikke startet |
| M5 | Erlang-C modell implementert og validert | 10. april 2026 | Ikke startet |
| M6 | Godkjent hoved-utkast + peer review gjennomført | Slutten av april 2026 | Ikke startet |
| M7 | Ferdigstilt rapport innlevert + muntlig eksamen | Rapport: 31. mai / Muntlig: tidlig juni | Ikke startet |

---

## Leveranser per fase

### Fase 1 — Initiering (fullført)

| ID | Leveranse | Frist | Status |
|---|---|---|---|
| L0 | Proposal levert | 7. mars 2026 | FULLFORT |

### Fase 2 — Planlegging (fullfort)

| ID | Leveranse | Frist | Status |
|---|---|---|---|
| L1 | Avklart problemstilling + mål + avgrensninger | 7. mars | FULLFORT |
| L2 | Modellvalg — Erlang-C (M/M/c) identifisert og begrunnet | 7. mars | FULLFORT |
| L3 | Litteratursøk — planlegging (søkeord, databaser, avgrensning) | 10. mars | FULLFORT |
| L4 | Dataplan — datakilder, variabler, kvalitet, tilgangsstatus | 10. mars | FULLFORT |
| L5 | Godkjent prosjektstyringsplan | 15. mars | GODKJENT 13. mars 2026 |
| L6 | MS Project Gantt-diagram med referanseplan (baseline) | 15. mars | FULLFORT |

### Fase 3 — Gjennomføring (starter uke 12, 17. mars 2026)

| ID | Leveranse | Uke / Frist | Status |
|---|---|---|---|
| L7 | Rapportskjelett + introduksjon og problemstilling v1 | Uke 12 | FULLFORT (v0.2, 09.03) |
| L8 | Datainnhenting — LEO/BRIS, DSB-årsrapporter, SSB | Uke 12 | Påbegynt (20%) — BRIS 110 SV 2025 + nasjonal BRIS 2025 + MOB 2018/2023/2024/2025 inne |
| L8b | ROS/beredskapsanalyse-gjennomgang — dokumentanalyse | Uke 12–13 | DATA INNE — `Beredskapsanalyse_110 Sør-Vest_J03.pdf` + `Overordnet risiko- og sårbarhetsanalyse 110 Sør-Vest_J05.pdf` + `Veiledning til forskrift.pdf` i 004 data/ |
| L8c | Eksplorativ dataanalyse (EDA) | Uke 12–13 | Ikke startet |
| L9 | Parameterestimering — λ og μ per skiftperiode | Uke 13 | Ikke startet |
| L10 | Erlang-C modellering med VL-korreksjon | Uke 14 | Ikke startet |
| L11 | Modellvalidering | Uke 14–15 | Ikke startet |
| L11b | Sensitivitetsanalyse | Uke 15 | Ikke startet |
| L12 | Teorikapittel | Uke 14–15 | Ikke startet |
| L13 | Benchmarking — alle 12 norske 110-sentraler | Uke 15 | Ikke startet |
| L14 | Generaliseringsanalyse | Uke 15–16 | Ikke startet |
| L15 | Resultater og diskusjon — rapportutkast | Uke 16 | Ikke startet |
| L16 | Godkjent hoved-utkast + peer review | Slutten av april | Ikke startet |

### Fase 4 — Avslutning

| ID | Leveranse | Frist | Status |
|---|---|---|---|
| L17 | Ferdigstilt rapport (inkl. kode på GitHub) | 31. mai 2026 | Ikke startet |
| L18 | Muntlig eksamen | Tidlig juni 2026 | Ikke startet |

---

## Risikoregister (aktive)

| ID | Risiko | Sannsynlighet | Konsekvens | Status |
|---|---|---|---|---|
| R1 | LEO/BRIS-datakvalitet utilstrekkelig | Middels | Høy | Åpen |
| R2 | Erlang-C-forutsetninger brytes empirisk | Middels | Middels | Åpen |
| R3 | Ring-flom forstyrrer Poisson-antagelse | Middels | Middels | Åpen |
| R4 | VL-antagelse holder ikke i praksis | Middels | Lav | Åpen |
| R5 | Benchmarking vanskelig pga. heterogen bemanning | Høy | Middels | Åpen |
| R6 | Tilgang til tvers-sentraldata (LEO post-2024) | — | — | LUKKET 10. mars 2026 |
| R7 | Tidskollisjon med vaktarbeid ved 110 Sør-Vest | Høy | Middels | Åpen |
| R8 | Prokrastinering — skippertak mot frist | Middels | Høy | Åpen |
| R9 | Sensitive funn fra ROS-gjennomgang | Middels | Middels | Åpen |

---

## Datagrunnlag

| Kilde | Status |
|---|---|
| BRIS fullrapport 110 Sør-Vest 2025 | INN — 004 data/ (hele 2025) |
| BRIS fullrapport nasjonal 2025 | INN — 004 data/ (alle sentraler, mangler opprinnelig oppdragstype) |
| BRIS fullrapport nasjonal 2023 og 2024 | INN — 004 data/ |
| BRIS fullrapport nasjonal 2018 | INN — 004 data/ (referanseår) |
| MOB-årsrapporter DSB 2022–2025 | INN — 004 data/ (bemanning + anropstall alle sentraler) |
| LEO/BRIS 110 Sør-Vest 2020–2024 | Tilgjengelig hos DSB — ikke hentet ennå |
| ROS/beredskapsanalyse 110 Sør-Vest | INN — `Beredskapsanalyse_110 Sør-Vest_J03.pdf` + `Overordnet risiko- og sårbarhetsanalyse 110 Sør-Vest_J05.pdf` |
| SSB befolkningsdata | Offentlig — ikke lastet ned ennå |
| Strukturerte intervjuer | Påbegynt — uformell telefonsamtale Midt-Norge 110 (15. mars) |
| Operatørdata fra BRIS (anonymisert) | IKKE MULIG — strukturell begrensning i BRIS, bekreftet |

**Merknad BRIS:** Sekundære anrop (ring-flom) og operatørbinding per samtale kan ikke
eksporteres fra LEO/BRIS. Modellen estimerer serverutnyttelse (ρ) indirekte via λ og μ.
Dokumenteres som strukturell databegrensning i avsnitt 1.4 (antakelser) og 5.1 (datakilder).

---

## Litteraturliste

34 kilder registrert og lastet ned (33 PDF + 1 nettside). Verifisert 17. mars 2026.

**Åpne punkter:**
- Nr 10 og 32 mulig duplikat (samme tittel, L'Ecuyer et al. 2018) — sjekk PDF-innhold
- Nr 22 og 23 har samme URL registrert — rett opp feil lenke for én av dem

---

## Intervjulogg

| Dato | Sentral | Form | Funn |
|---|---|---|---|
| 15. mars 2026 | Midt-Norge 110 | Telefonsamtale (uformell) | Minimum 3 operatører. 3 ekstra servicemedarbeidere (ABA-testing) utenfor LEO. Operatørene dekker service i helger/sykdom. |

**Neste intervjuer:** Strukturert spørreskjema utarbeides (se `002 meetings/intervjuguide_110-sentraler_UTKAST.md`)

---

## Neste steg

1. **Uke 12 (nå):** Start L8c — EDA på BRIS 110 SV 2025 (anropsvolum per time/dag, hendelsestyper, Poisson-test)
2. **Uke 12:** Hent inn BRIS 2020–2024 for 110 SV (lengre tidsserie)
3. **Uke 12–13:** Strukturerte intervjuer med vaktledere (μ-estimat T1, VL-praksis)
4. **Uke 13:** Parameterestimering λ og μ per skiftperiode (L9)

---

## Versjonshistorikk

| Versjon | Dato | Endring |
|---|---|---|
| 1.0 | 2026-03-13 | Opprettet ved godkjenning av fase 2 |
| 1.1 | 2026-03-17 | Datagrunnlag oppdatert (BRIS + MOB inne), litteraturliste ferdig (34 kilder), intervjulogg opprettet, BRIS-begrensning dokumentert |
