"""Lemonade change — a greedy that must spend the right coins first.

Each customer pays with a £5, £10, or £20 note for a £5 drink, in order. You
must give correct change from notes you have already collected. The greedy rule:
when giving £15 change for a £20, hand over a £10 + £5 if you can, and only fall
back to three £5s otherwise — £5 notes are precious because every kind of change
needs them. Fail the moment you cannot make change.

Renders on the array view: each cell is a bill in the queue; served customers
glow green (sorted_ranges), the current customer is highlighted (placed).
"""

MAX_LEN = 16


def trace(array: list[float]):
    bills = [int(v) for v in array]
    steps: list = []
    counts = {"fives": 0, "tens": 0}
    five = ten = 0

    def add(note, current=None, served=-1):
        counts["fives"] = five
        counts["tens"] = ten
        steps.append({
            "i": len(steps), "line": 0,
            "structures": {
                "array": list(bills),
                "sorted_ranges": [[0, served]] if served >= 0 else [],
                "placed": current,
                "counts": dict(counts),
            },
            "highlight": {"index": current, "found": None},
            "note": note,
        })

    if any(b not in (5, 10, 20) for b in bills):
        add("Bills must each be 5, 10, or 20.")
        return _result(bills, steps, False)

    add("Till starts empty. Every drink costs £5; give exact change from notes "
        "you already hold.")

    ok = True
    for i, b in enumerate(bills):
        if b == 5:
            five += 1
            add(f"Customer {i} pays £5 — no change needed. Keep it.", current=i, served=i)
        elif b == 10:
            if five >= 1:
                five -= 1
                ten += 1
                add(f"Customer {i} pays £10 — return one £5.", current=i, served=i)
            else:
                add(f"Customer {i} pays £10 but there is no £5 to return — fail.",
                    current=i, served=i - 1)
                ok = False
                break
        else:  # 20
            if ten >= 1 and five >= 1:
                ten -= 1
                five -= 1
                add(f"Customer {i} pays £20 — return £10 + £5 (save the small "
                    f"notes for later).", current=i, served=i)
            elif five >= 3:
                five -= 3
                add(f"Customer {i} pays £20 — no £10, so return three £5s.",
                    current=i, served=i)
            else:
                add(f"Customer {i} pays £20 but change (£15) can't be made — fail.",
                    current=i, served=i - 1)
                ok = False
                break

    if ok:
        add(f"Everyone served — change was always available. £5×{five}, £10×{ten} "
            f"left in the till.", current=len(bills) - 1, served=len(bills) - 1)
    return _result(bills, steps, ok)


def _result(bills, steps, ok):
    return {
        "meta": {
            "algorithm": "lemonade_change",
            "view": "array",
            "language": "python",
            "served_all": bool(ok),
        },
        "array": list(bills),
        "steps": steps,
    }
