from dataclasses import dataclass
from datetime import date

from game.rewards import Reward


@dataclass(frozen=True)
class DailyActivity:
    activity_id: str
    title: str
    target: int
    reward: Reward


class DailyService:
    def __init__(self, activities: tuple[DailyActivity, ...]):
        self.activities = {a.activity_id: a for a in activities}
        self.progress: dict[str, int] = {}
        self.claimed_on: dict[str, date] = {}

    def advance(self, activity_id: str, amount: int = 1) -> int:
        if amount <= 0:
            raise ValueError("amount must be positive")
        activity = self.activities[activity_id]
        current = min(activity.target, self.progress.get(activity_id, 0) + amount)
        self.progress[activity_id] = current
        return current

    def claim(self, activity_id: str, today: date | None = None) -> Reward:
        today = today or date.today()
        activity = self.activities[activity_id]
        if self.progress.get(activity_id, 0) < activity.target:
            return Reward()
        if self.claimed_on.get(activity_id) == today:
            return Reward()
        self.claimed_on[activity_id] = today
        self.progress[activity_id] = 0
        return activity.reward


DEFAULT_DAILY_ACTIVITIES = (
    DailyActivity("daily_explore", "Explore 3 times today", 3, Reward(xp=20, credits=75)),
    DailyActivity("daily_battle", "Win 1 battle today", 1, Reward(xp=30, credits=100, crystals=1)),
)
