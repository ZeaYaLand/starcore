from dataclasses import dataclass
from random import Random


@dataclass
class Combatant:
    name: str
    health: int
    attack: int
    defense: int = 0
    energy: int = 0

    @property
    def alive(self) -> bool:
        return self.health > 0


@dataclass(frozen=True)
class CombatResult:
    winner: str
    rounds: int
    damage_dealt: int
    damage_taken: int
    energy_spent: int = 0


@dataclass(frozen=True)
class AttackResult:
    damage: int
    attacker_energy: int
    defender_health: int
    winner: str | None


class CombatService:
    def __init__(self, rng: Random | None = None):
        self.rng = rng or Random()

    def _damage(self, attacker: Combatant, defender: Combatant) -> int:
        base = max(1, attacker.attack - defender.defense)
        return self.rng.randint(max(1, base - 1), base + 1)

    def attack(self, attacker: Combatant, defender: Combatant, energy_cost: int = 10) -> AttackResult:
        if attacker.attack < 0 or defender.defense < 0:
            raise ValueError("combat stats cannot be negative")
        if energy_cost <= 0:
            raise ValueError("energy cost must be positive")
        if attacker.energy < energy_cost:
            raise ValueError("insufficient energy")
        if not attacker.alive or not defender.alive:
            raise ValueError("combatant is not alive")
        damage = self._damage(attacker, defender)
        defender.health = max(0, defender.health - damage)
        attacker.energy -= energy_cost
        return AttackResult(damage, attacker.energy, defender.health, attacker.name if not defender.alive else None)

    def use_ability(self, attacker: Combatant, defender: Combatant, damage: int, energy_cost: int) -> int:
        if damage <= 0 or energy_cost < 0 or attacker.energy < energy_cost or not defender.alive:
            return 0
        attacker.energy -= energy_cost
        dealt = min(defender.health, damage)
        defender.health -= dealt
        return dealt

    def fight(self, player: Combatant, enemy: Combatant) -> CombatResult:
        damage_dealt = 0
        damage_taken = 0
        rounds = 0
        energy_spent = 0
        while player.alive and enemy.alive:
            rounds += 1
            damage = self._damage(player, enemy)
            enemy.health = max(0, enemy.health - damage)
            damage_dealt += damage
            if not enemy.alive:
                break
            damage = self._damage(enemy, player)
            player.health = max(0, player.health - damage)
            damage_taken += damage
        winner = player.name if player.alive else enemy.name
        return CombatResult(winner, rounds, damage_dealt, damage_taken, energy_spent)
