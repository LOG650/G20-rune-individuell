# Bruk av kunstig intelligens — LOG650 G20 Individuell

**Student:** Rune Grødem
**Emne:** LOG650 – Logistikk og kunstig intelligens, Høgskolen i Molde, Vår 2026
**Oppgavetittel:** Kapasitetsstyring og bemanningsdimensjonering ved norske 110-sentraler
**Dokument:** Løpende KI-erklæring og brukslogg
**Sist oppdatert:** 2026-03-09

> **Bruk:** Dette dokumentet tjener to formål:
> 1. Grunnlag for seksjonen «Bruk av kunstig intelligens» i rapporten (seksjon 3.4 / 5.4 og Vedlegg D)
> 2. Løpende logg som oppdateres gjennom hele prosjektet — én linje per brukshendelse
>
> **Oppdateringsrutine:** Legg til en ny rad i loggene nedenfor etter hver session der KI-verktøy brukes. Dato, verktøy, formål og hva som faktisk ble tatt inn i arbeidet.

---

## Del 1 — Bruk av kunstig intelligens (rapporttekst)

*Denne seksjonen kopieres/tilpasses til rapporten som seksjon «Bruk av kunstig intelligens» (jf. HiMolde retningslinjer for KI på hjemmeeksamen).*

### KI-verktøy benyttet i prosjektet

I dette prosjektet er følgende KI-verktøy benyttet som støtteverktøy i ulike faser av arbeidsprosessen:

| Verktøy | Versjon/plattform | Primær bruksområde |
|---|---|---|
| Claude Code (Anthropic) | claude-sonnet-4-6, VSCode-extension og terminal | Prosjektplanlegging, koding, rapportstruktur, litteraturverifisering |
| ChatGPT (OpenAI) | GPT-4, chat.openai.com | Litteratursøk, metodiske innspill, Gantt-tilbakemeldinger |

### Formål og bruksbeskrivelse

**Claude Code** er benyttet som en interaktiv kode- og planleggingsassistent gjennom hele prosjektet. Konkrete bruksområder:

- **Prosjektstrukturering:** Utforming og revisjon av prosjektstyringsplanen (v1.0–v1.5), inkludert WBS, kritisk sti og Gantt-diagram (MS Project XML). Alle strukturelle beslutninger — hvilke leveranser som inkluderes, rekkefølge og tidsestimater — er tatt av undertegnede.
- **Koding og automatisering:** Generering av Python-scripts for filmanipulering (oppretting av Excel-litteraturliste, oppdatering av markdown-filer, konvertering til XML). All kode er gjennomgått og testet. Tolkninger av resultater og analytiske beslutninger er mine egne.
- **Litteratursøk og kildeverifisering:** Etter at ChatGPT foreslo referanser, ble disse manuelt verifisert av Claude Code via websøk. Dette avdekket bl.a. feil årstall (Ibrahim et al. 2016, ikke 2015) og manglende undertittel (Vera Institute 2019). Endelig kildeutvalg er mitt eget.
- **Rapportskall:** Generering av strukturert rapportskall (v0.1–v0.2) basert på HiMolde-mal og prosjektets problemstilling. Innhold i alle `[SKRIVES ETTER ...]`-seksjoner produseres av undertegnede selv etter datainnsamling og analyse.
- **Gjennomgang og kvalitetssikring:** KI-verktøyet er brukt til å identifisere inkonsistenser, feil og mangler i egne dokumenter. Alle endringer er vurdert og godkjent av undertegnede.

**ChatGPT** er benyttet som diskusjonspartner og idégenerator:

- **Litteratursøk:** Generert forslag til referanser og søkeord. Alle forslag er verifisert mot akademiske databaser og originaltekster før inkludering i litteraturlisten. ChatGPT er ikke oppført som kilde i referanselisten.
- **Metodiske innspill:** Forslag til forbedringer av Gantt-plan (to runder) og metodisk rammeverk for prosjektet. Forslagene er kritisk vurdert — noen akseptert, andre avvist — og alle endringer er undertegnedes eget valg.
- **Modellgjennomgang:** Presentasjon av utvidede modeller utover Erlang-C (Erlang-A, multi-skill queueing, robust optimering). Gjennomgangen er vurdert for scope-relevans, og kun et begrenset utvalg er tatt inn i teorikapittelet og litteraturlisten.

