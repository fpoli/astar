# -*- coding: UTF-8 -*-

import unittest
from collections import namedtuple

TestIO = namedtuple("Test", "input output")


def generateTests(cls):
    """Class decorator that generates a test method for each item in a list.

    Requires:
    - perform_test(self, data): a class method that performs a test on data.
    - tests: a list with all the data items to be used in perform_test.
    """

    # Get a reference to the perform_test method
    perform_test = getattr(cls, "perform_test")

    # Iterate the tests class variable
    for i, data in enumerate(cls.tests):
        # Build a new test function
        # Capture the iterator variable using default assignments
        def test(self, data=data):
            perform_test(self, data)
        # Give it a nice name
        test.__name__ = "test_{0}".format(i)
        # And set the function as a class method
        setattr(cls, test.__name__, test)

    # Then, remove the stuff used to generate the test methods
    delattr(cls, "perform_test")
    delattr(cls, "tests")

    # And return the modified class
    return cls
