# verktoy/ — PDF-eksport og hjelpeverktøy

Master-pipeline for konvertering av prosjektdokumenter fra Markdown til PDF.

## Oppsett

**Krav:**
- Pandoc 3.x (testet 3.9) — installert via winget (`JohnMacFarlane.Pandoc`)
- MiKTeX eller TeXLive med `xelatex`
- Python 3.12 med `reportlab` (kun for spørreskjema)

Skriptet `build_pdf.py` auto-detekterer Pandoc og XeLaTeX fra PATH eller kjente Windows-stier.

## To typer dokumenter

| Dokumenttype | Pipeline | Hvorfor |
|---|---|---|
| **Faglige dokumenter** (rapport, vedlegg, ønskelister) | Pandoc + XeLaTeX + `templates/dokument-header.tex` | Profesjonell typografi, matematikk ($\ldots$), figurer, tabeller med streker, innholdsfortegnelse |
| **Spørreskjema** (12 sentraler) | reportlab + `analyse/sporreskjema/md_til_pdf.py` | Fyllbar AcroForm-PDF — mottaker skriver svar direkte i PDFen |

## Bruksmåter

### Fra kommandolinje

```
python verktoy/build_pdf.py --dokument analyse/DSB_onskeliste_BRIS_datauttrekk.md --toc
python verktoy/build_pdf.py --rapport-full
python verktoy/build_pdf.py --alle-kapitler
python verktoy/build_pdf.py --skjema Oslo_110
python verktoy/build_pdf.py --alle-skjema
```

### Fra bat-fil (meny)

Dobbeltklikk `eksporter_pdf.bat` i prosjektroten for interaktiv meny.

Eller bruk direkte:
```
eksporter_pdf.bat --dokument analyse/DSB_onskeliste_BRIS_datauttrekk.md --toc
eksporter_pdf.bat --rapport-full
```

## Output-mapper

| Pipeline | Output |
|---|---|
| `--dokument`, `--alle-kapitler`, `--rapport-full` | `005 report/` |
| `--skjema`, `--alle-skjema` | `analyse/sporreskjema/pdf/` |

## Hva pipelinen håndterer

### Faglige dokumenter (Pandoc)

- **Norske bokstaver** (æøå) via `-V lang=nb-NO` og norsk orddeling
- **Inline matematikk** `$\lambda$` og display-math `$$ ... $$` — rendres som LaTeX
- **Figurer** — både `![]()` og HTML `<div align="center"><img ... /></div>` (sentrert, max 85 % bredde)
- **Tabeller** — alle bokser får streker (GRID) via `booktabs`-overstyring i `dokument-header.tex`
- **Innholdsfortegnelse** — med `--toc` (depth 3)
- **Sidehoder** — «LOG650 · Rune Grødem» (venstre), «Vår 2026» (høyre), e-post og sidetall i footer
- **Emoji-erstatning** — ✅/❌/⚠️/∧/∨/≠ erstattes automatisk med tekst-varianter (Segoe UI har ikke glyph)

### Spørreskjema (reportlab)

- **AcroForm-tekstfelt** (multiline) — mottaker kan skrive direkte i PDFen
- **Svarbokser** — 4 cm høyde (standard) / 5 cm (for «utdyping»/«beskriv»-spørsmål)
- **Tabeller med grid-streker** — alle bokser tydelige
- **Avviksfarging** — ↑ HØY (rød) / ↓ LAV (blå)
- **Sentralspesifikk framing** — hvert skjema merkes med sentralens navn

## Tilpasning

- **LaTeX-tilpasninger** — rediger `verktoy/templates/dokument-header.tex`
- **Emoji/symbol-erstatninger** — rediger dict `UNICODE_ERSTATNINGER` i `build_pdf.py`
- **Spørreskjema-layout** — rediger `analyse/sporreskjema/md_til_pdf.py` (STIL-dict, Tekstboks-klasse)

## Feilsøking

| Symptom | Løsning |
|---|---|
| `[WARNING] Missing character: ...` | Legg tegnet til i `UNICODE_ERSTATNINGER` |
| `Error producing PDF. ! LaTeX Error:` | Inspiser `.tex`-output ved å legge til `--keep-intermediate` og kjør xelatex manuelt |
| Figur mangler | Sjekk `--resource-path` — relative stier løses fra MD-filens mappe |
| Norske bokstaver kræsjer | Sjekk at MD-filen er UTF-8 (BOM-fri), ikke ANSI/Windows-1252 |

## Arbeidsflyt for sluttlevering

1. Oppdater MD-kilder (rapport, skjema, vedlegg)
2. Kjør relevant profil (`--rapport-full` eller `--alle-skjema`)
3. Åpne PDF i Adobe Acrobat Pro (du har fullpakke) for ev. redigering, signatur, form-validering
4. Lever PDF-er fra `005 report/` og `analyse/sporreskjema/pdf/`
