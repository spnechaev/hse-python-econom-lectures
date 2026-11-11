# Занятие 10. Задачи для самостоятельного решения

> **Домашняя работа.** В материалах курса приведены **предполагаемые списки домашних задач**. Домашние задания нужно решать и сдавать в **Яндекс.Контесте**. Актуальный список задач, условия и требования к оформлению находятся в Контесте. **При расхождениях информация в Контесте имеет приоритет.** Ссылки на контесты публикуются на **вики курса**.

Каждое решение — один файл `.py` с указанным классом. Задачи независимы: импортировать решения других задач не нужно. Используйте только стандартную библиотеку; `input()` и `print()` не нужны.

Типы аргументов соответствуют аннотациям. Проверяйте только ошибки содержимого, прямо перечисленные в условии. Проверяется тип исключения, а не точный текст сообщения. Методы изменения состояния возвращают `None`, если в условии не указан другой результат.

У каждого экземпляра собственное состояние. Публичные свойства, объявленные только для чтения, не имеют setter: присваивание им снаружи приводит к `AttributeError`. Не требуется защищаться от намеренного изменения внутренних атрибутов с `_`.

## Easy 1. Часы

Реализуйте `Clock(hour, minute)` — часы с точностью до минуты.

```python
class Clock:
    def __init__(self, hour: int, minute: int) -> None:
        ...

    @property
    def hour(self) -> int:
        ...

    @property
    def minute(self) -> int:
        ...

    def advance(self, minutes: int) -> None:
        ...

    def format(self) -> str:
        ...
```

При создании час должен быть от 0 до 23, минута — от 0 до 59 включительно. Иначе поднимите `ValueError`. Свойства `hour` и `minute` доступны только для чтения.

`advance(minutes)` переводит часы вперёд на указанное неотрицательное целое число минут. После 23:59 снова наступает 00:00; полные прошедшие сутки в состоянии не хранятся. Отрицательный сдвиг — `ValueError` без изменения времени. Нулевой сдвиг разрешён.

`format()` возвращает строку `HH:MM` из пяти символов: для однозначных часов и минут нужен ведущий ноль.

Примеры:

```python
clock = Clock(23, 50)
other = Clock(8, 5)
assert clock.advance(20) is None
assert (clock.hour, clock.minute) == (0, 10)
assert clock.format() == "00:10"
assert other.format() == "08:05"
clock.advance(2 * 24 * 60 + 5)
assert clock.format() == "00:15"

try:
    clock.advance(-1)
except ValueError:
    pass
else:
    raise AssertionError("Отрицательный сдвиг должен быть отклонён")
assert clock.format() == "00:15"
```

Ограничения: аргументы — целые числа, по модулю до 10⁹; до 100 000 вызовов. Каждый метод и чтение свойства — `O(1)` времени и памяти; нельзя проходить циклом по каждой добавляемой минуте.

Критерии: границы времени проверены, переход через сутки корректен, экземпляры независимы, ошибочная операция не меняет состояние.

## Easy 2. Прямоугольник

Реализуйте `Rectangle(width, height)` со строго положительными целыми размерами.

```python
class Rectangle:
    def __init__(self, width: int, height: int) -> None:
        ...

    @property
    def width(self) -> int:
        ...

    @property
    def height(self) -> int:
        ...

    def area(self) -> int:
        ...

    def perimeter(self) -> int:
        ...

    def resize(self, width: int, height: int) -> None:
        ...
```

Свойства `width` и `height` доступны только для чтения. `area()` возвращает площадь, `perimeter()` — периметр.

Если при создании хотя бы один размер неположителен, поднимите `ValueError`. Метод `resize(width, height)` заменяет оба размера и возвращает `None`. Он должен проверить **оба новых размера до любого изменения состояния**: при неположительной ширине или высоте нужен `ValueError`, а прежние размеры сохраняются целиком.

Примеры:

