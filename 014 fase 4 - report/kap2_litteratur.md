# 2. Litteratur

## 2.1 Søkestrategi

Litteratursøket er gjennomført i to runder. Første runde fulgte prosjektets opprinnelige problemstilling om Erlang-C-basert kapasitetsanalyse. Andre runde ble gjennomført etter at den metodiske tilnærmingen dreide mot prosedyrbasert ankomstkonfliktmodellering (se avsnitt 6.1), og rettet søket mot team-basert kapasitet, prosedyrkonformitet og degradert-modus-operasjoner i sikkerhets-kritiske systemer.

**Databaser:** Google Scholar, Scopus, Web of Science, PubMed, INFORMS PubsOnline, ScienceDirect, ProjectEuclid. Grå litteratur hentet fra DSB, NENA, APCO, Vera Institute og Lund University-arkiv.

**Søkeord, metodisk kjerne:**
`Erlang-C`, `M/M/c queue`, `call center capacity`, `staffing time-varying demand`, `queueing theory emergency services`, `Erlang-A`, `impatient customers`

**Søkeord, nødmeldesentral og dispatch:**
`emergency dispatch staffing`, `public safety answering point`, `PSAP capacity`, `emergency call center`, `fire dispatch`, `concurrent incidents`, `simultaneous incidents`

**Søkeord, team og prosedyr:**
`team-based call center`, `dual dispatch`, `paired dispatcher`, `cooperative servers`, `SOP compliance`, `degraded mode operations`, `cognitive load dispatcher`

**Søkeord, norsk/nordisk:**
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

**Inklusjonskriterier:** Fagfellevurderte artikler og avhandlinger med metodisk relevans for kapasitetsmodellering av flerserver-systemer; empiriske studier fra nødmeldesentraler; norsk/nordisk regulering og offentlig dokumentasjon med direkte relevans for 110-sentraler.

**Eksklusjonskriterier:** Rene simuleringsmodeller uten analytisk grunnlag; studier utelukkende om ressursdisponering i felt (ikke sentralnivå); bransjeblogger uten fagfellevurdering.

Av samlet ~670 målrettede treff er 45 inkludert som primær- eller støttekilder. Hovedfunnet på tvers av materialet er at Erlang-C og varianter dominerer call-center-litteraturen, mens nødmeldesentraler er svakt dekket, særlig i nordisk og norsk kontekst. Multiserver-job-rammeverket og prosedyrkonformitet som kapasitetsmetrikk er etablert teoretisk, men ikke tidligere anvendt på 110-data. De tematiske avsnittene under (2.2 til 2.5) gjennomgår funnene; avsnitt 2.6 oppsummerer kunnskapsgapene som denne studien adresserer.

---

## 2.2 Erlang-C og køteoretisk kapasitetsplanlegging

Dette avsnittet gjennomgår Erlang-C-tradisjonen fordi den er metodisk baseline for studien (kap 6.3) og fordi dens forutsetninger danner kontrasten som motiverer modellutviklingen i kap 3.6 og 3.7. Tre antagelser i Erlang-C bryter sammen for 110-konteksten og vurderes derfor særskilt nedenfor: stasjonær Poisson-ankomst, én-til-én betjening, og at servicetid utgjør hele kapasitetsbindingen. Litteraturen som behandler disse bruddene direkte (Halfin & Whitt 1981, Chelst & Barlach 1981, Harchol-Balter 2022, Gustavsson 2018) er kanoniske kilder for denne studiens modellvalg. Øvrige kilder er bakgrunnsstøtte.

Erlang-C (M/M/c)-modellen er det dominerende analytiske verktøyet for kapasitetsplanlegging i flerserver-servicesystemer med kø. Gans et al. (2003) gir en bredt sitert oversikt over modellens anvendelse i call-center-kontekst og knytter den til service level-mål som P(W > t). Modellen hviler på tre forutsetninger: Poisson-fordelte ankomster (rate λ), eksponentielle servicetider (rate μ) og c parallelle, uavhengige servere. For stabilt system kreves ρ = λ/(c·μ) < 1.

