# Ønskeliste — BRIS-datauttrekk for kapasitets- og belastningsanalyser ved 110-sentraler

**Utarbeidet av:** Rune Grødem, student LOG650 Forskningsprosjekt, Høgskolen i Molde
**Kontakt:** rune.grodemm@himolde.no
**Dato:** april 2026
**Mottaker:** DSB (til videre dialog og vurdering)

---

## 1. Bakgrunn og formål

Brannvesenet har en nasjonal dimensjoneringsforskrift (FOR-2023-01-06-23) som setter kvantitative, etterprøvbare krav til antall brannmannskap basert på innbyggertall og responstid. **Ingen tilsvarende nasjonal standard finnes for 110-operatører.** Bemanningsnivået fastsettes lokalt gjennom ROS- og beredskapsanalyser som er kvalitative og vanskelige å etterprøve på tvers av sentraler.

I forbindelse med forskningsprosjektet LOG650 ved Høgskolen i Molde («I hvilken grad samsvarer faktisk bemanning ved norske 110-sentraler med kapasitetsbehovet beregnet fra historiske hendelsesdata og køteoretiske modeller?») er det gjennomført en systematisk gjennomgang av de data som i dag er tilgjengelig via BRIS-uttrekk og DSBs årsrapporter. Denne gjennomgangen har avdekket flere data-hull som begrenser hvilke analyser som lar seg gjennomføre.

Dette dokumentet er en **prioritert ønskeliste** over data som — hvis gjort tilgjengelig i BRIS-uttrekk — vil muliggjøre kvantitativ bemannings- og belastningsanalyse på to nivåer:

1. **Sentral-nivå** (benchmarking på tvers av de 12 sentralene)
2. **Operatør-nivå** (dypere analyser av individuell belastning og arbeidsmønster)

Listen er utarbeidet fra **et 110-operativt perspektiv** med fokus på data som direkte påvirker evnen til å dimensjonere og evaluere bemanning.

---

## 2. Avgrensning mot tilstøtende systemer

For å unngå duplisering bygger ønskelisten på at følgende data dekkes — eller vil dekkes — av andre systemer:

| System | Forventet innhold |
|---|---|
| **Alarmmottak (dagens lokale systemer)** | Adresse, objekt-ID, objekttype, service-kontrakt for ABA-tilknytning |
| **Transwire (kommende nasjonalt ABA-system)** | Strukturert objektregister, ABA-historikk, sone/gruppe-informasjon |
| **Frequentis ICCS (nytt kommunikasjonssystem)** | Samtale-metadata, linje-type, samtalehåndtering |

Ønskelisten fokuserer derfor på **BRIS-native data** — det vil si oppdrags- og hendelsesdata som det er naturlig at 110 registrerer og lagrer som en del av saksbehandlingen, og som i dag enten ikke registreres, ikke eksporteres, eller ikke er lenket mot andre objekter i uttrekket.

Der det er overlapp med kommende systemer, er det ønskelig at BRIS **peker til** (f.eks. Transwire-objekt-ID) snarere enn duplisere innholdet.

---

## 3. Status i dag — hvilke analyser lar seg gjennomføre

Gjennomgangen av DSB-datasettet for 2025 (508 228 oppdrag, alle 12 sentraler) viser følgende status:

