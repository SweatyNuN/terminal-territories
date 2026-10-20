"""Tests for the grid starter app."""

from terminal_territories.client.main import GridApp, GridView


def test_render_marks_the_player_position() -> None:
    grid = GridView(grid_width=4, grid_height=3)
    grid.player_x = 2
    grid.player_y = 1

    lines = grid.render().plain.splitlines()

    assert lines == [
        ". . . .",
        ". . @ .",
        ". . . .",
    ]


async def test_move_button_moves_the_marker() -> None:
    app = GridApp()

    async with app.run_test() as pilot:
        grid = app.query_one(GridView)
        assert (grid.player_x, grid.player_y) == (0, 0)

        await pilot.click("#move")

        assert (grid.player_x, grid.player_y) == (1, 0)


async def test_marker_wraps_to_the_start_after_the_last_cell() -> None:
    app = GridApp()

    async with app.run_test() as pilot:
        grid = app.query_one(GridView)
        for _ in range(grid.grid_width * grid.grid_height - 1):
            grid.move_player()
        assert (grid.player_x, grid.player_y) == (
            grid.grid_width - 1,
            grid.grid_height - 1,
        )

        await pilot.click("#move")

        assert (grid.player_x, grid.player_y) == (0, 0)
