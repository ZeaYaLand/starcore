from dataclasses import dataclass

from game.genome import Organism


@dataclass(frozen=True)
class Ability:
    ability_id: str
    name: str
    energy_cost: int
    power: int
    stat: str
    cooldown: int = 0
    effect_id: str | None = None


@dataclass(frozen=True)
class AbilityResult:
    success: bool
    damage: int
    energy_spent: int
    cooldown: int = 0
    effect_id: str | None = None


ABILITIES = {
    "brutal_strike": Ability("brutal_strike", "Brutal Strike", 10, 12, "strength", cooldown=1),
    "vital_burst": Ability("vital_burst", "Vital Burst", 15, 10, "vitality", cooldown=2, effect_id="vital_burst"),
    "agile_strike": Ability("agile_strike", "Agile Strike", 8, 9, "agility", cooldown=1),
}


class AbilityService:
    def __init__(self):
        self._cooldowns: dict[tuple[int, str], int] = {}

    def use(self, ability_id: str, organism: Organism, energy: int) -> AbilityResult:
        ability = ABILITIES.get(ability_id)
        if ability is None or energy < ability.energy_cost:
            return AbilityResult(False, 0, 0)
        key = (id(organism), ability_id)
        if self._cooldowns.get(key, 0) > 0:
            return AbilityResult(False, 0, 0)
        stat_value = getattr(organism.genome, ability.stat)
        damage = ability.power + stat_value
        if ability.cooldown:
            self._cooldowns[key] = ability.cooldown
        return AbilityResult(True, damage, ability.energy_cost, ability.cooldown, ability.effect_id)

    def tick(self) -> None:
        self._cooldowns = {
            key: turns - 1 for key, turns in self._cooldowns.items() if turns > 1
        }

    def cooldown_remaining(self, organism: Organism, ability_id: str) -> int:
        return self._cooldowns.get((id(organism), ability_id), 0)
