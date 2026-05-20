# 🎃 Week 11: Midnight Monster Delivery

A spooky implementation of **Dijkstra's shortest-path algorithm** using Python's `heapq` module. Find the cheapest delivery routes through a haunted city — from Crypt Kitchen to Vampire Tower and everywhere in between.

## Overview

This module provides three functions for navigating a weighted directed graph representing a haunted city. All functions use a min-heap priority queue for efficient pathfinding.

**Constraints:**
- Python 3.11+
- Standard library only (`heapq`, `math`)
- Edge weights must be positive integers or floats

## The Haunted City Map

```
Crypt Kitchen ──(2)──▶ Fog Alley ──(1)──▶ Moon Bridge ──(5)──▶ Werewolf Den
      │                    │                    │                     │
     (5)                  (6)                  (3)                   (2)
      ▼                    ▼                    ▼                     ▼
 Bone Bridge ──(2)──▶ Goblin Market ◀──────────┘              Vampire Tower
                            │                                        ▲
                           (5)                                       │
                            └────────────────────────────────────────┘
```

## API Reference

### `validate_haunted_map(graph)`

Validates the structure of a graph before pathfinding.

```python
validate_haunted_map(HAUNTED_CITY)  # passes silently if valid
```

**Raises `ValueError` if:**
- `graph` is not a dictionary
- Any node's value is not a dictionary
- Any neighbor is not a node in the graph
- Any edge weight is not a positive number

---

### `monster_delivery_costs(graph, start) → dict[str, float]`

Returns the **cheapest cost from `start` to every node** in the graph.

```python
costs = monster_delivery_costs(HAUNTED_CITY, "Crypt Kitchen")
# {
#   "Crypt Kitchen":  0,
#   "Fog Alley":      2,
#   "Bone Bridge":    5,
#   "Moon Bridge":    3,
#   "Goblin Market":  6,
#   "Werewolf Den":   8,
#   "Vampire Tower": 10,
# }
```

Unreachable nodes are returned with a cost of `math.inf`.

**Raises `ValueError`** if the graph is invalid or `start` is not in the graph.

---

### `shortest_monster_delivery(graph, start, target) → tuple[float, list[str]]`

Returns the **cheapest cost and the full path** from `start` to `target`.

```python
cost, path = shortest_monster_delivery(HAUNTED_CITY, "Crypt Kitchen", "Vampire Tower")
# (10, ["Crypt Kitchen", "Fog Alley", "Moon Bridge", "Werewolf Den", "Vampire Tower"])
```

| Scenario | Returns |
|---|---|
| Normal reachable path | `(cost, [start, ..., target])` |
| `start == target` | `(0, [start])` |
| `start` or `target` not in graph | `(inf, [])` |
| Target unreachable | `(inf, [])` |

---

### `best_next_monster_stop(graph, start, targets) → tuple[str, float]`

*(Stretch challenge)* Given a list of candidate destinations, returns the **reachable target with the lowest cost** from `start`.

```python
best, cost = best_next_monster_stop(
    HAUNTED_CITY,
    "Crypt Kitchen",
    ["Vampire Tower", "Goblin Market", "Werewolf Den"]
)
# ("Goblin Market", 6)
```

- Ignores unreachable targets
- Tie-breaking: returns the target that appears **first** in the `targets` list
- Returns `("", math.inf)` if no target is reachable

## Algorithm Notes

All pathfinding functions implement **Dijkstra's algorithm** with:

- **Min-heap** (`heapq`) for O(log n) priority queue operations
- **Lazy deletion** — stale heap entries are skipped via the `current_cost > distances[node]` guard
- **Early exit** in `shortest_monster_delivery` once the target node is settled
- **Predecessor map** (`prev`) in `shortest_monster_delivery` for O(n) path reconstruction

**Time complexity:** O((V + E) log V)  
**Space complexity:** O(V + E)

## Running the Code

```bash
python solution.py
```

To experiment interactively:

```python
from solution import monster_delivery_costs, shortest_monster_delivery, HAUNTED_CITY

costs = monster_delivery_costs(HAUNTED_CITY, "Crypt Kitchen")
cost, path = shortest_monster_delivery(HAUNTED_CITY, "Crypt Kitchen", "Vampire Tower")
print(f"Cost: {cost}, Path: {' → '.join(path)}")
```
