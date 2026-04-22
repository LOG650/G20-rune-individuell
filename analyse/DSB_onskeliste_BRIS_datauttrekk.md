# Ønskeliste — BRIS-datauttrekk for kapasitets- og belastningsanalyser ved 110-sentraler

**Utarbeidet av:** Rune Grødem, student LOG650 Forskningsprosjekt, Høgskolen i Molde — Operatør, 110 Sør-Vest
**Kontakt:** rune.grodem@rogbr.no
**Dato:** april 2026
**Mottaker:** DSB (til videre dialog og vurdering)

---

## 1. Bakgrunn og formål

Dagens BRIS-uttrekk og MOB-årsrapporter er ikke tilstrekkelig til å gjennomføre robust, sammenlignbar bemannings- og belastningsanalyse på tvers av de 12 norske 110-sentralene. **Dette dokumentet er en prioritert ønskeliste** over data som — hvis gjort tilgjengelig i fremtidige BRIS-uttrekk — vil muliggjøre kvantitativ kapasitetsanalyse på to nivåer: sentral-nivå (nasjonal benchmarking) og operatør-nivå (individuell belastning og arbeidsmønster).

Bakgrunnen er kort: brannvesenet har en nasjonal dimensjoneringsforskrift (FOR-2023-01-06-23) som setter kvantitative bemanningskrav basert på innbyggertall og responstid. Ingen tilsvarende nasjonal standard finnes for 110-operatører — bemanning fastsettes lokalt gjennom kvalitative ROS-analyser. Behovet for et kvantitativt nasjonalt referansegrunnlag er identifisert i forskningsprosjektet LOG650 ved Høgskolen i Molde, der en gjennomgang av DSBs egne datasett (BRIS fullrapport 2025: 508 228 oppdrag, MOB 2022–2025) har avdekket konkrete data-hull. Listen er utarbeidet fra et 110-operativt perspektiv.

### 1.1 Begrepsforklaring

For å gjøre dokumentet leselig uten å kreve kjennskap til den underliggende rapporten, defineres her de sentrale begrepene som brukes:

| Begrep | Forklaring |
|---|---|
| **Op-binder** | Et tidsavgrenset intervall der én eller to operatører er aktivt bundet av en hendelse. Brukes som måleenhet for kapasitetsbelastning. |
| **D-pri1** | Pri-1-utrykning (bygningsbrann, trafikkulykke, farlig gods). Krever to operatører bundet parallelt («makkerpar»). |
| **D-aba** | Utrykning utløst av automatisk brannalarm (ABA). Håndteres serielt av én operatør (kvittering + oppdragsopprettelse + call-out, ca. 3 min). |
| **L-aba** | Automatisk brannalarm avklart uten utrykning (f.eks. matlaging bekreftet av nødtelefon innen 90 sek). |
| **Makkerpar-driftsstandard** | Prosedyrekrav om at to operatører (RØD = samtale med innringer + GUL = ressursvarsling og samband) håndterer hver pri-1-hendelse parallelt fra første sekund av akuttfasen. |
| **T1-henvendelser** | Korte telefonhenvendelser uten registrert hendelsestype (henvendelser, avklaringer, lukkede saker uten kategori). Utgjør ~88 % av samtalevolumet ved 110 Sør-Vest 2025. |
| **V3** | Versjon 3 av klassifiseringsregelen utviklet i forskningsprosjektet, der ABA-kategoriene (D-aba, L-aba) krever Kilde=Alarm for å skille reelle alarmsignaler fra publikumsmeldinger feilklassifisert som ABA. |
| **MOB** | DSBs årlige selvrapporteringsskjema fra 110-sentralene (planlagt bemanning, anropsvolum, oppdragstall). |
| **BRIS** | DSBs hendelsesdatabase med fullrapport-eksport per oppdrag (44 kolonner per rad). |

---

## 2. Avgrensning mot tilstøtende systemer

