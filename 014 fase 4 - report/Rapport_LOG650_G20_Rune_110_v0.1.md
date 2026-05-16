# Rapport: masterfil

**Tittel:** Kapasitetsstyring og bemanningsdimensjonering ved norske 110-sentraler. En analyse av operatørkapasitet med prosedyrbasert ankomstkonfliktmodell

**Emne:** LOG650 Logistikk og kunstig intelligens, Høgskolen i Molde, Vår 2026
**Student:** Rune Grødem (G20 individuell)
**Status:** Revidert Markdown-grunnlag for peer review (mai 2026)

---

## Hva er denne filen?

Dette er en oversiktsfil for rapporten. Den **inneholder ikke selve rapportteksten**. Innholdet er splittet i kapittelfiler som bygges sammen til en samlet PDF via `verktoy/build_pdf.py --rapport-full`.

Bruk denne filen til å finne riktig kapittel raskt, og til å se hvilken versjon hvert kapittel ligger på.

## Kapittelstruktur og pekere

| # | Kapittel | Fil | Versjon |
|---|---|---|---|
| Forside + 1 | Sammendrag, innledning, problemstilling | [`_forside_og_kap1.md`](_forside_og_kap1.md) | Peer review-utkast |
| 2 | Litteratur | [`kap2_litteratur.md`](kap2_litteratur.md) | v1.1 |
| 3 | Teori | [`kap3_teori.md`](kap3_teori.md) | v3.x |
| 4 | Casebeskrivelse: 110 Sør-Vest | [`kap4_casebeskrivelse.md`](kap4_casebeskrivelse.md) | v1.x |
| 5 | Metode og data | [`kap5_metode_data.md`](kap5_metode_data.md) | v3.x (LABA n=100) |
| 6 | Modell | [`kap6_modell.md`](kap6_modell.md) | v3.x (op-binder) |
| 7 | Analyse | [`kap7_analyse.md`](kap7_analyse.md) | v3.x (analyserammen 7.1–7.4) |
| 8 | Resultat | [`kap8_resultat.md`](kap8_resultat.md) | v1.x (variant A/B, scenario +1, bootstrap) |
| 9 | Diskusjon | [`kap9_diskusjon.md`](kap9_diskusjon.md) | v1.x |
| 10 | Konklusjon | [`kap10_konklusjon.md`](kap10_konklusjon.md) | v1.x |
| 11–12 | Referanser og vedlegg | [`_referanser_og_vedlegg.md`](_referanser_og_vedlegg.md) | Peer review-utkast |

## Bygging av samlet PDF

```
py verktoy/build_pdf.py --rapport-full
```

Output legges i `005 report/Rapport_LOG650_G20_Rune_110_samlet.pdf`. Pipelinen forbehandler emojier og HTML-figurblokker, kjører Pandoc + XeLaTeX og inkluderer ToC.

## Sentrale forskningsspørsmål

- **RQ1:** Ankomstrate og belastningsmønstre per skiftperiode
- **RQ2:** Håndteringstid og kapasitetsbinding utover samtaletid
- **RQ3:** Andel beredskapsanrop i brudd-/svikt-tilstand, strukturelt hverdag/helg-gap
- **RQ4:** ROS-/beredskapsanalysens metodiske grunnlag for bemanningsbeslutning
- **RQ5:** Strukturelle prediktorer som grunnlag for nasjonal dimensjoneringsmodell

## Hovedfunn (110 Sør-Vest 2025)

- 32,6 % av beredskapsanropene på natt/helg ankommer i svikt-tilstand (variant A); 33,2 % ved total operativ belastning (variant B)
- Erlang-C-grunnlinjen gir ρ ≤ 5,9 % for alle skifttyper, formelt korrekt, men metodisk utilstrekkelig
- Scenario «+1 operatør natt/helg» halverer sviktraten (ca. 33 % til 16,7 %)
- L-aba-bindingstid empirisk kalibrert til 4,53 min (n=100, 95 % CI [3,74; 5,43])

## Tilstøtende dokumenter

| Fil | Innhold |
|---|---|
| V3-arkivnotat | Lukket beslutningsgrunnlag for V3-klassifiseringsregelen |
| `VL_validering_bindingstider.md` | Empirisk validering av c_eff = c_total − 1 |
| Vurderingslogg | Avsluttet vurderingslogg for V1-V3 og rapportavgrensninger |
| `../012 fase 2 - plan/status.md` | Statuslogg for hele Fase 3-arbeidet |

---

*Dokumentstatus per 2026-05-01: Markdown-kildene er gjennomgått for peer review.*
