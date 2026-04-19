# Notat — V3-modell: kalibrering og metodevalg

**Dato:** 2026-04-19
**Forfatter:** Rune Grødem
**Formål:** Sporbarhet for metodiske valg i V3-modellen. Dokumenterer empirisk grunnlag og beslutningslogikk som ligger bak klassifiseringsreglene, bindingstidsparametrene og makkerpar-behandlingen i kapasitetsmodellen. Refereres fra kap 5 (metode) og kap 6 (modell) i hovedrapporten.

---

## 1. Bakgrunn og omfang

Modellutviklingen har gått gjennom tre faser: Erlang-C (M/M/c) som grunnlinje, en simultanitetsanalyse som mellomsteg, og til slutt en prosedyrbasert ankomstkonfliktmodell (V3). V3 er den modellen som presenteres i rapporten. Dette notatet dokumenterer de empiriske og operative premissene som V3 bygger på, slik at parametervalg og regler kan etterprøves.

Notatet dekker fire områder:

1. V3-klassifiseringsregelen (kategorisering av hendelser)
2. Makkerpar og op-binder-semantikk (modellens behandling av samtidig operatørbinding)
3. D-pri1 vs D-aba — to operative dynamikker for utrykningshendelser
4. Bindingstidsparametre og empirisk kalibrering (inkl. LABA-dybdeanalyse)

---

## 2. V3-klassifiseringsregelen

### 2.1 Kategoristruktur

V3 deler BRIS-hendelser i åtte kategorier:

| Kategori | Operativ betydning |
|---|---|
| **D-pri1** | Pri-1 utrykning uten ABA-bakgrunn (bygningsbrann, trafikkulykke, farlig gods, etc.) |
| **D-aba** | Utrykning utløst av automatisk brannalarm (ABA-signal → ressurs varslet) |
| **S** | Service / overføringstester (ABA-test utenfor beredskapskontekst) |
| **L-aba** | ABA-signal løst av 110 uten utrykning (automatisk alarm avklart) |
| **L-hendelse** | Reell hendelse løst av 110 uten utrykning (samtale, publikumsmelding, etc.) |
| **L-ukjent** | Oppdrag løst av 110 uten registrert opprinnelig type |
| **F** | Feilringing, ikke reell nødmelding, eCall-feil |
| **V** | Viderevarsling / viderekobling til nabosentral |

### 2.2 Reglene

For hver BRIS-rad:

```
HVIS Ressurs_varslet er utfylt:
    HVIS Opprinnelig_oppdragstype starter med "ABA" OG Kilde = "Alarm":
        → D-aba
    ELLERS:
        → D-pri1

HVIS Oppdragstype = "Service":
    → S

HVIS Oppdragstype er feilring/ikke-reell/eCall-feil:
    → F

HVIS Oppdragstype inneholder "viderevarslet" eller "viderekoble":
    → V

HVIS Oppdragstype er "Oppdrag løst av 110":
    HVIS Opprinnelig = "ABA" OG Kilde = "Alarm":
        → L-aba
    HVIS Opprinnelig = "ABA" (Kilde = Samtale eller blank):
        → L-hendelse
    HVIS Opprinnelig er utfylt:
        → L-hendelse
    ELLERS:
        → L-ukjent

ELLERS:
    → L-ukjent
```

### 2.3 Hvorfor Kilde = Alarm kreves for L-aba og D-aba

Den opprinnelige V2-regelen klassifiserte alle hendelser med `Opprinnelig = "ABA"` som L-aba eller (for utrykning) som D. Manuell gjennomgang av 50 L-aba-hendelser (LABA-dybdeanalysen, se §5) viste at 12 av 49 gyldige rader (24,5 %) ikke representerte automatisk brannalarm i operativ forstand:

- 4 «privat brannalarm uten tilknytting til 110» (ikke ISM-kunder, registrert via telefon)
- 3 «kun nødanrop, ikke alarm i ISM» (publikum rapporterer brannalarm, ikke ABA-signal)
- 3 tester / øvelser feilrevidert
- 1 innbruddsalarm feilkategorisert
- 1 prosedyrebrudd

