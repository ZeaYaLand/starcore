import pytest

from game.inventory import Inventory, InventoryItem


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


def test_stage_46_item_definition_supports_rarity_stats_and_durability():
    inventory = Inventory()
    blade = InventoryItem(
        "blade", "Star Blade", category="weapon", max_stack=1,
        rarity="epic", power=25, durability=40, max_durability=50,
        stats={"attack": 10, "agility": 2},
    )
    inventory.register_item(blade)
    inventory.add_item("blade")
    assert inventory.get_item("blade").rarity == "epic"
    assert inventory.get_item("blade").stats["attack"] == 10
    assert inventory.repair("blade", 20) == 10
    assert inventory.get_item("blade").durability == 50


def test_stage_46_rejects_invalid_item_definition():
    with pytest.raises(ValueError):
        InventoryItem("bad", "Bad", max_stack=0)
    with pytest.raises(ValueError):
        InventoryItem("bad", "Bad", durability=10, max_durability=5)
