import { COMPLEXITY_SPECS } from "./complexitySpecs.js";

export const NAV = [
  { label: "Home",       hash: "#/"          },
  { label: "Explore",    hash: "#/explore"   },
  { label: "Experience", hash: "#/experience"},
  { label: "A2Z",        hash: "#/a2z"       },
  { label: "Practice",   hash: "#/practice"  },
  { label: "Journey",    hash: "#/journey"   },
];

export const HERO = {
  title: "See the Algorithm.\nMaster the Story.",
  lead: "We turn complex data structures into cinematic visual journeys — real-world metaphors, live step-by-step traces, and AI-powered explanations.",
  primaryCTA: "Start Exploring",
  ghostCTA: "View A2Z Roadmap"
};

export const ACTS = [
  { title: "The Hook",     desc: "Every algorithm starts with a real-world problem worth solving. We set the stage with cinematic metaphors.", icon: "01" },
  { title: "The Reveal",   desc: "Watch the mechanics unfold in real-time. Animated graphs reveal the 'why' behind the 'how'.", icon: "02" },
  { title: "The Mechanics",desc: "Deep dive with interactive step traces and AI-powered breakdowns of each decision.", icon: "03" }
];

export const CATEGORIES = ["All", "Foundations", "Structures", "Mastery"];

// Every traceable algorithm, in one place. The Explore page, the engine's
// quick-switcher and compare mode all read from this — add a tracer here and
// it becomes discoverable everywhere.
export const ALGO_CATEGORIES = ["All", "Graphs", "Sorting", "Searching", "Patterns", "Greedy", "Structures", "DP", "Math"];

