# 6. Modell

## 6.1 Modellutvikling og metodisk begrunnelse

Prosjektet gjennomgikk en metodisk utvikling i tre faser. Alle tre faser er dokumentert fordi utviklingen i seg selv er analytisk informativ: overgangen fra Erlang-C til prosedyrbasert modell er ikke et teknisk valg, men en konsekvens av at den operative virkeligheten ved 110-sentraler bryter med M/M/c-modellens kjerneforutsetning om uavhengige, parallelle servere.

| Fase | Modell | Målmetrikk | Konklusjon |
|---|---|---|---|
| 1 | Erlang-C (M/M/c) | P(W > t), ρ | ρ < 6 % for alle skifttyper — kapasiteten ser komfortabel ut |
| 2 | Simultanitetsanalyse | P(≥ k aktive hendelser simultant) | Lav konfliktrate — men makkerpar-logikk ikke inkludert |
| 3 | Prosedyrbasert ankomstkonfliktmodell | P(brudd på driftsstandard ved ankomst) | Strukturelt kapasitetsgap — **primærmodell** |

Overgangen fra Fase 1 til Fase 3 er ikke en forkasting av køteoretisk metode, men en utvidelse: modellen spesifiserer hva som faktisk er en «opptatt server» i 110-kontekst, og svarer på et mer presist spørsmål enn Erlang-C kan formulere.

Modellrammeverket er utviklet med 110 Sør-Vest som case, men er prinsipielt overførbart til enhver 110-sentral. Det sentrale er ikke de eksakte prosentverdiene i denne studien, men metoden for å identifisere hvor ofte en ny hendelse ankommer i en tilstand der tilgjengelig operatørkapasitet allerede er bundet. Andre sentraler kan anvende samme logikk dersom de har data for ankomsttidspunkt, ressursvarsling og en proxy for akuttfasens varighet.

---

## 6.2 Klassifisering av henvendelser etter operativ binding

Dimensjonering av nødmeldesentraler kan ikke baseres på samlet telefonvolum alene. Det avgjørende er hvor mange henvendelser som på et gitt tidspunkt binder operatørkapasitet på en måte som reduserer evnen til å håndtere nye prioriterte hendelser. For å analysere dette skilles det mellom fire kategorier ut fra hvordan henvendelsene binder operatørkapasitet:

**Kategori A: Lavprioritert eller avbrytbar last.** Service-, test- og administrative henvendelser. Kategori A er normalt ikke alene dimensjonerende for grunnbemanning, men representerer likevel bakgrunnsbelastning som kan redusere den operative bufferen i perioder med høyt trykk.

**Kategori B: Reelle hendelser uten utrykning.** Saker med initiell hendelsestype der 110 foretar vurdering, avklaring eller rådgivning uten å sende ressurser. Selv om disse ikke utløser callout, beslaglegger de operatørkapasitet og er operative hendelser i beredskapsmessig forstand.

**Kategori C: Tidskritiske avklaringshendelser.** Typisk automatiske brannalarmer (ABA), der sentralen i en kort tidsperiode må avklare om hendelsen skal eskalere til utrykning. Slike hendelser kan også generere tilleggsanrop fra stedet og dermed binde mer kapasitet enn én synlig hendelse tilsier.

**Kategori D: Utrykningshendelser.** Hendelser med ressursvarsling og callout. Dette er den mest kritiske og tydelig observerbare kategorien, og den som i størst grad utløser samtidig RØD- og GUL-binding i akuttfasen.

I den foreliggende analysen kvantifiseres primært kategori D, fordi denne kan identifiseres robust i datasettet gjennom ressursvarsling og tidspunkt for første ressurs fremme. Dette gir et godt mål på den mest kritiske og dimensjoneringsrelevante delen av operatørbindingen, men innebærer samtidig at samlet operativ belastning sannsynligvis undervurderes. Kategori B, C og sammenstilte tilleggsanrop (se avsnitt 7.2) er operativt relevante, men lar seg ikke modellere like robust med det foreliggende datagrunnlaget.

