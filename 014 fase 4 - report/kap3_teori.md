# 3. Teori

Dette kapitlet etablerer det køteoretiske grunnlaget for kapasitetsanalysen. Det forklarer også hvorfor klassisk M/M/c-teori ikke er tilstrekkelig for 110-konteksten. Progresjonen går i fire trinn: Erlang-C som grunnlinje, deretter QED-regimet og square-root staffing, så multiserver-jobs (MSJ), og til slutt op-binder-semantikken — det teoretiske rammeverket for prosedyrbasert ankomstkonfliktmodellering.

## 3.1 Erlang-C (M/M/c) som referansemodell

Erlang-C-modellen (M/M/c) beskriver et system med $c$ identiske parallelle servere (Erlang, 1917; Gans et al., 2003). Ankomster følger en Poisson-prosess med rate $\lambda$, og servicetiden er eksponentielt fordelt med gjennomsnitt $1/\mu$. Kunder som ankommer når alle servere er opptatt, venter i en felles kø med uendelig kapasitet. Køen betjenes i «first-come-first-served»-rekkefølge.

Systemets tilbudte trafikk er $A = \lambda / \mu$ [Erlang], og serverutnyttelsen er $\rho = A / c$. For stabilt system kreves $\rho < 1$. Sannsynligheten for at en ankomst må vente (Erlang-C-formelen) er:

$$C(c, A) = \frac{A^c / (c! \cdot (1-\rho))}{\sum_{k=0}^{c-1} A^k/k! + A^c / (c! \cdot (1-\rho))}$$

Sannsynlighet for ventetid over en terskel $T$:

$$P(W > T) = C(c, A) \cdot e^{-(c\mu - \lambda)T}$$

Erlang-C er fundamentalt basert på fire antakelser: (1) Poisson-ankomster, (2) eksponentiell servicetid, (3) $c$ uavhengige og parallelle servere, og (4) én server betjener én kunde om gangen. De to siste forutsetningene er der modellen bryter sammen for 110-konteksten.

## 3.2 QED-regimet og square-root staffing

Halfin og Whitt (1981) etablerte det teoretiske grunnlaget for kvalitetsdrevet bemanning (Quality-and-Efficiency-Driven, QED) i flerserver-systemer. For stort $A$ kan bemanningen optimaliseres ved:

$$c = A + \beta \sqrt{A}$$

der $\beta > 0$ er en parameter som reflekterer ønsket servicenivå. Resultatet har to viktige konsekvenser:

1. **Kapasitetsbufferen er ikke-lineær i belastning.** Bemanningsbuffer vokser med kvadratroten av tilbudt trafikk — ikke lineært. For små $A$ dominerer buffer-termen, for store $A$ dominerer $A$ selv.

2. **Små systemer opererer strukturelt med lav utnyttelse.** Når $A$ er lite (slik det er for 110-sentraler med 2–3 operatører og $A < 1$), kreves $c \geq 2$ primært for å sikre tilstrekkelig responsivitet, ikke for å håndtere gjennomsnittlig volum. Serverutnyttelsen $\rho = A/c$ blir dermed lav.

Feldman et al. (2008) uttrykker dette direkte: *«When the load is small, the addition or removal of a single server will greatly affect the delay probability.»* For en 110-sentral med $c_{\text{eff}} = 2$ på natt/helg er denne følsomheten ekstrem — én operatør utgjør halve den operative kapasiteten.

Garnett et al. (2002) og Zeltyn og Mandelbaum (2005) utvidet rammeverket til Erlang-A (M/M/c+M). Her forlater kunder systemet etter en eksponentielt fordelt tålmodighetsterskel. For 110 er dette operativt relevant. Anrop som ikke besvares innen 30 sekunder overføres automatisk til Agder 110. Det er en tålmodighetsmekanisme som bryter med Erlang-C-forutsetningen om uendelig kø.

## 3.3 Det lav-belastede paradokset

Et sentralt teoretisk resultat — relevant for tolkning av de empiriske funnene i kapittel 7 — er at lav serverutnyttelse *ikke* impliserer overbemanning i små nødmeldesentraler. Dwars (2013) beskriver nødmeldesentraler som «intrinsically lightly-loaded systems». Lav utnyttelse er en strukturell konsekvens av stordriftsulempen ved små enheter, ikke et tegn på tilgjengelig kapasitet.

Gans et al. (2003) formaliserer mekanismen som «statistical economies of scale»: jo større servicesystemet er, desto høyere utnyttelse kan oppnås med samme servicenivå. For et system med $c = 2$ er stordriftsfordelene i praksis fraværende — systemets ytelse er svært sårbart for varians i etterspørsel.

