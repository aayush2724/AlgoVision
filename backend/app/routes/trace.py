from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

import re as _re

from app.tracers import (
    activity_selection,
    anagram, balanced_brackets, bellman_ford, bfs, binary_search,
    bipartite_check, bst_delete, bst_insert, bst_search, bubble_sort,
    coin_change, connected_components, counting_sort, dfs, dijkstra, dsu,
    edit_distance, fast_exponentiation, gcd_euclid, prime_factorisation,
    fenwick_tree, fibonacci_dp, find_middle, flood_fill, floyd_cycle,
    hash_table, heap_extract, heap_insert, heap_sort, house_robber, huffman,
    fractional_knapsack, job_sequencing,
    jump_game, jump_game_ii, candy, lemonade_change, assign_cookies,
    min_platforms, min_heap, kth_largest, kth_smallest,
    longest_substring_no_repeat, max_consecutive_ones_iii, longest_k_distinct,
    count_set_bits, power_of_two, single_number, min_bit_flips, power_set,
    insertion_sort, kadanes,
    kmp_search, knapsack_01, segment_tree, kruskals_mst, lcs, lis,
    linked_list_reverse, manacher, matrix_chain, merge_intervals, merge_sort,
    merge_two_sorted_lists, n_queens, next_greater_element, prefix_sums,
    prims_mst, quick_sort,
    rabin_karp, radix_sort, selection_sort, sieve, sliding_window,
    sliding_window_maximum, subset_sum, topological_sort,
    tree_traversal, trie_insert, two_sum_sorted, unique_paths, z_function,
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
    "dsu": dsu.trace,
    "connected_components": connected_components.trace,
    "bipartite_check": bipartite_check.trace,
    "bellman_ford": bellman_ford.trace,
}
# These need non-negative weights to be correct; the shared Graph model now
# allows negatives (for Bellman-Ford), so they reject them here instead.
NONNEGATIVE_GRAPH = {"dijkstra", "prims_mst", "kruskals_mst"}
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
    # 64 was too tight once merge_intervals and hash_table started using this
    # field: ten intervals with 3-digit bounds runs to ~89 chars, so valid
    # input was being rejected by the model before its own validator ran.
    # Each algorithm still enforces its own, stricter limit below.
    text:      str | None = Field(default=None, max_length=128)

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
            {"id": "huffman",       "name": "Huffman Coding (Greedy)",   "input": "text"},
            {"id": "activity_selection", "name": "Activity Selection (Greedy)", "input": "text"},
            {"id": "fractional_knapsack", "name": "Fractional Knapsack (Greedy)", "input": "text"},
            {"id": "job_sequencing", "name": "Job Sequencing (Greedy)",   "input": "text"},
            {"id": "jump_game",     "name": "Jump Game I (Greedy)",      "input": "array"},
            {"id": "jump_game_ii",  "name": "Jump Game II (Greedy)",     "input": "array"},
            {"id": "candy",         "name": "Candy (Greedy)",            "input": "array"},
            {"id": "lemonade_change", "name": "Lemonade Change (Greedy)", "input": "array"},
            {"id": "assign_cookies", "name": "Assign Cookies (Greedy)",  "input": "text"},
            {"id": "min_platforms", "name": "Minimum Platforms (Greedy)", "input": "text"},
            {"id": "min_heap",      "name": "Min-Heap — Build",          "input": "array"},
            {"id": "kth_largest",   "name": "Kth Largest (Min-Heap)",    "input": "text"},
            {"id": "kth_smallest",  "name": "Kth Smallest (Max-Heap)",   "input": "text"},
            {"id": "longest_substring_no_repeat", "name": "Longest Substring w/o Repeats", "input": "text"},
            {"id": "max_consecutive_ones_iii", "name": "Max Consecutive Ones III", "input": "text"},
            {"id": "longest_k_distinct", "name": "Longest Substring, K Distinct", "input": "text"},
            {"id": "count_set_bits", "name": "Count Set Bits (Kernighan)", "input": "text"},
            {"id": "power_of_two",  "name": "Power of Two — Bit Test",    "input": "text"},
            {"id": "single_number", "name": "Single Number (XOR)",        "input": "text"},
            {"id": "min_bit_flips", "name": "Minimum Bit Flips",          "input": "text"},
            {"id": "power_set",     "name": "Power Set (Bitmask)",        "input": "text"},
            {"id": "n_queens",      "name": "N-Queens (Backtracking)",   "input": "number"},
            {"id": "unique_paths",  "name": "Unique Paths (Grid DP)",    "input": "number"},
            {"id": "sieve",         "name": "Sieve of Eratosthenes",     "input": "number"},
            {"id": "kmp_search",    "name": "KMP Substring Search",      "input": "text"},
            {"id": "segment_tree",  "name": "Segment Tree — Range Sum",  "input": "array"},
            {"id": "fenwick_tree",  "name": "Fenwick Tree (BIT)",        "input": "array"},
            {"id": "hash_table",    "name": "Hash Table (Chaining)",     "input": "text"},
            {"id": "bst_delete",    "name": "BST — Delete a Node",       "input": "array"},
            {"id": "heap_extract",  "name": "Max-Heap — Extract",        "input": "array"},
            {"id": "dsu",           "name": "Union-Find (DSU)",          "input": "graph"},
            {"id": "merge_intervals", "name": "Merge Intervals",         "input": "text"},
            {"id": "coin_change",   "name": "Coin Change (Fewest Coins)", "input": "array"},
            {"id": "connected_components", "name": "Connected Components", "input": "graph"},
            {"id": "bipartite_check", "name": "Bipartite Check (2-Colouring)", "input": "graph"},
            {"id": "flood_fill",    "name": "Flood Fill (Paint Bucket)", "input": "number"},
            {"id": "house_robber",  "name": "House Robber (1-D DP)",     "input": "array"},
            {"id": "lis",           "name": "Longest Increasing Subsequence", "input": "array"},
            {"id": "subset_sum",    "name": "Subset Sum (DP Grid)",      "input": "number"},
            {"id": "z_function",    "name": "Z-Function",                "input": "text"},
            {"id": "rabin_karp",    "name": "Rabin–Karp (Rolling Hash)", "input": "text"},
            {"id": "manacher",      "name": "Manacher's Longest Palindrome", "input": "text"},
            {"id": "radix_sort",    "name": "Radix Sort (LSD)",          "input": "array"},
            {"id": "sliding_window_maximum", "name": "Sliding Window Maximum (Deque)", "input": "array"},
            {"id": "matrix_chain",  "name": "Matrix Chain Multiplication", "input": "array"},
            {"id": "heap_sort",     "name": "Heap Sort (In-Place)",      "input": "array"},
            {"id": "find_middle",   "name": "Find Middle of a List (Slow/Fast)", "input": "array"},
            {"id": "merge_two_sorted_lists", "name": "Merge Two Sorted Lists", "input": "text"},
            {"id": "anagram",       "name": "Anagram Check",             "input": "text"},
            {"id": "gcd_euclid",    "name": "GCD (Euclid's Algorithm)",  "input": "array"},
            {"id": "fast_exponentiation", "name": "Fast Exponentiation", "input": "array"},
            {"id": "prime_factorisation", "name": "Prime Factorisation", "input": "number"},
            {"id": "bellman_ford",  "name": "Bellman–Ford (Negative Edges)", "input": "graph"},
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


