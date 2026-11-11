#!/usr/bin/env python3
"""Создать схемы областей видимости, замыканий и декораторов."""

from html import escape
from math import hypot
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BLUE = "#2459a6"
GREEN = "#246954"


def text(x, y, value, *, size=23, anchor="start", weight="400", fill="#243247"):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" '
        f'font-weight="{weight}" fill="{fill}">{escape(value)}</text>'
    )


def box(x, y, width, height, label, detail, *, color=BLUE, fill="#eef3fb"):
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'rx="14" fill="{fill}" stroke="{color}" stroke-width="2"/>'
        + text(x + 20, y + 37, label, size=24, weight="600")
        + text(x + 20, y + 72, detail, size=19)
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
    body = text(40, 48, "Где искать имя: от текущей функции наружу", size=30, weight="600")
    rows = [
        (100, "L · Local", "Текущий вызов: name, clean_name"),
        (220, "E · Enclosing", "Внешняя функция make_labeler: prefix"),
        (340, "G · Global", "Модуль определения: separator"),
        (460, "B · Builtins", "Встроенные имена: len, int, print"),
    ]
    for y, label, detail in rows:
        body += box(60, y, 650, 90, label, detail)
        if y < 460:
            body += arrow(380, y + 90, 380, y + 115)
        body += arrow(715, y + 45, 785, y + 45, color=GREEN)
        body += text(800, y + 42, "Есть привязка?", size=23, fill=GREEN)
        body += text(800, y + 70, "Поиск закончен", size=20, fill=GREEN)
    body += text(60, 610, "Следующий уровень нужен, если на предыдущем нет подходящей привязки.", size=22)
    body += text(60, 648, "Локальные имена вызывающей функции не добавляются в эту цепочку.", size=22)
    body += text(60, 686, "Локальное имя без значения даёт UnboundLocalError, а не поиск снаружи.", size=21)
    save("name-resolution.svg", "Поиск имён LEGB", "Для обычного чтения имени в функции проверяются текущая функция, внешние определения функций, модуль определения и встроенные имена. Найденная привязка завершает поиск. Локальное имя без значения приводит к UnboundLocalError без перехода наружу.", body, 725)

    body = text(40, 48, "Каждый вызов фабрики создаёт своё состояние", size=30, weight="600")
    body += box(50, 110, 470, 100, "make_counter()", "Первый вызов фабрики")
    body += box(580, 110, 470, 100, "make_counter(100)", "Второй вызов фабрики")
    body += arrow(285, 210, 285, 285)
    body += arrow(815, 210, 815, 285)
    body += box(50, 290, 470, 110, "first_counter → next_value", "Своё current: 0 → 1 → 2 → 3", color=GREEN, fill="#edf7f1")
    body += box(580, 290, 470, 110, "second_counter → next_value", "Своё current: 100 → 101", color=GREEN, fill="#edf7f1")
    body += text(285, 460, "nonlocal current", size=26, anchor="middle", weight="600")
    body += text(815, 460, "nonlocal current", size=26, anchor="middle", weight="600")
    body += text(285, 500, "указывает на левую привязку", size=22, anchor="middle")
    body += text(815, 500, "указывает на правую привязку", size=22, anchor="middle")
    body += text(550, 570, "Внешний вызов закончился, доступ к нужной привязке сохранился.", size=23, anchor="middle")
    save("closure-state.svg", "Независимое состояние замыканий", "Две фабрики создают отдельные переменные current и возвращают отдельные функции next_value. nonlocal каждой функции меняет только свою внешнюю переменную.", body, 610)

    body = text(40, 48, "Создать обёртку и вызвать её — разные действия", size=30, weight="600")
    body += text(50, 105, "При декорировании", size=24, weight="600")
    body += box(50, 135, 300, 100, "func", "Исходная функция")
    body += box(405, 135, 300, 100, "trace(func)", "Создаёт wrapper")
    body += box(760, 135, 290, 100, "wrapper", "Сохраняет доступ к func", color=GREEN, fill="#edf7f1")
    body += arrow(350, 185, 400, 185)
    body += arrow(705, 185, 755, 185)
    body += text(50, 325, "При каждом вызове готовой функции", size=24, weight="600")
    body += box(50, 355, 300, 100, "Вход в wrapper", "Общее действие до func")
    body += box(405, 355, 300, 100, "func(*args, **kwargs)", "Исходная работа")
    body += box(760, 355, 290, 100, "Выход из wrapper", "Результат или исключение", color=GREEN, fill="#edf7f1")
    body += arrow(350, 405, 400, 405)
    body += arrow(705, 405, 755, 405)
    body += text(550, 525, "Нужны return для результата и отдельное решение о завершающих действиях.", size=22, anchor="middle")
    save("decorator-flow.svg", "Создание и вызов обёртки", "При декорировании trace получает исходную функцию и возвращает wrapper. При вызове wrapper выполняет общую работу, вызывает сохранённую функцию и передаёт результат или исключение дальше.", body, 570)

    body = text(40, 48, "Декоратор с параметром: три разных вызова", size=30, weight="600")
    rows = [
        (110, "1. announced(label)", 'Получает метку "Импорт"', "Возвращает decorate", "Декоратор с сохранённой меткой"),
        (290, "2. decorate(func)", "Получает исходную функцию", "Возвращает wrapper", "Доступ к label и func"),
        (470, "3. wrapper(*args, **kwargs)", "Получает данные очередного вызова", "Вызывает func", "Передаёт результат или исключение"),
    ]
    for y, left, left_detail, right, right_detail in rows:
        body += box(50, y, 450, 105, left, left_detail)
        body += arrow(500, y + 52, 595, y + 52)
        body += box(600, y, 450, 105, right, right_detail, color=GREEN, fill="#edf7f1")
    body += text(550, 635, "Первые два этапа — при определении; третий — при вызове готовой функции.", size=22, anchor="middle")
    save("decorator-factory.svg", "Три этапа параметризованного декоратора", "Фабрика получает настройку и возвращает декоратор. Декоратор получает функцию и возвращает обёртку. Обёртка получает аргументы каждого последующего вызова.", body, 680)
    print("Созданы 4 SVG-схемы")


if __name__ == "__main__":
    main()
