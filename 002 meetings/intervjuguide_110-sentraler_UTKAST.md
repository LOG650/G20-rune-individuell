# Intervjuguide — 110-sentraler (utkast)
**Prosjekt:** LOG650 G20 Rune Grødem — Kapasitetsanalyse 110-sentraler (Erlang-C)
**Status:** Punktliste til strukturert spørreskjema
**Versjon:** 0.1 — 15. mars 2026

---

## Formål med intervjuet
Verifisere og supplere DSB-årsrapportdata med operativ kunnskap som ikke fremkommer i
registerdata (LEO/BRIS/MOB). Særlig: håndteringstider, servicemedarbeider-organisering,
VL-rolle og lokal dimensjonerings-/analysepraksis.

---

## Format — valg mellom to tilnærminger

**Alternativ A — Uformell telefon/samtale ved anledning**
- Lavere terskel, raskere gjennomføring
- Egner seg for sentraler der du allerede har kontakt (Sør-Vest, Midt-Norge)
- Risiko: Mindre struktur, vanskeligere å sammenligne på tvers

**Alternativ B — Strukturert Teams-møte (30–45 min)**
- Gir mer presise, sammenlignbare svar
- Kan sende spørsmålsliste på forhånd
- Egner seg for sentraler uten eksisterende kontakt
- Anbefalt for sentraler der dataavvik er størst (se Tromsø, Agder, Sør-Vest)

**Anbefaling:** Gjør Sør-Vest og Midt-Norge uformelt (kjenner dem). Tilby øvrige sentraler
e-post med vedlagt spørreskjema som alternativ til møte — lavere terskel for deltakelse.

---

## Del 1 — Bemanning og organisering (verifisering av MOB-data)

### 1.1 Grunnbemanning
- Antall operatører per vakt: dag hverdag / natt hverdag / dag helg / natt helg?
  *(Verifiser mot MOB-data — se tabell nedenfor)*
- Er dette **minimum** eller **normalbemanning**?
- Finnes det definert **maksbemanning** (f.eks. ved stormøte/krise)?

### 1.2 Vaktleder (VL)
- Er VL alltid til stede i vaktrommet?
- Besvarer VL nødanrop direkte, eller kun ved kapasitetsproblem / som siste utvei?
- Har VL andre oppgaver som gjør dem utilgjengelig for anropshåndtering?
  *(Validerer c_effektiv = c_total − 1)*

### 1.3 Servicemedarbeidere og ABA-servicetesting
- Har sentralen dedikerte medarbeidere som håndterer servicetesting (ABA-anlegg)?
- Hvis ja: Antall? Fast stilling eller oppgave lagt til eksisterende rolle?
- Registreres disse anropene i LEO, eller håndteres de utenfor oppdrags-systemet?
  *(Midt-Norge: registreres ikke i LEO — kun «overfly»)*
- Hvem tar servicetestingene ved **fravær/sykdom/helg**?
- Omtrentlig antall servicetestinger per dag / uke?

### 1.4 Vikarer og ekstravakter
- Benyttes faste vikarer eller tilkallingsvakter?
- Hvorfra rekrutteres vikarer (internt / eksternt / andre sentraler)?
- Er vikarbruk systematisert/dokumentert, eller situasjonsbestemt?

### 1.5 Bakvakt
- Finnes en definert **bakvaktordning** (operatør tilgjengelig utenom normal vakt)?
- Hvilke situasjoner utløser bakvakt?
- Inngår bakvakt i bemanningsberegningen for sentralen?

---

## Del 2 — Hendelseshåndtering og håndteringstider (for μ-estimering)

### 2.1 Samtaletid og håndteringstid per kategori
- Hva er typisk **samtaletid** for et rent telefonoppdrag (ingen utrykking, T1)?
  *Eks.: «Anrop besvares, ingen brann, avsluttes» — anslå i minutter*
- Hva er typisk håndteringstid for en **automatisk brannalarm (ABA/T2)**?
  *Inkl. oppfølging etter selve samtalen?*
- Hva er typisk total operatørbindingstid for en **hendelse med utrykking (T3)**?
  *Samtale + koordinering + loggføring + ressursoppfølging*
- Binder pågående hendelser (T3) kapasitet for andre operatører simultant?
  *Kan én hendelse kreve to operatørers oppmerksomhet samtidig?*

### 2.2 Ring-flom (call surge)
- Opplever sentralen perioder med mange samtidige innkommende anrop fra én hendelse?
- Hva skjer operativt når kapasiteten er fullt utnyttet?
  *Kø, viderekobbling til nabosentral, bakvakt aktiveres?*
- Finnes intern statistikk eller logg over slike episoder?

---

## Del 3 — Logging og dataregistrering

