from dataclasses import dataclass

from game.combat import Combatant


@dataclass(frozen=True)
class AIAction:
    action: str
    target: str | None = None


class OrganismAI:
    """Deterministic baseline AI for organism decisions."""

    def decide(self, actor: Combatant, target: Combatant | None = None) -> AIAction:
        if actor.health <= 0:
            return AIAction("dead")
        if actor.energy <= 0:
            return AIAction("recover")
        if target is None or target.health <= 0:
            return AIAction("explore")
        if actor.health <= max(1, actor.defense // 2):
            return AIAction("recover", actor.name)
        return AIAction("attack", target.name)
