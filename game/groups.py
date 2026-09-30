from dataclasses import dataclass, field


@dataclass
class Group:
    group_id: str
    name: str
    owner_id: str
    members: set[str] = field(default_factory=set)


class GroupService:
    def __init__(self, max_members: int = 50):
        if max_members < 1:
            raise ValueError("max_members must be positive")
        self.max_members = max_members
        self.groups: dict[str, Group] = {}
        self._next_id = 1

    def create_group(self, owner_id: str, name: str) -> Group:
        if not owner_id or not name.strip():
            raise ValueError("owner_id and name are required")
        group_id = f"group-{self._next_id}"
        self._next_id += 1
        group = Group(group_id, name.strip(), owner_id, {owner_id})
        self.groups[group_id] = group
        return group

    def invite(self, group_id: str, inviter_id: str, player_id: str) -> bool:
        group = self._get(group_id)
        self._require_member(group, inviter_id)
        if not player_id or player_id in group.members:
            return False
        if len(group.members) >= self.max_members:
            return False
        group.members.add(player_id)
        return True

    def leave(self, group_id: str, player_id: str) -> bool:
        group = self._get(group_id)
        if player_id not in group.members:
            return False
        if player_id == group.owner_id:
            raise ValueError("owner cannot leave the group")
        group.members.remove(player_id)
        return True

    def disband(self, group_id: str, owner_id: str) -> bool:
        group = self._get(group_id)
        if group.owner_id != owner_id:
            return False
        del self.groups[group_id]
        return True

    def members(self, group_id: str) -> tuple[str, ...]:
        group = self._get(group_id)
        return tuple(sorted(group.members))

    def _get(self, group_id: str) -> Group:
        if group_id not in self.groups:
            raise KeyError("unknown group")
        return self.groups[group_id]

    @staticmethod
    def _require_member(group: Group, player_id: str) -> None:
        if player_id not in group.members:
            raise PermissionError("player is not a group member")
