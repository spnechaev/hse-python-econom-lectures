"""Управление отдельным процессом для долгого опыта из лекции 3.

В ноутбуке используются start_comparison, show_comparison и stop_comparison.
Повторный запуск не создаёт второй процесс, пока первый ещё работает.
Результат хранится во временном файле; файлы курса процесс не изменяет.

https://docs.python.org/3.14/library/subprocess.html#subprocess.Popen
"""

from __future__ import annotations

import argparse
import atexit
from dataclasses import dataclass
from itertools import permutations
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
from time import perf_counter
from typing import TextIO


@dataclass
class _Job:
    process: subprocess.Popen
    output: TextIO
    size: int
    started: float
    stopped: bool = False
    result: dict | None = None


_job: _Job | None = None


def comparison_status() -> dict:
    """Получить состояние, не дожидаясь окончания вычислений."""
    if _job is None:
        return {"state": "not_started"}
    job = _job
    if job.result is not None:
        return dict(job.result)

    result = {
        "state": "running",
        "size": job.size,
        "pid": job.process.pid,
        "elapsed": perf_counter() - job.started,
    }
    returncode = job.process.poll()
    if returncode is None:
        return result

    try:
        job.output.seek(0)
        output = job.output.read()
        if job.stopped:
            result["state"] = "stopped"
        elif returncode != 0:
            result.update(state="failed", error=output.strip(), returncode=returncode)
        else:
            try:
                payload = json.loads(output)
                if not isinstance(payload, dict) or not {"equal", "checked", "elapsed"} <= payload.keys():
                    raise ValueError("неполный результат")
                result.update(payload, state="done")
            except (ValueError, TypeError) as error:
                result.update(state="failed", error=f"Не удалось прочитать результат: {error}")
    finally:
        job.output.close()
        if job.process.stdin is not None:
            job.process.stdin.close()
    job.result = result
    return dict(result)


def show_comparison() -> None:
    """Напечатать текущее состояние или готовый результат."""
    result = comparison_status()
    state = result["state"]
    if state == "not_started":
        print("Долгий опыт ещё не запущен.")
    elif state == "running":
        print(f"Перебор {result['size']} элементов продолжается: прошло {result['elapsed']:.1f} с.")
        print("Остальные ячейки можно выполнять. Для остановки: stop_comparison().")
    elif state == "done":
        print(f"Совпадают без учёта порядка: {result['equal']}")
        print(f"Проверено перестановок: {result['checked']:,}")
        print(f"Время перебора: {result['elapsed']:.6f} с")
    elif state == "stopped":
        print(f"Опыт остановлен через {result['elapsed']:.1f} с.")
    else:
        print("Процесс завершился с ошибкой:")
        print(result.get("error") or f"Код завершения: {result.get('returncode')}")


def start_comparison(size: int = 14) -> None:
    """Запустить опыт; при повторном вызове показать уже работающий процесс."""
    global _job
    if type(size) is not int or not 0 <= size <= 14:
        raise ValueError("Для этого опыта size должен быть целым числом от 0 до 14.")
    if comparison_status()["state"] == "running":
        show_comparison()
        return

    output = tempfile.TemporaryFile(mode="w+", encoding="utf-8")
    started = perf_counter()
    try:
        process = subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "--worker", str(size)],
            stdin=subprocess.PIPE,
            stdout=output,
            stderr=subprocess.STDOUT,
        )
    except BaseException:
        output.close()
        raise
    _job = _Job(process, output, size, started)
    print(f"Запущен отдельный процесс: {size} элементов, PID {process.pid}.")
    print("Продолжайте лекцию. Проверить состояние: show_comparison().")


def _stop_current() -> None:
    if _job is None or _job.result is not None:
        return
    if _job.process.poll() is None:
        _job.stopped = True
        _job.process.terminate()
        try:
            _job.process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            _job.process.kill()
            _job.process.wait()
    comparison_status()


def stop_comparison() -> None:
    """Остановить свой процесс и освободить временный файл."""
    _stop_current()
    show_comparison()


def _watch_parent() -> None:
    # Parent holds the write end of stdin. Kernel exit/restart closes it,
    # including abrupt exits for which atexit handlers cannot run.
    # Use the raw descriptor: a daemon must not hold a buffered stdin lock
    # while the worker's main thread finishes and Python shuts down.
    while os.read(sys.stdin.fileno(), 1024):
        pass
    os._exit(0)


def _run_worker(size: int) -> None:
    threading.Thread(target=_watch_parent, daemon=True).start()
    second = list(range(size))
    target = tuple(second[::-1])
    checked = 0
    equal = False
    started = perf_counter()
    for candidate in permutations(second):
        checked += 1
        if candidate == target:
            equal = True
            break
    print(json.dumps({"equal": equal, "checked": checked, "elapsed": perf_counter() - started}), flush=True)


atexit.register(_stop_current)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", type=int, choices=range(15), required=True)
    args = parser.parse_args()
    _run_worker(args.worker)
