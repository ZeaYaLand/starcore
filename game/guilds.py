from dataclasses import dataclass, field


@dataclass
class Guild:
    guild_id: str
    name: str
    leader_id: str
    members: set[str] = field(default_factory=set)
    points: int = 0

    def __post_init__(self) -> None:
        self.members.add(self.leader_id)

    def add_member(self, player_id: str) -> None:
        if not player_id:
            raise ValueError("player_id is required")
        self.members.add(player_id)

    def remove_member(self, player_id: str) -> None:
        if player_id == self.leader_id:
            raise ValueError("leader cannot be removed")
        self.members.discard(player_id)

    def add_points(self, points: int) -> None:
        if points < 0:
            raise ValueError("points cannot be negative")
        self.points += points


class GuildService:
    def __init__(self):
        self.guilds: dict[str, Guild] = {}

    def create(self, guild_id: str, name: str, leader_id: str) -> Guild:
        if guild_id in self.guilds:
            raise ValueError("guild already exists")
        guild = Guild(guild_id, name, leader_id)
        self.guilds[guild_id] = guild
        return guild

    def get(self, guild_id: str) -> Guild:
        if guild_id not in self.guilds:
            raise KeyError(guild_id)
        return self.guilds[guild_id]

    def leaderboard(self) -> tuple[Guild, ...]:
        return tuple(sorted(self.guilds.values(), key=lambda guild: (-guild.points, guild.guild_id)))