| Analyse | Status i dag | Begrensning |
|---|---|---|
| Totalvolum per sentral | ✅ Direkte | — |
| Kategorifordeling (D/S/L-aba/L-hendelse/L-ukjent/F/V) | ⚠️ Inferert | Ingen eksplisitt kategori-kolonne; må utledes via Oppdragstype × Opprinnelig oppdragstype × Ressurs varslet |
| Bindingstid for utrykning (D) | ⚠️ Delvis | Alarmbehandlingstid kun fylt for ~12 % av rader |
| Bindingstid for ikke-utrykning (S, L, F, V) | ❌ Ingen data | Må estimeres — denne studien bruker manuell LEO-oppslag (50 hendelser) som validering |
| Samtalevarighet | ❌ Ingen data | T1-anrop (88 % av volum) har ingen tidsregistrering |
| Operatør-belastning | ❌ Ingen data | Operatør-ID har 0 % dekning i dagens BRIS-uttrekk |
| Makkerpar-samhandling | ❌ Ingen data | Umulig å måle uten operatør-ID |
| Samtidighet og kø | ⚠️ Inferert | Sammenstilte anrop utledes via gap-analyse i 110 ID-sekvens; overførte anrop kan ikke skilles fra sammenstilte |
| Faktisk vs planlagt bemanning | ❌ Ingen data | MOB-selvrapportering er årsaggregert planlagt bemanning |
| Realiseringsgrad av varslinger | ✅ Delvis | «Rykket ut»-timestamp er tilgjengelig, men ikke avlysningsgrunn |

---

## 4. Prioritert ønskeliste

Prioriteringen er basert på hvilke analyser dataene låser opp. **Høy** = direkte nødvendig for kapasitetsdimensjonering. **Medium** = muliggjør dypere analyse. **Lav** = kvalitetssikring og auditering.

### 4.1 Høy prioritet — kjerne-analyser for bemanningsdimensjonering

| # | Data | Begrunnelse (hvilken analyse) |
|---|---|---|
| 1 | **Operatør-ID per anrop og per oppdrag** (pseudonymisert) | Grunnleggende forutsetning for all operatør-nivå-analyse: belastning per operatør, makkerpar-samhandling, etterarbeidstid, handovers |
| 2 | **Samtalevarighet for alle samtaler** (ikke kun D) | Eliminerer prosjektets største datagap. I dag har 88 % av volumet (T1-henvendelser) ingen tidsregistrering, så bindingstid må estimeres skjønnsmessig |
| 3 | **Eksplisitt samtale↔oppdrag-tilknytning** | Muliggjør direkte måling av sammenstilte anrop og operatørtid per hendelse. I dag må sammenstilte utledes via gap-analyse |
| 4 | **Ventetid før besvarelse** + antall samtaler på vent ved ankomst | Grunnlag for direkte Erlang-A/Erlang-C-modellering. I dag er ventetider helt fraværende — vi kan ikke validere modellantakelser |
| 5 | **Skift-bemanningsliste** (operatør-IDer som var på vakt, per time eller per skift) | Kobler faktisk bemanning til faktisk belastning. I dag er MOB-selvrapportering årsaggregert planlagt bemanning, ikke faktisk |
| 6 | **Eksplisitt V3-lignende kategori-felt** satt av operatør (D/S/L-aba/L-hendelse/F/V eller tilsvarende) | Eliminerer klassifiseringslogikk som må utledes via fuzzy-matching av Oppdragstype og Opprinnelig oppdragstype |

### 4.2 Medium prioritet — dypere operatør- og kø-analyser

