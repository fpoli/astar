# -*- coding: UTF-8 -*-

from lib.models import Action, Tile, Position, action_to_dir


def kill_in_place(status, hero_id, killer_id=None):
    """Recursively kills a hero.

    The status given as parameter will be used to store the result.

    Arguments:
        status (Status): the (mutable) game status.
        hero_id (int): the id of the killed hero.
        killer_id (int | None): the id of the killer.

    Results:
        The status given as parameter will be used to store the result.
    """
    hero = status.heroes[hero_id]

    for other_id, other in enumerate(status.heroes):
        if other_id == hero_id:
            continue

        if other.pos == hero.spawn:
            kill_in_place(status, other_id)

    hero.pos = hero.spawn
    hero.mine_count = 0
    hero.life = 100

    for pos, owner in status.mine_owner.items():
        if owner == hero_id:
            if killer_id is None:
                status.mine_owner[pos] = None
            else:
                status.mine_owner[pos] = killer_id
                status.heroes[killer_id].mine_count += 1


def simulate_in_place(status, action):
    """Simulate a movement given a Status.

    Arguments:
        status (Status): the (mutable) game status.
        action (Action): the action to simulate.

    Results:
        The status given as parameter will be used to store the result.
    """
    hero_id = status.current_hero()
    hero = status.heroes[hero_id]
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
        owner = status.mine_owner[dst_pos]

        # hero is not the mine"s owner
        if owner != hero_id:

            # get mine
            if hero.life > 20:
                hero.life -= 20
                hero.mine_count += 1

                # remove mine from previous owner
                if owner is not None:
                    status.heroes[owner].mine_count -= 1

                status.mine_owner[dst_pos] = hero_id

            # Hero dies trying
            else:
                kill_in_place(status, hero_id, None)

    # Fight
    for other_id, other in enumerate(status.heroes):
        if other_id == hero_id:
            continue

        # Attack if 1-tile distance
        if abs(hero.pos.x - other.pos.x) + abs(hero.pos.y - other.pos.y) == 1:

            if other.life > 20:
                other.life -= 20

            else:
                # Hero kills the other
                kill_in_place(status, other_id, hero_id)

    # Mining
    hero.gold += hero.mine_count

    # Thirst
    hero.life = max(hero.life - 1, 1)

    status.turn += 1
    status.finished = status.turn >= status.max_turns

    return status


def simulate(original_status, action):
    """Simulate a movement given a Status.

    Arguments:
        original_status (Status): the game status. This will not be modified.
        action (Action): the action to simulate.

    Returns:
        Status: the next status (a new object).
    """
    status = original_status.clone()

    simulate_in_place(status, action)

    return status


def simulate_actions(original_status, actions):
    """Simulate a list of actions.

    Arguments:
        original_status (Status): the game status. This will not be modified.
        actions (list of Action): the actions.

    Returns:
        Status: the next status (a new object).
    """
    status = original_status.clone()

    for action in actions:
        simulate_in_place(status, action)

    return status
