import pytest

from game.achievements import Achievement, AchievementService
from game.rewards import Reward


def test_achievement_unlocks_at_target():
    service = AchievementService((Achievement("a", "Explorer", "explore", 3, Reward(xp=10)),))
    assert service.record_event("explore", 2) == ()
    assert service.record_event("explore") == ("a",)
    assert service.is_unlocked("a") is True


def test_already_unlocked_is_not_triggered_again():
    service = AchievementService((Achievement("a", "Explorer", "explore", 1, Reward(xp=10)),))
    assert service.record_event("explore") == ("a",)
    assert service.record_event("explore") == ()


def test_claim_returns_reward_and_clears_unlock():
    service = AchievementService((Achievement("a", "Explorer", "explore", 1, Reward(xp=10, credits=5)),))
    service.record_event("explore")
    assert service.claim("a") == Reward(xp=10, credits=5)
    assert service.claim("a") == Reward()


def test_invalid_event_amount_rejected():
    service = AchievementService((Achievement("a", "Explorer", "explore", 1, Reward()),))
    with pytest.raises(ValueError):
        service.record_event("explore", 0)
