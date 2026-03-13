# 004 data — Lokalt datagrunnlag (gitignored)

> **Denne mappen er gitignored i sin helhet, med unntak av denne README-filen.**
> Ingen filer herfra lastes opp til GitHub.
> Du er selv ansvarlig for å ta backup av innholdet.

---

## Innhold

### Kildeanalyser og interne dokumenter

| Fil | Kilde | Innhold | Sensitivitet |
|---|---|---|---|
| `Beredskapsanalyse-110-Vest-30-04-2022.pdf` | 110 Vest | Beredskapsanalyse inkl. dimensjoneringsgrunnlag | Intern |
| `Beredskapsanalyse-Bergen-brannvesen-2023.pdf` | Bergen brannvesen | Beredskapsanalyse | Intern |
| `Risiko-og-sarbarhetsanalyse-110-Vest.pdf` | 110 Vest | ROS-analyse med kapasitetsvurderinger | Intern |
| `Risiko-og-sarbarhetsanalyse-Bergen-brannvesen-2023-.pdf` | Bergen brannvesen | ROS-analyse | Intern |

### Rådata (legges her i fase 3)

| Forventet fil | Kilde | Innhold |
|---|---|---|
| `LEO_BRIS_110SV_2020_2025.csv` (eller tilsvarende) | 110 Sør-Vest / LEO | Hendelsestidsstempler, oppdragstype, varighet — primærdatagrunnlag |
| `LEO_alle_sentraler_2024_2025.csv` (eller tilsvarende) | LEO (alle sentraler) | Sammenlignbare hendelsesdata for benchmarking |
| `DSB_arsrapport_2025_bemanning.xlsx` (eller tilsvarende) | DSB | Bemanning og anropsvolum per sentral |
| `SSB_befolkning_dekningsomrade.csv` (eller tilsvarende) | SSB | Innbyggertall per dekningsområde |

---

## Regler for denne mappen

1. **Aldri modifiser rådata direkte** — all behandling skjer på kopier i Jupyter notebooks
2. **Aldri last opp til GitHub** — mappen er gitignored; dette er eneste unntaksfil
3. **Ingen personopplysninger** legges inn i åpne KI-verktøy (jf. GDPR og HiMolde KI-retningslinjer)
4. **Konfidensielle dokumenter** (ROS/beredskapsanalyser) behandles som interne og deles ikke

---

*Sist oppdatert: 2026-03-13*
