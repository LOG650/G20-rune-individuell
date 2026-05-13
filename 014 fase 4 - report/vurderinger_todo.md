# Vurderinger og lukking — LOG650 G20 Rune Grødem

Dette dokumentet er en lukket revisjonslogg for vurderinger som ble gjort under arbeidet med rapporten. Punktene under er enten innarbeidet i rapportkildene eller avgrenset eksplisitt i metode, modell og diskusjon.

## V1 — Sammenstilte anrop og skjult dobbeltbinding

**Identifisert:** 2026-04-07  
**Status:** Lukket i rapporten

Sammenstilte anrop kan binde en ekstra operatør dersom foreldreoppdraget allerede håndteres av en annen operatør. Dette er behandlet som en konservativ begrensning i modellen: hovedmodellen teller det sammenstilte anropet som egen belastningsenhet, men legger ikke inn ekstra binding for ukjent foreldreoppdrag når dette ikke kan spores sikkert i datagrunnlaget.

**Rapportmessig håndtering:** Modellkonservatisme og usikkerhet er dokumentert i kapittel 6 og diskutert i kapittel 8.

## V2 — Kategori A som operativ bakgrunnsbelastning

**Identifisert:** 2026-04-07  
**Status:** Lukket i rapporten

Kategori A/B/C er ikke beredskapsdimensjonerende på samme måte som kategori D, men skaper operativ belastning gjennom service, test, administrative henvendelser og avklaringer. Dette er tatt inn som kontekst for tolkning av modellresultatene og som et forbehold ved sammenligning mellom sentraler.

**Rapportmessig håndtering:** Avgrensning er presisert i kapittel 5, modellantagelser er samlet i kapittel 6, og praktiske implikasjoner er diskutert i kapittel 8.

## V3 — Total operativ belastning

**Identifisert:** 2026-04-07  
**Status:** Lukket i rapporten

V3 er videreført som supplerende analysevariant. Rapporten skiller mellom Variant A, som måler beredskapsbelastning, og Variant B, som inkluderer alle kategorier med kategoriavhengig bindingstid. Dette gir et bredere bilde av operatørbelastningen uten å erstatte hovedmodellen for beredskapskapasitet.

**Rapportmessig håndtering:** Klassifisering og databruk er beskrevet i kapittel 5, antagelsene er samlet i Tabell 6.3, resultatene er presentert i kapittel 7, og tolkningen er samlet i kapittel 8.

## Kontroll etter revisjon

| Kontrollpunkt | Resultat |
|---|---|
| Kapittelreferanser | Gjennomgått i rapportens Markdown-kilder |
| Tabellnummerering | Sekvensielt ryddet i kapittel 7 og komplettert med Tabell 6.3 |
| Kildehenvisninger | Korrigert og supplert i referanselisten |
| Midlertidige arbeidsmarkører | Fjernet fra rapportkildene og støttefilene i denne mappen |

Denne filen inngår som intern revisjonslogg og bygges ikke inn som selvstendig rapportkapittel.
