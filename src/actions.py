from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform this actin in engine scope for selected entity."""
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


class ActionWithDirection(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

        def perform(self, engine: Engine, entity: Entity) -> None:
            raise NotImplementedError()


class BumpAction(ActionWithDirection):
    """Utility class deciding which Action should be taken next: mele or move."""

    def perform(self, engine: Engine, entity: Entity) -> None:
        destination_x = entity.x + self.dx
        destination_y = entity.y + self.dy
        target = engine.game_map.get_entity_at_destination(
            destination_x=destination_x, destination_y=destination_y
        )
        if target:
            MeleAction(dx=self.dx, dy=self.dy).perform(engine=engine, entity=entity)
        else:
            MovementAction(dx=self.dx, dy=self.dy).perform(engine=engine, entity=entity)


class MeleAction(ActionWithDirection):
    """Class implementing mele attack movement."""

    def perform(self, engine: Engine, entity: Entity) -> None:
        destination_x = entity.x + self.dx
        destination_y = entity.y + self.dy
        target = engine.game_map.get_entity_at_destination(
            destination_x=destination_x, destination_y=destination_y
        )
        if not target:
            return

        print(f"You kicked {target.name}!")


class MovementAction(ActionWithDirection):
    """Class implementing entity movement."""

    def perform(self, engine: Engine, entity: Entity) -> None:
        destination_x = entity.x + self.dx
        destination_y = entity.y + self.dy

        # Check if tile is in bounds of the map
        if not engine.game_map.in_bounds(destination_x, destination_y):
            return

        # Check if tile is walkable
        if not engine.game_map.tiles["walkable"][destination_x, destination_y]:
            return

        # Check if there is an entity blocking move on the target tile
        if engine.game_map.get_entity_at_destination(
            destination_x=destination_x, destination_y=destination_y
        ):
            return

        # Move the entity if checks went through
        entity.move(self.dx, self.dy)
