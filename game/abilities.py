from dataclasses import dataclass

from game.genome import Organism


@dataclass(frozen=True)
class Ability:
    ability_id: str
    name: str
    energy_cost: int
    power: int
    stat: str


@dataclass(frozen=True)
class AbilityResult:
    success: bool
    damage: int
    energy_spent: int


ABILITIES = {
    "brutal_strike": Ability("brutal_strike", "Brutal Strike", 10, 12, "strength"),
    "vital_burst": Ability("vital_burst", "Vital Burst", 15, 10, "vitality"),
    "agile_strike": Ability("agile_strike", "Agile Strike", 8, 9, "agility"),
}


class AbilityService:
    def use(self, ability_id: str, organism: Organism, energy: int) -> AbilityResult:
        ability = ABILITIES.get(ability_id)
        if ability is None:
            return AbilityResult(False, 0, 0)
        if energy < ability.energy_cost:
            return AbilityResult(False, 0, 0)
        stat_value = getattr(organism.genome, ability.stat)
        damage = ability.power + stat_value
        return AbilityResult(True, damage, ability.energy_cost)
