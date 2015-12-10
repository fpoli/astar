# -*- coding: UTF-8 -*-

import random
from .abstract_goal import AbstractGoalBot
from lib.algorithms import astar
from lib.models.tile import Tile
from lib.models.action import Action, dir_to_action
from lib.goals import TavernGoal, MineGoal


class SimpleGoalBot(AbstractGoalBot):
    def choose_goal(self, status):
        """Chooses a goal for the given status.

        Arguments:
            status (Status): the game status.

        Returns:
            Goal: the chosen goal.
        """
        hero = status.heroes[self.hero_id]

        if hero.life <= 50:
            return TavernGoal(self.hero_id)
        else:
            return MineGoal(self.hero_id)

    def action_for_goal(self, status, goal):
        """Chooses an action to reach a goal.

        Arguments:
            status (Status): the game status.
            goal (Goal): the goal.

        Returns:
            Action: an action to reach the goal.
        """
        hero = status.heroes[self.hero_id]
        hero_positions = set([h.pos for h in status.heroes])

        zero_const = lambda _: 0

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

        if isinstance(goal, TavernGoal):
            is_goal = lambda node: (
                status.map[node] == Tile.tavern
            )

            path = astar.search(
                hero.pos,
                is_goal,
                succ,
                zero_const
            )

            if path:
                assert(path[0] == hero.pos)
                direction = path[1] - hero.pos
                action = dir_to_action(direction)
                return action

        elif isinstance(goal, MineGoal):
            is_goal = lambda node: (
                status.map[node] == Tile.mine and
                status.mine_owner[node] != hero.id
            )

            path = astar.search(
                hero.pos,
                is_goal,
                succ,
                zero_const
            )

            if path:
                assert(path[0] == hero.pos)
                direction = path[1] - hero.pos
                action = dir_to_action(direction)
                return action

        # No goal can be reached
        return Action.stay
