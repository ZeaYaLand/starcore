import pytest

from game.ranking import RankingService


def test_ranking_orders_by_score_then_player_id():
    ranking = RankingService()
    ranking.register("p2", 100)
    ranking.register("p1", 200)
    ranking.register("p3", 100)
    entries = ranking.leaderboard()
    assert [(entry.player_id, entry.score) for entry in entries] == [
        ("p1", 200),
        ("p2", 100),
        ("p3", 100),
    ]


def test_add_score_and_rank():
    ranking = RankingService()
    ranking.register("p1", 10)
    ranking.register("p2", 20)
    ranking.register("p3", 30)
    updated = ranking.add_score("p1", 25)
    assert updated.player_id == "p1"
    assert updated.score == 35
    assert ranking.rank_of("p1") == 1
    assert [entry.player_id for entry in ranking.leaderboard(limit=2)] == ["p1", "p3"]


def test_validation():
    ranking = RankingService()
    with pytest.raises(ValueError):
        ranking.register("", 0)
    with pytest.raises(ValueError):
        ranking.register("p1", -1)
    ranking.register("p1")
    with pytest.raises(ValueError):
        ranking.register("p1")
    with pytest.raises(ValueError):
        ranking.add_score("p1", -1)
    with pytest.raises(KeyError):
        ranking.add_score("missing", 1)
    with pytest.raises(KeyError):
        ranking.rank_of("missing")
    with pytest.raises(ValueError):
        ranking.leaderboard(limit=0)
