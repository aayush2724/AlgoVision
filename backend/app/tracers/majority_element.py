"""Majority Element — Boyer-Moore voting, the O(1)-space one-pass trick.

If some value appears more than n/2 times, it survives a cancellation game:
keep a candidate and a count; a matching vote raises the count, any other vote
lowers it, and when the count hits zero the next value becomes the candidate.
Because the true majority outnumbers everyone else combined, it can never be
fully cancelled out. A second pass verifies (an element surviving isn't a
guarantee unless a majority actually exists).

Reuses the `array` view: the current vote is the highlighted cell (`placed`),
and the running candidate/count ride in the note. No new renderer.
"""

MAX_LEN = 16


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(nums: list):
    arr = list(nums)
    n = len(arr)
    steps: list = []
    counts = {"votes": 0}

    def add(note, placed=None, found=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": arr[:],
                "placed": placed,
                "found": found,
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    if not arr:
        add("An empty array has no majority element.", found=False)
        return _result(arr, steps, None)

    add(f"Find a value appearing more than {n}//2 = {n // 2} times. Boyer-Moore "
        f"keeps one candidate and a count, cancelling opposing votes.")

    candidate = None
    count = 0
    for i, v in enumerate(arr):
        counts["votes"] += 1
        if count == 0:
            candidate = v
            count = 1
            add(f"Count is 0 — adopt {_fmt(v)} as the new candidate "
                f"(count 1).", placed=i)
        elif v == candidate:
            count += 1
            add(f"{_fmt(v)} matches the candidate — count rises to {count}.",
                placed=i)
        else:
            count -= 1
            add(f"{_fmt(v)} opposes candidate {_fmt(candidate)} — cancel a "
                f"vote, count falls to {count}.", placed=i)

    # Verify: surviving the vote only guarantees majority if one truly exists.
    occurrences = sum(1 for v in arr if v == candidate)
    add(f"The survivor is {_fmt(candidate)}. Verify by counting: it appears "
        f"{occurrences} time(s).", placed=None)
    if occurrences > n // 2:
        add(f"{occurrences} > {n // 2} — {_fmt(candidate)} is the majority "
            f"element. One pass to find it, one to confirm.", found=True)
        return _result(arr, steps, candidate)
    add(f"{occurrences} is not more than {n // 2} — there is no majority "
        f"element in this array.", found=False)
    return _result(arr, steps, None)


def _result(arr, steps, majority):
    return {
        "meta": {
            "algorithm": "majority_element",
            "view": "array",
            "language": "python",
            "majority": majority,
        },
        "array": arr,
        "steps": steps,
    }
