# DES-utvidelse — oppsett og datagrunnlag (v0.1)

**Status:** Utkast til gjennomgang. Rapporten er innlevert og låst (A). Dette er
videre arbeid jf. kap 9.5 punkt 3 («Simuleringsbasert modellering»). Ingenting her
endrer den leverte rapporten.

**Formål med dette dokumentet:** Beskrive *hva* en diskret hendelsessimulering (DES)
skal gjøre, *hvilke data* som inngår, og *hvilke valg* som må tas — før vi koder.

---

## 1. Hvorfor DES? Hva den tilfører over primærmodellen

Primærmodellen (den prosedyrebaserte ankomstkonfliktmodellen) er en **deterministisk
sweep**: for hvert beredskapsanrop telles aktive op-binder ved ankomst, og anropet
klassifiseres Normal / Brudd / Svikt. Den svarer presist på ett spørsmål — *«i hvilken
tilstand ankommer anropet?»* — men den har strukturelle begrensninger (kap 9.4.2):

| Begrensning i sweep-modellen | Hva DES legger til |
|---|---|
| Binær kapasitet (ledig/opptatt), ingen kø | Eksplisitt **kø** med disiplin og ventetid |
| Overløp til Agder ikke modellert dynamisk | **30-sek-regel + 10.-i-kø** som faktiske hendelser → overløpsrate |
| VL ekskludert fast (`c_eff = c−1`) | **VL som betinget ressurs** som kan tre inn under press |
| Deterministiske ankomsttider (faktisk logg) | **Stokastiske ankomster** (NHPP) → kan generere nye «år» |
| Punktestimat for bindingstid | **Fordelinger** for bindingstid → varians fanges |
| Ring-flom ikke tidsmessig korrelert | **Burst-klynging** kan modelleres eksplisitt (Gustavsson 2018) |
| Ett tall per scenario | **Replikasjoner** → konfidensintervall på alle utfall |

Kort sagt: sweep-modellen måler *prosedyreetterlevelse ved ankomst*. DES måler i tillegg
*systemdynamikk* — ventetid, overløp, VL-bruk — og gir usikkerhetsbånd gjennom gjentatte
kjøringer. Den lar oss også **teste organisatoriske endringer før implementering**
(funksjonsdifferensiering, alternativ overløpsterskel), slik van Buuren et al. (2017) og
Penverne et al. (2024) gjør.

**Viktig avgrensning:** DES *erstatter ikke* primærmodellen. Primærmodellen forblir
hovedfunnet. DES er en uavhengig, dynamisk kryssjekk og et verktøy for what-if.

---

## 2. Konseptuell modell

### 2.1 Entiteter (det som «strømmer» gjennom systemet)
Innkommende henvendelser, klassifisert i de samme 8 kategoriene som i rapporten
(D-pri1, D-aba, S, L-aba, L-hendelse, L-ukjent, F, V) + skjulte/sammenstilte anrop.

### 2.2 Ressurser
| Ressurs | Antall | Merknad |
|---|---|---|
| **Operatører** | 4 dag/hverdag, 3 øvrige (totalt, inkl. VL) | Modelleres som individuelle enheter |
| **Vaktleder (VL)** | 1 (del av totalen) | Normalt *ikke* i operatørpoolen; trer inn betinget |
| **Agder (overløp)** | ∞ | Mottakssluk; bærer en «tap av regionalkunnskap»-kostnad |

Makkerpar = en D-pri1-hendelse **ber om 2 operatørenheter samtidig** (q=2). Dette er
kjernen — samme op-binder-semantikk som rapporten, men nå som faktisk ressursforespørsel
i en kø, ikke bare en telling.

### 2.3 Hendelser (event-typer i simulatoren)
1. **Ankomst** — ny henvendelse av en gitt kategori
2. **Seize** — forsøk på å binde q operatører (1 eller 2)
3. **Kø** — hvis ikke nok ledige: anrop venter
4. **Overløp** — hvis ventetid > 30 sek *eller* kølengde ≥ 10 → rutes til Agder
5. **Service ferdig** — bindingstid utløpt → frigjør operatør(er)
6. **D-aba Fase 2** — med sannsynlighet p, +90 sek offset (som i rapporten)
7. **VL-inntreden** — betinget regel (se §5, åpent valg)

