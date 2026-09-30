import pytest

from game.guilds import GuildService


def test_create_guild_includes_leader():
    guild = GuildService().create("g1", "Nova", "p1")
    assert guild.members == {"p1"}


def test_members_and_points():
    guild = GuildService().create("g1", "Nova", "p1")
    guild.add_member("p2")
    guild.add_points(50)
    guild.remove_member("p2")
    assert guild.points == 50
    assert guild.members == {"p1"}


def test_leader_cannot_be_removed():
    guild = GuildService().create("g1", "Nova", "p1")
    with pytest.raises(ValueError):
        guild.remove_member("p1")


def test_guild_leaderboard():
    service = GuildService()
    service.create("g2", "B", "p2").add_points(10)
    service.create("g1", "A", "p1").add_points(20)
    assert [guild.guild_id for guild in service.leaderboard()] == ["g1", "g2"]
