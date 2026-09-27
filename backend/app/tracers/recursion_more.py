"""Recursion & backtracking leftovers (Steps 1, 2, 7) on the `grid` view.

* print_1_to_n / print_n_to_1 — where the print sits relative to the
  recursive call decides the order: before it (on the way down) or after it
  (printed while the calls unwind).
* recursive_bubble_sort / recursive_insertion_sort — one pass (or one
  insertion), then recurse on the smaller problem.
* count_good_numbers — even positions have 5 choices, odd ones 4, so the
  answer is 5^ceil(n/2) · 4^floor(n/2) mod 1e9+7, via fast power.
* sort_stack / reverse_stack — only push/pop: pop the top, solve the rest
  recursively, then insert the held value (in order / at the bottom).
* recursive_atoi — skip spaces, read a sign, then atoi(i, acc) consumes one
  digit per call; clamp to 32 bits.
* word_break — can(i) is true if some dictionary word starts at i and
  can(i + len) is true (memoised from the right).
* m_coloring / sudoku_solver / expression_add_operators — try each choice,
  recurse, undo on failure. Long searches emit their first STEP_CAP steps
  and then fast-forward to the answer.
"""

from app.tracers.grid_common import Grid, parse_matrix

TITLES = {
    "print_1_to_n": "Print 1 to N Using Recursion",
    "print_n_to_1": "Print N to 1 Using Recursion",
    "recursive_bubble_sort": "Recursive Bubble Sort",
    "recursive_insertion_sort": "Recursive Insertion Sort",
    "count_good_numbers": "Count Good Numbers",
    "sort_stack": "Sort a Stack Using Recursion",
    "reverse_stack": "Reverse a Stack Using Recursion",
    "recursive_atoi": "Recursive atoi()",
    "word_break": "Word Break",
    "m_coloring": "M-Coloring Problem",
    "sudoku_solver": "Sudoku Solver",
    "expression_add_operators": "Expression Add Operators",
}
MOD = 10 ** 9 + 7
STEP_CAP = 300


def _nums(text, n=10):
    try:
        a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("Numbers only, separated by commas.") from None
    if not (1 <= len(a) <= n) or any(abs(v) > 999 for v in a):
        raise ValueError(f"Give 1–{n} numbers within ±999.")
    return a


def _int(text, lo, hi):
    try:
        v = int((text or "").strip())
    except ValueError:
        raise ValueError("Give a whole number.") from None
    if not (lo <= v <= hi):
        raise ValueError(f"Keep it between {lo} and {hi}.")
    return v


def run(algo, text, target=None):
    if algo in ("print_1_to_n", "print_n_to_1"):
        return _print(_int(text, 1, 10), algo)
    if algo == "count_good_numbers":
        return _good(_int(text, 1, 10 ** 15))
    if algo in ("recursive_bubble_sort", "recursive_insertion_sort", "sort_stack",
                "reverse_stack"):
        a = _nums(text, 8 if "stack" in algo else 10)
        return globals()["_" + algo](a)
    if algo == "recursive_atoi":
        s = text or ""
        if not (1 <= len(s) <= 16):
            raise ValueError("Give 1–16 characters.")
        return _atoi(s)
    if algo == "word_break":
        if "|" not in (text or ""):
            raise ValueError("Give 'text | word,word,…', e.g. leetcode | leet,code.")
        s, words = text.split("|", 1)
        s = s.strip().lower()
        ws = [w.strip().lower() for w in words.split(",") if w.strip()]
        if not (1 <= len(s) <= 14) or not s.isalpha() or not (1 <= len(ws) <= 8) \
                or not all(w.isalpha() and len(w) <= 8 for w in ws):
            raise ValueError("Text of 1–14 letters and 1–8 words (≤ 8 letters each).")
        return _word_break(s, ws)
    if algo == "m_coloring":
        edges = _edges(text)
        if target is None or target != int(target) or not (1 <= target <= 4):
            raise ValueError("m (colours) must be 1–4.")
        return _coloring(edges, int(target))
    if algo == "sudoku_solver":
        raw = (text or "").replace(" ", "")
        if "," not in raw:          # compact rows: 530070000/600195000/…
            raw = "/".join(",".join(r) for r in raw.split("/") if r)
        g = parse_matrix(raw, max_side=9)
        n = len(g)
        if n not in (4, 9) or len(g[0]) != n or any(not (0 <= v <= n) for r in g for v in r):
            raise ValueError("Give a 4×4 or 9×9 grid with 0 for blanks.")
        return _sudoku(g)
    if algo == "expression_add_operators":
        s = (text or "").strip()
        if not (1 <= len(s) <= 5) or not s.isdigit():
            raise ValueError("Give 1–5 digits.")
        if target is None or target != int(target) or abs(target) > 99999:
            raise ValueError("Give a whole-number target.")
        return _add_ops(s, int(target))
    raise ValueError("Unknown algorithm.")


