from random import Random

from game.combat import Combatant, CombatService


def test_player_can_win_combat():
    player = Combatant("Player", 100, 25, 5)
    enemy = Combatant("Scout", 30, 5, 0)
    result = CombatService(Random(1)).fight(player, enemy)

    assert result.winner == "Player"
    assert enemy.health == 0
    assert result.rounds > 0
    assert result.damage_dealt > 0


def test_combatant_defense_reduces_damage():
    service = CombatService(Random(1))
    attacker = Combatant("A", 100, 10)
    defender = Combatant("B", 100, 1, 9)
    damage = service._damage(attacker, defender)

    assert damage >= 1
    assert damage <= 2


def test_enemy_can_win():
    player = Combatant("Player", 10, 1, 0)
    enemy = Combatant("Boss", 100, 20, 0)
    result = CombatService(Random(1)).fight(player, enemy)

    assert result.winner == "Boss"
    assert player.health == 0
