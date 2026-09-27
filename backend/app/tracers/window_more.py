"""More sliding windows (Step 10) — grow on the right, shrink on the left
while the window breaks a rule, and read the answer off each valid window.

* char_replacement — a window is fixable if (length − most frequent count)
  ≤ k: those are the characters to replace.
* binary_subarray_sum / nice_subarrays — "exactly goal" = "at most goal" −
  "at most goal − 1"; each at-most count adds the window length per step.
  (Nice subarrays count odd numbers, so read every value by its parity.)
* substrings_all_three — remember where a, b and c were last seen; every
  start up to the earliest of those makes a valid substring ending here.
* max_card_points — take k cards from the ends: start with all k from the
  left, then trade the leftmost-taken card for the next card from the right.
* subarrays_k_distinct — at-most(k) − at-most(k − 1) distinct values.
* min_window_substring — expand until every needed character is covered,
  then shrink while it still is; record the smallest.
* min_window_subsequence — scan forward to complete t in order, then scan
  back from there to tighten the start.

Uses the `grid` view with one row of values: the live window is tinted
(`deps`), the best window found so far glows green (`path`).
"""

from collections import Counter

from app.tracers.grid_common import Grid

TITLES = {
    "char_replacement": "Longest Repeating Character Replacement",
    "binary_subarray_sum": "Binary Subarrays With Sum",
    "nice_subarrays": "Count Number of Nice Subarrays",
    "substrings_all_three": "Substrings Containing All Three Characters",
    "max_card_points": "Maximum Points From Cards",
    "subarrays_k_distinct": "Subarrays With K Different Integers",
    "min_window_substring": "Minimum Window Substring",
    "min_window_subsequence": "Minimum Window Subsequence",
}
NUMERIC = {"binary_subarray_sum", "nice_subarrays", "max_card_points",
           "subarrays_k_distinct"}


def run(algo, text, target=None):
    raw = (text or "").replace(" ", "")
    if algo in NUMERIC:
        try:
            a = [int(t) for t in raw.split(",") if t != ""]
        except ValueError:
            raise ValueError("Numbers only, separated by commas.") from None
        if not (1 <= len(a) <= 12) or any(not (0 <= v <= 99) for v in a):
            raise ValueError("Give 1–12 whole numbers, each 0–99.")
        if algo == "binary_subarray_sum" and any(v not in (0, 1) for v in a):
            raise ValueError("Only 0s and 1s.")
        lo = 1 if algo in ("max_card_points", "subarrays_k_distinct") else 0
        if target is None or target != int(target) or not (lo <= target <= len(a)):
            raise ValueError(f"The target must be {lo}–{len(a)}.")
        return {"binary_subarray_sum": _exact_sum, "nice_subarrays": _nice,
                "max_card_points": _cards,
                "subarrays_k_distinct": _k_distinct}[algo](a, int(target))
    if algo in ("min_window_substring", "min_window_subsequence"):
        parts = raw.split(",")
        if len(parts) != 2 or not (1 <= len(parts[0]) <= 16) or \
                not (1 <= len(parts[1]) <= 6) or \
                not (parts[0].isalnum() and parts[1].isalnum()):
            raise ValueError("Give the text (≤ 16) and the pattern (≤ 6), comma-separated.")
        return (_min_window if algo == "min_window_substring" else _min_subseq)(*parts)
    if not (1 <= len(raw) <= 12) or not raw.isalpha():
        raise ValueError("Give 1–12 letters.")
    if algo == "substrings_all_three":
        if any(c not in "abc" for c in raw.lower()):
            raise ValueError("Only the letters a, b and c.")
        return _all_three(raw.lower())
    if target is None or target != int(target) or not (0 <= target <= len(raw)):
        raise ValueError(f"k must be 0–{len(raw)}.")
    return _replacement(raw.upper(), int(target))


def _grid(vals):
    G = Grid(1, len(vals))
    G.grid[0] = list(vals)
    return G


def _win(lo, hi):
    return [(0, j) for j in range(lo, hi + 1)]


def _replacement(s, k):
    G = _grid(s)
    G.counts = {"shrinks": 0}
    cnt = Counter()
    lo, best, best_win = 0, 0, (0, 0)
    G.add(f"A window can become one repeated letter if (length − count of its "
          f"most common letter) ≤ {k}.")
    for hi, ch in enumerate(s):
        cnt[ch] += 1
        while (hi - lo + 1) - max(cnt.values()) > k:
            cnt[s[lo]] -= 1
            lo += 1
            G.counts["shrinks"] += 1
        if hi - lo + 1 > best:
            best, best_win = hi - lo + 1, (lo, hi)
        top = max(cnt.values())
        G.add(f"Window {lo}..{hi}: length {hi - lo + 1}, most common appears "
              f"{top} → {hi - lo + 1 - top} to replace. Best {best}.", 0, hi,
              _win(lo, hi), _win(*best_win))
    G.add(f"Longest fixable window: {best}.", path=_win(*best_win))
    return G.result("char_replacement", best)


def _at_most(G, a, goal, key, label):
    if goal < 0:
        G.add(f"At most {goal}: impossible, count 0.")
        return 0
    lo = total = run = 0
    for hi, v in enumerate(a):
        run += key(v)
        while run > goal:
            run -= key(a[lo])
            lo += 1
        total += hi - lo + 1
        G.add(f"[{label} ≤ {goal}] window {lo}..{hi} is valid: {hi - lo + 1} new "
              f"subarray(s) end here. Running {total}.", 0, hi, _win(lo, hi))
    return total


