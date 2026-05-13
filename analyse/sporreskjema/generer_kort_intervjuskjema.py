"""
Lag ett kort, samlet intervjuskjema for alle 110-sentraler.

Output:
  pdf/Kort_intervjuskjema_alle_110_sentraler.pdf
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
PDF_DIR = ROOT / "pdf"
PDF_DIR.mkdir(exist_ok=True)
PDF_PATH = PDF_DIR / "Kort_intervjuskjema_alle_110_sentraler.pdf"

SENTRALER = [
    "Agder 110",
    "Finnmark 110",
    "Innlandet 110",
    "Midt-Norge 110",
    "Møre og Romsdal 110",
    "Nordland 110",
    "Oslo 110",
    "Sør-Vest 110",
    "Sør-Øst 110",
    "Tromsø 110",
    "Vest 110",
    "Øst 110",
]


BLUE = colors.HexColor("#1f4e79")
LIGHT = colors.HexColor("#f4f7fb")
GRID = colors.HexColor("#8a96a3")
TEXT = colors.HexColor("#111827")
MUTED = colors.HexColor("#4b5563")
FIELD_FILL = colors.HexColor("#fbfdff")


def safe_name(text: str) -> str:
    repl = {
        " ": "_",
        "-": "_",
        "ø": "o",
        "Ø": "O",
        "å": "a",
        "Å": "A",
        "æ": "ae",
        "Æ": "AE",
        "é": "e",
    }
    out = text
    for old, new in repl.items():
        out = out.replace(old, new)
    return "".join(ch for ch in out if ch.isalnum() or ch == "_")


def draw_text(c, x, y, text, size=9, bold=False, color=TEXT):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    c.drawString(x, y, text)


def draw_section(c, x, y, w, title):
    c.setFillColor(BLUE)
    c.rect(x, y - 18, w, 18, fill=True, stroke=False)
    draw_text(c, x + 6, y - 13, title, size=10, bold=True, color=colors.white)


def field(c, name, x, y, w, h, multiline=False, font_size=8):
    c.acroForm.textfield(
        name=name,
        tooltip=name,
        x=x,
        y=y,
        width=w,
        height=h,
        borderWidth=0.6,
        borderColor=GRID,
        fillColor=FIELD_FILL,
        textColor=TEXT,
        fontSize=font_size,
        fieldFlags="multiline" if multiline else "",
        forceBorder=True,
    )


def checkbox(c, name, x, y, label, size=8.5):
    c.acroForm.checkbox(
        name=name,
        tooltip=label,
        x=x,
        y=y,
        size=8,
        borderWidth=0.6,
        borderColor=GRID,
        fillColor=colors.white,
        textColor=TEXT,
        buttonStyle="check",
        forceBorder=True,
    )
    draw_text(c, x + 12, y + 1, label, size=size)


def draw_page_number(c, page, total):
    w, _ = c._pagesize
    draw_text(c, w - 45 * mm, 12 * mm, f"Side {page} av {total}", size=8, color=MUTED)


def draw_overview(c, total_pages):
    c.setPageSize(landscape(A4))
    w, h = landscape(A4)
    margin = 14 * mm
    x = margin
    y = h - margin

    draw_text(c, x, y - 4, "Kort intervjuskjema - samlet oversikt", size=17, bold=True, color=BLUE)
    draw_text(c, x, y - 21, "110-sentraler - bemanning, ABA, service og tallavvik", size=10, color=MUTED)

    headers = ["Sentral", "Min.", "Maks", "ABA registrering", "Service håndteres av", "Tallavvik"]
    col_w = [95, 70, 70, 175, 175, 155]
    row_h = 31
    table_y = y - 48

    c.setStrokeColor(GRID)
    c.setLineWidth(0.6)
    c.setFillColor(BLUE)
    c.rect(x, table_y - row_h, sum(col_w), row_h, fill=True, stroke=True)

    cur_x = x
    for hdr, cw in zip(headers, col_w):
        draw_text(c, cur_x + 4, table_y - 19, hdr, size=8.5, bold=True, color=colors.white)
        cur_x += cw

    for i, sentral in enumerate(SENTRALER):
        row_top = table_y - row_h * (i + 1)
        c.setFillColor(LIGHT if i % 2 else colors.white)
        c.rect(x, row_top - row_h, sum(col_w), row_h, fill=True, stroke=True)
        cur_x = x
        for cw in col_w:
            c.line(cur_x, row_top, cur_x, row_top - row_h)
            cur_x += cw
        c.line(x + sum(col_w), row_top, x + sum(col_w), row_top - row_h)

        draw_text(c, x + 4, row_top - 19, sentral, size=8.5, bold=True)
        base = f"oversikt_{safe_name(sentral)}"
        cell_x = x + col_w[0]
        for idx, cw in enumerate(col_w[1:], start=1):
            field(c, f"{base}_{idx}", cell_x + 3, row_top - row_h + 5, cw - 6, row_h - 10, multiline=True, font_size=7)
            cell_x += cw

    draw_page_number(c, 1, total_pages)
    c.showPage()


def draw_interview_page(c, sentral, page, total_pages):
    c.setPageSize(A4)
    w, h = A4
    margin = 14 * mm
    x = margin
    y = h - margin
    usable_w = w - 2 * margin
    base = safe_name(sentral)

    draw_text(c, x, y - 4, f"Kort intervjuskjema - {sentral}", size=15, bold=True, color=BLUE)

    meta_y = y - 30
    draw_text(c, x, meta_y + 4, "Dato:", size=8.5, bold=True)
    field(c, f"{base}_dato", x + 34, meta_y - 1, 76, 15)
    draw_text(c, x + 125, meta_y + 4, "Informant/rolle:", size=8.5, bold=True)
    field(c, f"{base}_informant", x + 225, meta_y - 1, usable_w - 225, 15)

    sec_y = meta_y - 22
    draw_section(c, x, sec_y, usable_w, "1. Bemanning")
    y1 = sec_y - 34
    draw_text(c, x, y1, "Minimumsbemanning (antall operatører + ev. vaktleder)", size=8.7, bold=True)
    labels = ["Dag hverdag", "Natt hverdag", "Dag helg", "Natt helg"]
    col_w = usable_w / 4
    for i, lab in enumerate(labels):
        xx = x + i * col_w
        draw_text(c, xx, y1 - 18, lab, size=8)
        field(c, f"{base}_min_{i}", xx, y1 - 40, col_w - 8, 17)

    y2 = y1 - 68
    draw_text(c, x, y2, "Maks/forsterket bemanning:", size=8.7, bold=True)
    field(c, f"{base}_maks", x + 145, y2 - 5, usable_w - 145, 18)
    y3 = y2 - 28
    draw_text(c, x, y3, "Er vaktleder med i bemanningstallene?", size=8.7, bold=True)
    checkbox(c, f"{base}_vl_ja", x + 190, y3 - 3, "Ja")
    checkbox(c, f"{base}_vl_nei", x + 245, y3 - 3, "Nei")
    checkbox(c, f"{base}_vl_delvis", x + 300, y3 - 3, "Delvis/usikkert")
    field(c, f"{base}_vl_kommentar", x + 405, y3 - 7, usable_w - 405, 18)

    sec_y = y3 - 30
    draw_section(c, x, sec_y, usable_w, "2. ABA-registrering")
    y1 = sec_y - 34
    draw_text(c, x, y1, "Hvordan registreres ABA?", size=8.7, bold=True)
    checkbox(c, f"{base}_aba_leo", x, y1 - 20, "LEO/BRIS som oppdrag")
    checkbox(c, f"{base}_aba_egen", x + 165, y1 - 20, "Egen ABA-kategori")
    checkbox(c, f"{base}_aba_lost", x + 310, y1 - 20, "Løst av 110 uten utrykning")
    checkbox(c, f"{base}_aba_ikke", x, y1 - 40, "Ikke i LEO/BRIS")
    checkbox(c, f"{base}_aba_annet", x + 165, y1 - 40, "Annet/varierer")
    draw_text(c, x, y1 - 61, "Kommentar:", size=8.2, bold=True)
    field(c, f"{base}_aba_kommentar", x + 75, y1 - 74, usable_w - 75, 33, multiline=True)

    sec_y = y1 - 92
    draw_section(c, x, sec_y, usable_w, "3. Service/test av ABA")
    y1 = sec_y - 34
    draw_text(c, x, y1, "Hvem håndterer service/test?", size=8.7, bold=True)
    checkbox(c, f"{base}_service_110", x, y1 - 20, "110-operatør på vakt")
    checkbox(c, f"{base}_service_dedikert", x + 165, y1 - 20, "Dedikert personell")
    checkbox(c, f"{base}_service_annen", x + 310, y1 - 20, "Annen enhet/ekstern")
    checkbox(c, f"{base}_service_varierer", x, y1 - 40, "Varierer ved helg/fravær/sykdom")
    draw_text(c, x, y1 - 61, "Når går service til 110-sentralen?", size=8.2, bold=True)
    field(c, f"{base}_service_kommentar", x + 180, y1 - 69, usable_w - 180, 22, multiline=True)

    sec_y = y1 - 88
    draw_section(c, x, sec_y, usable_w, "4. Tallavvik")
    y1 = sec_y - 34
    draw_text(c, x, y1, "Store avvik i MOB/BRIS/LEO-tallene?", size=8.7, bold=True)
    checkbox(c, f"{base}_avvik_ja", x + 205, y1 - 3, "Ja")
    checkbox(c, f"{base}_avvik_nei", x + 260, y1 - 3, "Nei")
    checkbox(c, f"{base}_avvik_usikker", x + 315, y1 - 3, "Usikkert")
    draw_text(c, x, y1 - 28, "Hva avviker, og hva er forklaringen?", size=8.2, bold=True)
    field(c, f"{base}_avvik_kommentar", x, y1 - 90, usable_w, 52, multiline=True)

    sec_y = y1 - 110
    draw_section(c, x, sec_y, usable_w, "5. Konklusjon for analysen")
    y1 = sec_y - 34
    draw_text(c, x, y1, "Kan tallene brukes slik de står?", size=8.7, bold=True)
    checkbox(c, f"{base}_bruk_direkte", x + 175, y1 - 3, "Ja")
    checkbox(c, f"{base}_bruk_korrigeres", x + 230, y1 - 3, "Må korrigeres")
    checkbox(c, f"{base}_bruk_usikker", x + 340, y1 - 3, "Usikkert")
    draw_text(c, x, y1 - 28, "Kort oppsummering:", size=8.2, bold=True)
    field(c, f"{base}_konklusjon", x, y1 - 83, usable_w, 45, multiline=True)

    draw_page_number(c, page, total_pages)
    c.showPage()


def main():
    total_pages = 1 + len(SENTRALER)
    c = canvas.Canvas(str(PDF_PATH))
    c.setTitle("Kort intervjuskjema - alle 110-sentraler")
    c.setAuthor("Rune Grødem")
    c.setSubject("LOG650 - intervjuskjema")

    draw_overview(c, total_pages)
    for i, sentral in enumerate(SENTRALER, start=2):
        draw_interview_page(c, sentral, i, total_pages)

    c.save()
    print(PDF_PATH)


if __name__ == "__main__":
    main()