| # | Data | Begrunnelse |
|---|---|---|
| 7 | **Ringt-til-nummer** (nødnummer 110 / servicenummer / pri1-linje / trippelvarsling) | Skiller innkommende linjetype — avdekker hvor mye av volumet som er samtale vs overføring/trippelvarsling |
| 8 | **Innringer-kategori** (publikum / objekteier / servicetekniker / nabosentral / AMK / politi) | Kontekst for kategorisering; forklarer f.eks. hvorfor noen sentraler har høyere S-andel |
| 9 | **Overføring-flagg** + destinasjon (ut/inn) | Skiller sammenstilte anrop fra overførte anrop (30-sek-regel). Dette er sentralt for korrekt tolkning av «skjulte 110 ID-sekvenser» som i dag varierer fra 23 % (Sør-Vest) til 65 % (Finnmark) |
| 10 | **Avbrutt-status og grunn** (innringer la på / operatør avsluttet / system-drop) | Tredje komponent som forklarer skjulte sekvenser |
| 11 | **Avlysningsgrunn** når ressurs varslet men ikke rykket ut | Kvantifiserer «tidlig varsling, avbryt hvis unødig»-praksisen. Våre data viser at 75–99 % av varslede faktisk rykker ut, men avlysningsgrunn er i dag fraværende |
| 12 | **Etterarbeidstid per oppdrag** (tid fra ressurs ledig til oppdrag lukket) | Ikke fanget i dag. Relevant for å måle faktisk operatørbinding utover den aktive fasen |
| 13 | **Ressurs-kategori varslet** (mannskapsbil/tankbil/stigebil/drone/farlig gods) | Kapasitetsbelastning varierer med type utalarmering — ikke alle D er like belastende for operatøren |
| 14 | **Trippelvarsling-flagg** + deltakende etater + samhandlingsvarighet | Kvantifiserer samhandling med AMK/politi — en stor del av den skjulte operatørbelastningen i dag |
| 15 | **Operatør-handover-logg** (oppdrag byttet mellom operatører, med tidspunkt) | Fanger makkerpar-overlevering og vaktskift-overføringer; i dag umulig å spore |
| 16 | **Operatør-rolle på vakten** (operatør / vaktleder / trainee / vikar — flagg, ikke person) | Kobler kapasitetsmodellens VL-korreksjon (c_eff = c_total − 1) til reelle data |

### 4.3 Lav prioritet — kvalitetssikring og dypere statistikk

| # | Data | Begrunnelse |
|---|---|---|
| 17 | **Call recording-ID / lenke** | Audit og kvalitetskontroll; enable stikkprøve-validering av data |
| 18 | **Mikrosekund-presise ankomsttidspunkter** (utover sekund-presisjon) | Gir grunnlag for rigorøs Poisson-test og burst-deteksjon på ankomstprosessen |
| 19 | **Pause/logout-tidspunkter per operatør** | Gjør det mulig å beregne faktisk aktiv tid (effektiv c) framfor påmeldt tid |
| 20 | **Stillingsstatus-flagg** (fast/vikar/ekstrahjelp/trainee) per operatør-ID | Kobler spørreskjema-spørsmål om vikarbruk direkte til operativ kapasitet |
| 21 | **Omklassifiserings-/korreksjons-logg** (hvis oppdrag endrer type etter lukking) | Synliggjør datakvalitet-arbeid og kan bidra til bedre kategorisering over tid |
| 22 | **Geokoordinater** (supplement til adresse) | Mer presis analyse av responstid, geografisk spredning og hendelsesklynger |

---

## 5. Hvilke analyser dette muliggjør

### 5.1 På sentral-nivå (nasjonal benchmarking)

- **Direkte kø-modellering** uten å måtte estimere ventetider og service-tider
- **Faktisk vs planlagt bemanning** — synliggjør reell belastning utover det MOB-rapporteringen fanger
- **Dekomponering av skjulte 110 ID-sekvenser** i sammenstilte/overførte/avbrutte — gjør sentralene direkte sammenlignbare
- **Burst-deteksjon** (ring-flom) basert på faktiske ankomsttidspunkter
- **Sesongvariasjon og tidsbasert belastning** med tilstrekkelig oppløsning
- **Dimensjoneringsstandard-underlag** — hvilken bemanning kreves for at X % av beredskapshendelser håndteres med makkerpar

### 5.2 På operatør-nivå (i dag helt utilgjengelig)

- **Individuell belastning:** antall oppdrag, varighet per oppdrag, etterarbeidstid per operatør per skift
- **Makkerpar-samhandling:** hvor ofte to operatører faktisk jobber sammen på samme hendelse, hvor lenge, og hvordan det påvirker håndteringstid
- **Handovers** mellom operatører (vaktskift, solo→makker, vikar-overtakelse)
- **Arbeidsmønster-fordeling:** hvor mye tid går til samtale, etterarbeid, pause, pauserom
- **Operatør-effektivitet** (internt benchmark innen en sentral) — utelukkende for kompetanseutvikling og risikohåndtering, ikke individuell vurdering

