from typing import Any, Iterable, Set

from tcod.console import Console
from tcod.context import Context

from actions import EscapeAction, MovementAction
from entity import Entity
from input_handlers import Handler, MainHandler


class Engine:
    def __init__(
        self, entities: Set[Entity], event_handler: MainHandler, player: Entity
    ) -> None:
        self.entities = entities
        self.event_handler = event_handler
        self.player = player

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.on_event(event)

            if not action:
                continue

            if isinstance(action, MovementAction):
                self.player.move(dx=action.dx, dy=action.dy)

            if isinstance(action, EscapeAction):
                raise SystemExit()

    def render(self, console: Console, context: Context) -> None:
        for entity in self.entities:
            console.print(x=entity.x, y=entity.y, text=entity.char, fg=entity.color)

        context.present(console=console)
        console.clear()