Halfin og Whitt (1981) etablerte det teoretiske grunnlaget for «square-root staffing», QED-regimet (Quality-and-Efficiency-Driven), der den optimale bemanningsbufferen over minimumskapasiteten vokser med √A, der A = λ/μ er tilbudt trafikk i Erlang. Dette resultatet er sentralt for å forstå den ikke-lineære sammenhengen mellom belastning og nødvendig kapasitet.

Garnett et al. (2002) og Zeltyn og Mandelbaum (2005) videreutviklet modellen til Erlang-A (M/M/c+M), der kunder forlater systemet dersom ventetiden overstiger en tålmodighetterskel. For 110-sentraler er «frafall» operasjonelt relevant: anrop som overføres til nabosentral Agder representerer nettopp dette. Erlang-A gir dermed et mer realistisk øvre tak på systembelastningen enn Erlang-C, som antar ubegrenset tålmodighet.

Tidsavhengig etterspørsel utfordrer stasjonæritetsforutsetningen i klassisk Erlang-C. Green et al. (2007), Feldman et al. (2008) og Jennings et al. (1996) utviklet ulike tilnærminger for å håndtere tidsvarierende ankomstrater: fra periode-segmentert statisk analyse til mer dynamiske approksimeringer. Stolletz (2008) foreslår en «stationary backlog-carryover»-metode for ikke-stasjonære M(t)/M(t)/c(t)-systemer. For 110-sentraler er dette relevant fordi ankomstraten λ varierer systematisk mellom skiftperioder og mellom hverdager og helger.

Koole og Mandelbaum (2002) gir en tilgjengelig introduksjon til modellvalg (Erlang-C, Erlang-A, nettverk av køer og simulering) og diskuterer under hvilke betingelser M/M/c er tilstrekkelig. De konkluderer med at Erlang-C er en god approksimering ved lav til moderat belastning, men systematisk undervurderer kapasitetsbehovet ved høy utnyttelsesgrad eller kompleks hendelsesstruktur.

Shen og Huang (2008) og Ibrahim et al. (2016) adresserer prognose av ankomstrater fra historiske data, herunder testing av Poisson-forutsetningen. Matteson et al. (2011) anvender disse metodene spesifikt på nødmeldetjeneste (EMS), og viser at ankomster i nødmeldesentraler typisk er Poisson-approksimerte innen korte tidsvindu, men viser overdispersjon på tvers av dager, noe som skyldes ukes- og sesongvariasjoner.

**Hva Erlang-C-tradisjonen ikke fanger for 110-konteksten.** Litteraturen som er gjennomgått er sentral som metodisk referansepunkt, men har tre svakheter for makkerpar-prosedyre: (i) den behandler servere som uavhengige og likeverdige, ikke som rolledifferensierte par; (ii) den modellerer kapasitetsbinding som samtaletid, ikke som binding utover samtale; (iii) den forutsetter stasjonær Poisson, som brytes ved ring-flom. Av kildene over er **Halfin og Whitt (1981)** kanonisk for å forklare hvorfor små systemer opererer strukturelt med lav utnyttelse, et resultat som er sentralt for tolkningen av Erlang-C-paradokset i kap 8.1. Øvrige kilder gir bakgrunnsforståelse av rammeverket, men adresserer ikke makkerpar-problemet direkte. Det er behandlet i 2.3 og 2.4.

---

## 2.3 Nødmeldesentraler: kapasitet og dimensjonering

Dette avsnittet er sentralt for studiens metodevalg fordi det er her tradisjonen som *direkte* modellerer nødmeldesentral-spesifikke kapasitetsdynamikker etableres. To grupper litteratur er særlig relevante: (i) studier som anvender køteori på reelle nødmeldesentraler (Gustavsson 2018, Dwars 2013, Penverne et al. 2024), og (ii) multi-enhets-dispatchmodeller som fanger at én hendelse kan binde flere ressurser samtidig (Chelst & Barlach 1981, Larson 1974, Harchol-Balter 2022). **Chelst og Barlach (1981)** og **Harchol-Balter (2022)** er kanoniske for studiens modellvalg; de gir det formelle rammeverket for D-pri1 som makkerpar-bundet «Type 2»-anrop. **Gustavsson (2018)** er kanonisk for empirisk parallellitet: makkerpar/solo-tilpasningen modellen kvantifiserer er den samme operative dynamikken hun dokumenterte ved SOS Alarm.

