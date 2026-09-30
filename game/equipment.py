from dataclasses import dataclass

from game.combat import Combatant


@dataclass(frozen=True)
class Equipment:
    item_id: str
    name: str
    slot: str
    attack_bonus: int = 0
    defense_bonus: int = 0
    health_bonus: int = 0


EQUIPMENT = {
    "plasma_blade": Equipment("plasma_blade", "Plasma Blade", "weapon", attack_bonus=5),
    "nano_armor": Equipment("nano_armor", "Nano Armor", "armor", defense_bonus=4, health_bonus=15),
    "gene_module": Equipment("gene_module", "Gene Module", "module", attack_bonus=2, defense_bonus=2, health_bonus=5),
}


class EquipmentLoadout:
    def __init__(self):
        self._slots: dict[str, Equipment] = {}

    def equip(self, equipment: Equipment) -> Equipment | None:
        previous = self._slots.get(equipment.slot)
        self._slots[equipment.slot] = equipment
        return previous

    def unequip(self, slot: str) -> Equipment | None:
        return self._slots.pop(slot, None)

    def get(self, slot: str) -> Equipment | None:
        return self._slots.get(slot)

    def apply(self, combatant: Combatant) -> Combatant:
        for item in self._slots.values():
            combatant.attack += item.attack_bonus
            combatant.defense += item.defense_bonus
            combatant.health += item.health_bonus
        return combatant
