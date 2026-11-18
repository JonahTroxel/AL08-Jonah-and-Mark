"""AL08 workshop access planner: traversals and fewest-hop routes."""

from collections import deque

from app_runner import run
from network_support import record_step, validate_request

STAGE = 3  # Keep at 1 for Monday, 2 for Tuesday, and 3 for Thursday.
MY_RESTRICTION = "A"  # Change to the case assigned by your instructor.


def breadth_first(graph, start):
    """Return BFS order, independent snapshots, and adjacency entries examined."""
    validate_request(graph, start)
    order = []
    trace = []
    edges_examined = 0
    discovered = {start}
    frontier = deque([start])

    while frontier:
        node = frontier.popleft()
        order.append(node)
        for neighbor in graph[node]:
            edges_examined += 1
            if neighbor not in discovered:
                discovered.add(neighbor)
                frontier.append(neighbor)
        record_step(trace, node, frontier, discovered)

    return order, trace, edges_examined


def depth_first(graph, start):
    """Return iterative DFS order, independent snapshots, and adjacency count."""
    validate_request(graph, start)
    order = []
    trace = []
    edges_examined = 0
    visited = set()
    frontier = [start]

    while frontier:
        node = frontier.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for neighbor in reversed(graph[node]):
            edges_examined += 1
            if neighbor not in visited:
                frontier.append(neighbor)
        record_step(trace, node, frontier, visited)

    return order, trace, edges_examined


def reconstruct_path(parents, goal):
    """Return start-to-goal order by following the BFS parent chain."""
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parents[node]
    path.reverse()
    return path


def shortest_hop_path(graph, start, goal, blocked=()):
    """Return a permitted fewest-hop path and parents, or None with parent state."""
    blocked_nodes = set(blocked)
    validate_request(graph, start, goal, blocked_nodes)
    if start in blocked_nodes or goal in blocked_nodes:
        return None, {}

    parents = {start: None}
    frontier = deque([start])
    while frontier:
        node = frontier.popleft()
        if node == goal:
            return reconstruct_path(parents, goal), parents
        for neighbor in graph[node]:
            if neighbor not in parents and neighbor not in blocked_nodes:
                parents[neighbor] = node
                frontier.append(neighbor)

    return None, parents


def main():
    """Run only the selected completed stage using supplied presentation."""
    run(STAGE, breadth_first, depth_first, shortest_hop_path, MY_RESTRICTION)


if __name__ == "__main__":
    main()
