# -*- coding: UTF-8 -*-

import heapq


def search(start, is_goal, heuristic, successor):
    """ Performs an A* search.

    Args:
        start (hashable): Node to start the search from
        is_goal (hashable -> bool): tells whether a node is a goal node
        heuristic (hashable -> int): assigns a cost to a node
        successor (hashable -> [(hashable, cost)]: returns successors
                of a node, with their costs

    Returns:
        [hashable]: sequence of states from start to goal
    """
    frontier = []
    parents = {}
    costs = {}

    heapq.heappush(frontier, (1, start))
    parents[start] = None
    costs[start] = 0
    goal = None

    while frontier:
        (priority, node) = heapq.heappop(frontier)

        if is_goal(node):
            goal = node
            break

        successors = successor(node)
        for s in successors:
            (next_node, cost) = s
            new_cost = costs[node] + cost
            if next_node not in costs or new_cost < costs[next_node]:
                parents[next_node] = node
                costs[next_node] = new_cost
                priority = costs[next_node] + heuristic(next_node)
                heapq.heappush(frontier, (priority, next_node))

    return backtrack(goal, parents)


def backtrack(node, parents, path=[]):
    """ Performs backtracking from goal node up to start node.

    Args:
        node (hashable): Goal node
        parents (dict): Hash node-parent
        path ([hashable]): path built so far

    Returns:
        [hashable]: Path from goal node to start node
    """
    if node is not None:
        return backtrack(parents[node], parents, path) + [node]
    else:
        return []