Kildekolonnen i BRIS skiller *hvordan* hendelsen ankom 110: `Alarm` (ABA-signal), `Samtale` (innringer), eller blank (operatør-initiert, typisk duplikat-oppdrag eller test). Operatøren bekreftet at reell ABA har Kilde = Alarm — med ett unntak (Samtale-registrerte ABA kan oppstå ved duplikat-oppdrag på samme adresse, der ny alarm ikke får ALARM-status fordi et tidligere åpent oppdrag eksisterer). Dette unntaket er sjeldent nok til å ikke motivere egen regel.

### 2.4 Virkning på 110 Sør-Vest 2025

| | V2 (før Kilde-filter) | V3 (etter Kilde-filter) |
|---|---:|---:|
| L-aba | 5 495 (8,9 %) | 3 430 (5,5 %) |
| L-hendelse | 2 214 (3,6 %) | 4 298 (6,9 %) |

2 065 oppdrag flyttes fra L-aba til L-hendelse. Tilsvarende for D-kategorien: 3 458 ABA-utrykninger deles i 3 056 D-aba (Kilde = Alarm) og 402 D-pri1 (Kilde = Samtale eller blank).

---

## 3. Op-binder-semantikk

### 3.1 Fra «event = slot» til «event = op-binder»

Klassisk M/M/c og enkel ankomstkonfliktmodellering teller én hendelse som én «aktiv enhet» som opptar én server-slot. For 110-kontekst bryter denne antakelsen sammen: makkerpar-prosedyren krever at to operatører er bundet samtidig på pri-1-hendelser, mens ABA-utløste hendelser håndteres serielt av én operatør. Én hendelse binder altså **enten én eller to operatører**, avhengig av type.

V3-modellen innfører derfor *op-binder-semantikk*: hver hendelse genererer én eller flere «op-binder-events» med:

- `ankomst_ts` — tidspunkt for op-binding starter
- `bind_min` — varighet i minutter
- `ops_bundet` — antall operatører (1 eller 2)

Sweep-algoritmen akkumulerer antall aktive op-binder ved hver ny ankomst.

### 3.2 Klassifisering

For hvert beredskapsanrop (D-pri1 eller D-aba) måles kapasitetstilstand ved ankomst:

| Tilstand | Kriterium | Operativ betydning |
|---|---|---|
| **Normal** | ledige ≥ 2 | Makkerpar mulig for ny hendelse |
| **Brudd** | ledige = 1 | Solo-håndtering mulig, makkerpar ikke mulig |
| **Svikt** | ledige ≤ 0 | Ingen ledig operatør — VL må overta eller overløp til Agder |

hvor `ledige = c_eff − n_aktive_op_binder`.

Merk at tidligere modellversjoner (V1–V2) brukte `n_aktive = antall aktive hendelser` uten hensyn til om hver hendelse krevde én eller to operatører. V3 korrigerer dette.

### 3.3 Empirisk grunnlag for op-binder-semantikk

Kilde: operativ beskrivelse fra vaktleder og operatører ved 110 Sør-Vest, april 2026.

- Pri-1-hendelser (bygningsbrann, trafikkulykke, farlig gods): makkerpar-krav fra første sekund. RØD-operatør og GUL-operatør bundet parallelt gjennom hele hendelsens aktive fase. Trippelvarsling, tidskritisk BAPS-informasjon, parallell radiobruk.
- ABA-utrykning: ikke pri-1, ingen trippelvarsling, ingen tidskritisk informasjon via BAPS. Operatør 1 kvitterer alarm, oppretter oppdrag i LEO, utfører call-out (≈ 3 min total), og er deretter tilgjengelig for neste oppgave. Eventuell nødtelefon fra stedet etter call-out kan besvares av vilkårlig operatør.

Empirisk verifisert fra BRIS 2025 Sør-Vest: median tid fra `Dato_og_Tid` til `Ressurs_varslet` er 74 sek for D-aba (P25 = 67, P75 = 80, P90 = 111). Dette stemmer overens med operativ beskrivelse av ~90 sek call-out. For D-pri1 er median 83 sek, mean 160 sek — lengre hale fordi flere delbeslutninger tas før utalarmering.

---

## 4. D-pri1 vs D-aba — to dynamikker

