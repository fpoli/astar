# -*- coding: UTF-8 -*-

import heapq


def one(a=None, b=None):
    """ Returns 1.

    Returns:
        int: The value 1
    """
    return 1


def search(start, is_goal, s, h, cost=one, max_depth=1):
    """ Performs an A* search up to given depth level.

    Args:
        start (hashable): Node to start the search from
        is_goal (hashable -> bool): tells whether a node is a goal node
        successor (hashable -> [hashable]: returns successors of a node
        heuristic (hashable -> int): estimates a cost to a node
        cost (hashable, hashable -> int): cost to move between nodes
        max_depth (int): maximum depth for this iteration

    Returns:
        [hashable]: sequence of states from start to goal
    """
    path = []
    while not path:
        path = limited_search(start, is_goal, s, h, cost, max_depth)
        max_depth = max_depth + 1
    return path


def limited_search(start, is_goal, s, h, cost=one, max_depth=1):
    """ Performs an A* search up to given depth level.

    Args:
        start (hashable): Node to start the search from
        is_goal (hashable -> bool): tells whether a node is a goal node
        successor (hashable -> [hashable]: returns successors of a node
        heuristic (hashable -> int): estimates a cost to a node
        cost (hashable, hashable -> int): cost to move between nodes
        max_depth (int): maximum depth for this iteration

    Returns:
        [hashable]: sequence of states from start to goal
    """
    frontier = []
    parents = {}
    depths = {}
    g = {}

    heapq.heappush(frontier, (1, start))
    parents[start] = None
    depths[start] = 0
    g[start] = 0

    while frontier:
        (priority, node) = heapq.heappop(frontier)

        if is_goal(node):
            return backtrack(node, parents)

        if depths[node] > max_depth:
            continue

        successors = s(node)
        for next_node in successors:
            new_cost = g[node] + cost(node, next_node)
            if next_node not in g or new_cost < g[next_node]:
                parents[next_node] = node
                depths[next_node] = depths[node] + 1
                g[next_node] = new_cost
                priority = g[next_node] + h(next_node)
                heapq.heappush(frontier, (priority, next_node))
    return []


def backtrack(node, parents):
    """ Performs backtracking from goal node up to start node.

    Args:
        node (hashable): Goal node
        parents (dict): Hash node-parent

    Returns:
        [hashable]: Path from goal node to start node
    """
    path = []
    while node is not None:
        path.append(node)
        node = parents[node]
    path.reverse()
    return path
