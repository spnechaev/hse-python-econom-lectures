#!/usr/bin/env python3
"""Проверить структуру новых комплектов «лекция + семинар + задачи»."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LESSON_DIRECTORIES = sorted(ROOT.glob("lesson[0-9][0-9]"))
REQUIRED_FILES = {"README.md", "lecture.ipynb", "seminar.ipynb", "tasks.md"}
REQUIRED_SECTIONS = {"Цели", "Перед началом", "Самопроверка", "Итоги"}
REQUIRED_LECTURE_SECTIONS = {"Неожиданно, но по правилам"}
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
TASK_HEADING = re.compile(r"^##\s+(Easy|Medium|Hard)\s+\d+\.", re.MULTILINE)


def validate_notebook(path: Path, number: str, kind: str) -> list[str]:
    problems: list[str] = []
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"не удалось прочитать JSON: {error}"]

    if notebook.get("nbformat") != 4:
        problems.append("ожидается nbformat 4")
    cells = notebook.get("cells")
    if not isinstance(cells, list) or not cells:
        return problems + ["поле cells отсутствует или пусто"]

    russian_kind = "Лекция" if kind == "lecture" else "Семинар"
    expected_title = f"# {russian_kind} {number}."
    first_source = "".join(cells[0].get("source", []))
    if not first_source.startswith(expected_title):
        problems.append(f"первая ячейка должна начинаться с {expected_title!r}")

    kernelspec = notebook.get("metadata", {}).get("kernelspec", {})
    if kernelspec.get("name") != "python3":
        problems.append("не указан kernel python3")

    cell_ids: set[str] = set()
    markdown_parts: list[str] = []
    for index, cell in enumerate(cells):
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
        elif cell.get("cell_type") == "markdown":
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
    if kind == "lecture":
        missing_lecture_sections = REQUIRED_LECTURE_SECTIONS - sections
        if missing_lecture_sections:
            problems.append(
                "отсутствуют обязательные разделы лекции "
                f"{sorted(missing_lecture_sections)}"
            )
    if kind == "seminar" and "exercise" not in {
        tag
        for cell in cells
        for tag in cell.get("metadata", {}).get("tags", [])
    }:
        problems.append("в практическом семинаре нет ячеек exercise")

    return problems


def validate_tasks(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        return [f"не удалось прочитать файл: {error}"]

    counts = {"Easy": 0, "Medium": 0, "Hard": 0}
    for level in TASK_HEADING.findall(text):
        counts[level] += 1

    problems: list[str] = []
    if counts["Easy"] != 3:
        problems.append(f"ожидалось 3 задачи Easy, найдено {counts['Easy']}")
    if counts["Medium"] != 2:
        problems.append(f"ожидалось 2 задачи Medium, найдено {counts['Medium']}")
    if counts["Hard"] > 1:
        problems.append(f"допускается не более 1 задачи Hard, найдено {counts['Hard']}")
    return problems


def main() -> int:
    if not LESSON_DIRECTORIES:
        print("Каталоги lesson?? не найдены", file=sys.stderr)
        return 1

    failed = False
    for directory in LESSON_DIRECTORIES:
        number = directory.name.removeprefix("lesson")
        missing = sorted(
            filename for filename in REQUIRED_FILES if not (directory / filename).is_file()
        )
        if missing:
            failed = True
            print(f"{directory.name}: отсутствуют файлы {', '.join(missing)}")
            continue

        for kind in ("lecture", "seminar"):
            path = directory / f"{kind}.ipynb"
            for problem in validate_notebook(path, number, kind):
                failed = True
                print(f"{path.relative_to(ROOT)}: {problem}")

        tasks_path = directory / "tasks.md"
        for problem in validate_tasks(tasks_path):
            failed = True
            print(f"{tasks_path.relative_to(ROOT)}: {problem}")

    if failed:
        return 1

    print(f"Проверено комплектов занятий: {len(LESSON_DIRECTORIES)}. Ошибок не найдено.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
