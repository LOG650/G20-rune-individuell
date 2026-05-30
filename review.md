# Sluttverifikasjon av rapporten – funn og restanse

**Dato:** 2026-05-29
**Rapport:** Kapasitetsstyring og bemanningsdimensjonering ved norske 110-sentraler (LOG650 G20, Rune Grødem)
**Omfang:** Kilder/sitatintegritet, pensumsamsvar, kapittelkonsistens, fagfelle- og sensorvurdering, språk, figurer, git/struktur.
**Metode:** Flertrinns verifikasjonsworkflow (84 delagenter) som åpnet hver brukte kilde-PDF, kryssjekket alle kapitler mot hverandre og mot kildedata (CSV/skript), med adversariell verifisering av hvert «må-rettes»-funn. Manuell kontroll av tallavvik mot `analyse/*.csv`.
**Revisjon (2026-05-29):** Punktene 3A-4, 3A-12, 3B-2, 3B-4, 3B-6 og del 5 er korrigert etter en uavhengig kryss-sjekk (Codex) som kjørte skriptene skrivebeskyttet. Hovedkritikken står; korreksjonene gjelder årsaksforklaring (tie-break i sweepen, ikke imputering), nøyaktige prosenttall for nevneren, Leonardsen-anbefalingen (ikke automatisk årstallsbytte), og at primærresultatet allerede er visualisert i Figur 8.2.

---

## 0. Status per 2026-05-29 (implementeringsrunde)

**Gjennomført og committet:**
- **3A (kildeintegritet) — komplett.** Det fabrikkerte sitatet (Interdep. 2009, 5 steder), Kim, Mukhopadhyay, NENA, Samdal, FIRE21, Gans og Shen & Huang er rettet. Leonardsen er forankret på den verifiserbare 2019-EMCC-artikkelen (PDF 62); 2021-oppføringen er fjernet og (2021)→(2019) gjennomført konsistent.
- **3B/3C uten avhengighet til hovedtallet — gjennomført:** A2-etikett «statistisk validert»→«forankret antagelse; bindingstidsfordeling bootstrap-kvantifisert» (3B-8, kap1/6), n=events vs anrop (3B-5), c=2-kolonnenote (3B-9), 18 901/18 930-fotnote (3B-7), RQ5-gjengivelse harmonisert kap1↔kap10 (3B-10), tabelltitler «operativ tilpasningsmodell»→«prosedyrebasert ankomstkonfliktmodell» (3C), 9,6× (3C), D-aba sekvensgap 17→8,7 % (3C).

> **OPPDATERING 2026-05-30 — LØST:** Modell-/hovedtallspørsmålet under er nå avgjort og implementert (uniform spredning av skjulte anrop + deterministisk sweep). Nytt hovedtall natt/helg Svikt = **21,0 %** (bånd 16,8–26,4 %). Alle avhengige punkter (3B-1 til 3B-6) er regenerert og renummerert i hele rapporten. Se `ENDRINGSLOGG_modelloppdatering_skjulte-anrop.md` for full før→etter. Avsnittet under er beholdt som historikk.

**KRITISK — utsatt til egen diskusjon (modell/hovedtall):**
- Tie-break-fiksen (deterministisk samtidighetsregel) avdekket at natt/helg Svikt faller fra **32,6 % til 18,8 %** (og dag fra 14,9 % til 5,0 %) når interpolerte skjulte anrop ikke lenger binder hverandre på ett kollapset tidsstempel. **Hovedtallet er dermed i betydelig grad et artefakt** av at skjulte anrop mangler reelle tidsstempler og stables på nærmeste nabos tidspunkt (`est_tid = before.iloc[-1]` i interpolasjonen). Den «riktige» verdien ligger trolig mellom 18,8 % og 32,6 %.
  - **Brukerens beslutning:** modellvalget tas i egen runde; det legges inn en eksplisitt begrensning om manglende tidsstempel på skjulte anrop. Modellskript/CSV/figurer er IKKE endret i denne runden (reversert til committet tilstand).
  - Mulige veier til diskusjonen: (a) spre skjulte anrops tidsstempler jevnt over sekvensgapet, (b) deterministisk uten samtidig binding (≈18,8 %), (c) behold 32,6 % med eksplisitt begrensning.
  - **Avhengige punkter UTSATT** (regenereres/avgjøres når modellvalget er tatt): 3B-1 (Tabell 8.4 variant B-celler), 3B-2 (32,6/32,8 kanonisk + «stokastisk støy»-forklaring), 3B-3 (kap9 20,3→20,5), 3B-4 (±1 pp→CI), 3B-6 (observert vs estimert nevner), samt robusthetspåstanden i sammendraget (3C).
