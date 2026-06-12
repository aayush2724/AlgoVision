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
          if w < 0 or w > 1_000_000:
            raise ValueError(f"Edge weight {w} out of range [0, 1000000]")
        except (TypeError, ValueError):
          raise ValueError(f"Edge weight must be a number, got: {e[2]!r}")
    return self

def adjacency(graph: Graph):
  adj: dict[str, list] = {n.id: [] for n in graph.nodes}
  for e in graph.edges:
    a, b = str(e[0]), str(e[1])
    w = float(e[2]) if len(e) > 2 else 1.0
    adj[a].append((b, w))
    adj[b].append((a, w))
  return adj
