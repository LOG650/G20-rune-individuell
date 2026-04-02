# 2. Litteratur

## 2.1 Søkestrategi

Litteratursøket er gjennomført i to runder. Første runde fulgte prosjektets opprinnelige problemstilling om Erlang-C-basert kapasitetsanalyse. Andre runde ble gjennomført etter at den metodiske tilnærmingen dreide mot prosedyrbasert ankomstkonfliktmodellering (se avsnitt 6.1), og rettet søket mot team-basert kapasitet, prosedyrkonformitet og degradert-modus-operasjoner i sikkerhets-kritiske systemer.

**Databaser:** Google Scholar, Scopus, Web of Science, PubMed, INFORMS PubsOnline, ScienceDirect, ProjectEuclid. Grå litteratur hentet fra DSB, NENA, APCO, Vera Institute og Lund University-arkiv.

**Søkeord — metodisk kjerne:**
`Erlang-C`, `M/M/c queue`, `call center capacity`, `staffing time-varying demand`, `queueing theory emergency services`, `Erlang-A`, `impatient customers`

**Søkeord — nødmeldesentral og dispatch:**
`emergency dispatch staffing`, `public safety answering point`, `PSAP capacity`, `emergency call center`, `fire dispatch`, `concurrent incidents`, `simultaneous incidents`

**Søkeord — team og prosedyr:**
`team-based call center`, `dual dispatch`, `paired dispatcher`, `cooperative servers`, `SOP compliance`, `degraded mode operations`, `cognitive load dispatcher`

**Søkeord — norsk/nordisk:**
`nødmeldesentral`, `110-sentral bemanning`, `AMK dimensjonering`, `Nordic fire rescue`, `SOS Alarm capacity`

| Database | Primære søkestrenger | Relevante treff | Inkludert |
|---|---|---|---|
| Google Scholar | Erlang-C + emergency dispatch | ~340 | 12 |
| Scopus | PSAP staffing + queueing | ~180 | 8 |
| INFORMS PubsOnline | M/M/c + call center | ~90 | 9 |
| Web of Science | team-based dispatch + cognitive load | ~60 | 4 |
| DSB / regjeringen.no | 110-sentral + dimensjonering | Målrettet søk | 7 |
| NENA / APCO | PSAP staffing guidelines | Målrettet søk | 3 |
| Lund University / NordForsk | Nordic fire rescue | Målrettet søk | 2 |

**Inklusjonskriterier:** Fagfellevurderte artikler og avhandlinger med metodisk relevans for kapasitetsmodellering av flerserer-systemer; empiriske studier fra nødmeldesentraler; norsk/nordisk regulering og offentlig dokumentasjon med direkte relevans for 110-sentraler.

**Eksklusjonskriterier:** Rene simuleringsmodeller uten analytisk grunnlag; studier utelukkende om ressursdisponering i felt (ikke sentralnivå); bransjeblogger uten fagfellevurdering.

---

## 2.2 Erlang-C og køteoretisk kapasitetsplanlegging

Erlang-C (M/M/c)-modellen er det dominerende analytiske verktøyet for kapasitetsplanlegging i flerserer-servicesystemer med kø. Gans et al. (2003) gir en bredt sitert oversikt over modellens anvendelse i call-center-kontekst og knytter den til service level-mål som P(W > t). Modellen hviler på tre forutsetninger: Poisson-fordelte ankomster (rate λ), eksponentielle servicetider (rate μ) og c parallelle, uavhengige servere. For stabilt system kreves ρ = λ/(c·μ) < 1.

Halfin og Whitt (1981) etablerte det teoretiske grunnlaget for «square-root staffing» — QED-regimet (Quality-and-Efficiency-Driven) — der den optimale bemanningsbufferen over minimumskapasiteten vokser med √A, der A = λ/μ er tilbudt trafikk i Erlang. Dette resultatet er sentralt for å forstå den ikke-lineære sammenhengen mellom belastning og nødvendig kapasitet.

