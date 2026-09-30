import pytest

from game.inventory import Inventory
from game.items import ItemEffect, ItemUseService, UsableItem


def test_using_item_consumes_one_and_returns_effect():
    inventory = Inventory()
    inventory.add_item("medkit", 2)
    item = UsableItem("medkit", "Medkit", ItemEffect("heal", 25))
    assert ItemUseService().use(inventory, item) == ItemEffect("heal", 25)
    assert inventory.items["medkit"] == 1


def test_using_missing_item_fails():
    with pytest.raises(ValueError):
        ItemUseService().use(Inventory(), UsableItem("medkit", "Medkit", ItemEffect("heal", 25)))


def test_temporary_effect_has_duration():
    inventory = Inventory()
    inventory.add_item("serum")
    effect = ItemUseService().use(
        inventory, UsableItem("serum", "Serum", ItemEffect("strength_boost", 5, duration=3))
    )
    assert effect.duration == 3


def test_invalid_effect_is_rejected():
    inventory = Inventory()
    inventory.add_item("bad")
    with pytest.raises(ValueError):
        ItemUseService().use(inventory, UsableItem("bad", "Bad", ItemEffect("heal", 0)))
