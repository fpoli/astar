#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
import ujson as json

class Environment:
	def __init__(self, server_api, game_params):
		self.status = None
		self.connection = requests.session()

		self.server_api = server_api
		self.game_params = game_params
		self.game_url = None

		self.__create_game()

	def __json_to_status(self, json_dict):
		"""Read the json and return the appropriate Status object.

		This is a private function (denoted by the leading double underscore).

		return: a Status object, complete with references to Map, Player,
		        Mine and Brasserie objects
		"""

		# TODO: build Status, Player, ... objects from json_dict
		status = json_dict

		return status

	def __create_game(self):
		"""Negotiate and start a new game with the server.

		This is a private function (denoted by the leading double underscore).
		"""

		# Wait for other players
		res = self.connection.post(self.server_api, self.game_params)

		if res.status_code == 200:
			# Decode json
			json_dict = json.loads(res.text)

			self.game_url = json_dict["playUrl"]
			self.status = self.__json_to_status(json_dict)
		else:
			raise Exception(
				"HTTP error {0}: {1}".format(res.status_code, res.text)
			)

	def get_status(self):
		"""Get the status of the environment

		return: a Status object, complete with references to Map, Player,
		         Mine and Brasserie objects
		"""

		# Ensure that we created a game before
		assert(self.status is not None)

		return self.status

	def send_action(self, action):
		"""Change the environment by executing an action

		action: an Action object.
		"""

		# Ensure that we created a game before
		assert(self.game_url is not None)

		res = self.connection.post(self.game_url, {"dir": action})

		if res.status_code == 200:
			# Decode json
			json_dict = json.loads(res.text)

			self.status = self.__json_to_status(json_dict)
		else:
			raise Exception(
				"HTTP error {0}: {1}".format(res.status_code, res.text)
			)


class TrainingEnvironment(Environment):
	def __init__(self, key, turns=1000):
		server_api = "http://vindinium.org/api/training"
		game_params = {"key": key, "turns": turns}
		super().__init__(server_api, game_params)


class ArenaEnvironment(Environment):
	def __init__(self, key):
		server_api = "http://vindinium.org/api/arena"
		game_params = {"key": key}
		super().__init__(server_api, game_params)
