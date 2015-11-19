# -*- coding: UTF-8 -*-

import unittest
from test import generate_tests
from status_samples import get_status_samples_dict
from lib.models import Map, Status, Action
from lib.bots import MaxnBot


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
