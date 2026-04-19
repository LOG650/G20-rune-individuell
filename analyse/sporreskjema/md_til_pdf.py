"""
Konverter et spørreskjema (Markdown) til fyllbar PDF (AcroForm) med profesjonell layout.

Bruk:  py md_til_pdf.py <sentralnavn>
Eks:   py md_til_pdf.py Sør_Øst_110
       py md_til_pdf.py --alle

Genererer <sentralnavn>.pdf i pdf/-mappen.
"""
import os
import re
import sys
import argparse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, black, white, Color
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Table, TableStyle, PageBreak,
    KeepTogether, Flowable, HRFlowable, CondPageBreak,
)

# === FARGER OG STIL ===
FARGE_PRIMAR = HexColor('#1a3a5c')
FARGE_SEKUNDAR = HexColor('#2a5a80')
FARGE_AKSENT = HexColor('#c44e52')
FARGE_LYS = HexColor('#f5f7fa')
FARGE_GRÅ = HexColor('#6b7280')
FARGE_BOX_RAMME = HexColor('#9ca3af')
FARGE_BOX_BG = HexColor('#fbfbfd')

STIL = {
    'H1': ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=18, leading=22,
                          spaceBefore=0, spaceAfter=4, textColor=FARGE_PRIMAR),
    'H1sub': ParagraphStyle('H1sub', fontName='Helvetica', fontSize=11, leading=14,
                             spaceBefore=0, spaceAfter=2, textColor=FARGE_SEKUNDAR),
    'H2': ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=14, leading=18,
                          spaceBefore=18, spaceAfter=6, textColor=FARGE_PRIMAR,
                          keepWithNext=True),
    'H3': ParagraphStyle('H3', fontName='Helvetica-Bold', fontSize=11.5, leading=15,
                          spaceBefore=10, spaceAfter=4, textColor=FARGE_SEKUNDAR,
                          keepWithNext=True),
    'Body': ParagraphStyle('Body', fontName='Helvetica', fontSize=10, leading=13,
                            spaceBefore=2, spaceAfter=4, alignment=TA_LEFT),
    'Kontekst': ParagraphStyle('Kontekst', fontName='Helvetica-Oblique', fontSize=9.5,
                                leading=12, leftIndent=12, rightIndent=4,
                                textColor=HexColor('#444c55'), spaceAfter=4,
                                borderPadding=(4, 6, 4, 6), backColor=FARGE_LYS),
    'Sitat': ParagraphStyle('Sitat', fontName='Helvetica-Oblique', fontSize=9.5,
                             leading=12, leftIndent=12, textColor=HexColor('#555555'),
                             spaceAfter=4),
    'Spm': ParagraphStyle('Spm', fontName='Helvetica', fontSize=10.5, leading=14,
                           spaceBefore=10, spaceAfter=4, keepWithNext=True),
    'Liste': ParagraphStyle('Liste', fontName='Helvetica', fontSize=10, leading=14,
                             leftIndent=18, spaceAfter=2),
    'Footer': ParagraphStyle('Footer', fontName='Helvetica', fontSize=8.5, leading=10,
                              textColor=FARGE_GRÅ, spaceBefore=20),
}


# === FLOWABLE: FYLLBAR TEKSTBOKS ===
class Tekstboks(Flowable):
    """Multi-linjet AcroForm textfield med ramme."""
    _teller = 0

    def __init__(self, hoyde_cm=2.4, etikett=None):
        Flowable.__init__(self)
        Tekstboks._teller += 1
        self.navn = f"svar_{Tekstboks._teller:03d}"
        self.height = hoyde_cm * cm
        self.width = 0  # fylles ut i wrap()
        self.etikett = etikett

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        # acroForm.textfield bruker absolutte sidekoordinater — vi må hente
        # aktuell CTM-posisjon for flowable sin bunn-venstre.
        x0, y0 = c.absolutePosition(0, 0)
        form = c.acroForm
        form.textfield(
            name=self.navn,
            tooltip=self.etikett or "Svar",
            x=x0, y=y0, width=self.width, height=self.height,
            borderWidth=0.6,
            borderColor=FARGE_BOX_RAMME,
            fillColor=FARGE_BOX_BG,
            textColor=black,
            fontSize=10,
            fieldFlags='multiline',
            forceBorder=True,
        )


