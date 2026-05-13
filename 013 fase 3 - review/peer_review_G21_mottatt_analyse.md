# Peer review fra G21 — gap-analyse og handlingsliste

| Felt | Innhold |
|---|---|
| **Vurderende gruppe** | G21 — Elisabeth K. Orlien og Kaylee Floden |
| **Gruppe vurdert** | G20 — Rune Grødem |
| **Tittel** | Kapasitetsstyring og bemanningsdimensjonering ved norske 110-sentraler — En analyse av operatørkapasitet med prosedyrbasert ankomstkonfliktmodell |
| **Sider rapport** | 79 |
| **Dato G21s vurdering** | 03.05.2026 |
| **Dato denne analysen** | 2026-05-12 |
| **Kilde-PDF** | `Peer_review_G21_til_G20_mottatt_2026-05-03.pdf` (denne mappen) |

## 0. Helhetsinntrykk fra G21 og hvordan det skal tolkes

G21s overordnede vurdering er klar og samlet:

> «Rapporten presenterer en ambisiøs og faglig sterk analyse … Samtidig fremstår analysen som metodisk sårbar, da modellen bygger på flere antakelser som er delvis empirisk basert, men hvor videre anvendelse i begrenset grad er validert. Dette gjør det uklart hvor robuste resultatene faktisk er. Videre fremstår generaliserbarheten utover caset som svakere underbygget enn det som antydes, særlig ettersom modellen ikke er testet på andre datasett eller sentraler. Språket er til tider komplekst, noe som reduserer klarheten.»

Tre overordnede strenger går gjennom hele reviewen:

1. **Usikkerhet er ikke integrert i resultatpresentasjonen.** Tall som 32,6 % Svikt og scenario +1 op presenteres som relativt definitive funn selv om de hviler på antagelser. Sensitivitetsanalysen i Tabell 7.10 dekker dette teknisk, men ikke kommunikativt.
2. **Generaliseringstone er sterkere enn ett case kan bære.** Bekymringen gjelder kap 7.9 (nasjonal benchmarking), 8.3.4–8.3.5 (implikasjoner for bemanningsstandarder) og 9.3–9.4 (konklusjon og anbefalinger).
3. **Språk og lesbarhet drar ned helhetsinntrykket.** Lange setninger, kompakt begrepsbruk, inkonsekvent terminologi («110-sentraler»), forkortelser ikke alltid definert, figurer/tabeller dårlig integrert i argumentasjonen.

Disse tre strengene er gjennomgående. Punkt-for-punkt nedenfor er konkretisering, ikke nye temaer.

## 1. Innledning (kap 1)

**G21s styrker:** Bakgrunn og kontekst kommer godt fram (1.1–1.2). Problemstillingen er klart formulert og operasjonalisert i RQ1–RQ5 (1.3). Studiens betydning er godt begrunnet.

**G21s forbedringspunkter:**

| # | G21s kritikk | Status pr. 2026-05-12 | Handling |
|---|---|---|---|
| 1.A | For omfattende og kompleks; deler av 1.1–1.2 ligger «tett opp mot analyse og diskusjon» | Åpen. Selvevalueringen 1. mai flagget det samme indirekte. | Kortere 1.1–1.2. Flytt analytiske refleksjoner til kap 4/8. |
| 1.B | Sterke påstander tidlig uten tilstrekkelig underbygging | Åpen. | Identifiser de tre–fire sterkeste påstandene i 1.1–1.2 og enten dempe formuleringen eller legg til kort kildebelegg. |
| 1.C | Begrepsbruken i 1.4 er kompakt; krevende å følge fra start | Åpen. 1.4 nomenklaturtabellen er bevart som kompakt referanse. | Vurder å splitte tabell 1.4 i to: én introduseres nå (D-pri1, D-aba, L-aba, op-binder, c_eff), én gradvis i kap 4–6. Eventuelt: kortere tabell + utvidet versjon i Vedlegg. |
| 1.D | Lange og sammensatte setninger reduserer lesbarheten | Åpen. | Språkrevisjon — se hovedtema 3 nedenfor. |

## 2. Litteratur og teori (kap 2 og 3)

**G21s styrker:** Faglig sterk dekning av køteori og kapasitetsanalyse (2.2–2.3). Kombinasjonen klassisk (Erlang-C) + avansert (multiserver-jobs, team-basert) er relevant. Kunnskapsgap-identifikasjonen i 2.6 er tydelig.

**G21s forbedringspunkter:**

