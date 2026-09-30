from random import Random

import pytest

from game.breeding import BreedingService, Organism
from game.genome import Genome


def parents():
    return (
        Organism("alpha", 2, Genome(strength=2, vitality=5, agility=8)),
        Organism("beta", 3, Genome(strength=7, vitality=4, agility=3)),
    )


def test_breeding_inherits_each_stat_from_a_parent():
    parent_a, parent_b = parents()
    child = BreedingService(Random(4)).breed(parent_a, parent_b, mutation_chance=0)
    assert child.generation == 4
    assert child.genome.strength in (2, 7)
    assert child.genome.vitality in (5, 4)
    assert child.genome.agility in (8, 3)


def test_breeding_can_apply_mutation():
    parent_a, parent_b = parents()
    child = BreedingService(Random(2)).breed(parent_a, parent_b, mutation_chance=1)
    assert child.generation == 4
    assert child.genome.strength >= 1
    assert child.genome.vitality >= 1
    assert child.genome.agility >= 1


def test_invalid_mutation_chance_is_rejected():
    parent_a, parent_b = parents()
    with pytest.raises(ValueError):
        BreedingService(Random(1)).breed(parent_a, parent_b, mutation_chance=1.1)
