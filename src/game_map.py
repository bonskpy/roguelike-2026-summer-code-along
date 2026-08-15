import numpy as np
from tcod.console import Console

from tile_types import SHROUD, wall


class GameMap:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.tiles = np.full(shape=(width, height), fill_value=wall, order="F")
        self.visible = np.full(shape=(width, height), fill_value=False, order="F")
        self.explored = np.full(shape=(width, height), fill_value=False, order="F")

    def in_bounds(self, coord_x: int, coord_y: int) -> bool:
        """Check if a point is in the map using x and y coordinates."""
        return (0 < coord_x <= self.width) and (0 < coord_y <= self.height)

    def render(self, console: Console) -> None:
        """Renders the map."""
        console.rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=SHROUD,
        )
