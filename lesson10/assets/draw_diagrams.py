#!/usr/bin/env python3
"""Пересоздать четыре SVG-схемы ООП-1 без внешних библиотек."""

from html import escape
from math import hypot
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BLUE = "#2459a6"
GREEN = "#246954"
RED = "#a93832"


def text(x, y, value, *, size=23, anchor="start", weight="400", fill="#243247"):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" '
        f'font-weight="{weight}" fill="{fill}">{escape(value)}</text>'
    )


def box(x, y, width, height, label, detail, *, color=BLUE, fill="#eef3fb"):
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="14" '
        f'fill="{fill}" stroke="{color}" stroke-width="2"/>'
        + text(x + 20, y + 37, label, size=24, weight="600")
        + text(x + 20, y + 72, detail, size=20)
    )


def arrow(x1, y1, x2, y2, *, color=BLUE):
    distance = hypot(x2 - x1, y2 - y1)
    dx, dy = (x2 - x1) / distance, (y2 - y1) / distance
    bx, by = x2 - 12 * dx, y2 - 12 * dy
    points = f"{x2},{y2} {bx - 6 * dy},{by + 6 * dx} {bx + 6 * dy},{by - 6 * dx}"
    return (
        f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="3"/>'
        f'<polygon points="{points}" fill="{color}"/>'
    )


def save(filename, title, description, body, height):
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="{height}" '
        f'viewBox="0 0 1100 {height}" role="img" aria-labelledby="title desc">'
        f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>'
        f'<rect width="1100" height="{height}" rx="18" fill="#fcfcfa"/>'
        '<g font-family="Arial, Helvetica, sans-serif">'
        + body + '</g></svg>\n'
    )
    (ROOT / filename).write_text(svg, encoding="utf-8")


def main():
    body = text(40, 48, "Один класс, два экземпляра, два состояния", size=30, weight="600")
    body += box(300, 105, 500, 105, "Класс Counter", "Общая настройка unit, методы __init__ и add")
    body += arrow(450, 210, 280, 315)
    body += arrow(650, 210, 820, 315)
    body += box(50, 320, 450, 115, "left → первый экземпляр", "Собственный атрибут value = 12", color=GREEN, fill="#edf7f1")
    body += box(600, 320, 450, 115, "right → второй экземпляр", "Собственный атрибут value = 1", color=GREEN, fill="#edf7f1")
    body += text(550, 505, "Методы описаны в классе; текущие значения принадлежат экземплярам.", size=23, anchor="middle")
    save("class-and-instances.svg", "Класс и отдельные экземпляры", "Counter задаёт общую настройку и методы. Два вызова Counter создают отдельные экземпляры со своими атрибутами value.", body, 550)

    body = text(40, 48, "Связанный метод передаёт нужный экземпляр", size=30, weight="600")
    body += box(50, 110, 410, 105, "left.add(3)", "Вызов через экземпляр")
    body += arrow(460, 162, 595, 162)
    body += box(600, 110, 450, 105, "Counter.add(left, 3)", "Эквивалент для обычного метода")
    body += arrow(820, 215, 820, 300)
    body += box(600, 305, 450, 115, "def add(self, amount)", "self → left, amount → 3", color=GREEN, fill="#edf7f1")
    body += box(50, 305, 410, 115, "saved_add = left.add", "Сохраняет связь с тем же left")
    body += arrow(460, 362, 595, 362)
    body += text(550, 500, "self.value относится к переданному объекту. Отдельно передавать self не нужно.", size=22, anchor="middle")
    save("bound-method.svg", "Объект в параметре self", "При вызове left.add экземпляр left автоматически становится self. Сохранённый связанный метод помнит тот же объект.", body, 545)

    body = text(40, 48, "Сначала проверить, затем изменить", size=30, weight="600")
    body += box(50, 105, 1000, 100, "Исходное состояние: quantity = 6", "Нужно списать amount; результат должен оставаться неотрицательным")
    body += arrow(550, 205, 550, 270)
    body += box(300, 275, 500, 105, "Проверки метода remove", "amount > 0 и amount <= quantity")
    body += arrow(420, 380, 280, 455, color=GREEN)
    body += arrow(680, 380, 820, 455, color=RED)
    body += box(50, 460, 450, 110, "Проверки прошли: amount = 2", "Изменить quantity: 6 → 4", color=GREEN, fill="#edf7f1")
    body += box(600, 460, 450, 110, "Отказ: amount = 100", "ValueError; quantity остаётся 6", color=RED, fill="#fcefeb")
    body += text(550, 630, "Сохранность при отказе обеспечивает порядок действий в коде метода.", size=23, anchor="middle")
    save("invariant-transition.svg", "Проверка изменения состояния", "Метод сначала проверяет сумму и доступное количество. Успешный путь изменяет состояние; отказ поднимает ValueError до изменения.", body, 675)

    body = text(40, 48, "Копии защищают границы внутреннего списка", size=30, weight="600")
    body += box(50, 110, 320, 110, "Входной список", 'source_entries = ["открыт"]')
    body += arrow(370, 165, 425, 165)
    body += box(430, 110, 620, 110, "EventLog.__init__", "self._entries = entries.copy()", color=GREEN, fill="#edf7f1")
    body += text(390, 270, "Изменение входного списка не меняет внутренний.", size=23)
    body += box(50, 355, 500, 115, "Внутреннее состояние журнала", "Изменяется методом record")
    body += arrow(550, 412, 625, 412)
    body += box(630, 355, 420, 115, "log.entries → новая копия", "Снимок для вызывающего кода", color=GREEN, fill="#edf7f1")
    body += text(550, 540, "Изменение снимка не меняет журнал; элементы здесь — неизменяемые строки.", size=22, anchor="middle")
    save("defensive-copy.svg", "Две границы копирования коллекции", "Конструктор EventLog копирует переданный список. Свойство entries возвращает новую поверхностную копию. Строковые элементы не требуют глубокого копирования.", body, 585)
    print("Созданы 4 SVG-схемы")


if __name__ == "__main__":
    main()
