from random import Random

from game.enemies import ENEMY_TEMPLATES, EnemyFactory


class RandomEnemyFactory:
    def __init__(self, rng: Random | None = None):
        self.rng = rng or Random()

    def create(self, difficulty: int = 1):
        if difficulty < 1:
            raise ValueError("difficulty must be at least 1")
        available = [template for template in ENEMY_TEMPLATES if template.genome.strength + template.genome.vitality + template.genome.agility <= difficulty * 10 + 10]
        if not available:
            available = list(ENEMY_TEMPLATES)
        template = self.rng.choice(available)
        return EnemyFactory().create(template.enemy_id)
