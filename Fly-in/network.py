"""Graph representation and shortest-path routing algorithms."""

from models import Link, Zone, ZoneType


class Graph:

    """Manages the network graph and pathfinding algorithms."""

    def __init__(
        self, zones: dict[str, Zone], connections: list[Link]
    ) -> None:
        self.zones = zones
        self.connections = connections
        self.neighbors: dict[str, list[str]] = {}
        for name in zones:
            self.neighbors[name] = []

        self.build_adjacency()

    def build_adjacency(self) -> None:
        """Populate the neighbor list, skipping any blocked zones."""
        for link in self.connections:
            zone_a = link.zone_a
            zone_b = link.zone_b

            # Blocked zones cannot be entered or used
            if self.zones[zone_a].zone_type == ZoneType.BLOCKED:
                continue
            if self.zones[zone_b].zone_type == ZoneType.BLOCKED:
                continue

            self.neighbors[zone_a].append(zone_b)
            self.neighbors[zone_b].append(zone_a)

    def edge_key(self, zone_a: str, zone_b: str) -> tuple[str, str]:
        """Return a sorted pair to uniquely identify an undirected link."""
        pair = sorted([zone_a, zone_b])
        return (pair[0], pair[1])

    def get_link(self, zone_a: str, zone_b: str) -> Link | None:
        """Find the Link object connecting two zones, if one exists."""
        for link in self.connections:
            if link.connects(zone_a) and link.connects(zone_b):
                return link
        return None

    def path_cost(self, path: list[str]) -> float:
        """Calculate the total movement cost along a path."""
        total = 0.0
        for i in range(1, len(path)):
            zone_name = path[i]
            total += self.zones[zone_name].zone_type.path_weight()
        return total

    def route_capacity(self, path: list[str]) -> int:
        """Find the bottleneck (minimum) capacity along a given route."""
        smallest = -1

        # Check zone capacities (start and end have unlimited capacity)
        for zone_name in path:
            zone = self.zones[zone_name]
            if zone.has_unlimited_capacity():
                continue
            if smallest == -1 or zone.max_drones < smallest:
                smallest = zone.max_drones

        # Check link capacities between consecutive zones
        for i in range(1, len(path)):
            link = self.get_link(path[i - 1], path[i])
            if link is None:
                continue
            if smallest == -1 or link.max_link_capacity < smallest:
                smallest = link.max_link_capacity

        return smallest if smallest != -1 else 1000

    def dijkstra(
        self,
        start: str,
        end: str,
        avoid_nodes: set[str],
        avoid_edges: set[tuple[str, str]],
    ) -> list[str]:
        """Find the lowest-cost route using Dijkstra's algorithm."""
        costs: dict[str, float] = {start: 0.0}
        parent_zone: dict[str, str] = {}
        visited: set[str] = set()

        while True:
            current_zone: str | None = None
            lowest_cost = float("inf")

            # Pick the unvisited zone with the lowest known cost
            for zone_name, cost in costs.items():
                if zone_name not in visited and cost < lowest_cost:
                    lowest_cost = cost
                    current_zone = zone_name

            if current_zone is None or current_zone == end:
                break

            visited.add(current_zone)

            for neighbor in self.neighbors[current_zone]:
                if neighbor in avoid_nodes:
                    continue

                edge = self.edge_key(current_zone, neighbor)
                if edge in avoid_edges:
                    continue

                step_weight = self.zones[neighbor].zone_type.path_weight()
                new_cost = costs[current_zone] + step_weight

                if neighbor not in costs or new_cost < costs[neighbor]:
                    costs[neighbor] = new_cost
                    parent_zone[neighbor] = current_zone

        if end not in costs:
            return []

        path: list[str] = []
        step = end
        while step != start:
            path.append(step)
            step = parent_zone[step]
        path.append(start)
        path.reverse()
        return path

    def get_all_paths(
        self, start: str, end: str, max_paths: int = 1000
    ) -> list[list[str]]:
        """Find multiple alternative routes using Yen's algorithm."""
        first_path = self.dijkstra(start, end, set(), set())
        if not first_path:
            return []

        all_paths: list[list[str]] = [first_path]

        while len(all_paths) < max_paths:
            candidates: list[list[str]] = []
            last_path = all_paths[-1]

            for i in range(len(last_path) - 1):
                branch_zone = last_path[i]
                path_prefix = last_path[: i + 1]

                blocked_edges: set[tuple[str, str]] = set()
                for existing_path in all_paths:
                    same_prefix = (
                        len(existing_path) > i
                        and existing_path[: i + 1] == path_prefix
                    )
                    if same_prefix:
                        edge = self.edge_key(
                            existing_path[i], existing_path[i + 1]
                        )
                        blocked_edges.add(edge)

                blocked_nodes = set(path_prefix[:-1])

                detour = self.dijkstra(
                    branch_zone, end, blocked_nodes, blocked_edges
                )
                if not detour:
                    continue

                candidate_path = path_prefix[:-1] + detour
                if candidate_path not in candidates:
                    candidates.append(candidate_path)

            if not candidates:
                break

            best_candidate = min(candidates, key=self.path_cost)
            candidates.remove(best_candidate)
            all_paths.append(best_candidate)

        return all_paths