### Sentrale begreper: anrop, oppdrag og hendelse

En sentral metodisk distinksjon i analysen er skillet mellom **anrop**, **oppdrag** og **hendelse**:

- **Anrop:** En faktisk innkommende telefon eller varsling til sentralen. Hvert anrop opptar en operatør.
- **Oppdrag:** En registrert sak i LEO/BRIS. Flere anrop kan bli sammenstilt i ett oppdrag.
- **Hendelse:** Den faktiske operative situasjonen som sentralen håndterer. Én hendelse kan generere flere innkommende anrop fra ulike innringere.

I praksis kan én hendelse generere flere anrop, mens disse anropene i statistikken sammenstilles i ett eksisterende oppdrag. Operatørkapasitet bindes dermed av flere anrop enn det antall synlige oppdrag alene tilsier. Denne asymmetrien mellom synlige oppdrag og faktisk operatørbinding er et gjennomgående metodisk poeng i analysen (se avsnitt 7.2).

---

## 6.3 Fase 1: Erlang-C (M/M/c) — grunnlinje og begrensninger

### 6.3.1 Modellparametere

M/M/c-modellen (Erlang-C) er spesifisert med følgende parametere for 110 Sør-Vest:

| Symbol | Beskrivelse | Verdi / kilde |
|---|---|---|
| λ | Ankomstrate beredskapsanrop [anrop/time] | Estimert per skifttype fra LEO/BRIS 2025 |
| μ | Servicerate [anrop/time] = 1 / E[samtaletid] | Vektet gjennomsnitt: 3,44 min⁻¹ (intervjudata) |
| c_eff | Effektive servere = c_total − 1 (VL-korreksjon) | Dag/hverdag: 3; øvrige skift: 2 |
| ρ | Systemutnyttelse = λ / (c_eff · μ) | Se Tabell 6.1 |
| T | Terskel for P(W > T) | 30 sek (automatisk overføring til Agder — bekreftet beredskapsanalyse s. 25) |

**VL-korreksjon:** Vaktlederen (VL) besvarer normalt ikke nødanrop (jf. prosedyre, avsnitt 4.2). Effektiv operatørkapasitet er derfor c_eff = c_total − 1 for alle skifttyper.

### 6.3.2 Erlang-C-formelen

Sannsynligheten for at et innkommende anrop må vente i kø (Erlang-C):

$$C(c, A) = \frac{A^c / (c! \cdot (1-\rho))}{\sum_{k=0}^{c-1} A^k/k! + A^c / (c! \cdot (1-\rho))}$$

der A = λ/μ er total tilbudt trafikk i Erlang og ρ = A/c er serverutnyttelsen.

Sannsynlighet for ventetid over terskel T:

$$P(W > T) = C(c, A) \cdot e^{-(c\mu - \lambda)T}$$

### 6.3.3 Resultater og begrensninger

**Tabell 6.1: Erlang-C resultater — 110 Sør-Vest 2025**

| Skifttype | λ (anrop/t) | c_eff | ρ | C(c,A) | P(W > 60s) |
|---|---|---|---|---|---|
| Dag / Hverdag | 2,57 | 3 | 4,9 % | 0,05 % | 0,02 % |
| Dag / Helg | 2,06 | 2 | 5,9 % | 0,66 % | 0,38 % |
| Natt / Hverdag | 1,18 | 2 | 3,4 % | 0,22 % | 0,13 % |
| Natt / Helg | 1,30 | 2 | 3,7 % | 0,27 % | 0,15 % |

*λ inkluderer kun beredskapsoppdrag (non-T1). P(W > 30s): automatisk overføring til Agder ved ubesvart anrop etter 30 sek (beredskapsanalyse s. 25), eller ved 10. anrop i kø.*

Erlang-C konkluderer med svært lav kapasitetsutnyttelse og nær null sannsynlighet for ventetid over 30 sekunder i alle skifttyper. Formelt er dette korrekt — men det er metodisk utilstrekkelig for 110-konteksten av fire grunner:

