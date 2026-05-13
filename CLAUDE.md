# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# LOG650 – G20 Rune Grødem – Prosjektinstruksjoner for Claude

## Prosjektinfo
- **Student:** Rune Grødem, G20 Individuell
- **Emne:** LOG650 Logistikk og kunstig intelligens, Høgskolen i Molde, Vår 2026
- **Arbeidsform:** Individuelt
- **Fase nå:** Fase 3 – Gjennomføring (starter uke 12, 17. mars 2026)
- **Frist hoved-utkast:** Slutten av april 2026
- **Frist endelig rapport:** 31. mai 2026
- **Muntlig eksamen:** Tidlig juni 2026
- **Karakterkrav:** C-nivå på arbeidskrav, B-krav på rapport + muntlig

## Problemstilling
**I hvilken grad samsvarer faktisk bemanning ved norske 110-sentraler med kapasitetsbehovet
beregnet fra historiske hendelsesdata og køteoretiske modeller?**

## Dobbel ambisjon
1. **Casestudie (110 Sør-Vest):** Dokumentere om faktisk bemanning samsvarer med
   kapasitetsbehovet beregnet fra historiske LEO/BRIS-data og Erlang-C-modellen
2. **Generaliseringsambisjon:** Undersøke om strukturelle prediktorer (hendelsesvolum,
   innbyggertall, areal) kan danne grunnlag for en nasjonal, etterprøvbar
   dimensjoneringsmodell for 110-operatører — analogt med dimensjoneringsforskriften
   for brannvesenet

## Bakgrunn og motivasjon
Dimensjoneringsforskriften (FOR-2023-01-06-23) gir kvantitativ, etterprøvbar standard
for brannstasjoner basert på innbyggertall og responstid. **Ingen tilsvarende nasjonal
standard finnes for 110-operatører.** Bemanningsnivået fastsettes gjennom lokale
ROS- og beredskapsanalyser som er kvalitative og vanskelige å etterprøve kvantitativt
på tvers av sentraler. Prosjektets ambisjon er å bygge et kvantitativt referansepunkt
for 110-operatører analogt med dimensjoneringsforskriftens rolle for brannvesenet.

## Primærcase: 110 Sør-Vest
- **Skift:** Dag 07:00–19:00, Natt 19:00–07:00
- **Bemanning dag:** 3 operatører + Vaktleder (VL) = totalt 4. c_effektiv = 3
- **Bemanning natt/helg:** 2 operatører + Vaktleder = totalt 3. c_effektiv = 2
- **VL-antagelse:** Vaktleder besvarer normalt IKKE nødanrop → c_effektiv = c_total − 1
- **De facto servicegrense:** 10. anrop i kø → overføres til Agder; ubesvart etter 30 sek = automatisk overføring til Agder
- **Data tilgjengelig:** LEO/BRIS tilbake til 2020; felles LEO for alle sentraler fra høst 2024
- **ROS/beredskapsanalyse:** Tilgjengelig — forfatterens tilgang til dokumenter for 110 Sør-Vest

## Modellutvikling — tre faser
1. **Erlang-C (M/M/c)** — Grunnlinje. Ga ρ < 6 % for alle skifttyper. Formelt korrekt
   men metodisk utilstrekkelig: fanger ikke makkerpar-drift eller kapasitetsbinding.
2. **Simultanitetsanalyse** — Lav konfliktrate, makkerpar-logikk ikke fanget.
3. **Prosedyrbasert ankomstkonfliktmodell** (PRIMÆRMODELL) — Måler kapasitetstilstand
   ved hvert beredskapsanrops ankomsttidspunkt.

## Primærmodell: Prosedyrbasert ankomstkonfliktmodell
For hvert beredskapsanrop klassifiseres kapasitetsnivå basert på antall aktive
hendelser (n_aktive) ved ankomsttidspunktet. En hendelse er «aktiv» fra ankomst
til estimert bindingstid er utløpt (RØD-fase + GUL-fase).