export const ALGORITHMS = [
  { id: "dijkstra",     name: "Dijkstra's Shortest Path", category: "Graphs", emoji: "📍", complexity: "O((V+E) log V)", input: "graph",
    hook: "Find the fastest route through a city." },
  { id: "bfs",          name: "Breadth-First Search",     category: "Graphs", emoji: "👤", complexity: "O(V + E)",       input: "graph",
    hook: "Explore the network level by level." },
  { id: "dfs",          name: "Depth-First Search",       category: "Graphs", emoji: "🗺️", complexity: "O(V + E)",       input: "graph",
    hook: "Dive deep, backtrack, map every corridor." },
  { id: "prims_mst",    name: "Prim's Spanning Tree",     category: "Graphs", emoji: "⚡", complexity: "O(E log V)",     input: "graph",
    hook: "Wire every town with the least cable possible." },
  { id: "kruskals_mst", name: "Kruskal's MST (Union-Find)", category: "Graphs", emoji: "🌉", complexity: "O(E log E)",   input: "graph",
    hook: "Cheapest bridges first — but never close a cycle." },

  { id: "merge_sort",     name: "Merge Sort",     category: "Sorting", emoji: "🏆", complexity: "O(n log n)", input: "array",
    hook: "Divide the chaos. Merge into order." },
  { id: "quick_sort",     name: "Quick Sort",     category: "Sorting", emoji: "🎯", complexity: "O(n log n)", input: "array",
    hook: "Pick a pivot — the crowd splits around it." },
  { id: "bubble_sort",    name: "Bubble Sort",    category: "Sorting", emoji: "🫧", complexity: "O(n²)",      input: "array",
    hook: "Heavy values sink, light ones rise." },
  { id: "insertion_sort", name: "Insertion Sort", category: "Sorting", emoji: "🃏", complexity: "O(n²)",      input: "array",
    hook: "Pick up a card, slide it into place." },
  { id: "selection_sort", name: "Selection Sort", category: "Sorting", emoji: "🥇", complexity: "O(n²)",      input: "array",
    hook: "Crown the champion of what's left. Repeat." },

  { id: "binary_search", name: "Binary Search", category: "Searching", emoji: "📚", complexity: "O(log n)", input: "array",
    hook: "Halve the search space with every guess." },
  { id: "bst_search",    name: "BST Search",    category: "Searching", emoji: "🔎", complexity: "O(log n)", input: "array",
    hook: "Each comparison discards a whole subtree." },

  { id: "two_sum_sorted", name: "Two Sum (Two Pointers)", category: "Patterns", emoji: "🛒", complexity: "O(n)", input: "array",
    hook: "Two pointers converge on the target sum." },
  { id: "sliding_window", name: "Sliding Window",         category: "Patterns", emoji: "📈", complexity: "O(n)", input: "array",
    hook: "Drop one, add one — never recount." },
  { id: "kadanes",        name: "Kadane's Max Subarray",  category: "Patterns", emoji: "💹", complexity: "O(n)", input: "array",
    hook: "Extend the run, or cut your losses." },

  { id: "linked_list_reverse", name: "Reverse a Linked List", category: "Structures", emoji: "🚃", complexity: "O(n)",     input: "array",
    hook: "Flip every coupling, one pointer at a time." },
  { id: "balanced_brackets",   name: "Balanced Brackets",     category: "Structures", emoji: "🍽️", complexity: "O(n)",     input: "text",
    hook: "The stack remembers what's still open." },
  { id: "bst_insert",          name: "BST — Build a Tree",    category: "Structures", emoji: "📁", complexity: "O(log n)", input: "array",
    hook: "Every value finds its own branch." },
  { id: "heap_insert",         name: "Max-Heap — Build",      category: "Structures", emoji: "🏥", complexity: "O(log n)", input: "array",
    hook: "The most urgent always rises to the top." },

  { id: "fibonacci_dp", name: "Fibonacci (Memoized)",       category: "DP", emoji: "💾", complexity: "O(n)",   input: "number",
    hook: "Remember the past to conquer the future." },
  { id: "knapsack_01",  name: "0/1 Knapsack",               category: "DP", emoji: "🎒", complexity: "O(n·W)", input: "text",
    hook: "A limited hold, priceless cargo." },
  { id: "lcs",          name: "Longest Common Subsequence", category: "DP", emoji: "🧬", complexity: "O(n·m)", input: "text",
    hook: "Find the sequence two strands share." },
  { id: "edit_distance", name: "Edit Distance (Levenshtein)", category: "DP", emoji: "✍️", complexity: "O(n·m)", input: "text",
    hook: "How many keystrokes turn one word into another?" },
  { id: "topological_sort", name: "Topological Sort (Kahn's)", category: "Graphs", emoji: "🗓️", complexity: "O(V + E)", input: "graph",
    hook: "Order the tasks so nothing starts before its prerequisite." },
  { id: "counting_sort", name: "Counting Sort",             category: "Sorting", emoji: "🗳️", complexity: "O(n + k)", input: "array",
    hook: "Sort without ever comparing two values." },
  { id: "prefix_sums",  name: "Prefix Sums",                category: "Patterns", emoji: "🧾", complexity: "O(n) build, O(1) query", input: "array",
    hook: "Pay once, then answer any range sum instantly." },
  { id: "next_greater_element", name: "Next Greater Element", category: "Patterns", emoji: "📈", complexity: "O(n)", input: "array",
    hook: "Who is the first taller person to your right?" },
  { id: "floyd_cycle",  name: "Cycle Detection (Floyd's)",  category: "Structures", emoji: "🐢", complexity: "O(n) time, O(1) space", input: "array",
    hook: "Two runners at different speeds reveal a hidden loop." },
  { id: "tree_traversal", name: "Tree Traversals",          category: "Structures", emoji: "🌳", complexity: "O(n)", input: "array",
    hook: "One tree, three reading orders — inorder comes out sorted." },
  { id: "level_order",  name: "Level-Order Traversal",      category: "Structures", emoji: "🪜", complexity: "O(n)", input: "array",
    hook: "Read a tree floor by floor — the queue holds exactly the next level." },
  { id: "tree_max_depth", name: "Maximum Depth of a Tree",  category: "Structures", emoji: "📏", complexity: "O(n)", input: "array",
    hook: "A node's depth is 1 + its deeper subtree — answers land bottom-up." },
  { id: "tree_diameter", name: "Diameter of a Tree",        category: "Structures", emoji: "📐", complexity: "O(n)", input: "array",
    hook: "The longest path between two nodes — and it need not touch the root." },
  { id: "lca_bt",       name: "Lowest Common Ancestor",     category: "Structures", emoji: "🧬", complexity: "O(n)", input: "text",
    hook: "The deepest node with both targets beneath it — found in one recursion." },
  { id: "frog_jump",    name: "Frog Jump (1-D DP)",         category: "DP", emoji: "🐸", complexity: "O(n)", input: "array",
    hook: "The gentlest 1-D DP: each stone is min(one-hop, two-hop) from before it." },
  { id: "buy_sell_stock", name: "Buy & Sell Stock",         category: "DP", emoji: "📉", complexity: "O(n)", input: "array",
    hook: "One buy, one sell — carry the lowest price so far and beat it in one pass." },
  { id: "coin_change_2", name: "Coin Change 2 (Ways)",       category: "DP", emoji: "🪙", complexity: "O(coins·amt)", input: "array",
    hook: "Not the fewest coins — the number of distinct ways to make the amount." },
  { id: "longest_common_substring", name: "Longest Common Substring", category: "DP", emoji: "🧵", complexity: "O(n·m)", input: "text",
    hook: "Like LCS, but contiguous — one mismatch resets the shared run to zero." },
  { id: "search_rotated", name: "Search in Rotated Array",     category: "Searching", emoji: "🔄", complexity: "O(log n)", input: "array",
    hook: "Binary search on a rotated sorted array — one half around mid is always clean." },
  { id: "dutch_flag",   name: "Sort 0s, 1s, 2s (Dutch Flag)", category: "Sorting", emoji: "🚦", complexity: "O(n)", input: "array",
    hook: "Three pointers sort three values in a single in-place pass." },
  { id: "majority_element", name: "Majority Element",          category: "Patterns", emoji: "🗳️", complexity: "O(n)", input: "array",
    hook: "Boyer-Moore voting: the true majority can never be fully cancelled out." },
  { id: "next_permutation", name: "Next Permutation",          category: "Patterns", emoji: "🔢", complexity: "O(n)", input: "array",
    hook: "Rearrange into the next-larger order: find the dip, bump it, reverse the tail." },
  { id: "stock_span",   name: "Stock Span",                  category: "Patterns", emoji: "📅", complexity: "O(n)", input: "array",
    hook: "How many days back was the price no higher? A monotonic stack answers in one pass." },
  { id: "largest_rectangle", name: "Largest Rectangle in Histogram", category: "Patterns", emoji: "🏙️", complexity: "O(n)", input: "array",
    hook: "Each bar stretches until a shorter one — the stack says exactly where." },
  { id: "rat_in_maze",  name: "Rat in a Maze",               category: "Patterns", emoji: "🐀", complexity: "O(4^(n²))", input: "number",
    hook: "Find every escape route by trying, failing, and un-marking squares." },
  { id: "word_search",  name: "Word Search",                 category: "Patterns", emoji: "🔠", complexity: "O(r·c·3^L)", input: "text",
    hook: "Trace a word through neighbouring letters — backtrack on every wrong turn." },
  { id: "trapping_rainwater", name: "Trapping Rainwater",    category: "Patterns", emoji: "🌧️", complexity: "O(n)", input: "array",
    hook: "Two pointers settle each bar against the lower of its two tallest walls." },
  { id: "asteroid_collision", name: "Asteroid Collision",    category: "Patterns", emoji: "☄️", complexity: "O(n)", input: "array",
    hook: "A stack of survivors: left-movers smash into right-movers until one wins." },
  { id: "find_min_rotated", name: "Min in Rotated Array",    category: "Searching", emoji: "🔃", complexity: "O(log n)", input: "array",
    hook: "Binary search for the wrap-around point — its index is the rotation count." },
  { id: "find_peak",    name: "Find Peak Element",           category: "Searching", emoji: "⛰️", complexity: "O(log n)", input: "array",
    hook: "Binary search on an unsorted array: follow the uphill slope to a peak." },
  { id: "dll_reverse",  name: "Reverse a Doubly Linked List", category: "Structures", emoji: "🔁", complexity: "O(n)", input: "array",
    hook: "Each node swaps its next and prev — reversal with no neighbour bookkeeping." },
  { id: "dll_delete_key", name: "Delete Key from DLL",       category: "Structures", emoji: "✂️", complexity: "O(n)", input: "array",
    hook: "Unlink every match from both sides in a single pass." },
  { id: "remove_nth_from_end", name: "Remove Nth From End",  category: "Structures", emoji: "🎯", complexity: "O(n)", input: "array",
    hook: "A fixed gap between two pointers finds the Nth-from-last in one pass." },
  { id: "longest_complete_word", name: "Longest Complete Word", category: "Structures", emoji: "🧩", complexity: "O(total letters)", input: "text",
    hook: "A trie finds the longest word whose every prefix is also a word." },
  { id: "ll_palindrome", name: "Linked List Palindrome",    category: "Structures", emoji: "🪞", complexity: "O(n)", input: "array",
    hook: "Reverse the back half in place, compare, then put it back — O(1) space." },
  { id: "odd_even_list", name: "Odd–Even Linked List",      category: "Structures", emoji: "🔀", complexity: "O(n)", input: "array",
    hook: "Two leapfrogging pointers split odd and even positions — only arrows change." },
  { id: "rotate_list",  name: "Rotate a Linked List",        category: "Structures", emoji: "🔄", complexity: "O(n)", input: "array",
    hook: "Close the list into a ring, walk to the cut point, and break it." },
  { id: "delete_middle", name: "Delete the Middle Node",     category: "Structures", emoji: "✂️", complexity: "O(n)", input: "array",
    hook: "Tortoise and hare with a head start stop right before the middle." },
  { id: "koko_bananas", name: "Koko Eating Bananas",         category: "Searching", emoji: "🍌", complexity: "O(n log max)", input: "array",
    hook: "Binary search on the answer: guess a speed, check it, halve the range." },
  { id: "min_max_partition", name: "Book Allocation / Split Array", category: "Searching", emoji: "📚", complexity: "O(n log sum)", input: "array",
    hook: "Minimise the biggest group sum — binary search the cap, fill greedily." },
  { id: "aggressive_cows", name: "Aggressive Cows",          category: "Searching", emoji: "🐄", complexity: "O(n log range)", input: "array",
    hook: "Maximise the minimum gap by binary-searching the gap itself." },
  { id: "subsets_recursion", name: "Subsets (Recursion Tree)", category: "Patterns", emoji: "🌳", complexity: "O(2ⁿ)", input: "array",
    hook: "Take it or skip it — the recursion tree's leaves are the power set." },
  { id: "generate_parentheses", name: "Generate Parentheses", category: "Patterns", emoji: "🧮", complexity: "O(Catalan(n))", input: "number",
    hook: "Backtracking that never builds an invalid prefix — watch the pruning." },
  { id: "binary_strings", name: "Binary Strings, No 11",      category: "Patterns", emoji: "💡", complexity: "O(Fib(n))", input: "number",
    hook: "One rule prunes the tree; the leaf count turns out to be Fibonacci." },
  { id: "combination_sum", name: "Combination Sum",           category: "Patterns", emoji: "➕", complexity: "exponential", input: "array",
    hook: "Take again or move on — every path to exactly zero is an answer." },
  { id: "infix_to_postfix", name: "Infix → Postfix", category: "Structures", emoji: "🧾", complexity: "O(n)", input: "text",
    hook: "You are rewriting an expression so every operator follows its operands, parking operators on a stack." },
  { id: "infix_to_prefix", name: "Infix → Prefix", category: "Structures", emoji: "🧾", complexity: "O(n)", input: "text",
    hook: "The postfix scan run right to left, then reversed." },
  { id: "postfix_to_infix", name: "Postfix → Infix", category: "Structures", emoji: "🧾", complexity: "O(n)", input: "text",
    hook: "A stack of sub-expressions, glued back together with brackets." },
  { id: "postfix_to_prefix", name: "Postfix → Prefix", category: "Structures", emoji: "🧾", complexity: "O(n)", input: "text",
    hook: "Pop two pieces, write the operator in front." },
  { id: "prefix_to_infix", name: "Prefix → Infix", category: "Structures", emoji: "🧾", complexity: "O(n)", input: "text",
    hook: "Scan right to left — the first pop is the left operand." },
  { id: "prefix_to_postfix", name: "Prefix → Postfix", category: "Structures", emoji: "🧾", complexity: "O(n)", input: "text",
    hook: "Scan right to left, write the operator at the back." },
  { id: "subsets_ii",   name: "Subsets II",                  category: "Patterns", emoji: "🌿", complexity: "O(2ⁿ)", input: "array",
    hook: "Skip equal values at the same level — every node is a distinct subset." },
  { id: "combination_sum_ii", name: "Combination Sum II",    category: "Patterns", emoji: "🪙", complexity: "exponential", input: "array",
    hook: "Each candidate once, no repeated answers — sort, skip twins, stop early." },
  { id: "combination_sum_iii", name: "Combination Sum III",  category: "Patterns", emoji: "🔢", complexity: "O(C(9,k))", input: "array",
    hook: "Exactly k digits 1–9 that hit the sum, each set found once." },
  { id: "palindrome_partition", name: "Palindrome Partitioning", category: "Patterns", emoji: "✂️", complexity: "O(n·2ⁿ)", input: "text",
    hook: "Only palindromic pieces get a branch; each leaf is a full partition." },
  { id: "letter_combinations", name: "Phone Letter Combinations", category: "Patterns", emoji: "📱", complexity: "O(4ⁿ)", input: "text",
    hook: "Each keypad digit branches into its letters — one level per digit." },
  { id: "lower_bound", name: "Lower Bound", category: "Searching", emoji: "⤓", complexity: "O(log n)", input: "array",
    hook: "First index ≥ X — keep searching left after a match." },
  { id: "upper_bound", name: "Upper Bound", category: "Searching", emoji: "⤒", complexity: "O(log n)", input: "array",
    hook: "First index > X — the edge just past every copy of X." },
  { id: "first_last_occurrence", name: "First & Last Occurrence", category: "Searching", emoji: "📍", complexity: "O(log n)", input: "array",
    hook: "Two boundary searches give the range (and count) of X." },
  { id: "floor_ceil", name: "Floor & Ceil", category: "Searching", emoji: "↕️", complexity: "O(log n)", input: "array",
    hook: "Largest ≤ X and smallest ≥ X, one search each." },
  { id: "kth_missing", name: "Kth Missing Positive", category: "Searching", emoji: "🕳️", complexity: "O(log n)", input: "array",
    hook: "Search on how many numbers are missing before each index." },
  { id: "single_element_sorted", name: "Single Element (Sorted)", category: "Searching", emoji: "🦄", complexity: "O(log n)", input: "array",
    hook: "Pairs flip from even to odd starts at the odd one out." },
  { id: "sqrt_search", name: "Square Root (Binary Search)", category: "Searching", emoji: "√", complexity: "O(log n)", input: "array",
    hook: "Binary-search the answer x: the largest with x·x ≤ n." },
  { id: "nth_root", name: "Nth Root", category: "Searching", emoji: "ⁿ√", complexity: "O(log m)", input: "array",
    hook: "Search x with xⁿ = m exactly — or prove there is none." },
  { id: "min_bouquets", name: "Min Days for Bouquets", category: "Searching", emoji: "💐", complexity: "O(n log max)", input: "array",
    hook: "Binary-search the day; count adjacent bloomed runs to check it." },
  { id: "search_2d_matrix", name: "Search a Sorted Matrix", category: "Searching", emoji: "🔲", complexity: "O(log RC)", input: "text",
    hook: "The matrix read row by row is one sorted list — search a flat index." },
  { id: "search_2d_matrix_ii", name: "Staircase Matrix Search", category: "Searching", emoji: "🪜", complexity: "O(R + C)", input: "text",
    hook: "From the top-right corner, each step drops a row or a column." },
  { id: "row_max_ones", name: "Row With Max 1s", category: "Searching", emoji: "🔦", complexity: "O(R log C)", input: "text",
    hook: "Binary-search each row for its first 1." },
  { id: "add_two_numbers", name: "Add Two Numbers (Lists)", category: "Structures", emoji: "➕", complexity: "O(max(m,n))", input: "text",
    hook: "Digit + digit + carry, node by node." },
  { id: "add_one_list", name: "Add 1 to a List Number", category: "Structures", emoji: "☝️", complexity: "O(n)", input: "text",
    hook: "Recurse to the tail; the carry ripples back to the head." },
  { id: "next_smaller", name: "Next Smaller Element", category: "Patterns", emoji: "📉", complexity: "O(n)", input: "array",
    hook: "The monotonic stack, mirrored: pop while the waiting value is bigger." },
  { id: "nge_circular", name: "Next Greater II (Circular)", category: "Patterns", emoji: "🔁", complexity: "O(n)", input: "array",
    hook: "Two laps round a circular array; the second only resolves." },
  { id: "remove_k_digits", name: "Remove K Digits", category: "Patterns", emoji: "✂️", complexity: "O(n)", input: "array",
    hook: "Delete a kept digit whenever a smaller one follows it." },
  { id: "sum_subarray_mins", name: "Sum of Subarray Minimums", category: "Patterns", emoji: "∑", complexity: "O(n)", input: "array",
    hook: "Count the windows each value is the minimum of, with two stacks." },
  { id: "remove_duplicates_sorted", name: "Remove Duplicates (Sorted)", category: "Patterns", emoji: "🧹", complexity: "O(n)", input: "array",
    hook: "Two pointers build the unique prefix in place." },
  { id: "rotate_array_k", name: "Rotate Array by K", category: "Patterns", emoji: "🔄", complexity: "O(n)", input: "array",
    hook: "Three reversals rotate in place with O(1) space." },
  { id: "move_zeros", name: "Move Zeros to End", category: "Patterns", emoji: "0️⃣", complexity: "O(n)", input: "array",
    hook: "Swap non-zeros down to the first zero; order is kept." },
  { id: "leaders", name: "Leaders in an Array", category: "Patterns", emoji: "👑", complexity: "O(n)", input: "array",
    hook: "Scan from the right with a running maximum." },
  { id: "longest_subarray_sum_k", name: "Longest Subarray Sum K", category: "Patterns", emoji: "📏", complexity: "O(n)", input: "array",
    hook: "A variable window for non-negative values: grow right, shrink left." },
  { id: "second_largest", name: "Second Largest Element", category: "Patterns", emoji: "🥈", complexity: "O(n)", input: "array",
    hook: "One pass, two trackers, no sorting." },
  { id: "iter_preorder", name: "Iterative Preorder Traversal", category: "Structures", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "You are visiting folders parent-first using your own stack instead of recursion." },
  { id: "iter_inorder", name: "Iterative Inorder Traversal", category: "Structures", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "Slide left pushing; pop, visit, turn right." },
  { id: "postorder_two_stacks", name: "Postorder With Two Stacks", category: "Structures", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "Stack 2 collects root-right-left, then reads back reversed." },
  { id: "postorder_one_stack", name: "Postorder With One Stack", category: "Structures", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "Go right only if that subtree isn't finished yet." },
  { id: "zigzag_traversal", name: "Zigzag Level Order Traversal", category: "Structures", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "Every other level is read right to left." },
  { id: "right_view", name: "Right / Left View of a Binary Tree", category: "Structures", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "Last node per level = right view; first = left view." },
  { id: "top_view", name: "Top View of a Binary Tree", category: "Structures", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "First node seen at each horizontal distance." },
  { id: "bottom_view", name: "Bottom View of a Binary Tree", category: "Structures", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "The last node at each horizontal distance wins." },
  { id: "vertical_order", name: "Vertical Order Traversal", category: "Structures", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "Columns by horizontal distance, top to bottom." },
  { id: "boundary_traversal", name: "Boundary Traversal", category: "Structures", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "Root, left edge, leaves, right edge (bottom-up)." },
  { id: "max_width", name: "Maximum Width of a Binary Tree", category: "Structures", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "Slots are numbered as if the tree were complete." },
  { id: "balanced_tree", name: "Check for a Balanced Binary Tree", category: "Structures", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "Try 1,2,2,3,3,null,null,4,4 for an unbalanced one." },
  { id: "symmetric_tree", name: "Symmetric Binary Tree", category: "Structures", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "Try 1,2,2,null,3,null,3 for a lopsided one." },
  { id: "max_path_sum", name: "Maximum Path Sum", category: "Structures", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "A path may bend at one node." },
  { id: "root_to_leaf_paths", name: "Root-to-Leaf Paths", category: "Structures", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "Each leaf closes one path." },
  { id: "children_sum", name: "Children Sum Property", category: "Structures", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "Values only ever go up — watch them change." },
  { id: "nodes_at_distance_k", name: "All Nodes at Distance K", category: "Structures", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "You are finding every node exactly k steps from a target, moving up and down the tree." },
  { id: "burn_tree", name: "Minimum Time to Burn a Binary Tree", category: "Structures", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "You are timing how long a fire takes to reach every node when it can spread up to parents as well as down." },
  { id: "count_complete_nodes", name: "Count Nodes in a Complete Binary Tree", category: "Structures", emoji: "🌳", complexity: "O(log² n)", input: "text",
    hook: "Perfect subtrees are counted without walking them." },
  { id: "frog_jump_k", name: "Frog Jump With K Distances", category: "DP", emoji: "🧮", complexity: "O(n·k)", input: "text",
    hook: "Each stone looks back up to K stones for the cheapest jump." },
  { id: "ninja_training", name: "Ninja's Training", category: "DP", emoji: "🧮", complexity: "O(n·m)", input: "text",
    hook: "You are planning a ninja's week so no activity repeats two days running and the points are maximal." },
  { id: "min_falling_path", name: "Minimum Falling Path Sum", category: "DP", emoji: "🧮", complexity: "O(n·m)", input: "text",
    hook: "You are descending a grid of hazards, choosing the cheapest of the three cells below each step." },
  { id: "triangle_path", name: "Triangle (Minimum Path Sum)", category: "DP", emoji: "🧮", complexity: "O(n·m)", input: "text",
    hook: "You are descending a triangle of costs, stepping to one of the two cells below." },
  { id: "partition_equal_subset", name: "Partition Equal Subset Sum", category: "DP", emoji: "🧮", complexity: "O(n·m)", input: "text",
    hook: "You are splitting a pile of weights into two sides that balance exactly." },
  { id: "count_subsets_sum_k", name: "Count Subsets With Sum K", category: "DP", emoji: "🧮", complexity: "O(n·m)", input: "text",
    hook: "You are counting the ways to make an exact total from coins used once each." },
  { id: "unbounded_knapsack", name: "Unbounded Knapsack", category: "DP", emoji: "🧮", complexity: "O(n·m)", input: "text",
    hook: "You are filling a pack from items in unlimited supply for the highest value." },
  { id: "rod_cutting", name: "Rod Cutting", category: "DP", emoji: "🧮", complexity: "O(n·m)", input: "text",
    hook: "You are cutting a rod into pieces to fetch the highest price, reusing any length as often as you like." },
  { id: "print_lcs", name: "Print the Longest Common Subsequence", category: "DP", emoji: "🧬", complexity: "O(n·m)", input: "text",
    hook: "You are finding the longest run of letters two words share in order, then reading it back from the table." },
  { id: "longest_palindromic_subseq", name: "Longest Palindromic Subsequence", category: "DP", emoji: "🧬", complexity: "O(n·m)", input: "text",
    hook: "You are finding the longest palindrome hidden as a subsequence by aligning the word with its reverse." },
  { id: "min_insert_palindrome", name: "Minimum Insertions to Make a Palindrome", category: "DP", emoji: "🧬", complexity: "O(n·m)", input: "text",
    hook: "You are counting the fewest letters to insert so a word reads the same backwards." },
  { id: "min_ins_del", name: "Minimum Insertions/Deletions (A → B)", category: "DP", emoji: "🧬", complexity: "O(n·m)", input: "text",
    hook: "You are turning one word into another using only insertions and deletions, keeping what they share." },
  { id: "shortest_supersequence", name: "Shortest Common Supersequence", category: "DP", emoji: "🧬", complexity: "O(n·m)", input: "text",
    hook: "You are building the shortest string that contains two words as subsequences." },
  { id: "distinct_subsequences", name: "Distinct Subsequences", category: "DP", emoji: "🧬", complexity: "O(n·m)", input: "text",
    hook: "You are counting the distinct ways a target word can be picked out of a longer string." },
  { id: "wildcard_match", name: "Wildcard Matching", category: "DP", emoji: "🧬", complexity: "O(n·m)", input: "text",
    hook: "Text, then pattern with ? (one char) and * (any run)." },
  { id: "number_of_islands", name: "Number of Islands", category: "Graphs", emoji: "🗺️", complexity: "O(R·C)", input: "text",
    hook: "You are a surveyor flying over a flooded map, naming each island the moment you first touch its shore." },
  { id: "rotten_oranges", name: "Rotten Oranges", category: "Graphs", emoji: "🗺️", complexity: "O(R·C)", input: "text",
    hook: "You are timing how fast rot spreads from every bad orange to its neighbours, minute by minute." },
  { id: "nearest_one_distance", name: "Distance of Nearest Cell Having 1", category: "Graphs", emoji: "🗺️", complexity: "O(R·C)", input: "text",
    hook: "You are stamping every cell with how far it is from the nearest lit cell, spreading from all lights at once." },
  { id: "surrounded_regions", name: "Surrounded Regions", category: "Graphs", emoji: "🗺️", complexity: "O(R·C)", input: "text",
    hook: "You are flipping every region that cannot reach the border, after rescuing the ones that can." },
  { id: "number_of_enclaves", name: "Number of Enclaves", category: "Graphs", emoji: "🗺️", complexity: "O(R·C)", input: "text",
    hook: "You are counting the land cells that cannot walk off the edge of the map." },
  { id: "binary_maze_path", name: "Shortest Path in a Binary Maze", category: "Graphs", emoji: "🧭", complexity: "O(R·C)", input: "text",
    hook: "You are finding the shortest path through a maze where every step costs the same." },
  { id: "min_effort_path", name: "Path With Minimum Effort", category: "Graphs", emoji: "🧭", complexity: "O(R·C log RC)", input: "text",
    hook: "You are hiking across a height map, choosing the route whose steepest single step is the gentlest." },
  { id: "swim_rising_water", name: "Swim in Rising Water", category: "Graphs", emoji: "🧭", complexity: "O(R·C log RC)", input: "text",
    hook: "You are waiting for the water to rise just enough that a route of submerged cells connects the corners." },
  { id: "largest_island", name: "Making a Large Island", category: "Graphs", emoji: "🧭", complexity: "O(R·C log RC)", input: "text",
    hook: "You are deciding where a single cell of landfill would create the largest island." },
  { id: "islands_ii", name: "Number of Islands II (Online)", category: "Graphs", emoji: "🧭", complexity: "O(k α(n))", input: "text",
    hook: "You are counting islands as land appears one cell at a time, merging neighbours as they touch." },
  { id: "floyd_warshall", name: "Floyd–Warshall (All-Pairs Shortest Paths)", category: "Graphs", emoji: "📐", complexity: "O(V³)", input: "text",
    hook: "You are a cartographer filling a distance table between every pair of cities, one detour city at a time." },
  { id: "city_fewest_neighbours", name: "City With the Fewest Neighbours in Reach", category: "Graphs", emoji: "📐", complexity: "O(V³)", input: "text",
    hook: "You are choosing the city with the fewest neighbours within reach once every road has been measured." },
  { id: "stock_ii", name: "Best Time to Buy & Sell Stock II (Unlimited)", category: "DP", emoji: "📈", complexity: "O(n)", input: "text",
    hook: "You are buying and selling as often as you like, holding at most one share at a time." },
  { id: "stock_iii", name: "Best Time to Buy & Sell Stock III (≤ 2 Trades)", category: "DP", emoji: "📈", complexity: "O(n)", input: "text",
    hook: "You are squeezing the most profit out of at most two buy-sell rounds." },
  { id: "stock_iv", name: "Best Time to Buy & Sell Stock IV (≤ k Trades)", category: "DP", emoji: "📈", complexity: "O(n·k)", input: "text",
    hook: "You are squeezing the most profit out of at most k buy-sell rounds." },
  { id: "stock_cooldown", name: "Buy & Sell Stock With Cooldown", category: "DP", emoji: "📈", complexity: "O(n)", input: "text",
    hook: "You are trading as often as you like but must sit out a day after every sale." },
  { id: "stock_fee", name: "Buy & Sell Stock With Transaction Fee", category: "DP", emoji: "📈", complexity: "O(n)", input: "text",
    hook: "You are trading as often as you like while every sale costs a fee." },
  { id: "print_lis", name: "Print the Longest Increasing Subsequence", category: "DP", emoji: "📏", complexity: "O(n²)", input: "text",
    hook: "You are rebuilding the longest increasing climb by following predecessor arrows back." },
  { id: "largest_divisible_subset", name: "Largest Divisible Subset", category: "DP", emoji: "📏", complexity: "O(n²)", input: "text",
    hook: "You are building the longest chain of numbers in which each divides the next." },
  { id: "longest_string_chain", name: "Longest String Chain", category: "DP", emoji: "📏", complexity: "O(n²)", input: "text",
    hook: "You are chaining words where each one is the previous word plus a single letter." },
  { id: "longest_bitonic", name: "Longest Bitonic Subsequence", category: "DP", emoji: "📏", complexity: "O(n²)", input: "text",
    hook: "You are finding the longest ridge that climbs to a peak and then only descends." },
  { id: "number_of_lis", name: "Number of Longest Increasing Subsequences", category: "DP", emoji: "📏", complexity: "O(n²)", input: "text",
    hook: "You are counting how many different longest increasing climbs the sequence contains." },
  { id: "cycle_undirected_bfs", name: "Cycle Detection in an Undirected Graph (BFS)", category: "Graphs", emoji: "🕸️", complexity: "O(V + E)", input: "graph",
    hook: "You are walking a trail network level by level, watching for a path that loops back on itself." },
  { id: "cycle_undirected_dfs", name: "Cycle Detection in an Undirected Graph (DFS)", category: "Graphs", emoji: "🕸️", complexity: "O(V + E)", input: "graph",
    hook: "You are walking a trail network as deep as you can, watching for a path that loops back on itself." },
  { id: "bridges", name: "Bridges in a Graph (Tarjan)", category: "Graphs", emoji: "🕸️", complexity: "O(V + E)", input: "graph",
    hook: "You are a network engineer finding the single cables whose loss would disconnect the network." },
  { id: "articulation_points", name: "Articulation Points", category: "Graphs", emoji: "🕸️", complexity: "O(V + E)", input: "graph",
    hook: "You are a network engineer finding the servers whose loss would split the network in two." },
  { id: "connect_network_ops", name: "Operations to Make a Network Connected", category: "Graphs", emoji: "🕸️", complexity: "O(V + E)", input: "graph",
    hook: "You are counting how many spare cables must move so every computer is connected." },
  { id: "cycle_directed", name: "Cycle Detection in a Directed Graph (DFS)", category: "Graphs", emoji: "➡️", complexity: "O(V + E)", input: "graph",
    hook: "You are checking a chain of task dependencies for a loop that would deadlock the schedule." },
  { id: "safe_states", name: "Find Eventual Safe States", category: "Graphs", emoji: "➡️", complexity: "O(V + E)", input: "graph",
    hook: "You are finding the tasks from which every dependency chain terminates, with no way into a loop." },
  { id: "kosaraju", name: "Strongly Connected Components (Kosaraju)", category: "Graphs", emoji: "➡️", complexity: "O(V + E)", input: "graph",
    hook: "You are grouping a one-way network into clusters where everyone can reach everyone, with two sweeps." },
  { id: "shortest_path_dag", name: "Shortest Path in a DAG", category: "Graphs", emoji: "➡️", complexity: "O(V + E)", input: "graph",
    hook: "You are finding the fastest route when every road is one-way, relaxing in dependency order." },
  { id: "floor_ceil_bst", name: "Floor and Ceil in a BST", category: "Structures", emoji: "🌲", complexity: "O(n)", input: "text",
    hook: "You are finding the nearest folder names just below and just above a target, in one descent each." },
  { id: "kth_bst", name: "Kth Smallest and Largest in a BST", category: "Structures", emoji: "🌲", complexity: "O(n)", input: "text",
    hook: "You are finding the k-th folder alphabetically by counting an in-order walk." },
  { id: "lca_bst", name: "LCA in a BST", category: "Structures", emoji: "🌲", complexity: "O(n)", input: "text",
    hook: "You are finding the deepest folder that contains two given folders, descending while they stay on the same side." },
  { id: "successor_predecessor", name: "Inorder Successor / Predecessor in a BST", category: "Structures", emoji: "🌲", complexity: "O(n)", input: "text",
    hook: "You are finding the folders immediately after and before a given name." },
  { id: "two_sum_bst", name: "Two Sum in a BST", category: "Structures", emoji: "🌲", complexity: "O(n)", input: "text",
    hook: "You are finding two values in a sorted tree that sum to a target, closing in from both ends." },
  { id: "bst_from_preorder", name: "Construct a BST From Preorder", category: "Structures", emoji: "🌲", complexity: "O(n)", input: "text",
    hook: "You are rebuilding a directory tree from the order its folders were first opened." },
  { id: "validate_bst", name: "Check if a Tree is a BST", category: "Structures", emoji: "🌲", complexity: "O(n)", input: "text",
    hook: "You are checking that every folder respects the bounds set by all its ancestors, not just its parent." },
  { id: "recover_bst", name: "Recover a BST With Two Swapped Nodes", category: "Structures", emoji: "🌲", complexity: "O(n)", input: "text",
    hook: "You are finding and swapping back the two folders that were filed out of order." },
  { id: "largest_bst", name: "Largest BST in a Binary Tree", category: "Structures", emoji: "🌲", complexity: "O(n)", input: "text",
    hook: "You are finding the largest subtree that is still a valid sorted tree, reporting upward." },
  { id: "is_min_heap", name: "Check if an Array is a Min-Heap", category: "Structures", emoji: "⛰️", complexity: "O(n)", input: "text",
    hook: "You are checking that every ticket is served no later than the two below it." },
  { id: "min_to_max_heap", name: "Convert a Min-Heap to a Max-Heap", category: "Structures", emoji: "⛰️", complexity: "O(n)", input: "text",
    hook: "You are turning a smallest-first queue into a biggest-first one by re-settling every parent." },
  { id: "connect_sticks", name: "Minimum Cost to Connect Sticks", category: "Structures", emoji: "⛰️", complexity: "O(n)", input: "text",
    hook: "You are joining ropes into one, always joining the two shortest to keep the total cost down." },
  { id: "rank_replace", name: "Replace Elements by Their Rank", category: "Structures", emoji: "⛰️", complexity: "O(n)", input: "text",
    hook: "You are replacing every score with its rank among the distinct values." },
  { id: "top_k_frequent", name: "Top K Frequent Elements", category: "Structures", emoji: "⛰️", complexity: "O(n)", input: "text",
    hook: "You are finding the k most frequent values with a heap that never grows past k." },
  { id: "hand_of_straights", name: "Hand of Straights", category: "Structures", emoji: "⛰️", complexity: "O(n)", input: "text",
    hook: "You are splitting cards into hands of consecutive values, always starting from the smallest card left." },
  { id: "task_scheduler", name: "Task Scheduler", category: "Structures", emoji: "⛰️", complexity: "O(n)", input: "text",
    hook: "You are scheduling tasks on one CPU where repeats need a cooldown, idling only when forced." },
  { id: "median_stream", name: "Find Median From a Data Stream", category: "Structures", emoji: "⛰️", complexity: "O(n)", input: "text",
    hook: "You are tracking the median of a stream by balancing two heaps." },
  { id: "remove_outer_parens", name: "Remove Outermost Parentheses", category: "Patterns", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "You are removing the outermost pair from every bracket group, tracking depth as you go." },
  { id: "reverse_words", name: "Reverse Words in a String", category: "Patterns", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "You are reversing the order of the words while keeping each word intact." },
  { id: "largest_odd_number", name: "Largest Odd Number in a String", category: "Patterns", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "You are cutting a digit string at its last odd digit to get the biggest odd number it starts with." },
  { id: "longest_common_prefix", name: "Longest Common Prefix", category: "Patterns", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "You are lining words up and reading down the columns until they disagree." },
  { id: "isomorphic_strings", name: "Isomorphic Strings", category: "Patterns", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "You are checking whether one word becomes the other under a consistent letter-for-letter cipher." },
  { id: "rotate_string", name: "Rotate String", category: "Patterns", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "You are checking whether one word is the other spun around, by looking inside the word doubled." },
  { id: "sort_by_frequency", name: "Sort Characters by Frequency", category: "Patterns", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "You are rewriting a word with its most frequent letters first." },
  { id: "max_nesting_depth", name: "Maximum Nesting Depth of Parentheses", category: "Patterns", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "You are tracking how deeply the parentheses nest, with a single counter." },
  { id: "roman_to_integer", name: "Roman to Integer", category: "Patterns", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "You are adding numeral values, subtracting any that stand before a bigger one." },
  { id: "string_to_integer", name: "String to Integer (atoi)", category: "Patterns", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "You are reading a number out of messy text: skip spaces, take a sign, read digits, stop." },
  { id: "sum_of_beauty", name: "Sum of Beauty of All Substrings", category: "Patterns", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "You are summing, over every substring, the gap between its most and least frequent letters." },
  { id: "char_replacement", name: "Longest Repeating Character Replacement", category: "Patterns", emoji: "🪟", complexity: "O(n)", input: "text",
    hook: "You are finding the longest stretch that becomes one repeated letter with at most k edits." },
  { id: "aho_corasick", name: "Aho–Corasick (Multi-Pattern Search)", category: "Patterns", emoji: "🤖", complexity: "O(n + m + matches)", input: "text",
    hook: "You are scanning a document for a whole list of keywords at once, with failure links so you never re-read." },
  { id: "substring_hash", name: "Substring Equality by Rolling Hash", category: "Patterns", emoji: "#️⃣", complexity: "O(n) + O(1) per query", input: "text",
    hook: "You are comparing substrings by fingerprint so each check costs one subtraction." },
  { id: "tarjan_scc", name: "Strongly Connected Components (Tarjan)", category: "Graphs", emoji: "🌀", complexity: "O(V + E)", input: "text",
    hook: "You are grouping a one-way network into clusters where everyone can reach everyone." },
  { id: "two_sat", name: "2-SAT (Implication Graph + SCC)", category: "Graphs", emoji: "⚖️", complexity: "O(n + m)", input: "text",
    hook: "You are deciding whether a set of either-or rules can all hold at once, via an implication graph." },
  { id: "lexicographic_topo", name: "Lexicographically Smallest Topological Order", category: "Graphs", emoji: "🔤", complexity: "O((V + E) log V)", input: "text",
    hook: "You are ordering dependent tasks, always picking the alphabetically first task that is ready." },
  { id: "convex_hull", name: "Convex Hull (Monotone Chain)", category: "Math", emoji: "🪢", complexity: "O(n log n)", input: "text",
    hook: "You are stretching the shortest fence around a scattered herd of points." },
  { id: "polygon_area", name: "Polygon Area (Shoelace Formula)", category: "Math", emoji: "📐", complexity: "O(n)", input: "text",
    hook: "You are measuring a plot of land by walking its corners and lacing the coordinates together." },
  { id: "closest_pair", name: "Closest Pair of Points (Divide & Conquer)", category: "Math", emoji: "📏", complexity: "O(n log n)", input: "text",
    hook: "You are finding the two closest towns on a map without comparing every pair." },
  { id: "digit_dp", name: "Digit DP (Count Numbers With Digit Sum S)", category: "DP", emoji: "🔢", complexity: "O(L·S·10)", input: "text",
    hook: "You are counting how many numbers up to N have digits summing to S, one digit position at a time." },
  { id: "tree_robber", name: "House Robber on a Tree", category: "DP", emoji: "🏠", complexity: "O(n)", input: "text",
    hook: "You are robbing linked treehouses without hitting two that are directly connected." },
  { id: "sos_dp", name: "Sum Over Subsets (SOS DP)", category: "DP", emoji: "🧮", complexity: "O(n·2ⁿ)", input: "text",
    hook: "You are computing, for every bitmask, the total over all of its sub-masks, one bit at a time." },
  { id: "sum_distances_tree", name: "Sum of Distances in a Tree (Rerooting)", category: "DP", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "You are computing every node's total distance to all the others by solving the root and rerooting." },
  { id: "bit_kth", name: "K-th Smallest With a Fenwick Tree", category: "Structures", emoji: "🌲", complexity: "O(log n) per op", input: "text",
    hook: "You are finding the k-th smallest value by descending a Fenwick tree of counts." },
  { id: "inversions_bit", name: "Count Inversions With a Fenwick Tree", category: "Structures", emoji: "🔀", complexity: "O(n log n)", input: "text",
    hook: "You are counting out-of-order pairs by inserting scores right to left into a Fenwick tree." },
  { id: "prefix_sum_2d", name: "2-D Prefix Sums (Rectangle Queries)", category: "Patterns", emoji: "▦", complexity: "O(RC) + O(1) per query", input: "text",
    hook: "You are pre-totalling a grid so any rectangle's sum is four lookups." },
  { id: "a_star_grid", name: "A* Search on a Grid", category: "Graphs", emoji: "⭐", complexity: "O(E log V)", input: "text",
    hook: "You are crossing a maze with a compass that always points roughly at the exit, so you waste few steps." },
  { id: "best_first_grid", name: "Greedy Best-First Search on a Grid", category: "Graphs", emoji: "🧭", complexity: "O(E log V)", input: "text",
    hook: "You are crossing a maze by always stepping toward whatever looks closest to the exit — fast, but not always shortest." },
  { id: "zero_one_bfs", name: "0-1 BFS (Minimum Cost Path)", category: "Graphs", emoji: "🔀", complexity: "O(V + E)", input: "text",
    hook: "You are crossing a grid where some moves are free and others cost one, always taking the free moves first." },
  { id: "max_flow", name: "Maximum Flow (Edmonds–Karp)", category: "Graphs", emoji: "🚰", complexity: "O(V·E²)", input: "text",
    hook: "You are pushing as much water from the source to the sink as the pipes allow." },
  { id: "min_cut", name: "Minimum s-t Cut", category: "Graphs", emoji: "✂️", complexity: "O(V·E²)", input: "text",
    hook: "You are finding the cheapest set of pipes whose removal stops all flow." },
  { id: "bipartite_matching", name: "Maximum Bipartite Matching (Kuhn)", category: "Graphs", emoji: "💞", complexity: "O(V·E)", input: "text",
    hook: "You are pairing applicants with jobs, nudging earlier matches aside to fit one more in." },
  { id: "lca_lifting", name: "Lowest Common Ancestor (Binary Lifting)", category: "Structures", emoji: "🪜", complexity: "O(log n) per query", input: "text",
    hook: "You are finding the nearest common ancestor of two nodes with power-of-two jump pointers." },
  { id: "kth_ancestor", name: "K-th Ancestor (Binary Lifting)", category: "Structures", emoji: "🪜", complexity: "O(log n) per query", input: "text",
    hook: "You are finding an ancestor k generations up by taking power-of-two jumps." },
  { id: "tsp_bitmask", name: "Travelling Salesman (Bitmask DP)", category: "DP", emoji: "🧳", complexity: "O(2ⁿ·n²)", input: "text",
    hook: "You are planning the cheapest tour that visits every city once, remembering the best cost for each set of visited cities." },
  { id: "assignment_bitmask", name: "Job Assignment (Bitmask DP)", category: "DP", emoji: "👷", complexity: "O(2ⁿ·n)", input: "text",
    hook: "You are assigning every job to a different worker for the lowest total cost, one subset of jobs at a time." },
  { id: "sparse_table", name: "Sparse Table (Range Minimum Query)", category: "Structures", emoji: "📊", complexity: "O(n log n) + O(1)", input: "text",
    hook: "You are pre-computing power-of-two blocks so any range minimum is two lookups." },
  { id: "sqrt_decomposition", name: "Sqrt Decomposition (Range Sum)", category: "Structures", emoji: "🧱", complexity: "O(√n) per op", input: "text",
    hook: "You are splitting the board into blocks of about √n so range sums and updates both stay cheap." },
  { id: "lazy_segment_tree", name: "Segment Tree With Lazy Propagation", category: "Structures", emoji: "🌲", complexity: "O(log n) per op", input: "text",
    hook: "You are adding to whole ranges of scores and summing ranges, deferring work until it is needed." },
  { id: "extended_gcd", name: "Extended Euclidean Algorithm", category: "Math", emoji: "🔢", complexity: "O(log min(a,b))", input: "text",
    hook: "You are running Euclid's division while keeping receipts, so the gcd comes back as a combination of a and b." },
  { id: "mod_inverse", name: "Modular Multiplicative Inverse", category: "Math", emoji: "🔑", complexity: "O(log m)", input: "text",
    hook: "You are finding the number that undoes a multiplication under a modulus." },
  { id: "ncr_mod", name: "nCr mod p (Fermat Inverse)", category: "Math", emoji: "🎲", complexity: "O(n + log p)", input: "text",
    hook: "You are counting ways to pick a team when the number is too big to hold, so you work modulo a prime." },
  { id: "euler_totient", name: "Euler's Totient Function", category: "Math", emoji: "φ", complexity: "O(√n)", input: "text",
    hook: "You are counting how many numbers below n share no factor with it." },
  { id: "spf_sieve", name: "Smallest Prime Factor Sieve", category: "Math", emoji: "🧮", complexity: "O(n log log n)", input: "text",
    hook: "You are stamping every number with its smallest prime factor so later factorisations are instant." },
  { id: "crt", name: "Chinese Remainder Theorem", category: "Math", emoji: "🧩", complexity: "O(k log M)", input: "text",
    hook: "You are finding the one day that satisfies several repeating schedules at once." },
  { id: "suffix_array", name: "Suffix Array (Prefix Doubling)", category: "Patterns", emoji: "🔤", complexity: "O(n log² n)", input: "text",
    hook: "You are sorting all suffixes of a word by doubling the prefix length you rank on each round." },
  { id: "lcp_kasai", name: "LCP Array (Kasai)", category: "Patterns", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "You are measuring how much each suffix shares with its sorted neighbour, reusing the previous answer." },
  { id: "longest_repeated_substring", name: "Longest Repeated Substring (SA + LCP)", category: "Patterns", emoji: "🔁", complexity: "O(n log n)", input: "text",
    hook: "You are finding the longest fragment that occurs twice, via sorted suffixes and their overlaps." },
  { id: "euler_path", name: "Euler Path / Circuit (Hierholzer)", category: "Graphs", emoji: "✏️", complexity: "O(E)", input: "text",
    hook: "You are planning a stroll that crosses every bridge in town exactly once." },
  { id: "longest_path_dag", name: "Longest Path in a DAG", category: "Graphs", emoji: "📈", complexity: "O(V + E)", input: "text",
    hook: "You are finding the longest possible trip through a one-way road network." },
  { id: "count_paths_dag", name: "Count Paths in a DAG", category: "Graphs", emoji: "🛤️", complexity: "O(V + E)", input: "text",
    hook: "You are counting every distinct route through a one-way road network." },
  { id: "matrix_exponentiation", name: "Matrix Exponentiation (Fibonacci)", category: "Math", emoji: "🧮", complexity: "O(log n)", input: "text",
    hook: "You are reaching the n-th Fibonacci number by squaring a tiny matrix instead of counting up." },
  { id: "ternary_search", name: "Ternary Search (Peak of a Unimodal Array)", category: "Searching", emoji: "⛰️", complexity: "O(log n)", input: "text",
    hook: "You are finding the peak of a single-humped ridge by probing two points at a time." },
  { id: "meet_in_middle", name: "Meet in the Middle (Subset Sums ≤ S)", category: "Patterns", emoji: "🤝", complexity: "O(2^(n/2)·n)", input: "text",
    hook: "You are counting subset sums by enumerating two half-piles and pairing them with a binary search." },
  { id: "nim", name: "Nim (XOR of Piles)", category: "Math", emoji: "🪨", complexity: "O(n)", input: "text",
    hook: "You are deciding whether the player to move in a matchstick game can force a win." },
  { id: "grundy_numbers", name: "Grundy Numbers (Subtraction Game)", category: "Math", emoji: "🎯", complexity: "O(n·m)", input: "text",
    hook: "You are labelling every pile size as winning or losing before the pebble game begins." },
  { id: "optimal_game", name: "Optimal Strategy for a Coin Game", category: "Math", emoji: "🪙", complexity: "O(n²)", input: "text",
    hook: "You and a rival take coins from either end of a row; you plan so your haul is the best possible." },
  { id: "build_pre_in", name: "Construct a Binary Tree from Preorder & Inorder", category: "Structures", emoji: "🌱", complexity: "O(n)", input: "text",
    hook: "You are rebuilding a tree from two traversal logs, taking roots from the front of the preorder list." },
  { id: "build_post_in", name: "Construct a Binary Tree from Postorder & Inorder", category: "Structures", emoji: "🌱", complexity: "O(n)", input: "text",
    hook: "You are rebuilding a tree from two traversal logs, taking roots from the end of the postorder list." },
  { id: "serialize_tree", name: "Serialize and Deserialize a Binary Tree", category: "Structures", emoji: "📦", complexity: "O(n)", input: "text",
    hook: "You are writing a tree as a line of text with markers for gaps, so it can be rebuilt exactly." },
  { id: "morris_inorder", name: "Morris Inorder Traversal", category: "Structures", emoji: "🧵", complexity: "O(n), O(1) space", input: "text",
    hook: "You are walking folders in name order with temporary threads instead of a stack." },
  { id: "morris_preorder", name: "Morris Preorder Traversal", category: "Structures", emoji: "🧵", complexity: "O(n), O(1) space", input: "text",
    hook: "You are walking folders parent-first with temporary threads instead of a stack." },
  { id: "flatten_tree", name: "Flatten a Binary Tree to a Linked List", category: "Structures", emoji: "📜", complexity: "O(n)", input: "text",
    hook: "You are unrolling a directory tree into a single chain in preorder, in place." },
  { id: "identical_trees", name: "Check if Two Trees are Identical", category: "Structures", emoji: "👯", complexity: "O(n)", input: "text",
    hook: "You are checking whether two directory trees match folder for folder." },
  { id: "merge_two_bsts", name: "Merge Two BSTs (sorted output)", category: "Structures", emoji: "🔀", complexity: "O(m + n)", input: "text",
    hook: "You are merging two sorted trees into one sorted listing, like two sorted shelves." },
  { id: "stack_array", name: "Implement a Stack Using an Array", category: "Structures", emoji: "🥞", complexity: "O(1) per op", input: "text",
    hook: "You are running a stack inside an array with a single top index." },
  { id: "queue_array", name: "Implement a Queue Using an Array", category: "Structures", emoji: "🎫", complexity: "O(1) per op", input: "text",
    hook: "You are running a queue in a fixed ring of seats, so nobody ever shuffles along." },
  { id: "stack_using_queue", name: "Implement a Stack Using a Queue", category: "Structures", emoji: "🔄", complexity: "O(n) push", input: "text",
    hook: "You are running a stack with one queue by rotating it after every push." },
  { id: "queue_using_stacks", name: "Implement a Queue Using Stacks", category: "Structures", emoji: "🔄", complexity: "O(1) amortised", input: "text",
    hook: "You are running a queue with two stacks: pour one into the other only when the second runs dry." },
  { id: "stack_linkedlist", name: "Implement a Stack Using a Linked List", category: "Structures", emoji: "🚃", complexity: "O(1) per op", input: "text",
    hook: "You are running a stack as a train: couple and uncouple only at the front." },
  { id: "queue_linkedlist", name: "Implement a Queue Using a Linked List", category: "Structures", emoji: "🚃", complexity: "O(1) per op", input: "text",
    hook: "You are running a queue as a train: join at the back, leave from the front." },
  { id: "min_stack", name: "Implement a Min Stack", category: "Structures", emoji: "📉", complexity: "O(1) per op", input: "text",
    hook: "You are keeping a stack that can report its smallest plate instantly." },
  { id: "lru_cache", name: "LRU Cache", category: "Structures", emoji: "🗃️", complexity: "O(1) per op", input: "text",
    hook: "You are running a cache that drops the entry untouched for longest when it is full." },
  { id: "lfu_cache", name: "LFU Cache", category: "Structures", emoji: "🗃️", complexity: "O(1) per op", input: "text",
    hook: "You are running a cache that drops the least-used entry when full, breaking ties by age." },
  { id: "design_twitter", name: "Design Twitter", category: "Structures", emoji: "🐦", complexity: "O(n log k)", input: "text",
    hook: "You are serving each user a feed of the newest posts from the people they follow." },
  { id: "clone_random_list", name: "Clone a Linked List With Random Pointers", category: "Structures", emoji: "🧬", complexity: "O(n), O(1) space", input: "text",
    hook: "You are duplicating a train whose carriages also point at random other carriages, without a lookup table." },
  { id: "flatten_list", name: "Flatten a Linked List (sorted columns)", category: "Structures", emoji: "🪜", complexity: "O(N·k)", input: "text",
    hook: "You are merging several sorted sidings into one long train, one siding at a time." },
  { id: "merge_k_lists", name: "Merge K Sorted Lists", category: "Structures", emoji: "🧺", complexity: "O(N log k)", input: "text",
    hook: "You are merging several sorted trains, always taking the smallest front carriage." },
  { id: "bracket_reversals", name: "Minimum Bracket Reversals to Balance", category: "Patterns", emoji: "🔃", complexity: "O(n)", input: "text",
    hook: "You are counting the fewest braces to flip so a chain of braces balances." },
  { id: "count_and_say", name: "Count and Say", category: "Patterns", emoji: "🗣️", complexity: "O(total length)", input: "text",
    hook: "You are reading each term aloud — two 1s, one 2 — to build the next one." },
  { id: "longest_happy_prefix", name: "Longest Happy Prefix (LPS)", category: "Patterns", emoji: "😊", complexity: "O(n)", input: "text",
    hook: "You are finding the longest border of a word — a prefix that reappears as its suffix." },
  { id: "count_palindromic_subseq", name: "Count Palindromic Subsequences", category: "Patterns", emoji: "🪞", complexity: "O(n²)", input: "text",
    hook: "You are counting every palindrome hiding as a subsequence, over widening intervals." },
  { id: "distinct_substrings", name: "Number of Distinct Substrings (Trie)", category: "Structures", emoji: "🌳", complexity: "O(n²)", input: "text",
    hook: "You are cataloguing every distinct fragment of a word by threading its suffixes into a trie." },
  { id: "max_xor_pair", name: "Maximum XOR of Two Numbers (Trie)", category: "Structures", emoji: "⊕", complexity: "O(n·B)", input: "text",
    hook: "You are pairing numbers so their bits disagree as high up as possible." },
  { id: "max_xor_queries", name: "Maximum XOR With an Element From an Array", category: "Structures", emoji: "⊕", complexity: "O((n + q)·B)", input: "text",
    hook: "You are answering XOR pairings while only numbers under each query's cap are allowed in." },
  { id: "trie_advanced", name: "Trie With Counts (insert, count, erase)", category: "Structures", emoji: "🌳", complexity: "O(L) per op", input: "text",
    hook: "You are keeping a dictionary that also knows how many words share each prefix, and can forget words." },
  { id: "ninja_friends", name: "Ninja and His Friends (Cherry Pickup II)", category: "DP", emoji: "🍫", complexity: "O(r·c²·9)", input: "text",
    hook: "You are steering two robots down an orchard together so they collect the most cherries." },
  { id: "max_sum_combination", name: "Maximum Sum Combinations", category: "Structures", emoji: "➕", complexity: "O(k log k)", input: "text",
    hook: "You are listing the k largest sums of one score from each of two boards." },
  { id: "accounts_merge", name: "Accounts Merge", category: "Graphs", emoji: "📇", complexity: "O(E α(n))", input: "text",
    hook: "You are tidying a contact book: any two cards that share an email belong to the same person." },
  { id: "ll_insert_head", name: "Insert at the Head of a Linked List", category: "Structures", emoji: "🚃", complexity: "O(1)", input: "text",
    hook: "You are coupling a new carriage at the front — no walk needed." },
  { id: "ll_delete_head", name: "Delete the Head of a Linked List", category: "Structures", emoji: "🚃", complexity: "O(1)", input: "text",
    hook: "You are uncoupling the front carriage: the head simply moves back one." },
  { id: "ll_length", name: "Length of a Linked List", category: "Structures", emoji: "🚃", complexity: "O(n)", input: "text",
    hook: "You are walking the train from the engine to the end, counting carriages." },
  { id: "ll_search", name: "Search in a Linked List", category: "Structures", emoji: "🚃", complexity: "O(n)", input: "text",
    hook: "You are walking the train carriage by carriage until you find the one you want." },
  { id: "dll_insert_head", name: "Insert Before the Head of a Doubly Linked List", category: "Structures", emoji: "🚋", complexity: "O(1)", input: "text",
    hook: "You are coupling a new carriage at the front of a two-way train." },
  { id: "dll_delete_head", name: "Delete the Head of a Doubly Linked List", category: "Structures", emoji: "🚋", complexity: "O(1)", input: "text",
    hook: "You are uncoupling the front carriage of a two-way train and clearing its backward link." },
  { id: "dll_pairs_sum", name: "Pairs With a Given Sum in a Sorted DLL", category: "Structures", emoji: "🚋", complexity: "O(n)", input: "text",
    hook: "You are walking a sorted two-way train from both ends to find pairs with a target total." },
  { id: "dll_remove_duplicates", name: "Remove Duplicates From a Sorted DLL", category: "Structures", emoji: "🚋", complexity: "O(n)", input: "text",
    hook: "You are removing repeated carriages from a sorted two-way train in a single pass." },
  { id: "ll_reverse_recursive", name: "Reverse a Linked List (Recursive)", category: "Structures", emoji: "🔁", complexity: "O(n)", input: "text",
    hook: "Each call reverses the rest of the train first, then flips its own coupling." },
  { id: "loop_length", name: "Length of a Loop in a Linked List", category: "Structures", emoji: "➰", complexity: "O(n)", input: "text",
    hook: "Two inspectors moving at different speeds meet inside a loop; one more lap measures it." },
  { id: "sort_012_list", name: "Sort a Linked List of 0s, 1s and 2s", category: "Structures", emoji: "🚥", complexity: "O(n)", input: "text",
    hook: "You are sorting carriages labelled 0, 1 and 2 by shunting each onto its own siding, then rejoining them." },
  { id: "sort_list", name: "Sort a Linked List (Merge Sort)", category: "Structures", emoji: "🔀", complexity: "O(n log n)", input: "text",
    hook: "You are sorting a train by splitting it in half, sorting each half and merging — no extra yard needed." },
  { id: "y_intersection", name: "Intersection Point of a Y-Shaped Linked List", category: "Structures", emoji: "🔱", complexity: "O(n + m)", input: "text",
    hook: "Two trains share a tail; two walkers who swap lines at the end meet exactly where they join." },
  { id: "reverse_k_group", name: "Reverse a Linked List in Groups of K", category: "Structures", emoji: "🔁", complexity: "O(n)", input: "text",
    hook: "You are reversing the train k carriages at a time, leaving a short tail as it is." },
  { id: "search_rotated_ii", name: "Search in Rotated Sorted Array II (duplicates)", category: "Searching", emoji: "🔄", complexity: "O(log n) avg", input: "text",
    hook: "You are searching a rotated shelf where repeated values can hide which half is sorted." },
  { id: "median_two_sorted", name: "Median of Two Sorted Arrays", category: "Searching", emoji: "⚖️", complexity: "O(log min(n,m))", input: "text",
    hook: "You are finding the median across two sorted shelves by cutting each in the right place." },
  { id: "kth_two_sorted", name: "K-th Element of Two Sorted Arrays", category: "Searching", emoji: "🎯", complexity: "O(log min(n,m))", input: "text",
    hook: "You are finding the k-th smallest book across two sorted shelves without merging them." },
  { id: "gas_station", name: "Minimise Max Distance to Gas Station", category: "Searching", emoji: "⛽", complexity: "O(n log R)", input: "text",
    hook: "You are placing k new fuel stations so the longest gap between any two is as short as possible." },
  { id: "peak_element_ii", name: "Find a Peak Element II (matrix)", category: "Searching", emoji: "⛰️", complexity: "O(n log m)", input: "text",
    hook: "You are finding a cell higher than its four neighbours by halving the columns." },
  { id: "matrix_median", name: "Median of a Row-Wise Sorted Matrix", category: "Searching", emoji: "▦", complexity: "O(r log c log R)", input: "text",
    hook: "You are finding the median of a grid of sorted shelves without pouring them together." },
  { id: "print_1_to_n", name: "Print 1 to N Using Recursion", category: "Patterns", emoji: "🔢", complexity: "O(n)", input: "text",
    hook: "Each call prints its number, then asks the next call to continue." },
  { id: "print_n_to_1", name: "Print N to 1 Using Recursion", category: "Patterns", emoji: "🔢", complexity: "O(n)", input: "text",
    hook: "Each call recurses first and prints only on the way back up." },
  { id: "recursive_bubble_sort", name: "Recursive Bubble Sort", category: "Sorting", emoji: "🫧", complexity: "O(n²)", input: "text",
    hook: "Each call bubbles the biggest remaining score to the end, then recurses on the rest." },
  { id: "recursive_insertion_sort", name: "Recursive Insertion Sort", category: "Sorting", emoji: "🃏", complexity: "O(n²)", input: "text",
    hook: "Each call slides one more score into the sorted prefix, then recurses." },
  { id: "count_good_numbers", name: "Count Good Numbers", category: "Patterns", emoji: "✅", complexity: "O(log n)", input: "text",
    hook: "You are counting licence plates where even slots take even digits and odd slots take primes." },
  { id: "sort_stack", name: "Sort a Stack Using Recursion", category: "Patterns", emoji: "🥞", complexity: "O(n²)", input: "text",
    hook: "You are sorting a stack with recursion alone, inserting each plate in its place." },
  { id: "reverse_stack", name: "Reverse a Stack Using Recursion", category: "Patterns", emoji: "🥞", complexity: "O(n²)", input: "text",
    hook: "You are reversing a stack with recursion alone, inserting each plate at the bottom." },
  { id: "recursive_atoi", name: "Recursive atoi()", category: "Patterns", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "Each call eats one digit and multiplies the running value by ten." },
  { id: "word_break", name: "Word Break", category: "Patterns", emoji: "🧩", complexity: "O(n·w·L)", input: "text",
    hook: "You are checking whether a string splits cleanly into dictionary words, working from the end." },
  { id: "m_coloring", name: "M-Coloring Problem", category: "Patterns", emoji: "🎨", complexity: "O(mⁿ)", input: "text",
    hook: "You are painting a map with m colours so no two neighbouring regions share one." },
  { id: "sudoku_solver", name: "Sudoku Solver", category: "Patterns", emoji: "🔢", complexity: "O(9^blanks)", input: "text",
    hook: "You are filling a Sudoku one blank at a time, erasing and retrying the moment a digit leads nowhere." },
  { id: "expression_add_operators", name: "Expression Add Operators", category: "Patterns", emoji: "➕", complexity: "O(4ⁿ)", input: "text",
    hook: "You are slotting +, − and × between digits until the expression hits the target." },
  { id: "valid_paren_star", name: "Valid Parenthesis String (with *)", category: "Greedy", emoji: "✳️", complexity: "O(n)", input: "text",
    hook: "You are checking bracket balance when a * can be either bracket or nothing." },
  { id: "shortest_job_first", name: "Shortest Job First (SJF) Scheduling", category: "Greedy", emoji: "⏱️", complexity: "O(n log n)", input: "text",
    hook: "You are running the shortest jobs first so the least total time is spent waiting." },
  { id: "lru_page_faults", name: "LRU Page Replacement (Page Faults)", category: "Greedy", emoji: "🗂️", complexity: "O(n·c)", input: "text",
    hook: "You are loading pages into a few frames, evicting the least recently used and counting the misses." },
  { id: "insert_interval", name: "Insert Interval", category: "Greedy", emoji: "📏", complexity: "O(n)", input: "text",
    hook: "You are inserting a new meeting into a sorted calendar, merging it with anything it overlaps." },
  { id: "non_overlapping_intervals", name: "Non-overlapping Intervals", category: "Greedy", emoji: "📏", complexity: "O(n log n)", input: "text",
    hook: "You are cancelling as few meetings as possible so none overlap, keeping the ones that end earliest." },
  { id: "greater_to_right", name: "Number of Greater Elements to the Right", category: "Structures", emoji: "↗️", complexity: "O(n²)", input: "text",
    hook: "You are counting, for each score, how many later scores beat it." },
  { id: "sum_subarray_ranges", name: "Sum of Subarray Ranges", category: "Structures", emoji: "📐", complexity: "O(n)", input: "text",
    hook: "You are summing max minus min over every stretch, with two monotonic stacks." },
  { id: "celebrity", name: "The Celebrity Problem", category: "Structures", emoji: "⭐", complexity: "O(n)", input: "text",
    hook: "At a party you must find the one guest everybody knows who knows nobody, with as few questions as possible." },
  { id: "cut_stick", name: "Minimum Cost to Cut a Stick", category: "DP", emoji: "🪵", complexity: "O(c³)", input: "text",
    hook: "You are sawing a plank at fixed marks, ordering the cuts so the total sawing length is least." },
  { id: "burst_balloons", name: "Burst Balloons", category: "DP", emoji: "🎈", complexity: "O(n³)", input: "text",
    hook: "You are popping balloons for coins, deciding which to pop last in every stretch." },
  { id: "boolean_evaluation", name: "Evaluate Boolean Expression to True", category: "DP", emoji: "🔣", complexity: "O(n³)", input: "text",
    hook: "You are counting the ways to bracket a chain of switches so the whole circuit reads true." },
  { id: "palindrome_partition_ii", name: "Palindrome Partitioning II (Min Cuts)", category: "DP", emoji: "✂️", complexity: "O(n²)", input: "text",
    hook: "You are slicing a word into palindromic pieces with as few cuts as possible." },
  { id: "partition_array_max_sum", name: "Partition Array for Maximum Sum", category: "DP", emoji: "🧱", complexity: "O(n·k)", input: "text",
    hook: "You are cutting a row into groups of at most k, promoting every member to the group's best." },
  { id: "min_subset_diff", name: "Partition Into Two Subsets With Minimum Difference", category: "DP", emoji: "⚖️", complexity: "O(n·sum)", input: "text",
    hook: "You are dividing a pile of weights into two sides that come as close to balancing as possible." },
  { id: "count_partitions_diff", name: "Count Partitions With Given Difference", category: "DP", emoji: "⚖️", complexity: "O(n·sum)", input: "text",
    hook: "You are counting ways to split players into two teams whose strength differs by exactly d." },
  { id: "target_sum", name: "Target Sum", category: "DP", emoji: "➕", complexity: "O(n·sum)", input: "text",
    hook: "You are putting + or − in front of each number so the total hits the target, counting every way." },
  { id: "max_rectangle_ones", name: "Maximal Rectangle of 1s", category: "DP", emoji: "▦", complexity: "O(r·c)", input: "text",
    hook: "You are finding the largest rectangle of open ground in a map of fields and fences." },
  { id: "largest_element", name: "Largest Element in an Array", category: "Patterns", emoji: "🏔️", complexity: "O(n)", input: "text",
    hook: "You are finding the highest score with one sweep." },
  { id: "check_sorted", name: "Check if an Array is Sorted", category: "Patterns", emoji: "📈", complexity: "O(n)", input: "text",
    hook: "You are checking that no score on the board is lower than the one before it." },
  { id: "linear_search", name: "Linear Search", category: "Patterns", emoji: "🔎", complexity: "O(n)", input: "text",
    hook: "You are scanning the board one entry at a time for a particular score." },
  { id: "union_sorted", name: "Union of Two Sorted Arrays", category: "Patterns", emoji: "🔗", complexity: "O(n + m)", input: "text",
    hook: "You are merging two sorted boards into one list with no repeats." },
  { id: "intersection_sorted", name: "Intersection of Two Sorted Arrays", category: "Patterns", emoji: "🔗", complexity: "O(n + m)", input: "text",
    hook: "You are listing the scores that appear on both sorted boards." },
  { id: "missing_number", name: "Find the Missing Number", category: "Patterns", emoji: "🕳️", complexity: "O(n)", input: "text",
    hook: "You are finding the one ticket number missing from 0..n by cancelling pairs with XOR." },
  { id: "max_consecutive_ones", name: "Maximum Consecutive Ones", category: "Patterns", emoji: "1️⃣", complexity: "O(n)", input: "text",
    hook: "You are finding the longest run of wins in a row." },
  { id: "rearrange_by_sign", name: "Rearrange Array Elements by Sign", category: "Patterns", emoji: "±", complexity: "O(n)", input: "text",
    hook: "You are arranging scores so positives and negatives alternate, keeping their order." },
  { id: "max_product_subarray", name: "Maximum Product Subarray", category: "Patterns", emoji: "✖️", complexity: "O(n)", input: "text",
    hook: "You are finding the stretch with the largest product, tracking the smallest too in case a negative flips it." },
  { id: "longest_sum_k_any", name: "Longest Subarray With Sum K (any sign)", category: "Structures", emoji: "🗺️", complexity: "O(n)", input: "text",
    hook: "You are finding the longest ledger stretch summing to k, even with refunds in the mix." },
  { id: "count_sum_k", name: "Count Subarrays With Sum K", category: "Structures", emoji: "🗺️", complexity: "O(n)", input: "text",
    hook: "You are counting the stretches of a ledger that add up to exactly k, using running totals as receipts." },
  { id: "largest_zero_sum", name: "Largest Subarray With Sum 0", category: "Structures", emoji: "0️⃣", complexity: "O(n)", input: "text",
    hook: "You are finding the longest stretch of a ledger that nets out to exactly zero." },
  { id: "count_xor_k", name: "Count Subarrays With XOR K", category: "Structures", emoji: "⊕", complexity: "O(n)", input: "text",
    hook: "You are counting stretches whose XOR hits a target, keeping running XORs as receipts." },
  { id: "longest_consecutive", name: "Longest Consecutive Sequence", category: "Structures", emoji: "🔢", complexity: "O(n)", input: "text",
    hook: "You are finding the longest run of consecutive numbers hidden in a shuffled pile." },
  { id: "majority_n3", name: "Majority Elements (> n/3)", category: "Patterns", emoji: "🗳️", complexity: "O(n)", input: "text",
    hook: "You are finding the scores that appear more than a third of the time, with two candidates." },
  { id: "repeating_missing", name: "Find the Repeating and Missing Numbers", category: "Patterns", emoji: "🔁", complexity: "O(n)", input: "text",
    hook: "You are finding the duplicated and the missing number from sums alone." },
  { id: "three_sum", name: "3 Sum", category: "Patterns", emoji: "3️⃣", complexity: "O(n²)", input: "text",
    hook: "You are finding every three scores that add to zero, with one anchor and two pointers." },
  { id: "four_sum", name: "4 Sum", category: "Patterns", emoji: "4️⃣", complexity: "O(n³)", input: "text",
    hook: "You are finding every four scores that add to a target, with two anchors and two pointers." },
  { id: "set_matrix_zeros", name: "Set Matrix Zeros", category: "Patterns", emoji: "0️⃣", complexity: "O(r·c)", input: "text",
    hook: "You are blanking out every row and column that holds a zero, marking first so the zeros do not spread." },
  { id: "rotate_matrix", name: "Rotate a Matrix by 90°", category: "Patterns", emoji: "🔄", complexity: "O(n²)", input: "text",
    hook: "You are turning a picture a quarter turn in place: flip it over the diagonal, then mirror each row." },
  { id: "spiral_order", name: "Spiral Traversal of a Matrix", category: "Patterns", emoji: "🌀", complexity: "O(r·c)", input: "text",
    hook: "You are reading a grid the way a snail walks: around the edge, then inward." },
  { id: "pascal_triangle", name: "Pascal's Triangle", category: "Patterns", emoji: "🔺", complexity: "O(n²)", input: "text",
    hook: "You are stacking rows where every number is the sum of the two above it." },
  { id: "merge_no_space", name: "Merge Two Sorted Arrays Without Extra Space", category: "Patterns", emoji: "🧩", complexity: "O((n+m) log(n+m))", input: "text",
    hook: "You are merging two sorted boards without a third one, comparing at shrinking gaps." },
  { id: "count_inversions", name: "Count Inversions", category: "Sorting", emoji: "🔀", complexity: "O(n log n)", input: "text",
    hook: "You are counting the pairs that are out of order, tallied during a merge sort." },
  { id: "reverse_pairs", name: "Reverse Pairs", category: "Sorting", emoji: "🔀", complexity: "O(n log n)", input: "text",
    hook: "You are counting pairs where an earlier score is more than double a later one, during a merge sort." },
  { id: "count_digits", name: "Count Digits of a Number", category: "Math", emoji: "🔢", complexity: "O(log n)", input: "text",
    hook: "You are peeling digits off a number one at a time and counting them." },
  { id: "reverse_number", name: "Reverse a Number", category: "Math", emoji: "↩️", complexity: "O(log n)", input: "text",
    hook: "You are peeling digits off one end and stacking them onto the other." },
  { id: "palindrome_number", name: "Palindrome Number", category: "Math", emoji: "🪞", complexity: "O(log n)", input: "text",
    hook: "You are checking whether a number reads the same reversed." },
  { id: "armstrong_number", name: "Armstrong Number", category: "Math", emoji: "💪", complexity: "O(log n)", input: "text",
    hook: "You are testing whether a number is the sum of its own digits raised to a power." },
  { id: "print_divisors", name: "Print All Divisors", category: "Math", emoji: "➗", complexity: "O(√n)", input: "text",
    hook: "You are listing divisors in pairs, so you only test up to the square root." },
  { id: "check_prime", name: "Check for a Prime Number", category: "Math", emoji: "🔐", complexity: "O(√n)", input: "text",
    hook: "You are a gatekeeper who tests divisors only up to the square root before letting a prime through." },
  { id: "factorial", name: "Factorial of a Number", category: "Patterns", emoji: "❗", complexity: "O(n)", input: "text",
    hook: "You are multiplying up from 1 to n, one factor at a time." },
  { id: "sum_first_n", name: "Sum of the First N Numbers", category: "Patterns", emoji: "∑", complexity: "O(1)", input: "text",
    hook: "You are summing 1 to n with the pairing trick instead of a loop." },
  { id: "reverse_array", name: "Reverse an Array (Two Pointers)", category: "Patterns", emoji: "↔️", complexity: "O(n)", input: "text",
    hook: "You are reversing the board by swapping from both ends inward." },
  { id: "palindrome_string", name: "Check if a String is a Palindrome", category: "Patterns", emoji: "🪞", complexity: "O(n)", input: "text",
    hook: "You are checking that a phrase reads the same backwards, comparing from both ends inward." },
  { id: "frequency_count", name: "Count Frequencies / Highest Occurring Element", category: "Structures", emoji: "📊", complexity: "O(n)", input: "text",
    hook: "You are tallying how often each score appears, in one pass." },
  { id: "check_ith_bit", name: "Check if the i-th Bit is Set", category: "Math", emoji: "🔦", complexity: "O(1)", input: "text",
    hook: "You are checking whether a single switch on a control panel is on." },
  { id: "check_odd", name: "Check if a Number is Odd (Bitwise)", category: "Math", emoji: "🎲", complexity: "O(1)", input: "text",
    hook: "One glance at the lowest bit tells you odd or even." },
  { id: "swap_xor", name: "Swap Two Numbers With XOR", category: "Math", emoji: "🔃", complexity: "O(1)", input: "text",
    hook: "You are swapping two values with three XORs and no spare variable." },
  { id: "divide_bits", name: "Divide Without * or /", category: "Math", emoji: "➗", complexity: "O(log n)", input: "text",
    hook: "You are dividing with nothing but shifts and subtractions, one power of two at a time." },
  { id: "xor_range", name: "XOR of Numbers in a Range", category: "Math", emoji: "⊕", complexity: "O(1)", input: "text",
    hook: "You are computing the XOR of a whole range from a four-step pattern, no loop needed." },
  { id: "single_number_iii", name: "Single Number III (Two Uniques)", category: "Math", emoji: "👯", complexity: "O(n)", input: "text",
    hook: "Two values appear once; a single differing bit splits the crowd into two groups." },
  { id: "binary_subarray_sum", name: "Binary Subarrays With Sum", category: "Patterns", emoji: "🪟", complexity: "O(n)", input: "text",
    hook: "You are counting stretches of 0s and 1s that sum to exactly the goal, as at-most minus at-most." },
  { id: "nice_subarrays", name: "Count Number of Nice Subarrays", category: "Patterns", emoji: "🪟", complexity: "O(n)", input: "text",
    hook: "You are counting stretches holding exactly k odd numbers, as at-most minus at-most." },
  { id: "substrings_all_three", name: "Substrings Containing All Three Characters", category: "Patterns", emoji: "🪟", complexity: "O(n)", input: "text",
    hook: "You are counting stretches that contain all three letters, from where each was last seen." },
  { id: "max_card_points", name: "Maximum Points From Cards", category: "Patterns", emoji: "🪟", complexity: "O(n)", input: "text",
    hook: "You are taking k cards from the two ends of a row for the highest total." },
  { id: "subarrays_k_distinct", name: "Subarrays With K Different Integers", category: "Patterns", emoji: "🪟", complexity: "O(n)", input: "text",
    hook: "You are counting stretches with exactly k distinct values, as at-most minus at-most." },
  { id: "min_window_substring", name: "Minimum Window Substring", category: "Patterns", emoji: "🪟", complexity: "O(n)", input: "text",
    hook: "You are finding the shortest stretch that contains every required letter." },
  { id: "min_window_subsequence", name: "Minimum Window Subsequence", category: "Patterns", emoji: "🪟", complexity: "O(n)", input: "text",
    hook: "You are finding the shortest stretch that contains the pattern as a subsequence." },
  { id: "word_ladder", name: "Word Ladder I", category: "Graphs", emoji: "🧩", complexity: "O(n)", input: "text",
    hook: "You are climbing from one word to another by changing a single letter per rung." },
  { id: "word_ladder_ii", name: "Word Ladder II (All Shortest Sequences)", category: "Graphs", emoji: "🧩", complexity: "O(n)", input: "text",
    hook: "You are listing every shortest ladder between two words." },
  { id: "alien_dictionary", name: "Alien Dictionary", category: "Graphs", emoji: "🧩", complexity: "O(n)", input: "text",
    hook: "You are a linguist deducing letter order from a dictionary written in an unknown tongue." },
  { id: "cheapest_flight_k", name: "Cheapest Flights Within K Stops", category: "Graphs", emoji: "🧩", complexity: "O(n)", input: "text",
    hook: "You are booking the cheapest route with at most k layovers, one round of fares at a time." },
  { id: "ways_to_arrive", name: "Number of Ways to Arrive at Destination", category: "Graphs", emoji: "🧩", complexity: "O(n)", input: "text",
    hook: "You are counting the number of different fastest routes between two cities." },
  { id: "min_multiplications", name: "Minimum Multiplications to Reach End", category: "Graphs", emoji: "🧩", complexity: "O(n)", input: "text",
    hook: "You are turning a dial by allowed multipliers, counting the fewest turns to reach the target." },
  { id: "most_stones", name: "Most Stones Removed With Same Row or Column", category: "Graphs", emoji: "🧩", complexity: "O(n)", input: "text",
    hook: "You are clearing stones that share a row or column, leaving one per connected group." },
  { id: "network_delay", name: "Network Delay Time", category: "Graphs", emoji: "📡", complexity: "O(n)", input: "graph",
    hook: "You are timing when the last server hears a broadcast sent along the fastest cables." },
  { id: "trie_insert",  name: "Trie — Prefix Tree",         category: "Structures", emoji: "🔤", complexity: "O(word length)", input: "text",
    hook: "How autocomplete stores a dictionary without repeating prefixes." },
  { id: "huffman",      name: "Huffman Coding",             category: "Greedy", emoji: "🗜️", complexity: "O(n log n)", input: "text",
    hook: "How ZIP shrinks a file: give the commonest letters the shortest codes." },
  { id: "activity_selection", name: "Activity Selection",   category: "Greedy", emoji: "📅", complexity: "O(n log n)", input: "text",
    hook: "Fit the most meetings in one room by always taking the earliest to finish." },
  { id: "fractional_knapsack", name: "Fractional Knapsack", category: "Greedy", emoji: "🎒", complexity: "O(n log n)", input: "text",
    hook: "Unlike 0/1 knapsack, you can take a slice — so greed by value-per-weight wins." },
  { id: "job_sequencing", name: "Job Sequencing",           category: "Greedy", emoji: "🗂️", complexity: "O(n²)", input: "text",
    hook: "Most profit before deadlines: take rich jobs first, run each as late as it can go." },
  { id: "jump_game",    name: "Jump Game I",                category: "Greedy", emoji: "🐇", complexity: "O(n)", input: "array",
    hook: "Can you reach the end? Track the farthest you can go — no need to try every jump." },
  { id: "jump_game_ii", name: "Jump Game II",               category: "Greedy", emoji: "🦘", complexity: "O(n)", input: "array",
    hook: "Fewest jumps to the end — expand the reachable window like a breadth-first sweep." },
  { id: "candy",        name: "Candy",                      category: "Greedy", emoji: "🍬", complexity: "O(n)", input: "array",
    hook: "Reward higher-rated neighbours more, with two passes instead of one impossible pass." },
  { id: "lemonade_change", name: "Lemonade Change",         category: "Greedy", emoji: "🍋", complexity: "O(n)", input: "array",
    hook: "Always give change with the biggest notes first — hoard the fives everyone needs." },
  { id: "assign_cookies", name: "Assign Cookies",           category: "Greedy", emoji: "🍪", complexity: "O(n log n)", input: "text",
    hook: "Content the most children: smallest cookie to the least greedy child it satisfies." },
  { id: "min_platforms", name: "Minimum Platforms",         category: "Greedy", emoji: "🚉", complexity: "O(n log n)", input: "text",
    hook: "How many platforms a station needs — the busiest overlapping moment wins." },
  { id: "min_heap",     name: "Min-Heap — Build",           category: "Structures", emoji: "🔻", complexity: "O(n log n)", input: "array",
    hook: "Every parent ≤ its children, so the smallest value floats to the root." },
  { id: "kth_largest",  name: "Kth Largest Element",        category: "Structures", emoji: "🥇", complexity: "O(n log k)", input: "text",
    hook: "A size-k min-heap keeps only the biggest k — its root is your answer." },
  { id: "kth_smallest", name: "Kth Smallest Element",       category: "Structures", emoji: "🥉", complexity: "O(n log k)", input: "text",
    hook: "A size-k max-heap keeps only the smallest k — its root is your answer." },
  { id: "longest_substring_no_repeat", name: "Longest Substring w/o Repeats", category: "Patterns", emoji: "🔡", complexity: "O(n)", input: "text",
    hook: "A window that stretches and snaps back the moment a character repeats." },
  { id: "max_consecutive_ones_iii", name: "Max Consecutive Ones III", category: "Patterns", emoji: "🚩", complexity: "O(n)", input: "text",
    hook: "The longest run of 1s if you may flip k zeros — a window with ≤k zeros." },
  { id: "longest_k_distinct", name: "Longest Substring, K Distinct", category: "Patterns", emoji: "🧺", complexity: "O(n)", input: "text",
    hook: "The widest window holding at most K different characters." },
  { id: "count_set_bits", name: "Count Set Bits",              category: "Math", emoji: "🔢", complexity: "O(set bits)", input: "text",
    hook: "Kernighan's trick: n & (n-1) erases the lowest 1, so you loop once per bit." },
  { id: "power_of_two", name: "Power of Two",                  category: "Math", emoji: "②", complexity: "O(1)", input: "text",
    hook: "A power of two has a single set bit — n & (n-1) tests it in one step." },
  { id: "single_number", name: "Single Number (XOR)",         category: "Math", emoji: "⊕", complexity: "O(n)", input: "text",
    hook: "Pairs cancel under XOR, so folding the array leaves just the lonely one." },
  { id: "min_bit_flips", name: "Minimum Bit Flips",           category: "Math", emoji: "🔀", complexity: "O(1)", input: "text",
    hook: "The bits of A XOR B are exactly the ones you must flip to turn A into B." },
  { id: "power_set",    name: "Power Set (Bitmask)",          category: "Math", emoji: "🎚️", complexity: "O(2ⁿ·n)", input: "text",
    hook: "Every subset is a binary number — count 0…2ⁿ-1 to list them all." },
  { id: "n_queens",     name: "N-Queens",                   category: "Patterns", emoji: "♛", complexity: "O(n!)", input: "number",
    hook: "Place, fail, take it back — backtracking you can watch." },
  { id: "unique_paths", name: "Unique Paths",               category: "DP", emoji: "🤖", complexity: "O(rows·cols)", input: "number",
    hook: "Count every route to the corner without listing one." },
  { id: "sieve",        name: "Sieve of Eratosthenes",      category: "Searching", emoji: "🔱", complexity: "O(n log log n)", input: "number",
    hook: "Strike out the multiples; the primes are what's left." },
  { id: "kmp_search",   name: "KMP Substring Search",       category: "Patterns", emoji: "🧾", complexity: "O(n + m)", input: "text",
    hook: "Find a pattern without ever re-reading a character." },
  { id: "segment_tree", name: "Segment Tree",               category: "Structures", emoji: "🗼", complexity: "O(log n) query", input: "array",
    hook: "Range sums in log time, because every node summarises a block." },
  { id: "fenwick_tree", name: "Fenwick Tree (BIT)",         category: "Structures", emoji: "🪜", complexity: "O(log n)", input: "array",
    hook: "Prefix sums that stay cheap when the numbers change." },

  // Batch 9 — the college-core gaps.
  { id: "hash_table",   name: "Hash Table (Chaining)",      category: "Structures", emoji: "🗄️", complexity: "O(1) average", input: "text",
    hook: "Where O(1) comes from — and what a collision costs." },
  { id: "bst_delete",   name: "BST — Delete a Node",        category: "Structures", emoji: "✂️", complexity: "O(log n)", input: "array",
    hook: "Three cases, and the third one needs a successor." },
  { id: "heap_extract", name: "Max-Heap — Extract",         category: "Structures", emoji: "⛏️", complexity: "O(log n)", input: "array",
    hook: "Take the top, sink the last leaf — that's heap sort." },
  { id: "dsu",          name: "Union-Find (DSU)",           category: "Graphs", emoji: "🔗", complexity: "O(α(n)) ≈ O(1)", input: "graph",
    hook: "Merge two circles; ask if they were already one." },
  { id: "merge_intervals", name: "Merge Intervals",         category: "Patterns", emoji: "📆", complexity: "O(n log n)", input: "text",
    hook: "Sort by start and the overlaps fall out in one pass." },
  { id: "coin_change",  name: "Coin Change (Fewest Coins)", category: "DP", emoji: "🪙", complexity: "O(coins·amount)", input: "array",
    hook: "Where grabbing the biggest coin first goes wrong." },

  // Batch 10 — graph-family, reusing existing views.
  { id: "connected_components", name: "Connected Components", category: "Graphs", emoji: "🧩", complexity: "O(V + E)", input: "graph",
    hook: "Sweep the graph — every island you can't bridge is its own component." },
  { id: "bipartite_check", name: "Bipartite Check", category: "Graphs", emoji: "🎨", complexity: "O(V + E)", input: "graph",
    hook: "Two colours, no clash? Then it splits into two clean teams." },
  { id: "flood_fill",   name: "Flood Fill (Paint Bucket)", category: "Graphs", emoji: "🪣", complexity: "O(rows·cols)", input: "number",
    hook: "Drop the bucket; the colour spreads to everything a wall doesn't stop." },

  // Batch 11 — DP classics, reusing the grid view.
  { id: "house_robber", name: "House Robber", category: "DP", emoji: "🏠", complexity: "O(n)", input: "array",
    hook: "Rob the street for the most loot — but never two houses in a row." },
  { id: "lis",          name: "Longest Increasing Subsequence", category: "DP", emoji: "📈", complexity: "O(n²)", input: "array",
    hook: "The longest run of ever-rising numbers, skips allowed." },
  { id: "subset_sum",   name: "Subset Sum", category: "DP", emoji: "🎯", complexity: "O(n·target)", input: "number",
    hook: "Can any handful hit the target exactly — without trying all 2ⁿ?" },

  // Batch 12 — string algorithms, reusing the array view.
  { id: "z_function",   name: "Z-Function", category: "Patterns", emoji: "🧬", complexity: "O(n)", input: "text",
    hook: "Where does the string's own prefix start again?" },
  { id: "rabin_karp",   name: "Rabin–Karp (Rolling Hash)", category: "Patterns", emoji: "🔖", complexity: "O(n + m)", input: "text",
    hook: "Compare cheap fingerprints first, characters only on a match." },
  { id: "manacher",     name: "Manacher's Longest Palindrome", category: "Patterns", emoji: "🪞", complexity: "O(n)", input: "text",
    hook: "The longest mirror-sequence, found in one linear pass." },

  // Batch 13 — sorting, windows, interval DP (existing views).
  { id: "radix_sort",   name: "Radix Sort (LSD)", category: "Sorting", emoji: "🔢", complexity: "O(d·n)", input: "array",
    hook: "Sort by one digit at a time — no comparisons ever." },
  { id: "sliding_window_maximum", name: "Sliding Window Maximum", category: "Patterns", emoji: "🏔️", complexity: "O(n)", input: "array",
    hook: "Every window's max, with a deque that looks at nothing twice." },
  { id: "matrix_chain", name: "Matrix Chain Multiplication", category: "DP", emoji: "✖️", complexity: "O(n³)", input: "array",
    hook: "Where to put the parentheses for the fewest multiplications." },

  // Batch 14 — in-place heap sort and two linked-list classics.
  { id: "heap_sort",    name: "Heap Sort (In-Place)", category: "Sorting", emoji: "⛰️", complexity: "O(n log n)", input: "array",
    hook: "Build a heap, swap the max to the end, re-heap — no extra memory." },
  { id: "find_middle",  name: "Find Middle of a List", category: "Structures", emoji: "🎯", complexity: "O(n)", input: "array",
    hook: "Two runners, one twice as fast — it stops on the middle." },
  { id: "merge_two_sorted_lists", name: "Merge Two Sorted Lists", category: "Structures", emoji: "🔗", complexity: "O(n + m)", input: "text",
    hook: "Splice the smaller head each time — one chain, no copying." },

  // Batch 15 — anagram + number theory (existing grid view).
  { id: "anagram",      name: "Anagram Check", category: "Patterns", emoji: "🔀", complexity: "O(n log n)", input: "text",
    hook: "Same letters, shuffled? Sort both and they line up." },
  { id: "gcd_euclid",   name: "GCD (Euclid's Algorithm)", category: "Math", emoji: "➗", complexity: "O(log n)", input: "array",
    hook: "Replace (a, b) with (b, a mod b) until the remainder is 0." },
  { id: "fast_exponentiation", name: "Fast Exponentiation", category: "Math", emoji: "⚡", complexity: "O(log n)", input: "array",
    hook: "Square your way to any power in a handful of steps." },
  { id: "prime_factorisation", name: "Prime Factorisation", category: "Math", emoji: "🧮", complexity: "O(√n)", input: "number",
    hook: "Divide out the smallest prime until only primes remain." },

  // Batch 16 (Tier B) — shortest paths with negative edges.
  { id: "bellman_ford", name: "Bellman–Ford (Negative Edges)", category: "Graphs", emoji: "🧭", complexity: "O(V·E)", input: "graph",
    hook: "Shortest paths even with negative edges — and it spots impossible loops." },
  // ── 2026-09-29: tracers for the rows the 20-module A2Z sheet added ──
  { id: "count_odd_digits", name: "Count Odd Digits in a Number", category: "Math", emoji: "🔢", complexity: "O(log n)", input: "text",
    hook: "You are tallying the odd digits as you peel a number apart." },
  { id: "largest_digit", name: "Largest Digit in a Number", category: "Math", emoji: "🔢", complexity: "O(log n)", input: "text",
    hook: "You are peeling digits and keeping the largest one you have seen." },
  { id: "perfect_number", name: "Check for a Perfect Number", category: "Math", emoji: "🔢", complexity: "O(n)", input: "text",
    hook: "You are checking whether a number equals the sum of its proper divisors." },
  { id: "lcm", name: "LCM of Two Numbers", category: "Math", emoji: "🔢", complexity: "O(log min(a,b))", input: "text",
    hook: "You are finding when two repeating cycles next line up, via their gcd." },
  { id: "array_sum", name: "Sum of Array Elements", category: "Patterns", emoji: "➕", complexity: "O(n)", input: "text",
    hook: "You are adding every score on the board into one total." },
  { id: "count_odd_array", name: "Count Odd Numbers in an Array", category: "Patterns", emoji: "🔢", complexity: "O(n)", input: "text",
    hook: "You are counting how many scores on the board are odd." },
  { id: "second_highest_freq", name: "Second Highest Occurring Element", category: "Patterns", emoji: "🗳️", complexity: "O(n)", input: "text",
    hook: "You are finding the score with the second-highest tally." },
  { id: "sum_high_low_freq", name: "Sum of Highest and Lowest Frequency", category: "Patterns", emoji: "🗳️", complexity: "O(n)", input: "text",
    hook: "You are adding the highest and lowest tallies on the board." },
  { id: "reverse_string", name: "Reverse a String (Two Pointers)", category: "Patterns", emoji: "🔁", complexity: "O(n)", input: "text",
    hook: "You are reversing a word by swapping letters from both ends inward." },
  { id: "set_rightmost_unset_bit", name: "Set the Rightmost Unset Bit", category: "Math", emoji: "💡", complexity: "O(1)", input: "text",
    hook: "You are switching on the lowest switch that is still off." },
  { id: "sum_array_rec", name: "Sum of Array Elements (Recursive)", category: "Patterns", emoji: "🪞", complexity: "O(n)", input: "text",
    hook: "Each call adds its element to whatever the rest of the array sums to." },
  { id: "sum_digits_rec", name: "Sum of Digits (Recursive)", category: "Math", emoji: "🪞", complexity: "O(log n)", input: "text",
    hook: "Each call peels one digit and adds it to the sum of the rest." },
  { id: "factorial_rec", name: "Factorial (Recursive)", category: "Math", emoji: "🪞", complexity: "O(n)", input: "text",
    hook: "Each call waits for the smaller factorial before multiplying its own factor in." },
  { id: "prime_rec", name: "Check for a Prime Number (Recursive)", category: "Math", emoji: "🪞", complexity: "O(√n)", input: "text",
    hook: "Each call tries one divisor, stopping at the square root." },
  { id: "sorted_rec", name: "Check if an Array is Sorted (Recursive)", category: "Patterns", emoji: "🪞", complexity: "O(n)", input: "text",
    hook: "Each call checks one neighbour pair and trusts the next call for the rest." },
  { id: "reverse_array_rec", name: "Reverse an Array (Recursive)", category: "Patterns", emoji: "🪞", complexity: "O(n)", input: "text",
    hook: "Each call swaps the outer pair and hands the inside to the next call." },
  { id: "reverse_string_rec", name: "Reverse a String (Recursive)", category: "Patterns", emoji: "🪞", complexity: "O(n)", input: "text",
    hook: "Each call swaps the outer two letters and recurses on the inside." },
  { id: "palindrome_rec", name: "Check if a String is a Palindrome (Recursive)", category: "Patterns", emoji: "🪞", complexity: "O(n)", input: "text",
    hook: "Each call compares the two outer letters and hands the inside to the next call." },
  { id: "pascal_element", name: "Pascal's Triangle I — One Element", category: "Patterns", emoji: "🔺", complexity: "O(c)", input: "text",
    hook: "You are computing a single entry of Pascal's triangle directly, with no triangle at all." },
  { id: "pascal_row", name: "Pascal's Triangle II — One Row", category: "Patterns", emoji: "🔺", complexity: "O(n)", input: "text",
    hook: "You are producing a whole row of Pascal's triangle from its previous entry each time." },
  { id: "ll_traverse", name: "Traverse a Linked List", category: "Structures", emoji: "🚃", complexity: "O(n)", input: "text",
    hook: "You are walking from the engine to the caboose, reading each carriage." },
  { id: "ll_delete_tail", name: "Delete the Tail of a Linked List", category: "Structures", emoji: "🚃", complexity: "O(n)", input: "text",
    hook: "You are walking to the second-last carriage so you can uncouple the last one." },
  { id: "ll_delete_kth", name: "Delete the Kth Node of a Linked List", category: "Structures", emoji: "🚃", complexity: "O(k)", input: "text",
    hook: "You are walking to the k-th carriage and bypassing it." },
  { id: "ll_delete_value", name: "Delete a Node by Value", category: "Structures", emoji: "🚃", complexity: "O(n)", input: "text",
    hook: "You are walking the train until you find the named carriage, then bypassing it." },
  { id: "ll_insert_tail", name: "Insert at the Tail of a Linked List", category: "Structures", emoji: "🚃", complexity: "O(n)", input: "text",
    hook: "You are walking to the end of the train to hook on a new carriage." },
  { id: "ll_insert_kth", name: "Insert at the Kth Position of a Linked List", category: "Structures", emoji: "🚃", complexity: "O(k)", input: "text",
    hook: "You are walking k carriages in and coupling a new one there." },
  { id: "ll_insert_before_value", name: "Insert Before a Value in a Linked List", category: "Structures", emoji: "🚃", complexity: "O(n)", input: "text",
    hook: "You are stopping one carriage early so you can couple a new one in before the named carriage." },
  { id: "dll_from_array", name: "Build a Doubly Linked List From an Array", category: "Structures", emoji: "🚃", complexity: "O(n)", input: "text",
    hook: "You are building a train from a list of carriages, coupling each both forward and back." },
  { id: "dll_delete_tail", name: "Delete the Tail of a Doubly Linked List", category: "Structures", emoji: "🚃", complexity: "O(1)", input: "text",
    hook: "You are uncoupling the last carriage of a two-way train — its backward link makes it instant." },
  { id: "dll_delete_kth", name: "Delete the Kth Node of a Doubly Linked List", category: "Structures", emoji: "🚃", complexity: "O(k)", input: "text",
    hook: "You are walking to the k-th carriage of a two-way train and lifting it out, relinking both sides." },
  { id: "dll_remove_node", name: "Remove a Given Node From a Doubly Linked List", category: "Structures", emoji: "🚃", complexity: "O(1)", input: "text",
    hook: "You are removing a specific carriage from a two-way train by relinking its neighbours directly." },
  { id: "dll_insert_before_tail", name: "Insert Before the Tail of a Doubly Linked List", category: "Structures", emoji: "🚃", complexity: "O(1)", input: "text",
    hook: "You are inserting a carriage just ahead of the caboose." },
  { id: "dll_insert_before_kth", name: "Insert Before the Kth Node of a Doubly Linked List", category: "Structures", emoji: "🚃", complexity: "O(k)", input: "text",
    hook: "You are inserting a carriage just before the k-th one, wiring four couplings." },
  { id: "dll_insert_before_node", name: "Insert Before a Given Node in a Doubly Linked List", category: "Structures", emoji: "🚃", complexity: "O(n)", input: "text",
    hook: "You are inserting a carriage ahead of a named one, using its backward link to find the spot." },
  { id: "heapify", name: "Heapify (Sift Down)", category: "Structures", emoji: "⛰️", complexity: "O(log n)", input: "text",
    hook: "You are sinking one misplaced ticket down until both tickets below it are lower priority." },
  { id: "build_heap", name: "Build a Max-Heap From an Array", category: "Structures", emoji: "⛰️", complexity: "O(n)", input: "text",
    hook: "You are turning a pile of tickets into a priority queue by settling each parent from the bottom up." },
  { id: "sort_k_sorted", name: "Sort a K-Sorted Array", category: "Structures", emoji: "⛰️", complexity: "O(n log k)", input: "text",
    hook: "You are sorting a nearly sorted list with a heap of only k+1 tickets." },
  { id: "bst_min_max", name: "Minimum and Maximum in a BST", category: "Structures", emoji: "🌲", complexity: "O(h)", input: "text",
    hook: "You are finding the alphabetically first and last folders by walking all the way left, then right." },
  { id: "bst_iterator", name: "BST Iterator (next / hasNext)", category: "Structures", emoji: "🌲", complexity: "O(1) amortised", input: "text",
    hook: "You are handing out folders in name order one at a time, keeping only the current path on a stack." },
  { id: "single_number_ii", name: "Single Number II (Every Other Value Thrice)", category: "Math", emoji: "⊕", complexity: "O(32n)", input: "text",
    hook: "Every value appears three times but one; counting bits modulo 3 exposes it." },
  { id: "distinct_islands", name: "Number of Distinct Islands", category: "Graphs", emoji: "🗺️", complexity: "O(R·C)", input: "text",
    hook: "You are a surveyor recording the outline of each island to count how many shapes are truly different." },
  { id: "shortest_palindrome", name: "Shortest Palindrome (KMP)", category: "Patterns", emoji: "🧬", complexity: "O(n)", input: "text",
    hook: "You are prepending as few letters as possible to make a word a palindrome, using a KMP border." },
  { id: "print_shortest_path", name: "Print the Shortest Path (Dijkstra + Parents)", category: "Graphs", emoji: "🧭", complexity: "O((V+E) log V)", input: "graph",
    hook: "You are a GPS that not only finds the fastest route but remembers each turn so it can read the route back." },
];