### 4.1 Modellering

| | D-pri1 | D-aba |
|---|---|---|
| Makkerpar-krav | Ja | Nei |
| Op-binding — Fase 1 | 2 ops × full bindingstid | 1 op × 3 min (alltid) |
| Op-binding — Fase 2 | N/A (inkludert i Fase 1) | 1 op × Y min, med sannsynlighet p, offset + 1,5 min |
| Full bindingstid | Median 11,1 min + 3 min kvittering = 14,1 min | Fase 1: 3 min. Fase 2 (hvis kom): 6 min (hoved) |
| Datagrunnlag | BRIS-beregnet (`Første_ressurs_fremme − Dato_og_Tid` + kvittering) | Operatør-informert (Fase 1), p og Y kalibrert (Fase 2) |

### 4.2 D-aba Fase 2 — empirisk kalibrering av p og Y

**p (andel D-aba med nødtelefon etter call-out):**

Empirisk underkant-estimat fra sekvensgap-metoden (sammenstilte anrop innen 0–Δ min etter en D-aba):

| Vindu | Andel D-aba med synlig sammenstilt anrop |
|---|---:|
| 90 s – 3 min | 8,7 % |
| 90 s – 5 min | 16,7 % |
| 90 s – 10 min | 28,8 % |
| 90 s – 15 min | 36,9 % |

Dette fanger kun nødtelefoner registrert som eget 110-ID. Nødtelefoner logget *inni* hovedoppdraget uten eget 110-ID er usynlige for sekvensgap-metoden. Operatørens kvalitative beskrivelse («ofte kommer det nødanrop etter call-out») og empirisk observasjon tilsier at reell andel ligger betydelig høyere enn 30–40 %.

Valgte scenarioverdier:

| Scenario | p | Y (min) |
|---|---:|---:|
| Lav (konservativ) | 0,30 | 3 |
| **Hoved** | **0,50** | **6** |
| Høy (pessimistisk) | 0,70 | 10 |

**Y (bindingstid Fase 2):** basert på operatørens beskrivelse av nødtelefon-intervju, veiledning til brannpanel, områdeavklaring, evt. avbryte utrykning, tilbakestilling av alarm. Estimat 3–10 min dekker spennet fra kort avklaring til lengre panel-veiledning.

### 4.3 Reproduserbarhet

Fase 2-events genereres deterministisk ved at hver D-aba tildeles Fase 2 hvis `rng.random() < p`, der `rng = np.random.default_rng(SEED_DABA)` med `SEED_DABA = 20260419`. Dette gir identiske resultater ved gjentatt kjøring og muliggjør sensitivitetsanalyse ved å variere `p` og `Y`.

---

## 5. LABA-dybdeanalyse — empirisk kalibrering av L-aba

### 5.1 Formål og metode

For å validere bindingstidsestimatet for L-aba (tidligere antatt 3 min) ble det trukket et stratifisert utvalg på 50 L-aba-hendelser fra 110 Sør-Vest 2025 (populasjon: 5 495 L-aba før V3-regelen, 3 430 etter). Utvalget er stratifisert på måned (4 per måned for 10 måneder + 5 per måned for 2 måneder) med fast random seed (20260418) for reproduserbarhet.

Hendelsene ble manuelt gjennomgått av en operatør ved 110 Sør-Vest som for hver hendelse registrerte:

- `T_alarm_inn` — når ABA-signalet ble mottatt i LEO
- `T_nødtelefon_inn` — når eventuell nødtelefon fra stedet ble besvart
- `T_avklart` — når operatør bekreftet ufarlig årsak
- `T_operatør_frigjort` — når oppdrag ble lukket

Bindingstid beregnes automatisk fra `T_alarm_inn` til `T_operatør_frigjort`. Kommentarfelt brukes til klassifiseringsobservasjoner.

### 5.2 Resultater

**Hele utvalget (n = 49 gyldige):**

| | Verdi |
|---|---:|
| Mean | 6,63 min |
| Median | 2,97 min |
| Std | 9,24 min |
| P90 | 13,73 min |
| P95 | 26,61 min |
| Max | 51,77 min |
| 95 % CI mean (bootstrap) | [4,41; 9,55] |

