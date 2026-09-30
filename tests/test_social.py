import pytest

from game.social import SocialService


def setup_service():
    service = SocialService()
    service.register("p1", "Nova")
    service.register("p2", "Zero")
    return service


def test_follow_and_unfollow():
    service = setup_service()
    assert service.follow("p1", "p2") is True
    assert "p1" in service.profiles["p2"].followers
    assert service.unfollow("p1", "p2") is True
    assert "p1" not in service.profiles["p2"].followers


def test_friend_request_and_acceptance_is_symmetric():
    service = setup_service()
    assert service.send_friend_request("p1", "p2") is True
    assert service.accept_friend_request("p2", "p1") is True
    assert service.profiles["p1"].friends == {"p2"}
    assert service.profiles["p2"].friends == {"p1"}


def test_duplicate_friend_request_is_rejected():
    service = setup_service()
    assert service.send_friend_request("p1", "p2") is True
    assert service.send_friend_request("p2", "p1") is False


def test_unknown_player_is_rejected():
    service = setup_service()
    with pytest.raises(KeyError):
        service.follow("p1", "missing")
