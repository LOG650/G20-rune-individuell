# Peer review-kriterier: revisjonslogg for rapporten

**Kilde:** `C:\Users\runeg\Downloads\veiledning peer-review LOG650.pdf`  
**Formål:** Dokumentere hvilke peer-review-risikoer som er rettet i rapportens Markdown-kilder.  
**Status etter revisjon 2026-05-01:** Kritiske formalia-, referanse- og konsistenspunkter er lukket i Markdown-kildene. PDF er ikke bygget på nytt i denne runden, i tråd med bestillingen.

## Kort helhetsdiagnose etter revisjon

Rapporten fremstår nå klarere for peer review. Hovedargumentet er fortsatt casestudien av 110 Sør-Vest, mens den nasjonale delen er tydeligere avgrenset som benchmarking og generaliseringsgrunnlag. De mest synlige kommentar-risikoene er ryddet: midlertidige arbeidsmerknader, dobbel figurnummerering, uklare tabellnumre, gamle kildehenvisninger, scenario-tallstøy og manglende referanser.

## Kriterier og gjennomførte rettinger

| Kriterieområde | Utført i Markdown-kildene |
|---|---|
| Innledning | Sammendrag og innledning presiserer casestudie/nasjonalt scope. RQ1-RQ5 er knyttet tydeligere til mangelen på kvantitativ dimensjoneringsstandard. |
| Litteratur og teori | Tidligere kildeavvik er ryddet, metodebro fra litteraturgap til modellvalg er styrket, og språkfeil i fler-/én-enhetsterminologi er korrigert. |
| Metode og data | Kryssreferanser til antagelsestabell er rettet, Tabell 6.3 er etablert, etikk/personvern er presisert, og valideringssamtaler er dokumentert som rolle-/tema-/datobasert støtte. |
| Analyse og resultater | Scenarioformuleringer bruker nå ca. 33 % -> 16,7 % i overordnede tekster, mens råtabeller beholder beregnede verdier. RQ-kobling er lagt inn. |
| Figurer og tabeller | Manuelle figurnumre er fjernet fra captiontekstene, Tabell 7.1-7.14 er sekvensialisert, og gamle 7.1b/7.3b-former er fjernet. |
| Diskusjon | Forventede/uventede funn er tydeligere merket, og implikasjoner er delt klarere i praksis, teori og policy. |
| Konklusjon | Scope er strammere, scenarioeffekten er harmonisert med kapittel 7, og anbefalingene er tydeligere knyttet til hva casen faktisk viser. |
| Referanser | Arbeidsmerknader er fjernet, manglende kilder er lagt til, og feil forskrifts-/rapportreferanser er korrigert. |

## Fil-for-fil status

| Fil | Status |
|---|---|
| `_forside_og_kap1.md` | Scope, sammendrag og scenarioformuleringer rettet. |
| `kap2_litteratur.md` | Arbeidslinjer fjernet, kildeomtaler og metodebro korrigert. |
| `kap3_teori.md` | Kildebruk og språkfeil rettet. |
| `kap4_casebeskrivelse.md` | Figurcaption og forskriftsreferanse korrigert. |
| `kap5_metode_data.md` | Kryssreferanser, etikk/personvern og dokumentasjon av validering presisert. |
| `kap6_modell.md` | Headingnivå, Tabell 6.3 og modellantagelser ryddet. |
| `kap7_analyse_resultater.md` | RQ-kobling, tabellsekvens, figurcaptioner og scenarioforklaring rettet. |
| `kap8_diskusjon.md` | Referansegrunnlag, forventede/uventede funn og implikasjoner styrket. |
| `kap9_konklusjon.md` | Tallkonsistens og nasjonalt scope harmonisert. |
| `_referanser_og_vedlegg.md` | Referanseliste ryddet og supplert. |
| `Rapport_LOG650_G20_Rune_110_v0.1.md` | Masterfil oppdatert med revidert status og lukket støttedokumentasjon. |
| `V3_oppstart_brief.md` | Konvertert til arkivnotat for lukket V3-beslutning. |
| Vurderingslogg for V1-V3 | Konvertert til lukket revisjonslogg. |

## Kontroll utført etter retting

| Kontroll | Resultat |
|---|---|
| Midlertidige markører i rapportmappen | Ingen treff i Markdown-kildene etter siste søk. |
| Gamle kildeavvik | Ingen treff på de identifiserte kilde- og forskriftsfeilene etter siste søk. |
| Tabellnummerering | Tabellene i kapittel 7 er sekvensielle fra 7.1 til 7.14. |
| Figurcaptioner | Manuelle `Figur x.y:`-prefikser er fjernet fra HTML-captiontekstene. |
| PDF-bygg | Ikke kjørt i denne runden etter eksplisitt bestilling. |

## Avgrenset til senere bygg

Når ny PDF skal produseres, bør selve PDF-en kontrolleres visuelt for paginering, innholdsfortegnelse, figurplassering og eventuelle Pandoc-/LaTeX-effekter. Dette er en PDF-layoutkontroll, ikke en gjenstående Markdown-retting.