```python
rectangle = Rectangle(3, 4)
other = Rectangle(1, 1)
assert rectangle.area() == 12
assert rectangle.perimeter() == 14
assert rectangle.resize(5, 2) is None
assert (rectangle.width, rectangle.height) == (5, 2)
assert rectangle.area() == 10
assert (other.width, other.height) == (1, 1)

for width, height in [(8, 0), (0, 8), (-1, 4), (4, -1)]:
    try:
        rectangle.resize(width, height)
    except ValueError:
        pass
    else:
        raise AssertionError("Оба размера должны быть положительными")
    assert (rectangle.width, rectangle.height) == (5, 2)
    assert rectangle.area() == 10

for width, height in [(0, 1), (1, 0), (-1, 2), (2, -1)]:
    try:
        Rectangle(width, height)
    except ValueError:
        pass
    else:
        raise AssertionError("Некорректные размеры нужно отклонить при создании")
```

Ограничения: аргументы — целые числа по модулю до 10⁶; до 100 000 изменений размера. Создание, методы и чтение свойств — `O(1)` времени и дополнительной памяти.

Критерии: площадь и периметр правильны, свойства не допускают публичного присваивания, экземпляры независимы, ошибка во втором аргументе `resize` не оставляет уже изменённую ширину.

## Easy 3. Набор результатов

Реализуйте `ScoreTable(scores)`, который хранит целые результаты от 0 до 100 включительно. Начальный список может быть пустым; повторные результаты разрешены.

```python
class ScoreTable:
    def __init__(self, scores: list[int]) -> None:
        ...

    @property
    def scores(self) -> list[int]:
        ...

    @property
    def count(self) -> int:
        ...

    def add(self, score: int) -> None:
        ...

    def best(self) -> int:
        ...
```

Свойства доступны только для чтения. `scores` каждый раз возвращает новый список в порядке добавления, `count` — текущее число результатов. Исходный список и выданные копии не должны позволять менять внутреннее состояние.

`add(score)` добавляет допустимый результат. Если в начальном списке или при добавлении встретилось значение вне диапазона, нужен `ValueError`. Неудачное добавление не меняет состояние. `best()` возвращает наибольший результат; для пустого набора — `ValueError`.

Примеры:

```python
source = [70, 0, 90]
table = ScoreTable(source)
source.append(100)
assert table.scores == [70, 0, 90]
copy = table.scores
copy[0] = 1
assert table.scores == [70, 0, 90]
assert table.add(100) is None
assert table.best() == 100
assert table.count == 4
assert ScoreTable([]).scores == []

try:
    table.add(-1)
except ValueError:
    pass
else:
    raise AssertionError("Результат вне диапазона")
assert table.scores == [70, 0, 90, 100]
```

Ограничения: до 100 000 начальных результатов и добавлений суммарно; значения на входе — целые по модулю до 10⁹. Создание — `O(n)`, `add` — амортизированная `O(1)`, `count` — `O(1)`, `scores` и `best` — не хуже `O(n)` по текущему числу результатов. Для хранения требуется `O(n)` памяти.

Критерии: весь начальный список проверен, копии независимы, нулевой результат допустим, отказ не портит накопленные данные.

## Medium 1. Редактор с отменой

Реализуйте `TextEditor(text="")`, хранящий текущий текст и историю его изменений.

```python
class TextEditor:
    def __init__(self, text: str = "") -> None:
        ...

    @property
    def text(self) -> str:
        ...

    @property
    def history_size(self) -> int:
        ...

    def append(self, suffix: str) -> None:
        ...

    def undo(self) -> str:
        ...
```

Свойства доступны только для чтения. В начале истории нет. Непустой `append(suffix)` дописывает суффикс к текущему тексту и сохраняет возможность отменить именно это изменение. Пустой суффикс ничего не меняет и не создаёт запись истории.

`undo()` отменяет последнее ещё не отменённое добавление и возвращает восстановленный текст. Если истории нет, поднимите `IndexError` без изменения текста. Начальный текст не является изменением, которое можно отменить. Новое добавление после `undo()` сохраняет возможность отменить это новое добавление; повторного применения отменённых изменений в задаче нет.

Примеры:

