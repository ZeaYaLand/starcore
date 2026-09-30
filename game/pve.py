from dataclasses import dataclass

from game.enemies import ENEMY_TEMPLATES, EnemyFactory


@dataclass(frozen=True)
class PvEEncounter:
    encounter_id: str
    name: str
    enemy_id: str
    reward: int
    kind: str


PVE_ENCOUNTERS = (
    PvEEncounter("hunt_brute", "Brute Hunt", "brute", 20, "hunt"),
    PvEEncounter("hunt_runner", "Runner Hunt", "runner", 25, "hunt"),
    PvEEncounter("trial_tank", "Tank Trial", "tank", 35, "trial"),
    PvEEncounter("overseer_event", "Overseer Event", "overseer", 100, "event"),
)


class PvEService:
    def __init__(self, enemy_factory: EnemyFactory | None = None):
        self.enemy_factory = enemy_factory or EnemyFactory()

    def encounters(self, kind: str | None = None) -> tuple[PvEEncounter, ...]:
        if kind is None:
            return PVE_ENCOUNTERS
        return tuple(item for item in PVE_ENCOUNTERS if item.kind == kind)

    def start(self, encounter_id: str):
        encounter = next((item for item in PVE_ENCOUNTERS if item.encounter_id == encounter_id), None)
        if encounter is None:
            raise KeyError(encounter_id)
        created = self.enemy_factory.create_boss(encounter.enemy_id) if encounter.enemy_id == "overseer" else self.enemy_factory.create(encounter.enemy_id)
        return encounter, created
