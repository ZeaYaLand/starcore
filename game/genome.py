from dataclasses import dataclass, replace
from random import Random


@dataclass(frozen=True)
class Genome:
    strength: int = 1
    vitality: int = 1
    agility: int = 1

    def __post_init__(self):
        if min(self.strength, self.vitality, self.agility) < 1:
            raise ValueError("genome stats must be at least 1")


@dataclass(frozen=True)
class Organism:
    genome: Genome
    generation: int = 1


class EvolutionService:
    def __init__(self, rng: Random | None = None):
        self.rng = rng or Random()

    def mutate(self, organism: Organism, mutation_chance: float = 0.25) -> Organism:
        if not 0 <= mutation_chance <= 1:
            raise ValueError("mutation_chance must be between 0 and 1")
        genome = organism.genome
        if self.rng.random() >= mutation_chance:
            return replace(organism, generation=organism.generation + 1)
        stat = self.rng.choice(("strength", "vitality", "agility"))
        value = getattr(genome, stat) + self.rng.choice((-1, 1))
        value = max(1, value)
        return Organism(replace(genome, **{stat: value}), organism.generation + 1)
