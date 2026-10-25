import shutil
import sys

# Rich text formatting introduces flicker into ghostty and probably other terminals
# Standard print hasn't shown any flicker yet but will become a problem at some point
# from rich import print
from terminal_territories.core.players import Player
from terminal_territories.core.state import Grid, Terrain


def _get_title_bar():
    return """
*----------------------*
| Terminal Territories |
*----------------------*

    """


def get_welcome_screen():
    return """Press F to continue....

Copyright: Me
    """


def get_main_menu():
    return """Main Menu
1. Join Game
2. Create Game

Press number to enter option
    """


def get_grid(grid: Grid, player_1: Player, player_2: Player) -> str:
    grid_string = ""
    for y, row in enumerate(grid):
        row_string = ""
        for x, cell in enumerate(row):
            # Render Player
            if player_1.x == x and player_1.y == y:
                row_string += str(player_1.id)
            elif player_2.x == x and player_2.y == y:
                row_string += str(player_2.id)
            else:
                # If no player render terrain or owner
                if cell.owner is not None:
                    row_string += cell.owner.letter
                elif cell.terrain == Terrain.PLAINS:
                    row_string += Terrain.PLAINS.value
                    # Index debug
                    # row_string += f"({x}{y}),"

        grid_string += row_string + "\n"
    return grid_string


def _pad_block(s: str, width: int | None = None) -> str:
    if width is None:
        width = shutil.get_terminal_size().columns
    lines = s.split("\n")
    box_w = max((len(line) for line in lines), default=0)
    pad = " " * max(0, (width - box_w) // 2)
    return "\n".join(pad + line for line in lines)


def _draw(ui: str):
    print(_pad_block(ui))


# TODO: Add some styling to text and spacing depending on terminal size
def draw_game(ui: str, player: Player | None = None):
    _clear()
    _draw(_get_title_bar())
    _draw(ui)
    if player is not None:
        _draw(player.controls.value)


def _clear():
    # TODO: Prefer \033[H + padded lines + \033[J (erase below) over \033[H\033[2J every frame. It reduces flicker at 10 FPS. Use the full clear only when changing screens or resizing.
    sys.stdout.write("\033[H\033[J")  # home cursor + erase screen
    sys.stdout.flush()
