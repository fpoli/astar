# -*- coding: UTF-8 -*-

from .position import Position


class Mine(object):
    """A mine object.

    Attributes:
        pos (Position): the mine position.
        owner (int): the hero's id that owns this mine.
    """

    def __init__(self, pos, owner=None):
        """Constructor.

        Args:
            pos (Position): the mine position.
            owner (int): the hero's id that owns this mine.
        """
        self.pos = pos
        self.owner = owner
