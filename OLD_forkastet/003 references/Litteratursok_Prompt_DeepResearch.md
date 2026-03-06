# Litteratursøk — Deep Research Prompt
## LOG650 Masteroppgave: Dimensjonering av røykdykkerbekledning under usikker etterspørsel

---

## INSTRUKSJON TIL AI

Du skal gjennomføre et systematisk akademisk litteratursøk for en masteroppgave i logistikk. Les hele dette dokumentet nøye før du søker. Målet er å identifisere **30–50 relevante, fagfellevurderte artikler** som til sammen dekker det teoretiske og metodiske grunnlaget for oppgaven. Kvalitet og presisjon er viktigere enn kvantitet — ikke ta med artikler bare for å fylle en liste.

For hver artikkel du finner skal du oppgi:
1. Full APA 7-referanse
2. Publiseringsår
3. Tidsskrift / kilde
4. Hovedbidrag (2–4 setninger)
5. Relevans for denne oppgaven (1–2 setninger)
6. Kategori (se kategorier nedenfor)
7. Type: **[Grunnlagsartikkel / Metodeartikkel / Empirisk case-studie / Review-artikkel]**

Organiser output etter kategori. Innen hver kategori: sorter kronologisk (eldste først).

---

## KONTEKST OG PROBLEMSTILLING

**Organisasjon:** Rogaland Brann og Redning IKS (RogBR), en norsk brann- og redningstjeneste med flere stasjoner i Rogaland fylke. Stasjonene er organisert i et nettverk der deltidstasjoner (Riska, Klepp, Ålgård m.fl.) deler utstyrspooler med hovedstasjoner (bl.a. Stangeland).

**Kritisk utstyr:** Røykdykkerbekledning (firefighter SCBA protective clothing / turnout gear). Hvert sett er personlig verneutstyr som må vaskes og tørkes etter bruk før det kan brukes igjen. Vaskeprosessen utgjør en kapasitetsbegrensning (ledetid).

**Kjerneproblemet:** RogBR mangler et kvantitativt beslutningsgrunnlag for å dimensjonere beholdningen. Dagens praksis baserer seg på tommelfingerregler. Dette kan gi enten overbeholdning (unødvendig kapitalbinding; 428 sett × 18 000 kr = ~7,7 MNOK) eller underbeholdning (operativ risiko: manglende verneutstyr ved innsats).

**Problemstilling:**
> Hvordan kan lagerstyring av røykdykkerbekledning dimensjoneres under usikker, hendelsesdrevet etterspørsel for å oppnå definert servicegrad til lavest mulig kapitalbinding?

**Prosjektmål:** Utvikle en kvantitativ beslutningsmodell implementert i Python som gir anbefalte lagernivåer for alle RogBR-stasjoner, slik at ønsket servicegrad (≥99 %) kan oppnås til lavest mulig totalkostnad eller med dokumentert trade-off mellom kostnad og tilgjengelighet.

---

## NØKKELKJENNETEGN VED PROBLEMET

Søket må ta høyde for følgende særtrekk — disse skiller oppgaven fra standard lagerstyringsprosjekter:

1. **Hendelsesdrevet, intermitterende etterspørsel** — Etterspørsel trigges av brannhendelser, ikke av jevn forbrukstakt. Mange dager har null etterspørsel; noen dager er det ekstrem etterspørsel ved storbrann.

2. **Sammensatt Poisson-prosess (Compound Poisson demand)** — Modellen er tolagdelt:
   - Hendelser ankommer med rate λ (Poisson-fordelt i tid)
   - Hver hendelse genererer et tilfeldig antall sett som trenger vask: X ~ f(x), der X = 0 ved lette hendelser (gressbrann), X > 0 kun ved røykdykkerinnsats
   - Total etterspørsel D = Σ Xᵢ over alle hendelser i perioden

3. **Multi-echelon nettverksstruktur** — Flere stasjoner deler utstyrspooler. Etterspørsel ved én stasjon påvirker tilgjengelighet for andre. Konkurrerende etterspørsel mellom stasjoner er eksplisitt.

4. **Kapasitetsbegrensning: vaskeprosess som ledetid** — Vaskesyklus (vask + tørk) utgjør effektiv ledetid L. I denne oppgaven behandles L empirisk (estimert fra data), ikke som en analytisk kømodell.