// Short face label per algorithm. Lives here because both the 3D keycaps
// and the flat mobile grid render it — keeping one copy stops them drifting.
// The legend printed on a keycap. Curated labels first (KEYCAP_LABEL); every
// other algorithm gets a 4-letter abbreviation derived from its id, so all
// 474 can sit on the board's layers without a hand-written label each:
//   one word  → its first four letters      (sieve → SIEV, heapify → HEAP)
//   two words → two letters of each         (heap_sort → HESO, lcm... → LCM)
//   more      → initials, up to four        (dll_insert_before_kth → DIBK)
export function capLabel(algo) {
  const curated = KEYCAP_LABEL[algo.id];
  if (curated) return curated;
  const parts = algo.id.split('_').filter(Boolean);
  let label;
  if (parts.length === 1) label = parts[0].slice(0, 4);
  else if (parts.length === 2) label = parts[0].slice(0, 2) + parts[1].slice(0, 2);
  else label = parts.map(w => w[0]).join('').slice(0, 4);
  return label.toUpperCase();
}

export const KEYCAP_LABEL = {
  dijkstra: 'DIJK', bfs: 'BFS', dfs: 'DFS', prims_mst: 'PRIM', kruskals_mst: 'KRSK',
  merge_sort: 'MRG', quick_sort: 'QCK', bubble_sort: 'BUB', insertion_sort: 'INS', selection_sort: 'SEL',
  binary_search: 'BIN', bst_search: 'BSTs', two_sum_sorted: '2SUM', sliding_window: 'WIN', kadanes: 'KDN',
  linked_list_reverse: 'LIST', balanced_brackets: '{ }', bst_insert: 'BST', heap_insert: 'HEAP',
  fibonacci_dp: 'FIB', knapsack_01: 'KNAP', lcs: 'LCS',
  edit_distance: 'EDIT', topological_sort: 'TOPO', counting_sort: 'CNT',
  prefix_sums: 'PRE', next_greater_element: 'NGE', floyd_cycle: 'CYCL',
  tree_traversal: 'WALK', trie_insert: 'TRIE', n_queens: 'NQ',
  unique_paths: 'PATH', sieve: 'PRIME',
  kmp_search: 'KMP', segment_tree: 'SEG', fenwick_tree: 'BIT',
  hash_table: 'HASH', bst_delete: 'DEL', heap_extract: 'POP',
  dsu: 'DSU', merge_intervals: 'IVAL', coin_change: 'COIN',
  connected_components: 'CC', bipartite_check: 'BIP', flood_fill: 'FILL',
  house_robber: 'ROB', lis: 'LIS+', subset_sum: 'SUBS',
  z_function: 'Z', rabin_karp: 'RK', manacher: 'PALI',
  radix_sort: 'RDX', sliding_window_maximum: 'WMAX', matrix_chain: 'MCM',
  heap_sort: 'HSRT', find_middle: 'MID', merge_two_sorted_lists: 'MRG2',
  anagram: 'ANAG', gcd_euclid: 'GCD', fast_exponentiation: 'POW', prime_factorisation: 'FCTR',
  bellman_ford: 'BELF',
};

