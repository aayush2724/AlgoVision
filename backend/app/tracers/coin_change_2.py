"""Coin Change 2 — counting the *number of ways* to make an amount.

The mirror image of minimum-coins: same table shape, but each cell adds
instead of minimises. Cell [c][a] = the number of distinct combinations that
make amount a using only the coins down to row c. It reads two neighbours:
the cell above (make a without this coin) plus the cell `coin` columns left
on the same row (use one more of this coin). Counting by row, not by coin
count, is what stops (1,2) and (2,1) being double-counted.

Reuses the `grid` view (coins × amount), exactly like the minimum-coins table.
No new renderer.
"""

MAX_COINS = 4
MAX_AMOUNT = 12


def trace(coins: list[int], amount: int):
    coin_list = [int(c) for c in coins]
    amt = int(amount)
    steps: list = []
    counts = {"cells": 0, "with_coin": 0, "without_coin": 0}

    rows = len(coin_list) + 1
    cols = amt + 1
    # Row 0 = no coins: there is exactly one way to make amount 0 (take
    # nothing), and no way to make any positive amount.
    grid = [[0] * cols for _ in range(rows)]
    grid[0][0] = 1

    row_labels = ["—"] + [str(c) for c in coin_list]
    col_labels = [str(a) for a in range(cols)]

    def snapshot():
        return [[str(v) for v in row] for row in grid]

    def add(note, current=None, deps=None, path=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "grid": snapshot(),
                "deps": [list(d) for d in (deps or [])],
                "path": [list(p) for p in (path or [])],
                "counts": dict(counts),
            },
            "highlight": {"cell": list(current) if current else None},
            "note": note,
        })

    if not coin_list:
        add("No coin denominations — nothing to make change with.")
        return _result(0, coin_list, amt, row_labels, col_labels, steps)

    add(f"Coins {coin_list}, target {amt}. Each cell counts the ways to make "
        f"this column's amount using only the coins down to this row. Row '—' "
        f"means no coins: exactly one way to make 0 (take nothing), zero ways "
        f"for anything more.", current=[0, 0])

    for r in range(1, rows):
        coin = coin_list[r - 1]
        add(f"Bring in coin {coin}. Every cell now also considers using one "
            f"more {coin}.", current=[r, 0])
        for a in range(cols):
            counts["cells"] += 1
            without = grid[r - 1][a]
            deps = [[r - 1, a]]
            if a >= coin:
                with_it = grid[r][a - coin]
                grid[r][a] = without + with_it
                deps.append([r, a - coin])
                counts["with_coin"] += 1
                add(f"Amount {a}: ways without coin {coin} ({without}) + ways "
                    f"using a {coin} then making {a - coin} ({with_it}) = "
                    f"{grid[r][a]}.", current=[r, a], deps=deps)
            else:
                grid[r][a] = without
                counts["without_coin"] += 1
                add(f"Amount {a}: coin {coin} is too big to use, so carry the "
                    f"{without} way(s) from the row above.",
                    current=[r, a], deps=deps)

    result = grid[rows - 1][amt]
    add(f"Done — there are {result} distinct way(s) to make {amt} from "
        f"{coin_list}. The whole table is O(coins × amount).",
        current=[rows - 1, amt], path=[[rows - 1, amt]])
    return _result(result, coin_list, amt, row_labels, col_labels, steps)


def _result(result, coins, amt, row_labels, col_labels, steps):
    return {
        "meta": {
            "algorithm": "coin_change_2",
            "view": "grid",
            "language": "python",
            "coins": coins,
            "amount": amt,
            "row_labels": row_labels,
            "col_labels": col_labels,
            "result": result,
        },
        "steps": steps,
    }
