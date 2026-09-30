from random import Random

import pytest

from game.genome import Genome
from game.mutations import MUTATIONS, MutationGenerator, apply_mutation


def test_positive_mutation_changes_genome():
    genome = Genome(strength=3, vitality=3, agility=3)
    mutation = next(m for m in MUTATIONS if m.mutation_id == "muscle_fibers")
    mutated = apply_mutation(genome, mutation)
    assert mutated.strength == 5
    assert mutated.vitality == 3
    assert mutated.agility == 3


def test_negative_delta_respects_genome_minimum():
    genome = Genome(strength=1, vitality=1, agility=1)
    mutation = next(m for m in MUTATIONS if m.mutation_id == "unstable_growth")
    mutated = apply_mutation(genome, mutation)
    assert mutated.vitality == 1
    assert mutated.strength == 4


def test_seeded_generator_is_reproducible():
    first = MutationGenerator(Random(42)).roll().mutation_id
    second = MutationGenerator(Random(42)).roll().mutation_id
    assert first == second


def test_invalid_rare_chance_is_rejected():
    with pytest.raises(ValueError):
        MutationGenerator(Random(1)).roll(1.1)
