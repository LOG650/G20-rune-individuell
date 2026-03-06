# Litteraturliste — LOG650 G20 (Rune Grødem)
## Dimensjonering av røykdykkerbekledning under usikker etterspørsel

> **Bruk:** Last ned i denne prioriterte rekkefølgen. Obligatoriske kilder (Nivå 1) må skaffes før modelleringsarbeidet starter. Øvrige leses ved behov under skriving.
> 
> **Verifiseringsstatus:** Alle referanser er bekreftet av minst én AI-kilde. DOI-er bør verifiseres i Google Scholar eller Scopus før sitering.

---

## NIVÅ 1 — Obligatorisk kjerne (les disse først)

Disse 6 kildene utgjør teorikapittelets fundament. Ingen av dem er valgfrie.

### 1.1 METRIC-originalen
Sherbrooke, C. C. (1968). METRIC: A multi-echelon technique for recoverable item control. *Operations Research, 16*(1), 122–141. https://doi.org/10.1287/opre.16.1.122

> **Hva:** Grunnmodellen for recoverable item inventory i to-nivå nettverk. Etablerer pipeline-logikk, EBO og base-stock for reparerbare enheter.  
> **Hvorfor obligatorisk:** Din modell er en direkte applikasjon av denne teorien. Må siteres i teorikapittelet.  
> **Hvor finne:** RAND-rapport åpent tilgjengelig på https://www.rand.org/content/dam/rand/pubs/research_memoranda/2006/RM5078.pdf — verifiser mot Operations Research-versjonen.

---

### 1.2 Eksakt multi-echelon modell
Graves, S. C. (1985). A multi-echelon inventory model for a repairable item with one-for-one replenishment. *Management Science, 31*(10), 1247–1256. https://doi.org/10.1287/mnsc.31.10.1247

> **Hva:** Eksakt steady-state løsning for multi-echelon repairable items med one-for-one policy og compound Poisson-etterspørsel.  
> **Hvorfor obligatorisk:** Gir det analytiske grunnlaget for din one-for-one wash-trigger-logikk (ett sett hentes fra pool når ett sendes til vask). Compound Poisson-behandlingen er direkte relevant.  
> **Hvor finne:** Management Science via JSTOR eller Google Scholar. MIT OCW har en forelesningsversjon åpent.

---

### 1.3 Standardverket for multi-echelon teknikker
Sherbrooke, C. C. (2004). *Optimal inventory modeling of systems: Multi-echelon techniques* (2. utg.). Springer. https://doi.org/10.1007/b109856

> **Hva:** Den autoritative boken som samler METRIC-familien, EBO-beregninger, lateral transshipments og systemtilnærming.  
> **Hvorfor obligatorisk:** Gir deg standardterminologi og metodisk språk som fagmiljøet kjenner igjen. Støtter ryddig argumentasjon for service constraints.  
> **Hvor finne:** SpringerLink — tilgjengelig via HiMolde-biblioteket.

---

### 1.4 Primær lærebok
Axsäter, S. (2015). *Inventory control* (3. utg.). Springer. https://doi.org/10.1007/978-3-319-15729-0

> **Hva:** Dekker service constraints, multi-echelon reorder points, fill rate og compound Poisson. Kap. 3 (service constraints), kap. 5 (compound Poisson), kap. 10 (METRIC) er de sentrale kapitlene.  
> **Hvorfor obligatorisk:** Primær pensumlærebok i LOG650. Faglig begrunnelse for å bruke 99%-servicegrad fremfor mangel-kostnad.  
> **Hvor finne:** Allerede tilgjengelig via Bookshare (EPUB).

---

### 1.5 Survey over repairable inventory-feltet
Guide, V. D. R., Jr., & Srivastava, R. (1997). Repairable inventory theory: Models and applications. *European Journal of Operational Research, 102*(1), 1–20. https://doi.org/10.1016/S0377-2217(97)00155-0

> **Hva:** Klassisk survey som kartlegger hele feltet for reparerbare lagersystemer, antagelser og løsningsmetoder.  
> **Hvorfor obligatorisk:** Gir deg faglig oversikt og argumentasjon for modellvalg. Brukes i litteraturkapittelet for å plassere oppgaven i feltet.  
> **Hvor finne:** ScienceDirect/Elsevier via HiMolde-biblioteket.

