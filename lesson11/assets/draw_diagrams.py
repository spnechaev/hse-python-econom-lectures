#!/usr/bin/env python3
"""Пересоздать четыре схемы сотрудничества классов для лекции 11."""
from html import escape
from math import hypot
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INK = '#243247'
BLUE = '#2459a6'
GREEN = '#246954'
RED = '#a93832'


def text(x, y, value, *, size=23, color=INK, anchor='start', bold=False):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'text-anchor="{anchor}" font-weight="{600 if bold else 400}">{escape(value)}</text>')


def box(x, y, width, height, title, lines, *, color=BLUE, fill='#eef3fb'):
    result = (f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="14" '
              f'fill="{fill}" stroke="{color}" stroke-width="2"/>')
    result += text(x + 20, y + 36, title, size=25, color=color, bold=True)
    for i, line in enumerate(lines):
        result += text(x + 20, y + 72 + 30*i, line, size=21)
    return result


def arrow(x1, y1, x2, y2, *, color=BLUE):
    length = hypot(x2-x1, y2-y1)
    dx, dy = (x2-x1)/length, (y2-y1)/length
    bx, by = x2-13*dx, y2-13*dy
    return (f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="3"/>'
            f'<polygon points="{x2},{y2} {bx-6*dy},{by+6*dx} {bx+6*dy},{by-6*dx}" fill="{color}"/>')


def save(filename, title, desc, body, height):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="{height}" '
           f'viewBox="0 0 1100 {height}" role="img" aria-labelledby="title desc">'
           f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>'
           f'<rect width="1100" height="{height}" rx="18" fill="#fcfcfa"/>'
           '<g font-family="Arial, Helvetica, sans-serif">' + body + '</g></svg>\n')
    (ROOT/filename).write_text(svg, encoding='utf-8')


def main():
    body = text(40, 50, 'Один заказ, несколько самостоятельных ролей', size=31, bold=True)
    body += box(50, 115, 300, 140, 'Order', ['Товары: 240 000 коп.', 'Вес: 1 500 г'])
    body += box(420, 115, 270, 140, 'Checkout', ['total(order)', 'Складывает цены'])
    body += box(760, 115, 290, 140, 'Courier', ['price(order)', 'Ответ: 50 000 коп.'], color=GREEN, fill='#edf7f1')
    body += arrow(350, 185, 415, 185)
    body += arrow(690, 155, 755, 155)
    body += arrow(755, 220, 695, 220, color=GREEN)
    body += text(723, 293, 'price(order)', size=20, anchor='middle')
    body += box(385, 345, 340, 110, 'Результат расчёта', ['Итого: 290 000 коп.'], color=GREEN, fill='#edf7f1')
    body += arrow(555, 255, 555, 340)
    body += text(550, 515, 'Checkout знает нужный метод, а формулу тарифа хранит доставка.', size=23, anchor='middle')
    save('object-collaboration.svg', 'Сотрудничество объектов', 'Заказ хранит стоимость товаров и вес. Checkout передаёт заказ объекту Courier, получает цену доставки и прибавляет её к стоимости товаров. Взаимодействие идёт через price(order).', body, 555)

    body = text(40, 50, 'Два разных отношения между классами', size=31, bold=True)
    body += text(55, 110, 'Композиция: пользуется помощником', size=25, bold=True)
    body += box(55, 140, 390, 135, 'Checkout', ['Хранит ссылку _delivery', 'Вызывает price(order)'])
    body += box(655, 140, 390, 135, 'Courier или Pickup', ['Отдельный объект', 'Свой способ расчёта'], color=GREEN, fill='#edf7f1')
    body += arrow(450, 205, 650, 205)
    body += text(550, 315, 'Можно передать другого помощника.', size=23, anchor='middle')
    body += text(55, 390, 'Наследование: подходит на место базового типа', size=25, bold=True)
    body += box(55, 425, 390, 135, 'ShippingLabel', ['text() и render()', 'Обещают вернуть строки'])
    body += box(655, 425, 390, 135, 'TrackedLabel', ['Переопределяет text()', 'Сохраняет общий договор'], color=GREEN, fill='#edf7f1')
    body += arrow(650, 490, 450, 490, color=GREEN)
    body += text(550, 610, 'Общий код не заменяет проверку пригодности наследника.', size=23, anchor='middle')
    save('composition-inheritance.svg', 'Композиция и наследование', 'При композиции Checkout хранит отдельный объект доставки. При наследовании TrackedLabel является подклассом ShippingLabel и должен сохранять обещания, нужные клиентам базового типа.', body, 650)

    body = text(40, 50, 'resize(5, 2): что обещано после успеха?', size=31, bold=True)
    body += box(50, 110, 460, 150, 'Rectangle', ['width = 5, height = 2', 'area() = 10'], color=GREEN, fill='#edf7f1')
    body += box(590, 110, 460, 150, 'BadSquare', ['width = 5, height = 5', 'area() = 25'], color=RED, fill='#fcefeb')
    body += text(280, 302, 'Договор выполнен', size=24, color=GREEN, anchor='middle', bold=True)
    body += text(820, 302, 'Договор нарушен', size=24, color=RED, anchor='middle', bold=True)
    body += text(550, 363, 'Отказать на (5, 2) — тоже нарушить прежнее обещание.', size=23, anchor='middle')
    body += box(240, 420, 620, 135, 'Клиенту нужна только площадь?', ['Отдельные Rectangle и Square умеют area().', 'Независимое изменение сторон ему не требуется.'])
    body += text(550, 610, 'Подстановка зависит от методов и их условий, а не только от названий фигур.', size=22, anchor='middle')
    save('rectangle-square-contract.svg', 'Контракт прямоугольника и квадрата', 'Rectangle.resize принимает произвольные положительные размеры и обязан сохранить оба переданных значения. Квадрат, принудительно делающий стороны равными или запрещающий неравные стороны, этому договору не соответствует. Для клиента, читающего только площадь, подходят отдельные реализации area().', body, 650)

    body = text(40, 50, 'Конкретные объекты выбираются в месте сборки', size=30, bold=True)
    body += box(50, 110, 300, 130, 'main', ['Создаёт заказ и доставку', 'Передаёт их в расчёт'])
    body += box(420, 110, 630, 130, 'Checkout', ['Требует price(order) → целое число копеек', 'Не называет класс конкретной доставки'])
    body += arrow(355, 175, 415, 175)
    body += text(50, 300, 'Договор выполняют:', size=24, bold=True)
    variants = [(50, 'Pickup', '0 копеек'), (405, 'Courier', 'Тариф по весу'), (760, 'RecordingDelivery', 'Заранее заданный ответ')]
    for x, label, detail in variants:
        body += box(x, 370, 290, 130, label, [detail], color=GREEN, fill='#edf7f1')
        body += arrow(x+145, 365, 735, 245, color=GREEN)
    body += text(550, 563, 'Реальная доставка и подставной объект нужны одному и тому же клиенту.', size=22, anchor='middle')
    body += text(550, 603, 'Передать объект — способ связать части; узкий договор задаёт направление связи.', size=21, anchor='middle')
    save('dependency-assembly.svg', 'Сборка зависимостей', 'Checkout зависит от небольшого договора price(order). Конкретный объект доставки выбирается снаружи. Pickup, Courier и RecordingDelivery выполняют нужный договор; подставной объект позволяет проверить расчёт локально.', body, 650)
    print('Созданы 4 SVG-схемы')


if __name__ == '__main__':
    main()
