import pytest

from game.genome import Genome, Organism
from game.lifecycle import LifecycleService


def test_lifecycle_progresses_through_stages():
    service = LifecycleService()
    assert service.state(0).stage == "birth"
    assert service.state(3).stage == "growth"
    assert service.state(10).stage == "mature"
    assert service.state(20).stage == "old"


def test_lifespan_ends_life():
    service = LifecycleService(lifespan=10)
    state = service.state(10)
    assert state.alive is False
    assert state.stage == "dead"


def test_advance_increases_age():
    state = LifecycleService().advance(9, 2)
    assert state.age == 11
    assert state.stage == "mature"


def test_invalid_age_and_ticks_are_rejected():
    service = LifecycleService()
    with pytest.raises(ValueError):
        service.state(-1)
    with pytest.raises(ValueError):
        service.advance(1, -1)


def test_lifecycle_accepts_existing_organism_model():
    organism = Organism(Genome())
    state = LifecycleService().age_organism(organism, 0, 3)
    assert state.age == 3
    assert state.stage == "growth"
