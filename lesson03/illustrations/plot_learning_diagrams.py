"""Построить пять схем для лекции 3.

Запуск: python plot_learning_diagrams.py (нужен matplotlib).
Для просмотра готовых PNG в ноутбуке matplotlib не требуется.
"""

from math import log2
import os
from pathlib import Path
import tempfile

os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "lecture03-diagram-mpl")
)

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


OUTPUT_DIR = Path(__file__).resolve().parent
WIDTH = 1040
PAPER = "#fffefa"
INK = "#263630"
MUTED = "#65716a"
BLUE = "#245fa8"
GREEN = "#267454"
AMBER = "#aa6018"
LINE = "#dce2dc"
BLUE_LIGHT = "#eaf1fa"
GREEN_LIGHT = "#eaf3ec"
AMBER_LIGHT = "#fff0d9"
GRAY = "#edf0eb"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "text.color": INK,
        "font.size": 13,
        "savefig.facecolor": PAPER,
    }
)


def canvas(height, title, subtitle):
    fig = plt.figure(figsize=(WIDTH / 100, height / 100), facecolor=PAPER)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set(xlim=(0, WIDTH), ylim=(height, 0))
    ax.axis("off")
    text(ax, 44, 32, title, size=22, weight="bold")
    text(ax, 44, 79, subtitle, size=12, color=MUTED)
    return fig, ax


def text(ax, x, y, value, size=13, color=INK, weight="normal", **kwargs):
    return ax.text(
        x, y, value, fontsize=size, color=color, weight=weight,
        va="top", **kwargs,
    )


def box(ax, x, y, width, height, fill="white", edge=LINE, radius=10):
    ax.add_patch(
        FancyBboxPatch(
            (x, y), width, height,
            boxstyle=f"round,pad=0,rounding_size={radius}",
            facecolor=fill, edgecolor=edge, linewidth=1,
        )
    )


def tile(ax, x, y, size, color):
    ax.add_patch(Rectangle((x, y), size, size, facecolor=color, edgecolor="none"))


def arrow(ax, x1, y1, x2, y2, color=MUTED):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1), (x2, y2), arrowstyle="->", mutation_scale=13,
            linewidth=1.4, color=color,
        )
    )


def save(fig, filename):
    # Reject cropped captions before writing a figure.
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bounds = fig.bbox
    for ax in fig.axes:
        for label in ax.texts:
            extent = label.get_window_extent(renderer)
            if not (
                bounds.x0 <= extent.x0 and extent.x1 <= bounds.x1
                and bounds.y0 <= extent.y0 and extent.y1 <= bounds.y1
            ):
                raise ValueError(f"Text outside {filename}: {label.get_text()}")
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=160)
    plt.close(fig)
    print(path.name)


def loop_work():
    fig, ax = canvas(
        755,
        "От кода — к числу действий",
        "Считаем выполнения count += 1. Одна цветная клетка — одно такое действие. n = 4.",
    )
    panels = [
        (
            "Один цикл", BLUE, BLUE_LIGHT,
            "count = 0\nfor i in range(n):\n    count += 1",
            1, 4, "n действий",
        ),
        (
            "Два цикла подряд", GREEN, GREEN_LIGHT,
            "count = 0\nfor i in range(n):\n    count += 1\nfor j in range(n):\n    count += 1",
            2, 8, "n + n = 2n действий",
        ),
        (
            "Вложенные циклы", AMBER, AMBER_LIGHT,
            "count = 0\nfor i in range(n):\n    for j in range(n):\n        count += 1",
            4, 16, "n × n = n² действий",
        ),
    ]
    for x, panel in zip((44, 370, 696), panels):
        title, color, light, source, rows, count, general = panel
        namespace = {"n": 4}
        exec(source, namespace)
        assert namespace["count"] == count
        box(ax, x, 126, 300, 551)
        text(ax, x + 18, 148, title, size=15, weight="bold", color=color)
        box(ax, x + 14, 191, 272, 156, fill=light, edge=light, radius=6)
        text(ax, x + 25, 208, source, size=11.1, family="DejaVu Sans Mono", linespacing=1.4)
        for row in range(rows):
            for col in range(4):
                tile(ax, x + 55 + col * 50, 381 + row * 43, 36, color)
        text(ax, x + 150, 583, f"{count} действий", size=22, weight="bold", ha="center")
        text(ax, x + 150, 630, general, size=13, color=color, ha="center")
    text(
        ax, 44, 708,
        "Проходы подряд: складываем работу. Полный проход внутри каждого шага: перемножаем.",
        size=12,
    )
    save(fig, "loop-work.png")


