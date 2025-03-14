from dataclasses import dataclass


@dataclass
class City:
    latitude: float
    longitude: float
    altitude: int
    location_name: str
