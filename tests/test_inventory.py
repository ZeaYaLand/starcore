import pytest

from game.inventory import Inventory


def test_credits_cannot_go_negative():
    inventory = Inventory(credits=50)
    assert inventory.spend_credits(75) is False
    assert inventory.credits == 50


def test_credits_can_be_added_and_spent():
    inventory = Inventory()
    inventory.add_credits(100)
    assert inventory.spend_credits(40) is True
    assert inventory.credits == 60


def test_items_stack_and_remove():
    inventory = Inventory()
    inventory.add_item("ore", 3)
    inventory.add_item("ore", 2)
    assert inventory.items["ore"] == 5
    assert inventory.remove_item("ore", 5) is True
    assert "ore" not in inventory.items


def test_negative_currency_is_rejected():
    inventory = Inventory()
    with pytest.raises(ValueError):
        inventory.add_credits(-1)
    with pytest.raises(ValueError):
        inventory.add_crystals(-1)
