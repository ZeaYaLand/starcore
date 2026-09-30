from game.combat import CombatResult
from game.rewards import Reward, RewardService


def test_victory_reward_can_be_claimed_once():
    service = RewardService()
    result = CombatResult("Player", 3, 30, 5)
    reward = Reward(xp=25, credits=100, crystals=2)

    first = service.claim_combat_reward("combat-1", result, reward)
    second = service.claim_combat_reward("combat-1", result, reward)

    assert first == reward
    assert second == Reward()


def test_defeat_gives_no_reward():
    service = RewardService()
    result = CombatResult("Enemy", 2, 5, 20)
    reward = Reward(xp=25, credits=100, crystals=2)

    assert service.claim_combat_reward("combat-2", result, reward) == Reward()
