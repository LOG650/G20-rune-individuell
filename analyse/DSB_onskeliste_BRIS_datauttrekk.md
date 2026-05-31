# Datagap for nasjonal kapasitetsanalyse av 110-sentraler: ønskeliste for BRIS/LEO, samtalemetadata og bemanningsdata

**Utarbeidet av:** Rune Grødem (student LOG650 Forskningsprosjekt, Høgskolen i Molde; operatør, 110 Sør-Vest)
**Kontakt:** rune.grodem@rogbr.no
**Dato:** mai 2026
**Mottaker:** DSB (til videre dialog og vurdering)

---

## 1. Bakgrunn og formål

Dagens BRIS-uttrekk og MOB-årsrapporter er ikke tilstrekkelig til å gjennomføre robust, sammenlignbar bemannings- og belastningsanalyse på tvers av de 12 norske 110-sentralene. **Dette dokumentet er en prioritert ønskeliste** over data som, hvis gjort tilgjengelig i fremtidige nasjonale uttrekk, vil muliggjøre kvantitativ kapasitetsanalyse på to nivåer: sentral-nivå (nasjonal benchmarking) og operativ rolle-nivå (rolle- og bemanningsmønstre, pseudonymisert og tilgangsstyrt).

Bakgrunnen er kort: brannvesenet har en nasjonal regulering, **brann- og redningsvesenforskriften (FOR-2021-09-15-2755)**, som fra 1. mars 2022 erstattet den tidligere dimensjoneringsforskriften (FOR-2002-06-26-729). Den setter kvantitative krav til organisering, bemanning og innsatstid for brann- og redningstjenesten basert på innbyggertall og responstid. Ingen tilsvarende, kvantitativt operasjonalisert standard finnes for 110-operatørbemanning. Den fastsettes lokalt gjennom kvalitative ROS- og beredskapsanalyser. Behovet for et kvantitativt nasjonalt referansegrunnlag er identifisert i forskningsprosjektet LOG650 ved Høgskolen i Molde, der en gjennomgang av DSBs egne datasett (BRIS fullrapport 2025: 508 228 oppdrag, MOB 2022 til 2025) har avdekket konkrete data-hull. Listen er utarbeidet fra et 110-operativt perspektiv.

**Avgrensning av analysebehov, ikke ett bestemt system.** Flere av feltene under ligger fysisk i andre systemer enn BRIS (samtalehåndtering, alarmmottak, vakt-/bemanningssystem). Ønskelisten er rammet om analysebehovet, *hvilke data trengs for nasjonal kapasitetsanalyse*, ikke om hvilket system de skal hentes fra. Seksjon 2 spesifiserer hvor hvert datapunkt naturlig hører hjemme.

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
| **Sammenstilt anrop** | Et anrop som gjelder en allerede pågående hendelse og trekkes inn i det eksisterende oppdraget, slik at det ikke får en egen synlig rad i BRIS-uttrekket. Binder operatørkapasitet, men er i dag «skjult». Tidsstempel og varighet finnes i LEO. |

---

## 2. Avgrensning mot tilstøtende systemer

For å unngå duplisering bygger ønskelisten på en **forutsetning** om at følgende data kan hentes ut, i strukturert, eksportbart format, fra andre systemer enn BRIS:

| System | Forventet innhold | Status / forbehold |
|---|---|---|
| **Alarmmottak (dagens lokale systemer)** | Adresse, objekt-ID, objekttype, service-kontrakt for ABA-tilknytning | Varierer mellom sentraler; nasjonal eksport ikke etablert |
| **Transwire (kommende nasjonalt ABA-system)** | Strukturert objektregister, ABA-historikk, sone/gruppe-informasjon | Under innføring, datatilgang for analyse må avklares |
| **Frequentis ICCS (nytt kommunikasjonssystem)** | Samtale-metadata, linje-type, samtalehåndtering | Under innføring, eksport-API for forskning ikke avklart |

**Hvis dataene over ikke lar seg hente ut fra disse systemene** i et format som er egnet for sammenstilt nasjonal analyse, vil det være naturlig at de tilsvarende feltene **inkluderes som en del av BRIS-uttrekket** (eventuelt som referansenøkler mot kildesystemet). For hver tilstøtende systemkategori bør DSB derfor avklare: (a) er data praktisk uttrekkbart der i dag, (b) hvis nei, hva er tidshorisont for at det skal bli det, og (c) hvis tidshorisonten er lang eller usikker, bør tilsvarende felt vurderes for BRIS-eksport i mellomtiden.

