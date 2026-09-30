from sqlalchemy import select

from database.models import Player


XP_PER_LEVEL = 100
MAX_ENERGY = 100


def xp_required_for_level(level: int) -> int:
    """Return the XP required to advance from the given level.

    STARCORE currently uses a fixed progression cost so large XP rewards can
    correctly advance a player through multiple levels in one operation.
    """
    return XP_PER_LEVEL


def get_or_create_player(session, telegram_id: int, username: str | None) -> Player:
    player = session.scalar(select(Player).where(Player.telegram_id == telegram_id))
    if player is None:
        player = Player(telegram_id=telegram_id, username=username)
        session.add(player)
        session.commit()
        session.refresh(player)
    elif player.username != username:
        player.username = username
        session.commit()
    return player


def add_xp(session, player: Player, amount: int) -> Player:
    if amount < 0:
        raise ValueError("XP amount cannot be negative")

    player.xp += amount
    while player.xp >= xp_required_for_level(player.level):
        player.xp -= xp_required_for_level(player.level)
        player.level += 1
        player.energy = MAX_ENERGY

    session.commit()
    session.refresh(player)
    return player


def spend_energy(session, player: Player, amount: int) -> Player:
    if amount < 0:
        raise ValueError("Energy amount cannot be negative")
    if player.energy < amount:
        raise ValueError("Not enough energy")

    player.energy -= amount
    session.commit()
    session.refresh(player)
    return player


def add_credits(session, player: Player, amount: int) -> Player:
    if amount < 0:
        raise ValueError("Credits amount cannot be negative")
    player.credits += amount
    session.commit()
    session.refresh(player)
    return player
