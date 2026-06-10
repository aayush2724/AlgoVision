export const NAV = [
  { label: "Home", hash: "#/" },
  { label: "Explore", hash: "#/explore" },
  { label: "Experience", hash: "#/experience" },
  { label: "Family", hash: "#/family" },
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
      { id:"3-7",  title:"Move Zeros to End",              difficulty:"E", viz:"particles",   world:"Centrifuge Separation",   hook:"Heavy particles (zeros) drift to the edge." },
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
      { id:"3-21", title:"Next Permutation",               difficulty:"M", viz:"clock",       world:"Combination Lock",        hook:"Click the lock one step forward." },
      { id:"3-22", title:"Leaders in an Array",            difficulty:"E", viz:"skyline",     world:"City Skyline",            hook:"Only the tallest buildings on the right are leaders." },
      { id:"3-23", title:"Longest Consecutive Sequence",   difficulty:"M", viz:"calendar",    world:"Gym Streak Calendar",     hook:"What is your longest unbroken check-in run?" },
      { id:"3-24", title:"Set Matrix Zeros",               difficulty:"M", viz:"grid",        world:"Contamination Spread",    hook:"One infected cell silences its entire row and column." },
      { id:"3-25", title:"Rotate Matrix 90°",              difficulty:"M", viz:"camera",      world:"Photo Rotation",          hook:"Rotate the image. The pixels rearrange themselves." },
      { id:"3-26", title:"Spiral Matrix",                  difficulty:"M", viz:"spiral",      world:"Crop Circle Survey",      hook:"Walk the field in an ever-tightening spiral." },
      { id:"3-27", title:"Pascal's Triangle",              difficulty:"E", viz:"triangle",    world:"Stadium Crowd Wave",      hook:"Each row is built from the two above it." },
      { id:"3-28", title:"Majority Element (>n/3)",        difficulty:"M", viz:"election",    world:"Coalition Government",    hook:"At most two parties can dominate." },
      { id:"3-29", title:"3Sum",                           difficulty:"M", viz:"market",      world:"Three-Item Deal",         hook:"Three prices. One exact total. Find all combos." },
      { id:"3-30", title:"4Sum",                           difficulty:"H", viz:"market",      world:"Four-Item Bundle",        hook:"The bundle deal with four exact items." },
      { id:"3-31", title:"Largest Subarray with 0 Sum",   difficulty:"M", viz:"balance",     world:"Financial Balance Sheet", hook:"Find the longest stretch that nets to zero." },
      { id:"3-32", title:"Count Subarrays with XOR=K",    difficulty:"H", viz:"mirror",      world:"Encryption Key Search",   hook:"How many segments encode the same secret?" },
      { id:"3-33", title:"Merge Overlapping Intervals",    difficulty:"M", viz:"timeline",    world:"Meeting Scheduler",       hook:"Merge all overlapping calendar blocks." },
      { id:"3-34", title:"Merge Two Sorted Arrays",        difficulty:"M", viz:"mergesort",   world:"Merging Flight Manifests",hook:"Two sorted passenger lists, combined in one pass." },
      { id:"3-35", title:"Find Repeating and Missing",     difficulty:"H", viz:"seats",       world:"Duplicate Boarding Pass", hook:"One passenger boarded twice, one never got a seat." },
      { id:"3-36", title:"Count Inversions",               difficulty:"H", viz:"bubbles",     world:"Disorder Meter",          hook:"How far is this queue from perfectly sorted?" },
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
      { id:"4-9",  title:"Search in Rotated Array II",      difficulty:"M", viz:"carousel",   world:"Duplicate Seats",         hook:"Some seats look identical. Search harder." },
      { id:"4-10", title:"Find Minimum in Rotated Array",   difficulty:"M", viz:"mountain",   world:"Valley in Rotated Terrain",hook:"The lowest point after the mountain spun." },
      { id:"4-11", title:"Find Minimum in Rotated II",      difficulty:"H", viz:"mountain",   world:"Foggy Valley Hunt",       hook:"Duplicates cloud your vision. Push through." },
      { id:"4-12", title:"Single Element in Sorted Array",  difficulty:"M", viz:"mirror",     world:"Odd Locker Out",          hook:"Every locker has a twin. Except one." },
      { id:"4-13", title:"Find Peak Element",               difficulty:"M", viz:"mountain",   world:"Mountain Peak Hike",      hook:"Climb until you can't go higher." },
      { id:"4-14", title:"Sqrt of N",                       difficulty:"E", viz:"construction",world:"Construction Grid",      hook:"How many tiles fit in a square of area N?" },
      { id:"4-15", title:"Nth Root of M",                   difficulty:"M", viz:"construction",world:"Nested Cube Packing",    hook:"How many smaller cubes fit inside the big one?" },
      { id:"4-16", title:"Koko Eating Bananas",             difficulty:"M", viz:"conveyor",   world:"Factory Output Rate",     hook:"What's the minimum speed to finish in time?" },
      { id:"4-17", title:"Minimum Days to Make Bouquets",   difficulty:"M", viz:"garden",     world:"Flower Delivery",         hook:"How long until enough blooms for the order?" },
      { id:"4-18", title:"Find Smallest Divisor",           difficulty:"M", viz:"postal",     world:"Cargo Packing",           hook:"Smallest divider that keeps total under the limit." },
      { id:"4-19", title:"Capacity to Ship in D Days",      difficulty:"M", viz:"shipping",   world:"Shipping Container",      hook:"Minimum capacity to deliver all packages in time." },
      { id:"4-20", title:"Kth Missing Positive Number",     difficulty:"E", viz:"seats",      world:"Missing Ticket Numbers",  hook:"Which ticket numbers were never printed?" },
      { id:"4-21", title:"Aggressive Cows",                 difficulty:"H", viz:"field",      world:"Cattle Farm Spacing",     hook:"Place cows as far apart as possible." },
      { id:"4-22", title:"Book Allocation Problem",         difficulty:"H", viz:"shipping",   world:"Textbook Distribution",   hook:"Divide books so the heaviest load is minimised." },
      { id:"4-23", title:"Split Array Largest Sum",         difficulty:"H", viz:"shipping",   world:"Pipeline Load Balancing", hook:"Split the pipeline so no segment overloads." },
      { id:"4-24", title:"Painter's Partition",             difficulty:"H", viz:"field",      world:"Mural Painting Crew",     hook:"Assign wall sections so no painter works too long." },
      { id:"4-25", title:"Median of Two Sorted Arrays",     difficulty:"H", viz:"balance",    world:"Median Salary Finder",    hook:"The middle ground between two payroll lists." },
      { id:"4-26", title:"Kth Element of Two Arrays",       difficulty:"H", viz:"balance",    world:"Combined Rankings",       hook:"Find rank K in the merged leaderboard." },
      { id:"4-27", title:"Row with Max 1s",                 difficulty:"M", viz:"grid",       world:"Survey Heatmap",          hook:"Which row has the most positive responses?" },
      { id:"4-28", title:"Search in 2D Matrix",             difficulty:"M", viz:"grid",       world:"Spreadsheet Search",      hook:"The value hides somewhere in the grid." },
      { id:"4-29", title:"Search in 2D Matrix II",          difficulty:"M", viz:"grid",       world:"Satellite Grid Scan",     hook:"Rows and columns are both sorted. Think smart." },
      { id:"4-30", title:"Find Peak Element II (2D)",       difficulty:"H", viz:"mountain",   world:"Terrain Peak Scanner",    hook:"In a 2D landscape, find any local maximum." },
    ]
  },

  {
    step: "Step 5", title: "Strings", progress: 20,
    problems: [
      { id:"5-1",  title:"Reverse Words in String",         difficulty:"E", viz:"dna",        world:"DNA Reversal",            hook:"Flip the sequence. The meaning survives." },
      { id:"5-2",  title:"Longest Palindrome Substring",    difficulty:"M", viz:"mirror",     world:"Mirror Word",             hook:"The word that reads the same forwards and back." },
      { id:"5-3",  title:"Roman to Integer",                difficulty:"E", viz:"clock",      world:"Sundial Reading",         hook:"Ancient notation, modern conversion." },
      { id:"5-4",  title:"String to Integer (atoi)",        difficulty:"M", viz:"terminal",   world:"Number Parser",           hook:"Raw text becomes a number. Handle the edge cases." },
      { id:"5-5",  title:"Longest Common Prefix",           difficulty:"E", viz:"dna",        world:"Gene Prefix Alignment",   hook:"The shared start of every sequence." },
      { id:"5-6",  title:"Count & Say",                     difficulty:"M", viz:"dna",        world:"Spoken DNA",              hook:"Describe what you see. Then describe that." },
      { id:"5-7",  title:"Compare Version Numbers",         difficulty:"M", viz:"clock",      world:"Software Versioning",     hook:"Is 1.10 greater than 1.9? You decide." },
      { id:"5-8",  title:"Anagram Check",                   difficulty:"E", viz:"shuffle",    world:"Anagram Puzzle",          hook:"Same letters, different arrangement." },
      { id:"5-9",  title:"Sort Characters by Frequency",    difficulty:"M", viz:"votes",      world:"Character Popularity",    hook:"Most-used letter leads the parade." },
      { id:"5-10", title:"Maximum Nesting Depth Parentheses",difficulty:"M", viz:"building",  world:"Building Floors",         hook:"How deep do the brackets go?" },
      { id:"5-11", title:"Isomorphic Strings",              difficulty:"E", viz:"mirror",     world:"Code Translation",        hook:"Every character maps to exactly one other." },
      { id:"5-12", title:"Rotate String",                   difficulty:"E", viz:"carousel",   world:"Drum Kit Rotation",       hook:"Is one string just a rotation of another?" },
      { id:"5-13", title:"Valid Anagram",                   difficulty:"E", viz:"shuffle",    world:"Scrambled Message",       hook:"Unscramble and compare." },
      { id:"5-14", title:"Implement strStr (KMP)",          difficulty:"H", viz:"searchbeam", world:"Genome Sequencer",        hook:"Find the pattern inside the text. No backtracking." },
      { id:"5-15", title:"Repeated String Match",           difficulty:"M", viz:"conveyor",   world:"Looped Tape",             hook:"How many times must the tape loop to contain the pattern?" },
    ]
  },

  {
    step: "Step 6", title: "Linked List", progress: 0,
    problems: [
      { id:"6-1",  title:"Linked List Intro & Traversal",   difficulty:"E", viz:"train",      world:"Train Carriages",         hook:"Each carriage knows only the next one." },
      { id:"6-2",  title:"Insertion at Head/Tail/Position", difficulty:"E", viz:"train",      world:"Adding a Carriage",       hook:"Hook a new carriage onto the train." },
      { id:"6-3",  title:"Deletion at Head/Tail/Position",  difficulty:"E", viz:"train",      world:"Detaching a Carriage",    hook:"Uncouple and reconnect around the gap." },
      { id:"6-4",  title:"Find Length",                     difficulty:"E", viz:"train",      world:"Counting Carriages",      hook:"Walk the train from engine to caboose." },
      { id:"6-5",  title:"Reverse a Linked List",           difficulty:"E", viz:"train",      world:"Train Reversal",          hook:"The engine becomes the caboose." },
      { id:"6-6",  title:"Find Middle of Linked List",      difficulty:"E", viz:"train",      world:"Midpoint of a Journey",   hook:"Fast and slow pointer. One reaches the end first." },
      { id:"6-7",  title:"Detect Loop (Floyd's)",           difficulty:"M", viz:"circuit",    world:"Circular Track Detector", hook:"Slow and fast runners. If they meet, it's a loop." },
      { id:"6-8",  title:"Find Start of Loop",              difficulty:"M", viz:"circuit",    world:"Loop Entry Point",        hook:"Where does the circular track begin?" },
      { id:"6-9",  title:"Remove Nth Node from End",        difficulty:"M", viz:"train",      world:"Remove From Rear",        hook:"Two pointers, N apart. Delete what follows." },
      { id:"6-10", title:"Delete Middle Node",              difficulty:"M", viz:"train",      world:"Surgery on a Chain",      hook:"Remove the middle link without counting first." },
      { id:"6-11", title:"Sort Linked List",                difficulty:"M", viz:"train",      world:"Sorting Train Cars",      hook:"Merge Sort on a chain. No random access." },
      { id:"6-12", title:"Odd-Even Linked List",            difficulty:"M", viz:"train",      world:"Odd-Even Carriage Split", hook:"Odd-indexed first, even-indexed after." },
      { id:"6-13", title:"Remove Duplicates (Sorted LL)",   difficulty:"E", viz:"train",      world:"Duplicate Carriage Removal",hook:"Every ID should appear only once." },
      { id:"6-14", title:"Merge Two Sorted Lists",          difficulty:"E", viz:"mergesort",  world:"Merging Two Train Routes",hook:"Two sorted timetables merged into one." },
      { id:"6-15", title:"Merge K Sorted Lists",            difficulty:"H", viz:"mergesort",  world:"K-Way Rail Merge",        hook:"Combine K lines into one master route." },
      { id:"6-16", title:"Reverse in Groups of K",          difficulty:"H", viz:"train",      world:"K-Block Reversal",        hook:"Flip every K carriages as a group." },
      { id:"6-17", title:"Rotate Linked List by K",         difficulty:"M", viz:"carousel",   world:"Rotating Train Ring",     hook:"Shift the chain K steps forward." },
      { id:"6-18", title:"Flatten a Multilevel LL",         difficulty:"H", viz:"building",   world:"Building Directory",      hook:"Flatten the nested floors into one corridor." },
      { id:"6-19", title:"Clone List with Random Pointers", difficulty:"H", viz:"dna",        world:"DNA Replication",         hook:"Copy every node including its random link." },
      { id:"6-20", title:"Add Two Numbers (LL)",            difficulty:"M", viz:"calculator", world:"Column Addition",         hook:"Add two numbers stored backwards in linked lists." },
    ]
  },

  {
    step: "Step 7", title: "Recursion", progress: 0,
    problems: [
      { id:"7-1",  title:"Factorial",                       difficulty:"E", viz:"fractal",    world:"Fractal Branching",       hook:"N roads split into N-1. Then N-2. All the way down." },
      { id:"7-2",  title:"Fibonacci",                       difficulty:"E", viz:"fractal",    world:"Rabbit Population",       hook:"Each generation is the sum of the last two." },
      { id:"7-3",  title:"Power Function (Fast Expo)",      difficulty:"M", viz:"racetrack",  world:"Compound Interest",       hook:"Square the result, halve the steps." },
      { id:"7-4",  title:"Print 1 to N / N to 1",          difficulty:"E", viz:"conveyor",   world:"Countdown Clock",         hook:"Stack the calls. Unwind on return." },
      { id:"7-5",  title:"Sum of First N Numbers",          difficulty:"E", viz:"triangle",   world:"Staircase Sum",           hook:"Each step adds one more." },
      { id:"7-6",  title:"Reverse a String (Recursion)",    difficulty:"E", viz:"mirror",     world:"Echo Chamber",            hook:"The last character answers first." },
      { id:"7-7",  title:"Palindrome Check (Recursion)",    difficulty:"E", viz:"mirror",     world:"Mirror Maze",             hook:"Is the entry the same as the exit?" },
      { id:"7-8",  title:"Sum of Digits",                   difficulty:"E", viz:"calculator", world:"Digital Root",            hook:"Reduce until one digit remains." },
      { id:"7-9",  title:"All Subsets of a String",         difficulty:"M", viz:"fractal",    world:"Power Set of Ingredients",hook:"Every possible combination of toppings." },
      { id:"7-10", title:"All Permutations of a String",    difficulty:"M", viz:"shuffle",    world:"Seating Arrangements",    hook:"Every possible seating order at the table." },
      { id:"7-11", title:"Phone Keypad Combinations",       difficulty:"M", viz:"keypad",     world:"Phone Keypad",            hook:"2 maps to ABC. What words can you spell?" },
      { id:"7-12", title:"N-Queens",                        difficulty:"H", viz:"chess",      world:"Chess Queen Placement",   hook:"Place N queens so none can attack another." },
      { id:"7-13", title:"Sudoku Solver",                   difficulty:"H", viz:"grid",       world:"Sudoku Board",            hook:"Fill the grid. If stuck, backtrack." },
      { id:"7-14", title:"Word Search",                     difficulty:"M", viz:"grid",       world:"Crossword Hunt",          hook:"Trace the word through the letter grid." },
      { id:"7-15", title:"Rat in a Maze",                   difficulty:"M", viz:"maze",       world:"Maze Navigation",         hook:"Explore every path. Retreat when stuck." },
      { id:"7-16", title:"Combination Sum I",               difficulty:"M", viz:"market",     world:"Change Machine",          hook:"Which coins sum to the target?" },
      { id:"7-17", title:"Combination Sum II",              difficulty:"M", viz:"market",     world:"Exact Change",            hook:"No coin used twice. Hit the exact total." },
      { id:"7-18", title:"Subset Sum",                      difficulty:"M", viz:"balance",    world:"Budget Allocation",       hook:"Does any subset of expenses hit the budget?" },
      { id:"7-19", title:"Palindrome Partitioning",         difficulty:"H", viz:"mirror",     world:"Mirror Cuts",             hook:"Split the string so every piece is a palindrome." },
      { id:"7-20", title:"K-th Permutation Sequence",       difficulty:"H", viz:"clock",      world:"Combination Lock Position",hook:"Go directly to the K-th setting." },
    ]
  },

  {
    step: "Step 8", title: "Bit Manipulation", progress: 0,
    problems: [
      { id:"8-1",  title:"Check if Bit is Set",             difficulty:"E", viz:"switch",     world:"Circuit Switch",          hook:"Is this particular wire live?" },
      { id:"8-2",  title:"Set / Unset / Toggle a Bit",      difficulty:"E", viz:"switch",     world:"Light Panel",             hook:"Flip exactly one switch. Leave the rest." },
      { id:"8-3",  title:"Check Power of 2",                difficulty:"E", viz:"mirror",     world:"Binary Balance",          hook:"A power of 2 has exactly one lit bit." },
      { id:"8-4",  title:"Count Set Bits (Kernighan's)",    difficulty:"E", viz:"switch",     world:"Active Circuit Count",    hook:"How many wires carry current?" },
      { id:"8-5",  title:"XOR of 1 to N",                   difficulty:"M", viz:"mirror",     world:"XOR Pattern Discovery",   hook:"The pattern repeats every 4 numbers." },
      { id:"8-6",  title:"Find Two Non-Repeating Numbers",  difficulty:"H", viz:"mirror",     world:"Two Unique Agents",       hook:"Two agents with no doubles. XOR reveals them." },
      { id:"8-7",  title:"Minimum Bit Flips",               difficulty:"M", viz:"switch",     world:"Network Packet Correction",hook:"Fewest bit changes to match the target." },
      { id:"8-8",  title:"Single Number III",               difficulty:"H", viz:"mirror",     world:"Spy Pair Isolation",      hook:"Two spies in a crowd of pairs. Find them both." },
    ]
  },

  {
    step: "Step 9", title: "Stacks & Queues", progress: 0,
    problems: [
      { id:"9-1",  title:"Implement Stack using Arrays",    difficulty:"E", viz:"stack",      world:"Plate Stack",             hook:"Last plate in is the first plate out." },
      { id:"9-2",  title:"Implement Queue using Arrays",    difficulty:"E", viz:"queue",      world:"Ticket Queue",            hook:"First in, first served." },
      { id:"9-3",  title:"Implement Stack using Queue",     difficulty:"M", viz:"queue",      world:"Reverse Queue Trick",     hook:"Build LIFO behaviour from FIFO parts." },
      { id:"9-4",  title:"Implement Queue using Stack",     difficulty:"M", viz:"stack",      world:"Double-Reverse Trick",    hook:"Two stacks make a queue." },
      { id:"9-5",  title:"Valid Parentheses",               difficulty:"E", viz:"building",   world:"Architecture Blueprint",  hook:"Every open bracket must find its close." },
      { id:"9-6",  title:"Min Stack",                       difficulty:"M", viz:"stack",      world:"Price Tracker",           hook:"Track the running minimum alongside every push." },
      { id:"9-7",  title:"Next Greater Element I",          difficulty:"M", viz:"skyline",    world:"Skyline View",            hook:"Looking right — what's the next taller building?" },
      { id:"9-8",  title:"Next Greater Element II (Circular)",difficulty:"M",viz:"carousel",  world:"Circular Skyline",        hook:"The skyline wraps around. Look again." },
      { id:"9-9",  title:"Daily Temperatures",              difficulty:"M", viz:"stockchart", world:"Weather Forecast",        hook:"How many days until a warmer day arrives?" },
      { id:"9-10", title:"Largest Rectangle in Histogram",  difficulty:"H", viz:"skyline",    world:"Billboard Space",         hook:"Largest sign that fits under the skyline." },
      { id:"9-11", title:"Maximal Rectangle",               difficulty:"H", viz:"grid",       world:"Urban Development Plot",  hook:"Largest rectangular building site in the city grid." },
      { id:"9-12", title:"Trapping Rain Water",             difficulty:"H", viz:"canyon",     world:"Canyon Rainfall",         hook:"The valley holds the water. How much?" },
      { id:"9-13", title:"Sliding Window Maximum",          difficulty:"H", viz:"windowslide",world:"Moving Sensor Window",    hook:"Track the peak reading as the sensor slides." },
      { id:"9-14", title:"LRU Cache",                       difficulty:"H", viz:"cache",      world:"Browser Cache",           hook:"Limited memory. Evict the least recently used page." },
      { id:"9-15", title:"LFU Cache",                       difficulty:"H", viz:"cache",      world:"Streaming Cache",         hook:"Evict the least frequently accessed content." },
    ]
  },

  {
    step: "Step 10", title: "Sliding Window & Two Pointers", progress: 0,
    problems: [
      { id:"10-1", title:"Longest Substring Without Repeat", difficulty:"M", viz:"windowslide",world:"No-Repeat Radio Window",  hook:"Slide the window until a song repeats." },
      { id:"10-2", title:"Max Sum Subarray of Size K",       difficulty:"E", viz:"windowslide",world:"K-Day Revenue Window",    hook:"Which K-day stretch earned the most?" },
      { id:"10-3", title:"Fruits into Baskets",              difficulty:"M", viz:"windowslide",world:"Two-Basket Harvest",      hook:"Carry only 2 fruit types. Maximum harvest?" },
      { id:"10-4", title:"Minimum Window Substring",         difficulty:"H", viz:"windowslide",world:"Minimum Coverage Area",   hook:"Smallest window that contains all required items." },
      { id:"10-5", title:"Longest Repeating Character Replace",difficulty:"M",viz:"windowslide",world:"Cable Re-Coating",      hook:"Fewest replacements to make K identical wires." },
      { id:"10-6", title:"Binary Subarrays with Sum K",      difficulty:"M", viz:"balance",    world:"Binary Signal Matching",  hook:"How many segments sum to exactly K?" },
      { id:"10-7", title:"Count Nice Subarrays",             difficulty:"M", viz:"powerline",  world:"Odd Power Spikes",        hook:"Count windows with exactly K power spikes." },
      { id:"10-8", title:"3Sum Closest",                     difficulty:"M", viz:"market",     world:"Three-Item Budget",       hook:"Three prices closest to target, not over." },
      { id:"10-9", title:"Container With Most Water",        difficulty:"M", viz:"canyon",     world:"Water Tank Design",       hook:"Two walls. Maximize the volume between them." },
      { id:"10-10",title:"Trapping Rain Water (2-pointer)",  difficulty:"H", viz:"canyon",     world:"Dam Engineering",         hook:"Left and right walls meet in the middle." },
    ]
  },

  {
    step: "Step 11", title: "Heaps", progress: 0,
    problems: [
      { id:"11-1", title:"Heap Introduction & Operations",   difficulty:"E", viz:"heap",       world:"Hospital Triage",         hook:"Sickest patient always treated first." },
      { id:"11-2", title:"Kth Largest Element",             difficulty:"M", viz:"heap",       world:"Top-K Leaderboard",       hook:"Maintain a running top-K without sorting all." },
      { id:"11-3", title:"Kth Smallest Element",            difficulty:"M", viz:"heap",       world:"Bottom-K Price Finder",   hook:"Find the K cheapest items in the market." },
      { id:"11-4", title:"Sort a K-Sorted Array",           difficulty:"M", viz:"heap",       world:"Nearly Sorted Conveyor",  hook:"Items almost in order. Small heap sorts them." },
      { id:"11-5", title:"K Closest Points to Origin",      difficulty:"M", viz:"radar",      world:"Radar Proximity Scan",    hook:"Which K blips are closest to the centre?" },
      { id:"11-6", title:"Top K Frequent Elements",         difficulty:"M", viz:"votes",      world:"Trending Hashtags",       hook:"The K most-used tags in the last hour." },
      { id:"11-7", title:"Find Median from Data Stream",    difficulty:"H", viz:"balance",    world:"Live Median Salary Tracker",hook:"Two heaps hold the left and right halves." },
      { id:"11-8", title:"Merge K Sorted Arrays",           difficulty:"H", viz:"mergesort",  world:"K-Way Postal Merge",      hook:"Pull the smallest item from K sorted piles." },
    ]
  },

  {
    step: "Step 12", title: "Greedy Algorithms", progress: 0,
    problems: [
      { id:"12-1", title:"N Meetings in One Room",           difficulty:"M", viz:"timeline",   world:"Conference Room Scheduler",hook:"Maximum meetings without overlap." },
      { id:"12-2", title:"Minimum Platforms",               difficulty:"M", viz:"timeline",   world:"Train Station Platforms", hook:"How many platforms to avoid collisions?" },
      { id:"12-3", title:"Job Sequencing with Deadlines",    difficulty:"M", viz:"calendar",   world:"Deadline-Driven Schedule",hook:"Max profit when every job has a deadline." },
      { id:"12-4", title:"Fractional Knapsack",             difficulty:"M", viz:"shipping",   world:"Cargo Loading",           hook:"Fill the container by value density." },
      { id:"12-5", title:"Minimum Coins",                   difficulty:"M", viz:"market",     world:"ATM Coin Dispenser",      hook:"Fewest coins to make exact change." },
      { id:"12-6", title:"Jump Game I",                     difficulty:"M", viz:"racetrack",  world:"Frog Leaping",            hook:"Can the frog reach the finish?" },
      { id:"12-7", title:"Jump Game II",                    difficulty:"M", viz:"racetrack",  world:"Minimum Jumps",           hook:"Fewest leaps to cross the pond." },
      { id:"12-8", title:"Assign Cookies",                  difficulty:"E", viz:"field",      world:"Cookie Distribution",     hook:"Satisfy the most children with limited cookies." },
      { id:"12-9", title:"Candy Problem",                   difficulty:"H", viz:"conveyor",   world:"Rating-Based Candy",      hook:"Higher-rated child always gets more than neighbours." },
      { id:"12-10",title:"Insert Interval",                 difficulty:"M", viz:"timeline",   world:"Calendar Merge",          hook:"Slot the new meeting. Merge any overlaps." },
      { id:"12-11",title:"Non-overlapping Intervals",       difficulty:"M", viz:"timeline",   world:"Conflict Resolution",     hook:"Remove fewest meetings to clear all conflicts." },
    ]
  },

  {
    step: "Step 13", title: "Trees", progress: 0,
    problems: [
      { id:"13-1", title:"Tree Traversals (Pre/In/Post)",   difficulty:"E", viz:"tree",       world:"Family Tree Walk",        hook:"Visit every relative in order." },
      { id:"13-2", title:"Level Order Traversal",           difficulty:"E", viz:"tree",       world:"Organisation Chart",      hook:"Read the company floor by floor." },
      { id:"13-3", title:"Height of Binary Tree",           difficulty:"E", viz:"building",   world:"Tallest Tower",           hook:"Count the floors from root to deepest leaf." },
      { id:"13-4", title:"Diameter of Binary Tree",         difficulty:"M", viz:"tree",       world:"Longest Road in a City",  hook:"Longest path between any two endpoints." },
      { id:"13-5", title:"Check Balanced Tree",             difficulty:"M", viz:"balance",    world:"Structural Integrity Check",hook:"No branch too much heavier than another." },
      { id:"13-6", title:"Lowest Common Ancestor",          difficulty:"M", viz:"tree",       world:"Corporate Reporting Line",hook:"Who is the closest shared manager?" },
      { id:"13-7", title:"Symmetric Tree",                  difficulty:"E", viz:"mirror",     world:"Mirror Architecture",     hook:"Does the tree reflect perfectly?" },
      { id:"13-8", title:"Path Sum I & II",                 difficulty:"M", viz:"tree",       world:"Budget Path",             hook:"Is there a root-to-leaf route totalling the target?" },
      { id:"13-9", title:"Binary Tree from Inorder+Preorder",difficulty:"H",viz:"tree",       world:"Reconstruct a Pedigree",  hook:"Rebuild the family tree from two visit lists." },
      { id:"13-10",title:"Serialize & Deserialize Tree",    difficulty:"H", viz:"dna",        world:"DNA Encoding",            hook:"Compress the tree to a string. Rebuild it exactly." },
      { id:"13-11",title:"Flatten Tree to Linked List",     difficulty:"M", viz:"train",      world:"Flatten a Circuit",       hook:"Unroll the tree into a straight line." },
      { id:"13-12",title:"Maximum Path Sum",                difficulty:"H", viz:"tree",       world:"Highest Revenue Route",   hook:"The most profitable path through the organisation." },
      { id:"13-13",title:"Zigzag Level Order",              difficulty:"M", viz:"tree",       world:"Zigzag Floor Walk",       hook:"Alternate left-to-right and right-to-left per floor." },
      { id:"13-14",title:"Boundary Traversal",              difficulty:"M", viz:"building",   world:"Building Perimeter Walk", hook:"Walk the outer edge of the structure." },
      { id:"13-15",title:"Vertical Order Traversal",        difficulty:"H", viz:"building",   world:"Column-By-Column Survey", hook:"Read the building column by column." },
      { id:"13-16",title:"Top View of Binary Tree",         difficulty:"M", viz:"building",   world:"Aerial City View",        hook:"What columns are visible from directly above?" },
      { id:"13-17",title:"Bottom View of Binary Tree",      difficulty:"M", viz:"building",   world:"Underground View",        hook:"What's visible from directly below?" },
      { id:"13-18",title:"Right Side View",                 difficulty:"M", viz:"building",   world:"Right Elevation",         hook:"Stand to the right. What can you see?" },
      { id:"13-19",title:"Left Side View",                  difficulty:"M", viz:"building",   world:"Left Elevation",         hook:"Stand to the left. One node per floor." },
      { id:"13-20",title:"Check Identical Trees",           difficulty:"E", viz:"mirror",     world:"Blueprint Comparison",    hook:"Are these two architectural plans identical?" },
      { id:"13-21",title:"BST: Search & Insert",            difficulty:"E", viz:"library",    world:"Binary Bookshelf",        hook:"Every left book is smaller. Every right is bigger." },
      { id:"13-22",title:"BST: Delete a Node",              difficulty:"M", viz:"library",    world:"Library Deaccession",     hook:"Remove a book and keep the shelf sorted." },
      { id:"13-23",title:"Kth Smallest in BST",             difficulty:"M", viz:"library",    world:"Kth Cheapest Book",       hook:"In-order walk. Stop at the Kth book." },
      { id:"13-24",title:"Validate BST",                    difficulty:"M", viz:"library",    world:"Shelf Integrity Audit",   hook:"Is every book truly in the right section?" },
    ]
  },

  {
    step: "Step 14", title: "Graphs", progress: 0,
    problems: [
      { id:"14-1", title:"BFS Traversal",                   difficulty:"E", viz:"social",     world:"Social Network Spread",   hook:"Influence ripples level by level." },
      { id:"14-2", title:"DFS Traversal",                   difficulty:"E", viz:"maze",       world:"Maze Exploration",        hook:"Go deep. Backtrack when stuck." },
      { id:"14-3", title:"Detect Cycle (Undirected, BFS)",  difficulty:"M", viz:"circuit",    world:"Circular Road Network",   hook:"Does any road loop back on itself?" },
      { id:"14-4", title:"Detect Cycle (Directed, DFS)",    difficulty:"M", viz:"circuit",    world:"Dependency Loop",         hook:"Does any task depend on itself?" },
      { id:"14-5", title:"Topological Sort (DFS)",          difficulty:"M", viz:"building",   world:"Construction Schedule",   hook:"Foundation before walls. Walls before roof." },
      { id:"14-6", title:"Topological Sort (Kahn's BFS)",   difficulty:"M", viz:"conveyor",   world:"Assembly Line Order",     hook:"Process tasks by dependency order." },
      { id:"14-7", title:"Number of Islands",               difficulty:"M", viz:"radar",      world:"Satellite Island Survey", hook:"Count distinct landmasses from above." },
      { id:"14-8", title:"Flood Fill",                      difficulty:"E", viz:"grid",       world:"Paint Bucket Tool",       hook:"Colour spreads to all connected neighbours." },
      { id:"14-9", title:"Rotten Oranges",                  difficulty:"M", viz:"grid",       world:"Contamination Spread",    hook:"Infection radiates outward. Minimum time?" },
      { id:"14-10",title:"Distance of Nearest Cell (0)",   difficulty:"M", viz:"radar",      world:"Nearest Emergency Exit",  hook:"BFS from all sources simultaneously." },
      { id:"14-11",title:"Bipartite Graph Check",           difficulty:"M", viz:"social",     world:"Two-Team Allocation",     hook:"Can this network be split into two rival groups?" },
      { id:"14-12",title:"Strongly Connected Components",   difficulty:"H", viz:"social",     world:"Mutual Follow Groups",    hook:"Who can reach everyone else in their cluster?" },
      { id:"14-13",title:"Dijkstra's Algorithm",            difficulty:"M", viz:"gps",        world:"GPS Navigation",          hook:"Find the cheapest route through a weighted city." },
      { id:"14-14",title:"Bellman-Ford Algorithm",          difficulty:"M", viz:"gps",        world:"Currency Arbitrage Check",hook:"Negative cycles mean infinite profit — detect them." },
      { id:"14-15",title:"Floyd-Warshall Algorithm",        difficulty:"H", viz:"gps",        world:"All-Pairs Distance Matrix",hook:"Every city's distance to every other city." },
      { id:"14-16",title:"Minimum Spanning Tree (Prim's)",  difficulty:"M", viz:"field",      world:"Cheapest Power Grid",     hook:"Connect all cities with the minimum cable." },
      { id:"14-17",title:"Minimum Spanning Tree (Kruskal's)",difficulty:"M",viz:"field",      world:"Railway Network Build",   hook:"Add the cheapest edge that doesn't form a cycle." },
      { id:"14-18",title:"Bridges in a Graph",              difficulty:"H", viz:"circuit",    world:"Critical Infrastructure", hook:"Which road, if removed, disconnects the network?" },
      { id:"14-19",title:"Articulation Points",             difficulty:"H", viz:"circuit",    world:"Single Point of Failure", hook:"Which router, if removed, splits the internet?" },
      { id:"14-20",title:"Word Ladder",                     difficulty:"H", viz:"dna",        world:"Genetic Mutation Path",   hook:"Mutate one gene at a time from source to target." },
    ]
  },

  {
    step: "Step 15", title: "Dynamic Programming", progress: 0,
    problems: [
      { id:"15-1", title:"Fibonacci (DP)",                  difficulty:"E", viz:"fractal",    world:"Compound Growth",         hook:"Cache the result. Never compute twice." },
      { id:"15-2", title:"Climbing Stairs",                 difficulty:"E", viz:"building",   world:"Staircase Paths",         hook:"1 or 2 steps. How many ways to the top?" },
      { id:"15-3", title:"Frog Jump",                       difficulty:"E", viz:"racetrack",  world:"Frog River Crossing",     hook:"Minimum energy to hop across all stones." },
      { id:"15-4", title:"House Robber I",                  difficulty:"M", viz:"conveyor",   world:"Non-Adjacent Heist",      hook:"Rob houses. Never hit two in a row." },
      { id:"15-5", title:"House Robber II (Circular)",      difficulty:"M", viz:"carousel",   world:"Circular Block Heist",    hook:"The street loops. First and last are neighbours." },
      { id:"15-6", title:"Longest Increasing Subsequence",  difficulty:"M", viz:"stockchart", world:"Market Growth Streak",    hook:"Longest unbroken rising trend in prices." },
      { id:"15-7", title:"Longest Common Subsequence",      difficulty:"M", viz:"dna",        world:"DNA Alignment",           hook:"Longest shared sequence between two genomes." },
      { id:"15-8", title:"Edit Distance",                   difficulty:"H", viz:"dna",        world:"Spell Correction",        hook:"Minimum edits to transform one word to another." },
      { id:"15-9", title:"0/1 Knapsack",                    difficulty:"M", viz:"shipping",   world:"Cargo Value Optimiser",   hook:"Maximize cargo value within weight limit." },
      { id:"15-10",title:"Unbounded Knapsack",              difficulty:"M", viz:"shipping",   world:"Unlimited Item Packing",  hook:"Each item can be used any number of times." },
      { id:"15-11",title:"Coin Change (Minimum Coins)",     difficulty:"M", viz:"market",     world:"ATM Minimum Dispense",    hook:"Fewest coins. Unlimited denominations." },
      { id:"15-12",title:"Coin Change II (Count Ways)",     difficulty:"M", viz:"market",     world:"Number of Payment Methods",hook:"How many ways to make exact change?" },
      { id:"15-13",title:"Partition Equal Subset Sum",      difficulty:"M", viz:"balance",    world:"Fair Cargo Split",        hook:"Can the load be divided perfectly in two?" },
      { id:"15-14",title:"Matrix Chain Multiplication",     difficulty:"H", viz:"grid",       world:"Optimal Pipeline Batching",hook:"Which order of operations minimises cost?" },
      { id:"15-15",title:"Burst Balloons",                  difficulty:"H", viz:"particles",  world:"Mining Sequence",         hook:"Pop in the right order to maximise coins." },
      { id:"15-16",title:"Word Break",                      difficulty:"M", viz:"dna",        world:"Sentence Segmentation",   hook:"Can the string be split into valid words?" },
      { id:"15-17",title:"Palindrome Partitioning II",      difficulty:"H", viz:"mirror",     world:"Minimum Mirror Cuts",     hook:"Fewest cuts to make every piece a palindrome." },
      { id:"15-18",title:"Maximum Profit in Job Scheduling",difficulty:"H", viz:"timeline",   world:"Freelancer Schedule",     hook:"Non-overlapping jobs with maximum total pay." },
      { id:"15-19",title:"Distinct Subsequences",           difficulty:"H", viz:"dna",        world:"Gene Pattern Count",      hook:"How many ways does T appear as a subsequence of S?" },
      { id:"15-20",title:"Regular Expression Matching",     difficulty:"H", viz:"dna",        world:"Pattern Matcher",         hook:"Does the genome match this regex pattern?" },
    ]
  },

  {
    step: "Step 16", title: "Tries", progress: 0,
    problems: [
      { id:"16-1", title:"Implement Trie",                  difficulty:"M", viz:"tree",       world:"Autocomplete Engine",     hook:"Every prefix is a path in the tree." },
      { id:"16-2", title:"Implement Trie II",               difficulty:"M", viz:"tree",       world:"Search Suggestions",      hook:"Count prefixes and complete words." },
      { id:"16-3", title:"Longest Word with All Prefixes",  difficulty:"M", viz:"tree",       world:"Progressive Password",    hook:"Every prefix of the word must also be valid." },
      { id:"16-4", title:"Number of Distinct Substrings",   difficulty:"H", viz:"dna",        world:"Genetic Variant Count",   hook:"How many unique substrings does the genome contain?" },
      { id:"16-5", title:"Maximum XOR of Two Numbers",      difficulty:"H", viz:"mirror",     world:"Maximum Contrast Pair",   hook:"Binary Trie reveals the most different pair." },
    ]
  },

  {
    step: "Step 17", title: "Bit Manipulation Advance", progress: 0,
    problems: [
      { id:"17-1", title:"Divide Without Division Operator",difficulty:"M", viz:"switch",     world:"Bit-Shift Division",      hook:"Shift right = divide by 2. Repeat." },
      { id:"17-2", title:"Reverse Bits",                   difficulty:"E", viz:"mirror",     world:"Bit Mirror",              hook:"Flip the binary number left to right." },
      { id:"17-3", title:"Number of 1 Bits (Hamming Weight)",difficulty:"E",viz:"switch",    world:"Network Packet Parity",   hook:"Count the active bits in the signal." },
      { id:"17-4", title:"Counting Bits",                  difficulty:"E", viz:"switch",     world:"Binary Counter Array",    hook:"Bit counts for 0 through N." },
      { id:"17-5", title:"Missing Number (XOR)",           difficulty:"E", viz:"seats",      world:"Missing Ticket",          hook:"XOR cancels pairs. The odd one out survives." },
      { id:"17-6", title:"Sum of Two Integers (No +)",     difficulty:"M", viz:"switch",     world:"Circuit Adder",           hook:"XOR for sum. AND+shift for carry." },
    ]
  },

  {
    step: "Step 18", title: "Strings Advance", progress: 0,
    problems: [
      { id:"18-1", title:"KMP Algorithm",                  difficulty:"H", viz:"searchbeam", world:"Genome Pattern Search",   hook:"Never backtrack. The failure function saves you." },
      { id:"18-2", title:"Z-Algorithm",                    difficulty:"H", viz:"searchbeam", world:"Radar Pattern Match",     hook:"Z-array tells you match lengths at every position." },
      { id:"18-3", title:"Rabin-Karp Algorithm",           difficulty:"H", viz:"searchbeam", world:"Rolling Hash Search",     hook:"A hash that slides across the text." },
      { id:"18-4", title:"Minimum Window Substring",       difficulty:"H", viz:"windowslide",world:"Emergency Supply Window",  hook:"Smallest window covering all required items." },
      { id:"18-5", title:"Smallest Window with All Chars", difficulty:"H", viz:"windowslide",world:"Minimal Coverage Scan",   hook:"Contract until nothing can be removed." },
    ]
  }

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
    { id: 'MG',    label: 'MG Road',           x: 200, y: 150 },
    { id: 'KORAM', label: 'Koramangala',        x: 350, y: 220 },
    { id: 'INDIR', label: 'Indiranagar',        x: 400, y: 80  },
    { id: 'WHFLD', label: 'Whitefield',         x: 600, y: 100 },
    { id: 'HSR',   label: 'HSR Layout',         x: 480, y: 240 },
    { id: 'ELCTY', label: 'Electronic City',    x: 550, y: 280 },
  ],
  links: [
    { source: 'MG',    target: 'KORAM', weight: 8  },
    { source: 'MG',    target: 'INDIR', weight: 5  },
    { source: 'INDIR', target: 'WHFLD', weight: 12 },
    { source: 'KORAM', target: 'HSR',   weight: 6  },
    { source: 'KORAM', target: 'INDIR', weight: 7  },
    { source: 'HSR',   target: 'ELCTY', weight: 9  },
    { source: 'WHFLD', target: 'HSR',   weight: 15 },
    { source: 'INDIR', target: 'HSR',   weight: 10 },
  ]
};
