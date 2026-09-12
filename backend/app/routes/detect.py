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
    "topological_sort": ["topological_sort", "topological", "topo sort", "kahn", "in-degree", "indegree", "prerequisite", "course schedule", "dependency order"],
    "counting_sort": ["counting_sort", "counting sort", "countingsort", "bucket", "tally", "count array", "radix"],
    "prefix_sums": ["prefix_sums", "prefix sum", "prefix_sum", "cumulative sum", "running total", "range sum", "presum"],
    "next_greater_element": ["next_greater_element", "next greater", "monotonic stack", "monotonic", "stack of indices"],
    "edit_distance": ["edit_distance", "edit distance", "levenshtein", "spell check", "min edits", "insert delete substitute"],
    "floyd_cycle": ["floyd_cycle", "floyd", "tortoise", "hare", "cycle detect", "detect cycle", "slow fast", "linked list cycle", "has_cycle"],
    "tree_traversal": ["tree_traversal", "inorder", "preorder", "postorder", "in-order", "pre-order", "post-order", "traversal", "traverse tree"],
    "trie_insert": ["trie_insert", "trie", "prefix tree", "autocomplete", "children[", "startswith", "is_end"],
    "n_queens": ["n_queens", "n-queens", "queens", "backtracking", "chessboard", "is_safe", "place queen"],
    "unique_paths": ["unique_paths", "unique paths", "grid path", "robot grid", "count paths", "obstacle grid"],
    "sieve": ["sieve", "eratosthenes", "primes", "is_prime", "prime sieve", "composite"],
    "kmp_search": ["kmp", "kmp_search", "knuth", "morris", "pratt", "failure function", "lps", "substring search", "pattern match"],
    "segment_tree": ["segment_tree", "segment tree", "segtree", "range query", "range sum", "build(", "query(node"],
    "fenwick_tree": ["fenwick_tree", "fenwick", "binary indexed", "bit tree", "lowbit", "i & -i", "index tree"],
    "hash_table": ["hash_table", "hashtable", "hash map", "hashmap", "separate chaining", "load factor", "buckets", "def hash(", "% len(buckets)"],
    "bst_delete": ["bst_delete", "delete_node", "remove_node", "inorder successor", "in-order successor", "min_value_node", "two children"],
    "heap_extract": ["heap_extract", "extract_max", "extract_min", "heappop", "sift_down", "siftdown", "heapify_down", "percolate_down"],
    "dsu": ["disjoint_set", "disjoint set", "union_find", "union-find", "path compression", "union by rank", "parent[x] = find", "def union("],
    "merge_intervals": ["merge_intervals", "merge intervals", "overlapping intervals", "intervals.sort", "key=lambda x: x[0]"],
    "coin_change": ["coin_change", "coin change", "fewest coins", "min_coins", "mincoins", "dp[amount]"],
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
    },
    "topological_sort": {
        "scene": "scheduler",
        "title": "Course Prerequisite Planner",
        "hook": "You are building a timetable where every course must come after its prerequisites.",
        "metaphors": {
            "node": "course",
            "edge": "prerequisite",
            "weight": "dependency",
            "visit": "Scheduling course",
            "start": "Courses with no prerequisites",
            "done": "A valid study order exists."
        }
    },
    "counting_sort": {
        "scene": "leaderboard",
        "title": "Ballot Box Tally",
        "hook": "You are counting votes into numbered bins, then reading the bins back in order.",
        "metaphors": {
            "node": "ballot",
            "edge": "bin",
            "weight": "tally",
            "visit": "Dropping a vote into its bin",
            "start": "Empty bins",
            "done": "Every ballot counted and read back in order."
        }
    },
    "prefix_sums": {
        "scene": "stocks",
        "title": "Running Balance Ledger",
        "hook": "You are keeping a running balance so any period's total is one subtraction away.",
        "metaphors": {
            "node": "entry",
            "edge": "running total",
            "weight": "amount",
            "visit": "Adding to the running total",
            "start": "Opening balance of zero",
            "done": "Any range now answers instantly."
        }
    },
    "next_greater_element": {
        "scene": "plates",
        "title": "Queue of Unanswered Questions",
        "hook": "You are stacking people still waiting for someone taller to walk past.",
        "metaphors": {
            "node": "person",
            "edge": "sightline",
            "weight": "height",
            "visit": "Checking who is still waiting",
            "start": "Nobody waiting yet",
            "done": "Everyone who could be answered has been."
        }
    },
    "edit_distance": {
        "scene": "dna",
        "title": "Spell-Checker Alignment",
        "hook": "You are a spell-checker measuring how many keystrokes separate two words.",
        "metaphors": {
            "node": "character",
            "edge": "edit",
            "weight": "cost",
            "visit": "Comparing two characters",
            "start": "Two empty prefixes",
            "done": "Cheapest edit recipe recovered."
        }
    },
    "floyd_cycle": {
        "scene": "train",
        "title": "Runners on a Loop Track",
        "hook": "Two runners at different speeds — if the track loops, the fast one laps the slow one.",
        "metaphors": {
            "node": "carriage",
            "edge": "coupling",
            "weight": "step",
            "visit": "Advancing a runner",
            "start": "Both runners at the head",
            "done": "The loop's entrance is found."
        }
    },
    "tree_traversal": {
        "scene": "files",
        "title": "Walking the Directory Tree",
        "hook": "You are a file indexer visiting every folder — the order you read them in changes everything.",
        "metaphors": {
            "node": "folder",
            "edge": "subfolder link",
            "weight": "name",
            "visit": "Reading folder",
            "start": "The root folder",
            "done": "Every folder visited exactly once."
        }
    },
    "trie_insert": {
        "scene": "library",
        "title": "Autocomplete Dictionary",
        "hook": "You are a search box storing words so every shared prefix is written down only once.",
        "metaphors": {
            "node": "letter",
            "edge": "next letter",
            "weight": "branch",
            "visit": "Following a letter",
            "start": "The empty prefix",
            "done": "Every word stored, prefixes shared."
        }
    },
    "n_queens": {
        "scene": "maze",
        "title": "The Chessboard Puzzle",
        "hook": "You are placing queens one row at a time, undoing your last move whenever you hit a dead end.",
        "metaphors": {
            "node": "square",
            "edge": "line of attack",
            "weight": "conflict",
            "visit": "Trying a square",
            "backtrack": "Taking the queen back off",
            "start": "An empty board",
            "done": "A board where no queen attacks another."
        }
    },
    "unique_paths": {
        "scene": "grid_power",
        "title": "Robot on a Warehouse Floor",
        "hook": "A robot may only move right or down — count the routes to the far corner without listing them.",
        "metaphors": {
            "node": "floor tile",
            "edge": "move",
            "weight": "routes to here",
            "visit": "Counting routes into a tile",
            "start": "The loading dock",
            "done": "Every route counted."
        }
    },
    "sieve": {
        "scene": "vault",
        "title": "The Prime Filter",
        "hook": "You are striking out every multiple until only the primes are left standing.",
        "metaphors": {
            "node": "number",
            "edge": "multiple",
            "weight": "factor",
            "visit": "Crossing out a multiple",
            "start": "Every number a candidate",
            "done": "Only primes remain."
        }
    },
    "kmp_search": {
        "scene": "dna",
        "title": "Genome Pattern Scanner",
        "hook": "You are scanning a long strand for a motif without ever re-reading a character.",
        "metaphors": {
            "node": "character",
            "edge": "alignment",
            "weight": "match length",
            "visit": "Comparing a character",
            "start": "The start of the strand",
            "done": "Every occurrence located in one pass."
        }
    },
    "segment_tree": {
        "scene": "grid_power",
        "title": "Regional Power Monitor",
        "hook": "Each node reports the total for its whole region, so a query reads a few summaries instead of every meter.",
        "metaphors": {
            "node": "region",
            "edge": "subdivision",
            "weight": "regional total",
            "visit": "Reading a region's total",
            "start": "The whole grid",
            "done": "Range total assembled from a few blocks."
        }
    },
    "fenwick_tree": {
        "scene": "stocks",
        "title": "Ledger with Live Corrections",
        "hook": "Running totals that stay cheap to update when yesterday's number changes.",
        "metaphors": {
            "node": "slot",
            "edge": "responsibility",
            "weight": "partial sum",
            "visit": "Folding a value into a slot",
            "start": "An empty ledger",
            "done": "Prefix total read from a handful of slots."
        }
    },
    "hash_table": {
        "scene": "library",
        "title": "Coat Check",
        "hook": "Your ticket number tells the attendant exactly which rail to walk to — until two coats get the same number.",
        "metaphors": {
            "node": "rail",
            "edge": "hook",
            "weight": "chain length",
            "visit": "Walking a rail",
            "start": "An empty cloakroom",
            "done": "Every coat on the rail its ticket names."
        }
    },
    "bst_delete": {
        "scene": "files",
        "title": "Filing Cabinet Reshuffle",
        "hook": "Pull one folder out and something has to fill the gap — and only one folder keeps the drawer in order.",
        "metaphors": {
            "node": "folder",
            "edge": "divider",
            "weight": "label",
            "visit": "Checking a folder",
            "start": "The drawer front",
            "done": "Gap filled, order intact."
        }
    },
    "heap_extract": {
        "scene": "scheduler",
        "title": "Triage Queue",
        "hook": "The most urgent patient is always at the front — take them and the queue has to re-settle around whoever is left.",
        "metaphors": {
            "node": "patient",
            "edge": "priority link",
            "weight": "urgency",
            "visit": "Comparing urgency",
            "start": "The most urgent case",
            "done": "Everyone seen, worst first."
        }
    },
    "dsu": {
        "scene": "social",
        "title": "Friend Circles",
        "hook": "Introduce two people and their whole circles merge — asking whether two people already share a circle has to be instant.",
        "metaphors": {
            "node": "person",
            "edge": "introduction",
            "weight": "circle size",
            "visit": "Finding someone's circle",
            "start": "Everyone a stranger",
            "done": "Circles settled."
        }
    },
    "merge_intervals": {
        "scene": "scheduler",
        "title": "Calendar Merge",
        "hook": "Overlapping meetings collapse into one block — but only if you read the day in order.",
        "metaphors": {
            "node": "booking",
            "edge": "overlap",
            "weight": "duration",
            "visit": "Checking a booking",
            "start": "The first booking of the day",
            "done": "The day reduced to its real busy blocks."
        }
    },
    "coin_change": {
        "scene": "vault",
        "title": "Cash Drawer",
        "hook": "Grabbing the biggest note first feels right and is sometimes wrong — the table checks every option so you don't have to.",
        "metaphors": {
            "node": "amount",
            "edge": "coin spent",
            "weight": "coins used",
            "visit": "Pricing an amount",
            "start": "Owing nothing",
            "done": "Fewest coins found."
        }
    }
}

# 60 detections per minute — fast, lightweight endpoint
@router.post("")
@limiter.limit("60/minute")
def detect(request: Request, req: DetectRequest):
    text = (req.code + " " + req.problem).lower()

    # An exact algorithm id always wins. Callers are documented to pass an id
    # as `problem` to fetch its real-world meta, and fuzzy scoring got that
    # wrong whenever a newer algorithm tied with an older one: ties fall back
    # to dict order, so 'bst_delete' resolved to bst_insert, 'dsu' to
    # kruskals_mst and 'merge_intervals' to greedy.
    probe = req.problem.strip().lower()
    if probe in SIGNATURES:
        return {
            "algorithm": probe,
            "confidence": 1.0,
            "realworld": REALWORLD_META.get(probe, REALWORLD_META["dijkstra"]),
        }

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
