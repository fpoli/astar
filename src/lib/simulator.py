# -*- coding: UTF-8 -*-

from copy import copy, deepcopy
from lib.models import Action, Tile, Position


def kill(status, id, killer=None):
    '''Recursively kills a hero.

    Arguments:
        status (Status): the game status.
        id (int): the id of the hero to be killed.
        killer (int | None): the id of the killed.
    '''
    hero = status.heroes[id]

    for i, h in enumerate(status.heroes):
        if h == hero:
            continue

        if h.pos.x == hero.spawn.x and h.pos.y == hero.spawn.y:
            kill(status, i)

    hero.pos.x = hero.spawn.x
    hero.pos.y = hero.spawn.y
    hero.mine_count = 0
    hero.life = 100

    for pos, value in status.mines.iteritems():
        if value == id + 1:
            if killer is None:
                status.mines[pos] = None
            else:
                status.mines[pos] = killer + 1
                status.heroes[killer].mine_count += 1


def simulate(original_status, action):
    '''Simulate a movement given a Status.

    Arguments:
        status (State): the game status.
        action (Action): the action to simulate.

    Returns:
        Status: the next status (as a new object)
    '''

    # Clone the status object
    status = copy(original_status)
    status.heroes = deepcopy(original_status.heroes)
    status.mines = deepcopy(original_status.mines)

    hero_id = status.turn % 4 + 1
    hero = status.heroes[hero_id - 1]

    # Compute next position
    dir_by_action = {
        Action.north: (0, -1),
        Action.south: (0, 1),
        Action.west: (-1, 0),
        Action.east: (1, 0),
        Action.stay: (0, 0)
    }
    dir = dir_by_action[action]

    dst_pos = Position(hero.pos.x + dir[0], hero.pos.y + dir[1])

    # Checks if there is an anemy
    enemy = None
    for h in status.heroes:
        if h.pos == dst_pos:
            enemy = h
            break

    # Compute side effects of movement
    tile = status.map[dst_pos]

    if tile == Tile.empty and not enemy:
        hero.pos = dst_pos

    elif tile == Tile.tavern:
        if hero.gold > 2:
            hero.gold -= 2
            hero.life = min(hero.life + 50, 100)

    elif tile == Tile.mine:
        mine = status.mines[dst_pos]

        # hero is not the mine's owner
        if mine.owner != hero_id:

            # get mine
            if hero.life > 20:
                hero.life -= 20
                hero.mine_count += 1

                # remove mine from previous owner
                if mine is not None:
                    status.heroes[mine.owner - 1].mine_count -= 1

                status.mines[dst_pos].owner = hero_id

            # dies trying
            else:
                kill(status, hero_id)

    # Fight
    for other_id, other in enumerate(status.heroes):
        if other == hero:
            continue

        # Attack if 1-tile distance
        if abs(hero.pos.x - other.pos.x) + abs(hero.pos.y - other.pos.y) == 1:

            if other.life > 20:
                other.life -= 20

            else:
                # Hero kills the other
                kill(status, other_id, hero_id)

    # Mining
    hero.gold += hero.mine_count

    # Thirst
    hero.life = max(hero.life - 1, 1)

    status.turn += 1
