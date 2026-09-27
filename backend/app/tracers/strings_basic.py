"""String basics (Step 5) — one pass over the characters, usually with a
counter or a map riding along.

* remove_outer_parens — track depth; a '(' at depth 0 and a ')' back to depth
  0 are the outer pair of a primitive group, so they are dropped.
* reverse_words — split on spaces (collapsing extras), reverse the word order.
* largest_odd_number — cut after the rightmost odd digit.
* longest_common_prefix — compare column by column until a word differs.
* isomorphic_strings — a consistent one-to-one character mapping both ways.
* rotate_string — goal is a rotation of s exactly when goal appears in s + s.
* sort_by_frequency — count, then write characters most-frequent first.
* max_nesting_depth — the highest depth the '(' counter reaches.
* roman_to_integer — add each value, but subtract when a smaller numeral
  stands before a bigger one (IV, IX, XC …).
* string_to_integer — atoi: skip spaces, read one sign, read digits, stop at
  anything else, clamp to 32-bit.
* sum_of_beauty — for every substring, (most frequent − least frequent); the
  table's cell (i, j) is the beauty of s[i..j].

Uses the `grid` view: row 0 holds the characters; later rows hold what the
algorithm derives (depth, mapping, output …). The current cell is outlined,
kept or matching cells glow green.
"""

from collections import Counter

from app.tracers.grid_common import Grid

TITLES = {
    "remove_outer_parens": "Remove Outermost Parentheses",
    "reverse_words": "Reverse Words in a String",
    "largest_odd_number": "Largest Odd Number in a String",
    "longest_common_prefix": "Longest Common Prefix",
    "isomorphic_strings": "Isomorphic Strings",
    "rotate_string": "Rotate String",
    "sort_by_frequency": "Sort Characters by Frequency",
    "max_nesting_depth": "Maximum Nesting Depth of Parentheses",
    "roman_to_integer": "Roman to Integer",
    "string_to_integer": "String to Integer (atoi)",
    "sum_of_beauty": "Sum of Beauty of All Substrings",
}
ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def run(algo, text, target=None):
    raw = text or ""
    if algo in ("reverse_words", "string_to_integer"):
        if not (1 <= len(raw) <= 24):
            raise ValueError("Give 1–24 characters.")
        return (_reverse_words if algo == "reverse_words" else _atoi)(raw)
    s = raw.replace(" ", "")
    if algo in ("longest_common_prefix", "isomorphic_strings", "rotate_string"):
        parts = [p for p in s.split(",") if p]
        two = algo != "longest_common_prefix"
        if (two and len(parts) != 2) or not (2 <= len(parts) <= 5) or \
                any(len(p) > 10 or not p.isalnum() for p in parts):
            raise ValueError("Give " + ("two words" if two else "2–5 words")
                             + " (up to 10 letters/digits), comma-separated.")
        return {"longest_common_prefix": _lcp, "isomorphic_strings": _iso,
                "rotate_string": _rotate}[algo](parts)
    if not (1 <= len(s) <= 12):
        raise ValueError("Give 1–12 characters.")
    if algo in ("remove_outer_parens", "max_nesting_depth"):
        if algo == "remove_outer_parens" and any(c not in "()" for c in s):
            raise ValueError("Only ( and ).")
        depth = 0
        for c in s:
            depth += 1 if c == "(" else -1 if c == ")" else 0
            if depth < 0:
                raise ValueError("The parentheses must be balanced.")
        if depth:
            raise ValueError("The parentheses must be balanced.")
        return (_outer if algo == "remove_outer_parens" else _depth)(s)
    if algo == "largest_odd_number" and not s.isdigit():
        raise ValueError("Digits only.")
    if algo == "roman_to_integer" and any(c not in ROMAN for c in s.upper()):
        raise ValueError("Roman numerals only: I V X L C D M.")
    if algo in ("sort_by_frequency", "sum_of_beauty") and not s.isalnum():
        raise ValueError("Letters and digits only.")
    if algo == "sum_of_beauty" and len(s) > 8:
        raise ValueError("Keep it to 8 characters — the table is n × n.")
    return {"largest_odd_number": _odd, "roman_to_integer": _roman,
            "sort_by_frequency": _freq, "sum_of_beauty": _beauty}[algo](s)


def _row_grid(s, rows):
    G = Grid(rows, len(s))
    G.grid[0] = list(s)
    return G


def _outer(s):
    G = _row_grid(s, 2)
    G.counts = {"kept": 0}
    depth, out = 0, []
    G.add("Track the depth. A '(' opening at depth 0, or a ')' closing back to "
          "depth 0, is the outer pair of a group — drop it; keep the rest.")
    for i, c in enumerate(s):
        if c == "(":
            keep = depth > 0
            depth += 1
        else:
            depth -= 1
            keep = depth > 0
        G.grid[1][i] = c if keep else "·"
        if keep:
            out.append(c)
            G.counts["kept"] += 1
        G.add(f"'{c}' — depth now {depth}: " + ("keep it." if keep else
                                               "an outer parenthesis, drop it."),
              1, i, match=keep)
    res = "".join(out)
    G.add(f"Result: '{res}'.",
          path=[(1, i) for i in range(len(s)) if G.grid[1][i] != "·"])
    return G.result("remove_outer_parens", res, ["input", "kept"])


