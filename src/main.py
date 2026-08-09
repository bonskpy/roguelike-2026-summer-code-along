import tcod

from actions import MovementAction
from input_handlers import MainHandler

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 80

# Typecasting is just passing variable to a constructor of chosed data type.
# In case of custom classes a dudermethod has to be prepared. Casting float to int
# will turncate return value. Casting string decimal to int throws error. It is good
# practice to use defensive casting (try/except) and return ValueError on failure.

player_x = int(SCREEN_WIDTH / 2)
player_y = int(SCREEN_HEIGHT / 2)


def main():
    print("Hello from rogue0!")

    player_x = int(SCREEN_WIDTH / 2)
    player_y = int(SCREEN_HEIGHT / 2)

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    handler = MainHandler()

    with tcod.context.new(
        columns=SCREEN_WIDTH, rows=SCREEN_HEIGHT, tileset=tileset, title="rogue0"
    ) as context:
        root_console = tcod.console.Console(
            width=SCREEN_WIDTH, height=SCREEN_HEIGHT, order="F"
        )
        while True:
            root_console.print(x=player_x, y=player_y, text="@")
            context.present(root_console)
            root_console.clear()

            for event in tcod.event.wait():
                action = handler.on_event(event)

                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy
                else:
                    continue


if __name__ == "__main__":
    main()