5. **Normativ vs. empirisk etterspørsel** — Etterspørselen estimeres fra to kilder: (a) historiske BRIS-hendelsesdata koblet til vaskelogg, og (b) ROS-analyse for planlagte beredskapsscenarioer.

6. **Servicegrad Type II (fill rate) er operasjonelt riktig** — Sannsynligheten for at et sett er tilgjengelig *når det etterspørres*, ikke bare at man ikke går tom per syklus.

---

## SØKEKATEGORIER

### Kategori T1 — Stokastisk lagerstyring: teori og servicegrad
**Formål:** Etablere det teoretiske fundamentet. (Q,R)- og (s,S)-politikk, sikkerhetslager, servicegrad Type I og II, bestillingspunkt under stokastisk etterspørsel.

**Søkestrenger:**
```
("safety stock" OR "reorder point") AND ("service level" OR "fill rate") AND ("stochastic demand" OR "uncertain demand")
("(Q,R) policy" OR "(s,S) policy" OR "continuous review inventory") AND ("service level" OR "stockout probability")
("Type I service level" OR "Type II service level" OR "fill rate" OR "cycle service level") AND "inventory"
```
**Prioriter:** Silver, Pyke & Thomas (1998); Zipkin (2000); Hadley & Whitin (1963); Axsäter (2006). Inkluder nyere reviewartikler (2015–2024).

---

### Kategori T2 — Intermitterende og hendelsesdrevet etterspørsel
**Formål:** Metodisk grunnlag for etterspørselsmodellering ved sjeldne, klumpede hendelser. Poisson og negativ binomialfordeling, Croston-metoden og forbedringer, compound Poisson.

**Søkestrenger:**
```
("intermittent demand" OR "lumpy demand" OR "sporadic demand") AND ("inventory" OR "stocking policy") AND ("Poisson" OR "negative binomial" OR "compound Poisson")
("compound Poisson demand" OR "stuttering Poisson") AND ("inventory management" OR "safety stock")
("Croston method" OR "Syntetos-Boylan") AND ("intermittent demand" OR "slow-moving items")
("event-driven demand" OR "incident-based demand") AND ("inventory" OR "emergency logistics")
```
**Prioriter:** Croston (1972); Syntetos & Boylan (2001, 2005); Teunter & Sani (2009). Inkluder nyere arbeid på compound Poisson i lagerstyring.

---

### Kategori T3 — Multi-echelon og nettverkslagerstyring
**Formål:** Modellering av lagernett med delte pooler og konkurrerende etterspørsel. METRIC-rammeverket og etterkommere. Spare parts / critical items i nettverk.

**Søkestrenger:**
```
("multi-echelon inventory" OR "multi-location inventory") AND ("pooling" OR "lateral transshipment" OR "shared stock") AND ("service level" OR "availability")
("METRIC" OR "VARI-METRIC" OR "MOD-METRIC") AND ("inventory" OR "spare parts" OR "availability")
("inventory pooling" OR "resource pooling") AND ("emergency" OR "critical items" OR "availability")
("multi-depot" OR "multi-location") AND ("stochastic demand" OR "uncertain demand") AND ("inventory optimization")
```
**Prioriter:** Sherbrooke (1968) METRIC; Graves (1985); Axsäter (1990); Van Houtum et al. (1996). Søk også etter nyere tilnærminger til pooling i beredskapssektoren.

---

### Kategori T4 — Lagerstyring for kritisk utstyr i beredskapssektoren
**Formål:** Empirisk og metodisk litteratur fra brannvesen, ambulanse, politi og militær — der lagerstyring av livskritisk utstyr under usikker hendelsesdrevet etterspørsel er studert.

**Søkestrenger:**
```
("fire department" OR "fire service" OR "fire brigade") AND ("inventory management" OR "equipment management" OR "resource allocation") AND ("service level" OR "availability" OR "optimization")
("emergency services" OR "EMS" OR "ambulance") AND ("inventory" OR "stocking" OR "dimensioning") AND ("stochastic" OR "uncertain demand")
("protective equipment" OR "PPE" OR "turnout gear" OR "firefighter equipment") AND ("inventory" OR "stock level" OR "dimensioning")
("military logistics" OR "defense logistics") AND ("spare parts" OR "critical inventory") AND ("multi-echelon" OR "service level")
("public safety" OR "emergency logistics") AND ("inventory optimization" OR "stock dimensioning")
```
**Merk:** Søk spesielt etter studier fra Slovakia, Tsjekkia, Polen og Skandinavia — det er gjort relevant arbeid på logistikkoptimalisering i europeiske brannvesen.

