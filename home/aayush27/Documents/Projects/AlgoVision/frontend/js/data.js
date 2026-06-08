// Static content that powers the cinematic story sections.

export const NAV = [
  { route: "/", label: "Home" },
  { route: "/explore", label: "Explore" },
  { route: "/experience", label: "Experience" },
  { route: "/a2z", label: "A2Z Journey" },
  { route: "/today", label: "Today" },
  { route: "/practice", label: "Practice" },
  { route: "/journey", label: "My Journey" },
  { route: "/realworld", label: "Real-World" },
];

export const ACTS = [
  {
    tag: "Act I · The Hook",
    title: "You already live inside an algorithm.",
    body: "Every time your phone reroutes you around traffic, a shortest-path search just ran in milliseconds. We start with the world you know — not the code.",
  },
  {
    tag: "Act II · The Reveal",
    title: "The hidden machine behind the magic.",
    body: "Watch the map dissolve into a graph of nodes and edges. The same structure quietly powers maps, social networks, and the internet itself.",
  },
  {
    tag: "Act III · The Mechanics",
    title: "Now you are ready for the code.",
    body: "Only once the intuition lands do we open the engine. Step through the algorithm line by line and watch each decision light up.",
  },
];

export const WORLDS = [
  {
    key: "sorting",
    icon: "🏆",
    name: "The Leaderboard",
    topic: "Sorting",
    line: "Ranking players from chaos to order, one comparison at a time.",
    complexity: "O(n log n)",
  },
  {
    key: "binary-search",
    icon: "🎯",
    name: "The Hunt",
    topic: "Binary Search",
    line: "Halving the search space until only the answer remains.",
    complexity: "O(log n)",
  },
  {
    key: "graphs",
    icon: "🌐",
    name: "Six Degrees",
    topic: "Graphs",
    line: "From friend suggestions to GPS routing — the world is a graph.",
    complexity: "O(V + E)",
  },
  {
    key: "dp",
    icon: "🧩",
    name: "The Memo Vault",
    topic: "Dynamic Programming",
    line: "Never solve the same subproblem twice. Remember, then conquer.",
    complexity: "Varies",
  },
  {
    key: "recursion",
    icon: "🪞",
    name: "The Fractal Mirror",
    topic: "Recursion",
    line: "A problem that contains smaller copies of itself, all the way down.",
    complexity: "Varies",
  },
  {
    key: "trees",
    icon: "🌳",
    name: "The Family Tree",
    topic: "Trees",
    line: "Hierarchies that branch — file systems, org charts, decisions.",
    complexity: "O(log n)",
  },
  {
    key: "heap",
    icon: "🎲",
    name: "The Priority Queue",
    topic: "Heap",
    line: "Always knowing what matters most, without checking everything.",
    complexity: "O(log n)",
  },
  {
    key: "sliding-window",
    icon: "🪟",
    name: "The Window",
    topic: "Sliding Window",
    line: "A moving frame that captures patterns in streaming data.",
    complexity: "O(n)",
  },
  {
    key: "two-pointers",
    icon: "👉",
    name: "The Meeting Point",
    topic: "Two Pointers",
    line: "Two seekers converging from opposite ends of possibility.",
    complexity: "O(n)",
  },
];

export const WORLDS_CATEGORIES = [
  { key: "all", label: "All" },
  { key: "foundations", label: "Foundations" },
  { key: "structures", label: "Structures" },
  { key: "mastery", label: "Mastery" },
];

export const CATEGORY_MAP = {
  sorting: "foundations",
  "binary-search": "foundations",
  graphs: "structures",
  dp: "mastery",
  recursion: "foundations",
  trees: "structures",
  heap: "structures",
  "sliding-window": "foundations",
  "two-pointers": "foundations",
};

export const FEATURES = [
  {
    icon: "✶",
    name: "Explain this step",
    line: "Ask the AI what any single step really means, tuned to your level.",
  },
  {
    icon: "🐞",
    name: "AI Bug Finder",
    line: "Paste your attempt and get a focused hint instead of the full answer.",
  },
  {
    icon: "🌍",
    name: "Real-world hooks",
    line: "Every concept opens with where it actually lives in the world.",
  },
  {
    icon: "💬",
    name: "Ask AlgoVision",
    line: "A tutor that knows the exact graph and step you are looking at.",
  },
];