```python
editor = TextEditor("A")
other = TextEditor()
assert editor.append("B") is None
editor.append("C")
assert (editor.text, editor.history_size) == ("ABC", 2)
assert editor.undo() == "AB"
editor.append("!")
assert editor.text == "AB!"
assert editor.undo() == "AB"
assert editor.undo() == "A"
assert editor.history_size == 0
assert other.text == "" and other.history_size == 0
editor.append("")
assert editor.history_size == 0

try:
    editor.undo()
except IndexError:
    pass
else:
    raise AssertionError("Отменять уже нечего")
assert editor.text == "A"
```

Ограничения: до 2 000 операций; длина текущего текста после каждого успешного добавления не больше 10 000. Строки могут содержать любые символы. Разрешено хранить прежние версии текста целиком. Не требуется доказывать отсутствие повторов одинаковых строк во внутреннем хранилище.

Критерии: сохранён порядок отмены, пустое добавление не расходует историю, экземпляры независимы. `text` и `history_size` читаются за `O(1)`. Создание, `append` и `undo` — не хуже `O(L)` времени, где `L` — максимальная длина участвующей строки. Память — не более `O(qL)`, где `q` — число операций.

## Medium 2. Схема мест

Реализуйте `SeatMap(rows, seats_per_row)` для прямоугольной схемы мест. Ряды и места в ряду нумеруются с 1. Изначально все места свободны.

```python
class SeatMap:
    def __init__(self, rows: int, seats_per_row: int) -> None:
        ...

    @property
    def rows(self) -> int:
        ...

    @property
    def seats_per_row(self) -> int:
        ...

    @property
    def free_count(self) -> int:
        ...

    @property
    def bookings(self) -> list[tuple[int, int]]:
        ...

    def book(self, row: int, seat: int) -> None:
        ...

    def cancel(self, row: int, seat: int) -> None:
        ...
```

Все свойства доступны только для чтения. При создании оба размера должны быть положительными; иначе — `ValueError`.

- `book(row, seat)` занимает свободное существующее место. Несуществующее или уже занятое место — `ValueError`.
- `cancel(row, seat)` освобождает занятое существующее место. Для несуществующего места — `ValueError`, для существующего свободного — `KeyError`.
- Любой отказ не меняет набор бронирований и число свободных мест.
- `free_count` показывает число свободных мест.
- `bookings` возвращает новый список занятых мест, отсортированный сначала по ряду, затем по номеру места. Изменение этого списка не меняет схему.

Примеры:

```python
hall = SeatMap(2, 3)
other = SeatMap(2, 3)
assert hall.book(2, 1) is None
hall.book(1, 3)
assert hall.bookings == [(1, 3), (2, 1)]
assert hall.free_count == 4
view = hall.bookings
view.clear()
assert hall.bookings == [(1, 3), (2, 1)]
assert other.bookings == [] and other.free_count == 6

for row, seat in [(2, 1), (0, 1), (1, 4)]:
    try:
        hall.book(row, seat)
    except ValueError:
        pass
    else:
        raise AssertionError("Повторное или несуществующее место")
    assert hall.bookings == [(1, 3), (2, 1)]
    assert hall.free_count == 4

assert hall.cancel(2, 1) is None
assert hall.bookings == [(1, 3)]
try:
    hall.cancel(2, 1)
except KeyError:
    pass
else:
    raise AssertionError("Это место уже свободно")
assert hall.free_count == 5
```

Ограничения: размеры и координаты — целые числа; размеры по модулю до 1 000, координаты по модулю до 10⁹. До 100 000 операций; число занятых мест не превышает 100 000. Хранить запись о каждом свободном месте не требуется.

Критерии: проверяются обе координаты, ошибки не меняют состояние, все экземпляры и возвращаемые списки независимы. Создание — `O(1)` времени и памяти; `book`, `cancel` и чтение `free_count` — в среднем `O(1)`; получение `bookings` — `O(k log k)` времени и `O(k)` памяти по числу занятых мест. Для состояния требуется `O(k)` памяти.

## Формат сдачи

Сдавайте решения в **Яндекс.Контесте**. Формат отправляемого решения и состав обязательных задач определяются условиями актуального контеста. Ссылки на контесты публикуются на вики курса.
