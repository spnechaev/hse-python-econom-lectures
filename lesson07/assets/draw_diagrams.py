"""Rebuild the hash-table lecture diagrams using only the standard library.

Run from the repository root: python3 lesson07/assets/draw_diagrams.py
"""

from html import escape
from pathlib import Path
from xml.etree import ElementTree


HERE = Path(__file__).resolve().parent
INK, BLUE, GREEN, ORANGE = '#203047', '#2764b7', '#197568', '#b66b13'


class Diagram:
    def __init__(self, title, subtitle, height=600):
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" '
            f'viewBox="0 0 1200 {height}" role="img">',
            f'<title>{escape(title)}</title><desc>{escape(subtitle)}</desc>',
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="7" markerHeight="7" orient="auto">'
            '<path d="M0 0L10 5L0 10Z" fill="#63768b"/></marker></defs>',
            '<style>text{font-family:Arial,DejaVu Sans,sans-serif}'
            '.mono{font-family:Menlo,DejaVu Sans Mono,monospace}</style>',
            f'<rect width="1200" height="{height}" rx="20" fill="#f5f7fb"/>',
        ]
        self.text(40, 52, title, 30, bold=True)
        self.text(40, 88, subtitle, 20)

    def text(self, x, y, s, size=22, color=INK, bold=False, mono=False, anchor='start'):
        self.parts.append(
            f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'font-weight="{700 if bold else 400}" text-anchor="{anchor}" '
            f'class="{"mono" if mono else ""}">{escape(str(s))}</text>'
        )

    def box(self, x, y, w, h, fill='#ffffff', stroke='#cdd7e4'):
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        )

    def arrow(self, x1, y1, x2, y2, label=None):
        self.parts.append(
            f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="#63768b" '
            'stroke-width="2.3" marker-end="url(#arrow)"/>'
        )
        if label:
            self.text((x1 + x2) / 2 + 10, (y1 + y2) / 2 - 8, label, 18, color=BLUE)

    def row(self, x, y, values, active=(), fixed=(), width=64):
        for index, value in enumerate(values):
            fill = '#dbf0e8' if index in fixed else '#fff0d8' if index in active else '#ffffff'
            self.box(x + index * (width + 10), y, width, 46, fill)
            self.text(x + index * (width + 10) + width / 2, y + 31, value, 24,
                      anchor='middle', mono=True)

    def card(self, x, y, w, lines, color=BLUE):
        self.box(x, y, w, 38 + 34 * len(lines))
        for index, line in enumerate(lines):
            self.text(x + 18, y + 34 + index * 34, line, 21,
                      color=color if index == 0 else INK, bold=index == 0)

    def save(self, filename):
        xml = '\n'.join(self.parts + ['</svg>']) + '\n'
        ElementTree.fromstring(xml)
        (HERE / filename).write_text(xml, encoding='utf-8')


def lookup_route(Diagram):
    d = Diagram('От ключа к значению: ищем 3',
                'Хеш выбирает корзину. Совпадение ключей проверяем внутри неё.', 650)
    for x, w, heading, value in [
        (40, 210, 'Ключ', '3'),
        (330, 290, 'Хеш', 'hash(3) = 3'),
        (700, 460, 'Номер корзины', 'hash(3) % 2 = 1'),
    ]:
        d.box(x, 125, w, 95)
        d.text(x + 20, 158, heading, 20, color=BLUE, bold=True)
        d.text(x + 20, 197, value, 26, mono=True)
    d.arrow(260, 175, 320, 175)
    d.arrow(630, 175, 690, 175)
    d.text(40, 277, 'Таблица: две независимые корзины', 22, bold=True)
    d.text(55, 337, '0', 25, mono=True)
    d.box(105, 298, 650, 60, '#edf0f5')
    d.text(130, 337, '[]', 25, mono=True)
    d.text(800, 337, 'Не просматриваем', 21)
    d.text(55, 432, '1', 25, mono=True, color=BLUE)
    d.box(105, 383, 650, 90, '#e8effa', '#2764b7')
    for x, value, fill, color in [(125, '[1, "one"]', '#fff0d8', ORANGE),
                                  (440, '[3, "three"]', '#dbf0e8', GREEN)]:
        d.box(x, 400, 290, 55, fill)
        d.text(x + 20, 436, value, 24, mono=True, color=color)
    d.arrow(1010, 232, 1010, 385)
    d.arrow(1000, 425, 770, 425)
    d.text(810, 407, 'Корзина 1', 22, color=BLUE, bold=True)
    d.text(125, 510, '1 ≠ 3 → дальше', 21, color=ORANGE)
    d.text(440, 510, '3 == 3 → нашли', 21, color=GREEN)
    d.box(40, 550, 1120, 65, '#dbf0e8')
    d.text(60, 590, 'Возвращаем "three". Ключи 1 и 3 делят корзину, но остаются разными.', 23)
    d.save('lookup-route.svg')


