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
    xp_progress_percent = round((player.xp / 100) * 100, 2)

    return {
        "level": player.level,
        "xp": player.xp,
        "xp_required": 100,
        "xp_progress_percent": xp_progress_percent,
        "credits": player.credits,
        "crystals": player.crystals,
        "energy": player.energy,
        "max_energy": 100,
        "organism": profile.organism,
        "genome": profile.genome,
        "characteristics": characteristics,
        "total_attributes": total_attributes,
        "achievements_unlocked": len(achievements),
        "inventory_items": len(inventory),
    }
