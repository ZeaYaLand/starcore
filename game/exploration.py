from dataclasses import dataclass
from random import Random


@dataclass(frozen=True)
class Zone:
    zone_id: str
    name: str
    difficulty: int
    events: tuple[str, ...]
    discoveries: tuple[str, ...]


ZONES = (
    Zone("crystal_caverns", "Crystal Caverns", 1, ("crystal_echo", "minor_ambush"), ("crystal_shard", "ancient_gene")),
    Zone("toxic_wastes", "Toxic Wastes", 2, ("toxic_storm", "mutant_pack"), ("toxin_sample", "mutagen")),
    Zone("void_rift", "Void Rift", 3, ("rift_anomaly", "elite_predator"), ("void_fragment", "rare_gene")),
)


@dataclass(frozen=True)
class ExplorationResult:
    zone_id: str
    event: str
    discovery: str
    danger: int


class ExplorationService:
    def __init__(self, rng: Random | None = None):
        self.rng = rng or Random()

    def explore(self, zone: Zone | None = None) -> ExplorationResult:
        selected = zone or self.rng.choice(ZONES)
        return ExplorationResult(
            zone_id=selected.zone_id,
            event=self.rng.choice(selected.events),
            discovery=self.rng.choice(selected.discoveries),
            danger=selected.difficulty,
        )
