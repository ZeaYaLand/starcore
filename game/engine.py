from dataclasses import dataclass
from random import Random


@dataclass(frozen=True)
class ExploreResult:
    success: bool
    message: str
    credits: int
    crystals: int
    energy_spent: int
    xp: int


class GameEngine:
    """Pure game-layer exploration logic.

    The XP service is injected so the engine does not depend on a concrete
    database service implementation. This keeps the game layer testable and
    avoids coupling it to SQLAlchemy/session details.
    """

    def __init__(self, player_service, rng: Random | None = None):
        self.player_service = player_service
        self.rng = rng or Random()

    def explore(self, player, energy_cost: int = 10) -> ExploreResult:
        if energy_cost <= 0:
            raise ValueError("energy_cost must be positive")
        if player.energy < energy_cost:
            return ExploreResult(False, "Not enough energy", 0, 0, 0, 0)

        player.energy -= energy_cost
        credits = self.rng.randint(10, 40)
        crystals = 1 if self.rng.random() < 0.20 else 0
        xp = self.rng.randint(5, 15)
        levels = self.player_service.add_xp(player, xp)
        message = "Exploration complete"
        if levels:
            message += f". Level up: +{levels}"
        return ExploreResult(True, message, credits, crystals, energy_cost, xp)
