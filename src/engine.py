from typing import Any, Iterable

from tcod.console import Console
from tcod.context import Context
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap
from input_handlers import MainHandler


class Engine:
    def __init__(
        self,
        event_handler: MainHandler,
        game_map: GameMap,
        player: Entity,
    ) -> None:
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.on_event(event)

            if not action:
                continue

            action.perform(engine=self, entity=self.player)

            self.update_fov()

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console=console)

        context.present(console=console)
        console.clear()

    def update_fov(self) -> None:
        """Calculate map tiles that are visible to the player."""
        self.game_map.visible[:] = compute_fov(
            transparency=self.game_map.tiles["transparent"],
            pov=(self.player.x, self.player.y),
            radius=8,
        )

        self.game_map.explored |= self.game_map.visible
