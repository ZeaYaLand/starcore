from dataclasses import dataclass, field


@dataclass
class SocialProfile:
    player_id: str
    display_name: str
    friends: set[str] = field(default_factory=set)
    followers: set[str] = field(default_factory=set)


class SocialService:
    def __init__(self):
        self.profiles: dict[str, SocialProfile] = {}
        self._requests: set[tuple[str, str]] = set()

    def register(self, player_id: str, display_name: str) -> SocialProfile:
        if not player_id or not display_name:
            raise ValueError("player_id and display_name are required")
        if player_id in self.profiles:
            raise ValueError("profile already exists")
        profile = SocialProfile(player_id, display_name)
        self.profiles[player_id] = profile
        return profile

    def follow(self, follower_id: str, target_id: str) -> bool:
        self._require_users(follower_id, target_id)
        if follower_id == target_id:
            return False
        self.profiles[target_id].followers.add(follower_id)
        return True

    def unfollow(self, follower_id: str, target_id: str) -> bool:
        self._require_users(follower_id, target_id)
        before = len(self.profiles[target_id].followers)
        self.profiles[target_id].followers.discard(follower_id)
        return len(self.profiles[target_id].followers) != before

    def send_friend_request(self, sender_id: str, target_id: str) -> bool:
        self._require_users(sender_id, target_id)
        if sender_id == target_id or target_id in self.profiles[sender_id].friends:
            return False
        request = (sender_id, target_id)
        if request in self._requests or (target_id, sender_id) in self._requests:
            return False
        self._requests.add(request)
        return True

    def accept_friend_request(self, receiver_id: str, sender_id: str) -> bool:
        self._require_users(receiver_id, sender_id)
        request = (sender_id, receiver_id)
        if request not in self._requests:
            return False
        self._requests.remove(request)
        self.profiles[receiver_id].friends.add(sender_id)
        self.profiles[sender_id].friends.add(receiver_id)
        return True

    def _require_users(self, first: str, second: str) -> None:
        if first not in self.profiles or second not in self.profiles:
            raise KeyError("unknown player")
