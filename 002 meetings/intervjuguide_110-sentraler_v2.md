# Intervjuguide — 110-sentraler
**Prosjekt:** LOG650 G20 Rune Grødem — Kapasitetsanalyse 110-sentraler
**Status:** Versjon 2.0 — konsolidert og generalisert
**Sist oppdatert:** 2026-03-29

---

## Formål
Verifisere og supplere registerdata (LEO/BRIS/MOB) med operativ kunnskap som ikke
fremkommer i data. Særlig: bindingstider, prosedyrstruktur (makkerpar), VL-rolle og
dimensjoneringsgrunnlag.

**Format:** Strukturert samtale, 30–40 minutter. Spørsmålsliste sendes på forhånd ved
forespørsel. Alternativt kortere telefonsamtale med fokus på Del A og Del B.

---

## Del A — Bemanning og rollefordeling

**A1. Grunnbemanning per skifttype**
Hvor mange operatører + vaktleder er normalt til stede i operatørrommet for
dag-hverdag / natt-hverdag / dag-helg / natt-helg?
*(Intervjuer fyller inn MOB-tall på forhånd for verifisering)*

**A2. Vaktlederens rolle i anropshåndtering**
Besvarer vaktleder nødanrop direkte som del av normal drift, eller kun unntaksvis
(f.eks. ved kapasitetsproblem / siste utvei)?
Hvilke oppgaver har VL som gjør dem utilgjengelig for anropshåndtering?

**A3. Makkerpar-prinsippet**
Jobber operatørene i par på hendelser — én som primærkontakt (RØD) og én som
koordinator (GUL) — eller håndteres hendelser normalt av én operatør alene?
Gjelder makkerpar for alle hendelsestyper, eller kun ved utrykningshendelser?
Hva skjer ved samtidskonflikt når det ikke er ledig makker?

---

## Del B — Bindingstid og hendelseshåndtering

**B1. Operatørbindingstid per hendelsestype**
Omtrent hvor lenge er en operatør bundet til en hendelse fra anrop mottas til
operatøren er fullt ledig igjen for neste anrop — inkludert koordinering etter samtalen?

| Hendelsestype | Estimert bindingstid (min) |
|---|---|
| ABA / falsk alarm (ingen utrykking) | |
| Enkelt oppdrag (helse, service, enkel brann, ingen utrykking) | |
| Utrykningshendelse (brann, ulykke, redning) | |
| Kompleks/langvarig hendelse (storbrann, RIG, søk og redning) | |

*Estimatene trenger ikke være eksakte — et typisk intervall (f.eks. 8–15 min) er tilstrekkelig.*

**B2. Oppgaver som binder kapasitet etter samtalen**
Hvilke oppgaver utfører operatøren etter at selve samtalen er avsluttet?
(f.eks. utalarmering, sambandshåndtering, ressursoppfølging, loggføring)
Er disse oppgavene vanligvis delegert til en makker (GUL-funksjon), eller
gjøres de av samme operatør som tok anropet?

**B3. Automatisk brannalarm (ABA)**
Håndteres ABA-anrop som regel av én operatør alene (solo), eller følges de
opp av en makker i koordinatorrollen?
Kommer det typisk inn en oppfølgingstelefon fra bygningen i etterkant av ABA-varsel?

---

## Del C — Kapasitetsgrenser og overflytpraksis

**C1. Overflyt til nabosentral**
Når overføres anrop automatisk til nabosentralen (f.eks. Agder)?
Er terskelen antall anrop i kø, ventetid, eller begge deler?
*(Verifiser: beredskapsanalysen oppgir «10. anrop ELLER ubesvart etter 30 sek»)*

**C2. Kapasitetssituasjoner i praksis**
Opplever vaktlaget situasjoner der det ikke er ledig operatør til å ta et nytt anrop
etter at arbeidsmetodikken (makkerpar) er fulgt?
Hva er den operative responsen i slike situasjoner — arbeider man videre «etter beste evne»?

---

## Del D — Dimensjoneringsgrunnlag

**D1. Grunnlag for bemanningsnivå**
Hva er den primære begrunnelsen for sentralens bemanningsnivå?
(ROS-/beredskapsanalyse, historisk erfaring, budsjett, nabosentral-sammenligning,
DSB-anbefaling — ranger gjerne de tre viktigste)

**D2. Differensiert bemanning dag/natt/helg**
Er den reduserte bemanningen natt og helg primært begrunnet i redusert volum av
beredskapsoppdrag, redusert volum av serviceanrop (ABA-testing mv.), eller begge?
Er det gjort en eksplisitt kvantitativ vurdering av beredskapsbelastning per skifttype?

---

## Del E — Avslutning

- Er det forhold ved sentralens drift som er særlig relevante for en kapasitetsanalyse,
  men som sjelden fanges opp i statistikk eller analyse?
- Ønsker dere å motta et sammendrag av studiens funn etter avslutning?

---

## Sentralspesifikke notater (fyll ut før hvert intervju)

| Sentral | MOB-bemanning (dag/natt) | Avvik/tema å verifisere |
|---|---|---|
| **Sør-Vest 110** | Dag: 3+VL, Natt/helg: 2+VL | Nattbemanning redusert 2023→2024. 30 sek overflow-terskel (bekreftet?) |
| **Tromsø 110** | Dag: 2+VL, Natt: 2+VL | Dag 2022→3→2 — årsak? c_eff = 1 etter VL-korreksjon |
| **Agder 110** | Se MOB | Mottar overløp fra Sør-Vest — kapasitetspåvirkning? |
| **Innlandet 110** | Økt fra 3→4 (2022→2023) | Årsak til økning? |
| **Møre og Romsdal** | Økt dag 3→4 (2023→2024) | Årsak til økning? |
| **Midt-Norge 110** | Stabil 4+VL | Servicetesting ikke i LEO — bekreft omfang |

---

*Versjon 2.0 — 2026-03-29 | Erstatter v0.1 (15.03.2026)*
*Endringer: Konsolidert fra 5 deler/20+ spørsmål til 5 deler/13 spørsmål.
Nytt fokus: makkerpar-prosedyre (A3), bindingstid per kategori (B1–B3),
30 sek overflytterskel (C1). Fjernet: detaljerte loggingsspørsmål, vikarer/bakvakt.*
