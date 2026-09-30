from game.ai import OrganismAI
from game.combat import Combatant


def test_dead_organism_does_not_act():
    actor = Combatant("A", 10, 5, 0, 20)
    assert OrganismAI().decide(actor).action == "dead"


def test_no_energy_recovers():
    actor = Combatant("A", 10, 5, 50, 0)
    assert OrganismAI().decide(actor).action == "recover"


def test_no_target_explores():
    actor = Combatant("A", 10, 5, 50, 20)
    assert OrganismAI().decide(actor).action == "explore"


def test_target_is_attacked_when_healthy():
    actor = Combatant("A", 10, 5, 50, 20)
    target = Combatant("B", 8, 4, 40, 20)
    result = OrganismAI().decide(actor, target)
    assert result.action == "attack"
    assert result.target == "B"


def test_dead_target_is_not_attacked():
    actor = Combatant("A", 10, 5, 50, 20)
    target = Combatant("B", 8, 4, 0, 20)
    assert OrganismAI().decide(actor, target).action == "explore"
