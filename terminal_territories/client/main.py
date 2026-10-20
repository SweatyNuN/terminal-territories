"""A minimal Textual app: move a marker around a grid with a button."""

from typing import Any

from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Footer, Header, Static


class GridView(Static):
    """Render a grid and a single player marker."""

    def __init__(
        self,
        grid_width: int = 8,
        grid_height: int = 5,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.player_x = 0
        self.player_y = 0

    def move_player(self) -> None:
        """Move the marker one cell right, wrapping to the next row."""
        self.player_x += 1
        if self.player_x >= self.grid_width:
            self.player_x = 0
            self.player_y = (self.player_y + 1) % self.grid_height
        self.refresh()

    def render(self) -> Text:
        rows: list[str] = []
        for y in range(self.grid_height):
            cells = [
                "@" if (x, y) == (self.player_x, self.player_y) else "."
                for x in range(self.grid_width)
            ]
            rows.append(" ".join(cells))
        return Text("\n".join(rows))


class GridApp(App):
    """The application shell: a grid and a button that moves the marker."""

    CSS = """
    Screen {
        align: center middle;
    }

    #board {
        width: auto;
        height: auto;
        align: center middle;
    }

    #grid {
        width: auto;
        height: auto;
        padding: 1 2;
        border: round $primary;
    }

    #move {
        width: 16;
        margin-top: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="board"):
            yield GridView(id="grid")
            yield Button("Move", id="move", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "move":
            self.query_one(GridView).move_player()


def main() -> None:
    GridApp().run()


if __name__ == "__main__":
    main()
