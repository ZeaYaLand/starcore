from dataclasses import dataclass

from game.inventory import Inventory


@dataclass(frozen=True)
class ShopItem:
    item_id: str
    price: int
    currency: str = "credits"
    quantity: int = 1


SHOP = {
    "ore": ShopItem("ore", 25),
    "medkit": ShopItem("medkit", 75),
    "quantum_core": ShopItem("quantum_core", 2, "crystals"),
}


class ShopService:
    def buy(self, inventory: Inventory, item_id: str) -> bool:
        item = SHOP.get(item_id)
        if item is None:
            return False
        if item.currency == "credits":
            if not inventory.spend_credits(item.price):
                return False
        elif item.currency == "crystals":
            if inventory.crystals < item.price:
                return False
            inventory.crystals -= item.price
        else:
            return False
        inventory.add_item(item.item_id, item.quantity)
        return True

    def sell(self, inventory: Inventory, item_id: str, price: int) -> bool:
        if price < 0:
            raise ValueError("price must be non-negative")
        if not inventory.remove_item(item_id):
            return False
        inventory.add_credits(price)
        return True
