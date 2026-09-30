from dataclasses import dataclass, field

from game.inventory import Inventory


@dataclass(frozen=True)
class Recipe:
    recipe_id: str
    output_item_id: str
    output_quantity: int
    ingredients: dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.recipe_id or not self.output_item_id:
            raise ValueError("recipe and output ids are required")
        if self.output_quantity <= 0:
            raise ValueError("output quantity must be positive")
        if not self.ingredients or any(not item_id or amount <= 0 for item_id, amount in self.ingredients.items()):
            raise ValueError("ingredients must contain positive quantities")


class CraftingService:
    def __init__(self):
        self.recipes: dict[str, Recipe] = {}

    def register_recipe(self, recipe: Recipe) -> None:
        if recipe.recipe_id in self.recipes:
            raise ValueError("recipe already exists")
        self.recipes[recipe.recipe_id] = recipe

    def get_recipe(self, recipe_id: str) -> Recipe:
        if recipe_id not in self.recipes:
            raise KeyError(recipe_id)
        return self.recipes[recipe_id]

    def can_craft(self, inventory: Inventory, recipe_id: str) -> bool:
        recipe = self.get_recipe(recipe_id)
        return all(inventory.items.get(item_id, 0) >= amount for item_id, amount in recipe.ingredients.items())

    def craft(self, inventory: Inventory, recipe_id: str) -> Recipe:
        recipe = self.get_recipe(recipe_id)
        if not self.can_craft(inventory, recipe_id):
            raise ValueError("insufficient ingredients")
        for item_id, amount in recipe.ingredients.items():
            if not inventory.remove_item(item_id, amount):
                raise ValueError("failed to consume ingredient")
        try:
            inventory.add_item(recipe.output_item_id, recipe.output_quantity)
        except Exception:
            for item_id, amount in recipe.ingredients.items():
                inventory.add_item(item_id, amount)
            raise
        return recipe