For å unngå duplisering bygger ønskelisten på en **forutsetning** om at følgende data kan hentes ut — i strukturert, eksportbart format — fra andre systemer enn BRIS:

| System | Forventet innhold | Status / forbehold |
|---|---|---|
| **Alarmmottak (dagens lokale systemer)** | Adresse, objekt-ID, objekttype, service-kontrakt for ABA-tilknytning | Varierer mellom sentraler; nasjonal eksport ikke etablert |
| **Transwire (kommende nasjonalt ABA-system)** | Strukturert objektregister, ABA-historikk, sone/gruppe-informasjon | Under innføring — datatilgang for analyse må avklares |
| **Frequentis ICCS (nytt kommunikasjonssystem)** | Samtale-metadata, linje-type, samtalehåndtering | Under innføring — eksport-API for forskning ikke avklart |

**Hvis dataene over ikke lar seg hente ut fra disse systemene** i et format som er egnet for sammenstilt nasjonal analyse, vil det være naturlig at de tilsvarende feltene **inkluderes som en del av BRIS-uttrekket** (eventuelt som referansenøkler mot kildesystemet). For hver tilstøtende systemkategori bør DSB derfor avklare: (a) er data praktisk uttrekkbart der i dag, (b) hvis nei, hva er tidshorisont for at det skal bli det, og (c) hvis tidshorisonten er lang eller usikker, bør tilsvarende felt vurderes for BRIS-eksport i mellomtiden.

Ønskelisten under fokuserer derfor på **BRIS-native data** — det vil si oppdrags- og hendelsesdata som det er naturlig at 110 registrerer og lagrer som en del av saksbehandlingen, og som i dag enten ikke registreres, ikke eksporteres, eller ikke er lenket mot andre objekter i uttrekket. Der det er overlapp med tilstøtende systemer, er det ønskelig at BRIS **peker til** (f.eks. Transwire-objekt-ID) snarere enn å duplisere innholdet — *forutsatt* at de tilstøtende systemene faktisk leverer den forutsatte dataen.

---

## 3. Status i dag — hvilke analyser lar seg gjennomføre

Gjennomgangen av DSB-datasettet for 2025 (508 228 oppdrag, alle 12 sentraler) viser følgende status:

| Analyse | Status i dag | Begrensning |
|---|---|---|
| Totalvolum per sentral | ✅ Direkte | — |
| Kategorifordeling (D/S/L-aba/L-hendelse/L-ukjent/F/V) | ⚠️ Inferert | Ingen eksplisitt kategori-kolonne; må utledes via Oppdragstype × Opprinnelig oppdragstype × Ressurs varslet |
| Bindingstid for utrykning (D) | ⚠️ Delvis | Alarmbehandlingstid kun fylt for ~12 % av rader |
| Bindingstid for ikke-utrykning (S, L, F, V) | ❌ Ingen data | Må estimeres skjønnsmessig eller via tidkrevende manuell LEO-oppslag¹ |
| Samtalevarighet | ❌ Ingen data | T1-anrop (88 % av volum) har ingen tidsregistrering |
| Operatør-belastning | ❌ Ingen data | Operatør-ID har 0 % dekning i dagens BRIS-uttrekk |
| Makkerpar-samhandling | ❌ Ingen data | Umulig å måle uten operatør-ID |
| Samtidighet og kø | ⚠️ Inferert | Sammenstilte anrop utledes via gap-analyse i 110 ID-sekvens; overførte anrop kan ikke skilles fra sammenstilte |
| Faktisk vs planlagt bemanning | ❌ Ingen data | MOB-selvrapportering er årsaggregert planlagt bemanning |
| Realiseringsgrad av varslinger | ✅ Delvis | «Rykket ut»-timestamp er tilgjengelig, men ikke avlysningsgrunn |

