# -*- coding: UTF-8 -*-

from enum import Enum
from .abstract_goal import AbstractGoalBot
from lib.algorithms import astar
from lib.models.tile import Tile
from lib.models.action import Action, dir_to_action


class SimpleGoalBot(AbstractGoalBot):
    goals = Enum("goals", "Tavern Mine")

    def choose_goal(self, status):
        """Chooses a goal for the given status.

        Arguments:
            status (Status): the game status.

        Returns:
            Goal: the chosen goal.
        """
        hero = status.heroes[self.hero_id]

        if hero.life <= 50:
            return SimpleGoalBot.goals.Tavern
        else:
            return SimpleGoalBot.goals.Mine

    def action_for_goal(self, status, goal):
        """Chooses an action to reach a goal.

        Arguments:
            status (Status): the game status.
            goal (Goal): the goal.

        Returns:
            Action: an action to reach the goal.
        """
        hero = status.heroes[self.hero_id]

        if goal is SimpleGoalBot.goals.Tavern:
            path = shortest_path_to_tavern(self.hero_id, status)
        elif goal is SimpleGoalBot.goals.Mine:
            path = shortest_path_to_mine(self.hero_id, status)

        if path:
            direction = path[1] - hero.pos
            action = dir_to_action(direction)
            return action
        else:
            # No goal can be reached
            return Action.stay


def shortest_path_to_tavern(hero_id, status):
    hero = status.heroes[hero_id]
    hero_positions = set([h.pos for h in status.heroes])

    def succ(node):
        initial_tile = status.map[node]
        if initial_tile != Tile.empty:
            return []
        neighbours = status.map.get_neighbours(node)
        valid_cells = [
            pos
            for pos, tile in neighbours.items()
            if tile != Tile.wall
        ]
        return set(valid_cells) - hero_positions

    is_goal = lambda node: (
        status.map[node] == Tile.tavern
    )

    path = astar.search(
        hero.pos,
        is_goal,
        succ,
        status.map.distance_to_tavern
    )

    return path


def shortest_path_to_mine(hero_id, status):
    hero = status.heroes[hero_id]
    hero_positions = set([h.pos for h in status.heroes])

    def succ(node):
        initial_tile = status.map[node]
        if initial_tile != Tile.empty:
            return []
        neighbours = status.map.get_neighbours(node)
        valid_cells = [
            pos
            for pos, tile in neighbours.items()
            if tile != Tile.wall
        ]
        return set(valid_cells) - hero_positions

    is_goal = lambda node: (
        status.map[node] == Tile.mine and
        status.mine_owner[node] != hero.id
    )

    goal_mines = [
        pos
        for pos, owner in status.mine_owner.items()
        if owner != hero_id
    ]
    heuristic = lambda pos: status.map.distance_to_mines(pos, goal_mines)

    path = astar.search(
        hero.pos,
        is_goal,
        succ,
        heuristic
    )

    return path