Forskning spesifikt på kapasitetsplanlegging i brann- og redningsnødmeldesentraler er begrenset. Det meste av empirisk call-center-forskning er gjennomført i kommersielle eller helserelaterte kontekster. Gustavsson (2018) og L'Ecuyer et al. (2018) er blant de få som anvender stokastiske modeller direkte på en nordisk nødmeldesentral (SOS Alarm Sverige). L'Ecuyer et al. modellerer eksplisitt «bursts» (korte, intense ankomsttopper utløst av enkelthendelser) og viser at disse bryter Poisson-uavhengighetsforutsetningen lokalt. Metodikken er direkte relevant for ring-flom-sensitivitetsanalysen i dette prosjektet.

Dwars (2013) gjennomfører kapasitetsplanlegging for en nederlandsk nødmeldesentral og strukturerer analysen rundt service level-definisjoner, sensitivitetsanalyse og sammenligning av modellalternativer. Metodisk design er nært beslektet med dette prosjektets tilnærming.

Penverne et al. (2024) viser hvordan digital tvilling-simulering kan brukes til å vurdere organisering av respons på nødanrop, inkludert effekten av interconnection mellom sentraler sammenlignet med isolert drift og full virtualisering. Studien er relevant for diskusjonen av overløpsarkitektur mellom nabosentraler i kapittel 8.

van Buuren et al. (2017) sammenligner to organisasjonsmodeller for EMS-sentraler (dedikert call taker kontra generalist), og finner at funksjonsatskillelse reduserer kapasitetskravet ved høy belastning. Analogien til 110-sentralenes VL-rolle og operatørroller er direkte.

Chelst og Barlach (1981) og Larson (1974) utviklet modeller for multi-enhetsdispatch i beredskapsoperative systemer, der én hendelse aktiverer flere ressurser simultant. Disse hyperkube-modellene adresserer en kapasitetsdimensjon Erlang-C ikke fanger: at én hendelse binder kapasitet på tvers av servere, ikke bare én server per anrop. Brill og Green (1984) utvider dette med å vise at simultan flereenhets-betjening har vesentlig annen kapasitetsdynamikk enn én-enhetssystemer, og at klassiske køteoretiske resultater (som ρ < 1 for stabilitet) må justeres når servere må aktiveres parallelt. Harchol-Balter (2022) generaliserer rammeverket til multiserver-job-køer (MSJ) der jobber krever flere servere parallelt, og viser at klassiske bemanningsformler systematisk undervurderer kapasitetsbehovet for slike systemer. Disse bidragene utgjør den teoretiske forløperen til den prosedyrbaserte modellens op-binder-semantikk, der pri-1-hendelser krever to servere (makkerpar) mens ABA-utrykning krever én server serielt.

Mukhopadhyay et al. (2022) gir en bred review av prediksjon, ressursallokering og dispatch-modeller i beredskapsmanagement. Konklusjonen er at analytiske kømodeller (Erlang-C og varianter) er veletablert for anropsmottak, men at koordineringsarbeidet etter anropsmottak (som i 110-kontekst inkluderer utalarmering, samband og oppdragsoppfølging) i liten grad er modellert innen samme rammeverk.

Internasjonale standarder for nødsentralbemanning (NENA, 2003; NENA, 2020) opererer med eksplisitte service level-mål: 90 % av anrop besvart innen 15 sekunder, 95 % innen 20 sekunder. Disse er strengere enn norsk praksis og illustrerer bredden i hva som anses som akseptabel svartid internasjonalt. Vera Institute of Justice (2019) dokumenterer den fulle «call processing chain» fra mottak til ressursutsendelse og viser at Erlang-C kun adresserer den første lenken i kjeden.

