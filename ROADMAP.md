# AlgoVision — Phased Build Plan

Mission: make DSA easier to **understand and analyse** for colleges and learners.
Method: metaphor-first (Hook → Reveal → Mechanics), always traceable on the
student's own input, never a canned animation when a real trace is possible.

**Stack (user decision, 2026-09-11): staying on FastAPI + vanilla ES modules.**
The user chose to keep and learn the current stack (Python/FastAPI backend +
ML service, buildless JS frontend, Docker). A PERN migration was considered
and cancelled.

Each phase below is a self-contained prompt. Execute one phase per session/turn,
verify its acceptance criteria, then stop so the phase can be committed before
the next begins.

**Status: Phases 0–5 DONE. Next up: Phase 6 (catalog batch 1).**

---

## Phase 0 — Stabilize (DONE, awaiting commit)

Audit fixes: Docker ML networking, decommissioned Groq model, dead config,
injection-blocklist removal, XSS escapes, offline BFS trace, WebGL disposal,
honest stats, repo junk removal, 17-test backend suite.

---

## Phase 1 — Array tracers: Binary Search + Merge Sort, end to end

**Prompt to execute:**

Add two real backend tracers that operate on a user-supplied array, and wire
them through the existing metaphor layer.

Backend:
- New `app/tracers/binary_search.py` — `trace(array: list[float|int], target)` →
  same step envelope as dijkstra/bfs (`i`, `structures`, `highlight`, `note`),
  with `structures` carrying `{low, high, mid, found}` per step and
  `meta.view = "array"`.
- New `app/tracers/merge_sort.py` — steps carry `{array, comparing, merging,
  sorted_ranges}`; keep total steps bounded (cap array length at 16 for trace
  clarity, validate server-side).
- Extend `/api/trace` request model: `algorithm` may now also be
  `binary_search` / `merge_sort`; add an `array: list` + optional `target`
  field (mutually exclusive with `graph` — validate). Keep `/api/trace/algorithms`
  listing in sync.
- Tests: correctness of both tracers (found/not-found, empty, single element,
  duplicates; merge sort produces sorted output and every step's array is a
  permutation of the input), plus endpoint validation tests.

Frontend:
- `engine.js`: an array-view renderer (SVG boxes with values, highlight
  low/high/mid or comparing/merging per step) chosen by `meta.view`; the
  existing graph view stays untouched for dijkstra/bfs.
- Experience page (`#/experience?algo=binary_search|merge_sort`): an input box
  where the student types their own comma-separated numbers (and target for
  binary search), with validation + a sensible default. RUN traces *their*
  input via the API; offline fallback implements both algorithms locally.
- Metaphor layer: reuse `library` scene (binary search) and `leaderboard`
  (merge sort) narration hooks from `detect.py`'s `REALWORLD_META` so
  narration speaks in catalog/leaderboard language.

Acceptance: all backend tests pass; from the UI I can paste `7,3,9,1` and watch
merge sort trace those exact values step by step, and search a sorted array
for a target with the low/high/mid window visibly narrowing; `node --check`
passes on changed JS.

---

## Phase 2 — Bring your own graph

**Prompt to execute:**

Make the graph algorithms (BFS, Dijkstra) run on a student-built graph instead
of the hardcoded sample.

- Graph editor on the experience page (graph view only): click empty canvas to
  add a node (auto-labelled A, B, C…), click two nodes in sequence to add an
  edge, click an edge weight to edit it (number input), right-click / long-press
  to delete node or edge. Keep it SVG, no new dependencies.
- "Start node" selector (dropdown or click-to-set) instead of hardcoded 'A'.
- Presets menu: the current sample graph, a small tree, a disconnected graph
  (teaches unreachable nodes), and "clear".
- The What-If sliders section adapts to the current edge list.
- Client-side validation mirrors server limits (≤50 nodes, ≤200 edges,
  weights 0–1,000,000) with friendly messages.
- Offline localTrace runs on the user graph (it currently reads
  DATA.SAMPLE_GRAPH directly — refactor to take the graph as an argument).
- State survives RUN/RESET but not navigation (no persistence yet — Phase 4).