def _print(n, algo):
    up = algo == "print_1_to_n"
    G = Grid(2, n)
    G.counts = {"calls": 0}
    out = []
    G.add("f(i) prints i, THEN calls f(i + 1): the prints happen on the way "
          "down, so they come out 1, 2, …, N." if up else
          "f(i) calls f(i + 1) FIRST and prints i afterwards: nothing prints "
          "until the deepest call returns, so the prints come out N, …, 1.")

    def f(i):
        G.counts["calls"] += 1
        if i > n:
            G.add(f"f({i}): {i} > {n} — the base case, return.", match=False)
            return
        G.grid[0][i - 1] = f"f({i})"
        stack = [(0, j) for j in range(i)]
        if up:
            out.append(i)
            G.grid[1][len(out) - 1] = i
            G.add(f"f({i}) prints {i}, then calls f({i + 1}).", 0, i - 1, stack)
            f(i + 1)
        else:
            G.add(f"f({i}) calls f({i + 1}) first.", 0, i - 1, stack)
            f(i + 1)
            out.append(i)
            G.grid[1][len(out) - 1] = i
            G.add(f"Back in f({i}): print {i}.", 1, len(out) - 1, stack)
    f(1)
    G.add(f"Printed: {out}.", path=[(1, j) for j in range(n)])
    return G.result(algo, out, ["calls", "printed"])


def _recursive_bubble_sort(a):
    arr = list(a)
    G = Grid(1, len(arr))
    G.grid[0] = arr[:]
    G.counts = {"comparisons": 0, "swaps": 0}
    G.add("bubble(n): one pass carries the largest of the first n values to "
          "position n − 1, then bubble(n − 1) sorts the rest. bubble(1) is done.")

    def bubble(n):
        settled = [(0, j) for j in range(n, len(arr))]
        if n <= 1:
            G.add("bubble(1): a single value is sorted — base case.",
                  path=[(0, j) for j in range(len(arr))])
            return
        swapped = False
        for i in range(n - 1):
            G.counts["comparisons"] += 1
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                G.counts["swaps"] += 1
                swapped = True
                G.grid[0] = arr[:]
                G.add(f"bubble({n}): {arr[i + 1]} > {arr[i]} — swap.", 0, i + 1,
                      [(0, i)], settled)
            else:
                G.add(f"bubble({n}): {arr[i]} ≤ {arr[i + 1]}.", 0, i + 1, [(0, i)],
                      settled, match=False)
        if not swapped:
            G.add("No swaps in that pass — already sorted; stop early.",
                  path=[(0, j) for j in range(len(arr))])
            return
        G.add(f"{arr[n - 1]} is in its final place; recurse on bubble({n - 1}).",
              0, n - 1, path=[(0, j) for j in range(n - 1, len(arr))])
        bubble(n - 1)
    bubble(len(arr))
    return G.result("recursive_bubble_sort", arr, ["array"])


def _recursive_insertion_sort(a):
    arr = list(a)
    G = Grid(1, len(arr))
    G.grid[0] = arr[:]
    G.counts = {"shifts": 0}
    G.add("insert(i): the prefix before i is sorted. Slide a[i] left past every "
          "bigger value, then recurse on insert(i + 1).", path=[(0, 0)])

    def insert(i):
        if i == len(arr):
            G.add("i reached the end — base case. Sorted.",
                  path=[(0, j) for j in range(len(arr))])
            return
        j = i
        while j > 0 and arr[j - 1] > arr[j]:
            arr[j - 1], arr[j] = arr[j], arr[j - 1]
            G.counts["shifts"] += 1
            G.grid[0] = arr[:]
            G.add(f"insert({i}): {arr[j - 1]} moves left past {arr[j]}.", 0, j - 1,
                  [(0, j)])
            j -= 1
        G.add(f"insert({i}): {arr[j]} is in place; prefix 0..{i} is sorted.", 0, j,
              path=[(0, k) for k in range(i + 1)])
        insert(i + 1)
    insert(1)
    return G.result("recursive_insertion_sort", arr, ["array"])


