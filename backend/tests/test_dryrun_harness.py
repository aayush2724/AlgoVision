"""The Practice page's dry run records a student's Python with a tracer that
runs in the browser on Pyodide (frontend/js/dryrun.worker.js). The tracer is
plain CPython, so it is extracted from the worker and exercised here."""

import json
import re
from pathlib import Path

import pytest

WORKER = Path(__file__).resolve().parents[2] / "frontend" / "js" / "dryrun.worker.js"


@pytest.fixture(scope="module")
def run():
    src = WORKER.read_text()
    harness = re.search(r"const HARNESS = String\.raw`(.*?)`;", src, re.S).group(1)
    ns: dict = {}
    exec(harness, ns)
    return lambda code, call="", cap=1500: json.loads(ns["_run"](code, call, cap))


BUGGY_BINARY_SEARCH = """def binary_search(arr, target):
    low = 0
    high = len(arr)
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid
    return -1"""


def test_records_lines_variables_and_output(run):
    r = run(BUGGY_BINARY_SEARCH, "print(binary_search([1, 3, 5, 7, 9], 7))")
    assert r["error"] is None and r["output"] == "3\n"
    assert r["callLine"] == len(r["lines"])
    inner = [s for s in r["steps"] if len(s["frames"]) == 2]
    frame = inner[-1]["frames"][-1]
    assert frame["name"] == "binary_search()"
    assert frame["vars"]["arr"]["items"] == ["1", "3", "5", "7", "9"]


def test_error_stops_where_it_was_raised(run):
    r = run(BUGGY_BINARY_SEARCH, "print(binary_search([1, 3, 5, 7, 9], 10))")
    assert r["error"]["type"] == "IndexError" and r["error"]["line"] == 6
    last = r["steps"][-1]
    # No bogus "returns None" while the exception unwinds.
    assert last["event"] == "exception" and last["line"] == 6
    assert last["frames"][-1]["vars"]["mid"]["r"] == "5"


def test_caught_exception_keeps_recording(run):
    r = run("try:\n    x = [1][3]\nexcept IndexError:\n    x = -1\nprint(x)")
    assert r["error"] is None and r["output"] == "-1\n"
    assert any(s["event"] == "line" and s["line"] == 4 for s in r["steps"])


def test_recursion_shows_the_call_stack(run):
    r = run("def fib(n):\n    if n < 2:\n        return n\n    return fib(n-1) + fib(n-2)", "print(fib(4))")
    assert r["output"] == "3\n"
    assert max(len(s["frames"]) for s in r["steps"]) == 5   # main + fib(4..1)


def test_infinite_loop_hits_the_step_cap(run):
    r = run("x = 0\nwhile True:\n    x += 1", cap=200)
    assert r["truncated"] and len(r["steps"]) == 200


def test_missing_base_case_is_explained(run):
    r = run("def f(n):\n    return f(n + 1)", "f(0)", cap=100_000)
    assert r["error"]["type"] == "RecursionError"
    assert "base case" in r["error"]["message"]


def test_syntax_error_and_input_are_reported(run):
    r = run("def f(:\n    pass")
    assert r["error"]["type"] == "SyntaxError" and r["steps"] == []
    r = run("n = int(input())")
    assert r["error"]["type"] == "RuntimeError" and "Then run" in r["error"]["message"]
