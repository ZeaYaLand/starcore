from sqlalchemy import select

from database.models import Player


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
