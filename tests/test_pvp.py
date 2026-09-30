import pytest

from game.pvp import PvPService


def test_registration_and_leaderboard():
    service = PvPService()
    service.register("b", 1200)
    service.register("a", 1300)
    assert [p.player_id for p in service.leaderboard()] == ["a", "b"]


def test_matchmaking_rejects_large_rating_gap():
    service = PvPService()
    service.register("a", 1000)
    service.register("b", 1400)
    with pytest.raises(ValueError):
        service.matchmake("a", "b", max_gap=250)


def test_match_result_updates_rating_and_record():
    service = PvPService()
    service.register("a")
    service.register("b")
    match = service.matchmake("a", "b")
    service.record_result(match, "a")
    assert service.players["a"].wins == 1
    assert service.players["b"].losses == 1
    assert service.players["a"].rating == 1025
    assert service.players["b"].rating == 975
