# -*- coding: UTF-8 -*-

import unittest
from lib.algortihms.maxn import maxn


class TestMaxnSimpleRun(unittest.TestCase):
    def test_simple(self):
        self.assertEqual('a', 'a')
    def test_fail(self):
        self.assertEqual('a', 'b')

if __name__ == '__main__':
    unittest.main()