- **3A-12:** LØST (2026-05-30). APCO/RETAINS (nå Taylor et al., 2005; fil `60-…`) og Larson (1974; fil `56-…`) er lastet ned, verifisert mot kilde, og oppdatert i referanselisten. Ingen siterte kilder mangler nå nedlastet PDF (utover klassikere/lovdata/SSB/DSB/interne dokumenter, som forventet er uten PDF).

**Ikke gjort (per instruks):** PDF er ikke bygget på nytt.

---

## 1. Samlet vurdering

**Rapporten er IKKE leveringsklar i nåværende form.** Selve modellen, dataene og argumentasjonsstrukturen står seg – ingen av funnene utfordrer den faglige substansen. Problemet er **sitatintegritet og intern tallkonsistens**: noen kildebruk kan ikke forsvares slik den står, og rapportens hovedtall spriker mot egne tabeller/kildedata noen steder. Ingen av rettelsene krever ny datainnsamling; de fleste er omformuleringer og metadatarettinger.

Det som er **rettet direkte** i denne runden er listet i del 2. Det som **må utbedres før innlevering** er listet i del 3 (prioritert). Del 4–7 dekker pensum, figurer, anbefalt restanalyse og git/struktur.

> Merk: alle delagent-funn er adversarielt etterprøvd. Der to delfunn ga motstridende anbefaling (45,6 % vs 46,0 %), er konflikten avgjort manuelt mot kildedata (`analyse/total_belastning_oppsummering.csv`) – se 3B-1.

---

## 2. Rettet direkte i denne runden (små ting)

### 2.1 Språk/korrektur (15 rettinger)
| Fil | Endring |
|---|---|
| _forside_og_kap1.md | «to operatører — én» → «to operatører: én» (em-dash, norsk + engelsk abstract) |
| kap2_litteratur.md | «prosedyr:» → «prosedyre:» |
| kap2_litteratur.md | «kapasitetsdegrasjon» → «kapasitetsdegradasjon» |
| kap2_litteratur.md | «korte tidsvindu» → «korte tidsvinduer» |
| kap3_teori.md | «formalt rammeverk» → «formelt rammeverk» (3.7-tittel) |
| kap3_teori.md | «ytelse er svært sårbart» → «sårbar» |
| kap3_teori.md | «mange samtidige innringer» → «innringere» |
| kap4_casebeskrivelse.md | «innebyggede kontrollen» → «innebygde» |
| kap6_modell.md | «et 20 til 22 % Brudd-rate» → «en Brudd-rate på 20 til 22 %» |
| kap9_diskusjon.md | «det totale antall ansatte» → «det totale antallet ansatte» |
| kap9_diskusjon.md | «Penverne et al. (2024) digitale tvilling» → «Penverne et al.s (2024)» |
| kap9_diskusjon.md | «som alternativ eller komplementær.» → «som alternativt eller komplementært tiltak.» |
| kap10_konklusjon.md | «denne casen — Svikt» → «denne casen: Svikt» (em-dash) |
| kap10_konklusjon.md | «punkt 1–3» → «punkt 1 til 3» (en-dash) |