Ønskelisten under fokuserer derfor på **BRIS-native data**, det vil si oppdrags- og hendelsesdata som det er naturlig at 110 registrerer og lagrer som en del av saksbehandlingen, og som i dag enten ikke registreres, ikke eksporteres, eller ikke er lenket mot andre objekter i uttrekket. Der det er overlapp med tilstøtende systemer, er det ønskelig at BRIS **peker til** (f.eks. Transwire-objekt-ID) snarere enn å duplisere innholdet, *forutsatt* at de tilstøtende systemene faktisk leverer den forutsatte dataen.

---

## 3. Status i dag: hvilke analyser lar seg gjennomføre

Gjennomgangen av DSB-datasettet for 2025 (508 228 oppdrag, alle 12 sentraler) viser følgende status:

| Analyse | Status i dag | Begrensning |
|---|---|---|
| Totalvolum per sentral | ✅ Direkte | (ingen) |
| Kategorifordeling (D/S/L-aba/L-hendelse/L-ukjent/F/V) | ⚠️ Inferert | Ingen eksplisitt kategori-kolonne; må utledes via Oppdragstype × Opprinnelig oppdragstype × Ressurs varslet |
| Bindingstid for utrykning (D) | ⚠️ Delvis | Alarmbehandlingstid kun fylt for ~12 % av rader |
| Bindingstid for ikke-utrykning (S, L, F, V) | ❌ Ingen data | Må estimeres skjønnsmessig eller via tidkrevende manuell LEO-oppslag¹ |
| Samtalevarighet | ❌ Ingen data | T1-anrop (88 % av volum) har ingen tidsregistrering |
| Operatør-belastning | ❌ Ingen data | Operatør-ID har 0 % dekning i dagens BRIS-uttrekk |
| Makkerpar-samhandling | ❌ Ingen data | Umulig å måle uten operatør-ID |
| Samtidighet og kø | ⚠️ Inferert | Sammenstilte anrop utgjør 67,6 % av nevneren i kapasitetsmodellen, men eksporteres ikke som egne rader. De må derfor utledes via gap-analyse i 110 ID-sekvensen og plasseres på tidsaksen ved en modellantagelse, noe som alene gir et usikkerhetsbånd på 16,8 til 26,4 % rundt hovedtallet. Tidsstempel og varighet finnes i LEO, men tas ikke med i uttrekket |
| Faktisk vs planlagt bemanning | ❌ Ingen data | MOB-selvrapportering er årsaggregert planlagt bemanning |
| Realiseringsgrad av varslinger | ✅ Delvis | «Rykket ut»-timestamp er tilgjengelig, men ikke avlysningsgrunn |

¹ *I forskningsprosjektet er bindingstid for L-aba kalibrert via en manuell dybdeanalyse av LEO-loggføringer, runde 2 med n = 100 (Kilde=Alarm), som ferdig hovedparameter: mean 4,53 min, 95 % CI [3,74; 5,43]. Dette er en ressurskrevende workaround som ikke vil være praktisk gjennomførbar for nasjonal benchmarking på tvers av 12 sentraler.*

---

## 4. Minimum viable datauttrekk (MVP): hvis bare fem felt kan etableres

Hvis tilgjengeliggjøring må fases over flere år, gir følgende fem datapunkter den klart største analyseverdien per krone og minst personvern- og forvaltningsbelastning. Listen er sortert slik at de første feltene gir konkret styringsnytte for DSB *uavhengig* av om de senere feltene realiseres.

| # | Datapunkt | Hva det låser opp |
|---|---|---|
| **MVP-1** | **Sammenstilte anrop synliggjort i uttrekket** med eksisterende LEO-tidsstempel (sekundnivå) og varighet, som egne rader på moderoppdraget (løpenummer) | Løser prosjektets største enkeltusikkerhet: sammenstilte anrop er 67,6 % av nevneren i kapasitetsmodellen og mangler i dag tidsstempel i uttrekket. Ren uttrekksendring, krever ingenting nytt av operatøren |
| **MVP-2** | **Faktisk bemannet kapasitet per sentral, time og rolle** | Kobler bemanning til belastning på samme tidsoppløsning. Erstatter MOB-årsaggregert planlagt bemanning. Rent styringsdata, ingen individdata |
| **MVP-3** | **Eksplisitt kategori etter harmonisert regel:** D-pri1, D-aba, L-aba, L-hendelse, L-ukjent, S, F, V (med Kilde=Alarm-krav for ABA-kategoriene) | Eliminerer dagens fuzzy-matching-logikk. Harmonisering, ikke ny registreringsbyrde, operatørene registrerer kategori uansett |
| **MVP-4** | **Samtalevarighet for alle samtaler** (ikke kun utrykninger) | Lukker det nest største datagapet: 88 % av volumet (T1) mangler tidsregistrering |
| **MVP-5** | **Pseudonymisert operativ rolle-ID** (RØD/GUL/VL/trainee/vikar, som rolle på vakten, ikke individbasert ID), **kun i tilgangsstyrt forskningsuttrekk** | Muliggjør makkerpar- og handover-analyse uten å eksponere enkeltoperatører |

