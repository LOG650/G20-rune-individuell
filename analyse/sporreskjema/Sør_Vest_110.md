# Spørreskjema — Sør-Vest 110
## Validering av kapasitetsdata for nasjonal benchmarkstudie
### LOG650, Høgskolen i Molde, vår 2026

**Student:** Rune Grødem
**Kontakt:** rune.grodem@rogbr.no
**Innlevering:** hovedutkast slutten av april 2026, endelig rapport 31. mai 2026

---

## Om studien

Brannvesenet har en nasjonal dimensjoneringsforskrift (FOR-2023-01-06-23) som setter
kvantitative, etterprøvbare krav til antall brannmannskap basert på innbyggertall og
responstid. **Ingen tilsvarende standard finnes for 110-operatører.** Bemanningsnivået
fastsettes lokalt gjennom ROS- og beredskapsanalyser som er kvalitative og vanskelige å
etterprøve på tvers av sentraler.

Forskningsprosjektet undersøker problemstillingen:

> *I hvilken grad samsvarer faktisk bemanning ved norske 110-sentraler med kapasitetsbehovet
> beregnet fra historiske hendelsesdata og køteoretiske/prosedyrbaserte modeller?*

Målet er å bygge et **kvantitativt referansepunkt** for 110-bemanning — ikke for å kritisere
lokale valg, men for å komplettere ROS-analyser med tallbaserte målepunkter som kan
sammenlignes på tvers av alle 12 sentraler.

- **Primærcase:** 110 Sør-Vest, der jeg har detaljerte LEO/BRIS-data og intern beredskapsanalyse
- **Benchmarkgrunnlag:** alle 12 sentraler via DSB-årsrapporter (MOB) og BRIS-fullrapporter
- **Modell:** prosedyrbasert ankomstkonfliktmodell som måler andel beredskapsanrop som
  håndteres i normal-, degradert- (solo) eller sviktnivå

**Hvorfor jeg kontakter Sør-Vest 110:** for å kunne benchmarke kapasitetsbelastning må jeg
verifisere at DSB-tallene gjenspeiler operativ virkelighet, og forstå lokale særtrekk ved
bemanning, vaktordning og arbeidsmetodikk.

> Svarene behandles konfidensielt. Sør-Vest 110 navngis kun med eksplisitt samtykke.

---

## Del 1 — Verifisering av DSB-rapporterte data (2022–2025)

Tabellene under er hentet fra det dere selv har rapportert til DSB via MOB-systemet. Jeg
ber dere bekrefte, korrigere eller utdype disse tallene.

### 1.1 Bemanning (MOB-rapportert)

> **Merknad:** MOB-tallene under er ett enkelt tall per skift-type per år, og skiller ikke mellom **normal bemanning** (planlagt nivå når alle stiller) og **minimumsbemanning** (det laveste nivået sentralen kan operere på, f.eks. ved sykdom eller fravær). Skillet er sentralt for kapasitetsanalysen og presiseres i Spm 4 (tabell 1.1b).

**Tabell 1.1a — MOB-rapportert bemanning per år:**

| Kategori | 2022 | 2023 | 2024 | 2025 | Endring 22–25 |
|---|---|---|---|---|---|
| Ansatte heltid | 23 | 24 | 24 | 25 | +8.7% |
| Operatører dag — hverdag | 4 | 4 | 4 | 4 | |
| Operatører natt — hverdag | 4 | 4 | 3 | 3 | |
| Operatører dag — helg | 4 | 4 | 3 | 3 | |
| Operatører natt — helg | 4 | 4 | 3 | 3 | |

Tallene over er det dere har rapportert til DSB. Tabell 1.1b under ber om presisering av hva som er *normalt planlagt* versus *minimum* — dette skillet kan ikke utledes fra MOB.

### 1.2 Oppdrag med utrykning (sammenlignbare tall 2022–2024)

