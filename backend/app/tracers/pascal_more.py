"""Pascal's Triangle I and II (Arrays / FAQs) on the `grid` view.

* pascal_element — the element at row r, column c (1-based) is C(r−1, c−1),
  built as a running product: multiply by (n − i), divide by (i + 1).
* pascal_row — the whole nth row from one running product: each cell is the
  previous cell · (n − i) / i, so no factorials and no earlier rows.
"""

from app.tracers.grid_common import Grid

TITLES = {
    "pascal_element": "Pascal's Triangle I — One Element",
    "pascal_row": "Pascal's Triangle II — One Row",
}


def run(algo, text, target=None):
    if algo == "pascal_element":
        parts = [p for p in (text or "").replace(" ", "").split(",") if p]
        if len(parts) != 2:
            raise ValueError("Give row,column — e.g. 5,3.")
        try:
            r, c = int(parts[0]), int(parts[1])
        except ValueError:
            raise ValueError("Whole numbers only.") from None
        if not (1 <= r <= 12) or not (1 <= c <= r):
            raise ValueError("Row 1–12, and column between 1 and the row.")
        return _element(r, c)
    try:
        n = int((text or "").strip())
    except ValueError:
        raise ValueError("Give the row number.") from None
    if not (1 <= n <= 12):
        raise ValueError("Row 1–12.")
    return _row(n)


def _element(r, c):
    n, k = r - 1, c - 1
    G = Grid(3, max(k, 1))
    G.grid = [[None] * max(k, 1) for _ in range(3)]
    G.counts = {"value": 1}
    G.add(f"Row {r}, column {c} is C({n}, {k}): start at 1, then {k} multiply-and-divide steps.")
    val = 1
    for i in range(k):
        G.grid[0][i] = n - i
        G.grid[1][i] = i + 1
        val = val * (n - i) // (i + 1)
        G.grid[2][i] = val
        G.add(f"× {n - i}, ÷ {i + 1} → {val}.", 2, i, deps=[(0, i), (1, i)],
              path=[(2, j) for j in range(i + 1)])
        G.counts["value"] = val
    if k == 0:
        G.grid[2][0] = 1
        G.add("Column 1 is always 1.", 2, 0, path=[(2, 0)])
    G.add(f"C({n}, {k}) = {val}.", path=[(2, j) for j in range(max(k, 1))])
    return G.result("pascal_element", val, ["× (n−i)", "÷ (i+1)", "running"],
                    [f"i={i}" for i in range(max(k, 1))])


def _row(n):
    G = Grid(1, n)
    G.grid = [[None] * n]
    G.counts = {"filled": 0}
    G.add(f"Row {n} has {n} entries. The first is 1; each next one is prev · (n − i) / i.")
    val = 1
    G.grid[0][0] = 1
    G.counts["filled"] = 1
    G.add("Entry 1 = 1.", 0, 0, path=[(0, 0)])
    for i in range(1, n):
        val = val * (n - i) // i
        G.grid[0][i] = val
        G.counts["filled"] += 1
        G.add(f"Entry {i + 1} = {G.grid[0][i - 1]} · {n - i} / {i} = {val}.", 0, i,
              deps=[(0, i - 1)], path=[(0, j) for j in range(i + 1)])
    return G.result("pascal_row", G.grid[0][:], ["row"], [str(i + 1) for i in range(n)])
