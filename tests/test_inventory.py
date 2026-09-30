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


def test_inventory_capacity_and_stack_limit():
    inventory = Inventory(capacity=1)
    inventory.add_item("ore", 3, max_stack=5)
    inventory.add_item("ore", 2, max_stack=5)
    with pytest.raises(ValueError):
        inventory.add_item("wood")
    with pytest.raises(ValueError):
        inventory.add_item("ore", 1, max_stack=5)


def test_equipment_can_be_equipped_and_unequipped():
    inventory = Inventory()
    inventory.add_item("blade")
    inventory.equip("blade", "weapon")
    assert inventory.equipped["weapon"] == "blade"
    assert inventory.unequip("weapon") == "blade"
    assert inventory.unequip("weapon") is None


def test_removing_last_equipped_item_clears_equipment():
    inventory = Inventory()
    inventory.add_item("blade")
    inventory.equip("blade", "weapon")
    assert inventory.remove_item("blade") is True
    assert inventory.equipped == {}
