# Tilleggssøk litteratur — LOG650 G20 Rune Grødem
## Fokusert deep research-prompt for ChatGPT, april 2026

---

## Formål med dette dokumentet

Dette er en **fokusert tilleggsprompt** til en allerede gjennomført litteraturkartlegging i prosjektet LOG650 (Høgskolen i Molde, vår 2026). Det første søket dekket kanonisk køteori, EMS call center-modellering og norsk regulering. Etter å ha utviklet primærmodellen har det oppstått et behov for mer presis litteratur på et avgrenset område.

**Du skal IKKE gjenta søk som allerede er dekket** (se seksjon 4 for hva vi har). Du skal **fokusere på de spesifikke gapene i seksjon 5**.

Format på svar: Følg malen i seksjon 7. Verifiser alle DOI-er, årstall og artikkelnumre — feil i forrige runde forsinket arbeidet.

---

## 1. Prosjektkontekst (kort versjon)

### Problemstilling
> *I hvilken grad samsvarer faktisk bemanning ved norske 110-sentraler med kapasitetsbehovet beregnet fra historiske hendelsesdata og køteoretiske modeller?*

### Case
**110 Sør-Vest** — én av tolv norske 110-sentraler (nødmeldesentral for brann/redning). Dekker Rogaland og deler av Vestland/Agder, ca. 555 000 innbyggere. Bemanning: 4 operatører + vaktleder på dag/hverdag, 3 operatører + vaktleder på natt/helg.

### Operativ kontekst som driver problemstillingen
- **Vaktleder besvarer normalt ikke nødanrop** → effektiv operatørkapasitet `c_eff = c_total − 1` (3 på dag hverdag, 2 ellers)
- **Makkerpar er driftsstandard:** Prosedyren krever to operatører per beredskapshendelse — én RØD (besvarer anropet) og én GUL (medlytt, utalarmering, samband). Begge er bundet parallelt fra første sekund i akuttfasen.
- **Solo-drift som degradert tilstand:** Når et nytt anrop kommer mens makkerparet er bundet, splittes makkerparet og operatørene jobber solo. Dette er ikke prosedyremessig riktig, men daglig praksis under press.
- **Bindingstid medianen 13 minutter** for beredskapsoppdrag — vesentlig lenger enn samtaletiden (3,4 min) fordi GUL er bundet til vindusmelding mottas (første ressurs fremme).

### Problemstillingens unike vinkling
Dimensjoneringsforskriften (FOR-2023-01-06-23) gir nasjonale kvantitative bemanningskrav for brannvesenet basert på innbyggertall og responstid. Ingen tilsvarende standard finnes for 110-operatører — bemanning fastsettes lokalt gjennom kvalitative ROS-analyser. Vårt prosjekt forsøker å lage et **kvantitativt referansepunkt** som kan supplere ROS — analogt med dimensjoneringsforskriftens rolle for brannstasjoner.

---

## 2. Modellutvikling — fra Erlang-C til prosedyrbasert ankomstkonflikt

### Fase 1: Erlang-C (M/M/c) som grunnlinje
Resultat: ρ < 6 % for alle skifttyper. P(ventetid > 30 sek) < 0,5 %.
Konklusjon: **Formelt korrekt, men metodisk utilstrekkelig.** Erlang-C antar uavhengige servere, fanger ikke makkerpar-binding, og baserer seg på undervurdert ankomstrate (synlige oppdrag).

### Fase 3: Prosedyrbasert ankomstkonfliktmodell (PRIMÆRMODELL)
For hvert beredskapsanrop klassifiseres kapasitetsnivå basert på antall aktive hendelser ved ankomsttidspunktet:

| Nivå | Definisjon | c_eff = 2 (natt/helg) | c_eff = 3 (dag) |
|---|---|---|---|
| **Normal** | Makkerpar mulig (ledige ≥ 2) | n_aktive = 0 | n_aktive ≤ 1 |
| **Brudd på driftsstandard** | Solo-håndtering (ledige = 1) | n_aktive = 1 | n_aktive = 2 |
| **Svikt** | Ingen ledig (ledige ≤ 0) | n_aktive ≥ 2 | n_aktive ≥ 3 |

