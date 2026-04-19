# 6. Modell

## 6.1 Modellutvikling og metodisk begrunnelse

Prosjektet gjennomgikk en metodisk utvikling i tre faser. Alle tre faser er dokumentert fordi utviklingen i seg selv er analytisk informativ: overgangen fra Erlang-C til prosedyrbasert modell er ikke et teknisk valg, men en konsekvens av at den operative virkeligheten ved 110-sentraler bryter med M/M/c-modellens kjerneforutsetning om uavhengige, parallelle servere.

| Fase | Modell | Målmetrikk | Konklusjon |
|---|---|---|---|
| 1 | Erlang-C (M/M/c) | P(W > t), ρ | ρ < 6 % for alle skifttyper — kapasiteten ser komfortabel ut |
| 2 | Simultanitetsanalyse | P(≥ k aktive hendelser simultant) | Lav konfliktrate — men makkerpar-logikk ikke inkludert |
| 3 | Prosedyrbasert ankomstkonfliktmodell | P(brudd på driftsstandard ved ankomst) | Strukturelt kapasitetsgap — **primærmodell** |

Overgangen fra Fase 1 til Fase 3 er ikke en forkasting av køteoretisk metode, men en utvidelse: modellen spesifiserer hva som faktisk er en «opptatt server» i 110-kontekst, og svarer på et mer presist spørsmål enn Erlang-C kan formulere.

Modellrammeverket er utviklet med 110 Sør-Vest som case, men er prinsipielt overførbart til enhver 110-sentral. Det sentrale er ikke de eksakte prosentverdiene i denne studien, men metoden for å identifisere hvor ofte en ny hendelse ankommer i en tilstand der tilgjengelig operatørkapasitet allerede er bundet. Andre sentraler kan anvende samme logikk dersom de har data for ankomsttidspunkt, ressursvarsling og en proxy for akuttfasens varighet.

---

## 6.2 Klassifisering av henvendelser etter operativ binding

Dimensjonering av nødmeldesentraler kan ikke baseres på samlet telefonvolum alene. Det avgjørende er hvor mange henvendelser som på et gitt tidspunkt binder operatørkapasitet på en måte som reduserer evnen til å håndtere nye prioriterte hendelser.

Klassifiseringen bruker tre felt fra BRIS i kombinasjon: `Oppdragstype` (sluttklassifisering), `Opprinnelig oppdragstype` (initiell hendelsestype) og `Kilde` (Alarm/Samtale/blank — innringingskanal). Alle 61 964 synlige oppdrag i 2025-datasettet klassifiseres i åtte kategorier. D-hendelser er delt i to undertyper fordi operativ prosedyre og makkerpar-krav skiller seg fundamentalt mellom pri-1-hendelser og ABA-utløst utrykning (se avsnitt 6.4.3–6.4.4).

| Kategori | Regel i BRIS | Antall (2025) | Andel |
|---|---|---|---|
| **D-pri1** (Pri-1-utrykning) | `Ressurs varslet` er ikke-tom ∧ ikke-(ABA + Alarm) | 4 499 | 7,3 % |
| **D-aba** (ABA-utløst utrykning) | `Ressurs varslet` ∧ `Opprinnelig` starter med «ABA» ∧ `Kilde = Alarm` | 3 056 | 4,9 % |
| **S** (Service) | `Oppdragstype = "Service"` | 22 542 | 36,4 % |
| **L-aba** (ABA løst av 110) | `Oppdragstype = "Oppdrag løst av 110"` ∧ `Opprinnelig = "ABA"` ∧ `Kilde = Alarm` | 3 430 | 5,5 % |
| **L-hendelse** (Reell hendelse løst av 110) | `Oppdragstype = "Oppdrag løst av 110"` ∧ `Opprinnelig` har verdi ∧ (≠ ABA ∨ `Kilde ≠ Alarm`) | 4 298 | 6,9 % |
| **L-ukjent** (Løst av 110, uklassifisert) | `Oppdragstype = "Oppdrag løst av 110"` ∧ `Opprinnelig` er tom | 16 768 | 27,1 % |
| **F** (Feilringing) | `Oppdragstype` ∈ {Nødanrop feilring, Ikke reell nødmelding, ECall feil bruk, ECall teknisk/ukjent, ECall veihjelp} | 6 824 | 11,0 % |
| **V** (Viderevarsling) | `Oppdragstype` inneholder «viderevarslet» eller «viderekoble» | 547 | 0,9 % |