def _good(n):
    e5, e4 = (n + 1) // 2, n // 2
    G = Grid(2, 3)
    G.grid = [["base", "exp", "result"], [5, e5, 1]]
    G.counts = {"multiplications": 0}
    G.add(f"Even indices (0, 2, …) must hold an even digit (5 choices); odd "
          f"indices a prime (2, 3, 5, 7 — 4 choices). {n} digit(s) → {e5} even "
          f"and {e4} odd position(s): 5^{e5} · 4^{e4} mod 1e9+7, by fast power.")

    def power(b, e):
        r = 1
        G.grid[1] = [b, e, r]
        while e:
            bit = e & 1
            if bit:
                r = r * b % MOD
                G.counts["multiplications"] += 1
            b = b * b % MOD
            e >>= 1
            G.counts["multiplications"] += 1
            G.grid[1] = [b, e, r]
            G.add(f"Lowest exponent bit is {bit}"
                  f"{' → multiply it into the result' if bit else ''}; square the "
                  f"base and halve the exponent → exp {e}, result {r}.", 1, 2)
        return r
    x = power(5, e5)
    G.add(f"5^{e5} mod 1e9+7 = {x}. Now 4^{e4}.")
    y = power(4, e4)
    res = x * y % MOD
    G.grid[1] = [None, None, res]
    G.add(f"Good numbers = {x} · {y} mod 1e9+7 = {res}.", path=[(1, 2)])
    return G.result("count_good_numbers", res, ["", "value"])


def _rows(stack, held, n):
    return [list(stack) + [None] * (n - len(stack)),
            list(held) + [None] * (n - len(held))]


def _sort_stack(a):
    n = len(a)
    st, held = list(a), []           # bottom → top
    G = Grid(2, n)
    G.grid = _rows(st, held, n)
    G.counts = {"pops": 0, "pushes": 0}
    G.add("sort(): pop the top, sort the rest recursively, then insert the held "
          "value. insert(x): if the top is bigger than x, pop it, insert x "
          "deeper, push it back. Only push/pop — the call stack holds values.")

    def show(note, col=None):
        G.grid = _rows(st, held, n)
        G.add(note, 0 if col is not None else None, col)

    def insert(x):
        if not st or st[-1] <= x:
            st.append(x)
            G.counts["pushes"] += 1
            show(f"{'Stack empty' if len(st) == 1 else f'Top {st[-2]} ≤ {x}'} — "
                 f"push {x}.", len(st) - 1)
            return
        top = st.pop()
        G.counts["pops"] += 1
        held.append(top)
        show(f"Top {top} > {x} — hold {top}, insert {x} deeper.")
        insert(x)
        held.pop()
        st.append(top)
        G.counts["pushes"] += 1
        show(f"Put {top} back on top.", len(st) - 1)

    def sort():
        if not st:
            show("Empty stack — sorted (base case).")
            return
        x = st.pop()
        G.counts["pops"] += 1
        held.append(x)
        show(f"Pop {x} and hold it while the rest is sorted.")
        sort()
        held.pop()
        show(f"The rest is sorted; insert the held {x}.")
        insert(x)
    sort()
    G.add(f"Sorted stack (bottom → top): {st}.", path=[(0, j) for j in range(n)])
    return G.result("sort_stack", st, ["stack", "held"])


def _reverse_stack(a):
    n = len(a)
    st, held = list(a), []
    G = Grid(2, n)
    G.grid = _rows(st, held, n)
    G.counts = {"pops": 0, "pushes": 0}
    G.add("reverse(): pop the top, reverse the rest, then insert the popped value "
          "at the BOTTOM. insert_bottom(x): pop everything above, push x, push "
          "them back.")

    def show(note, col=None):
        G.grid = _rows(st, held, n)
        G.add(note, 0 if col is not None else None, col)

    def insert_bottom(x):
        if not st:
            st.append(x)
            G.counts["pushes"] += 1
            show(f"Stack empty — {x} goes to the bottom.", 0)
            return
        top = st.pop()
        G.counts["pops"] += 1
        held.append(top)
        show(f"Hold {top} to reach the bottom.")
        insert_bottom(x)
        held.pop()
        st.append(top)
        G.counts["pushes"] += 1
        show(f"Push {top} back.", len(st) - 1)

    def reverse():
        if not st:
            show("Empty — nothing to reverse (base case).")
            return
        x = st.pop()
        G.counts["pops"] += 1
        held.append(x)
        show(f"Pop {x}; reverse the rest first.")
        reverse()
        held.pop()
        show(f"Insert {x} at the bottom.")
        insert_bottom(x)
    reverse()
    G.add(f"Reversed (bottom → top): {st}.", path=[(0, j) for j in range(n)])
    return G.result("reverse_stack", st, ["stack", "held"])


