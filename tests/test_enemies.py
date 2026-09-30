import pytest

from game.enemies import ENEMY_TEMPLATES, EnemyFactory


def test_enemy_templates_have_distinct_roles():
    assert len(ENEMY_TEMPLATES) == 3
    assert {enemy.ability_id for enemy in ENEMY_TEMPLATES} == {
        "brutal_strike", "agile_strike", "vital_burst"
    }


def test_enemy_factory_builds_combatant_and_ability():
    combatant, organism, ability = EnemyFactory().create("brute")
    assert combatant.name == "Brute"
    assert organism.genome.strength == 6
    assert ability.ability_id == "brutal_strike"
    assert combatant.energy == ability.energy_cost


def test_unknown_enemy_is_rejected():
    with pytest.raises(KeyError):
        EnemyFactory().create("unknown")
