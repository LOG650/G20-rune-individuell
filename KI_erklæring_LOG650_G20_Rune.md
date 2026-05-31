# Bruk av kunstig intelligens, LOG650 G20 Individuell

**Student:** Rune Grødem
**Emne:** LOG650, Logistikk og kunstig intelligens, Høgskolen i Molde, Vår 2026
**Oppgavetittel:** Kapasitetsstyring og bemanningsdimensjonering ved norske 110-sentraler
**Dokument:** Løpende KI-erklæring og brukslogg
**Sist oppdatert:** 2026-05-31

> **Bruk:** Dette dokumentet tjener to formål:
> 1. Grunnlag for seksjonen «Bruk av kunstig intelligens» i rapporten (seksjon 5.7.1 og Vedlegg D)
> 2. Løpende logg som oppdateres gjennom hele prosjektet, én linje per brukshendelse
>
> **Oppdateringsrutine:** Legg til en ny rad i loggene nedenfor etter hver session der KI-verktøy brukes. Dato, verktøy, formål og hva som faktisk ble tatt inn i arbeidet.

---

## Del 1: Bruk av kunstig intelligens (rapporttekst)

*Denne seksjonen kopieres/tilpasses til rapporten som seksjon «Bruk av kunstig intelligens» (jf. HiMolde retningslinjer for KI på hjemmeeksamen).*

### KI-verktøy benyttet i prosjektet

I dette prosjektet er KI-verktøy benyttet aktivt og i betydelig omfang gjennom hele arbeidsprosessen, inkludert til å utforme store deler av rapportteksten. Dette er bevisst og i tråd med føringene for emnet LOG650 «Logistikk og kunstig intelligens», der veileder har instruert at KI skal benyttes til tekstutforming. Følgende verktøy er brukt:

| Verktøy | Versjon/plattform | Primært bruksområde |
|---|---|---|
| Claude Code (Anthropic) | Sonnet 4.6 og senere Opus 4.8, VSCode-extension og terminal | Utkast til rapporttekst, koding og dataanalyse, figurgenerering, rapportstruktur, litteraturverifisering, konsistens- og kvalitetssikring |
| Codex (OpenAI) | Skrivebeskyttet, terminal | Uavhengig kryss-sjekk av analysekoden og at rapportens tall stemmer med kildedata, kjørt uavhengig av Claude Code |
| ChatGPT (OpenAI) | GPT-4, chat.openai.com | Litteratursøk, metodiske innspill, Gantt-tilbakemeldinger |

### Formål og bruksbeskrivelse

**Claude Code** er benyttet som en interaktiv skrive-, kode- og analyseassistent gjennom hele prosjektet. Konkrete bruksområder:

- **Rapporttekst:** Store deler av brødteksten i rapportkapitlene er utkast-generert av Claude Code på mine detaljerte instruksjoner, og deretter gjennomgått, korrigert, omarbeidet og godkjent av meg. Faglig innhold, struktur og argumentasjon er styrt av meg; KI har formulert utkast som jeg har kvalitetssikret og står faglig ansvarlig for.
- **Prosjektstrukturering:** Utforming og revisjon av prosjektstyringsplanen (v1.0 til v1.5), inkludert WBS, kritisk sti og Gantt-diagram (MS Project XML). Alle strukturelle beslutninger, hvilke leveranser som inkluderes, rekkefølge og tidsestimater, er tatt av undertegnede.
- **Koding og automatisering:** Generering av Python-scripts for filmanipulering (oppretting av Excel-litteraturliste, oppdatering av markdown-filer, konvertering til XML). All kode er gjennomgått og testet. Tolkninger av resultater og analytiske beslutninger er mine egne.
- **Figurer og tabeller:** Alle figurer i rapporten er generert av Python-kode (matplotlib) skrevet med Claude Code, basert på prosjektets egne data. Det er ikke brukt KI-bildegenerering. Jeg har spesifisert innhold, utvalg og utforming for hver figur, verifisert at de samsvarer med dataene, og står ansvarlig for tolkning og presentasjon. Tabeller er produsert fra de samme deterministiske skriptene eller skrevet manuelt.
- **Litteratursøk og kildeverifisering:** Etter at ChatGPT foreslo referanser, ble disse manuelt verifisert av Claude Code via websøk. Dette avdekket bl.a. feil årstall (Ibrahim et al. 2016, ikke 2015) og manglende undertittel (Vera Institute 2019). Endelig kildeutvalg er mitt eget.
- **Rapportskall:** Generering av strukturert rapportskall (v0.1 til v0.2) basert på HiMolde-mal og prosjektets problemstilling. Innhold i alle `[SKRIVES ETTER ...]`-seksjoner produseres av undertegnede selv etter datainnsamling og analyse.
- **Gjennomgang og kvalitetssikring:** KI-verktøyet er brukt til å identifisere inkonsistenser, feil og mangler i egne dokumenter. Alle endringer er vurdert og godkjent av undertegnede.

