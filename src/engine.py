from tcod.console import Console
from tcod.context import Context
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap


class Engine:
    def __init__(
        self,
        game_map: GameMap,
        player: Entity,
    ) -> None:
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_enemy_turn(self) -> None:
        """Display a notification that visible entity which is not a player is willing to act."""
        for entity in self.game_map.entities - {self.player}:
            if self.game_map.visible[entity.x, entity.y]:
                print(f"{entity.name} is wondering when it will be able to act.")

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
