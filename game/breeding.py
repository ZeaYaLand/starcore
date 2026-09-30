from dataclasses import dataclass
from random import Random

from game.genome import Genome
from game.mutations import MutationGenerator, apply_mutation, combine_genomes


@dataclass(frozen=True)
class Organism:
    organism_id: str
    generation: int
    genome: Genome


class BreedingService:
    def __init__(self, rng: Random | None = None):
        self.rng = rng or Random()
        self.mutations = MutationGenerator(self.rng)

    def breed(self, parent_a: Organism, parent_b: Organism, mutation_chance: float = 0.05, combination_chance: float = 0.10) -> Organism:
        if not 0 <= mutation_chance <= 1:
            raise ValueError("mutation_chance must be between 0 and 1")
        if not 0 <= combination_chance <= 1:
            raise ValueError("combination_chance must be between 0 and 1")
        genome = combine_genomes(parent_a.genome, parent_b.genome)
        if self.rng.random() < mutation_chance:
            genome = apply_mutation(genome, self.mutations.roll())
        combo = self.mutations.roll_combination(combination_chance)
        if combo is not None:
            genome = apply_mutation(genome, combo)
        return Organism(
            organism_id=f"{parent_a.organism_id}-{parent_b.organism_id}-{self.rng.randrange(1_000_000)}",
            generation=max(parent_a.generation, parent_b.generation) + 1,
            genome=genome,
        )
