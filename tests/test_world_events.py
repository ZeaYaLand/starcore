from game.events import EventService
from game.world_events import WorldEventState


def test_location_event_becomes_active_and_is_recorded():
    state = WorldEventState(EventService())
    event = state.trigger("storm_zone")
    assert event.event_id == "storm"
    assert state.active_event == event
    assert state.last_event() == "storm"


def test_clear_removes_active_event():
    state = WorldEventState(EventService())
    state.trigger("laboratory")
    state.clear()
    assert state.active_event is None


def test_event_history_preserves_order():
    state = WorldEventState(EventService())
    state.trigger("ruins")
    state.trigger("laboratory")
    assert state.history == ["signal", "cache"]