Acceptance: build a 6-node graph from scratch in the UI, run both BFS and
Dijkstra on it against the live API, see correct traces; a disconnected node
shows distance `—`/unreached and the narration says so; existing tests still
pass plus new tests only if backend changed (it shouldn't need to).

---

## Phase 3 — The analysis layer (understand → analyse)

**Prompt to execute:**

Add the tools that teach complexity, not just mechanics.

- Live counters beside the trace: comparisons / relaxations / queue-or-heap
  operations, incremented per step from data already present in the step
  stream (extend tracer `note`/`structures` with a `counts` dict server-side
  where needed; bump tests).
- A step-scrubber: slider + prev/next + play (speed control) replacing the
  single STEP button, so students can scrub backward — requires rendering any
  step index idempotently from `steps[i]` rather than incremental class
  toggling. Refactor `nextStep()` into `renderStep(i)`.
- Compare mode on the experience page: run two algorithms on the *same* input
  side by side (BFS vs Dijkstra on the current graph; merge sort vs binary
  search excluded — compare only like-for-like inputs). Show both step counts
  and counters; sync the scrubbers.
- A small "complexity card" per algorithm: Big-O table (best/avg/worst,
  space) plus a one-line plain-language reading of the live counters
  ("your graph: 12 relaxations for 7 nodes — that's the E log V at work").
  Content lives in `data.js`.

Acceptance: on the same graph, compare view shows BFS finishing in fewer
steps than Dijkstra with counters explaining why; scrubbing backward re-renders
any step correctly (no stale highlights); all tests pass.

---

## Phase 4 — Real progress, real Journey

**Prompt to execute:**

Make progress tracking honest and useful for a student working through A2Z.

- localStorage-backed progress store (`js/progress.js`): per-problem status
  (unseen / viewed / completed), per-algorithm trace-run counts, streak days.
  Wrap all reads/writes in try/catch; the site must work with storage blocked.
- A2Z page: per-step progress bars computed from real data; checkmarks on
  completed problems; "mark as understood" button on the problem viewer.
- Journey page: replace the sample stats with real ones from the store; keep
  an empty-state that invites the student to start Step 1. Remove the
  "SAMPLE DATA" label.
- Home hero stats stay content stats (they describe the catalog, not the user).
- Export/import progress as a JSON file download/upload (colleges: students
  can hand in or move machines).

Acceptance: completing a problem updates A2Z and Journey immediately and
survives reload; clearing site data yields the empty state, no errors in
console; `node --check` passes.

---

## Phase 5 — Widen the catalog + narration quality

**Prompt to execute:**

- New tracers: DFS (graph view, with backtrack steps), Quick Sort (array
  view, pivot/partition highlights), and one DP example — Fibonacci with
  memo table (new simple `table` view: cells fill in, cache hits glow).
  Same envelope, full tests, wired into `/api/trace/algorithms`, the
  experience page, detect signatures, and the metaphor layer (`maze`,
  `leaderboard`, `vault` scenes already exist).
- Expose the AI narration level (beginner / intermediate / advanced) as a
  UI toggle on the experience page — the backend already supports it.
- Narration prompt: pass the live counters and current structures into the
  ML `/explain` payload so the model narrates the actual state, not just the
  note string.
- README: rewrite feature list to match reality; add a "For educators"
  section (how to run it for a class, offline mode guarantees).

Acceptance: 7 algorithms traceable live (dijkstra, bfs, dfs, binary_search,
merge_sort, quick_sort, fibonacci_dp); level toggle changes narration tone;
all tests pass.

---

## Phase 6+ — Full catalog coverage (the long arc)

Goal (user directive): cover ALL algorithms and data structures — the full
GfG/A2Z syllabus, LeetCode patterns, and Codeforces/competitive-programming
topics. This lands in tiered batches, each batch a committable phase using
the same recipe: **tracer + view renderer + metaphor entry + detect
signature + tests**, all on the shared step envelope
(`{i, structures, highlight, note}`).

View types unlock topics — build a view once, reuse it for the whole family:
- `array` (done) → sorting family, searching, two pointers, sliding window,
  prefix sums, Kadane's
- `graph` (done) → DFS, topological sort, MST (Prim/Kruskal), A*, flood fill
- `tree` (new) → BST insert/search/delete, traversals, heaps, tries,
  segment trees, Fenwick/BIT, LCA/binary lifting
- `table` (new) → DP family: Fibonacci, knapsack, LCS, edit distance,
  matrix paths, bitmask DP
- `stack/queue` (new) → stack/queue ops, monotonic stack, expression
  evaluation, sliding-window maximum
- `list` (new) → linked lists: reverse, cycle detect (Floyd), merge
- `string` (new) → KMP, Z-function, Rabin-Karp, palindromes, anagrams

Suggested batch order (college-first, then patterns, then CP):
1. **Tier A — college core (GfG/A2Z):** remaining sorts (quick, insertion,
   bubble, selection, counting), DFS, linked lists, stacks/queues, BST,
   heaps, hashing, recursion/backtracking (N-Queens), DP classics
2. **Tier B — LeetCode patterns:** two pointers, sliding window, prefix
   sums, intervals, monotonic stack, tries, union-find (DSU)
3. **Tier C — Codeforces/CP:** segment tree, Fenwick tree, DSU with
   rank/path compression, LCA/binary lifting, KMP/Z, sieve + number
   theory, bitmask DP, max-flow intro

The A2Z catalog in `data.js` grows alongside: every problem entry should
eventually point at a real tracer, not a looping animation.

## Later (unscheduled ideas — do not build yet)

- Accounts / teacher dashboards (needs a database — deliberate decision point)
- Pseudocode panel with per-step line highlighting (`line` field already exists)
- Quiz mode: "predict the next step" before revealing it
- i18n for non-English classrooms
