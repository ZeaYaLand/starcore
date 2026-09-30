from dataclasses import dataclass

from game.enemies import EnemyTemplate


@dataclass(frozen=True)
class VictoryReward:
    xp: int
    credits: int


def reward_for_enemy(enemy: EnemyTemplate) -> VictoryReward:
    power = enemy.genome.strength + enemy.genome.vitality + enemy.genome.agility
    return VictoryReward(xp=25 + power * 5, credits=10 + power * 3)
