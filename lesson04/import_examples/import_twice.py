"""Run with a fresh interpreter to observe the import cache."""

import sys

print("Первый import:")
import greetings

print("Повторный import:")
import greetings as another_name

print("from ... import ...:")
from greetings import greet

print(greet("Маша"))
print("Один модуль:", greetings is another_name)
print("Та же функция:", greet is greetings.greet)
print("Модуль в кеше:", sys.modules["greetings"] is greetings)