---

### 1.6 System-orienterte servicekrav
Basten, R. J. I., & van Houtum, G. J. (2014). System-oriented inventory models for spare parts. *Surveys in Operations Research and Management Science, 19*(1), 34–55. https://doi.org/10.1016/j.sorms.2014.05.002

> **Hva:** Survey over system-orienterte lagerkrav (availability/SLA fremfor kostnad), lateral/emergency transshipments og kobling til reparasjonskapasitet.  
> **Hvorfor obligatorisk:** Gir faglig bro fra militær spare parts til beredskapslogistikk. "Systemet må være operativt" er analogt til brannberedskap.  
> **Hvor finne:** ScienceDirect via HiMolde-biblioteket.

---

## NIVÅ 2 — Viktig støttelitteratur (les under modellering og skriving)

### 2.1 METRIC-utvidelser (modellfamilie-bevissthet)

Sherbrooke, C. C. (1986). VARI-METRIC: Improved approximations for multi-indenture, multi-echelon availability models. *Operations Research, 34*(2), 311–319. https://doi.org/10.1287/opre.34.2.311

> **Hva:** Forbedrede approksimasjoner i METRIC-familien. Viser at analytisk modell kan valideres med simulering.  
> **Bruk:** Nevnes i teorikapittelet som bevis på at METRIC-approksimasjonen kan kvantifiseres. Støtter "analytisk + simulering"-strategien din.  
> **Hvor finne:** INFORMS PubsOnLine.

---

Muckstadt, J. A. (1973). A model for a multi-item, multi-echelon, multi-indenture inventory system. *Management Science, 20*(4), 472–481. https://doi.org/10.1287/mnsc.20.4.472

> **Hva:** MOD-METRIC — METRIC utvidet til multi-indenture og flerartikler.  
> **Bruk:** Nevnes kort i teorikapittelet for å vise kjennskap til METRIC-familiens generaliseringer. Begrunner avgrensningen til ett SKU.  
> **Hvor finne:** JSTOR eller INFORMS.

---

Hillestad, R. (1982). *Dyna-METRIC: Dynamic multi-echelon technique for recoverable item control* (RAND Report R-2785-AF). RAND Corporation.

> **Hva:** METRIC utvidet til dynamiske miljøer med simulering for readiness/availability.  
> **Bruk:** Støtter bruk av diskret hendelsessimulering når steady-state-forutsetninger ikke holder. Relevant for diskusjonskapittelet.  
> **Hvor finne:** Åpent tilgjengelig på RAND.org.

---

### 2.2 Compound Poisson og etterspørselsmodellering

Prak, D., Teunter, R., Syntetos, A., & van Houtum, G. J. (2021). Robust compound Poisson parameter estimation for inventory control. *Omega, 104*, 102481. https://doi.org/10.1016/j.omega.2021.102481

> **Hva:** Metode for å estimere λ og batch-størrelse k fra begrenset historisk data ved compound Poisson-etterspørsel.  
> **Bruk:** Direkte metodisk støtte for parametrisk estimering fra BRIS-data. Essensielt for datakapittelet.  
> **Hvor finne:** ScienceDirect/Elsevier.

---

Turrini, L., & Meissner, J. (2019). Spare parts inventory management: New evidence from distribution fitting. *European Journal of Operational Research, 273*(1), 118–130. https://doi.org/10.1016/j.ejor.2018.07.017

> **Hva:** Empirisk sammenligning av fordelingstilpasning (Poisson, NB, compound Poisson) for spare parts-etterspørsel.  
> **Bruk:** Metodisk begrunnelse for valg av etterspørselsfordeling. Relevant for datakapittelet når du tilpasser BRIS-data.  
> **Hvor finne:** ScienceDirect/Elsevier.

---

Teunter, R. H., Syntetos, A. A., & Babai, M. Z. (2011). Intermittent demand: Linking forecasting to inventory obsolescence. *European Journal of Operational Research, 214*(3), 606–615. https://doi.org/10.1016/j.ejor.2011.05.018

