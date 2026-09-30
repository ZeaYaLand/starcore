from dataclasses import dataclass
from random import Random


@dataclass(frozen=True)
class GameEvent:
    event_id: str
    title: str
    description: str
    credits: int = 0
    crystals: int = 0
    xp: int = 0
    energy_change: int = 0


EVENTS = (
    GameEvent("signal", "Unknown Signal", "A strange signal comes from the sector.", credits=20, xp=8),
    GameEvent("cache", "Hidden Cache", "You discover an abandoned supply cache.", credits=40, crystals=1, xp=12),
    GameEvent("storm", "Energy Storm", "An energy storm damages your reserves.", energy_change=-10, xp=6),
)


class EventService:
    def __init__(self, rng: Random | None = None):
        self.rng = rng or Random()

    def random_event(self) -> GameEvent:
        return self.rng.choice(EVENTS)

    def event_for_location(self, location: str) -> GameEvent:
        normalized = location.strip().lower()
        if normalized == "laboratory":
            return EVENTS[1]
        if normalized == "storm_zone":
            return EVENTS[2]
        return EVENTS[0]
