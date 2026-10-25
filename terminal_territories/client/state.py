from dataclasses import dataclass, field, replace
from enum import Enum

Grid = tuple[tuple[str, ...], ...]


def _empty_grid() -> Grid:
    return tuple(tuple("." for _ in range(8)) for _ in range(12))


class Screens(Enum):
    WELCOME = 1
    MENU = 2
    PLAYING = 3


@dataclass(frozen=True)
class GameState:
    screen: Screens = Screens.WELCOME
    grid: Grid = field(default_factory=_empty_grid)


def set_screen(gameState: GameState, screen: Screens) -> GameState:
    return replace(gameState, screen=screen)


def set_cell(gameState: GameState):
    pass
