from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple

from entity import Entity

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action:
    def __init__(self, entity: Entity) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Engine that this action belongs to."""
        return self.entity.game_map.engine

    def perform(self) -> None:
        """Perform this actin in engine scope for selected entity.
        This method must be overridden by Action subclasses."""
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()


class ActionWithDirection(Action):
    def __init__(self, entity: Entity, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def destination(self) -> Tuple[int, int]:
        """Get action destination coordinates (x, y)."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Entity that blocks movement at move destination."""
        return self.engine.game_map.get_entity_at_destination(*self.destination)

    def perform(self) -> None:
        raise NotImplementedError()


class MeleAction(ActionWithDirection):
    """Class implementing mele attack movement."""

    def perform(self) -> None:
        target = self.blocking_entity
        if not target:
            return

        print(f"You kicked {target.name}!")


class MovementAction(ActionWithDirection):
    """Class implementing entity movement."""

    def perform(self) -> None:
        destination_x, destination_y = self.destination

        # Check if tile is in bounds of the map
        if not self.engine.game_map.in_bounds(destination_x, destination_y):
            return

        # Check if tile is walkable
        if not self.engine.game_map.tiles["walkable"][destination_x, destination_y]:
            return

        # Check if there is an entity blocking move on the target tile
        if self.engine.game_map.get_entity_at_destination(
            destination_x=destination_x, destination_y=destination_y
        ):
            return

        # Move the entity if checks went through
        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    """Utility class deciding which Action should be taken next: mele or move."""

    def perform(self) -> None:
        if self.blocking_entity:
            return MeleAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
