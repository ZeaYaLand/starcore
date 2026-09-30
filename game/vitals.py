from dataclasses import dataclass


@dataclass
class Vitals:
    max_health: int = 100
    health: int = 100
    max_energy: int = 100
    energy: int = 100
    state: str = "healthy"

    def __post_init__(self) -> None:
        if self.max_health <= 0 or self.max_energy <= 0:
            raise ValueError("maximum vitals must be positive")
        self.health = max(0, min(self.health, self.max_health))
        self.energy = max(0, min(self.energy, self.max_energy))
        self._refresh_state()

    def heal(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("amount must be non-negative")
        self.health = min(self.max_health, self.health + amount)
        self._refresh_state()
        return self.health

    def damage(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("amount must be non-negative")
        self.health = max(0, self.health - amount)
        self._refresh_state()
        return self.health

    def restore_energy(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("amount must be non-negative")
        self.energy = min(self.max_energy, self.energy + amount)
        return self.energy

    def consume_energy(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("amount must be non-negative")
        self.energy = max(0, self.energy - amount)
        return self.energy

    def _refresh_state(self) -> None:
        if self.health == 0:
            self.state = "dead"
        elif self.health <= self.max_health // 4:
            self.state = "critical"
        elif self.health < self.max_health:
            self.state = "injured"
        else:
            self.state = "healthy"

    @property
    def alive(self) -> bool:
        return self.health > 0
