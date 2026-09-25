"""Проверки фонового опыта без выполнения перебора 14!."""

import contextlib
import io
from pathlib import Path
import subprocess
import sys
import time
import unittest
from unittest.mock import patch

import permutation_background as background


class BackgroundComparisonTests(unittest.TestCase):
    def setUp(self):
        background._stop_current()
        background._job = None
        self.output = contextlib.redirect_stdout(io.StringIO())
        self.output.__enter__()

    def tearDown(self):
        background._stop_current()
        self.output.__exit__(None, None, None)

    def wait_for_result(self):
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            result = background.comparison_status()
            if result["state"] != "running":
                return result
            time.sleep(0.01)
        self.fail("Small comparison did not finish")

    def test_completed_result_is_repeatable_and_closes_handles(self):
        background.start_comparison(4)
        result = self.wait_for_result()
        self.assertEqual(result["state"], "done", result)
        self.assertIs(result["equal"], True)
        self.assertEqual(result["checked"], 24)
        self.assertEqual(background.comparison_status(), result)
        self.assertTrue(background._job.output.closed)
        self.assertTrue(background._job.process.stdin.closed)

    def test_long_comparison_is_nonblocking_reused_and_stoppable(self):
        background.start_comparison(14)
        process = background._job.process
        self.assertEqual(background.comparison_status()["state"], "running")
        # Ordinary notebook computation continues while the worker is alive.
        self.assertEqual(sum(range(1000)), 499500)
        background.start_comparison(14)
        self.assertIs(background._job.process, process)
        background.stop_comparison()
        self.assertIsNotNone(process.poll())
        self.assertEqual(background.comparison_status()["state"], "stopped")
        self.assertTrue(background._job.output.closed)
        background.stop_comparison()

    def test_stop_before_start_and_restart_after_stop(self):
        background.stop_comparison()
        self.assertEqual(background.comparison_status()["state"], "not_started")
        background.start_comparison(14)
        background.stop_comparison()
        background.start_comparison(0)
        result = self.wait_for_result()
        self.assertEqual((result["state"], result["checked"]), ("done", 1))

    def test_invalid_size_does_not_create_process(self):
        for value in [-1, 15, 1.5, True]:
            with self.assertRaises(ValueError):
                background.start_comparison(value)
        self.assertIsNone(background._job)

    def test_process_failure_is_reported_and_file_is_closed(self):
        real_popen = subprocess.Popen
        def fail_instead(command, **kwargs):
            return real_popen([sys.executable, "-c", "raise RuntimeError('worker failed')"], **kwargs)
        with patch.object(background.subprocess, "Popen", side_effect=fail_instead):
            background.start_comparison(4)
        result = self.wait_for_result()
        self.assertEqual(result["state"], "failed")
        self.assertIn("worker failed", result["error"])
        self.assertTrue(background._job.output.closed)

    def test_spawn_failure_closes_temporary_file(self):
        real_file = background.tempfile.TemporaryFile
        opened = []
        def capture_file(*args, **kwargs):
            result = real_file(*args, **kwargs)
            opened.append(result)
            return result
        with patch.object(background.tempfile, "TemporaryFile", side_effect=capture_file):
            with patch.object(background.subprocess, "Popen", side_effect=OSError("cannot start")):
                with self.assertRaises(OSError):
                    background.start_comparison(4)
        self.assertTrue(opened[0].closed)

    def test_worker_exits_if_parent_channel_closes(self):
        process = subprocess.Popen(
            [sys.executable, str(Path(background.__file__).resolve()), "--worker", "14"],
            stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        try:
            process.stdin.close()
            self.assertEqual(process.wait(timeout=5), 0)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()


if __name__ == "__main__":
    unittest.main()
