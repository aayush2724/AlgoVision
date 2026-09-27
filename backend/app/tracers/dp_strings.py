"""String DP on a two-word table — the LCS family and its cousins.

Rows are the characters of A (plus an empty row), columns those of B.

* print_lcs — fill the LCS lengths, then walk back from the corner: a match
  moves diagonally and belongs to the answer; otherwise follow the larger side.
* longest_palindromic_subseq — the LCS of a word and its reverse.
* min_insert_palindrome — n − LPS: every character outside the longest
  palindromic subsequence needs a partner inserted.
* min_ins_del — delete what A has beyond the LCS, insert what B has beyond it.
* shortest_supersequence — walk the LCS table back, writing matched characters
  once and unmatched ones from whichever side we step away from.
* distinct_subsequences — dp[i][j] = ways B[:j] appears in A[:i]: skip A[i],
  plus (if they match) use it.
* wildcard_match — '?' eats one character, '*' eats any run (including none).

Uses the `grid` view: the filled cell is `row`/`col`, the cells it reads are
`deps`, and trace-back paths or matches glow green via `path`.
"""

TITLES = {
    "print_lcs": "Print the Longest Common Subsequence",
    "longest_palindromic_subseq": "Longest Palindromic Subsequence",
    "min_insert_palindrome": "Minimum Insertions to Make a Palindrome",
    "min_ins_del": "Minimum Insertions/Deletions (A → B)",
    "shortest_supersequence": "Shortest Common Supersequence",
    "distinct_subsequences": "Distinct Subsequences",
    "wildcard_match": "Wildcard Matching",
}
MAX_LEN = 8
ONE_WORD = {"longest_palindromic_subseq", "min_insert_palindrome"}


def run(algo, text, target=None):
    raw = (text or "").replace(" ", "")
    if algo in ONE_WORD:
        if not (1 <= len(raw) <= MAX_LEN) or not raw.isalnum():
            raise ValueError(f"Give one word of 1–{MAX_LEN} letters/digits.")
        return trace(algo, raw.lower(), raw.lower()[::-1])
    parts = raw.split(",")
    if len(parts) != 2 or not all(1 <= len(p) <= MAX_LEN for p in parts):
        raise ValueError(f"Give two words (1–{MAX_LEN} chars each), comma-separated.")
    a, b = parts
    if algo == "wildcard_match":
        if not a.isalnum() or any(not (c.isalnum() or c in "?*") for c in b):
            raise ValueError("Text: letters/digits. Pattern: letters/digits, ? and *.")
    elif not (a.isalnum() and b.isalnum()):
        raise ValueError("Letters and digits only.")
    return trace(algo, a.lower(), b.lower())


