# 8. Diskusjon

Denne diskusjonen knytter analysens fem hovedfunn (avsnitt 7.9) til problemstillingen, relevant teori og praktiske implikasjoner. Diskusjonen er strukturert rundt fire tema: det metodiske argumentet for en prosedyrbasert modell fremfor klassisk køteori, forholdet mellom modellprediksjoner og opplevd virkelighet, implikasjoner for bemanningsdimensjonering, og begrensninger og videre forskning.

> **Kort oversikt — diskusjonens svar på RQ1–RQ5** (fulltekstsvar i kap 9.2):
>
> - **RQ1 (ankomstrate og belastningsmønster):** Empirisk grunnlag etablert; topptung dagprofil og sårbar overgangssone ved skiftveksling kl. 19:00. Drøftes i 8.1.3 og 8.3.3.
> - **RQ2 (håndteringstid og kapasitetsbinding):** Aktiv bindingstid (median 13,0 min) er vesentlig lenger enn samtaletid (3,4 min). Drøftes i 8.1.3.
> - **RQ3 (ankomstkonflikt og dag/natt-gap):** Strukturelt gap dokumentert; svikt natt/helg 32,6 % (variant A) / 33,4 % (variant B). Drøftes i 8.2.1, 8.3.1 og 8.3.2.
> - **RQ4 (ROS-grunnlaget):** Kvalitativt — uten kvantitativ benchmark. Drøftes i 8.3.4.
> - **RQ5 (generaliserbarhet):** Teknisk overførbar, men forutsetter felles klassifisering. Drøftes i 8.3.4 og 8.4.1.

## 8.1 Hvorfor Erlang-C er utilstrekkelig — og hva som erstatter den

### 8.1.1 Det lav-belastede paradokset

Erlang-C konkluderer med at 110 Sør-Vest har svært lav systemutnyttelse (ρ < 6 %) og nær null sannsynlighet for ventetid over 30 sekunder (funn 1). Isolert sett kunne dette tyde på at sentralen er betydelig overbemannet. Resultatet er formelt korrekt, men operativt meningsløst — og dette er ikke et tilfelle unikt for 110.

Fenomenet er godt dokumentert i køteoretisk litteratur. Garnett, Mandelbaum og Reiman (2002) viser at for systemer med lav tilbudt trafikk (R) dominerer kvadratrotleddet i bemanningsformelen: $N = R + \beta\sqrt{R}$. Når R er lav, som ved 110-sentraler, gir dette uunngåelig lav utnyttelse — ikke fordi systemet er overbemannet, men fordi det opererer i det kvalitetsdrevne regimet (QD) der overskuddskapasitet er en strukturell nødvendighet for å opprettholde servicenivå. Feldman, Mandelbaum, Massey og Whitt (2008, s. 334) formulerer dette direkte: «When the load is small, the addition or removal of a single server will greatly affect the delay probability.» Med c_eff = 2 på natt/helg er 110 Sør-Vest i denne sonen — ett operatørskifte endrer kapasitetsbildet fundamentalt.

Dwars (2013) observerer det samme fenomenet i sin analyse av nederlandske ambulansesentraler: disse er «intrinsically lightly-loaded systems» der lav utnyttelse ikke bør tolkes som overkapasitet, men som en konsekvens av stordriftsulempen ved små enheter. Gans, Koole og Mandelbaum (2003) beskriver den inverse mekanismen som «statistical economies of scale» — og ved 110-sentraler med 2–3 operatører er disse stordriftsfordelene i praksis fraværende.

### 8.1.2 Makkerpar som flereenhets-betjening

Den fundamentale begrensningen ved Erlang-C for 110-konteksten er ikke ankomstprosessen eller fordelingen av betjeningstid, men antagelsen om at én server betjener én kunde. Prosedyren ved 110 Sør-Vest krever at to operatører (RØD og GUL) aktiveres fra første sekund av et beredskapsanrop (avsnitt 4.2.2). Dette er en form for simultan flereenhets-betjening som har vært formelt behandlet i køteorien siden Chelst og Barlach (1981), som utvider Larsons hyperkubemodell med «Type 2-anrop» — hendelser som krever to enheter samtidig. Brill og Green (1984) viser at slike systemer har vesentlig annen kapasitetsdynamikk enn enenhet-systemer, og Harchol-Balter (2022) generaliserer dette til multiserver-job-køer der jobber krever flere servere parallelt.

