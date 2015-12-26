# -*- coding: UTF-8 -*-

from .abstract_heurisitc import AbstractHeuristic
from lib.algorithms import astar
from lib.models.tile import Tile
from lib.models.action import Action, dir_to_action


class MineGoldHeuristic(AbstractHeuristic):
    """
    How much gold would you have at the end of the game, if every enemy
    would vanish from the map, and you could only capture one more mine?

    With gold+mines*turns_left you can't differentiate from two empty cells
    nearby, because that heuristic only changes when you capture mines.

    If you don't have the health, plug in the trip to the closest tavern and
    from the tavern to a mine.

    That's a neat way to plug mining into minimax.

    Source: https://www.reddit.com/r/vindinium/comments/2kgsx4/
    a_chat_with_the_creator_of_the_best_performing/
    """

    def hero_heuristic(self, status, hero_id):
        """ Heuristic that estimates the gold of a hero at the end of the game.

        Arguments:
            status (Status): the game status.
            hero_id (int): the hero's id.

        Returns:
            float: the estimated utility for the hero.
        """
        hero = status.heroes[hero_id]
        remaining_turns = status.remaining_turns_of_hero(hero_id)
        hero_gold = hero.gold + remaining_turns * hero.mine_count

        goal_mines = [
            pos
            for pos, owner in status.mine_owner.items()
            if owner != hero_id
        ]

        if not goal_mines:
            # There are no more mines
            return hero_gold

        mine_dist = status.map.distance_to_mines(hero.pos, goal_mines)

        life_after_attack = hero.life - mine_dist - 20

        if life_after_attack > 0:
            # The hero has enough life
            mine_gold = remaining_turns - mine_dist
        else:
            # The hero needs to drink at least one beer and go back
            tavern_dist = status.map.distance_to_tavern(hero.pos)
            mine_gold = (
                remaining_turns
                - 2                # pay beer
                - tavern_dist      # drink beer
                - tavern_dist + 1  # go back
                - mine_dist        # attack mine
            )

        return hero_gold + max(0, mine_gold)
