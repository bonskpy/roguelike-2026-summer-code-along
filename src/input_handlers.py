from typing import (  # Optional is a type annotation for types that can be None
    Optional,
    Protocol,
)

import tcod.event  # I am going to use only event module

from actions import Action, BumpAction, EscapeAction


# This defines contract. Any class implementing on_event() is a Handler.
class Handler(Protocol):
    def on_event(self, event: tcod.event.Event) -> Optional["Handler"]: ...


class MainHandler:
    def on_event(self, event: tcod.event.Event) -> Optional[Action]:
        action: Optional[Action] = None

        match event:
            case tcod.event.KeyDown(sym=tcod.event.KeySym.UP):
                action = BumpAction(dx=0, dy=-1)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.DOWN):
                action = BumpAction(dx=0, dy=1)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.LEFT):
                action = BumpAction(dx=-1, dy=0)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.RIGHT):
                action = BumpAction(dx=1, dy=0)
            case tcod.event.Quit():
                action = EscapeAction()

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
