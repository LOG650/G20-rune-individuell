# Vurderinger og åpne punkter — LOG650 G20 Rune Grødem

Dette dokumentet samler punkter som er identifisert underveis og som bør vurderes for inkludering i rapporten — spesielt i kap 6 (modellens konservatisme), kap 7 (sensitivitetsanalyse) og kap 8 (diskusjon og begrensninger).

---

## V1 — Sammenstilte anrop binder en ekstra operatør utover foreldreoppdraget

**Identifisert:** 2026-04-07
**Status:** Ikke implementert i modellen — dokumenteres som modellkonservatisme

### Innsikt
Hvert sammenstilt anrop (identifisert via sekvensgap i 110_ID) representerer en faktisk innkommende telefon som **må besvares av en annen operatør** enn den som allerede håndterer foreldreoppdraget. Det er logisk umulig at samme operatør samtidig snakker med innringer A om hendelsen og besvarer ny telefon fra innringer B om samme hendelse.

### Hvorfor dette gjør modellen mer konservativ enn nåværende dokumentasjon antyder

| Foreldretype | Modellens nåværende behandling | Faktisk binding | Avvik |
|---|---|---|---|
| **Kategori D** (vi sporer) | Foreldre = 2 op, sammenstilt = 1 op separat belastningsenhet | 3 op samtidig | ✓ Fanget korrekt — modellen teller begge i n_aktive |
| **Kategori C** (ABA, ikke sporet) | Sammenstilt = 1 op | Reelt 2 op (ABA-håndterer + ny op for sammenstilt anrop) | ❌ Mangler 1 op binding |
| **Kategori B** (henvendelse uten utrykning, ikke sporet) | Sammenstilt = 1 op | Reelt 2 op | ❌ Mangler 1 op binding |

### Operativ konsekvens

En ABA (kategori C) er normalt solo-håndtering — én operatør avklarer alarmen og lukker eller eskalerer. I det øyeblikket en sammenstilt telefon kommer inn fra publikum om samme bygning/hendelse, oppstår en **uplanlagt makkerpar-situasjon**:

- Operatør 1 fortsetter ABA-behandlingen
- Operatør 2 må ta den nye telefonen
- Begge er bundet til **samme operative situasjon**, men ad-hoc — ikke etter prosedyre

Dette er en tilstand modellen ikke fanger eksplisitt. Den teller belastningen, men ikke **koblingen** mellom foreldre og sammenstilt anrop.

### Forslag til håndtering

**Alternativ A — Dokumentere som ytterligere konservatisme (minimal innsats)**
Legge til ett punkt i avsnitt 6.4.8 (Modellens konservatisme) som forklarer at:
- Sammenstilte anrop knyttet til kategori B/C-foreldre representerer en skjult dobbeltbinding
- Modellen teller kun det sammenstilte anropet (1 min), ikke foreldreoppdragets samtidige binding
- Dette trekker resultatet ytterligere mot underestimering

**Alternativ B — Sensitivitetsanalyse**
Estimere andelen sammenstilte anrop som sannsynligvis er koblet til kategori B/C-foreldre, og kjøre modellen med denne ekstra bindingen påført. Eksempel:
- Antakelse: 30/50/70 % av sammenstilte anrop er koblet til ikke-sporte foreldre
- Hver av disse legger til 1 operatør-binding på samme tidspunkt som det sammenstilte anropet
- Sammenligne kapasitetsnivåfordeling med og uten denne korreksjonen

**Alternativ C — Eksplisitt dobbeltbindingsmodell**
Modellere alle sammenstilte anrop som å binde 2 operatører (en for foreldre, en for det sammenstilte anropet), uavhengig av hva foreldreoppdraget er. Dette ville være mest konservativt og lettest å forsvare.

### Empirisk usikkerhet — vi kan ikke vite eksakt hvilket oppdrag

Sekvensgap-metoden identifiserer at et anrop ble sammenstilt, men ikke hvilket oppdrag det ble knyttet til. Vi kan likevel:
- Estimere fordelingen av synlige oppdragstyper i samme tidsvindu (±10 min) som proxy for sannsynlig foreldre-kategori
- Bruke denne fordelingen som vekt i sensitivitetsanalysen

### Anbefaling

**Implementer Alternativ A (umiddelbart)** — utvid avsnitt 6.4.8 og 7.5 til å dokumentere effekten eksplisitt.

**Vurder Alternativ B (hvis tid)** — kjør sensitivitetsanalyse med 50 % som hovedscenario, dokumenter i kap 7 eller vedlegg.

**Skip Alternativ C** — for stor metodisk endring nå, og forutsetningen om at *alle* sammenstilte anrop kobles til ikke-sporte foreldre er for sterk.