### Tre operative nivåer
| Nivå | Tilstand | c_eff = 2 (natt/helg) | c_eff = 3 (dag) | Operativ konsekvens |
|---|---|---|---|---|
| **Normal** | Makkerpar mulig | n_aktive = 0 | n_aktive ≤ 1 | Full prosedyre, kvalitetssikret håndtering |
| **Degradert** | Solo-håndtering | n_aktive = 1 | n_aktive = 2 | Operatør klarer det, men uten makker. Økt kognitiv belastning, økt feilrisiko |
| **Svikt** | Ingen ledig operatør | n_aktive ≥ 2 | n_aktive ≥ 3 | VL må overta eller overløp til Agder |

### Operativ virkelighet: degradert drift er normaltilstand under press
Makkerpar er **prosedyrekrav** (driftsstandard), men i praksis opererer operatører
**ofte solo** fordi alternativet er å la innringer vente. Operatørene strekker seg
kontinuerlig for å hjelpe flest mulig. Kvaliteten går ned, men det blir som oftest
godt nok. Modellen kvantifiserer denne daglige tilpasningen — den gjør synlig noe
alle i bransjen vet, men ingen måler systematisk.

### Modellen som dimensjoneringsverktøy
Modellens praktiske verdi er at den kan brukes som kvantitativt input til
dimensjoneringsbeslutninger:
- **Input:** Hendelsesdata (BRIS/LEO) + ROS-parametre (bindingstider, skiftordning)
- **Output:** For et gitt bemanningsnivå c → andel anrop i Normal / Degradert / Svikt
- **Dimensjoneringsspørsmål:** «Hvor mange operatører trengs for at
  ≥ X % av beredskapsanropene håndteres med makkerpar (Normal)?»
- **Alternativt:** «Med hvilken bemanning holdes solo-andelen (Degradert) under Y %?»

Dette gir en kvantitativ, etterprøvbar standard som kan sammenlignes på tvers av
alle 12 sentraler — og som kan supplere kvalitative ROS-analyser med tallbaserte
referansepunkter.

### Erlang-C beholdes som grunnlinje
Erlang-C (M/M/c) presenteres som Fase 1 / sammenligningsgrunnlag. Den viser
hvorfor klassisk køteori er utilstrekkelig for 110-konteksten (ρ < 6 % ≠ tilstrekkelig
kapasitet), og danner det metodiske argumentet for primærmodellen.

## Operative særtrekk (må hensyntas i modellen)
- **VL-rollen:** c_effektiv = c_total − 1
- **Makkerpar-prosedyre vs. solo-drift:** Prosedyren krever to operatører per hendelse
  (makkerpar), men i praksis håndteres mange hendelser solo. Solo-drift er den daglige
  tilpasningen — kvaliteten synker men resultatet er «godt nok». Modellen kvantifiserer
  hvor ofte dette skjer.
- **Aktivt hendelsebilde:** Pågående hendelser binder kapasitet utover samtaletid
  (RØD-fase + GUL-fase). En operatør som håndterer en aktiv hendelse er ikke
  tilgjengelig for neste anrop selv om telefonsamtalen er avsluttet.
- **Ring-flom (call surge):** Brudd på Poisson-uavhengighet — behandles som
  sensitivitetscase. Jf. Gustavsson (2018) burst-modell.
- **Overløp til Agder:** 10. kø-anrop viderekoblet — de facto servicegrense.
  Tap av regionalkunnskap ved overløp — jf. Dwars (2013) og Gustavsson (2018).
- **30-sekunders-regel:** Ubesvart anrop etter 30 sek = automatisk overføring til Agder
  (bekreftet via beredskapsanalyse s. 25)

## 12 norske 110-sentraler
Finnmark, Troms, Nordland, Trøndelag, Møre og Romsdal, Vest, Sør-Vest, Agder,
Sør-Øst, Oslo, Øst og Innlandet.

## Datakilder
| Kilde | Status |
|---|---|
| LEO/BRIS 110 Sør-Vest 2020–2025 | TILGJENGELIG |
| ROS- og beredskapsanalyse 110 Sør-Vest | TILGJENGELIG |
| DSB årsrapporter (alle sentraler) | OFFENTLIG |
| SSB befolkningsdata | OFFENTLIG |
| LEO-data tvers-sentraler (post-2024) | TILGJENGELIG |

