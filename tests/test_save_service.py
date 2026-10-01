from database.database import Base, SessionLocal, engine
from services.player_service import get_or_create_player
from services.save_service import load_player, save_and_load_player, save_player


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_save_persists_player_state():
    with SessionLocal() as session:
        player = get_or_create_player(session, 58001, "save_user")
        player.credits = 777
        player.crystals = 12
        player.energy = 43
        player.level = 8
        player.xp = 321

        save_player(session, player)
        restored = load_player(session, 58001)

        assert restored is not None
        assert restored.credits == 777
        assert restored.crystals == 12
        assert restored.energy == 43
        assert restored.level == 8
        assert restored.xp == 321


def test_save_and_load_restores_same_player():
    with SessionLocal() as session:
        player = get_or_create_player(session, 58002, "restore_user")
        player.credits = 999
        player.level = 10

        restored = save_and_load_player(session, player)

        assert restored.id == player.id
        assert restored.telegram_id == 58002
        assert restored.credits == 999
        assert restored.level == 10


def test_load_missing_player_returns_none():
    with SessionLocal() as session:
        assert load_player(session, 999999) is None
