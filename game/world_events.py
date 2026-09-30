from dataclasses import dataclass, field

from game.events import EventService, GameEvent


@dataclass
class WorldEventState:
    event_service: EventService = field(default_factory=EventService)
    active_event: GameEvent | None = None
    history: list[str] = field(default_factory=list)

    def trigger(self, location: str) -> GameEvent:
        event = self.event_service.event_for_location(location)
        self.active_event = event
        self.history.append(event.event_id)
        return event

    def clear(self) -> None:
        self.active_event = None

    def last_event(self) -> str | None:
        return self.history[-1] if self.history else None
