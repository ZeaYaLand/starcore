import pytest

from game.vitals import Vitals


def test_damage_and_health_states():
    vitals = Vitals()
    assert vitals.state == "healthy"
    vitals.damage(80)
    assert vitals.health == 20
    assert vitals.state == "critical"
    vitals.damage(20)
    assert vitals.health == 0
    assert vitals.state == "dead"
    assert vitals.alive is False


def test_healing_is_capped():
    vitals = Vitals(health=40)
    assert vitals.heal(100) == 100
    assert vitals.state == "healthy"


def test_energy_is_capped_and_cannot_go_negative():
    vitals = Vitals(energy=20)
    assert vitals.consume_energy(50) == 0
    assert vitals.restore_energy(200) == 100


def test_invalid_amounts_are_rejected():
    vitals = Vitals()
    with pytest.raises(ValueError):
        vitals.heal(-1)
    with pytest.raises(ValueError):
        vitals.damage(-1)
    with pytest.raises(ValueError):
        vitals.restore_energy(-1)
    with pytest.raises(ValueError):
        vitals.consume_energy(-1)