**Hvorfor denne rekkefølgen?** MVP-1 er en ren uttrekksendring av data som alt finnes i LEO, og løser den største enkeltusikkerheten alene. MVP-1 til MVP-3 er strukturelle felt uten personvernimplikasjoner og løser sammen ca. 70 % av analysebehovet for nasjonal benchmarking. MVP-4 og MVP-5 utvider til service- og rolle-analyse og krever tydeligere tilgangsstyring, men kan etableres separat.

---

## 5. Komplett prioritert ønskeliste

> **Avgrensningsprinsipp:** Ønskelisten ber **ikke** om at BRIS alene skal bli et alt-omfattende system. Hvert datapunkt under er enten (a) data som er naturlig at 110 selv registrerer som del av saksbehandlingen og som derfor hører hjemme i BRIS/LEO, eller (b) data som primært bør hentes fra et tilstøtende system (Alarmmottak / Transwire / ICCS / vakt-/bemanningssystem), men hvor det nasjonale uttrekket bør inneholde en **referansenøkkel** for kobling. Hvis tilstøtende systemer ikke leverer den forutsatte dataen i sammenstilt nasjonalt format (jf. §2), bør tilsvarende felt vurderes for BRIS-eksport i mellomtiden.

Prioriteringen er basert på hvilke analyser dataene låser opp. **Høy** = direkte nødvendig for kapasitetsdimensjonering. **Medium** = muliggjør dypere analyse. **Lav** = kvalitetssikring og auditering.

### 5.1 Høy prioritet: kjerne-analyser for bemanningsdimensjonering

| # | Data | Begrunnelse (hvilken analyse) |
|---|---|---|
| 1 | **Sammenstilte anrop som egne, tidsstemplede rader i uttrekket** (løpenummer på moderoppdraget). Hvert anrop som trekkes inn i et eksisterende oppdrag eksporteres som egen rad knyttet til oppdrags-ID, med **ankomsttidspunkt på sekundnivå** (når samtalen kom, ikke når den ble knyttet til oppdraget) og **samtalevarighet** der den finnes. Sammenstilt, overført og avbrutt skilles med et statusflagg på raden | **Dette er ikke ny registrering, men eksport av data som alt ligger i LEO.** Sammenstilte anrop er 67,6 % av nevneren i kapasitetsmodellen, og fordi de mangler tidsstempel i dagens uttrekk må de plasseres på tidsaksen ved en modellantagelse, noe som alene gir et usikkerhetsbånd på 16,8 til 26,4 % rundt hovedtallet. Med faktiske sekund-tidsstempler måles ankomstkonflikten direkte, og faktisk varighet erstatter dagens konservative 1-minutts-antagelse. Statusflagget skiller samtidig sammenstilt fra overført (30-sek-regel) og avbrutt, uten gap-gjetting. Fanger også etterfølgende nødtelefoner etter ABA-utrykning (D-aba Fase 2), som i dag er usynlige fordi de logges *innenfor* hovedoppdragets ID |
| 2 | **Faktisk bemannet kapasitet** per sentral, time/skift og rolle (operatør / vaktleder / trainee / vikar) | Kobler faktisk bemanning til faktisk belastning på samme tidsoppløsning. I dag er MOB-selvrapportering årsaggregert planlagt bemanning, ikke realisert. Rent styringsdata på sentralnivå |
| 3 | **Eksplisitt kategori-felt** satt av operatør (D-pri1/D-aba/S/L-aba/L-hendelse/L-ukjent/F/V), inkludert eksplisitt skille mellom pri-1-utrykning (makkerpar) og ABA-utrykning (serielt), og krav om Kilde=Alarm for ABA-kategoriene | Eliminerer klassifiseringslogikk som i dag må utledes via fuzzy-matching av Oppdragstype × Opprinnelig oppdragstype × Kilde × Ressurs varslet. Avdekker også vesentlig variasjon mellom sentraler i registreringspraksis (L-aba-andel varierer 0,0 til 7,5 % mellom sentraler i 2025). Harmonisering, ikke ny registreringsbyrde |
| 4 | **Samtalevarighet for alle samtaler** (ikke kun D) | Eliminerer det nest største datagapet. I dag har 88 % av volumet (T1-henvendelser) ingen tidsregistrering, så bindingstid må estimeres skjønnsmessig |
| 5 | **Ventetid før besvarelse** + antall samtaler på vent ved ankomst | Grunnlag for direkte Erlang-A/Erlang-C-modellering. I dag er ventetider helt fraværende, vi kan ikke validere modellantagelser |
| 6 | **Pseudonymisert operativ rolle-ID** per anrop og oppdrag (RØD/GUL/VL/operatør på vakten), **i tilgangsstyrt forskningsuttrekk** | Forutsetning for makkerpar-, handover- og etterarbeidsanalyse. Rollebasert ID gir analytisk verdi uten å eksponere enkeltoperatører. Individbasert pseudonymisert ID kan vurderes som separat, forskningsregulert uttrekk underlagt egen tilgangsstyring |

