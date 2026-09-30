from random import Random

from game.advanced_combat import AdvancedCombatService
from game.combat import CombatService, Combatant
from game.effects import Effect


def test_advanced_attack_uses_existing_combat_and_effects():
    service = AdvancedCombatService(CombatService(Random(1)))
    service.apply_effect(Effect("buff", "attack", 2, remaining_turns=1))
    attacker = Combatant("A", 50, 10, 2, 30)
    defender = Combatant("B", 40, 8, 3, 20)
    result = service.attack(attacker, defender)
    assert result.effective_damage == result.attack.damage
    assert result.expired_effects == ("buff",)
    assert attacker.energy == 20


def test_critical_attack_applies_bonus_damage():
    service = AdvancedCombatService(CombatService(Random(2)))
    attacker = Combatant("A", 50, 10, 0, 30)
    defender = Combatant("B", 40, 8, 0, 20)
    result = service.attack(attacker, defender, critical=True)
    assert result.critical is True
    assert result.effective_damage == result.attack.damage * 2
