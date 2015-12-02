# -*- coding: UTF-8 -*-

from copy import copy
from .hero import Hero
from .map import Map
from .tavern import Tavern
from .mine import Mine
from .tile import Tile
from lib.equality_mixin import EqualityMixin


class Status(EqualityMixin):
    """Represents a game status.

    A status object holds information about the game status.

    Attributes:
        id (int): the game id.
        max_turns (int): maximum turns of the game (notice that each turn only
          a single hero moves).
        turn (int): current turn.
        finished (bool): is the game over?
        map (Map): a map instance.
        heroes ([Hero]): a list of Hero instances.
        mine_owner ({Position -> int | None}): a dictionary with the hero id
          that owns this mine (None or integer from 0 to 3, extremes included).
    """

    def __init__(self, status_dict, map_obj):
        """Constructor.

        Args:
            state (dict): the state object.
        """
        # Constants
        self.id = status_dict["id"]
        self.max_turns = status_dict["maxTurns"]

        # Variables
        self.turn = status_dict["turn"]
        self.finished = status_dict["finished"]

        # Processed objects
        self.map = map_obj
        self.heroes = []
        self.mine_owner = {}

        # Parse and create mines
        for mine in self.map.mines:
            i = mine.pos.y * self.map.size + mine.pos.x
            tile = status_dict["board"]["tiles"][i * 2: (i + 1) * 2]
            owner = None if tile[1] == "-" else int(tile[1]) - 1
            self.mine_owner[mine.pos] = owner

        # Create heroes
        for hero in status_dict["heroes"]:
            self.heroes.append(Hero(hero))

    def __str__(self):
        """Pretty map."""
        s = "Turn {0}/{1}\n".format(self.turn, self.max_turns)
        s += " "
        s += "-" * 2 * self.map.size + "\n"
        for y in range(self.map.size):
            s += "|"
            for x in range(self.map.size):
                tile = self.map[x, y]
                hero = [
                    h for h in self.heroes
                    if h.pos == (x, y)
                ]
                spawn = [
                    h for h in self.heroes
                    if h.spawn == (x, y)
                ]

                if tile == Tile.wall:
                    s += "##"
                elif any(hero):
                    s += "@"
                    s += str(hero[0].id)
                elif any(spawn):
                    s += ".."
                elif (x, y) in self.mine_owner:
                    owner = self.mine_owner[(x, y)]
                    s += "$"
                    s += "-" if owner is None else str(owner)
                elif tile == Tile.tavern:
                    s += "[]"
                else:
                    s += "  "
            s += "|\n"
        s += " " + "-" * 2 * self.map.size
        for i in range(4):
            s += "\n"
            s += str(self.heroes[i])
        return s

    def current_hero(self):
        """Returns the id of the hero that has to move in this turn."""
        return self.turn % 4

    def remaining_turns_of_hero(self, hero_id):
        """Returns the number of remaining turns for a hero."""
        remaining_rounds = (self.max_turns - self.turn - 1) // 4

        if hero_id >= self.turn % 4:
            return remaining_rounds + 1
        else:
            return remaining_rounds

    def clone(self):
        """Returns a new copy of the current state, duplicating only mutable
        objects.

        Returns:
            Status: the cloned status
        """
        new_status = copy(self)
        new_status.heroes = [copy(h) for h in self.heroes]
        new_status.mine_owner = self.mine_owner.copy()
        return new_status

    def __copy__(self):
        """ Returns a quick shallow copy.

        This gives a ~15%% speedup (benchmark on MaxnBot and ParanoidBot).

        Returns:
            Status: a status shallow copy.
        """
        status = Status.__new__(Status)
        status.__dict__.update(self.__dict__)
        return status
