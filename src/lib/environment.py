#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
import ujson as json

class Environment:
	def __init__(self, key):
		self.status = None
		self.connection = requests.session()

		# TODO: switch between 'training' mode and 'arena' mode
		# Maybe extending this Environment class with two classes
		# TrainingEnvironment and ArenaEnvironment?
		self.server_api = "http://vindinium.org/api/training"
		self.game_params = {"key": key, "turns": 1000}
		self.game_url = None

		self.__createGame()

	def __jsonToStatus(self, json_dict):
		"""Read the json and return the appropriate Status object.

		This is a private function (denoted by the leading double underscore).

		return: a Status object, complete with references to Map, Player,
		        Mine and Brasserie objects
		"""

		# TODO: build Status, Player, ... objects from json_dict
		status = json_dict

		return status

	def __createGame(self):
		"""Negotiate and start a new game with the server.

		This is a private function (denoted by the leading double underscore).
		"""

		# Wait for other players
		res = self.connection.post(self.server_api, self.game_params)

		if res.status_code == 200:
			# Decode json
			json_dict = json.loads(res.text)

			self.game_url = json_dict["playUrl"]
			self.status = self.__jsonToStatus(json_dict)
		else:
			raise Exception(
				"HTTP error {0}: {1}".format(res.status_code, res.text)
			)

	def getStatus(self):
		"""Get the status of the environment

		return: a Status object, complete with references to Map, Player,
		         Mine and Brasserie objects
		"""

		# Ensure that we created a game before
		assert(self.status is not None)

		return self.status

	def sendAction(self, action):
		"""Change the environment by executing an action

		action: an Action object.
		"""

		# Ensure that we created a game before
		assert(self.game_url is not None)

		res = self.connection.post(self.game_url, {"dir": action})

		if res.status_code == 200:
			# Decode json
			json_dict = json.loads(res.text)

			self.status = self.__jsonToStatus(json_dict)
		else:
			raise Exception(
				"HTTP error {0}: {1}".format(res.status_code, res.text)
			)