### Berørte kapitler
- Kap 6.4.4 — sammenstilte tilleggsanrop som belastningsenhet (utvidelse)
- Kap 6.4.8 — modellens konservatisme (nytt punkt)
- Kap 7.5 — kapasitetsanalyse (notat om effekten)
- Kap 7.5 sensitivitetsanalyse — eventuelt nytt scenario
- Kap 8 — diskusjon av modellens grenser

---

## V2 — Kategori A som operativ bakgrunnsbelastning og benchmarking-asymmetri

**Identifisert:** 2026-04-07
**Status:** Ikke implementert — dokumenteres som kvalitativ dimensjon

### Innsikt

110 Sør-Vest håndterer flere tusen kategori A-henvendelser per år (service, test, administrative). Disse er ikke modellert som beredskapsdimensjonerende, fordi:
- De har lav prioritet og kan vente i kø
- De har ikke dimensjonerende svartids-krav (i motsetning til beredskapsanrop med 30-sek-overflyt)

**Men de skaper reell operativ belastning** som modellen ikke kvantifiserer:

1. **Bakgrunnsstress:** Selv når operatøren ikke er bundet i en aktiv hendelse, må han eller hun kontinuerlig forholde seg til at kategori A-anrop ringer inn og må håndteres mellom beredskapsanrop.
2. **Akkumulert belastning over 12-timersskift:** Et 12-timers skift med høy bakgrunnsfrekvens av A-anrop tærer på operatørens kapasitet selv om hver enkelt henvendelse er kort.
3. **Konkurranse om grønn-tid:** Prosedyren krever at minst én operatør er ledig (grønn) for å ta neste nødtelefon. Når grønn-operatøren bruker tid på kategori A, reduseres bufferen for det neste beredskapsanropet.

### Benchmarking-asymmetri mellom sentraler

110 Sør-Vest har sannsynligvis **desidert høyest operativ belastning** sammenlignet med andre sentraler — ikke nødvendigvis fordi de har flest beredskapsoppdrag, men fordi de håndterer hele bakgrunnsbelastningen selv. Andre sentraler har løst dette på alternative måter:

- **Midt-Norge 110:** 3 dedikerte servicemedarbeidere håndterer ABA-testing utenfor LEO i normal arbeidstid. Operatørene tar over kun på helg/sykdom (verifisert i intervju 15.03.2026).
- **Andre sentraler:** Kan ha "forkontor" med vanlig åpningstid for å avlaste operatørene fra ikke-akutte henvendelser.

Dette innebærer at en direkte sammenligning av kapasitetsnivå på tvers av sentraler **ikke er apples-to-apples** uten å justere for hvordan kategori A og B håndteres organisatorisk.

### Hva som skal konkluderes (og hva som ikke skal)

**Ikke gjør:** Vurder om 12-timersskift er for langt. Det er ikke prosjektets oppgave å diskutere skiftordning.

**Gjør:** Konkluder nøkternt at:
- Skiftordningen ER 2-delt (12-timers dag og natt)
- Bakgrunnsbelastningen fra kategori A bygger seg opp over hvert skift
- Den fanges ikke kvantitativt i kapasitetsmodellen
- 110 Sør-Vest håndterer mer av denne belastningen enn enkelte andre sentraler som har dedikert servicepersonell

### Datagrunnlag som kan brukes

Fra BRIS 2025 for 110 Sør-Vest:
- 61 964 totale hendelser
- 7 555 kategori D (12,2 %)
- Resterende 54 409 (87,8 %) er kategori A/B/C blandet
- Av disse: 88 % er klassifisert som "110-oppdrag uten involvering av brannvesen" — i hovedsak service, test, telefonavklaringer

Per skift (gjennomsnitt):
- Dag/hverdag: ca. 200–250 A-henvendelser
- Natt/helg: lavere, men ikke null

Dette er volum vi kan dokumentere som bakgrunnsbelastning uten å hevde at det er beredskapsdimensjonerende.

### Forslag til håndtering

**Implementer i tre kapitler:**

1. **Kap 4.2.4 (Bemanningsreduksjon på helg) eller nytt avsnitt 4.3.x** — Beskriv volumforholdet mellom kategori A og kategori D, og forklar at A-volum bygger bakgrunnsbelastning utover beredskapsdimensjoneringen.

2. **Kap 7.2 eller nytt 7.x** — Vis det kvantitative volumforholdet mellom kategoriene, ikke som kapasitetsmål, men som kontekst for tolkningen av modellresultatene.

