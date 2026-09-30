from random import Random

import pytest

from game.random_enemies import RandomEnemyFactory


def test_random_factory_returns_known_enemy():
    combatant, organism, ability = RandomEnemyFactory(Random(1)).create()
    assert combatant.name in {"Brute", "Runner", "Tank"}
    assert ability.ability_id
    assert organism.generation == 1


def test_random_factory_is_reproducible_with_seed():
    first = RandomEnemyFactory(Random(7)).create()[0].name
    second = RandomEnemyFactory(Random(7)).create()[0].name
    assert first == second


def test_difficulty_must_be_positive():
    with pytest.raises(ValueError):
        RandomEnemyFactory(Random(1)).create(0)
