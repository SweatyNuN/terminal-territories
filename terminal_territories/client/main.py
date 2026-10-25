import sys
from time import sleep

import terminal_territories.client.draw as draw
import terminal_territories.client.input as input
import terminal_territories.client.players as players
import terminal_territories.client.state as state


def main():
    input.start_input()
    gameState = state.GameState()
    player_1 = players.Player(name="alex", letter="a", x=0, y=0)
    try:
        while True:
            key = input.get_key()
            # TODO: Game loop will baloon needs abstraction
            if key == "f":
                gameState = state.set_screen(gameState, state.Screens.MENU)
            if key == "2":
                gameState = state.set_screen(gameState, state.Screens.PLAYING)
            if key == "w":
                player_1 = players.up(player_1)
            if key == "s":
                player_1 = players.down(player_1)
            if key == "a":
                player_1 = players.left(player_1)
            if key == "d":
                player_1 = players.right(player_1)
            if key == "q":
                print("goodbye!")
                sys.exit(0)
            draw.clear()
            if gameState.screen == state.Screens.WELCOME:
                draw.draw_game(draw.get_welcome_screen())
            if gameState.screen == state.Screens.MENU:
                draw.draw_game(draw.get_main_menu())
            if gameState.screen == state.Screens.PLAYING:
                draw.draw_game(draw.get_grid(gameState.grid, player_1), show_controls=True)
            sleep(0.1)  # 10 FPS
    finally:
        input.stop_input()


if __name__ == "__main__":
    main()
