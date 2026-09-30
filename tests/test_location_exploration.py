from game.engine import GameEngine


class DummyPlayer:
    def __init__(self, energy=100):
        self.energy = energy
        self.xp = 0
        self.level = 1


class DummyPlayerService:
    def add_xp(self, player, xp):
        player.xp += xp
        return 0


def test_exploration_uses_location_energy_cost_and_event():
    player = DummyPlayer()
    result = GameEngine(DummyPlayerService()).explore(player, location_id="laboratory")

    assert result.success is True
    assert result.location_id == "laboratory"
    assert result.event_id == "cache"
    assert result.energy_spent == 15
    assert player.energy == 85
    assert result.crystals == 1


def test_storm_location_applies_event_energy_change():
    player = DummyPlayer()
    result = GameEngine(DummyPlayerService()).explore(player, location_id="storm_zone")

    assert result.success is True
    assert result.event_id == "storm"
    assert result.energy_spent == 20
    assert player.energy == 70


def test_unknown_location_does_not_change_player():
    player = DummyPlayer()
    result = GameEngine(DummyPlayerService()).explore(player, location_id="missing")

    assert result.success is False
    assert result.location_id is None
    assert player.energy == 100