def _depth(s):
    G = _row_grid(s, 2)
    G.counts = {"max_depth": 0}
    depth = 0
    G.add("Count open parentheses: '(' adds one, ')' removes one. The answer "
          "is the highest the counter ever gets.")
    for i, c in enumerate(s):
        depth += 1 if c == "(" else -1 if c == ")" else 0
        G.counts["max_depth"] = max(G.counts["max_depth"], depth)
        G.grid[1][i] = depth
        G.add(f"'{c}': depth {depth}.", 1, i)
    m = G.counts["max_depth"]
    G.add(f"Maximum nesting depth: {m}.",
          path=[(1, i) for i in range(len(s)) if G.grid[1][i] == m])
    return G.result("max_nesting_depth", m, ["char", "depth"])


def _reverse_words(raw):
    words = raw.split()
    G = Grid(2, max(len(words), 1))
    G.counts = {"words": len(words)}
    G.grid[0] = words[:] or [""]
    G.add("Split on spaces (extra spaces disappear), then write the words "
          "back in reverse order.")
    rev = words[::-1]
    for i, w in enumerate(rev):
        G.grid[1][i] = w
        G.add(f"Position {i} takes '{w}'.", 1, i, [(0, len(words) - 1 - i)])
    res = " ".join(rev)
    G.add(f"Result: '{res}'.", path=[(1, i) for i in range(len(rev))])
    return G.result("reverse_words", res, ["words", "reversed"])


def _odd(s):
    G = _row_grid(s, 1)
    G.counts = {"checked": 0}
    G.add("A number is odd iff its last digit is. Scan from the right for the "
          "first odd digit and cut there — that prefix is the largest odd one.")
    for i in range(len(s) - 1, -1, -1):
        G.counts["checked"] += 1
        if int(s[i]) % 2:
            res = s[:i + 1].lstrip("0")
            G.add(f"{s[i]} is odd — keep everything up to here: '{res}'.", 0, i,
                  path=[(0, j) for j in range(i + 1)])
            return G.result("largest_odd_number", res, ["digit"])
        G.add(f"{s[i]} is even — drop it.", 0, i, match=False)
    G.add("No odd digit at all — the answer is empty.", match=False)
    return G.result("largest_odd_number", "", ["digit"])


def _lcp(words):
    width = max(len(w) for w in words)
    G = Grid(len(words), width)
    for r, w in enumerate(words):
        G.grid[r] = list(w) + [None] * (width - len(w))
    G.counts = {"columns": 0}
    G.add("Line the words up and compare one column at a time; stop at the "
          "first column where they don't all agree.")
    prefix = ""
    rows = range(len(words))
    for c in range(width):
        col = [w[c] if c < len(w) else None for w in words]
        G.counts["columns"] += 1
        if None in col or len(set(col)) > 1:
            G.add(f"Column {c} disagrees — stop.", 0, c, [(r, c) for r in rows],
                  [(r, j) for r in rows for j in range(c)], match=False)
            break
        prefix += col[0]
        G.add(f"Column {c}: every word has '{col[0]}'. Prefix '{prefix}'.", 0, c,
              path=[(r, j) for r in rows for j in range(c + 1)])
    G.add(f"Longest common prefix: '{prefix}'.",
          path=[(r, j) for r in rows for j in range(len(prefix))])
    return G.result("longest_common_prefix", prefix, words)


def _iso(parts):
    a, b = parts
    n = max(len(a), len(b))
    G = Grid(2, n)
    G.grid[0] = list(a) + [None] * (n - len(a))
    G.grid[1] = list(b) + [None] * (n - len(b))
    G.counts = {"pairs": 0}
    fwd, back = {}, {}
    G.add("Isomorphic: a one-to-one mapping turns the first word into the "
          "second. Track the mapping in both directions.")
    ok = len(a) == len(b)
    if not ok:
        G.add("Different lengths — they can't be isomorphic.", match=False)
    for i in range(len(a) if ok else 0):
        x, y = a[i], b[i]
        G.counts["pairs"] += 1
        if fwd.get(x, y) != y or back.get(y, x) != x:
            ok = False
            clash = (f"'{x}' already maps to '{fwd[x]}'" if fwd.get(x, y) != y
                     else f"'{y}' is already the image of '{back[y]}'")
            G.add(f"Position {i}: '{x}' → '{y}', but {clash} — not isomorphic.",
                  0, i, [(1, i)], match=False)
            break
        fwd[x], back[y] = y, x
        G.add(f"Position {i}: '{x}' ↔ '{y}' is consistent.", 0, i, [(1, i)],
              [(r, j) for r in (0, 1) for j in range(i + 1)])
    if ok:
        G.add("Every pair is consistent both ways — isomorphic.",
              path=[(r, j) for r in (0, 1) for j in range(len(a))])
    return G.result("isomorphic_strings", ok, ["first", "second"])


