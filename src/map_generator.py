# Enable postponed evaluation for all annotations which will supress undefined name warning for overlaps() method.
# Without this line Python evaluates all type annotations at runtime, which might impact performance when importing large libraries for typing puroses (ie. numpy).
# This line should be right after any file-level docstrings.
# It simply tells Python to treat all type hints as strings.
from __future__ import annotations

import random
from typing import TYPE_CHECKING, Iterator, List, Tuple

import tcod

import tile_types
from game_map import GameMap

if TYPE_CHECKING:
    from entity import Entity


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        """Center of the rectangle room as integer tuple."""
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def overlaps(self, other: RectangularRoom) -> bool:
        """This method returns True if rooms overlap."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


def generate_dungeon(
    room_max_size: int,
    room_min_size: int,
    room_count: int,
    dungeon_width: int,
    dungeon_height: int,
    player: Entity,
) -> GameMap:
    """Generate a new dungeon."""

    dungeon = GameMap(width=dungeon_width, height=dungeon_height, entities=[player])
    rooms: List[RectangularRoom] = []

    for i in range(room_count):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        room_x = random.randint(0, dungeon_width - room_width - 1)
        room_y = random.randint(0, dungeon_height - room_height - 1)

        new_room = RectangularRoom(
            x=room_x, y=room_y, width=room_width, height=room_height
        )

        if any(new_room.overlaps(other_room) for other_room in rooms):
            continue

        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:  # meaning this is the first room
            player.x, player.y = new_room.center
        else:
            for x, y in generate_tunnel(new_room.center, rooms[-1].center):
                dungeon.tiles[x, y] = tile_types.floor

        rooms.append(new_room)

    return dungeon


def generate_tunnel(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    x1, y1 = start
    x2, y2 = end

    if random.random() < 0.5:
        corner_x, corner_y = x2, y1
    else:
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y