| # | G21s kritikk | Status pr. 2026-05-12 | Handling |
|---|---|---|---|
| 2.A | Kap 2.2–2.3 er deskriptiv — litteraturen presenteres uten kritisk vurdering av relevans og begrensninger | Åpen. | Legg inn 1–2 setninger per hovedkilde som vurderer hva metoden gjør godt og hvilke begrensninger den har for 110-konteksten. |
| 2.B | Teoretiske hull kobles først tydelig til modellvalget i 2.6 — sent | Åpen. | Lag korte forhåndssignaler i 2.2 og 2.3 om at «denne tradisjonen håndterer ikke makkerpar-binding/op-binder-semantikk → se kap 2.6». Alternativt: omplasser deler av 2.6 inn i 2.2/2.3 som delavslutninger. |
| 2.C | Kompakt og begrepstung framstilling — vanskelig å skille sentralt fra mindre relevant | Åpen. | Marker tre kanoniske kilder eksplisitt (Chelst & Barlach 1981; Harchol-Balter 2022; Gustavsson 2018). Andre kilder tones ned. |
| 2.D | Kilder vektlagt likt selv om betydningen for metodevalget varierer | Åpen. | Vurder visuelt: kort tabell i 2.6 der hver kilde får en kolonne «Direkte bidrag til modell» / «Bakgrunnsstøtte». |

Merknad: Penverne et al. (2024) er allerede flyttet inn i kap 2.3 (gjort etter selvevaluering 1. mai). Dette punktet er lukket fra selvevalueringen, men G21s bredere kritikk om analytisk grep står fortsatt åpen.

## 3. Metode (kap 5)

**G21s styrker:** Gjennomarbeidet, god sammenheng mellom forskningsdesign, data og analyse. Reelle operasjonelle data (LEO/BRIS). Validitet, reliabilitet og etikk inkludert insider-perspektivet behandlet eksplisitt i 5.6–5.7.

**G21s forbedringspunkter:**

| # | G21s kritikk | Status pr. 2026-05-12 | Handling |
|---|---|---|---|
| 3.A | Sentrale analyser bygger på antagelser som er *delvis* empirisk basert, men hvor videre anvendelse er begrenset validert — særlig bindingstider og klassifisering (5.3–5.4) | Åpen. LABA n=100 ga CI [3,74; 5,43] for L-aba. Andre bindingstider (S, F, V, L-hendelse, L-ukjent) er ekspert-anslag uten empirisk validering. | Eksplisitt avsnitt sist i 5.4 eller i 5.6 som listene hvilke bindingstider som er empirisk validert vs. anslått, og hvilken konsekvens dette har for hvilke resultater. Reflekteres så i resultatpresentasjon (se 4.A). |
| 3.B | Konsekvenser av antagelsene er ikke tilstrekkelig problematisert | Åpen. | Hver hovedantagelse (A1–A8 i Tabell 6.3) bør ha eksplisitt «Konsekvens hvis feil»-kolonne eller setning. |
| 3.C | Uklarhet rundt hvordan sammenstilling av anrop til oppdrag påvirker datagrunnlaget (5.3.4) — kan gi systematiske skjevheter | Delvis. Sekvensgap-forbehold lagt inn i 5.3.4 etter selvevalueringen — men kun som disclaimer, ikke systematisk skjevhetsdrøfting. | Utvid: hvilken retning trekker skjevheten? Overestimert eller underestimert kapasitet? Numerisk illustrasjon hvis mulig (hvor mye av 18 901 sekvensgap kunne realistisk vært overflyt vs. sammenstilling?). |
| 3.D | Validitet og reliabilitet er mer beskrivende enn kritisk | Åpen. | Reformuler 5.6: hva er konkrete trusler mot intern validitet, ekstern validitet, konstruktvaliditet — ikke kun beskrivelse av at de er vurdert. |
| 3.E | Insider-bias er identifisert, men i begrenset grad metodisk håndtert | Åpen. | Konkretiser hvordan tolkninger er kontrollert: triangulering med BRIS-data, blind tolkning fra annen lokal operatør, eller eksplisitt erkjennelse av begrensningen. |

## 4. Analyse og resultater (kap 7)

**G21s styrker:** Godt strukturert, logisk progresjon fra grunnleggende køteori til V3-modellen. Internt konsistente resultater. Scenarioanalyse og sensitivitetsanalyse styrker robustheten.

**G21s forbedringspunkter:**

