# -*- coding: UTF-8 -*-


def paranoid(root, succ, payoff, max_depth, paranoid_player, current_player,
             num_players):
    """ Performs the Paranoid search.

    Implements the Paranoid search algorithm by Sturtevant and Korf
    (for info see "On Pruning Techniques for Multi-Player Games",
    Sturtevant-Korf, 2000).

    Choose the best action for paranoid_player assuming that all the opponent
    players act to minimize his happyness.

    Args:
        root (Status): Root node of the search
        succ (Status -> [(Status, Action)]): returns successors of a status
        payoff (Status -> float): returns the payoff for paranoid_player only
        max_depth (int): the maximum depth allowed during the search
        paranoid_player (int): the paranoid player
        current_player (int): player that makes the decision
        num_players (int): number of players

    Returns:
        (status, [action]): Best payoff for given player and sequence of
          actions to reach it
    """
    children_nodes = succ(root)

    if len(children_nodes) == 0 or max_depth <= 0:
        return (payoff(root), [])

    next_player = (current_player + 1) % num_players
    choices = []
    for next_node, action in children_nodes:
        status, actions = paranoid(
            next_node,
            succ,
            payoff,
            max_depth - 1,
            paranoid_player,
            next_player,
            num_players
        )
        choices.append((status, [action] + actions))

    # Choose the best action
    if paranoid_player == current_player:
        return max(choices, key=lambda item: item[0])
    else:
        # Everyone is against the paranoid_player
        return min(choices, key=lambda item: item[0])
