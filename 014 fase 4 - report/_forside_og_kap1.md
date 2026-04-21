---
title: "Kapasitetsstyring og bemanningsdimensjonering ved norske 110-sentraler"
subtitle: "En analyse av operatørkapasitet med prosedyrbasert ankomstkonfliktmodell"
author: "Rune Grødem · G20 Individuell"
date: "April 2026 · Hoved-utkast"
abstract: |
  Norske 110-sentraler er kritisk beredskapsinfrastruktur som mottar nødmeldinger og koordinerer brann- og redningsinnsats. Bemanningsnivået fastsettes lokalt gjennom risiko- og beredskapsanalyser (ROS), men det finnes ingen nasjonal, kvantitativ standard for hvordan operativ belastning oversettes til konkret bemanning. Brannvesenet har derimot en egen dimensjoneringsforskrift (FOR-2023-01-06-23) som setter kvantitative krav basert på innbyggertall og responstid.

  Denne rapporten analyserer i hvilken grad faktisk bemanning ved 110 Sør-Vest (primærcase) samsvarer med kapasitetsbehovet beregnet fra historiske hendelsesdata. En innledende Erlang-C-analyse (M/M/c) viste svært lav systemutnyttelse (høyeste observerte verdi 5,9 %) for alle skifttyper — et resultat som er formelt korrekt, men metodisk utilstrekkelig fordi modellen ikke fanger at sentralens operative prosedyre (makkerpar-drift) krever to operatører parallelt per pri-1-hendelse. Studiens hovedmodell er derfor en **prosedyrbasert ankomstkonfliktmodell** med op-binder-semantikk, som måler sannsynligheten for at et beredskapsanrop ankommer i en tilstand der makkerpar-driftsstandarden ikke kan opprettholdes. Modellen skiller eksplisitt mellom D-pri1 (pri-1-utrykning, makkerpar) og D-aba (ABA-utrykning, serielt).

  Hovedfunnene for 110 Sør-Vest 2025 viser at **32,6 % av beredskapsanropene på natt/helg ankommer i svikt-tilstand** (variant A, beredskapsbelastning), stigende til 33,4 % ved inkludering av total operativ belastning (variant B). Over halvparten av beredskapsanropene på natt/helg ankommer i brudd eller svikt. En scenarioanalyse viser at én ekstra operatør på natt/helg halverer sviktraten (32,8 % → 16,7 %). Resultatene er benchmarket mot nasjonalt datagrunnlag (DSB BRIS 2025, 508 228 oppdrag, alle 12 sentraler). Studien fremstår som en av de første kvantitative kapasitetsanalysene av en norsk 110-sentral basert på historiske hendelsesdata, og foreslår en V3-klassifiseringsregel (D-pri1/D-aba/L-aba med Kilde=Alarm-krav) som forutsetning for sammenlignbar nasjonal benchmarking.

  **Nøkkelord:** 110-sentral · bemanningsdimensjonering · prosedyrbasert kapasitetsmodell · ankomstkonflikt · op-binder-semantikk · makkerpar · D-pri1 · D-aba · Erlang-C · køteori · LEO/BRIS · beredskap.
---

\newpage

## 1. Innledning

### 1.1 Bakgrunn og tema

Norske 110-sentraler er det primære kontaktpunktet for brann- og redningsnødmeldinger i Norge. De tolv sentralene — Finnmark, Troms, Nordland, Midt-Norge, Møre og Romsdal, Vest, Sør-Vest, Agder, Sør-Øst, Oslo, Øst og Innlandet — opererer døgnet rundt og koordinerer utrykningsressurser over store geografiske områder. I 2025 håndterte de samlet 508 228 registrerte oppdrag, med betydelig variasjon i volum og kategorifordeling mellom sentralene.

Bemanningsdimensjoneringen av 110-operatører reguleres av brann- og redningsvesenforskriften, som pålegger minimum to operatører i vaktrommet, men overlater fastsettelsen av bemanning utover dette til lokale risiko- og beredskapsanalyser. I kontrast gir dimensjoneringsforskriften for brannvesen (FOR-2023-01-06-23) ferdige, etterprøvbare bemanningskrav for kasernert og deltidsbrannvesen basert på innbyggertall og responstid. En tilsvarende kvantitativ, nasjonal standard mangler for 110-operatører.

Konsekvensene av utilstrekkelig kapasitet er todelt. Direkte: anrop kan overføres til nabosentral (Agder 110 i Sør-Vest-regionen) med tap av regionalkunnskap og forlenget responstid. Indirekte: operatørene kompenserer under press gjennom kvalitetsreduksjon — de fortsetter å svare, men uten makkerpar, uten full prosedyre-etterlevelse, med økt kognitiv belastning. Denne tilpasningen holder tjenesten i gang, men flytter kostnaden over på operatørens arbeidsforhold og over tid på beslutningskvaliteten i enkeltsituasjoner.