### 5.2 Medium prioritet: dypere kø- og samhandlingsanalyser

| # | Data | Begrunnelse |
|---|---|---|
| 7 | **Ringt-til-nummer** (nødnummer 110 / servicenummer / pri1-linje / trippelvarsling) | Skiller innkommende linjetype, avdekker hvor mye av volumet som er samtale vs overføring/trippelvarsling |
| 8 | **Innringer-kategori** (publikum / objekteier / servicetekniker / nabosentral / AMK / politi) | Kontekst for kategorisering; forklarer f.eks. hvorfor noen sentraler har høyere S-andel |
| 9 | **Avlysningsgrunn** når ressurs varslet men ikke rykket ut | Kvantifiserer «tidlig varsling, avbryt hvis unødig»-praksisen. Våre data viser at 75 til 99 % av varslede faktisk rykker ut, men avlysningsgrunn er i dag fraværende |
| 10 | **Etterarbeidstid per oppdrag** (tid fra ressurs ledig til oppdrag lukket) | Ikke fanget i dag. Relevant for å måle faktisk operativ binding utover den aktive fasen |
| 11 | **Ressurs-kategori varslet** (mannskapsbil/tankbil/stigebil/drone/farlig gods) | Kapasitetsbelastning varierer med type utalarmering, ikke alle D er like belastende |
| 12 | **Trippelvarsling-flagg** + deltakende etater + samhandlingsvarighet | Kvantifiserer samhandling med AMK/politi, en stor del av den skjulte operative belastningen i dag |
| 13 | **Rolle-handover-logg** (oppdrag byttet mellom roller på vakten, med tidspunkt, rolleflagg, ikke person) | Fanger makkerpar-overlevering og vaktskift-overføringer; i dag umulig å spore |

### 5.3 Lav prioritet: kvalitetssikring og dypere statistikk

| # | Data | Begrunnelse |
|---|---|---|
| 14 | **Anonymisert lenke til samtaleopptak** for tilgangsstyrt forskningsbruk | Stikkprøve-verifisering av datakvalitet og kategorisering. Bør ligge under egen avtale, ikke del av standardeksport |
| 15 | **Geokoordinater** (supplement til adresse) | Mer presis analyse av responstid, geografisk spredning og hendelsesklynger |

Ytterligere kvalitetsdata, som mikrosekund-presise ankomsttidspunkter for rigorøs Poisson- og burst-testing, aggregert stillingstype-fordeling per skift (andel fast/vikar/ekstrahjelp/trainee, uten individkobling) og en omklassifiserings-/korreksjonslogg, kan vurderes på et senere tidspunkt, men er ikke nødvendige for kapasitetsanalysen.

---

## 6. Hvilke analyser dette muliggjør

### 6.1 På sentral-nivå (nasjonal benchmarking)

- **Direkte kø-modellering** uten å måtte estimere ventetider og service-tider
- **Faktisk vs planlagt bemanning**, synliggjør reell belastning utover det MOB-rapporteringen fanger
- **Direkte måling av sammenstilte anrop** med faktisk tidspunkt og varighet (i stedet for inferert via gap-analyse), som skiller sammenstilt fra overført og avbrutt og gjør sentralene direkte sammenlignbare
- **Burst-deteksjon** (ring-flom) basert på faktiske ankomsttidspunkter
- **Sesongvariasjon og tidsbasert belastning** med tilstrekkelig oppløsning
- **Dimensjoneringsstandard-underlag**, hvilken bemanning kreves for at X % av beredskapshendelser håndteres med makkerpar

### 6.2 På operativ rolle-nivå (tilgangsstyrt forskningsbruk)

