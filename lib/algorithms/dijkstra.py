# -*- coding: UTF-8 -*-

import heapq
from collections import defaultdict


def compute_distances(goal_nodes, successor):
    """ Computes distances to a set of nodes using a Dijkstra search.

    Assumes that the cost of every action is 1.

    Arguments:
        goal_nodes ([hashable]): collection of goal nodes.
        successor (hashable -> [hashable]): returns successors of a node.

    Returns:
        {hashable -> int}: dict containing the minimum distance from each node
            to the nearest goal nodes. Infinite if there is no path.
    """
    distance = defaultdict(lambda: float("inf"))
    frontier = []

    for node in goal_nodes:
        distance[node] = 0
        heapq.heappush(frontier, (0, node))

    while frontier:
        (cost, node) = heapq.heappop(frontier)
        adjacent_nodes = successor(node)

        new_cost = cost + 1

        for next_node in adjacent_nodes:
            if next_node not in distance:
                distance[next_node] = new_cost
                heapq.heappush(frontier, (new_cost, next_node))

    return distance
