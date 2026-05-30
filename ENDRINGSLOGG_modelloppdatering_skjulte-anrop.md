# Endringslogg: modelloppdatering – skjulte anrop og deterministisk sweep

**Dato:** 2026-05-30
**Omfang:** Primærmodellen (prosedyrebasert ankomstkonfliktmodell) er endret, og hele resultat-/diskusjons-/konklusjonsapparatet er renummerert. Dette dokumentet oppsummerer hva som ble endret og før→etter for alle nøkkeltall.

---

## 1. Bakgrunn – hvorfor endringen

To svakheter ble avdekket i den opprinnelige modellen:

1. **Kollapset tidsstempel for skjulte anrop.** De 18 901 estimerte sammenstilte («skjulte») anropene mangler registrert ankomsttid. Den gamle interpolasjonen tildelte *alle* manglende sekvensnumre i et gap samme tidsstempel (nærmeste forrige nabos tid, `est_tid = before.iloc[-1]`). Mange skjulte anrop ble dermed stablet på ett sekund og **bandt hverandre kunstig** inn i Svikt.
2. **Ordreavhengig sweep.** Sweepen sorterte kun på `Dato_og_Tid` med ustabil sortering, slik at hendelser med identisk tidsstempel ble klassifisert i ulik rekkefølge mellom skript (gammelt 32,6 % vs 32,8 %).

Konsekvensen var at det gamle hovedtallet (natt/helg Svikt 32,6 %) i betydelig grad var et **artefakt** av kollaps + ordreavhengighet, ikke en robust modellprediksjon.

## 2. Hva ble endret i modellen

| Komponent | Før | Etter |
|---|---|---|
| Tidsplassering av skjulte anrop | kollaps (alle på forrige nabos tidsstempel) | **uniform/lineær spredning** i sekvensgapet (hovedtall) |
| Sweep / samtidighet | ordreavhengig (ustabil sortering) | **deterministisk samtidighetsregel**: teller hendelser startet *strengt før* ankomst ($t_e < \tau$); samtidige ankomster binder ikke hverandre |
| Sensitivitet for skjult-anrop-fordeling | ikke kvantifisert | nytt **bånd**: gulv (uten estimerte ankomsttidspunkt) / uniform (hovedtall) / burst front-load (B=4, valgt scenario) |

Antallet skjulte anrop er uendret (18 901); kun tidspunktene endres. Den deterministiske regelen gjør at primærmodell, +1-scenario og bootstrap nå gir samme tall (det tidligere 32,6/32,8-spriket er borte).

## 3. Nøkkeltall: før → etter

### Variant A (beredskapsbelastning), hovedtall

| Størrelse | Før (kollaps) | Etter (uniform) |
|---|---:|---:|
| **Natt/helg Svikt** | **32,6 %** | **21,0 %** |
| Natt/helg Brudd | 20,5 / 20,3 % | 9,8 % |
| Natt/helg Normal | 46,9 % | 69,2 % |
| Natt/helg Brudd+Svikt | 53,1 % | 30,8 % |
| Bootstrap-CI (Svikt natt/helg) | [32,1; 33,2] % | [20,1; 21,4] % |
| Dag Svikt | 14,9 % | 6,4 % |
| Dag Normal / Brudd | 69,2 / 15,9 % | 78,6 / 14,9 % |
| Alle: Normal / Brudd / Svikt | 59,6 / 17,9 / 22,5 % | 74,6 / 12,8 / 12,7 % |
| Natt/dag-asymmetri (Svikt) | ca. 2,2× | ca. 3,3× |

### Scenario +1 operatør (regenerert)

| | Før | Etter |
|---|---:|---:|
| Natt/helg Svikt (21,0 % →) | 16,7 % | **5,6 %** |
| Dag Svikt (6,4 % →) | 8,5 % | 3,5 % |

### Variant B (total belastning), hoved

| | Før | Etter |
|---|---:|---:|
| Natt/helg Svikt | 33,2 % | 24,6 % |
| Alle Svikt | 25,6 % | 18,8 % |
| Alle Brudd+Svikt | 45,6 % | 36,0 % |
| Natt/helg Svikt-bånd (lav–høy) | 30–38 % | 22–29 % |
| Dag Svikt-bånd (lav–høy) | 15–34 % | 9–27 % |

### Nytt sensitivitetsbånd (natt/helg, variant A)

