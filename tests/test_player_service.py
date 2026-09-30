from database.database import Base, engine, SessionLocal
from database.models import Player
from services.player_service import get_or_create_player


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_player_is_created_with_defaults():
    with SessionLocal() as session:
        player = get_or_create_player(session, 12345, "tester")
        assert player.telegram_id == 12345
        assert player.level == 1
        assert player.credits == 100
        assert player.crystals == 0
        assert player.energy == 100


def test_player_is_not_duplicated():
    with SessionLocal() as session:
        first = get_or_create_player(session, 12345, "tester")
        second = get_or_create_player(session, 12345, "tester")
        assert first.id == second.id
