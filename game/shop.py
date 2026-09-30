from dataclasses import dataclass

from game.inventory import Inventory


@dataclass(frozen=True)
class ShopItem:
    item_id: str
    price: int
    currency: str = "credits"
    quantity: int = 1
    sell_price: int | None = None


SHOP = {
    "ore": ShopItem("ore", 25, sell_price=10),
    "medkit": ShopItem("medkit", 75, sell_price=30),
    "quantum_core": ShopItem("quantum_core", 2, "crystals", sell_price=1),
}


class ShopService:
    def buy(self, inventory: Inventory, item_id: str, quantity: int = 1) -> bool:
        item = SHOP.get(item_id)
        if item is None or quantity <= 0:
            return False
        if item.price < 0 or item.quantity <= 0:
            return False
        total = item.price * quantity
        if item.currency == "credits":
            if not inventory.spend_credits(total):
                return False
        elif item.currency == "crystals":
            if inventory.crystals < total:
                return False
            inventory.crystals -= total
        else:
            return False
        inventory.add_item(item.item_id, item.quantity * quantity)
        return True

    def sell(self, inventory: Inventory, item_id: str, quantity: int = 1) -> bool:
        item = SHOP.get(item_id)
        if item is None or quantity <= 0:
            return False
        if item.sell_price is None or item.sell_price < 0:
            return False
        if not inventory.remove_item(item_id, quantity):
            return False
        inventory.add_credits(item.sell_price * quantity)
        return True
