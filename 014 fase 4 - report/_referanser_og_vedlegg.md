---

## 10. Referanser

*Foreløpig utvalg — fullstendig APA 7th norsk referanseliste vedlikeholdes i `012 fase 2 - plan/Litteraturliste_LOG650_G20_Rune.xlsx` og synkroniseres til rapporten ved endelig innlevering.*

Al-Sarhani, A., et al. (2025). *Cognitive load among emergency dispatchers: implications for error rates in simultaneous incident handling.*

APCO International. (2005). *Project RETAINS: Staffing and retention in public safety communications centers.*

Brann- og redningsvesenforskriften. (2021). *Forskrift om organisering, bemanning og utrustning av brann- og redningsvesen og nødmeldesentralene* (FOR-2021-09-17-2856). Justis- og beredskapsdepartementet.

Brill, P. H., & Green, L. (1984). Queues in which customers receive simultaneous service from a random number of servers. *Management Science*, *30*(1), 51–68.

Chelst, K., & Barlach, Z. (1981). Multiple unit dispatches in emergency services: models to estimate system performance. *Management Science*, *27*(12), 1390–1409.

Dimensjoneringsforskriften. (2023). *Forskrift om dimensjonering, utrusting og bemanning av brannvesen* (FOR-2023-01-06-23). Justis- og beredskapsdepartementet.

DSB. (2025). *Årsrapport 110-sentralene 2025*. Direktoratet for samfunnssikkerhet og beredskap.

Dwars, E. (2013). *Capacity planning in an emergency dispatch center: a case study of the Dutch ambulance service* (MSc-thesis). Universiteit van Amsterdam.

Erlang, A. K. (1917). Solution of some problems in the theory of probabilities of significance in automatic telephone exchanges. *The Post Office Electrical Engineers' Journal*, *10*, 189–197.

Feldman, Z., Mandelbaum, A., Massey, W. A., & Whitt, W. (2008). Staffing of time-varying queues to achieve time-stable performance. *Management Science*, *54*(2), 324–338.

Gans, N., Koole, G., & Mandelbaum, A. (2003). Telephone call centers: Tutorial, review, and research prospects. *Manufacturing & Service Operations Management*, *5*(2), 79–141.

Garnett, O., Mandelbaum, A., & Reiman, M. (2002). Designing a call center with impatient customers. *Manufacturing & Service Operations Management*, *4*(3), 208–227.

Green, L. V., Kolesar, P. J., & Whitt, W. (2007). Coping with time-varying demand when setting staffing requirements for a service system. *Production and Operations Management*, *16*(1), 13–39.

Gustavsson, J. (2018). *Capacity planning and agent behavior in emergency call centers: a study of SOS Alarm Sweden* (Lic. thesis). Linköping University.

Halfin, S., & Whitt, W. (1981). Heavy-traffic limits for queues with many exponential servers. *Operations Research*, *29*(3), 567–588.

Harchol-Balter, M. (2022). The multiserver-job queueing model. *Queueing Systems*, *100*(3–4), 201–225.

Interdepartemental arbeidsgruppe. (2009). *Forslag til felles organisering av nødmeldetjenesten*. Justis- og politidepartementet.

Jamtli, B., Svendsen, V. G., Jørgensen, M., Kramer-Johansen, J., Hov, M. R., & Hardeland, C. (2024). Protocol adherence and intuition-based decision making at the Oslo emergency medical communication center. *Scandinavian Journal of Trauma, Resuscitation and Emergency Medicine, 32*.

Jouini, O., Dallery, Y., & Nait-Abdallah, R. (2008). Analysis of the impact of team-based organizations in call center management. *Management Science*, *54*(2), 400–414.

Kim, J. S., Cho, Y. J., Baek, J. W., & Kim, H. M. (2008). Service capacity analysis of multi-server systems with cooperation. *European Journal of Operational Research*, *191*(3), 1137–1152.

Larson, R. C. (1974). A hypercube queueing model for facility location and redistricting in urban emergency services. *Computers & Operations Research*, *1*(1), 67–95.

L'Ecuyer, P., & Gustavsson, J. (2018). Modeling bursts in emergency call arrivals. *Proceedings of the 2018 Winter Simulation Conference*, 2956–2967.

Leonardsen, A.-C. L., Hardeland, C., Hellesø, R., & Grøndahl, V. A. (2021). Work experiences of emergency medical dispatchers in Norway: a qualitative study. *BMC Health Services Research, 21*.

Meld. St. 16. (2023–2024). *Felles verdier — felles ansvar*. Justis- og beredskapsdepartementet.

NENA. (2020). *NENA STA-020.1-2020: PSAP service level standard for 9-1-1.*

Normark, M. (2002). *Work and technology at an emergency call center.* Luleå University of Technology.

Rehn, M., et al. (2021). Dispatch accuracy in the Norwegian helicopter emergency medical service. *Scandinavian Journal of Trauma, Resuscitation and Emergency Medicine, 29*.

Rogaland brann og redning IKS. (2024). *Prosedyre arbeidsmetodikk, utalarmering og loggføring* (versjon 4, 16.12.2024). [Intern prosedyre.]

