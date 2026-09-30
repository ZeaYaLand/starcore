import pytest

from game.groups import GroupService


def test_create_group_owner_is_member():
    service = GroupService()
    group = service.create_group("p1", "Explorers")
    assert group.owner_id == "p1"
    assert service.members(group.group_id) == ("p1",)


def test_member_can_invite_and_leave():
    service = GroupService()
    group = service.create_group("p1", "Explorers")
    assert service.invite(group.group_id, "p1", "p2") is True
    assert service.members(group.group_id) == ("p1", "p2")
    assert service.leave(group.group_id, "p2") is True
    assert service.members(group.group_id) == ("p1",)


def test_non_member_cannot_invite():
    service = GroupService()
    group = service.create_group("p1", "Explorers")
    with pytest.raises(PermissionError):
        service.invite(group.group_id, "p2", "p3")


def test_owner_cannot_leave_but_can_disband():
    service = GroupService()
    group = service.create_group("p1", "Explorers")
    with pytest.raises(ValueError):
        service.leave(group.group_id, "p1")
    assert service.disband(group.group_id, "p1") is True
    with pytest.raises(KeyError):
        service.members(group.group_id)


def test_capacity_and_duplicates():
    service = GroupService(max_members=2)
    group = service.create_group("p1", "Explorers")
    assert service.invite(group.group_id, "p1", "p2") is True
    assert service.invite(group.group_id, "p1", "p2") is False
    assert service.invite(group.group_id, "p1", "p3") is False
