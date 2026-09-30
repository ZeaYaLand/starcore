from dataclasses import dataclass

from game.rewards import Reward


@dataclass(frozen=True)
class Quest:
    quest_id: str
    title: str
    target: int
    reward: Reward
    objective_type: str = "generic"
    min_danger: int = 0


@dataclass(frozen=True)
class QuestProgress:
    quest_id: str
    progress: int
    completed: bool
    claimed: bool


class QuestService:
    def __init__(self, quests: tuple[Quest, ...]):
        self.quests = {quest.quest_id: quest for quest in quests}
        self.progress: dict[str, int] = {}
        self.claimed: set[str] = set()

    def advance(self, quest_id: str, amount: int = 1) -> QuestProgress:
        if amount <= 0:
            raise ValueError("amount must be positive")
        quest = self.quests[quest_id]
        current = min(quest.target, self.progress.get(quest_id, 0) + amount)
        self.progress[quest_id] = current
        return self.status(quest_id)

    def record_event(self, objective_type: str, amount: int = 1, danger: int = 0) -> tuple[QuestProgress, ...]:
        if amount <= 0:
            raise ValueError("amount must be positive")
        updated = []
        for quest in self.quests.values():
            if quest.objective_type == objective_type and danger >= quest.min_danger:
                updated.append(self.advance(quest.quest_id, amount))
        return tuple(updated)

    def status(self, quest_id: str) -> QuestProgress:
        quest = self.quests[quest_id]
        current = self.progress.get(quest_id, 0)
        return QuestProgress(quest_id, current, current >= quest.target, quest_id in self.claimed)

    def claim(self, quest_id: str) -> Reward:
        status = self.status(quest_id)
        if not status.completed or status.claimed:
            return Reward()
        self.claimed.add(quest_id)
        return self.quests[quest_id].reward


DEFAULT_QUESTS = (
    Quest("explore_3", "Explore 3 times", 3, Reward(xp=30, credits=100), "explore"),
    Quest("danger_2", "Survive 2 dangerous expeditions", 2, Reward(xp=60, credits=180), "explore", min_danger=2),
    Quest("win_2", "Win 2 battles", 2, Reward(xp=50, credits=150, crystals=1), "battle"),
    Quest("breed_2", "Create 2 offspring", 2, Reward(xp=70, credits=120), "breed"),
)
