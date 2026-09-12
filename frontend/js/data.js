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
];

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

export const A2Z_STEPS = [
  {
    step: "Step 1", title: "Learn the Basics", progress: 100,
    problems: [
      { id:"1-1",  title:"User Input / Output",             difficulty:"E", viz:"terminal",    world:"ATM Machine",             hook:"Every program starts with a conversation." },
      { id:"1-2",  title:"Data Types",                      difficulty:"E", viz:"warehouse",   world:"Warehouse Shelves",        hook:"Every shelf holds a different kind of cargo." },
      { id:"1-3",  title:"If-Else / Switch Statements",     difficulty:"E", viz:"traffic",     world:"Traffic Signal",           hook:"Rules decide who moves and who waits." },
      { id:"1-4",  title:"Arrays",                          difficulty:"E", viz:"array",       world:"Train Carriages",          hook:"A line of boxes, each with an address." },
      { id:"1-5",  title:"Strings",                         difficulty:"E", viz:"dna",         world:"DNA Strand",               hook:"Characters chained together like genetic code." },
      { id:"1-6",  title:"For Loops",                       difficulty:"E", viz:"conveyor",    world:"Factory Conveyor Belt",    hook:"The machine that never gets tired." },
      { id:"1-7",  title:"While Loops",                     difficulty:"E", viz:"watchman",    world:"Security Guard",           hook:"Keep checking until the condition is met." },
      { id:"1-8",  title:"Functions (Pass by Value/Ref)",   difficulty:"E", viz:"courier",     world:"Courier Service",          hook:"Send a copy, or send the real thing?" },
      { id:"1-9",  title:"Time Complexity",                 difficulty:"M", viz:"racetrack",   world:"Formula 1 Race",           hook:"How fast does your code cross the finish line?" },
      { id:"1-10", title:"Space Complexity",                difficulty:"M", viz:"warehouse",   world:"RAM as Warehouse",         hook:"How much floor space does your solution rent?" },
    ]
  },
  {
    step: "Step 2", title: "Sorting Techniques", progress: 80,
    problems: [
      { id:"2-1",  title:"Selection Sort",    difficulty:"E", viz:"leaderboard", world:"Leaderboard Selection",  hook:"Find the champion, move them to the top. Repeat." },
      { id:"2-2",  title:"Bubble Sort",       difficulty:"E", viz:"bubbles",     world:"Bubble Tea Queue",       hook:"Heavy bubbles sink; light ones rise." },
      { id:"2-3",  title:"Insertion Sort",    difficulty:"E", viz:"cards",       world:"Sorting Playing Cards",  hook:"Pick a card, slide it into the right slot." },
      { id:"2-4",  title:"Merge Sort",        difficulty:"M", viz:"mergesort",   world:"Merging Sorted Piles",   hook:"Divide the chaos. Merge into order." },
      { id:"2-5",  title:"Quick Sort",        difficulty:"M", viz:"quicksort",   world:"Partition a Crowd",      hook:"Pick a pivot. The crowd splits around you." },
      { id:"2-6",  title:"Counting Sort",     difficulty:"E", viz:"votes",       world:"Election Vote Count",    hook:"Tally marks never lie." },
      { id:"2-7",  title:"Radix Sort",        difficulty:"M", viz:"postal",      world:"Postal Sorting Office",  hook:"Sort by zip code digit by digit." },
    ]
  },
  {
    step: "Step 3", title: "Arrays", progress: 60,
    problems: [
      { id:"3-1",  title:"Largest Element",                difficulty:"E", viz:"podium",      world:"Olympic Podium",          hook:"Who stands tallest on the stage?" },
      { id:"3-2",  title:"Second Largest Element",         difficulty:"E", viz:"podium",      world:"Silver Medal Hunt",       hook:"The runner-up is harder to find than you think." },
      { id:"3-3",  title:"Check if Array is Sorted",       difficulty:"E", viz:"conveyor",    world:"Quality Control Belt",    hook:"Is every package in the right order?" },
      { id:"3-4",  title:"Remove Duplicates (Sorted)",     difficulty:"E", viz:"dedup",       world:"Guest List Cleanup",      hook:"One invite per guest. Cross the rest out." },
      { id:"3-5",  title:"Left Rotate Array by One",       difficulty:"E", viz:"carousel",    world:"Carousel Ride",           hook:"The first rider moves to the back of the line." },
      { id:"3-6",  title:"Left Rotate Array by D",         difficulty:"M", viz:"carousel",    world:"Ferris Wheel Rotation",   hook:"Spin the wheel D slots. Who's at the top?" },
      { id:"3-7",  title:"Move Zeros to End",              difficulty:"E", viz:"particles",   world:"Centrifuge Separation",   hook:"Heavy particles drift to the edge." },
      { id:"3-8",  title:"Linear Search",                  difficulty:"E", viz:"searchbeam",  world:"Flashlight in the Dark",  hook:"Check every corner until you find it." },
      { id:"3-9",  title:"Union of Two Arrays",            difficulty:"M", viz:"venn",        world:"Venn Diagram Merge",      hook:"Two crowds become one, no duplicates." },
      { id:"3-10", title:"Intersection of Two Arrays",     difficulty:"M", viz:"venn",        world:"Common Friends",          hook:"Who do we both know?" },
      { id:"3-11", title:"Find Missing Number",            difficulty:"E", viz:"seats",       world:"Empty Theatre Seat",      hook:"One seat is empty. Which number is it?" },
      { id:"3-12", title:"Max Consecutive Ones",           difficulty:"E", viz:"powerline",   world:"Power Grid Uptime",       hook:"Longest uninterrupted stretch of power." },
      { id:"3-13", title:"Single Number (XOR)",            difficulty:"E", viz:"mirror",      world:"Spy Mirror Trick",        hook:"Everything cancels out. The odd one survives." },
      { id:"3-14", title:"Longest Subarray with Sum K",    difficulty:"M", viz:"windowslide", world:"Budget Window Shopping",  hook:"Find the shopping stretch that exactly hits budget." },
      { id:"3-15", title:"Two Sum",                        difficulty:"E", viz:"market",      world:"Supermarket Pairing",     hook:"Find two items that together hit the target price." },
      { id:"3-16", title:"Sort 0s 1s 2s (Dutch Flag)",    difficulty:"M", viz:"flag",        world:"Dutch National Flag",     hook:"Three colours. One pass. No extra space." },
      { id:"3-17", title:"Majority Element (>n/2)",        difficulty:"M", viz:"election",    world:"Majority Vote",           hook:"The candidate who dominates always reveals themselves." },
      { id:"3-18", title:"Maximum Subarray (Kadane's)",    difficulty:"M", viz:"stockchart",  world:"Best Stock Run",          hook:"Find the best winning streak in the market." },
      { id:"3-19", title:"Best Time to Buy & Sell Stock",  difficulty:"E", viz:"stockchart",  world:"Stock Trader",            hook:"Buy low. Sell high. One transaction." },
      { id:"3-20", title:"Rearrange by Sign",              difficulty:"M", viz:"teams",       world:"Team Alternation",        hook:"Positive and negative players, perfectly alternated." },
    ]
  },
  {
    step: "Step 4", title: "Binary Search", progress: 40,
    problems: [
      { id:"4-1",  title:"Binary Search on 1D Array",       difficulty:"E", viz:"library",    world:"Library Catalog",         hook:"Halve the search space every time." },
      { id:"4-2",  title:"Implement Lower Bound",           difficulty:"E", viz:"library",    world:"Bookshelf First Fit",     hook:"The first shelf where this book could live." },
      { id:"4-3",  title:"Implement Upper Bound",           difficulty:"E", viz:"library",    world:"Last Possible Slot",      hook:"The last place this book could possibly go." },
      { id:"4-4",  title:"Search Insert Position",          difficulty:"E", viz:"library",    world:"Insert Into Filing Cabinet",hook:"Where would this file naturally belong?" },
      { id:"4-5",  title:"Floor & Ceil of a Number",        difficulty:"E", viz:"elevator",   world:"Elevator Floor",          hook:"Which floor do you land on? And which is just above?" },
      { id:"4-6",  title:"First & Last Occurrence",         difficulty:"M", viz:"library",    world:"Archive Search",          hook:"When did this event first and last appear?" },
      { id:"4-7",  title:"Count Occurrences",               difficulty:"E", viz:"votes",      world:"Vote Counter",            hook:"How many ballots carry this name?" },
      { id:"4-8",  title:"Search in Rotated Array",         difficulty:"M", viz:"array",      world:"Rotated Carousel",        hook:"The ride spun. Find your seat anyway." },
      { id:"4-9",  title:"Find Minimum in Rotated Array",   difficulty:"M", viz:"mountain",   world:"Valley in Rotated Terrain",hook:"The lowest point after the mountain spun." },
      { id:"4-10", title:"Single Element in Sorted Array",  difficulty:"M", viz:"mirror",     world:"Odd Locker Out",          hook:"Every locker has a twin. Except one." },
      { id:"4-11", title:"Find Peak Element",               difficulty:"M", viz:"mountain",   world:"Mountain Peak Hike",      hook:"Climb until you can't go higher." },
      { id:"4-12", title:"Koko Eating Bananas",             difficulty:"M", viz:"conveyor",   world:"Factory Output Rate",     hook:"What's the minimum speed to finish in time?" },
      { id:"4-13", title:"Capacity to Ship in D Days",      difficulty:"M", viz:"shipping",   world:"Shipping Container",      hook:"Minimum capacity to deliver all packages in time." },
      { id:"4-14", title:"Median of Two Sorted Arrays",     difficulty:"H", viz:"balance",    world:"Median Salary Finder",    hook:"The middle ground between two payroll lists." },
    ]
  },
  {
    step: "Step 5", title: "Strings", progress: 20,
    problems: [
      { id:"5-1",  title:"Reverse Words in String",          difficulty:"E", viz:"dna",        world:"DNA Reversal",            hook:"Flip the sequence. The meaning survives." },
      { id:"5-2",  title:"Longest Palindrome Substring",     difficulty:"M", viz:"mirror",     world:"Mirror Word",             hook:"The word that reads the same forwards and back." },
      { id:"5-3",  title:"Roman to Integer",                 difficulty:"E", viz:"clock",      world:"Sundial Reading",         hook:"Ancient notation, modern conversion." },
      { id:"5-4",  title:"String to Integer (atoi)",         difficulty:"M", viz:"terminal",   world:"Number Parser",           hook:"Raw text becomes a number. Handle the edge cases." },
      { id:"5-5",  title:"Longest Common Prefix",            difficulty:"E", viz:"dna",        world:"Gene Prefix Alignment",   hook:"The shared start of every sequence." },
      { id:"5-6",  title:"Anagram Check",                    difficulty:"E", viz:"shuffle",    world:"Anagram Puzzle",          hook:"Same letters, different arrangement." },
      { id:"5-7",  title:"Isomorphic Strings",               difficulty:"E", viz:"mirror",     world:"Code Translation",        hook:"Every character maps to exactly one other." },
      { id:"5-8",  title:"Implement strStr (KMP)",           difficulty:"H", viz:"searchbeam", world:"Genome Sequencer",        hook:"Find the pattern inside the text. No backtracking." },
    ]
  },
  {
    step: "Step 6", title: "Linked List", progress: 0,
    problems: [
      { id:"6-1",  title:"Linked List Intro & Traversal",   difficulty:"E", viz:"train",      world:"Train Carriages",         hook:"Each carriage knows only the next one." },
      { id:"6-2",  title:"Insertion at Head/Tail/Position", difficulty:"E", viz:"train",      world:"Adding a Carriage",       hook:"Hook a new carriage onto the train." },
      { id:"6-3",  title:"Deletion at Head/Tail/Position",  difficulty:"E", viz:"train",      world:"Detaching a Carriage",    hook:"Uncouple and reconnect around the gap." },
      { id:"6-4",  title:"Reverse a Linked List",           difficulty:"E", viz:"train",      world:"Train Reversal",          hook:"The engine becomes the caboose." },
      { id:"6-5",  title:"Find Middle of Linked List",      difficulty:"E", viz:"train",      world:"Midpoint of a Journey",   hook:"Fast and slow pointer. One reaches the end first." },
      { id:"6-6",  title:"Detect Loop (Floyd's)",           difficulty:"M", viz:"circuit",    world:"Circular Track Detector", hook:"Slow and fast runners. If they meet, it's a loop." },
      { id:"6-7",  title:"Merge Two Sorted Lists",          difficulty:"E", viz:"mergesort",  world:"Merging Two Train Routes",hook:"Two sorted timetables merged into one." },
      { id:"6-8",  title:"Merge K Sorted Lists",            difficulty:"H", viz:"mergesort",  world:"K-Way Rail Merge",        hook:"Combine K lines into one master route." },
    ]
  },
  {
    step: "Step 7", title: "Recursion", progress: 0,
    problems: [
      { id:"7-1",  title:"Factorial",                       difficulty:"E", viz:"fractal",    world:"Fractal Branching",       hook:"N roads split into N-1. Then N-2. All the way down." },
      { id:"7-2",  title:"Fibonacci",                       difficulty:"E", viz:"fractal",    world:"Rabbit Population",       hook:"Each generation is the sum of the last two." },
      { id:"7-3",  title:"Power Function (Fast Expo)",      difficulty:"M", viz:"racetrack",  world:"Compound Interest",       hook:"Square the result, halve the steps." },
      { id:"7-4",  title:"All Subsets of a String",         difficulty:"M", viz:"fractal",    world:"Power Set of Ingredients",hook:"Every possible combination of toppings." },
      { id:"7-5",  title:"All Permutations of a String",    difficulty:"M", viz:"shuffle",    world:"Seating Arrangements",    hook:"Every possible seating order at the table." },
    ]
  },
];

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