**Bro til metodevalg.** Litteraturen i 2.3 etablerer to ting som er direkte forutsetninger for studiens modell: (i) at nødmeldesentraler skiller seg fra kommersielle call-sentre på en måte som krever utvidet rammeverk, særlig makkerpar og kapasitetsbinding utover samtaletid, og (ii) at multi-enhets-dispatchlitteraturen gir det formelle apparatet for å modellere dette. Gap 1 (prosedyrkonformitet som metrikk) og Gap 2 (D-pri1 som makkerpar-bundet jobb) i avsnitt 2.6 følger direkte fra denne gjennomgangen. Modellutformingen i kap 3.7 (op-binder-semantikk) er en konkret operasjonalisering av Chelst & Barlach (1981) og Harchol-Balter (2022) i 110-kontekst.

---

## 2.4 Team-basert kapasitet, prosedyrkonformitet og kognitiv belastning

Jouini et al. (2008) analyserer team-baserte call-center-organisasjoner der to agenter samarbeider om oppgaver, og finner at teamorganisering øker kapasitetsutnyttelsen ved moderat belastning men skaper sårbarhet ved høy belastning. Resultatet speiler 110-sentralenes makkerpar-logikk: normal drift (RØD+GUL) er effektiv, men binder kapasitet ved simultane hendelser. *Begrensning for 110:* Jouini modellerer kommersielle kundetjenester der team-organisering er valgfri; for 110 er makkerpar et prosedyrekrav, ikke et organisatorisk valg.

Kim et al. (2008) modellerer flerserver-systemer med serversamarbeid og viser at effektiv kapasitet avhenger av graden av parallell binding: der to servere er nødvendig per kunde, halveres reell kapasitet sammenlignet med standard M/M/c. Dette er det nærmeste matematiske analogon til makkerpar-prinsippet i 110-drift. *Begrensning:* Modellen antar homogen jobbsammensetning (alle kunder krever to servere); 110 har heterogen sammensetning der D-pri1 krever to og D-aba krever én.

Wallace og Whitt (2005) utvikler bemanningsalgoritmer for kompetansebasert routing (skill-based routing), der ulike operatørtyper med ulik kompetanse betjener ulike kundegrupper. Analogien til 110-sentralenes rolledifferensiering (operatør vs. vaktleder) er metodisk relevant. *Begrensning:* Skill-based routing forutsetter et stort antall agenter med ulik kompetanse; 110 har 2 til 4 agenter med tilnærmet samme kompetanse og én vaktleder, slik at hovedfordelen ved routing-algoritmen ikke realiseres.

Normark (2002) gjennomfører en kvalitativ studie av koordineringsarbeid ved SOS Alarm (Sverige) og dokumenterer at operatørenes faktiske arbeidsmønster avviker vesentlig fra det Erlang-C-modellen forutsetter: teknologiartefakter, parallell oppmerksomhet og koordineringsprotokoller binder kapasitet på måter modellen ikke fanger. Studien er den eneste nordiske empiriske analysen av operativt arbeid i en nødsentralkontekst og gir kvalitativt belegg for at op-binder-semantikken fanger en reell dynamikk. *Begrensning:* Kvalitativt design. Gir ikke kvantitative parametre direkte overførbare til modellen.

Al-Sarhani m.fl. (2025) studerer kognitiv belastning hos nødsentraloperatører og finner at simultane hendelser øker feilraten signifikant. Dette er relevant for diskusjonen av kapasitetsdegrasjon: «etter beste evne»-modus er ikke bare en teknisk kapasitetsbegrensning, men medfører økt kognitiv belastning og redusert beslutningskvalitet. *Begrensning:* Studien er fra Kuwait og bruker laboratoriebasert måling; overførbarhet til norsk operativ kontekst er ikke etablert.

APCO International (2005) dokumenterer bemanningspraksis og rekrutteringsutfordringer i amerikanske PSAP-er gjennom Project RETAINS og gir empiriske benchmarks for turnover-rater og bemanningsnivåer. *Begrensning:* Amerikansk PSAP-organisering skiller seg fra norsk 110-modell (kombinerte police/fire/EMS-dispatch vs. separate sentraler), og benchmarks må kontekstualiseres før de brukes direkte.

