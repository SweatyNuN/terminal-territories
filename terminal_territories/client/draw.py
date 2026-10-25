import sys

# Rich text formatting introduces flicker into ghostty and probably other terminals
# Standard print hasn't shown any flicker yet but will become a problem at some point
# from rich import print
from terminal_territories.client.players import Player
from terminal_territories.client.state import Grid, Terrain


def get_welcome_screen():
    return """
Terminal Territories
Press F to continue....
    """


def get_main_menu():
    return """
Main Menu
1. Join Game
2. Create Game

Press number to enter option
    """


def get_controls():
    return """
\n
q = quit
w = up
s = down
a = left
d = right
    """


def get_grid(grid: Grid, player: Player):
    grid_string = ""
    for x, row in enumerate(grid):
        row_string = ""
        for y, cell in enumerate(row):
            # Render Player
            if player.x == x and player.y == y:
                row_string += player.letter
            else:
                # If no player render terrain
                if cell.terrain == Terrain.PLAINS:
                    row_string += Terrain.PLAINS.value
                    # Index debug
                    # row_string += f"({x}{y}),"

        grid_string += row_string + "\n"
    return grid_string


# TODO: Add some styling to text and spacing depending on terminal size
def draw_game(ui: str, show_controls: bool = False):
    print(ui)
    if show_controls is True:
        print(get_controls())


def clear():
    # TODO: Prefer \033[H + padded lines + \033[J (erase below) over \033[H\033[2J every frame. It reduces flicker at 10 FPS. Use the full clear only when changing screens or resizing.
    sys.stdout.write("\033[H\033[2J")  # home cursor + erase screen
    sys.stdout.flush()
