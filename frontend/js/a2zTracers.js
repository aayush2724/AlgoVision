// ── A2Z → REAL TRACER LINKS ────────────────────────────────────────────────
//
// Striver's A2Z rows live in the GENERATED a2z.js (ids are append-only, do NOT
// hand-edit that file). This side-table is where a row earns a *real* trace:
// map an A2Z problem id to a catalog algorithm id (see ALGORITHMS in data.js).
//
// A row listed here renders the genuine, step-through trace on the student's
// own input — the same engine the Explore/Experience page runs — instead of
// the metaphor animation scene. A row that is absent falls back to the
// animation, so this map can grow one honest batch at a time.
//
// Only map a row when the existing tracer tells the SAME story the sheet asks
// for. "Reverse a singly linked list" → linked_list_reverse is honest;
// "Reverse a doubly linked list" is not (our tracer is singly), so it waits
// for its own tracer rather than borrowing a misleading one.
//
// Batch 1 (2026-09-15): the unambiguous 1:1 matches to existing tracers,
// spanning every view family (array, list, tree, graph, grid, string).

export const A2Z_TRACER = {
  // ── Step 1 — Basics (maths) ──
  "1-62": "gcd_euclid",              // GCD of Two Numbers

  // ── Step 2 — Sorting ──
  "2-1":  "selection_sort",          // Selection Sort
  "2-2":  "bubble_sort",             // Bubble Sort
  "2-8":  "insertion_sort",          // Insertion Sorting
  "2-9":  "merge_sort",              // Merge Sorting
  "2-10": "quick_sort",              // Quick Sorting

  // ── Step 3 — Arrays ──
  "3-19": "kadanes",                 // Kadane's Algorithm (max subarray sum)
  // Batch 25 (2026-09-21): array-scan classics + a binary-search variant.
  "3-17": "dutch_flag",              // Sort an Array of 0s, 1s and 2s
  "3-18": "majority_element",        // Majority Element (> n/2)
  "3-23": "next_permutation",        // Next Permutation
  "4-35": "search_rotated",          // Search in rotated sorted array-I

  // ── Step 4 — Binary Search ──
  "4-33": "binary_search",           // Search X in sorted array

  // ── Step 5 — Strings ──
  "5-18": "anagram",                 // Check if two strings are anagrams

  // ── Step 6 — Linked List ──
  "6-37": "find_middle",             // Middle of a LinkedList (tortoise-hare)
  "6-38": "linked_list_reverse",     // Reverse a LinkedList [Iterative]
  "6-40": "floyd_cycle",             // Detect a loop in a LinkedList

  // ── Step 7 — Recursion / Backtracking ──
  "7-33": "n_queens",                // N Queen

  // ── Step 8 — Bit Manipulation / Maths ──
  "8-30": "prime_factorisation",     // Print Prime Factors of a Number
  "8-33": "prime_factorisation",     // Prime factorisation of a Number

  // ── Step 9 — Stacks & Queues ──
  "9-13": "next_greater_element",    // Next Greater Element
  "9-33": "balanced_brackets",       // Balanced Parentheses

  // ── Step 14 — Binary Search Trees ──
  "14-18": "bst_search",             // Search in a Binary Search Tree

  // ── Step 15 — Graphs ──
  "15-60": "topological_sort",       // Topo Sort
  "15-61": "topological_sort",       // Topological sort / Kahn's algorithm

  // ── Step 16 — Dynamic Programming ──
  "16-25": "lcs",                    // Longest common subsequence
  "16-33": "edit_distance",          // Edit distance

  // ══ Batch 2 (2026-09-15): more honest 1:1 links to existing tracers. ══
  // Same rule as batch 1 — only when the tracer tells the SAME story. So
  // "Number of islands" (grid, counts regions) is NOT flood_fill (fills one
  // region); "Fractional knapsack" (greedy) is NOT knapsack_01 (0/1 DP);
  // "Implement Min Heap" is not our max-heap tracer. Those wait for their own.

  // ── Step 3 — Arrays ──
  "3-16":  "two_sum_sorted",         // Two Sum (two-pointer approach)
  "3-36":  "merge_intervals",        // Merge Overlapping Subintervals

  // ── Step 7 / 8 — Maths (fast exponentiation) ──
  "7-2":   "fast_exponentiation",    // Pow(x, n)
  "8-34":  "fast_exponentiation",    // Pow(x, n)

  // ── Step 9 — Stacks & Queues (monotonic deque) ──
  "9-24":  "sliding_window_maximum", // Sliding Window Maximum

  // ── Step 10 — Sliding Window & Two Pointer ──
  "10-1":  "longest_substring_no_repeat", // Longest Substring Without Repeating Characters
  "10-2":  "max_consecutive_ones_iii",    // Max Consecutive Ones III
  "10-3":  "longest_k_distinct",          // Fruit Into Baskets (≤2 distinct)
  "10-9":  "longest_k_distinct",          // Longest Substring With At Most K Distinct

  // ── Step 11 — Heaps ──
  "11-19": "min_heap",               // Implement Min Heap
  "11-21": "kth_largest",            // K-th Largest element in an array
  "11-22": "kth_smallest",           // Kth smallest element (priority queue)
  "11-27": "kth_largest",            // Kth largest element in a stream

  // ── Step 12 — Greedy ──
  "12-1":  "assign_cookies",         // Assign Cookies
  "12-2":  "fractional_knapsack",    // Fractional Knapsack
  "12-4":  "lemonade_change",        // Lemonade Change
  "12-6":  "activity_selection",     // N meetings in one room
  "12-8":  "jump_game_ii",           // Jump Game II
  "12-10": "job_sequencing",         // Job sequencing Problem
  "12-11": "candy",                  // Candy
  "12-14": "merge_intervals",        // Merge Intervals
  "12-17": "jump_game",              // Jump Game - I
  "12-18": "min_platforms",          // Minimum number of platforms

  // ── Step 13 — Binary Tree traversals (one trace shows pre/in/post) ──
  "13-3":  "tree_traversal",         // Preorder Traversal
  "13-38": "tree_traversal",         // Inorder Traversal
  "13-5":  "tree_traversal",         // Postorder Traversal
  "13-37": "tree_traversal",         // Pre, Post, Inorder in one traversal
  "13-43": "tree_traversal",         // Preorder, Inorder, Postorder in one traversal
  // Batch 23 — Binary Tree measures (BFS + recursive height family, LCA).
  "13-6":  "level_order",            // Level Order Traversal
  "13-44": "tree_max_depth",         // Maximum Depth in BT
  "13-46": "tree_diameter",          // Diameter of Binary Tree
  "13-53": "lca_bt",                 // LCA in BT

  // ── Step 15 — Graphs ──
  "15-3":  "connected_components",   // Connected Components
  "15-6":  "connected_components",   // Number of provinces
  "15-52": "dfs",                    // DFS
  "15-54": "flood_fill",             // Flood fill algorithm
  "15-58": "bipartite_check",        // Bipartite Graph (DFS)
  "15-64": "dijkstra",               // Dijkstra's Algorithm
  "15-69": "bellman_ford",           // Bellman Ford Algorithm
  "15-37": "prims_mst",              // Prim's Algorithm
  "15-73": "dsu",                    // Disjoint Set

  // ── Step 16 — Dynamic Programming ──
  "16-55": "house_robber",           // Maximum sum of non-adjacent elements
  "16-56": "house_robber",           // House robber
  "16-57": "unique_paths",           // Grid Unique Paths
  "16-58": "unique_paths",           // Unique paths II (obstacles — walls supported)
  "16-62": "subset_sum",             // Subset sum equal to target
  "16-64": "coin_change",            // Minimum Coins
  "16-41": "lis",                    // Longest Increasing Subsequence
  "16-75": "lis",                    // Longest Increasing Subsequence (DP-43)
  "16-47": "matrix_chain",           // Matrix chain multiplication
  "16-76": "matrix_chain",           // Matrix Chain Multiplication (Bottom-Up)

  // ── Step 17 — Tries ──
  "17-8":  "trie_insert",            // Trie Implementation and Operations

  // ── Step 18 — Strings ──
  "18-11": "rabin_karp",             // Rabin Karp Algorithm
  "18-12": "kmp_search",             // KMP Algorithm / LPS array

  // ══ Batch 3 (2026-09-15): the last honest links to existing tracers. ══
  // Deliberately NOT linked (tracer tells a different story): Step 10 windows
  // (our sliding_window is fixed-size-sum, those are variable-window strings),
  // prefix_sums subarray-search rows (our tracer is a range-query demo),
  // Merge-K lists (ours merges two), Implement Min Heap (ours is a max-heap),
  // Rod Cutting (unbounded, not 0/1), recursive sort variants (ours iterate).

  // ── Step 1 — Basics ──
  "1-25":  "fibonacci_dp",           // Fibonacci Number
  "1-106": "hash_table",             // Basic Hashing

  // ── Step 5 — Strings ──
  "5-14":  "manacher",               // Longest Palindromic Substring

  // ── Step 8 — Bit Manipulation & Maths ──
  "8-21":  "power_of_two",           // Check if a Number is Power of 2
  "8-22":  "count_set_bits",         // Count the Number of Set Bits
  "8-25":  "min_bit_flips",          // Minimum Bit Flips to Convert Number
  "8-26":  "single_number",          // Single Number - I
  "8-27":  "power_set",              // Power Set (Bit Manipulation)
  "8-32":  "sieve",                  // Count primes in range (Sieve of Eratosthenes)

  // ── Step 14 — Binary Search Trees ──
  "14-21": "bst_insert",             // Insert a given node in BST
  "14-7":  "bst_delete",             // Delete a node in BST

  // ── Step 15 — Graphs ──
  "15-63": "bfs",                    // Shortest path in undirected graph, unit weights (BFS)
  "15-74": "kruskals_mst",           // Find the MST weight (Kruskal / union-find)

  // ── Step 16 — Dynamic Programming ──
  "16-2":  "fibonacci_dp",           // Climbing stairs (same recurrence as Fibonacci)

  // ══ Batch 24 (2026-09-21): the DP remainder — 1D DP, stocks, counting, strings.
  "16-3":  "frog_jump",              // Frog Jump
  "16-35": "buy_sell_stock",         // Best time to buy and sell stock
  "16-65": "coin_change_2",          // Coin Change 2 (count ways)
  "16-27": "longest_common_substring", // Longest common substring

  // ══ Batch 26 (2026-09-27): Recursion + Stack — grid backtracking and the
  // two monotonic-stack classics that aren't next-greater in disguise.
  "7-18":  "word_search",            // Word Search
  "7-20":  "rat_in_maze",            // Rat in a Maze
  "9-25":  "stock_span",             // Stock span problem
  "9-39":  "largest_rectangle",      // Largest rectangle in a histogram

  // ══ Batch 27 (2026-09-27): two more stack/two-pointer classics and two
  // binary searches whose "sorted half" test isn't plain comparison to target.
  "9-17":  "trapping_rainwater",     // Trapping Rainwater
  "9-19":  "asteroid_collision",     // Asteroid Collision
  "4-37":  "find_min_rotated",       // Find minimum in Rotated Sorted Array
  "4-38":  "find_min_rotated",       // How many times rotated (= index of the min)
  "4-13":  "find_peak",              // Find peak element

  // ══ Batch 28 (2026-09-27): doubly linked lists (the list view now draws
  // dashed back-pointers and struck-out deletions) + a trie query.
  "6-9":   "dll_reverse",            // Reverse a Doubly Linked List
  "6-52":  "dll_delete_key",         // Delete all occurrences of a key in DLL
  "6-45":  "remove_nth_from_end",    // Remove Nth node from the back of the LL
  "17-3":  "longest_complete_word",  // Longest Word with All Prefixes

  // ══ Batch 29 (2026-09-27): the plain-view linked-list stragglers.
  "6-41":  "floyd_cycle",            // Starting point of the loop (Floyd phase 2)
  "6-43":  "ll_palindrome",          // Check if LL is palindrome
  "6-44":  "odd_even_list",          // Segregate odd and even nodes
  "6-46":  "delete_middle",          // Delete the middle node
  "6-56":  "rotate_list",            // Rotate a LL

  // ══ Batch 30 (2026-09-27): binary search on the answer. The array view
  // gained an optional number line for the answer range being searched.
  "4-16":  "koko_bananas",           // Koko eating bananas
  "4-18":  "koko_bananas",           // Smallest divisor (same ceil-sum check)
  "4-22":  "min_max_partition",      // Book Allocation Problem
  "4-24":  "min_max_partition",      // Painter's Partition
  "4-42":  "min_max_partition",      // Capacity to Ship Packages Within D Days
  "4-43":  "min_max_partition",      // Split array - largest sum
  "4-21":  "aggressive_cows",        // Aggressive Cows

  // ══ Batch 31 (2026-09-27): recursion trees on the existing tree view —
  // each call is a node, answers are green leaves.
  "7-28":  "subsets_recursion",      // Power Set
  "7-31":  "subsets_recursion",      // Subsets I (subset sums — leaf notes carry sums)
  "7-29":  "subsets_recursion",      // Count all subsequences with sum K (K input)
  "7-30":  "subsets_recursion",      // Check if there exists a subsequence with sum K
  "7-7":   "generate_parentheses",   // Generate Parentheses
  "7-27":  "binary_strings",         // Binary Strings Without Consecutive 1s
  "7-11":  "combination_sum",        // Combination Sum

  // ══ Batch 32 (2026-09-27): expression conversions on the stack view (now
  // with an output row, text-sized boxes and right-to-left scans).
  "9-9":   "infix_to_postfix",       // Infix to Postfix Conversion
  "9-36":  "infix_to_prefix",        // Infix to Prefix Conversion
  "9-11":  "postfix_to_infix",       // Postfix to Infix Conversion
  "9-35":  "postfix_to_prefix",      // Postfix to Prefix Conversion
  "9-10":  "prefix_to_infix",        // Prefix to Infix Conversion
  "9-34":  "prefix_to_postfix",      // Prefix to Postfix Conversion

  // ══ Batch 33 (2026-09-27): loop-style recursion (n-ary trees — the tree
  // renderer now draws every child, which also fixed 3+-child trie nodes).
  "7-32":  "subsets_ii",             // Subsets II
  "7-12":  "combination_sum_ii",     // Combination Sum II
  "7-15":  "combination_sum_iii",    // Combination Sum III
  "7-17":  "palindrome_partition",   // Palindrome partitioning
  "7-16":  "letter_combinations",    // Letter Combinations of a Phone Number

  // ══ Batch 34 (2026-09-27): binary-search boundary variants (one module).
  "4-2":   "lower_bound",            // Lower Bound
  "4-4":   "lower_bound",            // Search insert position (= lower bound)
  "4-3":   "upper_bound",            // Upper Bound
  "4-5":   "floor_ceil",             // Floor and Ceil in Sorted Array
  "4-6":   "first_last_occurrence",  // First and last occurrence
  "4-34":  "first_last_occurrence",  // Count occurrences (last − first + 1)
  "4-20":  "kth_missing",            // Kth Missing Positive Number
  "4-39":  "single_element_sorted",  // Single element in a Sorted Array

  // ══ Batches 35–39 (2026-09-27).
  // 35 — answer search on numbers
  "4-40":  "sqrt_search",            // Find square root of a number
  "4-41":  "nth_root",               // Find Nth root of a number
  "4-17":  "min_bouquets",           // Minimum days to make M bouquets
  // 36 — 2-D matrix searches (grid view)
  "4-29":  "search_2d_matrix",       // Search in a 2D matrix
  "4-48":  "search_2d_matrix_ii",    // Search in 2D matrix - II
  "4-47":  "row_max_ones",           // Find row with maximum 1's
  // 37 — list arithmetic (grid view as column addition)
  "6-51":  "add_two_numbers",        // Add two numbers in Linked List
  "6-50":  "add_one_list",           // Add one to a number represented by LL
  // 38 — more monotonic stack
  "9-15":  "next_smaller",           // Next Smaller Element
  "9-37":  "nge_circular",           // Next Greater Element - 2
  "9-21":  "remove_k_digits",        // Remove K Digits
  "9-18":  "sum_subarray_mins",      // Sum of Subarray Minimums
  // 39 — array fundamentals
  "3-2":   "second_largest",         // Second Largest Without Sorting
  "3-4":   "remove_duplicates_sorted", // Remove Duplicates from Sorted Array
  "3-5":   "rotate_array_k",         // Left Rotate Array by One (K = 1)
  "3-6":   "rotate_array_k",         // Left Rotate Array by K Places
  "3-7":   "move_zeros",             // Move Zeros to End
  "3-14":  "longest_subarray_sum_k", // Longest Subarray with Sum K (positives)
  "3-24":  "leaders",                // Leaders in an Array

  // ══ Batches 40–44 (2026-09-27): level-order binary trees (40 traversals,
  // 41 views, 42 checks) and table DP (43 grid DP, 44 string DP).
  "13-39":  "iter_preorder",           // Iterative Preorder Traversal
  "13-40":  "iter_inorder",            // Iterative Inorder Traversal
  "13-41":  "postorder_two_stacks",    // Post-order using 2 stacks
  "13-42":  "postorder_one_stack",     // Post-order using 1 stack
  "13-48":  "zigzag_traversal",        // Zig Zag or Spiral Traversal
  "13-51":  "right_view",              // Right/Left View
  "13-49":  "top_view",                // Top View
  "13-50":  "bottom_view",             // Bottom view
  "13-18":  "vertical_order",          // Vertical Order Traversal
  "13-17":  "boundary_traversal",      // Boundary Traversal
  "13-54":  "max_width",               // Maximum Width of BT
  "13-45":  "balanced_tree",           // Check for balanced binary tree
  "13-22":  "symmetric_tree",          // Symmetric Binary Tree
  "13-14":  "max_path_sum",            // Maximum path sum
  "13-52":  "root_to_leaf_paths",      // Print root to leaf path
  "13-55":  "children_sum",            // Children Sum Property
  "13-56":  "nodes_at_distance_k",     // Nodes at distance K
  "13-57":  "burn_tree",               // Minimum time to burn the BT
  "13-58":  "count_complete_nodes",    // Count nodes in a complete BT
  "16-4":   "frog_jump_k",             // Frog jump with K distances
  "16-7":   "ninja_training",          // Ninja's training
  "16-59":  "min_falling_path",        // Minimum Falling Path Sum
  "16-60":  "triangle_path",           // Triangle
  "16-15":  "partition_equal_subset",  // Partition equal subset sum
  "16-17":  "count_subsets_sum_k",     // Count subsets with sum K
  "16-23":  "unbounded_knapsack",      // Unbounded knapsack
  "16-66":  "rod_cutting",             // Rod Cutting Problem
  "16-67":  "print_lcs",               // Print Longest Common Subsequence
  "16-28":  "longest_palindromic_subseq", // Longest palindromic subsequence
  "16-68":  "min_insert_palindrome",   // Minimum insertions to make string palindrome
  "16-69":  "min_ins_del",             // Minimum insertions or deletions A to B
  "16-31":  "shortest_supersequence",  // Shortest common supersequence
  "16-32":  "distinct_subsequences",   // Distinct subsequences
  "16-34":  "wildcard_match",          // Wildcard matching
};