---

## 2.5 Nordisk og norsk nødmeldeforskning

Norsk- og nordiskspesifikk forskning på nødmeldesentralenes kapasitet er svært begrenset. Byrsell et al. (2023) undersøker svenske medisinske nødmeldesentralers evne til å besvare nødanrop og finner systematiske kapasitetsgap i perioder med høy belastning. Funnet støtter direkte prosjektets hypotese om at gjennomsnittlig lavt volum skjuler reelle kapasitetsproblemer ved belastningstopper. *Begrensning:* Medisinsk nødmeldetjeneste (AMK/SOS Alarm) skiller seg fra brann/redning (110) i organisering og oppdragstyper; analogien er konseptuelt, ikke parametrisk.

Leonardsen m.fl. (2019) gjennomfører en kvalitativ studie av norske AMK-operatørers arbeidsforhold og identifiserer belastningsfaktorer som ikke fanges av tekniske kapasitetsmål: mellommenneskelig koordinering, prioriteringsstress og rollen til den uformelle arbeidsorganiseringen. Funnene er analytisk overførbare til 110-kontekst. *Begrensning:* Kvalitativ. Gir ikke kvantitative parametre, men er sentral for fortolkningen i kap 8.2 (kvalitetsreduksjon som skjult buffer).

Samdal m.fl. (2021) analyserer dispatch-nøyaktighet for legebemannede ambulanser i Sør-Øst Norge og viser at disponeringsvalg er systematisk påvirket av kapasitetstilstand i sentralen. Funnet illustrerer at kapasitetsbegrensning har konsekvenser for beslutningskvalitet utover ren anropsrespons. *Begrensning:* Studien måler dispatch-nøyaktighet i ambulansetjeneste, ikke i brann-/redningssentral; metoden er ikke direkte importerbar, men funnet om kapasitetsdrevet beslutningskvalitet er konseptuelt relevant.

McNamee m.fl. (2025) kartlegger norske og nordiske brann- og redningsvesenets kapasitetsutfordringer i FIRE21-prosjektet og identifiserer dimensjonering og bemanning som sentrale problemstillinger på tvers av de nordiske landene. *Begrensning:* Fokus på utrykningsleddet (mannskap og kjøretøy), ikke sentraloperatørene. Gir kontekst, men ikke direkte anvendbare parametre for 110-modellen.

Norsk regulering belyses gjennom brann- og redningsvesenforskriften (2021) og stortingsmeldingene St.meld. nr. 41 (2000-2001) og Meld. St. 16 (2023-2024). Sistnevnte kobler eksplisitt ROS-analyse til bemanningskrav for nødmeldetjenesten og legitimerer prosjektets kvantitative tilnærming som svar på et dokumentert styringsbehov. Interdepartemental arbeidsgruppe (2009) er en sentral policy-anbefaling som drøfter felles organisering, svartidskrav og dimensjoneringsprinsipper for nødmeldetjenesten. Arbeidsgruppen erkjenner eksplisitt at det ikke finnes vitenskapelig grunnlag for gjeldende terskelverdier. Dette gapet motiverer prosjektets kvantitative ambisjon. Storesund m.fl. (2017), utført ved RISE Fire Research på oppdrag fra DSB, gir metodikk og parametre fra empirisk dimensjoneringsanalyse for norsk brannvesen, inkludert multivariat regresjon på 110-sentralenes alarmbehandlingstid. Studien er nærmeste metodiske forgjenger for dette prosjektets tilnærming.

---

## 2.6 Oppsummering og identifiserte kunnskapsgap

Litteraturgjennomgangen identifiserer fem gap som dette prosjektet adresserer:

**Gap 1: Prosedyrkonformitet som kapasitetsmetrikk.**
Eksisterende litteratur måler kapasitet som sannsynlighet for kø eller ventetid (Erlang-C), eller som andel anrop besvart innen t sekunder. Ingen av de gjennomgåtte studiene bruker prosedyrkonformitet ved ankomst som primær kapasitetsmetrikk. Med dette menes sannsynligheten for at et anrop ankommer i en tilstand der driftsstandarden (makkerpar) kan opprettholdes.

