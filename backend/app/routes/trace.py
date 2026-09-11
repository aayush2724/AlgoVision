from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from app.tracers import (
    bfs, binary_search, dfs, dijkstra, fibonacci_dp, merge_sort, quick_sort,
)
from app.tracers.common import Graph
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/trace", tags=["trace"])

GRAPH_TRACERS = {
    "dijkstra": dijkstra.trace,
    "bfs": bfs.trace,
    "dfs": dfs.trace,
}
SORT_TRACERS = {
    "merge_sort": merge_sort.trace,
    "quick_sort": quick_sort.trace,
}
ARRAY_ALGORITHMS = {"binary_search", "merge_sort", "quick_sort"}

MAX_BSEARCH_LEN = 64
MAX_MSORT_LEN = merge_sort.MAX_ARRAY_LEN  # 16 — keeps the trace readable
MAX_VALUE = 1_000_000

class TraceRequest(BaseModel):
    algorithm: str = Field(default="dijkstra", max_length=32)
    start:     str = Field(default="A",        max_length=32)
    graph:     Graph | None = None
    array:     list[float] | None = Field(default=None, max_length=MAX_BSEARCH_LEN)
    target:    float | None = None

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

    valid = list(GRAPH_TRACERS.keys()) + sorted(ARRAY_ALGORITHMS) + ["fibonacci_dp"]
    raise HTTPException(
      status_code=400,
      detail=f"Algorithm must be one of: {', '.join(valid)}"
    )