def growth_doubling():
    fig, ax = canvas(
        795,
        "Данных вдвое больше. А работы?",
        "Значения функций при n = 8, 16 и 32. Цветная клетка — одна условная операция.",
    )
    columns = (385, 630, 875)
    sizes = (8, 16, 32)
    for x, n in zip(columns, sizes):
        text(ax, x, 130, f"n = {n}", size=18, weight="bold", ha="center")
    for x1, x2 in zip(columns, columns[1:]):
        arrow(ax, x1 + 60, 146, x2 - 60, 146)
        text(ax, (x1 + x2) / 2, 119, "×2", size=11, ha="center", color=MUTED)

    rows = [
        ("log₂ n", "логарифмический рост", BLUE, BLUE_LIGHT, 192, 118, "+1", [int(log2(n)) for n in sizes]),
        ("n", "линейный рост", GREEN, GREEN_LIGHT, 326, 118, "×2", list(sizes)),
        ("n²", "квадратичный рост", AMBER, AMBER_LIGHT, 460, 249, "×4", [n * n for n in sizes]),
    ]
    for label, name, color, light, top, height, change, counts in rows:
        box(ax, 44, top, 952, height, fill=light, edge=light)
        text(ax, 66, top + 23, label, size=25, weight="bold", color=color)
        text(ax, 66, top + 72, name, size=10.5, color=MUTED)
        for x, n, count in zip(columns, sizes, counts):
            text(ax, x, top + 12, f"{count:,}".replace(",", " "), size=27, weight="bold", color=color, ha="center")
            side = n if label == "n²" else count
            tile_rows = n if label == "n²" else 1
            left = x - (side * 5 - 1) / 2
            for row in range(tile_rows):
                for col in range(side):
                    tile(ax, left + col * 5, top + 78 + row * 5, 4, color)
        for x1, x2 in zip(columns, columns[1:]):
            arrow(ax, x1 + 65, top + 40, x2 - 65, top + 40, color=color)
            text(ax, (x1 + x2) / 2, top + 12, change, size=12, color=color, ha="center")
    text(ax, 44, 744, "Сравниваем число действий при росте входа, а не секунды на конкретном компьютере.", size=12)
    save(fig, "growth-doubling.png")


def binary_search_idea():
    values = [2, 5, 8, 12, 16, 23, 38]
    target = 16
    middle = len(values) // 2
    assert values == sorted(values)
    assert all(value < target for value in values[:middle + 1])

    fig, ax = canvas(
        723,
        "Бинарный поиск: почему половину можно исключить?",
        "Ищем число 16. Список отсортирован по возрастанию.",
    )
    text(
        ax, 520, 142, "Сравниваем цель с серединой: 12 < 16",
        size=17, weight="bold", color=AMBER, ha="center",
    )
    arrow(ax, 520, 180, 520, 216, color=AMBER)
    array_x, cell_width, row_y = 114, 116, 228
    for index, value in enumerate(values):
        x = array_x + index * cell_width
        fill = AMBER_LIGHT if index == middle else GRAY if index < middle else BLUE_LIGHT
        color = AMBER if index == middle else MUTED if index < middle else BLUE
        ax.add_patch(
            Rectangle((x, row_y), cell_width, 70, facecolor=fill, edgecolor=LINE)
        )
        text(
            ax, x + cell_width / 2, row_y + 13, str(value),
            size=26, weight="bold" if index == middle else "normal",
            color=color, ha="center",
        )

    for start, end, color in [(0, middle + 1, MUTED), (middle + 1, len(values), BLUE)]:
        left, right = array_x + start * cell_width, array_x + end * cell_width
        ax.plot([left, left, right, right], [309, 318, 318, 309], color=color, linewidth=1.6)
    text(ax, 346, 341, "Здесь все числа ≤ 12 < 16", size=15, weight="bold", color=MUTED, ha="center")
    text(ax, 346, 378, "Исключаем всю эту часть, включая середину.", size=11.5, ha="center")
    text(ax, 752, 341, "Здесь ещё может быть 16", size=15, weight="bold", color=BLUE, ha="center")
    text(ax, 752, 378, "Остаются 3 кандидата из 7.", size=11.5, ha="center")

    text(ax, 44, 445, "Три возможных результата сравнения", size=16, weight="bold")
    rules = [
        (44, "Середина меньше цели", "values[middle] < target", "Продолжаем справа.", BLUE, BLUE_LIGHT),
        (370, "Середина больше цели", "values[middle] > target", "Продолжаем слева.", AMBER, AMBER_LIGHT),
        (696, "Середина равна цели", "values[middle] == target", "Возвращаем индекс middle.", GREEN, GREEN_LIGHT),
    ]
    for x, title, comparison, decision, color, light in rules:
        box(ax, x, 490, 300, 134, fill=light, edge=light)
        text(ax, x + 16, 509, title, size=13.5, weight="bold", color=color)
        text(ax, x + 16, 550, comparison, size=11.2, family="DejaVu Sans Mono")
        text(ax, x + 16, 585, decision, size=12)
    text(
        ax, 44, 668,
        "Исключать сразу целую часть списка позволяет именно его упорядоченность.",
        size=12, weight="bold",
    )
    save(fig, "binary-search-idea.png")