# === MARKDOWN → HTML (inline) ===
def md_inline_til_html(tekst):
    """Konverter inline markdown (**fet**, *kursiv*, «...») til reportlab-HTML."""
    t = tekst
    # Fet
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    # Kursiv (bruker *...* men ikke **)
    t = re.sub(r'(?<!\*)\*(?!\*)([^*]+?)\*(?!\*)', r'<i>\1</i>', t)
    # Backticks → fast bredde
    t = re.sub(r'`([^`]+)`', r'<font face="Courier" size="9">\1</font>', t)
    # HTML-escape (må komme før konvertering)
    # reportlab håndterer & og < — la være
    return t


# === PARSE MD TIL FLOWABLES ===
def parse_md_til_flowables(md_tekst, sentral_navn):
    """
    Parser Markdown og bygger flowables. Bruker block-akkumulering slik at hvert
    spørsmål (Spm + avklaring + liste + svar-boks) holdes sammen over sideskift.
    """
    linjer = md_tekst.split('\n')
    flowables = []
    # Block-akkumulering: når en Spm pågår, legges nye flowables i blokken
    # inntil svar-boks eller neste Spm/seksjon.
    aktiv_blokk = None

    def flush_blokk():
        nonlocal aktiv_blokk
        if aktiv_blokk:
            if len(aktiv_blokk) > 1:
                flowables.append(KeepTogether(aktiv_blokk))
            else:
                flowables.extend(aktiv_blokk)
            aktiv_blokk = None

    def legg_til(fl):
        if aktiv_blokk is not None:
            aktiv_blokk.append(fl)
        else:
            flowables.append(fl)

    def start_blokk(first_fl):
        nonlocal aktiv_blokk
        flush_blokk()
        aktiv_blokk = [first_fl]

    i = 0
    n = len(linjer)
    gjeldende_tabell = []

    def avslutt_tabell():
        nonlocal gjeldende_tabell
        if not gjeldende_tabell:
            return
        tbl = lag_tabell(gjeldende_tabell)
        legg_til(tbl)
        legg_til(Spacer(1, 4))
        gjeldende_tabell = []

    while i < n:
        linje = linjer[i]
        stripped = linje.strip()

        # Tabellrad — samle, ikke send til blokk ennå
        if stripped.startswith('|') and stripped.endswith('|'):
            gjeldende_tabell.append(stripped)
            i += 1
            continue
        elif gjeldende_tabell:
            avslutt_tabell()

        # Horisontal linje — avslutter eventuell åpen blokk
        if stripped == '---':
            flush_blokk()
            flowables.append(Spacer(1, 4))
            flowables.append(HRFlowable(width='100%', thickness=0.5,
                                         color=HexColor('#d1d5db'),
                                         spaceAfter=6, spaceBefore=2))
            i += 1
            continue

        if stripped == '':
            i += 1
            continue

        # H1
        if stripped.startswith('# '):
            flush_blokk()
            tekst = md_inline_til_html(stripped[2:].strip())
            flowables.append(Paragraph(tekst, STIL['H1']))
            i += 1
            continue

        # H2
        if stripped.startswith('## '):
            flush_blokk()
            tekst = md_inline_til_html(stripped[3:].strip())
            flowables.append(CondPageBreak(4 * cm))
            flowables.append(Paragraph(tekst, STIL['H2']))
            i += 1
            continue

        # H3
        if stripped.startswith('### '):
            flush_blokk()
            tekst = md_inline_til_html(stripped[4:].strip())
            flowables.append(Paragraph(tekst, STIL['H3']))
            i += 1
            continue

        # Svar-boks — matcher både "> *Svar:*" og "> *Utdyping (...)*"
        m_svar = re.match(r'^>\s*\*([^*]+)\*:?\s*$', stripped)
        if m_svar and any(k in m_svar.group(1).lower() for k in ('svar', 'utdyp', 'beskriv')):
            etikett = m_svar.group(1).strip().rstrip(':')
            legg_til(Spacer(1, 3))
            legg_til(Tekstboks(hoyde_cm=2.6, etikett=etikett))
            legg_til(Spacer(1, 4))
            # Svar-boks er siste element i en Spm-blokk — flush
            flush_blokk()
            i += 1
            continue

        # Blokksitat (kontekst, avklaring, konfidensialitet)
        if stripped.startswith('> '):
            sitat_linjer = [stripped[2:]]
            j = i + 1
            while j < n and linjer[j].strip().startswith('> '):
                s = linjer[j].strip()[2:]
                # Stopp hvis det blir en svar-boks
                if re.match(r'^\*(Svar|Utdyping|Beskrivelse)', s):
                    break
                sitat_linjer.append(s)
                j += 1
            sitat_tekst = ' '.join(sitat_linjer).strip()
            legg_til(Paragraph(md_inline_til_html(sitat_tekst), STIL['Kontekst']))
            legg_til(Spacer(1, 3))
            i = j
            continue

        # Spørsmål «**Spm N.** ...»
        m_spm = re.match(r'^\*\*Spm\s+(\d+)\.\*\*\s*(.*)$', stripped)
        if m_spm:
            nr = m_spm.group(1)
            rest = m_spm.group(2)
            j = i + 1
            # Samle påfølgende ikke-blokk-linjer i samme paragraf (flerlinje-Spm)
            while j < n:
                s = linjer[j].strip()
                if s == '' or s.startswith(('**Spm ', '> ', '- ', '|', '#', '---')):
                    break
                rest += ' ' + s
                j += 1
            tekst = f'<b><font color="#1a3a5c">Spm {nr}.</font></b> ' + md_inline_til_html(rest)
            # Start ny blokk for dette spørsmålet
            start_blokk(Paragraph(tekst, STIL['Spm']))
            i = j
            continue

        # Avkrysnings-punkter
        if stripped.startswith('- [ ]'):
            tekst_del = stripped[5:].strip()
            html = f'<font face="Helvetica">&#9744;</font>&nbsp;&nbsp;' + md_inline_til_html(tekst_del)
            legg_til(Paragraph(html, STIL['Liste']))
            i += 1
            continue

        if stripped.startswith('- '):
            tekst_del = stripped[2:].strip()
            html = f'&bull;&nbsp;&nbsp;' + md_inline_til_html(tekst_del)
            legg_til(Paragraph(html, STIL['Liste']))
            i += 1
            continue

        # Meta-linje som starter med **Label:** — egen paragraf
        m_meta = re.match(r'^\*\*([^*]+):\*\*\s*(.*)$', stripped)
        if m_meta:
            legg_til(Paragraph(md_inline_til_html(stripped), STIL['Body']))
            i += 1
            continue

        # Vanlig paragraf — samle til neste blokk-grense
        para_linjer = [stripped]
        j = i + 1
        while j < n:
            s = linjer[j].strip()
            if s == '' or s.startswith(('#', '- ', '|', '>', '**Spm ', '---')):
                break
            # Ikke slå sammen med neste **Label:**-linje
            if re.match(r'^\*\*[^*]+:\*\*', s):
                break
            para_linjer.append(s)
            j += 1
        para = ' '.join(para_linjer)
        legg_til(Paragraph(md_inline_til_html(para), STIL['Body']))
        i = j

    if gjeldende_tabell:
        avslutt_tabell()
    flush_blokk()

    return flowables


