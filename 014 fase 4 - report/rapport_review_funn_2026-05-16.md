# Reviewfunn for rapport før innlevering

Dato: 2026-05-16  
Omfang: repo, rapportkilder, byggeskript og utvalgte analyseoutputs. Rapportkildene er ikke endret.

## Kort konklusjon

Rapporten er ikke helt innleveringsklar ennå. De faglige hovedfunnene ser konsistente ut i resultatkapitlet, men flere kryssreferanser henger igjen fra kapittelomleggingen, og D-pri1-missingness er oppdatert til 19 % i kapittel 6/8 uten at all metode- og analysenarrativ er harmonisert. Dette bør ryddes før PDF leveres.

## Verifisering utført

- Lest repo-orientering, `CLAUDE.md`, rapportoversikt, byggeskript og alle faktiske rapportkapitler som inngår i `verktoy/build_pdf.py --rapport-full`.
- Bekreftet at faktisk byggeliste bruker `_forside_og_kap1.md`, `kap2_litteratur.md`, `kap3_teori.md`, `kap4_casebeskrivelse.md`, `kap5_metode_data.md`, `kap6_modell.md`, `kap7_analyse.md`, `kap8_resultat.md`, `kap9_diskusjon.md`, `kap10_konklusjon.md` og `_referanser_og_vedlegg.md`.
- Kontrollert figurstier i HTML-figurblokker. Alle seks bildefiler finnes.
- Kontrollert sentrale tall mot analyseoutputs: `analyse/bootstrap_dpri1_mar_sjekk.csv`, `analyse/bootstrap_dpri1_resultater.csv`, `analyse/kapasitet_v4_oppsummering.csv`, `analyse/total_belastning_oppsummering.csv` og `analyse/bindingstid_statistikk.csv`.
- Gjort maskinell ordtelling av kapittel 1-10 fra faktisk byggeliste. Grovt estimat: ca. 33 412 ord inkludert tabeller, ca. 29 457 ekskludert tabell-/figur-linjer. Dette er ikke identisk med institusjonell ordtelling, men avviker for mye fra metadataens `ca. 19 700` til å ignoreres.
- PDF er ikke bygget på nytt, for ikke å endre rapportoutput.

## Må endres før innlevering

### 1. Kryssreferanser er fortsatt preget av gammel kapittelstruktur

Dette er den største leveranserisikoen. Rapporten er nå delt i analyse kap. 7, resultat kap. 8, diskusjon kap. 9 og konklusjon kap. 10, men flere steder peker fortsatt til gammel plassering.

Konkrete steder:

- `kap7_analyse.md:3`, `:5`, `:9`, `:51`, `:98`, `:174`, `:184`: kapittel 7 sier at resultater/kvantifisering ligger i kap. 9, og at tolkning skjer i kap. 10. Riktig struktur er resultat i kap. 8, diskusjon i kap. 9 og konklusjon/anbefalinger i kap. 10.
- `kap4_casebeskrivelse.md:3` og `:96`: sier at analyseresultater eller hendelsestypefordeling analyseres/presenteres i kapittel 7. Etter splitten bør dette presiseres som analysegrunnlag i kap. 7 og resultater i kap. 8.
- `kap4_casebeskrivelse.md:114`: ROS-gjennomgangen sies å inngå i diskusjonen kapittel 8. Nå ligger ROS-resultat i 8.4 og diskusjon i kap. 9.
- `kap5_metode_data.md:7`: viser til `avsnitt 6.1 og 7.7`; 7.7 finnes ikke. Sannsynlig ny peker er kap. 8.6 for overførbarhet/generaliserbarhet, eventuelt 10.4 for videre validering.
- `kap5_metode_data.md:373`: viser til `kap 9.2 og 8.2.3`; 8.2.3 finnes ikke.
- `kap5_metode_data.md:393`: viser til `avsnitt 5.8`; kapittel 5 stopper på 5.7. Sannsynlig referanse er 5.5/5.6 eller vedlegg A.
- `kap5_metode_data.md:406`: viser til `7.7.4`; riktig sted for bootstrap/MAR-drøfting er 8.3.4.
- `kap6_modell.md:269` og `:371`: `bootstrap-CI 7.7.4` må rettes til 8.3.4.
- `kap6_modell.md:383`: modellresultatene sies å ligge i kap. 7; resultatene ligger nå i kap. 8.
- `kap9_diskusjon.md:7-11`: RQ-oversikten bør skrives om samlet. Den peker til ikke-eksisterende eller feil avsnitt som 8.1.3, 8.2.1, 7.8, 7.9 og 8.4.1.
- `kap9_diskusjon.md:18`: "Diskusjonen i 8.1 til 8.3" bør trolig være "Resultatene i 8.1 til 8.3".
- `kap10_konklusjon.md:9`: `kap 8.5 og 8.4.1` inneholder ikke gyldig 8.4.1. Hvis poenget er nasjonal del, bruk 8.5 og 8.6.
- `kap10_konklusjon.md:91`: versjonsfoteren sier "skarp åpningssetning i 9.1", men filen er kap. 10 og åpningssvaret står i 10.1.
- `_referanser_og_vedlegg.md:107-109`: `## 11. Vedlegg` og `## 12. Vedlegg` står rett etter hverandre. Det bør bare være én vedleggsoverskrift etter `## 11. Bibliografi`, sannsynligvis `## 12. Vedlegg`.

