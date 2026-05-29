# 9. Diskusjon

Denne diskusjonen knytter analysens fem hovedfunn (avsnitt 8.7) til problemstillingen, relevant teori og praktiske implikasjoner. Diskusjonen er strukturert rundt fire tema: det metodiske argumentet for en prosedyrebasert modell fremfor klassisk køteori, forholdet mellom modellprediksjoner og opplevd virkelighet, implikasjoner for bemanningsdimensjonering, og begrensninger og videre forskning.

> **Kort oversikt: diskusjonens svar på RQ1 til RQ5** (fulltekstsvar i kap 10.2):
>
> - **RQ1 (ankomstrate og belastningsmønster):** Empirisk grunnlag etablert; topptung dagprofil og sårbar overgangssone ved skiftveksling kl. 19:00. Resultater i kap 8.1; drøftes i 9.1.
> - **RQ2 (håndteringstid og kapasitetsbinding):** Aktiv bindingstid (D-pri1 median 14,1 min) er vesentlig lenger enn samtaletid (3,4 min). Drøftes i 9.1.3.
> - **RQ3 (ankomstkonflikt og dag/natt-gap):** Strukturelt gap dokumentert; svikt natt/helg 32,6 % (variant A) / 33,2 % (variant B). Resultater i 8.1 til 8.3; drøftes i 9.2 og 9.3.
> - **RQ4 (ROS-grunnlaget):** Kvalitativt, uten kvantitativ benchmark. Resultatobservasjoner i 8.4; drøftes i 9.3.4.
> - **RQ5 (generaliserbarhet):** Teknisk overførbar, men forutsetter felles klassifisering. Nasjonal benchmarking i 8.5; drøftes i 9.3.4 og 9.4.1.


Et forventet funn var at Erlang-C undervurderer kapasitetsbehovet når makkerpar-binding og aktivt hendelsebilde tas med. Mer overraskende er at total operativ belastning først og fremst forverrer dagkapasiteten, mens natt/helg fortsatt er strukturelt sårbar selv når modellen avgrenses til beredskapsbelastning.

## 9.1 Hvorfor Erlang-C er utilstrekkelig for 110-konteksten, og hvor den fortsatt fungerer

Resultatene i 8.1 til 8.3 dokumenterer at en prosedyrebasert ankomstkonfliktmodell gir et mer nyttig dimensjoneringsbilde enn klassisk Erlang-C i 110-konteksten. Det er en konklusjon basert på ett case og bør ikke leses som en generell underkjenning av køteoretiske metoder. Erlang-C og dens etterfølgere forblir godt egnet for systemer der antagelsene de bygger på faktisk holder: store call centre med tilstrekkelig statistisk masse, én-til-én betjening uten makkerpar-krav, og et arbeidsvolum dominert av samtaletid. Kritikken nedenfor gjelder spesifikt 110-kontekstens kombinasjon av lav last, makkerpar-prosedyre og lang bindingstid utover samtaletid, ikke køteorien som sådan.

### 9.1.1 Det lav-belastede paradokset

Erlang-C konkluderer med at 110 Sør-Vest har svært lav systemutnyttelse (ρ < 6 %) og nær null sannsynlighet for ventetid over 30 sekunder (funn 1). Isolert sett kunne dette tyde på at sentralen er betydelig overbemannet. Resultatet er formelt korrekt, men operativt utilstrekkelig som dimensjoneringsgrunnlag for 110, og dette er ikke et tilfelle unikt for 110.

Fenomenet er godt dokumentert i køteoretisk litteratur. Garnett et al. (2002) viser at for systemer med lav tilbudt trafikk (R) dominerer kvadratrotleddet i bemanningsformelen: $N = R + \beta\sqrt{R}$. Når R er lav, som ved 110-sentraler, gir dette uunngåelig lav utnyttelse, ikke fordi systemet er overbemannet, men fordi det opererer i det kvalitetsdrevne regimet (QD) der overskuddskapasitet er en strukturell nødvendighet for å opprettholde servicenivå. Feldman et al. (2008, s. 334) formulerer dette direkte: «When the load is small, the addition or removal of a single server will greatly affect the delay probability.» Med c_eff = 2 på natt/helg er 110 Sør-Vest i denne sonen, og ett operatørskifte endrer kapasitetsbildet fundamentalt.