### 5.3 På nasjonalt nivå

- **Generalisering til dimensjoneringsstandard:** hvilke strukturelle prediktorer (volum, innbyggertall, areal, objekt-tetthet) korrelerer med reelt bemanningsbehov
- **Scenarioanalyse:** simulere effekten av +1 operatør, skift-omlegging, sammenslåing av sentraler
- **Sammenligning mot internasjonale standarder** (f.eks. NENA STA-020.1 for 9-1-1)
- **Kvalitetsstyring** — hvilke sentraler ligger innenfor normalspekter, hvilke avviker, hvorfor

---

## 6. Tekniske og praktiske hensyn

- **Anonymisering:** Operatør-ID kan være pseudonymisert (hash eller løpenummer) for å beskytte individer. Identitet trenger ikke knyttes til ID i uttrekk brukt for forskning og benchmarking.
- **Historikk:** Minimum 3 års historikk er ønskelig for trendanalyser; 5 år for robuste sesongestimater.
- **Eksportformat:** Strukturert (CSV/Parquet/JSON) med konsistent koding (UTF-8). Dagens DSB-fullrapport er funksjonell, men krever fuzzy-matching på enkelte felt.
- **Frekvens:** Årlig oppdatert uttrekk er minimum; månedlig eller kvartalsvis vil støtte kontinuerlig kvalitetsstyring.
- **Tilgangsprosess:** Formalisert via DSB eller sektormyndighet — særlig for data som kan knyttes til operatør-nivå.
- **Kobling mot tilstøtende systemer:** Uttrekkformatet bør spesifisere **eksterne nøkler** (Transwire-objekt-ID, ICCS samtale-ID, kommune-nr) snarere enn å duplisere data fra disse systemene.

---

## 7. Anbefalt prioriteringsrekkefølge

Dersom tilgjengeliggjøring må fases, er følgende rekkefølge anbefalt basert på hvor raskt de låser opp nye analysemuligheter:

**Trinn 1 (umiddelbart mest verdifullt):**
- Operatør-ID (pseudonymisert) — #1
- Samtalevarighet for alle samtaler — #2
- Eksplisitt samtale↔oppdrag-tilknytning — #3

**Trinn 2 (neste år):**
- Ventetid og samtidighet — #4
- Skift-bemanningsliste — #5
- Eksplisitt kategori-felt — #6

**Trinn 3 (integrasjon med nye systemer):**
- Linje/innringer-data (koordineres med Frequentis ICCS) — #7, #8
- Overføring- og avbrutt-data (koordineres med ICCS) — #9, #10
- ABA-kobling (koordineres med Transwire) — knytte BRIS til Transwire-objekt-ID

**Trinn 4 (dypere analyse):**
- Etterarbeidstid, ressurs-kategori, trippelvarsling-data — #11–#14
- Rolle-flagg, handover-logg — #15, #16
- Lav-prioritet kvalitetsdata — #17–#22

---

## 8. Avsluttende merknad

Denne ønskelisten er utarbeidet som del av et forskningsprosjekt ved Høgskolen i Molde med 110 Sør-Vest som primærcase, men er ment å gi verdi for **alle 12 norske 110-sentraler** og for DSB som myndighet. Den speiler observasjoner fra gjennomgang av DSBs egne datasett (MOB, BRIS fullrapport 2025) samt interne beredskapsanalyser.

Forslagene er ikke ment som kritikk av dagens registreringspraksis, men som innspill til hvordan BRIS-uttrekket kan videreutvikles for å støtte kvantitativ kapasitetsanalyse som i dag mangler nasjonalt referansegrunnlag.

Kontakt for dialog, avklaringer eller utdyping:

- **Rune Grødem** — rune.grodemm@himolde.no
- Student, LOG650 Forskningsprosjekt, Høgskolen i Molde
- Operatør/vaktleder, 110 Sør-Vest
