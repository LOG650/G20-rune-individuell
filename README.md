# LOG650 — G20 Rune Grødem

**Prosjekttittel:** Kapasitetsstyring og bemanningsdimensjonering ved norske 110-sentraler
**Emne:** LOG650 Logistikk og kunstig intelligens, Høgskolen i Molde, Vår 2026
**Student:** Rune Grødem, G20 Individuell

---

## Problemstilling

> *I hvilken grad samsvarer faktisk bemanning ved norske 110-sentraler med kapasitetsbehovet beregnet fra historiske hendelsesdata og køteoretiske modeller?*

Prosjektet har en **dobbel ambisjon:**

1. **Casestudie (110 Sør-Vest):** Dokumentere i hvilken grad faktisk bemanning samsvarer med kapasitetsbehovet beregnet fra historiske LEO/BRIS-data og en Erlang-C kømodell
2. **Generaliseringsambisjon:** Undersøke om strukturelle prediktorer (hendelsesvolum, innbyggertall, areal) kan danne grunnlag for en nasjonal, etterprøvbar dimensjoneringsmodell for 110-operatører — analogt med dimensjoneringsforskriften (FOR-2023-01-06-23) for brannvesenet

---

## Primærmodell

**Erlang-C (M/M/c)** — fler-server kømodell kalibrert mot historiske hendelsesdata fra LEO/BRIS.

Nøkkelantagelse: Vaktleder (VL) besvarer normalt ikke nødanrop, noe som gir effektiv operatørkapasitet `c_effektiv = c_total − 1`.

| Skift | Bemanning | c_effektiv |
|---|---|---|
| Dag (07:00–19:00) | 3 operatører + VL | 3 |
| Natt/helg (19:00–07:00) | 2 operatører + VL | 2 |

---

## Prosjektstatus

| Fase | Beskrivelse | Frist | Status |
|---|---|---|---|
| **Fase 1** | Proposal | 15. mars 2026 | Innlevert 7. mars — avventer godkjenning |
| **Fase 2** | Prosjektstyringsplan + Gantt | 15. mars 2026 | Innlevert 11. mars — avventer godkjenning |
| **Fase 3** | Gjennomføring (EDA, modell, rapport) | Slutten av april 2026 | Starter uke 12 |
| **Fase 4** | Sluttrapport + muntlig eksamen | 31. mai / tidlig juni 2026 | Ikke startet |

**Karakterkrav:** C-nivå på arbeidskrav (fase 1–3), B-krav på sluttrapport + muntlig eksamen.

---

## Sentrale dokumenter

| Dokument | Fil |
|---|---|
| Prosjektstyringsplan v1.8 | [012 fase 2 - plan/Prosjektstyringsplan_G20_Rune_110.md](012%20fase%202%20-%20plan/Prosjektstyringsplan_G20_Rune_110.md) |
| Gantt-diagram (MS Project) | [012 fase 2 - plan/Gantt_LOG650_G20_Rune_110.mpp](012%20fase%202%20-%20plan/Gantt_LOG650_G20_Rune_110.mpp) |
| Gantt-diagram (XML-eksport) | [012 fase 2 - plan/Gantt_LOG650_G20_Rune_110.xml](012%20fase%202%20-%20plan/Gantt_LOG650_G20_Rune_110.xml) |
| Litteraturliste (26 kilder) | [012 fase 2 - plan/Litteraturliste_LOG650_G20_Rune.xlsx](012%20fase%202%20-%20plan/Litteraturliste_LOG650_G20_Rune.xlsx) |
| Proposal v3 | [011 fase 1 - proposal/Proposal_LOG650_G20_Rune_110_v3.md](011%20fase%201%20-%20proposal/Proposal_LOG650_G20_Rune_110_v3.md) |
| Rapportskjelett v0.1 | [014 fase 4 - report/Rapport_LOG650_G20_Rune_110_v0.1.md](014%20fase%204%20-%20report/Rapport_LOG650_G20_Rune_110_v0.1.md) |
| KI-erklæring og brukslogg | [KI_erklæring_LOG650_G20_Rune.md](KI_erklæring_LOG650_G20_Rune.md) |

---

## Datakilder

| Kilde | Innhold | Status |
|---|---|---|
| LEO/BRIS 2020–2025 (110 Sør-Vest) | Hendelsestidsstempler, oppdragstype, varighet | Tilgjengelig |
| LEO post-2024 (alle sentraler) | Sammenlignbare data — felles LEO-format | Tilgjengelig (bekreftet 10.03) |
| DSB årsrapporter 2025 | Bemanning, anropsvolum alle sentraler | Offentlig |
| SSB befolkningsdata | Innbyggertall per dekningsområde | Offentlig |
| ROS/beredskapsanalyse 110 Sør-Vest | Dimensjoneringsgrunnlag | Tilgjengelig |

> **Merk:** Rådata er gitignored og lagres utelukkende lokalt i `004 data/`. Ingen operasjonelle data fra 110 Sør-Vest er lastet opp til GitHub.

---

## Mappestruktur

```
000 templates/              Maler og referansestiler fra HiMolde
001 info/                   Kursinformasjon og generelle notater
002 meetings/               Møtereferater og korrespondanse
003 references/             Litteratur (PDF-artikler)
004 data/                   Rådata (gitignored — lagres kun lokalt)
011 fase 1 - proposal/      Godkjent proposal
012 fase 2 - plan/          Prosjektstyringsplan og Gantt-diagram
013 fase 3 - review/        Peer review-dokumenter
014 fase 4 - report/        Rapport (hovedleveranse)
analyse/notebooks/          Jupyter notebooks (EDA, modellering)
analyse/scripts/            Python-scripts
figurer/                    Genererte figurer til rapporten
KI_erklæring_LOG650_G20_Rune.md   Brukslogg og erklæring for KI-verktøy
```

---

## Teknisk stack

- **Analyse:** Python (pandas, numpy, scipy, statsmodels)
- **Visualisering:** matplotlib, seaborn
- **Notatbok:** Jupyter Notebooks
- **Prosjektstyring:** MS Project (Gantt med referanseplan/baseline)
- **Versjonskontroll:** Git / GitHub
- **KI-verktøy:** Claude Code (Anthropic), ChatGPT (OpenAI) — se KI-erklæring

---

*Opprettet: 2026-03-06 | Sist oppdatert: 2026-03-12*
