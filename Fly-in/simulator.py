"""Turn-based simulation engine for routing drones through the network."""

from models import Drone
from network import Graph


class Simulator:
    """Simulates drones moving turn-by-turn through the network."""

    def __init__(
        self,
        graph: Graph,
        nb_drones: int,
        start_name: str,
        end_name: str,
    ) -> None:
        self.graph = graph
        self.start_name = start_name
        self.end_name = end_name

        self.paths = graph.get_all_paths(start_name, end_name)

        self.drones: list[Drone] = []
        for drone_id in range(1, nb_drones + 1):
            self.drones.append(Drone(drone_id, start_name))

        self.reserved: dict[str, int] = {}
        self.link_reserved: dict[tuple[str, str], int] = {}
        self.total_moves = 0

        if not self.paths:
            return

        loads = [0] * len(self.paths)
        caps = [graph.route_capacity(path) for path in self.paths]

        for drone in self.drones:
            best_idx = 0
            best_cost = float("inf")

            for i, path in enumerate(self.paths):
                overflow = max(0, loads[i] - caps[i] + 1)
                cost = graph.path_cost(path) + (overflow * 5.0)

                if cost < best_cost:
                    best_cost = cost
                    best_idx = i

            drone.path = self.paths[best_idx]
            drone.path_index = 0
            loads[best_idx] += 1

    def get_next_zone(self, drone: Drone) -> str | None:
        """Return the next zone name in the drone's path, or None."""
        if drone.delivered:
            return None
        if drone.path_index + 1 >= len(drone.path):
            return None
        return drone.path[drone.path_index + 1]

    def count_occupants(self) -> dict[str, int]:
        """Count current drone occupants in each zone."""
        counts: dict[str, int] = {}
        for drone in self.drones:
            if drone.delivered or drone.is_in_transit():
                continue
            counts[drone.current_zone] = counts.get(drone.current_zone, 0) + 1
        return counts

    def has_room(
        self, zone_name: str, occupant_counts: dict[str, int]
    ) -> bool:
        """Check whether a zone has available capacity for another drone."""
        zone = self.graph.zones[zone_name]
        if zone.has_unlimited_capacity():
            return True
        current_load = (
            occupant_counts.get(zone_name, 0)
            + self.reserved.get(zone_name, 0)
        )
        return current_load < zone.max_drones

    def link_key(self, zone_a: str, zone_b: str) -> tuple[str, str]:
        """Build an undirected pair key for connection tracking."""
        return self.graph.edge_key(zone_a, zone_b)

    def has_link_room(
        self,
        old_zone: str,
        new_zone: str,
        link_counts: dict[tuple[str, str], int],
    ) -> bool:
        """Check if the connection between two zones has capacity."""
        link = self.graph.get_link(old_zone, new_zone)
        if link is None:
            return False
        key = self.link_key(old_zone, new_zone)
        return link_counts.get(key, 0) < link.max_link_capacity

    def process_turn(self, current_turn: int) -> list[str]:

        """Execute one simulation turn using multi-pass resolution."""

        occupant_counts = self.count_occupants()
        link_counts: dict[tuple[str, str], int] = dict(self.link_reserved)
        movements: list[str] = []
        moved_this_turn: set[int] = set()

        for drone in self.drones:
            if drone.delivered or not drone.is_in_transit():
                continue

            arrived = drone.advance_transit()

            if arrived:
                zone_name = drone.current_zone

                self.reserved[zone_name] = self.reserved.get(zone_name, 0) - 1

                key = drone.link_reservation_key

                assert key is not None

                self.link_reserved[key] -= 1

                link_counts[key] -= 1

                drone.link_reservation_key = None

                occupant_counts[zone_name] = (
                    occupant_counts.get(zone_name, 0) + 1
                )

                zone_obj = self.graph.zones[zone_name]

                movements.append(
                    f"D{drone.drone_id}-{zone_obj.get_colored_name()}"
                )

                if zone_name == self.end_name:
                    drone.delivered = True
            else:
                movements.append(
                    f"D{drone.drone_id}-{drone.transit_connection}"
                )

            moved_this_turn.add(drone.drone_id)

        state_changed = True
        while state_changed:
            state_changed = False

            for drone in self.drones:
                if drone.delivered or drone.drone_id in moved_this_turn:
                    continue

                next_zone = self.get_next_zone(drone)
                if next_zone is None:
                    continue

                old_zone = drone.current_zone

                if not self.has_room(next_zone, occupant_counts):
                    continue
                if not self.has_link_room(old_zone, next_zone, link_counts):
                    continue

                zone_object = self.graph.zones[next_zone]

                cost = zone_object.zone_type.move_cost()

                connection_name = f"{old_zone}-{next_zone}"

                key = self.link_key(old_zone, next_zone)

                occupant_counts[old_zone] -= 1

                drone.path_index += 1

                link_counts[key] = link_counts.get(key, 0) + 1

                if cost > 1:
                    self.reserved[next_zone] = (
                        self.reserved.get(next_zone, 0) + 1
                    )
                    self.link_reserved[key] = (
                        self.link_reserved.get(key, 0) + 1
                    )
                    drone.link_reservation_key = key

                    drone.start_transit(next_zone, cost - 1)

                    drone.transit_connection = connection_name

                    movements.append(f"D{drone.drone_id}-{connection_name}")
                else:
                    drone.current_zone = next_zone

                    occupant_counts[next_zone] = (
                        occupant_counts.get(next_zone, 0) + 1
                    )
                    movements.append(
                        f"D{drone.drone_id}-{zone_object.get_colored_name()}"
                    )

                    if next_zone == self.end_name:
                        drone.delivered = True

                moved_this_turn.add(drone.drone_id)

                state_changed = True

        return movements

    def all_delivered(self) -> bool:
        """Check if all drones reached the destination zone."""
        for drone in self.drones:
            if not drone.delivered:
                return False
        return True

    def run(self) -> None:
        """Run the simulation loop until all drones reach the goal."""
        if not self.paths:
            print("No path exists between start and end.")
            return

        turn_number = 0

        while not self.all_delivered():
            turn_number += 1

            movements = self.process_turn(turn_number)
            if not movements:
                print("Deadlock detected: no drones can move.")
                break

            self.total_moves += len(movements)
            print(" ".join(movements))

        print(f"Total Turns: {turn_number}")
