# 9. Konklusjon

## 9.1 Svar på problemstillingen

Problemstillingen er: *I hvilken grad samsvarer faktisk bemanning ved norske 110-sentraler med kapasitetsbehovet beregnet fra historiske hendelsesdata og køteoretiske modeller?*

Svaret avhenger kritisk av hvilken kapasitetsstandard som anvendes.

Mot en ren køteoretisk standard (ventetid < 30 sekunder i M/M/c) fremstår bemanningen som komfortabel: Erlang-C-analysen gir systemutnyttelse ρ < 6 % for alle skifttyper, og sannsynligheten for ventetid over 30 sekunder er mindre enn 1 % (funn 1). Dette resultatet er formelt korrekt, men operativt misvisende.

Mot en prosedyrebasert standard der driftsstandarden er at to operatører (makkerpar) kan håndtere pri-1-hendelser, er det et strukturelt kapasitetsgap. Primærmodellen (variant A) viser at 40,4 % av beredskapsanropene i 110 Sør-Vest 2025 ankommer i brudd eller svikt-tilstand (variant A), stigende til 46,0 % når total operativ belastning inkluderes (variant B hoved). På natt/helg (c_eff = 2) er over halvparten av beredskapsanropene i brudd eller svikt. Hvert tredje beredskapsanrop på natt/helg ankommer i ren svikt-tilstand der ingen operatør er ledig.

Samsvaret mellom bemanning og kapasitetsbehov er dermed **ikke tilstrekkelig** når målestokken er operativ prosedyrkonformitet. Erlang-C-baserte vurderinger skjuler denne diskrepansen fordi de ikke fanger makkerpar-bindingen eller differensieringen mellom pri-1-hendelser (D-pri1, makkerpar) og ABA-utrykning (D-aba, serial solo-håndtering).

## 9.2 Svar på forskningsspørsmålene

**RQ1: Hva er ankomstraten (λ) til 110 Sør-Vest per skiftperiode, og hvilke belastningsmønstre fremgår av historiske LEO/BRIS-data?**

Ankomstraten er estimert per skifttype: 2,57 anrop/t (dag/hverdag), 2,06 (dag/helg), 1,18 (natt/hverdag) og 1,30 (natt/helg). Volumet er topptung på dagtid (kl. 09–10) og viser en sårbar overgangssone ved skiftveksling kl. 19:00. Sammenstilte tilleggsanrop (18 901 per år) er identifisert via sekvensgap-metoden og utgjør 23 % av totalvolumet (korreksjonsfaktor 1,305×). Synlige oppdrag i BRIS undervurderer dermed faktisk operatørbelastning.

**RQ2: Hva er gjennomsnittlig håndteringstid (μ⁻¹) per hendelseskategori, og i hvilken grad binder aktivt hendelsebilde operatørkapasitet utover samtaletid?**

Modellen skiller mellom D-pri1 (pri-1-utrykning, makkerpar, median 14,1 min × 2 ops) og D-aba (ABA-utrykning, serial 3 min + valgfri Fase 2 på 6 min). L-aba er empirisk kalibrert til 6 min via LABA-dybdeanalysen (mean fra 50-hendelsers utvalg). Aktivt hendelsebilde binder operatørkapasitet vesentlig utover samtaletid — samtalen utgjør kun første del av akuttfasen, og operatørene er bundet frem til ressursene er fremme og loggføring er kvittert.

**RQ3: I hvilken andel av beredskapsanropene ankommer anropet i en tilstand der sentralens operative driftsstandard (makkerpar) ikke kan opprettholdes — og hva er det strukturelle kapasitetsgapet mellom hverdag og helg?**

For variant A (beredskapsbelastning) er svikt 14,9 % på dag hverdag og 32,6 % på natt/helg. Det strukturelle gapet mellom dag og natt er dermed betydelig: sviktraten dobles, og Normal-andelen faller fra 69 % til 47 %. Asymmetrien skyldes hovedsakelig at c=2 gir null buffer når en D-pri1 er aktiv — hele makkerparet er bundet, og neste beredskapsanrop ankommer automatisk i svikt. For variant B (total belastning, hoved-scenario) er natt/helg-Svikt 33,4 %.

**RQ4: I hvilken grad gir eksisterende ROS- og beredskapsanalyse for 110 Sør-Vest et tilstrekkelig metodisk grunnlag for å begrunne faktisk bemanning?**

ROS-analysen og beredskapsanalysen er kvalitative og gir ikke et etterprøvbart, tallbasert grunnlag for dimensjonering på tvers av sentraler. Analysene dokumenterer overløpsmekanismer og operative særtrekk, men fastsetter ikke eksplisitte, kvantitative servicenivåmål som kan måles mot observerte hendelsesdata. Meld. St. 16 (2023–2024) bekrefter at denne kvalitative tilnærmingen er gjeldende norsk praksis, og at en kvantitativ nasjonal standard ikke foreligger. Den interdepartementale arbeidsgruppen (2009) bemerket selv at det «ikke finnes vitenskapelig grunnlag for de valgte terskelverdiene» for svartid.

**RQ5: Kan strukturelle prediktorer (hendelsesvolum, innbyggertall, areal) danne grunnlag for en generaliserbar dimensjoneringsmodell på tvers av norske 110-sentraler?**

