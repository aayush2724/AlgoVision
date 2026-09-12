"""Hash table with separate chaining — where O(1) actually comes from.

The claim "hash maps are O(1)" holds only while the chains stay short. This
tracer makes the bargain visible: every key is hashed to a bucket in one
step, but two keys landing in the same bucket start a chain, and a lookup
then has to walk it. The table is deliberately small so collisions happen.
"""

MAX_KEYS = 8
MAX_TABLE = 7
DEFAULT_BUCKETS = 5


def _hash(key: str, buckets: int) -> int:
    """Sum of character codes, mod table size — small enough to do by hand."""
    return sum(ord(ch) for ch in key) % buckets


def trace(keys: list[str], buckets: int = DEFAULT_BUCKETS, lookup: str | None = None):
    key_list = [str(k) for k in keys]
    n_buckets = int(buckets)
    steps: list = []
    counts = {"hashes": 0, "collisions": 0, "inserts": 0, "probes": 0}

    chains: list[list[str]] = [[] for _ in range(n_buckets)]

    def snapshot():
        width = max(max((len(c) for c in chains), default=1), 1)
        return [
            [chain[i] if i < len(chain) else "" for i in range(width)]
            for chain in chains
        ]

    def add(note, current=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "grid": snapshot(),
                "chains": [list(c) for c in chains],
                "counts": dict(counts),
            },
            "highlight": {"cell": list(current) if current else None},
            "note": note,
        })

    if not key_list:
        add("No keys — an empty table.")
        return _result(chains, n_buckets, None, steps)

    add(f"A table with {n_buckets} buckets. The hash is deliberately simple: "
        f"add up the character codes, then take the remainder mod {n_buckets}. "
        f"That one calculation is what buys O(1) — it jumps straight to a "
        f"bucket instead of scanning.")

    for key in key_list:
        total = sum(ord(ch) for ch in key)
        b = total % n_buckets
        counts["hashes"] += 1

        if chains[b]:
            existing = ", ".join(repr(k) for k in chains[b])
            counts["collisions"] += 1
            chains[b].append(key)
            counts["inserts"] += 1
            add(f"'{key}' sums to {total}, and {total} mod {n_buckets} = {b} — "
                f"but bucket {b} already holds {existing}. That's a collision: "
                f"'{key}' joins the chain, which is now {len(chains[b])} long.",
                current=[b, len(chains[b]) - 1])
        else:
            chains[b].append(key)
            counts["inserts"] += 1
            add(f"'{key}' sums to {total}, and {total} mod {n_buckets} = {b} — "
                f"bucket {b} is empty, so it drops straight in. One step, no "
                f"searching.",
                current=[b, 0])

    occupied = sum(1 for c in chains if c)
    longest = max((len(c) for c in chains), default=0)
    add(f"{len(key_list)} keys in {occupied} of {n_buckets} buckets, "
        f"{counts['collisions']} collisions, longest chain {longest}. "
        f"A lookup costs one hash plus a walk down that chain — so O(1) holds "
        f"only while the chains stay short. Add keys without growing the "
        f"table and the chains, not the hash, become the cost.")

    found = None
    if lookup is not None:
        probe = str(lookup)
        total = sum(ord(ch) for ch in probe)
        b = total % n_buckets
        counts["hashes"] += 1
        add(f"Now look up '{probe}'. Hash it the same way: {total} mod "
            f"{n_buckets} = {b}. We go straight to bucket {b} — every other "
            f"bucket is skipped entirely, however full it is.",
            current=[b, 0])

        for pos, existing in enumerate(chains[b]):
            counts["probes"] += 1
            if existing == probe:
                found = True
                add(f"Slot {pos} of bucket {b} holds '{existing}' — found it "
                    f"after {counts['probes']} comparison"
                    f"{'' if counts['probes'] == 1 else 's'}.",
                    current=[b, pos])
                break
            add(f"Slot {pos} holds '{existing}', not '{probe}' — keep walking "
                f"the chain.", current=[b, pos])
        else:
            found = False
            tail = ("is empty" if not chains[b]
                    else f"holds {len(chains[b])} key(s), none of them '{probe}'")
            add(f"Bucket {b} {tail} — '{probe}' is not in the table. Note we "
                f"still only examined one bucket.",
                current=[b, 0])

    return _result(chains, n_buckets, found, steps)


def _result(chains, n_buckets, found, steps):
    width = max(max((len(c) for c in chains), default=1), 1)
    return {
        "meta": {
            "algorithm": "hash_table",
            "view": "grid",
            "language": "python",
            "row_labels": [f"#{i}" for i in range(n_buckets)],
            "col_labels": [f"slot {i}" for i in range(width)],
            "chains": [list(c) for c in chains],
            "buckets": n_buckets,
            "found": found,
        },
        "steps": steps,
    }