> **Datakvalitetsmerknad:** Flere sentraler tok i bruk nytt operativsystem (LEO/OHV) fra
> 2024, og fra 2025 registreres alle innkommende telefonsamtaler som egne hendelsesrader.
> Totalt oppdragsvolum er derfor **ikke** sammenlignbart på tvers av alle år. Tabellen
> nedenfor viser kun oppdrag MED utrykning (Brann + Ulykke), som er konsistent registrert
> alle år uavhengig av system.

| Kategori | 2022 | 2023 | 2024 | 2025* | Endring 22–24 |
|---|---|---|---|---|---|
| Oppdrag — Brann | 1148 | 1212 | 1088 | 1042 | |
| Oppdrag — Ulykke | 1356 | 1406 | 1392 | 1548 | |
| **Sum med utrykning** | **2504** | **2618** | **2480** | **2590** | **-1.0%** |
| Unødige/falske utrykninger | 4976 | 5007 | 4615 | 4005 | |

*2025-tall vises for orientering, men bør ikke brukes i trendsammenligning på grunn av systembytte.

### 1.3 Mottatte 110-anrop (MOB, selvrapportert)

> Sentralenes egne innrapporteringer, uavhengig av registreringssystem.

| | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Mottatte 110-anrop (MOB) | 14230 | 21609 | 22377 | 26348 |

**Spm 1.** Er tallene i 1.1–1.3 korrekte? Hvis nei — hva er riktige tall, og hva forklarer avviket?

> *Svar:*

**Spm 1b.** Hva inkluderer MOB-feltet «Mottatte 110-anrop» *konkret* hos dere? (Velg alle som gjelder — **flere svar kan brukes**)

- [ ] Kun besvarte telefonanrop på 110-nødlinjen
- [ ] Alle telefonanrop inkludert overførte, viderekoblede og avbrutte
- [ ] Automatiske ABA-signaler som kommer inn uten samtale
- [ ] Servicetelefon / teknisk support
- [ ] Alle henvendelser uavhengig av kanal
- [ ] Annet: ___

> *Kommentar (eksakt definisjon dere bruker):* MOB-skjemaet gir ikke en entydig definisjon, og variasjonen mellom sentraler i forholdet mellom MOB-anrop og DSB-oppdrag kan skyldes ulik tolkning. En presis avklaring her er nøkkel for nasjonal sammenligning.

---

## Del 2 — Vaktordning og bemanningsstruktur

**Kontekst (110 Sør-Vest):** Todelt skift med dag 07–19 og natt 19–07. Sentralen har
**6 vaktlag à 3 operatører + 1 vaktleder**. Normalbemanning er **3 operatører + VL = 4
personer på alle vakter** (også natt og helg). Sentralen kan på natt og helg gå ned til
**minimumsbemanning 2 operatører + VL = 3 personer**, og det er ikke planlagt å fylle opp
med vikarer ved fravær på disse skiftene. **Mer enn 50 % av vaktene på natt/helg
gjennomføres derfor på minimumsbemanning** (2+1 i stedet for 3+1). Sentralen tillater at
den 3. personen på natt/helg kan være vikar. Vi vet at noen sentraler kjører dagturnus i
stedet for todelt skift, og at faktisk bemanning kan avvike fra MOB-rapporten.

**Spm 2.** Hvilken vaktordning kjører Sør-Vest 110?

- [ ] Todelt skift (dag ca. 07–19, natt ca. 19–07)
- [ ] Dagturnus med separat natt (f.eks. 08–16 dag + egen natt)
- [ ] Annen ordning (beskriv under)

> *Beskrivelse:*

**Spm 3.** Avviker helgeordningen fra hverdager? På hvilken måte?

> *Svar:*

**Spm 4. — Tabell 1.1b: Normalbemanning vs. minimumsbemanning per skifttype.**

