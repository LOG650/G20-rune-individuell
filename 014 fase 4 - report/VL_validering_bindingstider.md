# Validering av bindingstidsestimater — til vaktleder

**Bakgrunn:** I prosjektet kvantifiserer jeg operativ belastning på 110 Sør-Vest basert på BRIS-data fra 2025. For beredskapsoppdrag (kategori D) har jeg databasert bindingstid (median 13 min fra anrop til første ressurs fremme + kvittering). For alle øvrige henvendelser mangler BRIS tidsdata, så jeg trenger operative estimater.

**Spørsmål:** Kan du se over tabellen under og gi en vurdering av om kategoriseringen og tidsestimatene virker rimelige?

---

## Kategorisering av hendelser uten utrykning (54 409 i 2025)

Alle tall er fra BRIS 2025 for 110 Sør-Vest.

| Kategori | Hva det er i praksis | Antall (2025) | Eksempel |
|---|---|---|---|
| **S — Service/overføringstest** | Servicetekniker ringer for overføringstest av brannalarmanlegg. Operatør mottar samtale i LEO, setter adresse (om den ikke kommer automatisk), tar imot signal i alarmmottak, verifiserer mottatt signal til servicetekniker, venter til anlegget er i hvile, kvitterer ut testen og lukker som service. | 22 542 | Servicetekniker tester anlegg på Kvadrat — operatør verifiserer signal og kvitterer |
| **L-aba — ABA løst av 110** | Automatisk brannalarm kommer inn. Overføres til LEO, operatør venter 90 sekunder. Dersom nødtelefon fra stedet mottas innen 90 sek → intervju. Hvis innringer bekrefter ufarlig årsak (f.eks. matlaging), lukkes oppdraget som «Oppdrag løst av 110». Uten nødtelefon innen 90 sek ville det ført til utrykning (kategori D). | 5 495 | ABA fra leilighet — nødtelefon innen 90 sek, innringer bekrefter matlaging → lukkes |
| **L-hendelse — Reell hendelse løst av 110** | Innringer melder noe reelt, operatør vurderer og løser uten å sende ressurs | 2 233 | Røyklukt fra nabo, operatør gir råd, ingen utrykning nødvendig |
| **L-ukjent — Løst av 110, uklassifisert** | Henvendelser som lukkes uten formell oppdragstype — bålspørsmål, service lukket feil, korte avklaringer | 16 536 | «Kan jeg tenne bål i hagen?» → kort svar, lukkes |
| **F — Feilringing** | Feilringing, ikke-nødmelding, eCall feil bruk | 6 830 | Noen trykker 110 i stedet for 112, kort avklaring |
| **V — Viderevarsling** | Viderekobling til annen etat eller intern varsling | 550 | Hendelse som egentlig er politi/AMK, viderekobles |

---

## Estimert bindingstid per kategori

Med «bindingstid» mener jeg: **hvor lenge er operatøren opptatt med denne hendelsen?** Ikke bare samtaletid, men også oppslag i LEO, tilbakeringing, etterarbeid.

| Kategori | Lavt estimat | Mitt hovedestimat | Høyt estimat | Kommentar |
|---|---|---|---|---|
| **S — Service** | 1 min | 2 min | 4 min | Motta samtale, adresse i LEO, ta imot signal, verifisere, vente på hvile, kvittere, lukke |
| **L-aba** | 2 min | 3 min | 5 min | Overføre til LEO, vente 90 sek, eventuelt intervju ved nødtelefon, lukke |
| **L-hendelse** | 3 min | 5 min | 8 min | Reell vurdering — ta imot, stille spørsmål, gi råd, konkludere |
| **L-ukjent** | 1 min | 3 min | 5 min | Blanding av korte og litt lengre — usikkert |
| **F — Feilringing** | 15 sek | 30 sek | 1 min | «Dette er 110, du vil ha 112/113» → henvis og lukk |
| **V — Viderevarsling** | 30 sek | 1 min | 2 min | Koble videre, kort beskjed |

---

## Hva jeg trenger tilbakemelding på

1. **Er kategoriseringen gjenkjennbar?** Mangler det en type, eller er noe slått sammen som burde vært skilt?
2. **Er bindingstidene rimelige?** For høye? For lave? Spesielt Service og L-aba — de er de to største gruppene.
3. **L-ukjent (16 536 hendelser):** Stemmer det at dette i hovedsak er korte henvendelser som ikke krever formell opprettelse?

Ikke tenk på at tallene må være eksakte — jeg kjører sensitivitetsanalyse med lav/hoved/høy for å vise at konklusjonen holder uansett.