Dwars (2013) observerer det samme fenomenet i nederlandske ambulansesentraler: disse er «intrinsically lightly-loaded systems». Lav utnyttelse bør ikke tolkes som overkapasitet, men som en konsekvens av stordriftsulempen ved små enheter. Gans et al. (2003) beskriver den inverse mekanismen som «statistical economies of scale». Ved 110-sentraler med to til tre operatører er disse stordriftsfordelene i praksis fraværende.

### 9.1.2 Makkerpar som flereenhets-betjening

Den fundamentale begrensningen ved Erlang-C for 110-konteksten er ikke ankomstprosessen eller fordelingen av betjeningstid, men antagelsen om at én server betjener én kunde. Prosedyren ved 110 Sør-Vest krever at to operatører (RØD og GUL) aktiveres fra første sekund av et beredskapsanrop (avsnitt 4.2.2). Dette er en form for simultan flereenhets-betjening som har vært formelt behandlet i køteorien siden Chelst og Barlach (1981), som utvider Larsons hyperkubemodell med «Type 2-anrop», det vil si hendelser som krever to enheter samtidig. Brill og Green (1984) viser at slike systemer har vesentlig annen kapasitetsdynamikk enn én-enhetssystemer, og Harchol-Balter (2022) generaliserer dette til multiserver-job-køer der jobber krever flere servere parallelt.

Primærmodellen i denne rapporten adresserer nettopp dette gjennom op-binder-semantikken (kap 3.7): i stedet for å modellere operatører som uavhengige servere som hver behandler én kunde av gangen, ekspanderes hver hendelse til ett eller flere op-binder-events som hver binder $q \in \{1, 2\}$ operatører i $d$ minutter. Dette løser Erlang-C-mangelen på tre presise måter: (i) D-pri1-events med $q = 2$ representerer makkerpar-bindingen direkte, slik at en aktiv pri-1-hendelse alltid blokkerer to operatører, ikke én; (ii) heterogene job sizes ($q = 2$ for D-pri1, $q = 1$ for D-aba og øvrige) fanger den operative differensieringen mellom hendelseskategorier som Erlang-C behandler likt; og (iii) prosedyrekalibrerte varigheter $d$ erstatter den eksponentielle servicetiden, slik at modellen reflekterer faktiske bindingsmønstre snarere enn matematisk bekvemmelighet. Kapasitetsnivåene (Normal/Brudd/Svikt) er direkte utledet fra prosedyrens rollestruktur, ikke fra køteoretiske antagelser om serverutnyttelse.

### 9.1.3 Bindingstid som kapasitetsbegrep

Funn 2 viser at operatørene for D-pri1-hendelser er bundet i median 14,1 minutter per oppdrag (inkludert +3 min kvitteringsvindu), vesentlig lenger enn den rene samtaletiden (median 3,4 minutter i Erlang-C). Denne diskrepansen er ikke overraskende i lys av litteraturen: van Buuren et al. (2017) dokumenterer i sin DES-modell av nederlandske nødmeldesentraler at funksjonsdifferensiering (call taker vs. dispatcher) gir markant ulike servicetider for ulike roller, og at den samlede bindingstiden per hendelse er summen av flere deloperasjoner. Gustavsson (2018) viser tilsvarende at agenter ved SOS Alarm komprimerer servicetiden under press, men at denne kompresjonen har en kvalitetskostnad.

For 110-dimensjonering innebærer dette at samtaletid alene er et alvorlig utilstrekkelig mål på kapasitetsbinding. Bindingstidsproxyen (anrop → første ressurs fremme + kvittering) fanger den operative virkeligheten bedre, men er fortsatt konservativ: den inkluderer ikke oppfølging, samband og loggføring etter at første ressurs er fremme.

---

## 9.2 Modellprediksjoner versus opplevd virkelighet

### 9.2.1 Gapet mellom modell og erfaring

Modellen predikerer at 32,6 % av beredskapsanropene på natt/helg ankommer i svikt-tilstand, der ingen operatør er ledig (funn 3). Dette er hvert tredje beredskapsanrop. Likevel opplever ikke operatørene total kollaps. Anropene besvares. Hendelsene håndteres. Hvordan kan modellen vise så høy sviktrate når systemet tilsynelatende fungerer?