## WBS — Fase 3 leveranser
```
L7  Rapportskjelett + intro v1                    (Uke 12)
L8  EDA — LEO/BRIS, belastningsmonstre per skift  (Uke 12–13)
L8b ROS/beredskapsanalyse-gjennomgang             (Uke 12–13)
L9  Parameterestimering (λ og μ per skiftperiode)   (Uke 13)
L10 Erlang-C modellering med VL-korreksjon        (Uke 14)
L11 Validering og sensitivitetsanalyse            (Uke 14–15)
L12 Teorikapittel                                 (Uke 14–15)
L13 Benchmarking (alle 12 sentraler via DSB)      (Uke 15)
L14 Generaliseringsanalyse                        (Uke 15–16)
L15 Resultater og diskusjon                       (Uke 16)
L16 Hoved-utkast + peer review                   (Slutten av april)
```

## Viktige filer
| Fil | Beskrivelse |
|---|---|
| `011 fase 1 - proposal/Proposal_LOG650_G20_Rune_110_v3.md` | Godkjent proposal v3 |
| `012 fase 2 - plan/Prosjektstyringsplan_G20_Rune_110.md` | Plan v1.8, innlevert 11. mars |
| `014 fase 4 - report/Rapport_LOG650_G20_Rune_110_v0.1.md` | Rapportskjelett med pekere til kapittelfiler |
| `014 fase 4 - report/kap4_casebeskrivelse.md` | Casebeskrivelse v1.1 |
| `014 fase 4 - report/kap5_metode_data.md` | Metode og data v2.0 |
| `014 fase 4 - report/kap6_modell.md` | Modell v2.0 |
| `014 fase 4 - report/kap7_analyse_resultater.md` | Analyse og resultater v1.0 |
| `KI_erklæring_LOG650_G20_Rune.md` | Løpende KI-brukslogg og erklæring |
| `004 data/` | Rådata (gitignored) |
| `002 meetings/` | Møtereferater og e-poster (gitignored) |

## LOG650Vault — kuratert litteraturbase (LLM Wiki)

