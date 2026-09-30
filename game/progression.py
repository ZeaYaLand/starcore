from dataclasses import dataclass


@dataclass
class Progression:
    xp: int = 0
    level: int = 1


class ProgressionService:
    """XP and level progression. XP is never allowed to be negative."""

    @staticmethod
    def xp_for_level(level: int) -> int:
        if level < 1:
            raise ValueError("level must be at least 1")
        return 100 * (level - 1)

    @staticmethod
    def add_xp(progress: Progression, amount: int) -> list[int]:
        if amount < 0:
            raise ValueError("XP amount must be non-negative")
        if amount == 0:
            return []

        progress.xp += amount
        levels_gained = []
        while progress.xp >= ProgressionService.xp_for_level(progress.level + 1):
            progress.level += 1
            levels_gained.append(progress.level)
        return levels_gained
