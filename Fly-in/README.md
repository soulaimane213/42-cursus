*This project has been created as part of the 42 curriculum by sofadl.*

# Fly-in Drones

## Description

Fly-in Drones is a Python simulation that routes a fleet of autonomous drones from a start hub to an end hub through a graph of connected zones. The goal is to move all drones to the destination in the fewest simulation turns possible without violating any capacity constraints or movement rules.

The simulation handles several rules:
- Zone capacities (`max_drones`, default 1)
- Connection capacities (`max_link_capacity`, default 1)
- Different zone types: `normal` (1 turn), `priority` (1 turn, preferred in pathfinding), `restricted` (2 turns), and `blocked` (inaccessible)
- Multi-drone starts and deliveries (start and end hubs have unlimited capacity)

## Instructions

### Requirements

- Python 3.10 or later
- No external libraries required (uses Python standard library only)
- `flake8` and `mypy` for code linting and static typing

### Installation

Install development dependencies:

```bash
make install
```

### Running the simulation

Using the Makefile:

```bash
make run
```

Run with a specific map file:

```bash
make run ARGS="maps/medium/01_dead_end_trap.txt"
```

Or run directly with Python:

```bash
python3 main.py maps/easy/01_linear_path.txt
```

### Other Makefile targets

```bash
make clean   # Remove __pycache__ and temporary cache files
make lint    # Run flake8 and mypy static checks
make debug   # Run using Python's pdb debugger
```

## Algorithm Explanation

### Graph construction

The flight graph is built from scratch without any forbidden libraries like `networkx` or `graphlib`:
- Hubs are parsed into `Zone` objects, and connections into `Link` objects.
- `Graph.build_adjacency()` creates an adjacency list (`dict[str, list[str]]`).
- Any zone defined as `blocked` is skipped completely during adjacency construction, so blocked zones are never reachable.

### Pathfinding

The pathfinding system uses two core components:
1. **Dijkstra's algorithm (`Graph.dijkstra`)**: Finds the lowest-cost path between two hubs based on movement costs:
   - `priority`: weight `0.9` (cheaper, so the algorithm prefers it)
   - `normal`: weight `1.0`
   - `restricted`: weight `2.0` (higher weight because it costs 2 turns)
   - `blocked`: inaccessible, excluded from graph
2. **Alternative routes (`Graph.get_all_paths`)**: Based on Yen's k-shortest paths approach. It takes the best path, tests detours by temporarily avoiding used edges, and collects multiple candidate paths.

### Drone assignment (Load balancing)

Drones are distributed across available paths before the simulation starts:
- For each candidate path, we calculate its bottleneck capacity (the minimum `max_drones` and `max_link_capacity` along that path).
- When assigning a drone to a path, we calculate an effective cost: `path_cost + (congestion * 4.0)`.
- This spreads drones across multiple parallel paths when available instead of crowding a single bottleneck.

### Turn-based simulation

Each simulation turn runs in two phases:
1. **Phase 1 (In-flight arrivals)**: Drones currently in transit toward restricted zones advance. If their countdown finishes, they land in the destination zone and release the link.
2. **Phase 2 (New moves)**: Drones check if their next zone and connection have room. A multi-pass loop runs during this phase so that when a drone moves forward, it immediately frees up space for the drone behind it in the exact same turn.

## Design Decisions

- **Pure Object-Oriented Architecture**: The code is separated into clean, modular classes:
  - `Zone`: Represents a hub with coordinates, zone type, color, and drone capacity.
  - `Link`: Represents a bidirectional edge between two hubs with link capacity.
  - `Drone`: Represents a drone, tracking current zone, transit countdown, and assigned route.
  - `Graph`: Handles adjacency representation, edge lookups, Dijkstra, and pathfinding.
  - `MapParser`: Handles file reading, format checks, and error reporting.
  - `Simulator`: Manages turn simulation, multi-pass movement resolution, and output formatting.
  - `TerminalColors`: Maps color names to ANSI terminal color codes.