Konsekvens: En sensor vil se dette som manglende sluttkontroll, selv om analysen ellers holder sammen.

### 2. D-pri1 missingness er ikke harmonisert

Oppdatert analyse ser ut til å være 4 499 D-pri1, 3 645 observerte og 854 manglende/avviste, altså 19 %. Dette støttes av `analyse/bootstrap_dpri1_mar_sjekk.csv` og `kap8_resultat.md:194`.

Tekst som fortsatt er i utakt:

- `kap5_metode_data.md:141`: sier 23,5 % manglende for kategori D og bruker dette i metoden. Det er riktig for samlet kategori D-dekning, men bør ikke framstå som D-pri1-imputering.
- `kap5_metode_data.md:191`: sier `~25 %` av D-pri1 mangler tidspunkt.
- `kap5_metode_data.md:247`: sier `~25 % imputert` for D-pri1.
- `kap7_analyse.md:106`: sier at 3 357 av 4 499 D-pri1 har registrert første ressurs fremme. Dette gir ca. 74,6 %, og kolliderer med 3 645/81 % i kap. 8.

Foreslått grep: skill tydelig mellom samlet kategori D-dekning i datakvalitetstabellen og D-pri1-spesifikk imputering i modellen. Hvis 3 645/854 er siste sannhet, bruk 19 % konsekvent i kap. 5, 6, 7 og 8.

### 3. Bindingstid 13,0 vs. 14,1 minutter blandes

`analyse/bindingstid_statistikk.csv` viser median 13,0 min for samlet `Total (anrop til fremme)` på kategori D, mens rapportens modellparameter for D-pri1 er 14,1 min inkl. +3 min kvitteringsvindu. Begge tall kan være sanne, men de brukes ikke alltid med presis nok etikett.

Konkrete steder:

- `kap7_analyse.md:22`: sier at primærmodellen bruker total bindingstid median 13,0 min inkl. akuttfase og kvittering. For D-pri1-modellen er dette misvisende; kap. 6, 7 og 8 bruker 14,1 min.
- `kap9_diskusjon.md:8`: RQ2-oppsummeringen bruker 13,0 min og peker til ugyldig 8.1.3.
- `kap9_diskusjon.md:36`: sier median 13,0 minutter per beredskapsoppdrag, mens diskusjonen ellers handler om D-pri1/makkerpar og bør enten bruke 14,1 min eller eksplisitt si samlet kategori D.

Foreslått grep: bruk 14,1 min når teksten omtaler D-pri1/makkerpar-binding i primærmodellen. Bruk 13,0 min bare hvis det eksplisitt merkes som samlet kategori D-median uten D-pri1-avgrensning.

### 4. Metadata/ordtelling er sannsynligvis feil

`_forside_og_kap1.md:5` oppgir `Antall ord: ca. 19 700 (kap. 1 til 10, eksklusive tabeller, kode og litteraturliste)`. Maskinell kontroll på faktisk byggeliste ga ca. 29 457 ord for kap. 1-10 når tabell- og figur-linjer ekskluderes. Selv med strengere institusjonell ordtelling er differansen stor.

Foreslått grep: tell på nytt med samme regel som skal brukes ved innlevering, og oppdater eller fjern ordtallet hvis det ikke er obligatorisk.

`_forside_og_kap1.md:5` og `:54` oppgir 31. mai 2026 som innleveringsdato. Hvis dette er planlagt/due date er det greit, men ved faktisk levering før 31. mai bør datoen kontrolleres.

### 5. Masterfil og README peker til gamle rapportfiler

Dette påvirker trolig ikke PDF-byggingen, men repoet fremstår mindre ferdig hvis Claude/sensor leser strukturen.

- `Rapport_LOG650_G20_Rune_110_v0.1.md:27-29` peker til `kap7_analyse_resultater.md`, `kap8_diskusjon.md` og `kap9_konklusjon.md`, som ikke er den faktiske kapittelstrukturen.
- `README.md:55` peker fortsatt til `kap7_analyse_resultater.md`.
- `verktoy/build_pdf.py:226-229` viser riktig nåværende byggeliste: `kap7_analyse.md`, `kap8_resultat.md`, `kap9_diskusjon.md`, `kap10_konklusjon.md`.

