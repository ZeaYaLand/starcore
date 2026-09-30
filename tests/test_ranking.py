import pytest

from game.ranking import RankingService


def test_ranking_orders_by_score_then_player_id():
    ranking = RankingService()
    ranking.register("p2", 100)
    ranking.register("p1", 200)
    ranking.register("p3", 100)
    assert ranking.leaderboard() == (
        ranking.leaderboard()[0],
        ranking.leaderboard()[1],
        ranking.leaderboard()[2],
    )
    assert [entry.player_id for entry in ranking.leaderboard()] == ["p1", "p2", "p3"]


def test_add_score_and_rank():
    ranking = RankingService()
    ranking.register("p1", 10)
    ranking.register("p2", 20)
    ranking.register("p3", 30)
    ranking.add_score("p1", 25)
    assert ranking.rank_of("p1") == 2
    assert ranking.leaderboard(limit=2)[0].player_id == "p3"


def test_validation():
    ranking = RankingService()
    with pytest.raises(ValueError):
        ranking.register("", 0)
    with pytest.raises(ValueError):
        ranking.register("p1", -1)
    ranking.register("p1")
    with pytest.raises(ValueError):
        ranking.add_score("p1", -1)
    with pytest.raises(KeyError):
        ranking.rank_of("missing")