1. **Makkerpar-prinsippet og samtidig binding:** Den operative prosedyren definerer to operatører (RØD + GUL) som standard for én hendelse. Både RØD og GUL bindes fra samme tidspunkt: så snart RØD-operatøren besvarer nødanropet, går GUL-operatøren i medlytt for å bygge situasjonsforståelse og avhjelpe med lokalisering før utalarmering. To operatører er dermed opptatt fra første sekund. Erlang-C modellerer én server per anrop og fanger ikke denne samtidige bindingen. Ved samtidskonflikter — der ingen dedikert makker er tilgjengelig — må én operatør fylle både RØD- og GUL-funksjonen alene.

2. **Kapasitetsbinding utover samtaletid:** GUL-operatøren er bundet gjennom hele akuttfasen: først i medlytt under RØD-samtalen, deretter i aktiv koordinering — utalarmering av ressurser, sambandskommunikasjon med mannskap underveis, og delvis fortsatt medlytt. GUL forblir bundet frem til vindusmelding mottas om at første ressurs er fremme på stedet, pluss kvittering og loggføring (anslagsvis 3 minutter). Først etter dette er GUL delvis frigjort og kan håndtere flere gule hendelser parallelt i en mer sporadisk oppfølgingsfase. Denne totale bindingsperioden er vesentlig lenger enn selve samtaletiden, men Erlang-C behandler den som null.

3. **Uavhengige servere:** M/M/c forutsetter at servere er uavhengige. I 110-kontekst er operatørene dynamisk koblet gjennom prosedyrens rollestruktur — RØD og GUL er komplementære, ikke parallelle. Rollene er ikke faste: ved neste hendelse roterer operatørene, og den som nettopp var GUL kan bli RØD på neste anrop.

4. **Undervurdert ankomstrate:** Ankomstraten λ estimeres fra synlige oppdrag i BRIS/LEO. Som dokumentert i avsnitt 7.2 undervurderer dette faktisk innkommende anropsvolum med anslagsvis 23 %, fordi tilleggsanrop til eksisterende hendelser sammenstilles automatisk og ikke registreres som egne oppdrag. Dette innebærer at Erlang-C ikke bare undervurderer antall innkommende belastningsenheter, men også bygger på en datadefinisjon der én synlig sak kan skjule flere samtidige kapasitetsbindende anrop. Selv en perfekt M/M/c-modell ville derfor vært basert på et ufullstendig inputgrunnlag.

Konsekvensen er at Erlang-C gir et misvisende bilde av kapasitetstilstanden: en modell som sier «nesten ingen ventetid» er lite operasjonelt informativ i et system der det operative problemet ikke er kø i klassisk forstand, men mangel på ledig makker ved ankomst av ny hendelse.

---

## 6.4 Fase 3: Prosedyrbasert ankomstkonfliktmodell — primærmodell

### 6.4.1 Konseptuell ramme

Primærmodellen tar utgangspunkt i prosedyrens kapasitetslogikk og stiller et presist spørsmål:

> *I hvilken andel av beredskapsanropene ankommer anropet i en tilstand der den operative driftsstandarden (makkerpar) kan opprettholdes?*

Dette er en **prosedyrkonformitetsmetrikk** — ikke et ventetidsmål. Kapasitetsproblemet ved 110-sentraler er i de fleste tilfeller ikke at anrop venter i kø, men at de ankommer når operatørene allerede er bundet i aktive hendelser slik at makkerpar-prinsippet brytes.

### 6.4.2 Operativ tilpasningslogikk

Modellen bygger pa en sentral observasjon om hvordan operatorene faktisk tilpasser seg ved samtidskonflikter: **makkerparet splittes**. Nar et nytt anrop ankommer og begge operatorene allerede er bundet i en aktiv hendelse, bryter de makkerparet og fordeler seg slik at hver operator handterer sin hendelse solo. Denne tilpasningen er ikke et sammenbrudd -- det er den operative virkeligheten som gjor at tjenesten opprettholdes under press.