MOB-tallet under er det dere rapporterte til DSB for 2025. **Vi ber dere fylle ut hva som er normalbemanning (planlagt nivå når alle stiller) og minimumsbemanning (det laveste nivået sentralen faktisk kan operere på).** Skillet er sentralt for kapasitetsanalysen — fyll inn antall operatører + VL der det er relevant. Hvis MOB-tallet ikke samsvarer med normal eller minimum, forklar gjerne i kommentarfeltet under.

| Vakttype | MOB-tall (2025) | Normalbemanning (op + VL) | Minimumsbemanning (op + VL) | Maks ved topp |
|---|---|---|---|---|
| Dag — hverdag | 4 | | | |
| Natt — hverdag | 3 | | | |
| Dag — helg | 3 | | | |
| Natt — helg/helligdag | 3 | | | |

> *Kommentar:* Andel av vaktene som gjennomføres på minimumsbemanning (anslag, %)?

**Spm 5.** Hvordan dekkes vakter ved sykdom eller annet fravær? (**Flere svar kan velges**)

- [ ] Tilkall fra vikarliste / ekstrahjelper
- [ ] Beredskapsvakt (hjemmevakt)
- [ ] Kolleger som tar over / forlenger egen vakt
- [ ] Driftes med redusert bemanning
- [ ] Annet: ___

**Spm 6.** Anslagsvis hvor stor andel av vaktene dekkes av vikarer/ekstrahjelper sammenlignet med fast ansatte?

> *Svar:*

**Spm 7.** Er vaktlag ofte satt opp med planlagt overkapasitet (f.eks. planlagt 5, definert minimum 4)? Anslag for typisk overkapasitet per vakttype?

> *Svar:*

**Spm 8.** Besvarer vaktleder (VL) normalt innkommende nødanrop ved Sør-Vest 110?

- [ ] Ja, alltid
- [ ] Ja, ved behov / høy belastning
- [ ] Nei, aldri
- [ ] Ingen dedikert VL-rolle

> *Utdyping:*

---

## Del 3 — Arbeidsmetodikk: makkerpar vs solo-drift

**Kontekst (110 Sør-Vest):**
Prosedyrestandarden krever at hver beredskapshendelse håndteres av to operatører
(«makkerpar»): én på samtale med innringer, én som håndterer ressursutkalling, loggføring
og oppfølging. I praksis går drift ofte over i **solo-håndtering** når flere hendelser
inntreffer samtidig — alternativet er å la neste innringer vente. Kvaliteten synker, men
blir «godt nok». Modellen vår forsøker å kvantifisere hvor ofte dette skjer.

**Spm 9.** Hvordan beskriver dere prosedyrestandarden ved Sør-Vest 110?

- [ ] Makkerpar er standard, solo-drift kun ved samtidige hendelser eller press
- [ ] Solo-drift er utgangspunktet; makkerpar aktiveres kun ved store hendelser
- [ ] Annen modell (beskriv)

> *Beskrivelse:*

**Spm 10.** Omtrentlig: hvor ofte må operatør jobbe solo på beredskapshendelser ved vanlig bemanning? (daglig, ukentlig, sjelden)

> *Svar:*

**Spm 11.** Har dere en intern norm/grense for hvor lenge et anrop kan vente før overføring til nabosentral? (Sør-Vest: 30 sek ubesvart → automatisk overføring til Agder; 10. anrop i kø overføres også.)

> *Svar:*

---

## Del 4 — Hendelseskategorier og operatørbindingstider

Studien bruker en **prosedyrebasert ankomstkonfliktmodell** der hver ny beredskapshendelse
måles mot kapasitetstilstanden (normal / degradert / svikt) på ankomsttidspunktet. Dette
krever at vi vet hvor lenge en operatør er **aktivt bundet** av en hendelse — ikke total
varighet i systemet, men fra anrop mottas til operatør er ferdig med oppfølging.

