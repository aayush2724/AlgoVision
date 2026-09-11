from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from app.tracers import (
    balanced_brackets, bfs, binary_search, bst_insert, bst_search,
    bubble_sort, dfs, dijkstra, fibonacci_dp, heap_insert, insertion_sort,
    kadanes, linked_list_reverse, merge_sort, quick_sort, selection_sort,
    sliding_window, two_sum_sorted,
)
from app.tracers.common import Graph
import os

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    enabled=os.getenv("ALGOVISION_DISABLE_RATELIMIT") != "1",
)
router = APIRouter(prefix="/trace", tags=["trace"])

GRAPH_TRACERS = {
    "dijkstra": dijkstra.trace,
    "bfs": bfs.trace,
    "dfs": dfs.trace,
}
SORT_TRACERS = {
    "merge_sort": merge_sort.trace,
    "quick_sort": quick_sort.trace,
    "bubble_sort": bubble_sort.trace,
    "insertion_sort": insertion_sort.trace,
    "selection_sort": selection_sort.trace,
}
ARRAY_ALGORITHMS = set(SORT_TRACERS) | {"binary_search", "linked_list_reverse"}

MAX_BSEARCH_LEN = 64
MAX_MSORT_LEN = merge_sort.MAX_ARRAY_LEN  # 16 — keeps the trace readable
MAX_VALUE = 1_000_000

class TraceRequest(BaseModel):
    algorithm: str = Field(default="dijkstra", max_length=32)
    start:     str = Field(default="A",        max_length=32)
    graph:     Graph | None = None
    array:     list[float] | None = Field(default=None, max_length=MAX_BSEARCH_LEN)
    target:    float | None = None
    text:      str | None = Field(default=None, max_length=64)

@router.get("/algorithms")
def algorithms():
    return {
        "algorithms": [
            {"id": "dijkstra",      "name": "Dijkstra's Shortest Path", "input": "graph"},
            {"id": "bfs",           "name": "Breadth-First Search",     "input": "graph"},
            {"id": "dfs",           "name": "Depth-First Search",       "input": "graph"},
            {"id": "binary_search", "name": "Binary Search",            "input": "array"},
            {"id": "merge_sort",    "name": "Merge Sort",               "input": "array"},
            {"id": "quick_sort",    "name": "Quick Sort",               "input": "array"},
            {"id": "bubble_sort",    "name": "Bubble Sort",             "input": "array"},
            {"id": "insertion_sort", "name": "Insertion Sort",          "input": "array"},
            {"id": "selection_sort", "name": "Selection Sort",          "input": "array"},
            {"id": "linked_list_reverse", "name": "Reverse a Linked List", "input": "array"},
            {"id": "balanced_brackets",   "name": "Balanced Brackets (Stack)", "input": "text"},
            {"id": "bst_insert",    "name": "BST — Build by Insertion", "input": "array"},
            {"id": "bst_search",    "name": "BST — Search",             "input": "array"},
            {"id": "heap_insert",   "name": "Max-Heap — Build",         "input": "array"},
            {"id": "two_sum_sorted", "name": "Two Sum (Two Pointers)",  "input": "array"},
            {"id": "sliding_window", "name": "Max Window Sum (Sliding Window)", "input": "array"},
            {"id": "kadanes",       "name": "Max Subarray (Kadane's)",  "input": "array"},
            {"id": "fibonacci_dp",  "name": "Fibonacci (Memoized DP)",  "input": "number"},
        ]
    }

def _validated_array(array, max_len, algo):
    if array is None:
        raise HTTPException(
            status_code=400,
            detail=f"Algorithm '{algo}' requires an 'array' of numbers.",
        )
    if len(array) > max_len:
        raise HTTPException(
            status_code=400,
            detail=f"Array too long — max {max_len} values for {algo}.",
        )
    if any(abs(x) > MAX_VALUE for x in array):
        raise HTTPException(
            status_code=400,
            detail=f"Array values must be within ±{MAX_VALUE}.",
        )
    return array

