import pytest

from game.inventory import Inventory
from game.shop import ShopService


def test_buy_with_credits():
    inventory = Inventory(credits=100)
    assert ShopService().buy(inventory, "ore") is True
    assert inventory.credits == 75
    assert inventory.items["ore"] == 1


def test_buy_with_crystals():
    inventory = Inventory(crystals=3)
    assert ShopService().buy(inventory, "quantum_core") is True
    assert inventory.crystals == 1
    assert inventory.items["quantum_core"] == 1


def test_buy_multiple_items():
    inventory = Inventory(credits=100)
    assert ShopService().buy(inventory, "ore", 2) is True
    assert inventory.credits == 50
    assert inventory.items["ore"] == 2


def test_cannot_buy_without_funds():
    inventory = Inventory(credits=10)
    assert ShopService().buy(inventory, "medkit") is False
    assert inventory.credits == 10
    assert inventory.items == {}


def test_sell_uses_shop_price_and_quantity():
    inventory = Inventory()
    inventory.add_item("ore", 3)
    assert ShopService().sell(inventory, "ore", 2) is True
    assert inventory.credits == 20
    assert inventory.items["ore"] == 1


def test_cannot_sell_more_than_owned():
    inventory = Inventory()
    inventory.add_item("ore")
    assert ShopService().sell(inventory, "ore", 2) is False
    assert inventory.credits == 0
    assert inventory.items["ore"] == 1


def test_invalid_quantity_rejected():
    inventory = Inventory(credits=100)
    assert ShopService().buy(inventory, "ore", 0) is False
    assert ShopService().sell(inventory, "ore", -1) is False
