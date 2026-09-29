"""Rebuild the lecture's SVG diagrams using only the standard library.

Run: python lesson04/assets/draw_diagrams.py
"""

from html import escape
from pathlib import Path


HERE = Path(__file__).resolve().parent
INK = "#203047"
BLUE = "#2764b7"
GREEN = "#197568"
ORANGE = "#b86524"


class Diagram:
    def __init__(self, title, subtitle, height=470):
        self.height = height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" '
            f'viewBox="0 0 1200 {height}" role="img">',
            f"<title>{escape(title)}</title><desc>{escape(subtitle)}</desc>",
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
            '<path d="M 0 0 L 10 5 L 0 10 z" fill="#63768b"/></marker></defs>',
            '<style>text{font-family:Arial,DejaVu Sans,sans-serif;fill:#203047}'
            '.mono{font-family:Menlo,DejaVu Sans Mono,monospace}</style>',
            f'<rect width="1200" height="{height}" rx="20" fill="#f5f7fb"/>',
            '<rect x="32" y="31" width="7" height="62" rx="3" fill="#2764b7"/>',
        ]
        self.text(58, 57, title, size=30, bold=True)
        self.text(58, 91, subtitle, size=19)

    def text(self, x, y, value, size=22, bold=False, color=INK, mono=False):
        cls = ' class="mono"' if mono else ""
        self.parts.append(
            f'<text x="{x}" y="{y}" font-size="{size}" '
            f'font-weight="{700 if bold else 400}" style="fill:{color}"{cls}>'
            f"{escape(value)}</text>"
        )

    def box(self, x, y, w, h, title, lines=(), fill="#ffffff", color=BLUE):
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" '
            f'fill="{fill}" stroke="#cdd7e4" stroke-width="1.5"/>'
        )
        self.text(x + 18, y + 33, title, size=23, bold=True, color=color)
        for i, line in enumerate(lines):
            self.text(x + 18, y + 67 + i * 29, line, size=20)

    def arrow(self, points, label=None, label_at=None):
        self.parts.append(
            f'<polyline points="{points}" fill="none" stroke="#63768b" '
            'stroke-width="2.5" marker-end="url(#arrow)"/>'
        )
        if label:
            self.text(*label_at, label, size=18, color=GREEN)

    def note(self, value):
        self.text(40, self.height - 25, value, size=19, color=GREEN)

    def save(self, name):
        (HERE / name).write_text("\n".join(self.parts + ["</svg>"]) + "\n", encoding="utf-8")


def data_pipeline():
    d = Diagram("От файла к ответу", "Автоматизация выполняет правило; анализ данных помогает ответить на вопрос.")
    boxes = [
        ("1. CSV", ["category, amount", "books, 300", "games, 500", "books, 200"]),
        ("2. Проверка", ["amount → int", "категория заполнена", "ошибка → сообщить"]),
        ("3. Вычисление", ["сумма по категориям", "books: 500", "games: 500"]),
        ("4. Результат", ["таблица или график", "отчёт в файл", "ответ человеку"]),
    ]
    for i, (title, lines) in enumerate(boxes):
        x = 35 + i * 295
        d.box(x, 147, 245, 202, title, lines)
        if i < 3:
            d.arrow(f"{x+245},245 {x+291},245")
    d.text(52, 398, "csv, pathlib", mono=True, size=20)
    d.text(348, 398, "ваши правила", size=20)
    d.text(638, 398, "Python / pandas", mono=True, size=20)
    d.text(920, 398, "Matplotlib", mono=True, size=20)
    d.note("Библиотека читает формат и строит график. Смысл показателя задаёте вы.")
    d.save("data-pipeline.svg")


def machine_learning():
    d = Diagram("Обучить модель ≠ применить модель", "Пример: оценить длительность поездки по расстоянию.", 540)
    d.text(40, 139, "ОБУЧЕНИЕ", size=17, bold=True, color=BLUE)
    d.box(40, 158, 285, 132, "Известные поездки", ["расстояния X", "реальные длительности y"])
    d.box(450, 158, 250, 132, "fit(X, y)", ["подобрать параметры", "по примерам"])
    d.box(825, 158, 325, 132, "Обученная модель", ["хранит найденную", "зависимость"])
    d.arrow("325,222 450,222")
    d.arrow("700,222 825,222")
    d.text(40, 328, "ПРИМЕНЕНИЕ И ПРОВЕРКА", size=17, bold=True, color=GREEN)
    d.box(40, 345, 285, 117, "Другая поездка", ["новое расстояние"])
    d.box(450, 345, 250, 117, "predict(X_new)", ["использовать модель"])
    d.box(825, 345, 325, 117, "Прогноз", ["сравнить с фактом"])
    d.arrow("325,402 450,402")
    d.arrow("700,402 825,402")
    d.arrow("987,290 987,316 575,316 575,345")
    d.note("Проверочные примеры не участвуют в обучении: иначе оценка качества будет нечестной.")
    d.save("machine-learning.svg")


