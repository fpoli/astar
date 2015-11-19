# -*- coding: UTF-8 -*-

from .position import Position
from lib.equality_mixin import EqualityMixin


class Mine(EqualityMixin):
    """A mine object.

    Attributes:
        pos (Position): the mine position.
        owner (int): the hero's id that owns this mine (from 0 to 3,
          extremes included).
    """

    def __init__(self, pos, owner=None):
        """Constructor.

        Args:
            pos (Position): the mine position.
            owner (int | None): the hero's id that owns this mine (from 0 to
                3, extremes included)
        """
        self.pos = pos
        self.owner = owner
