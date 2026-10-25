from dataclasses import dataclass, field, replace
from enum import Enum

from terminal_territories.core.exceptions import InvalidAction


class Terrain(Enum):
    PLAINS = "."
    FOREST = "f"
    HILLS = "h"
    RUINS = "r"
    WATER = "~"


@dataclass(frozen=True)
class GameCell:
    owner: int = 0
    terrain: Terrain = Terrain.PLAINS


Grid = tuple[tuple[GameCell, ...], ...]


def _empty_grid() -> Grid:
    return tuple(tuple(GameCell() for _ in range(12)) for _ in range(8))


class Screens(Enum):
    WELCOME = 1
    MENU = 2
    PLAYING = 3


@dataclass(frozen=True)
class GameState:
    # TODO: Take players and dice roll for who goes first
    turn: int = 1
    screen: Screens = Screens.WELCOME
    grid: Grid = field(default_factory=_empty_grid)


def set_screen(gameState: GameState, screen: Screens) -> GameState:
    return replace(gameState, screen=screen)


def set_cell(gameState: GameState, x: int, y: int, cell: GameCell) -> GameState:
    if not (0 <= y < len(gameState.grid) and 0 <= x < len(gameState.grid[y])):
        raise InvalidAction(f"cell ({x}, {y}) out of bounds")

    row = gameState.grid[y]
    new_row = (*row[:x], cell, *row[x + 1 :])
    new_grid = (*gameState.grid[:y], new_row, *gameState.grid[y + 1 :])
    return replace(gameState, grid=new_grid)


def set_turn(gameState: GameState, id: int):
    return replace(gameState, turn=id)
