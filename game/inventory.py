from dataclasses import dataclass, field


@dataclass(frozen=True)
class InventoryItem:
    item_id: str
    name: str
    category: str = "misc"
    max_stack: int = 99


@dataclass
class Inventory:
    credits: int = 0
    crystals: int = 0
    items: dict[str, int] = field(default_factory=dict)
    capacity: int = 20
    equipped: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.capacity <= 0:
            raise ValueError("capacity must be positive")

    def add_credits(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("amount must be non-negative")
        self.credits += amount

    def spend_credits(self, amount: int) -> bool:
        if amount < 0:
            raise ValueError("amount must be non-negative")
        if self.credits < amount:
            return False
        self.credits -= amount
        return True

    def add_crystals(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("amount must be non-negative")
        self.crystals += amount

    def add_item(self, item_id: str, quantity: int = 1, max_stack: int = 99) -> None:
        if not item_id or quantity <= 0 or max_stack <= 0 or quantity > max_stack:
            raise ValueError("invalid item or quantity")
        if item_id not in self.items and len(self.items) >= self.capacity:
            raise ValueError("inventory is full")
        current = self.items.get(item_id, 0)
        if current + quantity > max_stack:
            raise ValueError("stack limit exceeded")
        self.items[item_id] = current + quantity

    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        if quantity <= 0 or self.items.get(item_id, 0) < quantity:
            return False
        self.items[item_id] -= quantity
        if self.items[item_id] == 0:
            del self.items[item_id]
            for slot, equipped_id in list(self.equipped.items()):
                if equipped_id == item_id:
                    del self.equipped[slot]
        return True

    def equip(self, item_id: str, slot: str) -> None:
        if not item_id or not slot or self.items.get(item_id, 0) <= 0:
            raise ValueError("item is not in inventory")
        self.equipped[slot] = item_id

    def unequip(self, slot: str) -> str | None:
        return self.equipped.pop(slot, None)
