from time import sleep

import terminal_territories.client.draw as draw
import terminal_territories.client.input as input
import terminal_territories.client.state as state


def main():
    input.start_input()
    gameState = state.GameState()
    try:
        while True:
            key = input.get_key()
            if key == "e":
                gameState = state.set_screen(gameState, state.Screens.MENU)
            if key == "2":
                gameState = state.set_screen(gameState, state.Screens.PLAYING)
            draw.clear()
            if gameState.screen == state.Screens.WELCOME:
                draw.draw_game(draw.get_welcome_screen())
            if gameState.screen == state.Screens.MENU:
                draw.draw_game(draw.get_main_menu())
            if gameState.screen == state.Screens.PLAYING:
                draw.draw_game(draw.get_grid(gameState.grid))
            sleep(0.1)  # 10 FPS
    finally:
        input.stop_input()


if __name__ == "__main__":
    main()
