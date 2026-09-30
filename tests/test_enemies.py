import pytest

from game.enemies import ENEMY_TEMPLATES, EnemyFactory


def test_enemy_templates_have_distinct_roles():
    assert len(ENEMY_TEMPLATES) == 4
    assert {enemy.ability_id for enemy in ENEMY_TEMPLATES[:3]} == {
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


def test_boss_has_phases_and_reward():
    template = next(enemy for enemy in ENEMY_TEMPLATES if enemy.enemy_id == "overseer")
    assert template.boss is True
    assert [phase.phase_id for phase in template.phases] == ["phase_1", "phase_2", "phase_3"]
    assert template.reward == 100


def test_boss_changes_phase_by_health_threshold():
    _, _, _, boss = EnemyFactory().create_boss("overseer")
    assert boss.phase.phase_id == "phase_1"
    boss.update(0.59)
    assert boss.phase.phase_id == "phase_2"
    boss.update(0.29)
    assert boss.phase.phase_id == "phase_3"
    assert boss.phase_history == ["phase_1", "phase_2", "phase_3"]


def test_boss_reward_is_claimed_only_once():
    _, _, _, boss = EnemyFactory().create_boss("overseer")
    assert boss.defeat() == 100
    assert boss.defeat() == 0
    assert boss.defeated is True
