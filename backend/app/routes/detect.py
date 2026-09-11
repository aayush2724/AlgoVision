from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
import os
import re
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    enabled=os.getenv("ALGOVISION_DISABLE_RATELIMIT") != "1",
)
router = APIRouter(prefix="/detect", tags=["detect"])

class DetectRequest(BaseModel):
    code:    str = Field(default="", max_length=8_000)
    problem: str = Field(default="", max_length=500)

SIGNATURES = {
    # Each list also contains the algorithm's own id so callers can pass an
    # id as `problem` and get the matching real-world meta back.
    "dijkstra": ["heapq", "heappush", "heappop", "dist[", "shortest", "dijkstra", "priority queue", "pq"],
    "bfs": ["deque", "queue", "bfs", "level order", "breadth", "visited", "neighbors"],
    "dfs": ["dfs", "depth first", "recursive", "backtrack", "stack", "visited"],
    "binary_search": ["binary search", "binary_search", "low", "high", "mid", "bisect", "log n", "sorted array"],
    "merge_sort": ["merge sort", "merge_sort", "mergesort", "merge(", "divide", "conquer", "mid = len"],
    "quick_sort": ["quicksort", "quick sort", "quick_sort", "pivot", "partition"],
    "bubble_sort": ["bubble sort", "bubble_sort", "bubblesort", "adjacent swap"],
    "insertion_sort": ["insertion sort", "insertion_sort", "insertionsort", "key = arr"],
    "selection_sort": ["selection sort", "selection_sort", "selectionsort", "min_idx", "find minimum"],
    "linked_list_reverse": ["linked list", "linked_list", "linked_list_reverse", "listnode", ".next", "->next", "reverse list"],
    "balanced_brackets": ["balanced_brackets", "balanced bracket", "valid parenthes", "matching bracket", "isvalid(s"],
    "bst_insert": ["bst_insert", "bst", "binary search tree", "binarysearchtree", "node.left", "node.right", "root.left", "root.right"],
    "bst_search": ["bst_search", "search bst", "find in tree", "tree search"],
    "heap_insert": ["heap_insert", "heapify", "bubble up", "sift up", "max heap", "min heap", "binary heap", "max-heap"],
    "dynamic_programming": ["dp[", "memo", "memoization", "tabulation", "subproblem", "lru_cache", "functools", "dynamic_programming", "fibonacci", "fibonacci_dp", "fib("],
    "two_sum_sorted": ["two_sum_sorted", "two sum", "two_sum", "twosum", "two pointer", "while left < right", "pair with sum"],
    "sliding_window": ["sliding_window", "sliding window", "window sum", "window size", "subarray of size"],
    "kadanes": ["kadane", "kadanes", "max subarray", "maximum subarray", "max_ending_here", "best sum"],
    "prims_mst": ["prims_mst", "prim", "prims", "minimum spanning", "spanning tree", "mst"],
    "kruskals_mst": ["kruskals_mst", "kruskal", "kruskals", "union find", "union_find", "disjoint set", "dsu"],
    "knapsack_01": ["knapsack", "knapsack_01", "0/1 knapsack", "capacity", "weights[", "values["],
    "lcs": ["lcs", "longest common subsequence", "common subsequence", "edit distance"],
    "greedy": ["greedy", "interval", "sort(", "local optimal", "activity selection"],
}

