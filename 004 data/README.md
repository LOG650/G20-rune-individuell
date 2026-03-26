# 004 data — Lokalt datagrunnlag (gitignored)

> **Denne mappen er gitignored i sin helhet, med unntak av denne README-filen.**
> Ingen filer herfra lastes opp til GitHub.
> Du er selv ansvarlig for å ta backup av innholdet.

---

## Innhold

### Kildeanalyser og interne dokumenter (110 Sør-Vest — primærcase)

| Fil | Kilde | Innhold | Sensitivitet |
|---|---|---|---|
| `Beredskapsanalyse_110 Sør-Vest_J03.pdf` | 110 Sør-Vest | Beredskapsanalyse inkl. dimensjoneringsgrunnlag — **primærdokument for RQ4** | Intern |
| `Overordnet risiko- og sårbarhetsanalyse 110 Sør-Vest_J05.pdf` | 110 Sør-Vest | Overordnet ROS-analyse — **primærdokument for RQ4** | Intern |
| `Veiledning til forskrift.pdf` | DSB / Justisdept. | Veiledning til brann- og redningsvesenforskriften — regulatorisk kontekst | Offentlig |

### Kildeanalyser — sammenligningsgrunnlag

| Fil | Kilde | Innhold | Sensitivitet |
|---|---|---|---|
| `Beredskapsanalyse-110-Vest-30-04-2022.pdf` | 110 Vest | Beredskapsanalyse — sammenligningsgrunnlag | Intern |
| `Risiko-og-sarbarhetsanalyse-110-Vest.pdf` | 110 Vest | ROS-analyse — sammenligningsgrunnlag | Intern |

### Rådata — BRIS hendelsesdata

| Fil | Kilde | Innhold |
|---|---|---|
| `110 Sør Vest 2025.csv` | 110 Sør-Vest / LEO | Hendelsesdata 2025 — **primærdatagrunnlag for EDA og modellering** |
| `fullrapport2025.csv` | DSB / LEO (alle sentraler) | Hendelsesdata 2025, alle 12 sentraler — benchmarking |
| `Fullrapport2024_110-sentral.csv` | DSB / LEO (alle sentraler) | Hendelsesdata 2024, alle sentraler |
| `Fullrapport2023_110-sentral.csv` | DSB / BRIS (alle sentraler) | Hendelsesdata 2023, alle sentraler |
| `fullrapport2018.csv` | DSB / BRIS (alle sentraler) | Hendelsesdata 2018 — referanseår |

### Rådata — DSB bemanningsdata (MOB)

| Fil | Innhold |
|---|---|
| `20260315_174514_MOB_2025_110-sentral.xlsx` | Bemanning + anropstall alle sentraler 2025 |
| `20260315_174523_MOB_2024_110-sentral.xlsx` | Bemanning + anropstall alle sentraler 2024 |
| `20260315_174530_MOB_2023_110-sentral.xlsx` | Bemanning + anropstall alle sentraler 2023 |
| `20260315_174537_MOB_2022_110-sentral.xlsx` | Bemanning + anropstall alle sentraler 2022 |

### Mangler fortsatt

| Data | Kilde | Prioritet |
|---|---|---|
| BRIS 110 Sør-Vest 2020–2024 (dedikert uttrekk) | DSB — tilgjengelig, ikke hentet | Lav (nasjonal 2022–2024 dekker delvis) |
| SSB befolkningsdata per dekningsområde | SSB Statistikkbanken | Middels — trengs til RQ5 (uke 15) |

---

## Regler for denne mappen

1. **Aldri modifiser rådata direkte** — all behandling skjer på kopier i Jupyter notebooks
2. **Aldri last opp til GitHub** — mappen er gitignored; dette er eneste unntaksfil
3. **Ingen personopplysninger** legges inn i åpne KI-verktøy (jf. GDPR og HiMolde KI-retningslinjer)
4. **Konfidensielle dokumenter** (ROS/beredskapsanalyser) behandles som interne og deles ikke

---

*Sist oppdatert: 2026-03-13*
