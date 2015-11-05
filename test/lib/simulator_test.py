# -*- coding: UTF-8 -*-

import unittest
import ujson as json
import os
from test import generateTests
from lib.models import Map, Status, Action
from lib.simulator import simulate

# Dictionary (name --> status_json) with all the sample status loaded
sample_status = {}

# Load sample status json files
for basepath, _, files in os.walk("sample_status/"):
    for file in files:
    	with open(basepath + file, "r") as infile:
    		sample_status[file] = json.load(infile)


@generateTests
class TestSimulateGivesDifferentObjects(unittest.TestCase):

	def perform_test(self, status_dict):
		"""Test that simulate returns a new object"""
		map_obj = Map(status_dict["game"]["board"]["tiles"])
		status = Status(status_dict["game"], map_obj)
		next_status = simulate(status, Action.north)
		self.assertNotEqual(id(status), id(next_status))

	tests = sample_status.values()