Van Buuren, M., Kommer, G. J., van der Mei, R., & Bhulai, S. (2017). EMS call center models with and without function differentiation: a comparison. *Operations Research for Health Care, 12*, 16–28.

Vera Institute. (2019). *Behind the call: Understanding the work of 9-1-1 dispatchers.*

---

## 11. Vedlegg

### Vedlegg A — Python-implementasjon og GitHub-repo

Kildekode og analyseskript er versjonskontrollert på GitHub: [`LOG650/G20-rune-individuell`](https://github.com/LOG650/G20-rune-individuell).

**Sentrale analyseskript (`analyse/scripts/`):**

| Skript | Formål |
|---|---|
| `konflikt_total_belastning.py` | V3-primærmodell: ankomstkonfliktanalyse variant A (beredskap) og B (total belastning) |
| `scenario_pluss1.py` | Scenario +1 operatør per skift |
| `bindingstid_analyse.py` | Bindingstidsberegning og fordeling per hendelseskategori |
| `benchmark_trend_analyse.py` | Benchmarking alle 12 sentraler 2022–2025 (MOB-data) |
| `nasjonal_oversikt.py` | Nasjonal DSB 2025-oversikt (508 228 oppdrag, 7 figurer) |
| `nasjonal_2025_analyse.py` | Nasjonal klassifisering per sentral med V3-regler (D-pri1/D-aba/L-aba) |
| `uttrekk_laba_sorvest.py` | Stratifisert utvalgsgenerering for LABA-dybdeanalyse (n=50, utvidet til n=100) |

**PDF-pipeline:**
- `verktoy/build_pdf.py` er master-skript for konvertering MD → PDF (Pandoc + XeLaTeX for faglige dokumenter; reportlab for interaktive spørreskjemaer).
- `eksporter_pdf.bat` er interaktiv meny i prosjektroten.

### Vedlegg B — Spørreskjema til de 12 sentralene

Tilpasset spørreskjema er utviklet per sentral (`analyse/sporreskjema/<Sentral>_110.md`) med åtte deler:

1. Verifisering av MOB-rapporterte data (2022–2025)
2. Vaktordning og bemanningsstruktur (normal- vs minimumsbemanning)
3. Arbeidsmetodikk (makkerpar vs solo-drift)
4. Hendelseskategorier og operatørbindingstider
5. ROS- og beredskapsanalyse
6. Operativ belastning og opplevd bemanning
7. Sentralspesifikke avklaringer (DSB 2025-avvik i topp-3 / bunn-3)
8. Avsluttende kommentarer

Interaktiv PDF-versjon (AcroForm) genereres via `verktoy/build_pdf.py --alle-skjema`.

### Vedlegg C — DSB-ønskeliste: BRIS-datauttrekk

Et eget strategidokument (`analyse/DSB_onskeliste_BRIS_datauttrekk.md`) spesifiserer 22 prioriterte datapunkter som ville muliggjøre utvidet kvantitativ kapasitetsanalyse på nasjonalt nivå. Dokumentet er strukturert etter høy/medium/lav prioritet og avgrenser eksplisitt mot tilstøtende systemer (Alarmmottak, Transwire, Frequentis ICCS).

### Vedlegg D — Dokumentasjon av KI-bruk

Fullstendig brukslogg, rapporttekst og administrativ erklæring finnes i det løpende dokumentet:

**`KI_erklæring_LOG650_G20_Rune.md`** (prosjektrot)

Dokumentet inneholder:

- Del 1: «Bruk av kunstig intelligens» — rapporttekst
- Del 2: Løpende brukslogg med dato, verktøy, formål og hva som ble tatt inn
- Del 3: Administrativ erklæring (signeres ved innlevering)
- Del 4: Personvern og konfidensialitet

Det offisielle HiMolde-skjemaet «Erklæring om bruk av kunstig intelligens» leveres som separat administrativt vedlegg ved innlevering av sluttrapport.

### Vedlegg E — LABA-dybdeanalyse (detaljert metode)

Dybdeanalysen av L-aba-bindingstid er dokumentert i kap 5.4. Rådata (50 trukne hendelser / 49 gyldige, Kilde=Alarm-subset n=30) ligger i `004 data/laba_sorvest_2025_dybdeanalyse.xlsx`. Utvidet utvalg (n=100) er under innhenting og inngår ikke i hovedresultatet i denne rapportversjonen.

### Vedlegg F — VL-validering av bindingstider

Empirisk validering av forutsetningen $c_{\text{eff}} = c_{\text{total}} - 1$ (vaktleder besvarer normalt ikke nødanrop) er dokumentert i `014 fase 4 - report/VL_validering_bindingstider.md` og tilhørende PDF.

### Vedlegg G — Prosjektdokumentasjon

- `011 fase 1 - proposal/Proposal_LOG650_G20_Rune_110_v3.md` — godkjent proposal
- `012 fase 2 - plan/Prosjektstyringsplan_G20_Rune_110.md` — prosjektstyringsplan v1.8
- `012 fase 2 - plan/status.md` — løpende statuslogg v2.3
- `012 fase 2 - plan/Gantt_LOG650_G20_Rune_110.mpp` / `.xml` — Gantt-diagram