def _exact(a, goal, key, what, algo):
    G = _grid(a)
    G.add(f"Counting windows with {what} exactly {goal} directly is awkward, but "
          f"'at most' is easy: exactly {goal} = at-most({goal}) − at-most({goal - 1}).")
    x = _at_most(G, a, goal, key, what)
    y = _at_most(G, a, goal - 1, key, what)
    G.add(f"{x} − {y} = {x - y} subarray(s) with {what} exactly {goal}.")
    return G.result(algo, x - y)


def _exact_sum(a, goal):
    return _exact(a, goal, lambda v: v, "sum", "binary_subarray_sum")


def _nice(a, k):
    return _exact(a, k, lambda v: v % 2, "odd count", "nice_subarrays")


def _k_distinct(a, k):
    G = _grid(a)
    G.add(f"Exactly {k} distinct = at-most({k}) − at-most({k - 1}).")

    def at_most(kk):
        cnt, lo, total = Counter(), 0, 0
        for hi, v in enumerate(a):
            cnt[v] += 1
            while len(cnt) > kk:
                cnt[a[lo]] -= 1
                if not cnt[a[lo]]:
                    del cnt[a[lo]]
                lo += 1
            total += hi - lo + 1
            G.add(f"[≤ {kk} distinct] window {lo}..{hi}: {hi - lo + 1} new. "
                  f"Running {total}.", 0, hi, _win(lo, hi))
        return total
    x = at_most(k)
    y = at_most(k - 1) if k > 1 else 0
    G.add(f"{x} − {y} = {x - y} subarray(s) with exactly {k} distinct values.")
    return G.result("subarrays_k_distinct", x - y)


def _all_three(s):
    G = _grid(s)
    G.counts = {"added": 0}
    last = {"a": -1, "b": -1, "c": -1}
    total = 0
    G.add("Remember where a, b and c were last seen. A substring ending here "
          "contains all three iff it starts at or before the earliest of them.")
    for i, ch in enumerate(s):
        last[ch] = i
        m = min(last.values())
        total += m + 1
        G.counts["added"] = total
        G.add(f"At {i} ('{ch}'): last seen a={last['a']}, b={last['b']}, "
              f"c={last['c']} → {m + 1} valid start(s). Total {total}.", 0, i,
              _win(m, i) if m >= 0 else [])
    G.add(f"{total} substring(s) contain all three characters.")
    return G.result("substrings_all_three", total)


def _cards(a, k):
    n = len(a)
    G = _grid(a)
    cells = lambda l, r: [(0, j) for j in range(l)] + [(0, j) for j in range(n - r, n)]
    left, right = sum(a[:k]), 0
    best, bl = left, k
    G.add(f"Take all {k} cards from the left: {left}.", path=cells(k, 0))
    for t in range(1, k + 1):
        left -= a[k - t]
        right += a[n - t]
        if left + right > best:
            best, bl = left + right, k - t
        G.add(f"Swap: give back card {k - t} ({a[k - t]}), take card {n - t} "
              f"({a[n - t]}) → {left + right}. Best {best}.", 0, n - t,
              cells(k - t, t), cells(bl, k - bl))
    G.add(f"Maximum points: {best}.", path=cells(bl, k - bl))
    return G.result("max_card_points", best)


def _min_window(s, t):
    G = _grid(s)
    G.counts = {"shrinks": 0}
    need, have = Counter(t), Counter()
    missing, lo, best = len(t), 0, None
    G.add(f"Grow the window until it covers every character of '{t}' (with "
          f"counts), then shrink from the left while it still does.")
    for hi, ch in enumerate(s):
        have[ch] += 1
        if have[ch] <= need[ch]:
            missing -= 1
        while missing == 0:
            if best is None or hi - lo < best[1] - best[0]:
                best = (lo, hi)
            G.add(f"Window {lo}..{hi} ('{s[lo:hi + 1]}') covers '{t}'. Shrink.",
                  0, hi, _win(lo, hi), _win(*best))
            have[s[lo]] -= 1
            if have[s[lo]] < need[s[lo]]:
                missing += 1
            lo += 1
            G.counts["shrinks"] += 1
        G.add(f"Window {lo}..{hi}: still missing {missing} character(s).", 0, hi,
              _win(lo, hi), _win(*best) if best else (), match=False)
    res = s[best[0]:best[1] + 1] if best else ""
    G.add(f"Minimum window: '{res}'." if best else "No window covers the pattern.",
          path=_win(*best) if best else ())
    return G.result("min_window_substring", res)


def _min_subseq(s, t):
    G = _grid(s)
    G.counts = {"scans": 0}
    best = None
    i = 0
    G.add(f"Scan forward until '{t}' appears in order; then scan backward from "
          f"that end to find the latest possible start. Repeat from start + 1.")
    while i < len(s):
        j, k = 0, i
        while k < len(s) and j < len(t):
            if s[k] == t[j]:
                j += 1
            k += 1
        if j < len(t):
            break
        end = k - 1
        j, start = len(t) - 1, end
        while j >= 0:
            if s[start] == t[j]:
                j -= 1
            start -= 1
        start += 1
        G.counts["scans"] += 1
        if best is None or end - start < best[1] - best[0]:
            best = (start, end)
        G.add(f"Forward scan completes '{t}' at {end}; backward scan tightens the "
              f"start to {start}: '{s[start:end + 1]}'.", 0, end,
              _win(start, end), _win(*best))
        i = start + 1
    res = s[best[0]:best[1] + 1] if best else ""
    G.add(f"Minimum window subsequence: '{res}'." if best else
          f"'{t}' never appears in order.", path=_win(*best) if best else ())
    return G.result("min_window_subsequence", res)
