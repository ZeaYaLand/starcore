from random import Random

import pytest

from game.genome import EvolutionService, Genome, Organism


def test_genome_requires_positive_stats():
    with pytest.raises(ValueError):
        Genome(strength=0)


def test_evolution_always_advances_generation():
    organism = Organism(Genome(), generation=1)
    evolved = EvolutionService(Random(1)).mutate(organism, mutation_chance=0)
    assert evolved.generation == 2
    assert evolved.genome == organism.genome


def test_mutation_changes_a_stat_with_deterministic_rng():
    organism = Organism(Genome(), generation=1)
    evolved = EvolutionService(Random(1)).mutate(organism, mutation_chance=1)
    assert evolved.generation == 2
    assert evolved.genome != organism.genome
    assert min(evolved.genome.strength, evolved.genome.vitality, evolved.genome.agility) >= 1


def test_mutation_chance_is_validated():
    service = EvolutionService(Random(1))
    organism = Organism(Genome())
    with pytest.raises(ValueError):
        service.mutate(organism, mutation_chance=1.1)