def binary_search_steps():
    values = [2, 5, 8, 12, 16, 23, 38]
    target = 16
    left, right = 0, len(values)
    steps = []
    while left < right:
        middle = (left + right) // 2
        value = values[middle]
        steps.append((left, right, middle, value))
        if value == target:
            break
        if value < target:
            left = middle + 1
        else:
            right = middle
    assert steps == [(0, 7, 3, 12), (4, 7, 5, 23), (4, 5, 4, 16)]

    fig, ax = canvas(
        892,
        "Бинарный поиск: три шага до 16",
        "Позиции нумеруются с нуля. В работе только диапазон [left, right).",
    )
    for x, fill, label in [
        (44, BLUE_LIGHT, "ещё проверяем"), (282, GRAY, "уже исключено"),
        (520, AMBER_LIGHT, "середина"), (732, GREEN_LIGHT, "найдено"),
    ]:
        box(ax, x, 124, 20, 20, fill=fill, radius=3)
        text(ax, x + 29, 124, label, size=11.5)

    array_x, cell_width = 373, 75
    captions = [
        "12 < 16 → left = 4. Позиции 0–3 больше не рассматриваем.",
        "23 > 16 → right = 5. Позиции 5–6 больше не рассматриваем.",
        "16 = 16 → ответ: индекс 4. Поиск закончен.",
    ]
    for number, ((left, right, middle, value), caption) in enumerate(zip(steps, captions), start=1):
        top = 174 + (number - 1) * 206
        box(ax, 44, top, 952, 189)
        text(ax, 64, top + 22, f"Шаг {number}   [{left}, {right})", size=16, weight="bold")
        text(ax, 64, top + 62, f"middle = {middle}", size=13, color=MUTED, family="DejaVu Sans Mono")
        text(ax, 64, top + 91, f"values[{middle}] = {value}", size=12, color=MUTED, family="DejaVu Sans Mono")
        row_y = top + 49
        for index, item in enumerate(values):
            active = left <= index < right
            fill = BLUE_LIGHT if active else GRAY
            if index == middle:
                fill = GREEN_LIGHT if item == target else AMBER_LIGHT
            color = INK if active else "#8d978f"
            x = array_x + index * cell_width
            ax.add_patch(Rectangle((x, row_y), cell_width, 43, facecolor=fill, edgecolor=LINE))
            text(ax, x + cell_width / 2, row_y - 23, str(index), size=10, color=MUTED, ha="center")
            text(ax, x + cell_width / 2, row_y + 6, str(item), size=17, weight="bold" if index == middle else "normal", color=color, ha="center")
        lx, rx = array_x + left * cell_width, array_x + right * cell_width
        bracket_y = row_y + 53
        ax.plot([lx, lx, rx, rx], [bracket_y - 6, bracket_y, bracket_y, bracket_y - 6], color=BLUE, linewidth=1.6)
        text(ax, lx, bracket_y + 8, f"left = {left}", size=10.5, color=BLUE, ha="right")
        text(ax, rx, bracket_y + 8, f"right = {right}", size=10.5, color=BLUE, ha="left")
        text(ax, 64, top + 153, caption, size=12, color=GREEN if value == target else INK)
    text(ax, 44, 818, "right — первая позиция за рабочим диапазоном: она не включена.", size=12)
    text(ax, 44, 850, "right = 7 означает границу после последнего элемента, а не обращение к values[7].", size=11, color=MUTED)
    save(fig, "binary-search-steps.png")


