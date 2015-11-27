# -*- coding: UTF-8 -*-

import requests
import ujson as json
from lib.models import Status, Action, Map


class Environment:
    def __init__(self, server_api, game_params):
        self.connection = requests.session()

        self.server_api = server_api
        self.game_params = game_params

        self.play_url = None
        self.view_url = None
        self.token = None
        self.map = None
        self.hero = None
        self.status = None
        self.hero_id = None

        self.__create_game()

    def __create_game(self):
        """Negotiate and start a new game with the server.

        This is a private function (denoted by the leading double underscore).
        """

        # Wait for other players
        res = self.connection.post(self.server_api, self.game_params)

        if res.status_code == 200:
            # Decode json
            json_dict = json.loads(res.text)

            self.play_url = json_dict["playUrl"]
            self.view_url = json_dict["viewUrl"]
            self.token = json_dict["token"]
            self.map = Map(json_dict["game"]["board"]["tiles"])
            self.hero_id = json_dict["hero"]["id"] - 1
            self.status = Status(json_dict["game"], self.map)
        else:
            raise Exception(
                "HTTP error {0}: {1}".format(res.status_code, res.text)
            )

    def get_status(self):
        """Get the status of the environment.

        return: a Status object, complete with references to other models.
        """

        return self.status

    def send_action(self, action):
        """Change the environment by executing an action.

        Args:
            action (Action): the action to execute.
        """

        command = {
            Action.north: "North",
            Action.south: "South",
            Action.west: "West",
            Action.east: "East",
            Action.stay: "Stay"
        }

        direction = command[action]
        res = self.connection.post(self.play_url, {"dir": direction})

        if res.status_code == 200:
            # Decode json
            json_dict = json.loads(res.text)

            self.status = Status(json_dict["game"], self.map)
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