Dette gir en viktig teoretisk ramme for å tolke Erlang-C-resultater for 110 Sør-Vest: $\rho < 6$ % betyr *ikke* at sentralen er overbemannet med faktor 16. Det betyr at sentralen opererer i et regime der kvantitativ kømodellering må suppleres med strukturell kapasitetsanalyse.

## 3.4 Tidsvarierende etterspørsel og ikke-stasjonaritet

Klassisk Erlang-C forutsetter stasjonær $\lambda$, men empirisk er ankomstraten til nødmeldesentraler systematisk tidsvarierende (Green et al., 2007; Jennings et al., 1996). For 110-sentraler varierer $\lambda$ over døgnet, ukedager og årstid.

To tilnærminger håndterer dette:

1. **Periode-segmentert statisk analyse (PSSA):** Døgnet deles i skifttyper der $\lambda$ kan approksimeres som konstant, og Erlang-C anvendes separat per segment. Dette er tilnærmingen brukt i grunnlinjen i kapittel 6.3.

2. **Dynamisk modellering:** Stolletz (2008) foreslår «stationary backlog-carryover» (SBC) for ikke-stasjonære M(t)/M(t)/c(t)-systemer. Jennings et al. (1996) utvikler lignende approksimeringer for tidsavhengig bemanning.

For 110-kontekst er PSSA tilstrekkelig som grunnlinje fordi skiftperiodene er klart definerte og ankomstraten er rimelig stasjonær innenfor hver periode. Sterkere dynamisk modellering er et område for videre forskning (se kap 8.5).

## 3.5 Poisson-forutsetningens gyldighet

Matteson et al. (2011) tester Poisson-forutsetningen på EMS-ankomster og viser at den holder innen korte tidsvindu, men brytes av overdispersjon på tvers av dager — drevet av uke- og sesongvariasjoner. For 110-kontekst kommer en ytterligere utfordring: **ring-flom** (call surge).

Gustavsson (2018) og L'Ecuyer et al. (2018) modellerer eksplisitt «bursts» — korte, intense ankomsttopper utløst av enkelthendelser. Slike topper genereres typisk av trafikkulykker eller store branner som utløser mange samtidige innringer fra publikum. De foreslår en burst-modell der ankomstintensiteten etter en hendelse følger $A \cdot e^{-tB}$ — eksponentielt avtagende over tid. Modellen bryter med Poisson-uavhengighet lokalt og gir klyngede ankomster.

For den prosedyrbaserte modellen (kap 6.4) er konsekvensen at Erlang-C undervurderer kapasitetsbelastningen i burst-perioder. Den prosedyrbaserte modellen er mindre sårbar. Den bygger ikke på Poisson-forutsetningen, men måler faktisk observerte ankomsttidspunkter.

## 3.6 Multiserver-jobs og op-binder-semantikk

Den sentrale teoretiske begrensningen ved Erlang-C for 110-konteksten er ikke ankomstprosessen eller servicefordelingen, men **antagelsen om at én server betjener én kunde**. For pri-1-hendelser ved 110 krever prosedyren at to operatører aktiveres parallelt — dette er en form for *multiserver job* (MSJ) som har vært formelt behandlet i køteorien siden Chelst og Barlach (1981).

### 3.6.1 Hyperkubemodellen og Type 2-anrop

Larson (1974) utviklet hyperkubemodellen for ressursdisponering i beredskapsoperative systemer med $c$ enheter. Modellen behandler kapasitetstilstanden som en vektor $\vec{x} \in \{0, 1\}^c$. Hver komponent angir om den tilsvarende enheten er opptatt. Chelst og Barlach (1981) utvider modellen med «Type 2-anrop» — hendelser som krever to enheter simultant:

- **Type 1 (én enhet):** Lettere oppdrag der én enhet er tilstrekkelig.
- **Type 2 (to enheter):** Tunge hendelser der to enheter må aktiveres parallelt.

For 110-kontekst er analogien direkte. D-aba er et Type 1-oppdrag (én operatør serielt). D-pri1 er et Type 2-oppdrag (makkerpar). Chelst og Barlach viser at systemer med Type 2-anrop har fundamentalt annerledes kapasitetsdynamikk enn én-enhetssystemer. Konsekvensen er at bemanningsformler basert på $c$ parallelle servere undervurderer ressursbehovet.

### 3.6.2 Brill og Green — flerserver-blokkering

Brill og Green (1984) analyserer blokkeringssystemer der hver kunde krever $k \geq 1$ samtidige servere for sin behandling. De viser at den klassiske stabilitetsbetingelsen $\rho < 1$ er utilstrekkelig. Systemet kan bli ustabilt lenge før serverutnyttelsen når 1, fordi blokkeringssannsynligheten øker med $k$ og med varians i ankomst- og servicetid. For et system der $k = 2$ er praktisk kapasitet vesentlig lavere enn $c / 2$.

