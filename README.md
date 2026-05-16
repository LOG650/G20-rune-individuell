# LOG650 — G20 Rune Grødem

**Prosjekttittel:** Kapasitetsstyring og bemanningsdimensjonering ved norske 110-sentraler
**Emne:** LOG650 Logistikk og kunstig intelligens, Høgskolen i Molde, Vår 2026
**Student:** Rune Grødem, G20 Individuell

---

## Problemstilling

> *I hvilken grad samsvarer faktisk bemanning ved norske 110-sentraler med kapasitetsbehovet beregnet fra historiske hendelsesdata og køteoretiske modeller?*

Prosjektet har en **dobbel ambisjon:**

1. **Casestudie (110 Sør-Vest):** Dokumentere i hvilken grad faktisk bemanning samsvarer med kapasitetsbehovet beregnet fra historiske LEO/BRIS-data og en prosedyrbasert kapasitetsmodell
2. **Generaliseringsambisjon:** Undersøke om strukturelle prediktorer (hendelsesvolum, innbyggertall, areal) kan danne grunnlag for en nasjonal, etterprøvbar dimensjoneringsmodell for 110-operatører — analogt med dimensjoneringsforskriften (FOR-2023-01-06-23) for brannvesenet

---

## Modell

**Primærmodell: Prosedyrbasert ankomstkonfliktmodell** — måler sannsynligheten for at et beredskapsanrop ankommer i en tilstand der makkerpar-driftsstandarden ikke kan opprettholdes.

**Grunnlinje: Erlang-C (M/M/c)** — tradisjonell køteoretisk referansemodell som viser begrensningene ved klassisk tilnærming i 110-kontekst.

Nøkkelantagelse: Vaktleder (VL) besvarer normalt ikke nødanrop, noe som gir effektiv operatørkapasitet `c_eff = c_total − 1`.

| Skifttype | Min. bemanning | c_eff |
|---|---|---|
| Dag hverdag (07:00–19:00) | 3 operatører + VL | 3 |
| Natt/helg (19:00–07:00) | 2 operatører + VL | 2 |

---

## Prosjektstatus

| Fase | Beskrivelse | Frist | Status |
|---|---|---|---|
| **Fase 1** | Proposal | 15. mars 2026 | Godkjent |
| **Fase 2** | Prosjektstyringsplan + Gantt | 15. mars 2026 | Godkjent |
| **Fase 3** | Gjennomføring (EDA, modell, rapport) | Slutten av april 2026 | Pågår |
| **Fase 4** | Sluttrapport + muntlig eksamen | 31. mai / tidlig juni 2026 | Pågår |

**Karakterkrav:** C-nivå på arbeidskrav (fase 1–3), B-krav på sluttrapport + muntlig eksamen.

---

## Rapportkapitler

| Kapittel | Fil | Status |
|---|---|---|
| 1. Forside og innledning | [_forside_og_kap1.md](014%20fase%204%20-%20report/_forside_og_kap1.md) | Peer review-utkast |
| 2. Litteratur | [kap2_litteratur.md](014%20fase%204%20-%20report/kap2_litteratur.md) | v1.1 |
| 3. Teori | [kap3_teori.md](014%20fase%204%20-%20report/kap3_teori.md) | v3.x |
| 4. Casebeskrivelse | [kap4_casebeskrivelse.md](014%20fase%204%20-%20report/kap4_casebeskrivelse.md) | v1.x |
| 5. Metode og data | [kap5_metode_data.md](014%20fase%204%20-%20report/kap5_metode_data.md) | v3.x |
| 6. Modell | [kap6_modell.md](014%20fase%204%20-%20report/kap6_modell.md) | v3.x |
| 7. Analyse | [kap7_analyse.md](014%20fase%204%20-%20report/kap7_analyse.md) | v3.x |
| 8. Resultat | [kap8_resultat.md](014%20fase%204%20-%20report/kap8_resultat.md) | v1.x |
| 9. Diskusjon | [kap9_diskusjon.md](014%20fase%204%20-%20report/kap9_diskusjon.md) | v1.x |
| 10. Konklusjon | [kap10_konklusjon.md](014%20fase%204%20-%20report/kap10_konklusjon.md) | v1.x |
| 11–12. Referanser og vedlegg | [_referanser_og_vedlegg.md](014%20fase%204%20-%20report/_referanser_og_vedlegg.md) | Peer review-utkast |
| Rapportoversikt | [Rapport_LOG650_G20_Rune_110_v0.1.md](014%20fase%204%20-%20report/Rapport_LOG650_G20_Rune_110_v0.1.md) | Pågår |

---

## Sentrale dokumenter

| Dokument | Fil |
|---|---|
| Proposal v3 (godkjent) | [011 fase 1 - proposal/Proposal_LOG650_G20_Rune_110_v3.md](011%20fase%201%20-%20proposal/Proposal_LOG650_G20_Rune_110_v3.md) |
| Prosjektstyringsplan | [012 fase 2 - plan/Prosjektstyringsplan_G20_Rune_110.md](012%20fase%202%20-%20plan/Prosjektstyringsplan_G20_Rune_110.md) |
| KI-erklæring og brukslogg | [KI_erklæring_LOG650_G20_Rune.md](KI_erklæring_LOG650_G20_Rune.md) |

---

## Datakilder

| Kilde | Innhold | Status |
|---|---|---|
| BRIS/LEO 2025 (110 Sør-Vest) | 61 964 hendelser, 44 kolonner — primærdata | Tilgjengelig |
| DSB MOB-rapporter 2022–2025 | Bemanning, anropsvolum alle 12 sentraler | Tilgjengelig |
| SSB befolkningsdata | Innbyggertall per dekningsområde | Offentlig |
| Prosedyre- og analysedokumenter | Arbeidsmetodikk, ROS, beredskapsanalyse | Intern tilgang |

> **Merk:** Rådata er gitignored og lagres utelukkende lokalt i `004 data/`. Ingen operasjonelle data er lastet opp til GitHub.

---

## Mappestruktur

```
001 info/                   Kursinformasjon og generelle notater
002 meetings/               Møtereferater og korrespondanse (gitignored)
003 references/             Litteratur (PDF-artikler)
004 data/                   Rådata (gitignored)
005 report/                 Rapport-output (figurer, tabeller)
011 fase 1 - proposal/      Godkjent proposal
012 fase 2 - plan/          Prosjektstyringsplan og Gantt-diagram
013 fase 3 - review/        Peer review-dokumenter
014 fase 4 - report/        Rapportkapitler (hovedleveranse)
analyse/scripts/            Python-analyseskript
analyse/figurer/            Genererte figurer
analyse/notebooks/          Jupyter notebooks
```

---

## Teknisk stack

- **Analyse:** Python (pandas, numpy, scipy)
- **Visualisering:** matplotlib, seaborn
- **Versjonskontroll:** Git / GitHub
- **KI-verktøy:** Claude Code (Anthropic), ChatGPT (OpenAI) — se KI-erklæring

---

*Opprettet: 2026-03-06 | Sist oppdatert: 2026-04-05*
