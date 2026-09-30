from game.genome import Genome, Organism
from game.organism_combat import combatant_from_organism, stats_from_organism


def test_genome_maps_to_combat_stats():
    organism = Organism(Genome(strength=4, vitality=3, agility=7))
    stats = stats_from_organism(organism)

    assert stats.health == 80
    assert stats.attack == 13
    assert stats.defense == 3
    assert stats.initiative == 7


def test_stronger_genome_has_more_attack_and_health():
    weak = Organism(Genome(strength=1, vitality=1, agility=1))
    strong = Organism(Genome(strength=5, vitality=5, agility=1))

    weak_stats = stats_from_organism(weak)
    strong_stats = stats_from_organism(strong)
    assert strong_stats.attack > weak_stats.attack
    assert strong_stats.health > weak_stats.health


def test_organism_can_become_combatant():
    organism = Organism(Genome(strength=3, vitality=2, agility=4))
    combatant = combatant_from_organism("Mutant", organism)

    assert combatant.name == "Mutant"
    assert combatant.health == 70
    assert combatant.attack == 11
    assert combatant.defense == 2
