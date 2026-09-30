import pytest

from game.combat import CombatService, Combatant


def test_attack_deals_damage_and_spends_energy():
    attacker = Combatant("A", 100, 20, defense=2, energy=30)
    defender = Combatant("B", 40, 10, defense=5, energy=20)
    result = CombatService().attack(attacker, defender, energy_cost=10)
    assert result.damage >= 1
    assert attacker.energy == 20
    assert defender.health < 40


def test_attack_can_end_fight():
    attacker = Combatant("A", 100, 20, defense=2, energy=20)
    defender = Combatant("B", 5, 1, defense=0, energy=10)
    result = CombatService().attack(attacker, defender, energy_cost=10)
    assert result.winner == "A"
    assert defender.health == 0


def test_attack_requires_energy_and_living_combatants():
    attacker = Combatant("A", 100, 20, energy=5)
    defender = Combatant("B", 40, 10)
    with pytest.raises(ValueError):
        CombatService().attack(attacker, defender, energy_cost=10)

    attacker.energy = 20
    defender.health = 0
    with pytest.raises(ValueError):
        CombatService().attack(attacker, defender)


def test_fight_returns_winner():
    player = Combatant("Player", 100, 30, defense=10)
    enemy = Combatant("Enemy", 10, 1, defense=0)
    result = CombatService().fight(player, enemy)
    assert result.winner == "Player"
    assert result.rounds >= 1