export const GRAPH_ALGORITHMS = ALGORITHMS.filter(a => a.input === "graph");
// The comparison sorts share one input (any numbers) and one step shape, so
// compare mode can run any two of them side by side on the same values.
export const SORT_ALGORITHMS = ["bubble_sort", "insertion_sort", "selection_sort", "merge_sort", "quick_sort", "heap_sort"]
  .map(id => ALGORITHMS.find(a => a.id === id)).filter(Boolean);

export const WORLDS = [
  { name: "The Leaderboard",    metaphor: "Sorting",       category: "Foundations", emoji: "📊", hook: "Organize the chaos, one swap at a time.",          complexity: "O(n log n)", algo: "sorting"       },
  { name: "The Hunt",           metaphor: "Binary Search",  category: "Foundations", emoji: "🔍", hook: "Divide, conquer, find the needle in the haystack.", complexity: "O(log n)",   algo: "binary_search" },
  { name: "Six Degrees",        metaphor: "Graphs",         category: "Structures",  emoji: "🌐", hook: "Navigate the web of connections that define us.",   complexity: "O(V + E)",   algo: "bfs"           },
  { name: "The Memo Vault",     metaphor: "DP",             category: "Mastery",     emoji: "💾", hook: "Remember the past to conquer the future.",          complexity: "O(n)",       algo: "fibonacci_dp"  },
  { name: "The Priority Queue", metaphor: "Heaps",          category: "Structures",  emoji: "👑", hook: "Always keep the most important things on top.",     complexity: "O(log n)",   algo: "heap_insert"   },
  { name: "The Branching Tree", metaphor: "Recursion",      category: "Foundations", emoji: "🌿", hook: "Solve small to solve big.",                         complexity: "O(2^n)",     algo: "dfs"           },
  { name: "The Labyrinth",      metaphor: "Backtracking",   category: "Mastery",     emoji: "🗺️", hook: "Explore every path, but know when to turn back.",   complexity: "O(N!)",      algo: "dfs"           },
  { name: "The Hash Map",       metaphor: "Hashing",        category: "Structures",  emoji: "🔑", hook: "Instant lookup to any secret you store.",           complexity: "O(1)",       algo: "binary_search" },
  { name: "The Flow",           metaphor: "Linked Lists",   category: "Structures",  emoji: "🔗", hook: "One link at a time, building the chain.",            complexity: "O(n)",       algo: "linked_list_reverse" }
];

