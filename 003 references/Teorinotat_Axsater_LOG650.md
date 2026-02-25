# Teorinotat — Axsäter (2015): Inventory Control, 3. utg.
## LOG650 — Rune Grødem, G20
## Prosjekt: Dimensjonering av røykdykkerbekledning under usikker etterspørsel (RogBR)

> **Formål:** Dette dokumentet oppsummerer faglig relevante innsikter fra gjennomlesning av Axsäter (2015), direkte koblet til RogBR-prosjektet. Brukes som teorigrunnlag for rapport og modellvalg i fase 3.
>
> **ISBN:** 9783319157290 (3. utg., Springer, 2015)
> **Tilgang:** Bookshare (EPUB), lest og ekstrahert 2026-02-21

---

## SENTRAL INNSIKT: Hva slags problem er dette egentlig?

RogBR er **ikke** et klassisk lageroptimeringsproblem. Det er et **lukket system med fast populasjon**, nærmere beslektet med militære reservedelsmodeller enn vanlig varelagerstyring.

Draktene beveger seg mellom tre tilstander:
```
[Tilgjengelig på stasjon] ←→ [Til vask / i ledetid] ←→ [Avskrevet / ødelagt]
```

**Bestilling skjer kun ved:**
1. Drakt ødelagt / utslitt (forlater systemet permanent)
2. Økning i antall brukere

**Det egentlige spørsmålet er derfor:**
> Hvor mange drakter trenger vi totalt i systemet for å sikre at nok er tilgjengelig til enhver tid, gitt at noen alltid er til vask?

Dette er en **METRIC-type problemstilling** — ikke en (Q,R)-type problemstilling.

---

## KAP. 3 — Costs and Concepts

### 3.1.3 — Shortage Costs vs. Service Constraints ✅ DIREKTE RELEVANT

**Kjernen:** Mangel-kostnader er nesten umulige å estimere i praksis. For RogBR er dette enda mer sant enn i vanlig logistikk — det er ikke mulig å sette et kronebeløp på at en brannmann mangler røykdykkerutstyr under innsats.

**Axsäters løsning:** Erstatt mangel-kostnad med en **service constraint** — sett krav om at utstyret er tilgjengelig X% av tiden, og dimensjoner mot det.

**Kobling til RogBR:** Dette er den faglige begrunnelsen for å bruke 99,x% servicegradkrav som styringsparameter. Ikke et vilkårlig tall — men den akademisk anerkjente løsningen på problemet med ukvantifiserbare mangel-kostnader.

> *"Because shortage costs are so difficult to estimate, it is very common to replace them by a suitable service constraint."* — Axsäter (2015, s. kap. 3)

---

### 3.2.1 — Inventory Position (lagerposisjon) ✅ GRUNNBEGREP

**Definisjon:**
```
Lagerposisjon = Lagerbeholdning + Utestående ordrer − Restordrer
```

**Kobling til RogBR:**
- Lagerbeholdning = drakter fysisk på stasjon
- Utestående ordrer = drakter som er til vask og på vei tilbake
- Restordrer = udekkede behov (ønsket drakt finnes ikke)

Vaskeledetiden er "lead time". Det er **lagerposisjonen** — ikke bare det fysiske lageret — som er det riktige styringsbegrepet.

---

### 3.2.2 — Continuous vs. Periodic Review ⚠️ MÅ AVKLARES MED ROGBR

**Continuous review** (bestill straks lagerposisjonen faller under et nivå):
- Krever mindre sikkerhetslager
- Garderer mot usikkerhet kun i ledetid L

**Periodic review** (sjekk med faste intervaller T):
- Krever mer sikkerhetslager
- Garderer mot usikkerhet i T + L

**Åpent spørsmål for intervju med S01:** Bruker RogBR continuous review (løpende telling av utstyr) eller periodic review (ukentlig/månedlig gjennomgang)? Svaret påvirker sikkerhetslagerformelen direkte.

---

### 3.2.3 — (Q,R)- vs. (s,S)-politikk ✅ RELEVANT FOR MODELLVALG

| Policy | Beskrivelse | Egnet for |
|---|---|---|
| **(Q,R)** | Bestill fast mengde Q når lagerposisjon faller til R | Jevn, forutsigbar etterspørsel |
| **(s,S)** | Bestill opp til S når lagerposisjon faller under s | Variabel, lav og ujevn etterspørsel |

**Axsäters vurdering:** (s,S) er teoretisk optimal, men kostnadsforskjellen er liten. (Q,R) er enklere å administrere.

**Kobling til RogBR:** For drakter med lav og ujevn (lumpy) etterspørsel er (s,S) mer naturlig — man bestiller det man trenger, ikke et fast parti. Men dette er **underordnet** fordi RogBRs bestillingslogikk uansett er atypisk (bestilles kun ved avskrivning/nye brukere).

---

## KAP. 10 — Multi-Echelon Systems: Reorder Points

### 10.2 — METRIC-tilnærmingen (Sherbrooke 1968) ⭐ PRIMÆR MODELL

#### Hva METRIC er

METRIC (Multi-Echelon Technique for Recoverable Item Control) er en modell for å finne optimalt lagernivå i et to-nivå distribusjonssystem med sjelden og ujevn (Poisson) etterspørsel. Opprinnelig utviklet for militære fly-reservedeler der:
- Fast antall fly i operasjon
- Deler sendes til reparasjon med usikker ledetid
- Spørsmålet er: hvor mange reservedeler for å holde tilgjengeligheten oppe?

