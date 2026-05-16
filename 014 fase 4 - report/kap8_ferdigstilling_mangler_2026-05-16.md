# Kapittel 8: mangler og feil før ferdigstilling

Dato: 2026-05-16  
Omfang: `kap8_resultat.md` og leveranse-PDF slik den ligger i repoet per commit `816ce12`.

## Kritisk funn

### P1: PDF-en er ikke bygget fra siste kapittel 8-kilde

`kap8_resultat.md` ble endret i siste commit `816ce12`, men `005 report/Rapport_LOG650_G20_Rune_110_samlet.pdf` ble sist oppdatert i commit `382012a`. PDF-en inneholder derfor eldre kapittel 8-tekst.

Eksempler som finnes i PDF, men ikke lenger i samme form i kilden:

- `Arbmengde` finnes fortsatt i PDF, mens kilden bruker `Arbeidsmengde`.
- `3 357` finnes fortsatt i PDF, mens kilden bruker `3 645` gyldige D-pri1-observasjoner.
- `fem grep` finnes fortsatt i PDF, mens kilden i metodekapitlet nå bruker `seks grep`.
- `en ny beredskapsanrop` finnes fortsatt i PDF.

Tiltak: bygg PDF på nytt etter at punktene under er rettet. Ikke lever dagens PDF som final.

## Må rettes i kapittel 8-kilden

### P2: Grammatikkfeil i 8.1

Fil: `kap8_resultat.md`, ca. linje 55.

Nå:

> slik at en D-aba-hendelse på natt/helg *tillater* en ny beredskapsanrop i parallell drift

Foreslått:

> slik at en D-aba-hendelse på natt/helg *tillater* et nytt beredskapsanrop i parallell drift

Konsekvens hvis den står: synlig språkfeil i et sentralt forklaringsavsnitt.

### P2: Presiser bootstrap-/imputeringslogikk i 8.3.4

Fil: `kap8_resultat.md`, ca. linje 218.

Setningen under blander litt sammen median-imputering og pooled bootstrap-reimputering:

> Pooled imputering med observert median vil derfor systematisk *overestimere* binding for disse

Problemet er at avsnittet først sier at bootstrap-en trekker med erstatning fra de observerte verdiene. Da er det ikke helt presist å kalle dette `pooled imputering med observert median`.

Foreslått grep: skill mellom:

- punktestimatet, som bruker median-imputering
- bootstrap-CI-en, som trekker fra observert empirisk fordeling

Mulig formulering:

> Median-imputeringen i punktestimatet kan derfor overestimere binding for avbrutte utrykninger. Bootstrap-reimputeringen fra observert fordeling gir samtidig et bredere usikkerhetsbilde enn punktestimatet alene, men fanger ikke en full stratifisert missingness-modell.

## Bør vurderes før final

### P3: `op-bind` vs. `op-binder`

Fil: `kap8_resultat.md`, ca. linje 23.

Teksten bruker både `op-binder` og `op-bind`:

- `D-pri1 bidrar med 2 op-binder`
- `D-aba Fase 1 bidrar med 1 op-bind`

Foreslått: bruk `op-binder` konsekvent, eventuelt `op-binder-enhet(er)` dersom du vil gjøre begrepet mer lesbart.

### P3: Variant A-resultat støttes med variant B-scenariobånd

Fil: `kap8_resultat.md`, ca. linje 47.

Teksten sier at variant A-tallet 32,6 % skal leses med scenariobånd, men båndet som oppgis kommer fra variant B lav/hoved/høy. Det er metodisk greit hvis det er ment som et robusthetsbånd for total antagelsesvariasjon, men det bør ikke kunne misforstås som et rent variant A-konfidensintervall.

Foreslått presisering:

> Variant B-scenariobåndet brukes her som robusthetssjekk for antagelsesfølsomhet, ikke som et statistisk konfidensintervall for variant A.

### P3: Tabell 8.3 står under 8.2, men gjelder hele modellen

Fil: `kap8_resultat.md`, ca. linje 111.

`Oppsummering av modellantagelser` kommer rett etter scenarioanalysen, men tabellen gjelder hele resultatkapitlet. Det fungerer, men plasseringen kan oppleves litt tilfeldig.

Mulige valg:

- la den stå, men behold den som en overgang før 8.3
- flytt den tidligere, rett etter metodeavsnittet i 8.1
- gi den en kort brosetning: "Før variant B og sensitivitetsanalysen presenteres, samles modellantagelsene som ligger bak resultatene."

## Verifisert OK i kapittel 8-kilden

- D-pri1 missingness er harmonisert til `3 645` observerte / `854` manglende / `19 %`.
- `Arbmengde` er rettet til `Arbeidsmengde` i kilden.
- Nasjonal benchmarking skiller lokal Sør-Vest-eksport fra nasjonalt DSB-uttrekk.
- Tabell 8.8, 8.9 og 8.10 finnes og brukes konsistent.
- Vedleggs-/kapittelstruktur for 8.5, 8.6 og 8.7 ser konsistent ut med ny kapittelstruktur.

## Etter retting

1. Rett punktene over i `kap8_resultat.md`.
2. Kjør final PDF-rebuild via `verktoy/build_pdf.py --rapport-full`.
3. Kontroller at PDF ikke lenger inneholder:
   - `en ny beredskapsanrop`
   - `Arbmengde`
   - `3 357`
   - `fem grep`
4. Kontroller at PDF viser dagens veileder/ordtelling og kapittelstruktur.