**Kilde = Alarm-kravet for L-aba og D-aba:** Empirisk manuell gjennomgang av 50 L-aba-hendelser (LABA-dybdeanalyse, se avsnitt 5.4) viste at 24,5 % av oppdrag klassifisert med `Opprinnelig = ABA` faktisk ikke representerer automatisk brannalarm i operativ forstand — de omfatter publikumsmeldinger om brannalarm, private bygg uten 110-tilknytning, tester feilrevidert som oppdrag, og duplikatoppdrag. Kilde-feltet skiller hvordan hendelsen ankom 110: `Alarm` (ABA-signal), `Samtale` (publikumsinnringing), eller blank (operatør-initiert). Reell ABA har `Kilde = Alarm`. Ved å kreve dette for L-aba og D-aba sikres at klassifiseringen gjenspeiler operativ dynamikk, ikke registreringspraksis.

**Operativ beskrivelse av kategoriene:**

- **D-pri1 (Pri-1-utrykning):** Byggnings- og objektbrann, trafikkulykke, farlig gods og tilsvarende pri-1-hendelser. Gir makkerpar-binding (RØD + GUL parallelt), trippelvarsling, tidskritisk informasjon via BAPS. Bindingstid er databasert (se avsnitt 6.4.5).
- **D-aba (ABA-utløst utrykning):** Automatisk brannalarm som fører til ressurs varslet fordi avklaring ikke kom innen 90 sekunder. Ikke pri-1 — operatør oppretter oppdrag og utalarmerer serielt i ~3 min, uten makkerpar-krav (se avsnitt 6.4.6).
- **S (Service/overføringstest):** Servicetekniker ringer for overføringstest av brannalarmanlegg. Operatør mottar samtale i LEO, setter adresse om den ikke kommer automatisk, tar imot signal i alarmmottak, verifiserer mottatt signal til servicetekniker, venter til anlegget er i hvile, kvitterer ut testen og lukker som service.
- **L-aba (ABA løst av 110):** Automatisk brannalarm kommer inn og overføres til LEO. Operatør venter 90 sekunder. Dersom nødtelefon fra stedet mottas innen 90 sekunder og innringer bekrefter ufarlig årsak (f.eks. matlaging), lukkes oppdraget som «Oppdrag løst av 110». Bindingstiden er empirisk kalibrert til 6 min via LABA-dybdeanalysen (avsnitt 5.4). Uten nødtelefon innen fristen ville det ført til utrykning (kategori D-aba).
- **L-hendelse (Reell hendelse løst av 110):** Innringer melder noe reelt (røyklukt, branntilløp, ulykke), operatør vurderer og løser uten å sende ressurs. Inkluderer ABA-oppdrag med `Kilde = Samtale` (publikum rapporterer brannalarm uten ABA-signal).
- **L-ukjent (Løst av 110, uklassifisert):** Henvendelser som lukkes uten formell opprinnelig oppdragstype. Omfatter korte avklaringer (f.eks. bålregler), feilkategoriserte servicetester og andre henvendelser som ikke krever formell oppdragsopprettelse. Feltet `Opprinnelig oppdragstype` har 16 % dekning for hendelser uten utrykning — dette er ikke en datakvalitetsfeil, men en rasjonell arbeidsøkonomisk tilpasning der operatørene ikke bruker tid på å klassifisere korte henvendelser.
- **F (Feilringing):** Innringer har ringt feil nummer eller har en sak som ikke angår 110.
- **V (Viderevarsling):** Viderekobling til annen etat (politi/AMK) eller intern varsling.

I den foreliggende analysen kvantifiseres primært beredskapskategoriene D-pri1 og D-aba i primærmodellen (variant A, avsnitt 6.4). Den utvidede modellen (variant B, avsnitt 6.5) inkluderer alle åtte kategorier for å kvantifisere samlet operativ belastning. Bindingstider for ikke-D-kategorier er enten empirisk kalibrert (L-aba: LABA-dybdeanalyse, 6 min) eller operativt estimert og validert av vaktleder (S, L-hendelse, L-ukjent, F, V).

### Sentrale begreper: anrop, oppdrag og hendelse

En sentral metodisk distinksjon i analysen er skillet mellom **anrop**, **oppdrag** og **hendelse**:

