from dataclasses import dataclass


@dataclass(frozen=True)
class RankingEntry:
    player_id: str
    score: int


class RankingService:
    """General progression ranking, separate from the PvP leaderboard."""

    def __init__(self):
        self.scores: dict[str, int] = {}

    def register(self, player_id: str, score: int = 0) -> RankingEntry:
        if not player_id:
            raise ValueError("player_id is required")
        if score < 0:
            raise ValueError("score cannot be negative")
        if player_id in self.scores:
            raise ValueError("player already registered")
        self.scores[player_id] = score
        return RankingEntry(player_id, score)

    def add_score(self, player_id: str, amount: int) -> RankingEntry:
        if player_id not in self.scores:
            raise KeyError("unknown player")
        if amount < 0:
            raise ValueError("amount cannot be negative")
        self.scores[player_id] += amount
        return RankingEntry(player_id, self.scores[player_id])

    def leaderboard(self, limit: int | None = None) -> tuple[RankingEntry, ...]:
        if limit is not None and limit <= 0:
            raise ValueError("limit must be positive")
        entries = tuple(
            RankingEntry(player_id, score)
            for player_id, score in sorted(
                self.scores.items(), key=lambda item: (-item[1], item[0])
            )
        )
        return entries if limit is None else entries[:limit]

    def rank_of(self, player_id: str) -> int:
        if player_id not in self.scores:
            raise KeyError("unknown player")
        return 1 + sum(score > self.scores[player_id] for score in self.scores.values())
