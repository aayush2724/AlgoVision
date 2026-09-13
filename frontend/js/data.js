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
export const ALGO_CATEGORIES = ["All", "Graphs", "Sorting", "Searching", "Patterns", "Structures", "DP"];

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
  { id: "trie_insert",  name: "Trie — Prefix Tree",         category: "Structures", emoji: "🔤", complexity: "O(word length)", input: "text",
    hook: "How autocomplete stores a dictionary without repeating prefixes." },
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
