import tcod

from engine import Engine
from entity import Entity
from input_handlers import MainHandler
from map_generator import generate_dungeon

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

MAP_WIDTH = 80
MAP_HEIGHT = 45

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
ROOM_MAX_COUNT = 30

# Typecasting is just passing variable to a constructor of chosed data type.
# In case of custom classes a dudermethod has to be prepared. Casting float to int
# will turncate return value. Casting string decimal to int throws error. It is good
# practice to use defensive casting (try/except) and return ValueError on failure.


def main():
    print("Hello from rogue0!")

    player = Entity(x=int(SCREEN_WIDTH / 2), y=int(SCREEN_HEIGHT / 2), char="@")

    dungeon = generate_dungeon(
        room_max_size=ROOM_MAX_SIZE,
        room_min_size=ROOM_MIN_SIZE,
        room_count=ROOM_MAX_COUNT,
        dungeon_width=MAP_WIDTH,
        dungeon_height=MAP_HEIGHT,
        player=player,
    )
    main_handler = MainHandler()
    engine = Engine(event_handler=main_handler, game_map=dungeon, player=player)

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    with tcod.context.new(
        columns=SCREEN_WIDTH, rows=SCREEN_HEIGHT, tileset=tileset, title="rogue0"
    ) as context:
        root_console = tcod.console.Console(
            width=SCREEN_WIDTH, height=SCREEN_HEIGHT, order="F"
        )
        while True:
            events = tcod.event.wait()
            engine.render(console=root_console, context=context)
            engine.handle_events(events)


if __name__ == "__main__":
    main()