Modellen måler **andel anrop i hver tilstand** — ikke ventetid. Den måler operasjonell prosedyrkonformitet, ikke kø-stabilitet.

Resultat (med sammenstilte tilleggsanrop): På natt/helg (c=2) er kun 48 % i Normal og 23,5 % i svikt.

---

## 3. Hva som skiller prosjektet fra eksisterende litteratur

Den spesifikke metodiske vridningen er:

1. **Servere er ikke uavhengige** — de er prosedyremessig parret (RØD/GUL) og bundet parallelt
2. **Bindingstid ≠ samtaletid** — kapasiteten er låst gjennom hele akuttfasen
3. **Solo-drift modelleres som "degradert" i stedet for "okay"** — kvalitet faller når makker mangler, men anropet besvares fortsatt
4. **Måleenheten er prosedyrkonformitet, ikke ventetid** — vi måler andel anrop som ankommer i en tilstand der prosedyren kan opprettholdes
5. **Sekvensgapanalyse i 110_ID-feltet** brukes til å identifisere skjulte/sammenstilte tilleggsanrop som ikke er synlige i registerdata (gir 23 % korreksjon på ankomstvolum)

Disse fem grepene utgjør prosjektets bidrag. Punkt 1, 3, og 4 er direkte koblet til **team-basert kapasitet og prosedyrkonformitet** — der vi tror litteraturen er svakest.

---

## 4. Hva vi allerede har — IKKE søk etter dette

### A. Klassisk køteori og call center
- Gans, Koole & Mandelbaum (2003) — kanonisk tutorial
- Brown et al. (2005) — statistisk analyse av call center
- Halfin & Whitt (1981) — heavy traffic limits
- Koole & Mandelbaum (2002) — intro to queueing models
- Garnett, Mandelbaum & Reiman (2002) — Erlang-A og square-root staffing
- Green, Kolesar & Whitt (2007) — time-varying staffing
- Feldman, Mandelbaum, Massey & Whitt (2008) — ISA-algoritmen
- Wallace & Whitt (2005) — skill-based routing
- Ibrahim, Ye, L'Ecuyer & Shen (2016) — forecasting survey
- Shen & Huang (2008) — Poisson-SVD forecasting

### B. EMS / nødmeldesentral kapasitet
- Gustavsson (2018) — lic-thesis SOS Alarm, burst + agent + regional kunnskap
- L'Ecuyer, Gustavsson & Olsson (2018) — burst-modell SOS Alarm
- van Buuren et al. (2017) — function differentiation EMS
- Dwars (2013) — capacity planning, sammenslåing 21→10 nederlandske sentraler
- Matteson et al. (2011) — EMS forecasting Toronto
- Restrepo, Henderson & Topaloglu (2009) — Erlang-loss for ambulanseutsetting

### C. Norsk og nordisk regulering/kontekst
- Brann- og redningsvesenforskriften (FOR-2021-09-15-2755)
- Dimensjoneringsforskriften (FOR-2023-01-06-23)
- DSB Brannstudien (2013)
- DSB Melding om brannvernet (årsrapporter 2022–2025)
- St.meld. 41 (2000–2001) brann- og eksplosjonsvern
- Meld. St. 16 (2023–2024) brann- og redningsvesenet
- Prop. 15 L (2022–2023) — fagskole brann
- RISE Fire Research (2017) — utredning brannvesenets dimensjonering
- KoKom (2012) — sluttevaluering SAMLOK
- Kunnskapssenteret/FHI (2012) — effekt av felles nødnummer
- Interdep. arbeidsgruppe (2009) — fremtidig organisering nødmeldetjenesten
- NENA STA-020.1-2020 — 9-1-1 call processing standard

### D. Kjente kilder med mangelfull verifikasjon (vurderer å laste ned)
- Aksin, Armony & Mehrotra (2007) — modern call center review
- Mandelbaum & Zeltyn (2005) — M/M/n+G asymptotikk
- Whitt (1996) — server staffing time-varying
- Larson (1974) — hypercube model
- Jouini, Dallery & Nait-Abdallah (2008) — team-based call center
- Kim, Lee, Dudin & Klimenok (2008) — cooperation of servers
- Ellensen et al. (2023) — Swedish EMDC ability to answer
- Rehn et al. (2021) — dispatch accuracy Norway