export const SAMPLE_GRAPH = {
  nodes: [
    { id: "A", x: 100, y: 150, label: "Home"     },
    { id: "B", x: 250, y: 80,  label: "Uptown"   },
    { id: "C", x: 250, y: 220, label: "Downtown" },
    { id: "D", x: 420, y: 80,  label: "Airport"  },
    { id: "E", x: 420, y: 220, label: "Mall"     },
    { id: "F", x: 560, y: 150, label: "Station"  },
    { id: "G", x: 680, y: 150, label: "Office"   },
  ],
  links: [
    { source: "A", target: "B", weight: 4  },
    { source: "A", target: "C", weight: 2  },
    { source: "B", target: "D", weight: 5  },
    { source: "B", target: "E", weight: 10 },
    { source: "C", target: "E", weight: 3  },
    { source: "D", target: "F", weight: 2  },
    { source: "E", target: "F", weight: 4  },
    { source: "F", target: "G", weight: 1  },
  ]
};

// The full Striver A2Z sheet lives in its own module — 20 modules, and long
// enough that inlining it here buried everything else in this file.
export { A2Z_STEPS } from './a2z.js';

export const COMPLEXITY = {
  dijkstra: {
    rows: [["Time", "O((V + E) log V)"], ["Space", "O(V)"]],
    reading: (c, s) =>
      `Your graph: ${c.relaxations ?? 0} relaxations and ${c.heap_pushes ?? 0} heap pushes ` +
      `across ${s.V} nodes / ${s.E} edges — that's the (V + E)·log V at work. ` +
      `Every relaxation is the heap earning its keep.`,
  },
  bfs: {
    rows: [["Time", "O(V + E)"], ["Space", "O(V)"]],
    reading: (c, s) =>
      `Your graph: ${c.edge_checks ?? 0} edge checks and ${c.enqueues ?? 0} enqueues ` +
      `for ${s.V} nodes / ${s.E} edges — each node and edge touched a constant number ` +
      `of times. That's what linear O(V + E) looks like.`,
  },
  binary_search: {
    rows: [["Best", "O(1)"], ["Worst", "O(log n)"], ["Space", "O(1)"]],
    reading: (c, s) =>
      `${c.comparisons ?? 0} probe${(c.comparisons ?? 0) === 1 ? '' : 's'} to search ` +
      `${s.n} values — log₂(${s.n}) ≈ ${Math.max(1, Math.ceil(Math.log2(Math.max(s.n, 2))))}. ` +
      `Each probe halves what's left.`,
  },
  merge_sort: {
    rows: [["Best / Avg / Worst", "O(n log n)"], ["Space", "O(n)"]],
    reading: (c, s) =>
      `${c.comparisons ?? 0} comparisons and ${c.writes ?? 0} writes to sort ${s.n} values — ` +
      `n·log₂ n ≈ ${Math.round(s.n * Math.log2(Math.max(s.n, 2)))}. ` +
      `The ${c.merges ?? 0} merges are where the ordering actually happens.`,
  },
  dfs: {
    rows: [["Time", "O(V + E)"], ["Space", "O(V)"]],
    reading: (c, s) =>
      `Your graph: ${c.edge_checks ?? 0} edge checks and ${c.backtracks ?? 0} backtracks ` +
      `for ${s.V} nodes / ${s.E} edges — linear like BFS, but the stack dives deep ` +
      `before it sweeps wide.`,
  },
  quick_sort: {
    rows: [["Best / Avg", "O(n log n)"], ["Worst", "O(n²)"], ["Space", "O(log n)"]],
    reading: (c, s) =>
      `${c.comparisons ?? 0} comparisons and ${c.swaps ?? 0} swaps across ` +
      `${c.partitions ?? 0} partitions to sort ${s.n} values — ` +
      `n·log₂ n ≈ ${Math.round(s.n * Math.log2(Math.max(s.n, 2)))}. ` +
      `An already-sorted input would push this toward n² = ${s.n * s.n}.`,
  },
  bubble_sort: {
    rows: [["Best (sorted input)", "O(n)"], ["Avg / Worst", "O(n²)"], ["Space", "O(1)"]],
    reading: (c, s) =>
      `${c.comparisons ?? 0} comparisons and ${c.swaps ?? 0} swaps over ` +
      `${c.passes ?? 0} passes for ${s.n} values. A sorted input exits after one ` +
      `pass (${Math.max(s.n - 1, 0)} comparisons) — that's the O(n) best case.`,
  },
  insertion_sort: {
    rows: [["Best (sorted input)", "O(n)"], ["Avg / Worst", "O(n²)"], ["Space", "O(1)"]],
    reading: (c, s) =>
      `${c.comparisons ?? 0} comparisons and ${c.shifts ?? 0} shifts to place ` +
      `${c.inserts ?? 0} values. Nearly-sorted input shifts almost nothing — ` +
      `that's why insertion sort is the choice for small or nearly-ordered data.`,
  },
  selection_sort: {
    rows: [["Always", "O(n²)"], ["Space", "O(1)"], ["Swaps", "O(n)"]],
    reading: (c, s) =>
      `${c.comparisons ?? 0} comparisons — exactly n(n−1)/2 = ` +
      `${(s.n * (s.n - 1)) / 2} for ${s.n} values, no matter the order. ` +
      `Only ${c.swaps ?? 0} swaps though — selection sort never wastes a move.`,
  },
  linked_list_reverse: {
    rows: [["Time", "O(n)"], ["Space", "O(1)"]],
    reading: (c, s) =>
      `${c.flips ?? 0} pointer flips for ${s.n} nodes — one visit each, three ` +
      `pointers total. No extra memory, no matter how long the chain.`,
  },
  balanced_brackets: {
    rows: [["Time", "O(n)"], ["Space", "O(n)"]],
    reading: (c, s) =>
      `${c.pushes ?? 0} pushes and ${c.pops ?? 0} pops — each symbol touched ` +
      `once. The stack's depth is the price of remembering what's still open.`,
  },
  two_sum_sorted: {
    rows: [["Time", "O(n)"], ["Naive pairs", "O(n²)"], ["Space", "O(1)"]],
    reading: (c, s) =>
      `${c.checks ?? 0} pair checks and ${c.moves ?? 0} pointer moves for ${s.n} values — ` +
      `the naive approach would test up to ${(s.n * (s.n - 1)) / 2} pairs. ` +
      `Sorted order lets each check discard a whole line of candidates.`,
  },
  sliding_window: {
    rows: [["Time", "O(n)"], ["Naive", "O(n·k)"], ["Space", "O(1)"]],
    reading: (c, s) =>
      `${c.additions ?? 0} additions across ${c.windows ?? 0} windows — ` +
      `recomputing every window from scratch would cost far more. ` +
      `Drop one, add one: that's the whole trick.`,
  },
  kadanes: {
    rows: [["Time", "O(n)"], ["Naive subarrays", "O(n²)"], ["Space", "O(1)"]],
    reading: (c, s) =>
      `One pass: ${c.extensions ?? 0} extensions and ${c.restarts ?? 0} restarts over ` +
      `${s.n} values. Checking every subarray would mean ~${(s.n * (s.n + 1)) / 2} sums — ` +
      `Kadane's insight makes all but ${s.n} of them unnecessary.`,
  },
  bst_insert: {
    rows: [["Avg insert", "O(log n)"], ["Worst (sorted input)", "O(n)"], ["Space", "O(n)"]],
    reading: (c, s) =>
      `${c.comparisons ?? 0} comparisons to insert ${c.insertions ?? 0} values. ` +
      `Balanced height would be ~${Math.max(1, Math.ceil(Math.log2(Math.max(s.n, 2) + 1)))} — ` +
      `insert sorted numbers and the tree degenerates into an O(n) chain.`,
  },
  bst_search: {
    rows: [["Avg", "O(log n)"], ["Worst (chain)", "O(n)"], ["Space", "O(1)"]],
    reading: (c, s) =>
      `${c.comparisons ?? 0} comparison${(c.comparisons ?? 0) === 1 ? '' : 's'} to settle the ` +
      `search among ${s.n} values — each one discarded a whole subtree. ` +
      `That's binary search, living in a tree.`,
  },
  heap_insert: {
    rows: [["Per insert", "O(log n)"], ["Build (n inserts)", "O(n log n)"], ["Space", "O(n)"]],
    reading: (c, s) =>
      `${c.comparisons ?? 0} comparisons and ${c.swaps ?? 0} bubble-up swaps for ` +
      `${c.insertions ?? 0} inserts — each value climbs at most log₂(n) ≈ ` +
      `${Math.max(1, Math.ceil(Math.log2(Math.max(s.n, 2))))} levels. ` +
      `The maximum is always at the root, for free.`,
  },
  prims_mst: {
    rows: [["Time", "O(E log V)"], ["Space", "O(V + E)"], ["Tree edges", "V − 1"]],
    reading: (c, s) =>
      `${c.edge_checks ?? 0} frontier edges examined to add ${c.edges_added ?? 0} — ` +
      `always V−1 = ${Math.max(s.V - 1, 0)} for ${s.V} nodes, no matter how many ` +
      `edges exist. ${c.rejections ?? 0} were skipped as cycles.`,
  },
  kruskals_mst: {
    rows: [["Time", "O(E log E)"], ["Union-Find", "≈O(1) amortised"], ["Space", "O(V)"]],
    reading: (c, s) =>
      `${c.edge_checks ?? 0} of ${s.E} edges examined in sorted order: ` +
      `${c.unions ?? 0} unions, ${c.cycles_skipped ?? 0} rejected as cycles. ` +
      `The sort dominates the cost — union-find itself is near-constant per query.`,
  },
  knapsack_01: {
    rows: [["Time", "O(n·W)"], ["Naive subsets", "O(2ⁿ)"], ["Space", "O(n·W)"]],
    reading: (c, s) =>
      `${c.cells ?? 0} cells filled — each subproblem solved exactly once ` +
      `(${c.takes ?? 0} takes, ${c.skips ?? 0} skips). Trying every subset ` +
      `would mean 2ⁿ combinations; the table makes it a grid walk.`,
  },
  lcs: {
    rows: [["Time", "O(n·m)"], ["Naive", "O(2ⁿ)"], ["Space", "O(n·m)"]],
    reading: (c, s) =>
      `${c.cells ?? 0} cells with ${c.matches ?? 0} character matches — then a ` +
      `single traceback walk recovers the actual sequence. Without the table, ` +
      `you'd compare exponentially many subsequences.`,
  },
  fibonacci_dp: {
    rows: [["Time (memoized)", "O(n)"], ["Time (naive)", "O(2ⁿ)"], ["Space", "O(n)"]],
    reading: (c, s) =>
      `${c.computes ?? 0} computations + ${c.cache_hits ?? 0} cache hits = ` +
      `${c.calls ?? 0} total calls for fib(${s.n}). Naive recursion would need ` +
      `~${Math.round(Math.pow(1.618, Math.max(s.n, 1)))} calls — the vault turned ` +
      `exponential into linear.`,
  },
  topological_sort: {
    rows: [["Time", "O(V + E)"], ["Space", "O(V)"], ["Detects cycles", "yes"]],
    reading: (c, s) =>
      `${c.emitted ?? 0} tasks emitted after clearing ${c.edge_relaxations ?? 0} ` +
      `dependencies — every node and every edge touched exactly once, which is ` +
      `the V + E. If it stops early, the leftovers form a cycle.`,
  },
  counting_sort: {
    rows: [["Time", "O(n + k)"], ["Space", "O(k)"], ["Comparisons", "0"]],
    reading: (c, s) =>
      `${c.tallies ?? 0} tallies then ${c.writes ?? 0} writes, with ` +
      `${c.comparisons ?? 0} comparisons — it never compares two values. The catch ` +
      `is k: the bucket array is sized by your largest value, not your count.`,
  },
  prefix_sums: {
    rows: [["Build", "O(n)"], ["Each query", "O(1)"], ["Space", "O(n)"]],
    reading: (c, s) =>
      `${c.additions ?? 0} additions to build, then ${c.query_ops ?? 0} range ` +
      `query answered by a single subtraction. Ten more queries would still cost ` +
      `one subtraction each — that is the trade for the O(n) setup.`,
  },
  next_greater_element: {
    rows: [["Time", "O(n)"], ["Space", "O(n)"], ["Naive", "O(n²)"]],
    reading: (c, s) =>
      `${c.pushes ?? 0} pushes and ${c.pops ?? 0} pops — each index enters and ` +
      `leaves the stack at most once, so the work is linear even though the code ` +
      `has a loop inside a loop.`,
  },
  edit_distance: {
    rows: [["Time", "O(n·m)"], ["Space", "O(n·m)"], ["Traceback", "O(n + m)"]],
    reading: (c, s) =>
      `${c.cells ?? 0} cells filled — ${c.free_matches ?? 0} were free matches and ` +
      `${c.edits_charged ?? 0} cost an edit. Every cell is one min() over three ` +
      `neighbours, which is why the grid is the whole algorithm.`,
  },
  floyd_cycle: {
    rows: [["Time", "O(n)"], ["Space", "O(1)"], ["vs. hash set", "O(n) space"]],
    reading: (c, s) =>
      `${c.slow_moves ?? 0} slow steps against ${c.fast_moves ?? 0} fast ones. ` +
      `Storing every visited node in a set would also find the loop — but this ` +
      `uses two pointers and no extra memory at all.`,
  },
  tree_traversal: {
    rows: [["Time", "O(n) per walk"], ["Space", "O(height)"], ["Walks shown", "3"]],
    reading: (c, s) =>
      `${c.visits ?? 0} reads across three traversals of the same tree, with ` +
      `${c.descents ?? 0} recursive calls. Each walk touches every node once — ` +
      `only the moment of reading moves.`,
  },
  trie_insert: {
    rows: [["Insert", "O(word length)"], ["Lookup", "O(word length)"], ["Space", "O(total chars)"]],
    reading: (c, s) =>
      `${c.words_added ?? 0} words in ${c.nodes_created ?? 0} nodes, with ` +
      `${c.prefix_reuses ?? 0} steps riding an existing prefix. Lookup never ` +
      `depends on how many words are stored — only on how long yours is.`,
  },
  n_queens: {
    rows: [["Worst case", "O(n!)"], ["Space", "O(n)"], ["Pruning", "rows + diagonals"]],
    reading: (c, s) =>
      `${c.placements ?? 0} queens placed, ${c.conflicts ?? 0} squares rejected ` +
      `outright and ${c.backtracks ?? 0} taken back off. Pruning attacked ` +
      `squares before recursing is what keeps this far below brute force.`,
  },
  unique_paths: {
    rows: [["Time", "O(rows·cols)"], ["Space", "O(rows·cols)"], ["Brute force", "exponential"]],
    reading: (c, s) =>
      `${c.cells ?? 0} cells filled with ${c.additions ?? 0} additions` +
      `${c.blocked ? ` and ${c.blocked} wall(s)` : ''}. Every cell is solved ` +
      `once and reused — enumerating routes individually would blow up.`,
  },
  kmp_search: {
    rows: [["Time", "O(n + m)"], ["Space", "O(m)"], ["Naive", "O(n·m)"]],
    reading: (c, s) =>
      `${c.comparisons ?? 0} comparisons and ${c.shifts ?? 0} pattern shifts, ` +
      `finding ${c.matches ?? 0} match(es). The naive nested loop could have ` +
      `needed up to ${c.naive_would_cost ?? 0} — the failure table is what ` +
      `stops the text pointer from ever backing up.`,
  },
  segment_tree: {
    rows: [["Build", "O(n)"], ["Query", "O(log n)"], ["Space", "O(n)"]],
    reading: (c, s) =>
      `${c.nodes_built ?? 0} nodes built once, then the query touched only ` +
      `${c.nodes_visited ?? 0} of them and reused ${c.full_covers ?? 0} whole ` +
      `block(s). Summing the range directly would have read ` +
      `${c.elements_scanned_naively ?? 0} elements.`,
  },
  hash_table: {
    rows: [["Average", "O(1)"], ["Worst", "O(n)"], ["Space", "O(n)"]],
    reading: (c) =>
      `${c.hashes ?? 0} hash${(c.hashes ?? 0) === 1 ? '' : 'es'} computed and ` +
      `${c.collisions ?? 0} collision${(c.collisions ?? 0) === 1 ? '' : 's'}. ` +
      `The hash is always one step — the cost you actually pay is walking the ` +
      `chain it lands in, which is why a table that fills up stops being O(1).`,
  },
  bst_delete: {
    rows: [["Average", "O(log n)"], ["Worst", "O(n)"], ["Space", "O(1)"]],
    reading: (c) =>
      `${c.comparisons ?? 0} comparison${(c.comparisons ?? 0) === 1 ? '' : 's'} ` +
      `to find the node and its successor, then ${c.promotions ?? 0} value moved. ` +
      `Delete costs the same as a search — finding the node is the work, ` +
      `rewiring it is O(1).`,
  },
  heap_extract: {
    rows: [["Extract", "O(log n)"], ["Peek", "O(1)"], ["Heap sort", "O(n log n)"]],
    reading: (c) =>
      `${c.extractions ?? 0} extraction${(c.extractions ?? 0) === 1 ? '' : 's'}, ` +
      `${c.comparisons ?? 0} comparisons and ${c.swaps ?? 0} swaps. Each sift-down ` +
      `walks at most the height of the tree — do it once per value and you have ` +
      `sorted the array in O(n log n) without any extra memory.`,
  },
  dsu: {
    rows: [["Find / Union", "O(α(n))"], ["Effectively", "O(1)"], ["Space", "O(n)"]],
    reading: (c) =>
      `${c.finds ?? 0} finds, ${c.unions ?? 0} merges and ${c.rejections ?? 0} ` +
      `redundant link(s) rejected. α is the inverse-Ackermann function — it never ` +
      `exceeds 4 for any input that fits in memory, so treat these as constant time.`,
  },
  merge_intervals: {
    rows: [["Sort", "O(n log n)"], ["Merge pass", "O(n)"], ["Space", "O(n)"]],
    reading: (c, s) =>
      `One pass, ${c.comparisons ?? 0} comparison${(c.comparisons ?? 0) === 1 ? '' : 's'}, ` +
      `${c.merges ?? 0} merge(s). The pass is linear — the sort dominates, and ` +
      `without it you would be comparing every pair at O(n²).`,
  },
  coin_change: {
    rows: [["Time", "O(coins × amount)"], ["Space", "O(amount)"], ["Greedy", "wrong in general"]],
    reading: (c) =>
      `${c.cells ?? 0} cells filled — ${c.takes ?? 0} where spending the coin won, ` +
      `${c.skips ?? 0} where skipping it did. Each cell reads exactly two ` +
      `neighbours, which is why this beats trying every combination.`,
  },
  fenwick_tree: {
    rows: [["Update", "O(log n)"], ["Query", "O(log n)"], ["Space", "O(n)"]],
    reading: (c, s) =>
      `${c.updates ?? 0} values folded into ${c.slots_touched ?? 0} slots, and ` +
      `the prefix query read just ${c.query_reads ?? 0}. A plain prefix array ` +
      `queries faster but costs O(n) per update — this balances both.`,
  },
  sieve: {
    rows: [["Time", "O(n log log n)"], ["Space", "O(n)"], ["Crossing starts at", "p²"]],
    reading: (c, s) =>
      `${c.primes_found ?? 0} primes found with only ${c.crossings ?? 0} ` +
      `crossings. ${c.skipped_as_done ?? 0} primes were past √n, where no ` +
      `multiples remain to cross — that early stop is the optimisation.`,
  },
  connected_components: {
    rows: [["Time", "O(V + E)"], ["Space", "O(V)"], ["Components", "as found"]],
    reading: (c, s) =>
      `${c.components ?? 0} component(s) found by touching ${c.nodes_seen ?? 0} ` +
      `node(s) over ${c.edge_checks ?? 0} edge check(s) — each node and edge is ` +
      `visited once, which is the V + E. One component means the graph is fully ` +
      `connected.`,
  },
  bipartite_check: {
    rows: [["Time", "O(V + E)"], ["Space", "O(V)"], ["Fails on", "odd cycles"]],
    reading: (c, s) =>
      `${c.colored ?? 0} node(s) painted over ${c.edge_checks ?? 0} edge check(s), ` +
      `with ${c.conflicts ?? 0} clash(es). A single same-colour edge is enough to ` +
      `prove no two-team split exists — that edge sits on an odd-length cycle.`,
  },
  flood_fill: {
    rows: [["Time", "O(rows·cols)"], ["Space", "O(rows·cols)"], ["Connectivity", "4-way"]],
    reading: (c, s) =>
      `${c.filled ?? 0} cell(s) painted, ${c.edge_checks ?? 0} neighbour check(s), ` +
      `stopped by ${c.blocked ?? 0} wall(s). Each cell is painted once; the region ` +
      `it reaches is exactly the start's connected component on the grid.`,
  },
  house_robber: {
    rows: [["Time", "O(n)"], ["Space", "O(n)"], ["Choice per house", "rob / skip"]],
    reading: (c, s) =>
      `${c.houses ?? 0} house(s) decided — robbed ${c.robs ?? 0}, skipped ` +
      `${c.skips ?? 0}. Each house is one max() of two earlier answers, so the ` +
      `whole street is linear — no need to try every legal combination.`,
  },
  lis: {
    rows: [["Time", "O(n²)"], ["Space", "O(n)"], ["Best known", "O(n log n)"]],
    reading: (c, s) =>
      `${c.positions ?? 0} position(s) solved over ${c.comparisons ?? 0} ` +
      `backward comparison(s), extending an earlier run ${c.extensions ?? 0} ` +
      `time(s). Each position scans everything before it — that inner scan is ` +
      `the n², and a patience-sorting trick can cut it to n log n.`,
  },
  subset_sum: {
    rows: [["Time", "O(n·target)"], ["Space", "O(n·target)"], ["Brute force", "O(2ⁿ)"]],
    reading: (c, s) =>
      `${c.cells ?? 0} cell(s) filled, ${c.reachable ?? 0} reachable, the new ` +
      `number used in ${c.uses_item ?? 0}. Each cell reads just two cells above ` +
      `it — pseudo-polynomial in the target, but far cheaper than 2ⁿ subsets.`,
  },
  z_function: {
    rows: [["Time", "O(n)"], ["Space", "O(n)"], ["Naive", "O(n²)"]],
    reading: (c, s) =>
      `${c.comparisons ?? 0} character comparison(s), with ${c.box_reuses ?? 0} ` +
      `position(s) copying a mirror inside the Z-box instead of re-comparing. ` +
      `That reuse is what keeps the total comparisons linear in the length.`,
  },
  rabin_karp: {
    rows: [["Average", "O(n + m)"], ["Worst", "O(n·m)"], ["Space", "O(1)"]],
    reading: (c, s) =>
      `${c.hashes ?? 0} rolling hash(es), ${c.hash_hits ?? 0} fingerprint hit(s), ` +
      `${c.char_checks ?? 0} character check(s) (${c.collisions ?? 0} collision(s)). ` +
      `Most windows were dismissed on their fingerprint alone — that is the win, ` +
      `and the collisions are why a character check can never be skipped.`,
  },
  manacher: {
    rows: [["Time", "O(n)"], ["Space", "O(n)"], ["Naive", "O(n²)"]],
    reading: (c, s) =>
      `${c.centres ?? 0} centre(s), ${c.expansions ?? 0} expansion step(s), and ` +
      `${c.mirror_reuses ?? 0} centre(s) that copied a mirror's radius first. ` +
      `The mirror is why the total expansion work stays linear instead of n².`,
  },
  radix_sort: {
    rows: [["Time", "O(d·n)"], ["Space", "O(n + base)"], ["Comparisons", "0"]],
    reading: (c, s) =>
      `${c.passes ?? 0} pass(es) — one per digit — over ${c.placements ?? 0} ` +
      `bucket placement(s), with ${c.collects ?? 0} collect step(s) and zero ` +
      `comparisons. Linear in the count for a fixed digit width; the catch is d, ` +
      `the number of digits.`,
  },
  sliding_window_maximum: {
    rows: [["Time", "O(n)"], ["Space", "O(k)"], ["Naive", "O(n·k)"]],
    reading: (c, s) =>
      `${c.pushes ?? 0} push(es) and ${(c.pops_small ?? 0) + (c.pops_expired ?? 0)} ` +
      `pop(s) across ${c.windows ?? 0} window(s). Every index enters and leaves ` +
      `the deque at most once, so the whole scan is linear — re-scanning each ` +
      `window would be O(n·k).`,
  },
  matrix_chain: {
    rows: [["Time", "O(n³)"], ["Space", "O(n²)"], ["Brute force", "exponential"]],
    reading: (c, s) =>
      `${c.cells ?? 0} cell(s) filled over ${c.splits_tried ?? 0} split(s) tried. ` +
      `Each interval reuses the shorter intervals already solved — far cheaper ` +
      `than the Catalan-number explosion of ways to parenthesise by hand.`,
  },
  heap_sort: {
    rows: [["Time", "O(n log n)"], ["Space", "O(1)"], ["Stable", "no"]],
    reading: (c, s) =>
      `${c.comparisons ?? 0} comparison(s) and ${c.swaps ?? 0} swap(s), all in ` +
      `place. Build is O(n); each of the sift-downs is O(log n). The payoff over ` +
      `merge sort is the O(1) space — it never allocates a second array.`,
  },
  find_middle: {
    rows: [["Time", "O(n)"], ["Space", "O(1)"], ["Passes", "1"]],
    reading: (c, s) =>
      `Slow took ${c.slow_steps ?? 0} step(s) while fast took ${c.fast_steps ?? 0}. ` +
      `Because fast moves twice as quickly, slow lands on the middle in a single ` +
      `pass — no need to count the length first and walk it again.`,
  },
  merge_two_sorted_lists: {
    rows: [["Time", "O(n + m)"], ["Space", "O(1)"], ["vs. arrays", "no copy"]],
    reading: (c, s) =>
      `${c.comparisons ?? 0} comparison(s), ${c.splices ?? 0} splice(s). Each node ` +
      `is re-pointed exactly once and nothing is copied — the merge step of merge ` +
      `sort, but on pointers, in constant extra space.`,
  },
  anagram: {
    rows: [["Sort", "O(n log n)"], ["Count-map", "O(n)"], ["Space", "O(n)"]],
    reading: (c, s) =>
      `${c.comparisons ?? 0} column comparison(s), ${c.mismatches ?? 0} mismatch(es). ` +
      `Sorting both words and lining them up is O(n log n); tallying letter counts ` +
      `instead would settle it in a single O(n) pass.`,
  },
  gcd_euclid: {
    rows: [["Time", "O(log n)"], ["Space", "O(1)"], ["Naive", "O(n)"]],
    reading: (c, s) =>
      `${c.divisions ?? 0} division(s) to reach the answer. Each remainder step at ` +
      `least halves the larger number every two rounds, so Euclid is logarithmic — ` +
      `not the linear slog of testing every candidate divisor.`,
  },
  fast_exponentiation: {
    rows: [["Time", "O(log n)"], ["Space", "O(1)"], ["Naive", "O(n)"]],
    reading: (c, s) =>
      `${c.squarings ?? 0} squaring(s) and ${c.multiplies ?? 0} multiply(ies) — one ` +
      `per bit of the exponent. Squaring doubles the exponent reached each step, so ` +
      `log(exp) operations replace exp of them.`,
  },
  prime_factorisation: {
    rows: [["Time", "O(√n)"], ["Space", "O(1)"], ["Factors", "with multiplicity"]],
    reading: (c, s) =>
      `${c.trials ?? 0} trial divisor(s) tested, ${c.factors ?? 0} prime(s) pulled ` +
      `out. Testing only up to √n is the whole trick — any larger factor would have ` +
      `a matching smaller one already found.`,
  },
  bellman_ford: {
    rows: [["Time", "O(V·E)"], ["Space", "O(V)"], ["vs. Dijkstra", "handles negatives"]],
    reading: (c, s) =>
      `${c.rounds ?? 0} round(s), ${c.relaxations ?? 0} relaxation(s) over ` +
      `${c.edge_checks ?? 0} edge check(s). Sweeping every edge V−1 times is ` +
      `slower than Dijkstra, but it is the price of surviving negative weights — ` +
      `and one extra sweep is what exposes a negative cycle.`,
  },
};