- **Anrop:** En faktisk innkommende telefon eller varsling til sentralen. Hvert anrop opptar en operatør.
- **Oppdrag:** En registrert sak i LEO/BRIS. Flere anrop kan bli sammenstilt i ett oppdrag.
- **Hendelse:** Den faktiske operative situasjonen som sentralen håndterer. Én hendelse kan generere flere innkommende anrop fra ulike innringere.

I praksis kan én hendelse generere flere anrop, mens disse anropene i statistikken sammenstilles i ett eksisterende oppdrag. Operatørkapasitet bindes dermed av flere anrop enn det antall synlige oppdrag alene tilsier. Denne asymmetrien mellom synlige oppdrag og faktisk operatørbinding er et gjennomgående metodisk poeng i analysen (se avsnitt 7.2).

---

## 6.3 Fase 1: Erlang-C (M/M/c) — grunnlinje og begrensninger

### 6.3.1 Modellparametere

M/M/c-modellen (Erlang-C) er spesifisert med følgende parametere for 110 Sør-Vest:

| Symbol | Beskrivelse | Verdi / kilde |
|---|---|---|
| λ | Ankomstrate beredskapsanrop [anrop/time] | Estimert per skifttype fra LEO/BRIS 2025 |
| μ | Servicerate [anrop/time] = 1 / E[samtaletid] | Vektet gjennomsnitt: 3,44 min⁻¹ (intervjudata) |
| c_eff | Effektive servere = c_total − 1 (VL-korreksjon) | Dag/hverdag: 3; øvrige skift: 2 |
| ρ | Systemutnyttelse = λ / (c_eff · μ) | Se Tabell 6.1 |
| T | Terskel for P(W > T) | 30 sek (automatisk overføring til Agder — bekreftet beredskapsanalyse s. 25) |

**VL-korreksjon:** Vaktlederen (VL) besvarer normalt ikke nødanrop (jf. prosedyre, avsnitt 4.2). Effektiv operatørkapasitet er derfor c_eff = c_total − 1 for alle skifttyper.

### 6.3.2 Erlang-C-formelen

Sannsynligheten for at et innkommende anrop må vente i kø (Erlang-C):

$$C(c, A) = \frac{A^c / (c! \cdot (1-\rho))}{\sum_{k=0}^{c-1} A^k/k! + A^c / (c! \cdot (1-\rho))}$$

der A = λ/μ er total tilbudt trafikk i Erlang og ρ = A/c er serverutnyttelsen.

Sannsynlighet for ventetid over terskel T:

$$P(W > T) = C(c, A) \cdot e^{-(c\mu - \lambda)T}$$

### 6.3.3 Resultater og begrensninger

**Tabell 6.1: Erlang-C resultater — 110 Sør-Vest 2025**

| Skifttype | λ (anrop/t) | c_eff | ρ | C(c,A) | P(W > 60s) |
|---|---|---|---|---|---|
| Dag / Hverdag | 2,57 | 3 | 4,9 % | 0,05 % | 0,02 % |
| Dag / Helg | 2,06 | 2 | 5,9 % | 0,66 % | 0,38 % |
| Natt / Hverdag | 1,18 | 2 | 3,4 % | 0,22 % | 0,13 % |
| Natt / Helg | 1,30 | 2 | 3,7 % | 0,27 % | 0,15 % |

*λ inkluderer kun beredskapsoppdrag (non-T1). P(W > 30s): automatisk overføring til Agder ved ubesvart anrop etter 30 sek (beredskapsanalyse s. 25), eller ved 10. anrop i kø.*

Erlang-C konkluderer med svært lav kapasitetsutnyttelse og nær null sannsynlighet for ventetid over 30 sekunder i alle skifttyper. Formelt er dette korrekt — men det er metodisk utilstrekkelig for 110-konteksten av fire grunner:

1. **Makkerpar-prinsippet og samtidig binding:** Den operative prosedyren definerer to operatører (RØD + GUL) som standard for én hendelse. Både RØD og GUL bindes fra samme tidspunkt: så snart RØD-operatøren besvarer nødanropet, går GUL-operatøren i medlytt for å bygge situasjonsforståelse og avhjelpe med lokalisering før utalarmering. To operatører er dermed opptatt fra første sekund. Erlang-C modellerer én server per anrop og fanger ikke denne samtidige bindingen. Ved samtidskonflikter — der ingen dedikert makker er tilgjengelig — må én operatør fylle både RØD- og GUL-funksjonen alene.

