"""Assign cookies — the two-pointer greedy for maximum content children.

Each child has a greed factor; each cookie a size. A child is content if given a
cookie at least as big as their greed. To content the most children, sort both,
then walk a pointer up each: offer the smallest remaining cookie to the least
greedy child — if it fits, both move on; if not, that cookie is too small for
*everyone* left, so discard it and try the next cookie. Greedy because spending
a bigger cookie on a less greedy child can only ever waste it.

Renders on the array view: cells are the sorted greed factors; contented
children glow green (sorted_ranges), the child under consideration is
highlighted (placed).
"""

MAX_LEN = 10


def trace(greed: list[float], sizes: list[float]):
    g = sorted(int(x) for x in greed)
    s = sorted(int(x) for x in sizes)
    steps: list = []
    counts = {"content": 0, "cookies_used": 0}
    content_idx: list[int] = []

    def add(note, current=None):
        steps.append({
            "i": len(steps), "line": 0,
            "structures": {
                "array": list(g),
                "sorted_ranges": [[i, i] for i in content_idx],
                "placed": current,
                "counts": dict(counts),
            },
            "highlight": {"index": current, "found": None},
            "note": note,
        })

    if not g:
        add("No children to feed.")
        return _result(g, steps, 0)

    add(f"Children sorted by greed: {g}. Cookies sorted by size: {s}. "
        f"Match the smallest cookie to the least greedy child.")

    i = j = 0
    while i < len(g) and j < len(s):
        if s[j] >= g[i]:
            content_idx.append(i)
            counts["content"] += 1
            counts["cookies_used"] += 1
            add(f"Cookie {s[j]} satisfies child (greed {g[i]}) — content! "
                f"Move both pointers.", current=i)
            i += 1
            j += 1
        else:
            counts["cookies_used"] += 1
            add(f"Cookie {s[j]} is too small for child (greed {g[i]}) — it is "
                f"too small for everyone left, so discard it.", current=i)
            j += 1

    add(f"Done. {counts['content']} of {len(g)} children made content — the most "
        f"possible.", current=min(i, len(g) - 1))
    return _result(g, steps, counts["content"])


def _result(g, steps, content):
    return {
        "meta": {
            "algorithm": "assign_cookies",
            "view": "array",
            "language": "python",
            "content": content,
        },
        "array": list(g),
        "steps": steps,
    }