| Fordeling | Svikt | Brudd |
|---|---:|---:|
| Gulv (uten estimerte skjulte ankomsttidspunkt) | 16,8 % | 15,4 % |
| **Uniform (hovedtall)** | **21,0 %** | 9,8 % |
| Burst front-load (B=4, valgt scenario) | 26,4 % | 12,2 % |

## 4. Retorisk/innholdsmessig ramming (føringer fulgt)

- Hovedtall er **Svikt 21,0 %** («om lag ett av fem»). Gammelt «hvert tredje» er fjernet.
- **Brudd+Svikt 30,8 %** brukes som *supplerende* prosedyrebrudd/solo-drift-mål («om lag tre av ti»), ikke som hovedtall og ikke beskrevet som «3× dag».
- Den robuste konklusjonen er den **strukturelle natt/dag-asymmetrien i Svikt (≈3,3×)**, robust på tvers av fordelingsvalg; det presise nivået avhenger av antatt skjult-anrop-fordeling.
- Gulvet (16,8 %) omtales som «uten estimerte skjulte ankomsttidspunkt», ikke «uten antagelser».
- Burst (B=4) presenteres som et *valgt konservativt scenario*, ikke en kalibrert maksimumsgrense.
- Manglende ankomsttid for skjulte anrop er lagt inn som eksplisitt **begrensning** (kap 5.3.4/5.6, kap 8.3.5).

## 5. Filer endret

**Skript (`analyse/scripts/`):**
- `konflikt_total_belastning.py` – uniform interpolasjon (funksjon `build_hidden_rows`), deterministisk sweep, ny sensitivitetsblokk.
- `scenario_pluss1.py` – samme interpolasjon + sweep.
- `bootstrap_dpri1.py` – samme interpolasjon + sweep.

**Regenererte data/figurer:** `analyse/total_belastning_oppsummering.csv`, `analyse/scenario_pluss1_tabell.csv`, `analyse/bootstrap_dpri1_resultater.csv`, ny `analyse/sensitivitet_skjulte_anrop.csv`, samt tilhørende figurer.

**Rapportkapitler (`014 fase 4 - report/`):**
- `_forside_og_kap1.md` – sammendrag + abstract (norsk/engelsk).
- `kap3_teori.md` – 3.8 hovedtall, 3.7 Definisjon 3.2 (samtidighetsregel) + uniform spredning.
- `kap5_metode_data.md` – interpolasjonsbeskrivelse + eksplisitt begrensning om manglende ankomsttid.
- `kap6_modell.md` – sweep-/n_aktive-beskrivelse, A7, robusthetsspenn, CI.
- `kap7_analyse.md` – (ingen utfallsprosenter; modelltall ligger i kap 8).
- `kap8_resultat.md` – Tabell 8.1/8.2/8.4/8.5/8.6, ny **8.3.5** (sensitivitetsbånd, Tabell 8.6b), Funn 3/4/5.
- `kap9_diskusjon.md` – 9.2/9.3 (21,0 %, 30,8 %, 36,0 %, +1-effekt).
- `kap10_konklusjon.md` – 10.1/10.2 (RQ3-svar med bånd).
- `Rapport_LOG650_G20_Rune_110_v0.1.md` – Hovedfunn-oppsummering.

## 6. Verifikasjon utført

- Renummerering kjørt via workflow (per-kapittel) med egen verifiseringsfase; to flaggede rest-tall (kap6 Brudd-rate, kap9 +1-Normal) rettet manuelt.
- Grep for samtlige gamle modelltall i de aktive kapitlene: **ingen gjenstår** (kun benchmarking-koincidenser, f.eks. Oslo L-ukjent 40,4 %, Troms 20,3 %, verifisert urørt).
- Aritmetikk-sjekk: tabellrader summerer til 100; Brudd+Svikt natt/helg 9,8+21,0 = 30,8; Alle (A) 12,8+12,7 = 25,5; Alle (B) 17,2+18,8 = 36,0; asymmetri 21,0/6,4 = 3,28 ≈ 3,3×.

## 7. Konsekvens for konklusjonen

Den kvalitative konklusjonen står seg og styrkes: natt/helg er strukturelt mest presset, og +1-natt-anbefalingen er fortsatt den klart mest effektive (Svikt 21,0 % → 5,6 %). Det presise nivået er revidert ned fra «hvert tredje» (artefakt) til «om lag ett av fem» (uniform hovedtall), med et transparent bånd (16,8–26,4 %) og et artefaktfritt gulv (16,8 %).
