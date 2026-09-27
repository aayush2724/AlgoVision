"""Binary-search variants — same halving, different question at the middle.

Plain binary search stops at the first match. These keep going, because the
question isn't "is x here?" but "where is the *boundary*?":

* lower_bound — first index with arr[i] ≥ x (also: search insert position)
* upper_bound — first index with arr[i] > x
* first_last_occurrence — two searches: leftmost and rightmost x (their
  distance + 1 is the count of x)
* floor_ceil — two searches: largest value ≤ x and smallest value ≥ x
* kth_missing — in a strictly increasing list of positives, arr[i] − (i+1)
  numbers are missing before index i; search for where that count reaches k
* single_element_sorted — every value appears twice except one; before it,
  pairs start at even indices, after it at odd ones — search that flip

Each records a candidate `ans` whenever the middle satisfies the condition,
then keeps shrinking toward the boundary. Reuses the `array` view's
low/high/mid window; the recorded answer cell is outlined green.
"""

MAX_LEN = 16

TITLES = {
    "lower_bound": "Lower Bound",
    "upper_bound": "Upper Bound",
    "first_last_occurrence": "First & Last Occurrence",
    "floor_ceil": "Floor & Ceil",
    "kth_missing": "Kth Missing Positive",
    "single_element_sorted": "Single Element in a Sorted Array",
}
NEEDS_TARGET = {"lower_bound", "upper_bound", "first_last_occurrence",
                "floor_ceil", "kth_missing"}


def _f(v):
    return f"{v:g}"


def validate(algo: str, arr: list, target) -> str | None:
    if not arr:
        return "Give at least one number."
    if len(arr) > MAX_LEN:
        return f"Max {MAX_LEN} numbers."
    if algo in NEEDS_TARGET and target is None:
        return "This search needs a target value."
    if algo == "kth_missing":
        if any(v != int(v) or v < 1 for v in arr) or \
                any(b <= a for a, b in zip(arr, arr[1:])):
            return "Give strictly increasing positive whole numbers."
        if target != int(target) or not (1 <= target <= 1000):
            return "K must be a whole number 1–1000."
    if algo == "single_element_sorted":
        if any(b < a for a, b in zip(arr, arr[1:])):
            return "The array must be sorted."
        counts: dict = {}
        for v in arr:
            counts[v] = counts.get(v, 0) + 1
        singles = [v for v, c in counts.items() if c == 1]
        if len(singles) != 1 or any(c not in (1, 2) for c in counts.values()):
            return "Every value must appear exactly twice, except one that appears once."
    return None