- **Makkerpar-samhandling:** hvor ofte to operatører faktisk jobber sammen på samme hendelse, hvor lenge, og hvordan det påvirker håndteringstid
- **Rolle-handovers** (vaktskift, solo→makker, RØD↔GUL-rotasjon) som strukturell indikator på operativ binding
- **Belastningsfordeling per rolle** (operatør / vaktleder / trainee / vikar), aggregert per skift og sentral, ikke per individ
- **Effekt av rolle-sammensetning** på driftsstandard (f.eks. når vaktleder må tre inn som operatør)

### 6.3 På nasjonalt nivå

- **Generalisering til dimensjoneringsstandard:** hvilke strukturelle prediktorer (volum, innbyggertall, areal, objekt-tetthet) korrelerer med reelt bemanningsbehov
- **Scenarioanalyse:** simulere effekten av +1 operatør, skift-omlegging, sammenslåing av sentraler
- **Sammenligning mot internasjonale standarder** (f.eks. NENA STA-020.1 for 9-1-1)
- **Kvalitetsstyring**, hvilke sentraler ligger innenfor normalspekter, hvilke avviker, hvorfor

---

## 7. Tekniske og praktiske hensyn

- **Pseudonymisering og tilgangsstyring:** Rolle-ID på vakten er rent rollebasert og inneholder ingen individdata. Individbasert pseudonymisert operatør-ID (hash eller løpenummer) skal være underlagt egen tilgangsavtale, typisk forskningsregulert, og ikke inngå i standardeksport.
- **Historikk:** Minimum 3 års historikk er ønskelig for trendanalyser; 5 år for robuste sesongestimater.
- **Eksportformat:** Strukturert (CSV/Parquet/JSON) med konsistent koding (UTF-8). Dagens DSB-fullrapport er funksjonell, men krever fuzzy-matching på enkelte felt.
- **Frekvens:** Årlig oppdatert uttrekk er minimum; månedlig eller kvartalsvis vil støtte kontinuerlig kvalitetsstyring.
- **Tilgangsprosess:** Formalisert via DSB eller sektormyndighet, særlig for data som kan knyttes til rolle- eller individnivå.
- **Kobling mot tilstøtende systemer:** Uttrekkformatet bør spesifisere **eksterne nøkler** (Transwire-objekt-ID, ICCS samtale-ID, kommune-nr) snarere enn å duplisere data fra disse systemene.

---

## 8. Anbefalt prioriteringsrekkefølge

Dersom tilgjengeliggjøring må fases, er følgende rekkefølge anbefalt basert på hvor raskt de låser opp nye analysemuligheter, og samtidig minimerer personvernrisiko i tidlige trinn:

**Trinn 1 (MVP, umiddelbart mest verdifullt, rene uttrekks- og styringsdata):**
- Sammenstilte anrop som tidsstemplede rader med varighet (#1)
- Faktisk bemannet kapasitet per sentral/time/rolle (#2)
- Harmonisert kategori-felt (#3)

**Trinn 2 (utvidet kø- og service-data):**
- Samtalevarighet for alle samtaler (#4)
- Ventetid og samtidighet (#5)

**Trinn 3 (rolle-analyse, krever tilgangsavtale):**
- Pseudonymisert operativ rolle-ID (#6)

**Trinn 4 (integrasjon med nye systemer):**
- Linje- og innringer-data (#7, #8): koordineres med Frequentis ICCS
- ABA-objektkobling (Transwire-objekt-ID): koordineres med Transwire

**Trinn 5 (dypere analyse):**
- Avlysningsgrunn, etterarbeidstid, ressurs-kategori, trippelvarsling (#9 til #12)
- Rolle-handover-logg (#13)
- Lav-prioritet kvalitetsdata (#14, #15)

---

## 9. Avsluttende merknad

Denne ønskelisten er utarbeidet som del av et forskningsprosjekt ved Høgskolen i Molde med 110 Sør-Vest som primærcase, men er ment å gi verdi for **alle 12 norske 110-sentraler** og for DSB som myndighet. Den speiler observasjoner fra gjennomgang av DSBs egne datasett (MOB, BRIS fullrapport 2025) samt interne ROS- og beredskapsanalyser.

Forslagene er ikke ment som kritikk av dagens registreringspraksis, men som innspill til hvordan det nasjonale datagrunnlaget kan videreutvikles for å støtte kvantitativ kapasitetsanalyse som i dag mangler nasjonalt referansegrunnlag.

Kontakt for dialog, avklaringer eller utdyping:

- **Rune Grødem**, rune.grodem@rogbr.no
- Student, LOG650 Forskningsprosjekt, Høgskolen i Molde
- Operatør, 110 Sør-Vest