### Hvordan KI-genererte bidrag er bearbeidet

KI-verktøy er brukt som sparringspartner og teknisk assistent, ikke som primærforfatter. Konkret:

- Ingen KI-generert tekst er kopiert direkte inn i rapporten uten vesentlig bearbeiding
- Alle analytiske funn, tolkninger og konklusjoner er undertegnedes egne
- Alle referanseforslag fra KI er verifisert mot originalkilder
- Kode generert av KI er gjennomgått, testet og tilpasset

### Refleksjon — hvordan KI påvirket arbeidsprosessen

Bruken av Claude Code som iterativ assistent har effektivisert administrative og tekniske oppgaver (filhåndtering, versjonskontroll, Gantt-formatering) og frigjort tid til faglig fordypning. Verktøyet har fungert som en «rødflagg»-mekanisme som identifiserte feil (f.eks. feil årstall i referanser, inkonsistente avhengigheter i Gantt) som ellers kunne passert uoppdaget.

ChatGPT har vært nyttig for å få oversikt over et bredt metodisk landskap raskt, men krevde kritisk filtrering — særlig av referanseforslag og metodiske anbefalinger som lå utenfor prosjektets scope.

Alle vesentlige faglige beslutninger — problemstilling, modellvalg, analytisk tilnærming, tolkning — er tatt av undertegnede basert på faglig kunnskap, veileder-input og primærlitteratur.

---

## Del 2 — Løpende brukslogg

*Oppdateres etter hver session. Tilstrekkelig detaljert til å dokumentere bruksmønster ved forespørsel.*

### Claude Code (Anthropic, claude-sonnet-4-6)