def _atoi(s):
    G = Grid(1, len(s))
    G.grid[0] = list(s)
    G.counts = {"calls": 0}
    lo, hi = -2 ** 31, 2 ** 31 - 1
    G.add("Skip leading spaces, read one optional sign, then atoi(i, acc) eats "
          "one digit per call until a non-digit; clamp to the 32-bit range.")
    i = 0
    while i < len(s) and s[i] == " ":
        G.add("Skip a space.", 0, i, match=False)
        i += 1
    sign = 1
    if i < len(s) and s[i] in "+-":
        sign = -1 if s[i] == "-" else 1
        G.add(f"Sign '{s[i]}'.", 0, i)
        i += 1

    def rec(j, acc):
        G.counts["calls"] += 1
        if j == len(s) or not s[j].isdigit():
            why = "end of text" if j == len(s) else f"'{s[j]}' is not a digit"
            G.add(f"atoi({j}, {acc}): {why} — return {acc}.", 0,
                  j if j < len(s) else None, match=False)
            return sign * acc
        acc = acc * 10 + int(s[j])
        if not (lo <= sign * acc <= hi):
            G.add(f"atoi({j}): {sign * acc} leaves the 32-bit range — clamp.", 0, j)
            return hi if sign > 0 else lo
        G.add(f"atoi({j}, …): digit {s[j]} → acc = {acc}.", 0, j,
              path=[(0, k) for k in range(i, j + 1)])
        return rec(j + 1, acc)
    val = rec(i, 0)
    G.add(f"Result: {val}.")
    return G.result("recursive_atoi", val, ["char"])


def _word_break(s, words):
    n = len(s)
    G = Grid(2, n + 1)
    G.grid[0] = list(s) + ["∅"]
    G.grid[1] = [None] * n + ["T"]
    G.counts = {"checks": 0}
    ok = [False] * (n + 1)
    ok[n] = True
    G.add(f"can(i): does s[i:] split into words from {words}? can({n}) is true "
          f"(nothing left). Fill from the right so every can(i + len) is known.",
          1, n)
    for i in range(n - 1, -1, -1):
        for w in words:
            G.counts["checks"] += 1
            if s.startswith(w, i) and ok[i + len(w)]:
                ok[i] = True
                G.grid[1][i] = "T"
                G.add(f"can({i}): '{w}' starts here and can({i + len(w)}) is true "
                      f"→ true.", 1, i, [(0, k) for k in range(i, i + len(w))]
                      + [(1, i + len(w))])
                break
        else:
            G.grid[1][i] = "F"
            G.add(f"can({i}): no word both starts at {i} and leaves a breakable "
                  f"rest → false.", 1, i, match=False)
    G.add(f"can(0) = {ok[0]}: '{s}' {'can' if ok[0] else 'cannot'} be broken into "
          f"dictionary words.", 1, 0, match=ok[0])
    return G.result("word_break", ok[0], ["text", "can(i)"])


def _edges(text):
    edges = []
    for e in [p for p in (text or "").replace(" ", "").split(",") if p]:
        try:
            u, v = (int(x) for x in e.split("-"))
        except ValueError:
            raise ValueError("Give edges like 0-1,1-2,2-0 (nodes 0–7).") from None
        if not (0 <= u <= 7 and 0 <= v <= 7) or u == v:
            raise ValueError("Nodes 0–7, no self-loops.")
        edges.append((u, v))
    if not edges or len(edges) > 16:
        raise ValueError("Give 1–16 edges.")
    return edges


