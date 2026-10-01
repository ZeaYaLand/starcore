from sqlalchemy import select

from database.models import Player


def save_player(session, player: Player) -> Player:
    session.add(player)
    session.commit()
    session.refresh(player)
    return player


def load_player(session, telegram_id: int) -> Player | None:
    return session.scalar(select(Player).where(Player.telegram_id == telegram_id))


def save_and_load_player(session, player: Player) -> Player:
    save_player(session, player)
    restored = load_player(session, player.telegram_id)
    if restored is None:
        raise RuntimeError("Player could not be restored after save")
    return restored