### 3.1 Loggingspraksis i LEO
- Registreres samtaler konsekvent i LEO, eller finnes det kategorier som ikke logges?
  *(Midt-Norge: servicetesting ikke i LEO)*
- Registreres **operatør-ID** på oppdrag i jeres system?
  *(Bekreftet ikke i BRIS-eksport — men finnes det lokalt?)*
- Registreres **samtaletid/varighet** på telefonhenvendelser lokalt?
- Finnes interne rapporter eller uttrekk utover det DSB/BRIS eksporterer?

### 3.2 Standardisert arbeidsflyt — verifisering
*Beskriv gjerne avvik fra denne standard-beskrivelsen:*
- Innkommende anrop → operatør besvarer → vurderer → logger oppdrag → dispatcher/avslutter
- For ABA: innringer varsler → operatør legger i service → mottar tilbakemelding → avslutter
- For T3: oppdrag opprettes → ressurser varsles → operatør følger opp til ressurs er ledig

---

## Del 4 — Analyser og dimensjonering

### 4.1 ROS- og beredskapsanalyse
- Har sentralen utarbeidet ROS-analyse? Hvilket år ble den sist revidert?
  *(MOB 2025 data tilgjengelig — verifiserer mot svar)*
- Har sentralen utarbeidet beredskapsanalyse? Sist revidert?
- Er du/ledelsen kjent med innholdet i disse analysene?
- Er bemanningsnivået formelt begrunnet i analysene?
- Mulighet for å dele kopi av analyse (anonymisert/offentlig del)?

### 4.2 Dimensjoneringsgrunnlag
- Hva legges til grunn for fastsettelse av bemanningsnivå?
  *(ROS, historisk erfaring, nabosentral-sammenligning, DSB-anbefaling, budsjett?)*
- Er DSBs MOB-rapport kjent og brukt aktivt i dimensjoneringsdiskusjoner?
- Ønsker sentralen et kvantitativt dimensjoneringsverktøy (som Erlang-C-modellen)?

### 4.3 Trender og endringer (bemanningstrendverifisering)
*Basert på årsrapportdata 2022–2025 — be respondenten bekrefte/forklare avvik:*

| År | Op dag (hverd.) | Op natt (hverd.) | Op dag (helg) | Op natt (helg) | Anrop |
|---|---|---|---|---|---|
| 2022 | [se tabell] | | | | |
| 2023 | | | | | |
| 2024 | | | | | |
| 2025 | | | | | |

*(Fyll inn sentralspesifikke tall fra MOB-data før intervju)*

- Er endringer i bemanning mellom år et resultat av budsjett, ny ROS-analyse, rekruttering?
- Er det planlagte endringer i bemanning de neste 1–2 år?

---

## Del 5 — Avslutning

- Er det andre forhold ved sentralens drift som er relevante for en kapasitetsanalyse?
- Kan vi kontakte dere igjen ved behov for oppfølgingsspørsmål?
- Ønsker dere å få tilsendt et sammendrag av studiens funn etter avslutning?

---

## Sentralspesifikke observasjoner (fyll ut før hvert intervju)

### Bemanningsendringer å verifisere (fra MOB-data 2022–2025)

| Sentral | Endring å verifisere |
|---|---|
| **Sør-Vest 110** | Nattbemanning redusert fra 4 til 3 mellom 2023 og 2024. Årsak? |
| **Tromsø 110** | Endringer: 2022: dag=2/natt=3 → 2023: dag=3/natt=3 → 2024–25: dag=2/natt=2. Årsak? |
| **Innlandet 110** | Økt fra 3/3 (2022) til 4/4 (2023–2025). Årsak? |
| **Agder 110** | Nattbemanning redusert fra 3 til 3 (hverdag) mellom 2023 og 2024 — faktisk dagbemanning ned fra 4 til 3. Årsak? |
| **Møre og Romsdal 110** | Dagbemanning økt fra 3 (2022–23) til 4 (2024–25). Årsak? |
| **Midt-Norge 110** | Stabil 4/4. Servicetesting-organisering bekreftet 15.03.2026 — verifiser antall medarbeidere og dekning. |
| **Tromsø 110** | Kun c_effektiv=1 dag og natt (etter VL-korreksjon). Er dette reelt? Finnes kompenserende tiltak? |

### Prioriteringsrekkefølge for kontakt
1. Sør-Vest 110 (primærcase — mest kritisk)
2. Midt-Norge 110 (allerede kontaktet — oppfølging)
3. Tromsø 110 (ekstremuteligger — c_effektiv=1)
4. Agder 110 (nabosentral, mottar overløp fra Sør-Vest)
5. Øvrige sentraler etter behov

---

*Versjon 0.1 — punktliste til strukturert spørreskjema | 15. mars 2026*
*Neste steg: Pilottest på Sør-Vest → juster → send til øvrige sentraler*
