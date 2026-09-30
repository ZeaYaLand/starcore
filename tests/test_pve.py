import pytest

from game.pve import PVE_ENCOUNTERS, PvEService


def test_pve_contains_hunts_trials_and_events():
    service = PvEService()
    assert {item.kind for item in PVE_ENCOUNTERS} == {"hunt", "trial", "event"}
    assert len(service.encounters("hunt")) == 2
    assert len(service.encounters("trial")) == 1
    assert len(service.encounters("event")) == 1


def test_pve_starts_normal_encounter():
    encounter, created = PvEService().start("hunt_brute")
    combatant, organism, ability = created
    assert encounter.kind == "hunt"
    assert combatant.name == "Brute"
    assert organism.genome.strength == 6
    assert ability.ability_id == "brutal_strike"


def test_pve_starts_boss_event_through_existing_boss_system():
    encounter, created = PvEService().start("overseer_event")
    combatant, organism, ability, boss = created
    assert encounter.kind == "event"
    assert combatant.name == "Overseer"
    assert boss.phase.phase_id == "phase_1"


def test_unknown_pve_encounter_is_rejected():
    with pytest.raises(KeyError):
        PvEService().start("unknown")