I den operative virkeligheten binder en aktiv hendelse normalt 2 operatorer (ROD + GUL), men ved samtidskonflikter splittes makkerparet slik at operatorene fordeler seg. Modellen teller derfor antall aktive hendelser mot tilgjengelig kapasitet for a avgjore om neste hendelse kan handteres med makkerpar (den operative virkeligheten, ikke prosedyrekravet om 2). Antall ledige operatorer ved et gitt tidspunkt er:

$$\text{ledige}(t_i) = c_{\text{eff}} - n_{\text{aktive}}(t_i)$$

der $n_{\text{aktive}}$ er antall hendelser med uutlopt bindingstid som fortsatt er aktive.

### 6.4.3 Kapasitetsnivaer

Basert pa antall ledige operatorer klassifiseres hvert innkommende anrop til ett av tre nivaer:

**Tabell 6.2: Kapasitetsnivaer -- operativ tilpasningsmodell**

| Niva | Definisjon | Betingelse | Operativ konsekvens |
|---|---|---|---|
| **Normal** | Makkerpar mulig for neste hendelse | ledige >= 2 | Full prosedyre, kvalitetssikret handtering |
| **Brudd pa driftsstandard** | Kun 1 ledig -- solo-handtering | ledige = 1 | Operatoren klarer det, men uten makker. Okt kognitiv belastning, okt feilrisiko |
| **Svikt** | Ingen ledig operator | ledige = 0 | VL ma overta eller overlop til Agder |

For a illustrere hva dette innebarer i praksis:

**Med c_eff = 2 (natt/helg):**

| Situasjon | Hva skjer operativt | Kapasitetsniva |
|---|---|---|
| 0 aktive hendelser, nytt anrop | Makkerpar handterer sammen (ROD + GUL fra forste sekund) | Normal |
| 1 aktiv hendelse, nytt anrop | Makkerparet splitter -- hver tar sin hendelse solo | Brudd pa driftsstandard |
| 2 aktive hendelser, nytt anrop | Begge operatorer allerede opptatt solo -- ingen kan ta anropet | Svikt |

**Med c_eff = 3 (dag hverdag):**

| Situasjon | Hva skjer operativt | Kapasitetsniva |
|---|---|---|
| 0 aktive, nytt anrop | Makkerpar + 1 gronn ledig | Normal |
| 1 aktiv, nytt anrop | 2 ledige -- makkerpar mulig for neste hendelse | Normal |
| 2 aktive, nytt anrop | Kun 1 ledig -- solo-handtering | Brudd pa driftsstandard |
| 3 aktive, nytt anrop | Ingen ledig | Svikt |

Den kritiske asymmetrien mellom c_eff = 2 og c_eff = 3 er at med c_eff = 2 er det kun ett steg fra normal drift til svikt: allerede ved andre samtidige hendelse er begge operatorene opptatt. Med c_eff = 3 finnes en buffersone der operatorene kan jobbe solo for svikt inntreffer.

### 6.4.4 Sammenstilte tilleggsanrop som belastningsenhet

En vesentlig utvidelse av modellen er inkludering av **skjulte/sammenstilte anrop** -- anrop som automatisk knyttes til eksisterende oppdrag i LEO/BRIS og ikke registreres som egne saker (se avsnitt 7.2).

#### Identifisering

Disse anropene identifiseres gjennom gap i sekvensnummereringen i 110_ID-feltet. Hvert synlige oppdrag har et daglig sekvensnummer (f.eks. B06-250101-4, B06-250101-6). Manglende sekvensnumre (i dette tilfellet -5) representerer anrop som ble sammenstilt med et eksisterende oppdrag.

Et viktig forbehold: sekvensgapet forteller at et anrop ble sammenstilt, men ikke *hvilket* oppdrag det ble knyttet til. Dersom de synlige oppdragene er -23, -26 og -29, kan de manglende numrene (-24, -25, -27, -28) i prinsippet alle tilhore oppdrag -23, eller de kan vaere fordelt pa ulike aktive oppdrag. For kapasitetsmodellen har dette imidlertid ingen betydning: det avgjorende er at en operator var opptatt med et anrop pa det aktuelle tidspunktet, uavhengig av hvilket oppdrag anropet ble registrert under.

