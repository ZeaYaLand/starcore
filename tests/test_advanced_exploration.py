from random import Random

from game.advanced_exploration import AdvancedExplorationService
from game.exploration import ExplorationService, ZONES


def test_discoveries_are_persisted_without_duplicates():
    service = AdvancedExplorationService(ExplorationService(Random(1)))
    service.explore(ZONES[0])
    first_count = service.discovery_count()
    service.discovery_chain.add("crystal_shard")
    assert service.discovery_count() == first_count
    assert service.discoveries() == tuple(service.discovery_chain.discovered)


def test_exploration_records_discovery_from_existing_service():
    service = AdvancedExplorationService(ExplorationService(Random(2)))
    result = service.explore(ZONES[1])
    assert result.zone_id == "toxic_wastes"
    assert service.discovery_chain.has(result.discovery)
