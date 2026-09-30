from game.abilities import AbilityService
from game.genome import Genome, Organism


def test_strength_ability_scales_with_genome():
    organism = Organism(Genome(strength=4, vitality=1, agility=1))
    result = AbilityService().use("brutal_strike", organism, energy=20)
    assert result.success is True
    assert result.damage == 16
    assert result.energy_spent == 10
    assert result.cooldown == 1


def test_ability_requires_enough_energy():
    organism = Organism(Genome())
    result = AbilityService().use("brutal_strike", organism, energy=9)
    assert result.success is False


def test_unknown_ability_is_rejected():
    result = AbilityService().use("unknown", Organism(Genome()), energy=100)
    assert result.success is False


def test_cooldown_blocks_repeat_use_until_tick():
    service = AbilityService()
    organism = Organism(Genome(strength=4, vitality=1, agility=1))
    assert service.use("brutal_strike", organism, 100).success is True
    assert service.cooldown_remaining(organism, "brutal_strike") == 1
    assert service.use("brutal_strike", organism, 100).success is False
    service.tick()
    assert service.cooldown_remaining(organism, "brutal_strike") == 0
    assert service.use("brutal_strike", organism, 100).success is True


def test_ability_can_return_an_effect():
    service = AbilityService()
    organism = Organism(Genome(vitality=5))
    result = service.use("vital_burst", organism, 100)
    assert result.success is True
    assert result.effect_id == "vital_burst"