### 3.6.3 Harchol-Balter — moderne MSJ-rammeverk

Harchol-Balter (2022) generaliserer og formaliserer multiserver-job-rammeverket (MSJ). En MSJ har en *job size vector* $\vec{k}$ som angir hvor mange servere jobben krever parallelt. Kapasitetsdynamikken i slike systemer er strukturelt ulik klassisk M/M/c:

- **Bemanningskrav:** For å oppnå samme ventetid kreves flere servere enn i M/M/c.
- **Ankomstkonflikt:** Sannsynligheten for at en ankomst ikke kan starte behandling umiddelbart er ikke bare avhengig av $c$ og $A$, men av fordelingen av $\vec{k}$ blant aktive jobber.
- **Ikke-stabile regimer:** Systemer med store $\vec{k}$-jobber kan bli effektivt mettet ved moderat $\rho$.

For 110-sentraler med $c_{\text{eff}} = 2$ og en D-pri1 med $k = 2$: hele kapasiteten er bundet så lenge D-pri1 pågår. Dette svarer nøyaktig til Svikt-tilstanden i den prosedyrbaserte modellen (kap 6.4).

### 3.6.4 Team-basert kapasitet og function differentiation

Kim et al. (2008) modellerer flerserver-systemer med serversamarbeid. De viser at effektiv kapasitet avhenger av graden av parallell binding. Når to servere er nødvendig per kunde, halveres reell kapasitet sammenlignet med M/M/c med samme $c$. Dette er det nærmeste matematiske analogonet til makkerpar-prinsippet.

Jouini et al. (2008) analyserer team-baserte call-center-organisasjoner der to agenter samarbeider om oppgaver. De finner at team-organisering øker kapasitetsutnyttelsen ved moderat belastning, men skaper sårbarhet ved høy belastning. De viser også at *function differentiation* kan oppnå høyere effektivitet enn full pooling. I funksjonsdifferensierte systemer har agenter spesialiserte roller (typisk dispatcher vs. call taker). Motivasjon og spesialistkompetanse kompenserer for det statistiske tapet ved ikke å poole.

Van Buuren et al. (2017) validerer dette gjennom diskret hendelsessimulering (DES) av nederlandske EMS-sentraler. De viser at funksjonsdifferensiering reduserer kapasitetskravet ved høy belastning uten å øke total bemanning. Funnet er direkte relevant for avsnitt 8.3 (dimensjoneringsalternativer).

## 3.7 Op-binder-semantikk som formalt rammeverk

Op-binder-semantikken er forfatterens syntese. Den oversetter multiserver-job-rammeverket fra Chelst og Barlach (1981) og Harchol-Balter (2022) til 110-konteksten. Oversettelsen består av tre grep: (i) heterogene job sizes per hendelseskategori, (ii) prosedyrekalibrerte varigheter $d$ snarere enn eksponentielt fordelte servicetider, og (iii) kapasitet operasjonalisert som *ankomstkonflikt-andel* snarere enn ventetid. Rammeverket er ikke en ny teoretisk konstruksjon. Det er en konkret formalisering tilpasset prosedyrbasert nødmeldedrift.

Konkret for 110 Sør-Vest betyr dette:

- En **D-pri1-hendelse** (bygningsbrann med utrykning) skaper én op-binder-event med $q = 2$ — makkerparet er bundet i hele akuttfasen (RØD- og GUL-funksjon).
- En **D-aba-hendelse** (automatisk brannalarm med utrykning) skaper én op-binder-event med $q = 1$ for Fase 1 (oppdragsopprettelse + call-out), og — med sannsynlighet $p$ — én tilleggs-event med $q = 1$ for Fase 2 (nødtelefon eller panel-veiledning).
- En **L-aba-hendelse** (ABA uten utrykning, men med Kilde=Alarm) skaper én op-binder-event med $q = 1$.

De formelle definisjonene under generaliserer dette mønsteret:

**Definisjon 3.1 (Op-binder-event).** Et op-binder-event $e = (t, d, q)$ er en tidsavgrenset binding av $q$ operatører, der $q \in \{1, 2\}$, startende ved $t$ og varende i $d$ minutter.

**Definisjon 3.2 (Aktive op-binder).** Ved tidspunkt $\tau$ er antall aktive op-binder:

$$n_{\text{aktive}}(\tau) = \sum_{e \in \mathcal{E} : t_e \leq \tau < t_e + d_e} q_e$$

