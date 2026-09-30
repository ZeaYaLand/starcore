from dataclasses import dataclass

from game.rewards import Reward


@dataclass(frozen=True)
class Wallet:
    credits: int = 0
    crystals: int = 0


class EconomyService:
    def __init__(self, wallet: Wallet | None = None):
        self.wallet = wallet or Wallet()

    def add(self, reward: Reward) -> Wallet:
        if reward.credits < 0 or reward.crystals < 0:
            raise ValueError("rewards cannot contain negative resources")
        self.wallet = Wallet(
            credits=self.wallet.credits + reward.credits,
            crystals=self.wallet.crystals + reward.crystals,
        )
        return self.wallet

    def spend(self, *, credits: int = 0, crystals: int = 0) -> Wallet:
        if credits < 0 or crystals < 0:
            raise ValueError("spending amounts cannot be negative")
        if credits > self.wallet.credits or crystals > self.wallet.crystals:
            raise ValueError("insufficient resources")
        self.wallet = Wallet(
            credits=self.wallet.credits - credits,
            crystals=self.wallet.crystals - crystals,
        )
        return self.wallet

    def can_afford(self, *, credits: int = 0, crystals: int = 0) -> bool:
        return credits >= 0 and crystals >= 0 and credits <= self.wallet.credits and crystals <= self.wallet.crystals