Garnett et al. (2002) og Mandelbaum og Zeltyn (2005) videreutviklet modellen til Erlang-A (M/M/c+M), der kunder forlater systemet dersom ventetiden overstiger en tålmodighetterskel. For 110-sentraler er «frafall» operasjonelt relevant: anrop som overføres til nabosentral Agder representerer nettopp dette. Erlang-A gir dermed et mer realistisk øvre tak på systembelastningen enn Erlang-C, som antar ubegrenset tålmodighet.

Tidsavhengig etterspørsel utfordrer stasjonæritetsforutsetningen i klassisk Erlang-C. Green et al. (2007), Feldman et al. (2008) og Whitt (1996) utviklet ulike tilnærminger for å håndtere tidsvarierende ankomstrater: fra periode-segmentert statisk analyse til mer dynamiske approksimeringer. Stolletz (2008) foreslår en «stationary backlog-carryover»-metode for ikke-stasjonære M(t)/M(t)/c(t)-systemer. For 110-sentraler er dette relevant fordi ankomstraten λ varierer systematisk mellom skiftperioder og mellom hverdager og helger.

Koole og Mandelbaum (2002) gir en tilgjengelig introduksjon til modellvalg — Erlang-C, Erlang-A, nettverk av køer og simulering — og diskuterer under hvilke betingelser M/M/c er tilstrekkelig. De konkluderer med at Erlang-C er en god approksimering ved lav til moderat belastning, men systematisk undervurderer kapasitetsbehovet ved høy utnyttelsesgrad eller kompleks hendelsesstruktur.

Shen og Huang (2008) og Ibrahim et al. (2016) adresserer prognose av ankomstrater fra historiske data, herunder testing av Poisson-forutsetningen. Matteson et al. (2011) anvender disse metodene spesifikt på nødmeldetjeneste (EMS), og viser at ankomster i nødmeldesentraler typisk er Poisson-approksimerte innen korte tidsvindu, men viser overdispersjon på tvers av dager — noe som skyldes ukes- og sesongvariasjoner.

---

## 2.3 Nødmeldesentraler — kapasitet og dimensjonering

Forskning spesifikt på kapasitetsplanlegging i brann- og redningsnødmeldesentraler er begrenset. Det meste av empirisk call-center-forskning er gjennomført i kommersielle eller helserelaterte kontekster. Gustavsson (2018) og L'Ecuyer et al. (2018) er blant de få som anvender stokastiske modeller direkte på en nordisk nødmeldesentral (SOS Alarm Sverige). L'Ecuyer et al. modellerer eksplisitt «bursts» — korte, intense ankomsttopper utløst av enkelthendelser — og viser at disse bryter Poisson-uavhengighetsforutsetningen lokalt. Metodikken er direkte relevant for ring-flom-sensitivitetsanalysen i dette prosjektet.

Dwars (2013) gjennomfører kapasitetsplanlegging for en nederlandsk nødmeldesentral og strukturerer analysen rundt service level-definisjoner, sensitivitetsanalyse og sammenligning av modellalternativer. Metodisk design er nært beslektet med dette prosjektets tilnærming.

van Buuren et al. (2017) sammenligner to organisasjonsmodeller for EMS-sentraler — dedikert call taker kontra generalist — og finner at funksjonsatskillelse reduserer kapasitetskravet ved høy belastning. Analogien til 110-sentralenes VL-rolle og operatørroller er direkte.

Chelst og Barlach (1981) og Larson (1974) utviklet modeller for multi-enhetsdispatch i beredskapsoperative systemer, der én hendelse aktiverer flere ressurser simultant. Disse hyperkube-modellene adresserer en kapasitetsdimensjon Erlang-C ikke fanger: at én hendelse binder kapasitet på tvers av servere, ikke bare én server per anrop. Dette er forløperen til den prosedyrbaserte modellens logikk.

