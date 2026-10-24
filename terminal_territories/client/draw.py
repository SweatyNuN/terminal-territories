import sys

def welcome_screen():
    print("Terminal Territories")
    print("Press E to continue....")

def main_menu():
    print("Main Menu")
    print("1. Join Game")
    print("2. Create Game")


def draw_grid(grid):
    for row in grid:
        for cell in row:
            print(cell)
        print("\n")

def clear():
    sys.stdout.write("\033[H\033[2J")  # home cursor + erase screen
    sys.stdout.flush()