Forklaringen ligger i det modellen er designet for å måle: den måler brudd på *driftsstandarden*, ikke brudd på *tjenesten*. Svikt betyr at makkerpar-prosedyren ikke kan opprettholdes, ikke at ingen svarer. Operatørene kompenserer ved å tilpasse seg: makkerparet splittes, solo-drift inntreffer, kvalitetssikringen forsvinner, men anropet besvares. Denne tilpasningen er ikke et sammenbrudd; det er den daglige operative virkeligheten som gjør at tjenesten opprettholdes under press.

### 9.2.2 Kvalitetsreduksjon som usynlig buffer

Gustavsson (2018) dokumenterer denne mekanismen ved SOS Alarm: agenter under press komprimerer servicetiden og reduserer kvaliteten: «agents themselves are affected by their workload and duties, which inter alia affect their efficiency.» Tilpasningen er rasjonell fra operatørens perspektiv: det er bedre å svare fort med redusert kvalitet enn å la en innringer vente. Men konsekvensen er at kapasitetsproblemet aldri blir synlig i tradisjonell statistikk. Svartiden forblir akseptabel. Oppdragene lukkes. Årsrapporten viser ingen avvik.

Leonardsen et al. (2021) beskriver det samme fenomenet kvalitativt ved norske AMK-sentraler: operatørene utfører komplekse, simultane oppgaver (snakke, lokalisere, klassifisere, beslutte respons, gi førstehjelp per telefon) uten anerkjennelse for kompetansen som kreves. Arbeidspresset absorberes i hverdagstilpasningen og forblir usynlig for omgivelsene.

Modellens styrke er at den *gjør synlig det som ellers er usynlig*. Den kvantifiserer ikke feil eller forsinkelser; den kvantifiserer hvor ofte operatørene befinner seg i en tilstand der den operative standarden for korrekt og trygg hendelseshåndtering ikke er oppfylt. At operatørene likevel leverer en tilstrekkelig tjeneste under disse betingelsene er ikke et motargument mot modellen; det er en beskrivelse av den operative kostnaden som bæres av den enkelte operatøren.

**Driftsstandard versus regulatorisk minimumskrav.** Det er presisert at makkerpar-prinsippet ikke er et eksplisitt lovkrav i brann- og redningsvesenforskriften; forskriften fastsetter kun minimum to operatører per skift. Makkerpar er en *prosedyrestandard* etablert lokalt for å oppfylle de faglige sikkerhetsprinsippene som forskriften og tilhørende ROS-analyser bygger på: kvalitetssikring gjennom medlytt, redusert risiko for feil i adressefangst og utalarmering, og evne til å overholde 90-sekunders dispatch-frist. Når modellen viser at 32,6 % av beredskapsanropene på natt/helg ankommer i Svikt og ytterligere 20,3 % i Brudd, er den operative konsekvensen at sentralen i over halvparten av beredskapsanropene på disse skiftene må håndtere hendelsen med svekket eller fraværende kvalitetssikring sammenlignet med den standarden ROS-analysen forutsetter. Dette er en *systematisk planlagt avvikelse* fra driftsstandarden, ikke en sjelden unntaksbelastning. Spørsmålet for dimensjoneringspraksis er derfor ikke om sentralen overholder minimumsbemanningen (det gjør den), men om bemanningen faktisk realiserer de sikkerhetsprinsippene ROS-analysen legger til grunn, eller om den i realiteten planlegger med kronisk svekket kvalitetssikring som normaltilstand.

### 9.2.3 Alternative tolkninger av Svikt-andelen

Diskusjonen over har lagt en bestemt tolkning til grunn: at modellens høye Svikt-andel reflekterer et reelt kapasitetsproblem som operatørene kompenserer for gjennom kvalitetsreduksjon og solo-drift. Dette er forfatterens primære tolkning, men det er ikke den eneste mulige. Tre alternative forklaringer bør drøftes eksplisitt før funnene leses som dokumenterte:

**Alternativ 1: Modellens definisjon av Svikt er for streng.** Modellen klassifiserer en operatør som «opptatt» gjennom hele bindingstiden, for D-pri1 i median 14,1 minutter. Hvis operatører i praksis frigjøres helt eller delvis i sluttfasen (f.eks. GUL etter at første ressurs er på plass), er modellens effektive bindingstid for konservativ. Sviktraten ville da være overestimert. Mot dette taler at bindingstidsdefinisjonen er forankret i operativ prosedyre og operatørens egne beskrivelser av når kvittering og loggføring faktisk er avsluttet, men en empirisk validering med tidssensitiv operatøraktivitetslogg ville gitt sterkere belegg.

