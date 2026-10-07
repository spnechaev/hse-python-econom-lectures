"""Build lecture 5 diagrams with the standard library.

Run: python3 lesson05/assets/draw_diagrams.py
"""

from html import escape
from pathlib import Path
from xml.etree import ElementTree

HERE = Path(__file__).resolve().parent
INK = "#203047"
BLUE = "#2764b7"
GREEN = "#197568"


class Diagram:
    def __init__(self, title, subtitle, height=590):
        self.height = height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img">',
            f"<title>{escape(title)}</title><desc>{escape(subtitle)}</desc>",
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#63768b"/></marker></defs>',
            '<style>text{font-family:Arial,DejaVu Sans,sans-serif}.mono{font-family:Menlo,DejaVu Sans Mono,monospace}</style>',
            f'<rect width="1200" height="{height}" rx="20" fill="#f5f7fb"/>',
        ]
        self.text(40, 52, title, 30, bold=True)
        self.text(40, 88, subtitle, 20)

    def text(self, x, y, value, size=22, color=INK, mono=False, bold=False):
        self.parts.append(f'<text xml:space="preserve" x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{700 if bold else 400}" class="{"mono" if mono else ""}">{escape(value)}</text>')

    def box(self, x, y, w, h, fill="#ffffff", stroke="#cdd7e4"):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

    def arrow(self, points):
        self.parts.append(f'<polyline points="{points}" fill="none" stroke="#63768b" stroke-width="2.5" marker-end="url(#arrow)"/>')

    def obj(self, x, y, value, w=220):
        self.box(x, y, w, 60)
        self.text(x + 18, y + 39, value, mono=True)

    def slots(self, x, y, label):
        self.text(x, y - 18, label, color=BLUE, mono=True)
        self.box(x, y, 190, 110)
        for i in range(2):
            self.text(x + 16, y + 36 + i * 48, f"[{i}]", size=20, mono=True)
            self.parts.append(f'<circle cx="{x+145}" cy="{y+29+i*48}" r="5" fill="{BLUE}"/>')

    def save(self, filename):
        xml = "\n".join(self.parts + ["</svg>"]) + "\n"
        ElementTree.fromstring(xml)
        (HERE / filename).write_text(xml, encoding="utf-8")


def names_and_objects():
    d = Diagram("Имена ссылаются на объекты", "Присваивание связывает имя с объектом. Равные списки могут быть разными объектами.", 660)
    d.text(40, 140, "a = [10, 20]; b = a; c = [10, 20]", mono=True)
    for label, y in [("a", 212), ("b", 284), ("c", 356)]:
        d.text(95, y, label, 26, mono=True, color=BLUE)
    d.obj(330, 200, "[10, 20]")
    d.obj(330, 320, "[10, 20]")
    d.arrow("130,205 230,205 330,222")
    d.arrow("130,277 230,277 330,244")
    d.arrow("130,349 330,349")
    d.text(625, 233, "a is b → True", mono=True)
    d.text(625, 287, "a == c → True", mono=True)
    d.text(625, 341, "a is c → False", mono=True)
    d.text(40, 426, "Два независимых продолжения исходного примера", color=GREEN, bold=True)
    d.box(40, 450, 540, 155)
    d.box(610, 450, 550, 155)
    d.text(60, 487, "b = [99]", mono=True, color=BLUE)
    d.text(60, 524, "Имя b переходит к новому списку.", size=21)
    d.text(60, 567, "a → [10, 20]; b → [99]", mono=True, size=21)
    d.text(630, 487, "b.append(30)", mono=True, color=BLUE)
    d.text(630, 524, "Меняется общий список a и b.", size=21)
    d.text(630, 567, "a и b → [10, 20, 30]", mono=True, size=21)
    d.text(40, 637, "В обоих продолжениях c по-прежнему ссылается на свой список [10, 20].", size=19, color=GREEN)
    d.save("names-and-objects.svg")


def mixed_types():
    d = Diagram("Один список — объекты разных типов", "Тип принадлежит объекту. Список хранит ссылки, поэтому элементам не нужен общий тип.", 600)
    d.text(40, 140, 'values = ["Аня", 20, True, None]', mono=True)
    d.text(45, 277, "values", mono=True, color=BLUE)
    d.arrow("140,270 235,270")
    d.text(235, 202, "Объект list: четыре ссылки", color=BLUE, bold=True)
    d.box(235, 222, 690, 96)
    for i, (kind, value) in enumerate([("str", '"Аня"'), ("int", "20"), ("bool", "True"), ("NoneType", "None")]):
        x = 250 + i * 170
        d.box(x, 237, 150, 65, fill="#eef3fb")
        d.text(x + 15, 276, f"[{i}]", mono=True, size=20)
        d.parts.append(f'<circle cx="{x+115}" cy="270" r="5" fill="{BLUE}"/>')
        d.arrow(f"{x+115},275 {x+115},355 {x+75},355 {x+75},390")
        d.box(x - 5, 390, 160, 105)
        d.text(x + 12, 425, kind, size=21, color=GREEN, mono=True)
        d.text(x + 12, 469, value, size=24, mono=True)
    d.text(40, 563, "Это схема связей между объектами, а не их расположения в памяти.", size=20)
    d.save("mixed-types.svg")