| # | G21s kritikk | Status pr. 2026-05-12 | Handling |
|---|---|---|---|
| 4.A | Resultater (særlig Svikt-tilstand, 7.5) presenteres mer presist enn datagrunnlaget tilsier — usikkerheten i modellens antagelser integreres ikke i resultatene | **Åpen — dette er G21s mest substansielle punkt.** Tabell 7.10 har scenariosensitivitet (lav/hoved/høy = 28,1 / 33,2 / 38,5 %), men hovedtallet 32,6 / 33,2 % presenteres i resten av kapittelet uten bånd. | Hver gang Svikt-tallet presenteres (7.5, 7.6, 7.7, Funn 1–4): vis båndet, ikke punktestimat. Format: «33,2 % (lav–høy: 28–39 % under variant B-scenariobånd)» |
| 4.B | Samme gjelder scenarioanalysen (7.6): +1 op halverer Svikt 33 → 17 % — for definitivt formulert | Åpen. | Reformuler som «scenarioet indikerer at +1 op vil halvere Svikt under nåværende antagelsesgrunnlag; effekten er robust mot parametervariasjon i Tabell 7.10, men ikke validert mot historisk bemanningsendring». |
| 4.C | Det er ikke videreført i analysekapittelet hva modellen *faktisk måler* operasjonelt — selv om dette er diskutert i 6.4.8 | Delvis. Kap 7.4.1–7.4.2 forklarer kategorisering, men ikke koblet eksplisitt til hva tallene betyr operasjonelt. | Innledningsavsnitt til 7.5: «Svikt 32,6 % betyr at i 32,6 % av beredskapsanropene var det ingen ledig operatør for makkerpar-binding ved ankomsttidspunktet. Det betyr IKKE at anropet ble ubesvart — VL kan tre inn, kvalitet reduseres, eller overflyt til Agder. Modellen måler om driftsstandarden ble brutt, ikke om tjenesten brøt sammen.» |
| 4.D | Analysen er basert på ett case, samtidig som det trekkes bredere implikasjoner (kap 7.9) — svekker generaliseringsgrunnlaget | Åpen. | I 7.9 (nasjonal benchmarking): tydeliggjør at dette er kontekstualisering, ikke validering av modellen. Reformuler «implikasjoner» som «åpne forskningsspørsmål». |

## 5. Diskusjon (kap 8)

**G21s styrker:** God faglig refleksjon, kobler funnene til teori og operativ praksis. Erlang-C-begrensninger diskuteres mot empiriske funn. Makkerpar-logikken brukes aktivt.

**G21s forbedringspunkter:**

| # | G21s kritikk | Status pr. 2026-05-12 | Handling |
|---|---|---|---|
| 5.A | Diskusjonen er til tider **ensidig og bekreftende for egen modell** (særlig 8.1 og 8.3) | **Åpen — dette er G21s nest mest substansielle punkt.** | Legg inn alternative tolkninger eksplisitt: hva ville en konvensjonell Erlang-C-analytiker sett som svar? Hvor kunne modellen være feil? Drøft eksplisitt scenarioer der V3 underestimerer eller overestimerer kapasitet. |
| 5.B | Erlang-C-kritikken er faglig begrunnet, men fremstår kategorisk; begrenset drøfting av alternative anvendelser eller tolkninger | Åpen. | Avsnitt i 8.1 eller 8.2: «Erlang-C er fortsatt nyttig for samtaledimensjonering der makkerpar ikke er prosedyrekrav (f.eks. allmenne kundesentre). Begrensningen gjelder spesifikt 110-konteksten med makkerpar-binding.» |
| 5.C | Alternative forklaringer på resultater og situasjoner der modellen kan være mindre treffende — i liten grad diskutert | Åpen. | Hva hvis svikt 33 % skyldes registreringskonvensjoner i BRIS, ikke faktisk kapasitetspress? Hvis VL i praksis tar 30 % av nødanrop (ikke 0 % som modellen antar)? Hvis sammenstilte anrop er overestimert? Drøft 2–3 slike alternative tolkninger. |
| 5.D | Begrensninger (8.4) er ikke tilstrekkelig integrert i selve drøftingen av funnene | Åpen. | To grep: (i) flytt enkelte begrensninger inn som hørbarheter under hvert hovedfunn i 8.2–8.3; (ii) gjør 8.4 til en oppsummering av allerede løpende drøftede punkter, ikke en separat liste. |
| 5.E | Brede implikasjoner i 8.3.4–8.3.5 — bemanningsstandarder — ikke fullt støttet av ett case | Åpen. | Reformuler implikasjonene som hypoteser: «hvis funnene fra Sør-Vest skulle gjelde andre sentraler, kunne det implisere …». Skill empiri fra implikasjon eksplisitt. |

## 6. Konklusjon (kap 9)

**G21s styrker:** Konsis oppsummering, besvarer problemstilling og RQ-er. Studiens bidrag fremheves. Knytter funn til behov for kvantitativ tilnærming.

