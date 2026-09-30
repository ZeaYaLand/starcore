from dataclasses import dataclass, field

from game.abilities import Ability, ABILITIES
from game.genome import Genome, Organism
from game.organism_combat import combatant_from_organism


@dataclass(frozen=True)
class BossPhase:
    phase_id: str
    health_threshold: float
    ability_id: str


@dataclass(frozen=True)
class EnemyTemplate:
    enemy_id: str
    name: str
    genome: Genome
    ability_id: str
    boss: bool = False
    phases: tuple[BossPhase, ...] = ()
    reward: int = 0


ENEMY_TEMPLATES = (
    EnemyTemplate("brute", "Brute", Genome(strength=6, vitality=4, agility=1), "brutal_strike"),
    EnemyTemplate("runner", "Runner", Genome(strength=2, vitality=2, agility=7), "agile_strike"),
    EnemyTemplate("tank", "Tank", Genome(strength=2, vitality=7, agility=1), "vital_burst"),
    EnemyTemplate(
        "overseer", "Overseer", Genome(strength=8, vitality=8, agility=4), "brutal_strike",
        boss=True,
        phases=(
            BossPhase("phase_1", 1.0, "brutal_strike"),
            BossPhase("phase_2", 0.6, "vital_burst"),
            BossPhase("phase_3", 0.3, "agile_strike"),
        ),
        reward=100,
    ),
)


@dataclass
class BossState:
    template: EnemyTemplate
    current_phase: int = 0
    reward_claimed: bool = False
    defeated: bool = False
    phase_history: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.template.boss:
            raise ValueError("template is not a boss")
        self._sync_phase(1.0)

    @property
    def phase(self) -> BossPhase:
        return self.template.phases[self.current_phase]

    def update(self, health_ratio: float) -> BossPhase:
        self._sync_phase(health_ratio)
        return self.phase

    def defeat(self) -> int:
        self.defeated = True
        if self.reward_claimed:
            return 0
        self.reward_claimed = True
        return self.template.reward

    def _sync_phase(self, health_ratio: float) -> None:
        ratio = max(0.0, min(1.0, health_ratio))
        selected = 0
        for index, phase in enumerate(self.template.phases):
            if ratio <= phase.health_threshold:
                selected = index
        if selected != self.current_phase:
            self.current_phase = selected
            self.phase_history.append(self.phase.phase_id)
        elif not self.phase_history:
            self.phase_history.append(self.phase.phase_id)


class EnemyFactory:
    def create(self, enemy_id: str):
        template = next((item for item in ENEMY_TEMPLATES if item.enemy_id == enemy_id), None)
        if template is None:
            raise KeyError(enemy_id)
        organism = Organism(template.genome)
        combatant = combatant_from_organism(template.name, organism)
        ability: Ability = ABILITIES[template.ability_id]
        combatant.energy = ability.energy_cost
        return combatant, organism, ability

    def create_boss(self, enemy_id: str):
        template = next((item for item in ENEMY_TEMPLATES if item.enemy_id == enemy_id), None)
        if template is None:
            raise KeyError(enemy_id)
        if not template.boss:
            raise ValueError("enemy is not a boss")
        combatant, organism, ability = self.create(enemy_id)
        return combatant, organism, ability, BossState(template)
