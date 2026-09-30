import pytest

from game.economy import EconomyService, Wallet
from game.rewards import Reward


def test_rewards_increase_wallet():
    economy = EconomyService(Wallet(credits=10, crystals=1))
    assert economy.add(Reward(credits=25, crystals=2)) == Wallet(credits=35, crystals=3)


def test_spending_never_allows_negative_balance():
    economy = EconomyService(Wallet(credits=20, crystals=2))
    assert economy.spend(credits=7, crystals=1) == Wallet(credits=13, crystals=1)
    with pytest.raises(ValueError):
        economy.spend(credits=14)


def test_can_afford_checks_both_resources():
    economy = EconomyService(Wallet(credits=20, crystals=2))
    assert economy.can_afford(credits=20, crystals=2)
    assert not economy.can_afford(credits=21)
    assert not economy.can_afford(crystals=3)


def test_negative_resource_changes_are_rejected():
    economy = EconomyService()
    with pytest.raises(ValueError):
        economy.add(Reward(credits=-1))
    with pytest.raises(ValueError):
        economy.spend(crystals=-1)
