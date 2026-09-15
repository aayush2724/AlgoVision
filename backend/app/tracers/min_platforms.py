"""Minimum railway platforms — the sweep-line greedy.

Sort arrival and departure times separately, then sweep the timeline merging the
two sorted lists: every arrival before the next departure needs a fresh platform
(count up, track the peak); every departure frees one (count down). The peak
concurrent count is the answer. Sorting decouples the trains from their pairing —
only the *timing* of events matters.

Renders on the array view: cells are the sorted arrival times; a train that has
been given a platform glows green (sorted_ranges), the arrival being processed
is highlighted (placed).
"""

MAX_LEN = 10


def trace(arrivals: list[float], departures: list[float]):
    arr = sorted(int(x) for x in arrivals)
    dep = sorted(int(x) for x in departures)
    steps: list = []
    counts = {"platforms": 0, "peak": 0}
    seated: list[int] = []

    def add(note, current=None):
        steps.append({
            "i": len(steps), "line": 0,
            "structures": {
                "array": list(arr),
                "sorted_ranges": [[k, k] for k in seated],
                "placed": current,
                "counts": dict(counts),
            },
            "highlight": {"index": current, "found": None},
            "note": note,
        })

    n = len(arr)
    if not n:
        add("No trains — no platforms needed.")
        return _result(arr, steps, 0)

    add(f"Arrivals sorted: {arr}. Departures sorted: {dep}. Sweep the timeline; "
        f"the most overlapping trains is the platforms needed.")

    i = j = 0
    platforms = peak = 0
    while i < n:
        if arr[i] <= dep[j]:
            platforms += 1
            peak = max(peak, platforms)
            counts["platforms"] = platforms
            counts["peak"] = peak
            seated.append(i)
            add(f"Train arrives at {arr[i]} before the next departure ({dep[j]}) "
                f"— needs a platform. {platforms} in use (peak {peak}).", current=i)
            i += 1
        else:
            platforms -= 1
            counts["platforms"] = platforms
            add(f"A train departs at {dep[j]} before the next arrival ({arr[i]}) "
                f"— frees a platform. {platforms} in use.", current=i)
            j += 1

    add(f"Busiest moment needed {peak} platforms — that is the minimum.",
        current=n - 1)
    return _result(arr, steps, peak)


def _result(arr, steps, peak):
    return {
        "meta": {
            "algorithm": "min_platforms",
            "view": "array",
            "language": "python",
            "platforms": peak,
        },
        "array": list(arr),
        "steps": steps,
    }