**Kilde = Alarm-subset (V3-definert L-aba, n = 30):**

| | Verdi |
|---|---:|
| Mean | 5,88 min |
| Median | 2,87 min |
| P90 | 11,51 min |
| Max | 28,57 min |
| 95 % CI mean | [3,70; 8,56] |

### 5.3 Valgte parametre

| Scenario | L-aba bindingstid (min) |
|---|---:|
| Lav | 3 (tidligere antakelse, konservativ) |
| **Hoved** | **6** (mean fra Kilde = Alarm-subset, avrundet) |
| Høy | 9 (fanger industrivern-oppfølging og lignende langhalet-tilfeller) |

Median-basert antakelse (3 min) ville undervurdere total eksponering. Mean-basert (6 min) fanger den høyreskjeve fordelingen som drives av langhalede tilfeller (industrivern-tilbakeringing, mangelfull logg, varmekamera-oppfølging). Årlig eksponering L-aba (n = 3 430 etter V3-regel) ved 6 min = ca. 343 operatørtimer/år.

### 5.4 Klassifiseringsobservasjoner

Utover bindingstiden dokumenterte dybdeanalysen at 12 av 49 (24,5 %) L-aba-hendelser i V2-definisjonen ikke representerte automatisk brannalarm i operativ forstand. Denne observasjonen motiverte V3-regelen om `Kilde = Alarm` (§2.3).

---

## 6. Skjulte (sammenstilte) anrop

Sammenstilte anrop identifiseres via sekvensgap-metoden: for hver dag-ID i `110_ID`-nummereringen (`B06-ÅÅMMDD-NNN`) identifiseres manglende sekvensnumre og estimeres til å representere anrop som ble mottatt men ikke gitt eget oppdrag-ID (typisk andre innringer om samme hendelse).

- Totalt identifisert: 18 901 skjulte anrop for 110 Sør-Vest 2025 (korreksjonsfaktor 1,305× over registrert oppdragsvolum)
- Bindingstid: 1 min per skjult anrop (antatt)
- Op-binder: 1 op

Skjulte anrop inngår i både Variant A (beredskap) og Variant B (total belastning).

---

## 7. Modellens struktur — oppsummering

### 7.1 Variant A (beredskapsbelastning)

Inkluderer kun hendelser som utløser beredskapsrespons: D-pri1, D-aba (begge faser), skjulte anrop. D-aba Fase 2 bruker hoved-scenario (p = 0,50, Y = 6 min) som standard; sensitivitet rapporteres separat.

### 7.2 Variant B (total operativ belastning)

Inkluderer alle kategorier: D-pri1, D-aba, S, L-aba, L-hendelse, L-ukjent, F, V, skjulte anrop. Tre scenarioer kjøres (lav / hoved / høy).

### 7.3 Bindingstidsantakelser per scenario

| Kategori | Lav | Hoved | Høy | Op-binder |
|---|---:|---:|---:|---:|
| D-pri1 | databasert (median 14,1) | databasert | databasert | 2 |
| D-aba Fase 1 | 3 | 3 | 3 | 1 |
| D-aba Fase 2 (p, Y) | 0,30 / 3 | 0,50 / 6 | 0,70 / 10 | 1 |
| S | 1 | 2 | 4 | 1 |
| L-aba | 3 | 6 | 9 | 1 |
| L-hendelse | 3 | 5 | 8 | 1 |
| L-ukjent | 1 | 3 | 5 | 1 |
| F | 0,25 | 0,5 | 1 | 1 |
| V | 0,5 | 1 | 2 | 1 |
| Skjult | 1 | 1 | 1 | 1 |

---

## 8. Resultater 110 Sør-Vest 2025

### 8.1 Kategorifordeling etter V3

| Kategori | N | Andel |
|---|---:|---:|
| D-pri1 | 4 499 | 7,3 % |
| D-aba | 3 056 | 4,9 % |
| S | 22 542 | 36,4 % |
| L-aba | 3 430 | 5,5 % |
| L-hendelse | 4 298 | 6,9 % |
| L-ukjent | 16 768 | 27,1 % |
| F | 6 824 | 11,0 % |
| V | 547 | 0,9 % |
| **Total** | **61 964** | **100 %** |