**G21s forbedringspunkter:**

| # | G21s kritikk | Status pr. 2026-05-12 | Handling |
|---|---|---|---|
| 6.A | Konklusjonen er mer generell og definitiv enn datagrunnlaget støtter — særlig 9.3–9.4 | Åpen. Selvevalueringen 1. mai flagget tilsvarende for 9.4 punkt 4. | Tone ned 9.3 og 9.4 — case-baserte funn, hypotetiske implikasjoner. |
| 6.B | Generaliseringer er for sterke; modellen er ikke testet på andre sentraler/datasett | Åpen. | Tydeliggjør i hver setning som peker mot nasjonalt nivå at det er en hypotese, ikke et funn. |
| 6.C | Refleksjon rundt begrensninger/usikkerhet er i liten grad integrert i konklusjonen — svekker balansen | Åpen. | Legg inn 2–3 setninger i 9.5 eller eget kort avsnitt om hva som *ikke* kan konkluderes på grunnlag av studien. |

## 7. Skriveflyt, formelle aspekter, helhetsvurdering

**G21s styrker:** Tydelig og logisk struktur. Faglig presist språk. Forankret i relevant litteratur. Begreper, modeller, referanser stort sett konsistent. Høy originalitet i problemstilling og metodisk tilnærming.

**G21s forbedringspunkter:**

| # | G21s kritikk | Status pr. 2026-05-12 | Handling |
|---|---|---|---|
| 7.A | Skriveflyten er tung — lange og komplekse setninger særlig i teori-, metode- og analysedeler | **Åpen — dette krever en hel runde med språkrevisjon.** | Mål: gjennomsnittlig setningslengde under 25 ord i kap 3, 5 og 7. Bryt sammensatte setninger med semikolon og tankestreker. |
| 7.B | Inkonsekvent begrepsbruk — særlig i skrivemåten av sentrale begreper som «110-sentraler» | Åpen. | Søk og standardiser: «110-sentral», «110-sentralen», «110-sentraler», «110 Sør-Vest» — velg én skrivemåte per kontekst og bruk gjennomgående. |
| 7.C | Forkortelser ikke alltid tydelig definert eller konsekvent brukt | Åpen. | Lag forkortelsesliste først i rapporten eller i Vedlegg, definert ved første forekomst per kapittel: RØD/GUL/GRØNN, MOB, BRIS, LEO, ABA, ISM, VL, c_eff, op-binder, D-pri1, D-aba, L-aba, L-hendelse, L-ukjent. |
| 7.D | Kobling mellom tekst og figurer/tabeller er ikke alltid klar — det fremgår ikke tydelig hvordan de støtter argumentasjonen | Åpen. | Hver figur og tabell skal introduseres med en aktiv setning i brødteksten som forklarer *hva leseren skal se*, ikke bare *at det vises*. |

## 8. Sammenfattet: prioritert handlingsliste

Rangert etter G21s vekt og effekt på sluttinntrykket. Estimat for arbeidsmengde gitt 19 dager til innlevering 31. mai.

| Prioritet | Handling | G21-punkter | Estimat |
|---|---|---|---|
| **P1** | Integrer usikkerhet i resultatpresentasjon (scenariobånd ved hovedtall i kap 7.5–7.7) | 4.A, 4.B | 1–2 dager |
| **P1** | Tone ned generalisering i kap 7.9, 8.3, 9.3–9.4 | 4.D, 5.E, 6.A, 6.B | 1 dag |
| **P1** | Balansert diskusjon: alternative tolkninger, Erlang-C mindre kategorisk, begrensninger integrert løpende | 5.A, 5.B, 5.C, 5.D | 1–2 dager |
| **P1** | Språkrevisjon: setningslengde, «110-sentral»-standardisering, forkortelser, figur/tabell-integrering | 1.D, 7.A, 7.B, 7.C, 7.D | 2–3 dager |
| **P2** | Konsekvens-kolonne for antagelsene (kap 5.4, Tabell 6.3) | 3.A, 3.B | 0,5 dag |
| **P2** | Sekvensgap-skjevhetsdrøfting i 5.3.4 | 3.C | 0,5 dag |
| **P2** | Validitet/reliabilitet skarpere i 5.6 | 3.D, 3.E | 0,5 dag |
| **P2** | Innledning strammere (1.1–1.2), 1.4 gradvis begrepsintroduksjon | 1.A, 1.B, 1.C | 0,5 dag |
| **P2** | Konklusjon nøkternere, integrert begrensningsdrøfting (9.3–9.5) | 6.C | 0,5 dag |
| **P3** | Litteraturkapittel mer analytisk (kritisk vurdering pr. kilde, tidligere metodebro) | 2.A, 2.B, 2.C, 2.D | 1 dag |
| **P3** | Hva modellen faktisk måler — tydeligere i 7.5-innledning | 4.C | 0,5 dag |

