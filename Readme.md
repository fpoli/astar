# AStar

[![Build Status](https://magnum.travis-ci.com/fpoli/astar.svg?token=XpqKLcynjTRxpC4xqqri)](https://magnum.travis-ci.com/fpoli/astar)

AStar is an artificial intelligence project aimed at developing bots for the [Vindinium](http://vindinium.org/) programming challenge.

It is based on [renatopp's client](https://github.com/renatopp/vindinium-python), then modified by Federico Poli and Marco Zanella (alphabetic order).


## Usage

Create a file `bot.key` containing the bot's key:

	echo secret-key-of-the-bot > bot.key

Then, to start the client:

	make start

Or

	./script/main.py -k `cat bot.key` -b MaxnBot
	./script/main.py -k `cat bot.key` -b MaxnBot -e GoldHeuristic -m training
	./script/main.py -k `cat bot.key` -b PessimisticBot -m arena
	./script/main.py -k `cat bot.key` -b PessimisticBot -e MineGoldHeuristic -m arena --number 3
	...
	etc

To list all the parameters:

	./script/main.py -h


## Documentation

A project report is accessible at <http://astar.altervista.org/>.

To generate the automatic html documentation:

	make docs

It will be accessible at `docs/build/html/index.html`.


## Automatic tests

To execute linter and tests:

	make linter
	make test


## Some metrics

To run the client with profiling active:

       make profile

To analyze the results (file `main.calltree`) it is convenient to use `kcachegrind` (command `kcachegrind main.calltree`).

To benchmark the server response time, the simulator and some bots:

       make benchmark


## Dependencies

To install the dependencies on `Ubuntu 14.04`:

	sudo apt-get install python3-pip python3-sphinx
	sudo pip3 install -r requirements.txt


## License

Original work comes from [renatopp/vindinium-python](https://github.com/renatopp/vindinium-python) and is distributed under the MIT License.

Modified work Copyright (C) 2015-2016  Federico Poli, Marco Zanella

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