### 8.2 Kapasitetsfordeling — Variant A (beredskap)

| Skift | Normal | Brudd | Svikt | n |
|---|---:|---:|---:|---:|
| Alle | 59,6 % | 17,9 % | 22,5 % | 27 960 |
| Dag hverdag (c=3) | 69,2 % | 15,9 % | 14,9 % | 15 944 |
| Natt/helg (c=2) | 46,9 % | 20,5 % | **32,6 %** | 12 016 |

### 8.3 Kapasitetsfordeling — Variant B hoved (total belastning)

| Skift | Normal | Brudd | Svikt | n |
|---|---:|---:|---:|---:|
| Alle | 53,9 % | 20,1 % | 25,9 % | 82 369 |
| Dag hverdag (c=3) | 58,9 % | 19,0 % | 22,0 % | 53 952 |
| Natt/helg (c=2) | 44,4 % | 22,2 % | **33,4 %** | 28 417 |

### 8.4 Sensitivitetsspenn natt/helg (c=2), Variant B

| | Lav | Hoved | Høy |
|---|---:|---:|---:|
| Normal | 51,1 % | 44,4 % | 38,1 % |
| Brudd | 18,8 % | 22,2 % | 24,2 % |
| Svikt | 30,1 % | 33,4 % | 37,7 % |

Hovedfunnet er robust: uavhengig av D-aba Fase 2-antakelser er 30–38 % av beredskapsanrop på natt/helg i Svikt-tilstand.

---

## 9. Begrensninger og konservatisme

1. **Fase 2-binding er partielt synlig.** Empirisk estimat (17–37 % sammenstilte innen 5–15 min) er underkant fordi nødtelefoner logget inni hovedoppdraget ikke fanges.
2. **Klassifiseringspresisjon.** LABA-dybdeanalysen viste at ca. 25 % av V2-L-aba var feilklassifisert. V3-regelen (Kilde = Alarm) fjerner det meste, men en restandel kan fortsatt eksistere.
3. **Nasjonal sammenlignbarhet.** Andre sentraler (særlig Sør-Øst og Oslo med ≈ 0 % L-aba i DSB-data) kan ha ulik registreringspraksis. Benchmarking på tvers krever felles klassifiseringsregler.
4. **Deterministisk Fase 2-sampling.** Samme D-aba får alltid Fase 2 eller ikke (basert på fast seed). Reproduserbart, men undervurderer stokastisk variasjon. En DES-modell ville fanget dette bedre.

---

## 10. Endringslogg

| Dato | Endring |
|---|---|
| 2026-04-15 | V2-modell ferdigstilt: alle hendelser som 1 slot, L-aba = 3 min |
| 2026-04-18 | LABA-dybdeanalyse utfylt av lokal operatør (n = 50) |
| 2026-04-19 | V3-regel: Kilde = Alarm kreves for L-aba og D-aba. L-aba bindingstid 3 → 6 min |
| 2026-04-19 | Op-binder-semantikk innført. D-pri1 (2 ops × 14 min) og D-aba (Fase 1 + Fase 2) splittet |
| 2026-04-19 | Fase 2-parametre kalibrert (p = 0,50, Y = 6 min hoved) |
| 2026-04-19 | Skript oppdatert: `konflikt_total_belastning.py`, `nasjonal_oversikt.py`, `nasjonal_2025_analyse.py`, `uttrekk_laba_sorvest.py` |

---

## 11. Referanser til kildedata

- **BRIS 2025 Sør-Vest:** `004 data/*TESTDATASETT.xlsx` (61 964 rader)
- **DSB nasjonal 2025:** `004 data/2025_fullrapport_110_alle_sentraler_fra_dsb.xlsx` (508 228 rader)
- **LABA-dybdeanalyse (utfylt):** `analyse/laba_sorvest_2025_dybdeanalyse ferdig utfylt.xlsx`
- **Primær-modellskript:** `analyse/scripts/konflikt_total_belastning.py`
- **Prosedyre- og beredskapsanalyse 110 Sør-Vest:** interne dokumenter (kap 4 og 6 referanser)