**Definisjon 3.3 (Ekspansjon av hendelse).** Hver hendelse $h$ genererer én eller flere op-binder-events avhengig av type:
- **D-pri1:** Én event med $q = 2$ (makkerpar).
- **D-aba:** Én event med $q = 1$ (Fase 1), pluss én event med $q = 1$ (Fase 2) med sannsynlighet $p$, forskjøvet med 1,5 min.
- **Øvrige kategorier:** Én event med $q = 1$.

**Definisjon 3.4 (Kapasitetsnivå).** For et nytt beredskapsanrop som ankommer ved $\tau$ med effektiv kapasitet $c_{\text{eff}}$:

$$\text{Nivå}(\tau) = \begin{cases}
\text{Normal} & \text{hvis } c_{\text{eff}} - n_{\text{aktive}}(\tau) \geq 2 \\
\text{Brudd} & \text{hvis } c_{\text{eff}} - n_{\text{aktive}}(\tau) = 1 \\
\text{Svikt} & \text{hvis } c_{\text{eff}} - n_{\text{aktive}}(\tau) \leq 0
\end{cases}$$

Dette rammeverket reduserer til klassisk M/M/c når alle $q_e = 1$ og $d_e$ er eksponentielt fordelt. Erlang-C er dermed et spesialtilfelle av op-binder-semantikk. Rammeverkets generalitet ligger i tre egenskaper: det tillater heterogene job sizes, det bruker prosedyrekalibrerte varigheter, og det modellerer ankomstkonflikt eksplisitt — ikke bare ventetid.

## 3.8 Kvalitetsreduksjon som skjult buffer

Et siste teoretisk bidrag relevant for tolkning (kap 8.2) er litteratur om hvordan operatører tilpasser seg under press. Gustavsson (2018) dokumenterer ved SOS Alarm at agenter under press komprimerer servicetiden og reduserer kvaliteten: *«agents themselves are affected by their workload and duties, which inter alia affect their efficiency»*. Tilpasningen er rasjonell fra operatørens perspektiv. Det er bedre å svare fort med redusert kvalitet enn å la en innringer vente.

Al-Sarhani et al. (2025) viser at simultane hendelser øker kognitiv belastning og feilrate signifikant. Leonardsen et al. (2021) rapporterer tilsvarende funn fra norske AMK-sentraler: manglende debriefing, ingen tilbakemelding, og en opplevelse av usynlighet under høyt press.

Jamtli et al. (2024) beskriver hvordan arbeidspress påvirker beslutningstaking i slagtelefoner ved AMK Oslo, blant annet gjennom avveininger mellom protokoll og erfaringsbasert intuisjon.

Felles for disse studiene er at de dokumenterer en **skjult buffer**. Systemet fungerer ofte «godt nok» fordi operatørene bærer belastningen individuelt gjennom kvalitetsreduksjon, selv når den formelle driftsstandarden er brutt. Dette er en sentral tolkningsramme for kap 8.2. Modellens prediksjon av svikt ved 32,6 % av beredskapsanropene på natt/helg (variant A) er ikke motargument mot at sentralen fungerer. Det er en kvantifisering av den operative kostnaden som bæres av operatørene.

## 3.9 Oppsummering

Det teoretiske grunnlaget kan sammenfattes slik:

| Teorigren | Bidrag til modellen |
|---|---|
| Erlang-C (M/M/c) | Grunnlinje for kapasitetsmodellering; demonstrerer behovet for utvidet rammeverk |
| QED-regimet / square-root staffing | Forklarer hvorfor små systemer opererer strukturelt med lav utnyttelse |
| Erlang-A | Håndterer tålmodighetsterskel (overløp til Agder) |
| Tidsvarierende M(t)/M(t)/c(t) | Motiverer skift-segmentert analyse |
| Burst-modell (Gustavsson) | Identifiserer Poisson-brudd ved ring-flom |
| Multiserver jobs (MSJ) | Teoretisk grunnlag for D-pri1 som Type 2-anrop |
| Team-basert kapasitet (Kim, Jouini) | Matematisk analog til makkerpar-prinsippet |
| Function differentiation | Støtter organisatoriske alternativer til bemanningsøkning |
| Kvalitetsreduksjon (Gustavsson, Leonardsen) | Tolkningsramme for modell-vs-virkelighet-gapet |

Sammen gir disse det teoretiske fundamentet for å formulere 110-kapasitetsproblemet som en multiserver-job-modell med ankomstkonflikt-metrikk, operasjonalisert gjennom op-binder-semantikk (kap 6.4).

---

*Kap 3 — Versjon 1.2 | Sist oppdatert: 2026-05-13 (språkrevisjon, restaurering)* 