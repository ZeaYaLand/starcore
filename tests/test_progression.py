import pytest

from database.database import Base, SessionLocal, engine
from services.player_service import (
    add_credits,
    add_xp,
    get_or_create_player,
    spend_energy,
    xp_required_for_level,
)
from game.progression import ProgressionService


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_xp_level_up_resets_energy():
    with SessionLocal() as session:
        player = get_or_create_player(session, 1, "tester")
        player.energy = 10
        session.commit()

        add_xp(session, player, xp_required_for_level(1))

        assert player.level == 2
        assert player.xp == 0
        assert player.energy == 100


def test_multiple_level_ups_are_applied():
    with SessionLocal() as session:
        player = get_or_create_player(session, 2, "tester")
        add_xp(session, player, 250)

        assert player.level == 3
        assert player.xp == 50


def test_energy_can_be_spent_but_not_below_zero():
    with SessionLocal() as session:
        player = get_or_create_player(session, 3, "tester")
        spend_energy(session, player, 25)
        assert player.energy == 75

        with pytest.raises(ValueError):
            spend_energy(session, player, 100)


def test_credits_can_be_added():
    with SessionLocal() as session:
        player = get_or_create_player(session, 4, "tester")
        add_credits(session, player, 50)
        assert player.credits == 150


def test_negative_progression_is_rejected():
    with SessionLocal() as session:
        player = get_or_create_player(session, 5, "tester")

        with pytest.raises(ValueError):
            add_xp(session, player, -1)
        with pytest.raises(ValueError):
            add_credits(session, player, -1)
        with pytest.raises(ValueError):
            spend_energy(session, player, -1)


def test_stage_45_progression_service_levels_and_grants_skill_points():
    service = ProgressionService()
    progress = service.add_experience("stage45", 100)
    assert progress.level == 2
    assert progress.experience == 0
    assert progress.skill_points == 1


def test_stage_45_progression_handles_multiple_levels():
    service = ProgressionService()
    progress = service.add_experience("stage45_multi", 300)
    assert progress.level == 3
    assert progress.experience == 0
    assert progress.skill_points == 2