2. **Kapasitetsbinding utover samtaletid:** GUL-operatøren er bundet gjennom hele akuttfasen: først i medlytt under RØD-samtalen, deretter i aktiv koordinering — utalarmering av ressurser, sambandskommunikasjon med mannskap underveis, og delvis fortsatt medlytt. GUL forblir bundet frem til vindusmelding mottas om at første ressurs er fremme på stedet, pluss kvittering og loggføring (anslagsvis 3 minutter). Først etter dette er GUL delvis frigjort og kan håndtere flere gule hendelser parallelt i en mer sporadisk oppfølgingsfase. Denne totale bindingsperioden er vesentlig lenger enn selve samtaletiden, men Erlang-C behandler den som null.

3. **Uavhengige servere:** M/M/c forutsetter at servere er uavhengige. I 110-kontekst er operatørene dynamisk koblet gjennom prosedyrens rollestruktur — RØD og GUL er komplementære, ikke parallelle. Rollene er ikke faste: ved neste hendelse roterer operatørene, og den som nettopp var GUL kan bli RØD på neste anrop.

4. **Undervurdert ankomstrate:** Ankomstraten λ estimeres fra synlige oppdrag i BRIS/LEO. Som dokumentert i avsnitt 7.2 undervurderer dette faktisk innkommende anropsvolum med anslagsvis 23 %, fordi tilleggsanrop til eksisterende hendelser sammenstilles automatisk og ikke registreres som egne oppdrag. Dette innebærer at Erlang-C ikke bare undervurderer antall innkommende belastningsenheter, men også bygger på en datadefinisjon der én synlig sak kan skjule flere samtidige kapasitetsbindende anrop. Selv en perfekt M/M/c-modell ville derfor vært basert på et ufullstendig inputgrunnlag.

Konsekvensen er at Erlang-C gir et misvisende bilde av kapasitetstilstanden: en modell som sier «nesten ingen ventetid» er lite operasjonelt informativ i et system der det operative problemet ikke er kø i klassisk forstand, men mangel på ledig makker ved ankomst av ny hendelse.

---

## 6.4 Fase 3: Prosedyrbasert ankomstkonfliktmodell — primærmodell

### 6.4.1 Konseptuell ramme

Primærmodellen tar utgangspunkt i prosedyrens kapasitetslogikk og stiller et presist spørsmål:

> *I hvilken andel av beredskapsanropene ankommer anropet i en tilstand der den operative driftsstandarden (makkerpar) kan opprettholdes?*

Dette er en **prosedyrkonformitetsmetrikk** — ikke et ventetidsmål. Kapasitetsproblemet ved 110-sentraler er i de fleste tilfeller ikke at anrop venter i kø, men at de ankommer når operatørene allerede er bundet i aktive hendelser slik at makkerpar-prinsippet brytes.

### 6.4.2 Op-binder-semantikk

Modellens kjerne er *op-binder-semantikk*: hver hendelse genererer én eller flere op-binder-events, hvert med tre attributter:

- **Ankomsttidspunkt** $t$
- **Bindingstid** $d$ (minutter)
- **Operatører bundet** $q \in \{1, 2\}$

Ulike hendelsestyper binder ulike antall operatører. Pri-1-utrykning (D-pri1) krever makkerpar — to operatører bindes parallelt fra første sekund. ABA-utrykning (D-aba) og alle andre kategorier krever ikke makkerpar — én operatør håndterer serielt. Denne distinksjonen er forankret i prosedyre og operatørintervjuer (se avsnitt 4.2 og 5.3).

Sweep-algoritmen akkumulerer *antall aktive op-binder* ved hvert nytt ankomsttidspunkt:

$$n_{\text{aktive}}(t_i) = \sum_{j < i : t_j + d_j > t_i} q_j$$

Antall ledige operatører:

$$\text{ledige}(t_i) = c_{\text{eff}} - n_{\text{aktive}}(t_i)$$

### 6.4.3 Kapasitetsnivåer

Basert på antall ledige operatører klassifiseres hvert innkommende beredskapsanrop til ett av tre nivåer:

**Tabell 6.2: Kapasitetsnivåer — operativ tilpasningsmodell**