Primærmodellen i denne rapporten adresserer nettopp dette gjennom op-binder-semantikken (kap 3.7): i stedet for å modellere operatører som uavhengige servere som hver behandler én kunde av gangen, ekspanderes hver hendelse til ett eller flere op-binder-events som hver binder $q \in \{1, 2\}$ operatører i $d$ minutter. Dette løser Erlang-C-mangelen på tre presise måter: (i) D-pri1-events med $q = 2$ representerer makkerpar-bindingen direkte, slik at en aktiv pri-1-hendelse alltid blokkerer to operatører — ikke én; (ii) heterogene job sizes ($q = 2$ for D-pri1, $q = 1$ for D-aba og øvrige) fanger den operative differensieringen mellom hendelseskategorier som Erlang-C behandler likt; og (iii) prosedyrekalibrerte varigheter $d$ erstatter den eksponentielle servicetiden, slik at modellen reflekterer faktiske bindingsmønstre snarere enn matematisk bekvemmelighet. Kapasitetsnivåene (Normal/Brudd/Svikt) er direkte utledet fra prosedyrens rollestruktur, ikke fra køteoretiske antagelser om serverutnyttelse.

### 8.1.3 Bindingstid som kapasitetsbegrep

Funn 2 viser at operatørene er bundet i median 13,0 minutter per beredskapsoppdrag — vesentlig lenger enn den rene samtaletiden (median 3,4 minutter i Erlang-C). Denne diskrepansen er ikke overraskende i lys av litteraturen: van Buuren, Kommer, van der Mei og Bhulai (2017) dokumenterer i sin DES-modell av nederlandske nødmeldesentraler at funksjonsdifferensiering (call taker vs. dispatcher) gir markant ulike servicetider for ulike roller, og at den samlede bindingstiden per hendelse er summen av flere deloperasjoner. Gustavsson (2018) viser tilsvarende at agenter ved SOS Alarm komprimerer servicetiden under press — men at denne kompresjonen har en kvalitetskostnad.

For 110-dimensjonering innebærer dette at samtaletid alene er et alvorlig utilstrekkelig mål på kapasitetsbinding. Bindingstidsproxyen (anrop → første ressurs fremme + kvittering) fanger den operative virkeligheten bedre, men er fortsatt konservativ: den inkluderer ikke oppfølging, samband og loggføring etter at første ressurs er fremme.

---

## 8.2 Modellprediksjoner versus opplevd virkelighet

### 8.2.1 Gapet mellom modell og erfaring

Modellen predikerer at 32,6 % av beredskapsanropene på natt/helg ankommer i svikt-tilstand — der ingen operatør er ledig (funn 3). Dette er hvert tredje beredskapsanrop. Likevel opplever ikke operatørene total kollaps. Anropene besvares. Hendelsene håndteres. Hvordan kan modellen vise så høy sviktrate når systemet tilsynelatende fungerer?

Forklaringen ligger i det modellen er designet for å måle: den måler brudd på *driftsstandarden*, ikke brudd på *tjenesten*. Svikt betyr at makkerpar-prosedyren ikke kan opprettholdes — ikke at ingen svarer. Operatørene kompenserer ved å tilpasse seg: makkerparet splittes, solo-drift inntreffer, kvalitetssikringen forsvinner, men anropet besvares. Denne tilpasningen er ikke et sammenbrudd — det er den daglige operative virkeligheten som gjør at tjenesten opprettholdes under press.

### 8.2.2 Kvalitetsreduksjon som usynlig buffer

Gustavsson (2018) dokumenterer denne mekanismen ved SOS Alarm: agenter under press komprimerer servicetiden og reduserer kvaliteten — «agents themselves are affected by their workload and duties, which inter alia affect their efficiency.» Tilpasningen er rasjonell fra operatørens perspektiv: det er bedre å svare fort med redusert kvalitet enn å la en innringer vente. Men konsekvensen er at kapasitetsproblemet aldri blir synlig i tradisjonell statistikk. Svartiden forblir akseptabel. Oppdragene lukkes. Årsrapporten viser ingen avvik.

