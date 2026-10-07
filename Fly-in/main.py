"""Main entry point for the Fly-In Drones simulation project."""

import sys
from parser import MapParseError, MapParser
from network import Graph
from simulator import Simulator


def main() -> None:
    """Load the map file, build the network, and run the simulation."""
    filepath = sys.argv[1] if len(sys.argv) > 1 else "map.txt"

    try:
        parser = MapParser(filepath)
        parser.parse()
    except MapParseError as error:
        print("Failed to parse map file:")
        print(error)
        return

    start_zone = ""
    end_zone = ""
    for zone in parser.zones.values():
        if zone.is_start:
            start_zone = zone.name
        if zone.is_end:
            end_zone = zone.name

    graph = Graph(parser.zones, parser.connections)
    simulator = Simulator(graph, parser.nb_drones, start_zone, end_zone)
    simulator.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nbye")