| Nivå | Definisjon | Betingelse | Operativ konsekvens |
|---|---|---|---|
| **Normal** | Makkerpar mulig for neste hendelse | ledige ≥ 2 | Full prosedyre, kvalitetssikret håndtering |
| **Brudd på driftsstandard** | Kun 1 ledig — solo-håndtering | ledige = 1 | Operatøren klarer det, men uten makker. Økt kognitiv belastning, økt feilrisiko |
| **Svikt** | Ingen ledig operatør | ledige ≤ 0 | VL må overta eller overløp til Agder |

For å illustrere hva dette innebærer i praksis med c_eff = 2 (natt/helg):

| Tilstand | Eksempel aktive events | n_aktive | ledige | Nivå |
|---|---|---:|---:|---|
| Tomt | Ingen | 0 | 2 | Normal |
| 1 D-aba Fase 1 | D-aba binder 1 op i 3 min | 1 | 1 | Brudd |
| 1 D-pri1 | D-pri1 binder 2 ops i 14 min | 2 | 0 | Svikt |
| 2 D-aba | To D-aba serielt (2 × 1 op) | 2 | 0 | Svikt |

**Asymmetri c=2 vs c=3:** Med c_eff = 2 er én D-pri1-hendelse nok til å tømme all operatørkapasitet — neste beredskapsanrop i samme tidsvindu ankommer i Svikt. Med c_eff = 3 forblir én operatør ledig selv under en aktiv D-pri1, slik at pri-1-hendelser gir Brudd (ikke Svikt) for neste ankomst.

### 6.4.4 D-pri1: makkerpar-binding

Pri-1-hendelser følger prosedyrens RØD-GUL-rolle fra første sekund:

- **0–~1 min:** RØD i samtale med innringer, GUL i medlytt og lokalisering
- **~1–~2 min:** GUL utalarmerer ressurser (median 83 sek fra anrop til ressurs varslet), RØD fortsetter samtalen
- **~2–~11 min:** RØD i fortsatt innringerkontakt, GUL koordinerer samband og gir tidskritisk informasjon via BAPS
- **~11 min:** Første ressurs fremme → vindusmelding
- **+3 min:** Kvittering og loggføring → GUL delvis frigjort

Både RØD og GUL er bundet parallelt gjennom hele akuttfasen. Bindingstid per D-pri1 beregnes databasert som:

$$d_{\text{D-pri1}} = (T_{\text{første ressurs fremme}} - T_{\text{anrop}}) + 3 \text{ min kvittering}$$

For 4 499 D-pri1-hendelser i 2025 er median 14,1 min (P25 = 11,2, P90 = 27,3). De 25 % av D-pri1 som mangler tidspunkt for første ressurs fremme tildeles median.

**D-pri1 i sweep:** Hver D-pri1-hendelse genererer én op-binder-event med $q = 2$, $d = d_{\text{D-pri1}}$, ankomst $t$.

### 6.4.5 D-aba: serielt solo-håndtert med valgfri oppfølging

ABA-utrykning er ikke pri-1. Prosedyren krever ikke makkerpar fordi ABA ikke trippelvarsles, det gis ikke tidskritisk informasjon i BAPS, og operatøren som kvitterer alarmen er normalt den samme som oppretter oppdraget og utalarmerer ressurser. D-aba modelleres derfor i to faser:

**Fase 1 — oppdragsopprettelse og call-out (alltid)**
Én operatør kvitterer ABA-signalet, oppretter oppdrag i LEO og utalarmerer ressurser. Empirisk fra BRIS 2025: median 74 sek fra anrop til ressurs varslet (P75 = 80, P90 = 111). Med påfølgende registrering estimeres Fase 1 til:

$$d_{\text{D-aba, Fase 1}} = 3 \text{ min}, \quad q = 1$$

**Fase 2 — nødtelefon og panel-veiledning (valgfri)**
Etter call-out kommer ofte en nødtelefon fra stedet. Denne besvares av vilkårlig ledig operatør og inneholder intervju med innringer, veiledning til brannpanel, områdeavklaring, eventuelt tilbakestilling av alarm. Fase 2 modelleres stokastisk:

- Sannsynlighet $p$ for at Fase 2 forekommer (hoved: $p = 0{,}50$)
- Bindingstid $Y$ for Fase 2 når den forekommer (hoved: $Y = 6$ min)
- Fase 2 starter 90 sekunder etter Fase 1 (= 1,5 min offset)