Leonardsen, Hardeland, Hellesø og Grøndahl (2021) beskriver det samme fenomenet kvalitativt ved norske AMK-sentraler: operatørene utfører komplekse, simultane oppgaver — snakke, lokalisere, klassifisere, beslutte respons, gi førstehjelp per telefon — uten anerkjennelse for kompetansen som kreves. Arbeidspresset absorberes i hverdagstilpasningen og forblir usynlig for omgivelsene.

Modellens styrke er at den *gjør synlig det som ellers er usynlig*. Den kvantifiserer ikke feil eller forsinkelser — den kvantifiserer hvor ofte operatørene befinner seg i en tilstand der den operative standarden for korrekt og trygg hendelseshåndtering ikke er oppfylt. At operatørene likevel leverer en tilstrekkelig tjeneste under disse betingelsene er ikke et motargument mot modellen — det er en beskrivelse av den operative kostnaden som bæres av den enkelte operatøren.

**Driftsstandard versus regulatorisk minimumskrav.** Det er presisert at makkerpar-prinsippet ikke er et eksplisitt lovkrav i brann- og redningsvesenforskriften — forskriften fastsetter kun minimum to operatører per skift. Makkerpar er en *prosedyrestandard* etablert lokalt for å oppfylle de faglige sikkerhetsprinsippene som forskriften og tilhørende ROS-analyser bygger på: kvalitetssikring gjennom medlytt, redusert risiko for feil i adressefangst og utalarmering, og evne til å overholde 90-sekunders dispatch-frist. Når modellen viser at 32,6 % av beredskapsanropene på natt/helg ankommer i Svikt og ytterligere 20,3 % i Brudd, er den operative konsekvensen at sentralen i over halvparten av beredskapsanropene på disse skiftene må håndtere hendelsen med svekket eller fraværende kvalitetssikring sammenlignet med den standarden ROS-analysen forutsetter. Dette er en *systematisk planlagt avvikelse* fra driftsstandarden, ikke en sjelden unntaksbelastning. Spørsmålet for dimensjoneringspraksis er derfor ikke om sentralen overholder minimumsbemanningen (det gjør den), men om bemanningen faktisk realiserer de sikkerhetsprinsippene ROS-analysen legger til grunn — eller om den i realiteten planlegger med kronisk svekket kvalitetssikring som normaltilstand.

### 8.2.3 Implikasjoner for operatørbelastning

