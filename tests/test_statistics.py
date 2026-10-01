import json

from database.database import Base, SessionLocal, engine
from database.models import Player
from database.profile_models import PlayerProfile
from services.statistics_service import build_statistics


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_statistics_contains_current_player_progress():
    with SessionLocal() as session:
        player = Player(
            telegram_id=56001,
            username="stats_user",
            level=3,
            xp=40,
            credits=275,
            crystals=4,
            energy=65,
        )
        session.add(player)
        session.commit()
        session.refresh(player)

        profile = PlayerProfile(
            player_id=player.id,
            organism="Apex",
            strength=17,
            agility=14,
            vitality=22,
            intelligence=19,
            genome="CORE-56",
            achievements=json.dumps(["a", "b"]),
            inventory=json.dumps(["cell", "crystal", "core"]),
        )
        session.add(profile)
        session.commit()
        session.refresh(profile)

        stats = build_statistics(player, profile)

        assert stats["level"] == 3
        assert stats["xp"] == 40
        assert stats["xp_required"] == 100
        assert stats["xp_progress_percent"] == 40.0
        assert stats["xp_remaining"] == 60
        assert stats["credits"] == 275
        assert stats["crystals"] == 4
        assert stats["energy"] == 65
        assert stats["max_energy"] == 100
        assert stats["energy_percent"] == 65.0
        assert stats["total_attributes"] == 72
        assert stats["combat_index"] == 102
        assert stats["achievements_unlocked"] == 2
        assert stats["inventory_items"] == 3
        assert stats["collection_score"] == 5
        assert "organism" not in stats
        assert "genome" not in stats
        assert "characteristics" not in stats


def test_statistics_uses_profile_defaults_and_empty_collections():
    with SessionLocal() as session:
        player = Player(telegram_id=56002, username="defaults")
        session.add(player)
        session.commit()
        session.refresh(player)

        profile = PlayerProfile(player_id=player.id)
        session.add(profile)
        session.commit()
        session.refresh(profile)

        stats = build_statistics(player, profile)

        assert stats["total_attributes"] == 40
        assert stats["combat_index"] == 50
        assert stats["achievements_unlocked"] == 0
        assert stats["inventory_items"] == 0
        assert stats["collection_score"] == 0
        assert stats["xp_remaining"] == 100
        assert stats["energy_percent"] == 100.0
