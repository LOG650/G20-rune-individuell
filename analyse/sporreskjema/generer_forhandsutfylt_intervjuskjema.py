"""
Lag et forhåndsutfylt, samlet intervjuskjema basert på de tidligere
sentralspesifikke spørreskjemaene.

Hensikt:
- vise MOB/DSB-tall som allerede er funnet
- beskrive store avvik som må diskuteres
- gi korte felt for bekreftelse/korrigering i personlig intervju

Output:
  pdf/Forhandsutfylt_intervjuskjema_alle_110_sentraler.pdf
"""
from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Flowable,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
PDF_DIR = ROOT / "pdf"
PDF_DIR.mkdir(exist_ok=True)
PDF_PATH = PDF_DIR / "Forhandsutfylt_intervjuskjema_alle_110_sentraler.pdf"

FORM_FILES = [
    "Agder_110.md",
    "Finnmark_110.md",
    "Innlandet_110.md",
    "Midt_Norge_110.md",
    "Møre_og_Romsdal_110.md",
    "Nordland_110.md",
    "Oslo_110.md",
    "Sør_Vest_110.md",
    "Sør_Øst_110.md",
    "Tromsø_110.md",
    "Vest_110.md",
    "Øst_110.md",
]

BLUE = colors.HexColor("#1f4e79")
LIGHT_BLUE = colors.HexColor("#eaf2fb")
LIGHT = colors.HexColor("#f7f9fc")
GRID = colors.HexColor("#9aa6b2")
TEXT = colors.HexColor("#111827")
MUTED = colors.HexColor("#4b5563")
FIELD_FILL = colors.HexColor("#fbfdff")


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        "TitleBlue",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=21,
        textColor=BLUE,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        "H2Blue",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=BLUE,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        "H3Blue",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=10.2,
        leading=12.5,
        textColor=BLUE,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        "Small",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.7,
        leading=11.2,
        alignment=TA_LEFT,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        "SmallMuted",
        parent=styles["Small"],
        textColor=MUTED,
    )
)
styles.add(
    ParagraphStyle(
        "Tiny",
        parent=styles["Small"],
        fontSize=7.6,
        leading=9.4,
        spaceAfter=2,
    )
)
styles.add(
    ParagraphStyle(
        "BoxText",
        parent=styles["Small"],
        backColor=LIGHT,
        borderColor=GRID,
        borderWidth=0.4,
        borderPadding=5,
        spaceBefore=2,
        spaceAfter=5,
    )
)


class TextField(Flowable):
    counter = 0

    def __init__(self, name: str, height_cm: float = 1.0, font_size: int = 8):
        super().__init__()
        TextField.counter += 1
        self.name = f"{name}_{TextField.counter}"
        self.height = height_cm * cm
        self.width = 0
        self.font_size = font_size

    def wrap(self, avail_width, avail_height):
        self.width = avail_width
        return self.width, self.height

    def draw(self):
        x0, y0 = self.canv.absolutePosition(0, 0)
        self.canv.acroForm.textfield(
            name=self.name,
            tooltip=self.name,
            x=x0,
            y=y0,
            width=self.width,
            height=self.height,
            borderWidth=0.55,
            borderColor=GRID,
            fillColor=FIELD_FILL,
            textColor=TEXT,
            fontSize=self.font_size,
            fieldFlags="multiline",
            forceBorder=True,
        )


@dataclass
class Deviation:
    category: str
    description: str
    discussion: str


@dataclass
class CentralData:
    sentral: str
    file_name: str
    staff_years: dict[str, list[str]]
    ansatte_2025: str
    mob_anrop_2025: str
    dsb_total_2025: str
    dsb_mob_ratio: str
    deviations: list[Deviation]
    service_note: str


def plain(markdown_text: str) -> str:
    txt = markdown_text.replace("\r", "")
    txt = re.sub(r"\*\*(.*?)\*\*", r"\1", txt)
    txt = re.sub(r"\*(.*?)\*", r"\1", txt)
    txt = re.sub(r"`(.*?)`", r"\1", txt)
    txt = txt.replace("↑", "HØY").replace("↓", "LAV")
    txt = txt.replace("×", "x")
    txt = txt.replace("—", "-").replace("–", "-")
    txt = txt.replace("→", "->")
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt


def p(text: str, style="Small"):
    return Paragraph(html.escape(plain(text)), styles[style])


def pbold(text: str, style="Small"):
    return Paragraph(f"<b>{html.escape(plain(text))}</b>", styles[style])


def split_md_row(line: str) -> list[str]:
    return [plain(c.strip()) for c in line.strip().strip("|").split("|")]