# === TABELL-BYGGER ===
def lag_tabell(md_rader):
    """Konverter markdown-tabellrader til en reportlab Table."""
    # Filtrér ut separator-raden (|---|---|...)
    data_rader = []
    for r in md_rader:
        celler = [c.strip() for c in r.strip().strip('|').split('|')]
        if all(re.match(r'^:?-+:?$', c) for c in celler):
            continue
        data_rader.append(celler)

    if not data_rader:
        return Spacer(1, 1)

    # Wrap celler i Paragraph for bedre tekstflyt
    cell_stil = ParagraphStyle('TblCell', fontName='Helvetica', fontSize=9,
                                leading=11, alignment=TA_LEFT)
    cell_stil_hdr = ParagraphStyle('TblHdr', fontName='Helvetica-Bold', fontSize=9,
                                    leading=11, alignment=TA_LEFT, textColor=white)

    wrapped = []
    for i_r, rad in enumerate(data_rader):
        wr = []
        for celle in rad:
            tekst = md_inline_til_html(celle)
            # Farg avviks-celle
            if '↑ HØY' in tekst:
                tekst = tekst.replace('↑ HØY', '<font color="#c44e52"><b>↑ HØY</b></font>')
            elif '↓ LAV' in tekst:
                tekst = tekst.replace('↓ LAV', '<font color="#2563eb"><b>↓ LAV</b></font>')
            stil = cell_stil_hdr if i_r == 0 else cell_stil
            wr.append(Paragraph(tekst, stil))
        wrapped.append(wr)

    # Kolonnebredder — forsøk å gjøre første kolonne bredere
    n_kol = len(wrapped[0])
    if n_kol <= 2:
        col_widths = None
    elif n_kol == 6:
        col_widths = [4.5 * cm] + [2.0 * cm] * (n_kol - 1)
    elif n_kol == 7:
        col_widths = [4.8 * cm] + [1.8 * cm] * (n_kol - 1)
    else:
        col_widths = None

    tbl = Table(wrapped, colWidths=col_widths, hAlign='LEFT', repeatRows=1)
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), FARGE_SEKUNDAR),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, FARGE_LYS]),
        ('BOX', (0, 0), (-1, -1), 0.4, HexColor('#d1d5db')),
        ('LINEBELOW', (0, 0), (-1, 0), 0.4, FARGE_SEKUNDAR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    return tbl


# === HEADER / FOOTER ===
def lag_header_footer(sentral_navn):
    def draw(canvas, doc):
        canvas.saveState()
        w, h = A4
        # Header
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(FARGE_GRÅ)
        canvas.drawString(2 * cm, h - 1.2 * cm, f"Spørreskjema — {sentral_navn}")
        canvas.drawRightString(w - 2 * cm, h - 1.2 * cm, "LOG650 · Høgskolen i Molde · 2026")
        canvas.setStrokeColor(HexColor('#e5e7eb'))
        canvas.setLineWidth(0.3)
        canvas.line(2 * cm, h - 1.35 * cm, w - 2 * cm, h - 1.35 * cm)
        # Footer
        canvas.setFont('Helvetica', 8.5)
        canvas.setFillColor(FARGE_GRÅ)
        canvas.drawString(2 * cm, 1.2 * cm, "Rune Grødem · rune.grodemm@himolde.no")
        canvas.drawRightString(w - 2 * cm, 1.2 * cm, f"Side {doc.page}")
        canvas.restoreState()
    return draw


# === HOVEDFUNKSJON ===
def konverter(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_tekst = f.read()

    # Hent sentralnavn fra første H1
    m_tit = re.match(r'#\s+Spørreskjema\s+—\s+(.+?)$', md_tekst.split('\n')[0])
    sentral_navn = m_tit.group(1) if m_tit else os.path.basename(md_path).replace('.md', '')

    # Reset tekstboks-teller per skjema
    Tekstboks._teller = 0

    # Bygg flowables
    flowables = parse_md_til_flowables(md_tekst, sentral_navn)

    # Dokument-oppsett
    doc = BaseDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=1.9 * cm, bottomMargin=1.9 * cm,
        title=f"Spørreskjema — {sentral_navn}",
        author="Rune Grødem",
        subject="LOG650 Kapasitetsanalyse 110-sentraler",
    )
    frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    page_template = PageTemplate(
        id='main', frames=[frame],
        onPage=lag_header_footer(sentral_navn),
    )
    doc.addPageTemplates([page_template])
    doc.build(flowables)
    print(f"Skrevet: {pdf_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('sentral', nargs='?', help='Sentral (f.eks. Sør_Øst_110) eller --alle')
    ap.add_argument('--alle', action='store_true', help='Konverter alle skjemaer')
    args = ap.parse_args()

    utmappe = os.path.dirname(os.path.abspath(__file__))
    pdf_mappe = os.path.join(utmappe, 'pdf')
    os.makedirs(pdf_mappe, exist_ok=True)

    if args.alle or args.sentral == '--alle':
        md_filer = [f for f in os.listdir(utmappe) if f.endswith('.md') and f != 'README.md']
        for md in sorted(md_filer):
            md_path = os.path.join(utmappe, md)
            pdf_path = os.path.join(pdf_mappe, md.replace('.md', '.pdf'))
            konverter(md_path, pdf_path)
    else:
        navn = args.sentral or 'Sør_Øst_110'
        if not navn.endswith('.md'):
            navn += '.md'
        md_path = os.path.join(utmappe, navn)
        pdf_path = os.path.join(pdf_mappe, navn.replace('.md', '.pdf'))
        konverter(md_path, pdf_path)


if __name__ == '__main__':
    main()
