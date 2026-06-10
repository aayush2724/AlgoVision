export const NAV = [
  { label: "Home",       hash: "#/"          },
  { label: "Explore",    hash: "#/explore"   },
  { label: "Experience", hash: "#/experience"},
  { label: "A2Z",        hash: "#/a2z"       },
  { label: "Practice",   hash: "#/practice"  },
];

export const HERO = {
  title: "See the Algorithm.\nMaster the Story.",
  lead: "We turn complex data structures into cinematic visual journeys — real-world metaphors, live step-by-step traces, and AI-powered explanations.",
  primaryCTA: "Start Exploring",
  ghostCTA: "View A2Z Roadmap"
};

export const MARQUEE = [
  "Dynamic Programming", "Graph Theory", "Binary Search", "Recursion",
  "Trees", "Sorting", "Greedy", "Backtracking", "Bit Manipulation"
];

export const ACTS = [
  { title: "The Hook",     desc: "Every algorithm starts with a real-world problem worth solving. We set the stage with cinematic metaphors.", icon: "01" },
  { title: "The Reveal",   desc: "Watch the mechanics unfold in real-time. Animated graphs reveal the 'why' behind the 'how'.", icon: "02" },
  { title: "The Mechanics",desc: "Deep dive with interactive step traces and AI-powered breakdowns of each decision.", icon: "03" }
];

export const CATEGORIES = ["All", "Foundations", "Structures", "Mastery"];

export const WORLDS = [
  { name: "The Leaderboard",    metaphor: "Sorting",       category: "Foundations", emoji: "📊", hook: "Organize the chaos, one swap at a time.",          complexity: "O(n log n)", algo: "sorting"       },
  { name: "The Hunt",           metaphor: "Binary Search",  category: "Foundations", emoji: "🔍", hook: "Divide, conquer, find the needle in the haystack.", complexity: "O(log n)",   algo: "binary_search" },
  { name: "Six Degrees",        metaphor: "Graphs",         category: "Structures",  emoji: "🌐", hook: "Navigate the web of connections that define us.",   complexity: "O(V + E)",   algo: "bfs"           },
  { name: "The Memo Vault",     metaphor: "DP",             category: "Mastery",     emoji: "💾", hook: "Remember the past to conquer the future.",          complexity: "O(n·m)",     algo: "dynamic_programming" },
  { name: "The Priority Queue", metaphor: "Heaps",          category: "Structures",  emoji: "👑", hook: "Always keep the most important things on top.",     complexity: "O(log n)",   algo: "dijkstra"      },
  { name: "The Branching Tree", metaphor: "Recursion",      category: "Foundations", emoji: "🌿", hook: "Solve small to solve big.",                         complexity: "O(2^n)",     algo: "dfs"           },
  { name: "The Labyrinth",      metaphor: "Backtracking",   category: "Mastery",     emoji: "🗺️", hook: "Explore every path, but know when to turn back.",   complexity: "O(N!)",      algo: "dfs"           },
  { name: "The Hash Map",       metaphor: "Hashing",        category: "Structures",  emoji: "🔑", hook: "Instant lookup to any secret you store.",           complexity: "O(1)",       algo: "binary_search" },
  { name: "The Flow",           metaphor: "Linked Lists",   category: "Structures",  emoji: "🔗", hook: "One link at a time, building the chain.",            complexity: "O(n)",       algo: "bfs"           }
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
      { id:"4-8",  title:"Search in Rotated Array",         difficulty:"M", viz:"carousel",   world:"Rotated Carousel",        hook:"The ride spun. Find your seat anyway." },
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

export const CLIPS = [
  { tag: "TODAY", topic: "Graphs",   title: "Why GPS uses Dijkstra's, not BFS" },
  { tag: "TODAY", topic: "Arrays",   title: "Kadane's Algorithm: The Hidden Pattern" },
  { tag: "TODAY", topic: "Trees",    title: "Why BSTs beat Hash Maps for ranges" },
  { tag: "TODAY", topic: "DP",       title: "Memoization vs Tabulation — when each wins" },
  { tag: "TODAY", topic: "Sorting",  title: "Tim Sort: Python's secret weapon" },
  { tag: "TODAY", topic: "Strings",  title: "KMP: Pattern matching without backtracking" },
];

export const STATS = [
  { label: "Problems Solved",   value: "24",      target: 100 },
  { label: "Algorithms Traced", value: "6",        target: 20  },
  { label: "Streak",            value: "3 days",   target: 30  },
  { label: "Mastery Score",     value: "340 pts",  target: 1000},
];

export const REALWORLD = [
  { icon: "🗺️", metaphor: "Graphs",  title: "Google Maps",      desc: "Dijkstra's algorithm finds the shortest driving route in real time." },
  { icon: "🔗", metaphor: "DP",      title: "DNA Sequencing",   desc: "Edit distance (Levenshtein) powers genome alignment in bioinformatics." },
  { icon: "🛒", metaphor: "Hashing", title: "E-Commerce Cart",  desc: "Hash maps power O(1) product lookup for millions of SKUs." },
  { icon: "📱", metaphor: "BFS",     title: "Social Networks",  desc: "Facebook's friend-of-a-friend discovery uses breadth-first search." },
  { icon: "🧬", metaphor: "Trees",   title: "File Systems",     desc: "Every OS filesystem is a tree — directories are just nodes." },
  { icon: "⚙️", metaphor: "Heaps",  title: "OS Schedulers",    desc: "Priority queues decide which process gets CPU time next." },
];
