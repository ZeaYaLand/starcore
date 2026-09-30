from game.combat import Combatant
from game.equipment import EQUIPMENT, Equipment, EquipmentLoadout


def test_equip_replaces_same_slot():
    loadout = EquipmentLoadout()
    first_weapon = EQUIPMENT["plasma_blade"]
    second_weapon = Equipment("plasma_blade_mk2", "Plasma Blade MK2", "weapon", attack_bonus=8)

    old = loadout.equip(first_weapon)
    assert old is None
    replacement = loadout.equip(second_weapon)

    assert replacement is first_weapon
    assert loadout.get("weapon") is second_weapon


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