### 2.4 Tilstandsvariabler
Antall opptatte operatører, kølengde, VL ledig/opptatt, teller per kapasitetsnivå
(Normal/Brudd/Svikt — beholdes for direkte sammenligning med sweep-modellen).

---

## 3. Datagrunnlag — hva som mates inn

Alt nedenfor finnes allerede i prosjektet. **Ingen ny datainnhenting kreves** for
grunnversjonen.

### 3.1 Primærkilde
| Felt (BRIS 2025) | Brukes til | Status |
|---|---|---|
| `Dato_og_Tid` | Ankomsttidspunkt (trace) / NHPP-estimering | ✅ Har |
| `Oppdragstype`, `Opprinnelig_oppdragstype`, `Kilde` | Kategori-klassifisering (v3_kat) | ✅ Har (gjenbruk av eksisterende logikk) |
| `Ressurs_varslet` | D-aba call-out-tid, skille D/ikke-D | ✅ Har |
| `Forste_ressurs_fremme` | D-pri1 bindingstidsfordeling | ✅ Har (empirisk) |
| `110_ID` (sekvensnr) | Skjulte/sammenstilte anrop | ✅ Har (sekvensgap-metode) |
| `Time_paa_dognet`, `Ukedagsnr` | Skift- og helg-inndeling, c_eff | ✅ Har |

### 3.2 Parametre (fordelinger og punktverdier)
| Parameter | Verdi/fordeling | Kilde | Status for DES |
|---|---|---|---|
| D-pri1 bindingstid | Empirisk fordeling (median 14,1 min) | BRIS-tidsstempler | ✅ Kan trekkes direkte / fittes lognormal |
| D-aba Fase 1 | 3 min (call-out median 74 sek + reg.) | BRIS + prosedyre | ✅ Har |
| D-aba Fase 2 | p=0,50, Y=6 min (hoved) | Operativt estimat | ✅ Har (3 scenarioer) |
| L-aba | 4,5 min (mean 4,53, CI [3,74;5,43]) | LABA-dybdeanalyse n=100 | ✅ Empirisk |
| S, L-hendelse, L-ukjent, F, V | Punktestimater (lav/hoved/høy) | VL-validerte estimater | ⚠️ Punkt, ikke fordeling |
| Skjulte anrop | 1 min, q=1, antall via sekvensgap | Operativ vurdering | ✅ Har |
| c_total per skift | 4 / 3 | Turnus 110 Sør-Vest | ✅ Har |

### 3.3 Nye parametre DES krever (ikke i primærmodellen)
Disse er **antagelser** som må settes og sensitivitetstestes — flagget tydelig:
| Parameter | Hvorfor DES trenger den | Forslag til kilde |
|---|---|---|
| Overløpsterskel | 30 sek + 10.-i-kø | Beredskapsanalyse s. 25 (bekreftet) |
| VL-inntreden-regel | Når trer VL inn som operatør? | Antagelse — sensitivitetstestes (§5) |
| Variasjonskoeffisient (CV) for ikke-D bindingstider | Trekke stokastisk service | Antagelse (f.eks. CV=1, eksponentiell) eller fitt der data finnes |
| Burst-klynging (valgfritt) | Ring-flom-korrelasjon | Gustavsson (2018) $A\cdot e^{-tB}$ — eget sensitivitetscase |

---

## 4. To måter å drive ankomster på (designvalg)

| | **A. Trace-drevet** | **B. Fordelings-drevet (NHPP)** |
|---|---|---|
| Ankomster | Spill av faktiske 2025-tidsstempler | Generer fra estimert λ(t) per time/skift + kategorimiks |
| Stokastisk i | Kun bindingstid | Både ankomst og bindingstid |
| Styrke | **Validerings-bro** mot sweep-modellen | Generer nye «år» → ekte KI, burst-scenarioer |
| Svakhet | Kan ikke generere nye scenarioer | Avhenger av Poisson-/NHPP-tilpasning (R2/R3) |

**Anbefalt rekkefølge:** Start med **A** (validér at DES reproduserer sweep-modellens
Normal/Brudd/Svikt når service settes deterministisk), gå deretter til **B** for
what-if og konfidensintervall.

---

## 5. Designvalg (besluttet 2026-06-11)

