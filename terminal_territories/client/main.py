import sys
from time import sleep

import terminal_territories.client.draw as draw
import terminal_territories.client.input as input
import terminal_territories.client.players as players
import terminal_territories.client.state as state


def main():
    input.start_input()
    gameState = state.GameState()
    player_1 = players.Player(id=1, name="alex", letter="a", x=0, y=0)
    player_2 = players.Player(id=2, name="slade", letter="s", x=7, y=11)
    try:
        while True:
            key = input.get_key()
            # TODO: Game loop will baloon needs abstraction
            print(key)
            if key == "q":
                print("goodbye!")
                sys.exit(0)
            if gameState.screen == state.Screens.WELCOME:
                if key == "f":
                    gameState = state.set_screen(gameState, state.Screens.MENU)
                draw.draw_game(draw.get_welcome_screen())
            if gameState.screen == state.Screens.MENU:
                if key == "2":
                    gameState = state.set_screen(gameState, state.Screens.PLAYING)
                draw.draw_game(draw.get_main_menu())
            if gameState.screen == state.Screens.PLAYING:
                # Player 1 controls
                if key == "w":
                    player_1 = players.up(player_1)
                if key == "s":
                    player_1 = players.down(player_1)
                if key == "a":
                    player_1 = players.left(player_1)
                if key == "d":
                    player_1 = players.right(player_1)
                # Player 2 debug for local testing maybe make it the ai eventually
                if key == "i":
                    player_2 = players.up(player_2)
                if key == "k":
                    player_2 = players.down(player_2)
                if key == "j":
                    player_2 = players.left(player_2)
                if key == "l":
                    player_2 = players.right(player_2)
                draw.draw_game(
                    draw.get_grid(gameState.grid, player_1, player_2), show_controls=True
                )
            sleep(0.1)  # 10 FPS
    finally:
        input.stop_input()


if __name__ == "__main__":
    main()