3. **Kap 8 (Diskusjon)** — Eksplisitt avsnitt om:
   - Modellens fokus på beredskapsdimensjonering = bevisst avgrensning
   - Bakgrunnsbelastning fra kategori A er en reell operativ faktor
   - Benchmarkingen mellom sentraler er asymmetrisk fordi organisering av servicetesting varierer
   - Anbefaling: Sentraler som vurderer bemanning bør også vurdere hvordan ikke-akutte henvendelser organiseres (forkontor/dedikert servicepersonell vs. operatør-håndtering)

### Berørte kapitler
- Kap 4 (Casebeskrivelse) — utvidelse om volumprofil og servicetesting-organisering
- Kap 5 (Metode/Data) — eksplisitt avgrensning mot kategori A i operasjonalisering (eksisterer allerede, kan presiseres)
- Kap 7 (Resultater) — kontekstavsnitt om bakgrunnsbelastning
- Kap 8 (Diskusjon) — kvalitativ drøfting av operativ belastning og benchmarking-asymmetri

### Avhengigheter
- Trenger verifikasjon fra spørreskjemaer (sendt ut til alle 12 sentraler) om hvordan andre sentraler organiserer servicetesting
- Midt-Norge er allerede bekreftet (3 dedikerte personer)
- 110 Sør-Vest forfatterens egen kontekst — operatørene tar all servicetesting selv

---

## V3 — Kvantifisering av total operativ belastning (utvidet modell)

**Identifisert:** 2026-04-07
**Status:** Foreslått implementering — krever operative bindingstidsestimater

### Innsikt og motivasjon

Prosjektets eksistensberettigelse er å erstatte kvalitative ROS-vurderinger med en **kvantitativ, etterprøvbar modell**. Hvis vi lar bakgrunnsbelastningen fra kategori A/B/C forbli en kvalitativ kommentar i diskusjonen, faller vi tilbake i akkurat den fellen vi forsøker å unngå.

V2 dokumenterer at kategori A skaper reell operativ belastning. V3 går ett skritt videre: **vi bruker samme prosedyrbaserte ankomstkonfliktmodell, men på hele anropsvolumet — ikke bare kategori D**. Dette gir et komplementært bilde:

- **"Beredskapsbelastning"** (eksisterende modell) — Hvor ofte kan makkerpar opprettholdes for prioriterte hendelser?
- **"Total operativ belastning"** (utvidet modell) — Hvor ofte er operatørene faktisk opptatt med noe som binder kapasitet?

De to modellene måler forskjellige ting og bør presenteres parallelt, ikke som erstatning.

### Metodisk ramme

Den eksisterende modellen håndterer alt som "belastningsenhet med (start, varighet)". Modellen er agnostisk om hva belastningen er — det eneste som varierer er bindingstiden. Det betyr at vi kan utvide modellen ved å:

1. Klassifisere alle hendelser (61 964) i kategori A/B/C/D basert på initiell hendelsestype + ressursvarsling
2. Tildele bindingstid per kategori (operativt estimat)
3. Kjøre samme sweep-algoritme på det utvidede settet
4. Sammenligne resultatene med beredskapsmodellen

### Bindingstidsestimater per kategori (operativt utgangspunkt)

| Kategori | Beskrivelse | Estimert bindingstid | Begrunnelse |
|---|---|---|---|
| **A1** Service-test (ABA-test) | Anlegg legges i service-modus, etterpå tilbake | 2–5 min | Operativ erfaring — operatør må aktivt håndtere anlegget i LEO |
| **A2** Generell henvendelse / feilringing | Avklaring og lukking | 30 sek – 1 min | Kort dialog, lukkes umiddelbart |
| **A3** Administrativ henvendelse | Avklaring til mannskap, internt samband | 1–3 min | Kan variere |
| **B** Reell hendelse uten utrykning | Vurdering, avklaring, eventuell rådgivning | 5–10 min | Krever vurdering før lukking |
| **C** Tidskritisk avklaring (ABA reell) | Avklaring av om hendelse skal eskalere | 3–8 min | Inkluderer eventuelle tilleggsanrop |
| **D** Utrykningshendelse | Akuttfasen RØD+GUL bundet | Median 13 min | Allerede databasert |

**Viktig forbehold:** Disse estimatene må valideres mot operative samtaler før de brukes i rapporten. De er foreløpige og kan justeres ved sensitivitetsanalyse.

### Forslag til implementering

**Steg 1: Klassifisere hele datasettet (~2 timer arbeid)**
- Bruk `Kilde`-feltet (Alarm/Samtale) + initiell hendelsestype + tilstedeværelse av ressursvarsling
- Tildel kategori A/B/C/D til hver av de 61 964 hendelsene
- Kvalitetssjekk fordeling mot kjent volum

