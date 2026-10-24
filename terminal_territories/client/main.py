from time import sleep

from terminal_territories.client.input import get_key, start_input, stop_input
from terminal_territories.client.draw import draw_grid, main_menu, welcome_screen, clear
from terminal_territories.client.state import GameState

def main():
    start_input()
    last_key = None
    gameState = GameState()
    try:
        while True:
            key = get_key()
            if key is not None:
                last_key = key
            if key == "e":
                gameState.welcome_screen = True
                gameState.main_menu = True
            if key == "2":
                gameState.main_menu = False
                gameState.playing = True
            clear()
            if gameState.welcome_screen is False:
                welcome_screen()
            if gameState.main_menu is True:
                main_menu()
            if gameState.playing is True:
                draw_grid(gameState.grid)
            sleep(0.1) # 10 FPS
    finally:
        stop_input()


if __name__ == "__main__":
    main()
