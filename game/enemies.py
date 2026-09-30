from dataclasses import dataclass

from game.abilities import Ability, ABILITIES
from game.genome import Genome, Organism
from game.organism_combat import combatant_from_organism


@dataclass(frozen=True)
class EnemyTemplate:
    enemy_id: str
    name: str
    genome: Genome
    ability_id: str


ENEMY_TEMPLATES = (
    EnemyTemplate("brute", "Brute", Genome(strength=6, vitality=4, agility=1), "brutal_strike"),
    EnemyTemplate("runner", "Runner", Genome(strength=2, vitality=2, agility=7), "agile_strike"),
    EnemyTemplate("tank", "Tank", Genome(strength=2, vitality=7, agility=1), "vital_burst"),
)


class EnemyFactory:
    def create(self, enemy_id: str):
        template = next((item for item in ENEMY_TEMPLATES if item.enemy_id == enemy_id), None)
        if template is None:
            raise KeyError(enemy_id)
        organism = Organism(template.genome)
        combatant = combatant_from_organism(template.name, organism)
        ability: Ability = ABILITIES[template.ability_id]
        combatant.energy = ability.energy_cost
        return combatant, organism, ability
