from typing import Tuple

import numpy as np

# compatible with Console.tiles_rgb
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # np.int32 is for unicode code point
        ("fg", "3B"),  # 3B stands for 3 unsigned bytes
        ("bg", "3B"),
    ]
)
tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # True if this tile can be walked over.
        ("transparent", np.bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
    ]
)


def new_tile(
    *,
    walkable: bool,
    transparent: bool,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Define a new tile type such as wall or floor."""
    return np.array((walkable, transparent, dark), np.dtype)


wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("#"), (255, 255, 255), (50, 50, 150)),
)
floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("·"), (255, 255, 255), (0, 0, 100)),
)
