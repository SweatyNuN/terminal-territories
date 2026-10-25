from dataclasses import dataclass, replace
from enum import Enum


class Actions(Enum):
    MOVE = 0
    EXPAND = 1
    ATTACK = 2
    FORTIFY = 3


class Controls(Enum):
    MOVE = "[Q]uit, [E]xpand, [A]ttack, [F]ortify, IJKL = Move Directions"
    COLONISE = "[Q]uit, [M]ove, IJKL = Expand/Attack/Fortify Direction"


@dataclass(frozen=True)
class Player:
    id: int
    name: str
    letter: str
    x: int
    y: int
    action: Actions = Actions.MOVE
    controls: Controls = Controls.MOVE


def up(player: Player) -> Player:
    if player.y > 0 and player.y <= 7:
        return replace(player, y=player.y - 1)
    return player


def down(player: Player) -> Player:
    if player.y >= 0 and player.y < 7:
        return replace(player, y=player.y + 1)
    return player


def left(player: Player) -> Player:
    if player.x > 0 and player.x <= 11:
        return replace(player, x=player.x - 1)
    return player


def right(player: Player) -> Player:
    if player.x >= 0 and player.x < 11:
        return replace(player, x=player.x + 1)
    return player


def set_action(player: Player, action: Actions) -> Player:
    controls = Controls.COLONISE
    if action == Actions.MOVE:
        controls = Controls.MOVE

    return replace(player, action=action, controls=controls)
