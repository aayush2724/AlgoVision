from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

import re as _re

from app.tracers import (
    balanced_brackets, bfs, binary_search, bst_insert, bst_search,
    bubble_sort, counting_sort, dfs, dijkstra, edit_distance, fenwick_tree,
    fibonacci_dp, floyd_cycle, heap_insert, insertion_sort, kadanes,
    kmp_search, knapsack_01, segment_tree,
    kruskals_mst, lcs, linked_list_reverse, merge_sort, n_queens,
    next_greater_element, prefix_sums, prims_mst, quick_sort, selection_sort,
    sieve, sliding_window, topological_sort, tree_traversal, trie_insert,
    two_sum_sorted, unique_paths,
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
    "prims_mst": prims_mst.trace,
    "kruskals_mst": kruskals_mst.trace,
    "topological_sort": topological_sort.trace,
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
            {"id": "prims_mst",     "name": "Prim's Minimum Spanning Tree",    "input": "graph"},
            {"id": "kruskals_mst",  "name": "Kruskal's MST (Union-Find)",      "input": "graph"},
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
            {"id": "knapsack_01",   "name": "0/1 Knapsack (DP Grid)",   "input": "text"},
            {"id": "lcs",           "name": "Longest Common Subsequence", "input": "text"},
            {"id": "fibonacci_dp",  "name": "Fibonacci (Memoized DP)",  "input": "number"},
            {"id": "topological_sort", "name": "Topological Sort (Kahn's)", "input": "graph"},
            {"id": "counting_sort", "name": "Counting Sort",           "input": "array"},
            {"id": "prefix_sums",   "name": "Prefix Sums (Range Queries)", "input": "array"},
            {"id": "next_greater_element", "name": "Next Greater Element (Monotonic Stack)", "input": "array"},
            {"id": "edit_distance", "name": "Edit Distance (Levenshtein)", "input": "text"},
            {"id": "floyd_cycle",   "name": "Cycle Detection (Floyd's Tortoise & Hare)", "input": "array"},
            {"id": "tree_traversal", "name": "Tree Traversals (In/Pre/Post-order)", "input": "array"},
            {"id": "trie_insert",   "name": "Trie — Build a Prefix Tree", "input": "text"},
            {"id": "n_queens",      "name": "N-Queens (Backtracking)",   "input": "number"},
            {"id": "unique_paths",  "name": "Unique Paths (Grid DP)",    "input": "number"},
            {"id": "sieve",         "name": "Sieve of Eratosthenes",     "input": "number"},
            {"id": "kmp_search",    "name": "KMP Substring Search",      "input": "text"},
            {"id": "segment_tree",  "name": "Segment Tree — Range Sum",  "input": "array"},
            {"id": "fenwick_tree",  "name": "Fenwick Tree (BIT)",        "input": "array"},
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

    if req.algorithm == "counting_sort":
      arr = _validated_array(req.array, counting_sort.MAX_ARRAY_LEN, "counting_sort")
      if any(v != int(v) or v < 0 or v > counting_sort.MAX_VALUE for v in arr):
        raise HTTPException(
          status_code=400,
          detail=f"Counting sort needs whole numbers from 0 to "
                 f"{counting_sort.MAX_VALUE} — it allocates one bucket per value."
        )
      return counting_sort.trace([int(v) for v in arr])

    if req.algorithm == "prefix_sums":
      arr = _validated_array(req.array, prefix_sums.MAX_ARRAY_LEN, "prefix_sums")
      return prefix_sums.trace(arr)

    if req.algorithm == "next_greater_element":
      arr = _validated_array(req.array, next_greater_element.MAX_ARRAY_LEN,
                             "next_greater_element")
      return next_greater_element.trace(arr)

    if req.algorithm == "floyd_cycle":
      arr = _validated_array(req.array, floyd_cycle.MAX_LIST_LEN, "floyd_cycle")
      link = -1 if req.target is None else req.target
      if link != int(link) or int(link) < -1 or int(link) >= max(len(arr), 1):
        raise HTTPException(
          status_code=400,
          detail=f"'target' is the index the tail links back to: -1 for no "
                 f"cycle, or 0..{max(len(arr) - 1, 0)} to create one."
        )
      return floyd_cycle.trace(arr, int(link))

    if req.algorithm == "kmp_search":
      if req.text is None:
        raise HTTPException(
          status_code=400,
          detail="kmp_search requires 'text' — the haystack and the pattern "
                 "separated by a comma, e.g. ABABCABAB,ABAB"
        )
      cleaned = req.text.replace(" ", "").upper()
      if not _re.fullmatch(
          rf"[A-Z0-9]{{1,{kmp_search.MAX_TEXT}}},[A-Z0-9]{{1,{kmp_search.MAX_PATTERN}}}",
          cleaned):
        raise HTTPException(
          status_code=400,
          detail=f"Provide text (1-{kmp_search.MAX_TEXT} chars) and a pattern "
                 f"(1-{kmp_search.MAX_PATTERN} chars), comma-separated — "
                 f"e.g. ABABDABACDABABCABAB,ABABCABAB"
        )
      hay, needle = cleaned.split(",")
      if len(needle) > len(hay):
        raise HTTPException(
          status_code=400,
          detail="The pattern cannot be longer than the text."
        )
      return kmp_search.trace(hay, needle)

    if req.algorithm == "segment_tree":
      arr = _validated_array(req.array, segment_tree.MAX_ARRAY_LEN,
                             "segment_tree")
      if not arr:
        raise HTTPException(
          status_code=400,
          detail="segment_tree needs at least one value."
        )
      lo, hi = 0, len(arr) - 1
      if req.text:
        cleaned = req.text.replace(" ", "")
        if not _re.fullmatch(r"\d+:\d+", cleaned):
          raise HTTPException(
            status_code=400,
            detail="Query range is lo:hi — e.g. 2:5. Leave blank to sum "
                   "the whole array."
          )
        lo, hi = (int(x) for x in cleaned.split(":"))
        if lo > hi or hi >= len(arr):
          raise HTTPException(
            status_code=400,
            detail=f"Range must satisfy 0 ≤ lo ≤ hi ≤ {len(arr) - 1}."
          )
      return segment_tree.trace(arr, lo, hi)

    if req.algorithm == "fenwick_tree":
      arr = _validated_array(req.array, fenwick_tree.MAX_ARRAY_LEN,
                             "fenwick_tree")
      if not arr:
        raise HTTPException(
          status_code=400,
          detail="fenwick_tree needs at least one value."
        )
      upto = len(arr) - 1 if req.target is None else req.target
      if upto != int(upto) or int(upto) < 0 or int(upto) >= len(arr):
        raise HTTPException(
          status_code=400,
          detail=f"'target' is the prefix end index — 0..{len(arr) - 1}."
        )
      return fenwick_tree.trace(arr, int(upto))

    if req.algorithm == "tree_traversal":
      arr = _validated_array(req.array, tree_traversal.MAX_TREE_LEN,
                             "tree_traversal")
      return tree_traversal.trace(arr)

    if req.algorithm == "trie_insert":
      if req.text is None:
        raise HTTPException(
          status_code=400,
          detail="trie_insert requires 'text' — comma-separated words, "
                 "e.g. CAT,CAR,DOG"
        )
      words = [w for w in req.text.replace(" ", "").upper().split(",") if w]
      if not words:
        raise HTTPException(
          status_code=400,
          detail="Give at least one word — e.g. CAT,CAR,DOG"
        )
      if len(words) > trie_insert.MAX_WORDS:
        raise HTTPException(
          status_code=400,
          detail=f"Max {trie_insert.MAX_WORDS} words."
        )
      if any(not _re.fullmatch(rf"[A-Z]{{1,{trie_insert.MAX_WORD_LEN}}}", w)
             for w in words):
        raise HTTPException(
          status_code=400,
          detail=f"Words must be letters only, 1-{trie_insert.MAX_WORD_LEN} "
                 f"characters each."
        )
      return trie_insert.trace(words)

    if req.algorithm == "n_queens":
      if req.target is None:
        raise HTTPException(
          status_code=400,
          detail=f"n_queens requires 'target' — the board size "
                 f"({n_queens.MIN_N}-{n_queens.MAX_N})."
        )
      n = req.target
      if n != int(n) or int(n) < n_queens.MIN_N or int(n) > n_queens.MAX_N:
        raise HTTPException(
          status_code=400,
          detail=f"Board size must be a whole number between {n_queens.MIN_N} "
                 f"and {n_queens.MAX_N} — smaller boards have no solution and "
                 f"bigger ones make an unreadable trace."
        )
      return n_queens.trace(int(n))

    if req.algorithm == "unique_paths":
      if req.target is None:
        raise HTTPException(
          status_code=400,
          detail=f"unique_paths requires 'target' — the grid side "
                 f"(2-{unique_paths.MAX_SIDE})."
        )
      side = req.target
      if side != int(side) or int(side) < 2 or int(side) > unique_paths.MAX_SIDE:
        raise HTTPException(
          status_code=400,
          detail=f"Grid side must be a whole number between 2 and "
                 f"{unique_paths.MAX_SIDE}."
        )
      side = int(side)
      walls: list = []
      if req.text:
        cleaned = req.text.replace(" ", "")
        if not _re.fullmatch(r"\d+:\d+(,\d+:\d+)*", cleaned):
          raise HTTPException(
            status_code=400,
            detail="Walls are row:col pairs — e.g. 1:1,2:0. Leave blank for "
                   "an open grid."
          )
        walls = [tuple(int(x) for x in p.split(":")) for p in cleaned.split(",")]
        if any(r >= side or c >= side for r, c in walls):
          raise HTTPException(
            status_code=400,
            detail=f"Wall coordinates must be within 0..{side - 1}."
          )
        if (0, 0) in walls:
          raise HTTPException(
            status_code=400,
            detail="The start square cannot be a wall."
          )
      return unique_paths.trace(side, side, walls)

    if req.algorithm == "sieve":
      if req.target is None:
        raise HTTPException(
          status_code=400,
          detail=f"sieve requires 'target' — the upper limit n "
                 f"({sieve.MIN_N}-{sieve.MAX_N})."
        )
      n = req.target
      if n != int(n) or int(n) < sieve.MIN_N or int(n) > sieve.MAX_N:
        raise HTTPException(
          status_code=400,
          detail=f"n must be a whole number between {sieve.MIN_N} and "
                 f"{sieve.MAX_N}."
        )
      return sieve.trace(int(n))

    if req.algorithm == "edit_distance":
      if req.text is None:
        raise HTTPException(
          status_code=400,
          detail="edit_distance requires 'text' — two words separated by a comma."
        )
      cleaned = req.text.replace(" ", "").upper()
      if not _re.fullmatch(
          rf"[A-Z0-9]{{1,{edit_distance.MAX_LEN}}},[A-Z0-9]{{1,{edit_distance.MAX_LEN}}}",
          cleaned):
        raise HTTPException(
          status_code=400,
          detail=f"Provide two words (letters/digits, 1-{edit_distance.MAX_LEN} "
                 f"chars each) separated by a comma — e.g. KITTEN,SITTING"
        )
      a, b = cleaned.split(",")
      return edit_distance.trace(a, b)

    if req.algorithm == "knapsack_01":
      if req.text is None or req.target is None:
        raise HTTPException(
          status_code=400,
          detail="knapsack_01 requires 'text' (weight:value pairs, e.g. "
                 "'2:3,3:4') and 'target' (the capacity)."
        )
      cleaned = req.text.replace(" ", "")
      if not _re.fullmatch(r"\d+:\d+(,\d+:\d+)*", cleaned):
        raise HTTPException(
          status_code=400,
          detail="Items must be weight:value pairs — e.g. 2:3,3:4,4:5"
        )
      items = [tuple(int(x) for x in p.split(":")) for p in cleaned.split(",")]
      if len(items) > knapsack_01.MAX_ITEMS:
        raise HTTPException(
          status_code=400,
          detail=f"Max {knapsack_01.MAX_ITEMS} items."
        )
      if any(w < 1 or w > knapsack_01.MAX_WEIGHT_VALUE
             or v < 1 or v > knapsack_01.MAX_WEIGHT_VALUE for w, v in items):
        raise HTTPException(
          status_code=400,
          detail=f"Weights and values must be 1..{knapsack_01.MAX_WEIGHT_VALUE}."
        )
      cap = req.target
      if cap != int(cap) or int(cap) < 1 or int(cap) > knapsack_01.MAX_CAPACITY:
        raise HTTPException(
          status_code=400,
          detail=f"Capacity must be a whole number 1..{knapsack_01.MAX_CAPACITY}."
        )
      return knapsack_01.trace(items, int(cap))

    if req.algorithm == "lcs":
      if req.text is None:
        raise HTTPException(
          status_code=400,
          detail="lcs requires 'text' — two words separated by a comma."
        )
      cleaned = req.text.replace(" ", "").upper()
      if not _re.fullmatch(rf"[A-Z0-9]{{1,{lcs.MAX_LEN}}},[A-Z0-9]{{1,{lcs.MAX_LEN}}}",
                           cleaned):
        raise HTTPException(
          status_code=400,
          detail=f"Provide two words (letters/digits, 1-{lcs.MAX_LEN} chars "
                 f"each) separated by a comma — e.g. ABCBDAB,BDCAB"
        )
      a, b = cleaned.split(",")
      return lcs.trace(a, b)

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
                "knapsack_01", "lcs", "edit_distance",
                "counting_sort", "prefix_sums", "next_greater_element",
                "floyd_cycle", "tree_traversal", "trie_insert", "n_queens",
                "unique_paths", "sieve", "kmp_search", "segment_tree",
                "fenwick_tree",
                "balanced_brackets", "fibonacci_dp"])
    raise HTTPException(
      status_code=400,
      detail=f"Algorithm must be one of: {', '.join(valid)}"
    )
