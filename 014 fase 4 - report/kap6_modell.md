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

### 6.4.2 Definisjoner

**Aktiv hendelse:** En hendelse er aktiv fra ankomsttidspunktet til estimert bindingstid er utløpt. Bindingstid er den perioden en operatør er bundet til hendelsen — det vil si samtaletid (RØD-fase) pluss koordineringstid etter samtalen (GUL-fase: utalarmering, samband, logging).

**n_aktive:** Antall aktive hendelser på tidspunktet et nytt beredskapsanrop ankommer.

**Kapasitetsnivå:** Basert på n_aktive og c_eff klassifiseres hvert anrop til ett av tre nivåer:

**Tabell 6.2: Kapasitetsnivåer definert av arbeidsmetodikken**

| Nivå | Definisjon | Terskel c_eff = 2 | Terskel c_eff = 3 |
|---|---|---|---|
| **Normal** | Makkerpar mulig — én RØD og én GUL tilgjengelig, én GRØNN ledig | n_aktive = 0 | n_aktive = 0 |
| **Brudd på driftsstandard** | Nytt anrop uten ledig, dedikert GUL-makker. Operatørene jobber «etter beste evne». | n_aktive ≥ 1 | n_aktive ≥ 1 |
| **Svikt** | VL må bryte vaktlederfunksjon *eller* anrop overføres til Agder | n_aktive ≥ 2 | n_aktive ≥ 3 |

*Svikt er et deltilfelle av brudd på driftsstandard: enhver svikt er også brudd. For c_eff = 2 med n_aktive = 1: begge operatørene er bundet (RØD + GUL på H1) — ingen kan ta H2 uten å bryte sin pågående rolle. For c_eff = 3 med n_aktive = 1: GRØNN-operatøren kan besvare anropet, men vedkommende har ingen dedikert GUL-makker — makkerpar-kravet er brutt.*

Den kritiske asymmetrien mellom c_eff = 2 og c_eff = 3 er at ved c_eff = 3 med n_aktive = 1 er det fremdeles noen som *kan* svare (GRØNN), men ingen som kan fungere som dedikert makker. Svikt inntreffer ikke, men brudd på driftsstandard er et faktum. Ved c_eff = 2 med n_aktive = 1 er svikt umiddelbart nær — enhver ny hendelse overbelaster systemet.

### 6.4.3 Matematisk formulering

La {t_i, d_i} for i = 1, …, N betegne N beredskapsanrop med ankomsttidspunkt t_i og tilhørende bindingstid d_i.

For hvert anrop i beregnes:

$$n_{\text{aktive}}(t_i) = \left|\{j < i : t_j + d_j > t_i\}\right|$$

det vil si antall tidligere anrop hvis bindingstid ennå ikke er utløpt ved t_i.

Kapasitetsnivå for anrop i:

$$\text{Nivå}(i) = \begin{cases}
\text{Normal} & \text{hvis } n_{\text{aktive}}(t_i) = 0 \\
\text{Svikt} & \text{hvis } n_{\text{aktive}}(t_i) \geq c_{\text{eff}} \\
\text{Brudd} & \text{ellers}
\end{cases}$$

Agregerte metrikker for skifttype s:

$$\text{Sviktrate}(s) = \frac{|\{i \in s : \text{Nivå}(i) = \text{Svikt}\}|}{|s|}$$

$$\text{Bruddsrate}(s) = \frac{|\{i \in s : \text{Nivå}(i) \in \{\text{Brudd}, \text{Svikt}\}\}|}{|s|}$$

### 6.4.4 Bindingstidsestimater og proxy-valg

Bindingstid d_i estimeres fra BRIS-data som tidsintervallet fra anropets ankomsttidspunkt til første ressurs er fremme, pluss 3 minutter for kvittering av vindusmelding og loggføring:

> d_i = (Første ressurs fremme − Dato/tid anrop) + 3 min

Denne proxyen er valgt fordi den fanger den mest operative og dimensjoneringsrelevante fasen av hendelseshåndteringen:

- **Akuttfasen er den mest tidskritiske:** Det er i perioden fra anrop til ressurs er fremme at informasjonsbehovet er størst og RØD/GUL-koordineringen er mest aktiv.
- **Etter fremme stabiliseres driften:** Når første ressurs er på plass går mange hendelser over i en mer stabil driftsfase med sporadisk belastning på operatøren.
- **Kvitteringsvinduet (3 min) er dokumentert:** GUL-operatøren mottar vindusmelding som må kvitteres og logges etter at ressurs er fremme.

Proxyen fanger dermed ikke hele oppdragets livsløp, men den mest kritiske delen. Av 7 555 beredskapsoppdrag (kategori D) har 5 777 (76,5 %) registrert tidspunkt for første ressurs fremme. De resterende tildeles median bindingstid (se avsnitt 7.3).

Observert fordeling: median 13,0 min, P90 21,6 min. RØD-fasen (anrop → ressurs varslet) har median 1,2 min, GUL-fasen (varslet → fremme) har median 8,2 min.

### 6.4.5 To driftsmoduser

Modellen analyseres under to forutsetninger om operatørbinding per hendelse:

- **Prosedyre (2 operatører per hendelse):** Makkerpar iht. driftsstandard. Ledige = c_eff − 2 × n_aktive.
- **Beste evne (1 operatør per hendelse):** Solo-drift, slik det faktisk gjøres under press. Ledige = c_eff − 1 × n_aktive.

Klassifisering for begge:
- Normal: ledige ≥ 2 (makkerpar mulig for neste)
- Degradert: ledige = 1 (kun solo)
- Svikt: ledige ≤ 0 (VL/Agder)

Kontrasten mellom de to modusene kvantifiserer den daglige tilpasningen operatørene gjør for å holde tjenesten gående (se avsnitt 7.4).

### 6.4.6 Hva modellen måler — og hva den ikke måler

Modellen måler **P(brudd på driftsstandard ved ankomst)**: sannsynligheten for at et beredskapsanrop ankommer i en tilstand der makkerpar-driftsstandarden ikke kan opprettholdes.

Dette er ikke det samme som:
- P(ingen svarer) — noen svarer i nesten alle tilfeller
- P(W > t) i Erlang-C-forstand — tradisjonell ventetid i kø
- P(kapasitetskollaps) — systemet kollapser sjelden totalt

Det er en **operasjonell prosedyrmetrikk** som speiler 110-operatørenes erfarte kapasitetsproblem: ikke at anrop forblir ubesvarte, men at de besvares under betingelser der den operative standarden for korrekt og trygg hendelseshåndtering ikke er oppfylt.

### 6.4.7 Modellens konservatisme

Modellen gir sannsynligvis et **konservativt anslag** på faktisk operativ belastning, av fire grunner:

1. **Kun kategori D kvantifiseres.** Hendelser i kategori B og C binder også operatørkapasitet, men er ikke inkludert som egne belastningsenheter.
2. **Sammenstilte tilleggsanrop er ikke modellert.** Når flere innringere melder om samme hendelse, registreres bare det opprinnelige oppdraget. Tilleggsanropene opptar en operatør som ellers ville vært ledig.
3. **Imputering med median.** De 23,5 % av kategori D-hendelsene som mangler tidspunkt for første ressurs fremme er tildelt median bindingstid — dette kan undervurdere de tyngre hendelsene.
4. **Kun akuttfasen er modellert.** Bindingstiden er begrenset til akuttfasen (anrop → fremme + 3 min). Mange hendelser binder operatørkapasitet i lengre tid gjennom oppfølging, samband og loggføring.

Begrensningene i datagrunnlaget trekker i hovedsak i én retning: mot undervurdering av faktisk operativ belastning. Modellen bør derfor tolkes som et minimumsanslag: de faktiske kapasitetsutfordringene er sannsynligvis større enn det tallene alene viser, og særlig større i perioder med hendelser som genererer flere sammenstilte anrop.

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
        # Klassifiser
        if n_aktive == 0:
            nivaa = "Normal"
        elif n_aktive >= c_eff:
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