Problemstillingen er ikke at 110-sentraler generelt er overbemannet eller underbemannet. Den er at det ikke finnes et kvantitativt, etterprøvbart grunnlag for å avgjøre hva som er tilstrekkelig bemanning — og at eksisterende kvalitative vurderinger ikke fanger kapasitetsdynamikken som oppstår ved samtidige hendelser og makkerpar-krav ved pri-1-utrykninger.

### 1.2 Tidligere forskning og kunnskapsgap

Erlang-C-modellen (M/M/c) er veletablert innen kapasitetsplanlegging for flerserver-telefonisystemer og call-center-miljøer (Erlang, 1917; Gans, Koole & Mandelbaum, 2003). Halfin og Whitt (1981) etablerte kvalitetsdrevet bemanning (QED-regimet) gjennom square-root staffing-formelen, og Garnett, Mandelbaum og Reiman (2002) utvidet rammeverket til Erlang-A der kunder med tålmodighetsterskel forlater systemet. Disse modellene er metodisk velprøvde for kommersielle call-sentre, men anvendt sjelden på nødmeldesentraler med de særtrekkene som kjennetegner 110-operasjoner: makkerpar-prosedyre, aktivt hendelsebilde utover samtaletid, ring-flom ved enkelthendelser, og overløpsmekanismer.

Internasjonalt har Gustavsson (2018), L'Ecuyer og Gustavsson (2018) og Dwars (2013) anvendt stokastiske modeller direkte på nordiske og europeiske nødmeldesentraler. Chelst og Barlach (1981) og Larson (1974) utviklet flerserver-dispatch-modeller som fanger at én hendelse kan binde flere servere parallelt. Harchol-Balter (2022) formaliserer multiserver-jobs (MSJ) som rammeverk der jobber krever flere servere samtidig — direkte relevant for makkerpar-logikk. Van Buuren et al. (2017) viser gjennom diskret hendelsessimulering at funksjonsdifferensiering kan forbedre kapasitet uten bemanningsøkning. Forskningen på prosedyrkonformitet og kognitiv belastning (Normark, 2002; Al-Sarhani et al., 2025) dokumenterer at operatørenes faktiske arbeidsmønster avviker vesentlig fra det klassiske kømodeller forutsetter.

Norsk og nordisk forskning på 110-sentralenes kapasitet er derimot svært begrenset. Leonardsen et al. (2021) gir kvalitative funn fra AMK-sentraler. Rehn et al. (2021) analyserer dispatch-nøyaktighet for ambulanser. Men etter litteratursøket i denne studien har vi ikke funnet publiserte studier med kvantitative kapasitetsanalyser av norske 110-sentraler basert på historiske hendelsesdata.

Kunnskapsgapet er dermed konkret: **det finnes ingen kjent kvantitativ, etterprøvbar analyse av 110-kapasitet som fanger makkerpar-bindingen, skiller ulike hendelsesdynamikker, og kan anvendes systematisk på tvers av sentralene i Norge.** Eksisterende ROS- og beredskapsanalyser er kvalitative og ikke sammenlignbare på tvers. Denne studien søker å fylle dette gapet ved å utvikle og anvende en prosedyrbasert ankomstkonfliktmodell med 110 Sør-Vest som primærcase og nasjonal benchmarking som kontekst.

### 1.3 Problemstilling

**I hvilken grad samsvarer faktisk bemanning ved norske 110-sentraler med kapasitetsbehovet beregnet fra historiske hendelsesdata og køteoretiske modeller?**

Problemstillingen er todelt: den krever (i) en operasjonalisering av begrepet *kapasitetsbehov* som er relevant for 110-driftens prosedyrekrav, og (ii) en empirisk vurdering av hvor godt faktisk bemanning matcher dette behovet. Erlang-C danner grunnlinjen, men viser seg utilstrekkelig i denne konteksten (jf. kap 6); studien utvikler derfor en prosedyrbasert variant — den prosedyrbaserte ankomstkonfliktmodellen — som måler operativ kapasitet ved hvert beredskapsanrops ankomsttidspunkt. Forskningsspørsmålene under operasjonaliserer problemstillingen: RQ1–RQ2 etablerer det empiriske grunnlaget (ankomstrate og kapasitetsbinding), RQ3 måler kapasitetsgapet mot prosedyrstandarden, RQ4 sammenligner mot dagens kvalitative dimensjoneringsgrunnlag, og RQ5 prøver overførbarheten til en nasjonal dimensjoneringslogikk.

