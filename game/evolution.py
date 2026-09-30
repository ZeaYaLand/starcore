from dataclasses import dataclass

from game.genome import EvolutionService, Organism


@dataclass(frozen=True)
class EvolutionPath:
    path_id: str
    name: str
    required_generation: int
    stat: str
    threshold: int


EVOLUTION_PATHS = (
    EvolutionPath("apex_strength", "Apex Strength", 2, "strength", 4),
    EvolutionPath("apex_vitality", "Apex Vitality", 2, "vitality", 4),
    EvolutionPath("apex_agility", "Apex Agility", 2, "agility", 4),
)


class EvolutionPathService:
    def __init__(self, evolution: EvolutionService | None = None):
        self.evolution = evolution or EvolutionService()

    def eligible_paths(self, organism: Organism) -> tuple[EvolutionPath, ...]:
        return tuple(
            path for path in EVOLUTION_PATHS
            if organism.generation >= path.required_generation
            and getattr(organism.genome, path.stat) >= path.threshold
        )

    def evolve(self, organism: Organism, path_id: str) -> Organism:
        eligible = {path.path_id: path for path in self.eligible_paths(organism)}
        path = eligible.get(path_id)
        if path is None:
            raise ValueError("organism is not eligible for this evolution path")
        return self.evolution.mutate(organism, mutation_chance=0.0)