Funnet har konsekvenser utover den enkelte hendelsen. Den kaliforniske PSAP-studien (California Governor's Office of Emergency Services, 2024) dokumenterer at 38 % av PSAPene konsekvent er under minimumsbemanning, og at de viktigste driverne for personalflukt er stress og mental helse (74 %), ikke lønn. Operatører i aldersgruppen 35–44 år med 4–15 års erfaring — nettopp de mest kompetente — er hardest rammet. Studien viser en tilbakekoblingssløyfe: undermanning → økt press → turnover → ytterligere undermanning.

Leonardsen et al. (2021) rapporterer tilsvarende funn fra norske AMK-sentraler: manglende debriefing, ingen tilbakemelding, og en opplevelse av usynlighet. Jamtli, Svendsen, Jørgensen, Kramer-Johansen, Hov og Hardeland (2024) finner at operatører ved AMK Oslo under arbeidspress avviker fra protokollen og stoler mer på intuisjon — en rasjonell tilpasning som likevel øker risikoen for feil.

Disse funnene fra internasjonal og norsk forskning tyder på at kapasitetsproblemet modellen avdekker ved 110 Sør-Vest ikke er et isolert lokalt fenomen, men en strukturell konsekvens av det samme lav-belastede paradokset som rammer alle små nødmeldesentraler.

---

## 8.3 Implikasjoner for bemanningsdimensjonering

### 8.3.1 Svar på problemstillingen

Problemstillingen spør: *I hvilken grad samsvarer faktisk bemanning ved norske 110-sentraler med kapasitetsbehovet beregnet fra historiske hendelsesdata og køteoretiske modeller?*

Svaret er todelt. Erlang-C-analysen, som er den modelltypen nærmest gjeldende praksis for dimensjonering, gir inntrykk av at bemanningen er komfortabel (ρ < 6 %). Den prosedyrbaserte modellen viser at dette bildet er misvisende: med faktisk bemanning er 40,4 % av beredskapsanropene i brudd eller svikt (variant A), stigende til 46,0 % når total belastning inkluderes (variant B hoved). På natt/helg er over halvparten av beredskapsanropene i brudd eller svikt-tilstand (53,1 % variant A, 55,6 % variant B).

Samsvaret mellom bemanning og kapasitetsbehov avhenger dermed av hvilken standard man måler mot. Mot en ren køteoretisk standard (ventetid < 30 sek) ser bemanningen tilstrekkelig ut. Mot en prosedyrbasert standard (makkerpar opprettholdt) er det et strukturelt gap — størst på natt/helg (c_eff = 2), der asymmetrien mellom kapasitet og makkerpar-kravet er mest akutt. Modellen avdekker også at kapasitetsgapet primært drives av pri-1-hendelser (D-pri1): én aktiv bygningsbrann eller trafikkulykke binder hele makkerparet på natt/helg, slik at neste beredskapsanrop i samme tidsvindu automatisk ankommer i svikt.

### 8.3.2 Asymmetrien mellom dag og natt

Funn 4 viser at +1 operatør har størst effekt på natt/helg: Normal øker fra 46,9 % til 67,2 % (+20,3 pp) og svikt halveres fra 32,8 % til 16,7 %. Årsaken er strukturell: med c_eff = 2 er det kun ett steg fra normal drift til svikt når en D-pri1 er aktiv. Den tredje operatøren gir ikke bare 50 % mer kapasitet — den gir en kvalitativt annen driftssituasjon der D-pri1-hendelser ikke lenger automatisk medfører svikt for neste ankomst, og der operatørene kan jobbe solo før kapasiteten er helt uttømt.

Denne asymmetrien er konsistent med Garnetts square-root staffing-logikk (kap 3.2): marginalverdien av en ekstra server er størst når antallet servere er lavt. For c_eff = 2 er $\sqrt{c}$ = 1,41 — nesten like stor som c selv. For c_eff = 4 er $\sqrt{c}$ = 2 — halvparten av c. Investeringen i en ekstra operatør gir dermed avtagende avkastning for hvert nivå, men den første ekstra operatøren på natt/helg gir den klart største kapasitetsgevinsten. Dette stemmer også med multiserver-job-rammeverket (Harchol-Balter, 2022) der systemer med store $\vec{k}$-jobber har uforholdsmessig stor sensitivitet til marginell kapasitetsøkning (kap 3.6.3).

### 8.3.3 Bakgrunnsbelastningens rolle

Funn 5 viser at når alle hendelseskategorier inkluderes (variant B), faller Normal-andelen på dag hverdag fra 69,2 % til 58,9 % (−10 pp) og svikt øker fra 14,9 % til 22,0 %. Effekten skyldes primært servicevolumet (22 542 overføringstester per år) som er konsentrert på dagtid.

Dette funnet har implikasjoner for organisering. Ved 110 Sør-Vest håndterer de samme operatørene som tar nødanrop også servicetester. Midt-Norge 110 har en annen modell der servicetesting er skilt ut til dedikert personell. Van Buuren et al. (2017) viser gjennom DES-simulering at funksjonsdifferensiering — der ulike oppgavetyper håndteres av spesialiserte roller — kan forbedre kapasitetsbildet uten å endre bemanningsnivå. Jouini, Dallery og Nait-Abdallah (2008) finner tilsvarende at team-organisering med spesialisering kan oppnå høyere agenteffektivitet enn full pooling, fordi motivasjon og spesialistkompetanse kan veie opp for det statistiske tapet ved å ikke poole.

For 110-sentraler åpner dette for et organisatorisk alternativ til ren bemanningsøkning: skille servicelast fra beredskapslast. Dersom overføringstester håndteres av personell som ikke inngår i beredskapsoperatørgruppen, frigjøres kapasitet for beredskapsoppdrag uten å øke det totale antall ansatte i sentralen.

### 8.3.4 Mot en kvantitativ dimensjoneringsstandard

Den prosedyrbaserte modellen gir et rammeverk for å stille et dimensjoneringsspørsmål som i dag ikke stilles kvantitativt: *For et gitt bemanningsnivå c, hvilken andel av beredskapsanropene håndteres med makkerpar?*

I dag fastsettes bemanning utover minimumskravet (to operatører per skift, jf. brann- og redningsvesenforskriften) gjennom lokale ROS-analyser. Disse er kvalitative og vanskelige å etterprøve kvantitativt på tvers av sentraler. Meld. St. 16 (2023–2024) viderefører denne modellen uten å introdusere en nasjonal standard. Den interdepartementale arbeidsgruppen (2009) foreslo servicenivåkrav (8–10 sekunders svartid), men bemerket selv at det «ikke finnes vitenskapelig grunnlag for de valgte terskelverdiene.» NENA (2020) erkjenner tilsvarende at den internasjonale standarden (90 % besvart innen 15 sekunder) mangler empirisk begrunnelse.

Dimensjoneringsforskriften for brannvesen (FOR-2023-01-06-23) viser at en kvantitativ, etterprøvbar standard er mulig: den gir ferdige bemanningskrav basert på innbyggertall og responstid. En tilsvarende standard for 110-operatører ville ta utgangspunkt i hendelsesdata og operativ binding fremfor kvalitative risikovurderinger. Modellen i denne rapporten er et skritt i den retningen — den gir et kvantitativt grunnlag for å sammenligne kapasitetstilstand på tvers av sentraler, gitt at de har tilsvarende datatilgang.

### 8.3.5 Overløp som systemarkitektur

Overløpsmekanismen ved 110 Sør-Vest — automatisk overføring til Agder etter 30 sekunder eller ved 10. kø-anrop — fungerer som en de facto kapasitetsbuffer. Penverne, Martinez, Cellier et al. (2024) viser gjennom digital tvilling-simulering av franske nødmeldesentraler at slik «interconnection» (delt kø med regional prioritet) kan forbedre servicekvaliteten med 17–32 % sammenlignet med isolert drift, og at denne modellen faktisk presterer bedre enn full virtualisering (sammenslåing til én sentral). Årsaken er at regionalkunnskap bevares ved interconnection men tapes ved full sammenslåing — et funn som bekrefter Dwars' (2013) og Gustavssons (2018) observasjoner om regionalt kunnskapstap ved sentralsammenslåing.

For 110-sentralene innebærer dette at overløpsarkitekturen mellom nabosentraler kan ha større potensial enn full sentralsammenslåing — forutsatt at overløpsmekanismene er godt designet og at operatørene ved mottakersentralen har tilstrekkelig lokalkunnskap.

---

## 8.4 Begrensninger

### 8.4.1 Datamessige begrensninger

Analysen bygger på data fra én sentral (110 Sør-Vest) i ett kalenderår (2025). Generaliserbarhet til andre sentraler forutsetter at operative prosedyrer og registreringspraksis er tilstrekkelig like. Felles oppdragshåndteringssystem (LEO) fra høsten 2024 gir bedre grunnlag for sammenligning enn tidligere, men det er ikke verifisert at alle sentraler registrerer sammenstilte anrop og hendelsestyper likt.

Feltet `Opprinnelig oppdragstype` har 16 % dekning for hendelser uten utrykning. Dette medfører at 27 % av oppdragene klassifiseres som L-ukjent (avsnitt 6.2). L-ukjent er her en *naturlig kategori* for oppdrag uten registrert initiell hendelsestype — ikke et uttrykk for «missing data» i tradisjonell forstand. Andelen reflekterer at ikke alle henvendelser klassifiseres formelt før oppdraget lukkes, særlig korte avklaringer og videreformidlinger. Hadde dekningen vært høyere, kunne fordelingen mellom L-aba, L-hendelse og L-ukjent vært mer presis — men sensitivitetsanalysen (avsnitt 7.7) viser at hovedfunnet er robust uavhengig av bindingstidsantakelsene for disse kategoriene.

Nasjonal sammenligning gjennom DSBs 2025-datasett (508 228 oppdrag, alle 12 sentraler) viser at L-aba-andelen varierer betydelig mellom sentraler (0,0 % Sør-Øst og Oslo → 7,5 % Nordland). Denne variasjonen skyldes trolig ulik registreringspraksis mer enn reell ABA-belastning, og understreker at nasjonal benchmarking krever felles klassifiseringsregler før kvantitative sammenligninger kan tolkes normativt.

### 8.4.2 Modellmessige begrensninger

Modellen behandler kapasitetsbinding som binær: en operatør er enten tilgjengelig eller opptatt. I praksis finnes grader av tilgjengelighet — en operatør i GUL-oppfølgingsfase kan avbrytes for et nytt akutt anrop, men med en kostnad i form av kontekstbytte og potensielt forsinket respons. Modellen fanger ikke denne graderingen, noe som kan overestimere svikt i perioder der operatører er i sen oppfølgingsfase.

Vaktleder (VL) er ekskludert fra c_eff i alle skifttyper. I praksis kan VL tre inn som operatør under ekstremt press. Denne reservekapasiteten er ikke modellert, noe som gjør sviktanslaget konservativt. Samtidig innebærer VL-inntreden at oversiktsfunksjonen svekkes — en kostnad som ikke er kvantifisert.

Ring-flom (call surge) fra flere innringere som melder samme hendelse er delvis fanget gjennom sammenstilte anrop, men den tidsmessige korrelasjonen mellom slike anrop er ikke eksplisitt modellert. Gustavssons (2018) burst-modell ($A \cdot e^{-tB}$) gir et rammeverk for å modellere dette, men krever mer detaljerte ankomstdata enn det som er tilgjengelig i BRIS.

### 8.4.3 Antakelser med konsekvenser

Bindingstidsestimatene for ikke-D-kategorier (variant B) er delvis empirisk kalibrert (L-aba: LABA-dybdeanalyse, 50 trukne hendelser / 49 gyldige — hovedparameter bygger på Kilde=Alarm-subsettet, n = 30) og delvis operative estimater (S, L-hendelse, L-ukjent, F, V — forelagt vaktleder for validering). Sensitivitetsanalysen i avsnitt 7.7 viser at hovedfunnet er robust over hele spennet av rimelige antakelser — svikt på natt/helg er 30–38 % i alle scenarioer. D-aba Fase 2-parametrene ($p = 0,30/0,50/0,70$; $Y = 3/6/10$ min) fanger både operatørvurderingen og empirisk underkant-estimat fra sekvensgap-metoden.

LABA-hovedparameteren bygger på Kilde=Alarm-subsettet (n = 30) og har 95 % CI [3,70; 8,56] min for mean — en reell og betydelig usikkerhet. Et utvidet utvalg (n = 100) er under innhenting og inngår ikke i hovedresultatet i denne rapportversjonen; ny mean kan medføre en mindre revisjon. Median (2,87 min) og høy-scenario (9 min) er dekket i sensitivitetsanalysen.

Antagelsen om at sammenstilte anrop har 1 minutts bindingstid er en forenkling. Dersom reell bindingstid er høyere (f.eks. 2–3 minutter for anrop der innringer er stresset), undervurderer modellen effekten av skjulte anrop ytterligere.

---

## 8.5 Videre forskning

Tre retninger fremstår som mest lovende:

**1. Validering på tvers av sentraler.** Den viktigste utvidelsen er å kjøre samme modell på data fra flere 110-sentraler. Felles LEO-system fra 2024 gjør dette prinsipielt mulig. En tverrsentralanalyse ville teste om modellens funn er robuste utover 110 Sør-Vest, og gi grunnlag for å identifisere strukturelle prediktorer (hendelsesvolum, innbyggertall, areal) for dimensjoneringsbehov.

**2. Tidsvariabel analyse.** Modellen behandler dag- og nattskift som homogene perioder. En mer finkornet analyse — per time eller per totime — ville identifisere spesifikke sårbare perioder (f.eks. skiftveksling kl. 19:00) og muliggjøre mer målrettet bemanningsplanlegging. Jennings, Mandelbaum, Massey og Whitt (1996) og Stolletz (2008) gir rammeverk for tidsvariabel bemanningsoptimering som kunne tilpasses 110-konteksten.

**3. Simuleringsbasert modellering.** Dwars' (2013) DES-tilnærming og Penvernes (2024) digitale tvilling-simulering viser at diskret hendelsessimulering kan fange dynamikker som den deterministiske sweep-algoritmen ikke håndterer — blant annet stokastisk variasjon i ankomsttidspunkt, variabel servicetid og overløpsarkitektur mellom sentraler. En DES-modell kalibrert mot 110-data ville gi mer nyanserte kapasitetsestimater og mulighet for å teste organisatoriske endringer (f.eks. funksjonsdifferensiering av servicelast) før implementering.

---

*Kap 8 — Versjon 1.0 | Sist oppdatert: 2026-04-14*
