# -*- coding: UTF-8 -*-

import unittest
from test import generate_tests
from status_samples import get_status_samples, get_status_samples_dict
from lib.models import Map, Status, Action
from lib.bots import MaxnBot
from timeit import Timer
from random import choice


class TestMaxnBotAction(unittest.TestCase):

    def test_attacks_mine(self):
        """Test that the bot attacks a mine"""

        # Build models
        status_dict = get_status_samples_dict()["mine0"][0]
        map_obj = Map(status_dict["game"]["board"]["tiles"])
        status = Status(status_dict["game"], map_obj)

        bot = MaxnBot()
        action = bot.think(status)

        self.assertEqual(action, Action.north)

    def test_attacks_vulnerable_hero(self):
        """Test that the bot attacks a vulnerable hero"""

        # Build models
        status_dict = get_status_samples_dict()["attack0"][500]
        map_obj = Map(status_dict["game"]["board"]["tiles"])
        status = Status(status_dict["game"], map_obj)

        bot = MaxnBot()
        action = bot.think(status)

        self.assertEqual(action, Action.east)

    def test_bot_execution_time(self):
        """Test that the bot's execution time is not too big"""

        # Build models
        samples_dict = get_status_samples()
        samples_status = []
        for status_dict in samples_dict:
            map_obj = Map(status_dict["game"]["board"]["tiles"])
            status = Status(status_dict["game"], map_obj)
            samples_status.append(status)

        bot = MaxnBot()
        t = Timer(lambda: bot.think(choice(samples_status)))

        # We are interested in the maximum execution time, not in the average!
        # This, obviously, depends on the system used for testing.
        execution_time = max(t.repeat(repeat=3, number=1))

        self.assertLessEqual(execution_time, 0.9)
