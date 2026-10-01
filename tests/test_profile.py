from database.database import Base, SessionLocal, engine
from database.profile_models import PlayerProfile
from services.player_service import get_or_create_player
from services.profile_service import get_or_create_profile, profile_data


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_profile_is_created_with_complete_defaults():
    with SessionLocal() as session:
        player = get_or_create_player(session, 55001, "profile_user")
        profile = get_or_create_profile(session, player.id)
        data = profile_data(profile)

        assert data["organism"] == "Нулевой организм"
        assert data["characteristics"] == {
            "strength": 10,
            "agility": 10,
            "vitality": 10,
            "intelligence": 10,
        }
        assert data["genome"] == "CORE-0001"
        assert data["achievements"] == []
        assert data["inventory"] == []


def test_profile_is_not_duplicated():
    with SessionLocal() as session:
        player = get_or_create_player(session, 55002, "profile_user")
        first = get_or_create_profile(session, player.id)
        second = get_or_create_profile(session, player.id)

        assert first.id == second.id
        assert session.query(PlayerProfile).count() == 1


def test_profile_data_reads_achievements_and_inventory():
    with SessionLocal() as session:
        player = get_or_create_player(session, 55003, "profile_user")
        profile = get_or_create_profile(session, player.id)
        profile.achievements = '["first_blood", "explorer"]'
        profile.inventory = '["starter_cell", "crystal"]'
        session.commit()
        session.refresh(profile)

        data = profile_data(profile)

        assert data["achievements"] == ["first_blood", "explorer"]
        assert data["inventory"] == ["starter_cell", "crystal"]


def test_profile_characteristics_are_persisted():
    with SessionLocal() as session:
        player = get_or_create_player(session, 55004, "profile_user")
        profile = get_or_create_profile(session, player.id)
        profile.strength = 17
        profile.agility = 14
        profile.vitality = 22
        profile.intelligence = 19
        profile.genome = "CORE-55-ALPHA"
        session.commit()
        session.refresh(profile)

        data = profile_data(profile)

        assert data["characteristics"]["strength"] == 17
        assert data["characteristics"]["agility"] == 14
        assert data["characteristics"]["vitality"] == 22
        assert data["characteristics"]["intelligence"] == 19
        assert data["genome"] == "CORE-55-ALPHA"