**ChatGPT** er benyttet som diskusjonspartner og idégenerator:

- **Litteratursøk:** Generert forslag til referanser og søkeord. Alle forslag er verifisert mot akademiske databaser og originaltekster før inkludering i litteraturlisten. ChatGPT er ikke oppført som kilde i referanselisten.
- **Metodiske innspill:** Forslag til forbedringer av Gantt-plan (to runder) og metodisk rammeverk for prosjektet. Forslagene er kritisk vurdert, noen akseptert, andre avvist, og alle endringer er undertegnedes eget valg.
- **Modellgjennomgang:** Presentasjon av utvidede modeller utover Erlang-C (Erlang-A, multi-skill queueing, robust optimering). Gjennomgangen er vurdert for scope-relevans, og kun et begrenset utvalg er tatt inn i teorikapittelet og litteraturlisten.

### Hvordan arbeidet er fordelt mellom KI og forfatter

For å være transparent om den faktiske arbeidsmåten:

- **Store deler av rapportteksten og all analysekode er utkast-generert av KI** (primært Claude Code) på mine detaljerte instruksjoner. Jeg har deretter lest gjennom, korrigert, omarbeidet, verifisert og godkjent alt innhold. Ingenting er tatt inn i rapporten uten denne gjennomgangen.
- **Det faglige grunnlaget og alle beslutninger er mine:** problemstilling, forskningsspørsmål, operativ domenekunnskap fra eget arbeid ved 110 Sør-Vest (makkerpar-drift, vaktleder-rolle, solo-drift, overløpsregler), datatilgang, modellvalg, klassifiseringsregler og tolkning av funn. KI har formalisert, implementert og formulert; jeg har styrt, vurdert og avgjort. Det er mitt kunnskapsnivå og min faglige retning som har formet sluttproduktet.
- **Modellresultatene er ikke KI-genererte.** Alle tall i rapporten produseres av deterministiske Python-skript kjørt på registerdata med faste seed, og er reproduserbare uavhengig av KI.
- **Codex er brukt til uavhengig kontroll:** analysekoden ble kjørt skrivebeskyttet for å bekrefte at rapportens tall stemmer med kildedata, uavhengig av Claude Code.
- **Kildeintegritet:** alle referanser er verifisert mot originalkildene, og KI-foreslåtte kilder er aldri tatt inn uten slik verifisering. KI er ikke ført opp som kilde i referanselisten.

Denne bruken er mer omfattende enn den generiske HiMolde-malen for KI-erklæring forutsetter. Det er bevisst og avklart: LOG650 «Logistikk og kunstig intelligens» er et emne der veileder eksplisitt har instruert at KI skal benyttes til å utforme tekst. Jeg står likevel fullt faglig ansvarlig for alt innhold i rapporten, og innholdet gjenspeiler min egen kunnskap, mine vurderinger og mine beslutninger.

### Refleksjon, hvordan KI påvirket arbeidsprosessen

