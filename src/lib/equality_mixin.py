# -*- coding: UTF-8 -*-

class EqualityMixin(object):
    """This mixin implements a default comparison operator, such that instances
    of the same class with the same parameter's value will be equal.
    """

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