- **Single-pass parsing**: Lines are processed in order top-to-bottom so connections can only link previously defined zones, matching the subject rule.
- **Capacity reservations for restricted zones**: Moving into a restricted zone takes 2 turns. The drone reserves the destination zone when entering the connection to guarantee it will never get stuck on the connection.
- **Accurate line number tracking**: When reading the map, each line is paired with its real 1-based line number so error messages always report the exact file line.

## Visual Representation

The program provides colored terminal output using ANSI escape codes:
- Every printed movement (`D<ID>-<zone>`) is wrapped in the color defined in that zone's metadata (e.g. `[color=red]`).
- Over 20 colors are supported (including red, green, blue, yellow, orange, purple, gold, lime, brown, crimson, etc.).
- This makes it easy during peer evaluation to track drone movements and see which zones are active without reading plain black-and-white text.

## Performance Analysis

- **Speed**: Pathfinding and simulation execute in a fraction of a second across all maps.
- **Turn counts vs Reference Targets**:
  - **Easy Maps** (target < 10 turns):
    - `01_linear_path.txt`: **4 turns** (target ≤ 6)
    - `02_simple_fork.txt`: **4 turns** (target ≤ 8)
    - `03_basic_capacity.txt`: **4 turns** (target ≤ 6)
  - **Medium Maps** (target 10–30 turns):
    - `01_dead_end_trap.txt`: **8 turns** (target ≤ 12)
    - `02_circular_loop.txt`: **15 turns** (target ≤ 15)
    - `03_priority_puzzle.txt`: **7 turns** (target ≤ 12)
  - **Hard Maps** (target < 60 turns):
    - `01_maze_nightmare.txt`: **14 turns** (target ≤ 30)
    - `02_capacity_hell.txt`: **16 turns** (target ≤ 35)
    - `03_ultimate_challenge.txt`: **27 turns** (target ≤ 45)
  - **Challenger Map**:
    - `01_the_impossible_dream.txt`: **53 turns** (robust deadlock-free routing)

- **Reliability**: 0 rule violations, no deadlocks, and clean termination once all drones reach the goal.

## Challenges Faced

1. **Building Graph Logic from Scratch**:
   - Because forbidden libraries like `networkx` cannot be used, I had to build the graph and Dijkstra's algorithm from scratch using plain Python dictionaries and lists.
2. **Parsing Map Metadata**:
   - Handling optional metadata brackets `[key=value]` and making sure edge cases like comments and spaces didn't break the parser.
3. **Spreading Drones Across Paths**:
   - Finding a simple way to assign drones to different paths so they don't all queue up on the exact same single path.

## Testing Strategy

The project was validated using a multi-step testing strategy:
- **Parser Test Suite (37 tests)**: Verified that all error cases (missing start/end hubs, negative capacities, duplicate zones/links, unknown zone types, tabs, malformed brackets) fail with clear line numbers.
- **Edge-Case Logic Maps (20 tests)**: Verified specific simulation rules including pipeline moves, connection bottlenecks, dead ends, equal forks, and cyclic loops.
- **Benchmark Maps**: Verified turn counts and 0 rule violations across all official maps (`easy`, `medium`, `hard`, and `challenger`).

## Example Usage

Input map (`maps/easy/01_linear_path.txt`):

```text
nb_drones: 2
start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [color=blue]
end_hub: goal 3 0 [color=red]
connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
```

Running the program:

```bash
python3 main.py maps/easy/01_linear_path.txt
```

Expected output:

```text
D1-waypoint1
D1-waypoint2 D2-waypoint1
D1-goal D2-waypoint2
D2-goal
Total Turns: 4
```

## Resources

- [Dijkstra's algorithm — Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Yen's k-shortest path algorithm — Wikipedia](https://en.wikipedia.org/wiki/Yen%27s_algorithm)
- [Python enum documentation](https://docs.python.org/3/library/enum.html)
- [mypy documentation](https://mypy.readthedocs.io/)
- [flake8 documentation](https://flake8.pycqa.org/)

### Use of AI

An AI assistant was used as a learning aid during the project to:
- Explain the theory behind Dijkstra's algorithm and how to adapt it for weighted zone types.
- Help brainstorm the object-oriented architecture and class separation (`Zone`, `Link`, `Drone`, `Graph`, `Simulator`).
- Discuss general pathfinding concepts and learning resources.