Bruken av Claude Code som iterativ assistent har vært gjennomgripende. Verktøyet har generert utkast til både rapporttekst og analysekode, effektivisert tekniske oppgaver (filhåndtering, versjonskontroll, figurgenerering) og fungert som en «rødflagg»-mekanisme som fanget feil og inkonsistenser (f.eks. feil årstall i referanser, inkonsistente avhengigheter i Gantt, tallavvik mellom kapitler) som ellers kunne passert uoppdaget. Det har frigjort tid til faglig vurdering, men ikke erstattet den: hver formulering, hvert tall og hver tolkning er prøvd mot min egen domenekunnskap før den er beholdt.

ChatGPT har vært nyttig for å få oversikt over et bredt metodisk landskap raskt, men krevde kritisk filtrering, særlig av referanseforslag og metodiske anbefalinger som lå utenfor prosjektets scope.

Alle vesentlige faglige beslutninger, problemstilling, modellvalg, analytisk tilnærming, tolkning, er tatt av undertegnede basert på faglig kunnskap, veileder-input og primærlitteratur.

---

## Del 2: Løpende brukslogg

*Oppdateres etter hver session. Tilstrekkelig detaljert til å dokumentere bruksmønster ved forespørsel.*

### Claude Code (Anthropic, claude-sonnet-4-6)

