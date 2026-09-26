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
    "huffman": ["huffman", "huffman coding", "prefix code", "prefix-free", "greedy encoding", "compression", "variable length code", "heapq.heappush"],
    "activity_selection": ["activity_selection", "activity selection", "n meetings", "n-meetings", "meetings in one room", "maximum meetings", "interval scheduling", "sort by finish", "earliest finish"],
    "fractional_knapsack": ["fractional_knapsack", "fractional knapsack", "value per weight", "value/weight", "greedy knapsack", "take a fraction", "ratio sort"],
    "count_set_bits": ["count_set_bits", "count set bits", "hamming weight", "popcount", "number of 1 bits", "brian kernighan", "n & (n-1)"],
    "power_of_two": ["power_of_two", "power of two", "power of 2", "is power of two", "single set bit"],
    "single_number": ["single_number", "single number", "appears once", "xor all", "unpaired number", "x ^ x"],
    "min_bit_flips": ["min_bit_flips", "minimum bit flips", "bit flips to convert", "hamming distance", "differing bits"],
    "power_set": ["power_set", "power set", "all subsets", "subsets bitmask", "generate subsets", "1 << n"],
    "min_heap": ["min_heap", "min heap", "min-heap", "priority queue", "sift up", "bubble up", "heapify min"],
    "kth_largest": ["kth_largest", "kth largest", "k-th largest", "top k largest", "size-k min-heap"],
    "kth_smallest": ["kth_smallest", "kth smallest", "k-th smallest", "size-k max-heap"],
    "longest_substring_no_repeat": ["longest_substring_no_repeat", "longest substring without repeating", "no repeating characters", "unique window"],
    "max_consecutive_ones_iii": ["max_consecutive_ones_iii", "max consecutive ones", "flip k zeros", "at most k zeros"],
    "longest_k_distinct": ["longest_k_distinct", "at most k distinct", "k distinct characters", "fruit into baskets"],
    "jump_game": ["jump_game", "jump game", "can jump", "reach last index", "farthest reach", "max reach"],
    "jump_game_ii": ["jump_game_ii", "jump game ii", "jump game 2", "minimum jumps", "min jumps", "fewest jumps"],
    "candy": ["candy", "candies", "distribute candy", "ratings neighbour", "two pass candy"],
    "lemonade_change": ["lemonade_change", "lemonade change", "lemonade stand", "give change", "five ten twenty"],
    "assign_cookies": ["assign_cookies", "assign cookies", "greed factor", "content children", "cookie size"],
    "min_platforms": ["min_platforms", "minimum platforms", "railway platforms", "arrival departure", "train platform", "overlapping trains"],
    "job_sequencing": ["job_sequencing", "job sequencing", "deadline", "job scheduling", "maximize profit", "sequence jobs", "profit deadline"],
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
    "connected_components": ["connected_components", "connected component", "count components", "number of components", "count islands", "islands", "island count", "reachable set"],
    "bipartite_check": ["bipartite_check", "bipartite", "two color", "two colour", "2-color", "2-colour", "graph coloring", "graph colouring", "odd cycle", "two teams"],
    "flood_fill": ["flood_fill", "flood fill", "paint bucket", "paint fill", "fill region", "num islands", "number of islands", "4-directional", "grid fill", "bucket fill"],
    "house_robber": ["house_robber", "house robber", "rob houses", "adjacent houses", "non-adjacent", "rob(", "maximum loot", "cannot rob two"],
    "lis": ["lis", "longest increasing subsequence", "increasing subsequence", "longest increasing", "length of lis", "patience sorting"],
    "subset_sum": ["subset_sum", "subset sum", "partition equal", "target sum", "can partition", "sum to target", "dp[i][s]", "achievable sum"],
    "z_function": ["z_function", "z function", "z-function", "z array", "z algorithm", "z-algorithm", "prefix match"],
    "rabin_karp": ["rabin_karp", "rabin karp", "rabin-karp", "rolling hash", "polynomial hash", "fingerprint", "string hash"],
    "manacher": ["manacher", "manachers", "longest palindrome", "longest palindromic", "palindromic substring", "palindrome substring"],
    "radix_sort": ["radix_sort", "radix sort", "radixsort", "lsd", "digit sort", "bucket by digit"],
    "sliding_window_maximum": ["sliding_window_maximum", "sliding window maximum", "window maximum", "max in window", "monotonic deque", "deque maximum"],
    "matrix_chain": ["matrix_chain", "matrix chain", "matrix-chain", "chain multiplication", "parenthesization", "parenthesisation", "optimal parenthes"],
    "heap_sort": ["heap_sort", "heap sort", "heapsort", "in-place heap", "sift down sort", "build heap sort"],
    "find_middle": ["find_middle", "find middle", "middle of list", "middle node", "slow fast pointer", "slow and fast", "tortoise middle"],
    "merge_two_sorted_lists": ["merge_two_sorted_lists", "merge two sorted", "merge sorted lists", "merge two lists", "merge linked lists", "splice sorted"],
    "anagram": ["anagram", "anagrams", "rearrange letters", "same letters", "permutation of", "sorted letters match"],
    "gcd_euclid": ["gcd_euclid", "gcd", "greatest common divisor", "euclid", "euclidean", "hcf", "common divisor"],
    "fast_exponentiation": ["fast_exponentiation", "fast exponentiation", "binary exponentiation", "exponentiation by squaring", "fast power", "pow(", "modular exponent"],
    "prime_factorisation": ["prime_factorisation", "prime factorization", "prime factorisation", "prime factors", "factorize", "factorise", "trial division"],
    "bellman_ford": ["bellman_ford", "bellman ford", "bellman-ford", "negative weight", "negative edge", "negative cycle", "relax edges", "shortest path negative"],
    "level_order": ["level_order", "level order", "level-order", "breadth first tree", "bfs tree", "level by level", "queue traversal", "zigzag level"],
    "tree_max_depth": ["tree_max_depth", "maximum depth", "max depth", "height of tree", "tree height", "depth of binary tree", "deepest leaf"],
    "tree_diameter": ["tree_diameter", "diameter of binary tree", "diameter of tree", "longest path tree", "longest path between two nodes", "tree diameter"],
    "lca_bt": ["lca_bt", "lowest common ancestor", "lca", "common ancestor", "lca in bt", "split point ancestor"],
    "frog_jump": ["frog_jump", "frog jump", "frog leap", "minimum energy", "stones jump", "climbing stairs cost", "min cost stairs", "1d dp"],
    "buy_sell_stock": ["buy_sell_stock", "buy and sell stock", "best time to buy", "stock profit", "max profit", "buy low sell high", "one transaction"],
    "coin_change_2": ["coin_change_2", "coin change 2", "coin change ii", "number of ways coins", "count combinations coins", "ways to make amount", "combination sum coins"],
    "longest_common_substring": ["longest_common_substring", "longest common substring", "common substring", "contiguous common", "longest shared block"],
    "search_rotated": ["search_rotated", "rotated sorted array", "search in rotated", "pivoted array", "rotated binary search"],
    "dutch_flag": ["dutch_flag", "dutch national flag", "sort colors", "sort 0s 1s 2s", "sort zeros ones twos", "three way partition"],
    "majority_element": ["majority_element", "majority element", "boyer moore", "boyer-moore", "moore voting", "more than n/2", "appears more than half"],
    "next_permutation": ["next_permutation", "next permutation", "next larger arrangement", "next lexicographic", "rearrange next greater"],
    "stock_span": ["stock_span", "stock span", "span of stock", "consecutive days price", "previous greater element", "online stock span"],
    "largest_rectangle": ["largest_rectangle", "largest rectangle", "histogram", "maximum rectangle area", "largest area histogram"],
    "rat_in_maze": ["rat_in_maze", "rat in a maze", "rat in maze", "all paths maze", "maze paths", "escape routes"],
    "word_search": ["word_search", "word search", "word in grid", "word exists grid", "letters grid backtracking"],
    "trapping_rainwater": ["trapping_rainwater", "trapping rain water", "trapping rainwater", "trap rain", "water trapped between bars"],
    "asteroid_collision": ["asteroid_collision", "asteroid collision", "asteroids collide", "colliding asteroids"],
    "find_min_rotated": ["find_min_rotated", "minimum in rotated", "min rotated sorted", "how many times rotated", "rotation count", "find rotation"],
    "find_peak": ["find_peak", "peak element", "find peak", "local maximum", "bigger than neighbours", "bigger than neighbors"],
    "dll_reverse": ["dll_reverse", "reverse a doubly linked list", "reverse doubly linked", "reverse dll"],
    "dll_delete_key": ["dll_delete_key", "delete all occurrences", "delete key doubly linked", "remove key from dll", "delete occurrences of a key"],
    "remove_nth_from_end": ["remove_nth_from_end", "remove nth node", "nth node from the end", "nth from end", "delete nth from back"],
    "longest_complete_word": ["longest_complete_word", "complete string", "longest word with all prefixes", "all prefixes present", "longest word in dictionary"],
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
    "count_set_bits": {
        "scene": "vault",
        "title": "Bit Counter",
        "hook": "You are counting the 1s in a binary number, clearing the lowest one each step.",
        "metaphors": {"node": "bit", "edge": "position", "weight": "value",
                      "visit": "Clearing the lowest set bit", "start": "The full number",
                      "done": "All set bits counted."}
    },
    "power_of_two": {
        "scene": "vault",
        "title": "Power-of-Two Detector",
        "hook": "You are checking whether a number is a clean power of two — a single 1 in binary.",
        "metaphors": {"node": "bit", "edge": "position", "weight": "value",
                      "visit": "Testing n & (n-1)", "start": "The number in binary",
                      "done": "One set bit means yes."}
    },
    "single_number": {
        "scene": "vault",
        "title": "The Lone Number",
        "hook": "You are XOR-folding a list so every duplicate cancels and the unique value remains.",
        "metaphors": {"node": "bit", "edge": "position", "weight": "parity",
                      "visit": "XOR-ing in the next value", "start": "Zero",
                      "done": "The survivor is the single number."}
    },
    "min_bit_flips": {
        "scene": "vault",
        "title": "Bit-Flip Distance",
        "hook": "You are finding how many bits must flip to turn A into B — the differing positions.",
        "metaphors": {"node": "bit", "edge": "position", "weight": "difference",
                      "visit": "Marking a differing bit", "start": "A and B",
                      "done": "Set bits of A XOR B = flips needed."}
    },
    "power_set": {
        "scene": "vault",
        "title": "Subset Enumerator",
        "hook": "You are listing every subset by treating each as a binary on/off mask.",
        "metaphors": {"node": "element", "edge": "mask bit", "weight": "chosen",
                      "visit": "Reading a mask", "start": "The empty set",
                      "done": "All 2ⁿ subsets listed."}
    },
    "min_heap": {
        "scene": "scheduler",
        "title": "Priority Queue (Min-First)",
        "hook": "You are a priority queue that always keeps the smallest item ready at the top.",
        "metaphors": {"node": "item", "edge": "parent link", "weight": "priority",
                      "visit": "Bubbling a value up", "start": "An empty heap",
                      "done": "A valid min-heap — smallest at the root."}
    },
    "kth_largest": {
        "scene": "scheduler",
        "title": "Top-K Leaderboard",
        "hook": "You are keeping only the top k scores as results stream in.",
        "metaphors": {"node": "score", "edge": "parent link", "weight": "value",
                      "visit": "Comparing against the weakest kept", "start": "An empty shortlist",
                      "done": "The kth largest sits at the heap root."}
    },
    "kth_smallest": {
        "scene": "scheduler",
        "title": "Bottom-K Shortlist",
        "hook": "You are keeping only the smallest k values as results stream in.",
        "metaphors": {"node": "value", "edge": "parent link", "weight": "value",
                      "visit": "Comparing against the largest kept", "start": "An empty shortlist",
                      "done": "The kth smallest sits at the heap root."}
    },
    "longest_substring_no_repeat": {
        "scene": "stocks",
        "title": "Sliding Window Scanner",
        "hook": "You are dragging a window across text, growing it while every character stays unique.",
        "metaphors": {"node": "character", "edge": "window", "weight": "position",
                      "visit": "Extending the right edge", "start": "An empty window",
                      "done": "The longest run of unique characters."}
    },
    "max_consecutive_ones_iii": {
        "scene": "stocks",
        "title": "Flip-k-Zeros Window",
        "hook": "You are finding the longest run of 1s you can make by flipping up to k zeros.",
        "metaphors": {"node": "bit", "edge": "window", "weight": "position",
                      "visit": "Extending the window", "start": "An empty window",
                      "done": "The widest window with at most k zeros."}
    },
    "longest_k_distinct": {
        "scene": "market",
        "title": "K-Basket Fruit Picker",
        "hook": "You are collecting the longest run of items using at most K basket types.",
        "metaphors": {"node": "item", "edge": "window", "weight": "position",
                      "visit": "Extending the window", "start": "An empty window",
                      "done": "The widest window with at most K distinct items."}
    },
    "jump_game": {
        "scene": "maze",
        "title": "Stepping-Stone Crossing",
        "hook": "You are hopping across stepping stones, each marked with how far you may leap, trying to reach the far bank.",
        "metaphors": {"node": "stone", "edge": "leap", "weight": "max jump",
                      "visit": "Standing on a stone", "start": "The near bank",
                      "done": "The far bank is reachable (or not)."}
    },
    "jump_game_ii": {
        "scene": "maze",
        "title": "Fewest Leaps Across",
        "hook": "You are crossing the same stepping stones in as few leaps as possible.",
        "metaphors": {"node": "stone", "edge": "leap", "weight": "max jump",
                      "visit": "Scanning the current leap's range", "start": "The near bank",
                      "done": "Reached the far bank in the fewest leaps."}
    },
    "candy": {
        "scene": "market",
        "title": "Candy Distribution",
        "hook": "You are handing out sweets so every child with a higher rating than a neighbour gets more.",
        "metaphors": {"node": "child", "edge": "neighbour", "weight": "rating",
                      "visit": "Adjusting a child's candy", "start": "One each",
                      "done": "Fewest candies that keep every neighbour happy."}
    },
    "lemonade_change": {
        "scene": "market",
        "title": "Lemonade Stand Till",
        "hook": "You are running a lemonade stand, giving each customer correct change from the notes you already hold.",
        "metaphors": {"node": "customer", "edge": "payment", "weight": "note",
                      "visit": "Serving a customer", "start": "An empty till",
                      "done": "Everyone served, or change ran out."}
    },
    "assign_cookies": {
        "scene": "market",
        "title": "Cookie Sharing",
        "hook": "You are handing cookies to children so as many as possible get one big enough for them.",
        "metaphors": {"node": "child", "edge": "cookie", "weight": "size vs greed",
                      "visit": "Offering a cookie", "start": "Sorted children and cookies",
                      "done": "The most children made content."}
    },
    "min_platforms": {
        "scene": "scheduler",
        "title": "Station Platform Planner",
        "hook": "You are working out how many platforms a station needs so no two overlapping trains wait for one.",
        "metaphors": {"node": "train", "edge": "overlap", "weight": "time",
                      "visit": "An arrival or departure", "start": "An empty station",
                      "done": "The peak number of trains present at once."}
    },
    "fractional_knapsack": {
        "scene": "market",
        "title": "Market Stall Loot",
        "hook": "You are filling a bag of fixed capacity with the most valuable goods, and you may take a slice of any item.",
        "metaphors": {
            "node": "item",
            "edge": "choice",
            "weight": "value per unit weight",
            "visit": "Taking the best ratio next",
            "start": "An empty bag",
            "done": "The bag is full and worth the most it can be."
        }
    },
    "job_sequencing": {
        "scene": "scheduler",
        "title": "Deadline Job Board",
        "hook": "You are picking which paid jobs to run before their deadlines to earn the most.",
        "metaphors": {
            "node": "job",
            "edge": "slot",
            "weight": "profit",
            "visit": "Placing the richest job",
            "start": "An empty schedule",
            "done": "The most profitable set of jobs that meet their deadlines."
        }
    },
    "activity_selection": {
        "scene": "scheduler",
        "title": "Meeting Room Scheduler",
        "hook": "You are booking one meeting room to fit as many meetings as possible in a day.",
        "metaphors": {
            "node": "meeting",
            "edge": "overlap",
            "weight": "finish time",
            "visit": "Considering a meeting",
            "start": "An empty calendar",
            "done": "The most meetings that fit in one room."
        }
    },
    "huffman": {
        "scene": "files",
        "title": "File Compressor (ZIP)",
        "hook": "You are a compressor giving the commonest characters the shortest codes so the packed file is as small as possible.",
        "metaphors": {
            "node": "symbol",
            "edge": "bit (0 = left, 1 = right)",
            "weight": "frequency",
            "visit": "Merging the two rarest",
            "start": "Every character on its own",
            "done": "One tree — every character has a prefix-free code."
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
    },
    "connected_components": {
        "scene": "social",
        "title": "Friend Circles — Who Knows Whom",
        "hook": "Start with one person and sweep outward — everyone you can reach is one circle; the next stranger opens another.",
        "metaphors": {
            "node": "person",
            "edge": "friendship",
            "weight": "—",
            "visit": "Pulling someone into this circle",
            "start": "The first person, alone",
            "done": "Every separate circle counted."
        }
    },
    "bipartite_check": {
        "scene": "social",
        "title": "Split Into Two Teams",
        "hook": "Can everyone be split into two teams so every rivalry crosses between the teams and never sits inside one?",
        "metaphors": {
            "node": "player",
            "edge": "rivalry",
            "weight": "—",
            "visit": "Assigning a team",
            "start": "The first player on team A",
            "done": "Two clean teams — or a rivalry that can't be split."
        }
    },
    "flood_fill": {
        "scene": "grid_power",
        "title": "Paint Bucket Fill",
        "hook": "Click one tile and the colour floods outward to every tile it can reach without crossing a wall.",
        "metaphors": {
            "node": "tile",
            "edge": "shared border",
            "weight": "—",
            "visit": "Painting a tile",
            "start": "Where the bucket was dropped",
            "done": "The whole reachable region is one colour."
        }
    },
    "house_robber": {
        "scene": "vault",
        "title": "The Burglar's Street",
        "hook": "Loot a street of houses for the biggest haul — but hit two houses next door and the alarms connect.",
        "metaphors": {
            "node": "house",
            "edge": "adjacency",
            "weight": "loot",
            "visit": "Deciding rob vs skip",
            "start": "An empty sack at the first house",
            "done": "The biggest legal haul, with no two houses adjacent."
        }
    },
    "lis": {
        "scene": "stocks",
        "title": "Longest Winning Streak",
        "hook": "Pick the longest run of ever-rising numbers — skips allowed, but the order has to hold.",
        "metaphors": {
            "node": "day",
            "edge": "extension",
            "weight": "length",
            "visit": "Extending a run",
            "start": "Every day a run of one",
            "done": "The longest strictly rising subsequence found."
        }
    },
    "subset_sum": {
        "scene": "vault",
        "title": "Exact Change",
        "hook": "Can any handful of these numbers add up to exactly the target — without trying all 2^n handfuls?",
        "metaphors": {
            "node": "sum",
            "edge": "number used",
            "weight": "reachable",
            "visit": "Marking a sum reachable",
            "start": "Only zero is reachable",
            "done": "The target is proved reachable — or proved impossible."
        }
    },
    "z_function": {
        "scene": "dna",
        "title": "Where the Strand Repeats Itself",
        "hook": "At each position, how much of the strand's own opening sequence starts again right here?",
        "metaphors": {
            "node": "base",
            "edge": "match",
            "weight": "match length",
            "visit": "Measuring the prefix match",
            "start": "The start of the strand",
            "done": "Every position scored in one linear pass."
        }
    },
    "rabin_karp": {
        "scene": "dna",
        "title": "Fingerprint Scan",
        "hook": "Fingerprint every window of the strand and compare fingerprints — read the bases only when two match.",
        "metaphors": {
            "node": "base",
            "edge": "window",
            "weight": "hash",
            "visit": "Rolling the fingerprint forward",
            "start": "The first window fingerprinted",
            "done": "Every occurrence located, most windows never read."
        }
    },
    "manacher": {
        "scene": "dna",
        "title": "The Longest Mirror Sequence",
        "hook": "Find the longest stretch that reads the same both ways — reusing earlier mirrors instead of re-checking.",
        "metaphors": {
            "node": "base",
            "edge": "mirror",
            "weight": "radius",
            "visit": "Growing a palindrome around a centre",
            "start": "Every centre a palindrome of one",
            "done": "The longest palindrome found in linear time."
        }
    },
    "radix_sort": {
        "scene": "leaderboard",
        "title": "Sorting by Digit",
        "hook": "Sort whole numbers without ever comparing two — one stable pass per digit, least significant first.",
        "metaphors": {
            "node": "number",
            "edge": "bin",
            "weight": "digit",
            "visit": "Dropping a number in its digit bin",
            "start": "Unsorted numbers",
            "done": "Sorted after one pass per digit — no comparisons."
        }
    },
    "sliding_window_maximum": {
        "scene": "stocks",
        "title": "Best in Every Window",
        "hook": "The maximum of every window, tracked with a deque so no value is ever looked at twice.",
        "metaphors": {
            "node": "day",
            "edge": "window",
            "weight": "value",
            "visit": "Sliding the window forward",
            "start": "The first window",
            "done": "Every window's maximum in one linear pass."
        }
    },
    "matrix_chain": {
        "scene": "vault",
        "title": "Where to Parenthesise",
        "hook": "Multiply a chain of matrices in the cheapest order — the grid prices every split so you don't have to guess.",
        "metaphors": {
            "node": "sub-chain",
            "edge": "split",
            "weight": "multiplications",
            "visit": "Pricing a split",
            "start": "Single matrices cost nothing",
            "done": "The cheapest parenthesisation of the whole chain."
        }
    },
    "heap_sort": {
        "scene": "leaderboard",
        "title": "Podium, Cleared One at a Time",
        "hook": "Build a heap so the champion is on top, swap them to the end, and re-settle — the sorted list grows from the back.",
        "metaphors": {
            "node": "contender",
            "edge": "comparison",
            "weight": "score",
            "visit": "Sifting a value down",
            "start": "An unordered field",
            "done": "Sorted in place, no extra memory."
        }
    },
    "find_middle": {
        "scene": "train",
        "title": "Two Runners on the Track",
        "hook": "One runner takes two steps for every one the other takes — when the fast one hits the end, the slow one is at the middle.",
        "metaphors": {
            "node": "carriage",
            "edge": "coupling",
            "weight": "position",
            "visit": "Advancing the runners",
            "start": "Both at the head",
            "done": "Slow runner stops on the middle node."
        }
    },
    "merge_two_sorted_lists": {
        "scene": "train",
        "title": "Coupling Two Trains",
        "hook": "Two sorted trains become one — always couple on whichever front carriage is smaller, re-pointing rather than copying.",
        "metaphors": {
            "node": "carriage",
            "edge": "coupling",
            "weight": "value",
            "visit": "Splicing the smaller head",
            "start": "Two separate sorted trains",
            "done": "One sorted train, built by re-pointing alone."
        }
    },
    "anagram": {
        "scene": "dna",
        "title": "Same Letters, Shuffled",
        "hook": "Two words are anagrams when they are built from exactly the same letters — sort both and they line up.",
        "metaphors": {
            "node": "letter",
            "edge": "match",
            "weight": "position",
            "visit": "Comparing sorted letters",
            "start": "Two words in their own order",
            "done": "Same multiset of letters — or a mismatch that proves not."
        }
    },
    "gcd_euclid": {
        "scene": "vault",
        "title": "Shrinking to the Common Divisor",
        "hook": "Replace the pair with (smaller, remainder) over and over — the numbers collapse to their greatest common divisor.",
        "metaphors": {
            "node": "pair",
            "edge": "remainder step",
            "weight": "value",
            "visit": "Taking a remainder",
            "start": "The original two numbers",
            "done": "Remainder hits 0 — the other number is the gcd."
        }
    },
    "fast_exponentiation": {
        "scene": "vault",
        "title": "Powers by Squaring",
        "hook": "Read the exponent in binary — square each step, multiply in the base on a 1-bit — and reach the full power in log steps.",
        "metaphors": {
            "node": "bit",
            "edge": "square",
            "weight": "running result",
            "visit": "Squaring (and maybe multiplying)",
            "start": "Result of 1",
            "done": "The full power in log(exp) multiplications."
        }
    },
    "prime_factorisation": {
        "scene": "vault",
        "title": "Breaking a Number into Primes",
        "hook": "Divide out the smallest prime as often as it goes, then the next — what's left above 1 past the square root is prime.",
        "metaphors": {
            "node": "factor",
            "edge": "division",
            "weight": "remaining",
            "visit": "Pulling out a prime",
            "start": "The whole number",
            "done": "A product of primes, nothing left to factor."
        }
    },
    "bellman_ford": {
        "scene": "gps",
        "title": "Routing with Tolls and Rebates",
        "hook": "Some one-way roads charge you, some pay you back — find the cheapest route, and know when a money-making loop makes 'cheapest' meaningless.",
        "metaphors": {
            "node": "junction",
            "edge": "one-way road",
            "weight": "toll (can be negative)",
            "visit": "Relaxing a road",
            "start": "Your starting junction",
            "done": "Cheapest routes found — or a negative loop exposed."
        }
    },
    "level_order": {
        "scene": "files",
        "title": "Reading a Tree, Floor by Floor",
        "hook": "You are reading an org chart top to bottom — everyone on one level before anyone below, using a queue to hold the next row.",
        "metaphors": {
            "node": "person",
            "edge": "reports-to",
            "weight": "level",
            "visit": "Reading a person",
            "enqueue": "Line up their reports for the next row",
            "start": "The person at the top",
            "done": "Every level read in order, top to bottom."
        }
    },
    "tree_max_depth": {
        "scene": "files",
        "title": "How Deep Does It Go?",
        "hook": "You are measuring the deepest nested folder — a folder's depth is one more than its deepest child.",
        "metaphors": {
            "node": "folder",
            "edge": "subfolder link",
            "weight": "depth",
            "visit": "Measuring a folder",
            "start": "The deepest leaves first",
            "done": "The longest root-to-leaf chain, counted once."
        }
    },
    "tree_diameter": {
        "scene": "social",
        "title": "The Longest Chain of Friends",
        "hook": "You are finding the two people furthest apart in a family tree — the longest path may not even pass through the root.",
        "metaphors": {
            "node": "person",
            "edge": "relation",
            "weight": "path length",
            "visit": "Checking the path bending here",
            "start": "The leaves",
            "done": "The two furthest-apart nodes found in one pass."
        }
    },
    "lca_bt": {
        "scene": "files",
        "title": "The Nearest Shared Boss",
        "hook": "You are finding the lowest manager both employees report up to — the deepest node with both of them beneath it.",
        "metaphors": {
            "node": "person",
            "edge": "reports-to",
            "weight": "depth",
            "visit": "Asking a subtree if a target is inside",
            "start": "The person at the top",
            "done": "The split point — the lowest common ancestor."
        }
    },
    "frog_jump": {
        "scene": "maze",
        "title": "The Frog and the Stones",
        "hook": "A frog crosses a row of stones, hopping one or two at a time and paying the height difference — find the cheapest crossing.",
        "metaphors": {
            "node": "stone",
            "edge": "hop",
            "weight": "energy",
            "visit": "Pricing the cheapest way here",
            "start": "The first stone, free",
            "done": "The least-energy crossing, each stone solved once."
        }
    },
    "buy_sell_stock": {
        "scene": "stocks",
        "title": "One Buy, One Sell",
        "hook": "You are a trader with a single buy and a single sell — track the lowest price seen and the best profit against it, in one pass.",
        "metaphors": {
            "node": "day",
            "edge": "hold",
            "weight": "price",
            "visit": "Selling today against the low",
            "start": "Day one — the first low",
            "done": "The most profitable single trade."
        }
    },
    "coin_change_2": {
        "scene": "vault",
        "title": "Counting Every Way to Pay",
        "hook": "Not the fewest coins — the number of *distinct* combinations that make the amount, counted coin by coin so nothing is double-counted.",
        "metaphors": {
            "node": "amount",
            "edge": "coin added",
            "weight": "ways",
            "visit": "Adding the ways with and without this coin",
            "start": "One way to make nothing",
            "done": "Every distinct combination counted."
        }
    },
    "longest_common_substring": {
        "scene": "dna",
        "title": "The Longest Shared Run",
        "hook": "Two strands — find the longest *unbroken* stretch they share. A single mismatch breaks the run back to zero.",
        "metaphors": {
            "node": "base",
            "edge": "diagonal run",
            "weight": "run length",
            "visit": "Extending or resetting the run",
            "start": "Two raw strands",
            "done": "The longest contiguous shared block."
        }
    },
    "search_rotated": {
        "scene": "library",
        "title": "Search a Shelf That Was Rotated",
        "hook": "The catalog was cut and swapped at one point, so it isn't globally sorted — but one half around any midpoint always is. Search that half.",
        "metaphors": {
            "node": "book",
            "edge": "shelf order",
            "weight": "call number",
            "visit": "Checking the middle book",
            "start": "The whole rotated shelf",
            "done": "Found in log n, or proven absent."
        }
    },
    "dutch_flag": {
        "scene": "leaderboard",
        "title": "Sort the Flags in One Pass",
        "hook": "Three colours, three pointers — sweep once, swapping each item down to the reds or up to the blues, no counting.",
        "metaphors": {
            "node": "tile",
            "edge": "swap",
            "weight": "colour",
            "visit": "Placing the middle tile",
            "start": "A jumble of 0s, 1s and 2s",
            "done": "All 0s, then 1s, then 2s — sorted in place."
        }
    },
    "majority_element": {
        "scene": "social",
        "title": "The Vote That Can't Be Cancelled",
        "hook": "One candidate, one tally: matching votes add, opposing votes cancel. A true majority outnumbers everyone else combined, so it always survives.",
        "metaphors": {
            "node": "vote",
            "edge": "tally",
            "weight": "count",
            "visit": "Casting a vote for or against",
            "start": "No candidate yet",
            "done": "The survivor, verified as the majority."
        }
    },
    "next_permutation": {
        "scene": "leaderboard",
        "title": "The Next Arrangement Up",
        "hook": "Find the smallest rearrangement larger than this one: spot the rightmost dip, bump it with the smallest bigger value in the tail, then reverse the tail.",
        "metaphors": {
            "node": "position",
            "edge": "swap",
            "weight": "value",
            "visit": "Inspecting a position",
            "start": "The current arrangement",
            "done": "The very next permutation, in place."
        }
    },
    "stock_span": {
        "scene": "stocks",
        "title": "How Long Has This Price Been the Top?",
        "hook": "Each day, count how many days back the price stayed at or below today's. A stack keeps only the peaks that could still block a future day.",
        "metaphors": {
            "node": "trading day",
            "edge": "look-back",
            "weight": "price",
            "visit": "Closing today's price",
            "start": "The first trading day",
            "done": "Every day's streak, in one pass."
        }
    },
    "largest_rectangle": {
        "scene": "leaderboard",
        "title": "The Biggest Billboard on the Skyline",
        "hook": "Every building could set the billboard's height; it stretches until a shorter building cuts it off. The stack tells each one exactly where it stops.",
        "metaphors": {
            "node": "building",
            "edge": "stretch",
            "weight": "height",
            "visit": "Measuring a billboard",
            "start": "An empty skyline",
            "done": "The largest rectangle that fits under the skyline."
        }
    },
    "rat_in_maze": {
        "scene": "maze",
        "title": "Every Way Out of the Maze",
        "hook": "The rat tries down, left, right, up. At a dead end it walks back and un-marks the square, so a different route can use it later.",
        "metaphors": {
            "node": "square",
            "edge": "step",
            "weight": "—",
            "visit": "Stepping into a square",
            "start": "The top-left corner",
            "done": "Every escape route, listed in order."
        }
    },
    "word_search": {
        "scene": "library",
        "title": "Trace the Word Through the Letter Grid",
        "hook": "Start on a matching letter, then feel for the next one among the neighbours. Wrong turn? Lift your finger off the last letter and try another way.",
        "metaphors": {
            "node": "letter tile",
            "edge": "adjacent step",
            "weight": "letter",
            "visit": "Testing a neighbouring letter",
            "start": "Any tile with the first letter",
            "done": "The word traced tile by tile, or proven absent."
        }
    },
    "trapping_rainwater": {
        "scene": "leaderboard",
        "title": "Rain Over the Skyline",
        "hook": "Water over a rooftop rises to the lower of the two tallest walls around it. Walk in from both ends and always settle the side with the lower wall.",
        "metaphors": {
            "node": "rooftop",
            "edge": "wall",
            "weight": "height",
            "visit": "Settling a rooftop",
            "start": "A dry skyline",
            "done": "Every pocket of water measured in one pass."
        }
    },
    "asteroid_collision": {
        "scene": "plates",
        "title": "Asteroids on a Collision Course",
        "hook": "Right-movers wait on a stack; a left-mover smashes into them one by one until it dies, ties, or clears the way.",
        "metaphors": {
            "node": "asteroid",
            "edge": "collision",
            "weight": "size",
            "visit": "An asteroid arriving",
            "start": "An empty sky",
            "done": "Only the survivors remain, in order."
        }
    },
    "find_min_rotated": {
        "scene": "library",
        "title": "Where Does the Shelf Wrap Around?",
        "hook": "A sorted shelf was cut and swapped. Compare the middle book with the last: if it's bigger, the wrap-around point is to the right.",
        "metaphors": {
            "node": "book",
            "edge": "shelf order",
            "weight": "call number",
            "visit": "Checking the middle book at position",
            "start": "The whole rotated shelf",
            "done": "The smallest book — and how far the shelf was rotated."
        }
    },
    "find_peak": {
        "scene": "stocks",
        "title": "Find a Local High Without Sorting",
        "hook": "Stand in the middle of the chart. Going uphill? A peak must lie ahead. Downhill? One is behind you. Halve and repeat.",
        "metaphors": {
            "node": "day",
            "edge": "slope",
            "weight": "price",
            "visit": "Checking the slope at a day",
            "start": "The whole chart",
            "done": "A local high, found in log n."
        }
    },
    "dll_reverse": {
        "scene": "train",
        "title": "Turn the Whole Train Around",
        "hook": "Every carriage is coupled both ways. To reverse the train, each carriage just swaps its front and back couplings — no one needs to remember the neighbours.",
        "metaphors": {
            "node": "carriage",
            "edge": "coupling",
            "weight": "cargo",
            "visit": "Swapping a carriage's couplings",
            "start": "The engine at the front",
            "done": "The train now runs the other way."
        }
    },
    "dll_delete_key": {
        "scene": "train",
        "title": "Uncouple Every Faulty Carriage",
        "hook": "Walk the train once. At each faulty carriage, couple its neighbours straight to each other, front and back, and it drops out.",
        "metaphors": {
            "node": "carriage",
            "edge": "coupling",
            "weight": "cargo",
            "visit": "Inspecting a carriage",
            "start": "The front of the train",
            "done": "Every faulty carriage uncoupled in one pass."
        }
    },
    "remove_nth_from_end": {
        "scene": "train",
        "title": "Drop the Nth Carriage From the Back",
        "hook": "You can't walk a train backwards. Send a scout N carriages ahead, then walk together — when the scout reaches the end, you're right before the one to drop.",
        "metaphors": {
            "node": "carriage",
            "edge": "coupling",
            "weight": "cargo",
            "visit": "Walking the train",
            "start": "Both walkers at the engine",
            "done": "The carriage is gone, in a single pass."
        }
    },
    "longest_complete_word": {
        "scene": "library",
        "title": "The Longest Word Built Letter by Letter",
        "hook": "A word counts only if you could have spelled it one valid word at a time: n, ni, nin, ninj, ninja. In a trie, that means every letter on its path is a word end.",
        "metaphors": {
            "node": "letter",
            "edge": "next letter",
            "weight": "—",
            "visit": "Checking a letter's end mark",
            "start": "The empty root",
            "done": "The longest word whose every prefix is a word."
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
