# -*- coding: UTF-8 -*-

import unittest
from lib.algorithms.maxn import maxn


class TestMaxnSimpleRun(unittest.TestCase):
    def test_simple(self):
        def s(x):
            if x == 0:
                return [(1, 'a'), (2, 'b'), (3, 'c')]
            elif x == 1:
                return [(4, 'a'), (5, 'b'), (6, 'd')]
            elif x == 2:
                return [(7, 'a'), (8, 'b'), (9, 'd')]
            elif x == 3:
                return [(10, 'a'), (11, 'b'), (12, 'd')]

        def payoff(x):
            if x == 4:
                return (0, 1, 3)
            elif x == 5:
                return (3, 2, -1)
            elif x == 6:
                return (2, 0, 2)
            elif x == 7:
                return (1, 1, 2)
            elif x == 8:
                return (7, 1, 2)
            elif x == 9:
                return (6, 1, -3)
            elif x == 10:
                return (0, 2, 2)
            elif x == 11:
                return (1, 3, 0)
            elif x == 12:
                return (-1, 2, 3)

        actions = maxn(0, s, payoff, 0, 3)
        self.assertEqual(((3, 2, -1), ['a', 'b']), actions)


if __name__ == '__main__':
    unittest.main()
