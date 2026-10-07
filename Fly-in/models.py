"""Domain entities representing hubs, links, and drones."""

from enum import Enum


class TerminalColors:
    """Holds ANSI color codes used for terminal simulation output."""

    def __init__(self) -> None:
        """Set up the color map and reset code."""
        self.codes = {
            "black": "\033[30m",
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "magenta": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
            "gray": "\033[90m",
            "grey": "\033[90m",
            "orange": "\033[38;5;208m",
            "purple": "\033[38;5;129m",
            "violet": "\033[38;5;177m",
            "gold": "\033[38;5;220m",
            "lime": "\033[38;5;118m",
            "brown": "\033[38;5;130m",
            "crimson": "\033[38;5;160m",
            "maroon": "\033[38;5;88m",
            "darkred": "\033[38;5;124m",
            "rainbow": "\033[38;5;201m",
            "pink": "\033[38;5;213m",
            "teal": "\033[38;5;37m",
            "navy": "\033[38;5;19m",
            "olive": "\033[38;5;100m",
            "silver": "\033[38;5;246m",
        }
        self.reset = "\033[0m"

    def wrap(self, text: str, color: str | None) -> str:
        """Wrap text with the ANSI code for color, if it's recognized."""
        if color and color.lower() in self.codes:
            return f"{self.codes[color.lower()]}{text}{self.reset}"
        return text


class ZoneType(Enum):
    """Supported zone types and their routing properties."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"

    def move_cost(self) -> int:
        """Return the turn cost required to enter this zone."""
        costs = {
            ZoneType.NORMAL: 1,
            ZoneType.PRIORITY: 1,
            ZoneType.RESTRICTED: 2,
            ZoneType.BLOCKED: -1,
        }
        return costs[self]

    def path_weight(self) -> float:
        """Return weight used for Dijkstra path selection."""
        weights = {
            ZoneType.NORMAL: 1.0,
            ZoneType.PRIORITY: 0.9,
            ZoneType.RESTRICTED: 2.0,
            ZoneType.BLOCKED: 999.0,
        }
        return weights[self]


class Zone:
    """Represents a node/hub in the flight network."""

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone_type: ZoneType = ZoneType.NORMAL,
        color: str | None = None,
        max_drones: int = 1,
        is_start: bool = False,
        is_end: bool = False,
    ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.color = color
        self.is_start = is_start
        self.is_end = is_end
        self.max_drones = -1 if (is_start or is_end) else max_drones
        self.colors = TerminalColors()

    def has_unlimited_capacity(self) -> bool:
        """Check whether capacity limits apply to this zone."""
        return self.max_drones == -1

    def get_colored_name(self) -> str:
        """Wrap the zone name with its configured terminal color."""
        return self.colors.wrap(self.name, self.color)


class Link:
    """Represents a bidirectional connection between two zones."""

    def __init__(
        self,
        zone_a: str,
        zone_b: str,
        max_link_capacity: int = 1,
    ) -> None:
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity

    def connects(self, name: str) -> bool:
        """Check if this link connects to the specified zone."""
        return name == self.zone_a or name == self.zone_b


class Drone:
    """Represents an active drone navigating through the network."""

    def __init__(self, drone_id: int, start_zone: str) -> None:
        self.drone_id = drone_id
        self.current_zone = start_zone
        self.delivered = False
        self.path: list[str] = []
        self.path_index: int = 0
        self.in_transit_to: str | None = None
        self.turns_remaining: int = 0
        self.transit_connection: str | None = None
        self.link_reservation_key: tuple[str, str] | None = None

    def is_in_transit(self) -> bool:
        """Check whether the drone is currently flying across a link."""
        return self.in_transit_to is not None

    def start_transit(self, destination: str, turns: int) -> None:
        """Initiate multi-turn transit toward a restricted zone."""
        if self.is_in_transit():
            raise ValueError(f"D{self.drone_id} is already in transit")

        if self.delivered:
            raise ValueError(f"D{self.drone_id} is already delivered")

        self.in_transit_to = destination
        self.turns_remaining = turns

    def advance_transit(self) -> bool:
        """Advance transit countdown and land drone when completed."""
        if self.in_transit_to is None:
            raise ValueError(f"D{self.drone_id} is not in transit")

        self.turns_remaining -= 1

        if self.turns_remaining == 0:
            self.current_zone = self.in_transit_to
            self.in_transit_to = None
            return True

        return False
