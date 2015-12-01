# -*- coding: UTF-8 -*-

import unittest
from lib.algorithms.paranoid import paranoid


class TestMaxnSimpleRun(unittest.TestCase):
    def setUp(self):
        def succ(node):
            if node == 0:
                return [(1, 'a'), (2, 'b'), (3, 'c')]
            elif node == 1:
                return [(4, 'a'), (5, 'b'), (6, 'd')]
            elif node == 2:
                return [(7, 'a'), (8, 'b'), (9, 'd')]
            elif node == 3:
                return [(10, 'a'), (11, 'b'), (12, 'd')]
            else:
                return []

        def payoff(node):
            if node == 0:
                return (-1, 3, 0)
            elif node == 1:
                return (0, 1, 3)
            elif node == 2:
                return (1, 2, 3)
            elif node == 3:
                return (3, 2, 1)
            elif node == 4:
                return (0, 1, 3)
            elif node == 5:
                return (3, 2, -1)
            elif node == 6:
                return (2, 0, 2)
            elif node == 7:
                return (1, -1, 2)
            elif node == 8:
                return (7, -1, 2)
            elif node == 9:
                return (6, 1, -3)
            elif node == 10:
                return (0, 2, 2)
            elif node == 11:
                return (1, 3, 0)
            elif node == 12:
                return (-1, 3, 2)

        self.succ = succ
        self.payoff = payoff

    def test_simple(self):
        actions = paranoid(0, self.succ, self.payoff, 999, 0, 0, 3)
        expected_actions = ((1, -1, 2), ['b', 'a'])
        self.assertEqual(actions, expected_actions)

    def test_different_current_player(self):
        actions = paranoid(0, self.succ, self.payoff, 999, 0, 1, 3)
        expected_actions = ((-1, 3, 2), ['c', 'd'])
        self.assertEqual(actions, expected_actions)

    def test_different_root(self):
        actions = paranoid(2, self.succ, self.payoff, 999, 0, 0, 3)
        expected_actions = ((7, -1, 2), ['b'])
        self.assertEqual(actions, expected_actions)

    def test_on_leaf(self):
        actions = paranoid(10, self.succ, self.payoff, 999, 0, 0, 3)
        expected_actions = ((0, 2, 2), [])
        self.assertEqual(actions, expected_actions)

    def test_different_paranoid_player(self):
        actions = paranoid(0, self.succ, self.payoff, 999, 1, 0, 3)
        expected_actions = ((6, 1, -3), ['b', 'd'])
        self.assertEqual(actions, expected_actions)

    def test_different_root_and_paranoid_player(self):
        actions = paranoid(2, self.succ, self.payoff, 999, 1, 1, 3)
        expected_actions = ((6, 1, -3), ['d'])
        self.assertEqual(actions, expected_actions)

    def test_maximum_depth_0(self):
        actions = paranoid(0, self.succ, self.payoff, 0, 0, 0, 3)
        expected_actions = ((-1, 3, 0), [])
        self.assertEqual(actions, expected_actions)

    def test_maximum_depth_1(self):
        actions = paranoid(0, self.succ, self.payoff, 1, 0, 0, 3)
        expected_actions = ((3, 2, 1), ['c'])
        self.assertEqual(actions, expected_actions)
