import json

from database.models import Player
from database.profile_models import PlayerProfile


def build_statistics(player: Player, profile: PlayerProfile) -> dict:
    achievements = json.loads(profile.achievements or "[]")
    inventory = json.loads(profile.inventory or "[]")
    characteristics = {
        "strength": profile.strength,
        "agility": profile.agility,
        "vitality": profile.vitality,
        "intelligence": profile.intelligence,
    }

    total_attributes = sum(characteristics.values())
    xp_required = 100
    xp_progress_percent = round(min(player.xp / xp_required, 1) * 100, 2)
    energy_percent = round((player.energy / 100) * 100, 2)
    combat_index = total_attributes + (player.level * 10)
    collection_score = len(achievements) + len(inventory)

    return {
        # Progress analytics — intentionally different from the identity-focused profile.
        "level": player.level,
        "xp": player.xp,
        "xp_required": xp_required,
        "xp_progress_percent": xp_progress_percent,
        "xp_remaining": max(xp_required - player.xp, 0),
        # Resource analytics.
        "credits": player.credits,
        "crystals": player.crystals,
        "energy": player.energy,
        "max_energy": 100,
        "energy_percent": energy_percent,
        # Derived performance indicators.
        "total_attributes": total_attributes,
        "combat_index": combat_index,
        "achievements_unlocked": len(achievements),
        "inventory_items": len(inventory),
        "collection_score": collection_score,
    }
