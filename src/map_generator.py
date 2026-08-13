import random
from typing import Iterator, Tuple

import tcod

import tile_types
from game_map import GameMap


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


def generate_dungeon(dungeon_width: int, dungeon_height: int) -> GameMap:
    dungeon = GameMap(width=dungeon_width, height=dungeon_height)

    room1 = RectangularRoom(x=10, y=15, width=15, height=20)
    room2 = RectangularRoom(x=35, y=15, width=20, height=25)

    dungeon.tiles[room1.inner] = tile_types.floor
    dungeon.tiles[room2.inner] = tile_types.floor

    for x, y in generate_tunnel(start=(room1.center), end=(room2.center)):
        dungeon.tiles[x, y] = tile_types.floor

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
