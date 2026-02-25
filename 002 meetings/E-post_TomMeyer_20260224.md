# E-postutveksling — Tom Meyer, 24. februar 2026

| | |
|---|---|
| **Fra** | Rune Grødem |
| **Til** | Tom Meyer (Logistikkansvarlig, RogBR) |
| **Dato** | 24. februar 2026 |
| **Emne** | Datagrunnlag for vernebekledning |
| **Status** | Svar mottatt — delvis. Petter og Bent kontaktes for operativ detalj. |

---

## Svar fra Tom Meyer (rød tekst i original)

### Sp. 3 — Vaskekapasitet
**Vaskemaskinen tar 4 sett per vaskerunde.**

### Sp. 4 — Gjennomløpstid (turnaround)
Prosessflyt:
1. Klærne pakkes i plastikksekker på skadested
2. Vaskes i vaskemaskin (potensielt impregnering i samme runde)
3. Henges opp i tørkerom — **ca. ett døgn**
4. Legges inn i klespool

**Estimert total turnaround: ca. 24–36 timer fra innlevert til klart.**

> **Modellparameter W₀:** Dette er ledetiden som inngår i METRIC-modellen. Ledetid ≈ 1 døgn er et konkret estimat som kan brukes som startverdi — verifiseres og sensitivitetstestes.

### Sp. 5 — Ozone-behandling
**RBR utøver ikke ozonbehandling per i dag.**
Derimot: RBR har signert avtale om dekontaminering (CO₂-vask).

> **Modellkonsekvens:** CO₂-vask kan ha lengre prosessid enn ordinær vask — avklar med Tom/Petter om dette er rutine eller unntaksvis.

### Sp. 6 — Kassering
Tom ønsker å snakke om det. Gjennomgang med leverandør planlagt mars/april 2026.

> **Status:** Kriterier ikke formelt dokumentert ennå. Timing passer med fase 3-intervju.

### Sp. 7 — Pool-beholdning kommunikasjon ← KRITISK FUNN
> *"Vi har pr i dag en dårlig rutine på det. Vi skal i utgangspunktet forholde oss til en telleliste, men denne fungerer ikke i praksis."*

**Konsekvens for prosjektet:** Beholdningstall fra tellelisten er usikre. Faktisk antall sett per stasjon/pool må verifiseres i fase 3 — enten via manuell opptelling eller via RFID-data (hvis tilgjengelig).

> **Risiko R1 i prosjektplan bekreftes:** Datakvalitet er en reell utfordring. Tiltaket (kontakt logistikkansvarlig tidlig, vurdere datakvalitet) er allerede iverksatt.

---

## Nye kontakter identifisert

Tom Meyer sender spørsmålene videre til:

| Navn | Rolle | Hva de bidrar med |
|---|---|---|
| **Petter** | Operativt ansvarlig (navn ukjent) | Daglig styring av bekledning og vaskelinjer i praksis |
| **Bent** | Operativt ansvarlig (navn ukjent) | Daglig styring av bekledning og vaskelinjer i praksis |

> **Neste steg:** Ta kontakt med Petter og Bent i fase 3 (uke 11–12). Legg til i intervjuplan som Prioritet 2 (erstatter/supplerer S01-rollen for pool-struktur).

---

## Datagrunnlag-status etter denne e-posten

| Datakilde | Status | Kilde |
|---|---|---|
| BRIS-data (hendelser) | ✅ Tilgjengelig | `004 data/` |
| RFID-vaskedata | ❓ Uavklart — Petter/Bent har dette | Følges opp fase 3 |
| Vaskekapasitet (sett/runde) | ✅ **4 sett/runde** | Tom Meyer, 24.02.2026 |
| Turnaround-tid | ✅ **ca. 1 døgn** | Tom Meyer, 24.02.2026 |
| Beholdning per stasjon | ⚠️ Telleliste finnes men er upålitelig | Tom Meyer, 24.02.2026 |
| Kasserings-/utrangeringsdata | ❓ Avklares mars/april med leverandør | Tom Meyer, 24.02.2026 |
| Bemanning per stasjon | ❓ Ikke avklart ennå | — |

---

*Referanse: Epost-arkiv Rune Grødem, 24.02.2026*