BRIS gir tidsdata for beredskapshendelser med utrykning, men mangler tidsdata for alle
andre henvendelsestyper. Derfor trenger vi operative estimater. Kategoriseringen nedenfor
er utledet fra BRIS 2025 ved 110 Sør-Vest. Referansetallene er Sør-Vests estimater og er
oppgitt som utgangspunkt for diskusjon.

| Kategori | Hva det er i praksis | Sør-Vest ref (min) | Ops bundet | Deres estimat (min) |
|---|---|---|---|---|
| **D-pri1 — Pri-1-utrykning (makkerpar)** | Bygningsbrann, trafikkulykke, farlig gods og andre pri-1-hendelser. Krever to operatører bundet parallelt fra første sekund (RØD = innringer-samtale, GUL = ressursvarsling/samband) gjennom hele akuttfasen | 14 (median) | 2 | |
| **D-aba — ABA-utrykning (serielt)** | Automatisk brannalarm som leder til utrykning fordi avklaring ikke kom innen 90 sek. Ikke pri-1 — én operatør kvitterer alarm, oppretter oppdrag og utalarmerer ressurser serielt | ca. 3 min (lengre dersom nødtelefon kommer fra stedet etterpå) | 1 | |
| **S — Service/overføringstest** | Servicetekniker tester brannalarmanlegg; operatør verifiserer signal og kvitterer ut | 2 | 1 | |
| **L-aba — ABA løst av 110 uten utrykning** | Automatisk brannalarm der nødtelefon innen 90 sek bekrefter ufarlig årsak (f.eks. matlaging) — lukkes uten utrykning. Krever Kilde=Alarm i registreringen | 6 | 1 | |
| **L-hendelse — Reell hendelse løst av 110** | Innringer melder noe reelt; operatør gir råd eller avklarer uten å sende ressurs. Inkluderer ABA-oppdrag med Kilde=Samtale (publikumsmelding om alarm uten ABA-signal) | 5 | 1 | |
| **L-ukjent — Løst av 110 uten initiell hendelsestype** | Oppdrag lukket som «Løst av 110» der feltet «Opprinnelig oppdragstype» ikke er satt — typisk bål-spørsmål, service lukket feil, korte avklaringer og andre henvendelser uten formell klassifisering før lukking | 3 | 1 | |
| **F — Feilringing** | Feilringing, «ønsket 112/113», eCall feil bruk | 0,5 | 1 | |
| **V — Viderevarsling** | Viderekobling til annen etat eller intern varsling | 1 | 1 | |

**Spm 12.** Er kategoriseringen gjenkjennbar ved Sør-Vest 110? Mangler det en type, eller er noe slått sammen som burde vært skilt?

> *Svar:*

**Spm 13.** Er Sør-Vests bindingstidsestimater rimelige sammenlignet med deres operative praksis? Hvilke kategorier avviker mest, og hvorfor?

> *Svar:*

**Spm 14.** For beredskapshendelser (D): er det vanlig at én hendelse binder to eller flere operatører samtidig (makkerpar-håndtering)? Hvor lenge holder den parallelle bindingen?

> *Svar:*

---

## Del 5 — ROS- og beredskapsanalyse

**Innrapportert status (fra MOB):**
- ROS-analyse sist revidert: **2023**
- Beredskapsanalyse utarbeidet: **Ja**, sist revidert: **2023**

**Spm 15.** Bekrefter dere årstallene ovenfor? Hvis nei — hva er korrekt?

> *Svar:*

**Spm 16.** Har dere selv god kjennskap til analysen? Brukes den aktivt i driftsplanlegging, eller er den et formelt dokument som revideres periodisk?

> *Svar:*

**Spm 17.** Når er neste planlagte revisjon?

> *Svar:*

**Spm 18.** Hvilke metoder/data bruker dere for å dimensjonere bemanningsnivå? (Beredskapsanalyse, historiske hendelsesdata, avtaler med eier, faglig skjønn, annet?)

> *Svar:*

