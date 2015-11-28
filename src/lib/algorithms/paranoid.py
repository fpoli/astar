# -*- coding: UTF-8 -*-


def paranoid(root, succ, max_depth, unlucky_player, current_player, num_players):
    """ Performs the Paranoid search.

    Implements the Paranoid search algorithm by Sturtevant and Korf
    (for info see "On Pruning Techniques for Multi-Player Games",
    Sturtevant-Korf, 2000).

    All the players act to minimize the happyness of the unlucky_player.

    Args:
        node, succ, max_depth, unlucky_player, current_player, num_players
        root (Status): Root node of the search
        succ (Status -> [(Status, Action)]): returns successors of a status
        payoff (Status -> (float*)): returns a tuple of payoffs
        unlucky_player (int): the unlunky player
        current_player (int): player that makes the decision
        num_players (int): number of players

    Returns:
        (status, [action]): Best status for given player and sequence of
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
            max_depth - 1,
            unlucky_player,
            next_player,
            num_players
        )
        choices.append((status, [action] + actions))

    # Choose the best action
    if unlucky_player == current_player:
        return max(choices, key=lambda item:item[0])
    else:
        # Everyone is against the unlucky_player
        return min(choices, key=lambda item:item[0])
