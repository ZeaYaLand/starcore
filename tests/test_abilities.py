from game.abilities import AbilityService
from game.genome import Genome, Organism


def test_strength_ability_scales_with_genome():
    organism = Organism(Genome(strength=4, vitality=1, agility=1))
    result = AbilityService().use("brutal_strike", organism, energy=20)

    assert result.success is True
    assert result.damage == 16
    assert result.energy_spent == 10


def test_ability_requires_enough_energy():
    organism = Organism(Genome())
    result = AbilityService().use("brutal_strike", organism, energy=9)

    assert result.success is False
    assert result.damage == 0
    assert result.energy_spent == 0


def test_unknown_ability_is_rejected():
    result = AbilityService().use("unknown", Organism(Genome()), energy=100)
    assert result.success is False
