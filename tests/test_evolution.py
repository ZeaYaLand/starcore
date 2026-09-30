import pytest

from game.evolution import EvolutionPathService
from game.genome import Genome, Organism


def test_eligible_evolution_paths_require_generation_and_stat():
    service = EvolutionPathService()
    organism = Organism(Genome(strength=4, vitality=2, agility=2), generation=2)
    paths = service.eligible_paths(organism)
    assert [path.path_id for path in paths] == ["apex_strength"]


def test_evolution_rejects_ineligible_path():
    service = EvolutionPathService()
    organism = Organism(Genome(strength=3), generation=1)
    with pytest.raises(ValueError):
        service.evolve(organism, "apex_strength")


def test_eligible_evolution_advances_generation():
    service = EvolutionPathService()
    organism = Organism(Genome(strength=4), generation=2)
    evolved = service.evolve(organism, "apex_strength")
    assert evolved.generation == 3
    assert evolved.genome == organism.genome
