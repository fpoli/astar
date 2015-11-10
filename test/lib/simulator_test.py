# -*- coding: UTF-8 -*-

import unittest
from test import generate_tests
from status_samples import get_status_samples, get_sample_status_pairs
from lib.models import Map, Status, Action
from lib.simulator import simulate


@generate_tests
class TestSimulateGivesDifferentObjects(unittest.TestCase):

    def perform_test(self, status_dict):
        """Test that simulate returns a new object"""
        map_obj = Map(status_dict["game"]["board"]["tiles"])
        status = Status(status_dict["game"], map_obj)
        next_status = simulate(status, [Action.north] * 4)
        self.assertNotEqual(id(status), id(next_status))

    # All the sample status_dict
    tests = [
        item
        for game in get_status_samples().values()
        for item in game.values()
    ]


@generate_tests
class TestSimulateComparingStatus(unittest.TestCase):

    def perform_test(self, status_pair):
        """Test simulate by comparing simulated status"""
        dict_before, dict_after = status_pair

        # Build states
        map_obj = Map(dict_before["game"]["board"]["tiles"])
        status_before = Status(dict_before["game"], map_obj)
        status_after = Status(dict_after["game"], map_obj)

        # Get actions
        actions = [
            status_after.heroes[i].last_dir
            for i in range(4)
        ]

        # Run simulations
        simulated = simulate(status_before, actions)

        # Compare
        self.assertEqual(
            status_after,
            simulated,
            msg=(
                "Before:\n{before}\n" +
                "Actions: {actions}\n" +
                "After:\n{after}\n" +
                "Simulated:\n{sim}\n" +
                "Round: {b_id} {b_turn} --> {a_id} {a_turn}"
            ).format(
                before=status_before,
                actions=actions,
                after=status_after,
                sim=simulated,
                b_id=status_before.id,
                b_turn=status_before.turn,
                a_id=status_after.id,
                a_turn=status_after.turn
            )
        )

    tests = get_sample_status_pairs()
