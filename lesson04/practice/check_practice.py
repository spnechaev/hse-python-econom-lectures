"""Check the student's modules after task 6 has been completed."""

import contextlib
import importlib
import io
from pathlib import Path
import subprocess
import sys


def main() -> None:
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
        library = importlib.import_module("library_tools")
        report = importlib.import_module("show_report")
    assert captured.getvalue() == "", "Импорт модулей не должен ничего печатать"
    assert callable(report.main)

    assert library.return_day("2026-09-27") == "2026-10-11"
    assert library.return_day("2024-02-28", 2) == "2024-03-01"
    assert library.return_day("2026-12-31", 1) == "2027-01-01"
    assert library.return_day("2026-09-27", 0) == "2026-09-27"
    assert library.missing_items(["a", "b", "a"], ["a"]) == ["b", "a"]
    assert library.missing_items(["a"], ["a", "a"]) == []
    assert library.missing_items([], ["a"]) == []
    issued, returned = ["a", "b", "a"], ["b"]
    assert library.missing_items(issued, returned) == ["a", "a"]
    assert issued == ["a", "b", "a"] and returned == ["b"]

    script = Path(__file__).with_name("show_report.py")
    result = subprocess.run(
        [sys.executable, "-B", str(script)], check=True,
        capture_output=True, text=True, encoding="utf-8", timeout=10,
    )
    assert result.stderr == "", result.stderr
    assert result.stdout.splitlines() == ["2026-10-11", "['книга', 'кабель']"], result.stdout
    print("Проверки задания 6 пройдены.")


if __name__ == "__main__":
    main()
