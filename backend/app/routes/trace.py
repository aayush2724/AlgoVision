from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.tracers import bfs, dijkstra
from app.tracers.common import Graph

router = APIRouter(prefix="/trace", tags=["trace"])

TRACERS = {
    "dijkstra": dijkstra.trace,
    "bfs": bfs.trace,
}


class TraceRequest(BaseModel):
    algorithm: str = "dijkstra"
    start: str = "A"
    graph: Graph


@router.get("/algorithms")
def algorithms():
    return {
        "algorithms": [
            {"id": "dijkstra", "name": "Dijkstra's Shortest Path"},
            {"id": "bfs", "name": "Breadth-First Search"},
        ]
    }


@router.post("")
def run_trace(req: TraceRequest):
    fn = TRACERS.get(req.algorithm)
    if fn is None:
        raise HTTPException(status_code=400, detail=f"Unknown algorithm: {req.algorithm}")
    return fn(req.graph, req.start)
