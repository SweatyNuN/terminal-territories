import sys
import termios
import tty

ESC = "\x1b"
ALT_SCREEN = f"{ESC}[?1049h"
LEAVE_ALT_SCREEN = f"{ESC}[?1049l"
HIDE_CURSOR = f"{ESC}[?25l"
SHOW_CURSOR = f"{ESC}[?25h"
CLEAR = f"{ESC}[2J{ESC}[H"


def draw(x: int, y: int, width: int, height: int) -> str:
    """Build one complete frame.

    This is the part to replace with your own grid rendering.
    Return the characters exactly as they should appear on screen.
    """
    lines = ["", "  WASD to move, q to quit", ""]
    for row in range(height):
        cells = [" "] * width
        if row == y:
            cells[x] = "@"
        lines.append("".join(cells))

    # In raw mode output processing is off, so a bare "\n" does not return
    # the carriage. Always emit "\r\n" when starting a new line.
    return CLEAR + "\r\n".join(lines)


def main() -> None:
    if not sys.stdin.isatty():
        raise SystemExit("run this from a real terminal")

    width, height = 20, 6
    x = y = 0

    fd = sys.stdin.fileno()
    saved = termios.tcgetattr(fd)
    try:
        # Raw mode: no line buffering, no echo. read(1) returns on each key.
        tty.setraw(fd)
        sys.stdout.write(ALT_SCREEN + HIDE_CURSOR)

        while True:
            sys.stdout.write(draw(x, y, width, height))
            sys.stdout.flush()

            key = sys.stdin.read(1)
            if key == "q":
                break
            if key == "w":
                y = max(0, y - 1)
            elif key == "s":
                y = min(height - 1, y + 1)
            elif key == "a":
                x = max(0, x - 1)
            elif key == "d":
                x = min(width - 1, x + 1)
            # Arrow keys arrive as escape sequences, e.g. "\x1b[A" for up.
            # Read the next two bytes after ESC if you want to support them.
    finally:
        sys.stdout.write(SHOW_CURSOR + LEAVE_ALT_SCREEN)
        sys.stdout.flush()
        termios.tcsetattr(fd, termios.TCSADRAIN, saved)


if __name__ == "__main__":
    main()
