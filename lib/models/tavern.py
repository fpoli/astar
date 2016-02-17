# -*- coding: UTF-8 -*-

from lib.equality_mixin import EqualityMixin


class Tavern(EqualityMixin):
    """A tavern.

    Attributes:
        pos (Position): the tarven position.
    """

    def __init__(self, pos):
        """Constructor

        Args:
            pos (Position): the tarven position.
        """
        self.pos = pos