#### RogBR mappet mot METRIC

| METRIC-begrep | Symbol | RogBR-tolkning |
|---|---|---|
| Antall retailers | N | Antall stasjoner (Riska, Klepp, Ålgård, ...) |
| Sentrallager | S₀ | Stangeland / felles utstyrslager / vaskeri |
| Retailer i | Sᵢ | Stasjon i sin beholdning |
| Replenishment lead-time (lager) | L₀ | Ledetid fra leverandør (ny drakt) |
| Transportation time til retailer | Lᵢ | Vasketid + transporttid tilbake til stasjon i |
| Etterspørsel ved retailer i | λᵢ | Antall drakter som trenger vask per tidsenhet ved stasjon i |
| Order-up-to nivå | Sᵢ | **Det vi skal finne** — optimal beholdning per stasjon |

#### Modellens tre steg

**Steg 1 — Beregn sentrallagerstatus (eksakt)**

Lagerposisjonen holdes alltid lik S₀. Antall drakter "ute" til vask følger Poisson-fordeling med gjennomsnitt:
```
λ₀ · L₀  (total etterspørselsrate × vaskeledetid)
```

Gjennomsnittlig beholdning på sentrallager:
```
E[IL₀⁺] = Σ max(S₀ - n, 0) · P(D(L₀) = n)
```

Gjennomsnittlig antall restordrer på sentrallager:
```
E[IL₀⁻] = E[D(L₀)] - S₀ + E[IL₀⁺]
```

**Steg 2 — Beregn forsinkelse ved sentrallager (køteori)**

Sentrallageret tolkes som et **M/D/∞ køsystem**. Gjennomsnittlig forsinkelse beregnes med Littles lov:
```
W₀ = E[restordrer ved sentrallager] / λ₀
```

W₀ er gjennomsnittlig tid en stasjon må vente fordi sentrallageret ikke har drakt tilgjengelig. **Dette er risikoen vi dimensjonerer mot.**

**Steg 3 — Beregn beholdning per stasjon (approksimert)**

**METRIC-approksimasjonen:** Erstatt stokastisk forsinkelse W₀ med sitt gjennomsnitt. Effektiv ledetid for stasjon i:
```
L̃ᵢ = Lᵢ + W₀
```

Deretter behandles hver stasjon som et enkelt-echelon system med denne effektive ledetiden og Poisson-etterspørsel λᵢ. Sᵢ velges slik at ønsket servicegrad oppnås.

#### Fordelen med METRIC for implementasjon

METRIC **dekomponerer** problemet — sentrallager løses eksakt, deretter løses hver stasjon separat. Python-implementasjon er håndterbar:
1. Løs Poisson-kø for sentrallager
2. Beregn W₀
3. Iterer over stasjoner og finn Sᵢ for ønsket servicegrad

#### Begrensning som MÅ nevnes i rapporten

METRIC antar at forsinkelsene ved sentrallageret er **uavhengige** for ulike stasjoner. I virkeligheten: hvis alle drakter er ute til vask, rammer det alle stasjoner **samtidig** (common cause stockout). Dette er approksimasjonens svakhet. Axsäter nevner dette eksplisitt.

> *"Because successive stochastic delays at the warehouse depend on the inventory status at the warehouse and are not independent."* — Axsäter (2015, kap. 10)

**Konsekvens for rapporten:** Nevnes i diskusjonskapittelet som en avgrensning. Simulering kan brukes til å kvantifisere hvor stor feilen er.

---

## KONKLUSJON — Valg av primær modell

Basert på gjennomlesning av Axsäter (2015) og RogBRs systemstruktur:

| Vurdering | Konklusjon |
|---|---|
| Problemtype | Lukket system, fast populasjon — ikke klassisk lager |
| Primær modell | **METRIC** (Axsäter kap. 10.2 / Sherbrooke 1968) |
| Etterspørselsmodell | Poisson (lav frekvens) — se kap. 5.1.1 for compound Poisson |
| Servicegrad-type | Fill rate (Type II) — avklares med RogBR |
| (Q,R) vs (s,S) | Underordnet — bestillingslogikken er atypisk |
| Validering | Monte Carlo simulering etter analytisk løsning |

---

## NESTE LESESTEG

Etter at dette notatet er etablert, gjenstår følgende seksjoner:

| Seksjon | Formål |
|---|---|
| **Kap. 5.1.1** — Compound Poisson Demand | Etterspørselsmodell — er enkel Poisson nok, eller trenger vi compound? |
| **Kap. 5.4** — Service Levels | Presis definisjon av Type I vs Type II servicegrad |
| **Kap. 5.7.1** — Fill Rate (Compound Poisson) | Beregningsformler for fill rate |
| **Kap. 8.1.1** — Distribution Inventory Systems | Nettverksstruktur — bekreft at RogBR passer inn |
| **Kap. 8.1.4** — Lateral Transshipments | Utstyrsdeling mellom stasjoner |

---

## REFERANSE (APA 7)

Axsäter, S. (2015). *Inventory control* (3. utg.). Springer. https://doi.org/10.1007/978-3-319-15729-0

---

*Opprettet: 2026-02-21 | Neste oppdatering: etter gjennomlesning kap. 5.1.1*
