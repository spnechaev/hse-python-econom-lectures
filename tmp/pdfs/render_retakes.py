from pathlib import Path
import ast
import html
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Preformatted, PageBreak
from pypdf import PdfReader, PdfWriter
import fitz

root = Path.cwd()
for name, filename in [('Body', 'Arial.ttf'), ('Bold', 'Arial Bold.ttf'), ('Mono', 'Courier New.ttf')]:
    pdfmetrics.registerFont(TTFont(name, '/System/Library/Fonts/Supplemental/' + filename))
pdfmetrics.registerFontFamily('Body', normal='Body', bold='Bold')
styles = {
    'p': ParagraphStyle('p', fontName='Body', fontSize=10.5, leading=13, spaceAfter=6),
    'h': ParagraphStyle('h', fontName='Bold', fontSize=12, leading=15, spaceBefore=10, spaceAfter=6, keepWithNext=True),
    'm': ParagraphStyle('m', fontName='Bold', fontSize=10, leading=12, spaceAfter=6, keepWithNext=True),
    'c': ParagraphStyle('c', fontName='Mono', fontSize=9, leading=11, spaceAfter=6),
}

def inline(text):
    text = html.escape(text).replace('—', '-')
    text = re.sub(r'`([^`]+)`', r'<font name="Mono" size="9">\1</font>', text)
    return re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)


def flow(text):
    result = []
    for chunk in re.split(r'(```python\n.*?```)', text, flags=re.S):
        if chunk.startswith('```python'):
            code = chunk[10:-3].strip('\n')
            ast.parse(code)
            for line in code.splitlines():
                assert pdfmetrics.stringWidth(line, 'Mono', 9) < A4[0] - 80, line
            result.append(Preformatted(code, styles['c']))
        else:
            for paragraph in re.split(r'\n\s*\n', chunk.strip()):
                if not paragraph:
                    continue
                kind = 'h' if paragraph.startswith('## ') else 'm' if paragraph.startswith('**') else 'p'
                if kind == 'h':
                    paragraph = paragraph[3:]
                result.append(Paragraph(inline(paragraph.replace('\n', ' ')), styles[kind]))
    return result

writer = PdfWriter()
for variant in [6, 7]:
    source = (root / f'assessments/control_01_variant_{variant:02}.md').read_text()
    content = re.sub(r'^# .*\n\n', '', source)
    content = re.sub(r'^\*\*Время:.*\n\n', '', content, flags=re.M)
    front, back = content.split('## Задача 3.', 1)

    def decorate(canvas, document):
        canvas.setFont('Bold', 10)
        canvas.drawString(40, A4[1] - 30, f'Контрольная № 1 · Вариант {variant} · Пересдача')
        canvas.setFont('Body', 9)
        canvas.drawRightString(A4[0] - 40, A4[1] - 30, '60 минут · 10 баллов')
        canvas.setLineWidth(.3)
        canvas.line(40, A4[1] - 38, A4[0] - 40, A4[1] - 38)
        canvas.setFont('Body', 8)
        canvas.drawString(40, 25, f'Вариант {variant} · Python')
        canvas.drawRightString(A4[0] - 40, 25, f'{document.page} / 2')

    path = root / f'output/pdf/control_01_variant_{variant:02}_a4.pdf'
    SimpleDocTemplate(str(path), pagesize=A4, leftMargin=40, rightMargin=40, topMargin=49, bottomMargin=39).build(
        flow(front) + [PageBreak()] + flow('## Задача 3.' + back),
        onFirstPage=decorate, onLaterPages=decorate,
    )
    reader = PdfReader(path)
    assert len(reader.pages) == 2
    text = '\n'.join(page.extract_text() for page in reader.pages)
    assert text.count('assert ') == source.count('assert ')
    expected = 'replace_digit(1200, 1, 3) == 3200' if variant == 6 else 'swap_digits(1200, 1, 2) == 2100'
    assert expected in text
    writer.append(reader)
    for index, page in enumerate(fitz.open(path)):
        for block in page.get_text('blocks'):
            assert block[0] >= 35 and block[2] <= A4[0] - 35
        page.get_pixmap(matrix=fitz.Matrix(1.25, 1.25)).save(root / f'tmp/pdfs/retake-{variant}-{index+1}.png')
    print(f'Вариант {variant}: новый пример сохранён, 2 страницы A4.')
writer.write(root / 'output/pdf/control_01_retakes_06-07_a4.pdf')