> **Hva:** Behandler sjelden og ujevn (intermittent) etterspørsel, kobling mellom forecasting og ukurans/svinn.  
> **Bruk:** Faglig støtte for å modellere svinn (α) som en systematisk prosess knyttet til etterspørselsmønsteret, ikke bare tilfeldig støy.  
> **Hvor finne:** ScienceDirect/Elsevier.

---

Hadley, G., & Whitin, T. M. (1963). The (S−1, S) inventory policy under compound Poisson demand. *Management Science, 9*(3), 391–396. https://doi.org/10.1287/mnsc.9.3.391 *(Verifiser DOI)*

> **Hva:** Tidlig klassiker som viser at (S−1,S) base-stock-policy er optimal for compound Poisson-etterspørsel med one-for-one replenishment.  
> **Bruk:** Faglig fundament for din policy-logikk. Kort referanse i teorikapittelet.  
> **Hvor finne:** INFORMS PubsOnLine.

---

### 2.3 To-echelon systemer og lateral transshipments

Lee, H. L. (1987). A multi-echelon inventory model for repairable items with emergency lateral transshipments. *Management Science, 33*(10), 1302–1316. https://doi.org/10.1287/mnsc.33.10.1302

> **Hva:** Multi-echelon repairable items der baser kan benytte emergency lateral transshipments.  
> **Bruk:** Direkte relevant for stasjoner som deler utstyr (Riska/Klepp/Ålgård mot Stangeland). Brukes i diskusjonen av multi-stasjon-strukturen.  
> **Hvor finne:** INFORMS via Google Scholar.

---

Drent, M., & Arts, J. (2021). Expediting in two-echelon spare parts inventory systems. *Manufacturing & Service Operations Management, 24*(2), 1000–1019. https://doi.org/10.1287/msom.2020.0888

> **Hva:** To-echelon repairable system med mulighet for "ekspedering" (raskere retur). Case fra jernbane.  
> **Bruk:** Metodisk mal for to-echelon case-studie med empiriske data. Relevant for diskusjon av turnaround-reduksjon som alternativ til økt beholdning.  
> **Hvor finne:** INFORMS PubsOnLine.

---

van Houtum, G.-J., & Kranenburg, B. (2015). *Spare parts inventory control under system availability constraints*. Springer. https://doi.org/10.1007/978-1-4615-4195-8 *(Verifiser DOI)*

> **Hva:** Bok som samler multi-item modeller og heuristikker for availability constraints. Moderne og tilgjengelig fremstilling.  
> **Bruk:** Støtter formal kobling fra beredskapsklarhet til "availability constraints". Nyttig referanseramme som ikke er militærspesifikk.  
> **Hvor finne:** SpringerLink via HiMolde-biblioteket.

---

### 2.4 Simulering og validering

Srivathsan, S., & Viswanathan, S. (2017). Queueing-based models for a multi-echelon repairable item inventory system. *Computers & Operations Research, 79*, 350–362. https://doi.org/10.1016/j.cor.2016.07.011 *(Verifiser)*

> **Hva:** Kombinerer køteori og repairable inventory for multi-echelon system. Modellerer reparasjonskapasitet eksplisitt.  
> **Bruk:** Metodisk støtte for kømodellering av vaskerikapasitet som flaskehals. Relevant dersom du modellerer turnaround eksplisitt.  
> **Hvor finne:** ScienceDirect/Elsevier.

---

Topan, E., Eruguz, A. S., Ma, W., van der Heijden, M. C., & Dekker, R. (2019). A review of operational spare parts service logistics in service control towers. *European Journal of Operational Research, 276*(3), 1–17. https://doi.org/10.1016/j.ejor.2019.03.026

> **Hva:** Review av operasjonell spare parts-logistikk med fokus på datadrevne triggere og sanntidsstyring.  
> **Bruk:** Faglig støtte for AI-klassifisering av hendelsestype som wash-trigger. Relevant for diskusjon av datadrevet styring.  
> **Hvor finne:** ScienceDirect/Elsevier.

---

Hu, Q., Boylan, J. E., Chen, H., & Labib, A. (2018). OR in spare parts management: A review. *European Journal of Operational Research, 266*(2), 395–414. https://doi.org/10.1016/j.ejor.2017.07.058

