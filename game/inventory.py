from dataclasses import dataclass, field


@dataclass
class Inventory:
    credits: int = 0
    crystals: int = 0
    items: dict[str, int] = field(default_factory=dict)

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

    def add_item(self, item_id: str, quantity: int = 1) -> None:
        if not item_id or quantity <= 0:
            raise ValueError("invalid item or quantity")
        self.items[item_id] = self.items.get(item_id, 0) + quantity

    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        if quantity <= 0 or self.items.get(item_id, 0) < quantity:
            return False
        self.items[item_id] -= quantity
        if self.items[item_id] == 0:
            del self.items[item_id]
        return True