**Spm 19.** Er ROS-/beredskapsanalysen i nåværende form tilstrekkelig som grunnlag for å dimensjonere antall operatører? Hva mangler eventuelt?

> *Svar:*

---

## Del 6 — Operativ belastning og opplevd bemanning

**Spm 20.** Hvor ofte opplever dere perioder der antall aktive hendelser overstiger ledig operatørkapasitet? (Daglig, ukentlig, sjelden?)

> *Svar:*

**Spm 21.** Hva skjer operativt når kapasitetsgrensen nås?

- [ ] Vaktleder trer inn som operatør
- [ ] Overført til nabosentral
- [ ] Prioritering mellom hendelser
- [ ] Redusert kvalitet på håndtering (f.eks. solo-drift, kortere intervju)
- [ ] Annet: ___

**Spm 22.** Er det et definert antall samtidige hendelser/anrop som utløser tiltak eller varsling (f.eks. bistand fra nabosentral)?

> *Svar:*

**Spm 23.** Hvordan oppleves dagens bemanning fra et operativt perspektiv?

- [ ] Overdimensjonert
- [ ] Passe
- [ ] Knapt nok
- [ ] Underdimensjonert

> *Utdyping (gjerne med eksempler på når det merkes):*

---

## Del 7 — Sentralspesifikke avklaringer for Sør-Vest 110 (DSB 2025-data)

> **Hvorfor dette avsnittet er spesifikt for Sør-Vest 110:** DSB har i 2026 levert et fullstendig hendelsesdatasett for alle 12 sentraler (2025). Jeg har klassifisert alle oppdrag etter V3-logikken (D-pri1 / D-aba / S / L-aba / L-hendelse / L-ukjent / F / V) basert på kolonnene «Oppdragstype», «Opprinnelig oppdragstype», «Kilde» og «Ressurs varslet». D er splittet i D-pri1 (pri-1-utrykning, krever makkerpar) og D-aba (ABA-utrykning med Kilde=Alarm, håndteres serielt). Sammenligningen avdekker at **Sør-Vest 110 avviker betydelig fra nasjonalt snitt på enkelte kategorier** — spørsmålene under er generert kun for dere, basert på hvor deres tall ligger i topp-3 (↑ HØY) eller bunn-3 (↓ LAV) av de 12 sentralene. **Vi kan ikke benchmarke dere mot andre sentraler uten å forstå om disse avvikene skyldes registreringspraksis, lokal organisering eller reell operativ forskjell.**

Under vises **Sør-Vest 110s tall i nasjonal sammenheng**. Avvikene er flagget med ↑ HØY eller ↓ LAV. For hver flagget kategori følger et spesifikt oppfølgingsspørsmål merket **[SENTRALSPESIFIKT AVVIK ved Sør-Vest 110]**.

### 7.1 Deres sentral i nasjonal sammenheng (DSB 2025)

Totalvolum DSB 2025: **61,934** oppdrag. MOB-selvrapport: **26,348** mottatte anrop. Forhold DSB/MOB: **2.4×**.

| Kategori | Deres andel | Antall | Nasj. median | Nasj. spenn | Avvik |
|---|---:|---:|---:|---:|---|
| D-pri1 — pri-1-utrykning (makkerpar) | 7.2% | 4,472 | 10.3% | 7.0–24.9% | ↓ LAV |
| D-aba — ABA-utrykning (serielt) | 4.9% | 3,055 | 4.6% | 0.0–14.1% | – |
| L-aba — ABA løst av 110 uten utrykning | 5.5% | 3,430 | 3.8% | 0.0–7.5% | ↑ HØY |
| L-hendelse — reell hendelse løst av 110 | 6.9% | 4,298 | 7.3% | 3.3–10.2% | – |
| L-ukjent — lukket uten opprinnelig type | 27.1% | 16,766 | 29.4% | 13.8–40.4% | – |
| F — feilringing | 11.0% | 6,824 | 13.9% | 8.6–20.6% | – |
| V — viderekobling | 0.9% | 547 | 1.2% | 0.6–2.6% | ↓ LAV |

