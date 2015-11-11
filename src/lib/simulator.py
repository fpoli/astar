# -*- coding: UTF-8 -*-

from copy import copy, deepcopy
from lib.models import Action, Tile, Position, action_to_dir


def __kill(status, hero_id, killer_id=None):
    """Recursively kills a hero.

    The status given as parameter will be used to store the result.

    Arguments:
        status (Status): the (mutable) game status.
        hero_id (int): the id of the killed hero.
        killer_id (int | None): the id of the killer.

    Results:
        The status given as parameter will be used to store the result.
    """
    hero = status.heroes[hero_id - 1]

    for other_id, other in enumerate(status.heroes, start=1):
        if other_id == hero_id:
            continue

        if other.pos == hero.spawn:
            __kill(status, other_id)

    hero.pos = hero.spawn
    hero.mine_count = 0
    hero.life = 100

    for pos, mine in status.mines.items():
        if mine.owner == hero_id:
            if killer_id is None:
                status.mines[pos].owner = None
            else:
                status.mines[pos].owner = killer_id
                status.heroes[killer_id - 1].mine_count += 1


def __simulate_turn(status, action):
    """Simulate a movement given a Status.

    Arguments:
        status (Status): the (mutable) game status.
        action (Action): the action to simulate.

    Results:
        The status given as parameter will be used to store the result.
    """
    hero_id = status.current_hero()
    hero = status.heroes[hero_id - 1]
    hero.last_dir = action

    # Compute next position
    direction = action_to_dir(action)
    dst_pos = hero.pos + direction

    # Checks if there is an anemy
    enemy = None
    for other in status.heroes:
        if other.pos == dst_pos:
            enemy = other
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

        # hero is not the mine"s owner
        if mine.owner != hero_id:

            # get mine
            if hero.life > 20:
                hero.life -= 20
                hero.mine_count += 1

                # remove mine from previous owner
                if mine.owner is not None:
                    status.heroes[mine.owner - 1].mine_count -= 1

                status.mines[dst_pos].owner = hero_id

            # Hero dies trying
            else:
                __kill(status, hero_id, None)

    # Fight
    for other_id, other in enumerate(status.heroes, start=1):
        if other_id == hero_id:
            continue

        # Attack if 1-tile distance
        if abs(hero.pos.x - other.pos.x) + abs(hero.pos.y - other.pos.y) == 1:

            if other.life > 20:
                other.life -= 20

            else:
                # Hero kills the other
                __kill(status, other_id, hero_id)

    # Mining
    hero.gold += hero.mine_count

    # Thirst
    hero.life = max(hero.life - 1, 1)

    status.turn += 1
    status.finished = status.turn >= status.max_turns

    return status


def simulate_turn(original_status, action):
    """Simulate a movement given a Status.

    Arguments:
        original_status (Status): the game status. This will not be modified.
        action (Action): the action to simulate.

    Returns:
        Status: the next status (a new object).
    """
    # Clone the status object
    status = copy(original_status)
    status.heroes = deepcopy(original_status.heroes)
    status.mines = deepcopy(original_status.mines)

    __simulate_turn(status, action)

    return status


def simulate(original_status, actions):
    """Simulate a round (4 hero actions).

    Arguments:
        original_status (Status): the game status. This will not be modified.
        actions (tuple of 4 Actions): the actions, ordered by hero"s id.

    Returns:
        Status: the next status (a new object).
    """
    # Check that the next action is executed by hero 1
    assert(original_status.turn % 4 == 0)

    # Clone the status object
    status = copy(original_status)
    status.heroes = deepcopy(original_status.heroes)
    status.mines = deepcopy(original_status.mines)

    for hero_id in range(1, 5):
        __simulate_turn(status, actions[hero_id - 1])

    return status
