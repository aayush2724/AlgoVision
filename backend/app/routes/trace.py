from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from app.tracers import bfs, dijkstra
from app.tracers.common import Graph
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/trace", tags=["trace"])

TRACERS = {
    "dijkstra": dijkstra.trace,
    "bfs": bfs.trace,
}

class TraceRequest(BaseModel):
    algorithm: str  = Field(default="dijkstra", max_length=32)
    start:     str  = Field(default="A",        max_length=32)
    graph:     Graph

@router.get("/algorithms")
def algorithms():
    return {
        "algorithms": [
            {"id": "dijkstra", "name": "Dijkstra's Shortest Path"},
            {"id": "bfs", "name": "Breadth-First Search"},
        ]
    }

# 30 traces per minute — tracer is CPU-bound
@router.post("")
@limiter.limit("30/minute")
def run_trace(request: Request, req: TraceRequest):
    import re
    fn = TRACERS.get(req.algorithm)
    if fn is None:
      raise HTTPException(
        status_code=400,
        detail=f"Algorithm must be one of: {', '.join(TRACERS.keys())}"
      )
    # Validate start node exists in graph
    node_ids = {n.id for n in req.graph.nodes}
    if req.start not in node_ids:
      raise HTTPException(
        status_code=400,
        detail=f"Start node '{req.start}' not found in graph nodes."
      )
    # Sanitise algorithm name (already constrained by TRACERS dict lookup,
    # but belt-and-braces)
    if not re.match(r'^[a-z_]{1,32}$', req.algorithm):
      raise HTTPException(status_code=400, detail="Invalid algorithm name.")
    return fn(req.graph, req.start)
