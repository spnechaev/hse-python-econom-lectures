#!/usr/bin/env python3
"""Проверить базовую гигиену учебных ноутбуков."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted(ROOT.glob("seminar??/*.ipynb"))
EXPECTED_DIRECTORIES = {f"seminar{number:02d}" for number in range(1, 12)}
ALLOWED_TAGS = {
    "blocking-demo",
    "demo",
    "depends-on-previous-cell",
    "exercise",
    "jupyter-only",
    "naive-solution",
    "network",
    "requires-nb-mypy",
    "slow",
    "solution",
}
CELL_ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
SECTION = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
TASK_SECTION = re.compile(
    r"^(?:задани[ея]|задача|бонус(?:ное)? задание)\b", re.IGNORECASE
)
REQUIRED_SECTIONS = {"Цели", "Перед началом", "Самопроверка", "Итоги"}
DEADLINE = re.compile(
    r"(?:дедлайн|deadline|без штрафа|со штрафом|не принимается|"
    r"\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b|"
    r"\b\d{1,2}[/\-]\d{1,2}\b|"
    r"\b\d{1,2}\s+(?:сентября|октября)\b)",
    re.IGNORECASE,
)


def validate(path: Path) -> list[str]:
    problems: list[str] = []
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"не удалось прочитать JSON: {error}"]

    if notebook.get("nbformat") != 4:
        problems.append("ожидается nbformat 4")
    if not isinstance(notebook.get("cells"), list):
        return problems + ["поле cells отсутствует или имеет неверный тип"]

    number = path.parent.name.removeprefix("seminar")
    expected_title = f"# Семинар {number}."
    first_source = "".join(notebook["cells"][0].get("source", [])) if notebook["cells"] else ""
    if not first_source.startswith(expected_title):
        problems.append(f"первая ячейка должна начинаться с {expected_title!r}")

    kernelspec = notebook.get("metadata", {}).get("kernelspec", {})
    if kernelspec.get("name") != "python3":
        problems.append("не указан kernel python3")

    cell_ids: set[str] = set()
    markdown_parts: list[str] = []
    for index, cell in enumerate(notebook["cells"]):
        cell_id = cell.get("id")
        if not isinstance(cell_id, str) or not CELL_ID.fullmatch(cell_id):
            problems.append(f"ячейка {index}: некорректный id")
        elif cell_id in cell_ids:
            problems.append(f"ячейка {index}: повторяющийся id {cell_id!r}")
        else:
            cell_ids.add(cell_id)

        source = "".join(cell.get("source", []))
        if cell.get("cell_type") == "code":
            tags = cell.get("metadata", {}).get("tags", [])
            if not tags:
                problems.append(f"ячейка {index}: не указан тип кодовой ячейки")
            unknown_tags = set(tags) - ALLOWED_TAGS
            if unknown_tags:
                problems.append(
                    f"ячейка {index}: неизвестные теги {sorted(unknown_tags)}"
                )
            if cell.get("execution_count") is not None:
                problems.append(f"ячейка {index}: не сброшен execution_count")
            if cell.get("outputs"):
                problems.append(f"ячейка {index}: сохранён output")
        if cell.get("cell_type") == "markdown":
            markdown_parts.append(source)
            if source.count("```") % 2:
                problems.append(f"ячейка {index}: незакрытый блок кода Markdown")

    markdown = "\n".join(markdown_parts)
    sections = set(SECTION.findall(markdown))
    missing_sections = REQUIRED_SECTIONS - sections
    if missing_sections:
        problems.append(
            f"отсутствуют обязательные разделы {sorted(missing_sections)}"
        )
    if DEADLINE.search(markdown):
        problems.append("найден календарный дедлайн")

    task_sections = {
        section for section in sections if TASK_SECTION.search(section)
    }
    seminar_number = int(number)
    if seminar_number <= 8 and not task_sections:
        problems.append("не найдено ни одного задания")
    if seminar_number >= 9 and task_sections:
        problems.append(
            f"в справочном семинаре найдены задания {sorted(task_sections)}"
        )

    return problems


def main() -> int:
    if not NOTEBOOKS:
        print("Ноутбуки не найдены", file=sys.stderr)
        return 1

    failed = False
    if len(NOTEBOOKS) != len(EXPECTED_DIRECTORIES):
        failed = True
        print(
            f"Ожидалось ноутбуков: {len(EXPECTED_DIRECTORIES)}, "
            f"найдено: {len(NOTEBOOKS)}"
        )

    actual_directories = {path.parent.name for path in NOTEBOOKS}
    if actual_directories != EXPECTED_DIRECTORIES:
        failed = True
        missing = sorted(EXPECTED_DIRECTORIES - actual_directories)
        unexpected = sorted(actual_directories - EXPECTED_DIRECTORIES)
        if missing:
            print(f"Отсутствуют каталоги: {', '.join(missing)}")
        if unexpected:
            print(f"Неожиданные каталоги: {', '.join(unexpected)}")

    for path in NOTEBOOKS:
        problems = validate(path)
        if problems:
            failed = True
            for problem in problems:
                print(f"{path.relative_to(ROOT)}: {problem}")

    if failed:
        return 1

    print(f"Проверено ноутбуков: {len(NOTEBOOKS)}. Ошибок не найдено.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
