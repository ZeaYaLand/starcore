from game.enemies import ENEMY_TEMPLATES
from game.victory_rewards import reward_for_enemy


def test_victory_reward_scales_with_enemy_power():
    brute = next(enemy for enemy in ENEMY_TEMPLATES if enemy.enemy_id == "brute")
    runner = next(enemy for enemy in ENEMY_TEMPLATES if enemy.enemy_id == "runner")
    brute_reward = reward_for_enemy(brute)
    runner_reward = reward_for_enemy(runner)
    brute_power = sum((brute.genome.strength, brute.genome.vitality, brute.genome.agility))
    runner_power = sum((runner.genome.strength, runner.genome.vitality, runner.genome.agility))

    assert brute_reward.xp == 25 + brute_power * 5
    assert runner_reward.credits == 10 + runner_power * 3


def test_victory_reward_is_positive():
    for enemy in ENEMY_TEMPLATES:
        reward = reward_for_enemy(enemy)
        assert reward.xp > 0
        assert reward.credits > 0
