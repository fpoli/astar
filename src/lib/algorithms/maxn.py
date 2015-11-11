# -*- coding: UTF-8 -*-


def maxn(root, s, payoff, player, players):
    """ Performs the MaxN search.

    Implements the original MaxN search algorithm by Luckhardt and Irani
    (for info see "An Algorithmic Solution of N-Person Games",
    Luckhardt-Irani, 1986).

    Args:
        root (status): Root node of the search
        s (status -> [(status, action)]): returns successors of a status
        payoff (status -> (int*)): returns a tuple of payoffs
        player (int): player whose payoff shall be maximized
        players (int): number of players

    Returns:
        (status, [action]): Best status for given player and sequence of
        actions to reach it
    """
    if not s(root):
        return (payoff(root), [])

    next_player = (player + 1) % players
    children = []
    for (successor, action) in s(root):
        (status, actions) = maxn(successor, s, payoff, next_player, players)
        children.append((status, [action] + actions))
    return best(children, player)


def best(children, player):
    """ Returns best move for given player.

    Args:
        children ([(status, [actions])]): children to choose from
        player (int): player whose payoff shall be maximized

    Returns:
        (status, [actions]): child with best payoff
    """
    best_child = children[0]
    for child in children:
        if child[0][player] > best_child[0][player]:
            best_child = child
    return best_child
