from dataclasses import dataclass
from random import Random

from game.genome import Genome


@dataclass(frozen=True)
class Mutation:
    mutation_id: str
    name: str
    strength_delta: int = 0
    vitality_delta: int = 0
    agility_delta: int = 0
    rare: bool = False


MUTATIONS = (
    Mutation("muscle_fibers", "Muscle Fibers", strength_delta=2),
    Mutation("dense_cells", "Dense Cells", vitality_delta=2),
    Mutation("neural_spike", "Neural Spike", agility_delta=2),
    Mutation("unstable_growth", "Unstable Growth", strength_delta=3, vitality_delta=-1),
    Mutation("quantum_adaptation", "Quantum Adaptation", strength_delta=2, vitality_delta=2, agility_delta=2, rare=True),
)


def apply_mutation(genome: Genome, mutation: Mutation) -> Genome:
    return Genome(
        strength=max(1, genome.strength + mutation.strength_delta),
        vitality=max(1, genome.vitality + mutation.vitality_delta),
        agility=max(1, genome.agility + mutation.agility_delta),
    )


class MutationGenerator:
    def __init__(self, rng: Random | None = None):
        self.rng = rng or Random()

    def roll(self, rare_chance: float = 0.05) -> Mutation:
        if not 0 <= rare_chance <= 1:
            raise ValueError("rare_chance must be between 0 and 1")
        rare = [m for m in MUTATIONS if m.rare]
        common = [m for m in MUTATIONS if not m.rare]
        if rare and self.rng.random() < rare_chance:
            return self.rng.choice(rare)
        return self.rng.choice(common)