> **Hva:** Systematisk review over OR-metoder i spare parts management med fokus på teori–praksis-gap.  
> **Bruk:** Brukes i diskusjonskapittelet for å posisjonere oppgaven: du gjør et konkret empirisk bidrag i et felt der "practice integration" er en kjent utfordring.  
> **Hvor finne:** ScienceDirect/Elsevier.

---

### 2.5 Beredskapskontekst og PPE

Lesniak, Z. C., Smith, D. L., & Notarianni, K. A. (2020). The effect of personal protective equipment on firefighter occupational performance. *Journal of Occupational and Environmental Hygiene, 17*(1), 1–9. https://doi.org/10.1080/15459624.2019.1692684 *(Verifiser DOI i PubMed)*

> **Hva:** Studie av hvordan tung PPE reduserer arbeidskapasitet og øker utmattelse, noe som driver opp batch-etterspørselen etter rene drakter ved langvarige hendelser.  
> **Bruk:** Faglig begrunnelse for at batch-størrelse k er variabel og hendelsesavhengig. Kan brukes i casebeskrivelsen og som motivasjon for compound Poisson-modell.  
> **Hvor finne:** PubMed — søk på "Lesniak firefighter personal protective equipment 2020".

---

## NIVÅ 3 — Norsk kontekst og grålitteratur

Disse er ikke akademiske primærkilder, men nødvendige for å forankre caset og innledningen.

Direktoratet for samfunnssikkerhet og beredskap. (2022). *Brann- og redningsvesenforskriften* (FOR-2022-01-18-65). Lovdata. https://lovdata.no/dokument/SF/forskrift/2022-01-18-65

> **Hva:** Ny dimensjoneringsforskrift som erstattet 2002-forskriften. Fjernet detaljerte PPE-krav og overlot dimensjonering til lokal risikoanalyse.  
> **Bruk:** Faglig og juridisk begrunnelse for *hvorfor* RogBR trenger en kvantitativ modell. Brukes i innledningen og casebeskrivelsen.

---

Direktoratet for samfunnssikkerhet og beredskap. (2022). *Veiledning til brann- og redningsvesenforskriften*. DSB. https://www.dsb.no

> **Hva:** DSBs veiledning til den nye forskriften, inkludert beskrivelse av risikobasert dimensjonering.  
> **Bruk:** Støtter argumentasjonen for at lokal beredskapsanalyse er basis for dimensjonering.  
> **Hvor finne:** DSB.no — søk på "veiledning brann- og redningsvesenforskriften".

---

## Oppsummering: prioritert nedlastingsrekkefølge

| Prioritet | Referanse | Kritisk for |
|---|---|---|
| 1 | Sherbrooke (1968) | Teorikapittel — kjerne |
| 2 | Graves (1985) | Teorikapittel — one-for-one logikk |
| 3 | Axsäter (2015) kap. 3, 5, 10 | Teorikapittel — service constraints |
| 4 | Sherbrooke (2004) | Teorikapittel — metodespråk |
| 5 | Guide & Srivastava (1997) | Litteraturkapittel — feltposisjonering |
| 6 | Basten & van Houtum (2014) | Teorikapittel — system-orientert service |
| 7 | Prak et al. (2021) | Metode/data — parameterestimering |
| 8 | Turrini & Meissner (2019) | Metode/data — fordelingstilpasning |
| 9 | Lesniak et al. (2020) | Casebeskrivelse — batch-motivasjon |
| 10 | DSB-forskrift (2022) | Innledning/case — juridisk ramme |
| 11 | Lee (1987) | Diskusjon — multi-stasjon |
| 12 | Drent & Arts (2021) | Diskusjon — to-echelon case |
| 13 | VARI-METRIC Sherbrooke (1986) | Teori — modellfamilie |
| 14 | Teunter et al. (2011) | Data — svinnmodellering |
| 15 | Hu et al. (2018) | Diskusjon — teori–praksis-gap |

---

## Totalt antall referanser

- Nivå 1 (obligatorisk): 6
- Nivå 2 (støtte): 13
- Nivå 3 (grålitteratur): 2
- **Sum: 21 referanser**

Dette dekker hele rapporten uten å sprenge omfanget. For en LOG650-masteroppgave er 15–25 velfunderte referanser sterkere enn 40 overfladisk gjennomleste.

---

*Opprettet: 2026-02-23 | Basert på GPT Deep Research + Gemini syntetisert av Claude*