def trace(algo, a, b):
    n, m = len(a), len(b)
    grid = [[None] * (m + 1) for _ in range(n + 1)]
    steps: list = []
    counts = {"cells": 0}

    def add(note, row=None, col=None, deps=(), path=(), match=True):
        steps.append({"i": len(steps), "line": 0,
                      "structures": {"grid": [r[:] for r in grid], "row": row,
                                     "col": col, "deps": [list(d) for d in deps],
                                     "match": match,
                                     "path": [list(p) for p in path],
                                     "counts": dict(counts)},
                      "highlight": {"index": col}, "note": note})

    meta = {}
    if algo == "wildcard_match":
        dp = [[False] * (m + 1) for _ in range(n + 1)]
        dp[0][0] = True
        for j in range(1, m + 1):
            dp[0][j] = dp[0][j - 1] and b[j - 1] == "*"
        for i in range(n + 1):
            grid[i][0] = "✓" if dp[i][0] else "·"
        for j in range(m + 1):
            grid[0][j] = "✓" if dp[0][j] else "·"
        add("Rows: the text; columns: the pattern. dp[i][j] = the first i text "
            "characters match the first j pattern characters. Only leading '*'s "
            "can match an empty text.", 0, 0)
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                counts["cells"] += 1
                p = b[j - 1]
                if p == "*":
                    dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
                    deps = [(i, j - 1), (i - 1, j)]
                    why = "'*' matches nothing (left) or eats one more char (up)"
                elif p == "?" or p == a[i - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                    deps = [(i - 1, j - 1)]
                    why = f"'{p}' matches '{a[i - 1]}' — inherit the diagonal"
                else:
                    dp[i][j] = False
                    deps = []
                    why = f"'{p}' ≠ '{a[i - 1]}'"
                grid[i][j] = "✓" if dp[i][j] else "·"
                add(f"{why} → {'✓' if dp[i][j] else '·'}.", i, j, deps, match=dp[i][j])
        res = dp[n][m]
        add(f"The whole text {'matches' if res else 'does not match'} the pattern.",
            n, m, match=res)
    elif algo == "distinct_subsequences":
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            dp[i][0] = 1
            grid[i][0] = 1
        for j in range(1, m + 1):
            grid[0][j] = 0
        add(f"How many ways does '{b}' appear as a subsequence of '{a}'? An empty "
            f"target appears exactly once in anything (column 0).", 0, 0)
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                counts["cells"] += 1
                dp[i][j] = dp[i - 1][j]
                deps = [(i - 1, j)]
                if a[i - 1] == b[j - 1]:
                    dp[i][j] += dp[i - 1][j - 1]
                    deps.append((i - 1, j - 1))
                    note = (f"'{a[i - 1]}' = '{b[j - 1]}': ways skipping it "
                            f"({dp[i - 1][j]}) + ways using it ({dp[i - 1][j - 1]})")
                else:
                    note = f"'{a[i - 1]}' ≠ '{b[j - 1]}': only skip it"
                grid[i][j] = dp[i][j]
                add(f"{note} = {dp[i][j]}.", i, j, deps, match=dp[i][j] > 0)
        res = dp[n][m]
        add(f"'{b}' appears {res} way(s) in '{a}'.", n, m)
    else:
        L = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            grid[i][0] = 0
        for j in range(m + 1):
            grid[0][j] = 0
        intro = {
            "print_lcs": f"Longest common subsequence of '{a}' and '{b}': fill "
                         f"the lengths, then trace the answer back.",
            "longest_palindromic_subseq": f"The longest palindromic subsequence "
                                          f"of '{a}' is its LCS with its reverse "
                                          f"'{b}'.",
            "min_insert_palindrome": f"Characters of '{a}' outside its longest "
                                     f"palindromic subsequence each need a "
                                     f"partner inserted. So: LCS with the reverse.",
            "min_ins_del": f"Turn '{a}' into '{b}': keep their LCS, delete the rest "
                           f"of '{a}', insert the rest of '{b}'.",
            "shortest_supersequence": f"The shortest string containing both "
                                      f"'{a}' and '{b}' writes their LCS once.",
        }[algo]
        add(intro, 0, 0)
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                counts["cells"] += 1
                if a[i - 1] == b[j - 1]:
                    L[i][j] = L[i - 1][j - 1] + 1
                    deps = [(i - 1, j - 1)]
                    note = f"'{a[i - 1]}' = '{b[j - 1]}': diagonal + 1 = {L[i][j]}."
                else:
                    L[i][j] = max(L[i - 1][j], L[i][j - 1])
                    deps = [(i - 1, j), (i, j - 1)]
                    note = (f"'{a[i - 1]}' ≠ '{b[j - 1]}': better of up and left "
                            f"= {L[i][j]}.")
                grid[i][j] = L[i][j]
                add(note, i, j, deps)
        # Trace back (also builds the supersequence).
        i, j = n, m
        path, lcs, scs = [], [], []
        while i > 0 and j > 0:
            path.append((i, j))
            if a[i - 1] == b[j - 1]:
                lcs.append(a[i - 1])
                scs.append(a[i - 1])
                i, j = i - 1, j - 1
            elif L[i - 1][j] >= L[i][j - 1]:
                scs.append(a[i - 1])
                i -= 1
            else:
                scs.append(b[j - 1])
                j -= 1
        scs.extend(reversed(a[:i]))
        scs.extend(reversed(b[:j]))
        lcs_s = "".join(reversed(lcs))
        scs_s = "".join(reversed(scs))
        k = L[n][m]
        if algo == "print_lcs":
            res = lcs_s
            msg = f"LCS = '{lcs_s}' (length {k}). Green: the trace-back path."
        elif algo == "longest_palindromic_subseq":
            res = k
            msg = f"Longest palindromic subsequence: '{lcs_s}', length {k}."
        elif algo == "min_insert_palindrome":
            res = n - k
            msg = (f"LPS length {k}, so {n} − {k} = {n - k} insertion(s) make "
                   f"'{a}' a palindrome.")
        elif algo == "min_ins_del":
            res = {"deletions": n - k, "insertions": m - k}
            msg = (f"LCS length {k}: delete {n - k} from '{a}', insert {m - k} "
                   f"from '{b}' — {n + m - 2 * k} operations.")
        else:
            res = scs_s
            msg = (f"Shortest common supersequence: '{scs_s}' — length "
                   f"{n} + {m} − {k} = {len(scs_s)}.")
        meta["lcs"] = lcs_s
        add(msg, path=path)
    return {"meta": {"algorithm": algo, "view": "grid", "language": "python",
                     "result": res, **meta,
                     "row_labels": ["∅"] + list(a), "col_labels": ["∅"] + list(b)},
            "steps": steps}
