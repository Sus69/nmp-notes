"""Practical 1: Implementation of Uninformed Search Algorithms (BFS and DFS).

Course: Artificial Intelligence Lab
Subject Code: AI-LAB-01
Name: [Your Name]
Roll Number: [Your Roll Number]
Date: [DD/MM/YYYY]

Problem Statement:
Given an undirected/directed graph represented as an adjacency list, implement:
1. Breadth-First Search (BFS) to find the shortest path in an unweighted graph.
2. Depth-First Search (DFS) to explore paths recursively.
"""

from collections import deque
from typing import Dict, List, Optional, Set


def bfs(graph: Dict[str, List[str]], start_node: str, goal_node: Optional[str] = None) -> List[str]:
    """Perform Breadth-First Search (BFS) starting from `start_node`.

    Parameters:
        graph: Adjacency list representation of the graph.
        start_node: Node from which search begins.
        goal_node: Optional target node to terminate search early.

    Returns:
        List of nodes in the order they were visited.
    """
    if start_node not in graph:
        raise ValueError(f"Start node '{start_node}' not present in graph.")

    visited: Set[str] = set()
    queue: deque[str] = deque([start_node])
    traversal_order: List[str] = []

    visited.add(start_node)

    while queue:
        current_node = queue.popleft()
        traversal_order.append(current_node)

        if goal_node and current_node == goal_node:
            print(f"[BFS] Goal node '{goal_node}' found!")
            break

        for neighbor in graph.get(current_node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return traversal_order


def dfs(
    graph: Dict[str, List[str]],
    current_node: str,
    visited: Optional[Set[str]] = None,
    traversal_order: Optional[List[str]] = None,
) -> List[str]:
    """Perform recursive Depth-First Search (DFS) starting from `current_node`.

    Parameters:
        graph: Adjacency list representation of the graph.
        current_node: Current node being visited.
        visited: Set tracking visited nodes.
        traversal_order: List tracking exploration order.

    Returns:
        List of nodes in the order they were visited.
    """
    if visited is None:
        visited = set()
    if traversal_order is None:
        traversal_order = []

    visited.add(current_node)
    traversal_order.append(current_node)

    for neighbor in graph.get(current_node, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited, traversal_order)

    return traversal_order


def main() -> None:
    """Sample driver code to demonstrate BFS and DFS traversals."""
    # Sample Graph:
    #      A
    #     / \
    #    B   C
    #   / \   \
    #  D   E   F
    sample_graph: Dict[str, List[str]] = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "F"],
        "D": ["B"],
        "E": ["B"],
        "F": ["C"],
    }

    print("=" * 50)
    print("Practical 1: Breadth-First Search & Depth-First Search")
    print("=" * 50)

    start = "A"
    print(f"\nStarting node: {start}")

    # BFS Traversal
    bfs_result = bfs(sample_graph, start_node=start)
    print(f"BFS Traversal Order: {' -> '.join(bfs_result)}")

    # DFS Traversal
    dfs_result = dfs(sample_graph, current_node=start)
    print(f"DFS Traversal Order: {' -> '.join(dfs_result)}")


if __name__ == "__main__":
    main()
