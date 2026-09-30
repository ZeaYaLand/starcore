from dataclasses import dataclass

from game.inventory import Inventory


@dataclass(frozen=True)
class ItemEffect:
    effect_type: str
    amount: int
    duration: int = 0


@dataclass(frozen=True)
class UsableItem:
    item_id: str
    name: str
    effect: ItemEffect


class ItemUseService:
    def use(self, inventory: Inventory, item: UsableItem) -> ItemEffect:
        if inventory.items.get(item.item_id, 0) <= 0:
            raise ValueError("item is not in inventory")
        if item.effect.amount <= 0:
            raise ValueError("effect amount must be positive")
        if item.effect.duration < 0:
            raise ValueError("effect duration cannot be negative")
        if not inventory.remove_item(item.item_id):
            raise ValueError("unable to consume item")
        return item.effect


DEFAULT_USABLE_ITEMS = (
    UsableItem("medkit", "Medkit", ItemEffect("heal", 25)),
    UsableItem("energy_cell", "Energy Cell", ItemEffect("restore_energy", 20)),
    UsableItem("rage_serum", "Rage Serum", ItemEffect("strength_boost", 5, duration=3)),
    UsableItem("speed_serum", "Speed Serum", ItemEffect("agility_boost", 5, duration=3)),
)
