from dataclasses import dataclass, field

from game.exploration import ExplorationResult, ExplorationService, Zone


@dataclass
class DiscoveryChain:
    discovered: list[str] = field(default_factory=list)

    def add(self, discovery: str) -> None:
        if discovery not in self.discovered:
            self.discovered.append(discovery)

    def has(self, discovery: str) -> bool:
        return discovery in self.discovered


class AdvancedExplorationService:
    """Adds persistent discoveries and event chains to the existing exploration system."""

    def __init__(self, exploration: ExplorationService | None = None):
        self.exploration = exploration or ExplorationService()
        self.discovery_chain = DiscoveryChain()

    def explore(self, zone: Zone | None = None) -> ExplorationResult:
        result = self.exploration.explore(zone)
        self.discovery_chain.add(result.discovery)
        return result

    def discoveries(self) -> tuple[str, ...]:
        return tuple(self.discovery_chain.discovered)

    def discovery_count(self) -> int:
        return len(self.discovery_chain.discovered)