def _rotate(parts):
    s, goal = parts
    doubled = s + s
    G = Grid(2, len(doubled))
    G.grid[0] = list(doubled)
    G.counts = {"shifts": 0}
    G.add(f"Every rotation of '{s}' appears inside '{s}' + '{s}' = '{doubled}'. "
          f"So slide '{goal}' along it.")
    res = False
    if len(s) == len(goal):
        for k in range(len(s)):
            G.counts["shifts"] += 1
            G.grid[1] = [None] * len(doubled)
            for j, ch in enumerate(goal):
                G.grid[1][k + j] = ch
            window = doubled[k:k + len(s)]
            if window == goal:
                res = True
                G.add(f"Shift {k}: '{window}' matches — '{goal}' is a rotation.",
                      1, k, path=[(0, k + j) for j in range(len(s))])
                break
            G.add(f"Shift {k}: '{window}' ≠ '{goal}'.", 1, k,
                  [(0, k + j) for j in range(len(s))], match=False)
    else:
        G.add("Different lengths — can't be a rotation.", match=False)
    if not res:
        G.add(f"No shift matches — '{goal}' is not a rotation of '{s}'.", match=False)
    return G.result("rotate_string", res, ["s + s", "goal"])


def _freq(s):
    cnt = Counter(s)
    order = sorted(cnt, key=lambda c: (-cnt[c], c))
    G = Grid(2, len(order))
    G.grid[0] = order[:]
    G.counts = {"distinct": len(order)}
    G.add("Count each character, then write them most-frequent first (ties in "
          "character order).")
    out = ""
    for i, c in enumerate(order):
        G.grid[1][i] = cnt[c]
        out += c * cnt[c]
        G.add(f"'{c}' appears {cnt[c]} time(s) → output so far '{out}'.", 1, i)
    G.add(f"Result: '{out}'.", path=[(1, i) for i in range(len(order))])
    return G.result("sort_by_frequency", out, ["char", "count"])


def _roman(s):
    s = s.upper()
    G = _row_grid(s, 2)
    G.counts = {"subtractions": 0}
    total = 0
    G.add("Add each numeral's value — except when it stands before a bigger "
          "one, then subtract it (IV = 4, IX = 9, XC = 90).")
    for i, c in enumerate(s):
        v = ROMAN[c]
        nxt = ROMAN[s[i + 1]] if i + 1 < len(s) else 0
        if v < nxt:
            total -= v
            G.counts["subtractions"] += 1
            G.grid[1][i] = -v
            G.add(f"{c} ({v}) is before a bigger numeral — subtract. Total {total}.",
                  1, i, [(0, i + 1)], match=False)
        else:
            total += v
            G.grid[1][i] = v
            G.add(f"{c} ({v}) — add. Total {total}.", 1, i)
    G.add(f"{s} = {total}.", path=[(1, i) for i in range(len(s))])
    return G.result("roman_to_integer", total, ["numeral", "value"])


def _atoi(raw):
    G = Grid(1, len(raw))
    G.grid[0] = [c if c != " " else "␣" for c in raw]
    G.counts = {"digits": 0}
    G.add("atoi: skip leading spaces, read at most one sign, read digits, stop "
          "at the first non-digit, clamp to the 32-bit range.")
    i, n, sign, val = 0, len(raw), 1, 0
    while i < n and raw[i] == " ":
        G.add("Leading space — skip.", 0, i, match=False)
        i += 1
    if i < n and raw[i] in "+-":
        sign = -1 if raw[i] == "-" else 1
        G.add(f"Sign '{raw[i]}'.", 0, i)
        i += 1
    start = i
    while i < n and raw[i].isdigit():
        val = val * 10 + int(raw[i])
        G.counts["digits"] += 1
        G.add(f"Digit {raw[i]} → {sign * val}.", 0, i,
              path=[(0, j) for j in range(start, i + 1)])
        i += 1
    if i < n:
        G.add(f"'{raw[i]}' is not a digit — stop reading.", 0, i, match=False)
    res = max(-2 ** 31, min(2 ** 31 - 1, sign * val))
    G.add(f"Result: {res}" + (" (clamped to 32 bits)." if res != sign * val else "."),
          path=[(0, j) for j in range(start, i)])
    return G.result("string_to_integer", res, ["char"])


def _beauty(s):
    n = len(s)
    G = Grid(n, n)
    G.counts = {"substrings": 0}
    total = 0
    G.add("Beauty of a substring = most frequent count − least frequent count. "
          "Cell (i, j) is the beauty of s[i..j]; grow each start i to the right "
          "with a running count.")
    for i in range(n):
        cnt = Counter()
        for j in range(i, n):
            cnt[s[j]] += 1
            b = max(cnt.values()) - min(cnt.values())
            total += b
            G.counts["substrings"] += 1
            G.grid[i][j] = b
            G.add(f"'{s[i:j + 1]}': beauty {b}. Running sum {total}.", i, j)
    G.add(f"Sum of beauty over all {G.counts['substrings']} substrings: {total}.")
    return G.result("sum_of_beauty", total, [f"i={c}" for c in s],
                    [f"j={c}" for c in s])
