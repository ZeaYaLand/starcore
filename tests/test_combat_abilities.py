from game.combat import Combatant, CombatService


def test_ability_deals_damage_and_spends_energy():
    attacker = Combatant("Player", 100, 10, energy=20)
    defender = Combatant("Enemy", 50, 5)
    dealt = CombatService().use_ability(attacker, defender, damage=18, energy_cost=10)
    assert dealt == 18
    assert defender.health == 32
    assert attacker.energy == 10


def test_ability_fails_without_energy():
    attacker = Combatant("Player", 100, 10, energy=5)
    defender = Combatant("Enemy", 50, 5)
    dealt = CombatService().use_ability(attacker, defender, damage=18, energy_cost=10)
    assert dealt == 0
    assert defender.health == 50
    assert attacker.energy == 5


def test_ability_cannot_hit_dead_target():
    attacker = Combatant("Player", 100, 10, energy=20)
    defender = Combatant("Enemy", 0, 5)
    assert CombatService().use_ability(attacker, defender, damage=18, energy_cost=10) == 0
