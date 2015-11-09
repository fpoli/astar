# -*- coding: UTF-8 -*-

from collections import namedtuple


class Position(namedtuple("Position_", "x y")):

    def __add__(self, other):
        """Define sum, when the left term is a Position"""
        return Position(self.x + other[0], self.y + other[1])

    def __radd__(self, other):
        """Define sum, when the left term is _not_ a Position"""
        return Position(self.x + other[0], self.y + other[1])
