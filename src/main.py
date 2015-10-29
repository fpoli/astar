#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
from lib.environment import Environment

# Ensure that this script is being executed (not imported)
assert(__name__ == "__main__")

if len(sys.argv) < 2:
	print("Usage: {0} <key>".format(sys.argv[0]))
	exit(0)

else:
	key = sys.argv[1]
	env = Environment(key)

	while True:
		print("Status:", env.getStatus())
		env.sendAction("North")
