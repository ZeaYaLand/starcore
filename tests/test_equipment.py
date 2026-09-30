from game.combat import Combatant
from game.equipment import EQUIPMENT, EquipmentLoadout


def test_equip_replaces_same_slot():
    loadout = EquipmentLoadout()
    old = loadout.equip(EQUIPMENT["plasma_blade"])
    assert old is None
    previous = loadout.equip(EQUIPMENT["gene_module"])
    assert previous is None
    replacement = loadout.equip(EQUIPMENT["plasma_blade"])
    assert replacement is EQUIPMENT["gene_module"]


def test_equipment_changes_combat_stats():
    combatant = Combatant("Mutant", 100, 10, 3)
    loadout = EquipmentLoadout()
    loadout.equip(EQUIPMENT["plasma_blade"])
    loadout.equip(EQUIPMENT["nano_armor"])
    loadout.apply(combatant)

    assert combatant.attack == 15
    assert combatant.defense == 7
    assert combatant.health == 115


def test_unequip_removes_slot():
    loadout = EquipmentLoadout()
    loadout.equip(EQUIPMENT["nano_armor"])
    removed = loadout.unequip("armor")
    assert removed is EQUIPMENT["nano_armor"]
    assert loadout.get("armor") is None
