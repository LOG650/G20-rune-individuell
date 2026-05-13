"""
Master-pipeline for MD -> PDF i LOG650-prosjektet.

Tre profiler:
  --dokument <fil>     Faglig dokument (DSB-ønskeliste, vedlegg, enkeltkapittel)
                       Pandoc + XeLaTeX med dokument-header.tex
  --rapport-full       Sammenstilt rapport: alle kap1-9 + vedlegg, med ToC
  --skjema [navn]      Spørreskjema (interaktiv PDF, AcroForm) — kaller
                       analyse/sporreskjema/md_til_pdf.py
  --alle-skjema        Alle 12 spørreskjemaer

Eksempler:
  py verktoy/build_pdf.py --dokument analyse/DSB_onskeliste_BRIS_datauttrekk.md
  py verktoy/build_pdf.py --rapport-full
  py verktoy/build_pdf.py --skjema Sør_Vest_110
  py verktoy/build_pdf.py --alle-skjema

Krav:
  - Pandoc 3.x (testet 3.9)
  - MiKTeX/TeXLive med xelatex
  - reportlab (kun for skjema)

Output: 005 report/ for dokumenter, analyse/sporreskjema/pdf/ for skjema.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

# Tvinge UTF-8 på stdout/stderr (Windows-konsoll er cp1252 by default)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
VERKTOY = ROOT / "verktoy"
TEMPLATES = VERKTOY / "templates"
OUTPUT_DOK = ROOT / "005 report"
OUTPUT_DOK.mkdir(exist_ok=True)

# Auto-detekt Pandoc og XeLaTeX
def finn_kommando(navn, kandidater):
    """Søk PATH først, deretter kjente Windows-stier."""
    import shutil
    p = shutil.which(navn)
    if p:
        return p
    for k in kandidater:
        if Path(k).exists():
            return k
    return None

LOCALAPPDATA = os.environ.get("LOCALAPPDATA", "")
PANDOC = finn_kommando("pandoc", [
    f"{LOCALAPPDATA}/Microsoft/WinGet/Packages/JohnMacFarlane.Pandoc_Microsoft.Winget.Source_8wekyb3d8bbwe/pandoc-3.9.0.2/pandoc.exe",
])
XELATEX = finn_kommando("xelatex", [
    f"{LOCALAPPDATA}/Programs/MiKTeX/miktex/bin/x64/xelatex.exe",
])

if not PANDOC:
    print("FEIL: pandoc ikke funnet. Installer Pandoc 3.x og legg den i PATH.", file=sys.stderr)
    sys.exit(1)
if not XELATEX:
    print("FEIL: xelatex ikke funnet. Installer MiKTeX eller TeXLive.", file=sys.stderr)
    sys.exit(1)


# --- Pandoc-flagg per profil ---

def flagg_dokument(toc=False):
    """Faglig dokument med dokument-header.tex."""
    flagg = [
        f"--pdf-engine={XELATEX}",
        f"--include-in-header={TEMPLATES / 'dokument-header.tex'}",
        "-V", "geometry:a4paper,margin=2.3cm,top=2.5cm,bottom=2.3cm",
        "-V", "fontsize=11pt",
        "-V", "mainfont=Segoe UI",
        "-V", "sansfont=Segoe UI",
        "-V", "monofont=Consolas",
        "-V", "linkcolor=black",
        "-V", "urlcolor=blue!60!black",
        "-V", "lang=nb-NO",
        "--wrap=preserve",
    ]
    if toc:
        flagg += [
            "--toc", "--toc-depth=3",
            "-V", "toc-title:Innholdsfortegnelse",
            "-V", "documentclass=article",
            "-V", "abstract-title:Sammendrag",
        ]
    return flagg


# Emojier og unicode-symboler som må erstattes fordi Segoe UI ikke har glyph.
# Erstatninger velger tegn som er typografisk kompatible og finnes i fonten.
UNICODE_ERSTATNINGER = {
    # Emojier og symboler uten glyph i Segoe UI -> erstatt med tekst/ASCII
    "\u2705": "**[OK]**",        # ✅ -> [OK]
    "\u274c": "**[Mangler]**",   # ❌ -> [Mangler]
    "\u26a0\ufe0f": "**[!]**",   # ⚠️ -> [!]
    "\u26a0": "**[!]**",         # ⚠ -> [!]
    "\ufe0f": "",                # variant selector-16 (fjern)
    "\u2713": "[v]",             # ✓ -> [v]
    "\u2717": "[x]",             # ✗ -> [x]
    "\U0001f449": "->",          # 👉 -> ->
    "\U0001f4a1": "",            # 💡 -> (fjern)
    "\U0001f4cc": "",            # 📌 -> (fjern)
    # Logiske/matematiske symboler brukt i prosa (ikke inne i $...$)
    "\u2227": "OG",              # ∧ -> OG
    "\u2228": "ELLER",           # ∨ -> ELLER
    "\u2260": "!=",              # ≠ -> !=
    # NB: matematiske symboler (∈ ≤ ≥ ≈ ⊆) beholdes — de brukes inni $...$ og
    # rendres som LaTeX-matematikk. Pandoc-warnings for disse utenfor math-mode
    # er ikke-fatale og kan ignoreres.
    # Sammenstilte piler i spørreskjema-tabeller håndteres av reportlab, ikke her.
}

import re as _re

# HTML-figurblokk i rapporten:
#   <div align="center">
#     <img src="..." alt="..." width="80%">
#     <p align="center"><small><i>Figur X.Y: ...</i></small></p>
#   </div>
# Konverteres til pandoc-kompatibel markdown med attributter for bredde.
_HTML_FIGUR_RE = _re.compile(
    r'<div\s+align="center">\s*'
    r'<img\s+src="([^"]+)"\s+alt="([^"]*)"(?:\s+width="(\d+)%?")?\s*/?>\s*'
    r'<p\s+align="center">\s*<small>\s*<i>\s*(.*?)\s*</i>\s*</small>\s*</p>\s*'
    r'</div>',
    _re.DOTALL,
)


def forbehandle_md(md_tekst):
    """Erstatt emojier, unicode og konverter HTML-figurblokker til markdown."""
    # 1. HTML-figurblokker -> markdown ![]()
    def _figur_sub(m):
        src = m.group(1)
        alt = m.group(2) or ""
        width = m.group(3) or "80"
        caption = m.group(4) or alt
        # Pandoc-attributt {width=80%} setter figurbredde
        return f'![{caption}]({src}){{width={width}%}}\n'

    md_tekst = _HTML_FIGUR_RE.sub(_figur_sub, md_tekst)

    # 2. Emojier og unicode
    for fra, til in UNICODE_ERSTATNINGER.items():
        md_tekst = md_tekst.replace(fra, til)
    return md_tekst


def konverter_dokument(md_path, pdf_path, toc=False, ressursmappe=None):
    """Kjør pandoc med dokument-profil.

    Forbehandling: Emoji-erstatning gjøres i en midlertidig fil for å unngå
    LaTeX-advarsler om manglende glyph.
    """
    import tempfile
    md_path = Path(md_path).resolve()
    pdf_path = Path(pdf_path).resolve()
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    raw = md_path.read_text(encoding="utf-8")
    forbehandlet = forbehandle_md(raw)

    # Lag midlertidig fil i samme mappe for at relative stier til figurer skal fungere
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix=".md", delete=False,
        dir=md_path.parent, prefix=f"_tmp_{md_path.stem}_",
    ) as tf:
        tf.write(forbehandlet)
        tmp_md = Path(tf.name)

    try:
        cmd = [PANDOC, str(tmp_md), "-o", str(pdf_path)] + flagg_dokument(toc=toc)
        rp_deler = [str(md_path.parent), str(ROOT), str(ROOT / "analyse"), str(ROOT / "analyse" / "figurer")]
        if ressursmappe:
            rp_deler.insert(0, str(ressursmappe))
        cmd += [f"--resource-path={';'.join(rp_deler)}"]

        print(f"  Kjører: pandoc {md_path.name} -> {pdf_path.name}")
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    finally:
        try:
            tmp_md.unlink()
        except Exception:
            pass
    if res.returncode != 0:
        print(f"  FEIL ({res.returncode}):", file=sys.stderr)
        print(res.stderr[-2000:], file=sys.stderr)
        return False
    if res.stderr.strip():
        # pandoc skriver advarsler til stderr selv ved suksess
        print(f"  Advarsler: {res.stderr.strip()[:500]}")
    print(f"  OK {pdf_path.relative_to(ROOT)}")
    return True


def rapport_full():
    """Bygg samlet rapport: ren forside+kap1 + kap2-9 + referanser/vedlegg.

    Bruker `_forside_og_kap1.md` (stripped, uten placeholders) i stedet for
    `Rapport_LOG650_G20_Rune_110_v0.1.md` (skjelett med duplisert kap 2-9 innhold).
    Emoji-erstatning og figurreferanser håndteres via forbehandle_md() per fil.
    """
    import tempfile
    rapport_dir = ROOT / "014 fase 4 - report"
    deler = [
        rapport_dir / "_forside_og_kap1.md",
        rapport_dir / "kap2_litteratur.md",
        rapport_dir / "kap3_teori.md",
        rapport_dir / "kap4_casebeskrivelse.md",
        rapport_dir / "kap5_metode_data.md",
        rapport_dir / "kap6_modell.md",
        rapport_dir / "kap7_analyse_resultater.md",
        rapport_dir / "kap8_diskusjon.md",
        rapport_dir / "kap9_konklusjon.md",
        rapport_dir / "_referanser_og_vedlegg.md",
    ]
    manglende = [d for d in deler if not d.exists()]
    if manglende:
        print("FEIL: Disse filene mangler:", file=sys.stderr)
        for m in manglende:
            print(f"  - {m.relative_to(ROOT)}", file=sys.stderr)
        return False

    pdf_out = OUTPUT_DOK / "Rapport_LOG650_G20_Rune_110_samlet.pdf"

    # Forbehandle hver fil til temp-fil (emoji-erstatninger)
    tmp_filer = []
    try:
        for d in deler:
            raw = d.read_text(encoding="utf-8")
            forbehandlet = forbehandle_md(raw)
            tf = tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", suffix=".md", delete=False,
                dir=rapport_dir, prefix=f"_tmp_{d.stem}_",
            )
            tf.write(forbehandlet)
            tf.close()
            tmp_filer.append(Path(tf.name))

        cmd = [PANDOC] + [str(t) for t in tmp_filer] + ["-o", str(pdf_out)] + flagg_dokument(toc=True)
        analyse_dir = ROOT / "analyse"
        figurer_dir = ROOT / "analyse" / "figurer"
        cmd += [f"--resource-path={rapport_dir};{ROOT};{analyse_dir};{figurer_dir}"]
        print(f"Bygger samlet rapport ({len(deler)} filer) -> {pdf_out.name}")
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if res.returncode != 0:
            print("FEIL:", file=sys.stderr)
            print(res.stderr[-2000:], file=sys.stderr)
            return False
        if res.stderr.strip():
            print(f"  Advarsler: {res.stderr.strip()[:500]}")
        print(f"OK {pdf_out.relative_to(ROOT)}")
        return True
    finally:
        for tf in tmp_filer:
            try:
                tf.unlink()
            except Exception:
                pass


def alle_kapitler():
    """Konverter hver kapittelfil separat (mot vedlegg-bruk)."""
    rapport_dir = ROOT / "014 fase 4 - report"
    md_filer = sorted([f for f in rapport_dir.glob("kap*.md")])
    md_filer.append(rapport_dir / "Rapport_LOG650_G20_Rune_110_v0.1.md")
    n_ok = 0
    for md in md_filer:
        if not md.exists():
            continue
        pdf = OUTPUT_DOK / md.name.replace(".md", ".pdf")
        if konverter_dokument(md, pdf, toc=False):
            n_ok += 1
    print(f"\n{n_ok}/{len(md_filer)} kapitler konvertert.")


def skjema(navn=None):
    """Kall reportlab-pipeline for spørreskjema (AcroForm)."""
    skript = ROOT / "analyse" / "sporreskjema" / "md_til_pdf.py"
    if not skript.exists():
        print(f"FEIL: {skript} finnes ikke.", file=sys.stderr)
        return False
    cmd = [sys.executable, str(skript)]
    if navn:
        cmd.append(navn)
    print(f"Kjører spørreskjema-pipeline: {' '.join(cmd)}")
    return subprocess.run(cmd).returncode == 0


def alle_skjema():
    skript = ROOT / "analyse" / "sporreskjema" / "md_til_pdf.py"
    return subprocess.run([sys.executable, str(skript), "--alle"]).returncode == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dokument", metavar="MD-FIL", help="Konverter ett dokument")
    g.add_argument("--rapport-full", action="store_true", help="Sammenstilt rapport (alle kapitler + ToC)")
    g.add_argument("--alle-kapitler", action="store_true", help="Hver kapittelfil for seg")
    g.add_argument("--skjema", metavar="SENTRAL", nargs="?", const="", help="Spørreskjema (interaktiv PDF)")
    g.add_argument("--alle-skjema", action="store_true", help="Alle 12 spørreskjemaer")
    ap.add_argument("--toc", action="store_true", help="Inkluder innholdsfortegnelse (kun --dokument)")
    ap.add_argument("--ut", metavar="STI", help="Output-fil eller -mappe (overstyr standard)")
    args = ap.parse_args()

    if args.dokument:
        md = Path(args.dokument).resolve()
        if not md.exists():
            print(f"FEIL: {md} finnes ikke.", file=sys.stderr)
            sys.exit(1)
        if args.ut:
            pdf = Path(args.ut).resolve()
        else:
            pdf = OUTPUT_DOK / md.name.replace(".md", ".pdf")
        konverter_dokument(md, pdf, toc=args.toc)

    elif args.rapport_full:
        rapport_full()

    elif args.alle_kapitler:
        alle_kapitler()

    elif args.skjema is not None:
        skjema(args.skjema or None)

    elif args.alle_skjema:
        alle_skjema()


if __name__ == "__main__":
    main()