def web_request():
    d = Diagram("Веб-приложение: один запрос и один ответ", "Сервер принимает HTTP, обработчик выполняет правило, ответ возвращается клиенту.", 500)
    d.box(40, 185, 230, 152, "Браузер", ["пользователь", "открыл ссылку"])
    d.box(460, 185, 260, 152, "Сервер + FastAPI", ["разобрать запрос", "вызвать hello(name)"])
    d.box(875, 185, 285, 152, "Ваша функция", ["собрать приветствие", "вернуть dict"])
    d.arrow("270,220 460,220", "GET /hello?name=Ann", (264, 164))
    d.arrow("720,220 875,220", "name='Ann'", (724, 164))
    d.arrow("875,302 720,302", "словарь Python", (726, 375))
    d.arrow("460,302 270,302", "HTTP 200 + JSON", (275, 375))
    d.text(281, 425, '{"message": "Hello, Ann!"}', mono=True, size=23)
    d.note("Прямой вызов hello('Ann') проверяет функцию; HTTP требует работающего сервера.")
    d.save("web-request.svg")


def bot_exchange():
    d = Diagram("Бот общается с Telegram через API", "Long polling: программа ждёт новые события и отправляет ответ отдельным запросом.", 505)
    d.box(40, 180, 245, 167, "Пользователь", ["сообщение: «привет»", "ответ: «Вы написали:", "привет»"])
    d.box(470, 180, 260, 167, "Сервис Telegram", ["хранит обновления", "доставляет сообщения"])
    d.box(900, 180, 260, 167, "Python-бот", ["читает text и chat_id", "вычисляет ответ"])
    d.arrow("285,220 470,220", "сообщение", (318, 161))
    d.arrow("900,204 730,204", "getUpdates", (743, 141))
    d.arrow("730,267 900,267", "JSON события", (747, 254))
    d.arrow("900,326 730,326", "sendMessage", (746, 374))
    d.arrow("470,318 285,318", "ответ в чат", (328, 374))
    d.text(43, 433, "Цикл бота: получить → обработать → ответить → запросить следующие события", size=22)
    d.note("Вычисления идут в вашей программе. Приложение Telegram служит интерфейсом.")
    d.save("bot-exchange.svg")


def game_loop():
    d = Diagram("Игра — состояние, которое меняется каждый кадр", "Pygame доставляет события и рисует. Правила движения задаёт программа.", 565)
    for i, (title, lines) in enumerate([
        ("1. События", ["нажата клавиша?", "закрыто окно?"]),
        ("2. Обновление", ["x = x + speed · dt", "проверить границу"]),
        ("3. Рисование", ["очистить экран", "нарисовать объект"]),
    ]):
        x = 80 + i * 395
        d.box(x, 155, 300, 143, title, lines)
        if i < 2:
            d.arrow(f"{x+300},225 {x+395},225")
    d.arrow("1020,298 1020,334 230,334 230,298", "следующий кадр", (490, 366))
    d.parts.append('<rect x="80" y="395" width="1090" height="100" rx="13" fill="#213247"/>')
    d.parts.append('<circle cx="255" cy="445" r="21" fill="#f3bb59" opacity="0.4"/>')
    d.parts.append('<circle cx="725" cy="445" r="21" fill="#f3bb59"/>')
    d.arrow("290,445 688,445")
    d.text(95, 453, "x = 20", color="#ffffff", mono=True, size=19)
    d.text(775, 452, "x = 20 + 60 · 0.1 = 26", color="#ffffff", mono=True, size=21)
    d.note("dt — время между кадрами. Так скорость движения меньше зависит от частоты кадров.")
    d.save("game-loop.svg")


def ai_application():
    d = Diagram("Готовая модель — один из компонентов приложения", "Пример: превратить сообщение «завтра в 15:00 созвон» в черновик события.", 520)
    for i, (title, lines) in enumerate([
        ("Сообщение", ["текст человека", "+ текущая дата"]),
        ("Запрос к модели", ["инструкция", "+ нужный контекст"]),
        ("Ответ модели", ["кандидат:", "дата, время, тема"]),
        ("Проверка", ["формат и поля", "дата существует?"]),
    ]):
        x = 35 + i * 295
        d.box(x, 153, 245, 152, title, lines)
        if i < 3:
            d.arrow(f"{x+245},225 {x+291},225")
    d.box(40, 370, 600, 82, "Черновик → человек проверяет → сохранение", fill="#e7f2ef", color=GREEN)
    d.box(740, 370, 425, 82, "Ошибка → уточнить сообщение", fill="#fff0e3", color=ORANGE)
    d.arrow("985,305 985,338 340,338 340,370", "корректно", (560, 328))
    d.arrow("1080,305 1080,370", "не прошло", (1069, 345))
    d.note("Валидный JSON ещё не означает верный смысл: проверяем и структуру, и результат.")
    d.save("ai-application.svg")


