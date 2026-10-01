import json

from sqlalchemy import select

from database.profile_models import PlayerProfile


DEFAULT_ACHIEVEMENTS: list[str] = []
DEFAULT_INVENTORY: list[str] = []


def get_or_create_profile(session, player_id: int) -> PlayerProfile:
    profile = session.scalar(
        select(PlayerProfile).where(PlayerProfile.player_id == player_id)
    )
    if profile is None:
        profile = PlayerProfile(player_id=player_id)
        session.add(profile)
        session.commit()
        session.refresh(profile)
    return profile


def profile_data(profile: PlayerProfile) -> dict:
    return {
        "organism": profile.organism,
        "characteristics": {
            "strength": profile.strength,
            "agility": profile.agility,
            "vitality": profile.vitality,
            "intelligence": profile.intelligence,
        },
        "genome": profile.genome,
        "achievements": json.loads(profile.achievements or "[]"),
        "inventory": json.loads(profile.inventory or "[]"),
    }