| Dato | Fase | Formål | Output / hva ble tatt inn | Undertegnedes bidrag |
|---|---|---|---|---|
| 2026-02-XX | Fase 1 | Prosjektforslag — strukturering av problemstilling og metode | Utkast til problemstilling og RQ-er | Valg av problemstilling, tilpasning til 110-kontekst |
| 2026-03-01–06 | Fase 2 | Prosjektstyringsplan v1.0–v1.2: WBS, Gantt-tabell, kritisk sti | Strukturert planmal, WBS-leveranser | Alle tidsestimater, leveranseinnhold og prioriteringer |
| 2026-03-07 | Fase 2 | Fix av «strategisk tilpasning»-framing i ROS-seksjonen | Nøytral omformulering i plan og MEMORY.md | Godkjenning av nøytral framing |
| 2026-03-07 | Fase 2 | Tre-lags analyseramme + beredskapsperspektiv lagt til plan (v1.3) | Ny tekst i metodeavsnitt 3.2 | Faglig godkjenning av rammeverket |
| 2026-03-07 | Fase 2 | Litteratursøk-prompt og verifisering av ChatGPT-litteraturliste | Websøk-verifisering av 7 referanser, korreksjon av Ibrahim-årstall (2015→2016) og Vera Institute-tittel | Endelig kildeutvalg og vurdering av relevans |
| 2026-03-07 | Fase 2 | Opprettelse av Excel-litteraturliste (26 kilder, fargekodet) | Python-script + Excel-fil | Kategorisering, relevansvurdering, verifiseringsstatus |
| 2026-03-07 | Fase 2 | CLAUDE.md fullstendig omskrevet (gammelt prosjekt fjernet) | Ny CLAUDE.md med 110-kontekst | Godkjenning av innhold |
| 2026-03-07 | Fase 2 | MS Project XML Gantt opprettet (32 oppgaver) | Gantt_LOG650_G20_Rune_110.xml | Alle datoer, avhengigheter og milepæler |
| 2026-03-08 | Fase 2 | Plan v1.4: versjonshode 0.9→1.3, 18→12 sentraler med navneliste | Oppdatert plan | Korrektur og godkjenning |
| 2026-03-08 | Fase 2 | Plan v1.5: L8c (EDA) og L11b (sensitivitetsanalyse) splittet ut | Oppdatert plan + XML | Faglig beslutning om splitting |
| 2026-03-09 | Fase 2 | Gantt XML: avhengighetslogikk M4, L10, L14 korrigert + datokaskade | Oppdatert XML med korrekte FS-koblinger | Faglig godkjenning av ny sekvens |
| 2026-03-09 | Fase 2 | Litteraturliste: 5 nye referanser lagt til (Garnett 2002, Wallace & Whitt 2005, L'Ecuyer 2018, Vera Institute 2019, Meld. St. 16 2024) | Oppdatert Excel | Utvalg basert på scope-vurdering |
| 2026-03-09 | Fase 4 | Rapport v0.1 gjennomgått — 8 feil identifisert og rettet (v0.2) | Korrigeringer i rapportskall | Godkjenning av alle endringer |
| 2026-03-09 | Alle | Opprettelse av dette KI-erklæringsdokumentet | KI_erklæring_LOG650_G20_Rune.md | Godkjenning av innhold |

### ChatGPT (OpenAI, GPT-4)

| Dato | Formål | Output / hva ble tatt inn | Undertegnedes bidrag |
|---|---|---|---|
| 2026-03-07 | Litteratursøk — referanseforslag for Erlang-C og 110/PSAP | Liste på ~26 referanser | Kritisk verifisering, forkastelse av uverifiserbare, valg av 5 nye til litteraturliste |
| 2026-03-08 | Gantt-gjennomgang runde 1 — metodiske forbedringsforslag | 3 forslag (ROS-framing, tre-lags analyse, beredskapsperspektiv) | Aksepterte 2 av 3; avviste «kveldsskift» som tredje periode |
| 2026-03-08 | Gantt-gjennomgang runde 2 — strukturelle forbedringsforslag | 4 forslag (L8c, L11b, M4-avhengighet, L10-sekvens) | Aksepterte alle 4 etter faglig vurdering |
| 2026-03-09 | Utvidet modellgjennomgang — rammeverk utover Erlang-C | Oversikt over 12 modelltyper, ~25 referanseforslag, metodisk «oppskrift» | Aksepterte 5 referanser, metodisk framing for diskusjonskapittel; avviste sim-opt/MDP som utenfor scope |

---

## Del 3 — Administrativ erklæring

*Dette avsnittet tilsvarer det formelle «Erklæring om bruk av kunstig intelligens»-skjemaet fra HiMolde. Erklæringen signeres og leveres som administrativt vedlegg.*

**Jeg bekrefter at:**

- [ ] Jeg har lest og forstått HiMolde sine retningslinjer for bruk av KI på hjemmeeksamen
- [ ] All bruk av KI-verktøy er dokumentert i dette dokumentet
- [ ] Ingen KI-generert tekst er levert som mitt eget arbeid uten tydelig markering
- [ ] Alle referanser er verifisert mot originale akademiske kilder
- [ ] Ingen personopplysninger, konfidensielle data eller opphavsrettsbeskyttet materiale er lagt inn i åpne KI-verktøy
- [ ] All kode er gjennomgått, testet og forstått av meg
- [ ] Alle analytiske beslutninger, tolkninger og konklusjoner er mine egne

**Student:** Rune Grødem
**Dato:** [SIGNERES VED INNLEVERING]
**Underskrift:** ___________________________

> *Det offisielle skjemaet ligger i `000 templates/declaration-of-use-of-artificial-intelligence_-final.docx`. Fylles ut og signeres, og leveres som separat administrativt vedlegg ved innlevering av sluttrapport.*

---

## Del 4 — Personvern og konfidensialitet

Følgende er bekreftet for dette prosjektet:

- **Operasjonelle data fra 110 Sør-Vest** er ikke lagt inn i åpne KI-verktøy. LEO/BRIS-data behandles lokalt og deles ikke med Claude.ai-nettjenesten (kun Claude Code lokalt via VSCode-extension/terminal).
- **Personopplysninger** fra intervjuobjekter lagres ikke i KI-verktøy.
- **ROS/beredskapsanalyse** (intern, ikke offentlig) behandles konfidensielt og er ikke delt med åpne KI-plattformer.

---

*Versjon 1.0 | Opprettet: 2026-03-09 | Neste oppdatering: etter hver session med KI-bruk*
