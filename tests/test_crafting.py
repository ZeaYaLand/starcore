import pytest

from game.crafting import CraftingService, Recipe
from game.inventory import Inventory, InventoryItem


def make_inventory() -> Inventory:
    inventory = Inventory(capacity=10)
    inventory.register_item(InventoryItem("ore", "Ore", max_stack=99))
    inventory.register_item(InventoryItem("blade", "Blade", category="weapon", max_stack=1))
    inventory.add_item("ore", 3)
    return inventory


def test_recipe_registration_and_can_craft():
    service = CraftingService()
    service.register_recipe(Recipe("blade_recipe", "blade", 1, {"ore": 3}))
    inventory = make_inventory()
    assert service.can_craft(inventory, "blade_recipe")


def test_craft_consumes_ingredients_and_produces_output():
    service = CraftingService()
    service.register_recipe(Recipe("blade_recipe", "blade", 1, {"ore": 3}))
    inventory = make_inventory()
    service.craft(inventory, "blade_recipe")
    assert inventory.items == {"blade": 1}


def test_craft_rejects_missing_ingredients_without_mutating_inventory():
    service = CraftingService()
    service.register_recipe(Recipe("blade_recipe", "blade", 1, {"ore": 4}))
    inventory = make_inventory()
    with pytest.raises(ValueError):
        service.craft(inventory, "blade_recipe")
    assert inventory.items == {"ore": 3}


def test_duplicate_recipe_is_rejected():
    service = CraftingService()
    recipe = Recipe("blade_recipe", "blade", 1, {"ore": 3})
    service.register_recipe(recipe)
    with pytest.raises(ValueError):
        service.register_recipe(recipe)