REALWORLD_META = {
    "dijkstra": {
        "scene": "gps",
        "title": "GPS Navigation System",
        "hook": "You are Google Maps calculating the fastest route through a city.",
        "metaphors": {
            "node": "intersection",
            "edge": "road segment",
            "weight": "travel time (minutes)",
            "visit": "GPS scans this intersection",
            "relax": "Found a faster route via",
            "start": "Your current location",
            "done": "Shortest routes to all destinations calculated."
        }
    },
    "bfs": {
        "scene": "social",
        "title": "Social Network — Friend Discovery",
        "hook": "You are Facebook's friend suggestion engine exploring connections.",
        "metaphors": {
            "node": "person",
            "edge": "friendship",
            "weight": "connection strength",
            "visit": "Discovered connection",
            "enqueue": "Added to friend suggestions",
            "start": "Starting from your profile",
            "done": "All connections within reach mapped."
        }
    },
    "binary_search": {
        "scene": "library",
        "title": "Digital Library Catalog",
        "hook": "You are a library system searching 1 million books in milliseconds.",
        "metaphors": {
            "node": "book",
            "edge": "catalog section",
            "weight": "alphabetical position",
            "visit": "Opening catalog section",
            "mid": "Checking middle of remaining catalog",
            "start": "Entire catalog available",
            "done": "Book located."
        }
    },
    "dfs": {
        "scene": "maze",
        "title": "Maze Exploration",
        "hook": "You are a robot exploring an unknown maze, mapping every corridor.",
        "metaphors": {
            "node": "room",
            "edge": "corridor",
            "weight": "distance",
            "visit": "Entering room",
            "backtrack": "Dead end — backtracking",
            "start": "Starting room",
            "done": "Entire maze mapped."
        }
    },
    "merge_sort": {
        "scene": "leaderboard",
        "title": "Game Leaderboard Sorter",
        "hook": "You are sorting 1 million player scores for a global leaderboard.",
        "metaphors": {
            "node": "player score",
            "edge": "comparison",
            "weight": "score value",
            "visit": "Comparing scores",
            "merge": "Combining sorted groups",
            "start": "Unsorted leaderboard",
            "done": "Global leaderboard ready."
        }
    },
    "prims_mst": {
        "scene": "grid_power",
        "title": "Power Grid Planner",
        "hook": "Wire every town to the grid using the least cable possible.",
        "metaphors": {
            "node": "town",
            "edge": "cable run",
            "weight": "cable cost",
            "visit": "Connecting town",
            "start": "The first substation",
            "done": "Every town powered, minimum cable laid."
        }
    },
    "kruskals_mst": {
        "scene": "grid_power",
        "title": "Island Bridge Builder",
        "hook": "Cheapest bridges first — but never build one between islands already linked.",
        "metaphors": {
            "node": "island",
            "edge": "bridge",
            "weight": "build cost",
            "visit": "Inspecting a bridge",
            "start": "Every island alone",
            "done": "All islands joined for the minimum cost."
        }
    },
    "knapsack_01": {
        "scene": "vault",
        "title": "Cargo Hold Packing",
        "hook": "A limited hold, priceless cargo — every subproblem solved exactly once.",
        "metaphors": {
            "node": "cargo crate",
            "edge": "packing choice",
            "weight": "crate weight",
            "visit": "Weighing take vs skip",
            "start": "An empty hold",
            "done": "The manifest is optimal — guaranteed."
        }
    },
    "lcs": {
        "scene": "dna",
        "title": "Genome Alignment Lab",
        "hook": "Two DNA strands — find the longest sequence they share.",
        "metaphors": {
            "node": "base pair",
            "edge": "alignment",
            "weight": "match length",
            "visit": "Comparing bases",
            "start": "Two raw strands",
            "done": "The shared sequence is isolated."
        }
    },
    "two_sum_sorted": {
        "scene": "market",
        "title": "Supermarket Pairing",
        "hook": "Find two items that together hit the target price exactly.",
        "metaphors": {
            "node": "item",
            "edge": "pairing",
            "weight": "price",
            "visit": "Checking a pair",
            "start": "Cheapest and priciest items in hand",
            "done": "Pairing settled in one pass."
        }
    },
    "sliding_window": {
        "scene": "stocks",
        "title": "Best Sales Week",
        "hook": "Slide a fixed window over daily sales — never re-add what you already know.",
        "metaphors": {
            "node": "day",
            "edge": "streak",
            "weight": "revenue",
            "visit": "Sliding the window",
            "start": "The first k days",
            "done": "Best stretch found without recounting."
        }
    },
    "kadanes": {
        "scene": "stocks",
        "title": "Best Stock Run",
        "hook": "Find the most profitable streak — extend the run, or cut your losses.",
        "metaphors": {
            "node": "day",
            "edge": "streak",
            "weight": "gain/loss",
            "visit": "Extending the run",
            "start": "Day one",
            "done": "The best run is locked in."
        }
    },
    "bst_insert": {
        "scene": "files",
        "title": "Directory Tree Organizer",
        "hook": "Every file finds its folder — smaller names left, bigger right.",
        "metaphors": {
            "node": "folder",
            "edge": "subfolder link",
            "weight": "name order",
            "visit": "Comparing at folder",
            "start": "An empty drive",
            "done": "Every file filed — in-order walk reads alphabetically."
        }
    },
    "bst_search": {
        "scene": "files",
        "title": "File System Lookup",
        "hook": "Find one file among thousands — each folder halves the search.",
        "metaphors": {
            "node": "folder",
            "edge": "subfolder link",
            "weight": "name order",
            "visit": "Opening folder",
            "start": "Start at the root directory",
            "done": "Lookup complete."
        }
    },
    "heap_insert": {
        "scene": "scheduler",
        "title": "Hospital Triage Queue",
        "hook": "The most urgent patient is always seen first — the heap guarantees it.",
        "metaphors": {
            "node": "patient",
            "edge": "priority link",
            "weight": "urgency",
            "visit": "Checking urgency",
            "start": "An empty waiting room",
            "done": "Most urgent case on top, guaranteed."
        }
    },
    "bubble_sort": {
        "scene": "leaderboard",
        "title": "Bubble Tea Queue",
        "hook": "Heavy bubbles sink, light ones rise — one neighbour swap at a time.",
        "metaphors": {
            "node": "bubble",
            "edge": "comparison",
            "weight": "density",
            "visit": "Comparing neighbours",
            "start": "A fizzy, unsorted queue",
            "done": "Every bubble settled at its level."
        }
    },
    "insertion_sort": {
        "scene": "leaderboard",
        "title": "Sorting a Hand of Cards",
        "hook": "Pick up one card at a time and slide it into its place.",
        "metaphors": {
            "node": "card",
            "edge": "comparison",
            "weight": "face value",
            "visit": "Sliding a card",
            "start": "Cards dealt in random order",
            "done": "The whole hand reads in order."
        }
    },
    "selection_sort": {
        "scene": "leaderboard",
        "title": "Olympic Podium Selection",
        "hook": "Scan the field, crown the champion, repeat with whoever's left.",
        "metaphors": {
            "node": "athlete",
            "edge": "comparison",
            "weight": "score",
            "visit": "Scanning for the champion",
            "start": "The full unranked field",
            "done": "Every athlete on the right podium step."
        }
    },
    "linked_list_reverse": {
        "scene": "train",
        "title": "Train Yard Reversal",
        "hook": "Recouple every carriage so the train runs the other way.",
        "metaphors": {
            "node": "carriage",
            "edge": "coupling",
            "weight": "position",
            "visit": "Flipping a coupling",
            "start": "Engine at the front",
            "done": "The caboose leads — train reversed."
        }
    },
    "balanced_brackets": {
        "scene": "plates",
        "title": "Plate Stacking Inspector",
        "hook": "Every opened box must be closed in reverse order — the stack remembers.",
        "metaphors": {
            "node": "plate",
            "edge": "match",
            "weight": "depth",
            "visit": "Checking a symbol",
            "start": "An empty stack",
            "done": "Stack empty — everything matched."
        }
    },
    "quick_sort": {
        "scene": "leaderboard",
        "title": "Tournament Bracket Seeder",
        "hook": "You are a tournament seeder — pick a player, split the field around them.",
        "metaphors": {
            "node": "player score",
            "edge": "comparison",
            "weight": "score value",
            "visit": "Comparing against the pivot",
            "partition": "Splitting the field",
            "start": "Unseeded field",
            "done": "Every player seeded in order."
        }
    },
    "dynamic_programming": {
        "scene": "vault",
        "title": "Optimal Decision Vault",
        "hook": "You are a trading algorithm caching optimal decisions to avoid recalculating.",
        "metaphors": {
            "node": "subproblem",
            "edge": "dependency",
            "weight": "optimal value",
            "visit": "Computing subproblem",
            "memo": "Retrieving cached result",
            "start": "Base cases",
            "done": "Optimal solution found."
        }
    }
}

# 60 detections per minute — fast, lightweight endpoint
@router.post("")
@limiter.limit("60/minute")
def detect(request: Request, req: DetectRequest):
    text = (req.code + " " + req.problem).lower()
    scores = {}
    for algo, keywords in SIGNATURES.items():
        scores[algo] = sum(1 for kw in keywords if kw in text)
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        best = "dijkstra"
    meta = REALWORLD_META.get(best, REALWORLD_META["dijkstra"])
    return {
        "algorithm": best,
        "confidence": round(min(scores[best] / 3, 1.0), 2),
        "realworld": meta,
        # all_scores intentionally omitted
    }
