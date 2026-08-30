# Занятие 13. Задачи для самостоятельного решения

Все функции получают открытое соединение `sqlite3.Connection`. Тесты создают отдельную базу `:memory:` и включают внешние ключи до начала транзакции. SQL-запросы должны быть параметризованы; конкатенация пользовательских значений с SQL запрещена.

## Easy 1. Схема клиентов и заказов

Реализуйте:

```python
import sqlite3

def create_schema(connection: sqlite3.Connection) -> None:
    ...
```

Создайте три таблицы:

```text
customers
  id             INTEGER PRIMARY KEY
  email          TEXT NOT NULL UNIQUE
  name           TEXT NOT NULL, непустое после trim

orders
  id             INTEGER PRIMARY KEY
  customer_id    INTEGER NOT NULL -> customers(id)
  amount_cents   INTEGER NOT NULL, неотрицательное
  status         TEXT NOT NULL, одно из new/paid/cancelled

order_status_history
  id             INTEGER PRIMARY KEY
  order_id       INTEGER NOT NULL -> orders(id)
  old_status     TEXT NOT NULL
  new_status     TEXT NOT NULL
```

При удалении клиента его заказы должны удаляться каскадно; при удалении заказа каскадно удаляется история. Функция должна безопасно вызываться повторно через `CREATE TABLE IF NOT EXISTS`. Зафиксируйте DDL одной транзакцией.

Критерии проверки:

- ограничения находятся в схеме, а не только в Python;
- оба внешних ключа и обе каскадные связи заданы;
- некорректная сумма, пустое имя, неизвестный статус и дублирующийся email отклоняются SQLite;
- повторный вызов не удаляет существующие данные;
- при ошибке создания схема не остаётся частично созданной.

## Easy 2. Создание клиента

Реализуйте:

```python
def create_customer(
    connection: sqlite3.Connection,
    email: str,
    name: str,
) -> int:
    ...
```

Добавьте клиента параметризованным `INSERT`, подтвердите транзакцию и верните `id` новой строки. Пробелы по краям email и имени удалите до запроса. Пустые значения поднимут `ValueError`. Дублирующийся email преобразуйте из `sqlite3.IntegrityError` в `ValueError("email already exists")`, сохранив исходное исключение через `raise ... from ...`.

Пример:

```python
customer_id = create_customer(connection, " anna@example.test ", " Анна ")
row = connection.execute(
    "SELECT email, name FROM customers WHERE id = ?",
    (customer_id,),
).fetchone()
assert tuple(row) == ("anna@example.test", "Анна")
```

Критерии проверки:

- значения не подставляются через f-string;
- используется идентификатор реально вставленной строки;
- успешная операция зафиксирована;
- при конфликте транзакция откатывается;
- остальные ошибки SQLite не маскируются как конфликт email.

## Easy 3. Заказы клиента

Реализуйте:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class OrderInfo:
    order_id: int
    customer_email: str
    amount_cents: int
    status: str

def orders_for_customer(
    connection: sqlite3.Connection,
    email: str,
) -> list[OrderInfo]:
    ...
```

Одним запросом соедините `customers` и `orders`. Верните заказы клиента по убыванию суммы, а при равенстве — по возрастанию `orders.id`. Не выполняйте отдельный запрос для каждого заказа.

Пример результата:

```python
assert orders_for_customer(connection, "anna@example.test") == [
    OrderInfo(2, "anna@example.test", 2500, "paid"),
    OrderInfo(1, "anna@example.test", 900, "new"),
]
```

Критерии проверки:

- используются `JOIN`, `WHERE` и явный `ORDER BY`;
- email передаётся параметром;
- неизвестный клиент и клиент без заказов дают пустой список;
- выполняется ровно один `SELECT`.

## Medium 1. Статистика по всем клиентам

Реализуйте:

```python
@dataclass(frozen=True)
class CustomerStats:
    email: str
    orders_count: int
    paid_total_cents: int

def customer_statistics(
    connection: sqlite3.Connection,
    min_orders: int = 0,
) -> list[CustomerStats]:
    ...
```

Верните всех клиентов, у которых число заказов не меньше `min_orders`, включая клиентов без заказов при `min_orders=0`. `paid_total_cents` учитывает только заказы со статусом `paid`. Результат отсортируйте по убыванию оплаченной суммы, затем по email.

Ограничения:

- `min_orders < 0` поднимает `ValueError` до запроса;
- задача решается одним SQL-запросом;
- коррелированные запросы по одному на клиента запрещены.

Критерии проверки:

- используется `LEFT JOIN`, чтобы не потерять клиентов без заказов;
- число заказов считается через `COUNT(orders.id)`, а не `COUNT(*)`;
- условная сумма учитывает только `paid` и превращает отсутствие результата в ноль;
- фильтр агрегата находится в `HAVING`;
- сортировка полностью задана в SQL.

## Medium 2. Атомарная смена статуса

Реализуйте:

```python
def change_order_status(
    connection: sqlite3.Connection,
    order_id: int,
    new_status: str,
) -> bool:
    ...
```

Допустимые переходы:

```text
new -> paid
new -> cancelled
paid -> cancelled
```

Если заказа нет, верните `False` без записи истории. Если статус уже равен новому или переход запрещён, поднимите `ValueError`. При успешном переходе одной транзакцией:

1. обновите `orders.status`;
2. добавьте строку в `order_status_history` со старым и новым статусом;
3. подтвердите оба изменения вместе.

Критерии проверки:

- текущий статус читается внутри той же транзакции;
- `UPDATE` и `INSERT` параметризованы;
- при ошибке записи истории изменение заказа откатывается;
- успешная операция оставляет ровно одну строку истории;
- запрещённый переход не меняет ни одну таблицу;
- функция не скрывает неожиданную ошибку базы.

## Формат сдачи

Решения размещаются в модуле `homework13.py`, тесты — в `test_homework13.py`. Обязательны все пять задач. Для каждого теста создавайте новую базу `:memory:`; порядок тестов не должен иметь значения.
