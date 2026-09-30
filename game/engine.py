from dataclasses import dataclass
from random import Random

from game.events import EventService
from game.locations import get_location


@dataclass(frozen=True)
class ExploreResult:
    success: bool
    message: str
    location_id: str | None
    credits: int
    crystals: int
    energy_spent: int
    xp: int
    event_id: str | None = None


class GameEngine:
    """Game-layer exploration logic with location-specific events."""

    def __init__(self, player_service, event_service=None, rng: Random | None = None):
        # Preserve the Stage 2 constructor: GameEngine(service, Random(...)).
        if isinstance(event_service, Random) and rng is None:
            rng = event_service
            event_service = None
        self.player_service = player_service
        self.rng = rng or Random()
        self.event_service = event_service or EventService(self.rng)

    def explore(self, player, energy_cost: int = 10, location_id: str = "ruins") -> ExploreResult:
        if energy_cost <= 0:
            raise ValueError("energy_cost must be positive")

        location = get_location(location_id)
        if location is None:
            return ExploreResult(False, "Unknown location", None, 0, 0, 0, 0, None)

        # Location configuration is authoritative for exploration cost.
        energy_cost = location.energy_cost
        if player.energy < energy_cost:
            return ExploreResult(False, "Not enough energy", location.location_id, 0, 0, 0, 0, None)

        player.energy -= energy_cost
        event = self.event_service.event_for_location(location.location_id)
        credits = event.credits
        crystals = event.crystals
        xp = event.xp
        if event.energy_change:
            player.energy = max(0, player.energy + event.energy_change)

        self.player_service.add_xp(player, xp)
        return ExploreResult(True, event.title, location.location_id, credits, crystals, energy_cost, xp, event.event_id)
