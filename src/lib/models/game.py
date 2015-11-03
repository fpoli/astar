# -*- coding: UTF-8 -*-

from .hero import Hero
from .map import Map
from .tavern import Tavern
from .mine import Mine
from .tile import Tile


class Game(object):
    """Represents a game.

    A game object holds information about the game.

    Attributes:
        id (int): the game id.
        max_turns (int): maximum turns of the game (notice that each turn only
          a single hero moves).
        turn (int): current turn.
        map (Map): a map instance.
        heroes (list): a list of Hero instances.
        mines (list): a list of Mine instances.
        taverns (list): a list of Tavern instances.
    """

    def __init__(self, state):
        """Constructor.

        Args:
            state (dict): the state object.
        """
        # Constants
        self.id = state["game"]["id"]
        self.max_turns = state["game"]["maxTurns"]

        # Variables
        self.turn = state["game"]["turn"]

        # Processed objects
        self.map = None
        self.heroes = []
        self.mines = []
        self.taverns = []

        # Process the state, creating the objects
        self.__processState(state)

    def update(self, state):
        """Updates the game with new information.

        Notice that, this function does not re-create the objects, just update
        the current objects with new information.

        Args:
            state (dict): the state object.
        """
        size = state["game"]["board"]["size"]
        tiles = state["game"]["board"]["tiles"]
        heroes = state["game"]["heroes"]

        self.turn = state["game"]["turn"]

        for hero, hero_state in zip(self.heroes, heroes):
            hero.crashed    = hero_state["crashed"]
            hero.mine_count = hero_state["mineCount"]
            hero.gold       = hero_state["gold"]
            hero.life       = hero_state["life"]
            hero.last_dir   = hero_state.get("lastDir")
            hero.x          = hero_state["pos"]["y"]
            hero.y          = hero_state["pos"]["x"]

        for mine in self.mines:
            char = tiles[mine.x * 2 + mine.y * 2 * size + 1]
            mine.owner = None if char == "-" else int(char)

    def __processState(self, state):
        """Process the state."""
        # helper variables
        board = state["game"]["board"]
        size = board["size"]
        tiles = board["tiles"]
        tiles = [tiles[i:i + 2] for i in range(0, len(tiles), 2)]

        # run through the map and update map, mines and taverns
        self.map = Map(size)
        for y in range(size):
            for x in range(size):
                tile = tiles[y * size + x]
                if tile == "##":
                    self.map[x, y] = Tile.wall
                elif tile == "[]":
                    self.map[x, y] = Tile.tavern
                    self.taverns.append(Tavern(x, y))
                elif tile.startswith("$"):
                    self.map[x, y] = Tile.mine
                    self.mines.append(Mine(x, y))
                else:
                    self.map[x, y] = Tile.empty

        # create heroes
        for hero in state["game"]["heroes"]:
            pos = hero["spawnPos"]
            self.map[pos["y"], pos["x"]] = Tile.spawn
            self.heroes.append(Hero(hero))

    def __str__(self):
        """Pretty map."""
        s = " "
        s += "-" * (self.map.size) + "\n"
        for y in range(self.map.size):
            s += "|"
            for x in range(self.map.size):
                tile = self.map[x, y]
                hero = [h for h in self.heroes if h.x == x and h.y == y]

                if tile == Tile.wall:
                    s += "."
                elif any(hero):
                    s += str(hero[0].id)
                elif tile == Tile.spawn:
                    s += "s"
                elif tile == Tile.mine:
                    s += "M"
                elif tile == Tile.tavern:
                    s += "T"
                else:
                    s += " "
            s += "|\n"
        s += " " + "-" * (self.map.size)
        return s