#### Bindingstid

Sammenstilte anrop er typisk korte. Operatoren kjenner allerede hendelsen, og samtalen bestar normalt av en kort avklaring, bekreftelse pa at ressurs er pa vei, og sa legger innringer pa. Bindingstiden er i modellen satt til **1 minutt** som et kvalitativt estimat. Faktisk varighet kan variere: noen anrop kan vaere kortere (20-30 sekunder ved ren bekreftelse), andre noe lenger dersom innringer er stresset eller situasjonen har utviklet seg. Estimatet pa 1 minutt anses som rimelig konservativt for gjennomsnittet av slike anrop.

Selv om bindingstiden er kort, er den operative konsekvensen reell: operatoren er utilgjengelig for neste hendelse i det kritiske vinduet. I perioder med hoyt press kan det vaere nettopp dette korte anropet som vipper kapasiteten fra handterbart til svikt.

#### Modellparametere

I modellen behandles sammenstilte anrop som egne belastningsenheter med:
- **Tidspunkt:** Interpolert fra naermeste synlige oppdrags ankomsttidspunkt
- **Bindingstid:** 1 minutt (kvalitativt estimat, se over)

For 2025 er det identifisert 18 901 sammenstilte anrop (korreksjonsfaktor 1,305x). Disse legges til de 7 555 kategori D-hendelsene, slik at modellen totalt analyserer 26 456 belastningsenheter.

### 6.4.5 Matematisk formulering

La $\{t_i, d_i\}$ for $i = 1, \ldots, N$ betegne N belastningsenheter (beredskapsoppdrag + sammenstilte anrop) med ankomsttidspunkt $t_i$ og bindingstid $d_i$.

For hvert anrop $i$ beregnes:

$$n_{\text{aktive}}(t_i) = \left|\{j < i : t_j + d_j > t_i\}\right|$$

det vil si antall tidligere belastningsenheter hvis bindingstid enna ikke er utlopt ved $t_i$.

Kapasitetsniva for anrop $i$:

$$\text{Niva}(i) = \begin{cases}
\text{Normal} & \text{hvis } c_{\text{eff}} - n_{\text{aktive}}(t_i) \geq 2 \\
\text{Svikt} & \text{hvis } c_{\text{eff}} - n_{\text{aktive}}(t_i) \leq 0 \\
\text{Brudd} & \text{ellers (ledige} = 1\text{)}
\end{cases}$$

Bindingstid $d_i$ settes ulikt for de to typene belastningsenheter:
- **Kategori D:** $d_i$ = (Forste ressurs fremme -- Dato/tid anrop) + 3 min kvittering. Median 13,0 min.
- **Sammenstilt anrop:** $d_i$ = 1 min (kort avklaring).

### 6.4.6 Bindingstid-proxy for kategori D

Bindingstid-proxyen fanger den mest operative og dimensjoneringsrelevante fasen av hendelseshandteringen:

- **Akuttfasen er den mest tidskritiske:** Bade ROD og GUL bindes fra forste sekund. GUL gar umiddelbart i medlytt nar ROD besvarer anropet, for a bygge situasjonsforstaelse og avhjelpe med lokalisering. Deretter utalarmerer GUL ressurser, handterer samband og gir tidskritisk informasjon til mannskap underveis.
- **GUL forblir bundet til vindusmelding:** GUL-operatoren er bundet frem til vindusmelding mottas om at forste ressurs er fremme pa stedet. Etter kvittering og loggforing (anslagsvis 3 minutter) er GUL delvis frigjort.
- **Etter fremme stabiliseres driften:** Mange hendelser gar over i en mer stabil driftsfase med sporadisk belastning pa operatoren.

Av 7 555 kategori D-hendelser har 5 777 (76,5 %) registrert tidspunkt for forste ressurs fremme. De resterende tildeles median bindingstid. Observert fordeling: median 13,0 min, P90 21,6 min. Merk at bindingstiden representerer perioden der bade ROD og GUL er bundet parallelt -- ikke bare en av dem.

