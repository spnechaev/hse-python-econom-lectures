#!/usr/bin/env python3
"""Пересоздать SVG-схемы лекции 8 средствами стандартной библиотеки."""

from html import escape
from math import hypot
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INK = "#243247"
BLUE = "#2459a6"
RED = "#a93832"
GREEN = "#246954"


def text(x, y, value, *, size=23, fill=INK, anchor="start", weight="400"):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
        f'text-anchor="{anchor}" font-weight="{weight}">{escape(value)}</text>'
    )


def box(x, y, width, height, label, detail, *, fill="#eef3fb", stroke=BLUE):
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="14" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        + text(x + 22, y + 38, label, size=24, weight="600")
        + text(x + 22, y + 72, detail, size=19)
    )


def arrow(x1, y1, x2, y2, *, color=BLUE):
    distance = hypot(x2 - x1, y2 - y1)
    dx, dy = (x2 - x1) / distance, (y2 - y1) / distance
    base_x, base_y = x2 - 12 * dx, y2 - 12 * dy
    points = f"{x2},{y2} {base_x - 6 * dy},{base_y + 6 * dx} {base_x + 6 * dy},{base_y - 6 * dx}"
    return (
        f'<path d="M {x1} {y1} L {x2} {y2}" stroke="{color}" '
        f'stroke-width="3" fill="none"/>'
        f'<polygon points="{points}" fill="{color}"/>'
    )


def save(filename, title, description, body, height):
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="{height}" '
        f'viewBox="0 0 1100 {height}" role="img" aria-labelledby="title desc">'
        f'<title id="title">{escape(title)}</title>'
        f'<desc id="desc">{escape(description)}</desc>'
        f'<rect width="1100" height="{height}" rx="18" fill="#fcfcfa"/>'
        '<g font-family="Arial, Helvetica, sans-serif">'
        + body
        + '</g></svg>\n'
    )
    (ROOT / filename).write_text(svg, encoding="utf-8")


def main():
    body = text(40, 48, "Если обработку ошибки не написать", size=30, weight="600")
    rows = [
        (110, "Спецзначение", "Например, -1 или None", "Обычный возврат", "Проверка нужна в коде", "Следующая команда", "Может выдать неверный итог", BLUE),
        (280, "Статус / errno", "Отказ и причина отдельно", "Обычный возврат", "Проверка нужна в коде", "Следующая команда", "Может выдать неверный итог", BLUE),
        (450, "Исключение", "Нет успешного результата", "Выход с ошибкой", "Нет обычного результата", "Поиск обработчика", "Без него — остановка", RED),
    ]
    for y, label, detail, middle, middle_detail, end, end_detail, color in rows:
        body += box(40, y, 300, 100, label, detail, stroke=color)
        body += arrow(340, y + 50, 400, y + 50, color=color)
        body += box(405, y, 300, 100, middle, middle_detail, stroke=color)
        body += arrow(705, y + 50, 765, y + 50, color=color)
        body += box(770, y, 290, 100, end, end_detail, fill="#fcefeb", stroke=RED)
    body += text(550, 615, "Специальный результат проверяет код. Исключение само меняет ход выполнения.", size=22, anchor="middle")
    save("error-signals.svg", "Возврат ошибки и исключение", "Специальное значение и статус с errno сохраняют обычный возврат и требуют явной проверки. Исключение не возвращает обычного результата и начинает поиск обработчика; без него выполнение останавливается.", body, 650)

    body = text(40, 48, "Вызовы идут внутрь, исключение — наружу", size=30, weight="600")
    body += box(50, 95, 460, 95, "Вызывающий код", "try: total_quantity(lines)")
    body += box(130, 240, 460, 95, "total_quantity", "parse_item_basic(line)")
    body += box(210, 385, 460, 95, "parse_item_basic", 'int("много") → ValueError', fill="#fcefeb", stroke=RED)
    body += arrow(100, 190, 180, 240)
    body += arrow(180, 335, 260, 385)
    body += f'<path d="M 670 430 H 710 V 145" stroke="{RED}" stroke-width="3" fill="none"/>'
    body += text(740, 290, "Нет обработчика", size=21, fill=RED)
    body += text(740, 322, "внутри функций", size=21, fill=RED)
    body += box(740, 95, 310, 95, "except ValueError", "Здесь выбираем реакцию", fill="#edf7f1", stroke=GREEN)
    body += arrow(710, 145, 735, 145, color=RED)
    body += text(50, 540, "Функции со сбоем не возвращают обычный результат.", size=23)
    save("exception-propagation.svg", "Распространение исключения", "Вызов идёт через total_quantity к parse_item_basic. ValueError возвращается по цепочке вызовов к внешнему except.", body, 580)

    body = text(40, 48, "finally выполняется перед продолжением выхода", size=30, weight="600")
    labels = [(45, "Конец try", "Обычный путь"), (405, "return result", "Возврат результата"), (765, "Исключение", "Выход с ошибкой")]
    for x, label, detail in labels:
        body += box(x, 100, 290, 100, label, detail)
        body += arrow(x + 145, 200, 550, 275)
    body += box(355, 280, 390, 100, "finally", "Завершающее действие", fill="#edf7f1", stroke=GREEN)
    for x, label, detail in [(45, "Продолжить", "Следующая команда"), (405, "Вернуть result", "Вызывающему коду"), (765, "Передать ошибку", "Внешнему обработчику")]:
        body += arrow(550, 380, x + 145, 455)
        body += box(x, 460, 290, 100, label, detail)
    body += text(550, 615, "Если finally сам завершился без нового исключения или другого выхода", size=21, anchor="middle")
    save("finally-flow.svg", "Три пути через finally", "Успех, return и исключение проходят через finally, затем каждый путь продолжается своим способом при успешном завершающем действии.", body, 650)

    body = text(40, 48, "with ограничивает время жизни открытого файла", size=30, weight="600")
    body += box(50, 100, 1000, 90, 'with open(path, encoding="utf-8") as source:', "Войти в контекст и получить файловый объект")
    body += arrow(550, 190, 550, 235)
    body += box(140, 240, 820, 120, "Тело блока: файл открыт", "Читаем строки, разбираем данные, получаем результат", fill="#edf7f1", stroke=GREEN)
    for x, label in [(100, "Конец блока"), (440, "return"), (780, "Исключение")]:
        body += arrow(550, 360, x + 110, 415)
        body += text(x + 110, 445, label, size=23, anchor="middle")
        body += arrow(x + 110, 460, 550, 515)
    body += box(300, 520, 500, 95, "Действие выхода: закрыть файл", "Затем продолжить выбранный путь", fill="#eef3fb")
    body += text(550, 665, "Файловый менеджер не подавляет ошибку и не отменяет сделанную запись.", size=22, anchor="middle")
    save("file-lifetime.svg", "Время жизни файла в with", "После успешного входа файл открыт в теле блока; конец блока, return и исключение вызывают закрытие. Ошибка продолжает распространяться.", body, 705)
    print("Созданы 4 SVG-схемы")


if __name__ == "__main__":
    main()
