# -*- coding: UTF-8 -*-

import requests
import ujson as json
from .models import Game, Action


class Environment:
    def __init__(self, server_api, game_params):
        self.status = None
        self.connection = requests.session()

        self.server_api = server_api
        self.game_params = game_params
        self.game_url = None

        self.__create_game()

    def __json_to_status(self, json_dict):
        """Read the json and return the appropriate Game object.

        This is a private function (denoted by the leading double underscore).

        return: a Game object, complete with references to other models.
        """

        return Game(json_dict)

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
        """Get the status of the environment.

        return: a Game object, complete with references to other models.
        """

        # Ensure that we created a game before
        assert(self.status is not None)

        return self.status

    def send_action(self, action):
        """Change the environment by executing an action.

        Args:
            action (Action): the action to execute.
        """

        # Ensure that we created a game before
        assert(self.game_url is not None)

        command = {
            Action.north: "North",
            Action.south: "South",
            Action.west: "West",
            Action.east: "East",
            Action.stay: "Stay"
        }

        direction = command[action]
        res = self.connection.post(self.game_url, {"dir": direction})

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