---

## 5. GAPENE — det er DETTE du skal søke etter

### Gap 1: Team-basert kapasitet i nødmeldesentraler ⭐ HØYESTE PRIORITET

**Søkestreng-forslag:**
- `"buddy system" dispatcher emergency`
- `"two-person rule" emergency communications`
- `paired dispatcher protocol`
- `team-based call center capacity`
- `dual-operator emergency dispatch`
- `co-operating servers queueing`

**Hva vi leter etter:**
- Studier som modellerer to operatører som samarbeider om én hendelse
- Empiri fra sentraler som faktisk bruker makkerpar-prosedyrer
- Kø-modeller med "cooperating servers" / "paired servers"
- Teori om hvordan team-basert organisering påvirker kapasitet

**Hvorfor:** Vi tror Jouini et al. (2008) og Kim et al. (2008) er de eneste eksisterende, men vi vil verifisere at vi ikke har oversett nyere arbeid (2018–2026) på dette spesifikke temaet.

---

### Gap 2: Prosedyrkonformitet og degradert drift ⭐ HØYESTE PRIORITET

**Søkestreng-forslag:**
- `"degraded mode" operations call center`
- `"degraded mode" emergency dispatch`
- `procedure deviation safety-critical communication`
- `protocol compliance dispatcher under load`
- `SOP violation emergency operator`
- `degraded operations safety culture dispatch`

**Hva vi leter etter:**
- Studier som måler hvor ofte operatører avviker fra prosedyre under belastning
- Modeller for "degraded mode" / "graceful degradation" i sikkerhetskritiske kommunikasjonssystemer
- Empiri på prosedyrkonformitet i 911/112/110-sammenheng
- Kobling mellom prosedyrbrudd og kvalitet/utfall

**Hvorfor:** Vår modell måler "brudd på driftsstandard" som en operativ tilstand. Vi trenger litteratur som rammer dette inn teoretisk (resilience engineering, normal accidents, procedure compliance).

---

### Gap 3: Kognitiv belastning og solo-operatør-håndtering

**Søkestreng-forslag:**
- `cognitive workload solo dispatcher`
- `cognitive load emergency call taker`
- `dispatcher fatigue error rate`
- `single-operator multitasking emergency`
- `mental workload PSAP operator`

**Hva vi leter etter:**
- Studier som måler kognitiv belastning ved solo-operatør-arbeid vs makkerpar
- Empiri på feilrater under høyt press
- Direkte sammenlignende studier (alene vs to)

**Hvorfor:** Vi argumenterer at solo-drift øker feilrisiko. Vi trenger litteratur som understøtter denne påstanden empirisk, ikke bare anekdotisk.

---

### Gap 4: Ny forskning 2023–2026 på nødmeldesentral-bemanning

**Søkestreng-forslag:**
- `911 dispatcher staffing 2024 OR 2025`
- `PSAP staffing model 2023..2026`
- `emergency communications workforce planning recent`
- `AI machine learning dispatch staffing`
- `post-pandemic emergency call center staffing`

**Hva vi leter etter:**
- Helt fersk forskning som bygger på eller utfordrer Gustavsson/Dwars/L'Ecuyer
- Pandemi-effekter på dispatch-bemanning
- AI/ML-modeller for prognose og bemanning
- Reviews og meta-analyser fra de siste 2–3 årene

**Hvorfor:** Klassisk litteratur er fra 2002–2018. Vi vil dekke 2023–2026 for å sikre at vi ikke har gått glipp av nye paradigmer eller funn.

---

### Gap 5: Sammenstilte/relaterte anrop (call surge / aggregation)

**Søkestreng-forslag:**
- `call aggregation emergency dispatch`
- `duplicate call handling 911`
- `multiple callers single incident`
- `call surge emergency communications`
- `correlated arrivals call center`

**Hva vi leter etter:**
- Hvordan andre studier håndterer at flere innringere ringer om samme hendelse
- Metoder for å estimere "skjulte" anrop som ikke registreres som egne saker
- Burst-modeller utover L'Ecuyer/Gustavsson

