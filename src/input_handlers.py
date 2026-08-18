from __future__ import annotations

from typing import (  # Optional is a type annotation for types that can be None
    TYPE_CHECKING,
    Any,
    Iterable,
    Optional,
    Protocol,
)

import tcod.event  # I am going to use only event module

from actions import Action, BumpAction, EscapeAction

if TYPE_CHECKING:
    from engine import Engine


# This defines contract. Any class implementing on_event() is a Handler.
class Handler(Protocol):
    def on_event(self, event: tcod.event.Event) -> Optional["Handler"]: ...


class MainHandler:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.on_event(event)

            if not action:
                continue

            action.perform()

            self.engine.handle_enemy_turn()
            self.engine.update_fov()

    def on_event(self, event: tcod.event.Event) -> Optional[Action]:
        action: Optional[Action] = None

        match event:
            case tcod.event.KeyDown(sym=tcod.event.KeySym.UP):
                action = BumpAction(entity=self.engine.player, dx=0, dy=-1)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.DOWN):
                action = BumpAction(entity=self.engine.player, dx=0, dy=1)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.LEFT):
                action = BumpAction(entity=self.engine.player, dx=-1, dy=0)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.RIGHT):
                action = BumpAction(entity=self.engine.player, dx=1, dy=0)
            case tcod.event.Quit():
                action = EscapeAction(entity=self.engine.player)

        return action


# class EventHandler(tcod.event.EventDispatch[Action]):
#     def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
#         raise SystemExit()

#     def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
#         action: Optional[Action] = None

#         key = event.sym

#         if key == tcod.event.K_UP:
#             action = MovementAction(dx=0, dy=1)
#         if key == tcod.event.K_DOWN:
#             action = MovementAction(dx=0, dy=-1)
#         if key == tcod.event.K_LEFT:
#             action = MovementAction(dx=-1, dy=0)
#         if key == tcod.event.K_RIGHT:
#             action = MovementAction(dx=1, dy=0)

#         if key == tcod.event.Quit:
#             action = EscapeAction()

#         return action