### 2.2 Bibliografi-metadata (7 rettinger, verifisert mot PDF)
| Kilde | Endring | Kilde for korrekt verdi |
|---|---|---|
| Interdepartemental arbeidsgruppe (2009) | tittel «felles» → «fremtidig» organisering | PDF-forside + innholdsfortegnelse |
| Gustavsson (2018) | «Doktoravhandling, Université de Montréal» → «Lisensiatavhandling, Mittuniversitetet» | PDF: «Licentiate Thesis No. 141», ISBN/ISSN, Mid Sweden University |
| Harchol-Balter (2022) | sider 201-225 → 201-203 | PDF-header «Queueing Systems (2022) 100:201-203» |
| L'Ecuyer et al. (2018) | sider 3292-3303 → 525-536 | informs-sim.org-PDF (den lenkede versjonen) |
| Meld. St. 16 (2023-2024) | tittel «Felles verdier, felles ansvar» → «Brann- og redningsvesenet: Nærhet, lokalkunnskap og rask respons i hele landet» | PDF-tittelside (gammel tittel tilhørte en annen melding) |
| St.meld. nr. 41 (2000-2001) | utgiver «Kommunal- og regionaldepartementet» → «Arbeids- og administrasjonsdepartementet» | PDF s.2 pkt. 1.2 |
| Storesund m.fl. (2017) | «Ishol, A. M.» → «Ishol, H. M.» (Herbjørg M. Ishol) | PDF-forside |

> Sjekk gjerne den eksakte offisielle tittelformen/tegnsettingen på Meld. St. 16 mot regjeringen.no før innlevering.

### 2.3 Struktur/git
- `.gitignore`: `KML-kompendium-PDF-eksport/` og `LOG650Vault/` lagt til (synces ikke til git). **(Krav 9 ✓)**
- `003 references/`: 18 ubrukte kilde-PDF-er + 3 ikke-kilde markdown-filer flyttet til `003 references/ikke_brukt/`. 40 faktisk brukte kilder gjenstår. **(Krav 8 ✓)**

---

## 3. MÅ utbedres før innlevering (steg for steg)

> Disse er ikke rettet automatisk fordi de enten endrer faglig mening, gjelder hovedtall som går til styret, eller krever en redaksjonell beslutning fra deg. Anbefalt løsning er angitt for hver.

### 3A. Sitatintegritet (høyest prioritet – rapporten går til styret i RogBR)

**3A-1. Fabrikkert ordrett sitat (Interdepartemental arbeidsgruppe, 2009).**
«…ikke finnes vitenskapelig grunnlag for de valgte terskelverdiene» står i anførselstegn som ordrett sitat fire steder (kap2 §2.6, kap8 §8.4, kap9 §9.2.2/9-linje 112, kap10 §10.1), men finnes **ikke verbatim** i kilden. Det bærer rapportens kjernepremiss.
→ *Erstatt med indirekte tale*, eller bruk et reelt sitat med sidetall: s.52 «Det finnes i dag ikke systematisert tallmateriale eller relevant forskning med en kvalitet som kan gi grunnlag for en bred analyse» / s.92 «Det er ikke fastsatt nasjonale krav for hvor raskt innringeren skal komme i kontakt med operatøren.»

**3A-2. Falsk attribusjon av svartidskrav (Interdepartemental arbeidsgruppe, 2009).**
kap9 §9.2.2: arbeidsgruppen «foreslo servicenivåkrav (8 til 10 sekunders svartid)». Kilden foreslår **ikke** et tallfestet krav; 8–10 sek er internasjonale eksempler (Island/Sverige) og målte aksesstider (s.25/s.92).
→ Omformuler til at dette er internasjonale eksempler, ikke et forslag fra arbeidsgruppen.

**3A-3. Mekanisme-feilsitering (Kim et al., 2008).**
kap2 §2.4 og kap3 §3.6.4: «der to servere er nødvendig per kunde, halveres reell kapasitet sammenlignet med M/M/c». Dette er **motsatt** av kildens konklusjon: Kim et al. modellerer *frivillig* serversamarbeid som **bedrer** utnyttelsen, og stabilitetsbetingelsen er ρ=λ/(Nμ)<1 (uendret fra M/M/c). Også tabellrad kap3 §3.9 «Team-basert kapasitet (Kim, Jouini) – Matematisk analog til makkerpar».
→ *Fjern* Kim-påstanden om halvert kapasitet og knytt makkerpar-mekanismen til **Brill & Green (1984)** og **Harchol-Balter (2022)**, som allerede er korrekt sitert for nettopp dette. Hvis Kim fjernes som kilde: fjern bibliografi-oppføringen (ellers «sitert-men-ikke-brukt» motsatt vei). Hvis Kim beholdes: rett initial «Lee, M.» → «Lee, M. H.».