$$d_{\text{D-aba, Fase 2}} = Y, \quad q = 1, \quad t_{\text{Fase 2}} = t + 1{,}5 \text{ min}$$

For reproduserbarhet brukes fast random seed til å velge hvilke D-aba som får Fase 2.

**Empirisk grunnlag for p:** Sekvensgap-metoden gir underkant-estimat på 8,7–37 % for tidsvindu 3–15 min etter D-aba. Estimatet er underkant fordi nødtelefoner logget *inni* hovedoppdraget (uten eget 110-ID) er usynlige. Operatørens kvalitative beskrivelse («ofte kommer det nødtelefon etter call-out») og empirisk observasjon tilsier reell andel 40–60 %, som støtter hovedcase $p = 0{,}50$.

**Sensitivitetsspenn:** Lav ($p = 0{,}30$, $Y = 3$), hoved ($p = 0{,}50$, $Y = 6$), høy ($p = 0{,}70$, $Y = 10$).

### 6.4.6 Sammenstilte tilleggsanrop

**Skjulte/sammenstilte anrop** — anrop som automatisk knyttes til eksisterende oppdrag i LEO/BRIS og ikke registreres som egne saker — identifiseres gjennom gap i sekvensnummereringen i 110_ID-feltet. Hvert synlige oppdrag har et daglig sekvensnummer (f.eks. B06-250101-4, B06-250101-6). Manglende sekvensnumre representerer anrop som ble sammenstilt med et eksisterende oppdrag.

For 2025 er det identifisert 18 901 sammenstilte anrop (korreksjonsfaktor 1,305×). I modellen behandles de som op-binder-events med:

$$t = \text{interpolert fra nærmeste synlige oppdrag}, \quad d = 1 \text{ min}, \quad q = 1$$

Bindingstiden på 1 min er et konservativt estimat. Faktisk varighet kan være kortere (20–30 sek ved ren bekreftelse) eller lenger (dersom innringer er stresset). Selv kort bindingstid har operativ konsekvens — operatøren er utilgjengelig for neste hendelse i det kritiske vinduet.

### 6.4.7 Matematisk formulering

La $\mathcal{E} = \{(t_i, d_i, q_i)\}_{i=1}^{N}$ være mengden av op-binder-events generert fra alle hendelser, sortert etter $t$.

For hvert beredskapsanrop (D-pri1-ankomst, D-aba-ankomst, eller skjult anrop) beregnes:

$$n_{\text{aktive}}(t_i) = \sum_{j < i : t_j + d_j > t_i} q_j$$

Kapasitetsnivå:

$$\text{Nivå}(i) = \begin{cases}
\text{Normal} & \text{hvis } c_{\text{eff}} - n_{\text{aktive}}(t_i) \geq 2 \\
\text{Brudd} & \text{hvis } c_{\text{eff}} - n_{\text{aktive}}(t_i) = 1 \\
\text{Svikt} & \text{hvis } c_{\text{eff}} - n_{\text{aktive}}(t_i) \leq 0
\end{cases}$$

Events per hendelsestype:

| Kategori | Events per hendelse | $q$ | $d$ |
|---|---|---:|---|
| D-pri1 | 1 | 2 | Observert fra BRIS (median 14,1 min) |
| D-aba | 1 alltid + 1 med sannsynlighet $p$ | 1 | Fase 1: 3 min / Fase 2: $Y$ min |
| L-aba | 1 | 1 | 6 min (LABA-kalibrert) |
| L-hendelse | 1 | 1 | 5 min |
| L-ukjent | 1 | 1 | 3 min |
| S | 1 | 1 | 2 min |
| F | 1 | 1 | 0,5 min |
| V | 1 | 1 | 1 min |
| Skjult | 1 | 1 | 1 min |

### 6.4.8 Hva modellen måler — og hva den ikke måler

Modellen måler **P(brudd på driftsstandard ved ankomst)**: sannsynligheten for at et beredskapsanrop ankommer i en tilstand der makkerpar-driftsstandarden ikke kan opprettholdes.

Dette er ikke det samme som:
- P(ingen svarer) — noen svarer i nesten alle tilfeller
- P(W > t) i Erlang-C-forstand — tradisjonell ventetid i kø
- P(kapasitetskollaps) — systemet kollapser sjelden totalt