Mukhopadhyay et al. (2022) gir en bred review av prediksjon, ressursallokering og dispatch-modeller i beredskapsmanagement. Konklusjonen er at analytiske kømodeller (Erlang-C og varianter) er veletablert for anropsmottak, men at koordineringsarbeidet etter anropsmottak — som i 110-kontekst inkluderer utalarmering, samband og oppdragsoppfølging — i liten grad er modellert innen samme rammeverk.

Internasjonale standarder for nødsentralbemanning (NENA, 2003; NENA, 2020) opererer med eksplisitte service level-mål: 90 % av anrop besvart innen 15 sekunder, 95 % innen 20 sekunder. Disse er strengere enn norsk praksis og illustrerer bredden i hva som anses som akseptabel svartid internasjonalt. Vera Institute (2019) dokumenterer den fulle «call processing chain» fra mottak til ressursutsendelse og viser at Erlang-C kun adresserer den første lenken i kjeden.

---

## 2.4 Team-basert kapasitet, prosedyrkonformitet og kognitiv belastning

Jouini et al. (2008) analyserer team-baserte call-center-organisasjoner der to agenter samarbeider om oppgaver, og finner at teamorganisering øker kapasitetsutnyttelsen ved moderat belastning men skaper sårbarhet ved høy belastning. Resultatet speiler 110-sentralenes makkerpar-logikk: normal drift (RØD+GUL) er effektiv, men binder kapasitet ved simultane hendelser.

Kim et al. (2008) modellerer flerserer-systemer med servesamarbeid og viser at effektiv kapasitet avhenger av graden av parallell binding — der to servere er nødvendig per kunde, halveres reell kapasitet sammenlignet med standard M/M/c. Dette er det nærmeste matematiske analogon til makkerpar-prinsippet i 110-drift.

Wallace og Whitt (2005) utvikler bemanningsalgoritmer for kompetansebasert routing (skill-based routing), der ulike operatørtyper med ulik kompetanse betjener ulike kundegrupper. Analogien til 110-sentralenes rolledifferensiering (operatør vs. vaktleder) er metodisk relevant.

Normark (2002) gjennomfører en kvalitativ studie av koordineringsarbeid ved SOS Alarm (Sverige) og dokumenterer at operatørenes faktiske arbeidsmønster avviker vesentlig fra det Erlang-C-modellen forutsetter: teknologiartefakter, parallell oppmerksomhet og koordineringsprotokoller binder kapasitet på måter modellen ikke fanger. Studien er den eneste nordiske empiriske analysen av operativt arbeid i en nødsentralkontekst.

Al-Sarhani m.fl. (2025) studerer kognitiv belastning hos nødsentraloperatører og finner at simultane hendelser øker feilraten signifikant. Dette er relevant for diskusjonen av kapasitetsdegrasjon: «etter beste evne»-modus er ikke bare en teknisk kapasitetsbegrensning, men medfører økt kognitiv belastning og redusert beslutningskvalitet.

APCO International (2005) dokumenterer bemanningspraksis og rekrutteringsutfordringer i amerikanske PSAP-er gjennom Project RETAINS og gir empiriske benchmarks for turnover-rater og bemanningsnivåer.

---

## 2.5 Nordisk og norsk nødmeldeforskning

Norsk- og nordiskspesifikk forskning på nødmeldesentralenes kapasitet er svært begrenset. Ellensen et al. (2023) undersøker svenske nødmeldesentralers evne til å besvare medisinske nødanrop og finner systematiske kapasitetsgap i perioder med høy belastning — et funn som direkte støtter prosjektets hypotese om at gjennomsnittlig lavt volum skjuler reelle kapasitetsproblemer ved belastningstopper.

Leonardsen m.fl. (2019) gjennomfører en kvalitativ studie av norske AMK-operatørers arbeidsforhold og identifiserer belastningsfaktorer som ikke fanges av tekniske kapasitetsmål: mellommenneskelig koordinering, prioriteringsstress og rollen til den uformelle arbeidsorganiseringen. Funnene er analytisk overførbare til 110-kontekst.

