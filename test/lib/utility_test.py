# -*- coding: UTF-8 -*-

import unittest
from test import generate_tests
from status_samples import get_status_samples
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

        self.assertEqual(
            sum(utility_tuple), 0,
            msg="Utility is {utility}, but the sum is non-zero: {sum}".format(
                utility=utility_tuple,
                sum=sum(utility_tuple)
            )
        )

    tests = get_status_samples()