def independent_buckets(Diagram):
    d = Diagram('Корзины должны быть разными списками',
                'Копирование ссылки на один список не создаёт независимые корзины.', 600)
    d.text(40, 145, '[[]] * 3', 25, color=ORANGE, mono=True)
    d.text(660, 145, '[[] for _ in range(3)]', 24, color=GREEN, mono=True)
    d.text(40, 183, 'Три ссылки на один объект', 22, color=ORANGE)
    d.text(660, 183, 'Три отдельных объекта', 22, color=GREEN)
    for index, y in enumerate([225, 315, 405]):
        for x in [45, 665]:
            d.box(x, y, 110, 55)
            d.text(x + 55, y + 36, f'[{index}]', 25, mono=True, anchor='middle')
        d.arrow(165, y + 27, 325, 342)
        d.arrow(785, y + 27, 895, y + 27)
        d.box(905, y, 245, 55, '#dbf0e8' if index == 0 else '#ffffff')
        d.text(925, y + 36, '[["test", 1]]' if index == 0 else '[]', 24, mono=True)
    d.box(335, 315, 245, 55, '#fff0d8')
    d.text(355, 351, '[["test", 1]]', 24, mono=True)
    d.text(40, 512, 'После table[0].append(["test", 1]):', 22, mono=True)
    d.text(40, 552, 'Запись видна через все три ссылки.', 22, color=ORANGE)
    d.text(660, 552, 'Изменилась только корзина 0.', 22, color=GREEN)
    d.save('independent-buckets.svg')


def load_factor(Diagram):
    d = Diagram('Те же восемь ключей — разная длина цепочек',
                'Коэффициент заполнения α = число пар / число корзин. Здесь показаны только ключи.', 740)
    d.text(40, 143, '2 корзины: α = 8 / 2 = 4', 24, color=ORANGE, bold=True)
    d.text(660, 143, '8 корзин: α = 8 / 8 = 1', 24, color=GREEN, bold=True)
    for index in range(2):
        y = 215 + index * 125
        d.text(50, y + 33, str(index), 23, mono=True)
        d.box(95, y - 10, 455, 72, '#fff0d8')
        d.row(115, y, [index + 2 * j for j in range(4)])
    for index in range(8):
        y = 178 + index * 48
        d.text(670, y + 29, str(index), 21, mono=True)
        d.box(710, y, 420, 40)
        d.box(720, y + 3, 66, 34, '#dbf0e8')
        d.text(753, y + 28, str(index), 22, mono=True, anchor='middle')
    d.text(40, 459, 'Поиск 6: проверяем 0, 2, 4, 6.', 22, color=ORANGE)
    d.text(40, 497, 'Четыре пары в каждой цепочке.', 22)
    d.text(660, 593, 'Поиск 6: одна пара в корзине 6.', 22, color=GREEN)
    d.box(40, 628, 1120, 78, '#e8effa')
    d.text(60, 660, 'Малое α помогает при хорошем распределении хешей.', 23, bold=True)
    d.text(60, 691, 'Если все ключи попали в одну корзину, поиск всё равно может потребовать O(N).', 21)
    d.save('load-factor.svg')