def import_bindings():
    d = Diagram("Разный import — разные имена в вашем коде", "Модуль и функция остаются теми же объектами. Меняется способ обращения к ним.", 530)
    d.box(40, 145, 480, 285, "Ваш файл или ячейка", fill="#eaf1fb")
    d.text(64, 230, "import math", mono=True)
    d.text(64, 265, "имя math", size=21)
    d.text(64, 344, "from math import sqrt", mono=True)
    d.text(64, 379, "имя sqrt", size=21)
    d.box(715, 145, 440, 285, "Объект модуля math")
    d.text(740, 208, "pi = 3.14159…", mono=True)
    d.box(865, 248, 265, 85, "функция sqrt", fill="#e7f2ef", color=GREEN)
    d.text(740, 392, "factorial, sin, cos, …", mono=True, size=20)
    d.arrow("240,258 625,258 625,168 715,168")
    d.arrow("240,371 670,371 670,292 865,292")
    d.text(42, 471, "math.sqrt(9)     и     sqrt(9)     вызывают одну и ту же функцию", mono=True, size=23)
    d.note("from не копирует определение функции и не загружает только выбранную строку файла.")
    d.save("import-bindings.svg")


def import_loading():
    d = Diagram("Что происходит при import greetings", "Обычный импорт собственного .py-модуля; кеш sys.modules живёт внутри интерпретатора.", 620)
    d.box(40, 148, 285, 135, "1. Проверить кеш", ['sys.modules', 'имя "greetings"'])
    d.box(465, 148, 285, 135, "2. Найти модуль", ["каталоги из sys.path", "файл greetings.py"])
    d.box(880, 148, 280, 135, "3. Создать модуль", ["своё пространство имён", "добавить в кеш"])
    d.arrow("325,215 465,215", "нет в кеше", (340, 192))
    d.arrow("750,215 880,215")
    d.box(880, 378, 280, 135, "4. Выполнить код", ["сверху вниз", "создать greet и PREFIX"])
    d.box(40, 378, 585, 135, "5. Связать имя greetings с модулем", ["теперь доступно greetings.greet('Маша')", "повторный импорт использует этот же объект"])
    d.arrow("1020,283 1020,378")
    d.arrow("880,446 625,446", "успех", (756, 425))
    d.arrow("182,283 182,378", "уже в кеше", (200, 338))
    d.text(40, 562, "При ошибке загрузки импорт завершается исключением; новая запись модуля удаляется из кеша.", size=21)
    d.note("Встроенные модули и расширения загружаются иначе, но их имена тоже попадают в sys.modules.")
    d.save("import-loading.svg")


def package_tree():
    d = Diagram("Пакет содержит подмодули", "urllib — пакет стандартной библиотеки; parse — модуль для работы с URL.", 530)
    d.box(40, 151, 480, 267, "Пакет urllib", fill="#eaf1fb")
    for i, line in enumerate(["urllib/", "├── __init__.py", "├── parse.py", "├── request.py", "└── error.py"]):
        d.text(72, 225 + 37*i, line, mono=True, size=24)
    d.box(705, 151, 455, 108, "import urllib.parse", ["обращение: urllib.parse.urlsplit(...)"])
    d.box(705, 310, 455, 108, "from urllib import parse", ["обращение: parse.urlsplit(...)"])
    d.arrow("346,298 610,298 610,205 705,205")
    d.arrow("346,298 610,298 610,364 705,364")
    d.text(43, 468, "import urllib сам по себе не обязан загружать все подмодули пакета.", size=24, bold=True)
    d.note("Подмодуль импортируем явно. В обоих вариантах выше загружаются urllib и urllib.parse.")
    d.save("package-tree.svg")


def virtual_environments():
    d = Diagram("У каждого проекта — свой набор библиотек", "venv создаёт окружение; pip или uv устанавливает в него пакеты; import использует их.", 570)
    d.box(420, 128, 360, 90, "Установленный Python", ["основа для обоих окружений"])
    d.arrow("420,174 300,174 300,260")
    d.arrow("780,174 900,174 900,260")
    d.box(40, 260, 540, 224, "Проект A: бот", fill="#eaf1fb")
    d.box(620, 260, 540, 224, "Проект B: отчёт", fill="#e7f2ef", color=GREEN)
    for x, project in [(62, "bot"), (642, "report")]:
        d.text(x, 331, f"{project}/.venv/", mono=True, size=22)
        d.text(x, 370, "свой запуск Python", size=22)
        d.text(x, 409, "своя папка site-packages", mono=True, size=21)
        d.text(x, 449, "свои пакеты и их версии", size=22)
    d.text(43, 520, "pip устанавливает в выбранную среду. Python этой среды ищет там импортируемые модули.", size=21)
    d.note("Код проекта хранится рядом с .venv. Окружение можно заново собрать по списку зависимостей.")
    d.save("virtual-environments.svg")


if __name__ == "__main__":
    data_pipeline()
    machine_learning()
    web_request()
    bot_exchange()
    game_loop()
    ai_application()
    import_bindings()
    import_loading()
    package_tree()
    virtual_environments()
