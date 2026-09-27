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
    "ll_palindrome": ["ll_palindrome", "palindrome linked list", "linked list palindrome", "is list palindrome"],
    "odd_even_list": ["odd_even_list", "odd even linked list", "segregate odd and even", "odd and even nodes"],
    "rotate_list": ["rotate_list", "rotate a linked list", "rotate list", "rotate ll by k"],
    "delete_middle": ["delete_middle", "delete the middle node", "delete middle node", "remove middle of linked list"],
    "koko_bananas": ["koko_bananas", "koko eating bananas", "koko", "bananas per hour", "smallest divisor", "minimum eating speed"],
    "min_max_partition": ["min_max_partition", "book allocation", "allocate books", "painter's partition", "painters partition", "split array largest sum", "capacity to ship", "ship packages within d days"],
    "aggressive_cows": ["aggressive_cows", "aggressive cows", "place cows", "magnetic force between balls", "maximize minimum distance"],
    "subsets_recursion": ["subsets_recursion", "subsets", "subset sums", "all subsequences", "subsequences with sum k", "print all subsequences", "power set recursion"],
    "generate_parentheses": ["generate_parentheses", "generate parentheses", "balanced parentheses combinations", "all valid parentheses"],
    "binary_strings": ["binary_strings", "binary strings without consecutive", "no consecutive ones", "no consecutive 1s"],
    "combination_sum": ["combination_sum", "combination sum", "combinations that sum to target", "coin combinations list"],
    "infix_to_postfix": ["infix_to_postfix", "infix to postfix", "shunting yard", "shunting-yard", "reverse polish conversion"],
    "infix_to_prefix": ["infix_to_prefix", "infix to prefix", "polish notation conversion"],
    "postfix_to_infix": ["postfix_to_infix", "postfix to infix"],
    "postfix_to_prefix": ["postfix_to_prefix", "postfix to prefix"],
    "prefix_to_infix": ["prefix_to_infix", "prefix to infix"],
    "prefix_to_postfix": ["prefix_to_postfix", "prefix to postfix"],
    "subsets_ii": ["subsets_ii", "subsets ii", "subsets with duplicates", "unique subsets", "distinct subsets"],
    "combination_sum_ii": ["combination_sum_ii", "combination sum ii", "combination sum 2", "each number used once"],
    "combination_sum_iii": ["combination_sum_iii", "combination sum iii", "combination sum 3", "k numbers sum to n"],
    "palindrome_partition": ["palindrome_partition", "palindrome partitioning", "partition into palindromes", "all palindromic partitions"],
    "letter_combinations": ["letter_combinations", "letter combinations", "phone number letters", "keypad combinations", "phone keypad"],
    "lower_bound": ["lower_bound", "lower bound", "search insert position", "insert position", "first element not less than"],
    "upper_bound": ["upper_bound", "upper bound", "first element greater than"],
    "first_last_occurrence": ["first_last_occurrence", "first and last occurrence", "first and last position", "count occurrences", "number of occurrences"],
    "floor_ceil": ["floor_ceil", "floor and ceil", "floor in sorted array", "ceil in sorted array"],
    "kth_missing": ["kth_missing", "kth missing positive", "k-th missing", "missing positive number"],
    "single_element_sorted": ["single_element_sorted", "single element in a sorted array", "single non-duplicate", "appears once sorted"],
    "sqrt_search": ["sqrt_search", "square root", "floor sqrt", "integer square root"],
    "nth_root": ["nth_root", "nth root", "n-th root"],
    "min_bouquets": ["min_bouquets", "minimum days to make m bouquets", "bouquets", "bloom day"],
    "search_2d_matrix": ["search_2d_matrix", "search a 2d matrix", "search in a 2d matrix", "sorted matrix search"],
    "search_2d_matrix_ii": ["search_2d_matrix_ii", "search a 2d matrix ii", "row and column sorted", "staircase search"],
    "row_max_ones": ["row_max_ones", "row with maximum 1s", "row with max ones", "maximum number of 1s"],
    "add_two_numbers": ["add_two_numbers", "add two numbers", "sum of two linked lists"],
    "add_one_list": ["add_one_list", "add one to linked list", "add 1 to a number represented", "plus one linked list"],
    "next_smaller": ["next_smaller", "next smaller element", "nse"],
    "nge_circular": ["nge_circular", "next greater element ii", "next greater element 2", "circular next greater"],
    "remove_k_digits": ["remove_k_digits", "remove k digits", "smallest number after removing"],
    "sum_subarray_mins": ["sum_subarray_mins", "sum of subarray minimums", "subarray minimums"],
    "remove_duplicates_sorted": ["remove_duplicates_sorted", "remove duplicates from sorted array", "remove duplicates"],
    "rotate_array_k": ["rotate_array_k", "rotate array", "left rotate", "rotate by k"],
    "move_zeros": ["move_zeros", "move zeroes", "move zeros to end"],
    "leaders": ["leaders", "leaders in an array", "array leaders"],
    "longest_subarray_sum_k": ["longest_subarray_sum_k", "longest subarray with sum k", "longest subarray sum"],
    "second_largest": ["second_largest", "second largest element", "second largest"],
    "iter_preorder": ["iter_preorder", "iterative preorder"],
    "iter_inorder": ["iter_inorder", "iterative inorder"],
    "postorder_two_stacks": ["postorder_two_stacks", "postorder two stacks", "postorder using 2 stack"],
    "postorder_one_stack": ["postorder_one_stack", "postorder one stack", "postorder using 1 stack"],
    "zigzag_traversal": ["zigzag_traversal", "zigzag", "spiral traversal"],
    "right_view": ["right_view", "right view", "left view"],
    "top_view": ["top_view", "top view"],
    "bottom_view": ["bottom_view", "bottom view"],
    "vertical_order": ["vertical_order", "vertical order"],
    "boundary_traversal": ["boundary_traversal", "boundary traversal"],
    "max_width": ["max_width", "maximum width", "width of binary tree"],
    "balanced_tree": ["balanced_tree", "balanced binary tree", "height balanced"],
    "symmetric_tree": ["symmetric_tree", "symmetric tree", "mirror tree"],
    "max_path_sum": ["max_path_sum", "maximum path sum", "max path sum"],
    "root_to_leaf_paths": ["root_to_leaf_paths", "root to leaf path"],
    "children_sum": ["children_sum", "children sum property"],
    "nodes_at_distance_k": ["nodes_at_distance_k", "distance k", "nodes at distance"],
    "burn_tree": ["burn_tree", "burn the binary tree", "burn tree"],
    "count_complete_nodes": ["count_complete_nodes", "count nodes complete", "complete binary tree nodes"],
    "frog_jump_k": ["frog_jump_k", "frog jump with k", "frog jump k"],
    "ninja_training": ["ninja_training", "ninja training", "ninja's training"],
    "min_falling_path": ["min_falling_path", "minimum falling path", "falling path sum"],
    "triangle_path": ["triangle_path", "triangle", "triangle path sum"],
    "partition_equal_subset": ["partition_equal_subset", "partition equal subset", "equal sum partition"],
    "count_subsets_sum_k": ["count_subsets_sum_k", "count subsets with sum", "number of subsets with sum"],
    "unbounded_knapsack": ["unbounded_knapsack", "unbounded knapsack"],
    "rod_cutting": ["rod_cutting", "rod cutting", "cut the rod"],
    "print_lcs": ["print_lcs", "print lcs", "print longest common subsequence"],
    "longest_palindromic_subseq": ["longest_palindromic_subseq", "longest palindromic subsequence"],
    "min_insert_palindrome": ["min_insert_palindrome", "minimum insertions palindrome", "min insertions to make palindrome"],
    "min_ins_del": ["min_ins_del", "minimum insertions deletions", "convert string a to b"],
    "shortest_supersequence": ["shortest_supersequence", "shortest common supersequence"],
    "distinct_subsequences": ["distinct_subsequences", "distinct subsequences"],
    "wildcard_match": ["wildcard_match", "wildcard matching", "wildcard pattern"],
    "number_of_islands": ["number_of_islands", "number of islands", "connected components in matrix", "count islands"],
    "rotten_oranges": ["rotten_oranges", "rotten oranges", "rotting oranges"],
    "nearest_one_distance": ["nearest_one_distance", "distance of nearest cell", "nearest 1", "01 matrix"],
    "surrounded_regions": ["surrounded_regions", "surrounded regions", "replace o with x"],
    "number_of_enclaves": ["number_of_enclaves", "number of enclaves", "enclaves"],
    "binary_maze_path": ["binary_maze_path", "shortest path in binary maze", "binary maze", "shortest path binary matrix"],
    "min_effort_path": ["min_effort_path", "path with minimum effort", "minimum effort"],
    "swim_rising_water": ["swim_rising_water", "swim in rising water"],
    "largest_island": ["largest_island", "making a large island", "largest island"],
    "islands_ii": ["islands_ii", "number of islands ii", "islands 2", "online islands"],
    "floyd_warshall": ["floyd_warshall", "floyd warshall", "floyd-warshall", "all pairs shortest path"],
    "city_fewest_neighbours": ["city_fewest_neighbours", "city with the smallest number of neighbors", "city smallest neighbours", "threshold distance city"],
    "stock_ii": ["stock_ii", "best time to buy and sell stock ii", "stock ii"],
    "stock_iii": ["stock_iii", "best time to buy and sell stock iii", "stock iii"],
    "stock_iv": ["stock_iv", "best time to buy and sell stock iv", "stock iv"],
    "stock_cooldown": ["stock_cooldown", "stock with cooldown", "cooldown"],
    "stock_fee": ["stock_fee", "stock with transaction fee", "transaction fee"],
    "print_lis": ["print_lis", "print longest increasing subsequence", "print lis"],
    "largest_divisible_subset": ["largest_divisible_subset", "largest divisible subset"],
    "longest_string_chain": ["longest_string_chain", "longest string chain"],
    "longest_bitonic": ["longest_bitonic", "longest bitonic subsequence", "bitonic"],
    "number_of_lis": ["number_of_lis", "number of longest increasing subsequence", "number of lis"],
    "cycle_undirected_bfs": ["cycle_undirected_bfs", "cycle detection undirected bfs", "detect cycle undirected bfs"],
    "cycle_undirected_dfs": ["cycle_undirected_dfs", "cycle detection undirected dfs", "detect cycle undirected dfs", "detect a cycle in an undirected graph"],
    "bridges": ["bridges", "bridges in graph", "critical connections", "tarjan bridges"],
    "articulation_points": ["articulation_points", "articulation point", "cut vertex"],
    "connect_network_ops": ["connect_network_ops", "make network connected", "number of operations to make network connected"],
    "cycle_directed": ["cycle_directed", "cycle detection directed", "detect a cycle in a directed graph"],
    "safe_states": ["safe_states", "eventual safe states", "safe states"],
    "kosaraju": ["kosaraju", "kosaraju", "strongly connected components", "scc"],
    "shortest_path_dag": ["shortest_path_dag", "shortest path in dag", "dag shortest path"],
    "floor_ceil_bst": ["floor_ceil_bst", "floor and ceil in bst", "floor in bst", "ceil in bst"],
    "kth_bst": ["kth_bst", "kth smallest in bst", "kth largest in bst"],
    "lca_bst": ["lca_bst", "lca in bst", "lowest common ancestor bst"],
    "successor_predecessor": ["successor_predecessor", "inorder successor", "inorder predecessor"],
    "two_sum_bst": ["two_sum_bst", "two sum in bst", "pair with sum k bst"],
    "bst_from_preorder": ["bst_from_preorder", "bst from preorder", "construct bst preorder"],
    "validate_bst": ["validate_bst", "validate bst", "check if bst"],
    "recover_bst": ["recover_bst", "recover bst", "two nodes swapped"],
    "largest_bst": ["largest_bst", "largest bst"],
    "is_min_heap": ["is_min_heap", "check min heap", "array represents min heap"],
    "min_to_max_heap": ["min_to_max_heap", "min heap to max heap"],
    "connect_sticks": ["connect_sticks", "connect sticks", "connect ropes"],
    "rank_replace": ["rank_replace", "replace elements by rank", "array rank transform"],
    "top_k_frequent": ["top_k_frequent", "top k frequent"],
    "hand_of_straights": ["hand_of_straights", "hand of straights"],
    "task_scheduler": ["task_scheduler", "task scheduler"],
    "median_stream": ["median_stream", "median from data stream", "running median"],
    "remove_outer_parens": ["remove_outer_parens", "remove outermost parentheses"],
    "reverse_words": ["reverse_words", "reverse words in a string", "reverse every word"],
    "largest_odd_number": ["largest_odd_number", "largest odd number in string"],
    "longest_common_prefix": ["longest_common_prefix", "longest common prefix"],
    "isomorphic_strings": ["isomorphic_strings", "isomorphic strings"],
    "rotate_string": ["rotate_string", "rotate string"],
    "sort_by_frequency": ["sort_by_frequency", "sort characters by frequency"],
    "max_nesting_depth": ["max_nesting_depth", "maximum nesting depth"],
    "roman_to_integer": ["roman_to_integer", "roman to integer"],
    "string_to_integer": ["string_to_integer", "atoi", "string to integer"],
    "sum_of_beauty": ["sum_of_beauty", "sum of beauty of all substrings"],
    "char_replacement": ["char_replacement", "longest repeating character replacement"],
    "binary_subarray_sum": ["binary_subarray_sum", "binary subarrays with sum"],
    "nice_subarrays": ["nice_subarrays", "nice subarrays"],
    "substrings_all_three": ["substrings_all_three", "substrings containing all three characters"],
    "max_card_points": ["max_card_points", "maximum points you can obtain from cards"],
    "subarrays_k_distinct": ["subarrays_k_distinct", "subarrays with k different integers"],
    "min_window_substring": ["min_window_substring", "minimum window substring"],
    "min_window_subsequence": ["min_window_subsequence", "minimum window subsequence"],
    "word_ladder": ["word_ladder", "word ladder"],
    "word_ladder_ii": ["word_ladder_ii", "word ladder ii"],
    "alien_dictionary": ["alien_dictionary", "alien dictionary"],
    "cheapest_flight_k": ["cheapest_flight_k", "cheapest flights within k stops"],
    "ways_to_arrive": ["ways_to_arrive", "number of ways to arrive at destination"],
    "min_multiplications": ["min_multiplications", "minimum multiplications to reach end"],
    "most_stones": ["most_stones", "most stones removed"],
    "network_delay": ["network_delay", "network delay time"],
    "cut_stick": ["cut_stick", "minimum cost to cut a stick"],
    "burst_balloons": ["burst_balloons", "burst balloons"],
    "boolean_evaluation": ["boolean_evaluation", "evaluate boolean expression to true"],
    "palindrome_partition_ii": ["palindrome_partition_ii", "palindrome partitioning ii (min cuts)"],
    "partition_array_max_sum": ["partition_array_max_sum", "partition array for maximum sum"],
    "min_subset_diff": ["min_subset_diff", "partition into two subsets with minimum difference"],
    "count_partitions_diff": ["count_partitions_diff", "count partitions with given difference"],
    "target_sum": ["target_sum", "target sum"],
    "max_rectangle_ones": ["max_rectangle_ones", "maximal rectangle of 1s"],
    "largest_element": ["largest_element", "largest element in an array"],
    "check_sorted": ["check_sorted", "check if an array is sorted"],
    "linear_search": ["linear_search", "linear search"],
    "union_sorted": ["union_sorted", "union of two sorted arrays"],
    "intersection_sorted": ["intersection_sorted", "intersection of two sorted arrays"],
    "missing_number": ["missing_number", "find the missing number"],
    "max_consecutive_ones": ["max_consecutive_ones", "maximum consecutive ones"],
    "rearrange_by_sign": ["rearrange_by_sign", "rearrange array elements by sign"],
    "max_product_subarray": ["max_product_subarray", "maximum product subarray"],
    "longest_sum_k_any": ["longest_sum_k_any", "longest subarray with sum k (any sign)"],
    "count_sum_k": ["count_sum_k", "count subarrays with sum k"],
    "largest_zero_sum": ["largest_zero_sum", "largest subarray with sum 0"],
    "count_xor_k": ["count_xor_k", "count subarrays with xor k"],
    "longest_consecutive": ["longest_consecutive", "longest consecutive sequence"],
    "majority_n3": ["majority_n3", "majority elements (> n/3)"],
    "repeating_missing": ["repeating_missing", "find the repeating and missing numbers"],
    "three_sum": ["three_sum", "3 sum"],
    "four_sum": ["four_sum", "4 sum"],
    "set_matrix_zeros": ["set_matrix_zeros", "set matrix zeros"],
    "rotate_matrix": ["rotate_matrix", "rotate a matrix by 90°"],
    "spiral_order": ["spiral_order", "spiral traversal of a matrix"],
    "pascal_triangle": ["pascal_triangle", "pascal's triangle"],
    "merge_no_space": ["merge_no_space", "merge two sorted arrays without extra space"],
    "count_inversions": ["count_inversions", "count inversions"],
    "reverse_pairs": ["reverse_pairs", "reverse pairs"],
    "count_digits": ["count_digits", "count digits of a number"],
    "reverse_number": ["reverse_number", "reverse a number"],
    "palindrome_number": ["palindrome_number", "palindrome number"],
    "armstrong_number": ["armstrong_number", "armstrong number"],
    "print_divisors": ["print_divisors", "print all divisors"],
    "check_prime": ["check_prime", "check for a prime number"],
    "factorial": ["factorial", "factorial of a number"],
    "sum_first_n": ["sum_first_n", "sum of the first n numbers"],
    "reverse_array": ["reverse_array", "reverse an array (two pointers)"],
    "palindrome_string": ["palindrome_string", "check if a string is a palindrome"],
    "frequency_count": ["frequency_count", "count frequencies / highest occurring element"],
    "check_ith_bit": ["check_ith_bit", "check if the i-th bit is set"],
    "check_odd": ["check_odd", "check if a number is odd (bitwise)"],
    "swap_xor": ["swap_xor", "swap two numbers with xor"],
    "divide_bits": ["divide_bits", "divide without * or /"],
    "xor_range": ["xor_range", "xor of numbers in a range"],
    "single_number_iii": ["single_number_iii", "single number iii (two uniques)"],
    "ll_insert_head": ["ll_insert_head", "insert at the head of a linked list"],
    "ll_delete_head": ["ll_delete_head", "delete the head of a linked list"],
    "ll_length": ["ll_length", "length of a linked list"],
    "ll_search": ["ll_search", "search in a linked list"],
    "dll_insert_head": ["dll_insert_head", "insert before the head of a doubly linked list"],
    "dll_delete_head": ["dll_delete_head", "delete the head of a doubly linked list"],
    "dll_pairs_sum": ["dll_pairs_sum", "pairs with a given sum in a sorted dll"],
    "dll_remove_duplicates": ["dll_remove_duplicates", "remove duplicates from a sorted dll"],
    "ll_reverse_recursive": ["ll_reverse_recursive", "reverse a linked list (recursive)"],
    "loop_length": ["loop_length", "length of a loop in a linked list"],
    "sort_012_list": ["sort_012_list", "sort a linked list of 0s, 1s and 2s"],
    "sort_list": ["sort_list", "sort a linked list (merge sort)"],
    "y_intersection": ["y_intersection", "intersection point of a y-shaped linked list"],
    "reverse_k_group": ["reverse_k_group", "reverse a linked list in groups of k"],
    "search_rotated_ii": ["search_rotated_ii", "search in rotated sorted array ii (duplicates)"],
    "median_two_sorted": ["median_two_sorted", "median of two sorted arrays"],
    "kth_two_sorted": ["kth_two_sorted", "k-th element of two sorted arrays"],
    "gas_station": ["gas_station", "minimise max distance to gas station"],
    "peak_element_ii": ["peak_element_ii", "find a peak element ii (matrix)"],
    "matrix_median": ["matrix_median", "median of a row-wise sorted matrix"],
    "print_1_to_n": ["print_1_to_n", "print 1 to n using recursion"],
    "print_n_to_1": ["print_n_to_1", "print n to 1 using recursion"],
    "recursive_bubble_sort": ["recursive_bubble_sort", "recursive bubble sort"],
    "recursive_insertion_sort": ["recursive_insertion_sort", "recursive insertion sort"],
    "count_good_numbers": ["count_good_numbers", "count good numbers"],
    "sort_stack": ["sort_stack", "sort a stack using recursion"],
    "reverse_stack": ["reverse_stack", "reverse a stack using recursion"],
    "recursive_atoi": ["recursive_atoi", "recursive atoi()"],
    "word_break": ["word_break", "word break"],
    "m_coloring": ["m_coloring", "m-coloring problem"],
    "sudoku_solver": ["sudoku_solver", "sudoku solver"],
    "expression_add_operators": ["expression_add_operators", "expression add operators"],
    "valid_paren_star": ["valid_paren_star", "valid parenthesis string (with *)"],
    "shortest_job_first": ["shortest_job_first", "shortest job first (sjf) scheduling"],
    "lru_page_faults": ["lru_page_faults", "lru page replacement (page faults)"],
    "insert_interval": ["insert_interval", "insert interval"],
    "non_overlapping_intervals": ["non_overlapping_intervals", "non-overlapping intervals"],
    "greater_to_right": ["greater_to_right", "number of greater elements to the right"],
    "sum_subarray_ranges": ["sum_subarray_ranges", "sum of subarray ranges"],
    "celebrity": ["celebrity", "the celebrity problem"],
    "build_pre_in": ["build_pre_in", "construct a binary tree from preorder & inorder"],
    "build_post_in": ["build_post_in", "construct a binary tree from postorder & inorder"],
    "serialize_tree": ["serialize_tree", "serialize and deserialize a binary tree"],
    "morris_inorder": ["morris_inorder", "morris inorder traversal"],
    "morris_preorder": ["morris_preorder", "morris preorder traversal"],
    "flatten_tree": ["flatten_tree", "flatten a binary tree to a linked list"],
    "identical_trees": ["identical_trees", "check if two trees are identical"],
    "merge_two_bsts": ["merge_two_bsts", "merge two bsts (sorted output)"],
    "stack_array": ["stack_array", "implement a stack using an array"],
    "queue_array": ["queue_array", "implement a queue using an array"],
    "stack_using_queue": ["stack_using_queue", "implement a stack using a queue"],
    "queue_using_stacks": ["queue_using_stacks", "implement a queue using stacks"],
    "stack_linkedlist": ["stack_linkedlist", "implement a stack using a linked list"],
    "queue_linkedlist": ["queue_linkedlist", "implement a queue using a linked list"],
    "min_stack": ["min_stack", "implement a min stack"],
    "lru_cache": ["lru_cache", "lru cache"],
    "lfu_cache": ["lfu_cache", "lfu cache"],
    "design_twitter": ["design_twitter", "design twitter"],
    "clone_random_list": ["clone_random_list", "clone a linked list with random pointers"],
    "flatten_list": ["flatten_list", "flatten a linked list (sorted columns)"],
    "merge_k_lists": ["merge_k_lists", "merge k sorted lists"],
    "bracket_reversals": ["bracket_reversals", "minimum bracket reversals to balance"],
    "count_and_say": ["count_and_say", "count and say"],
    "longest_happy_prefix": ["longest_happy_prefix", "longest happy prefix (lps)"],
    "count_palindromic_subseq": ["count_palindromic_subseq", "count palindromic subsequences"],
    "distinct_substrings": ["distinct_substrings", "number of distinct substrings (trie)"],
    "max_xor_pair": ["max_xor_pair", "maximum xor of two numbers (trie)"],
    "max_xor_queries": ["max_xor_queries", "maximum xor with an element from an array"],
    "trie_advanced": ["trie_advanced", "trie with counts (insert, count, erase)"],
    "ninja_friends": ["ninja_friends", "ninja and his friends (cherry pickup ii)"],
    "max_sum_combination": ["max_sum_combination", "maximum sum combinations"],
    "accounts_merge": ["accounts_merge", "accounts merge"],
    "a_star_grid": ["a_star_grid", "a* search on a grid"],
    "best_first_grid": ["best_first_grid", "greedy best-first search on a grid"],
    "zero_one_bfs": ["zero_one_bfs", "0-1 bfs (minimum cost path)"],
    "max_flow": ["max_flow", "maximum flow (edmonds–karp)"],
    "min_cut": ["min_cut", "minimum s-t cut"],
    "bipartite_matching": ["bipartite_matching", "maximum bipartite matching (kuhn)"],
    "lca_lifting": ["lca_lifting", "lowest common ancestor (binary lifting)"],
    "kth_ancestor": ["kth_ancestor", "k-th ancestor (binary lifting)"],
    "tsp_bitmask": ["tsp_bitmask", "travelling salesman (bitmask dp)"],
    "assignment_bitmask": ["assignment_bitmask", "job assignment (bitmask dp)"],
    "sparse_table": ["sparse_table", "sparse table (range minimum query)"],
    "sqrt_decomposition": ["sqrt_decomposition", "sqrt decomposition (range sum)"],
    "lazy_segment_tree": ["lazy_segment_tree", "segment tree with lazy propagation"],
    "extended_gcd": ["extended_gcd", "extended euclidean algorithm"],
    "mod_inverse": ["mod_inverse", "modular multiplicative inverse"],
    "ncr_mod": ["ncr_mod", "ncr mod p (fermat inverse)"],
    "euler_totient": ["euler_totient", "euler's totient function"],
    "spf_sieve": ["spf_sieve", "smallest prime factor sieve"],
    "crt": ["crt", "chinese remainder theorem"],
    "suffix_array": ["suffix_array", "suffix array (prefix doubling)"],
    "lcp_kasai": ["lcp_kasai", "lcp array (kasai)"],
    "longest_repeated_substring": ["longest_repeated_substring", "longest repeated substring (sa + lcp)"],
    "euler_path": ["euler_path", "euler path / circuit (hierholzer)"],
    "longest_path_dag": ["longest_path_dag", "longest path in a dag"],
    "count_paths_dag": ["count_paths_dag", "count paths in a dag"],
    "matrix_exponentiation": ["matrix_exponentiation", "matrix exponentiation (fibonacci)"],
    "ternary_search": ["ternary_search", "ternary search (peak of a unimodal array)"],
    "meet_in_middle": ["meet_in_middle", "meet in the middle (subset sums ≤ s)"],
    "nim": ["nim", "nim (xor of piles)"],
    "grundy_numbers": ["grundy_numbers", "grundy numbers (subtraction game)"],
    "optimal_game": ["optimal_game", "optimal strategy for a coin game"],
    "aho_corasick": ["aho_corasick", "aho–corasick (multi-pattern search)"],
    "substring_hash": ["substring_hash", "substring equality by rolling hash"],
    "tarjan_scc": ["tarjan_scc", "strongly connected components (tarjan)"],
    "two_sat": ["two_sat", "2-sat (implication graph + scc)"],
    "lexicographic_topo": ["lexicographic_topo", "lexicographically smallest topological order"],
    "convex_hull": ["convex_hull", "convex hull (monotone chain)"],
    "polygon_area": ["polygon_area", "polygon area (shoelace formula)"],
    "closest_pair": ["closest_pair", "closest pair of points (divide & conquer)"],
    "digit_dp": ["digit_dp", "digit dp (count numbers with digit sum s)"],
    "tree_robber": ["tree_robber", "house robber on a tree"],
    "sos_dp": ["sos_dp", "sum over subsets (sos dp)"],
    "sum_distances_tree": ["sum_distances_tree", "sum of distances in a tree (rerooting)"],
    "bit_kth": ["bit_kth", "k-th smallest with a fenwick tree"],
    "inversions_bit": ["inversions_bit", "count inversions with a fenwick tree"],
    "prefix_sum_2d": ["prefix_sum_2d", "2-d prefix sums (rectangle queries)"],
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
    },
    "ll_palindrome": {
        "scene": "train",
        "title": "Does the Train Read the Same Both Ways?",
        "hook": "You can only walk a train front to back. So turn the back half around, walk both halves toward the middle comparing cargo, then turn it back.",
        "metaphors": {"node": "carriage", "edge": "coupling", "weight": "cargo",
                      "visit": "Comparing two carriages", "start": "The full train",
                      "done": "A verdict, with the train left exactly as it was."}
    },
    "odd_even_list": {
        "scene": "train",
        "title": "Split the Train Into Two Convoys",
        "hook": "Every other carriage recouples to the one two ahead, forming two convoys; then the second convoy is hitched to the end of the first.",
        "metaphors": {"node": "carriage", "edge": "coupling", "weight": "cargo",
                      "visit": "Recoupling a carriage", "start": "One mixed train",
                      "done": "Odd positions first, then even — no carriage moved."}
    },
    "rotate_list": {
        "scene": "train",
        "title": "Loop the Track, Then Cut It",
        "hook": "Hitch the last carriage to the engine to make a ring, roll to the right spot, and uncouple — the last K carriages are now at the front.",
        "metaphors": {"node": "carriage", "edge": "coupling", "weight": "cargo",
                      "visit": "Rolling to the cut point", "start": "The original train",
                      "done": "Rotated by changing just two couplings."}
    },
    "delete_middle": {
        "scene": "train",
        "title": "Uncouple the Middle Carriage",
        "hook": "Send a runner ahead at double speed with a two-carriage head start; when it hits the end, you're standing right before the middle one.",
        "metaphors": {"node": "carriage", "edge": "coupling", "weight": "cargo",
                      "visit": "Walking the train", "start": "Both walkers near the engine",
                      "done": "The middle carriage is gone, in one pass."}
    },
    "koko_bananas": {
        "scene": "market",
        "title": "How Slowly Can Koko Eat?",
        "hook": "Don't search the piles — search the answer. Guess a speed, time every pile; too slow means go faster, fast enough means try slower.",
        "metaphors": {"node": "pile", "edge": "—", "weight": "bananas",
                      "visit": "Timing a pile", "start": "Any speed from 1 to the biggest pile",
                      "done": "The slowest speed that still beats the guards."}
    },
    "min_max_partition": {
        "scene": "scheduler",
        "title": "Share the Work So the Busiest Is Least Busy",
        "hook": "Guess a workload cap, hand out work left to right until each person hits it. Too many people needed? Raise the cap. Few enough? Lower it.",
        "metaphors": {"node": "job", "edge": "—", "weight": "effort",
                      "visit": "Handing out a job", "start": "Cap between the biggest job and the total",
                      "done": "The smallest cap that still fits k people."}
    },
    "aggressive_cows": {
        "scene": "grid_power",
        "title": "Keep the Cows as Far Apart as Possible",
        "hook": "Guess a minimum gap and drop cows greedily left to right. All fit? Try a wider gap. Some left over? Narrow it.",
        "metaphors": {"node": "stall", "edge": "gap", "weight": "position",
                      "visit": "Testing a stall", "start": "Gaps from 1 to the full span",
                      "done": "The widest gap every cow can keep."}
    },
    "subsets_recursion": {
        "scene": "files",
        "title": "Every Packing List, One Yes/No at a Time",
        "hook": "For each item you ask one question — pack it or not? Two answers per item branch into a tree, and every leaf is one complete packing list.",
        "metaphors": {"node": "decision", "edge": "yes / no", "weight": "item",
                      "visit": "Deciding an item", "start": "An empty bag",
                      "done": "All 2ⁿ packing lists, found by branching."}
    },
    "generate_parentheses": {
        "scene": "plates",
        "title": "Stack and Unstack Plates Legally",
        "hook": "You may put a plate down while you have plates left, and pick one up only if one is down. Follow every legal choice and each leaf is a valid sequence.",
        "metaphors": {"node": "prefix", "edge": "place / remove", "weight": "—",
                      "visit": "Choosing the next move", "start": "An empty table",
                      "done": "Every balanced sequence, with illegal branches never tried."}
    },
    "binary_strings": {
        "scene": "files",
        "title": "Light Switches That Can't Both Be On",
        "hook": "A row of switches where no two neighbours may be on. Build left to right: 'off' is always fine, 'on' only after an 'off'.",
        "metaphors": {"node": "pattern", "edge": "off / on", "weight": "—",
                      "visit": "Setting the next switch", "start": "No switches set",
                      "done": "Every legal pattern — and their count is Fibonacci."}
    },
    "combination_sum": {
        "scene": "vault",
        "title": "Make Change, Listing Every Way",
        "hook": "Keep using the current coin while it fits, or retire it for good and move to the next. Each path that lands exactly on the amount is one way.",
        "metaphors": {"node": "handful", "edge": "use again / retire", "weight": "coin",
                      "visit": "Choosing a coin", "start": "Nothing picked",
                      "done": "Every combination that hits the target, each once."}
    },
    "infix_to_postfix": {
        "scene": "plates",
        "title": "Waiting Room for Operators",
        "hook": "Numbers walk straight through; operators wait in line until a weaker one arrives and sends the stronger ones out first.",
        "metaphors": {"node": "token", "edge": "—", "weight": "precedence",
                      "visit": "Reading a token", "start": "An empty stack",
                      "done": "The expression, rewritten."}
    },
    "infix_to_prefix": {
        "scene": "plates",
        "title": "The Same Queue, Run Backwards",
        "hook": "Read the expression from the right, let ')' open groups, and write the answer backwards — then flip it.",
        "metaphors": {"node": "token", "edge": "—", "weight": "precedence",
                      "visit": "Reading a token", "start": "An empty stack",
                      "done": "The expression, rewritten."}
    },
    "postfix_to_infix": {
        "scene": "plates",
        "title": "Rebuild the Brackets",
        "hook": "Each operator grabs the two most recent pieces off the pile and glues them into one bracketed piece.",
        "metaphors": {"node": "token", "edge": "—", "weight": "precedence",
                      "visit": "Reading a token", "start": "An empty stack",
                      "done": "The expression, rewritten."}
    },
    "postfix_to_prefix": {
        "scene": "plates",
        "title": "Move the Operator to the Front",
        "hook": "Same pile of pieces as postfix → infix, but each operator is written before its two operands.",
        "metaphors": {"node": "token", "edge": "—", "weight": "precedence",
                      "visit": "Reading a token", "start": "An empty stack",
                      "done": "The expression, rewritten."}
    },
    "prefix_to_infix": {
        "scene": "plates",
        "title": "Rebuild Brackets, Reading Backwards",
        "hook": "Scan from the right; the first piece off the pile is the LEFT operand this time.",
        "metaphors": {"node": "token", "edge": "—", "weight": "precedence",
                      "visit": "Reading a token", "start": "An empty stack",
                      "done": "The expression, rewritten."}
    },
    "prefix_to_postfix": {
        "scene": "plates",
        "title": "Move the Operator to the Back",
        "hook": "Scan from the right, pop two pieces, and glue them as left + right + operator.",
        "metaphors": {"node": "token", "edge": "—", "weight": "precedence",
                      "visit": "Reading a token", "start": "An empty stack",
                      "done": "The expression, rewritten."}
    },
    "subsets_ii": {
        "scene": "files",
        "title": "Packing Lists Without Repeats",
        "hook": "Two identical items give identical lists — so at each step, only reach for the first of any identical items.",
        "metaphors": {"node": "call", "edge": "choice", "weight": "—",
                      "visit": "Making a recursive call", "start": "The empty choice",
                      "done": "Every answer, found by branching."}
    },
    "combination_sum_ii": {
        "scene": "vault",
        "title": "Exact Change, Each Coin Once",
        "hook": "Coins sorted, each usable once. Skip a coin identical to the one just tried, and stop as soon as a coin is too big.",
        "metaphors": {"node": "call", "edge": "choice", "weight": "—",
                      "visit": "Making a recursive call", "start": "The empty choice",
                      "done": "Every answer, found by branching."}
    },
    "combination_sum_iii": {
        "scene": "vault",
        "title": "Pick k Digits That Hit the Sum",
        "hook": "Always pick a bigger digit than last time, so every set appears once; stop when a digit overshoots.",
        "metaphors": {"node": "call", "edge": "choice", "weight": "—",
                      "visit": "Making a recursive call", "start": "The empty choice",
                      "done": "Every answer, found by branching."}
    },
    "palindrome_partition": {
        "scene": "dna",
        "title": "Cut a Strand Into Mirror Pieces",
        "hook": "Snip the strand only where the piece reads the same both ways; every way to reach the end is one answer.",
        "metaphors": {"node": "call", "edge": "choice", "weight": "—",
                      "visit": "Making a recursive call", "start": "The empty choice",
                      "done": "Every answer, found by branching."}
    },
    "letter_combinations": {
        "scene": "files",
        "title": "What Words Could Those Keys Spell?",
        "hook": "Each keypad digit stands for 3 or 4 letters. Branch on every letter, one level per key.",
        "metaphors": {"node": "call", "edge": "choice", "weight": "—",
                      "visit": "Making a recursive call", "start": "The empty choice",
                      "done": "Every answer, found by branching."}
    },
    "lower_bound": {
        "scene": "library",
        "title": "Where Would This Book Go?",
        "hook": "Find the first shelf slot holding a call number at least as big — even after a match, keep checking left.",
        "metaphors": {"node": "book", "edge": "shelf order", "weight": "call number",
                      "visit": "Checking the middle book at position", "start": "The whole shelf",
                      "done": "The boundary, found in log n."}
    },
    "upper_bound": {
        "scene": "library",
        "title": "The First Book Past This Number",
        "hook": "Find the first slot strictly bigger; everything before it is at most your number.",
        "metaphors": {"node": "book", "edge": "shelf order", "weight": "call number",
                      "visit": "Checking the middle book at position", "start": "The whole shelf",
                      "done": "The boundary, found in log n."}
    },
    "first_last_occurrence": {
        "scene": "library",
        "title": "Where Does This Run of Copies Start and End?",
        "hook": "Two searches: one keeps sliding left after a match, the other keeps sliding right.",
        "metaphors": {"node": "book", "edge": "shelf order", "weight": "call number",
                      "visit": "Checking the middle book at position", "start": "The whole shelf",
                      "done": "The boundary, found in log n."}
    },
    "floor_ceil": {
        "scene": "library",
        "title": "The Nearest Books on Either Side",
        "hook": "The largest call number not above yours, and the smallest not below it.",
        "metaphors": {"node": "book", "edge": "shelf order", "weight": "call number",
                      "visit": "Checking the middle book at position", "start": "The whole shelf",
                      "done": "The boundary, found in log n."}
    },
    "kth_missing": {
        "scene": "library",
        "title": "Which Call Number Is Missing?",
        "hook": "Before each book, its number minus its position tells you how many numbers were skipped. Search on that count.",
        "metaphors": {"node": "book", "edge": "shelf order", "weight": "call number",
                      "visit": "Checking the middle book at position", "start": "The whole shelf",
                      "done": "The boundary, found in log n."}
    },
    "single_element_sorted": {
        "scene": "library",
        "title": "The Book Without a Twin",
        "hook": "Twins start on even slots until the odd one out shifts everything — search for where the pattern breaks.",
        "metaphors": {"node": "book", "edge": "shelf order", "weight": "call number",
                      "visit": "Checking the middle book at position", "start": "The whole shelf",
                      "done": "The boundary, found in log n."}
    },
    "sqrt_search": {
        "scene": "vault",
        "title": "Guess the Square Root",
        "hook": "Too big squared means go lower, small enough means try higher — halving the range of guesses each time.",
        "metaphors": {"node": "item", "edge": "—", "weight": "value",
                      "visit": "Checking", "start": "The input",
                      "done": "The answer."}
    },
    "nth_root": {
        "scene": "vault",
        "title": "Is There an Exact nth Root?",
        "hook": "Raise the guess to the nth power and compare — binary search over the candidates.",
        "metaphors": {"node": "item", "edge": "—", "weight": "value",
                      "visit": "Checking", "start": "The input",
                      "done": "The answer."}
    },
    "min_bouquets": {
        "scene": "market",
        "title": "When Can the Florist Open?",
        "hook": "Guess a day; walk the flowers counting adjacent bloomed runs. Enough bouquets? Try earlier.",
        "metaphors": {"node": "item", "edge": "—", "weight": "value",
                      "visit": "Checking", "start": "The input",
                      "done": "The answer."}
    },
    "search_2d_matrix": {
        "scene": "library",
        "title": "A Shelf of Shelves",
        "hook": "Read shelf after shelf and it's one sorted run — binary-search the position, then work out the shelf.",
        "metaphors": {"node": "item", "edge": "—", "weight": "value",
                      "visit": "Checking", "start": "The input",
                      "done": "The answer."}
    },
    "search_2d_matrix_ii": {
        "scene": "library",
        "title": "The Staircase Walk",
        "hook": "From the top-right corner every step rules out a whole row or column.",
        "metaphors": {"node": "item", "edge": "—", "weight": "value",
                      "visit": "Checking", "start": "The input",
                      "done": "The answer."}
    },
    "row_max_ones": {
        "scene": "grid_power",
        "title": "Which Row Lights Up Most?",
        "hook": "Each row is off-then-on; binary-search where it switches on.",
        "metaphors": {"node": "item", "edge": "—", "weight": "value",
                      "visit": "Checking", "start": "The input",
                      "done": "The answer."}
    },
    "add_two_numbers": {
        "scene": "train",
        "title": "Adding Column by Column",
        "hook": "Digit plus digit plus carry, one carriage at a time — the way you add on paper.",
        "metaphors": {"node": "item", "edge": "—", "weight": "value",
                      "visit": "Checking", "start": "The input",
                      "done": "The answer."}
    },
    "add_one_list": {
        "scene": "train",
        "title": "The Carry That Walks Back",
        "hook": "The +1 lands on the last carriage; recursion lets the carry ripple back to the front.",
        "metaphors": {"node": "item", "edge": "—", "weight": "value",
                      "visit": "Checking", "start": "The input",
                      "done": "The answer."}
    },
    "next_smaller": {
        "scene": "stocks",
        "title": "The Next Cheaper Day",
        "hook": "Waiting days leave the stack the moment a cheaper price arrives.",
        "metaphors": {"node": "item", "edge": "—", "weight": "value",
                      "visit": "Checking", "start": "The input",
                      "done": "The answer."}
    },
    "nge_circular": {
        "scene": "stocks",
        "title": "Next Higher Price, Round the Clock",
        "hook": "The chart wraps around, so sweep it twice; the second lap only settles who's still waiting.",
        "metaphors": {"node": "item", "edge": "—", "weight": "value",
                      "visit": "Checking", "start": "The input",
                      "done": "The answer."}
    },
    "remove_k_digits": {
        "scene": "plates",
        "title": "Shrink the Number",
        "hook": "A bigger digit sitting before a smaller one costs the most — remove it first.",
        "metaphors": {"node": "item", "edge": "—", "weight": "value",
                      "visit": "Checking", "start": "The input",
                      "done": "The answer."}
    },
    "sum_subarray_mins": {
        "scene": "stocks",
        "title": "How Often Is Each Day the Low?",
        "hook": "Each price is the low of every window that stretches until a cheaper day — count those windows.",
        "metaphors": {"node": "item", "edge": "—", "weight": "value",
                      "visit": "Checking", "start": "The input",
                      "done": "The answer."}
    },
    "remove_duplicates_sorted": {
        "scene": "leaderboard",
        "title": "Keep One of Each",
        "hook": "Walk the sorted list; copy each new value forward into the unique prefix.",
        "metaphors": {"node": "item", "edge": "—", "weight": "value",
                      "visit": "Checking", "start": "The input",
                      "done": "The answer."}
    },
    "rotate_array_k": {
        "scene": "leaderboard",
        "title": "Rotate With Three Flips",
        "hook": "Flip the front, flip the back, flip the whole — the order ends up rotated.",
        "metaphors": {"node": "item", "edge": "—", "weight": "value",
                      "visit": "Checking", "start": "The input",
                      "done": "The answer."}
    },
    "move_zeros": {
        "scene": "leaderboard",
        "title": "Sink the Zeros",
        "hook": "Swap every non-zero down to the first empty slot; zeros drift to the end.",
        "metaphors": {"node": "item", "edge": "—", "weight": "value",
                      "visit": "Checking", "start": "The input",
                      "done": "The answer."}
    },
    "leaders": {
        "scene": "leaderboard",
        "title": "Who Towers Over Everyone Behind?",
        "hook": "Walk in from the right keeping the tallest so far — anyone taller is a leader.",
        "metaphors": {"node": "item", "edge": "—", "weight": "value",
                      "visit": "Checking", "start": "The input",
                      "done": "The answer."}
    },
    "longest_subarray_sum_k": {
        "scene": "stocks",
        "title": "The Longest Run That Adds Up",
        "hook": "Stretch the window right; if the sum overshoots, shrink it from the left.",
        "metaphors": {"node": "item", "edge": "—", "weight": "value",
                      "visit": "Checking", "start": "The input",
                      "done": "The answer."}
    },
    "second_largest": {
        "scene": "leaderboard",
        "title": "The Runner-Up",
        "hook": "Keep a champion and a runner-up as you scan — no sorting needed.",
        "metaphors": {"node": "item", "edge": "—", "weight": "value",
                      "visit": "Checking", "start": "The input",
                      "done": "The answer."}
    },
    "iter_preorder": {
        "scene": "files",
        "title": "Iterative Preorder Traversal",
        "hook": "Level order with null for gaps (up to 15 nodes). Watch the stack: right is pushed before left.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "iter_inorder": {
        "scene": "files",
        "title": "Iterative Inorder Traversal",
        "hook": "Level order with null for gaps. Slide left pushing; pop, visit, turn right.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "postorder_two_stacks": {
        "scene": "files",
        "title": "Postorder With Two Stacks",
        "hook": "Level order with null for gaps. Stack 2 collects root-right-left, then reads back reversed.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "postorder_one_stack": {
        "scene": "files",
        "title": "Postorder With One Stack",
        "hook": "Level order with null for gaps. Go right only if that subtree isn't finished yet.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "zigzag_traversal": {
        "scene": "files",
        "title": "Zigzag Level Order Traversal",
        "hook": "Level order with null for gaps. Every other level is read right to left.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "right_view": {
        "scene": "files",
        "title": "Right / Left View of a Binary Tree",
        "hook": "Level order with null for gaps. Last node per level = right view; first = left view.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "top_view": {
        "scene": "files",
        "title": "Top View of a Binary Tree",
        "hook": "Level order with null for gaps. First node seen at each horizontal distance.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "bottom_view": {
        "scene": "files",
        "title": "Bottom View of a Binary Tree",
        "hook": "Level order with null for gaps. The last node at each horizontal distance wins.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "vertical_order": {
        "scene": "files",
        "title": "Vertical Order Traversal",
        "hook": "Level order with null for gaps. Columns by horizontal distance, top to bottom.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "boundary_traversal": {
        "scene": "files",
        "title": "Boundary Traversal",
        "hook": "Level order with null for gaps. Root, left edge, leaves, right edge (bottom-up).",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "max_width": {
        "scene": "files",
        "title": "Maximum Width of a Binary Tree",
        "hook": "Level order with null for gaps. Slots are numbered as if the tree were complete.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "balanced_tree": {
        "scene": "files",
        "title": "Check for a Balanced Binary Tree",
        "hook": "Level order with null for gaps. Try 1,2,2,3,3,null,null,4,4 for an unbalanced one.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "symmetric_tree": {
        "scene": "files",
        "title": "Symmetric Binary Tree",
        "hook": "Level order with null for gaps. Try 1,2,2,null,3,null,3 for a lopsided one.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "max_path_sum": {
        "scene": "files",
        "title": "Maximum Path Sum",
        "hook": "Level order with null for gaps; negatives welcome. A path may bend at one node.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "root_to_leaf_paths": {
        "scene": "files",
        "title": "Root-to-Leaf Paths",
        "hook": "Level order with null for gaps. Each leaf closes one path.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "children_sum": {
        "scene": "files",
        "title": "Children Sum Property",
        "hook": "Level order with null for gaps. Values only ever go up — watch them change.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "nodes_at_distance_k": {
        "scene": "files",
        "title": "All Nodes at Distance K",
        "hook": "The tree, then | target k. The search can move up through parents too.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "burn_tree": {
        "scene": "files",
        "title": "Minimum Time to Burn a Binary Tree",
        "hook": "The tree, then | start node. Fire spreads to children and the parent each minute.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "count_complete_nodes": {
        "scene": "files",
        "title": "Count Nodes in a Complete Binary Tree",
        "hook": "A complete tree in level order. Perfect subtrees are counted without walking them.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "frog_jump_k": {
        "scene": "vault",
        "title": "Frog Jump With K Distances",
        "hook": "2–10 heights and K. Each stone looks back up to K stones for the cheapest jump.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "ninja_training": {
        "scene": "vault",
        "title": "Ninja's Training",
        "hook": "One row per day, three task scores each (rows split by /). No task twice in a row.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "min_falling_path": {
        "scene": "vault",
        "title": "Minimum Falling Path Sum",
        "hook": "A matrix up to 6×6, rows split by /. Each cell reads the three cells above.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "triangle_path": {
        "scene": "vault",
        "title": "Triangle (Minimum Path Sum)",
        "hook": "Row i has i+1 numbers, rows split by /. Move to the same or next index.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "partition_equal_subset": {
        "scene": "vault",
        "title": "Partition Equal Subset Sum",
        "hook": "Up to 6 numbers (1–12, total ≤ 24). Equal halves ⇔ some subset reaches total/2.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "count_subsets_sum_k": {
        "scene": "vault",
        "title": "Count Subsets With Sum K",
        "hook": "Up to 6 numbers (1–12) and K. Each cell adds ways without and with the new value.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "unbounded_knapsack": {
        "scene": "vault",
        "title": "Unbounded Knapsack",
        "hook": "weight:value items (up to 5) and a capacity up to 12. Taking an item reads the same row.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "rod_cutting": {
        "scene": "vault",
        "title": "Rod Cutting",
        "hook": "The price of a piece of length 1, 2, 3, … (up to 8). The rod length is the number of prices.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "print_lcs": {
        "scene": "dna",
        "title": "Print the Longest Common Subsequence",
        "hook": "Two words (up to 8 chars). Fill the table, then trace the answer back from the corner.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "longest_palindromic_subseq": {
        "scene": "dna",
        "title": "Longest Palindromic Subsequence",
        "hook": "One word (up to 8 chars) — compared with its own reverse.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "min_insert_palindrome": {
        "scene": "dna",
        "title": "Minimum Insertions to Make a Palindrome",
        "hook": "One word (up to 8 chars). Insertions = length − longest palindromic subsequence.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "min_ins_del": {
        "scene": "dna",
        "title": "Minimum Insertions/Deletions (A → B)",
        "hook": "Two words: A then B (up to 8 chars). Keep the LCS, delete/insert the rest.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "shortest_supersequence": {
        "scene": "dna",
        "title": "Shortest Common Supersequence",
        "hook": "Two words (up to 8 chars). The LCS is written once.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "distinct_subsequences": {
        "scene": "dna",
        "title": "Distinct Subsequences",
        "hook": "Text, then target (up to 8 chars each). Count the ways the target appears.",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "wildcard_match": {
        "scene": "dna",
        "title": "Wildcard Matching",
        "hook": "Text, then pattern with ? (one char) and * (any run).",
        "metaphors": {"node": "node", "edge": "link", "weight": "value",
                      "visit": "Visiting", "start": "The input",
                      "done": "The answer."}
    },
    "number_of_islands": {
        "scene": "grid_power",
        "title": "Number of Islands",
        "hook": "0/1 grid, rows split by / (up to 7×7). Each new island gets its own letter.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "rotten_oranges": {
        "scene": "grid_power",
        "title": "Rotten Oranges",
        "hook": "0 empty, 1 fresh, 2 rotten. Cells show the minute they rot; −1 if some never can.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "nearest_one_distance": {
        "scene": "grid_power",
        "title": "Distance of Nearest Cell Having 1",
        "hook": "0/1 grid. A BFS from every 1 at once fills in each cell's distance.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "surrounded_regions": {
        "scene": "grid_power",
        "title": "Surrounded Regions",
        "hook": "X/O grid. Only O regions touching the border survive; the rest flip to X.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "number_of_enclaves": {
        "scene": "grid_power",
        "title": "Number of Enclaves",
        "hook": "0/1 grid. Land that can't walk off the edge is counted (marked E).",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "binary_maze_path": {
        "scene": "maze",
        "title": "Shortest Path in a Binary Maze",
        "hook": "1 = open, 0 = wall (up to 6×6). BFS from top-left to bottom-right.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "min_effort_path": {
        "scene": "maze",
        "title": "Path With Minimum Effort",
        "hook": "Heights 0–99. A route costs its steepest single step — Dijkstra on that.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "swim_rising_water": {
        "scene": "maze",
        "title": "Swim in Rising Water",
        "hook": "Heights 0–99. A route costs its highest cell — Dijkstra on that.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "largest_island": {
        "scene": "maze",
        "title": "Making a Large Island",
        "hook": "0/1 grid. Cells show island sizes; each 0 is tried as the one flip.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "islands_ii": {
        "scene": "maze",
        "title": "Number of Islands II (Online)",
        "hook": "Grid size, then the cells turned to land in order. Union-find keeps the count.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "floyd_warshall": {
        "scene": "vault",
        "title": "Floyd–Warshall (All-Pairs Shortest Paths)",
        "hook": "Edges: A>B:3 one way, A-B:3 both ways (up to 6 nodes). Negatives allowed.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "city_fewest_neighbours": {
        "scene": "vault",
        "title": "City With the Fewest Neighbours in Reach",
        "hook": "Roads as A-B:len (both ways) and a distance threshold. Floyd–Warshall, then count.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "stock_ii": {
        "scene": "stocks",
        "title": "Best Time to Buy & Sell Stock II (Unlimited)",
        "hook": "Up to 8 prices. Two states per day: free or holding a share.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "stock_iii": {
        "scene": "stocks",
        "title": "Best Time to Buy & Sell Stock III (≤ 2 Trades)",
        "hook": "Up to 8 prices, at most two trades: buy1, sell1, buy2, sell2.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "stock_iv": {
        "scene": "stocks",
        "title": "Best Time to Buy & Sell Stock IV (≤ k Trades)",
        "hook": "Up to 8 prices and k (1–3) trades.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "stock_cooldown": {
        "scene": "stocks",
        "title": "Buy & Sell Stock With Cooldown",
        "hook": "Up to 8 prices. After a sale you must rest one day.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "stock_fee": {
        "scene": "stocks",
        "title": "Buy & Sell Stock With Transaction Fee",
        "hook": "Up to 8 prices and the fee paid on every sale.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "print_lis": {
        "scene": "vault",
        "title": "Print the Longest Increasing Subsequence",
        "hook": "Up to 8 numbers. Keep each position's predecessor to print one LIS back.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "largest_divisible_subset": {
        "scene": "vault",
        "title": "Largest Divisible Subset",
        "hook": "Up to 8 positive numbers (sorted for you). 'Smaller' becomes 'divides'.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "longest_string_chain": {
        "scene": "vault",
        "title": "Longest String Chain",
        "hook": "Up to 8 words. A word extends a chain if deleting one letter gives the previous one.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "longest_bitonic": {
        "scene": "vault",
        "title": "Longest Bitonic Subsequence",
        "hook": "Up to 8 numbers. Rising into i plus falling out of i, minus 1.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "number_of_lis": {
        "scene": "vault",
        "title": "Number of Longest Increasing Subsequences",
        "hook": "Up to 8 numbers. Track the best length and how many ways reach it.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "cycle_undirected_bfs": {
        "scene": "grid_power",
        "title": "Cycle Detection in an Undirected Graph (BFS)",
        "hook": "Explore by BFS, remembering where you came from; a visited neighbour that isn't your parent closes a loop.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "cycle_undirected_dfs": {
        "scene": "grid_power",
        "title": "Cycle Detection in an Undirected Graph (DFS)",
        "hook": "Walk depth-first; meeting an already-visited node that isn't where you just came from means a loop.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "bridges": {
        "scene": "grid_power",
        "title": "Bridges in a Graph (Tarjan)",
        "hook": "A cable is critical when nothing below it can reach back above it — low-link beats discovery time.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "articulation_points": {
        "scene": "grid_power",
        "title": "Articulation Points",
        "hook": "A hub is critical when some branch below it can only reach the rest through it.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "connect_network_ops": {
        "scene": "grid_power",
        "title": "Operations to Make a Network Connected",
        "hook": "Every spare cable can join two groups; you need one move per extra group.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "cycle_directed": {
        "scene": "scheduler",
        "title": "Cycle Detection in a Directed Graph (DFS)",
        "hook": "One-way streets: only an edge back into your current route makes a loop.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "safe_states": {
        "scene": "scheduler",
        "title": "Find Eventual Safe States",
        "hook": "A room is safe if every corridor out of it eventually dead-ends — never into a loop.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "kosaraju": {
        "scene": "scheduler",
        "title": "Strongly Connected Components (Kosaraju)",
        "hook": "Finish order on the graph, then explore the reversed graph from the last finisher: each sweep is one tightly-knit group.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "shortest_path_dag": {
        "scene": "scheduler",
        "title": "Shortest Path in a DAG",
        "hook": "With no loops, relaxing edges in topological order settles every distance in one pass.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "floor_ceil_bst": {
        "scene": "files",
        "title": "Floor and Ceil in a BST",
        "hook": "Values inserted into a BST, then | x. One walk down for the floor, one for the ceil.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "kth_bst": {
        "scene": "files",
        "title": "Kth Smallest and Largest in a BST",
        "hook": "Values inserted into a BST, then | k. Inorder visits in sorted order.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "lca_bst": {
        "scene": "files",
        "title": "LCA in a BST",
        "hook": "Values inserted into a BST, then | a b. Go the way both lie until they split.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "successor_predecessor": {
        "scene": "files",
        "title": "Inorder Successor / Predecessor in a BST",
        "hook": "Values inserted into a BST, then | x. Smallest above x, largest below x.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "two_sum_bst": {
        "scene": "files",
        "title": "Two Sum in a BST",
        "hook": "Values inserted into a BST, then | k. Sorted inorder plus two pointers.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "bst_from_preorder": {
        "scene": "files",
        "title": "Construct a BST From Preorder",
        "hook": "A preorder listing; each value is placed by walking down from the root.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "validate_bst": {
        "scene": "files",
        "title": "Check if a Tree is a BST",
        "hook": "Any tree in level order. Each node must fit the window its ancestors set.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "recover_bst": {
        "scene": "files",
        "title": "Recover a BST With Two Swapped Nodes",
        "hook": "A BST with two values swapped, in level order. Inorder reveals the pair.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "largest_bst": {
        "scene": "files",
        "title": "Largest BST in a Binary Tree",
        "hook": "Any tree in level order. Subtrees report (is BST, size, min, max) upward.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "is_min_heap": {
        "scene": "scheduler",
        "title": "Check if an Array is a Min-Heap",
        "hook": "Up to 12 numbers read as a complete tree. Every parent must be ≤ its children.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "min_to_max_heap": {
        "scene": "scheduler",
        "title": "Convert a Min-Heap to a Max-Heap",
        "hook": "A min-heap array. Bottom-up heapify turns it into a max-heap.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "connect_sticks": {
        "scene": "scheduler",
        "title": "Minimum Cost to Connect Sticks",
        "hook": "Stick lengths (1–999). Always join the two cheapest — the heap tree shrinks each round.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "rank_replace": {
        "scene": "scheduler",
        "title": "Replace Elements by Their Rank",
        "hook": "Up to 12 numbers. Each becomes its rank among the distinct values.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "top_k_frequent": {
        "scene": "scheduler",
        "title": "Top K Frequent Elements",
        "hook": "Up to 12 numbers and k. Count, then keep a size-k min-heap.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "hand_of_straights": {
        "scene": "scheduler",
        "title": "Hand of Straights",
        "hook": "Cards and the group size. Start each group at the smallest card left.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "task_scheduler": {
        "scene": "scheduler",
        "title": "Task Scheduler",
        "hook": "Tasks as letters and the cooldown n. Idle only when nothing can run.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "median_stream": {
        "scene": "scheduler",
        "title": "Find Median From a Data Stream",
        "hook": "Numbers arriving one by one. Two heaps keep the median on top.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "remove_outer_parens": {
        "scene": "dna",
        "title": "Remove Outermost Parentheses",
        "hook": "A balanced string of ( and ) (up to 12). Drop each group's outer pair.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "reverse_words": {
        "scene": "dna",
        "title": "Reverse Words in a String",
        "hook": "A sentence (up to 24 chars). Extra spaces vanish; word order reverses.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "largest_odd_number": {
        "scene": "dna",
        "title": "Largest Odd Number in a String",
        "hook": "Digits (up to 12). Cut after the rightmost odd digit.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "longest_common_prefix": {
        "scene": "dna",
        "title": "Longest Common Prefix",
        "hook": "2–5 words. Compare one column at a time.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "isomorphic_strings": {
        "scene": "dna",
        "title": "Isomorphic Strings",
        "hook": "Two words. A consistent one-to-one letter mapping, both ways.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "rotate_string": {
        "scene": "dna",
        "title": "Rotate String",
        "hook": "Two words. The second is a rotation iff it appears in first + first.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "sort_by_frequency": {
        "scene": "dna",
        "title": "Sort Characters by Frequency",
        "hook": "Up to 12 letters/digits. Most frequent characters first.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "max_nesting_depth": {
        "scene": "dna",
        "title": "Maximum Nesting Depth of Parentheses",
        "hook": "Up to 12 characters with balanced parentheses.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "roman_to_integer": {
        "scene": "dna",
        "title": "Roman to Integer",
        "hook": "Roman numerals (up to 12). Subtract when a smaller one precedes a bigger one.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "string_to_integer": {
        "scene": "dna",
        "title": "String to Integer (atoi)",
        "hook": "Any text (up to 24). Spaces, one sign, digits, stop, clamp.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "sum_of_beauty": {
        "scene": "dna",
        "title": "Sum of Beauty of All Substrings",
        "hook": "Up to 8 letters. Cell (i, j) is the beauty of s[i..j].",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "char_replacement": {
        "scene": "stocks",
        "title": "Longest Repeating Character Replacement",
        "hook": "Letters and k. Window length − top count must stay ≤ k.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "binary_subarray_sum": {
        "scene": "stocks",
        "title": "Binary Subarrays With Sum",
        "hook": "0/1 values and the goal. Exactly = at-most(goal) − at-most(goal−1).",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "nice_subarrays": {
        "scene": "stocks",
        "title": "Count Number of Nice Subarrays",
        "hook": "Numbers and k. Count windows with exactly k odd numbers.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "substrings_all_three": {
        "scene": "stocks",
        "title": "Substrings Containing All Three Characters",
        "hook": "Letters a/b/c only. Track where each was last seen.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "max_card_points": {
        "scene": "stocks",
        "title": "Maximum Points From Cards",
        "hook": "Card points and k. Take k from the ends — trade left cards for right ones.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "subarrays_k_distinct": {
        "scene": "stocks",
        "title": "Subarrays With K Different Integers",
        "hook": "Numbers and k. Exactly k distinct = at-most(k) − at-most(k−1).",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "min_window_substring": {
        "scene": "stocks",
        "title": "Minimum Window Substring",
        "hook": "Text (≤ 16) and pattern (≤ 6). Grow to cover, shrink while covered.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "min_window_subsequence": {
        "scene": "stocks",
        "title": "Minimum Window Subsequence",
        "hook": "Text (≤ 16) and pattern (≤ 6). Forward scan, then tighten backward.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "word_ladder": {
        "scene": "vault",
        "title": "Word Ladder I",
        "hook": "begin,end | dictionary. BFS: one letter changes per level.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "word_ladder_ii": {
        "scene": "vault",
        "title": "Word Ladder II (All Shortest Sequences)",
        "hook": "begin,end | dictionary. Every shortest sequence is read back from BFS parents.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "alien_dictionary": {
        "scene": "vault",
        "title": "Alien Dictionary",
        "hook": "Words in alien sorted order. Each adjacent pair gives one letter rule.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "cheapest_flight_k": {
        "scene": "vault",
        "title": "Cheapest Flights Within K Stops",
        "hook": "Flights a>b:price, then | src dst k. k+1 Bellman-Ford rounds.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "ways_to_arrive": {
        "scene": "vault",
        "title": "Number of Ways to Arrive at Destination",
        "hook": "Roads a-b:time, then | src dst. Dijkstra that counts ties.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "min_multiplications": {
        "scene": "vault",
        "title": "Minimum Multiplications to Reach End",
        "hook": "start end | factors. BFS over values mod 100000.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "most_stones": {
        "scene": "vault",
        "title": "Most Stones Removed With Same Row or Column",
        "hook": "Stones as r:c. Same row or column = connected; answer = stones − groups.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "network_delay": {
        "scene": "scheduler",
        "title": "Network Delay Time",
        "hook": "Dijkstra from the source on one-way links; the delay is when the farthest node hears the signal.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "cut_stick": {
        "scene": "grid_power",
        "title": "Minimum Cost to Cut a Stick",
        "hook": "Length | cuts. Cell (i, j) = cheapest way to make every cut between cut i and cut j.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "burst_balloons": {
        "scene": "grid_power",
        "title": "Burst Balloons",
        "hook": "Up to 6 digits. Pick the LAST balloon to burst in each range.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "boolean_evaluation": {
        "scene": "grid_power",
        "title": "Evaluate Boolean Expression to True",
        "hook": "Alternate T/F with & | ^. Count the ways each range can be True / False.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "palindrome_partition_ii": {
        "scene": "dna",
        "title": "Palindrome Partitioning II (Min Cuts)",
        "hook": "Up to 10 letters. Fewest cuts so every piece is a palindrome.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "partition_array_max_sum": {
        "scene": "grid_power",
        "title": "Partition Array for Maximum Sum",
        "hook": "Values 0–99 and k. Each piece becomes its max; maximise the total.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "min_subset_diff": {
        "scene": "grid_power",
        "title": "Partition Into Two Subsets With Minimum Difference",
        "hook": "Up to 6 values 0–12. Reachable subset sums → closest split.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "count_partitions_diff": {
        "scene": "grid_power",
        "title": "Count Partitions With Given Difference",
        "hook": "Values and difference d. Count subsets summing to (total − d)/2.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "target_sum": {
        "scene": "grid_power",
        "title": "Target Sum",
        "hook": "Values and target. Signs split the array into two subsets.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "max_rectangle_ones": {
        "scene": "grid_power",
        "title": "Maximal Rectangle of 1s",
        "hook": "0/1 rows split by '/'. Each row becomes a histogram of heights.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "largest_element": {
        "scene": "leaderboard",
        "title": "Largest Element in an Array",
        "hook": "Up to 12 numbers. One pass keeps the biggest so far.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "check_sorted": {
        "scene": "leaderboard",
        "title": "Check if an Array is Sorted",
        "hook": "Up to 12 numbers. Every neighbour pair must be in order.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "linear_search": {
        "scene": "leaderboard",
        "title": "Linear Search",
        "hook": "Numbers and x. Check each position in turn.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "union_sorted": {
        "scene": "leaderboard",
        "title": "Union of Two Sorted Arrays",
        "hook": "Two sorted arrays split by '|'. Take the smaller, skip repeats.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "intersection_sorted": {
        "scene": "leaderboard",
        "title": "Intersection of Two Sorted Arrays",
        "hook": "Two sorted arrays split by '|'. Advance the smaller side.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "missing_number": {
        "scene": "vault",
        "title": "Find the Missing Number",
        "hook": "Distinct 0..n with one missing. XOR cancels every pair.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "max_consecutive_ones": {
        "scene": "leaderboard",
        "title": "Maximum Consecutive Ones",
        "hook": "0/1 values. Count the run; anything else resets it.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "rearrange_by_sign": {
        "scene": "leaderboard",
        "title": "Rearrange Array Elements by Sign",
        "hook": "Equal positives and negatives. + to even slots, − to odd slots.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "max_product_subarray": {
        "scene": "stocks",
        "title": "Maximum Product Subarray",
        "hook": "Up to 12 numbers. Track max AND min — a negative swaps them.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "longest_sum_k_any": {
        "scene": "vault",
        "title": "Longest Subarray With Sum K (any sign)",
        "hook": "Any signs and k. Map each prefix sum to where it first appeared.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "count_sum_k": {
        "scene": "vault",
        "title": "Count Subarrays With Sum K",
        "hook": "Any signs and k. Count earlier prefixes equal to prefix − k.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "largest_zero_sum": {
        "scene": "vault",
        "title": "Largest Subarray With Sum 0",
        "hook": "Any signs. A repeated prefix sum means a zero-sum stretch between.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "count_xor_k": {
        "scene": "vault",
        "title": "Count Subarrays With XOR K",
        "hook": "Numbers and k. Count earlier prefix XORs equal to prefix ⊕ k.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "longest_consecutive": {
        "scene": "vault",
        "title": "Longest Consecutive Sequence",
        "hook": "Up to 12 numbers. Only count from a run's first value.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "majority_n3": {
        "scene": "leaderboard",
        "title": "Majority Elements (> n/3)",
        "hook": "Up to 12 numbers. Two candidates, then verify their counts.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "repeating_missing": {
        "scene": "vault",
        "title": "Find the Repeating and Missing Numbers",
        "hook": "1..n with one value repeated. Sum and sum-of-squares give two equations.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "three_sum": {
        "scene": "leaderboard",
        "title": "3 Sum",
        "hook": "Up to 12 numbers. Sort, fix one, two pointers for the rest.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "four_sum": {
        "scene": "leaderboard",
        "title": "4 Sum",
        "hook": "Numbers and target. Fix two, two pointers for the rest.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "set_matrix_zeros": {
        "scene": "grid_power",
        "title": "Set Matrix Zeros",
        "hook": "Rows split by '/'. Mark rows and columns first, then clear.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "rotate_matrix": {
        "scene": "grid_power",
        "title": "Rotate a Matrix by 90°",
        "hook": "A square matrix. Transpose, then reverse each row.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "spiral_order": {
        "scene": "grid_power",
        "title": "Spiral Traversal of a Matrix",
        "hook": "Rows split by '/'. Walk the ring, then shrink the bounds.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "pascal_triangle": {
        "scene": "grid_power",
        "title": "Pascal's Triangle",
        "hook": "Set ROWS (1–8). Each inner value = the two above it.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "merge_no_space": {
        "scene": "leaderboard",
        "title": "Merge Two Sorted Arrays Without Extra Space",
        "hook": "Two sorted arrays split by '|'. Gap method, halving each round.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "count_inversions": {
        "scene": "leaderboard",
        "title": "Count Inversions",
        "hook": "Up to 12 numbers. Count pairs across halves during merge sort.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "reverse_pairs": {
        "scene": "leaderboard",
        "title": "Reverse Pairs",
        "hook": "Up to 12 numbers. Count a[i] > 2·a[j] across halves during merge sort.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "count_digits": {
        "scene": "vault",
        "title": "Count Digits of a Number",
        "hook": "A whole number. Each ÷10 removes one digit.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "reverse_number": {
        "scene": "vault",
        "title": "Reverse a Number",
        "hook": "A whole number. Peel n % 10 onto the reversed number.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "palindrome_number": {
        "scene": "vault",
        "title": "Palindrome Number",
        "hook": "A whole number. Reverse it and compare.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "armstrong_number": {
        "scene": "vault",
        "title": "Armstrong Number",
        "hook": "A whole number. Sum of digits^(digit count).",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "print_divisors": {
        "scene": "vault",
        "title": "Print All Divisors",
        "hook": "1–999. Divisors pair up, so stop at √n.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "check_prime": {
        "scene": "vault",
        "title": "Check for a Prime Number",
        "hook": "0–9999. Trial-divide up to √n.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "factorial": {
        "scene": "vault",
        "title": "Factorial of a Number",
        "hook": "0–12. Multiply 1 × 2 × … × n.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "sum_first_n": {
        "scene": "vault",
        "title": "Sum of the First N Numbers",
        "hook": "0–1000. Pair the ends: n(n + 1)/2.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "reverse_array": {
        "scene": "leaderboard",
        "title": "Reverse an Array (Two Pointers)",
        "hook": "Up to 12 numbers. Swap the ends, move inward.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "palindrome_string": {
        "scene": "dna",
        "title": "Check if a String is a Palindrome",
        "hook": "Up to 16 characters. Ignore case and symbols; compare the ends.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "frequency_count": {
        "scene": "leaderboard",
        "title": "Count Frequencies / Highest Occurring Element",
        "hook": "Up to 12 numbers. One pass with value → count.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "check_ith_bit": {
        "scene": "vault",
        "title": "Check if the i-th Bit is Set",
        "hook": "0–255 and bit i (0–7). AND with 1 << i.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "check_odd": {
        "scene": "vault",
        "title": "Check if a Number is Odd (Bitwise)",
        "hook": "0–255. The lowest bit decides parity.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "swap_xor": {
        "scene": "vault",
        "title": "Swap Two Numbers With XOR",
        "hook": "Two numbers 0–255. Three XORs, no temp.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "divide_bits": {
        "scene": "vault",
        "title": "Divide Without * or /",
        "hook": "Dividend, divisor (0–255). Subtract shifted divisors.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "xor_range": {
        "scene": "vault",
        "title": "XOR of Numbers in a Range",
        "hook": "N, or L, R (0–999). f(n) repeats every 4.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "single_number_iii": {
        "scene": "vault",
        "title": "Single Number III (Two Uniques)",
        "hook": "Pairs plus two singletons. Split by the lowest differing bit.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "ll_insert_head": {
        "scene": "train",
        "title": "Insert at the Head of a Linked List",
        "hook": "The list, and the value to insert. New node → old head, then move head.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "ll_delete_head": {
        "scene": "train",
        "title": "Delete the Head of a Linked List",
        "hook": "The list. Move head one step; free the old head.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "ll_length": {
        "scene": "train",
        "title": "Length of a Linked List",
        "hook": "The list. Walk to null, counting.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "ll_search": {
        "scene": "train",
        "title": "Search in a Linked List",
        "hook": "The list and x. No indexing — walk and compare.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "dll_insert_head": {
        "scene": "train",
        "title": "Insert Before the Head of a Doubly Linked List",
        "hook": "The DLL and a value. Fix next AND prev.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "dll_delete_head": {
        "scene": "train",
        "title": "Delete the Head of a Doubly Linked List",
        "hook": "The DLL. Move head; clear the new head's prev.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "dll_pairs_sum": {
        "scene": "train",
        "title": "Pairs With a Given Sum in a Sorted DLL",
        "hook": "A sorted DLL and the sum. Head and tail walk inward.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "dll_remove_duplicates": {
        "scene": "train",
        "title": "Remove Duplicates From a Sorted DLL",
        "hook": "A sorted DLL. Unlink each repeat (next and prev).",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "ll_reverse_recursive": {
        "scene": "train",
        "title": "Reverse a Linked List (Recursive)",
        "hook": "The list. Reverse the rest, then flip one arrow on the way back.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "loop_length": {
        "scene": "train",
        "title": "Length of a Loop in a Linked List",
        "hook": "The list and where the tail links back (−1 = none). Floyd, then count the ring.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "sort_012_list": {
        "scene": "train",
        "title": "Sort a Linked List of 0s, 1s and 2s",
        "hook": "0s, 1s and 2s. Build three chains by relinking, then join.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "sort_list": {
        "scene": "train",
        "title": "Sort a Linked List (Merge Sort)",
        "hook": "The list. Merge sort: split at the middle, merge by relinking.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "y_intersection": {
        "scene": "train",
        "title": "Intersection Point of a Y-Shaped Linked List",
        "hook": "A only | B only | shared tail. Pointers swap heads at the end.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "reverse_k_group": {
        "scene": "train",
        "title": "Reverse a Linked List in Groups of K",
        "hook": "The list and k. Reverse each full group; a short tail stays.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "search_rotated_ii": {
        "scene": "vault",
        "title": "Search in Rotated Sorted Array II (duplicates)",
        "hook": "A rotated array (duplicates allowed) and the target.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "median_two_sorted": {
        "scene": "vault",
        "title": "Median of Two Sorted Arrays",
        "hook": "Two sorted arrays split by '|'. Binary-search the cut.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "kth_two_sorted": {
        "scene": "vault",
        "title": "K-th Element of Two Sorted Arrays",
        "hook": "Two sorted arrays and k. The left part holds k values.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "gas_station": {
        "scene": "vault",
        "title": "Minimise Max Distance to Gas Station",
        "hook": "Station positions and k new stations. Binary-search the real answer.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "peak_element_ii": {
        "scene": "vault",
        "title": "Find a Peak Element II (matrix)",
        "hook": "Rows split by '/', neighbours distinct. Column max, then climb.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "matrix_median": {
        "scene": "vault",
        "title": "Median of a Row-Wise Sorted Matrix",
        "hook": "Sorted rows split by '/', odd cell count. Binary-search the value.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "print_1_to_n": {
        "scene": "vault",
        "title": "Print 1 to N Using Recursion",
        "hook": "N (1–10). Print before the call → ascending.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "print_n_to_1": {
        "scene": "vault",
        "title": "Print N to 1 Using Recursion",
        "hook": "N (1–10). Print after the call → descending.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "recursive_bubble_sort": {
        "scene": "leaderboard",
        "title": "Recursive Bubble Sort",
        "hook": "Up to 10 numbers. One pass, then bubble(n − 1).",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "recursive_insertion_sort": {
        "scene": "leaderboard",
        "title": "Recursive Insertion Sort",
        "hook": "Up to 10 numbers. Insert a[i], then insert(i + 1).",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "count_good_numbers": {
        "scene": "vault",
        "title": "Count Good Numbers",
        "hook": "Length n (≤ 10^15). 5^ceil(n/2) · 4^floor(n/2) by fast power.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "sort_stack": {
        "scene": "plates",
        "title": "Sort a Stack Using Recursion",
        "hook": "Stack bottom → top (≤ 8). Pop, sort the rest, insert in order.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "reverse_stack": {
        "scene": "plates",
        "title": "Reverse a Stack Using Recursion",
        "hook": "Stack bottom → top (≤ 8). Pop, reverse the rest, insert at the bottom.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "recursive_atoi": {
        "scene": "dna",
        "title": "Recursive atoi()",
        "hook": "Any text (≤ 16). Spaces, sign, then one digit per call.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "word_break": {
        "scene": "dna",
        "title": "Word Break",
        "hook": "Text | words. can(i) = a word starts at i and can(i + len).",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "m_coloring": {
        "scene": "vault",
        "title": "M-Coloring Problem",
        "hook": "Edges like 0-1,1-2 and m colours. Try, recurse, undo.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "sudoku_solver": {
        "scene": "grid_power",
        "title": "Sudoku Solver",
        "hook": "4×4 or 9×9, 0 = blank (9×9 rows may skip commas).",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "expression_add_operators": {
        "scene": "vault",
        "title": "Expression Add Operators",
        "hook": "1–5 digits and the target. Choose + − × or join between digits.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "valid_paren_star": {
        "scene": "vault",
        "title": "Valid Parenthesis String (with *)",
        "hook": "Only ( ) *. Track the range of possible open counts.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "shortest_job_first": {
        "scene": "scheduler",
        "title": "Shortest Job First (SJF) Scheduling",
        "hook": "Burst times. Shortest first minimises the average wait.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "lru_page_faults": {
        "scene": "scheduler",
        "title": "LRU Page Replacement (Page Faults)",
        "hook": "Page requests and capacity. Evict the least recently used.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "insert_interval": {
        "scene": "scheduler",
        "title": "Insert Interval",
        "hook": "Sorted intervals | new interval. Copy, absorb, copy.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "non_overlapping_intervals": {
        "scene": "scheduler",
        "title": "Non-overlapping Intervals",
        "hook": "Intervals like 1-2,2-3. Sort by end; keep what fits.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "greater_to_right": {
        "scene": "leaderboard",
        "title": "Number of Greater Elements to the Right",
        "hook": "Up to 10 numbers. For each index, count bigger values to its right.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "sum_subarray_ranges": {
        "scene": "stocks",
        "title": "Sum of Subarray Ranges",
        "hook": "Up to 10 numbers. Σ max·count − Σ min·count via monotonic stacks.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "celebrity": {
        "scene": "vault",
        "title": "The Celebrity Problem",
        "hook": "Square 0/1 'knows' matrix. Eliminate, then verify.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "build_pre_in": {
        "scene": "files",
        "title": "Construct a Binary Tree from Preorder & Inorder",
        "hook": "Preorder | inorder (distinct values). Root first, inorder splits the rest.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "build_post_in": {
        "scene": "files",
        "title": "Construct a Binary Tree from Postorder & Inorder",
        "hook": "Postorder | inorder (distinct values). Root last, inorder splits the rest.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "serialize_tree": {
        "scene": "files",
        "title": "Serialize and Deserialize a Binary Tree",
        "hook": "Level order, null for gaps. BFS writes '#' for missing children.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "morris_inorder": {
        "scene": "files",
        "title": "Morris Inorder Traversal",
        "hook": "Level order. Dashed edges are temporary threads.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "morris_preorder": {
        "scene": "files",
        "title": "Morris Preorder Traversal",
        "hook": "Level order. Visit when the thread is made, not when it's removed.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "flatten_tree": {
        "scene": "files",
        "title": "Flatten a Binary Tree to a Linked List",
        "hook": "Level order. Splice each left subtree into the right chain.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "identical_trees": {
        "scene": "files",
        "title": "Check if Two Trees are Identical",
        "hook": "Two level-order trees split by '|'. Compare in lockstep.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "merge_two_bsts": {
        "scene": "files",
        "title": "Merge Two BSTs (sorted output)",
        "hook": "Two BSTs as insertion orders split by '|'. Inorders, then merge.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "stack_array": {
        "scene": "plates",
        "title": "Implement a Stack Using an Array",
        "hook": "Ops: push x, pop, top. Array + top index.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "queue_array": {
        "scene": "scheduler",
        "title": "Implement a Queue Using an Array",
        "hook": "Ops: push x, pop, front. Circular array.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "stack_using_queue": {
        "scene": "plates",
        "title": "Implement a Stack Using a Queue",
        "hook": "Ops: push x, pop, top. Rotate after each push.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "queue_using_stacks": {
        "scene": "scheduler",
        "title": "Implement a Queue Using Stacks",
        "hook": "Ops: push x, pop, front. Pour in→out only when out is empty.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "stack_linkedlist": {
        "scene": "train",
        "title": "Implement a Stack Using a Linked List",
        "hook": "Ops: push x, pop, top. New nodes go at the head.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "queue_linkedlist": {
        "scene": "train",
        "title": "Implement a Queue Using a Linked List",
        "hook": "Ops: push x, pop, front. Enqueue at rear, dequeue at front.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "min_stack": {
        "scene": "plates",
        "title": "Implement a Min Stack",
        "hook": "Ops: push x, pop, top, getmin. Each entry keeps the min below it.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "lru_cache": {
        "scene": "scheduler",
        "title": "LRU Cache",
        "hook": "Ops: put k v, get k. Evict the least recently used.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "lfu_cache": {
        "scene": "scheduler",
        "title": "LFU Cache",
        "hook": "Ops: put k v, get k. Evict the least used (ties: least recent).",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "design_twitter": {
        "scene": "scheduler",
        "title": "Design Twitter",
        "hook": "Ops: post u t, follow a b, unfollow a b, feed u.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "clone_random_list": {
        "scene": "train",
        "title": "Clone a Linked List With Random Pointers",
        "hook": "Values | random index per node (−1 = null). Weave, point, unweave.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "flatten_list": {
        "scene": "train",
        "title": "Flatten a Linked List (sorted columns)",
        "hook": "Sorted columns split by '|'. Merge from the right.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "merge_k_lists": {
        "scene": "train",
        "title": "Merge K Sorted Lists",
        "hook": "Sorted lists split by '|'. Min-heap of heads.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "bracket_reversals": {
        "scene": "dna",
        "title": "Minimum Bracket Reversals to Balance",
        "hook": "Only { and }. Cancel pairs; ceil(close/2) + ceil(open/2).",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "count_and_say": {
        "scene": "dna",
        "title": "Count and Say",
        "hook": "n (1–8). Read the previous term run by run.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "longest_happy_prefix": {
        "scene": "dna",
        "title": "Longest Happy Prefix (LPS)",
        "hook": "Up to 16 letters. The KMP lps array's last value.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "count_palindromic_subseq": {
        "scene": "dna",
        "title": "Count Palindromic Subsequences",
        "hook": "Up to 10 letters. Interval DP with inclusion–exclusion.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "distinct_substrings": {
        "scene": "vault",
        "title": "Number of Distinct Substrings (Trie)",
        "hook": "Up to 8 letters. Insert every suffix; count new trie nodes.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "max_xor_pair": {
        "scene": "vault",
        "title": "Maximum XOR of Two Numbers (Trie)",
        "hook": "Numbers 0–255. Bit trie; walk towards the opposite bit.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "max_xor_queries": {
        "scene": "vault",
        "title": "Maximum XOR With an Element From an Array",
        "hook": "Array | queries 'x m'. Sort by m, insert values ≤ m.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "trie_advanced": {
        "scene": "files",
        "title": "Trie With Counts (insert, count, erase)",
        "hook": "Ops: insert w, countwords w, countprefix p, erase w. Nodes keep prefix|end counts.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "ninja_friends": {
        "scene": "grid_power",
        "title": "Ninja and His Friends (Cherry Pickup II)",
        "hook": "Rows split by '/'. Two walkers from the top corners; a shared cell counts once.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "max_sum_combination": {
        "scene": "leaderboard",
        "title": "Maximum Sum Combinations",
        "hook": "Two arrays | and k. Max-heap over index pairs.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "accounts_merge": {
        "scene": "vault",
        "title": "Accounts Merge",
        "hook": "Accounts 'Name email …' split by ';'. Union accounts sharing an email.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "a_star_grid": {
        "scene": "grid_power",
        "title": "A* Search on a Grid",
        "hook": "Rows of S . # G split by '/'. Expand the smallest f = g + h.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "best_first_grid": {
        "scene": "grid_power",
        "title": "Greedy Best-First Search on a Grid",
        "hook": "Rows of S . # G. Expand the smallest h only — fast, not always shortest.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "zero_one_bfs": {
        "scene": "grid_power",
        "title": "0-1 BFS (Minimum Cost Path)",
        "hook": "0/1 costs, rows split by '/'. Deque: 0-cost to the front.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "max_flow": {
        "scene": "vault",
        "title": "Maximum Flow (Edmonds–Karp)",
        "hook": "Edges from>to:capacity with source S and sink T. Augment along BFS paths.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "min_cut": {
        "scene": "vault",
        "title": "Minimum s-t Cut",
        "hook": "Edges from>to:capacity (S, T). Max flow, then what S can still reach.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "bipartite_matching": {
        "scene": "vault",
        "title": "Maximum Bipartite Matching (Kuhn)",
        "hook": "Left: allowed rights, separated by ';'. Kuhn's augmenting paths.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "lca_lifting": {
        "scene": "files",
        "title": "Lowest Common Ancestor (Binary Lifting)",
        "hook": "Level-order tree | two node values. Jump pointers are dashed.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "kth_ancestor": {
        "scene": "files",
        "title": "K-th Ancestor (Binary Lifting)",
        "hook": "Level-order tree | node k. Hop by the bits of k.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "tsp_bitmask": {
        "scene": "grid_power",
        "title": "Travelling Salesman (Bitmask DP)",
        "hook": "Distance matrix (≤ 5 cities). Rows are visited-sets as bitmasks.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "assignment_bitmask": {
        "scene": "grid_power",
        "title": "Job Assignment (Bitmask DP)",
        "hook": "cost[person][job] (≤ 4×4). Rows are job-sets as bitmasks.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "sparse_table": {
        "scene": "leaderboard",
        "title": "Sparse Table (Range Minimum Query)",
        "hook": "Array | min l r, … Two overlapping power-of-two blocks.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "sqrt_decomposition": {
        "scene": "leaderboard",
        "title": "Sqrt Decomposition (Range Sum)",
        "hook": "Array | sum l r, set i v. Whole blocks by their sum.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "lazy_segment_tree": {
        "scene": "leaderboard",
        "title": "Segment Tree With Lazy Propagation",
        "hook": "Array | add l r v, sum l r. Pending adds wait as 'lazy'.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "extended_gcd": {
        "scene": "vault",
        "title": "Extended Euclidean Algorithm",
        "hook": "a, b. Euclid down, then x, y back up: a·x + b·y = gcd.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "mod_inverse": {
        "scene": "vault",
        "title": "Modular Multiplicative Inverse",
        "hook": "a, m. The x of extended Euclid when gcd = 1.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "ncr_mod": {
        "scene": "vault",
        "title": "nCr mod p (Fermat Inverse)",
        "hook": "n, r (≤ 20). Factorials mod p, Fermat inverse for the division.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "euler_totient": {
        "scene": "vault",
        "title": "Euler's Totient Function",
        "hook": "n. φ = n·Π(1 − 1/p) over its distinct primes.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "spf_sieve": {
        "scene": "vault",
        "title": "Smallest Prime Factor Sieve",
        "hook": "n (≤ 60) and x to factorise. Sieve smallest prime factors.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "crt": {
        "scene": "vault",
        "title": "Chinese Remainder Theorem",
        "hook": "Congruences 'r m', comma-separated. Merge them pairwise.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "suffix_array": {
        "scene": "dna",
        "title": "Suffix Array (Prefix Doubling)",
        "hook": "2–10 letters. Rank by 1, 2, 4, … characters.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "lcp_kasai": {
        "scene": "dna",
        "title": "LCP Array (Kasai)",
        "hook": "2–10 letters. Walk suffixes in text order; h drops by ≤ 1.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "longest_repeated_substring": {
        "scene": "dna",
        "title": "Longest Repeated Substring (SA + LCP)",
        "hook": "2–10 letters. The biggest LCP between sorted neighbours.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "euler_path": {
        "scene": "vault",
        "title": "Euler Path / Circuit (Hierholzer)",
        "hook": "Undirected edges A-B, … 0 or 2 odd-degree vertices needed.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "longest_path_dag": {
        "scene": "vault",
        "title": "Longest Path in a DAG",
        "hook": "Directed edges from>to:weight, start S. Topo order, relax with max.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "count_paths_dag": {
        "scene": "vault",
        "title": "Count Paths in a DAG",
        "hook": "Directed edges with S and T. ways[v] = Σ ways[u].",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "matrix_exponentiation": {
        "scene": "vault",
        "title": "Matrix Exponentiation (Fibonacci)",
        "hook": "n (0–90). F(n) from [[1,1],[1,0]]ⁿ by square-and-multiply.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "ternary_search": {
        "scene": "vault",
        "title": "Ternary Search (Peak of a Unimodal Array)",
        "hook": "Rises strictly, then falls strictly. Keep two thirds each round.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "meet_in_middle": {
        "scene": "vault",
        "title": "Meet in the Middle (Subset Sums ≤ S)",
        "hook": "Up to 8 numbers and S. Half sums + binary search.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "nim": {
        "scene": "vault",
        "title": "Nim (XOR of Piles)",
        "hook": "Pile sizes (≤ 63). XOR ≠ 0 means the player to move wins.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "grundy_numbers": {
        "scene": "vault",
        "title": "Grundy Numbers (Subtraction Game)",
        "hook": "n | allowed removals. g(n) = mex of reachable Grundy numbers.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "optimal_game": {
        "scene": "grid_power",
        "title": "Optimal Strategy for a Coin Game",
        "hook": "Coin values (≤ 8). Take an end; the opponent plays perfectly too.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "aho_corasick": {
        "scene": "files",
        "title": "Aho–Corasick (Multi-Pattern Search)",
        "hook": "Text | patterns. Trie + dashed failure links; scan the text once.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "substring_hash": {
        "scene": "dna",
        "title": "Substring Equality by Rolling Hash",
        "hook": "Text | queries 'i j len'. Prefix hashes compare any two substrings in O(1).",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "tarjan_scc": {
        "scene": "vault",
        "title": "Strongly Connected Components (Tarjan)",
        "hook": "Directed edges A>B, … One DFS with disc/low and a stack.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "two_sat": {
        "scene": "vault",
        "title": "2-SAT (Implication Graph + SCC)",
        "hook": "Clauses like a|!b (! = not). Implication graph, then SCCs.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "lexicographic_topo": {
        "scene": "vault",
        "title": "Lexicographically Smallest Topological Order",
        "hook": "Directed edges. Kahn with a min-heap: always the smallest ready vertex.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "convex_hull": {
        "scene": "grid_power",
        "title": "Convex Hull (Monotone Chain)",
        "hook": "Points 'x y' (0–9) separated by ';'. Lower + upper chains with a stack.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "polygon_area": {
        "scene": "grid_power",
        "title": "Polygon Area (Shoelace Formula)",
        "hook": "Vertices 'x y' in order, separated by ';'. Shoelace formula.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "closest_pair": {
        "scene": "grid_power",
        "title": "Closest Pair of Points (Divide & Conquer)",
        "hook": "Points 'x y' separated by ';'. Split, solve halves, check the strip.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "digit_dp": {
        "scene": "grid_power",
        "title": "Digit DP (Count Numbers With Digit Sum S)",
        "hook": "N (≤ 99999) and the digit sum S. Stay tight along N's digits.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "tree_robber": {
        "scene": "files",
        "title": "House Robber on a Tree",
        "hook": "Level-order tree of house values. Each node keeps take/skip.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "sos_dp": {
        "scene": "grid_power",
        "title": "Sum Over Subsets (SOS DP)",
        "hook": "2, 4, 8 or 16 values (one per mask). Add one bit at a time.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "sum_distances_tree": {
        "scene": "files",
        "title": "Sum of Distances in a Tree (Rerooting)",
        "hook": "Level-order tree. Sizes bottom-up, then reroot top-down.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "bit_kth": {
        "scene": "leaderboard",
        "title": "K-th Smallest With a Fenwick Tree",
        "hook": "Ops: add v, remove v, kth k (values 1–16). Binary lifting on the tree.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "inversions_bit": {
        "scene": "leaderboard",
        "title": "Count Inversions With a Fenwick Tree",
        "hook": "Values 1–16. Scan right to left; count smaller values already seen.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
    },
    "prefix_sum_2d": {
        "scene": "grid_power",
        "title": "2-D Prefix Sums (Rectangle Queries)",
        "hook": "Matrix | 'r1 c1 r2 c2' queries. Four lookups per rectangle.",
        "metaphors": {"node": "node", "edge": "link", "weight": "cost",
                      "visit": "Visiting", "start": "The start",
                      "done": "The answer."}
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
