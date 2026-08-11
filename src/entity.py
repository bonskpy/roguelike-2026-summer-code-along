from typing import Tuple


class Entity:
    """This is a generic class that represents all in-game entities such as player, monsters and items."""

    def __init__(
        self, x: int, y: int, char: str, color: Tuple[int, int, int] = (255, 255, 255)
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy
