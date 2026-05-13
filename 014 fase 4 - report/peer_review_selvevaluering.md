# Peer review — selvevaluering ved bruk av peer-review-rammeverket

| Felt | Innhold |
|---|---|
| **Vurderende gruppe** | Selvevaluering ved bruk av peer-review-rammeverket |
| **Gruppe som blir vurdert** | G20 Individuell (Rune Grødem) |
| **Tittel på rapport** | *Kapasitetsstyring og bemanningsdimensjonering ved norske 110-sentraler — En analyse av operatørkapasitet med prosedyrbasert ankomstkonfliktmodell* |
| **Dato** | 2026-05-01 |

---

## 1. Helhetsinntrykk

Rapporten har en klar og original analytisk linje: den bruker Erlang-C som negativt referansepunkt for å motivere en prosedyrbasert ankomstkonfliktmodell med op-binder-semantikk, og anvender denne på et reelt LEO/BRIS-uttrekk fra 110 Sør-Vest 2025. Hovedfunnet — at hvert tredje beredskapsanrop på natt/helg ankommer i Svikt-tilstand, og at +1 operatør halverer dette — er empirisk konkret, robust over en bred sensitivitetsanalyse, og reelt beslutningsstøttende. Modellrammeverket framstår faglig solid: koblingen mellom Chelst & Barlach (1981), Harchol-Balter (2022) og makkerpar-binding er tett og godt argumentert, og LABA-dybdeanalysen i to runder hever de empiriske parameterne fra «orienteringsanslag» til kalibrerte estimater med rapporterte konfidensintervall.

Hovedutfordringene er av tre slag. (i) Det er en del overlapp mellom kap 5 og kap 6 (klassifisering, op-binder-definisjoner, antagelsestabeller dukker opp i begge), som kunne strammes opp. (ii) Variant B og særlig Tabell 7.10 mangler full transparens om at flere parametre varieres samtidig — det er strengt tatt en samlet scenariosensitivitet, ikke en individuell parametersensitivitet. (iii) Rapporten er ambisiøs i nasjonal benchmarking (kap 7.9) men begrenset i hva den faktisk leverer for de øvrige 11 sentralene; konklusjonen håndterer dette ryddig, men kap 1 og abstract kunne vært enda tydeligere på at primærmodellen kun er kjørt på Sør-Vest. Disse punktene er presiseringer, ikke strukturelle problemer — rapporten er klart innenfor B-nivå-ambisjonen sett under ett.

---

## 2. Områdevis vurdering

### 2.1 Innledning (kap 1)

**Styrker.** Bakgrunnsskissen er presis og knytter raskt sammen forskriftskrav, mangelen på kvantitativ standard og det operative dilemmaet (overløp vs. kvalitetsreduksjon). Problemstillingen i 1.3 er konkret og todelt formulert, og operasjonaliseringen i fem RQ-er er logisk: RQ1–RQ2 (empirisk grunnlag), RQ3 (kapasitetsgap), RQ4 (ROS-vurdering), RQ5 (generaliserbarhet). Begrepstabellen 1.4 er svært nyttig — leseren har D-pri1, D-aba, L-aba, op-binder og c_eff klart fra start.

**Forbedringspunkter.**
- *Avgrensningen i 1.5 er upresis om den nasjonale ambisjonen.* Punktet "Primærcase 110 Sør-Vest (2025) — hovedmodellen er kjørt på denne sentralen. Nasjonal del (kap 7.9, kap 8.4.1) er benchmarking og kontekst" er korrekt formulert, men problemstillingen i 1.3 er fortsatt formulert som "norske 110-sentraler" (flertall). Vurder å skrive RQ3 og RQ5 mer eksplisitt sentralspesifikt for RQ3 og hypotetisk for RQ5, eller å reformulere problemstillingen som "ved 110 Sør-Vest, og i hvilken grad kan rammeverket overføres nasjonalt".
- *Studiens betydning er bredt skissert, men kunne kobles enda tettere til hvem som skal bruke resultatet.* I 1.1 kunne det stå én setning til om hvilken beslutningstaker (DSB, lokalt vaktansvarlig, departementet) modellen skal støtte, gjerne med et konkret eksempel.
- *Abstract* (s. 1) er innholdsrikt og presist, men gjentar for mange tall (32,6 %, 33,2 %, 16,7 %, n=100, 4,53 min). Behold de viktigste én gang og la øvrige stå i sammendraget av funn.

### 2.2 Litteraturgjennomgang (kap 2)

**Styrker.** Søkestrategien (2.1) er forbilledlig dokumentert med databaser, søkeord, tellinger og inklusjons-/eksklusjonskriterier — noe som er sjeldent i masterprosjekter på dette nivået. Kap 2.6 oppsummerer fem kunnskapsgap som er konkrete og direkte koblet til studien (Gap 1: prosedyrkonformitet som metrikk; Gap 2: D-pri1 som MSJ; Gap 5: norsk 110-empiri). Bredden av relevant litteratur er solid: Erlang-C/A/QED, MSJ (Chelst, Brill & Green, Harchol-Balter), team-basert kapasitet (Kim, Jouini), nordisk empiri (Gustavsson, Leonardsen, Samdal, Byrsell).

**Forbedringspunkter.**
- *Tabellen i 2.1 oppgir "Inkludert: 12 + 8 + 9 + 4 + 7 + 3 + 2 = 45", men teksten under sier "av samlet ~670 målrettede treff er 45 inkludert".* Tallene stemmer, men summen og ~670 framstilles bare som anslag — vurder å opplyse hvor mange duplikater og hvor mange faktiske screenede sammendrag som ligger bak utvalget på 45.
- *Internasjonal litteratur dominerer 2.2–2.4; den nordiske (2.5) er kortere.* Det er greit gitt empirisk situasjon (få studier finnes), men én eller to setninger om hvilke spesifikke metoder fra Storesund et al. (2017) som kunne overføres direkte til 110-dimensjonering ville styrke koblingen mellom 2.5 og resten.
- *Penverne et al. (2024) introduseres først i kap 8.3.5 som en nøkkelreferanse for overløpsdiskusjonen,* men er ikke nevnt i kap 2. Flytt en kort omtale av digital tvilling-tilnærmingen til kap 2.3 (Nødmeldesentraler — kapasitet og dimensjonering) slik at den er etablert før diskusjonen.

### 2.3 Metode (kap 5)

**Styrker.** Refleksivitetsavsnittet i 5.1 er en av rapportens sterkeste passasjer: insider-posisjonen erkjennes eksplisitt, og fire konkrete avbøtende tiltak listes (registerdata som primærgrunnlag, deterministisk skript-flyt med fast seed, antagelsesdokumentasjon, triangulering). Tabell 5.5 (observasjonsstatus) og 5.6 (analysesteg) er forbilledlige — leseren ser umiddelbart hva som er observert, beregnet, estimert eller antatt. LABA-dybdeanalysen i 5.4 er beskrevet i en grad av detalj (utvalgsdesign, utfyllingsprosedyre, n=100, 95 % CI via bootstrap) som er på nivå med metodebeskrivelser i fagfellevurderte tidsskrift.

**Forbedringspunkter.**
- *Sekvensgapmetoden (5.3.4) er originell og lenger forklart i kap 7.2, men forutsetningen "LEO tildeler sekvensnumre kronologisk og uten andre årsaker til gap" får et nytt forbehold i kap 7.9.3 (Tabell 7.14) der det erkjennes at gap også kan stamme fra (i) overføringer til nabosentral og (ii) avbrutte anrop.* Dette forbeholdet bør innføres allerede i 5.3.4, ikke først ved den nasjonale benchmarken — det påvirker også Sør-Vest-tallet på 18 901 (selv om det er validert lokalt). Forslag: legg til én setning som sier "gapene kan i prinsippet også reflektere overflyt og avbrutte anrop; for Sør-Vest er sekvensgap-prosenten validert som overveiende sammenstillinger gjennom operativ dialog (jf. avsnitt 7.2)".
- *Antagelse 5.1 (innsatsvarighet ikke brukt som operatørbindingsmål) er solid begrunnet, men gjøres til et premiss for hele D-pri1-bindingstidsdefinisjonen.* Vurder å gjøre forutsetningen mer eksplisitt — f.eks. ved å vise hva sviktraten ville blitt dersom innsatsvarighet i stedet for "første ressurs fremme + 3 min" ble brukt som øvre grense. Dette ville være en nyttig sensitivitetstest av selve binding-definisjonen, ikke bare av binding-verdien.
- *Avsnitt 5.2.4 fletter sammen valideringssamtaler og LABA-dybdeanalyse i samme tabell.* Disse er metodisk ulike (samtaler vs. strukturert utfylling) og fortjener kanskje to tabeller eller en tydeligere markering. I tillegg står det "én operatør" om LABA-utfyllingen i 5.4.6 — vurder å diskutere hvordan inter-rater-reliabilitet kunne ha styrket analysen, selv om det ikke ble gjort.
- *Reliabilitet i 5.6.2:* skriptbasert, deterministisk flyt er en sterk reproduserbarhetsfordel, men "fast random seed" er kun relevant for D-aba Fase 2-stokastikken. Presiser at modellresultatene under variant A i hovedsak er deterministiske — usikkerheten ligger i parameterantagelser, ikke i stokastisk simulering.

### 2.4 Analyse og resultater (kap 7)

**Styrker.** Strukturen følger RQ-ene ryddig (7.1–7.2 → RQ1, 7.4 → RQ2, 7.5–7.7 → RQ3, 7.8 → RQ4, 7.9–7.10 → RQ5). Tabell 7.6 og 7.7 er kjernefunnene og presenteres nøkternt uten å gli inn i tolkning, slik krav til kapittelskille tilsier. Asymmetri-argumentet for c=2 vs c=3 (avsnitt 7.3 og 7.5) er logisk klart og illustrert med konkret eksempel-tabell. Sensitivitetsanalysen (Tabell 7.10) er bred nok til å gi tillit: selv med "lavt" scenario er Svikt natt/helg over 30 %.

**Forbedringspunkter.**
- *Tabell 7.10 (sensitivitetsanalyse variant B) varierer flere parametre samtidig (D-aba Fase 2 p og Y, samt L-aba/L-hendelse/L-ukjent/S/F/V).* Dette er en samlet "lav/hoved/høy"-scenariosensitivitet — ikke en parametervis ceteris paribus-test. Det er metodisk forsvarlig, men leseren bør ikke kunne misforstå dette som om man har isolert effekten av f.eks. p alene. Forslag: Legg til én setning før tabellen som eksplisitt sier "alle ikke-databaserte parametre varieres samtidig fra lav til høy; en parametervis dekomponering er ikke gjennomført", og vurder å inkludere én ekstra rad "p = 0,30, øvrige hovedscenario" og "L-aba = 7 min, øvrige hovedscenario" for å vise hvilken parameter som driver mest.
- *Kap 7.6, fotnote i Funn 4 (kap 7.11): "scenarioets baseline 32,8 % skyldes annen tilfeldig D-aba Fase 2-realisasjon enn primærmodellens 32,6 %; differansen er innenfor stokastisk støy".* Dette er en god ærlig kommentar, men antyder at scenarioet og primærmodellen ikke deler samme seed/realisasjon. Vurder å enten kjøre scenario med samme seed (deterministisk reproduksjon) eller å bruke gjennomsnittet over flere seeds (Monte Carlo). Slik det står nå må leseren ta forfatterens ord for at differansen er tilfeldig — en kjøring med n=10 seeds ville gitt en konfidensbredde i scenarioet.
- *Tabell 7.12 (volum og arbmengde nasjonalt) inneholder "Sør-Vest 61 934"* — i resten av rapporten brukes 61 964. Forskjellen er liten, men sjekk hvilket tall som er riktig (DSB nasjonal vs. lokal 110 Sør-Vest-eksport kan ha små avvik) og forklar avviket eller harmoniser. Tilsvarende: i Tabell 7.14 står Sør-Vest "61 934" og "18 930"; i kap 7.2 står "61 964" og "18 901". Forklar.
- *Variant A-resultatene rapporteres samlet (alle skifttyper). Det kunne vært nyttig med en kort oppsplittet tabell eller figur* der dag/hverdag, dag/helg, natt/hverdag, natt/helg vises hver for seg — ikke bare den aggregerte "natt/helg"-kolonnen. Dette er særlig relevant fordi dag/helg har c_eff=2 men dagens ankomstrate, og det er en interessant case-kombinasjon.
- *Avsnitt 7.9.2 viser at Oslo og Sør-Øst har 0,0 % L-aba og 0,0 % D-aba.* Dette er en bemerkelsesverdig observasjon som kanskje ikke utelukkende er registreringspraksis — noen sentraler kan ha andre alarm-mottakssystemer (Alarmmottak vs. ISM). Avsnittet behandler dette som "ulik registreringspraksis", men en kort kommentar om alternative tekniske/organisatoriske forklaringer ville styrke tolkningen.

### 2.5 Diskusjon (kap 8)

**Styrker.** Diskusjonen åpner med en tydelig RQ-oversikt og strukturerer seg rundt fire substantive tema. Avsnitt 8.2 (modellprediksjoner vs. opplevd virkelighet) er den faglig mest interessante delen: den setter ord på et reelt paradoks — at sentralen "fungerer" til tross for 33 % Svikt — og forklarer det gjennom kvalitetsreduksjon som skjult buffer (Gustavsson 2018, Leonardsen 2021). Den nye underseksjonen 8.2.2 om "driftsstandard versus regulatorisk minimumskrav" er en presis og nødvendig nyansering: makkerpar er en *prosedyrestandard*, ikke et lovkrav, og modellen kvantifiserer en *systematisk planlagt avvikelse*.

**Forbedringspunkter.**
- *Avsnitt 8.3.2 sammenligner +1 operatørs effekt med square-root staffing-logikken.* Sammenligningen er konseptuelt riktig (avtagende marginalverdi), men matematisk presisjon kunne styrkes: $\sqrt{c}$ er ikke direkte den parameteren som driver staffing-buffer i Halfin-Whitt-formelen — det er $\beta\sqrt{R}$ der R = λ/μ er tilbudt trafikk i Erlang. Vurder å reformulere som "marginalverdien av en ekstra server er empirisk størst når antall servere er lavt (jf. Halfin-Whitt-regimets konsentrasjon mot lav-A-buffer)" snarere enn å sammenligne $\sqrt{2}$ og $\sqrt{4}$ direkte.
- *Avsnitt 8.3.5 (overløp som systemarkitektur) kommer noe brått inn,* uten klar kobling tilbake til funnene. Penverne et al. (2024) har vært underkommunisert i tidligere kapitler. Enten utvid avsnittet med en konkret implikasjon for 110 Sør-Vest sin egen overløpsavtale med Agder, eller fjern det som eget avsnitt og flytt poenget inn i 8.3.4.
- *Det "uventede funnet" i innledningen til kap 8 — at total belastning forverrer dagkapasiteten mens natt/helg er sårbar selv ved beredskapsbelastning — kunne vært mer eksplisitt diskutert.* Det er nevnt, men ikke virkelig løftet som en hovedinnsikt. Vurder å gi denne én underseksjon i 8.3 (f.eks. 8.3.6 "To ulike kapasitetsproblem på dag og natt") der praktisk implikasjon er at dimensjoneringssvar (+1 operatør natt vs. funksjonsdifferensiering dag) er ulike.
- *Begrensningskapittelet 8.4 er solid, men kunne vært strengere:* selve modellrammen — at Brudd og Svikt er binære og ikke har relativ alvorlighetsgrad — er en betydelig forenkling som er nevnt, men ikke tatt på alvor som tolkningsgrense. En "Svikt" der ingen ledig op finnes på et tidspunkt der VL faktisk kan tre inn er kvalitativt ulik en "Svikt" der VL også er bundet i annen aktivitet. Dette kunne vært gjort tydeligere som en begrensning og pekt fram mot en alvorlighetsgradert versjon i videre forskning.

### 2.6 Konklusjon (kap 9)

**Styrker.** Konklusjonen svarer direkte på problemstillingen og hver enkelt RQ. Avsnitt 9.1 håndterer den case-spesifikke karakteren av funnene ryddig: konklusjonen formuleres for 110 Sør-Vest, mens nasjonale implikasjoner formuleres som hypoteser. Bidragene i 9.3 er tre-delt (metodisk, empirisk, praktisk) og knyttes klart til litteraturen (MSJ-rammeverket, square-root staffing, funksjonsdifferensiering). Anbefalingene i 9.4 er ærlig kategorisert som "case-spesifikk beslutningsstøtte" + "forutsetninger for nasjonal modell" + "videre forskning" — dette er metodisk redelig.

**Forbedringspunkter.**
- *Avsluttende refleksjon (9.5) gir det språkbruksmessig sterkeste kontrastparet i rapporten:* "kø-effektivitet vs. prosedyre-sikkerhet". Dette begrepsparet kunne vært introdusert tidligere — i kap 1 eller 3 — og brukt gjennomgående. Det ville bundet rapporten enda tettere sammen.
- *9.4 punkt 4 (Nasjonal dimensjoneringsstandard) framstår noe generelt formulert.* Vurder å konkretisere hva en slik standard kunne bestå av — f.eks. en terskelverdi (P(makkerpar) ≥ X %) eller et bemanningssvar gitt ankomstrate per kategori — slik at anbefalingen er handlingsrettet på et konkret nivå.
- *Begrensningsdrøftingen i konklusjonen er minimal.* Selv om kap 8.4 dekker dette, ville to setninger i 9.5 om at "modellen er gyldig under forutsetningen om at makkerpar er den korrekte driftsstandarden" eller tilsvarende ramme inn helhetsforståelsen.

### 2.7 Skriveflyt, formelle aspekter og helhetsvurdering

**Styrker.** Språk og struktur er gjennomgående klart akademisk, med konsistent terminologi (D-pri1, D-aba, L-aba, op-binder) som leseren raskt blir fortrolig med. Tabeller og figurer er nummerert konsistent og refereres i tekst. Matematiske formler er korrekt formulert i $\LaTeX$-notasjon. APA 7-referanser er gjennomført grundig, med både trykte og online-kilder. Bruk av forkortelser (RØD, GUL, GRØNN, VL, MOB, BRIS, LEO, ABA) er definert ved første forekomst.

**Forbedringspunkter.**
- *Kap 4 (casebeskrivelse) og kap 6.2 (klassifisering) overlapper substansielt med kap 5 (metode).* Klassifiseringstabellen står i både 5.3.2, 6.2 og delvis 7.4.1. Tilsvarende kap 4.2.2 og 6.4.4 om makkerpar-binding gjentar samme tidslinje (0–~1 min, ~1–~2 min, etc.). Vurder å konsolidere: la kap 4 være kort beskrivende, la kap 5 ha den korte operasjonaliseringstabellen, og la kap 6 ha den fulle modelldefinisjonen — uten å gjenta tabellene i alle tre.
- *Tabellen 7.5 (op-binder per kategori) og kap 6.4.7 (events per hendelsestype) inneholder samme informasjon i ulik form.* Konsolider eller kryssreferer eksplisitt.
- *Antagelse-nummerering* er brukt sporadisk: "Antagelse 5.1", "Antagelse 5.2", "Antagelse 6.1", men også "A1–A8" i Tabell 6.3. Velg én konvensjon og bruk den gjennomgående.
- *Figurkvalitet:* Figurene refereres med riktig nummer, men jeg har ikke kunnet vurdere selve den visuelle utformingen i denne reviewen (kun referansene i markdown-filene). Forfatteren bør sjekke at figurer har lesbare aksetekster, at fargene fungerer både i fargetrykk og gråskala, og at figurtekstene er konsekvent korte (ikke fulle forklaringer).
- *PDF-kompilering:* Det er en ressursavhengighet til den kompilerte PDF (referert i `Rapport_LOG650_G20_Rune_110_v0.1.md`). Ved final innlevering må kapittelfilene merges og kjøres gjennom Pandoc/XeLaTeX-pipeline (Vedlegg A). Sjekk at all matematikk og alle tabeller renderer korrekt, og at kryssreferanser (kap-X.Y, Tabell N.M) er løst.
- *Originalitet i bidraget:* Op-binder-semantikken som operasjonalisering av MSJ-rammeverket på en nordisk 110-sentral, kombinert med V3-klassifiseringsregelen og LABA-dybdeanalysen som empirisk kalibrering, framstår genuint originalt. Det er presist forfatterens eget bidrag, og den ydmyke formuleringen i kap 2.6 ("metodisk originalitet ligger i operasjonaliseringen [...] — ikke i utvikling av ny køteori") er passende.

---

## 3. Samlet vurdering

Rapporten er metodisk solid, empirisk grundig forankret, og leverer et originalt og handlingsrettet bidrag til et felt der norsk kvantitativ forskning er svært begrenset. Hovedanbefalingene for sluttarbeidet er: (1) konsolider overlappende beskrivelser mellom kap 4, 5 og 6 for å skjerpe strukturen; (2) gjør sensitivitetsanalysen i Tabell 7.10 mer transparent ved å tydeliggjøre at flere parametre varieres samlet og vurder å legge inn én parametervis variant; (3) reformuler problemstillingen og avgrensningen i kap 1 så det er enda klarere fra start at primærmodellen kun gjelder 110 Sør-Vest; (4) flytt nøkkelreferanser som Penverne et al. (2024) inn i kap 2 så de er etablert før diskusjonen; og (5) sjekk de små tallavvikene mellom Sør-Vest-totaler i kap 7.2 (61 964 / 18 901) versus kap 7.9 (61 934 / 18 930). Disse punktene er polering, ikke omarbeiding — analysen i seg selv står godt på egne ben.
