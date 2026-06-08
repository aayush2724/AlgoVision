export const NAV = [
  { label: "Home", hash: "#/" },
  { label: "Explore", hash: "#/explore" },
  { label: "Experience", hash: "#/experience" },
  { label: "A2Z Journey", hash: "#/a2z" },
  { label: "Today", hash: "#/today" },
  { label: "Practice", hash: "#/practice" },
  { label: "My Journey", hash: "#/journey" },
  { label: "Real-World", hash: "#/realworld" }
];

export const HERO = {
  title: "See the Algorithm. Master the Story.",
  lead: "We turn complex data structures into cinematic visual journeys. No more dry slides — just pure intuition.",
  primaryCTA: "Start Exploring",
  ghostCTA: "View Roadmap"
};

export const MARQUEE = [
  "Dynamic Programming", "Graph Theory", "Binary Search", "Recursion", "Trees", "Sorting", "Greedy", "Backtracking", "Bit Manipulation"
];

export const ACTS = [
  { title: "Act I: The Hook", desc: "Every algorithm starts with a problem worth solving. We set the stage with real-world metaphors.", icon: "🎯" },
  { title: "Act II: The Reveal", desc: "Watch the mechanics unfold in real-time. Cinematic animations reveal the 'why' behind the 'how'.", icon: "✨" },
  { title: "Act III: Mechanics", desc: "Deep dive into the logic with interactive traces and AI-powered step-by-step breakdowns.", icon: "⚙️" }
];

export const CATEGORIES = ["All", "Foundations", "Structures", "Mastery"];

export const WORLDS = [
  { name: "The Leaderboard", metaphor: "Sorting", category: "Foundations", emoji: "📊", hook: "Organize the chaos, one swap at a time.", complexity: "O(n log n)" },
  { name: "The Hunt", metaphor: "Binary Search", category: "Foundations", emoji: "🔍", hook: "Divide, conquer, and find the needle in the haystack.", complexity: "O(log n)" },
  { name: "Six Degrees", metaphor: "Graphs", category: "Structures", emoji: "🌐", hook: "Navigate the web of connections that define our world.", complexity: "O(V + E)" },
  { name: "The Memo Vault", metaphor: "DP", category: "Mastery", emoji: "💾", hook: "Remember the past to conquer the future.", complexity: "O(n*m)" },
  { name: "The Priority Queue", metaphor: "Heaps", category: "Structures", emoji: "👑", hook: "Always keep the most important things on top.", complexity: "O(log n)" },
  { name: "The Branching Tree", metaphor: "Recursion", category: "Foundations", emoji: "🌿", hook: "Solve small to solve big.", complexity: "O(2^n)" },
  { name: "The Labyrinth", metaphor: "Backtracking", category: "Mastery", emoji: "🗺️", hook: "Explore every path, but know when to turn back.", complexity: "O(N!)" },
  { name: "The Hash Map", metaphor: "Hashing", category: "Structures", emoji: "🔑", hook: "Instant access to any secret you store.", complexity: "O(1)" },
  { name: "The Flow", metaphor: "Linked Lists", category: "Structures", emoji: "🔗", hook: "One link at a time, building the chain.", complexity: "O(n)" }
];

export const A2Z_STEPS = [
  { step: "Step 1", title: "Learn the Basics", problems: 32, progress: 100 },
  { step: "Step 2", title: "Sorting Techniques", problems: 7, progress: 80 },
  { step: "Step 3", title: "Arrays", problems: 40, progress: 60 },
  { step: "Step 4", title: "Binary Search", problems: 35, progress: 40 },
  { step: "Step 5", title: "Strings", problems: 25, progress: 20 },
  { step: "Step 6", title: "Linked List", problems: 31, progress: 0 },
  { step: "Step 7", title: "Recursion", problems: 28, progress: 0 },
  { step: "Step 8", title: "Bit Manipulation", problems: 15, progress: 0 },
  { step: "Step 9", title: "Stacks & Queues", problems: 30, progress: 0 },
  { step: "Step 10", title: "Sliding Window & Two Pointers", problems: 20, progress: 0 },
  { step: "Step 11", title: "Heaps", problems: 18, progress: 0 },
  { step: "Step 12", title: "Greedy Algorithms", problems: 22, progress: 0 },
  { step: "Step 13", title: "Trees", problems: 50, progress: 0 },
  { step: "Step 14", title: "Graphs", problems: 45, progress: 0 },
  { step: "Step 15", title: "Dynamic Programming", problems: 55, progress: 0 },
  { step: "Step 16", title: "Tries", problems: 10, progress: 0 },
  { step: "Step 17", title: "Bit Manipulation Advance", problems: 12, progress: 0 },
  { step: "Step 18", title: "Strings Advance", problems: 10, progress: 0 }
];

export const CLIPS = [
  { tag: "Visual", title: "Why Recursion is a Mirror", topic: "Recursion", accent: "var(--blue)" },
  { tag: "Insight", title: "The Magic of XOR", topic: "Bitmasking", accent: "var(--violet)" },
  { tag: "Speed", title: "Binary Search in 60s", topic: "Search", accent: "var(--cyan)" },
  { tag: "Logic", title: "DP: The Memoization Secret", topic: "DP", accent: "var(--purple)" },
  { tag: "Graph", title: "Bridges and Articulation Points", topic: "Graphs", accent: "var(--blue-bright)" },
  { tag: "Math", title: "The Sieve of Eratosthenes", topic: "Number Theory", accent: "var(--gold)" }
];

export const REALWORLD = [
  { title: "GPS & Maps", metaphor: "Dijkstra", desc: "Calculating the shortest path through a city grid.", icon: "📍" },
  { title: "Social Networks", metaphor: "BFS", desc: "Finding 'Friends of Friends' in a massive graph.", icon: "👥" },
  { title: "File Compression", metaphor: "Huffman Coding", desc: "Reducing file size without losing a single bit.", icon: "🗜️" },
  { title: "DNA Alignment", metaphor: "DP", desc: "Matching genetic sequences to find evolutionary links.", icon: "🧬" },
  { title: "Game AI", metaphor: "A*", desc: "Helping NPCs find their way through complex levels.", icon: "🎮" },
  { title: "Search Engines", metaphor: "PageRank", desc: "Deciding which websites are the most important.", icon: "🌐" }
];

export const STATS = [
  { label: "Problems Solved", value: "142", target: 455 },
  { label: "Streak", value: "12 Days", target: 30 },
  { label: "Worlds Unlocked", value: "5/9", target: 9 },
  { label: "Concepts Mastered", value: "24", target: 100 }
];

export const SAMPLE_GRAPH = {
  nodes: [
    { id: 'A', x: 100, y: 150 },
    { id: 'B', x: 300, y: 50 },
    { id: 'C', x: 300, y: 250 },
    { id: 'D', x: 500, y: 50 },
    { id: 'E', x: 500, y: 250 },
    { id: 'F', x: 700, y: 150 }
  ],
  links: [
    { source: 'A', target: 'B', weight: 4 },
    { source: 'A', target: 'C', weight: 2 },
    { source: 'B', target: 'C', weight: 1 },
    { source: 'B', target: 'D', weight: 5 },
    { source: 'C', target: 'E', weight: 8 },
    { source: 'D', target: 'E', weight: 2 },
    { source: 'D', target: 'F', weight: 3 },
    { source: 'E', target: 'F', weight: 1 }
  ]
};
