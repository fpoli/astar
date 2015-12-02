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

        def full_payoff(node):
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
        self.full_payoff = full_payoff

    def test_simple(self):
        payoff = lambda status: self.full_payoff(status)[0]
        actions = paranoid(0, self.succ, payoff, 999, 0, 0, 3)
        self.assertEqual(actions, (1, ['b', 'a']))

    def test_different_current_player(self):
        payoff = lambda status: self.full_payoff(status)[0]
        actions = paranoid(0, self.succ, payoff, 999, 0, 1, 3)
        self.assertEqual(actions, (-1, ['c', 'd']))

    def test_different_root(self):
        payoff = lambda status: self.full_payoff(status)[0]
        actions = paranoid(2, self.succ, payoff, 999, 0, 0, 3)
        self.assertEqual(actions, (7, ['b']))

    def test_on_leaf(self):
        payoff = lambda status: self.full_payoff(status)[0]
        actions = paranoid(10, self.succ, payoff, 999, 0, 0, 3)
        self.assertEqual(actions, (0, []))

    def test_different_paranoid_player(self):
        payoff = lambda status: self.full_payoff(status)[1]
        actions = paranoid(0, self.succ, payoff, 999, 1, 0, 3)
        self.assertEqual(actions, (1, ['b', 'd']))

    def test_different_root_and_paranoid_player(self):
        payoff = lambda status: self.full_payoff(status)[1]
        actions = paranoid(2, self.succ, payoff, 999, 1, 1, 3)
        self.assertEqual(actions, (1, ['d']))

    def test_maximum_depth_0(self):
        payoff = lambda status: self.full_payoff(status)[0]
        actions = paranoid(0, self.succ, payoff, 0, 0, 0, 3)
        self.assertEqual(actions, (-1, []))

    def test_maximum_depth_1(self):
        payoff = lambda status: self.full_payoff(status)[0]
        actions = paranoid(0, self.succ, payoff, 1, 0, 0, 3)
        self.assertEqual(actions, (3, ['c']))