def extract_sentral(text: str, fallback: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("# Spørreskjema"):
            return plain(line.split("—", 1)[-1].replace("# Spørreskjema", "")).strip()
    return fallback.replace("_", " ")


def extract_staff(lines: list[str]) -> tuple[dict[str, list[str]], str, str]:
    staff_map = {
        "Operatører dag": "Dag hverdag",
        "Operatører natt": "Natt hverdag",
        "Operatører dag - helg": "Dag helg",
        "Operatører natt - helg": "Natt helg",
    }
    staff_years: dict[str, list[str]] = {}
    ansatte_2025 = ""
    mob_anrop_2025 = ""

    for line in lines:
        if not line.startswith("|"):
            continue
        cells = split_md_row(line)
        if len(cells) < 5:
            continue
        label = cells[0]
        if label.startswith("Ansatte heltid"):
            ansatte_2025 = cells[4]
        elif label.startswith("Operatører dag") and "helg" not in label.lower():
            staff_years["Dag hverdag"] = cells[1:5]
        elif label.startswith("Operatører natt") and "helg" not in label.lower():
            staff_years["Natt hverdag"] = cells[1:5]
        elif label.startswith("Operatører dag") and "helg" in label.lower():
            staff_years["Dag helg"] = cells[1:5]
        elif label.startswith("Operatører natt") and "helg" in label.lower():
            staff_years["Natt helg"] = cells[1:5]
        elif label.startswith("Mottatte 110-anrop"):
            mob_anrop_2025 = cells[4]

    return staff_years, ansatte_2025, mob_anrop_2025


def category_for(desc: str) -> str:
    d = desc.lower()
    if "aba løst" in d:
        return "ABA løst uten utrykning"
    if "d-aba" in d:
        return "D-aba / ABA-utrykning"
    if "utrykningsrate" in d:
        return "Utrykningsrate"
    if "d-pri1" in d:
        return "D-pri1"
    if "l-ukjent" in d:
        return "L-ukjent"
    if "l-hendelse" in d:
        return "L-hendelse"
    if "feilring" in d:
        return "Feilring"
    if "viderekoble" in d:
        return "Viderekobling"
    if "forhold dsb/mob" in d:
        return "DSB/MOB"
    if "alarmbehandlingstid" in d:
        return "Alarmbehandlingstid"
    return "Annet avvik"


def extract_deviations(text: str) -> list[Deviation]:
    pattern = re.compile(
        r"^\*\*Spm\s+\d+\.\*\*\s+\*\*\[SENTRALSPESIFIKT AVVIK[^\]]+\]\*\*\s*(.*?)(?=^\*\*Spm\s+\d+\.|\n---|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    deviations: list[Deviation] = []
    for match in pattern.finditer(text):
        block = match.group(1).strip()
        block = block.split("> *Svar:*", 1)[0]
        if "> *Avklaring:*" in block:
            desc, discussion = block.split("> *Avklaring:*", 1)
        else:
            desc, discussion = block, ""
        desc = plain(desc)
        discussion = plain(discussion)
        deviations.append(Deviation(category_for(desc), desc, discussion))
    return deviations


def service_note_for(sentral: str) -> str:
    if sentral == "Midt-Norge 110":
        return (
            "Tidligere intervjunotat 15.03.2026: Midt-Norge har 3 dedikerte personer "
            "som håndterer ABA-servicetesting. Ved helg, sykdom og overbelastning tas "
            "service av ordinære 110-operatører. Må bekreftes/korrigeres."
        )
    return "Ikke forhåndsavklart i tidligere skjema/notat. Må avklares i intervjuet."


def parse_form(path: Path) -> CentralData:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    sentral = extract_sentral(text, path.stem)
    staff_years, ansatte_2025, mob_anrop_2025 = extract_staff(lines)

    total = re.search(
        r"Totalvolum DSB 2025:\s+\*\*([^*]+)\*\* oppdrag\. MOB-selvrapport:\s+\*\*([^*]+)\*\* mottatte anrop\. Forhold DSB/MOB:\s+\*\*([^*]+)\*\*",
        text,
    )
    if total:
        dsb_total_2025, mob_from_total, dsb_mob_ratio = total.groups()
        mob_anrop_2025 = mob_anrop_2025 or mob_from_total
    else:
        dsb_total_2025, dsb_mob_ratio = "", ""

    return CentralData(
        sentral=sentral,
        file_name=path.name,
        staff_years=staff_years,
        ansatte_2025=ansatte_2025,
        mob_anrop_2025=mob_anrop_2025,
        dsb_total_2025=dsb_total_2025,
        dsb_mob_ratio=dsb_mob_ratio,
        deviations=extract_deviations(text),
        service_note=service_note_for(sentral),
    )


def staff_2025(data: CentralData, label: str) -> str:
    values = data.staff_years.get(label, [])
    return values[3] if len(values) >= 4 else ""


def staff_changes(data: CentralData) -> str:
    changes = []
    years = ["2022", "2023", "2024", "2025"]
    for label in ["Dag hverdag", "Natt hverdag", "Dag helg", "Natt helg"]:
        vals = data.staff_years.get(label, [])
        if len(vals) == 4 and len(set(vals)) > 1:
            changes.append(f"{label}: " + " -> ".join(f"{y}:{v}" for y, v in zip(years, vals)))
    return "; ".join(changes) if changes else "Ingen endring i MOB-bemanning 2022-2025."


def make_table(data, col_widths=None, header=True):
    table_data = []
    for row in data:
        table_data.append([p(str(cell), "Tiny") if not hasattr(cell, "wrap") else cell for cell in row])
    tbl = Table(table_data, colWidths=col_widths, hAlign="LEFT", repeatRows=1 if header else 0)
    style = [
        ("GRID", (0, 0), (-1, -1), 0.35, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), BLUE),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ]
    else:
        style.append(("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, LIGHT]))
    tbl.setStyle(TableStyle(style))
    return tbl


def add_overview(story: list, centrals: list[CentralData]):
    story.append(Paragraph("Forhåndsutfylt intervjuskjema - alle 110-sentraler", styles["TitleBlue"]))
    story.append(
        p(
            "Bruk i intervju: Les opp de forhåndsutfylte tallene og avvikene. Be informanten bekrefte, korrigere eller forklare. "
            "Målet er å avklare om tallene kan brukes direkte i analysen, eller om registreringspraksis/organisering gjør dem lite sammenlignbare.",
            "Small",
        )
    )
    rows = [["Sentral", "MOB bemanning 2025", "MOB anrop", "DSB oppdrag", "DSB/MOB", "Avvik å diskutere"]]
    for d in centrals:
        bem = (
            f"D-hv {staff_2025(d, 'Dag hverdag')}, "
            f"N-hv {staff_2025(d, 'Natt hverdag')}, "
            f"D-helg {staff_2025(d, 'Dag helg')}, "
            f"N-helg {staff_2025(d, 'Natt helg')}"
        )
        keys = ", ".join(dev.category for dev in d.deviations) or "Ingen flagget i gammel del 7"
        rows.append([d.sentral, bem, d.mob_anrop_2025, d.dsb_total_2025, d.dsb_mob_ratio, keys])
    story.append(make_table(rows, col_widths=[3.0 * cm, 4.2 * cm, 2.3 * cm, 2.3 * cm, 1.7 * cm, 5.0 * cm]))
    story.append(PageBreak())


def add_central(story: list, data: CentralData):
    story.append(Paragraph(f"{data.sentral} - forhåndsutfylt intervjuskjema", styles["TitleBlue"]))
    story.append(p(f"Kilde: tidligere spørreskjema {data.file_name}.", "SmallMuted"))

    story.append(Paragraph("1. Forhåndsutfylte nøkkeltall", styles["H2Blue"]))
    key_rows = [
        ["Punkt", "Forhåndsutfylt verdi"],
        ["Ansatte heltid 2025", data.ansatte_2025 or "Ikke funnet"],
        [
            "MOB bemanning 2025",
            (
                f"Dag hverdag {staff_2025(data, 'Dag hverdag')}; "
                f"natt hverdag {staff_2025(data, 'Natt hverdag')}; "
                f"dag helg {staff_2025(data, 'Dag helg')}; "
                f"natt helg {staff_2025(data, 'Natt helg')}."
            ),
        ],
        ["Endring i MOB-bemanning 2022-2025", staff_changes(data)],
        ["MOB mottatte 110-anrop 2025", data.mob_anrop_2025 or "Ikke funnet"],
        ["DSB oppdrag 2025", data.dsb_total_2025 or "Ikke funnet"],
        ["Forhold DSB/MOB", data.dsb_mob_ratio or "Ikke funnet"],
    ]
    story.append(make_table(key_rows, col_widths=[5.2 * cm, 12.0 * cm]))

    story.append(Paragraph("2. Bekreft/korriger bemanning", styles["H2Blue"]))
    story.append(
        p(
            "Spør konkret om MOB-tallet er minimumsbemanning, normalbemanning eller et gjennomsnitt. Fyll inn korrigert min/maks dersom MOB ikke viser reell drift.",
            "Small",
        )
    )
    bem_rows = [
        ["Vakttype", "MOB 2025", "Bekreftet/korrigert min", "Bekreftet/korrigert normal", "Maks/forsterket"],
    ]
    safe = re.sub(r"\W+", "_", data.sentral)
    for i, label in enumerate(["Dag hverdag", "Natt hverdag", "Dag helg", "Natt helg"]):
        bem_rows.append(
            [
                label,
                staff_2025(data, label),
                TextField(f"{safe}_min_{i}", 0.65, 7),
                TextField(f"{safe}_normal_{i}", 0.65, 7),
                TextField(f"{safe}_maks_{i}", 0.65, 7),
            ]
        )
    story.append(make_table(bem_rows, col_widths=[3.2 * cm, 2.2 * cm, 4.0 * cm, 4.1 * cm, 3.7 * cm]))
    story.append(p("[ ] MOB stemmer   [ ] MOB må korrigeres   [ ] Vaktleder er inkludert   [ ] Vaktleder er ikke inkludert", "Small"))
    story.append(TextField(f"{safe}_bemanning_kommentar", 1.15, 8))

    story.append(Paragraph("3. ABA og service", styles["H2Blue"]))
    aba_devs = [d for d in data.deviations if "ABA" in d.category or "aba" in d.description.lower()]
    if aba_devs:
        story.append(pbold("Forhåndsflagget ABA-avvik:", "Small"))
        for dev in aba_devs:
            story.append(p(f"{dev.category}: {dev.description}", "Tiny"))
    else:
        story.append(p("Ingen særskilt ABA-avvik ble flagget i gammelt skjema, men registreringspraksis må bekreftes.", "Small"))
    story.append(pbold("Service/test av ABA - forhåndsnotat:", "Small"))
    story.append(p(data.service_note, "BoxText"))
    story.append(p("[ ] ABA registreres i LEO/BRIS   [ ] ABA registreres i annen kategori   [ ] ABA/service håndteres utenfor LEO/BRIS   [ ] Usikkert", "Small"))
    story.append(TextField(f"{safe}_aba_service", 1.25, 8))

    story.append(Paragraph("4. Store avvik som må diskuteres", styles["H2Blue"]))
    if not data.deviations:
        story.append(p("Ingen sentralspesifikke avvik ble funnet i gammelt skjema.", "Small"))
    for idx, dev in enumerate(data.deviations, start=1):
        block = [
            Paragraph(f"<b>{idx}. {html.escape(dev.category)}</b>", styles["H3Blue"]),
            p(dev.description, "Small"),
        ]
        if dev.discussion:
            block.append(p(f"Diskuter: {dev.discussion}", "SmallMuted"))
        block.append(TextField(f"{safe}_avvik_{idx}", 1.05, 8))
        story.append(KeepTogether(block))

    story.append(Paragraph("5. Konklusjon etter intervju", styles["H2Blue"]))
    story.append(p("[ ] Tallene kan brukes som de står   [ ] Tallene kan brukes med korrigering   [ ] Ikke sammenlignbart uten større forbehold", "Small"))
    story.append(TextField(f"{safe}_konklusjon", 1.25, 8))
    story.append(PageBreak())


def draw_header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(1.7 * cm, height - 1.15 * cm, "LOG650 - forhåndsutfylt intervjuskjema")
    canvas.drawRightString(width - 1.7 * cm, height - 1.15 * cm, "Rune Grødem - 2026")
    canvas.setStrokeColor(colors.HexColor("#d8dee6"))
    canvas.setLineWidth(0.3)
    canvas.line(1.7 * cm, height - 1.28 * cm, width - 1.7 * cm, height - 1.28 * cm)
    canvas.drawRightString(width - 1.7 * cm, 1.05 * cm, f"Side {doc.page}")
    canvas.restoreState()


def main():
    centrals = [parse_form(ROOT / name) for name in FORM_FILES]
    TextField.counter = 0
    doc = BaseDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        leftMargin=1.7 * cm,
        rightMargin=1.7 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.5 * cm,
        title="Forhåndsutfylt intervjuskjema - alle 110-sentraler",
        author="Rune Grødem",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="normal", frames=[frame], onPage=draw_header_footer)])
    story: list = []
    add_overview(story, centrals)
    for central in centrals:
        add_central(story, central)
    if story and isinstance(story[-1], PageBreak):
        story.pop()
    doc.build(story)
    print(PDF_PATH)


if __name__ == "__main__":
    main()
