import sys
from time import sleep

import terminal_territories.client.draw as draw
import terminal_territories.client.input as input
import terminal_territories.core.players as players
import terminal_territories.core.state as state


def main():
    input.start_input()
    gameState = state.GameState()
    player = players.Player(id=1, name="alex", letter="a", x=0, y=0)
    player2 = players.Player(id=2, name="slade", letter="s", x=7, y=11)
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
                # Player 1 controls, turn consuming
                if player.action is players.Actions.MOVE:
                    if key == "i":
                        player = players.up(player)
                    if key == "k":
                        player = players.down(player)
                    if key == "j":
                        player = players.left(player)
                    if key == "l":
                        player = players.right(player)
                    # Player 1 contextual controls
                    if key == "e":
                        player = players.set_action(player, players.Actions.EXPAND)
                    if key == "a":
                        player = players.set_action(player, players.Actions.ATTACK)
                    if key == "f":
                        player = players.set_action(player, players.Actions.FORTIFY)
                else:
                    if key == "m":
                        player = players.set_action(player, players.Actions.MOVE)

                # Player 2 debug for local testing maybe make it the ai eventually
                draw.draw_game(draw.get_grid(gameState.grid, player, player2), player)
            sleep(0.1)  # 10 FPS
    finally:
        input.stop_input()


if __name__ == "__main__":
    main()
