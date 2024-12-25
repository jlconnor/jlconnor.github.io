# Python Code Snippets

## Prim's Algorithm

```python
from dataclasses import dataclass
from itertools import combinations, count
from typing import Dict, Iterator, List, Set, Tuple
import heapq

@dataclass(frozen=True)
class Edge:
    """Immutable edge representation with weight"""
    start: str
    end: str
    weight: float

    def __lt__(self, other: 'Edge') -> bool:
        return self.weight < other.weight

class Graph:
    """Graph representation optimized for Prim's algorithm"""
    def __init__(self, edges: List[Edge]):
        self._adjacency: Dict[str, List[Edge]] = {}
        self._build_adjacency_list(edges)

    def _build_adjacency_list(self, edges: List[Edge]) -> None:
        """Builds adjacency list representation from edges"""
        for edge in edges:
            # Add edge in both directions since graph is undirected
            self._adjacency.setdefault(edge.start, []).append(edge)
            self._adjacency.setdefault(edge.end, []).append(
                Edge(edge.end, edge.start, edge.weight)
            )

    def get_edges(self, vertex: str) -> Iterator[Edge]:
        """Returns iterator of edges connected to vertex"""
        return iter(self._adjacency.get(vertex, []))

def find_minimum_spanning_tree(edges: List[Edge]) -> List[Edge]:
    """
    Implements Prim's algorithm using a priority queue and itertools

    Args:
        edges: List of Edge objects representing the graph

    Returns:
        List of Edge objects in the minimum spanning tree
    """
    if not edges:
        return []

    graph = Graph(edges)
    mst: List[Edge] = []
    visited: Set[str] = set()

    # Start from first vertex we find
    start = edges[0].start
    visited.add(start)

    # Use priority queue for efficient minimum edge finding
    edge_queue: List[Edge] = []

    # Add all edges from starting vertex
    for edge in graph.get_edges(start):
        heapq.heappush(edge_queue, edge)

    # Keep track of number of vertices we've processed
    vertices_processed = count(start=1)

    # Continue until we've visited all vertices or run out of edges
    while edge_queue and next(vertices_processed) < len(graph._adjacency):
        # Get minimum weight edge
        edge = heapq.heappop(edge_queue)

        # Skip if we've already visited this vertex
        if edge.end in visited:
            continue

        # Add to MST and mark as visited
        mst.append(edge)
        visited.add(edge.end)

        # Add all edges from new vertex
        for next_edge in graph.get_edges(edge.end):
            if next_edge.end not in visited:
                heapq.heappush(edge_queue, next_edge)

    return mst

edges = [
    Edge("A", "B", 4),
    Edge("A", "C", 1),
    Edge("B", "C", 3),
    Edge("B", "D", 2),
    Edge("C", "D", 5)
]
mst = find_minimum_spanning_tree(edges)
```
