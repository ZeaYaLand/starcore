import pytest

from game.quests import Quest, QuestService
from game.rewards import Reward


def test_quest_progress_and_claim_once():
    service = QuestService((Quest("q1", "Explore", 3, Reward(xp=10, credits=20)),))
    assert service.advance("q1", 2).completed is False
    status = service.advance("q1", 2)
    assert status.progress == 3
    assert status.completed is True
    assert service.claim("q1") == Reward(xp=10, credits=20)
    assert service.claim("q1") == Reward()


def test_incomplete_quest_has_no_reward():
    service = QuestService((Quest("q1", "Explore", 3, Reward(xp=10)),))
    service.advance("q1")
    assert service.claim("q1") == Reward()


def test_progress_amount_must_be_positive():
    service = QuestService((Quest("q1", "Explore", 3, Reward()),))
    with pytest.raises(ValueError):
        service.advance("q1", 0)
