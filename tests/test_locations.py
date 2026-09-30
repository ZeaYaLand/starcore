from game.locations import LOCATIONS, get_location


def test_all_locations_have_valid_configuration():
    assert len(LOCATIONS) >= 3
    for location in LOCATIONS:
        assert location.location_id
        assert location.name
        assert location.description
        assert location.energy_cost > 0
        assert 0 <= location.danger <= 100


def test_get_location_is_case_insensitive():
    assert get_location("LABORATORY").location_id == "laboratory"


def test_unknown_location_returns_none():
    assert get_location("missing") is None