# 30 traces per minute — tracer is CPU-bound
@router.post("")
@limiter.limit("30/minute")
def run_trace(request: Request, req: TraceRequest):
    if req.graph is not None and req.array is not None:
      raise HTTPException(
        status_code=400,
        detail="Provide either 'graph' or 'array', not both."
      )

    if req.algorithm in GRAPH_TRACERS:
      if req.graph is None:
        raise HTTPException(
          status_code=400,
          detail=f"Algorithm '{req.algorithm}' requires a 'graph'."
        )
      node_ids = {n.id for n in req.graph.nodes}
      if req.start not in node_ids:
        raise HTTPException(
          status_code=400,
          detail=f"Start node '{req.start}' not found in graph nodes."
        )
      return GRAPH_TRACERS[req.algorithm](req.graph, req.start)

    if req.algorithm == "binary_search":
      arr = _validated_array(req.array, MAX_BSEARCH_LEN, "binary_search")
      if req.target is None:
        raise HTTPException(
          status_code=400,
          detail="binary_search requires a 'target' value to search for."
        )
      if abs(req.target) > MAX_VALUE:
        raise HTTPException(
          status_code=400,
          detail=f"Target must be within ±{MAX_VALUE}."
        )
      if any(arr[i] > arr[i + 1] for i in range(len(arr) - 1)):
        raise HTTPException(
          status_code=400,
          detail="Binary search requires a sorted array — sort your input first."
        )
      return binary_search.trace(arr, req.target)

    if req.algorithm in SORT_TRACERS:
      arr = _validated_array(req.array, MAX_MSORT_LEN, req.algorithm)
      return SORT_TRACERS[req.algorithm](arr)

    if req.algorithm == "linked_list_reverse":
      arr = _validated_array(req.array, linked_list_reverse.MAX_LIST_LEN,
                             "linked_list_reverse")
      return linked_list_reverse.trace(arr)

    if req.algorithm == "balanced_brackets":
      if req.text is None:
        raise HTTPException(
          status_code=400,
          detail="balanced_brackets requires 'text' — a bracket sequence."
        )
      cleaned = req.text.replace(" ", "")
      if len(cleaned) > balanced_brackets.MAX_TEXT_LEN:
        raise HTTPException(
          status_code=400,
          detail=f"Max {balanced_brackets.MAX_TEXT_LEN} bracket characters."
        )
      if any(c not in balanced_brackets.ALLOWED_CHARS for c in cleaned):
        raise HTTPException(
          status_code=400,
          detail="Only bracket characters allowed: ( ) [ ] { }"
        )
      return balanced_brackets.trace(cleaned)

    if req.algorithm in ("bst_insert", "heap_insert"):
      arr = _validated_array(req.array, bst_insert.MAX_TREE_LEN, req.algorithm)
      fn = bst_insert.trace if req.algorithm == "bst_insert" else heap_insert.trace
      return fn(arr)

    if req.algorithm == "bst_search":
      arr = _validated_array(req.array, bst_insert.MAX_TREE_LEN, "bst_search")
      if req.target is None:
        raise HTTPException(
          status_code=400,
          detail="bst_search requires a 'target' value to search for."
        )
      if abs(req.target) > MAX_VALUE:
        raise HTTPException(
          status_code=400,
          detail=f"Target must be within ±{MAX_VALUE}."
        )
      return bst_search.trace(arr, req.target)

    if req.algorithm == "two_sum_sorted":
      arr = _validated_array(req.array, two_sum_sorted.MAX_ARRAY_LEN, "two_sum_sorted")
      if req.target is None:
        raise HTTPException(
          status_code=400,
          detail="two_sum_sorted requires a 'target' sum."
        )
      if any(arr[i] > arr[i + 1] for i in range(len(arr) - 1)):
        raise HTTPException(
          status_code=400,
          detail="Two-pointer Two Sum requires a sorted array — sort your input first."
        )
      return two_sum_sorted.trace(arr, req.target)

    if req.algorithm == "sliding_window":
      arr = _validated_array(req.array, sliding_window.MAX_ARRAY_LEN, "sliding_window")
      k = req.target
      if k is None:
        raise HTTPException(
          status_code=400,
          detail="sliding_window requires 'target' — the window size k."
        )
      if k != int(k) or int(k) < 1 or int(k) > len(arr):
        raise HTTPException(
          status_code=400,
          detail=f"Window size k must be a whole number between 1 and {len(arr)}."
        )
      return sliding_window.trace(arr, int(k))

    if req.algorithm == "kadanes":
      arr = _validated_array(req.array, kadanes.MAX_ARRAY_LEN, "kadanes")
      return kadanes.trace(arr)

    if req.algorithm == "fibonacci_dp":
      if req.target is None:
        raise HTTPException(
          status_code=400,
          detail="fibonacci_dp requires 'target' — the n to compute."
        )
      n = req.target
      if n != int(n) or n < 0 or n > fibonacci_dp.MAX_N:
        raise HTTPException(
          status_code=400,
          detail=f"n must be a whole number between 0 and {fibonacci_dp.MAX_N}."
        )
      return fibonacci_dp.trace(int(n))

    valid = (list(GRAPH_TRACERS.keys()) + sorted(ARRAY_ALGORITHMS)
             + ["bst_insert", "bst_search", "heap_insert",
                "two_sum_sorted", "sliding_window", "kadanes",
                "balanced_brackets", "fibonacci_dp"])
    raise HTTPException(
      status_code=400,
      detail=f"Algorithm must be one of: {', '.join(valid)}"
    )