**Steg 2: Utvide konfliktmodellen (~2 timer arbeid)**
- Modifiser `konflikt_v4_korrigert.py` til å akseptere bindingstid per kategori
- Kjør modellen med to varianter:
  - **Variant A (eksisterende):** Kun kategori D + sammenstilte anrop
  - **Variant B (ny):** Alle kategorier med kategori-spesifikk bindingstid

**Steg 3: Presentere parallelt i kap 7 (~1 time arbeid)**
- To søylediagrammer side om side: "Beredskapsbelastning" og "Total operativ belastning"
- Vise hvor mye hardere kapasiteten presses når all belastning inkluderes
- Diskutere hva forskjellen betyr operativt

**Steg 4: Sensitivitetsanalyse på bindingstider (~1 time)**
- Variere kategori A-bindingstid mellom 30 sek, 1 min, 2 min
- Vise at konklusjonen er robust mot rimelige variasjoner

### Forventede funn (hypoteser)

1. **Variant B vil vise vesentlig høyere kapasitetspress** enn variant A — fordi de fleste timene har bakgrunnsanrop som binder operatører selv om det ikke er beredskapshendelser
2. **Forholdet er størst på dagtid** (når kategori A-volumet er høyt) — selv om c_eff = 3 er bedre buffer
3. **Helg/natt vil ikke bli like mye verre** — fordi A-volumet er lavere, men beredskapsvolumet er nesten likt
4. **Vi kan svare på spørsmålet:** "Hvor mye av operatørtiden brukes på beredskap vs. annet?"

### Hva dette gir prosjektet

1. **Sterkere svar på problemstillingen** — vi kvantifiserer ikke bare beredskapskapasitet, men total operativ kapasitet
2. **Tydeligere kontrast til ROS-analyser** — vi viser at en kvantitativ modell kan fange nyanser ROS ikke når
3. **Bedre benchmarking-grunnlag** — total belastning er en mer rettferdig sammenligning på tvers av sentraler (forutsatt at vi har tilsvarende data fra dem)
4. **Praktisk verdi for dimensjoneringsbeslutninger** — bemanningsbehovet bør reflektere hele arbeidsbyrden, ikke bare beredskapsspissene

### Risiko og forbehold

- **Bindingstider er estimater, ikke målinger** — må valideres operativt og presenteres med usikkerhet
- **Kategori A fanger ikke korte avbrytelser** — telefoner som varer 10 sek er ikke mindre forstyrrende enn de som varer 1 min
- **Ikke alle sammenligninger på tvers av sentraler er gyldige** — Midt-Norges 3 dedikerte servicemedarbeidere betyr at deres BRIS-tall ikke representerer operatørbelastning på samme måte (krysslenke V2)
- **Risiko for å rote til den primære fortellingen** — hvis variant B blir for dominerende kan kjernebudskapet om makkerpar/beredskap drukne. Anbefaling: Variant A forblir primærmodell, variant B er en utvidelse som styrker konklusjonen

### Anbefaling

**Prioritet: HØY.** Dette er et betydelig løft for prosjektets analytiske ambisjon og passer direkte til problemstillingens formål. Implementeres som tillegg til eksisterende modell, ikke som erstatning.

**Tidsestimat:** ~6 timer effektivt arbeid, fordelt på koding, validering og rapportskriving.

**Beste plassering i tidsplan:** Mellom kap 3 (teori) og kap 8 (diskusjon) — eller parallelt med kap 3-skrivingen siden den ene er teori og den andre er analyse.

### Berørte kapitler
- Kap 5 (Metode/Data) — utvide klassifiseringsbeskrivelsen til å inkludere alle kategorier
- Kap 6 (Modell) — utvide modellen til å akseptere kategori-spesifikk bindingstid
- Kap 7 (Resultater) — nytt avsnitt 7.x: "Total operativ belastning"
- Kap 8 (Diskusjon) — kobling mellom de to modellvariantene som komplementære perspektiv

### Avhengigheter
- Operative estimater for bindingstider per kategori (kan delvis utledes fra eksisterende intervjuer)
- Avgjørelse om hvor mye scope-utvidelse er forsvarlig før peer review (27. april)

---

## Mal for nye punkter

Bruk dette formatet for nye vurderinger:

```markdown
## V[N] — [Kort tittel]

**Identifisert:** YYYY-MM-DD
**Status:** [Ikke startet / Under vurdering / Implementert / Forkastet]

### Innsikt
[Hva er observasjonen / problemet / muligheten?]

### Konsekvens for modellen / rapporten
[Hvordan påvirker dette resultatene eller tolkningen?]

### Forslag til håndtering
[Konkrete alternativer med innsats/effekt]

### Anbefaling
[Hvilket alternativ velges, og hvorfor]

### Berørte kapitler
[Liste over kapitler/avsnitt som må oppdateres]
```

---

*Opprettet: 2026-04-07*
