"""Coin change (minimum coins) — the DP table, filled cell by cell.

Why a table and not a one-line greedy: greedy works for (1, 5, 10, 25) and
quietly fails for (1, 3, 4) at amount 6 — greedy takes 4+1+1 = 3 coins, the
table finds 3+3 = 2. Watching the table fill is what makes that visible.

Each cell [c][a] answers: using only the coins down to row c, what is the
fewest coins that make amount a? Every cell reads exactly two neighbours —
the cell above (don't use this coin) and the cell `coin` columns left on the
same row (spend one more of it).
"""

MAX_COINS = 4
MAX_AMOUNT = 12


def trace(coins: list[int], amount: int):
    coin_list = [int(c) for c in coins]
    amt = int(amount)
    steps: list = []
    counts = {"cells": 0, "takes": 0, "skips": 0}

    rows = len(coin_list) + 1
    cols = amt + 1
    # Row 0 is "no coins at all": only amount 0 is reachable, and it costs 0.
    grid = [[None] * cols for _ in range(rows)]
    grid[0][0] = 0

    row_labels = ["—"] + [str(c) for c in coin_list]
    col_labels = [str(a) for a in range(cols)]

    def snapshot():
        return [["∞" if v is None else str(v) for v in row] for row in grid]

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
        return _result(None, coin_list, amt, row_labels, col_labels, steps)

    add(f"Coins {coin_list}, target {amt}. Each cell asks: using only the "
        f"coins down to this row, what is the fewest coins that make this "
        f"column's amount? Row '—' means no coins at all — only amount 0 is "
        f"reachable, and it costs 0 coins.",
        current=[0, 0])

    for r in range(1, rows):
        coin = coin_list[r - 1]
        add(f"Row {coin}: the {coin}-coin is now available too. Anything the "
            f"rows above could already make stays available at the same price, "
            f"so each cell starts from the one above it.",
            current=[r, 0])

        for a in range(cols):
            counts["cells"] += 1
            skip = grid[r - 1][a]
            deps = [[r - 1, a]]
            take = None
            if a >= coin and grid[r][a - coin] is not None:
                take = grid[r][a - coin] + 1
                deps.append([r, a - coin])

            if take is not None and (skip is None or take < skip):
                grid[r][a] = take
                counts["takes"] += 1
                add(f"Amount {a}: spend one {coin}-coin and we still owe "
                    f"{a - coin}, which costs {grid[r][a - coin]} — so "
                    f"{grid[r][a - coin]} + 1 = {take} coins. "
                    + (f"Cheaper than the {skip} from the row above."
                       if skip is not None else
                       "The row above could not make this amount at all."),
                    current=[r, a], deps=deps)
            else:
                grid[r][a] = skip
                counts["skips"] += 1
                if skip is None and take is None:
                    add(f"Amount {a}: still unreachable — neither skipping the "
                        f"{coin}-coin nor spending one lands here.",
                        current=[r, a], deps=deps)
                elif take is None:
                    add(f"Amount {a}: a {coin}-coin is too big to spend here, "
                        f"so we inherit {skip} from the row above.",
                        current=[r, a], deps=deps)
                else:
                    add(f"Amount {a}: spending a {coin}-coin would cost {take}, "
                        f"but the row above already does it in {skip} — keep "
                        f"the cheaper one.",
                        current=[r, a], deps=deps)

    best = grid[rows - 1][amt]

    if best is None:
        add(f"Amount {amt} cannot be made from {coin_list} at all — no "
            f"combination of these coins lands exactly on it.",
            current=[rows - 1, amt])
    else:
        used = _coins_used(grid, coin_list, amt)
        add(f"Fewest coins for {amt}: {best} ({' + '.join(str(c) for c in used)}). "
            f"Filled {counts['cells']} cells, each reading two neighbours — "
            f"that's the O(coins × amount) you pay to avoid trying every "
            f"combination.",
            current=[rows - 1, amt],
            path=_reconstruct(grid, coin_list, amt))

    return _result(best, coin_list, amt, row_labels, col_labels, steps)


def _walk_back(grid, coin_list, amt):
    """Yield (row, amount) as the chosen cells are traced to the origin."""
    r, a = len(coin_list), amt
    if grid[r][a] is None:
        return
    yield r, a
    while a > 0 and r > 0:
        if grid[r - 1][a] == grid[r][a]:
            r -= 1
        else:
            a -= coin_list[r - 1]
            yield r, a


def _reconstruct(grid, coin_list, amt):
    return [[r, a] for r, a in _walk_back(grid, coin_list, amt)]


def _coins_used(grid, coin_list, amt):
    r, a, used = len(coin_list), amt, []
    while a > 0 and r > 0:
        if grid[r - 1][a] == grid[r][a]:
            r -= 1
        else:
            used.append(coin_list[r - 1])
            a -= coin_list[r - 1]
    return sorted(used, reverse=True)


def _result(best, coin_list, amt, row_labels, col_labels, steps):
    return {
        "meta": {
            "algorithm": "coin_change",
            "view": "grid",
            "language": "python",
            "row_labels": row_labels,
            "col_labels": col_labels,
            "coins": coin_list,
            "amount": amt,
            "fewest": best,
        },
        "steps": steps,
    }
