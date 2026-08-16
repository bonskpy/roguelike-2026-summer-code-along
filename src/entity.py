from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Tuple, TypeVar

if TYPE_CHECKING:
    from game_map import GameMap


class Entity:
    """This is a generic class that represents all in-game entities such as player, monsters and items."""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "Unknown",
        blocks_movement: bool = False,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement

    def spawn(self: T, entity_x: int, entity_y: int, dungeon: GameMap) -> T:
        """Create a copy of entity class instance in a given place."""

        clone = copy.deepcopy(self)
        clone.x = entity_x
        clone.y = entity_y
        dungeon.entities.add(clone)
        return clone

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy


T = TypeVar("T", bound=Entity)
