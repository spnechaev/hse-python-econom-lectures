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
        tools = importlib.import_module("report_tools")
        report = importlib.import_module("show_report")
    assert captured.getvalue() == "", "Импорт модулей не должен ничего печатать"
    assert callable(report.main)

    assert tools.report_due("2026-02-10") == "2026-03-31"
    assert tools.report_due("2024-01-15") == "2024-02-29"
    assert tools.report_due("2025-01-31") == "2025-02-28"
    assert tools.report_due("2026-12-05") == "2027-01-31"
    assert tools.missing_items(["a", "b", "a"], ["a"]) == ["b", "a"]
    assert tools.missing_items(["a"], ["a", "a"]) == []
    assert tools.missing_items([], ["a"]) == []
    issued, returned = ["a", "b", "a"], ["b"]
    assert tools.missing_items(issued, returned) == ["a", "a"]
    assert issued == ["a", "b", "a"] and returned == ["b"]

    script = Path(__file__).with_name("show_report.py")
    result = subprocess.run(
        [sys.executable, "-B", str(script)], check=True,
        capture_output=True, text=True, encoding="utf-8", timeout=10,
    )
    assert result.stderr == "", result.stderr
    assert result.stdout.splitlines() == ["2026-03-31", "['книга', 'кабель']"], result.stdout
    print("Проверки задания 6 пройдены.")


if __name__ == "__main__":
    main()