¹ *I forskningsprosjektet er bindingstid for L-aba kalibrert via en manuell dybdeanalyse av 50 trukne LEO-loggføringer (hovedparameter bygger på Kilde=Alarm-subsettet, n = 30; et utvidet utvalg n = 100 er under innhenting). Dette er en ressurskrevende workaround som ikke vil være praktisk gjennomførbar for nasjonal benchmarking på tvers av 12 sentraler.*

---

## 4. Prioritert ønskeliste

> **Avgrensningsprinsipp:** Ønskelisten ber **ikke** om at BRIS skal bli et alt-omfattende system. Hvert datapunkt under er enten (a) data som er naturlig at 110 selv registrerer som del av saksbehandlingen og som derfor hører hjemme i BRIS, eller (b) data som primært bør hentes fra et tilstøtende system (Alarmmottak / Transwire / ICCS) — men hvor BRIS bør inneholde en **referansenøkkel** for kobling. Hvis tilstøtende systemer ikke leverer den forutsatte dataen i sammenstilt nasjonalt format (jf. §2), bør tilsvarende felt vurderes for BRIS-eksport i mellomtiden.

Prioriteringen er basert på hvilke analyser dataene låser opp. **Høy** = direkte nødvendig for kapasitetsdimensjonering. **Medium** = muliggjør dypere analyse. **Lav** = kvalitetssikring og auditering.

### 4.1 Høy prioritet — kjerne-analyser for bemanningsdimensjonering

| # | Data | Begrunnelse (hvilken analyse) |
|---|---|---|
| 1 | **Operatør-ID per anrop og per oppdrag** (pseudonymisert) | Grunnleggende forutsetning for all operatør-nivå-analyse: belastning per operatør, makkerpar-samhandling, etterarbeidstid, handovers |
| 2 | **Samtalevarighet for alle samtaler** (ikke kun D) | Eliminerer prosjektets største datagap. I dag har 88 % av volumet (T1-henvendelser) ingen tidsregistrering, så bindingstid må estimeres skjønnsmessig |
| 3 | **Eksplisitt samtale↔oppdrag-tilknytning** (alle innkommende samtaler lenkes til riktig oppdrag-ID, ikke bare den første) | Muliggjør direkte måling av sammenstilte anrop og operatørtid per hendelse. I dag må sammenstilte utledes via sekvensgap-analyse. Lar oss også måle etterfølgende nødtelefoner (D-aba Fase 2 — sannsynlighet $p$ og varighet $Y$ for nødtelefon fra stedet etter ABA-utrykning), som i dag bare kan estimeres som underkant fra sekvensgap fordi mange Fase 2-anrop logges *innenfor* hovedoppdragets ID og er usynlige som egne hendelser |
| 4 | **Ventetid før besvarelse** + antall samtaler på vent ved ankomst | Grunnlag for direkte Erlang-A/Erlang-C-modellering. I dag er ventetider helt fraværende — vi kan ikke validere modellantakelser |
| 5 | **Skift-bemanningsliste** (operatør-IDer som var på vakt, per time eller per skift) | Kobler faktisk bemanning til faktisk belastning. I dag er MOB-selvrapportering årsaggregert planlagt bemanning, ikke faktisk |
| 6 | **Eksplisitt V3-lignende kategori-felt** satt av operatør (D-pri1/D-aba/S/L-aba/L-hendelse/L-ukjent/F/V eller tilsvarende), inkludert eksplisitt skille mellom pri-1-utrykning (makkerpar) og ABA-utrykning (serielt), og krav om Kilde=Alarm for ABA-kategoriene | Eliminerer klassifiseringslogikk som i dag må utledes via fuzzy-matching av Oppdragstype × Opprinnelig oppdragstype × Kilde × Ressurs varslet. Avdekker også vesentlig variasjon mellom sentraler i registreringspraksis (L-aba-andel varierer 0,0–7,5 % mellom sentraler i 2025) |

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

- **Rune Grødem** — rune.grodem@rogbr.no
- Student, LOG650 Forskningsprosjekt, Høgskolen i Molde
- Operatør, 110 Sør-Vest
