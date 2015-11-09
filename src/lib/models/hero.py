# -*- coding: UTF-8 -*-

from lib.equality_mixin import EqualityMixin
from .position import Position
from .action import str_to_action


class Hero(EqualityMixin):
    """Represents a hero in the game.

    Attributes:
        id (int): the hero's id.
        name (string): the bot's name.
        user_id (string): the bot's id (None in training mode).
        elo (int): the bot's ELO (None in training mode).
        crashed (bool): True if the bot has been disconnected.
        mine_count (int): the number of mines this hero owns.
        gold (int): current amount of gold earned by this hero.
        life (int): current hero's life.
        last_dir (string): last bot movement (may be None).
        pos (Position): the bot's position.
        spawn (Position): the bot's spawn position.
    """

    def __init__(self, hero):
        """Constructor.

        Args:
            hero (dict): the hero data from the server.
        """
        # Constants
        self.id         = hero["id"]
        self.name       = hero["name"]
        self.user_id    = hero.get("userId")
        self.elo        = hero.get("elo")

        # Variables
        self.crashed    = hero["crashed"]
        self.mine_count = hero["mineCount"]
        self.gold       = hero["gold"]
        self.life       = hero["life"]
        last_dir_raw = hero.get("lastDir")
        self.last_dir = str_to_action(last_dir_raw) if last_dir_raw else None
        self.pos        = Position(hero["pos"]["y"],
                                   hero["pos"]["x"])
        self.spawn      = Position(hero["spawnPos"]["y"],
                                   hero["spawnPos"]["x"])

    def __str__(self):
        return "Hero {id}: {name} ({x}, {y}) {life}/100 {gold}$ " +
        "({mines:+})".format(
            id=self.id,
            name=self.name,
            x=self.pos.x,
            y=self.pos.y,
            life=self.life,
            gold=self.gold,
            mines=self.mine_count
        )
