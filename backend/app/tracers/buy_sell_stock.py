"""Best Time to Buy and Sell Stock — the one-pass DP that reads like a scan.

The insight that collapses the O(n²) brute force to O(n): to sell on day i for
the most profit, you only need the cheapest price seen *before* i. So sweep
left to right, carry the minimum price so far, and at each day ask "sell today
against that minimum — is this the best profit yet?"

Reuses the `array` view (prices as cells). The buy→sell span of the best trade
lights up green (`best_window`); the current cheapest-so-far → today span is
the active window. No new renderer.
"""

MAX_DAYS = 16


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(prices: list):
    p = [int(x) for x in prices]
    n = len(p)
    steps: list = []
    counts = {"days": 0, "new_lows": 0, "new_bests": 0}

    def add(note, window=None, profit=None, best=None, best_window=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "window": window,
                "sum": profit,
                "best": best,
                "best_window": best_window,
                "counts": dict(counts),
            },
            "highlight": {"index": window[1] if window else None},
            "note": note,
        })

    if not p:
        add("No prices — no trade to make.")
        return _result(p, steps, 0, [])

    add(f"Buy low, sell high, one transaction. Sweep left to right carrying the "
        f"cheapest price seen so far — the best sell is always against that low.")

    min_price = p[0]
    min_day = 0
    best = 0
    best_window: list = [0, 0]
    counts["days"] += 1
    add(f"Day 0: price {_fmt(p[0])} is the cheapest so far. No profit selling "
        f"on the day you buy.", [0, 0], 0, best, list(best_window))

    for i in range(1, n):
        counts["days"] += 1
        profit = p[i] - min_price
        note = (f"Day {i}: price {_fmt(p[i])}. Selling against the low "
                f"{_fmt(min_price)} (day {min_day}) yields {_fmt(profit)}.")
        window = [min_day, i]
        if profit > best:
            best = profit
            best_window = [min_day, i]
            counts["new_bests"] += 1
            note += " New best trade!"
        if p[i] < min_price:
            min_price = p[i]
            min_day = i
            counts["new_lows"] += 1
            note += f" And {_fmt(p[i])} is a new low to buy at."
        add(note, window, profit, best, list(best_window))

    if best > 0:
        add(f"Best profit is {_fmt(best)} — buy day {best_window[0]} "
            f"({_fmt(p[best_window[0]])}), sell day {best_window[1]} "
            f"({_fmt(p[best_window[1]])}). One pass, O(n).",
            None, best, best, list(best_window))
    else:
        add("Prices only fell — no profitable trade, best is 0.",
            None, 0, 0, list(best_window))
    return _result(p, steps, best, best_window)


def _result(prices, steps, best, best_window):
    return {
        "meta": {
            "algorithm": "buy_sell_stock",
            "view": "array",
            "language": "python",
            "result": best,
            "best_window": best_window,
        },
        "array": prices,
        "steps": steps,
    }