def shallow_copy():
    d = Diagram("Поверхностная копия: новый внешний список", "Вложенные списки остаются общими: копируются ссылки на них.", 570)
    d.text(40, 140, "base = [[1, 2], [3, 4]]; copied = base.copy()", mono=True)
    d.slots(90, 225, "base")
    d.slots(900, 225, "copied")
    d.obj(490, 200, "[1, 2]")
    d.obj(490, 350, "[3, 4]")
    d.arrow("235,254 360,254 490,230")
    d.arrow("235,302 360,302 490,380")
    d.arrow("1045,254 1115,254 1115,180 600,180 600,200")
    d.arrow("1045,302 1115,302 1115,435 600,435 600,410")
    d.text(70, 488, "base is copied → False", mono=True)
    d.text(70, 531, "base[0] is copied[0] → True", mono=True, color=GREEN)
    d.save("shallow-copy.svg")


def repeated_rows():
    d = Diagram("Повторить ссылку или создать новую строку", "Состояние после присваивания 7 в элемент [0][1] каждого списка.", 620)
    d.text(40, 140, "wrong = [[0] * 3] * 2", mono=True, size=21)
    d.text(620, 140, "right = [[0] * 3 for _ in range(2)]", mono=True, size=21)
    d.text(40, 181, "wrong[0][1] = 7", mono=True, color=BLUE)
    d.text(620, 181, "right[0][1] = 7", mono=True, color=GREEN)
    d.slots(40, 258, "wrong")
    d.slots(620, 258, "right")
    d.obj(335, 280, "[0, 7, 0]", 230)
    d.obj(930, 250, "[0, 7, 0]", 230)
    d.obj(930, 375, "[0, 0, 0]", 230)
    d.arrow("185,287 275,287 335,300")
    d.arrow("185,335 275,335 335,321")
    d.arrow("765,287 850,287 930,280")
    d.arrow("765,335 850,335 930,405")
    d.text(40, 483, "Один объект строки, две ссылки.", size=21)
    d.text(620, 483, "Два отдельных объекта строки.", size=21)
    d.text(40, 530, "[[0, 7, 0], [0, 7, 0]]", mono=True, size=21)
    d.text(620, 530, "[[0, 7, 0], [0, 0, 0]]", mono=True, size=21)
    d.text(40, 591, "Умножение повторяет ссылки на те же объекты. Вложенные списки не копируются.", size=20, color=GREEN)
    d.save("repeated-rows.svg")


def deepcopy_graph():
    d = Diagram("deepcopy сохраняет связи внутри копии", "В этом примере вложенная строка скопирована один раз: обе новые ссылки ведут к ней.", 570)
    d.text(40, 137, "from copy import deepcopy", mono=True, size=21)
    d.text(40, 175, "row = [1, 2]; base = [row, row]; cloned = deepcopy(base)", mono=True, size=21)
    d.slots(40, 280, "base")
    d.slots(620, 280, "cloned")
    d.obj(340, 305, "[1, 2]")
    d.obj(930, 305, "[1, 2]")
    d.text(340, 269, "row", mono=True, color=BLUE)
    d.arrow("367,276 367,305")
    for x, target in [(185, 340), (765, 930)]:
        d.arrow(f"{x},309 {target-50},309 {target},323")
        d.arrow(f"{x},357 {target-50},357 {target},346")
    d.text(40, 452, "base[0] is cloned[0] → False", mono=True)
    d.text(40, 495, "cloned[0] is cloned[1] → True", mono=True, color=GREEN)
    d.text(40, 545, "Изменение cloned[0] затронет cloned[1], но не исходную row.", size=21)
    d.save("deepcopy-graph.svg")


def json_roundtrip():
    d = Diagram("JSON: из объекта в текст и обратно", "dumps возвращает строку str; loads читает строку и создаёт объекты Python.", 730)
    for x, title in [(35, "Python · dict"), (435, "JSON · str"), (835, "Python · новый dict")]:
        d.text(x + 10, 158, title, size=22, color=BLUE, bold=True)
        d.box(x, 240, 330, 310)
    d.arrow("220,225 220,196 580,196 580,225")
    d.arrow("640,225 640,196 1000,196 1000,225")
    d.text(295, 187, "json.dumps", size=21, mono=True)
    d.text(710, 187, "json.loads", size=21, mono=True)
    py = ["{", "  'name': 'Аня',", "  'scores': [10, 20],", "  'active': True,", "  'note': None", "}"]
    js = ["{", '  "name": "Аня",', '  "scores": [', "    10,", "    20", "  ],", '  "active": true,', '  "note": null', "}"]
    for x, lines in [(50, py), (450, js), (850, py)]:
        for i, line in enumerate(lines):
            d.text(x, 275 + i * 32, line, size=20, mono=True)
    d.text(40, 595, "text = json.dumps(data, ensure_ascii=False, indent=2)", mono=True, size=21)
    d.text(40, 631, "restored = json.loads(text)", mono=True, size=21)
    d.text(40, 697, "Для открытого файла: json.dump(data, file) записывает; json.load(file) читает.", size=21, color=GREEN)
    d.save("json-roundtrip.svg")


if __name__ == "__main__":
    names_and_objects()
    mixed_types()
    shallow_copy()
    repeated_rows()
    deepcopy_graph()
    json_roundtrip()
