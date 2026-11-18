"""Supplied readable model, traversal, and route output with shared colors."""

from textwrap import fill
from console_style import color_text, print_color


def show_model(graph):
    """Display direct connections with a readable explanation for an empty list."""
    print_color("WORKSHOP ACCESS PLANNER", "heading")
    print("Rooms are nodes; a connection means an allowed direct passage.")
    print("The supplied model is fictional, two-way and unweighted.\n")
    for node, neighbors in graph.items():
        room = color_text(node, "code")
        if neighbors:
            connections = color_text(", ".join(neighbors), "success")
            print(f"  {room}: {connections}")
        else:
            unavailable = color_text("No direct connections", "caution")
            print(f"  {room}: {unavailable}")


def show_model_result(errors):
    """Report the supplied connection check without exposing raw error collections."""
    if not errors:
        print_color("\nConnection checks passed.", "success")
    else:
        print_color("\nPlease correct the model:", "caution")
        for error in errors:
            print("  - " + error)


def show_list(label, values, color="code"):
    """Wrap room names to keep the report readable in a normal console window."""
    text = ", ".join(values)
    if not text:
        text = "(empty)"
    print_color(fill(label + text, width=88, subsequent_indent="    "), color)


def show_traversal(label, order, trace, edges, seen_label):
    """Show inspection order and the first four purposeful teaching snapshots."""
    print_color("\n" + label, "heading")
    show_list("Inspection order: ", order, "success")
    print_color(f"Adjacency entries examined: {edges}", "code")
    for index, step in enumerate(trace[:4], start=1):
        print_color(f"  Step {index}: inspected {step['processed']}", "heading")
        show_list("    Pending (stored order): ", step["pending"])
        show_list("    " + seen_label + " (alphabetical): ", step["seen"])
    print_color("Only the first four new-visit snapshots are shown.", "caution")


def show_route(label, path):
    """Present a connected route/hop count or a clear unavailable-route result."""
    print_color("\n" + label, "heading")
    if path is None:
        print_color("No permitted route is available.", "caution")
    else:
        print_color("Route: " + " -> ".join(path), "success")
        print_color(f"Direct passages: {len(path) - 1}", "code")