Totalt P1 + P2 + P3: ca. 9–12 dager. Med språkrevisjon som tidligst kan starte etter strukturelle endringer, blir realistisk ferdigstilling ca. 13–14 dager. Margin på 5–6 dager til administrative skjema, PDF-bygging, korrekturlesing.

## 9. Forhold til selvevaluering 1. mai

Selvevalueringen `014 fase 4 - report/peer_review_selvevaluering.md` ble skrevet 1. mai — to dager før G21s review (3. mai). G21s review og selvevalueringen overlapper, men de er ikke identiske:

| Tema | Selvevaluering 1. mai | G21 3. mai | Status |
|---|---|---|---|
| Tabell 7.10 transparens (samlet variasjon) | Eksplisitt nevnt | Implisitt i 4.A | Delvis adressert i revisjon 1 |
| Tallavvik 61 964/61 934 | Eksplisitt nevnt | Ikke nevnt | Adressert i revisjon 1 |
| Penverne flyttet til kap 2 | Eksplisitt nevnt | Ikke nevnt | Adressert i revisjon 1 |
| Konsolidering kap 4/5/6 | Eksplisitt nevnt | Ikke nevnt | Åpent |
| 8.3.6 «To kapasitetsproblem» | Eksplisitt nevnt | Ikke nevnt | Åpent |
| Usikkerhet integrert i resultater | Indirekte (Funn 4 stokastisk støy) | **Hovedpunkt** | Åpent |
| Generaliseringstone | Bare for kap 1 og 9.4 | **Hovedpunkt på tvers (7.9, 8.3, 9.3-9.4)** | Åpent |
| Balansert diskusjon | Begrensning i kap 8.4 strammere | **Hovedpunkt** | Åpent |
| Språk og setningslengde | Ikke nevnt | **Hovedpunkt** | Åpent |
| Standardisering «110-sentral» | Ikke nevnt | Eksplisitt | Åpent |

G21 traff de tre tyngste strukturelle problemene som selvevalueringen bare snittet rundt: usikkerhet i framstilling, generaliseringstone, og språk. Det er disse som må prioriteres i revisjon 2.

## 10. Filer som mest sannsynlig må endres

| Fil | Hovedendringer |
|---|---|
| `_forside_og_kap1.md` | 1.A, 1.B, 1.C, 1.D — innledning stramme, begreper gradvis |
| `kap2_litteratur.md` | 2.A, 2.B, 2.C, 2.D — kritisk vurdering pr. kilde, metodebro tidligere |
| `kap3_teori.md` | 7.A — språkrevisjon |
| `kap5_metode_data.md` | 3.A–3.E, 7.A — antagelsesproblematisering, validitetskritikk, sekvensgap-skjevhet, språk |
| `kap6_modell.md` | 3.B — konsekvens-kolonne i Tabell 6.3 |
| `kap7_analyse_resultater.md` | 4.A, 4.B, 4.C, 4.D, 7.A, 7.D — scenariobånd, generaliseringstone, modellens målegrep, språk, figur-/tabellintegrering |
| `kap8_diskusjon.md` | 5.A, 5.B, 5.C, 5.D, 5.E — balansert diskusjon, alternative tolkninger, Erlang-C nyansert, begrensninger integrert |
| `kap9_konklusjon.md` | 6.A, 6.B, 6.C — nøkternere, begrensninger inn |
| Alle kapitler | 7.B, 7.C — terminologi standardisert, forkortelser definert |

## 11. Hva G21 *ikke* påpekte men selvevalueringen tok opp

G21 nevner ikke følgende selvevaluerings-punkter:

- Konsolidering av overlapp mellom kap 4.2.2 / 6.4.4 / 7.4.2 (makkerpar-tidslinjen)
- Konsolidering av klassifisering mellom 5.3.2 / 6.2 / 7.4.1
- Antagelse-nummerering (Metodeforbehold N.M vs A1–A8)
- Egen underseksjon 8.3.6 «To ulike kapasitetsproblem»
- Tallavvik 61 964 / 61 934 og 18 901 / 18 930 (allerede lukket)
- Variant A oppsplittet per skifttype
- Kø-effektivitet vs prosedyre-sikkerhet introdusert tidligere

Disse er valgfrie, men selvevalueringen identifiserte dem som svake punkter. Vurder å lukke dem hvis tid tillater etter at G21s hovedpunkter er adressert.
