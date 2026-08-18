from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Optional

import numpy as np
from tcod.console import Console

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

from tile_types import SHROUD, wall


class GameMap:
    def __init__(
        self, width: int, height: int, engine: Engine, entities: Iterable[Entity]
    ) -> None:
        self.width = width
        self.height = height
        self.engine = engine
        self.entities = set(entities)
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

        for entity in self.entities:
            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, text=entity.char, fg=entity.color)

    def get_entity_at_destination(
        self, destination_x: int, destination_y: int
    ) -> Optional[Entity]:
        """Checks for blocking entity at destination coordinates and returns it if present."""
        for entity in self.entities:
            if entity.x == destination_x and entity.y == destination_y:
                if entity.blocks_movement:
                    return entity
        return None
