from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Optional, Tuple, TypeVar

if TYPE_CHECKING:
    from game_map import GameMap


class Entity:
    """This is a generic class that represents all in-game entities such as player, monsters and items."""

    game_map: GameMap

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "Unknown",
        blocks_movement: bool = False,
        game_map: Optional[GameMap] = None,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        if game_map:
            self.game_map = game_map
            game_map.entities.add(self)

    def spawn(self: T, entity_x: int, entity_y: int, dungeon: GameMap) -> T:
        """Create a copy of entity class instance in a given place."""

        clone = copy.deepcopy(self)
        clone.x = entity_x
        clone.y = entity_y
        clone.game_map = dungeon
        dungeon.entities.add(clone)
        return clone

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        """Place this entity at a new location.  Handles moving across GameMaps."""
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "game_map"):  # Possibly uninitialized.
                self.game_map.entities.remove(self)
            self.game_map = gamemap
            gamemap.entities.add(self)


T = TypeVar("T", bound=Entity)