export const A2Z_STEPS = [
  { step: 1, name: "Basics of Programming", problems: 25, focus: "flow, loops, patterns" },
  { step: 2, name: "Maths for DSA", problems: 30, focus: "number theory, combinatorics" },
  { step: 3, name: "Arrays & Strings", problems: 45, focus: "fundamentals" },
  { step: 4, name: "Sorting & Searching", problems: 35, focus: "divide & conquer" },
  { step: 5, name: "Bit Manipulation", problems: 20, focus: "bitwise wizardry" },
  { step: 6, name: "Two Pointers", problems: 25, focus: "efficiency patterns" },
  { step: 7, name: "Sliding Window", problems: 20, focus: "streaming windows" },
  { step: 8, name: "Stacks & Queues", problems: 30, focus: "LIFO/FIFO" },
  { step: 9, name: "Linked Lists", problems: 35, focus: "pointers & links" },
  { step: 10, name: "Binary Trees", problems: 40, focus: "tree traversal" },
  { step: 11, name: "Binary Search Trees", problems: 25, focus: "ordered trees" },
  { step: 12, name: "Greedy Algorithms", problems: 40, focus: "local optima" },
  { step: 13, name: "Recursion & Backtracking", problems: 45, focus: "recursive depth" },
  { step: 14, name: "Dynamic Programming", problems: 55, focus: "memoization" },
  { step: 15, name: "Graphs: BFS & DFS", problems: 40, focus: "graph traversal" },
  { step: 16, name: "Shortest Path", problems: 30, focus: "Dijkstra, Bellman-Ford" },
  { step: 17, name: "Topological Sort", problems: 25, focus: "DAG ordering" },
  { step: 18, name: "A2Z Mastery", problems: 44, focus: "mixed practice" },
];

export const CLIPS = [
  { tag: "Sorting", title: "Why quicksort loves randomness", topic: "Sorting", accent: "blue" },
  { tag: "Graphs", title: "GPS in 60 seconds: Dijkstra demystified", topic: "Graphs", accent: "violet" },
  { tag: "DP", title: "The Memo Vault: caching without tears", topic: "Dynamic Programming", accent: "cyan" },
  { tag: "Trees", title: "Binary trees are just branches in time", topic: "Trees", accent: "blue" },
  { tag: "BFS", title: "Social networks run on shortest paths", topic: "BFS", accent: "purple" },
  { tag: "Recursion", title: "Fractals are recursion you can see", topic: "Recursion", accent: "cyan" },
];

export const REALWORLD = [
  { algorithm: "Dijkstra", real: "GPS Navigation", icon: "🗺️", desc: "Finding the fastest route between two points." },
  { algorithm: "BFS", real: "Social Networks", icon: "👥", desc: "Finding friends-of-friends and shortest connections." },
  { algorithm: "Huffman", real: "File Compression", icon: "🗜️", desc: "Compressing data by frequency-based encoding." },
  { algorithm: "DP", real: "DNA Alignment", icon: "🧬", desc: "Comparing genetic sequences for evolutionary distance." },
  { algorithm: "A*", real: "Game AI", icon: "🎮", desc: "Intelligent pathfinding for NPCs and bots." },
  { algorithm: "PageRank", real: "Search Rankings", icon: "🔍", desc: "Ranking web pages by link authority and relevance." },
];

export const STATS = [
  { label: "Problems Solved", value: 127 },
  { label: "Streak", value: 12 },
  { label: "Worlds Unlocked", value: 4 },
  { label: "Concepts Mastered", value: 23 },
];

export const JOURNEY_TRACK = [
  { topic: "Sorting", mastered: 18, total: 25 },
  { topic: "Graphs", mastered: 12, total: 30 },
  { topic: "Trees", mastered: 8, total: 20 },
  { topic: "DP", mastered: 5, total: 45 },
  { topic: "Recursion", mastered: 14, total: 20 },
];

export const SAMPLE_GRAPH = {
  nodes: [
    { id: "A", x: 90, y: 200 },
    { id: "B", x: 250, y: 90 },
    { id: "C", x: 250, y: 310 },
    { id: "D", x: 430, y: 150 },
    { id: "E", x: 430, y: 320 },
    { id: "F", x: 600, y: 220 },
  ],
  edges: [
    ["A", "B", 4],
    ["A", "C", 2],
    ["B", "C", 1],
    ["B", "D", 5],
    ["C", "D", 8],
    ["C", "E", 10],
    ["D", "E", 2],
    ["D", "F", 6],
    ["E", "F", 3],
  ],
};

export const BUGGY_BINARY_SEARCH = `function binarySearch(arr, target) {
  let left = 0;
  let right = arr.length;
  while (left <= right) {
    let mid = Math.floor((left + right) / 2);
    if (arr[mid] === target) return mid;
    if (arr[mid] < target) right = mid;
    else left = mid + 1;
  }
  return -1;
}`;

export const BUG_FINDER_TIPS = [
  "Check boundary conditions carefully",
  "Verify your mid calculation",
  "Trace through with a small example",
];