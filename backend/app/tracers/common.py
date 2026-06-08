from typing import Optional

from pydantic import BaseModel


class GNode(BaseModel):
    id: str
    x: float = 0.0
    y: float = 0.0


class Graph(BaseModel):
    nodes: list[GNode]
    edges: list[list]  # [a, b] or [a, b, weight]


def adjacency(graph: Graph):
    adj: dict[str, list] = {n.id: [] for n in graph.nodes}
    for e in graph.edges:
        a, b = e[0], e[1]
        w = float(e[2]) if len(e) > 2 else 1.0
        adj.setdefault(a, []).append((b, w))
        adj.setdefault(b, []).append((a, w))
    return adj
