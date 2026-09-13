from pydantic import BaseModel, Field, model_validator

MAX_NODES = 50
MAX_EDGES = 200

class GNode(BaseModel):
  id: str = Field(max_length=32)
  x:  float = 0.0
  y:  float = 0.0

class Graph(BaseModel):
  nodes: list[GNode] = Field(max_length=MAX_NODES)
  edges: list[list]  = Field(max_length=MAX_EDGES)

  @model_validator(mode="after")
  def validate_edges(self):
    node_ids = {n.id for n in self.nodes}
    for e in self.edges:
      if len(e) < 2 or len(e) > 3:
        raise ValueError("Each edge must be [nodeA, nodeB] or [nodeA, nodeB, weight]")
      a, b = str(e[0]), str(e[1])
      if a not in node_ids or b not in node_ids:
        raise ValueError(f"Edge references unknown node: {a!r} or {b!r}")
      if len(e) == 3:
        try:
          w = float(e[2])
        except (TypeError, ValueError):
          raise ValueError(f"Edge weight must be a number, got: {e[2]!r}")
        # Negative weights are allowed (Bellman-Ford / Floyd-Warshall need
        # them); algorithms that require non-negative weights — Dijkstra, Prim,
        # Kruskal — reject negatives themselves in the route layer.
        if w < -1_000_000 or w > 1_000_000:
          raise ValueError(f"Edge weight {w} out of range [-1000000, 1000000]")
    return self

def adjacency(graph: Graph):
  adj: dict[str, list] = {n.id: [] for n in graph.nodes}
  for e in graph.edges:
    a, b = str(e[0]), str(e[1])
    w = float(e[2]) if len(e) > 2 else 1.0
    adj[a].append((b, w))
    adj[b].append((a, w))
  return adj

def directed_adjacency(graph: Graph):
  """Edges read as directed a -> b — for algorithms whose whole point is
  direction (Bellman-Ford, Floyd-Warshall), the way topological_sort already
  reads them."""
  adj: dict[str, list] = {n.id: [] for n in graph.nodes}
  for e in graph.edges:
    a, b = str(e[0]), str(e[1])
    w = float(e[2]) if len(e) > 2 else 1.0
    adj[a].append((b, w))
  return adj

def edge_list(graph: Graph):
  """Directed edges as (a, b, w) triples — Bellman-Ford relaxes over these."""
  out = []
  for e in graph.edges:
    a, b = str(e[0]), str(e[1])
    w = float(e[2]) if len(e) > 2 else 1.0
    out.append((a, b, w))
  return out
