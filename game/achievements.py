from dataclasses import dataclass

from game.rewards import Reward


@dataclass(frozen=True)
class Achievement:
    achievement_id: str
    title: str
    objective_type: str
    target: int
    reward: Reward


class AchievementService:
    def __init__(self, achievements: tuple[Achievement, ...]):
        self.achievements = {a.achievement_id: a for a in achievements}
        self.progress: dict[str, int] = {}
        self.unlocked: set[str] = set()

    def record_event(self, objective_type: str, amount: int = 1) -> tuple[str, ...]:
        if amount <= 0:
            raise ValueError("amount must be positive")
        newly_unlocked = []
        for achievement in self.achievements.values():
            if achievement.objective_type != objective_type or achievement.achievement_id in self.unlocked:
                continue
            current = min(achievement.target, self.progress.get(achievement.achievement_id, 0) + amount)
            self.progress[achievement.achievement_id] = current
            if current >= achievement.target:
                self.unlocked.add(achievement.achievement_id)
                newly_unlocked.append(achievement.achievement_id)
        return tuple(newly_unlocked)

    def is_unlocked(self, achievement_id: str) -> bool:
        return achievement_id in self.unlocked

    def claim(self, achievement_id: str) -> Reward:
        if achievement_id not in self.unlocked:
            return Reward()
        self.unlocked.remove(achievement_id)
        return self.achievements[achievement_id].reward


DEFAULT_ACHIEVEMENTS = (
    Achievement("explorer", "Explorer", "explore", 10, Reward(xp=100, credits=250)),
    Achievement("survivor", "Survivor", "battle", 10, Reward(xp=120, credits=300)),
    Achievement("breeder", "Breeder", "breed", 5, Reward(xp=150, credits=350)),
    Achievement("mutant", "Mutant", "mutation", 3, Reward(xp=180, credits=400, crystals=2)),
)