Det er en **operasjonell prosedyrmetrikk** som speiler 110-operatørenes erfarte kapasitetsproblem: ikke at anrop forblir ubesvarte, men at de besvares under betingelser der den operative standarden for korrekt og trygg hendelseshåndtering ikke er oppfylt.

### 6.4.9 Modellens konservatisme

Modellen gir sannsynligvis et **konservativt anslag** på faktisk operativ belastning:

1. **Ikke-D-kategorier er ikke inkludert i variant A.** Reelle hendelser uten utrykning (L-hendelse), ABA-avklaringer (L-aba), servicetester (S) og øvrige kategorier binder også operatørkapasitet, men er ikke modellert i primærmodellen. Variant B (avsnitt 6.5) adresserer dette.
2. **Imputering med median for D-pri1.** De ~25 % av D-pri1-hendelsene som mangler tidspunkt for første ressurs fremme er tildelt median bindingstid — dette kan undervurdere de tyngre hendelsene.
3. **Kun akuttfasen er modellert for D-pri1.** Mange hendelser binder operatørkapasitet lenger gjennom oppfølging, samband og loggføring.
4. **Sammenstilte anrop antas 1 minutt.** Faktisk varighet kan være lenger dersom innringer trenger mer avklaring.
5. **D-aba Fase 2-sannsynlighet er underkant-estimert.** Sekvensgap-metoden fanger kun nødtelefoner med eget 110-ID. Nødtelefoner logget inni hovedoppdraget er usynlige. Hoved-scenario ($p = 0{,}50$) kompenserer delvis, men tung sensitivitet mot $p$ er undersøkt i avsnitt 7.7.3.
6. **Feilkategoriserte tilleggsanrop.** Under høyt press hender det at anrop som operativt tilhører en pågående hendelse lukkes som egne saker med ikke-beredskapsrelevant hendelsestype (service, feilringing, løst av 110). Estimatet på 18 901 sammenstilte anrop er derfor sannsynligvis underestimat.

Begrensningene trekker i hovedsak i én retning: mot undervurdering. Resultatene bør leses som et minimumsanslag på brudd- og sviktrisiko, ikke som et maksimumsanslag.

---

## 6.5 Utvidet modell: total operativ belastning (variant B)

### 6.5.1 Motivasjon

Primærmodellen (avsnitt 6.4) kvantifiserer kapasitetsnivå kun for beredskapskategoriene (D-pri1, D-aba og sammenstilte anrop) — til sammen 27 960 op-binder-events av ca. 82 000 i variant B. De resterende ~54 000 op-binder-events representerer henvendelser som ikke utløser utrykning, men som likevel binder operatørkapasitet: overføringstester, ABA-avklaringer, rådgivning, feilringing og viderevarsling. Å la denne belastningen forbli ukvantifisert ville innebære at prosjektet, som eksplisitt søker å erstatte kvalitative ROS-vurderinger med kvantitativ analyse, etterlater den største delen av arbeidsvolumet som en kvalitativ kommentar.

Variant B bruker **samme sweep-algoritme** som primærmodellen, men utvider belastningsgrunnlaget til å inkludere alle 61 964 synlige oppdrag pluss 18 901 sammenstilte anrop. De to variantene besvarer ulike spørsmål:

| Variant | Belastningsenheter | Spørsmål |
|---|---|---|
| **A (primær)** | D-pri1 + D-aba (Fase 1+2) + sammenstilte (27 960 events) | Kan driftsstandard opprettholdes for beredskapsoppdrag? |
| **B (utvidet)** | Alle kategorier + sammenstilte (~82 000 events) | Hvor opptatt er operatørene faktisk gjennom skiftet? |

### 6.5.2 Bindingstidsestimater

Bindingstiden for D-pri1 er databasert (avsnitt 6.4.4). L-aba er empirisk kalibrert via LABA-dybdeanalysen (avsnitt 5.4). D-aba Fase 1 bygger på operativ prosedyre (avsnitt 4.2). D-aba Fase 2 ($p$, $Y$) og øvrige ikke-D-kategorier (S, L-hendelse, L-ukjent, F, V) er operative estimater forelagt vaktleder ved 110 Sør-Vest for validering (se Vedlegg X).

Fordi mange av estimatene er antakelser snarere enn målinger, kjøres modellen med tre scenarioer:

