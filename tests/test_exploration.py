from random import Random

from game.exploration import ZONES, ExplorationService


def test_exploration_uses_selected_zone():
    zone = ZONES[1]
    result = ExplorationService(Random(7)).explore(zone)
    assert result.zone_id == zone.zone_id
    assert result.event in zone.events
    assert result.discovery in zone.discoveries
    assert result.danger == zone.difficulty


def test_random_exploration_returns_known_zone():
    result = ExplorationService(Random(42)).explore()
    assert result.zone_id in {zone.zone_id for zone in ZONES}
    assert result.danger >= 1


def test_zones_have_events_and_discoveries():
    for zone in ZONES:
        assert zone.events
        assert zone.discoveries
        assert zone.difficulty >= 1
