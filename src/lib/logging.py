# -*- coding: UTF-8 -*-

import os
import errno
import time
import ujson as json


def mkdir_parents(path):
    """Create a folder, making also parent folders as needed
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class Logger:
    def __init__(self, run_dir, game_id):
        self.run_dir = run_dir
        self.game_id = game_id
        self.data = []

    def _prepare(self):
        base_path = "{0}/{1}".format(self.run_dir, self.game_id)
        mkdir_parents(base_path)
        mkdir_parents(base_path + "/turns")

    def store_status(self, turn, status_text):
        self._prepare()
        filename = "{run}/{gid}/turns/{gid}_{turn}.json".format(
            run=self.run_dir,
            gid=self.game_id,
            turn=turn
        )
        with open(filename, "w") as out_file:
            out_file.write(status_text)

    def store_value(timestamp=None, **kwargs):
        values = kwargs

        if timestamp is not None:
            if timestamp is True:
                timestamp = time.time()
            values["timestamp"] = timestamp

        self.data.append(values)

    def write_values(self):
        self._prepare()
        filename = "{run}/{gid}/data.json".format(
            run=self.run_dir,
            gid=self.game_id,
        )

        with open(filename, "w") as out_file:
            text = json.dumps(self.data)
            out_file.write(text)
