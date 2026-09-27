"""Computational geometry (batch 82) on the `grid` view, used as a coordinate
plane: column = x, row = y (drawn with y increasing upward).

* convex_hull — Andrew's monotone chain: sort points by x, then build the
  lower and upper chains with a stack; pop while the last turn is not a
  strict left turn (cross product ≤ 0).
* polygon_area — shoelace formula: area = ½·|Σ (xᵢ·yᵢ₊₁ − xᵢ₊₁·yᵢ)|.
* closest_pair — divide and conquer: split by x, solve both halves, then
  only points within d of the split line (the strip) can do better, and
  each needs to be checked against at most a few neighbours by y.
"""

import math

from app.tracers.grid_common import Grid

TITLES = {
    "convex_hull": "Convex Hull (Monotone Chain)",
    "polygon_area": "Polygon Area (Shoelace Formula)",
    "closest_pair": "Closest Pair of Points (Divide & Conquer)",
}


def _points(text, lo, hi):
    pts = []
    for part in [p.strip() for p in (text or "").split(";") if p.strip()]:
        try:
            x, y = (int(v) for v in part.replace(",", " ").split())
        except ValueError:
            raise ValueError("Points look like '0 0; 3 1; 2 4' (x y, separated by ';').") from None
        if not (0 <= x <= 9 and 0 <= y <= 9):
            raise ValueError("Keep coordinates within 0–9.")
        pts.append((x, y))
    if not (lo <= len(pts) <= hi):
        raise ValueError(f"Give {lo}–{hi} points.")
    return pts


def run(algo, text, target=None):
    if algo == "convex_hull":
        return _hull(sorted(set(_points(text, 1, 12))))
    pts = _points(text, 3 if algo == "polygon_area" else 2, 10)
    if len(set(pts)) != len(pts):
        raise ValueError("Points must be distinct.")
    return (_area if algo == "polygon_area" else _closest)(pts)


def _plane(pts):
    W = max(x for x, _ in pts) + 1
    H = max(y for _, y in pts) + 1
    G = Grid(H, W)
    cell = lambda p: (H - 1 - p[1], p[0])
    return G, cell, [str(H - 1 - r) for r in range(H)], [str(c) for c in range(W)]


def _cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _hull(pts):
    G, cell, rows, cols = _plane(pts)
    for p in pts:
        r, c = cell(p)
        G.grid[r][c] = "•"
    G.counts = {"cross_products": 0, "pops": 0}
    G.add("Sort the points left to right. Build the LOWER chain with a stack: "
          "before pushing a point, pop while the last two stack points and it "
          "do not make a strict left (counter-clockwise) turn. Then the UPPER "
          "chain the same way, right to left.")
    if len(pts) < 3:
        G.add(f"Fewer than 3 distinct points — the hull is just {pts}.",
              path=[cell(p) for p in pts])
        return G.result("convex_hull", [list(p) for p in pts], rows, cols)

    def chain(seq, name):
        st = []
        for p in seq:
            while len(st) >= 2:
                cr = _cross(st[-2], st[-1], p)
                G.counts["cross_products"] += 1
                if cr > 0:
                    break
                G.counts["pops"] += 1
                G.add(f"{name}: {st[-2]} → {st[-1]} → {p} turns "
                      f"{'right' if cr < 0 else 'straight'} (cross {cr}) — pop {st[-1]}.",
                      *cell(p), [cell(q) for q in st], match=False)
                st.pop()
            st.append(p)
            G.add(f"{name}: push {p}. Chain {st}.", *cell(p), [], [cell(q) for q in st])
        return st

    lower = chain(pts, "Lower")
    upper = chain(pts[::-1], "Upper")
    hull = lower[:-1] + upper[:-1]
    for i, p in enumerate(hull):
        r, c = cell(p)
        G.grid[r][c] = i
    G.add(f"Join the chains (dropping repeated ends): {len(hull)} hull vertices, "
          f"counter-clockwise, numbered in order.", path=[cell(p) for p in hull])
    return G.result("convex_hull", [list(p) for p in hull], rows, cols)


def _area(pts):
    G, cell, rows, cols = _plane(pts)
    for i, p in enumerate(pts):
        r, c = cell(p)
        G.grid[r][c] = i
    G.counts = {"terms": 0}
    G.add("Vertices are numbered in the order given. Walk around the polygon: "
          "each edge (xᵢ, yᵢ) → (xᵢ₊₁, yᵢ₊₁) adds xᵢ·yᵢ₊₁ − xᵢ₊₁·yᵢ, the signed "
          "(doubled) area of the triangle it makes with the origin.")
    total, n = 0, len(pts)
    for i in range(n):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        term = x1 * y2 - x2 * y1
        total += term
        G.counts["terms"] += 1
        G.add(f"Edge {i} → {(i + 1) % n}: {x1}·{y2} − {x2}·{y1} = {term}. Running sum "
              f"{total}.", *cell(pts[(i + 1) % n]), [cell(pts[i])],
              [cell(p) for p in pts[:i + 1]])
    area = abs(total) / 2
    G.add(f"Area = |{total}| / 2 = {area:g}"
          + (" (the sum was negative: the vertices run clockwise)." if total < 0 else "."),
          path=[cell(p) for p in pts])
    return G.result("polygon_area", area, rows, cols)


def _closest(pts):
    G, cell, rows, cols = _plane(pts)
    for p in pts:
        r, c = cell(p)
        G.grid[r][c] = "•"
    G.counts = {"distance_checks": 0}
    G.add("Sort by x and split in half. Solve each half, take the smaller "
          "distance d, then look only at points within d of the dividing line.")
    dist = lambda a, b: math.hypot(a[0] - b[0], a[1] - b[1])

    def solve(p):
        if len(p) <= 3:
            best = (math.inf, None)
            for i in range(len(p)):
                for j in range(i + 1, len(p)):
                    G.counts["distance_checks"] += 1
                    d = dist(p[i], p[j])
                    if d < best[0]:
                        best = (d, (p[i], p[j]))
            if best[1]:
                G.add(f"Small group {p}: check every pair — best {best[0]:.3f} "
                      f"between {best[1][0]} and {best[1][1]}.", None, None,
                      [cell(q) for q in p], [cell(q) for q in best[1]])
            return best
        mid = len(p) // 2
        mx = p[mid][0]
        G.add(f"Split {len(p)} points at x = {mx}.", None, None,
              [cell(q) for q in p if q[0] == mx])
        best = min(solve(p[:mid]), solve(p[mid:]), key=lambda t: t[0])
        strip = sorted([q for q in p if abs(q[0] - mx) < best[0]], key=lambda q: q[1])
        improved = False
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if strip[j][1] - strip[i][1] >= best[0]:
                    break
                G.counts["distance_checks"] += 1
                d = dist(strip[i], strip[j])
                if d < best[0]:
                    best, improved = (d, (strip[i], strip[j])), True
        G.add(f"Strip around x = {mx} (width ±{best[0]:.3f}): {len(strip)} point(s) "
              + ("— a closer pair crosses the line!" if improved else
                 "— nothing closer across the line."), None, None,
              [cell(q) for q in strip], [cell(q) for q in best[1]])
        return best

    d, pair = solve(sorted(pts))
    G.add(f"Closest pair: {pair[0]} and {pair[1]}, distance {d:.4f}.",
          path=[cell(q) for q in pair])
    return G.result("closest_pair", [round(d, 4), [list(pair[0]), list(pair[1])]], rows, cols)
