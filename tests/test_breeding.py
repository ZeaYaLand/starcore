from random import Random

import pytest

from game.breeding import BreedingService, Organism
from game.genome import Genome
from game.mutations import MutationGenerator, combine_genomes


def parents():
    return (
        Organism("alpha", 2, Genome(strength=2, vitality=5, agility=8)),
        Organism("beta", 3, Genome(strength=7, vitality=4, agility=3)),
    )


def test_breeding_inherits_strongest_gene_from_parents():
    parent_a, parent_b = parents()
    child = BreedingService(Random(4)).breed(parent_a, parent_b, mutation_chance=0, combination_chance=0)
    assert child.generation == 4
    assert child.genome == Genome(strength=7, vitality=5, agility=8)


def test_breeding_can_apply_mutation():
    parent_a, parent_b = parents()
    child = BreedingService(Random(2)).breed(parent_a, parent_b, mutation_chance=1, combination_chance=0)
    assert child.generation == 4
    assert child.genome.strength >= 1
    assert child.genome.vitality >= 1
    assert child.genome.agility >= 1


def test_combination_mutation_can_be_forced():
    parent_a, parent_b = parents()
    child = BreedingService(Random(5)).breed(parent_a, parent_b, mutation_chance=0, combination_chance=1)
    assert child.generation == 4
    assert child.genome.strength >= 8 or child.genome.vitality >= 6 or child.genome.agility >= 9


def test_combine_genomes_keeps_the_strongest_trait():
    result = combine_genomes(Genome(strength=2, vitality=8, agility=3), Genome(strength=7, vitality=4, agility=9))
    assert result == Genome(strength=7, vitality=8, agility=9)


def test_rare_mutation_can_be_forced():
    mutation = MutationGenerator(Random(1)).roll(rare_chance=1)
    assert mutation.rare is True


def test_invalid_chances_are_rejected():
    parent_a, parent_b = parents()
    with pytest.raises(ValueError):
        BreedingService(Random(1)).breed(parent_a, parent_b, mutation_chance=1.1)
    with pytest.raises(ValueError):
        BreedingService(Random(1)).breed(parent_a, parent_b, combination_chance=-0.1)