**Lokasjon:** `../LOG650Vault/` (utenfor dette repoet — `C:\Users\runeg\OneDrive\Documents\Skole utdanning\Logistikk studie\LOG650 LOGISTIKK OG KI\LOG650Vault\`)

Dette er en Obsidian-basert LLM-wiki som inneholder kuraterte sammendrag av all relevant litteratur for prosjektet. Den skal **brukes aktivt** ved alt teori-, litteratur- og diskusjonsarbeid i resten av oppgaven.

### Struktur
- `raw/` — 30+ originale PDF-er (immutable kilder, leses men endres aldri)
- `wiki/sources/` — én kuratert sammendragsside per kilde (29 ferdige)
- `wiki/concepts/` — begreper og teorier (Erlang-A, square-root staffing, QED-regime, ...)
- `wiki/entities/` — personer, organisasjoner (Gustavsson, SOS Alarm, Mandelbaum, ...)
- `wiki/topics/` — tematiske synteser på tvers av kilder (makkerpar_drift, prosedyrebasert_ankomstkonflikt, ...)
- `index.md` — katalog over alle sider, **les denne først** for å finne relevante kilder
- `log.md` — kronologisk append-only logg over ingest/query/lint
- `CLAUDE.md` — vault-spesifikke regler (Obsidian wikilinks, YAML frontmatter, sitatformat)

### Viktige klynger
- **Klynge 1:** EMS call center kø-modeller (komplett) — burst-modeller, function differentiation, capacity planning
- **Klynge 2:** Klassisk call center kø-teori (komplett) — Gans/Koole/Mandelbaum, Halfin-Whitt, ISA, square-root staffing
- **Klynge 3:** Norsk nødmeldetjeneste (pågår) — DSB, brannstudien, SAMLOK, fagskole brann
- **Klynge 4:** Internasjonale standarder (pågår) — NENA STA-020.1

### Kanoniske kilder (KRITISK for diskusjon og teori)
- **Gustavsson 2018 (lic-thesis)** — burst-modell + agent-oppførsel + tap av regionalkunnskap. Direkte parallell til vår makkerpar/solo-drift-observasjon.
- **L'Ecuyer & Gustavsson 2018** — burst-modell SOS Alarm
- **Dwars 2013** — DES + sammenslåingsanalyse 21→10 nederlandske sentraler
- **Garnett, Mandelbaum & Reiman 2002** — Erlang-A + square-root staffing
- **Gans, Koole & Mandelbaum 2003** — kanonisk tutorial
- **Interdep. arbeidsgruppe 2009** — kanonisk policy-anbefaling for nødmelde-organisering
- **NENA STA-020.1-2020** — kanonisk 9-1-1 service-level-standard

### Bruksregler
- **Ved spørsmål om litteratur eller teori:** les `LOG650Vault/index.md` først, deretter relevante `wiki/sources/*.md`-sider.
- **Ved sitater i rapporten:** bruk wiki-sammendraget som inngang, men hent eksakt sitat fra originalen i `raw/`.
- **Når kap 3 (teori) eller kap 8 (diskusjon) skal skrives:** start alltid med å sjekke vault for relevante kilder og topics.
- **Vault-vedlikehold:** Du oppretter ikke wiki-sider på eget initiativ — det er en separat workflow brukeren styrer fra vaulten. Hovedrepoet konsumerer vaulten, men endrer den ikke.
- **Hvis en relevant kilde mangler i vaulten:** flagg det til brukeren slik at hen kan ingest-e den der.

## Analyse — skript og notebooks

### Eksisterende skript
| Fil | Beskrivelse |
|---|---|
| `analyse/scripts/konflikt_v4_korrigert.py` | Primærmodell: ankomstkonflikt med sammenstilte anrop |
| `analyse/scripts/bindingstid_analyse.py` | Bindingstidsberegning og fordeling |
| `analyse/scripts/benchmark_trend_analyse.py` | Benchmarking alle 12 sentraler 2022–2025 |
| `analyse/scripts/scenario_pluss1.py` | Scenarioanalyse (+1 operatør) |
| `analyse/scripts/kapasitet_figurer.py` | Figurgenerering for kapasitetsanalyse |
| `analyse/scripts/konflikt_beredskap_v3.py` | Tidligere versjon av konfliktmodellen |

### Datafilnavn i `004 data/` (eksisterende nedlastede filer)
```
# DSB MOB-filer (bemanningsdata alle sentraler)
20260315_174537_MOB_2022_110-sentral.xlsx
20260315_174530_MOB_2023_110-sentral.xlsx
20260315_174523_MOB_2024_110-sentral.xlsx
20260315_174514_MOB_2025_110-sentral.xlsx

# BRIS fullrapport (hendelsesdata 2025, alle sentraler)
20260315_174350_fullrapport.csv   — UTF-8 med BOM (encoding="utf-8-sig")
                                    Separator: auto (sep=None, engine="python")
                                    Hopp over 2 rader (skiprows=2), rad 1 er header

# Interndokumenter (110 Vest / Bergen brannvesen)
Beredskapsanalyse-110-Vest-30-04-2022.pdf
Beredskapsanalyse-Bergen-brannvesen-2023.pdf
Risiko-og-sarbarhetsanalyse-110-Vest.pdf
Risiko-og-sarbarhetsanalyse-Bergen-brannvesen-2023-.pdf
```

### Kjente BRIS-datastruktur (2025 fullrapport)
- **Nøkkelkolonner:** `Dato anrop` (format `%d.%m.%Y`), `Time på døgnet`, `110-sentral`, `Oppdrag ID`, `Kilde` (verdier: `Alarm` / `Samtale`)
- **110 Sør-Vest 2025:** 61 964 hendelsesrader, 44 kolonner
- **Kritiske datakvalitetsgrenser:**
  - `Operatør-ID`: 0 % dekning (100 % null) — systemstrukturell begrensning bekreftet av DSB
  - `Innsatsvarighet`: ~9 % dekning (kun utrykningshendelser T2/T3)
  - `Alarmbehandlingstid`: ~12 % dekning
  - T1-anrop (88 % av volum, "110-oppdrag uten involvering av brannvesen"): ingen tidsregistrering i BRIS — håndteringstid hentes fra intervjuer

### Sentralnavn-normalisering
Sentralnavn i BRIS/MOB kan ha encoding-feil (f.eks. `S?r-Vest 110`, `S\u00f8r-Vest 110`). Bruk `SENTRALER_NORM`-ordboken i `benchmark_trend_analyse.py` som referanse ved ny kode.

## Rapportregler

### Språk og notasjon
- Bruk norsk i rapporttekst. Behold æ, ø, å i Markdown og tabeller.
- Inline matematikk skrives med `$...$`, ikke `\(...\)`.
- Lagre tekstfiler som UTF-8.

### Kapittelskille (VIKTIG)
Skill tydelig mellom:
- **Casebeskrivelse (kap 4):** Beskriver sentralen, situasjonen og historiske fakta.
  Beskrivende figurer for volum og belastning hører her.
- **Metode og data (kap 5):** Beskriver metodevalg, datagrunnlag, operasjonalisering
  og datakvalitet. Ingen resultater eller modellformulering.
- **Modell (kap 6):** Modellformulering, matematikk og implementasjon.
- **Analyse/Resultat (kap 7):** Resultater presenteres nøkternt med figurer og tabeller.
  Ingen vurdering — det hører i diskusjon (kap 8).
- **Diskusjon (kap 8):** Vurdering av funn mot problemstilling, teori og begrensninger.

### Figurer i rapporten
Standard format for figurer:
```html
<div align="center">
  <img src="..." alt="..." width="80%">
  <p align="center"><small><i>Figur X.Y: Kort figurtekst.</i></small></p>
</div>
```
Figurtekst skal være kort og nøktern, ikke en hel forklaring.

### Tabeller i rapporten
- Tabeller limes inn som Markdown-tabeller.
- Bruk tabellnummer i teksten (f.eks. Tabell 5.1).
- Kort introduksjonssetning i brødteksten før tabellen.

### Rapportsjekkliste
- Innledningen skal være kort (1–2 sider), aktualisere temaet og lede til problemstilling.
- Problemstillingen må være så presis at rapporten verken svarer på mer eller mindre enn det som er formulert.
- Avgrensninger skal begrunnes faglig, ikke med tidsmangel.
- Antagelser skal skrives eksplisitt som antagelser med konsekvenser — aldri som verifiserte fakta.
- Resultatkapitlet presenterer funn nøkternt; vurderinger hører i diskusjonskapitlet.
- Diskusjonskapitlet knytter funn til problemstilling, litteratur, usikkerhet og praktiske implikasjoner.
- Konklusjonen svarer direkte på problemstillingen.

### Review
Når en aktivitet eller et kapittel skal reviewes, bruk en egen subagent (Agent-verktøyet)
for å sikre uavhengighet fra konteksten i hovedsamtalen.

## Tekniske retningslinjer
- **Rapport i Markdown** — én fil per kapittel i `014 fase 4 - report/`, lenket fra `Rapport_LOG650_G20_Rune_110_v0.1.md`
- **Encoding:** Alltid `encoding='utf-8'` i Python. BRIS CSV leses med `encoding='utf-8-sig'` (BOM)
- **Python-stack:** pandas, numpy, scipy, matplotlib, seaborn, openpyxl
- **Versjonskontroll:** Git (GitHub: LOG650/G20-rune-individuell)
- **Referansestil:** APA 7th norsk (se `000 templates/Referansestiler/`)
- **Rådata:** Lagres i `004 data/` (gitignored) — aldri modifisert direkte
- **Figurer:** Genererte figurer lagres i `analyse/figurer/`
- **KI-brukslogg:** Oppdater `KI_erklæring_LOG650_G20_Rune.md` etter hver session

## Risikofaktorer å huske
- **R2/R3:** Poisson-antagelse må testes eksplisitt på LEO/BRIS-data
- **R6:** ~~Tvers-sentraldata (LEO post-2024) — avklar tilgang~~ LUKKET: tilgang bekreftet 10. mars 2026
- **R7:** Tidskollisjon med vaktarbeid ved 110 Sør-Vest — buffer i Gantt
- **R9:** ROS-gjennomgang må formuleres som metodisk vurdering, ikke personkritikk

## Framing-retningslinje (VIKTIG)
ROS/beredskapsanalyser er **kvalitative og vanskelige å etterprøve kvantitativt** på
tvers av sentraler — IKKE at de er strategisk manipulert eller bestillingsverk.
Prosjektet *supplerer og sammenligner* med eksisterende analyser, det *angriper* dem ikke.
