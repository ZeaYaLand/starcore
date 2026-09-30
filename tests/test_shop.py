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


def test_cannot_buy_without_funds():
    inventory = Inventory(credits=10)
    assert ShopService().buy(inventory, "medkit") is False
    assert inventory.credits == 10
    assert inventory.items == {}


def test_sell_returns_credits():
    inventory = Inventory()
    inventory.add_item("ore")
    assert ShopService().sell(inventory, "ore", 10) is True
    assert inventory.credits == 10
    assert inventory.items == {}


def test_negative_sell_price_rejected():
    with pytest.raises(ValueError):
        ShopService().sell(Inventory(), "ore", -1)
