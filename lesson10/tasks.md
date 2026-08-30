# Занятие 10. Задачи для самостоятельного решения

Решения оформляются в модуле с указанными классами и функциями. `input` и `print` в предметной логике не используются.

## Easy 1. Транзакция как `dataclass`

Создайте неизменяемую запись:

```python
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    category: str
    amount: Decimal
```

В `__post_init__` проверьте, что идентификатор и категория не пусты после `strip()`, а сумма строго положительна. Некорректные данные приводят к `ValueError`.

Пример:

```python
transaction = Transaction("t-1", "food", Decimal("120.50"))
assert transaction.amount == Decimal("120.50")
assert transaction == Transaction("t-1", "food", Decimal("120.50"))
```

Ограничения:

- `float` для суммы не используется;
- поля после создания нельзя переназначить;
- проверка находится внутри класса.

Критерии проверки:

- корректные `__init__`, `__repr__` и `__eq__` создаются `dataclass`;
- каждый инвариант проверен отдельно;
- исходные значения не исправляются молча.

## Easy 2. Счёт с инвариантом

Реализуйте класс:

```python
from decimal import Decimal

class Account:
    def __init__(self, account_id: str, balance: Decimal = Decimal("0")):
        ...

    @property
    def balance(self) -> Decimal:
        ...

    def deposit(self, amount: Decimal) -> None:
        ...

    def withdraw(self, amount: Decimal) -> None:
        ...
```

Сумма операции должна быть положительной. Списание не может сделать баланс отрицательным. Поле `_balance` не изменяется снаружи через публичный setter.

Пример:

```python
account = Account("a-1", Decimal("100"))
account.deposit(Decimal("25"))
account.withdraw(Decimal("40"))
assert account.balance == Decimal("85")
```

Критерии проверки:

- инвариант проверяется до изменения состояния;
- при ошибке баланс остаётся прежним;
- методы ничего не печатают и возвращают `None`.

## Easy 3. Декоратор подсчёта вызовов

Реализуйте декоратор:

```python
def count_calls(func):
    ...
```

Обёрнутая функция должна работать с любыми позиционными и именованными аргументами. Число вызовов хранится в атрибуте `calls` обёртки. Используйте `functools.wraps`.

Пример:

```python
@count_calls
def net_amount(amount: int, fee: int = 0) -> int:
    """Return amount after fee."""
    return amount - fee

assert net_amount(100, fee=7) == 93
assert net_amount(50) == 50
assert net_amount.calls == 2
assert net_amount.__name__ == "net_amount"
assert net_amount.__doc__ == "Return amount after fee."
```

Критерии проверки:

- счётчик увеличивается перед каждым вызовом;
- результат и исключения исходной функции не подменяются;
- метаданные сохраняются через `wraps`.

## Medium 1. Отчёт через композицию

Используйте `Transaction` из Easy 1. Реализуйте:

```python
class BudgetReport:
    def __init__(self, transactions: list[Transaction]):
        ...

    def total(self) -> Decimal:
        ...

    def total_by_category(self) -> dict[str, Decimal]:
        ...

    def with_transaction(self, transaction: Transaction) -> "BudgetReport":
        ...
```

`with_transaction` возвращает новый отчёт и не меняет старый. Список, переданный в конструктор, не должен позволять позже изменить внутреннее состояние отчёта.

Пример:

```python
source = [Transaction("t-1", "food", Decimal("100"))]
report = BudgetReport(source)
source.append(Transaction("t-2", "taxi", Decimal("50")))
assert report.total() == Decimal("100")

extended = report.with_transaction(
    Transaction("t-3", "food", Decimal("25"))
)
assert report.total() == Decimal("100")
assert extended.total_by_category()["food"] == Decimal("125")
```

Критерии проверки:

- класс композирует записи, а не наследуется от `list`;
- входной контейнер защитно копируется или преобразуется в кортеж;
- методы не раскрывают изменяемую внутреннюю коллекцию;
- суммирование начинается с `Decimal("0")`.

## Medium 2. Сервис и структурный интерфейс

Опишите источник транзакций протоколом и реализуйте сервис:

```python
from collections.abc import Iterable
from typing import Protocol

class TransactionSource(Protocol):
    def load(self) -> Iterable[Transaction]:
        ...

class ReportService:
    def __init__(self, source: TransactionSource):
        ...

    def build(self) -> BudgetReport:
        ...
```

Создайте две реализации источника:

- `MemoryTransactionSource`, принимающий готовые записи;
- `CsvTransactionSource`, принимающий `Iterable[str]` формата `id;category;amount`.

Обе реализации должны подходить сервису без наследования от `TransactionSource`.

Пример:

```python
source = MemoryTransactionSource([
    Transaction("t-1", "food", Decimal("100")),
])
service = ReportService(source)
assert service.build().total() == Decimal("100")
```

Ограничения:

- сервис не проверяет конкретный класс источника;
- разбор CSV находится в `CsvTransactionSource`;
- источник передаётся в конструктор, а не создаётся внутри `build`;
- ошибки разбора содержат номер строки.

Критерии проверки:

- протокол содержит только реально нужный метод;
- сервис зависит от интерфейса `load()`;
- тест сервиса использует память и не обращается к файлам;
- новая реализация источника не требует изменения сервиса.

## Формат сдачи

Решения размещаются в модуле `homework10.py`. Рядом необходимо добавить `test_homework10.py` с тестами обычных сценариев и ошибок. Hard-задачи нет.
