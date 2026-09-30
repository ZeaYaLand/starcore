from dataclasses import dataclass

from game.combat import CombatResult


@dataclass(frozen=True)
class Reward:
    xp: int = 0
    credits: int = 0
    crystals: int = 0


class RewardService:
    def __init__(self):
        self._claimed: set[str] = set()

    def claim_combat_reward(self, combat_id: str, result: CombatResult, victory_reward: Reward) -> Reward:
        if combat_id in self._claimed:
            return Reward()
        if result.winner != "Player":
            return Reward()
        self._claimed.add(combat_id)
        return victory_reward
