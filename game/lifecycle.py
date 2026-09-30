from dataclasses import dataclass

from game.genome import Organism


@dataclass(frozen=True)
class LifecycleState:
    age: int
    stage: str
    alive: bool


class LifecycleService:
    """Tracks age and life stages without replacing the existing Organism model."""

    STAGES = ((0, "birth"), (3, "growth"), (10, "mature"), (20, "old"))
    DEFAULT_LIFESPAN = 30

    def __init__(self, lifespan: int = DEFAULT_LIFESPAN):
        if lifespan < 1:
            raise ValueError("lifespan must be positive")
        self.lifespan = lifespan

    def state(self, age: int) -> LifecycleState:
        if age < 0:
            raise ValueError("age cannot be negative")
        alive = age < self.lifespan
        stage = "dead" if not alive else self._stage_for_age(age)
        return LifecycleState(age, stage, alive)

    def advance(self, age: int, ticks: int = 1) -> LifecycleState:
        if ticks < 0:
            raise ValueError("ticks cannot be negative")
        return self.state(age + ticks)

    def age_organism(self, organism: Organism, age: int, ticks: int = 1) -> LifecycleState:
        if not isinstance(organism, Organism):
            raise TypeError("organism must be an Organism")
        return self.advance(age, ticks)

    def _stage_for_age(self, age: int) -> str:
        stage = "birth"
        for threshold, name in self.STAGES:
            if age >= threshold:
                stage = name
        return stage
