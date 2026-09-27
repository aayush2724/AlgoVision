"""All-pairs shortest paths on a distance matrix (Step 15).

* floyd_warshall — for each intermediate node k, every pair (i, j) asks: is
  going through k shorter than what we have? dist[i][j] = min(dist[i][j],
  dist[i][k] + dist[k][j]). After all k, the matrix holds every shortest
  distance; a negative diagonal means a negative cycle.
* city_fewest_neighbours — run Floyd–Warshall on an undirected road map, then
  count, for each city, how many others are within the distance threshold;
  the city with the fewest (the later name on ties) wins.

Input is an edge list typed as text — "A>B:3" is a one-way edge, "A-B:3" goes
both ways — because the answer *is* the matrix, drawn on the `grid` view: the
cell being improved is `row`/`col`, the two cells it reads are `deps`, and
row/column k is tinted while it is the intermediate.
"""

from app.tracers.grid_common import Grid

TITLES = {
    "floyd_warshall": "Floyd–Warshall (All-Pairs Shortest Paths)",
    "city_fewest_neighbours": "City With the Fewest Neighbours in Reach",
}
MAX_NODES = 6
INF = "∞"


def parse_edges(text, undirected_only=False):
    tokens = [t for t in (text or "").replace(" ", "").split(",") if t]
    if not tokens:
        raise ValueError("Give edges like A>B:3, B-C:1 (> one way, - both ways).")
    edges, names = [], []
    for t in tokens:
        both = "-" in t.split(":")[0]
        if undirected_only and not both:
            raise ValueError("Roads go both ways here — write them as A-B:3.")
        sep = "-" if both else ">"
        try:
            ends, w = t.split(":")
            a, b = ends.split(sep)
            w = int(w)
        except ValueError:
            raise ValueError(f"'{t}' should look like A>B:3 or A-B:3.") from None
        if not (a.isalnum() and b.isalnum()) or len(a) > 3 or len(b) > 3 or a == b:
            raise ValueError(f"'{t}': node names are 1–3 letters/digits, two different ones.")
        if abs(w) > 999:
            raise ValueError("Weights must be within ±999.")
        for x in (a, b):
            if x not in names:
                names.append(x)
        edges.append((a, b, w))
        if both:
            edges.append((b, a, w))
    if len(names) > MAX_NODES:
        raise ValueError(f"Max {MAX_NODES} nodes so the matrix stays readable.")
    return sorted(names), edges


def run(algo, text, target=None):
    if algo == "floyd_warshall":
        names, edges = parse_edges(text)
        return _floyd(names, edges, "floyd_warshall")
    names, edges = parse_edges(text, undirected_only=True)
    if any(w < 0 for _, _, w in edges):
        raise ValueError("Road lengths can't be negative.")
    if target is None or target != int(target) or not (0 <= target <= 9999):
        raise ValueError("Give the distance threshold (0–9999).")
    return _floyd(names, edges, "city_fewest_neighbours", int(target))


def _floyd(names, edges, algo, threshold=None):
    n = len(names)
    idx = {x: i for i, x in enumerate(names)}
    d = [[0 if i == j else None for j in range(n)] for i in range(n)]
    for a, b, w in edges:
        i, j = idx[a], idx[b]
        if d[i][j] is None or w < d[i][j]:
            d[i][j] = w
    G = Grid(n, n)
    show = lambda v: INF if v is None else v
    G.grid = [[show(v) for v in row] for row in d]
    G.counts = {"improvements": 0, "checks": 0}
    G.add("Start with direct edges only (∞ = no direct edge). For each k, try "
          "routing every pair i→j through k.")
    for k in range(n):
        band = [(k, j) for j in range(n)] + [(i, k) for i in range(n)]
        G.add(f"Intermediate {names[k]}: can any route get shorter by passing "
              f"through {names[k]}? (Row and column {names[k]} tinted.)", deps=band)
        for i in range(n):
            for j in range(n):
                if i == k or j == k or d[i][k] is None or d[k][j] is None:
                    continue
                G.counts["checks"] += 1
                via = d[i][k] + d[k][j]
                if d[i][j] is None or via < d[i][j]:
                    old = show(d[i][j])
                    d[i][j] = via
                    G.grid[i][j] = via
                    G.counts["improvements"] += 1
                    G.add(f"{names[i]}→{names[j]}: via {names[k]} = {d[i][k]} + "
                          f"{d[k][j]} = {via}, better than {old}.", i, j,
                          deps=[(i, k), (k, j)])
    neg = [names[i] for i in range(n) if d[i][i] < 0]
    labels = dict(row_labels=names, col_labels=names)
    if algo == "floyd_warshall":
        if neg:
            G.add(f"Negative diagonal at {', '.join(neg)}: a negative cycle — "
                  f"shortest paths through it are undefined.", match=False)
        else:
            G.add(f"All-pairs shortest distances are final. O(V³): at most "
                  f"{n}³ = {n ** 3} checks.")
        return G.result(algo, [[show(v) for v in row] for row in d],
                        negative_cycle=bool(neg), **labels)
    reach = []
    for i in range(n):
        near = [j for j in range(n) if j != i and d[i][j] is not None
                and d[i][j] <= threshold]
        reach.append(len(near))
        G.add(f"{names[i]} reaches {len(near)} other cit(ies) within "
              f"{threshold}.", i, None, path=[(i, j) for j in near])
    best = min(range(n), key=lambda i: (reach[i], -i))
    G.add(f"Fewest reachable neighbours: {names[best]} ({reach[best]}); ties go "
          f"to the later name.", best, None,
          path=[(best, j) for j in range(n) if j != best and d[best][j] is not None
                and d[best][j] <= threshold])
    return G.result(algo, names[best], reach=dict(zip(names, reach)), **labels)