def rehash(Diagram):
    d = Diagram('Resize: заново распределяем пары по корзинам',
                'Ключи и значения сохраняются. Меняется делитель в hash(key) % capacity.', 720)
    d.text(40, 145, 'До: capacity = 2', 24, color=ORANGE, bold=True)
    d.text(760, 145, 'После: capacity = 8', 24, color=GREEN, bold=True)
    d.text(45, 207, '0', 23, mono=True)
    d.box(85, 177, 320, 45)
    d.text(105, 207, '[]', 24, mono=True)
    d.text(45, 285, '1', 23, mono=True)
    d.box(85, 245, 320, 240, '#fff0d8')
    for index, value in enumerate(['[1, "one"]', '[5, "five"]', '[3, "THREE"]']):
        y = 265 + index * 70
        d.box(103, y, 284, 50)
        d.text(120, y + 33, value, 23, mono=True)
    for index in range(8):
        y = 177 + index * 52
        d.text(760, y + 30, str(index), 22, mono=True)
        d.box(805, y, 350, 44, '#dbf0e8' if index in (1, 3, 5) else '#ffffff')
        values = {1: '[1, "one"]', 3: '[3, "THREE"]', 5: '[5, "five"]'}
        d.text(825, y + 30, values.get(index, '[]'), 23, mono=True)
    for key, y in [(1, 251), (3, 355), (5, 459)]:
        d.box(445, y - 25, 260, 50, '#e8effa')
        d.text(575, y + 8, f'hash({key}) % 8 = {key}', 20, mono=True, anchor='middle')
        d.arrow(715, y, 745, y)
    d.text(40, 545, 'Все три ключа имели', 22)
    d.text(40, 579, 'остаток 1 при делении на 2.', 22)
    d.box(40, 620, 1120, 65, '#fff0d8')
    d.text(60, 661, 'Просто дописать корзины нельзя: поиск 3 теперь идёт в корзину 3, а не в 1.', 23)
    d.save('rehash.svg')


def put_update(Diagram):
    d = Diagram('Вставка: новая пара или новое значение?',
                'Два последовательных вызова на одной таблице. Здесь len(table) = 2.', 740)
    states = [
        (140, 'До вызовов', ['[1, "one"]', '[3, "three"]'], None),
        (315, '1. table_put(table, 5, "five") → True',
         ['[1, "one"]', '[3, "three"]', '[5, "five"]'], 2),
        (490, '2. table_put(table, 3, "THREE") → False',
         ['[1, "one"]', '[3, "THREE"]', '[5, "five"]'], 1),
    ]
    for y, title, pairs, changed in states:
        d.text(40, y, title, 23, color=BLUE, bold=True, mono=y != 140)
        d.box(40, y + 20, 1120, 90)
        d.text(60, y + 75, 'table[1]', 22, mono=True, color=BLUE)
        for index, value in enumerate(pairs):
            x = 240 + index * 300
            fill = '#dbf0e8' if index == changed and y == 315 else '#fff0d8' if index == changed else '#ffffff'
            d.box(x, y + 38, 270, 54, fill)
            d.text(x + 18, y + 74, value, 23, mono=True)
    d.arrow(1090, 260, 1090, 290)
    d.arrow(1090, 435, 1090, 465)
    d.text(40, 650, 'Ключ 5 добавлен: пар стало три. При замене значения ключа 3 их осталось три.', 23)
    d.text(40, 695, 'Совпала корзина ≠ совпал ключ. Возвращаемый bool сообщает о новом ключе.', 22, color=BLUE)
    d.save('put-update.svg')


def delete_pair(Diagram):
    d = Diagram('Удаление: убираем пару из списка', 'Продолжаем тот же пример: удаляем ключ 3 после замены его значения.', 660)
    d.text(40, 145, 'table_delete(table, 3)', 24, mono=True, color=BLUE, bold=True)
    d.text(40, 215, 'До', 24, bold=True)
    for x, idx, value in [(220, 0, '[1, "one"]'), (530, 1, '[3, "THREE"]'), (840, 2, '[5, "five"]')]:
        d.text(x + 130, 190, 'index = ' + str(idx), 20, anchor='middle', color=BLUE, mono=True)
        d.box(x, 205, 270, 64, '#fff0d8' if idx == 1 else '#ffffff')
        d.text(x + 135, 246, value, 23, anchor='middle', mono=True)
    d.text(220, 312, 'Ключ 1 не подходит.', 21)
    d.text(530, 312, 'Ключ 3 найден.', 21, color=ORANGE)
    d.text(530, 350, 'del bucket[1]', 23, color=ORANGE, mono=True)
    d.arrow(975, 280, 665, 395)
    d.text(870, 355, 'Сдвиг на место 1', 20, color=BLUE)
    d.text(40, 448, 'После', 24, bold=True)
    for x, idx, value in [(220, 0, '[1, "one"]'), (530, 1, '[5, "five"]')]:
        d.box(x, 410, 270, 64, '#dbf0e8')
        d.text(x + 135, 451, value, 23, anchor='middle', mono=True)
        d.text(x + 135, 509, 'index = ' + str(idx), 20, anchor='middle', color=GREEN, mono=True)
    d.box(40, 545, 1120, 78, '#dbf0e8')
    d.text(60, 577, 'Первый вызов возвращает True: пара удалена.', 22, color=GREEN, bold=True)
    d.text(60, 608, 'Повторный вызов с ключом 3 вернёт False: такого ключа уже нет.', 21)
    d.save('delete-pair.svg')


def identity_keys(Diagram):
    d = Diagram('Ключ узнаём по объекту или по равенству', 'NaN не равен самому себе. Ниже показаны результаты отдельных сравнений is и ==.', 800)
    d.box(40, 120, 1120, 65, '#dce8fa')
    d.text(600, 162, 'stored_key is key or stored_key == key', 27, mono=True, anchor='middle', color=BLUE)
    d.box(40, 210, 535, 305)
    d.box(625, 210, 535, 305)
    d.text(60, 249, 'Повторно передали nan_key', 24, color=BLUE, bold=True)
    d.text(645, 249, 'Создали other_nan = float("nan")', 22, color=ORANGE, bold=True)
    d.text(60, 295, 'stored_key', 21, mono=True)
    d.text(340, 295, 'key', 21, mono=True)
    d.arrow(175, 310, 260, 355)
    d.arrow(355, 310, 300, 355)
    d.box(210, 365, 180, 50, '#dbf0e8')
    d.text(300, 398, 'Объект A: NaN', 21, anchor='middle', color=GREEN)
    d.text(60, 455, 'is → True;  == → False', 23, mono=True)
    d.text(60, 490, 'Один объект: обновляем значение.', 22, color=GREEN)
    d.box(645, 300, 215, 60, '#dbf0e8')
    d.box(905, 300, 235, 60, '#fff0d8')
    d.text(752, 338, 'Объект A: NaN', 21, anchor='middle', color=GREEN)
    d.text(1022, 338, 'Объект B: NaN', 21, anchor='middle', color=ORANGE)
    d.text(752, 397, 'stored_key', 21, anchor='middle', mono=True)
    d.text(1022, 397, 'key', 21, anchor='middle', mono=True)
    d.text(645, 455, 'is → False;  == → False', 23, mono=True)
    d.text(645, 490, 'Другой объект: добавляем пару.', 22, color=ORANGE)
    d.text(40, 560, 'После обновления A и вставки B в корзине две пары:', 23, color=BLUE, bold=True)
    d.box(40, 585, 535, 65, '#dbf0e8')
    d.text(60, 626, '[объект A, "updated"]', 24, mono=True)
    d.box(625, 585, 535, 65, '#fff0d8')
    d.text(645, 626, '[объект B, "second"]', 24, mono=True)
    d.text(40, 706, 'При True у is правая часть or уже не вычисляется.', 23)
    d.text(40, 751, 'Одну и ту же проверку используем при вставке, поиске и удалении.', 22)
    d.save('identity-keys.svg')


def indexed_join(Diagram):
    d = Diagram('Соединяем таблицы по ключу', 'Ключи балансов уникальны. В этом примере баланс есть для каждого профиля.', 810)
    d.text(40, 145, '1. Один проход по балансам → строим индекс', 24, color=BLUE, bold=True)
    d.box(40, 170, 350, 150)
    d.text(60, 204, 'Балансы', 22, color=BLUE, bold=True)
    d.text(60, 247, 'c-2     300', 24, mono=True)
    d.text(60, 290, 'c-1     120', 24, mono=True)
    d.arrow(410, 245, 570, 245)
    d.box(590, 170, 570, 150, '#dce8fa')
    d.text(610, 204, 'balance_by_client: dict', 22, color=BLUE, bold=True, mono=True)
    d.text(610, 247, 'c-2  →  300', 24)
    d.text(610, 290, 'c-1  →  120', 24)
    d.text(40, 375, '2. Идём по профилям → берём баланс из индекса', 24, color=BLUE, bold=True)
    d.text(60, 425, 'Профили', 22, color=BLUE, bold=True)
    d.text(430, 425, 'Поиск по ключу', 22, color=BLUE, bold=True)
    d.text(850, 425, 'Результат', 22, color=GREEN, bold=True)
    for y, key, balance, name in [(450, 'c-1', 120, 'Анна'), (535, 'c-2', 300, 'Борис')]:
        d.box(40, y, 290, 62)
        d.text(60, y + 39, f'{key}   {name}', 24, mono=True)
        d.arrow(345, y + 31, 410, y + 31)
        d.box(425, y, 335, 62, '#dce8fa')
        d.text(445, y + 39, f'индекс[{key!r}]', 23, mono=True)
        d.arrow(775, y + 31, 830, y + 31)
        d.box(845, y, 315, 62, '#dbf0e8')
        d.text(865, y + 39, f'{name} · {balance}', 24, color=GREEN)
    d.box(40, 640, 1120, 125, '#dbf0e8')
    d.text(60, 678, 'Было: до n × m сравнений во вложенных циклах.', 23)
    d.text(60, 715, 'Стало: O(n + m) в среднем; индекс занимает O(m) памяти.', 23, color=GREEN, bold=True)
    d.text(60, 750, 'n — число профилей, m — число балансов. Порядок результата — как у профилей.', 21)
    d.save('indexed-join.svg')


def ordered_dedup(Diagram):
    d = Diagram('Убираем повторы, сохраняем первые появления', 'seen отвечает «уже встречали?». unique хранит результат в нужном порядке.', 840)
    d.text(40, 140, 'Вход:', 23, color=BLUE, bold=True)
    d.text(150, 140, 'c-2 → c-1 → c-2 → c-3 → c-1', 25, mono=True)
    d.text(40, 188, 'Старт: seen = set(); unique = []', 22, mono=True)
    for x, label in [(60, 'Шаг'), (165, 'Ключ'), (300, 'В seen?'), (475, 'Действие'), (800, 'unique после шага')]:
        d.text(x, 240, label, 22, color=BLUE, bold=True)
    states = [
        ('c-2', False, '[c-2]'),
        ('c-1', False, '[c-2, c-1]'),
        ('c-2', True, '[c-2, c-1]'),
        ('c-3', False, '[c-2, c-1, c-3]'),
        ('c-1', True, '[c-2, c-1, c-3]'),
    ]
    for i, (key, seen, unique) in enumerate(states):
        y = 260 + i * 70
        d.box(40, y, 1120, 57, '#fff0d8' if seen else '#dbf0e8')
        d.text(60, y + 36, i + 1, 23)
        d.text(165, y + 36, key, 23, mono=True)
        d.text(300, y + 36, 'да' if seen else 'нет', 23, color=ORANGE if seen else GREEN)
        d.text(475, y + 36, 'пропускаем' if seen else 'в seen и в unique', 22)
        d.text(800, y + 36, unique, 22, mono=True)
    d.box(40, 640, 535, 150)
    d.text(60, 676, 'seen: множество', 23, color=BLUE, bold=True)
    d.text(60, 716, '{c-1, c-2, c-3}', 24, mono=True)
    d.text(60, 756, 'Порядок элементов не гарантирован.', 21)
    d.box(605, 640, 555, 150, '#dbf0e8')
    d.text(625, 676, 'unique: список', 23, color=GREEN, bold=True)
    d.text(625, 716, '[c-2, c-1, c-3]', 24, mono=True)
    d.text(625, 756, 'Порядок задаёт добавление в список.', 21)
    d.save('ordered-dedup.svg')


if __name__ == '__main__':
    for draw in (
        lookup_route, independent_buckets, put_update, delete_pair,
        identity_keys, load_factor, rehash, indexed_join, ordered_dedup,
    ):
        draw(Diagram)
    print('Rebuilt 9 hash-table diagrams.')
