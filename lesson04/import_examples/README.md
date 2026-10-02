# Опыты с import

Нужен только Python 3.14. Из корня курса:

```bash
python lesson04/import_examples/reuse_function.py
python lesson04/import_examples/import_twice.py
python lesson04/import_examples/package_demo.py
python lesson04/import_examples/import_bindings.py
python lesson04/import_examples/greetings.py
```

- `reuse_function.py`: функция обработки пробелов определена в `text_tools.py` и используется из другого файла через `from text_tools import normalize_spaces`.
- `import_twice.py`: тело `greetings.py` выполняется при первой загрузке; повторный импорт использует тот же модуль. `from` даёт ещё одно имя той же функции.
- `package_demo.py`: импорт `urllib` сам по себе не загружает `urllib.parse`; явный импорт подмодуля загружает его и связывает с пакетом.
- `import_bindings.py`: переназначение `settings.limit` не меняет ранее импортированное имя `limit`, а изменение общего списка видно через обе ссылки.
- Прямой запуск `greetings.py` выполняет также блок `if __name__ == "__main__"`.

Каждая команда запускает отдельный интерпретатор. Поэтому кеш импортов ноутбука не влияет на результат. В [лекции](../lecture.ipynb) сначала разобран пример с функцией из соседнего файла; последующие опыты запускаются из ячеек и показывают загрузку модулей и связывание имён.
