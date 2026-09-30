from dataclasses import dataclass, field

from game.locations import Location, LOCATIONS, get_location


@dataclass
class WorldState:
    current_location_id: str = "ruins"
    visited_locations: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        if get_location(self.current_location_id) is None:
            raise ValueError("unknown starting location")
        self.visited_locations.add(self.current_location_id)

    @property
    def current_location(self) -> Location:
        location = get_location(self.current_location_id)
        if location is None:
            raise ValueError("current location no longer exists")
        return location

    def move_to(self, location_id: str) -> Location:
        location = get_location(location_id)
        if location is None:
            raise ValueError("unknown location")
        self.current_location_id = location.location_id
        self.visited_locations.add(location.location_id)
        return location

    def available_locations(self) -> tuple[Location, ...]:
        return tuple(LOCATIONS)