**Gap 2: Makkerpar-bundet håndtering (D-pri1) som driftsstandard.**
Standard M/M/c-modellen forutsetter én server per kunde. Kim et al. (2008) og Jouini et al. (2008) nærmer seg team-basert kapasitet, og Harchol-Balter (2022) formaliserer multiserver-jobs (MSJ) som teoretisk rammeverk. Etter litteratursøket i denne studien er det ikke funnet publiserte arbeider som modellerer et nødmeldesystem der pri-1-utrykninger (D-pri1) krever makkerpar mens ABA-utrykninger (D-aba) håndteres serielt, og der brudd på makkerpar-kravet er det operative kapasitetsproblemet som skal kvantifiseres. Den prosedyrbaserte modellen i denne studien fremstår dermed som en ny empirisk anvendelse av en op-binder-formalisering (jf. kap 3.7) på en nordisk 110-sentral.

**Gap 3: Kapasitetsbinding utover samtaletid.**
Erlang-C-modellen forutsetter at servere er ledige igjen umiddelbart etter samtalens slutt. I 110-kontekst er operatøren bundet i koordineringsfasen (GUL-funksjon) etter at samtalen er avsluttet. «After-call work» er diskutert i kommersiell call-center-litteratur (Gans et al., 2003), men er ikke modellert empirisk i nødmeldesentralkontekst.

**Gap 4: Bemanningsdifferensiering uten empirisk beredskapsgrunnlag.**
Ingen identifiserte studier dokumenterer og kvantifiserer helge/hverdag-asymmetrier i bemanning relativt til beredskapsbelastning i nødmeldesentraler. Den praksis dette prosjektet identifiserer, at bemanningsreduksjon på helg er begrunnet i lavere servicetelefon-volum og ikke i lavere beredskapsbelastning, er ikke belyst i litteraturen.

**Gap 5: Norsk 110-forskning og felles klassifisering.**
Etter litteratursøket i denne studien er det ikke funnet publiserte, kvantitative kapasitetsanalyser av norske 110-sentraler. Eksisterende dimensjoneringsgrunnlag baseres på lokale, kvalitative ROS-analyser. Den interdepartementale arbeidsgruppen (2009) anbefalte felles dimensjoneringsstandarder for nødmeldetjenesten, men bemerket samtidig at det «ikke finnes vitenskapelig grunnlag for de valgte terskelverdiene» for svartid (jf. avsnitt 2.5). Dette prosjektet fremstår dermed som en av de første kvantitative analysene av en norsk 110-sentrals bemanning basert på historiske hendelsesdata. Studien foreslår parallelt en V3-klassifiseringsregel (D-pri1, D-aba, L-aba med Kilde=Alarm-krav) som forutsetning for sammenlignbar benchmarking på tvers av sentraler.

### Studiens posisjonering i forhold til de fem gapene

Denne studien fyller særlig **Gap 1, 2 og 5**. Prosedyrkonformitet ved ankomst (Gap 1) operasjonaliseres som målbar metrikk via op-binder-semantikk. Op-binder-semantikken adresserer Gap 2: D-pri1 med makkerpar-krav modelleres som direkte teoretisk parallell til multiserver-jobs. Modellen anvendes på norske 110-data for første gang (Gap 5). Studien adresserer også Gap 3 (kapasitetsbinding utover samtaletid via observerte tidsstempler for første ressurs fremme) og Gap 4 (helg/hverdag-asymmetri kvantifisert mot beredskapsbelastning, ikke bare totalvolum). Metodisk originalitet ligger i operasjonaliseringen av prosedyrekrav som målbar kapasitetsmetrikk, ikke i utvikling av ny køteori.

---

*Kap 2 · Versjon 1.3 | Sist oppdatert: 2026-05-13 (kritisk kildevurdering, bro til metodevalg, restaurering av 2.6)*