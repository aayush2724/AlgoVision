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
    hook: "Operators wait on a stack until precedence lets them out." },
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
  { id: "add_one_list", name: "Add 1 to a List Number", category: "Structures", emoji: "☝️", complexity: "O(n)", input: "array",
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
    hook: "Watch the stack: right is pushed before left." },
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
    hook: "The search can move up through parents too." },
  { id: "burn_tree", name: "Minimum Time to Burn a Binary Tree", category: "Structures", emoji: "🌳", complexity: "O(n)", input: "text",
    hook: "Fire spreads to children and the parent each minute." },
  { id: "count_complete_nodes", name: "Count Nodes in a Complete Binary Tree", category: "Structures", emoji: "🌳", complexity: "O(log² n)", input: "text",
    hook: "Perfect subtrees are counted without walking them." },
  { id: "frog_jump_k", name: "Frog Jump With K Distances", category: "DP", emoji: "🧮", complexity: "O(n·k)", input: "text",
    hook: "Each stone looks back up to K stones for the cheapest jump." },
  { id: "ninja_training", name: "Ninja's Training", category: "DP", emoji: "🧮", complexity: "O(n·m)", input: "text",
    hook: "No task twice in a row." },
  { id: "min_falling_path", name: "Minimum Falling Path Sum", category: "DP", emoji: "🧮", complexity: "O(n·m)", input: "text",
    hook: "Each cell reads the three cells above." },
  { id: "triangle_path", name: "Triangle (Minimum Path Sum)", category: "DP", emoji: "🧮", complexity: "O(n·m)", input: "text",
    hook: "Move to the same or next index." },
  { id: "partition_equal_subset", name: "Partition Equal Subset Sum", category: "DP", emoji: "🧮", complexity: "O(n·m)", input: "text",
    hook: "Equal halves ⇔ some subset reaches total/2." },
  { id: "count_subsets_sum_k", name: "Count Subsets With Sum K", category: "DP", emoji: "🧮", complexity: "O(n·m)", input: "text",
    hook: "Each cell adds ways without and with the new value." },
  { id: "unbounded_knapsack", name: "Unbounded Knapsack", category: "DP", emoji: "🧮", complexity: "O(n·m)", input: "text",
    hook: "Taking an item reads the same row." },
  { id: "rod_cutting", name: "Rod Cutting", category: "DP", emoji: "🧮", complexity: "O(n·m)", input: "text",
    hook: "The rod length is the number of prices." },
  { id: "print_lcs", name: "Print the Longest Common Subsequence", category: "DP", emoji: "🧬", complexity: "O(n·m)", input: "text",
    hook: "Fill the table, then trace the answer back from the corner." },
  { id: "longest_palindromic_subseq", name: "Longest Palindromic Subsequence", category: "DP", emoji: "🧬", complexity: "O(n·m)", input: "text",
    hook: "One word (up to 8 chars) — compared with its own reverse." },
  { id: "min_insert_palindrome", name: "Minimum Insertions to Make a Palindrome", category: "DP", emoji: "🧬", complexity: "O(n·m)", input: "text",
    hook: "Insertions = length − longest palindromic subsequence." },
  { id: "min_ins_del", name: "Minimum Insertions/Deletions (A → B)", category: "DP", emoji: "🧬", complexity: "O(n·m)", input: "text",
    hook: "Keep the LCS, delete/insert the rest." },
  { id: "shortest_supersequence", name: "Shortest Common Supersequence", category: "DP", emoji: "🧬", complexity: "O(n·m)", input: "text",
    hook: "The LCS is written once." },
  { id: "distinct_subsequences", name: "Distinct Subsequences", category: "DP", emoji: "🧬", complexity: "O(n·m)", input: "text",
    hook: "Count the ways the target appears." },
  { id: "wildcard_match", name: "Wildcard Matching", category: "DP", emoji: "🧬", complexity: "O(n·m)", input: "text",
    hook: "Text, then pattern with ? (one char) and * (any run)." },
  { id: "number_of_islands", name: "Number of Islands", category: "Graphs", emoji: "🗺️", complexity: "O(R·C)", input: "text",
    hook: "0/1 grid, rows split by / (up to 7×7). Each new island gets its own letter." },
  { id: "rotten_oranges", name: "Rotten Oranges", category: "Graphs", emoji: "🗺️", complexity: "O(R·C)", input: "text",
    hook: "0 empty, 1 fresh, 2 rotten. Cells show the minute they rot; −1 if some never can." },
  { id: "nearest_one_distance", name: "Distance of Nearest Cell Having 1", category: "Graphs", emoji: "🗺️", complexity: "O(R·C)", input: "text",
    hook: "0/1 grid. A BFS from every 1 at once fills in each cell's distance." },
  { id: "surrounded_regions", name: "Surrounded Regions", category: "Graphs", emoji: "🗺️", complexity: "O(R·C)", input: "text",
    hook: "X/O grid. Only O regions touching the border survive; the rest flip to X." },
  { id: "number_of_enclaves", name: "Number of Enclaves", category: "Graphs", emoji: "🗺️", complexity: "O(R·C)", input: "text",
    hook: "0/1 grid. Land that can't walk off the edge is counted (marked E)." },
  { id: "binary_maze_path", name: "Shortest Path in a Binary Maze", category: "Graphs", emoji: "🧭", complexity: "O(R·C)", input: "text",
    hook: "1 = open, 0 = wall (up to 6×6). BFS from top-left to bottom-right." },
  { id: "min_effort_path", name: "Path With Minimum Effort", category: "Graphs", emoji: "🧭", complexity: "O(R·C log RC)", input: "text",
    hook: "Heights 0–99. A route costs its steepest single step — Dijkstra on that." },
  { id: "swim_rising_water", name: "Swim in Rising Water", category: "Graphs", emoji: "🧭", complexity: "O(R·C log RC)", input: "text",
    hook: "Heights 0–99. A route costs its highest cell — Dijkstra on that." },
  { id: "largest_island", name: "Making a Large Island", category: "Graphs", emoji: "🧭", complexity: "O(R·C log RC)", input: "text",
    hook: "0/1 grid. Cells show island sizes; each 0 is tried as the one flip." },
  { id: "islands_ii", name: "Number of Islands II (Online)", category: "Graphs", emoji: "🧭", complexity: "O(k α(n))", input: "text",
    hook: "Grid size, then the cells turned to land in order. Union-find keeps the count." },
  { id: "floyd_warshall", name: "Floyd–Warshall (All-Pairs Shortest Paths)", category: "Graphs", emoji: "📐", complexity: "O(V³)", input: "text",
    hook: "Edges: A>B:3 one way, A-B:3 both ways (up to 6 nodes). Negatives allowed." },
  { id: "city_fewest_neighbours", name: "City With the Fewest Neighbours in Reach", category: "Graphs", emoji: "📐", complexity: "O(V³)", input: "text",
    hook: "Roads as A-B:len (both ways) and a distance threshold. Floyd–Warshall, then count." },
  { id: "stock_ii", name: "Best Time to Buy & Sell Stock II (Unlimited)", category: "DP", emoji: "📈", complexity: "O(n)", input: "text",
    hook: "Up to 8 prices. Two states per day: free or holding a share." },
  { id: "stock_iii", name: "Best Time to Buy & Sell Stock III (≤ 2 Trades)", category: "DP", emoji: "📈", complexity: "O(n)", input: "text",
    hook: "Up to 8 prices, at most two trades: buy1, sell1, buy2, sell2." },
  { id: "stock_iv", name: "Best Time to Buy & Sell Stock IV (≤ k Trades)", category: "DP", emoji: "📈", complexity: "O(n·k)", input: "text",
    hook: "Up to 8 prices and k (1–3) trades." },
  { id: "stock_cooldown", name: "Buy & Sell Stock With Cooldown", category: "DP", emoji: "📈", complexity: "O(n)", input: "text",
    hook: "Up to 8 prices. After a sale you must rest one day." },
  { id: "stock_fee", name: "Buy & Sell Stock With Transaction Fee", category: "DP", emoji: "📈", complexity: "O(n)", input: "text",
    hook: "Up to 8 prices and the fee paid on every sale." },
  { id: "print_lis", name: "Print the Longest Increasing Subsequence", category: "DP", emoji: "📏", complexity: "O(n²)", input: "text",
    hook: "Up to 8 numbers. Keep each position's predecessor to print one LIS back." },
  { id: "largest_divisible_subset", name: "Largest Divisible Subset", category: "DP", emoji: "📏", complexity: "O(n²)", input: "text",
    hook: "Up to 8 positive numbers (sorted for you). 'Smaller' becomes 'divides'." },
  { id: "longest_string_chain", name: "Longest String Chain", category: "DP", emoji: "📏", complexity: "O(n²)", input: "text",
    hook: "Up to 8 words. A word extends a chain if deleting one letter gives the previous one." },
  { id: "longest_bitonic", name: "Longest Bitonic Subsequence", category: "DP", emoji: "📏", complexity: "O(n²)", input: "text",
    hook: "Up to 8 numbers. Rising into i plus falling out of i, minus 1." },
  { id: "number_of_lis", name: "Number of Longest Increasing Subsequences", category: "DP", emoji: "📏", complexity: "O(n²)", input: "text",
    hook: "Up to 8 numbers. Track the best length and how many ways reach it." },
  { id: "cycle_undirected_bfs", name: "Cycle Detection in an Undirected Graph (BFS)", category: "Graphs", emoji: "🕸️", complexity: "O(V + E)", input: "graph",
    hook: "Explore by BFS, remembering where you came from; a visited neighbour that isn't your par" },
  { id: "cycle_undirected_dfs", name: "Cycle Detection in an Undirected Graph (DFS)", category: "Graphs", emoji: "🕸️", complexity: "O(V + E)", input: "graph",
    hook: "Walk depth-first; meeting an already-visited node that isn't where you just came from me" },
  { id: "bridges", name: "Bridges in a Graph (Tarjan)", category: "Graphs", emoji: "🕸️", complexity: "O(V + E)", input: "graph",
    hook: "A cable is critical when nothing below it can reach back above it — low-link beats disco" },
  { id: "articulation_points", name: "Articulation Points", category: "Graphs", emoji: "🕸️", complexity: "O(V + E)", input: "graph",
    hook: "A hub is critical when some branch below it can only reach the rest through it." },
  { id: "connect_network_ops", name: "Operations to Make a Network Connected", category: "Graphs", emoji: "🕸️", complexity: "O(V + E)", input: "graph",
    hook: "Every spare cable can join two groups; you need one move per extra group." },
  { id: "cycle_directed", name: "Cycle Detection in a Directed Graph (DFS)", category: "Graphs", emoji: "➡️", complexity: "O(V + E)", input: "graph",
    hook: "One-way streets: only an edge back into your current route makes a loop." },
  { id: "safe_states", name: "Find Eventual Safe States", category: "Graphs", emoji: "➡️", complexity: "O(V + E)", input: "graph",
    hook: "A room is safe if every corridor out of it eventually dead-ends — never into a loop." },
  { id: "kosaraju", name: "Strongly Connected Components (Kosaraju)", category: "Graphs", emoji: "➡️", complexity: "O(V + E)", input: "graph",
    hook: "Finish order on the graph, then explore the reversed graph from the last finisher: each " },
  { id: "shortest_path_dag", name: "Shortest Path in a DAG", category: "Graphs", emoji: "➡️", complexity: "O(V + E)", input: "graph",
    hook: "With no loops, relaxing edges in topological order settles every distance in one pass." },
  { id: "floor_ceil_bst", name: "Floor and Ceil in a BST", category: "Structures", emoji: "🌲", complexity: "O(n)", input: "text",
    hook: "Values inserted into a BST, then | x. One walk down for the floor, one for the ceil." },
  { id: "kth_bst", name: "Kth Smallest and Largest in a BST", category: "Structures", emoji: "🌲", complexity: "O(n)", input: "text",
    hook: "Values inserted into a BST, then | k. Inorder visits in sorted order." },
  { id: "lca_bst", name: "LCA in a BST", category: "Structures", emoji: "🌲", complexity: "O(n)", input: "text",
    hook: "Values inserted into a BST, then | a b. Go the way both lie until they split." },
  { id: "successor_predecessor", name: "Inorder Successor / Predecessor in a BST", category: "Structures", emoji: "🌲", complexity: "O(n)", input: "text",
    hook: "Values inserted into a BST, then | x. Smallest above x, largest below x." },
  { id: "two_sum_bst", name: "Two Sum in a BST", category: "Structures", emoji: "🌲", complexity: "O(n)", input: "text",
    hook: "Values inserted into a BST, then | k. Sorted inorder plus two pointers." },
  { id: "bst_from_preorder", name: "Construct a BST From Preorder", category: "Structures", emoji: "🌲", complexity: "O(n)", input: "text",
    hook: "A preorder listing; each value is placed by walking down from the root." },
  { id: "validate_bst", name: "Check if a Tree is a BST", category: "Structures", emoji: "🌲", complexity: "O(n)", input: "text",
    hook: "Any tree in level order. Each node must fit the window its ancestors set." },
  { id: "recover_bst", name: "Recover a BST With Two Swapped Nodes", category: "Structures", emoji: "🌲", complexity: "O(n)", input: "text",
    hook: "A BST with two values swapped, in level order. Inorder reveals the pair." },
  { id: "largest_bst", name: "Largest BST in a Binary Tree", category: "Structures", emoji: "🌲", complexity: "O(n)", input: "text",
    hook: "Any tree in level order. Subtrees report (is BST, size, min, max) upward." },
  { id: "is_min_heap", name: "Check if an Array is a Min-Heap", category: "Structures", emoji: "⛰️", complexity: "O(n)", input: "text",
    hook: "Up to 12 numbers read as a complete tree. Every parent must be ≤ its children." },
  { id: "min_to_max_heap", name: "Convert a Min-Heap to a Max-Heap", category: "Structures", emoji: "⛰️", complexity: "O(n)", input: "text",
    hook: "A min-heap array. Bottom-up heapify turns it into a max-heap." },
  { id: "connect_sticks", name: "Minimum Cost to Connect Sticks", category: "Structures", emoji: "⛰️", complexity: "O(n)", input: "text",
    hook: "Stick lengths (1–999). Always join the two cheapest — the heap tree shrinks each round." },
  { id: "rank_replace", name: "Replace Elements by Their Rank", category: "Structures", emoji: "⛰️", complexity: "O(n)", input: "text",
    hook: "Up to 12 numbers. Each becomes its rank among the distinct values." },
  { id: "top_k_frequent", name: "Top K Frequent Elements", category: "Structures", emoji: "⛰️", complexity: "O(n)", input: "text",
    hook: "Up to 12 numbers and k. Count, then keep a size-k min-heap." },
  { id: "hand_of_straights", name: "Hand of Straights", category: "Structures", emoji: "⛰️", complexity: "O(n)", input: "text",
    hook: "Cards and the group size. Start each group at the smallest card left." },
  { id: "task_scheduler", name: "Task Scheduler", category: "Structures", emoji: "⛰️", complexity: "O(n)", input: "text",
    hook: "Tasks as letters and the cooldown n. Idle only when nothing can run." },
  { id: "median_stream", name: "Find Median From a Data Stream", category: "Structures", emoji: "⛰️", complexity: "O(n)", input: "text",
    hook: "Numbers arriving one by one. Two heaps keep the median on top." },
  { id: "remove_outer_parens", name: "Remove Outermost Parentheses", category: "Strings", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "A balanced string of ( and ) (up to 12). Drop each group's outer pair." },
  { id: "reverse_words", name: "Reverse Words in a String", category: "Strings", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "A sentence (up to 24 chars). Extra spaces vanish; word order reverses." },
  { id: "largest_odd_number", name: "Largest Odd Number in a String", category: "Strings", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "Digits (up to 12). Cut after the rightmost odd digit." },
  { id: "longest_common_prefix", name: "Longest Common Prefix", category: "Strings", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "2–5 words. Compare one column at a time." },
  { id: "isomorphic_strings", name: "Isomorphic Strings", category: "Strings", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "Two words. A consistent one-to-one letter mapping, both ways." },
  { id: "rotate_string", name: "Rotate String", category: "Strings", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "Two words. The second is a rotation iff it appears in first + first." },
  { id: "sort_by_frequency", name: "Sort Characters by Frequency", category: "Strings", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "Up to 12 letters/digits. Most frequent characters first." },
  { id: "max_nesting_depth", name: "Maximum Nesting Depth of Parentheses", category: "Strings", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "Up to 12 characters with balanced parentheses." },
  { id: "roman_to_integer", name: "Roman to Integer", category: "Strings", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "Roman numerals (up to 12). Subtract when a smaller one precedes a bigger one." },
  { id: "string_to_integer", name: "String to Integer (atoi)", category: "Strings", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "Any text (up to 24). Spaces, one sign, digits, stop, clamp." },
  { id: "sum_of_beauty", name: "Sum of Beauty of All Substrings", category: "Strings", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "Up to 8 letters. Cell (i, j) is the beauty of s[i..j]." },
  { id: "char_replacement", name: "Longest Repeating Character Replacement", category: "Patterns", emoji: "🪟", complexity: "O(n)", input: "text",
    hook: "Letters and k. Window length − top count must stay ≤ k." },
  { id: "build_pre_in", name: "Construct a Binary Tree from Preorder & Inorder", category: "Trees", emoji: "🌱", complexity: "O(n)", input: "text",
    hook: "Preorder | inorder (distinct values). Root first, inorder splits the rest." },
  { id: "build_post_in", name: "Construct a Binary Tree from Postorder & Inorder", category: "Trees", emoji: "🌱", complexity: "O(n)", input: "text",
    hook: "Postorder | inorder (distinct values). Root last, inorder splits the rest." },
  { id: "serialize_tree", name: "Serialize and Deserialize a Binary Tree", category: "Trees", emoji: "📦", complexity: "O(n)", input: "text",
    hook: "Level order, null for gaps. BFS writes '#' for missing children." },
  { id: "morris_inorder", name: "Morris Inorder Traversal", category: "Trees", emoji: "🧵", complexity: "O(n), O(1) space", input: "text",
    hook: "Level order. Dashed edges are temporary threads." },
  { id: "morris_preorder", name: "Morris Preorder Traversal", category: "Trees", emoji: "🧵", complexity: "O(n), O(1) space", input: "text",
    hook: "Level order. Visit when the thread is made, not when it's removed." },
  { id: "flatten_tree", name: "Flatten a Binary Tree to a Linked List", category: "Trees", emoji: "📜", complexity: "O(n)", input: "text",
    hook: "Level order. Splice each left subtree into the right chain." },
  { id: "identical_trees", name: "Check if Two Trees are Identical", category: "Trees", emoji: "👯", complexity: "O(n)", input: "text",
    hook: "Two level-order trees split by '|'. Compare in lockstep." },
  { id: "merge_two_bsts", name: "Merge Two BSTs (sorted output)", category: "Trees", emoji: "🔀", complexity: "O(m + n)", input: "text",
    hook: "Two BSTs as insertion orders split by '|'. Inorders, then merge." },
  { id: "stack_array", name: "Implement a Stack Using an Array", category: "Stacks", emoji: "🥞", complexity: "O(1) per op", input: "text",
    hook: "Ops: push x, pop, top. Array + top index." },
  { id: "queue_array", name: "Implement a Queue Using an Array", category: "Queues", emoji: "🎫", complexity: "O(1) per op", input: "text",
    hook: "Ops: push x, pop, front. Circular array." },
  { id: "stack_using_queue", name: "Implement a Stack Using a Queue", category: "Stacks", emoji: "🔄", complexity: "O(n) push", input: "text",
    hook: "Ops: push x, pop, top. Rotate after each push." },
  { id: "queue_using_stacks", name: "Implement a Queue Using Stacks", category: "Queues", emoji: "🔄", complexity: "O(1) amortised", input: "text",
    hook: "Ops: push x, pop, front. Pour in→out only when out is empty." },
  { id: "stack_linkedlist", name: "Implement a Stack Using a Linked List", category: "Stacks", emoji: "🚃", complexity: "O(1) per op", input: "text",
    hook: "Ops: push x, pop, top. New nodes go at the head." },
  { id: "queue_linkedlist", name: "Implement a Queue Using a Linked List", category: "Queues", emoji: "🚃", complexity: "O(1) per op", input: "text",
    hook: "Ops: push x, pop, front. Enqueue at rear, dequeue at front." },
  { id: "min_stack", name: "Implement a Min Stack", category: "Stacks", emoji: "📉", complexity: "O(1) per op", input: "text",
    hook: "Ops: push x, pop, top, getmin. Each entry keeps the min below it." },
  { id: "lru_cache", name: "LRU Cache", category: "Design", emoji: "🗃️", complexity: "O(1) per op", input: "text",
    hook: "Ops: put k v, get k. Evict the least recently used." },
  { id: "lfu_cache", name: "LFU Cache", category: "Design", emoji: "🗃️", complexity: "O(1) per op", input: "text",
    hook: "Ops: put k v, get k. Evict the least used (ties: least recent)." },
  { id: "design_twitter", name: "Design Twitter", category: "Design", emoji: "🐦", complexity: "O(n log k)", input: "text",
    hook: "Ops: post u t, follow a b, unfollow a b, feed u." },
  { id: "clone_random_list", name: "Clone a Linked List With Random Pointers", category: "Linked Lists", emoji: "🧬", complexity: "O(n), O(1) space", input: "text",
    hook: "Values | random index per node (−1 = null). Weave, point, unweave." },
  { id: "flatten_list", name: "Flatten a Linked List (sorted columns)", category: "Linked Lists", emoji: "🪜", complexity: "O(N·k)", input: "text",
    hook: "Sorted columns split by '|'. Merge from the right." },
  { id: "merge_k_lists", name: "Merge K Sorted Lists", category: "Linked Lists", emoji: "🧺", complexity: "O(N log k)", input: "text",
    hook: "Sorted lists split by '|'. Min-heap of heads." },
  { id: "bracket_reversals", name: "Minimum Bracket Reversals to Balance", category: "Strings", emoji: "🔃", complexity: "O(n)", input: "text",
    hook: "Only { and }. Cancel pairs; ceil(close/2) + ceil(open/2)." },
  { id: "count_and_say", name: "Count and Say", category: "Strings", emoji: "🗣️", complexity: "O(total length)", input: "text",
    hook: "n (1–8). Read the previous term run by run." },
  { id: "longest_happy_prefix", name: "Longest Happy Prefix (LPS)", category: "Strings", emoji: "😊", complexity: "O(n)", input: "text",
    hook: "Up to 16 letters. The KMP lps array's last value." },
  { id: "count_palindromic_subseq", name: "Count Palindromic Subsequences", category: "Strings", emoji: "🪞", complexity: "O(n²)", input: "text",
    hook: "Up to 10 letters. Interval DP with inclusion–exclusion." },
  { id: "distinct_substrings", name: "Number of Distinct Substrings (Trie)", category: "Tries", emoji: "🌳", complexity: "O(n²)", input: "text",
    hook: "Up to 8 letters. Insert every suffix; count new trie nodes." },
  { id: "max_xor_pair", name: "Maximum XOR of Two Numbers (Trie)", category: "Tries", emoji: "⊕", complexity: "O(n·B)", input: "text",
    hook: "Numbers 0–255. Bit trie; walk towards the opposite bit." },
  { id: "max_xor_queries", name: "Maximum XOR With an Element From an Array", category: "Tries", emoji: "⊕", complexity: "O((n + q)·B)", input: "text",
    hook: "Array | queries 'x m'. Sort by m, insert values ≤ m." },
  { id: "trie_advanced", name: "Trie With Counts (insert, count, erase)", category: "Tries", emoji: "🌳", complexity: "O(L) per op", input: "text",
    hook: "Ops: insert w, countwords w, countprefix p, erase w. Nodes keep prefix|end counts." },
  { id: "ninja_friends", name: "Ninja and His Friends (Cherry Pickup II)", category: "Dynamic Programming", emoji: "🍫", complexity: "O(r·c²·9)", input: "text",
    hook: "Rows split by '/'. Two walkers from the top corners; a shared cell counts once." },
  { id: "max_sum_combination", name: "Maximum Sum Combinations", category: "Heaps", emoji: "➕", complexity: "O(k log k)", input: "text",
    hook: "Two arrays | and k. Max-heap over index pairs." },
  { id: "accounts_merge", name: "Accounts Merge", category: "Graphs", emoji: "📇", complexity: "O(E α(n))", input: "text",
    hook: "Accounts 'Name email …' split by ';'. Union accounts sharing an email." },
  { id: "ll_insert_head", name: "Insert at the Head of a Linked List", category: "Linked Lists", emoji: "🚃", complexity: "O(1)", input: "text",
    hook: "The list, and the value to insert. New node → old head, then move head." },
  { id: "ll_delete_head", name: "Delete the Head of a Linked List", category: "Linked Lists", emoji: "🚃", complexity: "O(1)", input: "text",
    hook: "The list. Move head one step; free the old head." },
  { id: "ll_length", name: "Length of a Linked List", category: "Linked Lists", emoji: "🚃", complexity: "O(n)", input: "text",
    hook: "The list. Walk to null, counting." },
  { id: "ll_search", name: "Search in a Linked List", category: "Linked Lists", emoji: "🚃", complexity: "O(n)", input: "text",
    hook: "The list and x. No indexing — walk and compare." },
  { id: "dll_insert_head", name: "Insert Before the Head of a Doubly Linked List", category: "Linked Lists", emoji: "🚋", complexity: "O(1)", input: "text",
    hook: "The DLL and a value. Fix next AND prev." },
  { id: "dll_delete_head", name: "Delete the Head of a Doubly Linked List", category: "Linked Lists", emoji: "🚋", complexity: "O(1)", input: "text",
    hook: "The DLL. Move head; clear the new head's prev." },
  { id: "dll_pairs_sum", name: "Pairs With a Given Sum in a Sorted DLL", category: "Linked Lists", emoji: "🚋", complexity: "O(n)", input: "text",
    hook: "A sorted DLL and the sum. Head and tail walk inward." },
  { id: "dll_remove_duplicates", name: "Remove Duplicates From a Sorted DLL", category: "Linked Lists", emoji: "🚋", complexity: "O(n)", input: "text",
    hook: "A sorted DLL. Unlink each repeat (next and prev)." },
  { id: "ll_reverse_recursive", name: "Reverse a Linked List (Recursive)", category: "Linked Lists", emoji: "🔁", complexity: "O(n)", input: "text",
    hook: "The list. Reverse the rest, then flip one arrow on the way back." },
  { id: "loop_length", name: "Length of a Loop in a Linked List", category: "Linked Lists", emoji: "➰", complexity: "O(n)", input: "text",
    hook: "The list and where the tail links back (−1 = none). Floyd, then count the ring." },
  { id: "sort_012_list", name: "Sort a Linked List of 0s, 1s and 2s", category: "Linked Lists", emoji: "🚥", complexity: "O(n)", input: "text",
    hook: "0s, 1s and 2s. Build three chains by relinking, then join." },
  { id: "sort_list", name: "Sort a Linked List (Merge Sort)", category: "Linked Lists", emoji: "🔀", complexity: "O(n log n)", input: "text",
    hook: "The list. Merge sort: split at the middle, merge by relinking." },
  { id: "y_intersection", name: "Intersection Point of a Y-Shaped Linked List", category: "Linked Lists", emoji: "🔱", complexity: "O(n + m)", input: "text",
    hook: "A only | B only | shared tail. Pointers swap heads at the end." },
  { id: "reverse_k_group", name: "Reverse a Linked List in Groups of K", category: "Linked Lists", emoji: "🔁", complexity: "O(n)", input: "text",
    hook: "The list and k. Reverse each full group; a short tail stays." },
  { id: "search_rotated_ii", name: "Search in Rotated Sorted Array II (duplicates)", category: "Binary Search", emoji: "🔄", complexity: "O(log n) avg", input: "text",
    hook: "A rotated array (duplicates allowed) and the target." },
  { id: "median_two_sorted", name: "Median of Two Sorted Arrays", category: "Binary Search", emoji: "⚖️", complexity: "O(log min(n,m))", input: "text",
    hook: "Two sorted arrays split by '|'. Binary-search the cut." },
  { id: "kth_two_sorted", name: "K-th Element of Two Sorted Arrays", category: "Binary Search", emoji: "🎯", complexity: "O(log min(n,m))", input: "text",
    hook: "Two sorted arrays and k. The left part holds k values." },
  { id: "gas_station", name: "Minimise Max Distance to Gas Station", category: "Binary Search", emoji: "⛽", complexity: "O(n log R)", input: "text",
    hook: "Station positions and k new stations. Binary-search the real answer." },
  { id: "peak_element_ii", name: "Find a Peak Element II (matrix)", category: "Binary Search", emoji: "⛰️", complexity: "O(n log m)", input: "text",
    hook: "Rows split by '/', neighbours distinct. Column max, then climb." },
  { id: "matrix_median", name: "Median of a Row-Wise Sorted Matrix", category: "Binary Search", emoji: "▦", complexity: "O(r log c log R)", input: "text",
    hook: "Sorted rows split by '/', odd cell count. Binary-search the value." },
  { id: "print_1_to_n", name: "Print 1 to N Using Recursion", category: "Recursion", emoji: "🔢", complexity: "O(n)", input: "text",
    hook: "N (1–10). Print before the call → ascending." },
  { id: "print_n_to_1", name: "Print N to 1 Using Recursion", category: "Recursion", emoji: "🔢", complexity: "O(n)", input: "text",
    hook: "N (1–10). Print after the call → descending." },
  { id: "recursive_bubble_sort", name: "Recursive Bubble Sort", category: "Sorting", emoji: "🫧", complexity: "O(n²)", input: "text",
    hook: "Up to 10 numbers. One pass, then bubble(n − 1)." },
  { id: "recursive_insertion_sort", name: "Recursive Insertion Sort", category: "Sorting", emoji: "🃏", complexity: "O(n²)", input: "text",
    hook: "Up to 10 numbers. Insert a[i], then insert(i + 1)." },
  { id: "count_good_numbers", name: "Count Good Numbers", category: "Recursion", emoji: "✅", complexity: "O(log n)", input: "text",
    hook: "Length n (≤ 10^15). 5^ceil(n/2) · 4^floor(n/2) by fast power." },
  { id: "sort_stack", name: "Sort a Stack Using Recursion", category: "Recursion", emoji: "🥞", complexity: "O(n²)", input: "text",
    hook: "Stack bottom → top (≤ 8). Pop, sort the rest, insert in order." },
  { id: "reverse_stack", name: "Reverse a Stack Using Recursion", category: "Recursion", emoji: "🥞", complexity: "O(n²)", input: "text",
    hook: "Stack bottom → top (≤ 8). Pop, reverse the rest, insert at the bottom." },
  { id: "recursive_atoi", name: "Recursive atoi()", category: "Recursion", emoji: "🔤", complexity: "O(n)", input: "text",
    hook: "Any text (≤ 16). Spaces, sign, then one digit per call." },
  { id: "word_break", name: "Word Break", category: "Recursion", emoji: "🧩", complexity: "O(n·w·L)", input: "text",
    hook: "Text | words. can(i) = a word starts at i and can(i + len)." },
  { id: "m_coloring", name: "M-Coloring Problem", category: "Backtracking", emoji: "🎨", complexity: "O(mⁿ)", input: "text",
    hook: "Edges like 0-1,1-2 and m colours. Try, recurse, undo." },
  { id: "sudoku_solver", name: "Sudoku Solver", category: "Backtracking", emoji: "🔢", complexity: "O(9^blanks)", input: "text",
    hook: "4×4 or 9×9, 0 = blank (9×9 rows may skip commas)." },
  { id: "expression_add_operators", name: "Expression Add Operators", category: "Backtracking", emoji: "➕", complexity: "O(4ⁿ)", input: "text",
    hook: "1–5 digits and the target. Choose + − × or join between digits." },
  { id: "valid_paren_star", name: "Valid Parenthesis String (with *)", category: "Greedy", emoji: "✳️", complexity: "O(n)", input: "text",
    hook: "Only ( ) *. Track the range of possible open counts." },
  { id: "shortest_job_first", name: "Shortest Job First (SJF) Scheduling", category: "Greedy", emoji: "⏱️", complexity: "O(n log n)", input: "text",
    hook: "Burst times. Shortest first minimises the average wait." },
  { id: "lru_page_faults", name: "LRU Page Replacement (Page Faults)", category: "Greedy", emoji: "🗂️", complexity: "O(n·c)", input: "text",
    hook: "Page requests and capacity. Evict the least recently used." },
  { id: "insert_interval", name: "Insert Interval", category: "Greedy", emoji: "📏", complexity: "O(n)", input: "text",
    hook: "Sorted intervals | new interval. Copy, absorb, copy." },
  { id: "non_overlapping_intervals", name: "Non-overlapping Intervals", category: "Greedy", emoji: "📏", complexity: "O(n log n)", input: "text",
    hook: "Intervals like 1-2,2-3. Sort by end; keep what fits." },
  { id: "greater_to_right", name: "Number of Greater Elements to the Right", category: "Stacks", emoji: "↗️", complexity: "O(n²)", input: "text",
    hook: "Up to 10 numbers. For each index, count bigger values to its right." },
  { id: "sum_subarray_ranges", name: "Sum of Subarray Ranges", category: "Stacks", emoji: "📐", complexity: "O(n)", input: "text",
    hook: "Up to 10 numbers. Σ max·count − Σ min·count via monotonic stacks." },
  { id: "celebrity", name: "The Celebrity Problem", category: "Stacks", emoji: "⭐", complexity: "O(n)", input: "text",
    hook: "Square 0/1 'knows' matrix. Eliminate, then verify." },
  { id: "cut_stick", name: "Minimum Cost to Cut a Stick", category: "Dynamic Programming", emoji: "🪵", complexity: "O(c³)", input: "text",
    hook: "Length | cuts. Cell (i, j) = cheapest way to make every cut between cut i and cut j." },
  { id: "burst_balloons", name: "Burst Balloons", category: "Dynamic Programming", emoji: "🎈", complexity: "O(n³)", input: "text",
    hook: "Up to 6 digits. Pick the LAST balloon to burst in each range." },
  { id: "boolean_evaluation", name: "Evaluate Boolean Expression to True", category: "Dynamic Programming", emoji: "🔣", complexity: "O(n³)", input: "text",
    hook: "Alternate T/F with & | ^. Count the ways each range can be True / False." },
  { id: "palindrome_partition_ii", name: "Palindrome Partitioning II (Min Cuts)", category: "Dynamic Programming", emoji: "✂️", complexity: "O(n²)", input: "text",
    hook: "Up to 10 letters. Fewest cuts so every piece is a palindrome." },
  { id: "partition_array_max_sum", name: "Partition Array for Maximum Sum", category: "Dynamic Programming", emoji: "🧱", complexity: "O(n·k)", input: "text",
    hook: "Values 0–99 and k. Each piece becomes its max; maximise the total." },
  { id: "min_subset_diff", name: "Partition Into Two Subsets With Minimum Difference", category: "Dynamic Programming", emoji: "⚖️", complexity: "O(n·sum)", input: "text",
    hook: "Up to 6 values 0–12. Reachable subset sums → closest split." },
  { id: "count_partitions_diff", name: "Count Partitions With Given Difference", category: "Dynamic Programming", emoji: "⚖️", complexity: "O(n·sum)", input: "text",
    hook: "Values and difference d. Count subsets summing to (total − d)/2." },
  { id: "target_sum", name: "Target Sum", category: "Dynamic Programming", emoji: "➕", complexity: "O(n·sum)", input: "text",
    hook: "Values and target. Signs split the array into two subsets." },
  { id: "max_rectangle_ones", name: "Maximal Rectangle of 1s", category: "Dynamic Programming", emoji: "▦", complexity: "O(r·c)", input: "text",
    hook: "0/1 rows split by '/'. Each row becomes a histogram of heights." },
  { id: "largest_element", name: "Largest Element in an Array", category: "Arrays", emoji: "🏔️", complexity: "O(n)", input: "text",
    hook: "Up to 12 numbers. One pass keeps the biggest so far." },
  { id: "check_sorted", name: "Check if an Array is Sorted", category: "Arrays", emoji: "📈", complexity: "O(n)", input: "text",
    hook: "Up to 12 numbers. Every neighbour pair must be in order." },
  { id: "linear_search", name: "Linear Search", category: "Arrays", emoji: "🔎", complexity: "O(n)", input: "text",
    hook: "Numbers and x. Check each position in turn." },
  { id: "union_sorted", name: "Union of Two Sorted Arrays", category: "Arrays", emoji: "🔗", complexity: "O(n + m)", input: "text",
    hook: "Two sorted arrays split by '|'. Take the smaller, skip repeats." },
  { id: "intersection_sorted", name: "Intersection of Two Sorted Arrays", category: "Arrays", emoji: "🔗", complexity: "O(n + m)", input: "text",
    hook: "Two sorted arrays split by '|'. Advance the smaller side." },
  { id: "missing_number", name: "Find the Missing Number", category: "Arrays", emoji: "🕳️", complexity: "O(n)", input: "text",
    hook: "Distinct 0..n with one missing. XOR cancels every pair." },
  { id: "max_consecutive_ones", name: "Maximum Consecutive Ones", category: "Arrays", emoji: "1️⃣", complexity: "O(n)", input: "text",
    hook: "0/1 values. Count the run; anything else resets it." },
  { id: "rearrange_by_sign", name: "Rearrange Array Elements by Sign", category: "Arrays", emoji: "±", complexity: "O(n)", input: "text",
    hook: "Equal positives and negatives. + to even slots, − to odd slots." },
  { id: "max_product_subarray", name: "Maximum Product Subarray", category: "Arrays", emoji: "✖️", complexity: "O(n)", input: "text",
    hook: "Up to 12 numbers. Track max AND min — a negative swaps them." },
  { id: "longest_sum_k_any", name: "Longest Subarray With Sum K (any sign)", category: "Hashing", emoji: "🗺️", complexity: "O(n)", input: "text",
    hook: "Any signs and k. Map each prefix sum to where it first appeared." },
  { id: "count_sum_k", name: "Count Subarrays With Sum K", category: "Hashing", emoji: "🗺️", complexity: "O(n)", input: "text",
    hook: "Any signs and k. Count earlier prefixes equal to prefix − k." },
  { id: "largest_zero_sum", name: "Largest Subarray With Sum 0", category: "Hashing", emoji: "0️⃣", complexity: "O(n)", input: "text",
    hook: "Any signs. A repeated prefix sum means a zero-sum stretch between." },
  { id: "count_xor_k", name: "Count Subarrays With XOR K", category: "Hashing", emoji: "⊕", complexity: "O(n)", input: "text",
    hook: "Numbers and k. Count earlier prefix XORs equal to prefix ⊕ k." },
  { id: "longest_consecutive", name: "Longest Consecutive Sequence", category: "Hashing", emoji: "🔢", complexity: "O(n)", input: "text",
    hook: "Up to 12 numbers. Only count from a run's first value." },
  { id: "majority_n3", name: "Majority Elements (> n/3)", category: "Arrays", emoji: "🗳️", complexity: "O(n)", input: "text",
    hook: "Up to 12 numbers. Two candidates, then verify their counts." },
  { id: "repeating_missing", name: "Find the Repeating and Missing Numbers", category: "Arrays", emoji: "🔁", complexity: "O(n)", input: "text",
    hook: "1..n with one value repeated. Sum and sum-of-squares give two equations." },
  { id: "three_sum", name: "3 Sum", category: "Two Pointers", emoji: "3️⃣", complexity: "O(n²)", input: "text",
    hook: "Up to 12 numbers. Sort, fix one, two pointers for the rest." },
  { id: "four_sum", name: "4 Sum", category: "Two Pointers", emoji: "4️⃣", complexity: "O(n³)", input: "text",
    hook: "Numbers and target. Fix two, two pointers for the rest." },
  { id: "set_matrix_zeros", name: "Set Matrix Zeros", category: "Matrix", emoji: "0️⃣", complexity: "O(r·c)", input: "text",
    hook: "Rows split by '/'. Mark rows and columns first, then clear." },
  { id: "rotate_matrix", name: "Rotate a Matrix by 90°", category: "Matrix", emoji: "🔄", complexity: "O(n²)", input: "text",
    hook: "A square matrix. Transpose, then reverse each row." },
  { id: "spiral_order", name: "Spiral Traversal of a Matrix", category: "Matrix", emoji: "🌀", complexity: "O(r·c)", input: "text",
    hook: "Rows split by '/'. Walk the ring, then shrink the bounds." },
  { id: "pascal_triangle", name: "Pascal's Triangle", category: "Matrix", emoji: "🔺", complexity: "O(n²)", input: "text",
    hook: "Set ROWS (1–8). Each inner value = the two above it." },
  { id: "merge_no_space", name: "Merge Two Sorted Arrays Without Extra Space", category: "Arrays", emoji: "🧩", complexity: "O((n+m) log(n+m))", input: "text",
    hook: "Two sorted arrays split by '|'. Gap method, halving each round." },
  { id: "count_inversions", name: "Count Inversions", category: "Sorting", emoji: "🔀", complexity: "O(n log n)", input: "text",
    hook: "Up to 12 numbers. Count pairs across halves during merge sort." },
  { id: "reverse_pairs", name: "Reverse Pairs", category: "Sorting", emoji: "🔀", complexity: "O(n log n)", input: "text",
    hook: "Up to 12 numbers. Count a[i] > 2·a[j] across halves during merge sort." },
  { id: "count_digits", name: "Count Digits of a Number", category: "Math", emoji: "🔢", complexity: "O(log n)", input: "text",
    hook: "A whole number. Each ÷10 removes one digit." },
  { id: "reverse_number", name: "Reverse a Number", category: "Math", emoji: "↩️", complexity: "O(log n)", input: "text",
    hook: "A whole number. Peel n % 10 onto the reversed number." },
  { id: "palindrome_number", name: "Palindrome Number", category: "Math", emoji: "🪞", complexity: "O(log n)", input: "text",
    hook: "A whole number. Reverse it and compare." },
  { id: "armstrong_number", name: "Armstrong Number", category: "Math", emoji: "💪", complexity: "O(log n)", input: "text",
    hook: "A whole number. Sum of digits^(digit count)." },
  { id: "print_divisors", name: "Print All Divisors", category: "Math", emoji: "➗", complexity: "O(√n)", input: "text",
    hook: "1–999. Divisors pair up, so stop at √n." },
  { id: "check_prime", name: "Check for a Prime Number", category: "Math", emoji: "🔐", complexity: "O(√n)", input: "text",
    hook: "0–9999. Trial-divide up to √n." },
  { id: "factorial", name: "Factorial of a Number", category: "Recursion", emoji: "❗", complexity: "O(n)", input: "text",
    hook: "0–12. Multiply 1 × 2 × … × n." },
  { id: "sum_first_n", name: "Sum of the First N Numbers", category: "Recursion", emoji: "∑", complexity: "O(1)", input: "text",
    hook: "0–1000. Pair the ends: n(n + 1)/2." },
  { id: "reverse_array", name: "Reverse an Array (Two Pointers)", category: "Arrays", emoji: "↔️", complexity: "O(n)", input: "text",
    hook: "Up to 12 numbers. Swap the ends, move inward." },
  { id: "palindrome_string", name: "Check if a String is a Palindrome", category: "Strings", emoji: "🪞", complexity: "O(n)", input: "text",
    hook: "Up to 16 characters. Ignore case and symbols; compare the ends." },
  { id: "frequency_count", name: "Count Frequencies / Highest Occurring Element", category: "Hashing", emoji: "📊", complexity: "O(n)", input: "text",
    hook: "Up to 12 numbers. One pass with value → count." },
  { id: "check_ith_bit", name: "Check if the i-th Bit is Set", category: "Bit Manipulation", emoji: "🔦", complexity: "O(1)", input: "text",
    hook: "0–255 and bit i (0–7). AND with 1 << i." },
  { id: "check_odd", name: "Check if a Number is Odd (Bitwise)", category: "Bit Manipulation", emoji: "🎲", complexity: "O(1)", input: "text",
    hook: "0–255. The lowest bit decides parity." },
  { id: "swap_xor", name: "Swap Two Numbers With XOR", category: "Bit Manipulation", emoji: "🔃", complexity: "O(1)", input: "text",
    hook: "Two numbers 0–255. Three XORs, no temp." },
  { id: "divide_bits", name: "Divide Without * or /", category: "Bit Manipulation", emoji: "➗", complexity: "O(log n)", input: "text",
    hook: "Dividend, divisor (0–255). Subtract shifted divisors." },
  { id: "xor_range", name: "XOR of Numbers in a Range", category: "Bit Manipulation", emoji: "⊕", complexity: "O(1)", input: "text",
    hook: "N, or L, R (0–999). f(n) repeats every 4." },
  { id: "single_number_iii", name: "Single Number III (Two Uniques)", category: "Bit Manipulation", emoji: "👯", complexity: "O(n)", input: "text",
    hook: "Pairs plus two singletons. Split by the lowest differing bit." },
  { id: "binary_subarray_sum", name: "Binary Subarrays With Sum", category: "Patterns", emoji: "🪟", complexity: "O(n)", input: "text",
    hook: "0/1 values and the goal. Exactly = at-most(goal) − at-most(goal−1)." },
  { id: "nice_subarrays", name: "Count Number of Nice Subarrays", category: "Patterns", emoji: "🪟", complexity: "O(n)", input: "text",
    hook: "Numbers and k. Count windows with exactly k odd numbers." },
  { id: "substrings_all_three", name: "Substrings Containing All Three Characters", category: "Patterns", emoji: "🪟", complexity: "O(n)", input: "text",
    hook: "Letters a/b/c only. Track where each was last seen." },
  { id: "max_card_points", name: "Maximum Points From Cards", category: "Patterns", emoji: "🪟", complexity: "O(n)", input: "text",
    hook: "Card points and k. Take k from the ends — trade left cards for right ones." },
  { id: "subarrays_k_distinct", name: "Subarrays With K Different Integers", category: "Patterns", emoji: "🪟", complexity: "O(n)", input: "text",
    hook: "Numbers and k. Exactly k distinct = at-most(k) − at-most(k−1)." },
  { id: "min_window_substring", name: "Minimum Window Substring", category: "Patterns", emoji: "🪟", complexity: "O(n)", input: "text",
    hook: "Text (≤ 16) and pattern (≤ 6). Grow to cover, shrink while covered." },
  { id: "min_window_subsequence", name: "Minimum Window Subsequence", category: "Patterns", emoji: "🪟", complexity: "O(n)", input: "text",
    hook: "Text (≤ 16) and pattern (≤ 6). Forward scan, then tighten backward." },
  { id: "word_ladder", name: "Word Ladder I", category: "Graphs", emoji: "🧩", complexity: "O(n)", input: "text",
    hook: "begin,end | dictionary. BFS: one letter changes per level." },
  { id: "word_ladder_ii", name: "Word Ladder II (All Shortest Sequences)", category: "Graphs", emoji: "🧩", complexity: "O(n)", input: "text",
    hook: "begin,end | dictionary. Every shortest sequence is read back from BFS parents." },
  { id: "alien_dictionary", name: "Alien Dictionary", category: "Graphs", emoji: "🧩", complexity: "O(n)", input: "text",
    hook: "Words in alien sorted order. Each adjacent pair gives one letter rule." },
  { id: "cheapest_flight_k", name: "Cheapest Flights Within K Stops", category: "Graphs", emoji: "🧩", complexity: "O(n)", input: "text",
    hook: "Flights a>b:price, then | src dst k. k+1 Bellman-Ford rounds." },
  { id: "ways_to_arrive", name: "Number of Ways to Arrive at Destination", category: "Graphs", emoji: "🧩", complexity: "O(n)", input: "text",
    hook: "Roads a-b:time, then | src dst. Dijkstra that counts ties." },
  { id: "min_multiplications", name: "Minimum Multiplications to Reach End", category: "Graphs", emoji: "🧩", complexity: "O(n)", input: "text",
    hook: "start end | factors. BFS over values mod 100000." },
  { id: "most_stones", name: "Most Stones Removed With Same Row or Column", category: "Graphs", emoji: "🧩", complexity: "O(n)", input: "text",
    hook: "Stones as r:c. Same row or column = connected; answer = stones − groups." },
  { id: "network_delay", name: "Network Delay Time", category: "Graphs", emoji: "📡", complexity: "O(n)", input: "graph",
    hook: "Dijkstra from the source on one-way links; the delay is when the farthest node hears the" },
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
  { id: "coin_change",  name: "Coin Change (Fewest Coins)", category: "DP", emoji: "🪙", complexity: "O(coins·amount)", input: "number",
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
];