### 7.2 Oppfølgingsspørsmål — sentralspesifikke avvik for Sør-Vest 110

**Spm 25.** **[SENTRALSPESIFIKT AVVIK ved Sør-Vest 110]** ABA løst uten utrykning er høy (5.5%, 3430 oppdrag). Nasjonalt: median 3.8%, spenn 0.0–7.5%. **Dette avviker fra forventet mønster og må forklares lokalt.**

> *Avklaring:* Er terskelen for å lukke ABA uten utrykning annerledes hos dere — lengre venteperiode før utkalling, mer kontakt med objektet, eller annen prosedyre?

> *Svar:*

**Spm 26.** **[SENTRALSPESIFIKT AVVIK ved Sør-Vest 110]** Utrykningsrate (D-andel) er lav (12.2%). Nasjonal median: 18.4%, spenn 9.3–24.9%. **Dere ligger blant de nederste 3 av 12 sentraler — avviker fra forventet mønster og må forklares lokalt.**

> *Avklaring:* Filtreres flere henvendelser ut som «løst av 110» før utrykning aktiveres, eller har dere lokale samarbeidsformer (politi/AMK/brann) som håndterer en del hendelser før utalarmering?

> *Svar:*

**Spm 27.** **[SENTRALSPESIFIKT AVVIK ved Sør-Vest 110]** D-pri1-andel (pri-1-utrykninger som krever makkerpar) er lav (7.2%). Nasjonal median: 10.3%, spenn 7.0–24.9%. **Dere ligger blant de nederste 3 av 12 sentraler.**

> *Avklaring:* Skyldes dette ulik registreringspraksis (f.eks. om Opprinnelig oppdragstype settes til ABA på utrykninger som ikke er ren ABA), reell forskjell i pri-1-volum, eller lokal terskel for å klassifisere oppdrag som pri-1 vs ABA-utrykning?

> *Svar:*

**Spm 28.** **[SENTRALSPESIFIKT AVVIK ved Sør-Vest 110]** Forhold DSB/MOB er lavt (2.4×). Nasjonal median: 2.5×. MOB-selvrapport: 26,348 mottatte anrop. DSB-oppdrag: 61,934. **Dere ligger blant de nederste 3 av 12 sentraler i differanse — krever forklaring for at MOB- og DSB-tall skal kunne brukes konsistent.**

> *Avklaring:* **Hva teller dere egentlig i MOB-feltet «Mottatte 110-anrop»?** MOB-skjemaet gir ikke en entydig definisjon, og variasjonen mellom sentraler kan skyldes dette. Vi ber om å få bekreftet konkret hva deres tall inkluderer: (a) kun besvarte telefonanrop på 110-nødlinjen, (b) alle telefonanrop inkludert overførte, viderekoblede og avbrutte, (c) også automatiske ABA-signaler som kommer inn uten samtale, (d) også servicetelefon, eller (e) alle henvendelser uavhengig av kanal. Dette er en nøkkelavklaring for om MOB-anroptallet kan brukes som felles mål på tvers av sentraler.

> *Svar:*

---

## Del 8 — Avsluttende kommentarer

**Spm 29.** Har det skjedd spesielle hendelser (storulykker, klimahendelser, nye oppgaver, organisasjonsendringer) i perioden 2022–2025 som har hatt vesentlig påvirkning på kapasitetssituasjonen?

> *Svar:*

**Spm 30.** Er det andre forhold ved kapasitetssituasjonen ved Sør-Vest 110 som er viktig å forstå, og som ikke dekkes av spørsmålene ovenfor?

> *Svar:*

---

*Takk for at dere tar dere tid til å svare. Svarene kan returneres til rune.grodem@rogbr.no.*
*Spørsmål kan rettes til Rune Grødem, student LOG650 Forskningsprosjekt, Høgskolen i Molde.*