# -*- coding: UTF-8 -*-

def maxn(node, successors, evaluation, player, max_players):
    if not successors(node):
        return evaluation(node)

    next_player = (player + 1) % max_players
    nodes = successors(node)
    children = [ maxn(child, successors, evaluation, next_player, max_players) for child in nodes ]
    return choose(children, player)


def choose(children, player):
    best = children[0]
    for child in children:
        if child[player] > best[player]:
            best = child
    return best
