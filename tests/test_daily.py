from datetime import date, timedelta

import pytest

from game.daily import DailyActivity, DailyService
from game.rewards import Reward


def test_daily_reward_claims_once_per_day():
    service = DailyService((DailyActivity("d1", "Explore", 2, Reward(xp=10, credits=20)),))
    today = date(2026, 10, 1)
    service.advance("d1", 2)

    assert service.claim("d1", today) == Reward(xp=10, credits=20)
    assert service.claim("d1", today) == Reward()


def test_daily_activity_can_be_completed_again_next_day():
    service = DailyService((DailyActivity("d1", "Explore", 1, Reward(xp=10)),))
    day_one = date(2026, 10, 1)
    day_two = day_one + timedelta(days=1)

    service.advance("d1")
    assert service.claim("d1", day_one) == Reward(xp=10)
    service.advance("d1")
    assert service.claim("d1", day_two) == Reward(xp=10)


def test_incomplete_daily_has_no_reward():
    service = DailyService((DailyActivity("d1", "Explore", 2, Reward(xp=10)),))
    assert service.claim("d1", date(2026, 10, 1)) == Reward()


def test_daily_progress_requires_positive_amount():
    service = DailyService((DailyActivity("d1", "Explore", 2, Reward()),))
    with pytest.raises(ValueError):
        service.advance("d1", 0)
