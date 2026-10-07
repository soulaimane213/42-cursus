"""Parser for drone network map files."""

from models import Link, Zone, ZoneType


class MapParseError(Exception):
    """Raised when the map file is malformed."""

    def __init__(self, line_number: int, message: str) -> None:
        """Store the line number and message of the error."""
        self.line_number = line_number
        self.message = message
        error_text = "Line " + str(line_number) + ": " + message
        super().__init__(error_text)


class MapParser:
    """Reads a map file and builds zones, connections, and drone count."""

    def __init__(self, filepath: str) -> None:
        """Set up empty storage before reading the file."""
        self.filepath = filepath
        self.nb_drones = 0
        self.zones: dict[str, Zone] = {}
        self.connections: list[Link] = []
        self.seen_connections: set[str] = set()
        self.got_nb_drones = False

    def read_lines(self) -> list[tuple[int, str]]:
        """Open the file and return a list of (line_number, text) pairs."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                raw_lines = file.readlines()
        except OSError as error:
            raise MapParseError(0, "Cannot open file: " + str(error))

        result: list[tuple[int, str]] = []

        for index in range(len(raw_lines)):
            line_number = index + 1
            line = raw_lines[index].strip()

            if line == "":
                continue

            if line.startswith("#"):
                continue

            if "#" in line:
                pos = line.index("#")
                line = line[:pos].strip()

            if line == "":
                continue

            result.append((line_number, line))

        return result

    def parse_nb_drones_line(self, line: str, line_number: int) -> None:
        """Parse a nb_drones: line."""
        if self.got_nb_drones:
            raise MapParseError(
                line_number,
                "Duplicate nb_drones definition: "
                "nb_drones can only be specified once",
            )

        parts = line.split(":")
        if len(parts) != 2:
            raise MapParseError(line_number, "Invalid nb_drones format")

        value_text = parts[1].strip()

        if not value_text.isdigit():
            raise MapParseError(
                line_number, "nb_drones must be a positive integer"
            )

        value = int(value_text)

        if value <= 0:
            raise MapParseError(
                line_number, "nb_drones must be greater than zero"
            )

        self.nb_drones = value
        self.got_nb_drones = True

    def parse_int_field(
        self, text: str, line_number: int, field_name: str
    ) -> int:
        """Parse a signed integer field, raising MapParseError on error."""
        is_negative = text.startswith("-")
        digits_part = text[1:] if is_negative else text

        if digits_part == "" or not digits_part.isdigit():
            raise MapParseError(
                line_number, f"Invalid {field_name}: {text}"
            )

        return int(text)

    def split_fields_and_metadata(
        self, rest: str, line_number: int
    ) -> tuple[str, str]:
        """Split line into (fields_text, metadata_text)."""
        rest = rest.strip()

        if not rest.endswith("]"):
            if "[" in rest:
                raise MapParseError(line_number, "Unmatched '[' in line")
            return rest, ""

        depth = 0
        open_index = -1
        for i in range(len(rest) - 1, -1, -1):
            if rest[i] == "]":
                depth += 1
            elif rest[i] == "[":
                depth -= 1
                if depth == 0:
                    open_index = i
                    break

        if open_index == -1:
            raise MapParseError(line_number, "Unmatched ']' in line")

        metadata_text = rest[open_index:]
        fields_text = rest[:open_index].strip()
        return fields_text, metadata_text

    def parse_metadata(
        self, text: str, line_number: int, allowed_keys: set[str]
    ) -> dict[str, str]:
        """Parse a [key=value key2=value2] block."""
        text = text.strip()
        if text == "":
            return {}

        if text.count("[") != 1 or text.count("]") != 1:
            raise MapParseError(
                line_number, "Metadata must be a single [ ] block"
            )

        if not text.startswith("[") or not text.endswith("]"):
            raise MapParseError(
                line_number, "Metadata must be inside [ ]"
            )

        inner = text[1:-1].strip()
        if inner == "":
            return {}

        result: dict[str, str] = {}

        for piece in inner.split():
            if piece == "":
                continue
            if "=" not in piece:
                raise MapParseError(
                    line_number, "Invalid metadata: " + piece
                )
            key_value = piece.split("=")
            if len(key_value) != 2:
                raise MapParseError(
                    line_number, "Invalid metadata: " + piece
                )
            key = key_value[0].strip()
            value = key_value[1].strip()
            if key == "" or value == "":
                raise MapParseError(
                    line_number, "Invalid metadata: " + piece
                )
            if key not in allowed_keys:
                raise MapParseError(
                    line_number, f"Unknown metadata key: {key}"
                )
            if key in result:
                raise MapParseError(
                    line_number, f"Duplicate metadata key: {key}"
                )
            result[key] = value

        return result

    def parse_zone_line(self, line: str, line_number: int) -> None:
        """Parse one hub/start_hub/end_hub line and store the Zone."""
        if line.startswith("start_hub:"):
            prefix = "start_hub:"
            is_start = True
            is_end = False
        elif line.startswith("end_hub:"):
            prefix = "end_hub:"
            is_start = False
            is_end = True
        elif line.startswith("hub:"):
            prefix = "hub:"
            is_start = False
            is_end = False
        else:
            raise MapParseError(
                line_number, "Unknown line type: " + line
            )

        rest = line[len(prefix):].strip()

        if "]" in rest and not rest.endswith("]"):
            last_bracket = rest.rfind("]")
            trailing = rest[last_bracket + 1:].strip()
            if trailing != "":
                raise MapParseError(
                    line_number,
                    "Unexpected text after metadata block: " + trailing,
                )

        fields_text, metadata_text = self.split_fields_and_metadata(
            rest, line_number
        )

        fields = fields_text.split()

        if len(fields) != 3:
            raise MapParseError(
                line_number,
                "Expected 'name x y', got: " + fields_text,
            )

        name = fields[0]
        x_text = fields[1]
        y_text = fields[2]

        if name in self.zones:
            raise MapParseError(
                line_number, "Duplicate zone name: " + name
            )

        if "-" in name:
            raise MapParseError(
                line_number, "Zone name cannot contain '-'"
            )

        x = self.parse_int_field(x_text, line_number, "x coordinate")
        y = self.parse_int_field(y_text, line_number, "y coordinate")

        allowed_meta = {"zone", "color", "max_drones", "max_zone"}
        metadata = self.parse_metadata(
            metadata_text, line_number, allowed_meta
        )

        zone_type_text = metadata.get("zone", "normal")

        try:
            zone_type = ZoneType(zone_type_text)
        except ValueError:
            raise MapParseError(
                line_number, "Invalid zone type: " + zone_type_text
            )

        color = metadata.get("color", None)
        max_drones = 1

        # max_drones is ignored on start_hub and end_hub per subject rules
        if not (is_start or is_end):
            max_drones_text = (
                metadata.get("max_drones")
                or metadata.get("max_zone")
                or "1"
            )

            if not max_drones_text.isdigit():
                raise MapParseError(
                    line_number,
                    "Invalid max_drones: " + max_drones_text,
                )

            max_drones = int(max_drones_text)
            if max_drones <= 0:
                raise MapParseError(
                    line_number, "max_drones must be positive"
                )

        zone = Zone(
            name=name,
            x=x,
            y=y,
            zone_type=zone_type,
            color=color,
            max_drones=max_drones,
            is_start=is_start,
            is_end=is_end,
        )

        self.zones[name] = zone

    def parse_connection_line(self, line: str, line_number: int) -> None:
        """Parse one connection line and store the Link."""
        prefix = "connection:"
        rest = line[len(prefix):].strip()

        if "]" in rest and not rest.endswith("]"):
            last_bracket = rest.rfind("]")
            trailing = rest[last_bracket + 1:].strip()
            if trailing != "":
                raise MapParseError(
                    line_number,
                    "Unexpected text after metadata block: " + trailing,
                )

        names_text, metadata_text = self.split_fields_and_metadata(
            rest, line_number
        )

        if "-" not in names_text:
            raise MapParseError(
                line_number,
                "Expected 'name1-name2', got: " + names_text,
            )

        names = names_text.split("-")
        if len(names) != 2:
            raise MapParseError(
                line_number,
                "Expected exactly two zone names: " + names_text,
            )

        zone_a = names[0].strip()
        zone_b = names[1].strip()

        if zone_a == "" or zone_b == "":
            raise MapParseError(
                line_number, "Empty zone name in connection"
            )

        if zone_a not in self.zones:
            raise MapParseError(
                line_number, "Unknown zone: " + zone_a
            )

        if zone_b not in self.zones:
            raise MapParseError(
                line_number, "Unknown zone: " + zone_b
            )

        if zone_a == zone_b:
            raise MapParseError(
                line_number, "Zone cannot connect to itself"
            )

        sorted_pair = sorted([zone_a, zone_b])
        key = sorted_pair[0] + "|" + sorted_pair[1]

        if key in self.seen_connections:
            raise MapParseError(
                line_number,
                "Duplicate connection: " + names_text,
            )

        metadata = self.parse_metadata(
            metadata_text, line_number, {"max_link_capacity"}
        )

        capacity_text = metadata.get("max_link_capacity", "1")
        if not capacity_text.isdigit():
            raise MapParseError(
                line_number,
                "Invalid max_link_capacity: " + capacity_text,
            )
        capacity = int(capacity_text)
        if capacity <= 0:
            raise MapParseError(
                line_number, "max_link_capacity must be positive"
            )

        link = Link(
            zone_a=zone_a, zone_b=zone_b, max_link_capacity=capacity
        )

        self.connections.append(link)
        self.seen_connections.add(key)

    def validate_start_and_end(self) -> None:
        """Check that exactly one start zone and one end zone exist."""
        start_count = 0
        end_count = 0

        for zone in self.zones.values():
            if zone.is_start:
                start_count += 1
            if zone.is_end:
                end_count += 1

        if start_count == 0:
            raise MapParseError(0, "No start_hub found in the file")
        if start_count > 1:
            raise MapParseError(0, "More than one start_hub found")

        if end_count == 0:
            raise MapParseError(0, "No end_hub found in the file")
        if end_count > 1:
            raise MapParseError(0, "More than one end_hub found")

    def parse(self) -> None:
        """Run the full parsing pipeline."""
        lines = self.read_lines()

        if len(lines) == 0:
            raise MapParseError(1, "File is empty, expected nb_drones line")

        first_line_number, first_line = lines[0]
        if not first_line.startswith("nb_drones:"):
            raise MapParseError(
                first_line_number,
                "First line must start with 'nb_drones:'",
            )

        known_prefixes = [
            "nb_drones:",
            "hub:",
            "start_hub:",
            "end_hub:",
            "connection:",
        ]

        for line_number, line in lines:

            matched = False
            for prefix in known_prefixes:
                if line.startswith(prefix):
                    matched = True
                    break

            if not matched:
                raise MapParseError(
                    line_number, "Unrecognized line: " + line
                )

            if line.startswith("nb_drones:"):
                self.parse_nb_drones_line(line, line_number)

            elif line.startswith("start_hub:"):
                self.parse_zone_line(line, line_number)

            elif line.startswith("end_hub:"):
                self.parse_zone_line(line, line_number)

            elif line.startswith("hub:"):
                self.parse_zone_line(line, line_number)

            elif line.startswith("connection:"):
                self.parse_connection_line(line, line_number)

        if not self.got_nb_drones:
            raise MapParseError(
                1, "File is empty, expected nb_drones line"
            )

        self.validate_start_and_end()
