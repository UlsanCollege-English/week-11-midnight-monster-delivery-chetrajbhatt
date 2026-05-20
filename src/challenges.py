"""Week 11: Midnight Monster Delivery.
 
Implement Dijkstra's algorithm using a heap-based priority queue.
 
Rules:
- Use Python 3.11+.
- Use the standard library only.
- Use heapq for the priority queue.
- Edge weights must be positive.
"""
 
import heapq
from math import inf
 
 
HAUNTED_CITY = {
    "Crypt Kitchen": {
        "Fog Alley": 2,
        "Bone Bridge": 5,
    },
    "Fog Alley": {
        "Moon Bridge": 1,
        "Goblin Market": 6,
    },
    "Bone Bridge": {
        "Goblin Market": 2,
    },
    "Moon Bridge": {
        "Werewolf Den": 5,
        "Goblin Market": 3,
    },
    "Goblin Market": {
        "Vampire Tower": 5,
    },
    "Werewolf Den": {
        "Vampire Tower": 2,
    },
    "Vampire Tower": {},
}
 
 
def validate_haunted_map(graph: dict[str, dict[str, int]]) -> None:
    """Raise ValueError if the haunted map is invalid.
 
    A valid haunted map:
    - is a dictionary
    - each node maps to a dictionary of neighbors
    - every neighbor is also a node in the graph
    - every edge weight is positive
 
    Args:
        graph: Weighted graph represented as an adjacency dictionary.
 
    Raises:
        ValueError: If the graph is invalid.
    """
    if not isinstance(graph, dict):
        raise ValueError("Graph must be a dictionary.")
 
    for node, neighbors in graph.items():
        if not isinstance(neighbors, dict):
            raise ValueError(
                f"Node '{node}' must map to a dictionary of neighbors."
            )
        for neighbor, weight in neighbors.items():
            if neighbor not in graph:
                raise ValueError(
                    f"Neighbor '{neighbor}' of '{node}' is not a node in the graph."
                )
            if not isinstance(weight, int | float) or weight <= 0:
                raise ValueError(
                    f"Edge weight from '{node}' to '{neighbor}' must be a positive number, got {weight!r}."
                )
 
 
def monster_delivery_costs(
    graph: dict[str, dict[str, int]],
    start: str,
) -> dict[str, float]:
    """Return the cheapest delivery cost from start to every location.
 
    Use Dijkstra's algorithm with heapq.
 
    Args:
        graph: Weighted graph represented as an adjacency dictionary.
        start: Starting location.
 
    Returns:
        Dictionary mapping each location to its cheapest known cost.
        Unreachable locations should stay as math.inf.
 
    Raises:
        ValueError: If the graph is invalid or start is missing.
    """
    validate_haunted_map(graph)
    if start not in graph:
        raise ValueError(f"Start location '{start}' is not in the graph.")
 
    # Initialise all distances to infinity, then set start to 0.
    distances: dict[str, float] = {node: inf for node in graph}
    distances[start] = 0
 
    # Min-heap stores (cost, node). Start with cost 0 at the start node.
    frontier: list[tuple[float, str]] = [(0, start)]
 
    while frontier:
        current_cost, current_node = heapq.heappop(frontier)
 
        # Skip stale entries — a cheaper path was already found.
        if current_cost > distances[current_node]:
            continue
 
        # Relaxation: update neighbours if a cheaper path is found.
        for neighbor, weight in graph[current_node].items():
            new_cost = current_cost + weight
            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                heapq.heappush(frontier, (new_cost, neighbor))
 
    return distances
 
 
def shortest_monster_delivery(
    graph: dict[str, dict[str, int]],
    start: str,
    target: str,
) -> tuple[float, list[str]]:
    """Return the cheapest cost and path from start to target.
 
    Use Dijkstra's algorithm with heapq and reconstruct the path using
    a previous-node map.
 
    Args:
        graph: Weighted graph represented as an adjacency dictionary.
        start: Starting location.
        target: Destination location.
 
    Returns:
        (cost, path), where path is in start-to-target order.
        If start or target is missing, return (math.inf, []).
        If target is unreachable, return (math.inf, []).
        If start equals target, return (0, [start]).
    """
    validate_haunted_map(graph)
 
    # Missing start or target: return sentinel immediately.
    if start not in graph or target not in graph:
        return (inf, [])
 
    if start == target:
        return (0, [start])
 
    distances: dict[str, float] = {node: inf for node in graph}
    distances[start] = 0
 
    # prev tracks which node we arrived from on the cheapest path.
    prev: dict[str, str | None] = {node: None for node in graph}
 
    frontier: list[tuple[float, str]] = [(0, start)]
 
    while frontier:
        current_cost, current_node = heapq.heappop(frontier)
 
        # Early exit once we've settled the target.
        if current_node == target:
            break
 
        if current_cost > distances[current_node]:
            continue
 
        for neighbor, weight in graph[current_node].items():
            new_cost = current_cost + weight
            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                prev[neighbor] = current_node
                heapq.heappush(frontier, (new_cost, neighbor))
 
    # Target is unreachable.
    if distances[target] == inf:
        return (inf, [])
 
    # Reconstruct path by walking backwards through prev.
    path: list[str] = []
    node: str | None = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
 
    return (distances[target], path)
 
 
def best_next_monster_stop(
    graph: dict[str, dict[str, int]],
    start: str,
    targets: list[str],
) -> tuple[str, float]:
    """Return the reachable target with the cheapest delivery cost.
 
    Stretch challenge.
 
    Rules:
    - Ignore unreachable targets.
    - If no target is reachable, return ("", math.inf).
    - If there is a tie, return the target that appears first in targets.
 
    Args:
        graph: Weighted graph represented as an adjacency dictionary.
        start: Starting location.
        targets: Possible destination locations.
 
    Returns:
        A tuple of (target, cost).
    """
    # Run Dijkstra once from start, then look up each target's cost.
    if start not in graph:
        return ("", inf)
 
    all_costs = monster_delivery_costs(graph, start)
 
    best_target = ""
    best_cost: float = inf
 
    for t in targets:
        cost = all_costs.get(t, inf)
        # Strict less-than preserves first-in-list tie-breaking.
        if cost < best_cost:
            best_cost = cost
            best_target = t
 
    return (best_target, best_cost)