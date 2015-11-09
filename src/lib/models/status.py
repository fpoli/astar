# -*- coding: UTF-8 -*-

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
        map (Map): a map instance.
        heroes ([Hero]): a list of Hero instances.
        mines ({Position -> Mine}): a dictionary with the Mine instances.
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

        # Processed objects
        self.map = map_obj
        self.heroes = []
        self.mines = {}

        # Parse and create mines
        for pos in self.map.mines:
            i = pos.y * self.map.size + pos.x
            tile = status_dict["board"]["tiles"][i * 2: (i + 1) * 2]
            owner = None if tile[1] == "-" else int(tile[1])
            self.mines[pos] = Mine(pos, owner)

        # Create heroes
        for hero in status_dict["heroes"]:
            self.heroes.append(Hero(hero))

    def __str__(self):
        """Pretty map."""
        s = " "
        s += "-" * 2 * self.map.size + "\n"
        for y in range(self.map.size):
            s += "|"
            for x in range(self.map.size):
                tile = self.map[x, y]
                hero = [
                    h for h in self.heroes
                    if h.pos == (x, y)
                ]
                mine = self.mines.get((x, y))

                if tile == Tile.wall:
                    s += "##"
                elif any(hero):
                    s += "@"
                    s += str(hero[0].id)
                elif tile == Tile.spawn:
                    s += ".."
                elif mine:
                    s += "$"
                    s += "-" if mine.owner is None else str(mine.owner)
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
