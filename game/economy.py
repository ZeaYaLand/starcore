from dataclasses import dataclass

from game.rewards import Reward


@dataclass(frozen=True)
class Wallet:
    credits: int = 0
    crystals: int = 0


@dataclass(frozen=True)
class EconomyTransaction:
    kind: str
    credits: int
    crystals: int
    balance_after: Wallet


class EconomyService:
    def __init__(self, wallet: Wallet | None = None):
        self.wallet = wallet or Wallet()
        self.transactions: list[EconomyTransaction] = []

    def _record(self, kind: str, credits: int, crystals: int) -> Wallet:
        self.transactions.append(EconomyTransaction(kind, credits, crystals, self.wallet))
        return self.wallet

    def add(self, reward: Reward) -> Wallet:
        if reward.credits < 0 or reward.crystals < 0:
            raise ValueError("rewards cannot contain negative resources")
        self.wallet = Wallet(
            credits=self.wallet.credits + reward.credits,
            crystals=self.wallet.crystals + reward.crystals,
        )
        return self._record("add", reward.credits, reward.crystals)

    def spend(self, *, credits: int = 0, crystals: int = 0) -> Wallet:
        if credits < 0 or crystals < 0:
            raise ValueError("spending amounts cannot be negative")
        if credits > self.wallet.credits or crystals > self.wallet.crystals:
            raise ValueError("insufficient resources")
        self.wallet = Wallet(
            credits=self.wallet.credits - credits,
            crystals=self.wallet.crystals - crystals,
        )
        return self._record("spend", -credits, -crystals)

    def can_afford(self, *, credits: int = 0, crystals: int = 0) -> bool:
        return credits >= 0 and crystals >= 0 and credits <= self.wallet.credits and crystals <= self.wallet.crystals

    def transaction_history(self) -> tuple[EconomyTransaction, ...]:
        return tuple(self.transactions)
