from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    location_id: str
    name: str
    description: str
    energy_cost: int
    danger: int


LOCATIONS = (
    Location("ruins", "Ancient Ruins", "Fragments of a forgotten civilization.", 10, 10),
    Location("laboratory", "Abandoned Laboratory", "A sealed research complex hides useful technology.", 15, 25),
    Location("storm_zone", "Energy Storm Zone", "A dangerous sector filled with unstable energy.", 20, 50),
)


def get_location(location_id: str) -> Location | None:
    normalized = location_id.strip().lower()
    return next((location for location in LOCATIONS if location.location_id == normalized), None)