// ── Generated cards ─────────────────────────────────────────────────────────
// The hand-written cards above cover the classics. Every other algorithm gets
// a card from its compact spec in complexitySpecs.js: the rows are the spec's,
// and the reading is assembled from whatever counters the tracer reports,
// plus the bound's value for the current input when the size is known.

// Counters that describe a state rather than a tally read better as "k = 3".
const STATE_COUNTERS = new Set(["k", "depth", "size", "count", "distinct", "heap_size",
  "nodes", "max_depth", "best", "window", "reach", "sum", "largest", "odd", "value",
  "result", "gcd", "lcm", "acc", "flow", "profit", "total", "total_wait", "cost",
  "peak", "platforms", "fives", "tens", "remaining", "open", "close", "lps"]);

function counterPhrase(key, value) {
  const words = key.replace(/_/g, " ");
  if (key.length <= 2 || STATE_COUNTERS.has(key)) return `${words} = ${value}`;
  const one = value === 1 && /s$/.test(words) && !/ss$/.test(words);
  return `${value} ${one ? words.slice(0, -1) : words}`;
}

// The bound's value for this input, when the formula is only in n or in V/E.
function boundValue(time, s) {
  const n = s?.n || 0, V = s?.V || 0, E = s?.E || 0;
  const lg = x => Math.log2(Math.max(x, 2));
  const fact = x => { let r = 1; for (let i = 2; i <= Math.min(x, 15); i++) r *= i; return r; };
  const t = time.replace(/\s+/g, "");
  const table = {};
  if (n > 1) Object.assign(table, {
    "O(n)": ["n", n], "O(n²)": ["n²", n * n], "O(n³)": ["n³", n ** 3],
    "O(nlogn)": ["n·log₂ n", Math.round(n * lg(n)), true],
    "O(logn)": ["log₂ n", Math.ceil(lg(n)), true],
    "O(log²n)": ["log₂² n", Math.ceil(lg(n) ** 2), true],
    "O(nlog²n)": ["n·log₂² n", Math.round(n * lg(n) ** 2), true],
    "O(√n)": ["√n", Math.ceil(Math.sqrt(n)), true],
    "O(2ⁿ)": ["2ⁿ", 2 ** Math.min(n, 30)], "O(n·2ⁿ)": ["n·2ⁿ", n * 2 ** Math.min(n, 30)],
    "O(2ⁿ·n)": ["2ⁿ·n", n * 2 ** Math.min(n, 30)], "O(n!)": ["n!", fact(n)],
  });
  if (V > 1) Object.assign(table, {
    "O(V+E)": ["V + E", V + E], "O(E)": ["E", E], "O(V²)": ["V²", V * V], "O(V³)": ["V³", V ** 3],
    "O(V·E)": ["V·E", V * E], "O(V·E²)": ["V·E²", V * E * E],
    "O((V+E)logV)": ["(V + E)·log₂ V", Math.round((V + E) * lg(V)), true],
    "O(ElogV)": ["E·log₂ V", Math.round(E * lg(V)), true],
    "O(ElogE)": ["E·log₂ E", Math.round(E * lg(E)), true],
  });
  const hit = table[t];
  return hit ? `${hit[0]} ${hit[2] ? "≈" : "="} ${hit[1]}` : "";
}

