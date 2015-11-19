# -*- coding: UTF-8 -*-

import unittest
from test import generate_tests
from status_samples import get_status_samples
from lib.heuristics.gold import gold_score, heuristic
from lib.models import Status, Map
from lib.utility import utility


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
class TestGoldHeuristicOnLeafs(unittest.TestCase):

    def perform_test(self, status_dict):
        """Test that the heuristic on leafs is consistent with the utility"""

        # Build models
        map_obj = Map(status_dict["game"]["board"]["tiles"])
        status = Status(status_dict["game"], map_obj)

        # Simulate a final status
        status.turn == status.max_turns

        heuristic_tuple = heuristic(status)
        utility_tuple = utility(status)

        # Check that heuristic and utility are consistent
        for i in range(4):
            for j in range(4):
                if utility_tuple[i] > utility_tuple[j]:
                    self.assertGreater(heuristic_tuple[i], heuristic_tuple[j])
                elif utility_tuple[i] == utility_tuple[j]:
                    self.assertEqual(heuristic_tuple[i], heuristic_tuple[j])
                else:
                    self.assertLess(heuristic_tuple[i], heuristic_tuple[j])

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
