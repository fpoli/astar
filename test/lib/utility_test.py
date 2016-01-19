# -*- coding: UTF-8 -*-

import unittest
from test import generate_tests
from status_samples import get_status_samples, get_status_samples_dict
from lib.utility import utility
from lib.models import Status, Map


@generate_tests
class TestUtilityZeroSum(unittest.TestCase):

    def perform_test(self, status_dict):
        """Test that the utility is a zero sum tuple"""

        # Build models
        map_obj = Map(status_dict["game"]["board"]["tiles"])
        status = Status(status_dict["game"], map_obj)

        utility_tuple = utility(status)

        self.assertAlmostEqual(
            sum(utility_tuple), 0,
            msg="Utility is {utility}, but the sum is non-zero: {sum}".format(
                utility=utility_tuple,
                sum=sum(utility_tuple)
            )
        )

    tests = get_status_samples()


class TestUtilityValue(unittest.TestCase):

    def test_utility_value_yupgvpr5_2400(self):
        """Test the utility value on yupgvpr5 2400"""

        # Build models
        status_dict = get_status_samples_dict()["yupgvpr5"][2400]
        map_obj = Map(status_dict["game"]["board"]["tiles"])
        status = Status(status_dict["game"], map_obj)

        utility_tuple = utility(status)

        self.assertEqual(utility_tuple, (8, -8, -8, 8))

    def test_utility_value_nztclzmi_0(self):
        """Test the utility value on nztclzmi 0"""

        # Build models
        status_dict = get_status_samples_dict()["nztclzmi"][0]
        map_obj = Map(status_dict["game"]["board"]["tiles"])
        status = Status(status_dict["game"], map_obj)

        utility_tuple = utility(status)

        self.assertEqual(utility_tuple, (0, 0, 0, 0))
