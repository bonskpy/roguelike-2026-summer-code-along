import numpy as np
from tcod.console import Console

from tile_types import floor, wall


class GameMap:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.tiles = np.full(shape=(width, height), fill_value=floor, order="F")

        self.tiles[30:33, 22] = wall

    def in_bounds(self, coord_x: int, coord_y: int) -> bool:
        """Check if a point is in the map using x and y coordinates."""
        return (0 < coord_x <= self.width) and (0 < coord_y <= self.height)

    def render(self, console: Console) -> None:
        console.rgb[0 : self.width, 0 : self.height] = self.tiles["dark"]