def _coloring(edges, m):
    n = max(max(e) for e in edges) + 1
    adj = {i: set() for i in range(n)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    color = [0] * n
    G = Grid(2, n)
    G.grid[0] = list(range(n))
    G.counts = {"tries": 0, "backtracks": 0}
    G.add(f"Colour nodes 0..{n - 1} in order with colours 1..{m}. A colour is "
          f"allowed if no neighbour already has it; if none fits, undo and go back.")

    def solve(i):
        if i == n:
            return True
        for c in range(1, m + 1):
            G.counts["tries"] += 1
            clash = sorted(v for v in adj[i] if color[v] == c)
            if clash:
                if len(G.steps) < STEP_CAP:
                    G.add(f"Node {i}: colour {c} clashes with neighbour {clash[0]}.",
                          1, i, [(1, v) for v in clash], match=False)
                continue
            color[i] = c
            G.grid[1] = [x or None for x in color]
            if len(G.steps) < STEP_CAP:
                G.add(f"Node {i}: colour {c} is free — try it.", 1, i)
            if solve(i + 1):
                return True
            color[i] = 0
            G.counts["backtracks"] += 1
            G.grid[1] = [x or None for x in color]
            if len(G.steps) < STEP_CAP:
                G.add(f"Nothing works after node {i} = {c} — undo.", 1, i, match=False)
        return False
    ok = solve(0)
    G.add(f"Coloured with ≤ {m} colour(s): {color}." if ok
          else f"Impossible with {m} colour(s).",
          path=[(1, j) for j in range(n)] if ok else ())
    return G.result("m_coloring", ok, ["node", "colour"], coloring=color if ok else None)


def _sudoku(g):
    n = len(g)
    b = int(n ** 0.5)
    G = Grid(n, n)
    G.counts = {"placements": 0, "backtracks": 0}
    board = [r[:] for r in g]
    given = [(r, c) for r in range(n) for c in range(n) if g[r][c]]
    snap = lambda: [[x or None for x in row] for row in board]

    def fits(r, c, v):
        br, bc = r - r % b, c - c % b
        return all(board[r][j] != v for j in range(n)) and \
            all(board[i][c] != v for i in range(n)) and \
            all(board[i][j] != v for i in range(br, br + b) for j in range(bc, bc + b))

    for r, c in given:
        v, board[r][c] = board[r][c], 0
        if not fits(r, c, v):
            raise ValueError("The given digits already clash.")
        board[r][c] = v
    G.grid = snap()
    G.add(f"Fill blanks left to right, top to bottom. Try each digit 1..{n} that "
          f"isn't in the row, column or {b}×{b} box; recurse; if the rest fails, "
          f"erase it and try the next digit.", deps=given)
    blanks = [(r, c) for r in range(n) for c in range(n) if not g[r][c]]

    def solve(k):
        if k == len(blanks):
            return True
        r, c = blanks[k]
        for v in range(1, n + 1):
            if fits(r, c, v):
                board[r][c] = v
                G.counts["placements"] += 1
                if len(G.steps) < STEP_CAP:
                    G.grid = snap()
                    G.add(f"({r}, {c}) ← {v}.", r, c, given)
                if solve(k + 1):
                    return True
                board[r][c] = 0
                G.counts["backtracks"] += 1
                if len(G.steps) < STEP_CAP:
                    G.grid = snap()
                    G.add(f"({r}, {c}) = {v} leads nowhere — erase.", r, c, given,
                          match=False)
        return False
    ok = solve(0)
    capped = len(G.steps) >= STEP_CAP
    G.grid = snap()
    G.add(("Solved!" if ok else "No solution.")
          + (" (Later steps were fast-forwarded.)" if capped else ""),
          deps=given, path=blanks if ok else ())
    return G.result("sudoku_solver", board if ok else None)


def _add_ops(s, t):
    n = len(s)
    w = 2 * n - 1
    G = Grid(1, w)
    G.counts = {"expressions": 0}
    found = []
    G.add(f"Between each pair of digits choose +, −, × or nothing (joining "
          f"digits). Track the last operand so × can undo it: value − last + "
          f"last × next. Keep expressions that equal {t}.")

    def show(expr, val):
        cells = []
        for ch in expr:
            if ch.isdigit() and len(cells) % 2 == 1:
                cells.append("")
            cells.append(ch)
        G.grid[0] = cells
        ok = val == t
        if len(G.steps) < STEP_CAP:
            G.add(f"{expr} = {val}" + (" ✓" if ok else ""), 0, None, match=ok,
                  path=[(0, j) for j in range(w)] if ok else ())

    def dfs(i, expr, val, last):
        if i == n:
            G.counts["expressions"] += 1
            if val == t:
                found.append(expr)
            show(expr, val)
            return
        for j in range(i + 1, n + 1):
            part = s[i:j]
            if len(part) > 1 and part[0] == "0":
                break
            x = int(part)
            if i == 0:
                dfs(j, part, x, x)
            else:
                dfs(j, expr + "+" + part, val + x, x)
                dfs(j, expr + "-" + part, val - x, -x)
                dfs(j, expr + "*" + part, val - last + last * x, last * x)
    dfs(0, "", 0, 0)
    G.add(f"{len(found)} expression(s) equal {t}: {found or 'none'}.")
    return G.result("expression_add_operators", found, ["expr"])
