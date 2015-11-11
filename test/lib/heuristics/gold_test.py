# -*- coding: UTF-8 -*-

import unittest
from test import generate_tests
from status_samples import get_status_samples
from lib.heuristics.gold import gold_score, heuristic
from lib.models import Status, Map


@generate_tests
class TestGoldHeuristicZeroSum(unittest.TestCase):

    def perform_test(self, status_dict):
        """Test that the heuristic is a zero sum tuple"""

        # Build models
        map_obj = Map(status_dict["game"]["board"]["tiles"])
        status = Status(status_dict["game"], map_obj)

        heuristic_tuple = heuristic(status)

        self.assertEqual(
            sum(heuristic_tuple), 0,
            msg="heuristic is {h}, but the sum is non-zero: {sum}".format(
                h=heuristic_tuple,
                sum=sum(heuristic_tuple)
            )
        )

    tests = get_status_samples()


@generate_tests
class TestGoldScoreCodomain(unittest.TestCase):

    def perform_test(self, status_dict):
        """Test that the values of gold_score are between 0 and 1"""

        # Build models
        map_obj = Map(status_dict["game"]["board"]["tiles"])
        status = Status(status_dict["game"], map_obj)

        for hero_id in range(1, 5):
            for opponent_id in range(1, 5):
                score = gold_score(status, hero_id, opponent_id)
                self.assertGreaterEqual(score, 0)
                self.assertLessEqual(score, 1)

    tests = get_status_samples()
