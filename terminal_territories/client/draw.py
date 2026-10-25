import sys

from terminal_territories.client.state import Grid


def get_welcome_screen():
    return """
Terminal Territories
Press E to continue....
    """


def get_main_menu():
    return """
Main Menu
1. Join Game
2. Create Game
    """


def get_grid(grid: Grid):
    grid_string = ""
    for row in grid:
        row_string = ""
        for cell in row:
            row_string += cell
        grid_string += row_string + "\n"
    return grid_string


def draw_game(ui: str):
    print(ui)


def clear():
    sys.stdout.write("\033[H\033[2J")  # home cursor + erase screen
    sys.stdout.flush()