**3A-4. Leonardsen – bibliografi og PDF matcher ikke (avklaringsbehov, ikke automatisk bytte).** *(presisert)*
Det eksisterer tre distinkte Leonardsen-artikler. Bibliografien har to (2019 «Healthcare workers' experiences…» og 2021 «Work experiences of EMD…»), men den **nedlastede PDF-en** (tidl. `62-…`) er en *tredje* artikkel: Leonardsen et al. (2019) «Exploring individual and work organizational peculiarities…» (om EMCC call-takeres arbeidsorganisering), BMC HSR 19:545. Denne PDF-en matcher ingen av de to bibliografioppføringene – men den **støtter faktisk kap2/kap6-bruken om operatørenes arbeidsforhold bedre** enn 2021-oppføringen gjør.
→ Hovedtiltaket er derfor å **avklare hvilken Leonardsen-artikkel hver påstand faktisk skal hvile på**, deretter rette bibliografi-metadata og laste ned riktig PDF for hver. **Ikke** bytt automatisk (2019→2021): det kan godt være den lokale 2019-EMCC-artikkelen som er den riktige kilden for kap2 §2.5 og kap6 §6.7. Når kildevalget er avklart, sørg for konsistent årstall per påstand (kap6 §6.7 vs §6.4.3 bruker i dag ulikt år for samme A7-poeng).

**3A-5. FIRE21 / McNamee m.fl. (2025) – feilsitering.**
kap2 §2.5: rapporten «kartlegger … kapasitetsutfordringer» og «identifiserer dimensjonering og bemanning som sentrale problemstillinger». FIRE21 handler om **problemløsningskompetanse, problemløsningsnettverk og risikobilde** – ikke dimensjonering/bemanning. Også «fokus på utrykningsleddet (mannskap og kjøretøy)» treffer ikke kildens innhold.
→ Omformuler til det kilden faktisk dekker, eller vurder å fjerne en perifer kilde.

**3A-6. Mukhopadhyay et al. (2022) – Erlang-attribusjon.**
kap2 §2.3: «analytiske kømodeller (Erlang-C og varianter) er veletablert for anropsmottak». Ordet «Erlang» finnes ikke i kilden; køteorien der gjelder dekningsmodeller for utrykningsenheter (hypercube/MEXCLP), ikke telefonmottak.
→ Fjern Erlang-C-attribusjonen til denne kilden, eller omformuler til kildens faktiske tema.

**3A-7. Samdal et al. (2021) – overtolkning + upresist objekt.**
kap1 §1.2 og kap2 §2.5: «disponeringsvalg er systematisk påvirket av kapasitetstilstand i sentralen». Kilden tilskriver dispatch-unøyaktighet **vage kriterier og dårlig CAD-datakvalitet**, ikke sentralens kapasitetstilstand. «Legebemannede ambulanser» er også upresist (kilden gjelder P-EMS = legehelikopter/legebil, eksplisitt skilt fra vanlige ambulanser).
→ Omformuler påstanden og objektet.

**3A-8. NENA 2003 vs 2020 – tall tilskrevet feil kilde.**
kap2 §2.3 co-siterer «(NENA, 2003; NENA, 2020)» for «90 % innen 15 sek, 95 % innen 20 sek». Disse tallene tilhører **kun NENA-STA-020.1-2020**; 2003-rapporten bruker P.01 Grade of Service.
→ Attribuer 15/20-sekunders-tallene kun til NENA (2020). **Verifiser også** påstanden i kap9 §9.2.2 om at «NENA (2020) erkjenner … mangler empirisk begrunnelse» – denne ble ikke verifisert i kjøringen og har samme risikoprofil som 3A-1.

**3A-9. Penverne et al. (2024) – kausalpåstand + tall.**
kap9: (a) «regionalkunnskap tapes ved virtualisering» er forfatterens syntese (bro til Dwars/Gustavsson), ikke Penvernes funn (kilden forklarer forskjellen med kø-nettverksstruktur). (b) Tallet «17 til 32 %» bør være **«11 til 32 %»** (per sentral) eller **«21 %»** (snitt).
→ Marker regionalkunnskap-koblingen som egen tolkning, og rett tallintervallet.

**3A-10. Gans et al. (2003) – ikke-ordrett «sitat».**
kap3 §3.3: «statistical economies of scale» i anførselstegn. Kilden skriver «economies of scale» uten «statistical».
→ Fjern «statistical», eller fjern anførselstegnene (ideen er korrekt attribuert).

**3A-11. Shen & Huang (2008) – feil PDF/oppføring.**
Nedlastet PDF var søster-artikkelen («Forecasting Time Series of Inhomogeneous Poisson Processes», Annals of Applied Statistics 2(2):601-623), ikke bibliografioppføringen («Interday forecasting…», M&SOM 10(3):391-410). kap2 §2.2-påstanden «testing av Poisson-forutsetningen» støttes heller ikke av Shen & Huang (de *antar* Poisson).
→ Last ned riktig PDF *eller* endre bibliografien til den faktisk brukte artikkelen, og juster Poisson-test-attribusjonen (hør trolig til Brown et al./Ibrahim).

**3A-12. Kilder sitert uten matchende nedlastet PDF.** ✅ LØST (2026-05-30).
- **APCO/RETAINS (2005):** PDF lastet ned (fil `60-…`), verifisert. Endret til personforfattere: Taylor, M. J., Gardner, V., Clark, P., & McCombs, B. (2005), og in-tekst-sitering i kap2 §2.4 oppdatert tilsvarende.
- **Larson (1974):** journalartikkel-PDF lastet ned (fil `56-…`), verifisert. Bibliografi rettet: «queueing» → «queuing», DOI 10.1016/0305-0548(74)90076-8 lagt til.
- **Leonardsen** ble løst tidligere ved å forankre på den verifiserbare 2019-EMCC-artikkelen (PDF 62), jf. 3A-4.
(Erlang 1917, lovdata-forskrift, SSB, DSB-datasett og interne Norconsult/RogBR-dokumenter er forventet uten PDF og er greit.)

### 3B. Tallkonsistens (interne motsigelser mot egne tabeller/kildedata)

**3B-1. Tabell 8.4 «Alle» variant B er foreldet.** *(avklart manuelt mot CSV)*
Tabell 8.4 viser «Alle» variant B = 53,9 / 20,1 / 25,9. Kildedata `analyse/total_belastning_oppsummering.csv` gir **54,4 / 20,0 / 25,6**. Narrativtallet 45,6 % (kap9 §9.3.1, kap10 §10.1) = 20,0 + 25,6 er altså **korrekt**; det er tabellcellene som er utdaterte (øvrige rader i 8.4 matcher CSV).
→ **Oppdater Tabell 8.4 «Alle»-rad variant B til 54,4 / 20,0 / 25,6.** (Ikke endre 45,6 % i teksten.)

**3B-2. Punktestimat 32,6 % vs 32,8 % (variant A natt/helg Svikt; Brudd 20,5 vs 20,3).** *(årsak verifisert i kode)*
To skript gir to verdier: `konflikt_total_belastning.py` (primærmodell) → 32,6 / 20,5 (Tabell 8.1, brukt overalt); `scenario_pluss1.py` baseline og bootstrap-skriptet → 32,8 / 20,3 (Tabell 8.2/8.6). **Årsaken er ikke imputeringsregime eller «stokastisk støy».** Begge skript bruker samme event-mengde, samme `SEED_DABA` og samme 27 960 events, men `kjor_sweep` sorterer kun på `events.sort_values("Dato_og_Tid")` – uten sekundær sorteringsnøkkel og med pandas' ustabile standard-quicksort. Events med **identisk tidsstempel** klassifiseres derfor i ulik rekkefølge mellom skriptene, noe som gir ~1 567 avvik i aktive-tellingen og dermed ulik Normal/Brudd/Svikt på vippetilfeller. Tabell 8.1 kaller 32,6 «punktestimat», mens Tabell 8.6 kaller 32,8 «Punktestimat» og 32,6 «bootstrap-mean» – direkte motstrid om hva «punktestimat» er. «Stokastisk støy»-forklaringen i §8.2 er feil.
→ **Innfør en deterministisk tie-break/samtidighetsregel i sweepen** (sekundær sorteringsnøkkel, f.eks. kategori-prioritet, evt. `kind="mergesort"` for stabil sortering) slik at alle skript gir **ett** kanonisk tall. Behold 32,6 / 20,5 som offisielt hovedtall (primærmodell, brukt i hele rapporten); rett §8.2-forklaringen fra «stokastisk støy» til tie-break-/samtidighetsårsaken, og harmoniser Tabell 8.1/8.2/8.6 mot den kanoniske kjøringen.

**3B-3. kap9 §9.2.2 blander to kjøringer.** «…ankommer i Svikt og ytterligere 20,3 % i Brudd» kombinerer Svikt 32,6 (Tabell 8.1) med Brudd 20,3 (Tabell 8.2/8.6). Samme tabell (8.1) gir Brudd = 20,5.
→ Endre 20,3 % → 20,5 % (gir sum 53,1 %, som matcher §9.3.1).

**3B-4. Usikkerhet ±1 pp i Sammendrag/Abstract overdriver.** §Sammendrag og §Abstract: «±1 prosentpoeng». Bootstrap-CI er [32,1; 33,2], dvs. asymmetrisk −0,5 / +0,6 pp rundt 32,6 (jf. §5.6.1 og §8.3.4).
→ Mest presist: **oppgi selve intervallet [32,1; 33,2]** i begge avsnitt. Et symmetrisk «±0,5 prosentpoeng» er et akseptabelt alternativ, men intervallet er å foretrekke fordi CI-en ikke er helt symmetrisk.

**3B-5. n = 27 960 «events» vs «anrop».** Tabell 8.1-kolonnen «anrop» (n=27 960) inkluderer 1 504 D-aba Fase 2-events (oppfølgingsfase, ikke nytt innkommende anrop), og 27 960 brukes også som «events» i kap6 og i «27 960 av 80 865 anrop» (§8.3.1). To enheter blandes. (Verifisert sammensetning: 4 499 D-pri1 + 3 056 D-aba Fase 1 + 1 504 D-aba Fase 2 + 18 901 skjulte = 27 960.)
→ Avklar eksplisitt at nevneren er klassifiserte op-binder-events, *eller* ekskluder Fase 2 fra nevneren. Skill konsekvent «events» fra «beredskapsanrop».

**3B-6. Transparens om estimert nevner ved hovedfunnet.** *(prosent korrigert)* For hele variant A er de 18 901 interpolerte skjulte anropene **67,6 %** av nevneren (27 960 events), og de observerte ankomstene (7 555 = D-pri1 + D-aba Fase 1) er 27,0 % (resten er 1 504 avledede Fase 2-events). Isolert for natt/helg er skjult-andelen lavere, om lag 59 %. Dette oppgis aldri der hovedtallet presenteres (Funn 3/Tabell 8.1/sammendrag).
→ Tilføy 1–2 setninger: 7 555 observerte beredskapsankomster vs 18 901 estimerte skjulte anrop, og at bootstrap-CI ikke dekker usikkerhet i interpolerte ankomsttider. (Vurder å rapportere Svikt-andel også for kun observerte anrop.)

**3B-7. 61 964/61 934 og 18 901/18 930 (Sør-Vest).** Oppdrags-differansen er forklart i §8.5, men skjult-anrop-differansen (18 901 vs 18 930) er uforklart, og forklaringen står langt fra tabellene.
→ Fotnote ved Tabell 8.8 og 8.10 som dekker begge tallpar.

**3B-8. A2-etiketten «statistisk validert».** Tabell 6.3 + §6.7 + §1.6 merker A2 (q=2 makkerpar) «Empirisk + statistisk validert». Bootstrap validerer kun bindingstids*fordelingen* gitt q=2; selve q=2 er prosedyreforankret (rapporten sier dette korrekt i §8.3.4). CLAUDE.md krever at antagelser ikke fremstilles som verifiserte fakta.
→ Endre etikett til f.eks. «Forankret antagelse; bindingstidsfordeling empirisk + bootstrap-kvantifisert».

**3B-9. «Natt/helg (c=2)»-kolonnen aggregerer tre skifttyper.** Kolonnen omfatter også dag/helg (c_eff=2, høyest λ=2,06), men omtales konsekvent som «natt/helg». Et styre kan feilaktig tidfeste +1-tiltaket til natt.
→ Presiser kolonneetikett/fotnote («c_eff=2-skift: natt + helg dag») eller vis dag/helg som egen rad. (Flagget også i din egen `peer_review_selvevaluering.md` linje 58.)

**3B-10. RQ5 gjengis ulikt i kap1 vs kap10.** kap1 §1.3 (åpent «hvilke forhold», inkl. «klassifiseringspraksis») vs kap10 §10.2 (ja/nei-form, «klassifiseringspraksis» droppet – nettopp variabelen svaret handler om).
→ Gjengi RQ5 ordrett identisk i kap10. Kontroller RQ1–RQ4 samtidig.

### 3C. Mindre avvik (bør, men ikke kritisk)
- 9,6× (kap8) vs 10× (kap9/kap10) for Finnmark/Oslo-volum (faktisk 9,65). Standardiser.
- Tabelltitler «Kapasitetsnivåer i operativ tilpasningsmodell» (Tabell 6.2, 7.2) bruker et modellnavn som ikke er definert ellers; resten sier «prosedyrebasert ankomstkonfliktmodell». Harmoniser.
- D-aba Fase 2 nedre grense: «17 til 37 %» (§5.6.1) vs «8,7 til 37 %» (§6.4.5/§7.4.3). 17 ≈ 5-min-verdien, ikke nedre grense.
- Sammendrag: «Funnene er robuste mot variasjon i modellantagelser» overclaimer for dag-funnet (sensitivitetsbånd 15–34 % på dag). Avgrens til natt/helg.

---

## 4. Pensumsamsvar (KML-kompendiet) – krav 2

**Sterkt samsvar.** Rapporten bruker pensumets køteori korrekt og slik kompendiet lærer den: Kendall-notasjon (M/M/c), Erlang-C-formelen og halefordelingen P(W>t) identisk med kompendiets ligninger, A=λ/μ, ρ=A/c, stabilitet ρ<1, de fem M/M/c-forutsetningene eksplisitt vurdert, Erlang-A (frafall/overløp), P-K/variasjonskoeffisient-effekten, sensitivitets-/scenarioanalyse. Rapporten går faglig **lenger** enn pensum (multiserver-jobs, op-binder-semantikk) **uten å motsi det**. Ingen reelle motsigelser mot pensum.

**Pensum-foreskrevne metoder som mangler (ikke må-krav, men styrker):** formell test av Poisson-antagelsen (KS/χ² – pensum Steg 2; i dag eksplisitt ikke testet, §5.6.3), DES-validering av primærmodellen (pensumets foreskrevne metode for ikke-markovske systemer), Littles lov som sanity-sjekk på n_aktive, og kostnad-vs-service-dimensjonering (max(c_serv, c_kost)). Se del 6.

---

## 5. Figurer – krav 11

**Mengden er akseptabel, men i nedre sjikt** (6 figurer på ~30 400 ord, sterkt konsentrert i kap 8). Du er ferdig, så kun det som virkelig løfter formidlingen er listet.

> **Korreksjon (verifisert):** Primærresultatet er **allerede visualisert** i **Figur 8.2** (`total_belastning_A_vs_B.png`, kap8 §8.3 linje 152), som viser variant A vs B for begge skifttyper. Den opprinnelige anbefalingen om en egen «primærresultat»-figur var derfor delvis overflødig. De foreslåtte kandidatfilene `kap_fig1_nivaa_basis.png` og `kapasitet_v4_med_skjulte.png` er dessuten **utdaterte for dagens modell** (viser natt/helg-svikt rundt 23,5 % / eldre basisvariant, ikke 32,6 %) og må **ikke** brukes.

**Eneste reelle «bør»:**
1. **Erlang-C-paradokset** (ρ<6 % vs svikt ~33 %) – rapportens retoriske kjerne (sammendrag, §9.1.1, §10.5), vises aldri visuelt. Må eventuelt regenereres (ny enkel figur), ikke hentes fra eksisterende filer.

**Kjekt å ha (ikke nødvendig):** én nasjonal benchmarking-figur i §8.5 (`analyse/figurer/nasjonal_*`), Poisson-test-figur (`EDA_fig6_poisson.png`) i §5.6.3, døgnprofil λ (`EDA_fig2_lambda_vakttype.png`).

Konklusjon: rapporten er **forsvarlig som den er** på figursiden. Hvis du legger til én figur, lag en Erlang-C-paradoks-figur. **Enhver ny resultatfigur må regenereres fra `analyse/total_belastning_oppsummering.csv`** – ikke gjenbruk de gamle `kap_fig*`/`kapasitet_v4`-filene, som tilhører en tidligere modellversjon.

---

## 6. Anbefalt restanalyse før rapporten er «gjennomgått så grundig som mulig» – krav 7

**Påkrevd før innlevering (ingen ny data):** rett alle punkter i del 3A og 3B.

**Anbefalt (styrker etterprøvbarhet og lukker tallspriket ved kilden):**
1. **Innfør deterministisk tie-break/samtidighetsregel i `kjor_sweep`** (sekundær sorteringsnøkkel eller stabil sortering) i `konflikt_total_belastning.py` *og* `scenario_pluss1.py`/bootstrap-skriptet, slik at 32,6/32,8-spriket (3B-2) forsvinner i datagrunnlaget i stedet for å forklares i fotnote. Regenerer Tabell 8.1/8.2/8.6 fra den deterministiske kjøringen.
2. **Regenerer Tabell 8.4 programmatisk fra `total_belastning_oppsummering.csv`** for å eliminere foreldede celler (3B-1) – og legg gjerne inn en enkel script-sjekk som feiler hvis tabell ≠ CSV.
3. **Rapporter Svikt-andelen både for observerte anrop (D-pri1+D-aba) og full base** (3B-6), så estimert-andelens effekt på 32,6 % er synlig.
4. **Formell Poisson-test** (KS/χ²) på mellomankomsttider for Erlang-C-grunnlinjen (pensum Steg 2; R2/R3 i risikoregisteret).
5. **Verifiser NENA (2020)-selverkjennelsen** (3A-8). (3A-12: manglende PDF-er er nå lastet ned og verifisert, se 3A-12.)

**Valgfritt (videre arbeid, ikke for denne innleveringen):** DES-validering av primærmodellen; Littles lov-sanity-sjekk; kostnad-vs-service-dimensjonering.

---

## 7. Git og struktur – krav 9, 10

- `.gitignore` oppdatert: KML-kompendium og LOG650Vault holdes utenfor git (verifisert med `git check-ignore`). **(9 ✓)**
- Ubrukte kilder flyttet til `003 references/ikke_brukt/` (git-sporet rename, historikk bevart). **(8 ✓)**
- Endringene i denne runden (språk, bibliografi-metadata, .gitignore, filflytting, denne review.md, regenerert PDF) er commitet og pushet. **(10 – se commit)**
- **Merk:** flere av de flyttede ubrukte PDF-ene er kanoniske kilder fra prosjektets vault (burst-modell `32` (dublett av brukt `10`), brannstudien `20`, SAMLOK `25`, NASA-TLX `42`/`51`). De er ikke sitert i rapporten nå – bekreft at det er bevisst.

---

## 8. Bibliografi-helse (krav 1, oppsummert)
- Alle 48 bibliografioppføringer er sitert i teksten; ingen usiterte oppføringer, ingen siteringer uten oppføring, ingen brutte koblinger.
- 40 brukte kilder med PDF ble åpnet og verifisert (metadata + faktisk bruk). De fleste er korrekte; avvikene er listet i 3A og 2.2.
- Hovedmønsteret i feilene: rapporten parafraserer/ekstrapolerer kilder presist på substans, men **strammer formuleringen for hardt** («finner», «viser», «dokumenterer», ordrette anførselstegn) der kilden er svakere eller sier noe annet. Gjennomgå spesielt verb og anførselstegn ved kildebruk.
