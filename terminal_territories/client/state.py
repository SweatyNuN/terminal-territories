from dataclasses import dataclass, field, replace
from enum import Enum


class Terrain(Enum):
    PLAINS = "."
    FOREST = "f"
    HILLS = "h"
    RUINS = "r"
    WATER = "~"


@dataclass(frozen=True)
class GameCell:
    terrain: Terrain = Terrain.PLAINS
    owner = None


Grid = tuple[tuple[GameCell, ...], ...]


def _empty_grid() -> Grid:
    return tuple(tuple(GameCell() for _ in range(12)) for _ in range(8))


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
