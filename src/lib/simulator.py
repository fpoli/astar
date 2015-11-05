# -*- coding: UTF-8 -*-


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


def simulate(status, action):
    '''Simulate a movement given a Status.

    Arguments:
        status (State): the game status.
        action (Action): the action to simulate.

    Returns:
        Status: the next status (as a new object)
    '''
    id = status.turn % 4
    hero = status.heroes[id]

    # Compute next position
    dir_by_action = {
        Action.north: (0, -1),
        Action.south: (0, 1),
        Action.west: (-1, 0),
        Action.east: (1, 0),
        Action.stay: (0, 0)
    }
    dir = dir_by_action(action)

    x_, y_ = hero.pos.x + dir[0], hero.pos.y + dir[1]
    hero_ = None

    for h in status.heroes:
        if h.pos.x == x_ and h.pos.y == y_:
            hero_ = h
            break

    # Compute side effects of movement
    tile = status._game.map[x_, y_]

    if tile == 0 and not hero_:
        # EMPTY
        hero.pos.x = x_
        hero.pos.y = y_

    elif tile == 3:
        # TAVERN
        if hero.gold > 2:
            hero.gold -= 2
            hero.life = min(hero.life + 50, 100)

    elif tile == 4:
        # MINE
        mine = status.mines[x_, y_]

        # hero is not the mine's owner
        if mine != id + 1:

            # get mine
            if hero.life > 20:
                hero.life -= 20
                hero.mine_count += 1

                # remove mine from previous owner
                if mine is not None:
                    status.heroes[mine - 1].mine_count -= 1

                status.mines[x_, y_] = id + 1

            # dies trying
            else:
                kill(status, id)

    # Fight
    for i, h in enumerate(status.heroes):
        if h == hero:
            continue

        # Attack if 1-tile distance
        if abs(hero.pos.x - h.pos.x) + abs(hero.pos.y - h.pos.y) == 1:

            if h.life > 20:
                h.life -= 20

            else:
                kill(status, i, id)

    # Mining
    hero.gold += hero.mine_count

    # Thirst
    hero.life = max(hero.life - 1, 1)

    status.turn += 1