**Hvorfor:** Vår sekvensgap-metode for å identifisere sammenstilte anrop kan ha presedens i litteraturen som vi ikke kjenner til.

---

### Gap 6: Norsk og nordisk dispatch-litteratur 2020–2026

**Søkestreng-forslag:**
- `nødmeldesentral kapasitet dimensjonering`
- `110-sentral bemanning analyse`
- `AMK 113 staffing Norway`
- `SOS Alarm capacity 2023..2026`
- `Nordic emergency communications staffing`

**Hva vi leter etter:**
- Nyere norske/nordiske studier på dispatch-bemanning som vi ikke har funnet
- Masteroppgaver, lisensiatavhandlinger, RISE/SINTEF-rapporter
- Politidirektoratet/Helsedirektoratet-rapporter på 112/113

**Hvorfor:** Vi har god dekning av internasjonal litteratur, men nordisk-spesifikk forskning er sparsom. Det styrker generaliserbarheten til norsk kontekst hvis vi finner mer.

---

## 6. Hva du IKKE skal gjøre

- ❌ **Ikke gjenta søk på generelle Erlang-C eller call center-tema** — vi har dekket dette
- ❌ **Ikke ta med PR-/blogg-kilder eller white papers** uten akademisk vekt (med unntak av offentlige rapporter fra DSB/NENA/lignende)
- ❌ **Ikke fabrikker DOI-er eller artikkelnumre** — feil i forrige runde forsinket arbeidet
- ❌ **Ikke ta med kilder uten verifiserbar URL eller DOI**
- ❌ **Ikke ta med kilder eldre enn år 2000** med mindre de er klassiske og direkte relevante for et av de seks gapene

---

## 7. Format på svar

For hver kilde du foreslår, bruk dette formatet:

```markdown
### [Forfatter(e), år]

**Tittel:** [tittel]
**Tidsskrift/utgiver:** [tidsskrift, volum, sider eller utgiver/rapportnummer]
**DOI/URL:** [verifiserbar lenke]
**Gap dekket:** [Gap 1 / Gap 2 / ... — bruk numrene fra seksjon 5]
**Relevans for prosjektet (2–4 setninger):** [hvorfor denne kilden er nyttig — vær spesifikk om hvordan den knyttes til vår problemstilling, modell eller diskusjon]
**Type:** [empirisk studie / modellutvikling / review / regulatorisk dokument / metaanalyse]
**Tilgang:** [open access / behind paywall / preprint / institusjonell tilgang]
**Sitatpotensiale:** [hvor i rapporten dette mest sannsynlig brukes — kap 2 litteratur / kap 3 teori / kap 8 diskusjon]
```

Etter listen, oppsummer:
- Antall kilder funnet per gap
- Eventuelle gap som var vanskelige å fylle (og hvorfor)
- Kilder du anser som **mest verdifulle** (topp 3–5)
- Forslag til søkestrenger som ikke var i seksjon 5, men som ga gode treff

---

## 8. Verifiseringskrav

Før du leverer listen:

1. **Verifiser hver DOI** ved å sjekke at den faktisk eksisterer (crossref.org eller doi.org)
2. **Verifiser årstall** mot tidsskriftets metadata
3. **Verifiser artikkel/sidenummer** der relevant
4. **Marker alle usikre opplysninger** med ⚠️ og forklar hva som ikke ble bekreftet

---

## 9. Avsluttende kontekst

Prosjektet skal leveres 31. mai 2026 med peer review fra 27. april. Tilleggssøket skal støtte spesifikt:

- **Kap 3 (Teori)** — gir teoretisk fundament for primærmodellen
- **Kap 7.7 (Generaliserbarhet)** og **Kap 8 (Diskusjon)** — plasserer funnene i et internasjonalt forskningslandskap
- **Kap 8.4 (Begrensninger)** — viser at vi har vurdert hva vi kunne ha gjort annerledes basert på nyere metoder

Takk for grundig arbeid. Be om avklaring dersom noe er uklart i prompten.

---

*Versjon 2.0 (tilleggssøk) — 7. april 2026 | Erstatter ikke `litteratur_prompt_chatgpt.md` v1.0, men supplerer det.*
