# -*- coding: UTF-8 -*-

import unittest
from status_samples import get_status_samples_dict
from lib.models import Status, Map


class TestStatusRemainingTurnsOfHero(unittest.TestCase):
    def setUp(self):
        status_dict = get_status_samples_dict()["2nw864rp"][0]
        self.map = Map(status_dict["game"]["board"]["tiles"])
        self.status = Status(status_dict["game"], self.map)

    def test_maxturns_2400(self):
        """Test when maxTurns=2400"""

        expected = [600, 600, 600, 600]

        # Check initial value
        for hero_id in range(4):
            self.assertEqual(
                self.status.remaining_turns_of_hero(hero_id),
                expected[hero_id],
                msg="Turn {t}, max_turns {m}, hero {h}".format(
                    t=self.status.turn,
                    m=self.status.max_turns,
                    h=hero_id
                )
            )

        for turn in range(2400):
            # Similate a game turn
            expected[self.status.current_hero()] -= 1
            self.status.turn += 1

            # Check value
            for hero_id in range(4):
                self.assertEqual(
                    self.status.remaining_turns_of_hero(hero_id),
                    expected[hero_id],
                    msg="Turn {t}, max_turns {m}, hero {h}".format(
                        t=self.status.turn,
                        m=self.status.max_turns,
                        h=hero_id
                    )
                )
