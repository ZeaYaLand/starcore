from dataclasses import dataclass

from game.combat import AttackResult, CombatService, Combatant
from game.effects import EffectService


@dataclass(frozen=True)
class AdvancedAttackResult:
    attack: AttackResult
    critical: bool
    effective_damage: int
    expired_effects: tuple[str, ...]


class AdvancedCombatService:
    """Integrates the existing combat and effect systems for advanced turns."""

    def __init__(self, combat: CombatService | None = None, effects: EffectService | None = None):
        self.combat = combat or CombatService()
        self.effects = effects or EffectService()

    def attack(self, attacker: Combatant, defender: Combatant, energy_cost: int = 10, critical: bool = False) -> AdvancedAttackResult:
        attack = self.combat.attack(attacker, defender, energy_cost)
        bonus = attack.damage if critical else 0
        if bonus:
            defender.health = max(0, defender.health - bonus)
        expired = self.effects.tick()
        return AdvancedAttackResult(attack, critical, attack.damage + bonus, expired)

    def apply_effect(self, effect) -> None:
        self.effects.apply(effect)