def _parse_intervals(text: str):
    """'1-3, 2-6, 8-10' -> [[1,3], [2,6], [8,10]]. Server-side, so the error
    messages are the ones the student actually sees."""
    cleaned = text.replace(" ", "")
    if not cleaned:
        return []
    parts = [p for p in cleaned.split(",") if p]
    if len(parts) > merge_intervals.MAX_INTERVALS:
        raise HTTPException(
            status_code=400,
            detail=f"At most {merge_intervals.MAX_INTERVALS} intervals — the "
                   f"trace has to stay readable.",
        )
    out = []
    for p in parts:
        if not _re.fullmatch(r"\d+-\d+", p):
            raise HTTPException(
                status_code=400,
                detail=f"Could not read {p!r} as an interval. Use whole-number "
                       f"start-end pairs, e.g. 1-3, 2-6, 8-10",
            )
        a, b = (int(v) for v in p.split("-"))
        if a > b:
            raise HTTPException(
                status_code=400,
                detail=f"Interval {p!r} ends before it starts.",
            )
        if b > merge_intervals.MAX_VALUE:
            raise HTTPException(
                status_code=400,
                detail=f"Interval bounds must be 0–{merge_intervals.MAX_VALUE}.",
            )
        out.append([a, b])
    return out


def _parse_keys(text: str):
    """'CAT,DOG,OWL | DOG' -> (['CAT','DOG','OWL'], 'DOG')."""
    head, sep, tail = text.partition("|")
    keys = [k.strip().upper() for k in head.split(",") if k.strip()]
    lookup = tail.strip().upper() or None if sep else None
    if not keys:
        raise HTTPException(
            status_code=400,
            detail="Give at least one key, e.g. CAT,DOG,OWL,FOX",
        )
    if len(keys) > hash_table.MAX_KEYS:
        raise HTTPException(
            status_code=400,
            detail=f"At most {hash_table.MAX_KEYS} keys — beyond that the "
                   f"chains stop fitting on screen.",
        )
    for k in keys + ([lookup] if lookup else []):
        if not _re.fullmatch(r"[A-Z0-9]{1,10}", k):
            raise HTTPException(
                status_code=400,
                detail=f"Key {k!r} must be 1–10 letters or digits.",
            )
    return keys, lookup


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
      if req.algorithm in NONNEGATIVE_GRAPH and any(
          len(e) > 2 and float(e[2]) < 0 for e in req.graph.edges):
        raise HTTPException(
          status_code=400,
          detail=f"'{req.algorithm}' needs non-negative edge weights. For "
                 f"negative weights, use Bellman-Ford."
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

    if req.algorithm == "heap_extract":
      arr = _validated_array(req.array, heap_extract.MAX_TREE_LEN,
                             "heap_extract")
      return heap_extract.trace(arr)

    if req.algorithm == "bst_delete":
      arr = _validated_array(req.array, bst_delete.MAX_TREE_LEN, "bst_delete")
      if req.target is None:
        raise HTTPException(
          status_code=400,
          detail="bst_delete requires a 'target' — the value to remove."
        )
      if abs(req.target) > MAX_VALUE:
        raise HTTPException(
          status_code=400,
          detail=f"Target must be within ±{MAX_VALUE}."
        )
      return bst_delete.trace(arr, req.target)

    if req.algorithm == "coin_change":
      coins = _validated_array(req.array, coin_change.MAX_COINS, "coin_change")
      if not coins:
        raise HTTPException(
          status_code=400,
          detail="coin_change needs at least one coin denomination."
        )
      if any(c != int(c) or int(c) < 1 for c in coins):
        raise HTTPException(
          status_code=400,
          detail="Coin denominations must be whole numbers of 1 or more."
        )
      if req.target is None:
        raise HTTPException(
          status_code=400,
          detail="coin_change requires a 'target' — the amount to make."
        )
      amount = req.target
      if amount != int(amount) or not (0 <= int(amount) <= coin_change.MAX_AMOUNT):
        raise HTTPException(
          status_code=400,
          detail=f"Amount must be a whole number from 0 to "
                 f"{coin_change.MAX_AMOUNT} — the table has to stay readable."
        )
      return coin_change.trace([int(c) for c in coins], int(amount))

    if req.algorithm == "merge_intervals":
      if req.text is None:
        raise HTTPException(
          status_code=400,
          detail="merge_intervals requires 'text' — intervals as start-end "
                 "pairs, e.g. 1-3, 2-6, 8-10, 15-18"
        )
      intervals = _parse_intervals(req.text)
      return merge_intervals.trace(intervals)

    if req.algorithm == "activity_selection":
      if req.text is None:
        raise HTTPException(
          status_code=400,
          detail="activity_selection requires 'text' — meetings as start-end "
                 "pairs, e.g. 1-3, 2-6, 8-10, 15-18"
        )
      intervals = _parse_intervals(req.text)
      if not intervals:
        raise HTTPException(
          status_code=400,
          detail="Give at least one meeting — e.g. 1-3, 2-6, 8-10."
        )
      return activity_selection.trace(intervals)

    if req.algorithm == "fractional_knapsack":
      if req.text is None:
        raise HTTPException(
          status_code=400,
          detail="fractional_knapsack requires 'text' — weight:value pairs then "
                 "'| capacity', e.g. 10:60, 20:100, 30:120 | 50"
        )
      raw = req.text.replace(" ", "")
      if "|" not in raw:
        raise HTTPException(
          status_code=400,
          detail="Add the capacity after a '|' — e.g. 10:60, 20:100 | 50"
        )
      item_part, cap_part = raw.split("|", 1)
      if not _re.fullmatch(r"\d+:\d+(,\d+:\d+)*", item_part):
        raise HTTPException(
          status_code=400,
          detail="Items must be weight:value pairs — e.g. 10:60,20:100"
        )
      items = [[int(x) for x in p.split(":")] for p in item_part.split(",")]
      if len(items) > fractional_knapsack.MAX_ITEMS:
        raise HTTPException(status_code=400,
          detail=f"Max {fractional_knapsack.MAX_ITEMS} items.")
      if any(w < 1 or w > fractional_knapsack.MAX_WEIGHT_VALUE
             or v < 1 or v > fractional_knapsack.MAX_WEIGHT_VALUE for w, v in items):
        raise HTTPException(status_code=400,
          detail=f"Weights and values must be 1..{fractional_knapsack.MAX_WEIGHT_VALUE}.")
      if not _re.fullmatch(r"\d+", cap_part):
        raise HTTPException(status_code=400, detail="Capacity must be a whole number.")
      cap = int(cap_part)
      if cap < 1 or cap > fractional_knapsack.MAX_CAPACITY:
        raise HTTPException(status_code=400,
          detail=f"Capacity must be 1..{fractional_knapsack.MAX_CAPACITY}.")
      return fractional_knapsack.trace(items, cap)

    if req.algorithm == "job_sequencing":
      if req.text is None:
        raise HTTPException(
          status_code=400,
          detail="job_sequencing requires 'text' — deadline:profit pairs, "
                 "e.g. 2:100, 1:19, 2:27, 1:25, 3:15"
        )
      raw = req.text.replace(" ", "")
      if not _re.fullmatch(r"\d+:\d+(,\d+:\d+)*", raw):
        raise HTTPException(
          status_code=400,
          detail="Jobs must be deadline:profit pairs — e.g. 2:100,1:19,3:15"
        )
      jobs = [[int(x) for x in p.split(":")] for p in raw.split(",")]
      if len(jobs) > job_sequencing.MAX_JOBS:
        raise HTTPException(status_code=400,
          detail=f"Max {job_sequencing.MAX_JOBS} jobs.")
      if any(d < 1 or d > job_sequencing.MAX_DEADLINE for d, _ in jobs):
        raise HTTPException(status_code=400,
          detail=f"Deadlines must be 1..{job_sequencing.MAX_DEADLINE}.")
      if any(p < 0 or p > job_sequencing.MAX_PROFIT for _, p in jobs):
        raise HTTPException(status_code=400,
          detail=f"Profits must be 0..{job_sequencing.MAX_PROFIT}.")
      return job_sequencing.trace(jobs)

    if req.algorithm in ("jump_game", "jump_game_ii", "candy", "lemonade_change"):
      arr = _validated_array(req.array, 16, req.algorithm)
      ints = [int(x) for x in arr]
      if any(x != v for x, v in zip(arr, ints)):
        raise HTTPException(status_code=400, detail="Values must be whole numbers.")
      if req.algorithm in ("jump_game", "jump_game_ii") and any(v < 0 for v in ints):
        raise HTTPException(status_code=400, detail="Jump lengths must be 0 or more.")
      if req.algorithm == "candy" and any(v < 0 for v in ints):
        raise HTTPException(status_code=400, detail="Ratings must be 0 or more.")
      if req.algorithm == "lemonade_change" and any(v not in (5, 10, 20) for v in ints):
        raise HTTPException(status_code=400, detail="Bills must each be 5, 10, or 20.")
      tracer = {"jump_game": jump_game, "jump_game_ii": jump_game_ii,
                "candy": candy, "lemonade_change": lemonade_change}[req.algorithm]
      return tracer.trace(ints)

    if req.algorithm in ("assign_cookies", "min_platforms"):
      if req.text is None or "|" not in req.text:
        raise HTTPException(
          status_code=400,
          detail=f"{req.algorithm} requires 'text' — two number lists split by "
                 f"'|', e.g. 1,2,3 | 1,1")
      left_raw, right_raw = req.text.replace(" ", "").split("|", 1)
      def _ints(s):
        parts = [p for p in s.split(",") if p]
        if not parts or not all(_re.fullmatch(r"\d+", p) for p in parts):
          raise HTTPException(status_code=400,
            detail="Both sides must be comma-separated whole numbers.")
        return [int(p) for p in parts]
      left, right = _ints(left_raw), _ints(right_raw)
      if len(left) > 10 or len(right) > 10:
        raise HTTPException(status_code=400, detail="Max 10 numbers per list.")
      if req.algorithm == "assign_cookies":
        return assign_cookies.trace(left, right)
      if len(left) != len(right):
        raise HTTPException(status_code=400,
          detail="Give equal numbers of arrivals and departures.")
      return min_platforms.trace(left, right)

    if req.algorithm == "min_heap":
      arr = _validated_array(req.array, min_heap.MAX_TREE_LEN, "min_heap")
      ints = [int(x) for x in arr]
      if any(x != v for x, v in zip(arr, ints)):
        raise HTTPException(status_code=400, detail="Values must be whole numbers.")
      return min_heap.trace(ints)

    if req.algorithm in ("kth_largest", "kth_smallest"):
      if req.text is None or "|" not in req.text:
        raise HTTPException(
          status_code=400,
          detail=f"{req.algorithm} requires 'text' — numbers then '| k', "
                 f"e.g. 3,2,1,5,6,4 | 2")
      seq_raw, k_raw = req.text.replace(" ", "").split("|", 1)
      parts = [p for p in seq_raw.split(",") if p]
      if not parts or not all(_re.fullmatch(r"-?\d+", p) for p in parts):
        raise HTTPException(status_code=400, detail="Give comma-separated whole numbers.")
      nums = [int(p) for p in parts]
      if len(nums) > 14:
        raise HTTPException(status_code=400, detail="Max 14 numbers.")
      if not _re.fullmatch(r"\d+", k_raw):
        raise HTTPException(status_code=400, detail="k must be a whole number.")
      k = int(k_raw)
      if k < 1 or k > len(nums):
        raise HTTPException(status_code=400, detail=f"k must be between 1 and {len(nums)}.")
      tracer = kth_largest if req.algorithm == "kth_largest" else kth_smallest
      return tracer.trace(nums, k)

    if req.algorithm == "longest_substring_no_repeat":
      if req.text is None:
        raise HTTPException(status_code=400,
          detail="longest_substring_no_repeat requires 'text' — a word, e.g. ABCABCBB.")
      cleaned = req.text.replace(" ", "").upper()
      if not _re.fullmatch(rf"[A-Z0-9]{{1,{longest_substring_no_repeat.MAX_LEN}}}", cleaned):
        raise HTTPException(status_code=400,
          detail=f"One word of letters/digits, 1-{longest_substring_no_repeat.MAX_LEN} chars.")
      return longest_substring_no_repeat.trace(cleaned)

    if req.algorithm == "max_consecutive_ones_iii":
      if req.text is None or "|" not in req.text:
        raise HTTPException(status_code=400,
          detail="max_consecutive_ones_iii requires 'text' — bits then '| k', e.g. 1,1,0,0,1 | 2")
      bits_raw, k_raw = req.text.replace(" ", "").split("|", 1)
      parts = [p for p in bits_raw.split(",") if p]
      if not parts or any(p not in ("0", "1") for p in parts):
        raise HTTPException(status_code=400, detail="Bits must each be 0 or 1.")
      if len(parts) > 20:
        raise HTTPException(status_code=400, detail="Max 20 bits.")
      if not _re.fullmatch(r"\d+", k_raw):
        raise HTTPException(status_code=400, detail="k must be a whole number.")
      return max_consecutive_ones_iii.trace([int(p) for p in parts], int(k_raw))

    if req.algorithm == "longest_k_distinct":
      if req.text is None or "|" not in req.text:
        raise HTTPException(status_code=400,
          detail="longest_k_distinct requires 'text' — a word then '| k', e.g. ECEBA | 2")
      seq_raw, k_raw = req.text.split("|", 1)
      cleaned = seq_raw.replace(" ", "").upper()
      if not _re.fullmatch(rf"[A-Z0-9]{{1,{longest_k_distinct.MAX_LEN}}}", cleaned):
        raise HTTPException(status_code=400,
          detail=f"One word of letters/digits, 1-{longest_k_distinct.MAX_LEN} chars.")
      k_raw = k_raw.strip()
      if not _re.fullmatch(r"\d+", k_raw) or int(k_raw) < 1:
        raise HTTPException(status_code=400, detail="k must be a whole number ≥ 1.")
      return longest_k_distinct.trace(cleaned, int(k_raw))

    if req.algorithm in ("count_set_bits", "power_of_two"):
      if req.text is None or not _re.fullmatch(r"\d+", req.text.strip()):
        raise HTTPException(status_code=400,
          detail=f"{req.algorithm} requires 'text' — a whole number, e.g. 13.")
      n = int(req.text.strip())
      if n > count_set_bits.MAX_N:
        raise HTTPException(status_code=400,
          detail=f"Keep the number 0..{count_set_bits.MAX_N} (fits 12 bits).")
      return (count_set_bits if req.algorithm == "count_set_bits"
              else power_of_two).trace(n)

    if req.algorithm == "single_number":
      if req.text is None:
        raise HTTPException(status_code=400,
          detail="single_number requires 'text' — comma-separated numbers, e.g. 4,1,2,1,2.")
      parts = [p for p in req.text.replace(" ", "").split(",") if p]
      if not parts or not all(_re.fullmatch(r"\d+", p) for p in parts):
        raise HTTPException(status_code=400, detail="Give comma-separated whole numbers.")
      nums = [int(p) for p in parts]
      if len(nums) > 15 or any(v > single_number.MAX_N for v in nums):
        raise HTTPException(status_code=400,
          detail=f"Up to 15 numbers, each 0..{single_number.MAX_N}.")
      return single_number.trace(nums)

    if req.algorithm == "min_bit_flips":
      if req.text is None or "|" not in req.text:
        raise HTTPException(status_code=400,
          detail="min_bit_flips requires 'text' — two numbers as 'a | b', e.g. 10 | 7.")
      a_raw, b_raw = req.text.replace(" ", "").split("|", 1)
      if not (_re.fullmatch(r"\d+", a_raw) and _re.fullmatch(r"\d+", b_raw)):
        raise HTTPException(status_code=400, detail="Both A and B must be whole numbers.")
      a, b = int(a_raw), int(b_raw)
      if a > min_bit_flips.MAX_N or b > min_bit_flips.MAX_N:
        raise HTTPException(status_code=400,
          detail=f"Keep A and B 0..{min_bit_flips.MAX_N}.")
      return min_bit_flips.trace(a, b)

    if req.algorithm == "power_set":
      if req.text is None:
        raise HTTPException(status_code=400,
          detail="power_set requires 'text' — 2-5 elements, e.g. A,B,C.")
      raw = req.text.replace(" ", "").upper()
      els = [p for p in raw.split(",") if p] if "," in raw else list(raw)
      if not (1 <= len(els) <= power_set.MAX_ELEMENTS):
        raise HTTPException(status_code=400,
          detail=f"Give 1-{power_set.MAX_ELEMENTS} elements, e.g. A,B,C.")
      if any(not _re.fullmatch(r"[A-Z0-9]", e) for e in els):
        raise HTTPException(status_code=400, detail="Elements must be single letters or digits.")
      return power_set.trace(els)

    if req.algorithm == "hash_table":
      if req.text is None:
        raise HTTPException(
          status_code=400,
          detail="hash_table requires 'text' — comma-separated keys, "
                 "optionally followed by | and a key to look up, "
                 "e.g. CAT,DOG,OWL,FOX | DOG"
        )
      keys, lookup = _parse_keys(req.text)
      return hash_table.trace(keys, hash_table.DEFAULT_BUCKETS, lookup)

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

    if req.algorithm == "anagram":
      if req.text is None:
        raise HTTPException(
          status_code=400,
          detail="anagram requires 'text' — two words separated by a comma, "
                 "e.g. LISTEN,SILENT"
        )
      cleaned = req.text.replace(" ", "").upper()
      if not _re.fullmatch(rf"[A-Z0-9]{{1,{anagram.MAX_LEN}}},[A-Z0-9]{{1,{anagram.MAX_LEN}}}",
                           cleaned):
        raise HTTPException(
          status_code=400,
          detail=f"Give two words (letters/digits, 1-{anagram.MAX_LEN} chars "
                 f"each) separated by a comma — e.g. LISTEN,SILENT"
        )
      a, b = cleaned.split(",")
      return anagram.trace(a, b)

    if req.algorithm == "gcd_euclid":
      pair = _validated_array(req.array, 2, "gcd_euclid")
      if len(pair) != 2:
        raise HTTPException(
          status_code=400,
          detail="gcd_euclid needs exactly two numbers, e.g. 48, 36."
        )
      if any(v != int(v) or v < 0 or v > gcd_euclid.MAX_VALUE for v in pair):
        raise HTTPException(
          status_code=400,
          detail=f"Both numbers must be whole values from 0 to "
                 f"{gcd_euclid.MAX_VALUE}."
        )
      if pair[0] == 0 and pair[1] == 0:
        raise HTTPException(
          status_code=400,
          detail="gcd(0, 0) is undefined — give at least one non-zero number."
        )
      return gcd_euclid.trace(int(pair[0]), int(pair[1]))

    if req.algorithm == "fast_exponentiation":
      pair = _validated_array(req.array, 2, "fast_exponentiation")
      if len(pair) != 2:
        raise HTTPException(
          status_code=400,
          detail="fast_exponentiation needs two numbers: base, exponent — "
                 "e.g. 3, 13."
        )
      base, exp = pair
      if base != int(base) or not (1 <= int(base) <= fast_exponentiation.MAX_BASE):
        raise HTTPException(
          status_code=400,
          detail=f"Base must be a whole number from 1 to "
                 f"{fast_exponentiation.MAX_BASE}."
        )
      if exp != int(exp) or not (0 <= int(exp) <= fast_exponentiation.MAX_EXP):
        raise HTTPException(
          status_code=400,
          detail=f"Exponent must be a whole number from 0 to "
                 f"{fast_exponentiation.MAX_EXP}."
        )
      return fast_exponentiation.trace(int(base), int(exp))

    if req.algorithm == "prime_factorisation":
      if req.target is None:
        raise HTTPException(
          status_code=400,
          detail="prime_factorisation requires 'target' — the number to factor."
        )
      n = req.target
      if n != int(n) or int(n) < 2 or int(n) > prime_factorisation.MAX_VALUE:
        raise HTTPException(
          status_code=400,
          detail=f"Give a whole number from 2 to {prime_factorisation.MAX_VALUE} "
                 f"to factor."
        )
      return prime_factorisation.trace(int(n))

    if req.algorithm == "heap_sort":
      arr = _validated_array(req.array, heap_sort.MAX_ARRAY_LEN, "heap_sort")
      return heap_sort.trace(arr)

    if req.algorithm == "find_middle":
      arr = _validated_array(req.array, find_middle.MAX_LIST_LEN, "find_middle")
      if not arr:
        raise HTTPException(
          status_code=400,
          detail="find_middle needs a non-empty list."
        )
      return find_middle.trace(arr)

    if req.algorithm == "merge_two_sorted_lists":
      if req.text is None:
        raise HTTPException(
          status_code=400,
          detail="merge_two_sorted_lists requires 'text' — two sorted lists "
                 "separated by '|', e.g. 1,3,5,7 | 2,4,6"
        )
      halves = req.text.split("|")
      if len(halves) != 2:
        raise HTTPException(
          status_code=400,
          detail="Give exactly two lists separated by a single '|', "
                 "e.g. 1,3,5,7 | 2,4,6"
        )
      lists = []
      for half in halves:
        nums = []
        for tok in half.replace(" ", "").split(","):
          if tok == "":
            continue
          try:
            nums.append(float(tok))
          except ValueError:
            raise HTTPException(
              status_code=400,
              detail=f"'{tok}' is not a number. Use comma-separated numbers, "
                     f"e.g. 1,3,5,7 | 2,4,6"
            )
        if len(nums) > merge_two_sorted_lists.MAX_EACH:
          raise HTTPException(
            status_code=400,
            detail=f"Each list holds at most {merge_two_sorted_lists.MAX_EACH} "
                   f"values — the chains have to stay readable."
          )
        if any(nums[i] > nums[i + 1] for i in range(len(nums) - 1)):
          raise HTTPException(
            status_code=400,
            detail="Each list must already be sorted ascending — merging "
                   "relies on that. Sort your input first."
          )
        lists.append(nums)
      if not lists[0] and not lists[1]:
        raise HTTPException(
          status_code=400,
          detail="Both lists are empty — give at least one value to merge."
        )
      return merge_two_sorted_lists.trace(lists[0], lists[1])

    if req.algorithm == "radix_sort":
      arr = _validated_array(req.array, radix_sort.MAX_ARRAY_LEN, "radix_sort")
      if any(v != int(v) or v < 0 or v > radix_sort.MAX_VALUE for v in arr):
        raise HTTPException(
          status_code=400,
          detail=f"Radix sort needs whole numbers from 0 to "
                 f"{radix_sort.MAX_VALUE}."
        )
      return radix_sort.trace([int(v) for v in arr])

    if req.algorithm == "sliding_window_maximum":
      arr = _validated_array(req.array, sliding_window_maximum.MAX_ARRAY_LEN,
                             "sliding_window_maximum")
      k = req.target
      if k is None:
        raise HTTPException(
          status_code=400,
          detail="sliding_window_maximum requires 'target' — the window size k."
        )
      if k != int(k) or int(k) < 1 or int(k) > len(arr):
        raise HTTPException(
          status_code=400,
          detail=f"Window size k must be a whole number between 1 and {len(arr)}."
        )
      return sliding_window_maximum.trace(arr, int(k))

    if req.algorithm == "matrix_chain":
      dims = _validated_array(req.array, matrix_chain.MAX_MATRICES + 1,
                              "matrix_chain")
      if len(dims) < 2:
        raise HTTPException(
          status_code=400,
          detail="matrix_chain needs at least 2 dimensions (one matrix) — "
                 "e.g. 40, 20, 30 is two matrices 40×20 and 20×30."
        )
      if any(v != int(v) or v < 1 or v > 1000 for v in dims):
        raise HTTPException(
          status_code=400,
          detail="Matrix dimensions must be whole numbers from 1 to 1000."
        )
      return matrix_chain.trace([int(v) for v in dims])

    if req.algorithm == "z_function":
      if req.text is None:
        raise HTTPException(
          status_code=400,
          detail="z_function requires 'text' — a single word, e.g. AABAAB."
        )
      cleaned = req.text.replace(" ", "").upper()
      if not _re.fullmatch(rf"[A-Z0-9]{{1,{z_function.MAX_LEN}}}", cleaned):
        raise HTTPException(
          status_code=400,
          detail=f"Give one word of letters or digits, 1-{z_function.MAX_LEN} "
                 f"characters — e.g. AABXAAB."
        )
      return z_function.trace(cleaned)

    if req.algorithm == "huffman":
      if req.text is None:
        raise HTTPException(
          status_code=400,
          detail="huffman requires 'text' — a word to encode, e.g. ABRACADABRA."
        )
      cleaned = req.text.replace(" ", "").upper()
      if not _re.fullmatch(rf"[A-Z0-9]{{2,{huffman.MAX_LEN}}}", cleaned):
        raise HTTPException(
          status_code=400,
          detail=f"Give a word of letters or digits, 2-{huffman.MAX_LEN} "
                 f"characters — e.g. ABRACADABRA."
        )
      if len(set(cleaned)) < 2:
        raise HTTPException(
          status_code=400,
          detail="huffman needs at least two distinct characters to build a tree."
        )
      return huffman.trace(cleaned)

    if req.algorithm == "manacher":
      if req.text is None:
        raise HTTPException(
          status_code=400,
          detail="manacher requires 'text' — a single word, e.g. BABAD."
        )
      cleaned = req.text.replace(" ", "").upper()
      if not _re.fullmatch(rf"[A-Z0-9]{{1,{manacher.MAX_LEN}}}", cleaned):
        raise HTTPException(
          status_code=400,
          detail=f"Give one word of letters or digits, 1-{manacher.MAX_LEN} "
                 f"characters — e.g. FORGEEKSSKEEGFOR."
        )
      return manacher.trace(cleaned)

    if req.algorithm == "rabin_karp":
      if req.text is None:
        raise HTTPException(
          status_code=400,
          detail="rabin_karp requires 'text' — the haystack and the pattern "
                 "separated by a comma, e.g. ABRACADABRA,ABRA"
        )
      cleaned = req.text.replace(" ", "").upper()
      if not _re.fullmatch(
          rf"[A-Z0-9]{{1,{rabin_karp.MAX_TEXT}}},[A-Z0-9]{{1,{rabin_karp.MAX_PATTERN}}}",
          cleaned):
        raise HTTPException(
          status_code=400,
          detail=f"Provide text (1-{rabin_karp.MAX_TEXT} chars) and a pattern "
                 f"(1-{rabin_karp.MAX_PATTERN} chars), comma-separated — "
                 f"e.g. ABRACADABRA,ABRA"
        )
      hay, needle = cleaned.split(",")
      if len(needle) > len(hay):
        raise HTTPException(
          status_code=400,
          detail="The pattern cannot be longer than the text."
        )
      return rabin_karp.trace(hay, needle)

    if req.algorithm == "house_robber":
      arr = _validated_array(req.array, house_robber.MAX_HOUSES, "house_robber")
      if any(v != int(v) or v < 0 for v in arr):
        raise HTTPException(
          status_code=400,
          detail="House loot must be whole numbers of 0 or more."
        )
      return house_robber.trace([int(v) for v in arr])

    if req.algorithm == "lis":
      arr = _validated_array(req.array, lis.MAX_LEN, "lis")
      if any(v != int(v) for v in arr):
        raise HTTPException(
          status_code=400,
          detail="Longest increasing subsequence needs whole numbers."
        )
      return lis.trace([int(v) for v in arr])

    if req.algorithm == "subset_sum":
      arr = _validated_array(req.array, subset_sum.MAX_ITEMS, "subset_sum")
      if not arr:
        raise HTTPException(
          status_code=400,
          detail="subset_sum needs at least one number."
        )
      if any(v != int(v) or v < 1 or v > subset_sum.MAX_VALUE for v in arr):
        raise HTTPException(
          status_code=400,
          detail=f"Numbers must be whole values from 1 to "
                 f"{subset_sum.MAX_VALUE} — the grid has to stay readable."
        )
      if req.target is None:
        raise HTTPException(
          status_code=400,
          detail="subset_sum requires a 'target' — the sum to hit."
        )
      t = req.target
      if t != int(t) or int(t) < 0 or int(t) > subset_sum.MAX_TARGET:
        raise HTTPException(
          status_code=400,
          detail=f"Target sum must be a whole number from 0 to "
                 f"{subset_sum.MAX_TARGET}."
        )
      return subset_sum.trace([int(v) for v in arr], int(t))

    if req.algorithm == "flood_fill":
      if req.target is None:
        raise HTTPException(
          status_code=400,
          detail=f"flood_fill requires 'target' — the grid side "
                 f"(2-{flood_fill.MAX_SIDE})."
        )
      side = req.target
      if side != int(side) or int(side) < 2 or int(side) > flood_fill.MAX_SIDE:
        raise HTTPException(
          status_code=400,
          detail=f"Grid side must be a whole number between 2 and "
                 f"{flood_fill.MAX_SIDE}."
        )
      side = int(side)
      # 'start' doubles as the start cell here — "r:c", defaulting to 0:0.
      start_raw = (req.start or "").replace(" ", "")
      if start_raw in ("", "A"):
        sr, sc = 0, 0
      elif _re.fullmatch(r"\d+:\d+", start_raw):
        sr, sc = (int(x) for x in start_raw.split(":"))
      else:
        raise HTTPException(
          status_code=400,
          detail="Start cell is row:col — e.g. 0:0."
        )
      if sr >= side or sc >= side:
        raise HTTPException(
          status_code=400,
          detail=f"Start cell must be within 0..{side - 1}."
        )
      walls: list = []
      if req.text:
        cleaned = req.text.replace(" ", "")
        if not _re.fullmatch(r"\d+:\d+(,\d+:\d+)*", cleaned):
          raise HTTPException(
            status_code=400,
            detail="Walls are row:col pairs — e.g. 1:1,2:0. Leave blank for "
                   "an open canvas."
          )
        walls = [tuple(int(x) for x in p.split(":")) for p in cleaned.split(",")]
        if any(r >= side or c >= side for r, c in walls):
          raise HTTPException(
            status_code=400,
            detail=f"Wall coordinates must be within 0..{side - 1}."
          )
        if (sr, sc) in walls:
          raise HTTPException(
            status_code=400,
            detail="The start cell cannot be a wall."
          )
      return flood_fill.trace(side, side, walls, (sr, sc))

    valid = (list(GRAPH_TRACERS.keys()) + sorted(ARRAY_ALGORITHMS)
             + ["bst_insert", "bst_search", "heap_insert",
                "two_sum_sorted", "sliding_window", "kadanes",
                "knapsack_01", "lcs", "edit_distance",
                "counting_sort", "prefix_sums", "next_greater_element",
                "floyd_cycle", "tree_traversal", "trie_insert", "n_queens",
                "unique_paths", "sieve", "kmp_search", "segment_tree",
                "fenwick_tree",
                "hash_table", "bst_delete", "heap_extract",
                "merge_intervals", "coin_change", "flood_fill",
                "house_robber", "lis", "subset_sum",
                "z_function", "rabin_karp", "manacher",
                "radix_sort", "sliding_window_maximum", "matrix_chain",
                "heap_sort", "find_middle", "merge_two_sorted_lists",
                "anagram", "gcd_euclid", "fast_exponentiation",
                "prime_factorisation",
                "balanced_brackets", "fibonacci_dp", "huffman",
                "activity_selection", "fractional_knapsack", "job_sequencing",
                "jump_game", "jump_game_ii", "candy", "lemonade_change",
                "assign_cookies", "min_platforms", "min_heap", "kth_largest",
                "kth_smallest", "longest_substring_no_repeat",
                "max_consecutive_ones_iii", "longest_k_distinct",
                "count_set_bits", "power_of_two", "single_number",
                "min_bit_flips", "power_set"])
    raise HTTPException(
      status_code=400,
      detail=f"Algorithm must be one of: {', '.join(valid)}"
    )