def array_boxes(ax, x, y, values, color, width=52, height=42):
    for i, value in enumerate(values):
        ax.add_patch(Rectangle((x + i * width, y), width, height, facecolor=color, edgecolor=LINE))
        text(ax, x + (i + 0.5) * width, y + 10, str(value), size=12, ha="center")


def memory_accounting():
    fig, ax = canvas(
        906,
        "Что занимает память?",
        "Пример: функция получает список чисел и возвращает новый список их квадратов.",
    )
    panels = [
        (44, "Вход", BLUE, BLUE_LIGHT, "values", "n элементов уже даны", "Вход не включаем\nв дополнительную память."),
        (370, "Результат", GREEN, GREEN_LIGHT, "result", "Θ(n) для результата", "Память для ответа\nсчитаем отдельно."),
        (696, "Временные данные", AMBER, AMBER_LIGHT, "Переменные цикла", "Θ(1) сверх результата", "Число переменных\nне растёт с n."),
    ]
    for x, title, color, light, label, cost, caption in panels:
        box(ax, x, 129, 300, 250)
        text(ax, x + 18, 151, title, size=16, weight="bold", color=color)
        text(ax, x + 18, 193, label, size=12, color=MUTED)
        if label == "values":
            array_boxes(ax, x + 46, 229, [10, 20, 30, 40], light)
        elif label == "result":
            array_boxes(ax, x + 30, 229, [v * v for v in [10, 20, 30, 40]], light, width=60)
        else:
            box(ax, x + 18, 229, 264, 42, fill=light, edge=light, radius=4)
            text(ax, x + 150, 241, "i = 3     value = 40", size=12, ha="center", family="DejaVu Sans Mono")
        text(ax, x + 18, 297, cost, size=15, weight="bold", color=color)
        text(ax, x + 18, 333, caption, size=10.5, color=MUTED, linespacing=1.25)

    text(ax, 44, 418, "Другой пример: обход со срезом", size=18, weight="bold")
    box(ax, 44, 465, 952, 253, fill="#f5f6f1", edge="#f5f6f1")
    text(ax, 65, 482, "for value in values[1:]:", size=14, family="DejaVu Sans Mono")
    text(ax, 65, 543, "Исходный values", size=12, color=BLUE)
    array_boxes(ax, 270, 536, [10, 20, 30, 40], BLUE_LIGHT, width=66)
    text(ax, 65, 622, "Временный срез", size=12, color=AMBER)
    array_boxes(ax, 270, 615, [20, 30, 40], AMBER_LIGHT, width=66)
    arrow(ax, 562, 559, 562, 637, color=AMBER)
    text(ax, 622, 550, "Ещё n − 1 ячеек списка", size=14, weight="bold", color=AMBER)
    text(ax, 622, 591, "Θ(n) вспомогательной\nпамяти", size=14, color=AMBER, linespacing=1.5)
    text(ax, 65, 680, "Срез создаёт новый список ссылок на прежние элементы.", size=11, color=MUTED)

    text(ax, 44, 753, "for value in values:", size=14, family="DejaVu Sans Mono")
    text(ax, 395, 754, "Прямой обход не создаёт копию списка.", size=13, color=GREEN)
    text(ax, 44, 813, "Итого для списка квадратов: результат — Θ(n), вспомогательная память — Θ(1).", size=12)
    text(ax, 44, 851, "Здесь считаем ячейки и переменные, не учитывая размер отдельных целых чисел.", size=11, color=MUTED)
    save(fig, "memory-accounting.png")


if __name__ == "__main__":
    loop_work()
    growth_doubling()
    binary_search_idea()
    binary_search_steps()
    memory_accounting()