Rehn m.fl. (2021) analyserer dispatch-nøyaktighet for legebemannede ambulanser i Sør-Øst Norge og viser at disponeringsvalg er systematisk påvirket av kapasitetstilstand i sentralen — et eksempel på at kapasitetsbegrensning har konsekvenser for beslutningskvalitet utover ren anropsrespons.

McNamee m.fl. (2025) kartlegger norske og nordiske brann- og redningsvesenets kapasitetsutfordringer i FIRE21-prosjektet og identifiserer dimensjonering og bemanning som sentrale problemstillinger på tvers av de nordiske landene.

Norsk regulering belyses gjennom brann- og redningsvesenforskriften (2021), dimensjoneringsforskriften (2023), og stortingsmeldingene St.meld. nr. 41 (2001) og Meld. St. 16 (2024). Sistnevnte kobler eksplisitt ROS-analyse til bemanningskrav for nødmeldetjenesten og legitimerer prosjektets kvantitative tilnærming som svar på et dokumentert styringsbehov. RISE Fire Research (2017) gir metodikk og parametre fra empirisk dimensjoneringsanalyse for norsk brannvesen — nærmeste metodiske forgjenger for dette prosjektets tilnærming.

---

## 2.6 Oppsummering og identifiserte kunnskapsgap

Litteraturgjennomgangen identifiserer fem gap som dette prosjektet adresserer:

**Gap 1 — Prosedyrkonformitet som kapasitetsmetrikk.**
Eksisterende litteratur måler kapasitet som sannsynlighet for kø eller ventetid (Erlang-C) eller som andel anrop besvart innen t sekunder. Ingen av de gjennomgåtte studiene bruker prosedyrkonformitet ved ankomst — det vil si sannsynligheten for at et anrop ankommer i en tilstand der driftsstandarden (makkerpar) kan opprettholdes — som primær kapasitetsmetrikk.

**Gap 2 — To-server-per-kunde som driftsstandard.**
Standard M/M/c-modellen forutsetter én server per kunde. Kim et al. (2008) og Jouini et al. (2008) nærmer seg team-basert kapasitet, men ingen studier modellerer et system der to servere er prosedyrens normkrav per hendelse — og der brudd på dette kravet er det operative kapasitetsproblemet som skal kvantifiseres.

**Gap 3 — Kapasitetsbinding utover samtaletid.**
Erlang-C-modellen forutsetter at servere er ledige igjen umiddelbart etter samtalens slutt. I 110-kontekst er operatøren bundet i koordineringsfasen (GUL-funksjon) etter at samtalen er avsluttet. «After-call work» er diskutert i kommersiell call-center-litteratur (Gans et al., 2003), men er ikke modellert empirisk i nødmeldesentralkontekst.

**Gap 4 — Bemanningsdifferensiering uten empirisk beredskapsgrunnlag.**
Ingen identifiserte studier dokumenterer og kvantifiserer helge/hverdag-asymmetrier i bemanning relativt til beredskapsbelastning i nødmeldesentraler. Den praksis dette prosjektet identifiserer — at bemanningsreduksjon på helg er begrunnet i lavere servicetelefon-volum, ikke i lavere beredskapsbelastning — er ikke belyst i litteraturen.

**Gap 5 — Norsk 110-forskning.**
Det finnes ingen publiserte, kvantitative kapasitetsanalyser av norske 110-sentraler. Eksisterende dimensjoneringsgrunnlag baseres utelukkende på lokale, kvalitative ROS-analyser. Dette prosjektet er etter det vi kan fastslå det første som anvender historiske hendelsesdata og kvantitativ modellering for å vurdere om faktisk bemanning ved en norsk 110-sentral er tilstrekkelig.

---

*Kap 2 — Versjon 1.0 | Sist oppdatert: 2026-03-29*
*Neste: Kapitlene 3 (Teori), 4 (Case) og 6 (Modell) suppleres basert på samme kildegrunnlag.*