**Alternativ 2: VL-rollen i praksis er mer aktiv enn modellen antar.** Forutsetningen $c_{\text{eff}} = c_{\text{total}} - 1$ er empirisk støttet (jf. VL-valideringsnotatet), men kan tenkes å bryte sammen i akkurat de tilfellene modellen klassifiserer som Svikt, der VL trer inn fordi det ikke er noe alternativ. Hvis VL i praksis besvarer en ikke-triviell andel av anrop i Svikt-tilstand, reduseres den reelle ubesvarte-andelen, men oversiktsrollen svekkes til en kostnad som ikke er modellert. Dette er en gradvis svekkelse, ikke en binær feil: modellens Svikt-andel ville fortsatt beskrive en operasjonelt presset tilstand, men ikke en der ingen er tilgjengelig.

**Alternativ 3: Registreringspraksis i BRIS gjør sekvensgap til en upålitelig proxy for skjulte anrop.** Sekvensgap-metoden er validert lokalt for Sør-Vest, men antagelsen om at gap representerer sammenstilte anrop hviler på registreringspraksis som ikke er uavhengig revidert. Hvis en større andel av gapene reflekterer overflyt til Agder eller avbrutte anrop (jf. Tabell 8.10, der Sør-Vest har 23,4 % skjult-rate og andre sentraler 23 til 65 %), er de 18 901 skjulte anropene en blanding heller enn et rent sammenstillings-estimat. Modellens kapasitetsbinding fra skjulte anrop er da delvis spuriøs.

Hvert av disse alternativene trekker tolkningen i samme retning: Svikt-andelen som *registrert* over- eller underestimat avhenger av hvilken antagelse som svikter. Sensitivitetsanalysen (Tabell 8.5) fanger noe av usikkerheten, men ikke alternativene 1 og 2, som krever empirisk arbeid utover denne studiens ramme. Vurderingen er at hovedfunnet, at natt/helg er strukturelt sårbar, er robust mot alle tre alternativene, fordi alle tre i hovedsak påvirker tolkningen av tallets *størrelse*, ikke retningen av asymmetrien mellom dag og natt. Men leseren bør forstå at det presise tallet 32,6 % er en modellprediksjon under spesifikke antagelser, ikke en målt observasjon av faktiske kapasitetsbrudd.

### 9.2.4 Implikasjoner for operatørbelastning

