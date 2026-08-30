# Занятие 12. Задачи для самостоятельного решения

Решения оформляются как функции с указанными сигнатурами. Сетевые запросы в тестах заменяются переданными coroutine-функциями: домашняя работа должна проверяться без интернета.

## Easy 1. URL с параметрами запроса

Реализуйте:

```python
from collections.abc import Sequence

def add_query_params(
    base_url: str,
    params: dict[str, str | int | Sequence[str | int] | None],
) -> str:
    ...
```

Добавьте параметры через `urllib.parse.urlencode(..., doseq=True)`. Значения `None` пропустите. Уже существующие параметры URL сохраните; параметры из `params` добавьте после них. Фрагмент `#...`, если он есть, должен остаться в конце.

Пример:

```python
url = add_query_params(
    "https://api.example.test/search?lang=ru#results",
    {"q": "курс Python", "page": 2, "tag": ["http", "async"], "empty": None},
)
assert url == (
    "https://api.example.test/search?lang=ru&q=%D0%BA%D1%83%D1%80%D1%81+Python"
    "&page=2&tag=http&tag=async#results"
)
```

Критерии проверки:

- URL разбирается и собирается функциями `urllib.parse`, а не конкатенацией строк;
- специальные символы корректно кодируются;
- последовательность превращается в повторяющиеся параметры;
- исходные аргументы не изменяются.

## Easy 2. Краткое описание репозитория из JSON

Ответ GitHub API уже преобразован из JSON в Python-объект. Реализуйте:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class RepoSummary:
    full_name: str
    stars: int
    language: str | None
    archived: bool

def parse_repo(payload: object) -> RepoSummary:
    ...
```

Ожидается словарь с полями `full_name`, `stargazers_count`, `language`, `archived`. Поднимите `ValueError`, если корень не является словарём, обязательного поля нет или его тип неверен. Учтите, что `bool` является подклассом `int`: звёзды `True` принимать нельзя. Неизвестные поля игнорируются.

Пример:

```python
payload = {
    "full_name": "python/cpython",
    "stargazers_count": 70_000,
    "language": "Python",
    "archived": False,
    "ignored": {"anything": True},
}
assert parse_repo(payload) == RepoSummary("python/cpython", 70_000, "Python", False)
```

Критерии проверки:

- проверены все четыре типа;
- `language` допускает только строку или `None`;
- сообщение `ValueError` называет проблемное поле;
- входной словарь не изменяется.

## Easy 3. Конкурентные задержанные значения

Реализуйте:

```python
import asyncio

async def delayed_values(items: list[tuple[str, float]]) -> list[str]:
    ...
```

Для каждой пары создайте coroutine, которая ждёт `delay` через `asyncio.sleep()` и возвращает `value`. Запустите все операции конкурентно через `asyncio.TaskGroup`. Результат должен сохранять порядок входа, а не порядок завершения.

Пример:

```python
assert asyncio.run(delayed_values([
    ("slow", 0.03),
    ("fast", 0.01),
])) == ["slow", "fast"]
```

Ограничения:

- `0 <= delay <= 0.1`;
- `time.sleep` запрещён;
- пустой список возвращает пустой список;
- функции `gather` и `as_completed` в этой задаче не используются.

Критерии проверки:

- задачи действительно перекрываются по времени;
- результаты читаются из объектов `Task` после выхода из `TaskGroup`;
- время определяется максимальной, а не суммарной задержкой с разумной погрешностью.

## Medium 1. Несколько запросов с общим тайм-аутом

Дана асинхронная зависимость:

```python
from collections.abc import Awaitable, Callable

Fetch = Callable[[str], Awaitable[dict]]
```

Реализуйте:

```python
async def fetch_all(
    urls: list[str],
    fetch: Fetch,
    timeout: float,
) -> list[dict]:
    ...
```

Все вызовы `fetch(url)` запускаются через один `TaskGroup`. Весь пакет, включая ожидание всех задач, ограничен одним `asyncio.timeout(timeout)`. Результаты сохраняют порядок URL. При ошибке одного запроса `TaskGroup` должен отменить остальные; исключение не превращается в значение результата.

Пример тестовой зависимости:

```python
async def fake_fetch(url: str) -> dict:
    await asyncio.sleep(0.01)
    return {"url": url}

assert asyncio.run(fetch_all(["a", "b"], fake_fetch, 0.1)) == [
    {"url": "a"}, {"url": "b"}
]
```

Критерии проверки:

- сеть и конкретная HTTP-библиотека не зашиты в функцию;
- `TaskGroup` и `asyncio.timeout` применены как контекстные менеджеры;
- тайм-аут всего пакета поднимает `TimeoutError`;
- пустой список обработан;
- фоновых задач после возврата или исключения не остаётся.

## Medium 2. Ограниченный конкурентный `map`

Реализуйте обобщённую функцию:

```python
from collections.abc import Awaitable, Callable, Iterable
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")

async def map_limited(
    worker: Callable[[T], Awaitable[R]],
    items: Iterable[T],
    limit: int,
) -> list[R]:
    ...
```

Все элементы запускаются в одном `TaskGroup`, но одновременно внутри `worker` находится не более `limit` задач. Используйте один `asyncio.Semaphore`. Результат сохраняет порядок входа; сам `items` может быть одноразовым генератором.

Ограничения:

- `limit <= 0` поднимает `ValueError` до запуска задач;
- материализовать `items` один раз разрешено;
- polling, `time.sleep` и ручное изменение внутреннего счётчика semaphore запрещены.

Критерии проверки:

- ограничение конкурентности выполняется даже при исключениях;
- semaphore используется через `async with`;
- ошибка worker отменяет соседние задачи через семантику `TaskGroup`;
- фоновых задач после завершения нет;
- порядок результата не зависит от порядка завершения.

## Hard 1. Первый успешный источник

Несколько независимых источников могут вернуть одинаковые данные. Реализуйте:

```python
from collections.abc import Awaitable, Callable, Sequence
from typing import TypeVar

T = TypeVar("T")

async def first_success(
    factories: Sequence[Callable[[], Awaitable[T]]],
    timeout: float,
) -> T:
    ...
```

Запустите все фабрики конкурентно. Верните первый **успешный** результат. Ошибка отдельного источника не должна останавливать остальные. Сразу после успеха отмените и дождитесь всех незавершённых задач. Если общий тайм-аут истёк, поднимите `TimeoutError`. Если все источники завершились ошибкой, поднимите `ExceptionGroup("all sources failed", errors)`.

Пустая последовательность поднимает `ValueError`.

Критерии проверки:

- coroutine создаётся вызовом каждой фабрики ровно один раз;
- задачи обрабатываются по фактическому завершению;
- после успеха, тайм-аута и всех ошибок каждая созданная задача завершена или отменена и дождана;
- `CancelledError` не проглатывается как обычная ошибка источника;
- очистка выполняется в `finally`;
- первый успешный результат возвращается независимо от порядка фабрик.

## Формат сдачи

Решения размещаются в модуле `homework12.py`, тесты — в `test_homework12.py`. Основные пять задач обязательны; Hard-задача необязательна. Тесты не должны обращаться во внешнюю сеть.
