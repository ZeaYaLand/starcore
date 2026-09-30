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


def test_economy_2_records_transaction_history():
    economy = EconomyService(Wallet(credits=100, crystals=5))
    economy.add(Reward(credits=25, crystals=1))
    economy.spend(credits=10, crystals=2)
    history = economy.transaction_history()
    assert [item.kind for item in history] == ["add", "spend"]
    assert history[0].balance_after == Wallet(credits=125, crystals=6)
    assert history[1].balance_after == Wallet(credits=115, crystals=4)
    assert history[1].credits == -10
    assert history[1].crystals == -2


def test_transaction_history_is_read_only_view():
    economy = EconomyService()
    economy.add(Reward(credits=1))
    history = economy.transaction_history()
    assert isinstance(history, tuple)
    assert len(history) == 1
