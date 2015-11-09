# -*- coding: UTF-8 -*-

from lib.models.action import Action


class BaseBot(object):
    def __init__(self):
        self.status = None

    def sense(self, env):
        """Retrieve the status of the game from the environment.

        Arguments:
            env (Environment): the environment with the game status.
        """
        self.status = env.get_status()

    def possible_actions(self):
        """Returns the list of possible actions in the current status.

        Returns:
            [Action]: the list of possible actions.
        """
        return list(Action)

    def think(self, actions):
        """Chooses the action to perform.

        Arguments:
            actions ([Action]): the actions among which the bot can choose.

        Returns:
            Action: the chosen action.
        """
        raise Exception("Not implemented")

    def do(self, env, action):
        """Chooses the action to perform.

        Arguments:
            env (Environment): the environment with the game status.
            action (Action): the action to perform on the environment.
        """
        env.send_action(action)
