from dataclasses import dataclass


@dataclass
class PlayerProgress:
    player_id: str
    level: int = 1
    experience: int = 0
    skill_points: int = 0


class ProgressionService:
    """Deterministic player XP and level progression for Stage 45."""

    BASE_XP = 100

    def __init__(self, base_xp: int = BASE_XP):
        if base_xp < 1:
            raise ValueError("base_xp must be positive")
        self.base_xp = base_xp
        self.players: dict[str, PlayerProgress] = {}

    def register(self, player_id: str) -> PlayerProgress:
        if not player_id:
            raise ValueError("player_id is required")
        return self.players.setdefault(player_id, PlayerProgress(player_id))

    def xp_to_next_level(self, level: int) -> int:
        if level < 1:
            raise ValueError("level must be positive")
        return self.base_xp * level

    def add_experience(self, player_id: str, amount: int) -> PlayerProgress:
        if amount < 0:
            raise ValueError("experience cannot be negative")
        progress = self.register(player_id)
        progress.experience += amount
        while progress.experience >= self.xp_to_next_level(progress.level):
            progress.experience -= self.xp_to_next_level(progress.level)
            progress.level += 1
            progress.skill_points += 1
        return progress