---

### Kategori T5 — Datametode: kobling av hendelsesregistre og lagerdata
**Formål:** Metodisk grunnlag for å estimere etterspørselsparametre fra operasjonelle hendelsesdata. Hvordan koble hendelsestype (BRIS-registre) til faktisk ressursforbruk (vaskelogg) for å estimere λ og fordelingen til X.

**Søkestrenger:**
```
("demand estimation" OR "demand modeling") AND ("event data" OR "incident data" OR "operational data") AND ("inventory" OR "logistics")
("data-driven inventory" OR "empirical demand distribution") AND ("emergency" OR "incident-based" OR "event-driven")
("parameter estimation" OR "distribution fitting") AND ("Poisson" OR "negative binomial") AND ("logistics" OR "inventory" OR "emergency services")
("operational data" OR "administrative data") AND ("stochastic modeling" OR "demand forecasting") AND ("public safety" OR "emergency")
```

---

### Kategori T6 — Simulering som valideringsmetode
**Formål:** Monte Carlo og diskret-hendelsessimulering som metode for å beregne servicegrad og trade-offs under realistisk variasjon — spesielt relevant for validering av den analytiske modellen.

**Søkestrenger:**
```
("Monte Carlo simulation" OR "discrete event simulation") AND ("inventory management" OR "safety stock") AND ("service level" OR "stockout")
("simulation" AND "inventory optimization") AND ("stochastic demand" OR "uncertain demand") AND ("validation" OR "sensitivity analysis")
("agent-based" OR "discrete event") AND ("emergency logistics" OR "fire service" OR "EMS") AND ("simulation")
```

---

## INKLUSJONS- OG EKSKLUSJONSKRITERIER

**Inkluder:**
- Fagfellevurderte artikler i anerkjente tidsskrift (Operations Research, EJOR, IJPR, IJPE, MSOM, Omega, IISE Transactions m.fl.)
- Bøker og bokkapitler fra anerkjente forlag (Springer, Wiley, McGraw-Hill) der de er standardreferanser
- Publisert fra 1960 (seminal works) til 2024
- Engelskspråklig (primært), men nordiske og europeiske bidrag på norsk/skandinavisk er velkomne

**Ekskluder:**
- Ikke-fagfellevurderte blogposter, populærvitenskapelige artikler, grå litteratur
- Artikler om matvarekjeder, mote/sesong, eller andre domener uten overføringsverdi til kritisk beredskapslogistikk
- Artikler om *forecasting only* uten kobling til lagerdimensjonering
- Rene metaheuristikk-artikler (genetiske algoritmer, swarm) uten operasjonsanalytisk fundament

---

## STRUKTURERT OUTPUT — FORVENTET FORMAT

For **hver artikkel**, oppgi følgende:

```
### [Forfatternavn, År]
**Full referanse (APA 7):** ...
**Tidsskrift:** ...
**Kategori:** T1 / T2 / T3 / T4 / T5 / T6
**Type:** Grunnlagsartikkel / Metodeartikkel / Empirisk case / Review
**Hovedbidrag:** [2–4 setninger om hva artikkelen viser/beviser/foreslår]
**Relevans for oppgaven:** [1–2 setninger om direkte kobling til RogBR-problemet]
```

---

## AVSLUTTENDE INSTRUKSJON

Etter at du har listet alle artiklene, skriv et kortfattet **syntesenotat** (maks 300 ord) som:
1. Identifiserer de 8–10 artiklene du vurderer som **absolutt uunnværlige** for denne oppgaven
2. Peker på eventuelle **kunnskapshull** — aspekter av problemet som ser ut til å mangle god dekning i litteraturen
3. Foreslår **2–3 nøkkelartikler** som bør leses i sin helhet *før* modellvalget tas

Dette syntesenotatet vil brukes direkte i neste fase av prosjektet: valg av modelltilnærming og skriving av teorikapittelet.