1. **VL-regel: betinget inntreden.** VL er normalt utenfor operatørpoolen, men trer
   inn som operatør ved Svikt/overløpsfare. Lar oss kvantifisere reservekapasiteten
   rapporten eksplisitt lar stå åpen (kap 9.4.2). Den rene broen (VL aldri operatør,
   `c_eff = c−1`) kjøres som *referanse* i valideringssteget, men hovedmodellen bruker
   betinget inntreden.
2. **Omfang v1: validerings-bro først.** D1 bygger trace-drevet DES som reproduserer
   sweepens Normal/Brudd/Svikt før kø/overløp/VL legges på (D2+).
3. **Prioritetsdisiplin i kø:** *Åpent, men foreslått* D-pri1 > D-aba > øvrige
   (avklares ved D2). FIFO som referanse.
4. **Scenarioprioritet:** S1 (+1 natt/helg), S4 (burst/ring-flom), S3
   (funksjonsdifferensiering) — i den rekkefølgen. S2/S5 sekundært.

---

## 6. Utfallsmål og scenarioer

### 6.1 Utfallsmål (per skifttype, med KI over replikasjoner)
- Kapasitetsnivå-fordeling (Normal/Brudd/Svikt) — **bro mot rapporten**
- Ventetidsfordeling og P(W > 30 sek)
- **Overløpsrate til Agder** (anrop/år, %) — nytt, ikke i sweep
- VL-utnyttelse / antall inntredener
- Andel D-pri1 som binder makkerpar uforstyrret

### 6.2 Scenarioer
| # | Scenario | Spørsmål |
|---|---|---|
| S0 | Baseline (faktisk bemanning) | Reproduserer DES rapportens funn? |
| S1 | +1 operatør natt/helg | Bekrefter +9,8 pp Normal-gevinst dynamisk? |
| S2 | +1 operatør dag hverdag | Sekundærtiltakets effekt |
| S3 | Funksjonsdifferensiering (S skilt ut) | Frigjør service-skille kapasitet? (jf. Midt-Norge) |
| S4 | Burst-ankomster (ring-flom) | Hvor sårbar er systemet for korrelert pågang? |
| S5 | Alternativ overløpsterskel | Designsensitivitet for Agder-kobling |

---

## 7. Verktøy og implementasjon

- **Språk/stack:** Python (gjenbruk pandas/numpy). DES-motor: **SimPy** (prosessbasert,
  lett, godt dokumentert, passer ressurs-/kø-logikk).
- **Plassering:** `015 fase 5 - DES/` (skript, notebooks, figurer) — atskilt fra rapporten.
- **Reproduserbarhet:** Fast seed per replikasjon; resultat-CSV + figurer som i resten av
  prosjektet.
- **Validering:** (i) Trace-DES med deterministisk service ≈ sweep-modellen;
  (ii) overløpsrate / P(W>30s) sammenholdes med Erlang-C og beredskapsanalysen;
  (iii) ankomstvolum mot BRIS-tellinger.

---

## 8. Foreslått rekkefølge (når vi starter)

1. **D0** Ekstraher arrival-trace + kategori + bindingstidsfordelinger fra BRIS (gjenbruk eksisterende klassifisering)
2. **D1** SimPy-skjelett: operatører som ressurs, makkerpar = 2 enheter, trace-drevet, deterministisk service → **valider mot sweep**
3. **D2** Legg på kø + overløp (30 sek / 10.-i-kø) + VL-regel
4. **D3** Stokastisk service (fordelinger) + replikasjoner → KI
5. **D4** NHPP-ankomster (fordelings-drevet) + burst-case
6. **D5** Scenarioer S1–S5 + figurer + notat

---

## 9. Risiko / forbehold
- **R-DES-1:** NHPP-tilpasning forutsetter Poisson-test (R2/R3 fra rapporten) — gjøres eksplisitt i D4.
- **R-DES-2:** Overløp og VL-inntreden er ikke direkte logget i BRIS → forblir antagelser med sensitivitetsspenn, ikke målte fakta.
- **R-DES-3:** Ikke-D-bindingstider mangler fordelingsform → CV settes som antagelse.
- **R-DES-4:** Scope-glidning. DES er rik; vi holder oss til S0–S5 og validerings-broen først.