Funnet har konsekvenser utover den enkelte hendelsen. Den kaliforniske PSAP-studien (California Governor's Office of Emergency Services, 2024) dokumenterer bred bemanningsbelastning: 10 PSAP-er rapporterte mer enn 30 % vakans, 38 PSAP-er lå mellom 10 og 29 % vakans, og gjennomsnittlig vakans i utvalget var 19 %. Studien peker samtidig på stress og mental helse som sentrale årsaker til personalavgang, fulgt av økonomiske og praktiske forhold. Det illustrerer en tilbakekoblingssløyfe: lav bemanning → økt press → turnover → ytterligere bemanningspress.

Leonardsen et al. (2021) rapporterer tilsvarende funn fra norske AMK-sentraler: manglende debriefing, ingen tilbakemelding, og en opplevelse av usynlighet. Jamtli et al. (2024) beskriver hvordan arbeidspress påvirker beslutningstaking i slagtelefoner ved AMK Oslo, blant annet gjennom avveininger mellom protokoll og erfaringsbasert intuisjon.

Disse funnene fra internasjonal og norsk forskning tyder på at kapasitetsproblemet modellen avdekker ved 110 Sør-Vest ikke er et isolert lokalt fenomen, men en strukturell konsekvens av det samme lav-belastede paradokset som rammer alle små nødmeldesentraler.

---

## 9.3 Implikasjoner for bemanningsdimensjonering

Implikasjonene kan skilles i tre nivåer. For praksis peker funnene mot +1 operatør på natt/helg som primært tiltak, med +1 operatør på dag hverdag som sekundært tiltak og funksjonsdifferensiering av servicelast som alternativt eller komplementært tiltak. For teori viser studien hvordan multiserver-job-rammeverket kan operasjonaliseres som op-binder-semantikk i en nødmeldesentral. For policy viser analysen at en nasjonal dimensjoneringsstandard først krever felles klassifiseringsregler og et datagrunnlag som fanger operativ binding, ikke bare registrerte oppdrag.

### 9.3.1 Svar på problemstillingen

Problemstillingen spør: *I hvilken grad samsvarer faktisk bemanning ved 110 Sør-Vest med kapasitetsbehovet beregnet fra historiske hendelsesdata og køteoretiske modeller, og hva indikerer funnene om overførbarhet til norske 110-sentraler?*

Svaret er todelt. Erlang-C-analysen, som er den modelltypen nærmest gjeldende praksis for dimensjonering, gir inntrykk av at bemanningen er komfortabel (ρ < 6 %). Den prosedyrebaserte modellen viser at dette bildet er misvisende: med faktisk bemanning er 40,4 % av beredskapsanropene i brudd eller svikt (variant A), stigende til 45,6 % når total belastning inkluderes (variant B hoved). På natt/helg er over halvparten av beredskapsanropene i brudd eller svikt-tilstand (53,1 % variant A og 55,2 % variant B).

Samsvaret mellom bemanning og kapasitetsbehov avhenger dermed av hvilken standard man måler mot. Mot en ren køteoretisk standard (ventetid < 30 sek) ser bemanningen tilstrekkelig ut. Mot en prosedyrebasert standard (makkerpar opprettholdt) er det et strukturelt gap, størst på natt/helg (c_eff = 2), der asymmetrien mellom kapasitet og makkerpar-kravet er mest akutt. Modellen avdekker også at kapasitetsgapet primært drives av pri-1-hendelser (D-pri1): én aktiv bygningsbrann eller trafikkulykke binder hele makkerparet på natt/helg, slik at neste beredskapsanrop i samme tidsvindu automatisk ankommer i svikt.

### 9.3.2 Asymmetrien mellom dag og natt

Funn 4 viser at +1 operatør har størst effekt på natt/helg: Normal øker fra 46,9 % til 67,2 % (+20,3 pp) og svikt reduseres fra ca. 33 % til 16,7 %. Årsaken er strukturell: med c_eff = 2 er det kun ett steg fra normal drift til svikt når en D-pri1 er aktiv. Den tredje operatøren gir ikke bare 50 % mer kapasitet, den gir en kvalitativt annen driftssituasjon der D-pri1-hendelser ikke lenger automatisk medfører svikt for neste ankomst, og der operatørene kan jobbe solo før kapasiteten er helt uttømt.

Denne asymmetrien er konsistent med square-root staffing-logikken i små servicesystemer (kap 3.2): marginalverdien av en ekstra server er størst når antallet servere er lavt og bufferkapasiteten er knapp. I Halfin-Whitt-formuleringen er bufferleddet knyttet til tilbudt trafikk ($\beta\sqrt{R}$), ikke direkte til $\sqrt{c}$, men den operative tolkningen er den samme her: når c_eff = 2, endrer én ekstra operatør hele terskelstrukturen for makkerpar-drift. Investeringen i en ekstra operatør gir dermed avtagende avkastning for hvert nivå, men den første ekstra operatøren på natt/helg gir den klart største kapasitetsgevinsten. Dette stemmer også med multiserver-job-rammeverket (Harchol-Balter, 2022) der systemer med store $\vec{k}$-jobber har uforholdsmessig stor sensitivitet til marginell kapasitetsøkning (kap 3.6.3).

### 9.3.3 Bakgrunnsbelastningens rolle

Funn 5 viser at når alle hendelseskategorier inkluderes (variant B), faller Normal-andelen på dag hverdag fra 69,2 % til 59,5 % (en reduksjon på 9,7 pp) og svikt øker fra 14,9 % til 21,6 %. Effekten skyldes primært servicevolumet (22 542 overføringstester per år) som er konsentrert på dagtid.

Dette funnet har implikasjoner for organisering. Ved 110 Sør-Vest håndterer de samme operatørene som tar nødanrop også servicetester. Midt-Norge 110 har en annen modell der servicetesting er skilt ut til dedikert personell. Van Buuren et al. (2017) viser gjennom DES-simulering at funksjonsdifferensiering, der ulike oppgavetyper håndteres av spesialiserte roller, kan forbedre kapasitetsbildet uten å endre bemanningsnivå. Jouini et al. (2008) finner tilsvarende at team-organisering med spesialisering kan oppnå høyere agenteffektivitet enn full pooling, fordi motivasjon og spesialistkompetanse kan veie opp for det statistiske tapet ved å ikke poole.

For 110-sentraler åpner dette for et organisatorisk alternativ til ren bemanningsøkning: skille servicelast fra beredskapslast. Dersom overføringstester håndteres av personell som ikke inngår i beredskapsoperatørgruppen, frigjøres kapasitet for beredskapsoppdrag uten å øke det totale antallet ansatte i sentralen.

### 9.3.4 Mot en kvantitativ dimensjoneringsstandard: et åpent forskningsspørsmål

Den prosedyrebaserte modellen gir et rammeverk for å stille et dimensjoneringsspørsmål som i dag ikke stilles kvantitativt: *For et gitt bemanningsnivå c, hvilken andel av beredskapsanropene håndteres med makkerpar?* Spørsmålet i seg selv er modellens vesentligste praktiske bidrag, uavhengig av hvilke konkrete terskelverdier en eventuell standard skulle bygge på.

I dag fastsettes bemanning utover minimumskravet (to operatører per skift, jf. brann- og redningsvesenforskriften) gjennom lokale ROS-analyser. Disse er kvalitative og vanskelige å etterprøve kvantitativt på tvers av sentraler. Meld. St. 16 (2023-2024) viderefører denne modellen uten å introdusere en nasjonal standard. Interdepartemental arbeidsgruppe (2009) foreslo servicenivåkrav (8 til 10 sekunders svartid), men bemerket selv at det «ikke finnes vitenskapelig grunnlag for de valgte terskelverdiene.» NENA (2020) erkjenner tilsvarende at den internasjonale standarden (90 % besvart innen 15 sekunder) mangler empirisk begrunnelse.

Brann- og redningsvesenforskriften (FOR-2021-09-15-2755) viser at kvantitative og etterprøvbare krav er mulig på brann- og redningssiden gjennom krav til organisering, beredskap, bemanning og innsatstid. En tilsvarende standard for 110-operatører kunne i prinsippet ta utgangspunkt i hendelsesdata og operativ binding fremfor kvalitative risikovurderinger. Modellen i denne rapporten er ett mulig metodisk byggesteinsforslag i den retningen: den gir et kvantitativt rammeverk for å beskrive kapasitetstilstand for *én* sentral. Hvorvidt den lar seg skalere til en nasjonal standard, er et åpent forskningsspørsmål studien ikke besvarer.

Diskusjonen om en nasjonal dimensjoneringsstandard reiser flere praktiske og normative spørsmål denne studien ikke kan løse: hvilket prosedyrekrav (makkerpar eller annet) som skal være referansen, hvilken Svikt-terskel som er akseptabel, hvordan kostnadene ved økt bemanning veies mot kapasitetsgevinsten, og hvem som skal være regulatorisk eier av en slik standard. Disse spørsmålene er politiske og faglige, ikke metodiske, og bør behandles i en bredere prosess. Det studien bidrar med er et *kvantitativt rammeverk for å stille spørsmålet*, ikke et ferdig svar.


En eventuell nasjonal anvendelse forutsetter at variablene som inngår i modellen er harmonisert på tvers av sentraler: registreringsregel for D-aba/L-aba, håndtering av service, tolkning av sammenstilte anrop, og definisjon av effektiv bemanning. Tabell 8.9 viser at disse variablene per i dag *ikke* er harmonisert: L-aba varierer fra 0,0 % til 7,5 %, og D-pri1 fra 7,0 % til 24,9 %. Uten harmonisering kan nasjonale DSB/LEO/BRIS-tall fortsatt brukes som deskriptiv benchmarking, men ikke som normativ rangering av kapasitet eller bemanningsriktighet.

### 9.3.5 Overløp som systemarkitektur

Overløpsmekanismen ved 110 Sør-Vest (automatisk overføring til Agder etter 30 sekunder eller ved 10. kø-anrop) fungerer som en de facto kapasitetsbuffer. Penverne et al. (2024) viser gjennom digital tvilling-simulering av franske nødmeldesentraler at slik «interconnection» (delt kø med regional prioritet) kan forbedre servicekvaliteten med 17 til 32 % sammenlignet med isolert drift, og at denne modellen faktisk presterer bedre enn full virtualisering (sammenslåing til én sentral). Årsaken er at regionalkunnskap bevares ved interconnection men tapes ved full sammenslåing, et funn som bekrefter observasjonene hos Dwars (2013) og Gustavsson (2018) om regionalt kunnskapstap ved sentralsammenslåing.

For 110-sentralene innebærer dette at overløpsarkitekturen mellom nabosentraler kan ha større potensial enn full sentralsammenslåing, forutsatt at overløpsmekanismene er godt designet og at operatørene ved mottakersentralen har tilstrekkelig lokalkunnskap.

---

## 9.4 Begrensninger

### 9.4.1 Datamessige begrensninger

Analysen bygger på data fra én sentral (110 Sør-Vest) i ett kalenderår (2025). Generaliserbarhet til andre sentraler forutsetter at operative prosedyrer og registreringspraksis er tilstrekkelig like. Felles oppdragshåndteringssystem (LEO) fra høsten 2024 gir bedre grunnlag for sammenligning enn tidligere, men det er ikke verifisert at alle sentraler registrerer sammenstilte anrop og hendelsestyper likt.

Det er forsøkt innhentet avklaringer fra andre sentraler, men det foreligger ikke full svarprosent. Per 06.05.2026 finnes dokumenterte svar fra fire sentraler (Innlandet, Finnmark, Midt-Norge og Vest). Dette svekker ikke hovedfunnene for 110 Sør-Vest, fordi primærmodellen bygger på lokalt LEO/BRIS-uttrekk, prosedyredokumentasjon og lokal validering. Det begrenser derimot hvor langt den nasjonale benchmarkingen kan tolkes: tallene kan beskrive struktur og variasjon, men ikke brukes til å konkludere om lokale årsaker uten forbehold.

Praktisk betyr dette at ikke alle spørsmål til andre sentraler må være bekreftet for at rapporten skal være troverdig. Avklaringer er særlig viktige når de kan endre tolkningen av et nasjonalt benchmarksignal:


| Avklaringstype | Hvorfor den betyr noe | Håndtering hvis svar mangler |
|---|---|---|
| MOB-bemanning og VL-inkludering | Påvirker `c_eff` og oppdrag per effektiv operatør | Bruk MOB som rapportert proxy, ikke som faktisk vaktbemanning |
| ABA- og servicepraksis | Kan forklare 0 % eller svært høy L-aba/D-aba/S-andel | Merk som mulig registrerings-/organisasjonsforskjell |
| Svært høyt/lavt DSB/MOB-forhold eller skjult 110-ID-rate | Kan skyldes ulike telledefinisjoner, overføringer eller sammenstilling | Behold registertall, men ikke tolk som direkte sammenlignbart anropsvolum |
| Store kategoriavvik som påvirker rangering | Kan flytte sentral mellom D, L-aba, L-hendelse og L-ukjent | Presenter som avvik uten lokal årsak, ikke som feil |

Andre opplysninger, som detaljerte lokale bindingstider, subjektiv opplevelse av bemanning, ROS-revisjonsår og interne turnusnyanser ved andre sentraler, er nyttige for senere lokal modellering, men er ikke nødvendige for denne rapportens hovedkonklusjon.

Feltet `Opprinnelig oppdragstype` har 16 % dekning for oppdrag uten utrykning. Dette medfører at 27 % av oppdragene klassifiseres som L-ukjent (avsnitt 6.2). L-ukjent er her en *naturlig kategori* for oppdrag uten registrert initiell hendelsestype, ikke et uttrykk for «missing data» i tradisjonell forstand. Andelen reflekterer at ikke alle henvendelser klassifiseres formelt før oppdraget lukkes, særlig korte avklaringer og videreformidlinger. Hadde dekningen vært høyere, kunne fordelingen mellom L-aba, L-hendelse og L-ukjent vært mer presis. Sensitivitetsanalysen (avsnitt 8.3) viser imidlertid at hovedfunnet er robust uavhengig av bindingstidsantakelsene for disse kategoriene.

Nasjonal sammenligning gjennom DSBs 2025-datasett (508 228 oppdrag, alle 12 sentraler) viser at L-aba-andelen varierer betydelig mellom sentraler (fra 0,0 % i Sør-Øst og Oslo til 7,5 % i Nordland). Denne variasjonen skyldes trolig ulik registreringspraksis mer enn reell ABA-belastning. Det understreker at nasjonal benchmarking krever felles klassifiseringsregler før kvantitative sammenligninger kan tolkes normativt.

### 9.4.2 Modellmessige begrensninger

Modellen behandler kapasitetsbinding som binær: en operatør er enten tilgjengelig eller opptatt. I praksis finnes grader av tilgjengelighet. En operatør i GUL-oppfølgingsfase kan avbrytes for et nytt akutt anrop, men med en kostnad i form av kontekstbytte og potensielt forsinket respons. Modellen fanger ikke denne graderingen, noe som kan overestimere svikt i perioder der operatører er i sen oppfølgingsfase.

Vaktleder (VL) er ekskludert fra c_eff i alle skifttyper. I praksis kan VL tre inn som operatør under ekstremt press. Denne reservekapasiteten er ikke modellert, noe som gjør sviktanslaget konservativt. Samtidig innebærer VL-inntreden at oversiktsfunksjonen svekkes, en kostnad som ikke er kvantifisert.

Ring-flom (call surge) fra flere innringere som melder samme hendelse er delvis fanget gjennom sammenstilte anrop. Den tidsmessige korrelasjonen mellom slike anrop er ikke eksplisitt modellert. Gustavssons (2018) burst-modell ($A \cdot e^{-tB}$) gir et rammeverk for dette, men krever mer detaljerte ankomstdata enn BRIS gir.

### 9.4.3 Antakelser med konsekvenser

Bindingstidsestimatene for ikke-D-kategorier (variant B) er delvis empirisk kalibrert (L-aba via LABA-dybdeanalyse, n=100, Kilde=Alarm-subset) og delvis operative estimater (S, L-hendelse, L-ukjent, F, V, forelagt vaktleder). Sensitivitetsanalysen i avsnitt 8.3 viser at hovedfunnet er robust over hele spennet av rimelige antagelser: svikt på natt/helg er 30 til 38 % i alle scenarioer.

LABA-hovedparameteren bygger på Kilde=Alarm-subsettet (n = 100) og har 95 % CI [3,74; 5,43] min for mean, substansielt strammere enn første runde (n = 30, CI [3,70; 8,56]). Median (3,27 min) og høy-scenario (7 min) er dekket i sensitivitetsanalysen. Endringen fra n=30 til n=100 reduserte hovedverdien fra 6 min til 4,5 min og senket variant B-Svikt på natt/helg marginalt (33,4 til 33,2 %).

Antagelsen om at sammenstilte anrop har 1 minutts bindingstid er en forenkling. Dersom reell bindingstid er høyere (f.eks. 2 til 3 minutter for anrop der innringer er stresset), undervurderer modellen effekten av skjulte anrop ytterligere. En fullstendig vurdering av antagelses-konsekvenser er gitt i avsnitt 6.7 (Tabell 6.3 og «Konsekvenser hvis antagelsene svikter»).

---

## 9.5 Videre forskning

Tre retninger fremstår som mest lovende.

**1. Validering på tvers av sentraler.** Den viktigste utvidelsen er å kjøre samme modell på data fra flere 110-sentraler. Felles LEO-system fra 2024 gjør dette prinsipielt mulig. En tverrsentralanalyse ville teste om modellens funn er robuste utover 110 Sør-Vest, og gi grunnlag for å identifisere strukturelle prediktorer for dimensjoneringsbehov.

**2. Tidsvariabel analyse.** Modellen behandler dag- og nattskift som homogene perioder. En mer finkornet analyse, per time eller per totime, ville identifisere spesifikke sårbare perioder (f.eks. skiftveksling kl. 19:00) og muliggjøre mer målrettet bemanningsplanlegging. Jennings et al. (1996) og Stolletz (2008) gir rammeverk for tidsvariabel bemanningsoptimering som kunne tilpasses 110-konteksten.

**3. Simuleringsbasert modellering.** Dwars' (2013) DES-tilnærming og Penverne et al.s (2024) digitale tvilling viser at diskret hendelsessimulering kan fange dynamikker som den deterministiske sweep-algoritmen ikke håndterer. Stokastisk variasjon i ankomsttidspunkt, variabel servicetid og overløpsarkitektur mellom sentraler er eksempler. En DES-modell kalibrert mot 110-data ville gi mer nyanserte kapasitetsestimater og mulighet for å teste organisatoriske endringer før implementering.