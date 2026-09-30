import pytest

from game.effects import Effect, EffectService


def test_effect_changes_stat():
    service = EffectService({"strength": 10})
    service.apply(Effect("rage", "strength", 5))
    assert service.stat("strength") == 15


def test_temporary_effect_expires():
    service = EffectService({"agility": 10})
    service.apply(Effect("speed", "agility", 4, remaining_turns=2))
    assert service.stat("agility") == 14
    assert service.tick() == ()
    assert service.stat("agility") == 14
    assert service.tick() == ("speed",)
    assert service.stat("agility") == 10


def test_remove_effect():
    service = EffectService()
    service.apply(Effect("shield", "armor", 3))
    assert service.remove("shield") is True
    assert service.stat("armor") == 0
    assert service.remove("shield") is False


def test_invalid_effect_rejected():
    service = EffectService()
    with pytest.raises(ValueError):
        service.apply(Effect("", "strength", 1))
    with pytest.raises(ValueError):
        service.apply(Effect("x", "strength", 0))
    with pytest.raises(ValueError):
        service.apply(Effect("x", "strength", 1, remaining_turns=-1))