export function cardFromSpec([time, space, why, ...extra]) {
  return {
    generated: true,
    rows: [["Time", time], ["Space", space], ...extra],
    reading: (c, s) => {
      const parts = Object.entries(c || {})
        .filter(([, v]) => typeof v === "number")
        .map(([k, v]) => counterPhrase(k, v));
      const size = s?.V ? `${s.V} nodes / ${s.E} edges` : s?.n > 1 ? `${s.n} values` : "";
      const head = parts.length
        ? `Your run${size ? ` on ${size}` : ""}: ${parts.join(" · ")}.`
        : size ? `Your run on ${size}.` : "";
      const bound = boundValue(time, s);
      return [head, why, bound ? `For this input that bound is ${bound}.` : ""]
        .filter(Boolean).join(" ");
    },
  };
}

for (const [id, spec] of Object.entries(COMPLEXITY_SPECS)) {
  if (!COMPLEXITY[id]) COMPLEXITY[id] = cardFromSpec(spec);
}

// Each insight opens the live trace of the algorithm it is about — there is
// no separate article behind these cards, so the card never promises one.
export const CLIPS = [
  { tag: "TODAY", topic: "Graphs",   title: "Why GPS uses Dijkstra's, not BFS",            algo: "dijkstra" },
  { tag: "TODAY", topic: "Arrays",   title: "Kadane's Algorithm: The Hidden Pattern",       algo: "kadanes" },
  { tag: "TODAY", topic: "Trees",    title: "Why BSTs beat Hash Maps for ranges",           algo: "bst_search" },
  { tag: "TODAY", topic: "DP",       title: "Memoization vs Tabulation — when each wins",   algo: "fibonacci_dp" },
  { tag: "TODAY", topic: "Sorting",  title: "Merge Sort: why divide and conquer wins",      algo: "merge_sort" },
  { tag: "TODAY", topic: "Strings",  title: "KMP: Pattern matching without backtracking",   algo: "kmp_search" },
];

// Illustrative, not claims about any named company's internals.
export const REALWORLD = [
  { icon: "🗺️", metaphor: "Graphs",  title: "Navigation apps",  desc: "Shortest-path algorithms in Dijkstra's family are the backbone of turn-by-turn routing." },
  { icon: "🔗", metaphor: "DP",      title: "DNA Sequencing",   desc: "Edit distance (Levenshtein) underpins sequence alignment in bioinformatics." },
  { icon: "🛒", metaphor: "Hashing", title: "E-Commerce Cart",  desc: "Hash maps give O(1) product lookup across catalogues of millions of items." },
  { icon: "📱", metaphor: "BFS",     title: "Social Networks",  desc: "Friend-of-a-friend suggestions are a breadth-first search over the social graph." },
  { icon: "🧬", metaphor: "Trees",   title: "File Systems",     desc: "A filesystem is a tree — directories are inner nodes, files are leaves." },
  { icon: "⚙️", metaphor: "Heaps",  title: "OS Schedulers",    desc: "Priority queues decide which process gets CPU time next." },
];
