import sys, tty, termios, select

_fd = sys.stdin.fileno()
_old_settings = termios.tcgetattr(_fd)

def start_input():
    tty.setcbreak(_fd)

def stop_input():
    termios.tcsetattr(_fd, termios.TCSADRAIN, _old_settings)

def get_key():
    if select.select([sys.stdin], [], [], 0)[0]:
        ch = sys.stdin.read(1)
        if ch == "\x1b":  # ESC — probably an arrow key sequence
            seq = sys.stdin.read(2) if select.select([sys.stdin], [], [], 0.01)[0] else ""
            return {"[A": "UP", "[B": "DOWN", "[C": "RIGHT", "[D": "LEFT"}.get(seq, "ESC")
        return ch
    return None
