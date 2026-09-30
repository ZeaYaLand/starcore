from random import Random

from game.events import EVENTS, EventService


def test_random_event_is_known():
    event = EventService(Random(1)).random_event()
    assert event in EVENTS


def test_location_specific_events():
    service = EventService(Random(1))
    assert service.event_for_location("laboratory").event_id == "cache"
    assert service.event_for_location("storm_zone").event_id == "storm"
    assert service.event_for_location("unknown").event_id == "signal"


def test_event_rewards_are_defined():
    for event in EVENTS:
        assert event.event_id
        assert event.title
        assert event.description
