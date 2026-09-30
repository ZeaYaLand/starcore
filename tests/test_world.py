import pytest

from game.world import WorldState


def test_world_starts_at_valid_location_and_tracks_visit():
    world = WorldState()
    assert world.current_location_id == "ruins"
    assert "ruins" in world.visited_locations


def test_world_can_move_between_existing_locations():
    world = WorldState()
    location = world.move_to("laboratory")
    assert location.location_id == "laboratory"
    assert world.current_location_id == "laboratory"
    assert "laboratory" in world.visited_locations


def test_unknown_location_is_rejected():
    world = WorldState()
    with pytest.raises(ValueError):
        world.move_to("unknown")


def test_available_locations_use_existing_location_registry():
    world = WorldState()
    ids = {location.location_id for location in world.available_locations()}
    assert {"ruins", "laboratory", "storm_zone"}.issubset(ids)
