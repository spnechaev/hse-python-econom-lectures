# Занятие 11. Задачи для самостоятельного решения

Решения оформляются как функции и классы с указанными сигнатурами. `input` и `print` не используются.

## Easy 1. Сумма по дереву категорий

Дана иерархия категорий:

```python
from dataclasses import dataclass, field

@dataclass
class Category:
    name: str
    amount: int = 0
    children: list["Category"] = field(default_factory=list)
```

Реализуйте:

```python
def total_amount(root: Category) -> int:
    ...
```

Сумма узла входит в итог вместе с суммами всех потомков.

Пример:

```python
root = Category("all", children=[
    Category("food", 1200, [Category("cafes", 400)]),
    Category("transport", 700),
])
assert total_amount(root) == 2300
```

Критерии проверки:

- лист является базовым случаем без специального имени;
- каждое поддерево обрабатывается ровно один раз;
- время `O(N)`, стек вызовов `O(H)`, где `H` — высота.

## Easy 2. Путь до категории

Реализуйте DFS-поиск первого узла с заданным именем:

```python
def find_category_path(root: Category, target: str) -> list[str] | None:
    ...
```

Верните имена от корня до найденного узла включительно. Если узла нет, верните `None`.

Пример:

```python
assert find_category_path(root, "cafes") == ["all", "food", "cafes"]
assert find_category_path(root, "rent") is None
```

Ограничения:

- порядок детей определяет порядок DFS;
- вход гарантированно является деревом без циклов;
- глобальные переменные не используются.

Критерии проверки:

- путь строится только для успешной ветви;
- найденный результат немедленно передаётся вверх;
- время `O(N)`, память `O(H)` без учёта результата.

## Easy 3. Стабильная очередь заявок с приоритетом

Заявка содержит `id` и целый `priority`: большее число означает более высокий приоритет. При равенстве раньше обслуживается заявка, которая раньше встретилась во входе.

```python
def priority_order(requests: list[dict]) -> list[str]:
    ...
```

Используйте появившиеся в Python 3.14 функции `heapq.heappush_max` и `heapq.heappop_max`. Храните записи `(priority, -order, request_id)`: максимальный приоритет извлекается первым, а среди равных приоритетов большее значение `-order` соответствует более ранней заявке.

До Python 3.14 ту же задачу обычно решали через min-heap и отрицательный приоритет: `(-priority, order, request_id)`. В решении этой задачи нужен новый max-heap API.

Пример:

```python
requests = [
    {"id": "r-1", "priority": 2},
    {"id": "r-2", "priority": 5},
    {"id": "r-3", "priority": 5},
]
assert priority_order(requests) == ["r-2", "r-3", "r-1"]
```

Критерии проверки:

- исходные словари не изменяются;
- счётчик устраняет сравнение самих заявок;
- порядок равных приоритетов стабилен;
- время `O(N log N)`, память `O(N)`.

## Medium 1. Бинарное дерево поиска

Реализуйте узел и три операции:

```python
from dataclasses import dataclass

@dataclass
class SearchNode:
    key: int
    value: str
    left: "SearchNode | None" = None
    right: "SearchNode | None" = None

def bst_insert(
    root: SearchNode | None,
    key: int,
    value: str,
) -> SearchNode:
    ...

def bst_find(root: SearchNode | None, key: int) -> str | None:
    ...

def bst_items(root: SearchNode | None) -> list[tuple[int, str]]:
    ...
```

Меньшие ключи хранятся слева, большие — справа. Повторный ключ заменяет значение. `bst_items` выполняет inorder-обход и возвращает пары по возрастанию ключа.

Пример:

```python
root = None
for key, value in [(30, "c"), (10, "a"), (20, "b"), (40, "d")]:
    root = bst_insert(root, key, value)
assert bst_find(root, 20) == "b"
assert bst_items(root) == [(10, "a"), (20, "b"), (30, "c"), (40, "d")]
```

Критерии проверки:

- инвариант BST сохраняется после каждой вставки;
- пустое дерево обработано;
- inorder даёт отсортированные ключи;
- время операции `O(H)`, не заявляется безусловное `O(log N)`.

## Medium 2. Крупнейшие транзакции без полной сортировки

Транзакция содержит уникальный `id` и целую `amount`. Реализуйте:

```python
def top_transactions(transactions: list[dict], k: int) -> list[str]:
    ...
```

Верните идентификаторы `k` крупнейших транзакций по убыванию суммы. При равенстве раньше идёт запись, раньше встретившаяся во входе. Поддерживайте min-heap не более чем из `k` записей; полная сортировка всего входа запрещена.

Пример:

```python
transactions = [
    {"id": "t-1", "amount": 500},
    {"id": "t-2", "amount": 1200},
    {"id": "t-3", "amount": 1200},
    {"id": "t-4", "amount": 700},
]
assert top_transactions(transactions, 2) == ["t-2", "t-3"]
```

Ограничения:

- `0 <= k <= len(transactions) <= 1_000_000`;
- размер кучи не превосходит `k`;
- исходный список не изменяется.

Критерии проверки:

- ключ качества учитывает сумму и исходный порядок;
- время `O(N log k)`, память `O(k)` без результата;
- `k=0`, равные суммы и `k=N` обработаны явно.

## Hard 1. Планировщик с обновлением и отменой

Реализуйте класс:

```python
class TaskScheduler:
    def add(self, task_id: str, priority: int) -> None:
        ...

    def cancel(self, task_id: str) -> bool:
        ...

    def pop(self) -> str:
        ...

    def __len__(self) -> int:
        ...
```

Большее значение `priority` обслуживается раньше. При равенстве сохраняется порядок последнего добавления или обновления. Повторный `add` обновляет приоритет существующей задачи.

Используйте:

- max-heap записей `[priority, -order, task_id]` через API Python 3.14;
- словарь `task_id -> актуальная запись`;
- уникальный маркер удалённой задачи;
- ленивое удаление: старая запись помечается, а физически пропускается при `pop`.

Пример:

```python
scheduler = TaskScheduler()
scheduler.add("a", 2)
scheduler.add("b", 5)
scheduler.add("c", 5)
scheduler.add("a", 10)
assert scheduler.cancel("c") is True
assert scheduler.cancel("missing") is False
assert scheduler.pop() == "a"
assert scheduler.pop() == "b"
```

Пустой `pop` поднимает `KeyError`.

Критерии проверки:

- в словаре находится только актуальная запись каждой живой задачи;
- обновление не ломает инвариант кучи;
- отменённые и устаревшие записи никогда не возвращаются;
- `len` считает живые задачи, а не физические записи heap;
- `add` и `pop` имеют амортизированное `O(log N)`, `cancel` — ожидаемое `O(1)` плюс будущая очистка.

## Формат сдачи

Решения размещаются в модуле `homework11.py`. Рядом можно добавить `test_homework11.py`. Основные пять задач обязательны; Hard-задача необязательна.
