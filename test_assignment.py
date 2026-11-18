"""Focused checks for the AL08 model, traversals, and route contracts."""

from copy import deepcopy

from main import (
    MY_RESTRICTION,
    breadth_first,
    depth_first,
    reconstruct_path,
    shortest_hop_path,
)
from network_data import GOAL, GRAPH, RESTRICTIONS, START
from network_support import validate_model

TEST_STAGE = 3  # Keep at 1 for Monday, 2 for Tuesday, and 3 for Thursday.


def test_model():
    """Check a valid model, diagnose a broken copy, and preserve the fixture."""
    original = deepcopy(GRAPH)
    assert validate_model(GRAPH) == []

    broken = {node: neighbors[:] for node, neighbors in GRAPH.items()}
    broken["Reception"].remove("Office")
    assert "Office->Reception: missing reciprocal connection" in validate_model(broken)
    broken["Entrance"].append("UnknownRoom")
    errors = validate_model(broken)
    assert "Entrance: unknown node UnknownRoom" in errors

    broken["Reception"].append("Office")
    broken["Entrance"].remove("UnknownRoom")
    assert validate_model(broken) == []
    assert GRAPH == original


def test_traversals():
    """Check listed-neighbor traversal order, edge counts, and source preservation."""
    tiny = {"A": ["B", "C"], "B": ["A"], "C": ["A"], "D": []}
    original = deepcopy(tiny)

    bfs_order, bfs_trace, bfs_edges = breadth_first(tiny, "A")
    assert bfs_order == ["A", "B", "C"]
    assert bfs_edges == 4
    assert len(bfs_trace) == len(bfs_order)
    assert bfs_trace[0] == {
        "processed": "A",
        "pending": ["B", "C"],
        "seen": ["A", "B", "C"],
    }

    dfs_order, dfs_trace, dfs_edges = depth_first(tiny, "A")
    assert dfs_order == ["A", "B", "C"]
    assert dfs_edges == 4
    assert len(dfs_trace) == len(dfs_order)
    assert dfs_trace[0] == {
        "processed": "A",
        "pending": ["C", "B"],
        "seen": ["A"],
    }

    assert breadth_first(tiny, "D")[0:3:2] == (["D"], 0)
    assert depth_first(tiny, "D")[0:3:2] == (["D"], 0)
    assert tiny == original

    full_bfs, _, full_bfs_edges = breadth_first(GRAPH, START)
    full_dfs, _, full_dfs_edges = depth_first(GRAPH, START)
    assert len(full_bfs) == 11 and len(set(full_bfs)) == 11
    assert len(full_dfs) == 11 and len(set(full_dfs)) == 11
    assert "Annex" not in full_bfs and "Annex" not in full_dfs
    assert full_bfs_edges == full_dfs_edges == 26

    try:
        breadth_first(tiny, "Missing")
    except ValueError as error:
        assert "Unknown start: Missing" in str(error)
    else:
        raise AssertionError("An unknown start should raise ValueError.")


def _assert_valid_route(graph, start, goal, blocked, path):
    """Check route endpoints, permitted rooms, and each direct passage."""
    assert path[0] == start
    assert path[-1] == goal
    assert not (set(path) & set(blocked))
    for current, following in zip(path, path[1:]):
        assert following in graph[current]


def test_paths_and_personal_case():
    """Check route edge cases and the expected outputs for all issued cases."""
    original = deepcopy(GRAPH)
    path, parents = shortest_hop_path(GRAPH, START, GOAL)
    assert path == ["Entrance", "Reception", "Office", "Loading"]
    assert len(path) - 1 == 3
    _assert_valid_route(GRAPH, START, GOAL, (), path)

    same_node_path, same_node_parents = shortest_hop_path(GRAPH, "Annex", "Annex")
    assert same_node_path == ["Annex"]
    assert same_node_parents == {"Annex": None}

    unreachable_path, unreachable_parents = shortest_hop_path(GRAPH, START, "Annex")
    assert unreachable_path is None
    assert set(unreachable_parents) == set(GRAPH) - {"Annex"}
    assert unreachable_parents[START] is None

    blocked_start, blocked_start_parents = shortest_hop_path(
        GRAPH, START, GOAL, [START]
    )
    blocked_goal, blocked_goal_parents = shortest_hop_path(
        GRAPH, START, GOAL, [GOAL]
    )
    assert (blocked_start, blocked_start_parents) == (None, {})
    assert (blocked_goal, blocked_goal_parents) == (None, {})

    assert reconstruct_path(parents, GOAL) == path
    assert parents[START] is None

    expected_cases = {
        "A": (
            ["Entrance", "Reception", "Hallway", "Assembly", "Inspection", "Packing", "Loading"],
            6,
        ),
        "B": (None, None),
        "C": (["Entrance", "Reception", "Office", "Loading"], 3),
    }
    for case, (expected_path, expected_hops) in expected_cases.items():
        blocked = RESTRICTIONS[case]["blocked"]
        actual_path, _ = shortest_hop_path(GRAPH, START, GOAL, blocked)
        assert actual_path == expected_path
        if actual_path is not None:
            _assert_valid_route(GRAPH, START, GOAL, blocked, actual_path)
            assert len(actual_path) - 1 == expected_hops

    personal_blocked = RESTRICTIONS[MY_RESTRICTION]["blocked"]
    personal_path, _ = shortest_hop_path(GRAPH, START, GOAL, personal_blocked)
    assert personal_path == expected_cases[MY_RESTRICTION][0]
    assert GRAPH == original


if __name__ == "__main__":
    test_model()
    if TEST_STAGE >= 2:
        test_traversals()
    if TEST_STAGE >= 3:
        test_paths_and_personal_case()
    print("Selected-stage checks passed.")