// Short face label per algorithm. Lives here because both the 3D keycaps
// and the flat mobile grid render it — keeping one copy stops them drifting.
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

// The full Striver A2Z sheet lives in its own module — 18 steps, and long
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

export const CLIPS = [
  { tag: "TODAY", topic: "Graphs",   title: "Why GPS uses Dijkstra's, not BFS" },
  { tag: "TODAY", topic: "Arrays",   title: "Kadane's Algorithm: The Hidden Pattern" },
  { tag: "TODAY", topic: "Trees",    title: "Why BSTs beat Hash Maps for ranges" },
  { tag: "TODAY", topic: "DP",       title: "Memoization vs Tabulation — when each wins" },
  { tag: "TODAY", topic: "Sorting",  title: "Tim Sort: Python's secret weapon" },
  { tag: "TODAY", topic: "Strings",  title: "KMP: Pattern matching without backtracking" },
];

export const REALWORLD = [
  { icon: "🗺️", metaphor: "Graphs",  title: "Google Maps",      desc: "Dijkstra's algorithm finds the shortest driving route in real time." },
  { icon: "🔗", metaphor: "DP",      title: "DNA Sequencing",   desc: "Edit distance (Levenshtein) powers genome alignment in bioinformatics." },
  { icon: "🛒", metaphor: "Hashing", title: "E-Commerce Cart",  desc: "Hash maps power O(1) product lookup for millions of SKUs." },
  { icon: "📱", metaphor: "BFS",     title: "Social Networks",  desc: "Facebook's friend-of-a-friend discovery uses breadth-first search." },
  { icon: "🧬", metaphor: "Trees",   title: "File Systems",     desc: "Every OS filesystem is a tree — directories are just nodes." },
  { icon: "⚙️", metaphor: "Heaps",  title: "OS Schedulers",    desc: "Priority queues decide which process gets CPU time next." },
];