| Kategori | Lavt | Hovedscenario | Høyt |
|---|---|---|---|
| D-pri1 | Databasert | Databasert | Databasert |
| D-aba Fase 1 | 3 min | 3 min | 3 min |
| D-aba Fase 2 ($p$, $Y$) | 0,30, 3 min | 0,50, 6 min | 0,70, 10 min |
| L-aba | 3 min (konservativ) | 6 min (LABA-mean) | 9 min (P90-nært) |
| L-hendelse | 3 min | 5 min | 8 min |
| L-ukjent | 1 min | 3 min | 5 min |
| S (Service) | 1 min | 2 min | 4 min |
| F (Feilringing) | 15 sek | 30 sek | 1 min |
| V (Viderevarsling) | 30 sek | 1 min | 2 min |

**Antagelse 6.1:** Bindingstidsestimatene representerer gjennomsnittlig tid operatøren er opptatt med hendelsen, inkludert LEO-arbeid og etterarbeid. Konsekvens: estimatene er usikre, men sensitivitetsanalysen (avsnitt 7.7) viser at hovedfunnet er robust over hele spennet lav–høy.

### 6.5.3 Algoritmisk identitet med primærmodellen

Variant B bruker nøyaktig samme sweep-algoritme som variant A (avsnitt 6.4.7). Eneste forskjell er at belastningsgrunnlaget utvides fra D-pri1 + D-aba + sammenstilte til alle kategorier + sammenstilte, med kategori-spesifikk bindingstid og op-binder-tall. Kapasitetsnivåene (Normal/Brudd/Svikt) og c_eff-verdiene er identiske.

---

## 6.6 Implementasjon

Begge modellene er implementert i Python. Erlang-C er beregnet med scipy.special og numpy. Ankomstkonfliktmodellen bruker en sweep-algoritme over sorterte op-binder-events som gir O(N) kompleksitet for sweep-en over N events (pluss O(N log N) for sortering).

Hovedlogikken: hver hendelse ekspanderes til én eller flere op-binder-events. D-pri1 gir ett event med $q = 2$. D-aba gir Fase 1 alltid ($q = 1$, 3 min) pluss Fase 2 med sannsynlighet $p$ ($q = 1$, $Y$ min, offset 1,5 min). Øvrige hendelser gir ett event med $q = 1$. Sweep-en akkumulerer aktiv op-binder ved hver ankomst.

```python
# Pseudokode — op-binder-semantikk
def ekspander_events(hendelse, scenario):
    """Konverter én hendelse til én eller flere op-binder-events."""
    if hendelse.kategori == "D-pri1":
        return [Event(t=hendelse.t, d=hendelse.bind_D, q=2)]
    if hendelse.kategori == "D-aba":
        events = [Event(t=hendelse.t, d=3.0, q=1)]  # Fase 1 alltid
        if rng.random() < scenario["daba_p"]:
            events.append(Event(t=hendelse.t + 1.5, d=scenario["daba_Y"], q=1))
        return events
    # Alle andre: 1 op-bind
    return [Event(t=hendelse.t, d=scenario[hendelse.kategori], q=1)]

def sweep_opbinder(events, c_eff):
    """Sorter events etter ankomst. Akkumuler aktiv op-binder."""
    events = sorted(events, key=lambda e: e.t)
    aktive = []  # liste av (slutt_ts, q) for pågående events
    for e in events:
        aktive = [(s, q) for s, q in aktive if s > e.t]  # fjern utløpte
        n_aktive = sum(q for _, q in aktive)
        ledige = c_eff - n_aktive
        if ledige >= 2:
            nivå = "Normal"
        elif ledige == 1:
            nivå = "Brudd"
        else:
            nivå = "Svikt"
        aktive.append((e.t + e.d, e.q))
        yield e, n_aktive, nivå
```

Modellen er implementert i `analyse/scripts/konflikt_total_belastning.py`. Scenario +1 operatør bruker samme logikk med doblede c_eff-verdier (`analyse/scripts/scenario_pluss1.py`). Parameterkalibrering og beslutningsgrunnlag er dokumentert i `analyse/notat_V3_modellutvikling.md`.

Kildekode og Jupyter notebooks er versjonskontrollert på GitHub (se Vedlegg A).
KI-verktøy benyttet i implementasjonsfasen er dokumentert i Vedlegg D.

---

*Kap 6 — Versjon 3.1 | Sist oppdatert: 2026-04-19 (V3 op-binder-semantikk, D-pri1/D-aba-splitt)*
