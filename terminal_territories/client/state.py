class GameState:
    def __init__(self):
      self.welcome_screen = False
      self.main_menu = False
      self.playing = False
      self.grid = [["e"*10]*20]