### 6.4.7 Hva modellen maler -- og hva den ikke maler

Modellen maler **P(brudd pa driftsstandard ved ankomst)**: sannsynligheten for at et anrop ankommer i en tilstand der makkerpar-driftsstandarden ikke kan opprettholdes.

Dette er ikke det samme som:
- P(ingen svarer) -- noen svarer i nesten alle tilfeller
- P(W > t) i Erlang-C-forstand -- tradisjonell ventetid i ko
- P(kapasitetskollaps) -- systemet kollapser sjelden totalt

Det er en **operasjonell prosedyrmetrikk** som speiler 110-operatorenes erfarte kapasitetsproblem: ikke at anrop forblir ubesvarte, men at de besvares under betingelser der den operative standarden for korrekt og trygg hendelseshandtering ikke er oppfylt.

### 6.4.8 Modellens konservatisme

Selv med inkludering av sammenstilte anrop gir modellen sannsynligvis et **konservativt anslag** pa faktisk operativ belastning:

1. **Kategori B og C er ikke inkludert.** Reelle hendelser uten utrykning og tidskritiske avklaringer (ABA) binder ogsa operatorkapasitet, men er ikke modellert som egne belastningsenheter.
2. **Imputering med median.** De 23,5 % av kategori D-hendelsene som mangler tidspunkt for forste ressurs fremme er tildelt median bindingstid -- dette kan undervurdere de tyngre hendelsene.
3. **Kun akuttfasen er modellert.** Mange hendelser binder operatorkapasitet lenger gjennom oppfolging, samband og loggforing.
4. **Sammenstilte anrop antas 1 minutt.** Faktisk varighet kan variere; noen kan vare lenger dersom innringer trenger mer avklaring.
5. **Feilkategoriserte tilleggsanrop.** Under hoyt press hender det at anrop som operativt tilhorer en pagaende hendelse lukkes som egne saker med ikke-beredskapsrelevant hendelsestype (service, feilringing, lost av 110) i stedet for a bli sammenstilt med det aktive oppdraget. Estimatet pa 18 901 sammenstilte anrop er derfor sannsynligvis et underestimat.

Begrensningene trekker i hovedsak i en retning: mot undervurdering. Resultatene bor leses som et minimumsanslag pa brudd- og sviktrisiko, ikke som et maksimumsanslag.

---

## 6.5 Implementasjon

Begge modellene er implementert i Python. Erlang-C er beregnet med scipy.special og numpy. Ankomstkonfliktmodellen bruker en sweep-algoritme for sporing av aktive hendelsers utløpstidspunkter, noe som gir O(N log N) kompleksitet over N anrop.

```python
# Pseudokode — ankomstkonfliktdeteksjon
import heapq

def ankomstkonflikt(anrop, bindingstid_func, c_eff):
    aktive = []  # min-heap over utløpstidspunkter
    for anrop_i in sorted(anrop, key=lambda x: x.tidspunkt):
        # Fjern utløpte hendelser
        while aktive and aktive[0] <= anrop_i.tidspunkt:
            heapq.heappop(aktive)
        n_aktive = len(aktive)
        ledige = c_eff - n_aktive
        # Klassifiser
        if ledige >= 2:
            nivaa = "Normal"
        elif ledige <= 0:
            nivaa = "Svikt"
        else:
            nivaa = "Brudd"
        # Legg til ny aktiv hendelse
        utlop = anrop_i.tidspunkt + bindingstid_func(anrop_i.kategori)
        heapq.heappush(aktive, utlop)
        yield anrop_i, n_aktive, nivaa
```

Kildekode og Jupyter notebooks er versjonskontrollert på GitHub (se Vedlegg A).
KI-verktøy benyttet i implementasjonsfasen er dokumentert i Vedlegg D.

---

*Kap 6 — Versjon 2.0 | Sist oppdatert: 2026-04-02*