Foreslått grep: oppdater master/README eller merk dem eksplisitt som utdaterte interne arbeidsfiler.

## Bør endres før innlevering

### 6. Konsisjon: samme Erlang-C-tabell gjentas i kap. 6 og kap. 7

`kap6_modell.md:93-100` og `kap7_analyse.md:13-20` inneholder i praksis samme Erlang-C-resultat, bare med ulik tabellnummerering. Siden brukeren spesifikt ber om konsishet, er dette en tydelig kandidat for stramming.

Foreslått grep: behold full tabell ett sted. Kapittel 6 kan ha modellen/formelen og henvise til kap. 7, eller kapittel 7 kan ha kort oppsummering og henvise til Tabell 6.1. Ikke presenter samme baseline som to selvstendige tabeller med ulike nummer.

### 7. Figur- og versjonsmerking bør sluttvaskes

- `kap4_casebeskrivelse.md:91-94`: figuren har `Figur 4.1` i `alt`-teksten, men ikke i synlig caption. Byggeskriptet bruker caption-teksten i `<p>`, så PDF-caption vil sannsynligvis ikke starte med `Figur 4.1:`.
- `kap8_resultat.md:387`: versjonsfoteren sier `Kap 9`, men filen er kap. 8.
- `kap10_konklusjon.md:91`: se punkt 1; versjonsfoteren peker til 9.1.

Foreslått grep: gjør en siste søk/erstatt-kontroll på `Kap 9 | Versjon`, `Figur 4.1`, `9.1` i kap10-foteren og alle kapittelnummer i fotere.

### 8. Små språkvaskpunkter som bør tas

Disse er ikke strukturelle, men de skaper unødvendig støy i en ellers teknisk rapport:

- `kap5_metode_data.md:145`: mangler punktum før "I tillegg" etter encoding-eksemplene.
- `kap5_metode_data.md:167`: `Byggingsbrann` bør være `Bygningsbrann`.
- `kap5_metode_data.md:399`: teksten sier "fem grep", men listen har seks grep.
- `kap6_modell.md:385`: `ved aktivere VL-rolle` bør være `ved mer aktiv VL-rolle` eller tilsvarende.
- `kap8_resultat.md:55`: `en ny beredskapsanrop` bør være `et nytt beredskapsanrop`.
- `kap9_diskusjon.md:66`: `VL-rollen i praksis er aktivere` bør være `VL-rollen i praksis er mer aktiv`.
- `kap9_diskusjon.md:70`: `Hver av disse alternativene` bør være `Hvert av disse alternativene`.
- Begrepsformene `antagelse/antagelser` og `antakelse/antakelser` blandes. Velg én form for sluttversjonen. `Antakelse` er vanlig bokmålsform, men det viktigste er konsekvens.

### 9. Nasjonal benchmarking: forkortelsen `Arbmengde` ser uferdig ut

`kap8_resultat.md:262` og `:277` bruker `Arbmengde`. Det er forståelig, men ser mer ut som et regnearkfelt enn rapporttekst. Hvis tabellbredden tillater det, skriv `Arbeidsmengde`.

## Kan stå, basert på kontrollen

- Figurfilene som brukes i rapporten finnes: `bindingstid_per_time.png`, `bindingstid_beredskap_fordeling_v2.png`, `scenario_pluss1_operator.png`, `total_belastning_A_vs_B.png`, `total_belastning_sensitivitet.png` og `bootstrap_dpri1_ci.png`.
- Hovedtallene i resultatkapitlet stemmer med analyseoutputs jeg sjekket: variant A natt/helg Svikt 32,6 %, variant B hovedscenario natt/helg Svikt 33,2 %, +1-operatør natt/helg Svikt 16,7 %, bootstrap-CI for variant A natt/helg Svikt [32,09; 33,16] avrundet til [32,1; 33,2].
- Kapittel 1 sin rapportstruktur (`_forside_og_kap1.md:187-207`) stemmer i hovedsak med den nye 7/8/9/10-delingen. Problemet ligger primært i eldre lokale henvisninger inne i kap. 4-10 og i master/README.

## Prioritert rekkefølge for Claude

1. Rett alle kapittel-/avsnittsreferanser etter ny struktur, særlig kap. 7, kap. 9 RQ-oversikt og kap. 10 omfangstekst.
2. Harmoniser D-pri1 missingness til 3 645 observerte / 854 manglende / 19 %, eller dokumenter eksplisitt hvorfor andre prosenter gjelder samlet kategori D og ikke D-pri1.
3. Skill 13,0 min samlet kategori D fra 14,1 min D-pri1-parameter.
4. Oppdater ordtelling/metadata og fjern duplisert vedleggsoverskrift.
5. Stram Erlang-C-duplisering og ta språkvasklisten.
