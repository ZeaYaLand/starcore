from game.ai import OrganismAI
from game.combat import Combatant


def test_dead_organism_does_not_act():
    actor = Combatant("A", 0, 10, 5, 20)
    assert OrganismAI().decide(actor).action == "dead"


def test_no_energy_recovers():
    actor = Combatant("A", 50, 10, 5, 0)
    assert OrganismAI().decide(actor).action == "recover"


def test_no_target_explores():
    actor = Combatant("A", 50, 10, 5, 20)
    assert OrganismAI().decide(actor).action == "explore"


def test_target_is_attacked_when_healthy():
    actor = Combatant("A", 50, 10, 5, 20)
    target = Combatant("B", 40, 8, 4, 20)
    result = OrganismAI().decide(actor, target)
    assert result.action == "attack"
    assert result.target == "B"


def test_dead_target_is_not_attacked():
    actor = Combatant("A", 50, 10, 5, 20)
    target = Combatant("B", 0, 8, 4, 20)
    assert OrganismAI().decide(actor, target).action == "explore"