Ja — men med forbehold om felles klassifisering. Nasjonal DSB-oversikt for 2025 (508 228 oppdrag, alle 12 sentraler) viser at volum varierer 10× mellom Finnmark (7 402) og Oslo (71 421), mens kategorifordeling (særlig L-aba) varierer ulikt ved eksisterende registreringspraksis. Sentraler som Sør-Øst og Oslo har ≈0 % L-aba mens Nordland har 7,5 % — variasjoner som trolig skyldes ulik registreringspraksis mer enn reell ABA-belastning. Strukturell prediksjon på tvers av sentraler krever derfor først harmonisering av klassifiseringsregler. Den V3-klassifiseringen som er utviklet i denne studien (D-pri1/D-aba/L-aba/L-hendelse/L-ukjent/S/F/V med Kilde=Alarm-krav for ABA-kategoriene) kan danne grunnlag for slik harmonisering.

## 9.3 Bidrag og praktiske implikasjoner

Rapporten bidrar på tre nivåer:

**Metodisk bidrag.** Den prosedyrbaserte ankomstkonfliktmodellen introduserer *op-binder-semantikk* som teoretisk rammeverk: hver hendelse ekspanderes til én eller flere op-binder-events som reflekterer operativ binding snarere enn statiske serverslots. Dette er en konkretisering av multiserver-job-litteraturen (Chelst & Barlach, 1981; Harchol-Balter, 2022) tilpasset nødmeldesentralkontekst. Modellen reduserer til klassisk M/M/c som spesialtilfelle, men fanger dynamikk Erlang-C ikke kan uttrykke: differensiering mellom tunge og lette utrykninger, makkerpar-krav for pri-1, og ankomstkonflikt som kapasitetsmetrikk.

**Empirisk bidrag.** Studien er den første kvantitative kapasitetsanalysen av en norsk 110-sentral basert på historiske hendelsesdata. Den dokumenterer strukturelt kapasitetsgap særlig på natt/helg, og kvantifiserer effekten av +1 operatør (svikt halveres fra 33 % til 17 % på natt/helg). LABA-dybdeanalysen etablerer empirisk grunnlag for L-aba-parameter og avdekker ~25 % feilklassifisering i eksisterende BRIS-kategorier.

**Praktiske implikasjoner.** For 110 Sør-Vest spesifikt peker analysen på to dimensjoneringsalternativer:

1. **Bemanningsøkning:** +1 operatør på natt/helg gir den klart største kapasitetsgevinsten (Svikt halveres). Den første ekstra operatøren på natt/helg har større marginalverdi enn én ekstra på dag hverdag — analog til square-root staffing-logikk i QED-regimet (kap 3.2).

2. **Funksjonsdifferensiering:** Skille servicelast fra beredskapslast. Servicevolumet (22 542 overføringstester per år, konsentrert på dagtid) kan håndteres av dedikert personell utenfor beredskapsoperatørgruppen, som allerede praktisert ved Midt-Norge 110. Van Buuren et al. (2017) og Jouini et al. (2008) gir teoretisk belegg for at dette kan forbedre kapasitetsbildet uten å øke total bemanning.

For den nasjonale dimensjoneringsdebatten er det viktigste bidraget å vise at **en kvantitativ standard er mulig**. Dimensjoneringsforskriften for brannvesen (FOR-2023-01-06-23) viser at kvantitative bemanningskrav basert på innbyggertall og responstid er praktisk gjennomførbare. En tilsvarende standard for 110-operatører bør ta utgangspunkt i prosedyrkonform håndtering av beredskapsanrop som målemetrikk, ikke bare svartidsstatistikk.

## 9.4 Anbefalinger

Basert på analysen foreslås følgende:

1. **Dimensjonering av 110 Sør-Vest:** Vurder +1 operatør på natt/helg som primær tiltak. Alternativt (eller i tillegg): skille servicelast ut av beredskapsoperatørgruppen.

2. **Nasjonalt:** Utvikling av en kvantitativ dimensjoneringsstandard for 110-operatører analogt med brannvesenforskriften. Målemetrikken bør inkludere prosedyrkonformitet (makkerpar opprettholdt ved ankomst), ikke bare svartid.

3. **DSB/datainfrastruktur:** En utvidelse av BRIS-datauttrekket med 22 prioriterte felt (operatør-ID, samtalevarighet, ventetid m.m.) vil muliggjøre mer presis nasjonal benchmarking. Se `analyse/DSB_onskeliste_BRIS_datauttrekk.md`.

4. **Klassifiseringsharmonisering:** Nasjonal benchmarking av L-aba og D-aba forutsetter at alle sentraler bruker felles klassifiseringsregler med Kilde=Alarm-krav. Den V3-regelen som er utviklet i denne studien kan danne grunnlag.

5. **Videre forskning:** Validering på tvers av sentraler, tidsvariabel DES-modellering, og dypere analyse av nødtelefonfase etter D-aba er prioriterte retninger (se avsnitt 8.5).

## 9.5 Avsluttende refleksjon

Erlang-C-paradokset er den sentrale metodiske lærdommen: ρ < 6 % betyr ikke at systemet er overbemannet. For små nødmeldesentraler opererer kapasitetsteorien i et regime der klassiske mål for servere og ventetid er utilstrekkelige. Det operative kapasitetsproblemet er ikke at anrop ikke blir besvart — operatørene svarer i nesten alle tilfeller — men at de besvares under forhold der den prosedyrestandarden for korrekt og trygg hendelseshåndtering ikke er oppfylt.

Denne operative kostnaden bæres i dag av den enkelte operatøren gjennom kvalitetsreduksjon som skjult buffer. Den forblir usynlig i tradisjonell statistikk: svartiden er akseptabel, oppdragene lukkes, årsrapporten viser ingen avvik. Modellens bidrag er å gjøre denne skjulte belastningen målbar, slik at dimensjoneringsbeslutninger kan tas med grunnlag i operativ realitet — ikke bare i statistikk som skjuler kostnaden.

---

*Kap 9 — Versjon 1.0 | Skrevet: 2026-04-19*
