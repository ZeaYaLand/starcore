from random import Random

from game.engine import GameEngine


class DummyPlayer:
    def __init__(self, energy=100):
        self.energy = energy
        self.xp = 0
        self.level = 1


def test_explore_spends_energy_and_rewards_resources():
    player = DummyPlayer()
    service = type("Service", (), {"add_xp": lambda self, p, xp: setattr(p, "xp", p.xp + xp) or 0})()
    result = GameEngine(service, Random(1)).explore(player, 10)

    assert result.success is True
    assert result.energy_spent == 10
    assert player.energy == 90
    assert result.credits >= 10
    assert result.xp >= 5


def test_explore_requires_energy():
    player = DummyPlayer(energy=5)
    service = type("Service", (), {"add_xp": lambda self, p, xp: 0})()
    result = GameEngine(service, Random(1)).explore(player, 10)

    assert result.success is False
    assert player.energy == 5
    assert result.energy_spent == 0


def test_invalid_energy_cost_is_rejected():
    player = DummyPlayer()
    service = type("Service", (), {"add_xp": lambda self, p, xp: 0})()
    try:
        GameEngine(service, Random(1)).explore(player, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")