| Dato | Fase | Formål | Output / hva ble tatt inn | Undertegnedes bidrag |
|---|---|---|---|---|
| 2026-02-XX | Fase 1 | Prosjektforslag, strukturering av problemstilling og metode | Utkast til problemstilling og RQ-er | Valg av problemstilling, tilpasning til 110-kontekst |
| 2026-03-01 til 06 | Fase 2 | Prosjektstyringsplan v1.0 til v1.2: WBS, Gantt-tabell, kritisk sti | Planmal, WBS-leveranser | Alle tidsestimater, leveranseinnhold og prioriteringer |
| 2026-03-07 | Fase 2 | Fix av «strategisk tilpasning»-framing i ROS-seksjonen | Nøytral omformulering i plan og MEMORY.md | Godkjenning av nøytral framing |
| 2026-03-07 | Fase 2 | Tre-lags analyseramme + beredskapsperspektiv lagt til plan (v1.3) | Ny tekst i metodeavsnitt 3.2 | Faglig godkjenning av rammeverket |
| 2026-03-07 | Fase 2 | Litteratursøk-prompt og verifisering av ChatGPT-litteraturliste | Websøk-verifisering av 7 referanser, korreksjon av Ibrahim-årstall (2015→2016) og Vera Institute-tittel | Endelig kildeutvalg og vurdering av relevans |
| 2026-03-07 | Fase 2 | Opprettelse av Excel-litteraturliste (26 kilder, fargekodet) | Python-script + Excel-fil | Kategorisering, relevansvurdering, verifiseringsstatus |
| 2026-03-07 | Fase 2 | CLAUDE.md fullstendig omskrevet (gammelt prosjekt fjernet) | Ny CLAUDE.md med 110-kontekst | Godkjenning av innhold |
| 2026-03-07 | Fase 2 | MS Project XML Gantt opprettet (32 oppgaver) | Gantt-XML | Alle datoer, avhengigheter og milepæler |
| 2026-03-08 | Fase 2 | Plan v1.4: versjonshode 0.9→1.3, 18→12 sentraler med navneliste | Oppdatert plan | Korrektur og godkjenning |
| 2026-03-08 | Fase 2 | Plan v1.5: L8c (EDA) og L11b (sensitivitetsanalyse) splittet ut | Oppdatert plan + XML | Faglig beslutning om splitting |
| 2026-03-09 | Fase 2 | Gantt XML: avhengighetslogikk M4, L10, L14 korrigert + datokaskade | Oppdatert XML med korrekte FS-koblinger | Faglig godkjenning av ny sekvens |
| 2026-03-09 | Fase 2 | Litteraturliste: 5 nye referanser lagt til (Garnett 2002, Wallace & Whitt 2005, L'Ecuyer 2018, Vera Institute 2019, Meld. St. 16 2024) | Oppdatert Excel | Utvalg basert på scope-vurdering |
| 2026-03-09 | Fase 4 | Rapport v0.1 gjennomgått, 8 feil identifisert og rettet (v0.2) | Korrigeringer i rapportskall | Godkjenning av alle endringer |
| 2026-03-09 | Alle | Opprettelse av dette KI-erklæringsdokumentet | KI-erklæringen | Godkjenning av innhold |
| 2026-03-13 | Fase 3 | EDA på BRIS 2025: hendelsesfordeling, døgnprofil, kategoriklassifisering | Python-skript for klassifisering og figurer | Alle beslutninger om kategorigrenser og figurutforming |
| 2026-03-15 | Fase 3 | Analyse av bindingstid, utkast til kapasitetsmodell | bindingstid-skript, fordelinger og figurer | Tolkning av fordelinger, valg av imputerings­strategi |
| 2026-03-22 | Fase 3 | Erlang-C-grunnlinje, implementasjon og tolkning | Python + sympy/scipy for Erlang-C-formelen | Valg av samtaletid (3,44 min), tolkning av lav ρ |
| 2026-04-05 | Fase 3 | Benchmarking alle 12 sentraler 2022 til 2025 | benchmark-skript, MOB-bearbeidelse | Datavalg, figuroppsett |
| 2026-04-07 | Fase 3 | V1: Sammenstilte anrop og sekvensgap-metoden, diskusjon av modellantagelser | Notat med beslutningsgrunnlag | Vurdering av konservativitet, dokumentasjon |
| 2026-04-07 | Fase 3 | V2: Kategori A som operativ bakgrunnsbelastning, modellutvidelse | Variant B-design | Beslutning om todelt modell A/B |
| 2026-04-07 | Fase 3 | V3: Total operativ belastning, metodisk avklaring av A vs B | Sluttdesign i kap 6.5 | Faglig vurdering |
| 2026-04-15 | Fase 3 | Utvikling av spørreskjema for 12 sentraler, struktur | skjema-skript + 12 md-skjemaer | Spørsmålsformuleringer, prioritering, intern kalibrering med lokale operatører |
| 2026-04-18 | Fase 3 | Nasjonal DSB 2025-oversikt, 508 228 oppdrag, 7 figurer | nasjonal-skript, anomalidokumentasjon | Tolkning av kategoriavvik, normalisering av sentralnavn |
| 2026-04-18 | Fase 3 | DSB-ønskeliste BRIS-datauttrekk, 22 prioriterte felt | ønskeliste-dokumentet | Prioriterte felt, faglig begrunnelse |
| 2026-04-19 | Fase 3 | LABA dybdeanalyse n=50 utfylt, V3-regelutvidelse (Kilde=Alarm-krav) | Re-klassifisering av 2 065 oppdrag, V3-regel implementert i alle 5 skript | Tolkning av klassifiseringsobservasjoner, regeldesign |
| 2026-04-19 | Fase 3 | V3 op-binder-semantikk + D-pri1/D-aba-splitt, modellrefaktorering | Refaktorert primærmodell, D-pri1 (makkerpar) vs D-aba (seriell) | Operativ vurdering, prosedyreverifisering |
| 2026-04-19 | Fase 4 | Skriving av kap 1, 3, 9, innledning, teori, konklusjon (v1.0) | Markdown-utkast | Alle faglige formuleringer, valg av kanoniske kilder, struktur |
| 2026-04-19 | Fase 4 | Oppdatering av kap 2, 4, 5, 6, 7, 8 til V3-semantikk | Konsistent V3-terminologi gjennom hele rapporten | Faglig verifisering av alle endringer |
| 2026-04-19 | Fase 4 | Sammenstilling av modellutvikling-notat (V1 til V3) | modellutvikling-notatet | Beslutningsrasjonale, sporbarhet |
| 2026-04-20 | Fase 3 | LABA-dybdeanalyse, videre klassifiseringsarbeid | Re-klassifisering og bindingstidsuttrekk | Tolkning, regeldesign og godkjenning |

> **Merknad om loggen:** Den detaljerte radvise loggen ble ikke ført kontinuerlig etter 2026-04-20. Hovedmilepælene i sluttfasen er dokumentert i prosjektets git-historikk (committer datert mai 2026) og oppsummeres her:
>
> - **Slutten av april til mai 2026 (Fase 4):** Skriving og ferdigstilling av alle rapportkapitler (kap 1 til 10, referanser og vedlegg) med Claude Code, gjennomgått, korrigert og godkjent av meg.
> - **Mai 2026:** Nasjonal benchmarking, sensitivitetsanalyser (fordeling av skjulte anrop, bootstrap-konfidensintervall) og scenarioanalyse (+1 operatør).
> - **29. til 31. mai 2026:** Flertrinns kvalitets- og kildeverifikasjon, inkludert uavhengig Codex-kryss-sjekk av tallene mot kildedata, typografi- og konsistensretting, regenerering av figurer (blant annet Figur 7.1), og skjerping av DSB-ønskelisten. Rapporten ble gjennomgått som ferdig og deretter gjenåpnet samme dag for å innarbeide en ærlig KI-erklæring og personvern-redegjørelse før innlevering.

---

## Del 3: Administrativ erklæring

Jeg, Rune Grødem, erklærer at:

- Bruken av kunstig intelligens i dette arbeidet er gjort rede for i Del 1 og Del 2 over og i Vedlegg D i rapporten.
- Bruken er i tråd med Høgskolen i Moldes retningslinjer for KI på hjemmeeksamen og med veileders føringer for emnet LOG650, der KI skal benyttes til tekstutforming.
- Jeg står fullt faglig ansvarlig for alt innhold i rapporten. Alle faglige beslutninger, tolkninger og konklusjoner er mine egne, og alt KI-generert utkastsmateriale er gjennomgått, korrigert og godkjent av meg.
- Ingen kilder er fabrikert. Alle referanser er verifisert mot originalkildene, og KI er ikke ført opp som kilde.
- Det offisielle, signerte HiMolde-skjemaet «Erklæring om bruk av kunstig intelligens» leveres som separat administrativt vedlegg.

Sted og dato: ______________________________

Signatur: ______________________________ (Rune Grødem)

---

## Del 4: Personvern og konfidensialitet

Datagrunnlaget i prosjektet er ikke-sensitive registerdata uten personopplysninger:

- **BRIS-fullrapport (110 Sør-Vest 2025)** og **DSB MOB-rapporter (2022 til 2025)** er lastet ned fra innlogget side på brannstatistikk.no. MOB-rapportene er ikke unntatt offentlighet, og BRIS-dataene inneholder ikke innmelders navn eller telefonnummer.
- **Alle resultater i rapporten er aggregerte** (prosentfordelinger, medianer, ankomstrater, fordelingstabeller). Kommune og andre geografiske indikatorer er utelatt, slik at verken adresser, kommuner, enkelthendelser eller enkeltpersoner kan knyttes til resultatene.
- **DSB (BRIS Support) har vurdert datagrunnlaget** (e-post april 2026) og bekreftet at datasettet kan deles i peer review uten databehandleravtale, at MOB-tallene ikke er unntatt offentlighet, og at aggregerte analyseresultater kan publiseres. Ved å utelate kommune og geografiske indikatorer er ytterligere anonymisering ikke nødvendig.
- **ROS- og beredskapsanalyser** er ikke gjengitt i sin helhet. For 110 Sør-Vest er kun deler som ikke er unntatt offentlighet benyttet, etter en konkret vurdering mot unntaksbestemmelsene. 110 Vests tilsvarende analyser er offentlig tilgjengelige via Bergen kommune.

Ettersom datagrunnlaget er ikke-sensitivt og alle resultater er aggregerte og ikke-identifiserende, reiser verken analysen eller den KI-assisterte arbeidsflyten personvernhensyn utover det som er redegjort for her.