- **RQ1:** Hva er ankomstraten (λ) til 110 Sør-Vest per skiftperiode, og hvilke belastningsmønstre fremgår av historiske LEO/BRIS-data?
- **RQ2:** Hva er gjennomsnittlig håndteringstid (μ⁻¹) per hendelseskategori, og i hvilken grad binder aktivt hendelsebilde operatørkapasitet utover samtaletid?
- **RQ3:** I hvilken andel av beredskapsanropene ankommer anropet i en tilstand der sentralens operative driftsstandard (makkerpar) ikke kan opprettholdes — og hva er det strukturelle kapasitetsgapet mellom hverdag og helg?
- **RQ4:** I hvilken grad gir eksisterende ROS- og beredskapsanalyse for 110 Sør-Vest et tilstrekkelig metodisk grunnlag for å begrunne faktisk bemanning?
- **RQ5:** Kan strukturelle prediktorer (hendelsesvolum, innbyggertall, areal) danne grunnlag for en generaliserbar dimensjoneringsmodell på tvers av norske 110-sentraler?

### 1.4 Sentrale begreper og notasjon

Modellen og rapporten bygger på en spesifikk nomenklatur som introduseres formelt i kap 3 og 6, men brukes gjennomgående fra kap 4. Tabellen under gir minimumsdefinisjoner for leseren:

| Begrep | Kort definisjon |
|---|---|
| **D-pri1** | Pri-1-utrykning (bygningsbrann, trafikkulykke, farlig gods). Krever makkerpar — to operatører bundet parallelt under akuttfasen. |
| **D-aba** | ABA-utrykning (automatisk brannalarm). Håndteres serielt av én operatør; valgfri Fase 2 (nødtelefon/panel-veiledning) med sannsynlighet $p$. |
| **L-aba** | ABA-hendelse uten utrykning, men med Kilde=Alarm. Egen kategori for å skille reelle alarmhendelser fra øvrige korte oppdrag. |
| **L-hendelse / L-ukjent** | Korte oppdrag uten initiell hendelsestype eller uten registrert klassifisering. |
| **Op-binder** | Tidsavgrenset binding av $q \in \{1, 2\}$ operatører fra et tidspunkt $t$ i $d$ minutter. Hver hendelse ekspanderes til ett eller flere op-binder-events. |
| **Kilde=Alarm-krav** | V3-regel: L-aba og D-aba krever at oppdragets Kilde-felt er «Alarm» — sikrer at ABA-kategoriene ikke forurenses av telefonhenvendelser feilklassifisert som ABA. |
| **c_eff** | Effektiv operatørkapasitet $= c_{\text{total}} - 1$ (vaktleder besvarer normalt ikke nødanrop). |

### 1.5 Avgrensninger

Prosjektet avgrenses til følgende:

- **Vaktromsbemanning** — ikke ressursdisponering i brannvesenet, taktisk hendelseshåndtering eller organisatoriske beslutninger.
- **Retrospektivt og planleggingsrettet** — ikke et sanntidssystem for kapasitetsstyring.
- **Primærcase 110 Sør-Vest (2025)** — hovedmodellen er kjørt på denne sentralen. Nasjonal del (kap 7.8, kap 8.4.1) er benchmarking og kontekst, ikke full prosedyrbasert kapasitetsmodellering for de øvrige 11 sentralene.
- **Ekstraordinære hendelser** (langvarige storbranner, katastrofescenarier) holdes utenfor modellens primære gyldighetsområde og behandles i diskusjonskapittelet.
- **Ring-flom (call surge)** belyses som operativ ekstrembelastning, men modelleres ikke som primærscenario.

### 1.6 Rapportens struktur

Rapporten består av ni kapitler. **Kapittel 2** gjennomgår relevant litteratur strukturert etter fem tematiske områder: klassisk køteori, nødmeldesentraler, team-basert kapasitet og prosedyrkonformitet, nordisk nødmeldeforskning, og dimensjoneringsregulering. **Kapittel 3** etablerer det teoretiske rammeverket — Erlang-C som grunnlinje, QED-regimet, multiserver-jobs og op-binder-semantikk. **Kapittel 4** beskriver 110 Sør-Vest som case med bemanning, arbeidsmetodikk og operative særtrekk. **Kapittel 5** presenterer metode og data, inkludert V3-klassifiseringsregelen og LABA-dybdeanalysen. **Kapittel 6** utvikler kapasitetsmodellen gjennom tre faser: Erlang-C, simultanitetsanalyse og prosedyrbasert ankomstkonfliktmodell. **Kapittel 7** presenterer analyseresultater for 110 Sør-Vest 2025 inkludert scenario +1 operatør og variant A/B. **Kapittel 8** diskuterer funnene mot problemstilling, teori og begrensninger. **Kapittel 9** besvarer problemstillingen og gir anbefalinger for dimensjonering og videre forskning.
