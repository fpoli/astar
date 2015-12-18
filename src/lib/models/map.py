# -*- coding: UTF-8 -*-

from math import sqrt
from lib.equality_mixin import EqualityMixin
from .tile import Tile
from .tavern import Tavern
from .mine import Mine
from .position import Position


class Map(EqualityMixin):
    """Represents static elements in the game, such as walls, paths, taverns,
    mines and spawn points.

    The y axis points downward.

    Attributes:
        size (int): the board size (in a single axis).
        taverns ([Tavern]): the taverns.
        mines ([Position]): the position of the mines.
        __board ([[Tile]]): the board tiles, indexed by x and y.
    """

    def __init__(self, board):
        """Constructor.

        Args:
            board (string): the board string received from the server.
        """
        self.size = int(sqrt(len(board) / 2))
        assert(self.size * self.size * 2 == len(board))

        self.taverns = []
        self.mines = []
        self.__board = None

        self.__fill_board(board)

    def __fill_board(self, board):
        # Prepare the board
        self.__board = [[None] * self.size for _ in range(self.size)]

        # Parse the board string
        for y in range(self.size):
            for x in range(self.size):
                i = y * self.size + x
                raw_tile = board[i * 2: (i + 1) * 2]

                if raw_tile == "##":
                    tile = Tile.wall

                elif raw_tile == "[]":
                    tile = Tile.tavern
                    self.taverns.append(Tavern(Position(x, y)))

                elif raw_tile.startswith("$"):
                    tile = Tile.mine
                    self.mines.append(Mine(Position(x, y)))

                else:
                    tile = Tile.empty

                self.__board[x][y] = tile

    def is_outside(self, pos):
        """Test if a position is outside the board

        Args:
            pos (tuple): the position.

        Returns:
            bool: true iff the position is outside the board.
        """
        return (pos[0] < 0 or pos[1] < 0 or
                pos[0] >= self.size or pos[1] >= self.size)

    def __getitem__(self, pos):
        """Returns an item in the map.

        Args:
            pos (tuple): the position asked for.

        Returns:
            Tile | None: the tile, None if the position is outside the map).
        """
        if self.is_outside(pos):
            return None
        else:
            return self.__board[pos[0]][pos[1]]

    def get_neighbours(self, pos):
        """Returns a dictionary with the tiles next to a given position.

        Arguments:
            pos (tuple): the position.

        Returns:
            {Position -> Tile}: a dictionary with the cells next to pos.
        """
        neighbours = {}
        directions = [
            Position(+1, 0),
            Position(-1, 0),
            Position(0, +1),
            Position(0, -1)
        ]
        for d in directions:
            new_pos = pos + d
            if not self.is_outside(new_pos):
                neighbours[new_pos] = self.__board[new_pos[0]][new_pos[1]]
        return neighbours

    def __str__(self):
        """Pretty map."""
        s = " "
        s += "-" * (self.size) + "\n"
        for y in range(self.size):
            s += "|"
            for x in range(self.size):
                s += str(self[x, y] or " ")
            s += "|\n"
        s += " " + "-" * (self.size)
        return s