def trace(algo: str, array: list, target=None):
    arr = list(array) if algo in ("kth_missing", "single_element_sorted") \
        else sorted(array)
    n = len(arr)
    steps: list = []
    counts = {"comparisons": 0}

    def add(note, low, high, mid=None, ans=None, found=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {"low": low, "high": high, "mid": mid, "ans": ans,
                           "found": found, "counts": dict(counts)},
            "highlight": {"index": mid},
            "note": note,
        })

    def boundary(pred, what, going_left):
        """Binary search for the edge where pred(arr[mid]) holds; returns the
        recorded index or None. going_left: on a hit, keep searching left."""
        low, high, ans = 0, n - 1, None
        add(f"Search for {what}. Range 0..{high}.", low, high)
        while low <= high:
            mid = (low + high) // 2
            counts["comparisons"] += 1
            if pred(arr[mid]):
                ans = mid
                side = f"{low}..{mid - 1}" if going_left else f"{mid + 1}..{high}"
                add(f"arr[{mid}] = {_f(arr[mid])} qualifies — record position "
                    f"{mid}, but a better one may lie "
                    f"{'left' if going_left else 'right'}: search {side}.",
                    low, high, mid, ans)
                if going_left:
                    high = mid - 1
                else:
                    low = mid + 1
            else:
                away = "right" if going_left else "left"
                side = f"{mid + 1}..{high}" if going_left else f"{low}..{mid - 1}"
                add(f"arr[{mid}] = {_f(arr[mid])} doesn't qualify — the answer "
                    f"is to the {away}: search {side}.", low, high, mid, ans)
                if going_left:
                    low = mid + 1
                else:
                    high = mid - 1
        return ans

    x = target
    if algo == "lower_bound":
        ans = boundary(lambda v: v >= x, f"the first value ≥ {_f(x)}", True)
        res = n if ans is None else ans
        add(f"Lower bound of {_f(x)} is index {res}"
            + (" (past the end — every value is smaller)" if ans is None else
               f" (value {_f(arr[res])})")
            + ". That is also where to insert it to keep the order.",
            *_frame(ans, n), ans, ans, ans is not None)
        result = res
    elif algo == "upper_bound":
        ans = boundary(lambda v: v > x, f"the first value > {_f(x)}", True)
        res = n if ans is None else ans
        add(f"Upper bound of {_f(x)} is index {res}"
            + (" (past the end)" if ans is None else f" (value {_f(arr[res])})")
            + f". Everything before it is ≤ {_f(x)}.",
            *_frame(ans, n), ans, ans, ans is not None)
        result = res
    elif algo == "first_last_occurrence":
        first = _exact_edge(arr, x, True, add, counts)
        last = _exact_edge(arr, x, False, add, counts)
        if first is None:
            add(f"{_f(x)} never appears: [-1, -1], count 0.", 0, n - 1,
                found=False)
            result = [-1, -1]
        else:
            add(f"{_f(x)} occupies positions {first}..{last} — count "
                f"{last - first + 1}, from two O(log n) searches.",
                first, last, None, last, True)
            result = [first, last]
    elif algo == "floor_ceil":
        fl = boundary(lambda v: v <= x, f"the floor — largest value ≤ {_f(x)}", False)
        ce = boundary(lambda v: v >= x, f"the ceil — smallest value ≥ {_f(x)}", True)
        fv = None if fl is None else arr[fl]
        cv = None if ce is None else arr[ce]
        add(f"Floor of {_f(x)} = {'none' if fv is None else _f(fv)}, ceil = "
            f"{'none' if cv is None else _f(cv)}.",
            min(i for i in (fl, ce, n - 1) if i is not None),
            max(i for i in (fl, ce, 0) if i is not None), None,
            ce if ce is not None else fl, fv is not None or cv is not None)
        result = [fv, cv]
    elif algo == "kth_missing":
        k = int(x)
        low, high = 0, n - 1
        add(f"Before index i, arr[i] − (i+1) positives are missing. Find where "
            f"that count first reaches {k}.", low, high)
        while low <= high:
            mid = (low + high) // 2
            counts["comparisons"] += 1
            miss = arr[mid] - (mid + 1)
            if miss < k:
                add(f"Up to arr[{mid}] = {_f(arr[mid])}, {miss} numbers are "
                    f"missing — fewer than {k}, go right.", low, high, mid)
                low = mid + 1
            else:
                add(f"Up to arr[{mid}] = {_f(arr[mid])}, {miss} numbers are "
                    f"missing — at least {k}, go left.", low, high, mid)
                high = mid - 1
        result = k + low
        add(f"The range closed with {low} array value(s) below the answer, so "
            f"the {k}th missing number is {k} + {low} = {result}.",
            0, n - 1, None, None, True)
    else:  # single_element_sorted
        low, high = 0, n - 1
        add("Pairs start at even indices before the single element and at odd "
            "ones after it. Check the pair at an even mid.", low, high)
        while low < high:
            mid = (low + high) // 2
            if mid % 2:
                mid -= 1
            counts["comparisons"] += 1
            if arr[mid] == arr[mid + 1]:
                add(f"arr[{mid}] = arr[{mid + 1}] — a pair starts at an even "
                    f"index, so the single one is further right.", low, high, mid)
                low = mid + 2
            else:
                add(f"arr[{mid}] ≠ arr[{mid + 1}] — the pattern is already "
                    f"broken, so the single one is at {mid} or left of it.",
                    low, high, mid)
                high = mid
        result = arr[low]
        add(f"Range closed on position {low}: {_f(result)} is the element that "
            f"appears once. O(log n) instead of XOR-ing everything.",
            low, low, low, low, True)

    return {
        "meta": {"algorithm": algo, "view": "array", "language": "python",
                 "result": result},
        "array": arr,
        "steps": steps,
    }


def _frame(ans, n):
    """low/high for a final step: the answer cell alone, or the whole array
    when the answer is past the end (so nothing useful gets dimmed)."""
    return (ans, ans) if ans is not None else (0, n - 1)


def _exact_edge(arr, x, leftmost, add, counts):
    low, high, ans = 0, len(arr) - 1, None
    add(f"Find the {'first' if leftmost else 'last'} {_f(x)}.", low, high)
    while low <= high:
        mid = (low + high) // 2
        counts["comparisons"] += 1
        v = arr[mid]
        if v == x:
            ans = mid
            add(f"arr[{mid}] = {_f(x)} — record it, but keep looking "
                f"{'left' if leftmost else 'right'} for an earlier/later copy.",
                low, high, mid, ans)
            if leftmost:
                high = mid - 1
            else:
                low = mid + 1
        elif v < x:
            add(f"arr[{mid}] = {_f(v)} < {_f(x)} — go right.", low, high, mid, ans)
            low = mid + 1
        else:
            add(f"arr[{mid}] = {_f(v)} > {_f(x)} — go left.", low, high, mid, ans)
            high = mid - 1
    return ans
