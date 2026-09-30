from dataclasses import dataclass

from game.combat import Combatant
from game.genome import Organism


@dataclass(frozen=True)
class CombatStats:
    health: int
    attack: int
    defense: int
    initiative: int


def stats_from_organism(organism: Organism) -> CombatStats:
    genome = organism.genome
    return CombatStats(
        health=50 + genome.vitality * 10,
        attack=5 + genome.strength * 2,
        defense=genome.vitality,
        initiative=genome.agility,
    )


def combatant_from_organism(name: str, organism: Organism) -> Combatant:
    stats = stats_from_organism(organism)
    return Combatant(name, stats.health, stats.attack, stats.defense)
