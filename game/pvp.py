from dataclasses import dataclass

from game.combat import CombatService, Combatant, CombatResult


@dataclass
class PlayerRating:
    player_id: str
    rating: int = 1000
    wins: int = 0
    losses: int = 0


@dataclass(frozen=True)
class Match:
    match_id: str
    player_a: str
    player_b: str
    rating_gap: int


class PvPService:
    def __init__(self, combat: CombatService | None = None):
        self.combat = combat or CombatService()
        self.players: dict[str, PlayerRating] = {}
        self.matches: list[Match] = []
        self._next_match = 1

    def register(self, player_id: str, rating: int = 1000) -> PlayerRating:
        if not player_id:
            raise ValueError("player_id is required")
        if rating < 0:
            raise ValueError("rating cannot be negative")
        player = self.players.get(player_id)
        if player is None:
            player = PlayerRating(player_id, rating)
            self.players[player_id] = player
        return player

    def leaderboard(self) -> tuple[PlayerRating, ...]:
        return tuple(sorted(self.players.values(), key=lambda item: (-item.rating, item.player_id)))

    def matchmake(self, player_a: str, player_b: str, max_gap: int = 250) -> Match:
        a = self.players.get(player_a)
        b = self.players.get(player_b)
        if a is None or b is None or player_a == player_b:
            raise ValueError("both distinct players must be registered")
        gap = abs(a.rating - b.rating)
        if gap > max_gap:
            raise ValueError("rating gap is too large")
        match = Match(f"match_{self._next_match}", player_a, player_b, gap)
        self._next_match += 1
        self.matches.append(match)
        return match

    def record_result(self, match: Match, winner: str) -> None:
        if winner not in (match.player_a, match.player_b):
            raise ValueError("winner must belong to the match")
        loser = match.player_b if winner == match.player_a else match.player_a
        self.players[winner].wins += 1
        self.players[loser].losses += 1
        self.players[winner].rating += 25
        self.players[loser].rating = max(0, self.players[loser].rating - 25)
